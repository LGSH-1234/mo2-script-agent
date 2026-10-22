# 13-分镜多参考图生视频管线 (Multi-Reference I2V Storyboard Pipeline)

> **归属系统**：即梦 Seedance 2.5 终极 AI 电影大师全流程制作系统 V8.0（0818多参版）
> **核心定位**：本文件是 **0818多参版的核心专章**——定义视频制作全流程的最优组织方式：**剧本创作 → 拆分分镜 → 确定多参考资产（角色含不同状态/场景/道具/角色音色音频）→ 分镜多参考图生视频提示词撰写 → ⏸️ 生成确认（默认不生成）**。
> **核心铁律**：**图生视频能力完整保留，但默认不生成**。本管线默认停在「分镜多参考图生视频提示词包」交付物——每镜一条多参考 I2V 提示词（即梦 Seedance 2.5 执行）；仅当用户**明确确认需要生成**时，才弹出 ⏸️ 确认单并在 Seedance 2.5 中生成。
> **关联模块**：`SKILL.md` | [references/05 资产圣经](05-lira-asset-generation.md) | [references/06 声音工程](06-audio-driven-sound-engineering.md) | [references/08 提示词模板库](08-master-prompt-templates.md)

---

## 一、 管线总览 (Pipeline Overview)

本管线把「AI 视频制作」从"先写分镜提示词、再碰运气"重组为**资产驱动的多参考分镜生成**：所有跨镜一致性（角色长什么样、声音什么样、场景在什么状态）都在 Step 3 的**多参考资产**中一次性锁定，Step 4 每镜的提示词只需**引用**这些资产 + 描述本镜独有的动作/台词/运镜。**每镜生成时，把该镜引用的多参资产（角色图/场景图/道具图/音色音频）一并作为参考图/参考音频上传**——这就是"分镜多参考图生视频"。

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Step 1       │    │ Step 2       │    │ Step 3       │    │ Step 4       │    │ Step 5       │
│ 剧本创作     │───>│ 拆分分镜     │───>│ 确定多参考   │───>│ 分镜多参考   │───>│ ⏸️ 生成确认  │
│ (创作，不生成)│    │ (分镜蓝图)   │    │ 资产         │    │ 图生视频提示 │    │ (默认不生成) │
│              │    │              │    │ (角色含状态/ │    │ 词撰写       │    │ 用户确认后   │
│              │    │              │    │  场景/道具/  │    │ (多参锁定+   │    │ 才生成，可   │
│              │    │              │    │  音色音频)   │    │  台词音效+   │    │ 迁可灵等模型)│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │                   │                   │
   [Gate G0]          [Gate G1]          [Gate G2 强确认]     [交付物=提示词包]     [Gate G4 确认单]
   等级L/S/F          声音/主题确认       资产卡+命名字典       默认终点·不生成       确认后进入生成
