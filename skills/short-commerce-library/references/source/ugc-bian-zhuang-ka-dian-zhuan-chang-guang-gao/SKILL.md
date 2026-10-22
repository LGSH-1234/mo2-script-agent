---
name: "ugc-bian-zhuang-ka-dian-zhuan-chang-guang-gao"
description: "以同机位对齐与重拍卡点转场，为全品类产品呈现从日常到惊艳的蜕变视觉奇观。"
version: "4.1"
display_name: "变装卡点转场广告"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
video_model: "Seedance_2.5"
image_model: "gpt_image_2_5_sunburst"
---

> ### 🎵 【系统默认铁律 · 音乐核心技能 · 声音政策弹性条款（最高优先级）】
> 1. **音乐为作品本体**：本技能以音乐/歌舞/MV/卡点节拍为核心表达，**音乐照常生成**，不适用「默认无 BGM」一刀切；视频提示词应标注音乐属性（曲风/BPM/情绪/卡点节拍点）。
> 2. **同期声仍必须正常准确**：对白/环境音/动作音效/Foley 照常准确生成、与音乐并存，严禁削弱。
> 3. **非音乐本体镜头**：与音乐无关的纯展示/口播镜头，不额外铺无关 BGM。
> 4. **用户要求无音乐时**：用户明确「无音乐 / no bgm」则切纯同期声模式，视频提示词末尾追加 `不生成音乐 / no bgm`。


> ### 🚨 【系统默认铁律 · 视频提示词 AU 角色微表情强制注入准则】
> 1. **默认强制性**：在图生视频（I2V）与多参视频生成阶段，提示词**必须默认带有角色 FACS/AU 精准微动作描述词**（AU 编号、解剖学肌肉位移、`A~E` 级量化强度、`0.2s 视线先导`、`AU45 眨眼抑制`）。
> 2. **豁免条件**：**除非用户在交互中明确声明"不需要表情"或"无微表情"**，否则默认所有涉及有人格属性的角色镜头均**无条件全量携带**。
> 3. **特异性智能转译**：若画面为纯造型/服饰/转场空镜，AU 规则自动转译为"造型动力学"（服饰飘动、面料垂坠、转场闪光、造型切换），并显式声明 `[本镜无角色主体，AU 自动转为造型动力学]`。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：角色（`@CHAR`）、场景（`@SCN`）、造型（`@OUTFIT`）、道具（`@PROP`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成（before/after 变装须同一面部骨相与同一机位对齐）。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **转场对齐铁律**：变装 transition 广告的核心是"before/after 同机位、同姿态、同构图，靠 beat drop 瞬间切换的视觉魔法"——必须通过精准机位对齐、卡点转场技巧（手势遮挡/甩镜/跳切）、造型强反差，把服饰造型转化为可见的惊艳蜕变，严禁机位错位、转场脱拍与 before/after 反差不足。
> ### 🚨 【钢人论证补丁 · 变装合规铁律（Bidirectional Steelmanning Fix · 严禁焦虑造假 + 服饰带货落点）】
> 1. **严禁 before 焦虑造假**：before/after 反差必须靠"造型/服饰/妆造/气场"的真实升级实现，**严禁故意把 before 扮丑、邋遢、打暗光、丑化身材或容貌**来制造虚假反差（制造容貌焦虑/身材焦虑式营销，平台明令打击），before 须是真实自然的日常状态而非被贬低的"反面教材"。
> 2. **服饰带货落点铁律**：变装广告的商业目的是卖服饰/造型——after 造型必须露出可识别的商品细节（材质/版型/剪裁/logo/搭配），多套连变应对应可购买的 SKU/链接锚点，严禁纯炫技变装而无商品转化落点。
> 3. **身材包容性**：不鼓吹"变瘦才美/单一标准身材才配变装"的单一审美，尊重真实体型多样性，变装惊艳靠造型巧思而非身材贬损，避免身材羞辱暗示。
> 4. **平台合规**：卡点 BGM 须商用授权，服饰品牌/logo 露出须获授权，hashtag/挑战赛须遵守平台报备规则，严禁未授权盗用音乐与他人肖像。


# 变装卡点转场广告全流程创作系统 V4.1

> **定位**：以 TikTok/抖音爆款 transition 变装卡点为标杆，用 before/after 同机位对齐、beat drop 瞬间变装、手势遮挡/甩镜转场魔法与多套造型连变，把服饰造型转化为可见的惊艳蜕变欲望。核心信条：**对齐即魔法，卡点即惊艳，反差即传播。**

---

## 一、 核心美学基因（Transition Transformation DNA）

