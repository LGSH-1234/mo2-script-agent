# Real DeepSeek verification

日期：2026-10-22（Asia/Shanghai）

- 服务端 `/api/health`：`model=deepseek-flash`，`model_configured=true`。
- 真实脚本生成：HTTP 200；返回 4 场；`origin=deepseek`；版本从 1 变为 2。
- 真实分镜链路：HTTP 200；返回 10 镜、总时长 50 秒、10 条非空视频提示词；版本变为 3。
- 真实局部修改：先生成差异提案，再应用；HTTP 200；仅更新指定镜头；版本变为 4；`approved_version` 清空。
- 验收项目及其 SQLite 版本、资产、提案、任务记录已删除，避免污染本地案例。

没有记录密钥、完整剧本或模型原始响应。视频仍是本地模拟 Provider，未调用视频供应商。
