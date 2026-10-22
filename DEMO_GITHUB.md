# MO² Episode Agent DEMO（可分享）

本仓库包含可本地/容器运行的 **Episode Agent Web DEMO**（FastAPI + 已构建前端）。

## 最快启动

```bash
# 需要 Python 3.11+；前端产物已在 web/dist
cp .env.example .env   # 按需填入密钥；无密钥也可先看壳与静态流程
./start-public.sh
# 浏览器打开 http://127.0.0.1:8766/storyboard
```

同源代理路径：`/demo-proxy/`（与壳嵌入一致）。

## Docker

```bash
docker build -t mo2-demo .
docker run --rm -p 8766:8766 --env-file .env mo2-demo
```

## 说明

- 不要提交 `.env`（已在 `.gitignore`）。
- GitHub Pages **无法**直接跑本仓库的 FastAPI 后端；请用本机/`start-public.sh` 或 Docker，或自行接到任意支持容器的托管。
- Origin 同源仓：`yvla8585/mo2-script-agent`（Cursor Origin）。
