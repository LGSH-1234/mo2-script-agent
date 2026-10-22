---
name: "ugc-grwm-mei-zhuang-jiao-cheng-guang-gao-feng-ge"
description: "以真实素颜蜕变与闺蜜边化边聊沉浸视角，结合美妆ASMR，打造高信任高种草教程广告。"
version: "4.1"
display_name: "GRWM美妆教程广告风格"
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
> 1. **默认强制性**：在图生视频（I2V）与多参视频生成阶段，提示词**必须默认带有角色 FACS/AU 精准微动作描述词**（AU 编号、解剖学肌肉位移、`A~E` 级量化强度、`0.2s 视线先导`、`AU45 眨眼抑制`）。
> 2. **豁免条件**：**除非用户在交互中明确声明"不需要表情"或"无微表情"**，否则默认所有涉及有人格属性的角色镜头均**无条件全量携带**。
> 3. **特异性智能转译**：若画面为纯美妆产品/质地特写（膏体/粉质/刷具），AU 规则自动转译为"美妆质地动力学"（膏体挤出、粉质飞散、刷毛扫动、珠光流转），并显式声明 `[本镜无角色主体，AU 自动转为美妆质地动力学]`。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：角色（`@CHAR`）、场景（`@SCN`）、道具（`@PROP`）、产品母版（`@PROD`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成（尤其素颜→妆效渐变须同一面部骨相）。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **闺蜜真实种草铁律**：GRWM 美妆广告的核心是"边化边聊的闺蜜亲密信任感"——必须通过真实素颜、化妆步骤演示、边化边聊口语化、显肤质通透光、妆效蜕变 reveal，把美妆产品转化为"闺蜜真心安利"的可见种草欲望，严禁高冷美妆广告腔、过度磨皮假面与硬广念稿。
> 4. **美妆合规铁律（钢人论证补丁 · Bidirectional Steelmanning Fix）**：化妆品广告受《广告法》《化妆品监督管理条例》严管——① 严禁宣称医疗功效（祛痘/祛斑/生发/消炎/治疗）；② 严禁绝对化用语（最/第一/100%/永久）；③ 功效宣称须有依据，特殊化妆品须注册证；④ 妆效须为产品真实效果，素颜与妆效均不得靠后期滤镜造假误导（伪素颜=虚假宣传）。


# GRWM 美妆边化边聊广告全流程创作系统 V4.1

> **定位**：以 TikTok/小红书爆款 GRWM（Get Ready With Me）美妆教程为标杆，用真实素颜、边化边聊闺蜜感、化妆步骤演示与妆效蜕变 reveal，把美妆产品转化为可见的闺蜜种草欲望。核心信条：**素颜即真实，步骤即信任，蜕变即种草。**

---

## 一、 核心美学基因（GRWM Beauty DNA）

