---
name: "ugc-zhi-shi-bo-zhu-kou-bo-guang-gao-feng-ge"
description: "以权威专家视角与硬核干货拆解，结合知识可视化与专业口播光，打造高信任度商业种草。"
version: "4.1"
display_name: "知识博主口播广告风格"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
video_model: "Seedance_2.5"
image_model: "gpt_image_2"
---

> ### 🚨 【系统默认铁律 · 全程无音乐 · 同期声优先（No-BGM Default · 最高优先级）】
> 1. **默认无 BGM**：所有视频/图生视频（I2V / Multi-Ref I2V）提示词**默认不生成任何 BGM/配乐/背景音乐**，且提示词**末尾必须显式追加约束**：`不生成音乐 / no bgm`。
> 2. **同期声必须正常准确**：去音乐 ≠ 去声音——角色对白、环境音、动作音效、声音特效（Foley）**必须正常、准确、完整生成**，严禁因禁乐而整体静默或削弱音效。
> 3. **唯一解除条件**：仅当**用户明确要求**音乐/配乐时方可临时生成音乐（用户要求优先准则）。
> 4. **弹性条款（音乐类技能自适应）**：若本技能以音乐为作品本体/核心表达（如 MV/歌舞/音乐舞蹈/卡点编舞/默片配乐），则音乐照常生成，视频提示词改标注音乐属性（曲风/BPM/情绪/卡点节拍）替代 `no bgm`；纯展示/口播等非音乐本体镜头仍不铺无关 BGM。


> ### 🚨 【系统默认铁律 · 视频提示词 AU 角色微表情强制注入准则】
> 1. **默认强制性**：在图生视频（I2V）与多参视频生成阶段，涉及**角色**（如知识博主 `@CHAR_EXPERT`）的提示词**必须默认带有角色 FACS/AU 精准微动作描述词**（AU 编号、解剖学肌肉位移、`A~E` 级量化强度、`0.2s 视线先导`、`AU45 眨眼抑制`）。
> 2. **豁免条件**：**除非用户在交互中明确声明"不需要表情"或"无微表情"**，否则默认所有涉及有人格属性的角色镜头均**无条件全量携带**。
> 3. **特异性智能转译（知识/图表专属）**：知识图表/白板/产品无人类面部主体，故该类镜头 AU 规则**强制转译为"知识可视化动力学"**（图表呈现/白板书写/数据动画/产品演示），并显式声明 `[本镜无角色面部主体，AU 自动转为知识可视化动力学]`；纯场景空镜转为"环境动力学"。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：知识博主（`@CHAR_EXPERT`）、场景（`@SCN_STUDIO`）、产品（`@PROD_ITEM`）、知识图表道具（`@PROP_CHART`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成（博主须同一面部骨相；产品/图表须同一款式、同一 UI 100% 一致，严禁漂移失真）。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **知识口播种草铁律**：知识博主口播广告的核心是"用专业干货讲解 + 知识可视化把产品转化为可信任的知识种草"——必须通过专业口播光、四段式知识叙事、专业可信表演、知识可视化动力学、清晰口播，制造可信任知识种草，严禁伪科学虚假科普、无资质背书、专业知识误导、绝对化权威与软广不标注。
> ### 🚨 【钢人论证补丁 · 知识科普合规铁律（Bidirectional Steelmanning Fix · 伪科学红线 + 资质背书真实 + 医疗健康特殊品类 + 知识付费真实 + 软广绝对化客观）】
> 1. **伪科学虚假科普红线**：专业知识须有科学依据/权威来源，严禁传播伪科学/谣言/虚假科普，严禁"致癌/包治/神效/100%"式恐吓营销与不实宣称（违反《广告法》第二十八条虚假广告、《网络信息内容生态治理规定》谣言信息）。
> 2. **专业资质背书真实**：领域专家/机构背书须真实执业资质（医师/律师/教师/营养师/工程师等），严禁冒充专家/虚构头衔/伪造资质/演员扮演专家（违反《广告法》第三十八条代言人、各专业执业资质法规）。
> 3. **医疗健康特殊品类红线**：涉及医疗/药品/医疗器械/保健品须严格遵守特殊广告审查，严禁非医疗广告涉及疾病治疗功能、严禁利用医生患者形象代言药品保健品（违反《广告法》第十六条第四十六条、《医疗广告管理办法》）。
> 4. **知识付费课程真实**：知识付费课程/教程须真实交付，严禁"包过/包就业/月入过万/稳赚不赔"虚假承诺诱导，师资/课时/退款规则须明示真实（违反《广告法》第二十四条教育培训广告、《消费者权益保护法》）。
> 5. **软广标注与绝对化客观**：软广须依法标注"广告"（《互联网广告管理办法》），严禁"最权威/第一/顶级专家/唯一正确"绝对化用语（《广告法》第九条），知识科普须客观中立不得贬低同行、制造焦虑误导。


