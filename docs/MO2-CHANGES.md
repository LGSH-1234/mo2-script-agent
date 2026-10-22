# aigc-agent 复用与改造

上游：`yihuandeps/aigc-agent`，固定提交 `c236e7d54be9363f961d75d6159cb78945d48c9e`。

完整跟踪源码已复制到本项目；原有 CLI 和模块保留。新增 Web 工作台及状态控制层，没有把原项目描述为现成网页产品。

|上游能力|本版处理|实际调用位置|
|---|---|---|
|ModelGateway / ModelsConfig / ProviderConfig|复用；配置 DeepSeek 兼容接口与 JSON 输出|web_app/runtime.py|
|SkillHub|复用；只加载 runtime-skills 中三个固定 Skill|web_app/runtime.py|
|EventBus|复用模型调用事件；不等同于生产任务队列|web_app/runtime.py、app.py|
|Asset / AssetType|复用资产数据结构；新增 SQLite 保存和版本引用|web_app/store.py|
|Character / render_passport|保留可调用人物描述能力；当前 UI 未采集人物档案，默认没有输入|web_app/runtime.py|
|CLI 人审|新增网页确认与版本门禁；不调用 CLI stdin 审批|web_app/app.py|
|Loop / Graph 引擎|保留源码；本 Demo 采用确定性阶段控制，未复用其自动执行循环|src/aigc_agent/、web_app/app.py|
|媒体供应商|本次未启用；新增明确标识的模拟任务|web_app/store.py|
|文件式资产保存|新增 SQLite 项目、版本、提案、素材和任务|web_app/store.py|

## 新增目录

- `web/`：React 19 + TypeScript + Vite 前端，MO² 视觉风格。
- `web_app/`：FastAPI 接口、结构校验、DeepSeek 运行时和 SQLite 状态。
- `runtime-skills/`：脚本、分镜、视频提示词三个受控阶段。
- `web-skills/`：`zenstory-ai/drama-skills` 原始快照与许可证，固定提交 `fdb7b7c58017e3eae64eca382c2a85ede368dab0`。
- `tests/test_web_demo.py`：流程、错误保存、版本、幂等、重试和契约测试。
- `start.sh / start.command`：本地启动。

## 改造结果

从终端调用的通用创作框架，增加为“对话区 + 脚本/分镜工作区 + 镜头详情”的专用 Agent。人必须确认当前版本，再主动提交每个镜头。任何修改会撤销确认，历史版本与旧结果保留。

视频状态由本地模拟时钟驱动：约 2 秒排队后运行、约 7 秒完成或失败。它不是后台真实视频 Worker。未来替换 Provider 时保留任务接口，并新增队列、回调验签和供应商约束。

## 来源与许可

保留上游 LICENSE 与 THIRD_PARTY_NOTICES.md（及各目录原有声明），未将其改写为自有版权。三个创作 Skill 的原始来源与 MIT 声明也保留。本轮不向 GitHub 发布或部署。
