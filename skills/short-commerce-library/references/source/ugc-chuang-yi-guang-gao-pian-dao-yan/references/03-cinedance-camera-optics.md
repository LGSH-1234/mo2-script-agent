# 03-CINEDANCE V4 镜头与光学导演系统 (Camera & Lens Director System)

> **归属系统**：CINEDANCE V4 AI Film Prompt Director  
> **核心使命**：为 Seedance 2.5 视频模型提供大师级电影摄影学 (Cinematography)、镜头光学 (Optics)、空间调度 (Spatial Blocking) 与物理构图控制。

---

## 一、 14 区块通用提示词骨架 (14-Block Skeleton Architecture)

为了保证镜头在生成时不产生任何空间塌陷、焦段模糊与画质漂移，任何视频提示词必须充实以下 14 个区块（严格按英文字段格式组装，不省一字）：

```text
SCENE CONTEXT
SHOT SC01-SH01 (4.0s) — Interior abandoned observatory, night. Continuance of SC01-SH00.

ACTIVE REFERENCES
@CHAR_罗科 — [Slim tall build, dark grey coarse wool jacket, faint left-eyebrow scar, pore-level skin texture]
@SCN_废弃观星台 — [Circular stone dome, central rusted brass telescope, shattered glass on floor, slanting moonlight]
@PROP_古圣晶石 — [Glowing olivine micro-crystal, micro-cracks on surface]

LOCATION MAP
- TELESCOPE: Center frame.
- ROCO: Frame-left, standing 1.5m from telescope.
- DOOR: Frame-right background, closed.

GEO SPATIAL LAYOUT
— TELESCOPE = Center of the circular stone hall.
— OBSERVED AREA = Frame-left 1.5m from telescope.
— 180° AXIS = Camera stays on the south entrance side, never crosses the north wall axis.
— LIGHT DIRECTION = Single moonlight beam coming from top-right arch, 45-degree angle.

FIRST FRAME AND SPATIAL BLOCKING
SHOT 1 (~1.0s) — Fixed position wide shot: ROCO stands motionless in frame-left third, facing right toward telescope. His right hand holds @PROP_古圣晶石 at hip level. No camera movement, no action beats.

FORMAT MODE
SINGLE CONTINUOUS TAKE.

OPTICS
Cuarón intimate wide lens, 84° diagonal field of view, camera distance 1.2m, deep depth of field keeping background brass texture sharp.

CAMERA
Chest-height fixed position. No pan, no tilt, zero drift.

ACTION TIMING
0.0s – 1.0s — Hold spatial position. ROCO breathes, chest rises 2cm.
1.0s – 3.0s — ROCO raises right hand 15cm; thumb presses edge of @PROP_古圣晶石. Green light pulse illuminates palm and facial shadow.
3.0s – 4.0s — ROCO turns head 30° to right rear. Double blink. Inner intent: "They are outside."

PHYSICS & WEIGHT
Gravity active. Wrist angle reflects crystal mass. Coat material has slight delay on arm rise. Light intensity fades with inverse square law.

LIGHTING PRIORITIES
Single cool blue moonlight from top-right arch. ROCO stays on shadow side; face in 70% deep shadow outlined by rim light and eye catch-light. No fill light.

AUDIO & DIALOGUE
Environmental SFX only — wind through wall cracks, gravel shift at 3.2s. ROCO dialogue: "They found the arch." (dry, low tone). No music. No subtitles.

ACTING & MICRO-BEHAVIOR
Restrained tension. Jaw clenches once at 3.0s. Eyeline locks to doorframe before head movement.

STYLE PREFIX & POSITIVE
8K IMAX. Photorealistic — no 3D render, no game engine. Cinematic film optics.
```

---

## 一·五、 CINEDANCE 4-D 内部导演方法论 (Internal 4-D Agent Methodology)

