---
name: mo2-storyboard
description: 脚本转逐镜分镜表
status: active
version: 1.0.0
---
# 分镜设计
改编自 zenstory-ai/drama-skills 的 short-drama-storyboard（MIT），固定上游 fdb7b7c58017e3eae64eca382c2a85ede368dab0。
一镜一个主要叙事职责，明确起点、唯一主要动作和终点。
每镜引用真实脚本场景，保持人物站位、视线、持物和光线连续。
运镜服务情绪或信息揭示；固定镜头也可以成立。对白所需时间须被镜头容纳。
输出遵循调用方 Board JSON Schema；不要求先生成参考图，不调用媒体工具。
