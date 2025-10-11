# MCP Base64 Server

Python MCP stdio server that provides tools to encode files to Base64 and decode Base64 payloads back to disk.

## Installation

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -e .[dev]
```

## Running the Server

```bash
PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server
```

### JSON-RPC Example

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cli","version":"0.0.0"}}}\n' | \
PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server
printf '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}\n' | \
PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server
```

## Tools

| Name | Description | Parameters |
| --- | --- | --- |
| `encode_file_to_base64` | Encode the file at an absolute path to a Base64 string. | `file_path` – absolute path to the source file |
| `decode_base64_to_file` | Decode a Base64 payload into a target file. | `base64_content` – Base64 string; `file_path` – absolute path where bytes are written |

## Development

```bash
./.venv/bin/ruff check .
./.venv/bin/python -m pytest -q
```

## FAQ / TODO

- Ensure absolute paths when calling tools; relative paths are rejected.
- Future improvement: optional overwrite controls for `decode_base64_to_file`.