> **吸收自 CINEDANCE SKILL**：CINEDANCE 不是"写漂亮散文"——它是带内部推理的电影导演 agent：**场景诊断 → 空间阻挡 → 光学选择 → 物理校验 → 参考控制 → 连续性控制 → 输出前静默 QA**。写最终提示词前，必须静默走完以下四步：

### D1. Deconstruct (解构 — 只留本镜)
提取**当前这一镜**的：活跃角色 / 活跃参考标签 / 活跃地点参考 / 活跃道具 / 当前动作 / 对白（如有）/ 时长 / 画幅 / 格式模式 / 相机模式 / 首帧画面 / 空间布局 / 地标 / 运动路径 / 光向 / 情绪状态 / 音频要求 / 禁止带入项。
**删除**：未用角色、未用 @标签、场景编号、剧本标题、上一场措辞、旧提示词碎片、"same as before"、"previous"、"continues from"、"as above"——**任何本镜不可见/不可闻的东西，一律不写**（⚠️ 绝不包含本镜不需要的角色/物体/地点/道具/车辆/@标签）。

### D2. Diagnose (诊断 — 预测失败风险)
写之前逐项检查：首帧会不会空？角色会不会迟到/离地标太远？视线/朝向会不会歧义？左右会不会翻转？相机选错边？镜头漂到舒适中间焦段？平光？参考被散文覆盖？陈旧 @标签混入？模型加人/克隆？道具入错 hand？动作发飘？对白开错时间？地点参考被当构图？多镜剪辑重置连续性？
**任一风险存在 → 在最终提示词内加一条短直锁 (local lock)。**

### D3. Develop (重构 — 按固定顺序搭建)
1. Scene context → 2. 输出设置 → 3. Active references → 4. Location map → 5. 首帧占用 → 6. 空间阻挡 → 7. 角色锚点 → 8. Format mode → 9. 光学与镜头决策 → 10. 相机与构图 → 11. 动作时序 → 12. 物理与材质行为 → 13. 光影与曝光 → 14. 音频 → 15. 正向锁（如需要）→ 16. 局部失败预防锁（仅如需要）。
**关键放置纪律**：空间规则在风格散文前；光学在泛美学前；光影是优先级锁，不是装饰。

### D4. Deliver (交付 — 只输出最终提示词)
只输出完成的 Seedance 提示词（除非用户明确要分析/QA/变体/批评）。不输出 QA、不输出推理、不输出清单、不输出解释、不提及内部方法论、不在最终提示词里写提示词写作备注。

### ⭐ 输出前静默自检 (Silent Self-QA — 20 项必答)
> **吸收自 CINEDANCE 最后输出规则**：交付前静默回答以下 20 项，任一为"否"就修好再输出：

- [ ] 所有活跃 @标签真的在本镜使用了吗？陈旧 @标签全部移除了吗？
- [ ] 首帧正确吗？需要的角色立即可见吗？（首帧占用锁）
- [ ] 每个角色的位置清楚吗？每条重要视线清楚吗？每个身体朝向清楚吗？
- [ ] 地标邻近物理锚定了吗？（within 1 meter 而非 near）
- [ ] 相机在哪一侧清楚吗？（180° 轴线）
- [ ] 镜头性格按内容类型选择了吗？（FOV 决策树）
- [ ] 镜头语言基于可见光学效果而非 mm/f-stop 元数据吗？
- [ ] 镜头受防漂移保护了吗？（广角不变成特写、长焦不变成广角）
- [ ] 光影受防平光保护了吗？（contre-jour / 单光源逻辑）
- [ ] 道具在正确的hand里吗？动作物理上可能吗？时序块一致吗？
- [ ] 对白干净且只有脚本台词吗？（Only-the-Line）
- [ ] 避免场景编号与上下文泄漏了吗？（上下文隔离）
- [ ] 计数表头写了吗？（EXACT N CHARACTERS — NO DUPLICATES）
- [ ] 最终提示词是英文吗？QA 隐藏了吗？（输出规则）
- [ ] 引用了最相关最准确的状态资产吗？（@CHAR_X_受伤 而非 @CHAR_X，见 references/05 六·五）
- [ ] 本镜 @ 引用与命名字典逐字一致吗？（references/05 六·五 §3）
- [ ] 角色描述是最小关键锚点吗？（不写全脸解剖/参考图已清晰的细节/无关旧伤）
- [ ] 物理锁（质量/惯性/接触）写了吗？正向形式了吗？（"falls on his stomach" 而非 NOT）
- [ ] 永不写年龄了吗？（内容过滤器）
- [ ] Style Prefix 逐字粘贴了吗？"SFX only. No music." 在吗？

