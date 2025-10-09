# MCP Base64 Server

A Python MCP server (stdio transport) for Base64 file conversion.

## Installation

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -e . ruff pytest pytest-asyncio
```

## Running the Server

```bash
PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server
```

For testing:
```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1.0"}}}\n' | PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server
```

## Tools

| Tool | Description |
|------|-------------|
| encode_file_to_base64 | Encodes the file at the given absolute path to a base64 string. Requires absolute path; validates existence; rejects path traversal. |
| decode_base64_to_file | Decodes the base64 string to a file at the given absolute path. Validates path; creates directories if needed; binary write. |

## Usage Examples

JSON-RPC example to encode a file:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "encode_file_to_base64",
    "arguments": {"file_path": "/absolute/path/to/file"}
  }
}
```

To decode:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "decode_base64_to_file",
    "arguments": {"base64_content": "SGVsbG8gV29ybGQ=", "file_path": "/path/to/output"}
  }
}
```

## IDE Configuration

To use this MCP server in Cline or another IDE, add the following to your MCP settings JSON (e.g., `~/.cline/data/settings/cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "mcp-base64": {
      "type": "stdio",
      "command": "/path/to/.venv/bin/python",
      "args": ["-m", "mcp_base64.server"],
      "env": {
        "PYTHONPATH": "/path/to/src"
      }
    }
  }
}
```

Replace `/path/to/` with the actual path to the project directory.

## FAQ/TODO

- Only absolute paths allowed
- Paths with ".." are rejected
- Binary I/O is used for files

License: MIT
