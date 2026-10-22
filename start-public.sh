#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
MO2_PYTHON="${MO2_PYTHON:-python3}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8766}"
if [ ! -x .venv/bin/python ]; then
  "$MO2_PYTHON" -m venv .venv
fi
if ! .venv/bin/python -c 'import fastapi, uvicorn, aigc_agent, dotenv, multipart, pypdf, striprtf' >/dev/null 2>&1; then
  .venv/bin/python -m pip install -r requirements-demo.lock
  .venv/bin/python -m pip install --no-deps -e .
fi
if [ ! -f web/dist/index.html ]; then
  printf '%s\n' '缺少前端构建产物 web/dist，请先 npm ci && npm run build。'
  exit 1
fi
printf '%s\n' "Listening on http://${HOST}:${PORT}"
exec .venv/bin/python -m uvicorn web_app.app:app --host "$HOST" --port "$PORT"
