---
name: mo2-video-prompt
description: 分镜转独立单镜视频提示词
status: active
version: 1.0.0
---
# 视频提示词
改编自 zenstory-ai/drama-skills 的 short-drama-video-prompts（MIT），固定上游 fdb7b7c58017e3eae64eca382c2a85ede368dab0。
静态锚点 → 起点 → 主要动作 → 次级反应 → 运镜 → 声音 → 终点。
不改变分镜边界；对白保持原文，描述可执行的动作。
不伪造图片；无图采用独立文生路径，有图只引用真实素材。
输出遵循调用方 JSON Schema。在整表确认之前编写提示词，确认之后才可手动提交视频任务。
禁用自动续接、多镜容器、自动重试与合片。
