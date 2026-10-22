# 04-ACTING SYSTEM 行为驱动表演系统 (Behavior Performance System)

> **核心公理 (The Core Axiom)**：  
> **表演是在假想情境下压力中的真实行为 (Behavior under pressure in imaginary circumstances)，绝非静态情绪 (Emotion) 的展示。**  
> 角色在镜头中想要得到某物 (Objective)，遭遇了障碍 (Obstacle)，并采取具体的行为战术 (Tactics) 去争取。情绪是拼搏的副产品，绝对不能在提示词中直接描写情绪形容词！
> **归属引擎**：叙事与导演引擎 (E1) + 声音工程引擎 (E5)（六引擎体系见 [references/10](10-capability-engines.md)）
> **角色丰富度**：主角瞄准量表 4+（活的），配角 2-3 级差异化处理——**所有角色绝不使用同一表演强度**，强者静弱者动、反应错峰（见 §十/§十一）；用户声音样本锚定 `@CharID_AUDIO_XX` 见 [references/11](11-user-asset-logo-placement.md)

---

## 一、 坏表演 vs 好表演 的提示词对比

| ❌ AI 假感坏表演 (Emotion Slop) | ✅ 大师级物理好表演 (Physical Action) |
|---|---|
| “他感到非常愤怒，大声喝彩” | “他下巴咬紧，左侧太阳穴肌肉抽搐一次，双唇紧闭，呼吸急促导致胸口起伏 3 厘米” |
| “她感到伤心流泪” | “她视线压低 10 度，下唇微微颤抖，微停顿 0.3 秒，随后急速眨眼两次” |
| “角色非常震惊” | “角色瞳孔放大，身体瞬间冻结 0.2 秒，右手握着的晶石因手指脱力向下滑落 2 厘米” |
| “他深情地看着她” | “他视线锁定她的左眼，头部向右微倾 5 度，眼神保持湿润高光，呼吸频率放缓” |

---

## 二、 ACTING SYSTEM 五大表演支柱 (The Five Pillars)

### 1. Objective (物理目标)
- 描述角色在镜头中通过物理行动想要达成的具体目的（用物理动词描述，如“逼对方退后”、“隐瞒右手的伤”）。
- 绝不能写心理状态，必须写可以被摄像机拍摄到的物理行动。

### 2. Obstacle & Stakes (阻碍与筹码)
- 阻碍：是什么在阻止角色获得目标？（如：重伤的右臂无法抬起、门外有敌人逼近）。
- 筹码：若失败会有什么后果？筹码越高，物理肌肉张力越强。

### 3. Tactics (行为战术)
- 战术是实现目标的具体手段（施压 ➔ 假装镇定 ➔ 拖延时间 ➔ 突然爆发）。
- 每次战术改变，必须伴随着微观动作的改变。

### 4. Beats (动作节拍切片)
- 将 4 秒或 12 秒的镜头划分为微观节拍（Beats），每个节拍对应特定的物理时序：
  - `0.0s – 1.0s`：节拍 A (保持僵局，视线锁定)
  - `1.0s – 3.0s`：节拍 B (战术切换，试探性抬手)
  - `3.0s – 4.0s`：节拍 C (阻碍爆发，肌肉咬紧)

### 5. Subtext (潜台词 INNER)
- 物理动作背后隐藏的真正意图，在 Prompt 中以 `INNER: "..."` 标注，帮助 AI 注入微妙的面部肌肉张力。

---

## 三、 眼神生命 (Eye Life) 与眨眼分级解算

眼睛是 AI 画面中传达生命感的第一核心，僵硬的 AI 往往是因为“死眼”：

### 1. 瞳孔高光 (Catch-light Reflection)
- 瞳孔必须有湿润的自然反光（如：`wet living eyes with active catch-lights matching moonlight source`）。

### 2. 视线先导公理 (Eyeline Precedes Motion)
- 头部旋转前 0.2 秒，视线必须先于头部锁定目标。
- 描述：`Eyeline locks to the right doorframe 0.2s before the head rotates.`

