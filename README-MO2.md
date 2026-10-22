# MO² 脚本分镜 Agent · 本地 Demo

导演文本 → 脚本 → 分镜与视频提示词 → 编辑 → 确认当前版本 → 手动逐镜生成 → 结果查看。

这是接入 MO² 本地网站的 Agent 工作台，没有产品画布或节点。顶部导航顺序为：首页、我的项目、关于我们、Agent、分镜。界面沿用 MO² 的深色、荧光绿和细描边。原版 aigc-agent 文档保留在 README.md；本文件是改造版启动入口。

## 启动

需要 Python 3.11+。源码包附带已构建前端，演示不需要安装 Node。

```bash
bash start.sh
```

macOS 可双击 `start.command`。首次启动会联网安装 `requirements-demo.lock` 中的依赖。浏览器打开 http://127.0.0.1:8766 。只监听本机，不是线上网址。

若 Python 路径不同：`MO2_PYTHON=/path/to/python3 bash start.sh`。端口被占用时先检查正在运行的服务，不要结束不明进程。

## 五分钟演示

1. 首页点击 Agent 后面的「分镜」，再点击「载入案例」，进入「雨夜来信」预置脚本和 6 镜分镜。
2. 切到「脚本」查看两场戏，再回「分镜表」。点击第 2 镜，编辑名称或画面内容并保存。版本增加，确认状态清除。
3. 点击「确认此版分镜表」→「确认此版本」。此时不会创建视频任务。
4. 点击任一镜头→「生成视频（模拟）」→「提交生成」。观察排队、生成中、完成，再播放样例。勾选失败选项可演示失败与手动重试。
5. 刷新页面，内容和任务仍在。查看版本历史，或导出 CSV。

预置脚本明确标为案例。视频是 6 秒技术样例，不是 AI 生成的故事画面；模拟任务不调用视频模型、不产生费用。Figma 的修改差异页是设计示例。

「导入脚本」支持 PDF、Word、TXT、Markdown、RTF 多选，显示文件名、类型和大小，支持去重、移除。本阶段只在当前前端页面展示附件，不解析、不上传，刷新后清空；模型仍以填写的导演文本为输入。

## 连接真实 DeepSeek

复制 `.env.example` 为 `.env`，只在本机填写 `DEEPSEEK_API_KEY`，然后重启服务。不要把密钥放进前端、飞书、聊天或源码包。

默认模型 `deepseek-flash`，可在 `.env` 的 `DEEPSEEK_MODEL` 修改。生成脚本、拆解分镜、生成提示词、对话修改均走真实 API，没有预置答案降级。未配置时明确报错并保留已有内容。

已完成一次真实 DeepSeek 验收：脚本返回 4 场、分镜返回 10 镜且每镜有提示词，局部修改返回差异提案并应用为新版本。验收使用的临时项目已清理；不把生成内容写入源码包或飞书。

## 开发

```bash
cd web
npm ci
npm run build
```

`web/dist` 由 FastAPI 提供。开发时可运行 `npm run dev`，Vite 已设置 API 代理。API 文档：http://127.0.0.1:8766/docs 。

```bash
.venv/bin/python -m pytest tests/test_web_demo.py -q
```

本地项目、版本和附件保存在 `local-data/`。源码包排除了此目录。模型缺钥、非法输出、版本冲突不会覆盖现有成果。

## 文件入口

|路径|用途|
|---|---|
|web/src/main.tsx、style.css|交互和 MO² 样式|
|web/src/SiteHeader.tsx、ProjectsPage.tsx、site.css|全站导航、真实本地项目列表和响应式布局|
|web/public/site/|从 REA 页面证据重建的首页、关于我们、价格展示和本地素材|
|scripts/reconstruct-site.mjs|公开页面重建脚本；不加载原站运行脚本|
|web_app/app.py|阶段接口、确认门禁、局部修改与模拟任务|
|web_app/runtime.py|复用上游 ModelGateway、SkillHub、EventBus|
|web_app/models.py|脚本、分镜与请求契约|
|web_app/store.py|SQLite、版本、资产与幂等任务|
|web_app/prompts.py|实际运行 Prompt|
|runtime-skills/|三个已改造且启用的 Skill|
|web-skills/|固定版本的原始 Skill 来源|
|docs/MO2-CHANGES.md|真实复用和改造清单|

## 原型与文档

- Figma：https://www.figma.com/design/WrIqp1jn9UvKbug3Nqf7Jq
- 飞书：https://acndwie2d1ts.feishu.cn/wiki/Y9nsw7Hk2iydV0kALaFc3D9hnsf
- aigc-agent 上游：https://github.com/yihuandeps/aigc-agent/tree/c236e7d54be9363f961d75d6159cb78945d48c9e

## 当前范围

单人本地演示；导演与创作者共用一次确认，不包含多人权限、联签审批、真实视频供应商、费用结算、自动合片、生产任务队列或部署。正式接入视频前需按供应商能力校验时长、画幅、素材和参数。本 Demo 的单镜 1–30 秒不是视频供应商能力声明。

网站复刻范围及浏览器验收见 [本地网站接入说明](docs/LOCAL-SITE.md)。本地首页和关于页保留原站产品介绍；其中出现的画布、Seedance 等能力是原产品内容，不代表分镜 Agent 已接入这些功能。原 Agent、付费购买、席位实时方案和作品观看仍链接官方服务。
