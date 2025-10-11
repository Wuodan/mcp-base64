"""MCP stdio server exposing Base64 file conversion tools."""

from __future__ import annotations

import asyncio
import base64
import binascii
from pathlib import Path
from typing import Annotated, Any, Awaitable, Callable

from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    CallToolResult,
    ErrorData,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)
from pydantic import BaseModel, Field

server = Server("mcp-base64")


class EncodeParams(BaseModel):
    """Input schema for encode_file_to_base64."""

    file_path: Annotated[str, Field(description="Absolute path of the file to encode.")]


class DecodeParams(BaseModel):
    """Input schema for decode_base64_to_file."""

    base64_content: Annotated[str, Field(description="Base64 content to decode.")]
    file_path: Annotated[str, Field(description="Absolute destination file path.")]


def _tool_error(message: str, *, code: int = 400) -> McpError:
    raise McpError(ErrorData(code=code, message=message))


def _require_absolute_file(path_str: str) -> Path:
    path = Path(path_str)
    if not path.is_absolute():
        _tool_error("Expected absolute file path.")
    try:
        resolved = path.resolve(strict=False)
    except OSError as exc:  # pragma: no cover - Path.resolve handles errors variably per OS
        _tool_error(str(exc), code=500)
    return resolved


async def encode_file_to_base64(file_path: str) -> str:
    """Encode the file at the given absolute path to a Base64 string."""

    path = _require_absolute_file(file_path)
    if not path.exists() or not path.is_file():
        _tool_error("Source file does not exist.", code=404)
    try:
        data = path.read_bytes()
    except OSError as exc:
        _tool_error(str(exc), code=500)
    return base64.b64encode(data).decode("ascii")


async def decode_base64_to_file(base64_content: str, file_path: str) -> str:
    """Decode Base64 content into the target file and return the written path."""

    path = _require_absolute_file(file_path)
    if path.exists() and path.is_dir():
        _tool_error("Destination path is a directory.")
    try:
        raw = base64.b64decode(base64_content, validate=True)
    except (ValueError, binascii.Error):
        _tool_error("Invalid Base64 content.")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    except OSError as exc:
        _tool_error(str(exc), code=500)
    return str(path)


def _tool_definitions() -> list[Tool]:
    return [
        Tool(
            name="encode_file_to_base64",
            description="Encode a file to Base64 text.",
            inputSchema=EncodeParams.model_json_schema(),
        ),
        Tool(
            name="decode_base64_to_file",
            description="Decode Base64 text into a file.",
            inputSchema=DecodeParams.model_json_schema(),
        ),
    ]


@server.list_tools()
async def list_tools(_: ListToolsRequest) -> ListToolsResult:
    """Return available tools."""

    return ListToolsResult(tools=_tool_definitions())


async def _handle_encode(arguments: dict[str, Any] | None) -> str:
    params = EncodeParams.model_validate(arguments or {})
    return await encode_file_to_base64(**params.model_dump())


async def _handle_decode(arguments: dict[str, Any] | None) -> str:
    params = DecodeParams.model_validate(arguments or {})
    return await decode_base64_to_file(**params.model_dump())


_TOOL_HANDLERS: dict[str, Callable[[dict[str, Any] | None], Awaitable[str]]] = {
    "encode_file_to_base64": _handle_encode,
    "decode_base64_to_file": _handle_decode,
}


@server.call_tool()
async def call_tool(
    name: str,
    arguments: dict[str, Any] | None,
) -> list[TextContent] | CallToolResult:
    """Dispatch tool requests to their handlers."""

    handler = _TOOL_HANDLERS.get(name)
    if handler is None:
        _tool_error(f"Unknown tool: {name}", code=404)

    result = await handler(arguments)
    return [TextContent(type="text", text=str(result))]


async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(notification_options=NotificationOptions()),
        )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