| 维度 | 变装卡点转场范式 |
|---|---|
| **叙事结构** | 三段式变装：①before 日常/便服/素颜开场 → ②卡点转场魔法（手势遮挡/甩镜/跳切瞬间变装）→ ③after 惊艳造型 reveal + 多套连变 + 定格 |
| **主角设定** | 变装达人——时尚、表现力、镜头感，before/after 强反差，绝非静态模特 |
| **光影配方** | 手机竖屏动感时尚光，转场卡点闪光，before 平淡 after 鲜艳对比，Key:Fill 2.5:1 |
| **焦段/机位** | 手机竖屏 9:16 全身，固定机位（保证 before/after 同机位对齐），转场甩动/跳切 |
| **AU 微表情** | before 随意松弛 → after 自信 AU6+AU12+AU17 下颌，变装惊艳反差，纯造型转译为"造型动力学" |
| **节奏** | 强卡点转场，beat drop 瞬间变装，15 秒多套连变 |
| **声场** | 卡点 BGM + 转场音效（whoosh/闪光/切换）+ 节拍 drop |
| **调色** | 时尚高饱和质感，before 平淡 after 鲜艳强对比 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: Fashion transition transformation ad vertical still, 9:16 phone-shot aesthetic, before-after outfit change, beat-drop transition magic, glam reveal, trendy transformer. A fashion-forward creator in a stunning glam outfit mid-transformation pose, confident expression, dynamic fashion lighting, vertical full-body framing, high-saturation editorial energy, transition flash::3.0 
[LIGHT ANGLE] Key Light fashion softbox 30° camera-right 5200K dynamic shaping, Fill bounce 45° camera-left Key:Fill ratio 2.5:1 editorial, Rim 150° behind transition flash +1.5 stop glam edge, practical neon accent, catchlight bright at 11 o'clock::2.5. 
[COLOR TEMP] Key 5200K CRI 92, Fill 5000K CRI 90, neon accent magenta/cyan, white balance 5200K vibrant bias, phone-native high-saturation editorial grading::1.5. 
[CAMERA] Height 1.3m full-body, azimuth 0° frontal fixed rig, 26mm phone-equiv wide T2.0 vertical 9:16 full-body, locked-off for before/after alignment, focus plane on outfit and face::2.0. 
[MICRO-TEXTURE] Glam outfit fabric sheen sequins/drape; confident skin glow makeup editorial; before outfit plain cotton contrast; sneaker/heels material authentic; transition motion blur flash::3.0. 
[ATMOSPHERE] Dynamic fashion energy, transition flash bloom, editorial vibrant vibe, zero dull, high-energy glam immersive::1.5. 
iPhone 15 Pro, 26mm equiv wide, native phone processing, vibrant editorial, 9:16 --ar 9:16 --style raw --v 8 --s 250 --c 4 --no dull before, no static pose, no moody dark, no misaligned framing, blurry face
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
变装卡点转场广告竖屏关键帧，9:16，手机拍摄质感，before-after 换装，beat drop 转场魔法，惊艳 reveal，潮流变装达人。一位时尚先锋创作者身着惊艳华丽造型，变装中姿态，自信表情，动感时尚光，竖屏全身构图，高饱和大片活力，转场闪光。
【光影角度量化】：主光为时尚柔光箱，位于摄影机右侧 30°、5200K、动感塑形；辅光为反光补光，位于摄影机左侧 45°，光比 Key:Fill = 2.5:1 大片感；轮廓光为转场闪光，位于后方 150°、过曝 +1.5 档，华丽边缘光；环境 practical 霓虹点缀；11 点钟方向存在明亮眼神光。
【色温显色】：主光 5200K CRI 92；辅光 5000K CRI 90；霓虹点缀品红/青色；白平衡 5200K 鲜艳偏置；手机原生高饱和大片调色。
【视角机位】：摄影机高度 1.3 米全身，正方位角 0° 固定机位，26mm 手机等效广角 T2.0 竖屏 9:16 全身，锁定机位保证 before/after 对齐，焦平面锁定造型与面部。
【微观质感证据链】：华丽造型面料光泽亮片/垂坠；自信皮肤光泽大片妆容；before 便服平淡棉质对比；球鞋/高跟鞋材质真实；转场运动模糊闪光。
【大气体积介质】：动感时尚活力，转场闪光光晕，大片鲜艳氛围，零平淡，高能量华丽沉浸。
iPhone 15 Pro，26mm 等效广角，手机原生处理，鲜艳大片，9:16 竖屏。