```

**五步对应 G 门**：Step 1=G0 · Step 2=G1 · Step 3=G2（强确认）· Step 4=G3（分镜蓝图+提示词撰写，**默认交付终点**）· Step 5=G4（⏸️ 生成确认，默认不执行）。

---

## 二、 Step 1 — 剧本创作 (Script Creation)

**目标**：产出可拆分的故事本体。只创作，不生成任何资产与视频。

### SOP
1. **大师十问**（见 [references/10](10-capability-engines.md)）：主题、主角欲望、阻碍、三幕转折、情绪弧线、主题句……选出故事核心基因 ≥3 项，写入项目卡。
2. **角色设定**：每个角色 = 性格核心 + 目标 + 阻碍 + 行为习惯（为 Step 3 角色资产与 Step 4 ACTING 描述打底）。
3. **三幕结构 + 能量级 1-5**：标记每幕的情绪能量曲线，供 Step 2 拆分分镜时确定镜头节奏。

### 产出物
- 项目卡（制作等级 L/S/F + 故事核心基因）
- 完整剧本 / 故事大纲
- 角色设定表

---

## 三、 Step 2 — 拆分分镜 (Storyboard Breakdown)

**目标**：把剧本切成"一镜一卡"的分镜序列，每镜标注可执行的镜头参数。只规划，不生成。

### SOP（每镜一张分镜卡）
| 分镜卡字段 | 填写规范 |
|---|---|
| 镜头编号 | SH01、SH02…（连续编号，供命名字典与提示词引用） |
| 时长 | 单镜建议 3-10s（Seedance 2.5 单次 4-30s；长片可用 30s 分镜或多镜拼合） |
| 景别 | 全景 / 中景 / 近景 / 特写 / 大特写 |
| 运镜 | 固定 / 推 / 拉 / 摇 / 移 / 跟 / 升降 / 手持（描述动机，禁止无意义漂移） |
| 叙事任务 | 五问公理自检：推动故事什么？承接上一镜什么？无叙事任务则砍（0817叙事驱动增强） |
| 动作/表情 | 物理层面指令（本镜主角在做什么，微秒级时序） |
| 情感解析 | 潜台词：动作背后的情绪与意图（供 ACTING 描述） |
| 台词 | 本镜台词原文（只在本镜提示词 AUDIO 区出现） |
| 音效 | 本镜需要的环境/动作/生理音效（五层架构） |
| 引用资产占位 | 本镜将引用哪些多参资产（Step 3 完成后回填 @标签） |

### 产出物
- 分镜蓝图（分镜卡序列）
- 每镜一条"时间戳剧本分镜"（0s-3s / 3s-7s… 动作+情感解析，格式见 [references/08 模板2](08-master-prompt-templates.md) 与即梦手册 30 秒长视频公式）

---

## 四、 Step 3 — 确定多参考资产 (Multi-Reference Asset Lock — 资产先行)

**目标**：确定全片**多参考资产**并锁定——这些资产将作为**每镜图生视频生成的多参参考素材**（参考图 / 参考音频）上传。**凡资产必须先确定（G2 强确认，等待用户批准才可推进）。**

> **完整资产生成规范见 [references/05](05-lira-asset-generation.md)**（分图多视角 / 取景框裁切 / 状态资产树 / 单一衍生源公理 / 压测）；声音资产见 [references/06](06-audio-driven-sound-engineering.md)。本节约简为"多参考资产清单"视角。

### 4.1 多参考资产类型总表（Multi-Reference Asset Inventory）

| 资产类型 | @ 标签格式 | 含状态 | 作为多参用途 | 参考规范 |
|---|---|---|---|---|
| **角色** | `@CHAR_[名]` | 基准态 + 状态资产树 | 上传作参考图，锁定面孔/身形/服装/状态 | 分图多视角（V1 无头全身 + V7 面部极特写），禁止单图拼贴；每状态独立一张，单一衍生源 |
| **场景** | `@SCN_[名]_[状态]` | 日/夜/雨/战后/晨… | 上传作参考图，锁定环境/打光/锚点 | 21:9 宽银幕 + 3/4 视角 + 锚点；每时间/天气/损坏状态独立一张 |
| **道具** | `@PROP_[名]_[状态]` | 完整/使用/激活/受损/隐藏 | 上传作参考图，锁定道具外观/状态/材质 | 每剧情状态独立一张 |
| **角色音色音频** | `@VOX_[名]` / `@CharID_AUDIO_[名]` | 音色指纹不变，语气可变 | 上传作参考音频，锁定角色声线 | 六维音色建模 + VOX LOCK；用户声音样本锚定 `@CharID_AUDIO_XX` |
| **通用音频（音效/环境声）** | `@音频[序号]` | — | 上传作参考音频，提供音效节奏/卡点 | 24kHz 干净音效，≤30s 总时长 |

### 4.2 角色资产（含不同状态）——一致性第一来源

- **基准态 `@CHAR_唐末`**：全片唯一"修改母本"。分图多视角（V1 正面全身·无头 + V2 背面全身·无头 + V7 面部极特写），压测 10/10 + 同框测试。
- **状态资产树**：受伤 / 换装 / 妆造 / 老年 / 病态 / 湿 / 战损 / 亡……**每个状态独立一张，全部从基准资产一次点修改衍生**（单一衍生源公理，严禁链式修改）。
- **身份连续铁律**：任何状态资产的面孔/体型/比例必须与基准 100% 连续；每状态过"与基准同框不串"压测。
- **IDENTITY LOCK（英文，跨镜逐字）**：`@CHAR_唐末 — [EN identity lock descriptor]` 全片逐字附加，禁止翻译回写（见 references/05 §二.4）。

### 4.3 场景与道具资产（含不同状态）

- 场景基准态 + 状态族（日/夜/雨/战后/晨…）：@ 精确到本镜状态，绝不拿基准态代替夜戏/雨戏。
- 道具基准态 + 状态族（完整/使用/激活/受损/隐藏…）：@ 精确到本镜状态。
- 场景锚点必留；单光源逻辑（一个主光源、一个阴影方向）。

### 4.4 角色音色音频资产——一致性第二来源

> **图生视频默认只生成同期声，不生成音乐（同步声锁）**。台词、音效、音色全部在此锁定。

- **六维音色建模**（音域声部 / 语速节奏 / 口音方言 / 语气情绪基调 / 呼吸微发音 / 录音空间混响）→ 写成 1-2 句 Voice Prompt。
- **VOX LOCK（跨镜逐字）**：同一角色在争吵/突变场景下语气词变化 + 声调升高，**但音色指纹不变**；声音提示词每次该角色开口都逐字粘贴、永不修改。
- **用户声音样本**：用户提供的声音样本锚定为 `@CharID_AUDIO_唐末`，上传作参考音频，全项目不漂移（见 [references/11](11-user-asset-logo-placement.md)）。
- **声音压测**：10 次生成声音可辨；漂移则把措辞锁得更死。

### 4.5 多参输入规格（Seedance 2.5 上限，多参考资产按需分批）

| 模态 | 上限 | 最佳实践 |
|---|---|---|
| 图片 | 单次 ≤30 张 | 1-8 主体效果较好；多视角分图优于单图拼贴；**分镜生成时按"本镜激活资产"只传相关几张**（1-5 张参考图效果最佳） |
| 音频 | 单次 ≤10 段，总 ≤30s | 1-5 主体效果好；5-10s 时长效果好 |
| 视频 | 单次 ≤10 段，总 ≤30s | 白模/动作参考 10-20s 原生高帧率 |

### 4.6 @ 命名字典 + 分镜-资产匹配清单

- **@ 命名字典表**：`@标签 | 资产名 | 状态 | 描述符(逐字) | 参考图/音频编号 | 所属分镜范围`。**资产卡 @ 名 = 分镜提示词 @ 引用 = 界面参考名，一字不差。**
- **分镜-资产匹配清单**：每镜列出**本镜激活资产清单**（角色/场景/道具/音色音频各自 @ 哪张），@ 引用必须指向**该镜状态下最准确的那张资产**（带伤出场引 `@CHAR_唐末_受伤`，夜戏引 `@SCN_长安_宫城_夜`）。

### 产出物（G2 强确认门）
- 资产圣经（角色/场景/道具分图多视角资产图 + 状态资产树）
- 角色音色音频资产（六维音色描述 + VOX LOCK + 用户声音样本锚定）
- @ 命名字典表 + 分镜-资产匹配清单
- **⛔ 在此强行停下，等待用户批准全部资产后才可推进。**

---

## 五、 Step 4 — 分镜多参考图生视频提示词撰写 (Multi-Reference I2V Prompt Writing — 核心交付物)

**目标**：为**每一个分镜**撰写一条**多参考图生视频提示词**——引用 Step 3 锁定的多参资产 + 描述本镜独有的动作/台词/运镜。**这是默认交付物，系统在此停下，不生成视频。**

### 5.1 多参考 I2V 提示词公式（六模块）

```
分镜多参考图生视频提示词 =
  【模块A：多参考素材锁定层】+ 【模块B：一句话概述】+ 【模块C：时间戳情节描述】
  + 【模块D：台词与音效】+ 【模块E：音色与角色形象一致性描述】+ 【模块F：全局补充/禁止项】