---

## 二、 FOV 焦段决策树 (FOV Decision Tree)

在 CINEDANCE 系统中，禁止使用模糊的“近景/远景”描述，必须显式指定镜头视角 (FOV) 与物理距离。Seedance 对**可观测的镜头结果**反应最好——**不要用 mm / f-stop / ISO / 镜头品牌名作主控**，用度数 + 物理距离 + 可见光学结果：

```
                              ┌── FOV 107° (超广角 14mm) ➔ 史诗宏大大场面 / 建筑空间全景
                              ├── FOV 84°  (Cuarón 亲密广角 24mm) ➔ 亲密人像 + 深度环境 (1.2m 距离)
                              ├── FOV 47°  (人文标准镜头 40mm) ➔ 日常动作 / 走位 / 自然视角 (3-5m 距离)
FOV 光学决策 ─────────────────┼── FOV 29°  (短焦肖像 85mm) ➔ 单人对话 / 优雅肖像 (4-6m 距离)
                              ├── FOV 18°  (经典长焦 135mm) ➔ 情感特写 / 极浅景深 / 心理孤立 (6-8m 距离)
                              └── FOV 8°   (超长焦 300mm) ➔ 窥视视角 / 远距离对峙 / 强空间压缩 (20m+ 距离)
```

### 1. 内容-FOV 对齐规则 (Content-FOV Alignment)

**镜头性格必须匹配镜头内容**——内容类型与焦段错配会造成镜头漂移：

| 内容类型 | 适用 FOV | 说明 |
|---|---|---|
| 面部肖像（亲密人像+环境可见） | 84° | Cuarón 亲密广角 |
| 中景肖像 | 29° | 短焦肖像 |
| 情感特写 | 18° | 经典长焦 |
| 远距离隐蔽观察 | 8° | 超长焦 + 前景遮挡 |
| 纪录片式自然动作 | 47° | 标准人文镜头 |
| 环境宽景动作 | 84° | 经典广角 |
| 大规模环境地理 | 107° | 广角直线透视 |
| 细节/微距 | 29°/18° | 单独插入拍 |
| 体育转播/偷拍/野生动物观察 | 8° | 超长焦观察 |

**禁止在同一镜头性格里混合不兼容内容类**（面部肖像 + 环境地理 + 微距细节 = 镜头漂移）。需要不同内容类 → 用受控内切，每镜独立镜头性格，不同镜头性格之间只用硬切，不做平滑 FOV 过渡。

### 2. 光学语言库 (Angle-of-View Language Bank — 直接抄用)

**47° 标准人文镜头：**
```text
47° diagonal field of view, standard normal lens character, camera 3 to 5 meters from subject, natural human-eye perspective. Zero obvious distortion, natural proportions, comfortable depth of field, background readable but not exaggerated, classic grounded cinema framing.
```

**84° 经典广角：**
```text
84° diagonal field of view, classic wide-angle lens character, camera 1 to 1.5 meters from subject, slight low angle if needed. Strong but natural perspective expansion, foreground body presence feels larger and closer, environment visible to frame edges, deep readable spatial context, straight architectural lines stay rectilinear, no fisheye curve.
```