# 知识博主口播广告全流程创作系统 V4.1

> **定位**：以 TikTok/抖音/B 站爆款知识博主干货口播为标杆，用专业干货讲解、专业口播光、四段式知识叙事与专业可信表演，把产品转化为可信任的知识种草欲望。核心信条：**干货即信任，专业即权威，知识即种草。**

---

## 一、 核心美学基因（Knowledge Edu Blogger Talking-Head DNA）

| 维度 | 知识博主口播范式 |
|---|---|
| **叙事结构** | 四段式知识口播：①痛点提问开场（抛出问题/悬念）→ ②干货知识讲解（专业科普/方法论）→ ③产品解决方案（知识落地/产品结合）→ ④信任背书种草 CTA |
| **主角设定** | 知识博主/领域专家（专业、可信、亲和），单人口播主导 + 知识图表/产品"论据主角"，专业真实 |
| **光影配方** | 专业口播光，窗光 + 环形灯，右侧 40° 5000K，Key:Fill 1.6:1 干净专业显面部，轮廓光柔和，明亮通透无阴影 |
| **焦段/机位** | 手机竖屏 9:16，口播中景（35mm 等效）+ 讲解特写（50mm 等效）+ 产品图表微距（100mm 等效） |
| **AU 微表情** | 讲解专注 AU4+AU7 + 强调笃定 AU9+AU10 + 信任微笑 AU6+AU12 + 专业眼神，图表转"知识可视化动力学" |
| **节奏** | 口播节奏，知识卡点，痛点-干货-方案-背书，20-30 秒知识弧 |
| **声场** | 清晰口播人声 + 轻知识 BGM（简约/科技轻音乐）+ 图表切换音效 |
| **调色** | 明亮专业调，干净通透，知识博主专业感，拒绝花哨拒绝暗沉 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: Knowledge edu blogger talking-head ad vertical still, 9:16 phone-shot aesthetic, professional studio softbox light, trustworthy expert delivery, clean bright authoritative, knowledge popularization mood. A professional knowledge blogger delivering expert explanation, bright even studio lighting, confident trustworthy gaze, clean professional framing, vertical, edu blogger mood::3.0 
[LIGHT ANGLE] Key Light window/ring softbox 40° camera-right 5000K bright clean professional, Fill bounce 40° camera-left Key:Fill ratio 1.6:1 clean face-revealing, Rim soft ambient, practical studio accent, catchlight bright at 11 o'clock in both eyes::2.5. 
[COLOR TEMP] Key 5000K CRI 96 neutral bright, Fill 4900K CRI 94, clean professional bias, white balance 5000K accurate, phone-native bright edu grading::1.5. 
[CAMERA] Half-body eye-level height 1.4m, azimuth 10° near-frontal, 35mm talking medium + 50mm explanation close T2.0 + 100mm product chart macro T2.8 vertical 9:16, focus plane on face and chart, shallow DOF studio bokeh::2.0. 
[MICRO-TEXTURE] Blogger skin pores real no airbrush; professional attire fabric detail; chart whiteboard graphic crisp; product material authentic; trustworthy expression::3.0. 
[ATMOSPHERE] Bright professional studio vibe, clean light haze, trustworthy knowledge immersion, zero dark zero clutter, authoritative authentic::1.5. 
iPhone 15 Pro, 35mm talking equiv, native phone processing, bright professional, 9:16 --ar 9:16 --style raw --v 8 --s 250 --c 4 --no dark tone, no clutter, no gloomy, distorted anatomy, blurry face
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
知识博主口播广告竖屏关键帧，9:16，手机拍摄质感，专业演播室柔光，可信专家讲解，干净明亮权威，知识科普氛围。一位专业知识博主正在进行专家讲解，明亮均匀演播室光，自信可信目光，干净专业构图，竖屏构图，知识博主氛围。
【光影角度量化】：主光为窗光/环形柔光箱，位于摄影机右侧 40°、5000K、明亮干净专业；辅光为反光补光，位于摄影机左侧 40°，光比 Key:Fill = 1.6:1 干净显面部；轮廓光柔和环境；环境 practical 演播室点缀；博主眼中 11 点钟方向存在明亮眼神光。
【色温显色】：主光 5000K CRI 96 中性明亮；辅光 4900K CRI 94；干净专业偏置；白平衡 5000K 准确；手机原生明亮知识调色。
【视角机位】：半身平视高度 1.4 米，方位角 10° 近正面，口播中景 35mm + 讲解特写 50mm T2.0 + 产品图表微距 100mm T2.8 竖屏 9:16，焦平面锁定面部与图表，浅景深演播室虚化。
【微观质感证据链】：博主皮肤毛孔真实拒绝磨皮；职业着装面料细节；图表白板图形清晰；产品材质真实；可信表情。
【大气体积介质】：明亮专业演播室氛围，干净光雾霭，可信知识沉浸，零暗沉零杂乱，权威真实。
iPhone 15 Pro，35mm 口播等效，手机原生处理，明亮专业，9:16 竖屏。