```

### 5.2 模块 A — 多参考素材锁定层（Multi-Reference Lock Layer）

**每镜先列本镜激活资产，逐条绑定用途**——从分镜-资产匹配清单逐字复制：

```text
【本镜多参考素材锁定】
- 角色（含状态）：@CHAR_唐末_受伤 for character reference — [命名字典中受伤态描述符，逐字粘贴]。100% 保持该参考的面孔/身形/服装/伤口状态，绝不漂移。
- 场景（精确状态）：@SCN_长安_宫城_夜 for location reference — take only the space and the texture: [夜间宫城材质/月光光影]。Do not use as a starting frame, do not inherit the composition, the angle or the color.
- 道具（精确状态）：@PROP_圣晶石_激活 for prop reference — [激活态描述符]。材质/光感/形态严格还原。
- 音色音频（角色声音）：@CharID_AUDIO_唐末 / @VOX_唐末 for voice reference — 声线指纹严格保持（六维音色描述逐字）。
```

**规则**：
- 每条 @ 引用必须带**用途标注**（`for character reference` / `for location reference` / `for prop reference` / `for voice reference`）——否则模型自己决定参考用途。
- 状态跨镜连续：上一镜受伤，下一镜仍引用 `@CHAR_唐末_受伤`；伤口/血/破损绝不跨镜重置。
- 上传参考素材时，只传**本镜激活的那几张**（1-5 张最佳），不把全片资产图一次性堆上去。

### 5.3 模块 B — 一句话概述

`主体 + 地点 + 事件 + 题材/风格 + 特殊运镜`（如：**写实古装剧情片，雨夜长安宫城走廊，受伤的唐末持剑对峙三名追兵，手持近景跟拍**）。

### 5.4 模块 C — 时间戳情节描述（Timestamp Plot Description）

按时间戳分段写本镜的动作/表情/运镜（**精确到秒**，物理层面指令 + 情感解析潜台词）：

```text
[00:00 - 00:03] 动作/物理指令：@CHAR_唐末_受伤 背靠宫墙站立，右臂持 @PROP_圣晶石_激活，剑尖低垂；镜头从脚部缓慢上摇至面部。
[00:03 - 00:07] 情感解析/潜台词：他呼吸沉重，眼神在阴影中仍显凌厉——不是恐惧，是死战前的最后清点。
[00:07 - 00:10] 动作/物理指令：雨滴沿剑刃滑落，他猛地抬头，目光锁定镜头方向（走廊尽头），眉心紧蹙，握剑指节发白。
```

### 5.5 模块 D — 台词与音效 (Dialogue & Sound Effects)

- **台词唯一铁律**：台词只住本模块，带引号；谁没台词就完全沉默；"半笑"是表情不是声音。
- **对白四要素**：声音+情绪 → 引号台词 → 物理动作 → 面部反应（动作与台词永不混写）。
- **音效五层架构**：L1 物理碰撞 / L2 衣物质感 / L3 人体生理 / L4 空间环境底噪 / L5 叙事声桥；按时间戳卡点（100ms 轴）。
- **同步声锁**：`Environmental SFX and dialogue only. No music. No BGM. No subtitles.`

```text
【台词】"圣晶石……你们拿不走。"（@VOX_唐末：低沉干涩男低音，句尾带极轻的吸气声，语速缓慢克制）
【音效】[00:00-00:03] L4 雨声底噪 + L1 雨水滴落剑刃声；[00:03-00:07] L3 粗重呼吸声；[00:07-00:10] 走廊尽头脚步声渐近。
```

### 5.6 模块 E — 音色与角色形象一致性描述 (Voice & Identity Consistency — 跨镜一致性控制核心)

**此模块是控制不同分镜生成一致性的关键**——音色用 VOX LOCK，形象用 IDENTITY LOCK，两者全片逐字、永不修改：

```text
【音色一致性 VOX LOCK】@VOX_唐末 声音 = "低沉干涩男低音，每分钟 100 字，语速缓慢带重音微停顿，藏区口音硬朗腔调，克制隐忍；争吵/突变场景语气词变化+声调升高，但音色指纹不变。"（逐字复制自命名字典，每次开口都用）
【形象一致性 IDENTITY LOCK】@CHAR_唐末_受伤 = "[EN identity lock：age-bracket/face/eyes/hair/build/costume/wound descriptor 逐字] 100% matches the reference。"（英文撰写禁止翻译回写）
```

### 5.7 模块 F — 全局补充与禁止项 (Global Supplement & Negative)

- **全局补充**：贯穿全镜的机位/环境特征/光影/氛围/整体声音（如"全镜保持雨夜冷蓝基调，低机位，无快速剪辑"）。
- **禁止项**（局部小锁，不输出独立大块）：`No flat front light. No duplicate characters. No subtitles.` 措辞纪律见 SKILL.md（正向形式、不写年龄、禁词字典）。

### 5.8 中英双语铁律

所有输出提示词**同时提供【中文版】+【英文版】**：中文版供用户校验，英文版供模型执行；台词按项目语言（0817增强）。多参考 I2V 提示词同样遵守。

### 产出物（Step 4 = 默认终点）
- **分镜多参考图生视频提示词包**：每镜一条（中英双语），含模块 A-F。
- **⛔ 在此停下**：不自动生成、不默认调用生成。把提示词包交付给用户，进入 Step 5 确认门。

---

## 六、 跨分镜一致性控制清单 (Cross-Storyboard Consistency Checklist)

**目的**：保证不同分镜生成时，角色长相/声音/服装/场景状态/道具状态全程一致。**每个分镜提示词撰写后、交付前，逐项自检：**

| # | 一致性维度 | 自检项 | 控制机制 |
|---|---|---|---|
| 1 | 角色形象 | 本镜 @CHAR 引用是否精确到该镜状态？描述符是否逐字来自命名字典？ | IDENTITY LOCK + 分镜-资产匹配 |
| 2 | 角色音色 | 本镜台词是否带 @VOX/@CharID_AUDIO 引用？六维音色描述是否逐字？ | VOX LOCK + 用户声音样本锚定 |
| 3 | 服装/妆造状态 | 本镜角色状态（受伤/换装/湿…）是否与剧情时间线一致、跨镜不重置？ | 状态资产树 + 状态跨镜连续 |
| 4 | 场景状态 | 本镜 @SCN 是否精确到日/夜/雨/战后状态？锚点是否统一？ | 场景状态族 + 单光源逻辑 |
| 5 | 道具状态 | 本镜 @PROP 是否精确到完整/激活/受损状态？ | 道具状态族 |
| 6 | 台词/音效 | 台词是否只在 AUDIO 区、带引号？音效是否按五层+时间戳？ | 对白四要素 + 同步声锁 |
| 7 | 镜头/空间 | 180° 轴线是否一致？首帧是否已含角色？ | GEO 地理锁 + 首帧物理锚定 |
| 8 | 禁止项 | 是否无字幕/BGM/串脸/多余角色？ | 措辞纪律 + 局部小锁 |

**逐镜自检通过后，才把该镜提示词放入提示词包。**

---

## 七、 Step 5 — ⏸️ 生成确认 (Generation Confirmation — 默认不生成)

**图生视频能力完整保留，但默认不生成。** 系统默认停在 Step 4 的提示词包交付物上。

### 7.1 默认行为（No-Default-Generation）
- 提示词包交付后，**不自动进入生成**，不默认调用任何模型。
- 提示词包是**Seedance 2.5 专属**的：用户确认后直接在即梦 Seedance 2.5 中执行——本版本"不默认生成"的核心目的：**资产与提示词先锁定，确认后才生成**，绝不擅自调用。

### 7.2 确认单 (Confirmation Sheet — 用户明确确认后才弹出)
仅当用户明确表达"生成/出片/发车/开始生成"时，弹出确认单：

```
⏸️ 生成确认单
- 模型：□ 即梦 Seedance 2.5（默认） □ 其他（请指定）
- 分辨率：□ 480p □ 720p □ 720p+
- 画幅：□ 16:9 □ 9:16 □ 1:1 □ 21:9（2.39:1） □ 其他
- 风格：□ 电影写实 □ 国漫/三渲二 □ 科幻 □ 其他（按提示词包 Style）
- 时长：□ 4s □ 8s □ 10s □ 30s □ 超长 30-180s □ 其他
- 同步声锁：□ 仅同期声（台词+音效，无音乐、无字幕，默认） □ 需要配乐（用户显式要求才选）
```

- 全部经用户确认后才进入生成环节；**绝不擅自假定、绝不默认生成。**
- 每个分镜单独确认（或用户明确"整包统一参数生成"后批量确认）。

### 7.3 生成后质量门
按 [references/07](07-hellgrind-production-pipeline.md) 奥斯卡 80 分评审表逐镜验收；不过 80 分 → Loop 循环修复（上限 3 次）。

---

## 八、 完整模板示例 (Full Multi-Reference I2V Prompt Example)

> 场景：古装武侠片《圣晶石》，SH03 镜——雨夜宫城走廊，受伤的唐末持激活态圣晶石对峙追兵。资产已锁定（@CHAR_唐末_受伤 / @SCN_长安_宫城_夜 / @PROP_圣晶石_激活 / @VOX_唐末）。

### 【中文版】（供用户校验）

```text
SH03（8.0s）——雨夜宫城走廊 · 分镜多参考图生视频提示词