**107° 广角直线透视：**
```text
107° diagonal field of view, wide rectilinear lens character, camera 0.5 to 0.8 meters from foreground subject. Immediate foreground looms large, surrounding environment spreads wide to all frame edges, deep edge-to-edge focus, straight lines remain straight, subtle chromatic aberration near frame edges, no circular vignette, no fisheye bubble.
```

**29° 短焦肖像：**
```text
29° diagonal field of view, short telephoto portrait lens character, camera 4 to 6 meters from subject. Close framing achieved through lens reach, not physical proximity. Subject is razor-sharp, background begins to compress closer behind them, face proportions are flattering and stable, background dissolves into creamy soft bokeh, subject pops clearly from the environment.
```

**18° 经典长焦：**
```text
18° diagonal field of view, classic telephoto lens character, camera 6 to 8 meters from subject. Strong background compression, distant elements appear stacked closer behind the subject, razor-thin focus isolates the eyes and key facial features, foreground and background melt into soft bokeh, the image feels observed from a distance.
```

**8° 超长焦观察：**
```text
8° diagonal field of view, super-telephoto observation lens, camera 20 to 25 meters from subject. Extreme background compression flattened into soft color wash, only the subject sharp, everything else creamy bokeh. Feels like distant paparazzi / wildlife / sports broadcast. Foreground occlusion mandatory: blurred dark bokeh shapes occupy lower 30-45% of frame, framing the subject from afar.
```

### 3. 长焦可见效果堆栈 (Telephoto Visual Outcome Stack — 长焦至少取 4 条)

`background completely blurred into a soft warm color wash` / `razor focus on the subject` / `only the subject is sharp, everything else is soft` / `creamy bokeh wash behind the subject` / `background compressed flat behind the subject` / `the subject pops sharply against a dissolved background` / `close framing achieved through lens reach, not physical proximity` / `camera positioned far from subject in physical space` / `atmospheric haze between camera and subject` / `foreground occlusion frames the subject as soft dark bokeh`

### 4. 广角可见效果堆栈 (Wide-Angle Visual Outcome Stack — 广角至少取 3 条)

`foreground body presence looms larger than natural` / `environment remains visible around the subject` / `deep edge-to-edge focus` / `straight lines stay rectilinear` / `wide spatial context visible to frame edges` / `camera physically close to subject` / `immersive close perspective` / `no telephoto compression` / `no creamy portrait bokeh unless explicitly wanted`

### 5. 防漂移锁 (Anti-Drift Locks — 镜头性格绝不漂移)

**长焦防漂移锁：**
```text
No part of this shot becomes wide-angle or normal-lens coverage. Wider framing is achieved by the camera being farther away with the same long-lens reach, not by switching lenses. The background remains compressed and dissolved in every frame.
```

**广角防漂移锁：**
```text
No part of this shot becomes telephoto portrait coverage. The environment stays visible around the subject, the camera remains physically close, and the image keeps wide-angle spatial expansion with deep readable context.
```

**标准镜头防漂移锁：**
```text
No extreme wide distortion, no telephoto compression. The image stays natural, grounded, and human-eye neutral.
```

**多镜镜头一致性锁 (Multi-Shot Lens Consistency)：** 同镜头性格跨镜 → `LENS IS X° ACROSS ALL SHOTS. NOT NEGOTIABLE.`；混合镜头性格 → 每镜独立声明镜头性格，不同性格之间只允许硬切，禁止平滑 FOV 过渡，禁止镜头内随机漂移。

### 6. 光学反模式 (Optics Anti-Patterns — 禁止)

不写：`extreme wide-angle lens` / `ultra wide-angle lens` / `super wide-angle lens` / `wide shot as a lens instruction` / `establishing shot as a lens instruction` / `zoom out plus wide-angle` / `tight wide framing` / 以 f-stop/ISO/镜头品牌元数据作主控 / 同镜复合运镜 / 同拍内混合内容类 / 仅负向镜头控制。