【English Prompt】：
Knowledge edu blogger talking-head ad vertical still, 9:16 phone-shot, professional studio softbox light, trustworthy expert delivery, clean bright authoritative, knowledge popularization mood. Professional knowledge blogger delivering expert explanation, bright even studio lighting, confident trustworthy gaze, clean professional, vertical, edu blogger. Key window/ring softbox 40° camera-right 5000K bright clean professional, Fill bounce 40° camera-left Key:Fill 1.6:1 clean face-revealing, Rim soft ambient, practical accent, catchlight bright 11 o'clock both eyes. Key 5000K CRI 96 neutral bright, Fill 4900K CRI 94, clean professional bias, WB 5000K accurate, phone-native bright edu. Camera half-body eye-level 1.4m, azimuth 10° near-frontal, 35mm talking medium + 50mm explanation close T2.0 + 100mm product chart macro T2.8 vertical 9:16, focus face chart, shallow DOF bokeh. Blogger skin pores no airbrush; professional attire fabric; chart whiteboard crisp; product material authentic; trustworthy expression. Bright professional studio, clean light haze, trustworthy knowledge. iPhone 15 Pro, 35mm talking equiv, 9:16.

【负向提示词 (Negative Prompt)】：
dark tone, clutter, gloomy, distorted anatomy, blurry face, plastic skin, extra limbs, text gibberish, watermark, low resolution, 2.39:1 widescreen.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；知识博主 `@CHAR_EXPERT` 用标准 10 格 Model Card；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_EXPERT 知识博主】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 172cm, WEIGHT 60kg, BODY RATIO 7.5 heads, BIRTHDAY 1993.07.10, NATIONALITY Chinese, STYLE professional/trustworthy/knowledgeable, SPECIALTY knowledge sharing/expert explanation. Column 2 headless front full-body standing pose cropped below chin professional confident posture, smart casual attire complete neckline-to-shoe framing. Column 3 full back view standing pose with head head-to-toe showcasing attire back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, expression A professional neutral. Columns 4-6 bottom row same three-view, expression B engaged explaining. Bottom row 2 panels props close-up: knowledge chart whiteboard macro, product demo macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm authentic no airbrush; professional attire fabric distinct; chart graphic crisp; product material detail; no plastic skin::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, no body distortion, plastic skin, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 172cm、体重 60kg、身材比例 7.5 头身、生日 1993.07.10、国籍 中国、风格 专业/可信/知识、特长 知识分享/专家讲解。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图博主专业自信站姿，领口到鞋底完整入画，商务休闲着装。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示着装背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）表情 A 专业中性；下排表情 B 投入讲解。底部横排 2 格**道具特写**：格 1 知识图表白板微距；格 2 产品演示微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、真实拒绝磨皮；职业着装面料分明；图表图形清晰；产品材质细节；拒绝塑料皮肤。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, body distortion, plastic skin, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_EXPERT` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相 100% 一致（同一张脸）；正面全身栏严禁头部入画，背面全身栏严禁缺头；知识博主专业可信形象，严禁失真塑料化。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_EXPERT : references/assets/knowledge_blogger.png （知识博主，全片同一面部骨相，专业可信亲和）
- @PROD_ITEM : references/assets/product_item.png （产品母版，同一款式同一卖点）
- @SCN_STUDIO : references/assets/studio_scene.png （演播室/书房场景母版，明亮专业，知识氛围）
- @PROP_CHART : references/assets/knowledge_chart.png （知识图表道具母版，白板/图表/数据动画）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 26 秒的知识博主口播广告竖屏序列，画幅 9:16 / 30fps / 手机原生质感。

[0.0s-6.0s]：痛点提问开场——@CHAR_EXPERT 于 @SCN_STUDIO 抛出痛点问题/悬念开场，专业口播光，博主 AU4+AU7 讲解专注（皱眉眼睑收紧），视线锁定镜头，[知识可视化动力学]（图表呈现/问题悬念），手机竖屏 35mm 口播中景，4 秒钩子。

[6.0s-14.0s]：干货知识讲解——@CHAR_EXPERT 专业科普/方法论讲解，@PROP_CHART 知识图表辅助论证，博主强调笃定 AU9+AU10，[知识可视化动力学]（图表呈现/白板书写/数据动画），50mm 讲解特写 + 100mm 图表微距，知识卡点，干货密集。

[14.0s-21.0s]：产品解决方案——@PROD_ITEM 产品作为知识落地的解决方案登场，@CHAR_EXPERT 讲解产品如何解决问题，博主信任微笑 AU6+AU12，[知识可视化动力学]（产品演示/数据对比），35mm 中景 + 100mm 产品微距，知识落地高潮。

[21.0s-26.0s]：信任背书种草 CTA——@CHAR_EXPERT 口播信任背书种草（专业背书/资质/客观建议），博主 AU6+AU12 信任真诚，产品自然露出，可信任知识种草收尾。

[FACS/AU 表演微动作]：@CHAR_EXPERT 知识博主——0.0s 起 AU4+AU7（讲解专注皱眉眼睑收紧），强度 C 级（专业专注），视线 0.2s 先导锁定镜头/图表；6.0s 干货强调 AU9+AU10（皱鼻上唇提升笃定强调），强度 C 级（专业笃定）；14.0s 产品方案 AU6+AU12（信任微笑），强度 B 级（可信推荐）；21.0s CTA AU6+AU12 信任真诚（专业背书），强度 B 级；AU45 自然眨眼配合口播节奏；@PROD_ITEM/@PROP_CHART——[知识可视化动力学] 图表呈现/白板书写/数据动画/产品演示，并声明 `[本镜无角色面部主体，AU 自动转为知识可视化动力学]`。

[CineDance 运镜与光学]：手机竖屏 35mm 口播中景 + 50mm 讲解特写 + 100mm 产品图表微距，半身平视高度 1.4m，方位角 10° 近正面，浅景深演播室虚化，口播用中景固定/讲解用特写 push-in/图表用微距插入，知识卡点，竖屏 9:16 构图，快门等效 180°，口播稳定运镜。

[光影角度量化]：主光窗光/环形柔光箱右侧 40° 5000K 明亮干净专业；辅光反光补光左侧 40° 光比 Key:Fill 1.6:1 干净显面部；轮廓光柔和环境；环境 practical 演播室点缀；博主眼中 11 点钟明亮眼神光。

[色温显色]：主光 5000K CRI 96 中性明亮；辅光 4900K CRI 94；干净专业偏置；白平衡 5000K 准确；手机原生明亮知识调色。

[微观质感证据链]：博主皮肤毛孔真实拒绝磨皮；职业着装面料细节；图表白板图形清晰；产品材质真实；可信表情。

[大气体积介质]：明亮专业演播室氛围，干净光雾霭，可信知识沉浸，零暗沉零杂乱，权威真实。

[同步声锁与台词原语言保留]：No subtitles.（字幕/知识点/产品信息/图表花字须后期硬压，绝不由模型生成）。知识声场——清晰口播人声 + 轻知识 BGM（简约/科技轻音乐）+ 图表切换音效，声画同步精准，26 秒知识弧；台词保留原语言口语化专业可信，口型同步精准锁定。

[资产单一源铁律]：@CHAR_EXPERT 从基准博主资产一次性生成所有镜头状态，**面部骨相 100% 一致（同一张脸）**；@PROD_ITEM 须同一款式、同一卖点 100% 一致（严禁漂移/改款式）；@PROP_CHART 图表保持基准一致；严禁链式修改导致博主/产品/图表漂移。
[声音政策·默认无音乐] 不生成音乐 / no bgm —— 禁止任何 BGM/配乐/背景音乐；同期声（对白/环境音/动作音效/声音特效 Foley）须正常、准确、完整生成。
```

