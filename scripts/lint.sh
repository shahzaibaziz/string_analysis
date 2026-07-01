#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "${STRING_ANALYSIS_USE_PATH:-}" != "1" ] && [ -x "$ROOT_DIR/.venv/bin/ruff" ]; then
  RUFF="$ROOT_DIR/.venv/bin/ruff"
else
  RUFF="ruff"
fi

cd "$ROOT_DIR"

echo "Running linter..."
"$RUFF" check app tests