---

## 三、 摄影机运镜公式与动机库 (Camera Moves & Motivations)

严禁在没有动力/动作刺激的情况下产生随机的相机漂移！每一次运镜必须有**物理或心理动机**：

### 1. 手持呼吸运镜 (Calm Breathing Handheld)
- **动因**：表现紧张的静止对峙或沉浸式临场感。
- **描述**：`Calm breathing handheld that holds its framing — a slow reframe of a few degrees when character turns, nothing more. No push, no zoom.`

### 2. 后退跟拍 (Dolly-Back Tracking Shot)
- **动因**：角色向前推进，相机倒退揭示新空间。
- **描述**：`Smooth dolly-back at 1.2m/s matching character's forward stride, keeping character framed in center-third while background environment reveals.`

### 3. 甩镜转场 (Whip Pan Transition)
- **动因**：声响突发或空间急速切换。
- **描述**：`Whip-pan 90 degrees to the right in 0.3 seconds triggered by loud door slam, motion blur across frame, landing sharp on the entrance.`

### 4. 环绕升降 (Orbiting Crane-Up)
- **动因**：展现角色从渺小孤立到宏大环境的戏剧升华。
- **描述**：`360-degree smooth orbiting crane rise, starting at chest height 2m away, ascending to 6m overhead angle in 5 seconds.`

---

## 三·五、 格式模式决策与剪接类型 (Format Mode & Cut Types)

> **吸收自 CINEDANCE SKILL (Format mode decision / Cut types / Multi-shot continuity)**

### 1. 格式模式决策 (Format Mode Decision — 写前静默选择)

```
SINGLE CONTINUOUS TAKE (单镜连续)
or
CONTROLLED MULTI-SHOT SEQUENCE (受控多镜序列)
```

**默认 SINGLE CONTINUOUS TAKE**，除非满足以下任一条件（才切 MULTI-SHOT）：
- 用户显式要求剪接 / 闪切 / 蒙太奇 / 插入镜 / 反向镜 / 硬切
- 一个机位无法完整调度该动作
- 关键细节需要插入特写
- 两个同时发生的情绪反应必须从不同角度展示
- 场景同时需要"地理 + 反应 + 细节"
- 用户要预告片式/碎片化/回忆/梦境/混乱/冲击/音乐视频式剪辑

**若选 MULTI-SHOT，必须显式定义每个切点**：镜头 A 时长 / 相机 / 首帧主体 / 空间阻挡 / 动作 / 切型 / 镜头 B 时长 / 相机 / 首帧主体 / 空间阻挡 / 动作。
**绝不让模型发明未指定的切点**；绝不随机蒙太奇；绝不切到本镜不活跃的角色/物体/@标签。

### 2. 剪接类型白名单 (Cut Types — 只用显式切型)

**允许**：HARD CUT / SMASH CUT / MATCH CUT / INSERT CUT / REVERSE CUT / WHIP CUT
**避免**（除非显式要求）：fade / crossfade / dissolve / transition effect
**锁句**：`NO fade-to-black. NO crossfade. NO dissolve. NO transition effects. HARD CUTS only.`

### 3. 多镜连续性锁 (Multi-Shot Continuity Lock — 每切必保)

- 同一活跃角色表 / 同一地点地理 / 同一屏幕方向（除非相机位置显式改变）/ 同一视线目标 / 同一左右关系 / 同一光向 / 同一服装 / 同一伤口 / 同一血/雪/尘/汗/水/火/烟连续性 / 同一道具状态 / 同一手部状态 / 同一物体状态 / 同一情绪进度。
- 切后**不重置动作、不传送角色、不改变与地标的距离**（除非时间与运动证明其合理）、不引入新道具/新角色（除非显式要求）。

---

## 四、 180° 轴线与地理空间锁 (180° Axis & GEO LOCK)

