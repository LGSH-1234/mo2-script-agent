# MO² 脚本分镜 Agent DEMO（可分享）

本仓库包含可本地/容器运行的 **脚本分镜 Agent Web DEMO**（FastAPI + 已构建前端）。

## 最快启动

```bash
# 需要 Python 3.11+；前端产物已在 web/dist
cp .env.example .env   # 按需填入密钥；无密钥也可进欢迎页走导入直出（路径 B）
./start-public.sh
# 浏览器打开（务必进 storyboard，不要只开根路径）
# http://127.0.0.1:8766/storyboard
```

打开地址：**http://127.0.0.1:8766/storyboard**

无密钥时：可进欢迎页，主路径只走 **导入脚本 →「开始写分镜」**（路径 B）；模型相关步骤会给出可读错误，不应白屏。

静态资源走 `/demo-proxy/assets/*`（与现网同轨）；服务端已映射，直连 8766 即可。

## Docker

```bash
docker build -t mo2-demo .
docker run --rm -p 8766:8766 mo2-demo
# 有密钥时再加 --env-file .env
```

然后打开 http://127.0.0.1:8766/storyboard

## 说明

- 不要提交 `.env`（已在 `.gitignore`）。
- GitHub Pages **无法**直接跑本仓库的 FastAPI；请用本机 `./start-public.sh`、Docker，或自行接到支持容器的托管。
- 本 DEMO 是完整 Agent 顶栏，不是壳站 3010 embed。
- 仓根 [README.md](./README.md) 已是 DEMO 首屏入口。
