#!/usr/bin/env bash
# Run the BadWordsChecker CLI from anywhere in the project
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PY="$SCRIPT_DIR/venv/bin/python3"
if [ ! -x "$VENV_PY" ]; then
  echo "Python venv not found. Please run: make install" >&2
  exit 1
fi
# Ensure Python can find the badwordschecker package
export PYTHONPATH="$SCRIPT_DIR"
exec "$VENV_PY" -m badwordschecker.cli "$@"