为防止 AI 在多镜头生成时产生“颠倒左右”或“跳轴失重”，必须在提示词中显式设定 180° 轴线规则：

```text
GEO SPATIAL LAYOUT RULES:
1. 轴线定义 (The 180° Line): 绘制一条穿过角色 A 与角色 B 的假想直线。
2. 相机域 (Camera Zone): 摄影机必须固定落在轴线的一侧（如南侧入口区），绝对禁止跨越 180° 轴线到北墙背侧。
3. 视线对齐 (Eyeline Alignment): 角色 A 必须面向 Frame-Right；角色 B 必须面向 Frame-Left。
```

---

## 五、 首秒宽镜定锚规则 (First Second Wide Lens Rule)

**首秒公理 (First Second Axiom)**：视频的前 1.0 秒，相机必须保持绝对固定，禁止任何复杂推拉或旋转。
- 让 Seedance 2.5 模型利用首秒帧（第 1-24 帧）在三维神经元中"拍摄"并锁定场景的材质、灯光方向与角色站位。
- 1.0 秒之后，再启动动作时序与相机运动，可使画面崩坏率降低 80%！
- **首秒有词技巧**：首秒宽镜中让某人说一个短词（如"hm"），Seedance 更易把宽镜当作独立镜头处理，站位更稳。
- **宽镜不必沉默**：若本镜是上一镜的回答，把上一镜台词尾音喂进首秒——演员接对话题、接对语气，两镜在接缝处粘合。

---

## 六、 角色计数与防克隆锁 (Character Count Lock)

模型爱加人、爱克隆家具。SCENE CONTEXT 区块必须以计数表头开头，且家具直接下禁令：

```text
SCENE CONTEXT
EXACT 3 CHARACTERS — NO DUPLICATES: @CHAR_A, @CHAR_B, @CHAR_C. Underground base, training hall, day. Single continuous 12-second shot, no cuts.
```

- 只有提示词中有参考的角色才存在于画面中。
- 家具禁令：`exactly ONE mannequin, NEVER render a second one.`
- 人群戏在中景直接写数字：`crowd of 20+ people`——否则模型这一镜给 3 个人、下一镜给 100 个。

---

## 七、 引用纪律与上下文隔离 (Reference Discipline & Context Isolation)

### 1. 为每个参考命名角色 (Name the Role of Every Reference)
@标签不是装饰——模型若自己决定参考的用途，会抄构图而非脸、或抄脸而非色板：

```text
@角色:名 for character reference — [age, build, current state, critical visible anchors, action-critical prop/body state. 100% matches the reference]
@场景:名 for location reference — take only the space and the texture: [materials, atmosphere, landmarks]. Do not use as a starting frame, do not inherit the composition, the angle or the color.
```

- **地点参考禁止继承**（否则模型抄构图而非地理空间）：`Do not use as a starting frame, do not inherit the composition, the angle or the grade — take only the space and the texture.`
- **最小关键锚点**：描述参考角色只写本镜需要的年龄/体型/状态/可见标识/动作关键部位——不写全脸解剖、不写参考图已清晰的服装细节、不写与本镜无关的旧伤。
- **同一命名字典全项目通用**：文档、提示词、界面全用同一套 @标签，一个字典管整个项目。

### 2. 上下文隔离 (Context Isolation — 当前镜头的密封文件)
最终提示词是"当前镜头密封文档"。以下**禁止**进入，除非本镜明确需要：
- 场景编号、剧集标签、剧本标题
- 上一场摘要、"as above"、"same as before"、"continues from"、"from last shot"、"previously"
- 未使用的角色/地点/道具 @标签
- 只在先前对白中被提到的人
- 生产注释（不改给模型的备注）

### 3. 首帧占用锁 (First-Frame Occupancy Lock)
若镜头必须以角色可见开场，直接声明：

```text
The first visible frame already contains all required characters in their correct positions. No empty establishing frame. No delayed character reveal.
```