【模块A：多参考素材锁定层】
- 角色：@CHAR_唐末_受伤 for character reference —— 左臂绷带、脸颊血渍、干裂嘴唇、黑色交领劲装破损；面孔/身形/服装/伤口状态与参考 100% 一致，绝不漂移。
- 场景：@SCN_长安_宫城_夜 for location reference —— 只取空间与质感：青石走廊、宫灯暖光与冷蓝月光交错、雨幕与积水倒影。不继承参考图构图/角度/色彩。
- 道具：@PROP_圣晶石_激活 for prop reference —— 掌心大小菱形晶石，内部蓝光脉动，表面水珠折射。
- 音色：@VOX_唐末 for voice reference —— 低沉干涩男低音，声线指纹严格保持。

【模块B：一句话概述】
写实古装武侠，雨夜长安宫城走廊，受伤的唐末持激活圣晶石与三名追兵对峙，手持近景跟拍，克制悲壮。

【模块C：时间戳情节描述】
[00:00-00:03] 动作/物理指令：@CHAR_唐末_受伤 背靠宫墙，右臂持 @PROP_圣晶石_激活 于胸前，剑尖低垂；镜头从积水地面缓慢上摇至面部。
[00:03-00:07] 情感解析/潜台词：呼吸沉重，眼神在宫灯与月光的交界处仍显凌厉——不是恐惧，是死战前的最后清点。
[00:07-00:08] 动作/物理指令：雨滴沿剑刃滑落，他猛地抬头锁向走廊尽头，眉心紧蹙，握剑指节发白，圣晶石蓝光骤亮。

