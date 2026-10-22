# MO² 脚本分镜 Agent — 公开 Demo

可克隆运行的 **Episode Agent Web DEMO**（FastAPI `web_app` + 已构建的 Vite `web`）。前端固定使用同源路径 **`/demo-proxy/`**（`vite.config.ts` 中 `base: '/demo-proxy/'`）；服务端在 `web_app/app.py` 挂载 **`/demo-proxy/assets`**，与壳站嵌入方式一致。

## 启动

需要 **Python 3.11+**（Debian/Ubuntu 请先安装 `python3-venv`）。前端产物已在 `web/dist`，**无需 Node** 即可跑演示。

```bash
git clone https://github.com/LGSH-1234/mo2-script-agent.git
cd mo2-script-agent

cp .env.example .env   # 可选：填入 DEEPSEEK_API_KEY 以使用真实模型；无密钥也可浏览界面与模拟流程

# 本机演示（仅 127.0.0.1）
bash start.sh

# 对外监听（默认 0.0.0.0:8766，可用 PORT / HOST 覆盖）
bash start-public.sh
```

**Docker：**

```bash
docker build -t mo2-demo .
docker run --rm -p 8766:8766 --env-file .env mo2-demo
```

## 打开页面

启动后请在浏览器打开：

**`http://127.0.0.1:8766/storyboard`**

（若改了 `PORT`，把 `8766` 换成你的端口。）

欢迎页为 **导入路径 B**：上传 Word / TXT / PDF 等已有脚本 →「开始写分镜」→ 进入分镜表（本阶段不走「从一句创意写脚本」路径）。

## 关于 `/demo-proxy/`

构建后的 HTML/JS 引用 **`/demo-proxy/assets/...`**。若只用静态文件服务器打开根路径 `/`、而没有 FastAPI 提供的 `/demo-proxy/assets` 映射，页面会 **白屏**。请始终使用上面的 **`start.sh` / `start-public.sh` 或 Docker**，不要单独 `python -m http.server` 根目录。

## 密钥与安全

- **不要** 提交 `.env` 或任何 API 密钥（已在 `.gitignore`）。
- 模板见 [`.env.example`](.env.example)。

## 更多文档

| 文件 | 说明 |
|------|------|
| [README-MO2.md](README-MO2.md) | 本地 Demo 五分钟演练、DeepSeek 配置 |
| [DEMO_GITHUB.md](DEMO_GITHUB.md) | 对外分享与托管说明 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 完整 AIGC Agent 架构（上游能力） |

上游同源仓（Cursor Origin）：`yvla8585/mo2-script-agent`（`main` 约 `cf9ad02` 一带的 demo-proxy 布局）。

## License

MIT — 见 [LICENSE](LICENSE)。
