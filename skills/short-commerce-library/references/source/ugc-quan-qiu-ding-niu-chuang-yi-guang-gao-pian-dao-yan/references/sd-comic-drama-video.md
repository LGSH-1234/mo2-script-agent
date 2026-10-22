# 漫剧 · 分镜转视频 · 电影级质感 · references/07

> **核心原则**：本文件管"锁定的资产/分镜，怎么变成可交付的竖屏短剧或漫剧"。覆盖三种产出形态：
> ① 竖屏短剧（图生视频，Seedance 2.5 默认）② 漫剧/动态漫画（分镜静帧 + Ken Burns + 配音）
> ③ 分镜转视频 Demo（关键镜跑片段验证一致性）。全部须达**全员演技在线 · 超越真人感顶级质感 · 电影级别**。
> 吸收自 Seedance 2.5 官方协议与 CINEDANCE 十四段骨架（同源）。

---

## 一、Seedance 2.5 官方提示词协议（默认目标模型）

### 0 · 执行铁律（每次生成前必守）
```
1. 模型与参数先确认，绝不替用户默认：任何文生图/图生视频/配音前，模型/分辨率/尺寸/风格未确认→停确认门提问。
2. 默认 Seedance 2.5；用户改选其他模型则切换，能力不丢。
3. 生成参数不写进提示词：时长/分辨率/比例/运动强度由页面/接口设置，提示词只描述内容意图。
4. 正向描述优先；只有"素材职责、编辑范围、易误带入内容"需显式限制。
5. 一份参考素材 = 唯一职责：写明"提供什么 + 不采用什么"，不让模型猜。
```

### 1 · 文本指令基础公式（组合式）
```
<主体> + <动作或事件> + <场景与环境>(可选) + <视觉风格>(可选) + <运镜或切镜>(可选) + <声音>(可选)
基础模板：
 <主体>在<场景与环境>中<主要动作或事件>。画面呈现<视觉风格>。镜头采用<景别、机位、运镜>。声音包括<对白/环境/音效>。
要点：主体+动作优先；场景写地点/时间/天气/空间关系；风格写光/色/材质/质感；运镜写景别/机位/运动/对焦/衔接。
```

### 2 · 有参考素材时：明确素材职责（映射写进提示词）
```
模板：@图片1用于<主体>的<外貌/服装/结构/材质>。@视频1用于<动作/运镜/节奏>。@音频1用于<角色>的<音色/台词/环境声>。
示例：@图片1用于<陶艺师>五官/发型/深绿围裙，不采用图片背景。@图片2用于<工作室>木台/窗位/晨光，不采用图中人物。
同物体多视角：@图片1正面 @图片2左侧 @图片3右侧 @图片4背面，四张共定义同一物，成片始终只有一个。
参考视频已给准动作/运镜/顺序时：只说继承哪些，不逐动作复述（重复易与素材冲突）。
```

> **⛔ 声锁铁律（视频禁项 · 与 SKILL.md「⛔ 同步声锁」完全一致）**：本参考产出的所有视频 / 图生视频 / 漫剧样片，**默认不生成字幕、不生成背景音乐**；字幕后期硬压，BGM 仅用户显式要求才加。下方所有提示词模板默认携带 `No subtitles. No music. No BGM.`；验收时逐镜核对成片确实无字幕、无自带 BGM。

### 3 · 声音与文字特殊字符（自然语言外显区分）
```
音乐 () 例：(背景播放舒缓钢琴乐)      音效 <> 例：<远处传来钟声>
台词 {} 例：{你好，欢迎回来}            字幕 【】 例：【第一章：启程】
控制：无背景音乐只留对白环境声→写"无背景音乐，只保留人物对白、环境声和动作音效。不要字幕。"
非中文台词先标语言：女孩用日语轻声说：{もう大丈夫です}
声线公式：台词语言+地区变体/口音+表达方式+说话人+{台词}
```

### 4 · 跨模型适配（能力全保留）
```
Seedance 2.5/即梦(默认)：上公式+参考映射+特殊字符；精简不堆比喻；每镜 2–3s；只出音效。
可灵：中文加深语义；运镜参数 0.4–0.6；参考图职责写清。
Runway：运动控制词优先；镜头运动显式。   Sora：详细物理因果，自然语言长句。
Midjourney/Flux/SD(文生图)：关键词式英文；--ar/--style raw 仅用户指定时用。
Suno/Udio(配乐)：Style 短准、Genre 首位；Lyrics 完整有结构标签。
```

### 5 · 确认门（Hard-Stop，模型无关）
```
🛑【确认门】已完成设计方案与提示词。请确认：目标模型[默认 Seedance 2.5/指定] ·
分辨率/时长/尺寸/画幅[已确认/待确认] · 风格基调[已锁定/待确认]。用户确认后才执行生成。
```