【English Prompt】：
Fashion transition transformation ad vertical still, 9:16 phone-shot, before-after outfit change, beat-drop transition magic, glam reveal, trendy transformer. Fashion-forward creator stunning glam outfit mid-transformation pose, confident expression, dynamic fashion light, vertical full-body, high-saturation editorial energy, transition flash. Key fashion softbox 30° camera-right 5200K dynamic, Fill bounce 45° camera-left Key:Fill 2.5:1 editorial, Rim 150° transition flash +1.5 stop glam edge, practical neon accent, catchlight bright 11 o'clock. Key 5200K CRI 92, Fill 5000K CRI 90, neon magenta/cyan, WB 5200K vibrant, phone-native high-saturation editorial. Camera 1.3m full-body, azimuth 0° fixed rig, 26mm phone-equiv wide T2.0 vertical 9:16, locked-off before/after alignment, focus outfit face. Glam outfit sheen sequins drape; confident skin glow editorial makeup; before plain cotton contrast; heels material; transition motion blur flash. Dynamic fashion energy, transition flash bloom, editorial vibrant. iPhone 15 Pro, 26mm equiv, 9:16.

【负向提示词 (Negative Prompt)】：
dull before look, static boring pose, moody dark, misaligned before/after framing, low contrast, blurry face, distorted anatomy, extra limbs, text, watermark, low resolution, 2.39:1 widescreen.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_TRANSFORMER 变装达人】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 175cm, WEIGHT 60kg, BODY RATIO 7.6 heads, BIRTHDAY 1999.09.09, NATIONALITY Chinese, STYLE fashion/transformative/expressive, SPECIALTY transition/modeling. Column 2 headless front full-body standing pose cropped below chin confident model posture, glam fashion outfit complete neckline-to-shoe framing showcasing silhouette. Column 3 full back view standing pose with head head-to-toe showcasing outfit back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, hairstyle A glam styled. Columns 4-6 bottom row same three-view, hairstyle B before messy variant. Bottom row 2 panels wardrobe and props close-up: glam outfit sequin fabric macro, before plain cotton fabric macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm editorial glow no airbrush; hair strands distinct styled; glam outfit sequin sheen drape; before plain cotton contrast texture; authentic fabric detail::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, plastic skin, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 175cm、体重 60kg、身材比例 7.6 头身、生日 1999.09.09、国籍 中国、风格 时尚/变装/表现力、特长 转场/模特表现。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图达人自信站姿，领口到鞋底完整入画，华丽时尚造型，展示剪影。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示造型背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）造型 A 华丽定型；下排造型 B before 随意凌乱变体。底部横排 2 格**着装道具特写**：格 1 华丽造型亮片面料微距；格 2 before 平淡棉质面料微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、大片光泽拒绝磨皮；发丝根根分明定型；华丽造型亮片光泽垂坠；before 平淡棉质对比质感；面料细节真实。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, plastic skin, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_TRANSFORMER` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相/身材比例 100% 一致（before/after 同一张脸）；正面全身栏严禁头部入画，背面全身栏严禁缺头。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_TRANSFORMER : references/assets/fashion_transformer.png （变装达人，before/after 同一面部骨相，自信镜头感）
- @OUTFIT_BEFORE : references/assets/before_outfit.png （before 日常便服母版，平淡棉质，反差基线）
- @OUTFIT_AFTER : references/assets/after_outfit.png （after 惊艳华丽造型母版，亮片垂坠光泽，多套连变）
- @SCN_TRANSITION : references/assets/transition_scene.png （转场场景母版，固定机位对齐背景，动感时尚）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 15 秒的变装卡点转场广告竖屏序列（可循环），画幅 9:16 / 30fps / 手机原生质感。

[0.0s-3.0s]：before 日常开场——@CHAR_TRANSFORMER 身着 @OUTFIT_BEFORE 平淡便服于 @SCN_TRANSITION，随意松弛神态，手机竖屏 26mm 全身固定机位，before 平淡光，为转场反差铺垫基线。

[3.0s-5.0s]：卡点转场魔法——beat drop 瞬间，@CHAR_TRANSFORMER 用手势遮挡/甩镜/跳切触发变装，转场闪光，同一机位同一姿态对齐，`[转场空镜 AU 自动转为造型动力学]`（服饰切换/闪光/面料飘动），视觉魔法核心。

[5.0s-12.0s]：after 惊艳 reveal + 多套连变——@CHAR_TRANSFORMER 变身 @OUTFIT_AFTER 华丽造型，AU6+AU12+AU17 自信微笑下颌收紧，卡点连续切换多套造型，动感时尚光，after 鲜艳高饱和，惊艳反差高潮。

[12.0s-15.0s]：造型定格——@CHAR_TRANSFORMER 最终造型自信定格，AU6+AU12 自信微笑，before/after 对比同框或闪回，品牌/服饰定格，惊艳蜕变收尾（可循环回 before）。

[FACS/AU 表演微动作]：0.0s before 为 @CHAR_TRANSFORMER 的松弛随意神态（AU 放松基线），强度 A 级；5.0s after reveal 转 AU6+AU12（自信微笑）+ AU17（下颌收紧显气场），强度 C 级（自信惊艳）；12.0s 定格 AU6+AU12 自信微笑 B 级；视线 0.2s 先导锁定镜头（气场感），AU45 眨眼随节拍，before 松弛 ↔ after 自信的强反差表演。

[CineDance 运镜与光学]：手机竖屏 26mm 等效广角全身，**固定锁定机位（locked-off）保证 before/after 同机位同姿态对齐**（转场魔法核心），转场瞬间配甩动/跳切/手势遮挡对齐 beat drop，after 多套连变卡点快切，竖屏 9:16 全身构图，快门等效 180°。

[光影角度量化]：主光时尚柔光箱右侧 30° 5200K 动感塑形；辅光反光补光左侧 45° 光比 Key:Fill 2.5:1 大片感；轮廓光转场闪光后方 150° +1.5 档华丽边缘；环境 practical 霓虹点缀；11 点钟明亮眼神光。before 光平淡、after 光鲜艳形成对比。

[色温显色]：主光 5200K CRI 92；辅光 5000K CRI 90；霓虹点缀品红/青色；白平衡 5200K 鲜艳偏置；手机原生高饱和大片调色，before 低饱和 after 高饱和对比。

[微观质感证据链]：华丽造型面料光泽亮片/垂坠；自信皮肤光泽大片妆容；before 便服平淡棉质对比；球鞋/高跟鞋材质真实；转场运动模糊闪光。

[大气体积介质]：动感时尚活力，转场闪光光晕，大片鲜艳氛围，零平淡，高能量华丽沉浸。

[同步声锁与台词原语言保留]：No subtitles.（字幕/造型名花字须后期硬压，绝不由模型生成）。卡点 BGM 声场——强节拍卡点 BGM + 转场音效（whoosh/闪光/切换音）+ beat drop 落在变装瞬间，多套连变卡点对齐，15 秒循环；无台词或保留原语言口播，口型同步精准锁定。

[资产单一源铁律]：@CHAR_TRANSFORMER 从基准达人资产一次性生成 before/after/多套造型所有状态，**面部骨相 100% 一致（before/after 同一张脸，严禁换脸）**；@OUTFIT_BEFORE/@OUTFIT_AFTER 造型在转场前后保持基准一致；机位锁定确保对齐零漂移。
[声音政策·音乐核心] 音乐为作品本体，照常生成并标注（曲风/BPM/情绪/卡点节拍）；同期声（对白/环境音/动作音效/Foley）须正常准确生成；若用户要求无音乐则末尾改为「不生成音乐 / no bgm」。
```