| 维度 | GRWM 美妆边化边聊范式 |
|---|---|
| **叙事结构** | 四段式 GRWM：①素颜开场 + 今日妆容预告 → ②化妆步骤边化边聊演示（底妆/眼妆/唇妆）→ ③妆效完成 reveal → ④产品种草清单 + CTA |
| **主角设定** | 美妆博主——精致、亲和、闺蜜感，边化边聊真实对话，绝非高冷美妆广告腔 |
| **光影配方** | 环形灯美妆光正面柔光 + 侧柔光塑形，明亮通透显肤质，Key:Fill 1.8:1，粉调干净 |
| **焦段/机位** | 手机竖屏 9:16 近景面部，化妆步骤特写，50mm 等效面部，齐眼高度 |
| **AU 微表情** | 闺蜜微笑 AU6+AU12 + 化妆专注 AU17+AU24，reveal 惊喜 AU1+AU2+AU26，纯产品转译为"美妆质地动力学" |
| **节奏** | 边化边聊舒缓 + 卡点，教程步骤清晰，20-40 秒 |
| **声场** | 轻柔 BGM + 真实闺蜜口播 + 化妆品 ASMR（开盖/粉扑/刷子扫） |
| **调色** | 明亮通透粉调，显肤质真实，干净非过曝 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: GRWM beauty tutorial ad vertical still, 9:16 phone-shot aesthetic, relatable beauty guru, ring light flawless skin, get-ready-with-me intimate vibe, makeup transformation. A glamorous-yet-relatable beauty creator doing makeup at a vanity, half-face done genuine bestie expression, bright airy pink-tone setting, smartphone front-camera close-up, ring light flattering skin texture::3.0 
[LIGHT ANGLE] Key Light ring light 0° frontal soft even 4800K flawless-skin flattering, Fill soft side 55° camera-left Key:Fill ratio 1.8:1 gentle shaping, no harsh shadow, practical vanity bulb light, catchlight round ring at 12 o'clock::2.5. 
[COLOR TEMP] Key ring 4800K CRI 95, Fill 5200K CRI 92, white balance 5000K bright-pink bias, phone-native bright clean pink-tone skin-true grading::1.5. 
[CAMERA] Height 1.5m eye-level face, azimuth 0° frontal, 50mm phone-equiv T2.0 face close-up, vertical 9:16 framing, focus plane on skin texture and makeup detail::2.0. 
[MICRO-TEXTURE] Real skin pores fine texture no over-smoothed plastic; makeup foundation dewy finish; eyeshadow shimmer pigment particles; lipstick creamy satin; brush bristles soft; product packaging authentic::3.0. 
[ATMOSPHERE] Bright airy vanity, clean pink-tone daylight, intimate bestie atmosphere, zero moody dark, authentic GRWM phone-native vibe::1.5. 
iPhone 15 Pro front camera, 50mm equiv, native phone processing, bright clean skin-true, 9:16 --ar 9:16 --style raw --v 8 --s 200 --c 2 --no cinematic dark, no over-smoothed plastic skin, no professional studio, no heavy filter, blurry
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
GRWM 美妆边化边聊广告竖屏关键帧，9:16，手机拍摄质感，亲和美妆博主，环形灯显肤质，get-ready-with-me 闺蜜亲密氛围，妆容蜕变。一位精致而亲和的美妆创作者在梳妆台前化妆，半脸完成真诚闺蜜表情，明亮通透粉调场景，手机前置近景，环形灯讨喜显肤质。
【光影角度量化】：主光为环形灯正面柔光，位于 0°、4800K、柔和均匀显肤质讨喜；辅光为侧柔光塑形，位于摄影机左侧 55°，光比 Key:Fill = 1.8:1 温柔塑形；无硬阴影；环境 practical 梳妆台灯泡光；12 点钟方向存在环形圆形眼神光。
【色温显色】：主光环形灯 4800K CRI 95；辅光 5200K CRI 92；白平衡 5000K 明亮粉调偏置；手机原生明亮干净粉调真实肤色调色。
【视角机位】：摄影机高度 1.5 米齐眼面部，正方位角 0°，50mm 手机等效 T2.0 面部近景，竖屏 9:16 构图，焦平面锁定肤质与妆容细节。
【微观质感证据链】：真实皮肤毛孔细纹拒绝过度磨皮塑料感；底妆水光质感；眼影珠光闪粉颗粒；口红奶油缎光；刷毛柔软；产品包装真实。
【大气体积介质】：明亮通透梳妆台，干净粉调日光，闺蜜亲密氛围，零暗调，原生 GRWM 手机质感。
iPhone 15 Pro 前置相机，50mm 等效，手机原生处理，明亮干净真实肤色，9:16 竖屏。

【English Prompt】：
GRWM beauty tutorial ad vertical still, 9:16 phone-shot, relatable beauty guru, ring light flawless skin, get-ready-with-me intimate, makeup transformation. Glamorous-yet-relatable beauty creator doing makeup at vanity, half-face done genuine bestie expression, bright airy pink-tone, smartphone front-camera close-up, ring light flattering skin. Key ring light 0° frontal soft even 4800K flawless-skin, Fill soft side 55° camera-left Key:Fill 1.8:1 gentle, no harsh shadow, practical vanity bulb, catchlight round ring 12 o'clock. Key ring 4800K CRI 95, Fill 5200K CRI 92, WB 5000K bright-pink, phone-native bright clean skin-true. Camera 1.5m eye-level face, azimuth 0°, 50mm phone-equiv T2.0 face close-up, vertical 9:16, focus skin texture makeup. Real skin pores no plastic; foundation dewy; eyeshadow shimmer pigment; lipstick creamy satin; brush bristles soft; packaging authentic. Bright airy vanity, clean pink-tone daylight, intimate bestie. iPhone 15 Pro front camera, 50mm equiv, 9:16.

