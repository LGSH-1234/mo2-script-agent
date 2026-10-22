#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
MO2_PYTHON="${MO2_PYTHON:-python3}"
if [ ! -x .venv/bin/python ]; then
  "$MO2_PYTHON" -m venv .venv
fi
if ! .venv/bin/python -c 'import fastapi, uvicorn, aigc_agent, dotenv, multipart, pypdf, striprtf' >/dev/null 2>&1; then
  .venv/bin/python -m pip install -r requirements-demo.lock
  .venv/bin/python -m pip install --no-deps -e .
fi
if [ ! -f web/dist/index.html ]; then
  printf '%s\n' '缺少前端构建产物，请在 web 目录执行 npm ci && npm run build。'
  exit 1
fi
printf '%s\n' '打开 http://127.0.0.1:8766；按 Ctrl+C 停止。'
exec .venv/bin/python -m uvicorn web_app.app:app --host 127.0.0.1 --port 8766
