# 变装卡点转场广告 · 极速上手指南（skill-intro.md）

> **一句话定位**：以 TikTok/抖音爆款 transition 变装卡点为标杆，用 before/after 同机位对齐、beat drop 瞬间变装、手势遮挡/甩镜转场魔法与多套造型连变，把服饰造型转化为可见的惊艳蜕变欲望。**对齐即魔法，卡点即惊艳，反差即传播。**

## 🚀 30 秒上手流程

1. **锁基准资产**：先定 `@CHAR_TRANSFORMER`（变装达人 Model Card）+ `@OUTFIT_BEFORE`（before 平淡便服）+ `@OUTFIT_AFTER`（after 惊艳华丽造型，可多套）+ `@SCN_TRANSITION`（固定机位对齐背景），一次性锁定，全程 @ 引用禁止链式改（before/after 须同一面部骨相、同一机位对齐）。
2. **选文生图版本**：默认用 `SKILL.md §二` 的 MJ v8 专属版或常规通用版；用户点名"角色资产卡/Model Card/定妆卡"时才输出第三版本（10 格，before/after 双造型头部三视角）。
3. **写剧本**：套三段式变装——①before 日常便服开场铺垫 → ②卡点转场魔法瞬间变装 → ③after 惊艳 reveal 多套连变定格（详见 `02-viral-script-hooks.md`）。
4. **生成视频**：套 `SKILL.md §三` 的 11 段式多参引擎，**除台词外整体描述必须用中文**，竖屏 9:16 手机原生，逐段注入造型动力学 + 光影五子层，**固定锁定机位对齐 beat drop**。
5. **配音效**：卡点 BGM + 转场音效 whoosh/闪光 + beat drop 落在变装瞬间（详见 `03-sound-design-asmr.md`）。

## 🎯 五大不可动摇配方速查

| 配方 | 数值锚点 |
|---|---|
| **同机位对齐魔法** | 手机竖屏 26mm 全身**固定锁定机位（locked-off）**，before/after 同机位、同姿态、同构图，靠 beat drop 瞬间切换（转场魔法核心，严禁机位错位） |
| **动感时尚光反差** | 时尚柔光箱右侧 30° 5200K Key:Fill 2.5:1 大片感，before 平淡低饱和 ↔ after 鲜艳高饱和强对比，转场闪光 +1.5 档华丽边缘光 |
| **卡点转场技巧** | 手势遮挡/甩镜/跳切三种转场触发，beat drop 精准落在切换帧，15 秒多套连变卡点快切 |
| **before→after AU 反差** | before 松弛随意（A 级基线）→ after 自信 AU6+AU12+AU17（C 级气场），变装惊艳反差表演 |
| **造型强反差** | @OUTFIT_BEFORE 平淡棉质 ↔ @OUTFIT_AFTER 华丽亮片垂坠，反差越大传播越强，同一面部骨相 100% 一致 |

## ⚠️ 三条红线
- **严禁机位错位**：before/after 必须同机位、同姿态、同构图对齐，绝不允许转场脱拍、机位漂移（对齐即魔法，错位即穿帮）。
- **严禁换脸**：before 与 after 须同一面部骨相 100% 一致，绝不允许变装前后像换了个人（破坏 transition 可信度）。
- **字幕铁律**：No subtitles.（字幕/造型名花字绝不由模型生成，须后期硬压）；卡点 BGM 声场对齐 beat drop，台词保留原语言口语化，口型同步精准。

## 📚 深入查阅
- 完整提示词双版本 + Model Card：`SKILL.md`
- 美学基因：`references/01-transition-transformation-dna.md`
- 剧本钩子：`references/02-viral-script-hooks.md`
- 声场工程：`references/03-sound-design-asmr.md`
- 运镜光学：`references/cinedance-camera-optics.md`
- AU 表演：`references/perf-acting-au-system.md`
- 3D 白模：`references/whitebox-3d-rendering-guide.md`
- 生图引擎/多参引擎：`references/midjourney-v8-t2i-engine.md`、`references/multiref-ensemble-acting.md`
