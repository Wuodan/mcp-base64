from __future__ import annotations

import asyncio
import json
import os
import sys
from base64 import b64decode
from pathlib import Path
from typing import Any

import pytest
from mcp.shared.exceptions import McpError

from mcp_base64 import server


@pytest.mark.asyncio
async def test_encode_decode_round_trip(tmp_path: Path) -> None:
    source = tmp_path / "sample.bin"
    source.write_bytes(os.urandom(32))

    encoded = await server.encode_file_to_base64(str(source))
    assert isinstance(encoded, str)
    assert b64decode(encoded) == source.read_bytes()

    target = tmp_path / "restored.bin"
    written_path = await server.decode_base64_to_file(encoded, str(target))
    assert written_path == str(target.resolve())
    assert target.read_bytes() == source.read_bytes()


@pytest.mark.asyncio
async def test_encode_requires_absolute_path(tmp_path: Path) -> None:
    relative = Path("not_absolute.txt")
    file = tmp_path / "file.txt"
    file.write_text("content")
    with pytest.raises(McpError):
        await server.encode_file_to_base64(str(relative))


@pytest.mark.asyncio
async def test_decode_rejects_invalid_base64(tmp_path: Path) -> None:
    dest = tmp_path / "out.bin"
    with pytest.raises(McpError):
        await server.decode_base64_to_file("***", str(dest))


@pytest.mark.asyncio
async def test_stdio_round_trip(tmp_path: Path) -> None:
    binary_path = tmp_path / "binary.dat"
    payload = os.urandom(48)
    binary_path.write_bytes(payload)

    env = os.environ.copy()
    src_root = Path(__file__).resolve().parents[1] / "src"
    env["PYTHONPATH"] = f"{src_root}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)

    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "mcp_base64.server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    assert proc.stdin is not None
    assert proc.stdout is not None

    async def send(message: dict[str, Any], *, expect_response: bool = True) -> dict[str, Any]:
        proc.stdin.write(json.dumps(message).encode("utf-8") + b"\n")
        await proc.stdin.drain()
        if not expect_response:
            return {}
        while True:
            line = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
            if not line:
                stderr_output = await proc.stderr.read()
                raise AssertionError(f"Server terminated unexpectedly: {stderr_output!r}")
            decoded = json.loads(line.decode("utf-8"))
            if "id" in decoded and decoded.get("id") == message.get("id"):
                return decoded

    init_response = await send(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "0.0.0"},
            },
        }
    )
    assert init_response.get("result") is not None

    await send(
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        expect_response=False,
    )

    tools_response = await send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tools = tools_response.get("result", {}).get("tools", [])
    assert tools, "Expected tools in list response"
    encode_tool = next(tool for tool in tools if tool["name"] == "encode_file_to_base64")
    decode_tool = next(tool for tool in tools if tool["name"] == "decode_base64_to_file")
    encode_schema = encode_tool.get("inputSchema", {}).get("properties", {})
    decode_schema = decode_tool.get("inputSchema", {}).get("properties", {})
    assert encode_schema.get("file_path", {}).get("description")
    assert decode_schema.get("file_path", {}).get("description")
    assert decode_schema.get("base64_content", {}).get("description")

    encode_call = await send(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "encode_file_to_base64",
                "arguments": {"file_path": str(binary_path.resolve())},
            },
        }
    )
    encoded_text = encode_call.get("result", {}).get("content", [{}])[0].get("text")
    assert encoded_text
    assert b64decode(encoded_text) == payload

    restored_path = tmp_path / "restored.dat"
    decode_call = await send(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "decode_base64_to_file",
                "arguments": {
                    "base64_content": encoded_text,
                    "file_path": str(restored_path.resolve()),
                },
            },
        }
    )
    decoded_text = decode_call.get("result", {}).get("content", [{}])[0].get("text")
    assert decoded_text == str(restored_path.resolve())
    assert restored_path.read_bytes() == payload

    proc.stdin.close()
    try:
        await asyncio.wait_for(proc.wait(), timeout=5)
    finally:
        if proc.returncode is None:
            proc.kill()
