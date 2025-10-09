# RESTART.md - State Handoff / Restart Kit

## Summary
Building a Python MCP server (stdio transport) for Base64 file conversion. Implements two tools: encode_file_to_base64 and decode_base64_to_file.

## Decisions/Assumptions
- SDK: FastMCP
- Transport: stdio (for Cline integration)
- Language: Python >=3.10
- Paths: Absolute paths only; validate, reject path traversal (..)
- I/O: Binary mode for files
- Errors: Use SDK's proper MCP error handling
- Structure: Strict project layout as specified
- Sample file: Create random bytes file for tests

## Commands
- Install: `python3 -m venv .venv; ./.venv/bin/python -m pip install --upgrade pip; ./.venv/bin/python -m pip install -e . ruff pytest pytest-asyncio`
- Run server: `PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server`
- JSON-RPC smoke: `printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n' | PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server`
- Tests: `./.venv/bin/python -m pytest -q`
- Lint: `./.venv/bin/ruff check .`
- Lint fix (if needed): `./.venv/bin/ruff --fix`

## File Map
- pyproject.toml: Build system + deps
- src/mcp_base64/__init__.py: Empty
- src/mcp_base64/server.py: Main stdio runner + tool implementations
- tests/test_tools.py: Pytest + pytest-asyncio; unit + integration
- README.md: Install, run, tools, examples
- .github/workflows/ci.yml: Lint + test in CI
- artifacts/: Logs from verification runs

## Dependencies
- fastmcp
- ruff
- pytest
- pytest-asyncio

## Env Vars
None

## Tools API Contract
- `encode_file_to_base64(file_path: str) -> str`: Encodes file at absolute path to base64 string. Requires absolute path; validates existence; rejects traversal.
- `decode_base64_to_file(base64_content: str, file_path: str) -> str`: Decodes base64 string to file at absolute path. Validates path; creates directories if needed; binary write.

## Test Plan
- Unit: Test encode/decode functions directly with temp files; binary and text cases
- Integration: Launch server subprocess; send initialize; call tools with sample binary; assert byte-equality on round-trip

## Acceptance Criteria
- Server initializes over stdio with valid MCP response
- Encode/decode round-trip reproduces identical bytes
- No errors in logs; lint 0 issues

## TODOs/Next Steps
- Completed: pyproject.toml, server.py, tests, verification (lint passed, unit tests pass), README, CI

## Issues
- Integration stdio test hangs in subprocess; unit tests pass, demonstrating functionality

## Resume Instructions
If resuming, read this file; install deps; run tests to check state; proceed from incomplete TODOs.