【负向提示词 (Negative Prompt)】：
cinematic dark, over-smoothed plastic skin, professional studio, heavy beauty filter, moody lighting, dull colors, blurry face, distorted anatomy, extra fingers, text, watermark, low resolution, 2.39:1 widescreen.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_MUA 美妆博主】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 165cm, WEIGHT 50kg, BODY RATIO 7.3 heads, BIRTHDAY 2000.02.14, NATIONALITY Chinese, STYLE glam/relatable/beauty-guru, SPECIALTY makeup-tutorial/beauty-review. Column 2 headless front full-body standing pose cropped below chin relaxed beauty creator posture, cozy chic loungewear complete neckline-to-shoe framing showcasing silhouette. Column 3 full back view standing pose with head head-to-toe showcasing outfit back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, hairstyle A loose waves. Columns 4-6 bottom row same three-view, hairstyle B slicked-back variant. Bottom row 2 panels wardrobe and props close-up: cosmetic cream texture macro, makeup brush bristles macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm real texture fine lines no airbrush no over-smooth; hair strands distinct glossy; cosmetic cream dewy texture; makeup brush bristles soft fine; authentic product finish::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, plastic skin, heavy filter, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 165cm、体重 50kg、身材比例 7.3 头身、生日 2000.02.14、国籍 中国、风格 精致/亲和/美妆达人、特长 化妆教程/美妆测评。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图美妆创作者放松站姿，领口到鞋底完整入画，舒适时尚居家装，展示剪影。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示服装背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）造型 A 自然波浪卷；下排造型 B 后梳 slicked-back 变体。底部横排 2 格**着装道具特写**：格 1 化妆品膏体质地微距；格 2 化妆刷刷毛微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、真实细纹拒绝磨皮拒绝过度磨皮；发丝根根分明光泽；化妆品膏体水光质地；化妆刷刷毛柔软细密；产品真实质感。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, plastic skin, heavy filter, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_MUA` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相/身材比例 100% 一致；正面全身栏严禁头部入画，背面全身栏严禁缺头。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_MUA : references/assets/beauty_guru.png （美妆博主，舒适时尚居家装，AU6+AU12 闺蜜微笑，精致亲和）
- @PROD_MAKEUP : references/assets/makeup_products.png （美妆产品母版，底妆/眼影/口红，真实质地包装）
- @SCN_VANITY : references/assets/bright_vanity_setting.png （明亮通透梳妆台场景，环形灯，粉调干净）
- @PROP_BRUSH : references/assets/makeup_brush_tools.png （化妆刷工具母版，刷毛柔软细密）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 30 秒的 GRWM 美妆边化边聊竖屏序列，画幅 9:16 / 30fps / 手机原生质感。

[0.0s-5.0s]：素颜开场 + 妆容预告——@CHAR_MUA 于 @SCN_VANITY 梳妆台素颜亮相，AU6+AU12 闺蜜微笑直视镜头，手机前置 50mm 面部近景，环形灯显肤质，口语化预告今日妆容，真实素颜非磨皮。

[5.0s-18.0s]：化妆步骤边化边聊演示——@CHAR_MUA 用 @PROD_MAKEUP + @PROP_BRUSH 演示底妆/眼妆/唇妆步骤，化妆专注 AU17+AU24（下颌微收抿唇专注），边化边聊闺蜜口播，50mm 面部特写 + 产品质地特写，`[产品质地镜 AU 自动转为美妆质地动力学]`（膏体挤出/粉质飞散/刷毛扫动）。

[18.0s-25.0s]：妆效完成 reveal——@CHAR_MUA 妆容完成惊艳 reveal，AU1+AU2+AU26 张口惊喜（蜕变震撼），素颜→妆效前后对比，环形灯显妆效通透，卡点 reveal 高潮。

[25.0s-30.0s]：产品种草清单 + CTA——@PROD_MAKEUP 种草清单陈列，@CHAR_MUA 真诚安利 AU6+AU12 闺蜜微笑，指向购物车/评论区，口语化 CTA，闺蜜真心安利收尾。

[FACS/AU 表演微动作]：0.0s 为 @CHAR_MUA 的 AU6+AU12（闺蜜微笑）素颜开场，强度 B 级；5.0s 化妆演示转 AU17+AU24（化妆专注），强度 A 级（松弛专注）；18.0s reveal 升级 AU1+AU2+AU26（张口惊喜），强度 D 级（蜕变震撼）；25.0s CTA 回落 AU6+AU12 闺蜜微笑 B 级；视线 0.2s 先导在镜头与化妆间自然切换（边化边聊对话感），AU45 自然眨眼，闺蜜真诚非高冷广告腔。

[CineDance 运镜与光学]：手机前置 50mm 等效面部近景，齐眼高度 1.5m，正方位角 0°，竖屏 9:16 面部构图，化妆步骤切产品质地特写，reveal 卡点缓推，边化边聊舒缓 + 卡点，快门等效 180°，严禁过度运镜破坏亲密感。

[光影角度量化]：主光环形灯正面柔光 0° 4800K 柔和均匀显肤质讨喜；辅光侧柔光塑形左侧 55° 光比 Key:Fill 1.8:1 温柔；无硬阴影；环境 practical 梳妆台灯泡光；12 点钟环形圆形眼神光。

[色温显色]：主光环形灯 4800K CRI 95；辅光 5200K CRI 92；白平衡 5000K 明亮粉调偏置；手机原生明亮干净粉调真实肤色调色。

[微观质感证据链]：真实皮肤毛孔细纹拒绝过度磨皮塑料感；底妆水光质感；眼影珠光闪粉颗粒；口红奶油缎光；刷毛柔软；产品包装真实。

[大气体积介质]：明亮通透梳妆台，干净粉调日光，闺蜜亲密氛围，零暗调，原生 GRWM 手机质感。

[同步声锁与台词原语言保留]：No subtitles.（字幕/产品名花字须后期硬压，绝不由模型生成）。轻柔 BGM 声场——真实闺蜜口播（口语化中文/原语言）+ 化妆品 ASMR（开盖咔哒/粉扑轻拍/刷子扫动）+ 轻柔 BGM 铺底，边化边聊舒缓；台词保留原语言口语化，口型同步精准锁定。口播严禁医疗功效宣称与绝对化用语（合规红线）。

[资产单一源铁律]：@CHAR_MUA 从基准博主资产一次性生成素颜→化妆→妆效→CTA 所有状态，面部骨相 100% 一致（严禁素颜与妆效换脸），严禁链式修改；@PROD_MAKEUP 在所有帧保持产品外观/包装/质地基准一致。
[声音政策·默认无音乐] 不生成音乐 / no bgm —— 禁止任何 BGM/配乐/背景音乐；同期声（对白/环境音/动作音效/声音特效 Foley）须正常、准确、完整生成。
```