【模块D：台词与音效】
台词："圣晶石……你们拿不走。"（@VOX_唐末：低沉干涩，句尾极轻吸气，语速缓慢克制）
音效：[00:00-00:03] L4 雨声底噪 + L1 雨水滴落剑刃声；[00:03-00:07] L3 粗重呼吸 + 心跳声；[00:07-00:08] 走廊尽头密集脚步声逼近，圣晶石低频嗡鸣渐强。
Environmental SFX and dialogue only. No music. No BGM. No subtitles.

【模块E：音色与角色形象一致性描述】
音色一致性 VOX LOCK：@VOX_唐末 声音 = "低沉干涩男低音，语速缓慢带重音微停顿，藏区口音硬朗腔调，克制隐忍；突变场景语气词变化+声调升高，音色指纹不变。"
形象一致性 IDENTITY LOCK：@CHAR_唐末_受伤 = "[EN descriptor: mid-20s Han man, sharp brows, high nose bridge, firm jawline, black cross-collar brocade outfit, left-arm bandage, dried blood on cheek, cracked lips] 100% matches the reference."

【模块F：全局补充与禁止项】
全镜保持雨夜冷蓝基调 + 宫灯暖光对冲，低机位，轻微手持呼吸感，无快速剪辑；无字幕，无 BGM，无多余角色。
```

### 【英文版】（供模型执行）

```text
SH03 (8.0s) — Rainy night palace corridor · Multi-Reference I2V Prompt