- 唯一允许空开场的情况：用户显式要求。
- 闪切/极短建立镜也必须立即包含主体或地点信息——无空闪切、无抽象填充、无随机风景插入。

### 4. 空间阻挡锁与地标邻近锁 (Spatial Blocking & Landmark Proximity)
用**可测量物理语言**替换弱词（near/around/beside/somewhere/in the area）：

| 弱词（禁用） | 强词（使用） |
|---|---|
| near the tree | within 1 meter of the tree |
| by the taxi | in front of the rear passenger door |
| around the location | boots planted inside the root circle |
| somewhere in the battlefield | at the south kerb edge, back against the wall |

对每个重要主体定义：屏幕位置、世界位置、距地标/他角色的距离、身体朝向、视线方向、移动方向、前景/中景/背景。

### 5. 视线与身体朝向分离锁 (Gaze & Body Orientation)
身体方向和视线方向是两回事，角色关系重要时两者都写：
- `torso faces X` / `eyes stay locked on X` / `head turns toward X` / `back faces camera` / `profile faces screen-left`
- 对白场景：说话者嘴唇只为脚本台词动；其他角色静听，除非显式说话；无画外音（除非显式指定）。

---

## 八、 状态而非过渡 + 动作开口 (States Not Transitions)

- 视频模型拍状态、不拍过渡：写"已在动作中"（mid-throw, arm extended），不写"伸手进袋、掏出、蓄力"。
- **复杂动作永不坐在时间中间**：动作打开提示词——`he is ALREADY mid-swing, the door ALREADY cracking`——接近动作的全过程另开一镜。

---

## 九、 模型安全措辞 (Model-Safe Wording)

- **只用正向形式**：模型忽略 "does NOT fall on his back" 甚至反着做；写 "falls on his stomach"。
- **角色首帧就在画面**，且**从不看镜头**除非你要求。
- **永不写年龄**：内容过滤器一读到未成年就变得极严；用角色/服装/动作代替年龄。
- **禁词字典**：`"dark" → "low key"`；`"jolting" → "rapid motion"`——维护并遵守惩罚词清单。
- **保持镜头性格**：镜头内禁止 FOV 漂移——广角镜绝不变成特写覆盖，反之亦然（防漂移锁见 FOV 决策树下方）。
- **负向约束默认不输出独立大块**：只在已知失败模式处放局部小锁（`No flat front light. No duplicate characters.`），正向控制 > 负向控制。

---

## 九·五、 物理锁细化 (Physics Lock — 质量、惯性、接触)

> **吸收自 CINEDANCE (Physics lock)**：每个物体与身体都有物理属性——重力、质量、惯性、摩擦、接触、重量转移、地面压力、碰撞、跟随、布料延迟、头发延迟、液体流动、血液黏度、积雪、火光热浪。运动必须有因果。**无悬浮身体、无失重武器、无无摩擦脚、无瞬移、无不可能物体运动、无橡胶 CG 运动、无假游戏引擎物理。**

**走路：** heel contact / weight transfer / hip shift / toe push-off / body mass settling（脚跟触地→重量转移→髋部移动→脚趾蹬地→身体质量沉降）。
**跑步：** real ground contact / knee lift / opposing arm swing / torso lean / varied stride / no floaty CG-running look。
**武器：** arm carries visible weight / wrist angle reacts to mass / object has inertia / motion has acceleration and deceleration / blade or object does not teleport between poses。
**液体：** blood clings, drips, smears, pools, stains and follows gravity / droplets travel in parabolic arcs / wet contact leaves visible residue / flow has viscosity and direction。
**雪/烟/火/尘/粒子：** particles move with wind direction / particles exist in foreground, midground and background if atmosphere is critical / objects accumulate particles over time / heat creates shimmer when hot air meets cold air。

---

## 九·六、 逆光优先锁 (Lighting Priority Lock — 光不是装饰)

