import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
import base64
import random

from src.mcp_base64.utils import encode_file_to_base64, decode_base64_to_file


@pytest.fixture
def sample_text_file(tmp_path):
    text_file = tmp_path / "sample.txt"
    content = "Hello, World! This is a test file."
    text_file.write_text(content, encoding="utf-8")
    return text_file


@pytest.fixture
def sample_binary_file(tmp_path):
    binary_file = tmp_path / "sample.bin"
    content = bytes(random.getrandbits(8) for _ in range(256))  # Random 256 bytes
    binary_file.write_bytes(content)
    return binary_file


def test_encode_text_file(sample_text_file):
    abs_path = str(sample_text_file.resolve())
    result = encode_file_to_base64(file_path=abs_path)
    decoded = base64.b64decode(result.encode("ascii"))
    assert decoded == sample_text_file.read_bytes()


def test_encode_binary_file(sample_binary_file):
    abs_path = str(sample_binary_file.resolve())
    result = encode_file_to_base64(file_path=abs_path)
    decoded = base64.b64decode(result.encode("ascii"))
    assert decoded == sample_binary_file.read_bytes()


def test_decode_to_file(tmp_path):
    # Create base64 from random bytes
    original_data = bytes(random.getrandbits(8) for _ in range(128))
    base64_str = base64.b64encode(original_data).decode("ascii")
    output_file = tmp_path / "output.bin"
    abs_path = str(output_file.resolve())

    decode_base64_to_file(base64_content=base64_str, file_path=abs_path)
    assert output_file.exists()
    assert output_file.read_bytes() == original_data


def test_integration_round_trip(sample_binary_file, tmp_path):
    abs_path = str(sample_binary_file.resolve())
    output_file = tmp_path / "roundtrip.bin"
    abs_output = str(output_file.resolve())

    # Call the functions directly to simulate MCP flow
    base64_str = encode_file_to_base64(file_path=abs_path)
    decode_base64_to_file(base64_content=base64_str, file_path=abs_output)

    # Assert
    original = sample_binary_file.read_bytes()
    decoded = output_file.read_bytes()
    assert decoded == original


def test_integration_stdio(sample_binary_file, tmp_path):
    # Create the server as subprocess
    cmd = [sys.executable, "-m", "src.mcp_base64.server"]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    def send_request(req):
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()
        response = ""
        line = proc.stdout.readline()
        response += line
        # Read until complete JSON
        try:
            resp = json.loads(response.strip())
            return resp
        except json.JSONDecodeError:
            # Read more lines if needed, but for simplicity assume one line
            return json.loads(line.strip())

    try:
        # Initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "0.1.0"}
            }
        }
        resp = send_request(init_req)
        assert resp["id"] == 1
        assert "result" in resp

        # Send initialized notification
        init_notify = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        send_request(init_notify)  # Notification, no response expected

        # List tools (to check tools are exposed)
        list_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        resp = send_request(list_req)
        assert resp["id"] == 2
        tools = resp["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert "encode_file_to_base64" in tool_names
        assert "decode_base64_to_file" in tool_names

        # Encode the sample file
        abs_path = str(sample_binary_file.resolve())
        encode_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "encode_file_to_base64",
                "arguments": {"file_path": abs_path}
            }
        }
        resp = send_request(encode_req)
        assert resp["id"] == 3
        base64_str = resp["result"]["content"][0]["text"]

        # Decode to temp file
        output_file = tmp_path / "integration_out.bin"
        abs_output = str(output_file.resolve())
        decode_req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "decode_base64_to_file",
                "arguments": {"base64_content": base64_str, "file_path": abs_output}
            }
        }
        resp = send_request(decode_req)
        assert resp["id"] == 4

        # Assert roundtrip
        original = sample_binary_file.read_bytes()
        decoded = output_file.read_bytes()
        assert decoded == original

    finally:
        proc.terminate()
        proc.wait()
        stderr = proc.stderr.read()
        if stderr:
            pytest.fail(f"Server stderr: {stderr}")