[Module A: Multi-Reference Lock Layer]
- Character: @CHAR_唐末_受伤 for character reference — left-arm bandage, dried blood on cheek, cracked lips, damaged black cross-collar outfit; face/body/costume/wound state 100% match the reference, no drift.
- Location: @SCN_长安_宫城_夜 for location reference — take only the space and the texture: bluestone corridor, warm palace-lantern light clashing with cold blue moonlight, rain curtain and puddle reflections. Do not use as a starting frame, do not inherit the composition, the angle or the color.
- Prop: @PROP_圣晶石_激活 for prop reference — palm-sized diamond crystal, blue light pulsing inside, water droplets refracting on surface.
- Voice: @VOX_唐末 for voice reference — low dry baritone, voice fingerprint strictly preserved.

[Module B: One-Line Overview]
Realistic wuxia. Rainy night Chang'an palace corridor. Wounded Tangmo holding the activated crystal, facing three pursuers. Handheld medium close tracking shot. Restrained, tragic.

[Module C: Timestamp Plot Description]
[00:00-00:03] Action/Physical: @CHAR_唐末_受伤 leans back against the palace wall, right arm holding @PROP_圣晶石_激活 at chest height, sword tip low; camera slowly tilts up from rain-soaked ground to his face.
[00:03-00:07] Subtext: Heavy breathing; eyes remain sharp at the meeting line of lantern light and moonlight — not fear, a final inventory before a death fight.
[00:07-00:08] Action/Physical: Rain drips off the blade; he snaps his head toward the end of the corridor, brows knit, knuckles white on the sword grip, the crystal's blue light flares.