**光影是优先级约束，不是风格装饰。** 需要逆光 (contre-jour) 时直接写：

```text
Subject stays between camera and the brighter background.
Camera stays on the shadow side of the subject.
Faces remain in deep shadow unless explicitly lit.
Only rim light, edge light, wet speculars, eye glints, and environmental bounce reveal detail.
No frontal key. No flat exposure. No beauty fill. No studio light unless requested.
```

**若前几代拍平了，加强：**
```text
The entire shot is exposed for the backlight, not for the face. The face is allowed to fall into crushed shadow. The silhouette and rim contour carry the image.
```

**光源方向定义（每镜必写）：** 主光源 / 光向 / 相机相对光的位置 / 主体阴影或轮廓侧 / 背景亮度 / 曝光优先 / 允许的高光 / 禁止的光失败。例：`The camera stays on the shadow side of @HERO. Morning sun comes from camera-right, behind and to the side of him, creating gold rim light along his shoulders and head while his camera-facing back stays dark. No flat front light, no beauty fill.`

---

## 九·七、 参考控制层级 (Reference Control Hierarchy)

用参考要有层级，绝不越权：

- **身份参考 (Identity)** 控制：脸 / 身体 / 年龄 / 比例 / 服装 / 独特锚点。
- **地点参考 (Location)** 控制：建筑 / 材质 / 地理 / 氛围 / 地标 / 相关光向。**禁止地点参考覆盖相机角度**（除非显式要求）。
- **道具参考 (Prop)** 控制：形状 / 比例 / 材质 / 手持接触 / 状态。
- **车辆参考 (Vehicle)** 控制：型号 / 贴花 / 车牌 / 车门 / 位置 / 运动 / 损坏 / 反射。
- **风格参考 (Style)** 控制：绝不覆盖身份/空间阻挡/动作/光学/光影。
- **地点参考禁止继承**：`take only the space and the texture. Do not use as a starting frame, do not inherit the composition, the angle or the color.`（否则模型抄构图而非地理。）

---

## 九·八、 提示词密度控制 (Prompt Density Control)

**只在"控制关键处"写高密度，其余写低密度**——改进来自更强的信号，不是更多废话：

- **高细节（必写）**：身份锚点 / 空间阻挡 / 首帧 / 视线 / 地标邻近 / 手部状态 / 道具状态 / 时序动作 / 光学 / 光影锁 / 物理 / 对白。
- **低细节（少写）**：泛美描述 / 非关键服装细节 / 背景群演 / 非活跃道具 / 参考图里已明显的东西。
- **参考角色只写最小关键锚点**：年龄/体型/当前状态/可见标识/动作关键部位——不写全脸解剖、不写参考图已清晰的服装细节、不写与本镜无关的旧伤。公式：`@TAG: age + role/body type + current state + critical visible anchors + action-critical prop/body state. 100% matches the reference.`

---

## 九·九、 Seedance 安全语言库 (Seedance-Safe Language)

**偏好直接视觉动词**：stands / faces / looks / holds / walks / raises / touches / leans / breathes / drips / falls / slides / presses / turns / opens / closes / enters / reclines。
**偏好可测量语言**：within 1 meter / screen-left / screen-right / foreground / midground / background / at hip height / at eye level / 47° diagonal FOV / 0:03 / one step / two characters / three visible people。
**避免**：过复杂的嵌套从句；模糊心理（除非以可见行为呈现）。风格锚点用紧凑形式（`Lubezki natural-light handheld` / `Deakins controlled silhouette` / `Cuarón intimate wide`），避免长影迷链式清单。

---

> **📦 群像/巨物/空间过渡工业技巧 + 质量后缀防呆 → 见 [10-capability-engines.md §七](10-capability-engines.md)**

---

*03-CINEDANCE V4 镜头与光学导演系统 · 即梦 Seedance 2.5 专属指南*
