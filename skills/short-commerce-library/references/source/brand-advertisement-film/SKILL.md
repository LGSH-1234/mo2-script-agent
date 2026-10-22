---
name: brand-advertisement-film
display_name: 品牌大片
description: 为品牌制作 现代TVC、品牌故事、情绪大片、质感广告 短视频。
tools: ["sandbox_generate_image", "render_video", "sandbox_generate_video", "sandbox_process_video"]
---

# 品牌大片

## 核心原则

为品牌制作 现代TVC、品牌故事、情绪大片、质感广告 短视频。

## 输入诊断

每次生产前，识别并判断以下维度：

- 品牌素材图片:(如果用户没输入则询问用户)
- 品牌/商品名称:(可选, 如果用户有输入则一定要使用)
- 标语/Slogan: (可选, 如果用户有输入则一定要使用)
- 视觉参考图: (可选, 如果用户有输入则一定要使用)
- 视频比例：(如果用户没输入则询问用户)

## 强制要求

必读：
- 必须使用`load_skill`工具加载 `marketing-video` 再进行创作
- 没有品牌/商品参考图则一定要反问用户要求输入