[Module D: Dialogue & Sound]
Dialogue: "The sacred crystal… you will not take it." (@VOX_唐末: low dry baritone, faint inhale at the line end, slow restrained pace)
SFX: [00:00-00:03] L4 rain bed tone + L1 rain hitting the blade; [00:03-00:07] L3 heavy breathing and heartbeat; [00:07-00:08] rapid footsteps approaching from corridor end, crystal low hum rising.
Environmental SFX and dialogue only. No music. No BGM. No subtitles.

[Module E: Voice & Identity Consistency]
VOX LOCK: @VOX_唐末 voice = "low dry baritone, slow pace with stressed micro-pauses, hard highland accent, restrained and stoic; under sudden change, tone words shift and pitch rises, but the voice fingerprint never changes."
IDENTITY LOCK: @CHAR_唐末_受伤 = "[mid-20s Han man, sharp brows, high nose bridge, firm jawline, black cross-collar brocade outfit, left-arm bandage, dried blood on cheek, cracked lips] 100% matches the reference."

[Module F: Global & Negative]
Whole shot: cold blue rain-night key with warm lantern-light contrast, low camera, slight handheld breathing, no fast cuts; no subtitles, no BGM, no extra characters.
```

> **交付方式**：提示词包交付后，系统**默认停下**。询问用户："提示词包已就绪。需要我用即梦 Seedance 2.5 生成吗？"——用户确认后才进入 Step 5 生成。

---

## 九、 常用分镜类型补充模板 (Quick Sub-Templates)

### 1. 对话分镜（双人对手戏）
- 模块 A 传两角色参考图 + 两音色音频；模块 C 分时段写 A 说/B 反应（聆听与反应四规则）；模块 D 台词唯一铁律 + 混音规则（人声干净近麦、环境音说话时自动压低）。

### 2. 动作/打斗分镜
- 模块 C 微秒级时序（0.0-0.5s 起手 → 1.2s 碰撞 → 2.5s 反应）；L1 物理打击音卡点；物理与重力（接触阴影、惯性）。

### 3. 环境/空镜分镜（B-roll）
- 无角色 @ 引用，只传场景状态资产；模块 B 强调氛围/光/时间；音效走 L4 环境底噪 + L5 声桥（衔接上/下一镜情绪）。

### 4. 多人同框分镜
- 模块 A 逐人绑定参考图 + 显式"各角色外貌/服装/体型严格独立，互不串脸"（多人独立锁，见 [references/02](02-seedance-25-full-capabilities.md) §三.5）。

### 5. 一镜到底长分镜（30s）
- 单镜 30s 长提示词：模块 C 拆多个时间戳阶段（参照即梦手册 30 秒长视频公式）；白模参考视频场景下遵守**单段完整生成铁律**（见 [references/01](01-whitebox-champion-rendering.md)），严禁切割拼接。

---

## 十、 质量自检清单 (Delivery Checklist)

- [ ] 五步管线全部走完：剧本 → 分镜 → 多参考资产 → 多参考 I2V 提示词 →（用户确认后）生成
- [ ] 每镜提示词含完整模块 A-F，中英双语
- [ ] 每镜 @ 引用与命名字典一字不差，@ 引用精确到状态（角色受伤/场景夜雨/道具激活）
- [ ] 每镜含台词与音效（台词只在 AUDIO 区、带引号；音效按五层+时间戳）
- [ ] 每镜含音色一致性（VOX LOCK）+ 形象一致性（IDENTITY LOCK）描述
- [ ] 跨分镜一致性清单 8 项全部自检通过
- [ ] **默认不生成**：未生成任何视频；已向用户交付提示词包并询问是否生成
- [ ] 用户确认生成后：确认单（模型/分辨率/画幅/风格/时长/同步声锁）全部经用户批复
- [ ] 生成后：奥斯卡 80 分评审（见 [references/07](07-hellgrind-production-pipeline.md)）

---

*13-分镜多参考图生视频管线 · 0818多参版核心专章 · Seedance 2.5 专属系统*