---

## 四、 黄金分镜画面完整拆解表（26 秒知识博主口播版）

| 时间 | 景别 | 画面内容 | 表演（AU/知识可视化动力学） | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-6.0s | 口播中景 | 痛点提问悬念开场 | 博主 AU4+AU7 讲解专注 / 问题图表动力学 | 35mm 固定 1.4m / 专业口播光 | 清晰口播 + 轻知识 BGM |
| 6.0-14.0s | 讲解特写+图表 | 干货知识专业讲解 | 博主 AU9+AU10 强调笃定 / 白板数据动力学 | 50mm+100mm push-in / Key:Fill 1.6:1 | 干货口播 + 图表音效 |
| 14.0-21.0s | 中景+产品微距 | 产品解决方案落地 | 博主 AU6+AU12 信任微笑 / 产品演示动力学 | 35mm+100mm / 明亮通透 | 方案口播 + 知识卡点 |
| 21.0-26.0s | 中景定格 | 信任背书种草 CTA | 博主 AU6+AU12 信任真诚 | 中景定格 / 专业口播 | 背书口播 + 客观建议 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-knowledge-edu-blogger-dna.md` | 构思美学时 | 知识博主口播基因、专业口播光、专业可信权威 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 四段式知识、痛点提问钩子、干货讲解模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | 清晰口播人声、轻知识 BGM、图表切换音效 |
| `references/cinedance-camera-optics.md` | 生成视频时 | 口播中景、讲解特写、产品图表微距、竖屏 9:16 运镜 |
| `references/perf-acting-au-system.md` | 生成角色时 | 讲解专注 AU4+AU7、强调笃定 AU9+AU10、知识可视化动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | 知识图表解算、口播轨迹锁定、专业口播光渲染 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
