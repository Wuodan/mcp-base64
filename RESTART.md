## Summary
- Python MCP stdio server offering Base64 encode/decode file tools using official `mcp` SDK.
- Primary module `src/mcp_base64/server.py`; tests under `tests/`.
- Packaging managed by `pyproject.toml`; no global state.

## Key Decisions & Assumptions
- Use official `mcp` Python SDK with stdio transport.
- Require absolute file paths for all file interactions; reject non-absolute or directory traversal.
- Persist artifacts for verification logs under `artifacts/`.

## Commands
- Install deps: `./.venv/bin/python -m pip install -e .[dev]`
- Run server (stdio): `PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server`
- Smoke initialize: `printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n' | PYTHONPATH=src ./.venv/bin/python -m mcp_base64.server`
- Unit tests: `./.venv/bin/python -m pytest -q`
- Lint: `./.venv/bin/ruff check .`
- Integration (round-trip) test executed via pytest suite `tests/test_tools.py::test_stdio_round_trip`.

## File Map
- `pyproject.toml` – project metadata, deps, tooling config.
- `src/mcp_base64/__init__.py` – package export.
- `src/mcp_base64/server.py` – MCP stdio server implementation (encode/decode tools).
- `tests/test_tools.py` – unit & integration tests.
- `artifacts/` – lint/test logs (`lint.log`, `unit-test.log`, `integration-test.log`).
- `.github/workflows/ci.yml` – CI pipeline (Python 3.11 running lint/tests).
- `README.md` – usage, install, JSON-RPC example, TODO/FAQ.

## Dependencies
- Runtime: `mcp`, `pydantic`.
- Dev/test: `pytest`, `pytest-asyncio`, `ruff`.

## Environment Variables
- None required.

## Tools API Contract
- `encode_file_to_base64(file_path: str) -> str`
  - Params: absolute file path to existing file. Returns Base64 string.
- `decode_base64_to_file(base64_content: str, file_path: str) -> str`
  - Params: Base64 payload and absolute target file path. Returns resolved file path string.
- Errors: raise `ToolError` with concise message on validation or I/O failure.

## Test Plan & Acceptance
- Unit tests: encoder handles binary/text, rejects non-absolute paths, decode round-trip.
- Integration: spawn stdio server, initialize, invoke both tools on sample binary and confirm byte equality plus parameter metadata presence.
- Acceptance: 3 verification commands succeed; logs stored without errors or warnings.

## TODO / Next Steps
- Implement server tools and validation helpers.
- Write tests (unit + async integration).
- Author README and CI workflow.
- Run lint/tests; capture logs in `artifacts/`.
- Ensure parameter descriptions visible in tool schema.

## Resume Instructions
- Install dependencies via pip editable mode with `[dev]` extras.
- Review `server.py` for tool implementations.
- Run tests and lint commands before development continues.
