---
name: mo2-script-write
description: 导演文本转结构化脚本
status: active
version: 1.0.0
---
# 脚本编写
改编自 zenstory-ai/drama-skills 的 short-drama-write（MIT），固定上游 fdb7b7c58017e3eae64eca382c2a85ede368dab0。
保留用户事实和对白；用可见行动承载情绪。每场有明确进入、变化和退出状态。
先因果后修辞，去掉无功能的重复解释；按目标时长控制动作和对白。
输出遵循调用方的 Script JSON Schema，不写文件、不自动续集。