---

## 四、 黄金分镜画面完整拆解表（15 秒变装转场循环版）

| 时间 | 景别 | 画面内容 | AU 微表情 | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-3.0s | 竖屏全身 | before 日常便服随意开场反差基线 | 松弛基线 | 手机 26mm 固定机位 / before 平淡光 | 卡点 BGM 铺垫 |
| 3.0-5.0s | 全身转场 | beat drop 手势遮挡/甩镜瞬间变装 | [造型动力学] | 固定锁定机位对齐 / 转场闪光 | beat drop + whoosh 转场音 |
| 5.0-12.0s | 竖屏全身 | after 惊艳 reveal 多套造型连变 | AU6+AU12+AU17 | 26mm 卡点快切 / after 鲜艳光 | BGM 卡点高潮 + 切换音 |
| 12.0-15.0s | 全身定格 | 最终造型自信定格 before/after 对比 | AU6+AU12 | 26mm 定格 / 动感时尚光 | BGM 收尾 + 循环点 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-transition-transformation-dna.md` | 构思美学时 | 变装转场基因、before/after 对齐魔法、造型强反差 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 三段式变装、卡点转场技巧、多套连变模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | 卡点 BGM、转场音效 whoosh、beat drop 对齐 |
| `references/cinedance-camera-optics.md` | 生成视频时 | 固定锁定机位对齐、甩镜跳切转场、竖屏 9:16 运镜 |
| `references/perf-acting-au-system.md` | 生成人物时 | before 松弛/after 自信 AU6+AU12+AU17、造型动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | before/after 机位对齐锁定、转场轨迹、造型切换动力学 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
