#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "${STRING_ANALYSIS_USE_PATH:-}" != "1" ] && [ -x "$ROOT_DIR/.venv/bin/pytest" ]; then
  PYTEST="$ROOT_DIR/.venv/bin/pytest"
else
  PYTEST="pytest"
fi

cd "$ROOT_DIR"

echo "Running unit tests..."
"$PYTEST" -v