### 3. 三阶眨眼分级 (Three-Tier Blink System)
- **Lazy Blink (懒散眨眼)**：表示犹豫、思考或疲惫。
- **Double Blink (双眨眼)**：表示震惊后的快速神经质重置。
- **Hard Reset Blink (重置眨眼)**：表示下定决心或掩饰慌乱。

---

## 四、 重力、质量与微停顿 (Gravity, Mass & Micro-Pauses)

### 1. 质量与重力延迟 (Mass & Weight Friction)
- 物体有质量时，举起物体的动作会拉低肩线，且手臂抬升速度有减速曲线。
- 描述：`The crystal sheathing his right arm has heavy mass, dragging his right shoulder 3cm lower than the left. Arm movement shows a 0.1s inertial delay.`

### 2. 生物微停顿 (Micro-Pauses)
- 人类在做出反应前，神经传递需要 0.1–0.3 秒的静止评估阶段。
- 描述：`Character experiences a 0.2s micro-pause upon hearing the noise before executing the head turn.`

---

## 四·五、 聆听与反应 (Listening & Reaction — 表演质量的试金石)

> **吸收自 ACTING SKILL (Listening and reaction — the main test of quality)**：表演不在台词里，而在台词之间。把以下真实聆听的可见标记写进场景：

1. **反应先于对方台词结束 (Reaction starts before the partner's line ends)**：一个人在对方说到一半时就懂了——脸和身体已经在回答。等对方说完才"开机"的表情 = 死表演。写法：`REIN's thumb STOPS on the glass, and only then her head turns to the door — the interrupted work is the accent of the beat.`
2. **先想后说 (Thought before word)**：回答难题前有微停顿——人显式地决定说什么。立即回答且匀速 = 背稿，无生命。写法：`a 0.2s micro-pause before he answers, the decision visible on his face.`
3. **评估时刻 (The assessment moment)**：重要事件（消息/威胁/侮辱）发生后，角色需要时间消化——从零点几秒到长停顿。电影活在特写里的评估：一张脸、失焦的目光、世界在晃动。写法：`the news lands; he holds one long beat, gaze defocused, processing — then answers.`
4. **对手传染 (Contagion from the partner)**：节奏/音量/能量随对手变化——一声吼要么被吼回去、要么被点名的安静压住——但总是"回应"，不是"压过去"。写法：`he answers the shout with pointed quiet, not volume.`

---

## 四·六、 身体的物理参数 (The Body's Physical Life)

> **吸收自 ACTING SKILL (The body: the character's physical life)**：身体在说第一句台词之前就把故事讲了。为每个角色设定以下参数：

- **重心 (Center of Gravity)**：高（胸/下巴——自信、攻击性、地位）或低（肩/塌——疲惫、恐惧、顺从）。
- **节奏 (Tempo)**：快/乱（紧张、兴奋剂能量）或慢/经济（控制、威胁——最危险的人动得最少）。
- **开放度 (Openness)**：肩正、掌开 vs 抱臂、低头、封闭姿势。
- **呼吸 (Breath)**：高而急促（恐慌）vs 低而慢（控制）。**呼吸是状态最诚实的指标**——刚跑完的人不可能平稳说话，声音与物理必须匹配（声画物理一致）。
- **事务 (Business — 手要有活干)**：角色不"闲聊"——他修引擎、数钱、擦杯子——边干活边说话。事务杀死虚假的舞台腔（手忙于真相）、制造场景节奏（停顿被动作填满）、生成潜台词（怎么数钱比说什么更动人）。**被打断事务规则 (The Interrupted-Action Rule)**：最强的重音是角色**停下手头的事**——切面包切到一半停住 = 那句话成了事件。用"停"做标点。
- **距离即戏剧 (Proxemics)**：亲密 <0.5m（爱或暴力，擅自进入是侵略；10cm 处的耳语比隔屋喊更可怕）、个人 0.5–1.2m（信任）、社交 1.2–3.5m（戒备/公事）、公共 >3.5m（疏离/层级）。**距离改变 = 节拍改变。**
- **地位即行为 (Status — 可见的隐形层级)**：高地位=头不动、动作慢、长凝视、答前停顿、占据空间、碰别人的东西；低地位=忙乱、频繁摸脸、破碎语言、陪笑、用眼神请示。最有趣的是**地位破格**：老板显露一秒恐惧；下属突然停止微笑。经典场景形状：高调入场然后崩落；低调入场然后掀翻全场。

---

## 四·七、 台词的艺术 (How Good Acting Sounds)

> **吸收自 ACTING SKILL (Speech)**：

- **节奏写在文本里**：精确交付——快 ≠ 含糊。
- **重叠正常**：台词踩着对方尾巴说，但关键词保持干净。
- **音量对比——最可怕的话说得最轻 (Volume contrast)**：吼叫是弱者的货币；掌控场景的人压低音量，所有人都凑过来。`The most frightening things are said the quietest.`
- **停顿是事件，不是洞 (Pauses are events, not holes)**：停顿合法仅当其中发生什么（评估/决定/拒绝回答）。
- **真实话语有杂质**：打断、半听清的话、重复、未完成短语——完美造句杀死街头真实感。

---

## 四·八、 ⭐ 微生命规则 (Micro-Life Rule — 静止不冻结)

> **吸收自 Hell Grind 制作简报 (Write physics, not adjectives)**：**一静帧内，每 1–2 秒必须有一个可见的微事件**——胸口的呼吸起伏、鼻翼翕动、眉毛一紧一松、一次吞咽。**把静止写成"被保持的紧张"，绝不写成"冻结"**——"nobody moves" 这类安抚性短语会把画面本身冻住。

- **微事件清单**：`the breath lifts the chest` / `a nostril moves` / `a brow tenses and relaxes` / `one lazy blink, a quick DOUBLE-BLINK, one HARD reset-blink` / `a slow swallow` / `fingers adjust grip by millimeters`。
- **静止 = 被保持的紧张 (Stillness as held tension)**：不写"他站着不动"，写"他像石像一样站着，只有喉咙在吞咽，指节慢慢收紧"。
- **情绪词禁写**：不写"sad/angry/shocked"——模型会即兴发挥出浅薄结果。写肌肉的功：颤抖、咬紧的牙关、颧骨绷紧、鼻腔轻呼。**在肌肉之上加意图**：每段动作为主角写一句内心独白（`INNER: "..."` 未说出口）。
- **凝视方向必写**：清晰的凝视方向或游离的眼睛——持续工作的微表情让脸更活。

---

## 五、 对白隔离与卡点铁律 (Dialogue Isolation)

- **物理动作描述中绝对不包含台词**！
- 任何台词必须且只能在 `AUDIO` 区块中以双引号指定，并附带声线特征与音效卡点：
  ```text
  AUDIO & DIALOGUE
  - Environmental SFX: heavy rain hitting stone floor, thunder rumble at 2.5s.
  - ROCO Dialogue at 3.0s: "They found the entrance." (Voice: low-pitched, gravelly, breathy, dry).
  - Constraints: Environmental SFX only. No background music. No subtitles.
  ```
- **台词唯一铁律 (Only-the-Line Rule)**：只允许引号内的脚本台词被说出——无额外词、无即兴、无字幕、无画外音（除非显式指定）、无旁白；不说话的角色嘴唇必须紧闭（`Lips are still when not speaking`）；写在动作里的"半笑/half-laugh"是面部表情，不出声。
- **对白构建四要素公式**：声音+情绪 → 引号台词 → 物理动作 → 面部反应。台词永远只住在 AUDIO 区块，动作与台词永不混写。
- **前后静默**：需要干净对白时，每句台词前后至少 1 秒环境静默（`at least 1 second of silence before and after each spoken line`）；若需立即开口，`line begins within the first 0.3 seconds`。
- **混音规则**：人声干净近麦、环境音垫底、说话时环境音自动压低 (ambience ducks under dialogue)。
- **罕见人名附音标转写**：否则模型会读破名字。
- **剪辑缝技巧**：宽镜对白中把上一镜台词尾音喂入本镜（帮助唇形与节奏）；每个新生成用上一镜收尾那句开头——情绪随文本一起跨过接缝。

---

## 六、 角色表演大师档案 (Character Acting Master Profile)

每个常驻角色必须建立 **一份永久表演档案**（150–220 词、英文、单段流畅散文、全部可观测可拍摄），它是"这个角色如何行动"的唯一真相源。写成一次，每场戏重写适配（见第七节），**永不整段复制粘贴**。

**模板（块顺序固定）**：
```text
Character acting as [NAME]. [年龄/体格/姿势——身体是履历的档案]。
[心理引擎一句话——解释身体性的内在驱力]。
Vocal profile: [音高/音色、口音/出身、语速与表达方式、情绪下声音如何破/变]。
Key physical habits and tics: [招牌小动作+触发条件；压力小动作+触发条件；隐藏行为——
他们用什么隐藏感受；面部面具 + 面具在什么确切条件下碎裂]。
Walking style: [为步态命名并拆解——重量/节奏/脚位/躯干手臂头的动作]。
However, when [情绪触发器], [转变——姿势/步态/脸如何变化]。
[可选：软化目标——唯一让脸真正柔和的人/物]。
```

**写作规则（吸收自 Hell Grind ACTING 系统）**：
1. **只写可观测行为**：绝不写"他很紧张"，写"下唇颤抖、喉咙重咽、长吸气"。每个内在状态必须有一个身体标记。
2. **每个小动作有触发**：格式 = [小动作] + [何时/为何]。"他谈话时掰指节装自信" > "他掰指节"。无触发的小动作是装饰，有触发的是剧作。
3. **为步态命名**：可记忆的杜撰名（"power-walk"、"peacock strut"、"battering-ram stride"）锚定生物力学，再拆解。
4. **面具 + 裂缝（必含）**：每个档案必须至少一条 `However, when X — ...` 从句：主导的威压步态在被拒绝时碎成孩童式垮肩；大嗓门在提到家人时闪过恐慌。同时扮演两种真相 = 人 vs 木偶的分界线。
5. **一个软化目标**：仅一个人/动物/物件让脸真正柔软，一个——不是两个。
6. **不含服装/不含镜头/不含色彩**：服装在场景块，镜头光影在其他区块；档案必须能扛住任何换装。
7. **体格携带履历**：职业、旧伤、自我形象必须能从身体里读出来。

---

## 七、 场景适配：重写而非粘贴 (Scene Adaptation)

大师档案是角色"是谁"；每场戏必须**重写进当下**，而非整段粘贴：

1. **只写在场角色**：画面里没有的角色 → 不写段落。
2. **保持恒定内核**：身份、声线档案、招牌小动作、眼活、情绪主线跨场不变——这是跨切一致性所在；绝不与大师档案矛盾。
3. **为本场重新表达**：选择/强调/修改/删减具体行为以适配本场姿势（坐/站/跑/藏）、动作节拍、情绪状态与时段。
4. **转移而非删除 (Transform, don't delete)**：本场物理上无法发生的行为要"转化"而非移除——焦虑踱步者瘫坐沙发时，把同样的神经引擎转移为微摇、弹指、撕纸。能量恒定，出口变化。
5. **单段流畅散文**：折叠成角色语气的散文，不用列表、不用标题。
6. **以角色参考标签开头**：`@角色:名 — ...`，让模型把表演绑定到正确的人。

---

## 八、 状态而非过渡 (States, Not Transitions)

视频生成模型**拍状态拍得好、拍过渡拍得差**。描述角色"已在动作状态中"（mid-throw, mid-punch, mid-pace, mid-argument），而非到达该状态的过程（"伸手进袋、掏出、蓄力"会崩；"mid-throw, arm extended"能落地）。逐拍串联状态，而不是叙述连续过程。

**复杂动作永不坐在时间中间**：动作要打开提示词——"he is ALREADY mid-swing, the door ALREADY cracking"——接近门的全过程是另一个镜头。

---

## 九、 坏表演图集 (Atlas of Bad Acting — 15 条识别与修复)

| # | 症状 | 表现 | 提示词级修复 |
|---|---|---|---|
| 1 | 示意式表演 (Indication) | 脸"表演"情绪：挑眉、做鬼脸 | 把脸从任务中移除；写目标 + 给手找活干 |
| 2 | 演结果 (Playing the result) | 从第一秒就演结局 | 只写角色此刻知道的事 |
| 3 | 等提示 (Waiting for cue) | 对方说话时脸是空的 | 写反应从对方台词中途开始 |
| 4 | 单战术 (Monotactics) | 整场一个色调（全程喊/全程哀求） | 标记节拍；每个节拍换一个新战术动词 |
| 5 | 手势图解 (Gesture illustration) | 手势重复台词（说"大"就张开双臂） | 手势要么先于思想、要么与话语矛盾、要么缺席 |
| 6 | 廉价情绪 (Free emotion) | 无铺垫无触发的眼泪/暴怒 | 建阶梯：克制 → 崩裂；情绪必须有代价 |
| 7 | 身体违背传记 | 混混有舞者姿势；瘾君子皮肤光鲜 | 设定身体档案：重心/节奏/磨损 |
| 8 | 台词太干净 | 街头角色说书面语 | 污染台词：打断、吞尾音、重复 |
| 9 | 威胁信号 (Threat signaling) | 暴力前"阴森"停顿/眯眼/慢转身 | 威胁是日常的；暴力无预兆降临 |
| 10 | 群演同步 (Synchronized ensemble) | 所有人同一瞬间同样反应 | 反应如波浪错峰：一个先懂，一个半拍后，一个没懂 |
| 11 | 死停顿 (Dead pauses) | 沉默里什么都没发生 | 填评估或事务——或删掉 |
| 12 | 情绪重置 (Emotional reset) | 强事件后角色瞬间"恢复" | 状态有惯性：余波拖入下一拍 |
| 13 | 评论角色 (Commenting the role) | 表演向观众眨眼（"我们俩都知道这很好笑"） | 完全相信情境；喜剧用死严肃演 |
| 14 | 特写过载 (Close-up overload) | 特写上还在大幅表演 | 景别越紧，动作越少：只有眼睛和思想 |
| 15 | 死眼 (Dead eyes) | 冻结凝视、无眨眼、无扫视、眼光呆滞 | 完整应用第三节眼活——眼活永不是可选项 |

---

## 十、 表演量表 0-5 (Performance Scale — 自检)

- **0 模特 (Mannequin)**：念出台词，行为缺席。
- **1 朗诵者 (Declaimer)**："有表现力"的台词、示意情绪、图解式身体。
- **2 勤恳者 (Diligent)**：能猜出目标，但单一战术、反应迟缓、空停顿。
- **3 匠人 (Craftsman)**：有目标有节拍、倾听对手、身体合理。缺：潜台词、意外战术、状态惯性。
- **4 活的 (Alive)**：连续行为、对比战术、潜台词偏离台词、地位在身体里、反应先于台词、至少一个"意外但真实"的选择。**所有主角戏瞄准 4+。**
- **5 磁石 (Magnet)**：4 的一切 + 悖论——角色同时是搞笑且吓人、残酷且迷人、说谎且动人。**双真相规则 (Two-Truths Rule)**：5 级角色永远同时扮演两种真相（帮忙——且怨恨；道歉——且防御；爱——且已离开）。单一无矛盾的情绪在特写上读起来是合成的。

---

## 十一、 群像与空间表演法则 (Ensemble & Space)

- **群像反应呈波浪传播，绝不同步**：一个人先懂笑点，第二个人慢半拍，第三个人完全没懂。同步的相同反应 = 假（除非刻意编排的喜剧同步）。
- **反应比动作更值钱**：每个事件之后最有价值的画幅是"看见它的人的脸"。
- **威胁冻结 (Freeze at the threat)**：群体持续微动（换重心/打手势/倾身），关键威胁到来时一切 STOP。喧闹 → 静止的对比就是标点。
- **移动 = 动机**：没人无内心冲动而穿房间——朝向某物或逃离某物。动机化事件：逼近（升级）、转身背对（否认/藏脸）、站而对方坐（夺权）、冲突中坐下（悖论权力）、停在门口（门槛=决定点）、开始收拾（身体发出的最后通牒）。
- **强者静止沉默；弱者烦躁叫喊**：危险不是由危险者演出来的，而是由周围人的紧张演出来的。暴力无预兆、无"蓄力"。
- **退化累积 (Degradation accumulates)**：角色被故事磨损，身体要累积携带——更灰、更重、反应更慢，绝不在场间重置。
- **距离即戏剧 (Proxemics)**：亲密 <0.5m（爱或暴力，擅自进入是侵略）、个人 0.5–1.2m（信任）、社交 1.2–3.5m（戒备/公事）、公共 >3.5m（疏离/层级）。距离改变 = 节拍改变。
- **地位即行为 (Status)**：高地位=头不动、动作慢、长凝视、答前停顿、占据空间；低地位=忙乱、频繁摸脸、破碎语言、陪笑、用眼神请示。最有趣的是**地位破格**：老板显露一秒恐惧；下属突然停止微笑。

---

## 十二、 声音锁定 (Voice Lock — 与画面同等重要)

- **声音不是资产**：Seedance 在一种语调内为每个角色持有 3-4 种声音——足够一部长片，但前提是你管理声音。
- **前期锁定**：在对话开始前的预制作阶段锁定每个主角的声音（音域/语速/口音/举止）。声音提示词**逐字粘贴**进音频栏，每次角色开口都用，**永不修改**。
- **VOX LOCK 跨镜一致性锁定**：六维音色建模 + 用户声音资产双轨锁定：
  ```
  VOX LOCK: [角色名] 声音 = "低沉干涩"（六维音色描述）
  同一角色在 [争吵/突变] 场景下：语气词变化 + 声调升高，但音色指纹不变
  用户声音样本：@CharID_AUDIO_XX 逐字锚定，全项目不漂移（见 references/11）
  ```
- **声音压测**：与外貌压测同样方式测试声音跨代保持——若漂移，回头把措辞锁得更死。
- **声音提示词公式（1-2 句，引号内）**：
  ```text
  "A [age]-year-old [origin / accent descriptor]. [Timbre and register];
  [pace and delivery manner]; [emotional character — and how it shifts under pressure]."
  ```
- 例：`"A 60-year-old ex-boxer and night-cab driver, working-class city accent. Low, hoarse, unhurried baritone; short flat economical sentences with long comfortable pauses; calm and faintly amused, going quieter — never louder — as things get serious."`
- 档案内的声音档案（第六节 Vocal profile）描述语速转变/破音/低语等戏剧性行为；音频栏的 Voice prompt 锁定声音本身。两者必须互相一致。
- **同期声锁**：图生视频默认只生成同期声（台词/音效/声音特效），不生成音乐：`SFX only. No music. No BGM.`（除非用户显式要求配乐）。

---

## 十三、 表演发送前清单 (Pre-Send Acting Checklist)

> **吸收自 ACTING SKILL (Pre-send checklist)**：任何含表演的镜头交付前，逐项确认：

- [ ] 画面内每个角色都有目标吗？（以针对特定对手的动词表述，绝非状态词）
- [ ] 阻碍与筹码存在吗？失败的代价真实吗？
- [ ] 2–4 次节拍变化，且每次都以可见行为呈现（停顿/姿势/节奏/凝视）？
- [ ] 反应在对方台词中途开始了吗？评估时刻在场吗？（四·五）
- [ ] 每个角色都有"事务"吗？被打断事务的重音被有意使用了吗？（四·六）
- [ ] 距离在变化且变化有动机吗？地位在身体里而非只是台词里吗？（四·六）
- [ ] 所有小动作都有触发吗？面具带裂缝吗（"However, when X..."）？（§六）
- [ ] 眼活显式写了吗：扫视、眨眼质量、瞳孔高光、眼先于头？（§三）
- [ ] 角色说话时 Voice prompt 逐字粘贴了吗？沉默角色省略了吗？（§十二）
- [ ] 状态而非过渡；表演里不含服装/镜头/色彩？（§八 + §六规则 6）
- [ ] 群像反应错峰了吗？强者静弱者动了吗？（§十一）
- [ ] 量表自检：这段表演能得 4+ 吗？（§十）
- [ ] 微生命规则：静止处有微事件吗？情绪词换成肌肉描写了吗？（四·八）

---

*04-ACTING SYSTEM 行为驱动表演系统 · 即梦 Seedance 2.5 专属指南*