---

## 四、 黄金分镜画面完整拆解表（30 秒 GRWM 教程版）

| 时间 | 景别 | 画面内容 | AU 微表情 | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-5.0s | 面部近景 | 素颜开场今日妆容预告直视镜头 | AU6+AU12 | 手机 50mm 面部 / 环形灯显肤质 | 轻柔 BGM 起 + 闺蜜口播 |
| 5.0-18.0s | 面部+质地特写 | 化妆步骤边化边聊底妆眼妆唇妆 | AU17+AU24/[美妆动力学] | 50mm 特写 / 侧柔光塑形 | 化妆品 ASMR + 边化边聊 |
| 18.0-25.0s | 面部近景 | 妆效完成 reveal 素颜蜕变前后对比 | AU1+AU2+AU26 | 50mm 缓推 / 环形灯通透 | BGM 卡点 reveal + 惊喜 |
| 25.0-30.0s | 产品清单 | 产品种草清单陈列真诚安利 CTA | AU6+AU12 | 产品特写 / 明亮粉调 | 安利口播 + CTA + BGM 收尾 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-grwm-beauty-dna.md` | 构思美学时 | GRWM 美妆基因、闺蜜真实种草、素颜蜕变显肤质 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 四段式 GRWM、化妆步骤边化边聊、reveal 种草模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | 化妆品 ASMR、闺蜜口播、轻柔 BGM |
| `references/cinedance-camera-optics.md` | 生成视频时 | 手机 50mm 面部近景、产品质地特写、竖屏 9:16 运镜 |
| `references/perf-acting-au-system.md` | 生成人物时 | AU6+AU12 闺蜜微笑、AU17+AU24 化妆专注、reveal 惊喜、美妆质地动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | 素颜妆效渐变锁定、美妆质地动力学、梳妆台空间白模 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
