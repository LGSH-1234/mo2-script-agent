FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOST=0.0.0.0 PORT=8766
COPY requirements-demo.lock pyproject.toml ./
COPY src ./src
COPY web_app ./web_app
COPY web/dist ./web/dist
COPY web/public ./web/public
COPY runtime-skills ./runtime-skills
COPY web-skills ./web-skills
COPY config ./config
COPY skills ./skills
COPY start-public.sh ./
RUN pip install --no-cache-dir -r requirements-demo.lock \
 && pip install --no-cache-dir --no-deps -e . \
 && chmod +x start-public.sh
EXPOSE 8766
CMD ["bash", "-lc", "exec python -m uvicorn web_app.app:app --host 0.0.0.0 --port ${PORT:-8766}"]