---

## 二、漫剧（动态漫画）样片流程

```
漫剧 = 分镜静帧（漫画/插画质感）+ Ken Burns 运镜 + 配音/拟音 + 漫画质感滤镜；成本低、出片快，先跑试播验证爽点/钩子。
步骤：
 1. 用资产锁定的 @CharID/@SceneID 生成分镜静帧（漫画风：清晰描边/平涂色块/微噪点笔触，非 3D render）。
 2. 每镜加 Ken Burns：缓推/横摇/变焦（幅度小，2–4s 一轮），让静帧"活"——替代实拍运镜。
 3. 配音：按声线卡(§六/references/04)生成对白；静帧对口型难，改用"画外音+角色微动"或"气泡字幕+音效"。
 4. 拟音/环境声：用 <> 音效层（门响/风/心跳）补空间；音乐 () 只在情感阀门开时进。
 5. 漫画质感滤镜：轻微颗粒/笔触纹理/描边强化；锁一套调色(60:30:10)跨镜一致。
 6. 剪辑：按六维衔接(§9)用"匹配剪辑/声音桥"连静帧，避免跳变；钩子镜黑场/定格收束。
```

**Ken Burns 参数（漫剧专用）**：
```
缓推：scale 1.0→1.08，duration 3s，ease-in-out（情绪逼近）
横摇：x -3%→+3%，duration 4s（环境揭示）
变焦：center 缩放 1.1，duration 2.5s（特写强调）
禁忌：幅度过大(>12%)→晕；过快(<1.5s)→廉价；全场同参数→死板。
```

---

## 三、分镜转视频 Demo（关键镜验证）

```
目的：全量生成前，先跑 3–8s 片段验证角色一致性/六维衔接/质感，再决定是否全量。
选镜：每集选 2–3 个关键镜（钩子镜、大爽爆发镜、身份揭晓镜）。
提示词：用 §一 公式 + 资产 @引用 + §四 电影级质量段；图生视频时把对应关键帧作参考图。
验证：跑完看 ①脸是否一致(三图卡锚) ②动作物理因果 ③色温/光位跨镜一致 ④有无 plastic/wax。
不达标→回 references/06 改 descriptor 或回 §四 补质量段，不靠死磨单镜。
```

---

## 四、电影级质感与全员演技（落到每条提示词）

```
Style Prefix（项目级视觉锁，逐字复制进每镜末尾；按项目重写，不套用别片）：
 Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
 Cinematography: floating immersive camera that lives with the actors; natural motivated light; painterly composed frames, strong silhouettes.
 Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze. Key light from sky/windows only.
 Color: 60:30:10 — dominant/secondary/accent.
 Camera: Physical cine lens. 180° shutter motion blur.
 Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
 Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with catch-lights, visible breath and chest rise.
 Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
 Composition: Rule of thirds + golden ratio. Continuity: Characters, props, environment identical across every cut.
 Technical: 24fps smooth motion. 8K detail. No jitter.
 Audio: Environmental SFX only. No music. No subtitles.

质量段（每条提示词必含）：8K detail, pore-level skin, no jitter, no flicker; faces stay exactly their references at every distance.
负向词（必含）：plastic skin, wax figure, airbrushed, symmetric doll face, extra fingers, deformed hands,
 watermark, text overlay, cinematic feel, unreal engine, 3D render.
技术尾标：Photoreal. NON-IP. 9:16. [时长]s. SFX only. NO CGI. Cinematic.
```

---

## 五、配音/配乐（声线人格）

```
 · 每个角色声线卡原样贴进 AUDIO 段（references/04/06）；潜台词靠重音/停顿/吞咽声（"他说过回来"后 0.4s 吞咽）。
 · 空间叙事：小房间 Early Reflection、空旷地无反射，暗示孤独。
 · 音乐动机：3–5 音符可识别主题，只在情感阀门开时精确进出（参考大师评审 references/08）。
 · 生成阶段自带"配乐"只添乱 → 提示词末尾写 "No music. SFX only."，音乐留后期。
```

---

## 六、反模式

```
❌ 提示词写时长/分辨率（应由页面设置）
❌ 参考图不点名职责（模型猜错把构图当脸）
❌ 没确认门就生成（替用户默认模型/画幅）
❌ 漫剧 Ken Burns 幅度过大/过快（晕/廉价）
❌ 质量段缺负向词 plastic/wax（AI 味）
❌ 音乐写进生成提示词（剪辑添乱）
❌ 全量生成前不跑 Demo 验证一致性（最贵错误）
```
