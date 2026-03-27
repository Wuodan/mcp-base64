#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

uv run yamllint .
uv run pymarkdown \
  --config .pymarkdown.json scan \
  --exclude '**/.venv*/**' \
  README.md
uv run ruff check .
uv run pyright .
