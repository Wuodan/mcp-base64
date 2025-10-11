# MCP Base64 Server

Python MCP stdio server that provides tools to encode files to Base64 and decode Base64 payloads back to disk.

## Installation on Your PC

```bash
git clone https://github.com/factory/mcp-base64.git
cd mcp-base64
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -e .[dev]
```

Record the absolute path to the virtual environment’s Python interpreter (for example `/path/to/mcp-base64/.venv/bin/python`). The IDE plugin will call this interpreter in stdio mode.

## IDE Plugin Configuration

Most MCP-enabled IDE plugins accept a JSON configuration that specifies the stdio command. Adapt the template below to your environment. Replace the paths with the absolute locations on your machine.

```json
{
  "name": "Base64 Converter",
  "command": "/path/to/mcp-base64/.venv/bin/python",
  "args": ["-m", "mcp_base64.server"],
  "metadata": {
    "description": "Encode and decode files with Base64"
  }
}
```

No additional environment variables are required when installed in editable mode.

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
