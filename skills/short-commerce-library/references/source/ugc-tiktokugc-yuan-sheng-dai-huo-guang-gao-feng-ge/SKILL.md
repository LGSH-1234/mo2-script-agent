---
name: "ugc-tiktokugc-yuan-sheng-dai-huo-guang-gao-feng-ge"
description: "以真实素人测评与手机原生手持质感，去广告化唤醒痛点与信任，打造高转化爆款带货Vlog。"
version: "4.1"
display_name: "TikTokUGC原生带货广告风格"
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
> 3. **特异性智能转译**：若画面为纯产品/静物特写（产品质地/开箱/使用演示），AU 规则自动转译为"产品物理动力学"（质地流动、光泽反射、开合结构、蒸汽/水珠），并显式声明 `[本镜无角色主体，AU 自动转为产品物理动力学]`。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：角色（`@CHAR`）、场景（`@SCN`）、道具（`@PROP`）、材质母版（`@MAT`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **去广告化原生铁律**：TikTok UGC 带货的核心是"看起来不像广告，像真实朋友推荐"——必须通过手机原生质感、环形灯平光、手持微晃、真实素人、口语化种草，构建可信的原生信任感，严禁过度精致的电影级布光、专业模特腔与硬广既视感。
> ### 🚨 【钢人论证补丁 · TikTok UGC 带货合规铁律（Bidirectional Steelmanning Fix · 软广标注/虚假种草刷单/素人证言真实/产品宣称合规/价格交易真实）】
> 1. **软广标注红线**：UGC"去广告化"本质仍是商业广告，必须依法显著标注"广告"，严禁以"真实分享/亲测/自用"伪装隐匿广告身份误导消费者（违反《广告法》第十四条广告可识别性、《互联网广告管理办法》第九条）。
> 2. **虚假种草与刷单炒信**：严禁虚构使用体验、编造素人好评、刷单炒信、虚假销量/评价/互动数据（违反《反不正当竞争法》第八条、《电子商务法》第十七条）。
> 3. **素人证言与肖像真实**：出镜素人须为真实使用者并获肖像授权，严禁雇佣"托儿"冒充真实用户、AI 伪造素人证言、盗用他人肖像（违反《广告法》第三十八条代言人须使用过商品、《民法典》肖像权）。
> 4. **产品宣称与特殊品类合规**：带货产品宣称须真实有据，食品/化妆品/医疗器械等特殊品类严禁疗效/功效虚假宣称与绝对化用语（违反《广告法》《化妆品监督管理条例》）。
> 5. **价格与交易真实**：带货价格/优惠/库存/限时须真实，严禁虚构原价、虚假促销、诱导脱离平台私下交易（违反《价格法》《电子商务法》）。


# TikTok UGC 原生带货广告全流程创作系统 V4.1

> **定位**：以 TikTok/抖音爆款 UGC 原生带货为标杆，用手机原生质感、真实素人测评、3 秒钩子与去广告化信任感，把产品转化为"像朋友推荐"的可见种草欲望。核心信条：**真实即信任，钩子即留存，原生即转化。**

---

## 一、 核心美学基因（TikTok UGC Native DNA）

| 维度 | TikTok UGC 原生带货范式 |
|---|---|
| **叙事结构** | 五段式钩子带货：①3 秒钩子（痛点/悬念/利益前置）→ ②痛点共鸣（场景代入）→ ③产品真实测评（核心卖点）→ ④效果见证（前后对比/使用感）→ ⑤CTA 行动号召（点购物车/评论区） |
| **主角设定** | 真实感素人创作者——邻家、亲和、可信，非专业模特，去广告化，"像朋友推荐"，绝非硬广腔 |
| **光影配方** | 手机原生质感，环形灯 ring light 正面平光 + 自然窗光，明亮通透，真实非电影 Key:Fill 1.5:1 低对比 |
| **焦段/机位** | 手机主摄 26mm 等效自拍视角，手持微晃真实感，竖屏 9:16，齐胸/齐眼高度 |
| **AU 微表情** | 种草兴奋 AU6+AU12 真诚微笑 + AU1+AU2 挑眉惊喜，口语化真实，纯产品转译为"产品物理动力学" |
| **节奏** | 快节奏卡点，3 秒钩子黄金，15-30 秒，信息密集，TikTok 热门 BGM 卡点 |
| **声场** | TikTok 热门 BGM 卡点 + 真实人声口播（口语化）+ 环境同期声 + 音效点缀（叮/whoosh） |
| **调色** | 手机原生高饱和明亮，真实质感，通透，非电影级调色 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: TikTok UGC native commerce ad vertical still, 9:16 phone-shot aesthetic, authentic girl-next-door creator, ring light, real review vibe, not-an-ad native feel. A relatable young creator in cozy casual outfit holding a hero product, genuine excited expression, bright airy home setting, smartphone front-camera selfie look, natural window light::3.0 
[LIGHT ANGLE] Key Light ring light 0° frontal soft even 4500K flattering flat, Fill natural window 70° camera-left Key:Fill ratio 1.5:1 airy low-contrast, no harsh rim, practical ambient home light, catchlight round ring at 12 o'clock::2.5. 
[COLOR TEMP] Key ring 4500K CRI 92, Fill window 5500K CRI 90, white balance 5000K neutral-bright, phone-native high-saturation bright clean grading::1.5. 
[CAMERA] Height 1.4m chest-to-eye selfie, azimuth 0° frontal, 26mm phone-equiv T2.0 slight handheld micro-shake, vertical 9:16 framing, focus plane on creator face and product::2.0. 
[MICRO-TEXTURE] Real skin pores fine lines no beauty-filter plastic; cozy knit fabric natural pilling; hero product authentic material finish fingerprints; home lived-in clutter real; phone-native slight noise grain::3.0. 
[ATMOSPHERE] Bright airy home, natural window daylight, real lived-in atmosphere, zero cinematic haze, authentic UGC phone-native vibe::1.5. 
iPhone 15 Pro front camera, 26mm equiv, native phone processing, bright clean, 9:16 --ar 9:16 --style raw --v 8 --s 150 --c 2 --no cinematic lighting, no studio, no professional model, no film grain, no dark moody
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
TikTok UGC 原生带货广告竖屏关键帧，9:16，手机拍摄质感，真实邻家素人创作者，环形灯，真实测评氛围，去广告化原生感。一位亲和的年轻创作者身着舒适日常装，手持主推产品，真诚兴奋表情，明亮通透居家场景，手机前置自拍视角，自然窗光。
【光影角度量化】：主光为环形灯正面平光，位于 0°、4500K、柔和均匀讨喜；辅光为自然窗光，位于摄影机左侧 70°，光比 Key:Fill = 1.5:1 通透低对比；无硬轮廓光；环境 practical 居家光；12 点钟方向存在环形圆形眼神光。
【色温显色】：主光环形灯 4500K CRI 92；窗光辅光 5500K CRI 90；白平衡 5000K 中性明亮；手机原生高饱和明亮干净调色。
【视角机位】：摄影机高度 1.4 米齐胸到齐眼自拍，正方位角 0°，26mm 手机等效 T2.0 轻微手持微晃，竖屏 9:16 构图，焦平面锁定创作者面部与产品。
【微观质感证据链】：真实皮肤毛孔细纹拒绝美颜塑料感；舒适针织面料自然起球；主推产品真实材质指纹；居家生活化杂乱真实；手机原生轻微噪点颗粒。
【大气体积介质】：明亮通透居家，自然窗光日光，真实生活化氛围，零电影雾霭，原生 UGC 手机质感。
iPhone 15 Pro 前置相机，26mm 等效，手机原生处理，明亮干净，9:16 竖屏。

【English Prompt】：
TikTok UGC native commerce ad vertical still, 9:16 phone-shot, authentic girl-next-door creator, ring light, real review vibe, not-an-ad native feel. Relatable young creator cozy casual outfit holding hero product, genuine excited expression, bright airy home, smartphone front-camera selfie, natural window light. Key ring light 0° frontal soft even 4500K flattering flat, Fill window 70° camera-left Key:Fill 1.5:1 airy, no harsh rim, catchlight round ring 12 o'clock. Key ring 4500K CRI 92, Fill window 5500K CRI 90, WB 5000K neutral-bright, phone-native high-saturation clean. Camera 1.4m chest-to-eye selfie, azimuth 0°, 26mm phone-equiv T2.0 handheld micro-shake, vertical 9:16, focus creator face product. Real skin pores no plastic; cozy knit natural pilling; hero product authentic finish; home lived-in clutter; phone-native noise grain. Bright airy home, natural window daylight, authentic UGC phone-native. iPhone 15 Pro front camera, 26mm equiv, 9:16.

【负向提示词 (Negative Prompt)】：
cinematic lighting, studio setup, professional model, film grain, dark moody, over-polished, beauty filter plastic skin, hard rim light, anamorphic, 2.39:1 widescreen, text, watermark, low resolution.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_CREATOR 真实感素人创作者】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 168cm, WEIGHT 52kg, BODY RATIO 7.2 heads, BIRTHDAY 1999.06.20, NATIONALITY Chinese, STYLE authentic/relatable/girl-next-door, SPECIALTY talking-head-review/honest-testimonial. Column 2 headless front full-body standing pose cropped below chin relaxed creator posture, cozy casual everyday outfit complete neckline-to-shoe framing showcasing relatable silhouette. Column 3 full back view standing pose with head head-to-toe showcasing outfit back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, hairstyle A natural loose hair. Columns 4-6 bottom row same three-view, hairstyle B casual claw-clip updo. Bottom row 2 panels wardrobe and props close-up: cozy knit fabric natural weave macro, hero product in-hand authentic macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm freckles fine lines no airbrush no beauty filter; hair strands distinct natural; cozy knit fabric natural pilling weave; hero product authentic material finish; relaxed genuine posture::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, plastic skin, beauty filter, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 168cm、体重 52kg、身材比例 7.2 头身、生日 1999.06.20、国籍 中国、风格 真实/亲和/邻家感、特长 口播测评/真实见证。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图创作者放松站姿，领口到鞋底完整入画，舒适日常装，展示亲和剪影。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示服装背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）造型 A 自然散发；下排造型 B 鲨鱼夹盘发。底部横排 2 格**着装道具特写**：格 1 舒适针织面料自然织纹微距；格 2 主推产品手持真实微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、雀斑细纹拒绝磨皮拒绝美颜滤镜；发丝根根分明自然；舒适针织面料自然起球织纹；主推产品真实材质质感；放松真诚体态。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, plastic skin, beauty filter, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_CREATOR` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相/身材比例 100% 一致；正面全身栏严禁头部入画，背面全身栏严禁缺头。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_CREATOR : references/assets/ugc_creator.png （真实感素人创作者，舒适日常装，AU6+AU12 真诚微笑，邻家亲和）
- @PROD_HERO : references/assets/hero_product.png （主推产品母版，真实材质质感，核心卖点可视）
- @SCN_HOME : references/assets/bright_home_setting.png （明亮通透居家真实场景，自然窗光，生活化）
- @PROP_PHONE : references/assets/phone_selfie_rig.png （手机自拍支架母版，手持微晃视角）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 15-30 秒（紧凑基线 15 秒）的 TikTok UGC 原生带货竖屏序列，画幅 9:16 / 30fps / 手机原生质感。

[0.0s-3.0s]：3 秒钩子——@CHAR_CREATOR 手持 @PROD_HERO 直视镜头，AU1+AU2 挑眉惊喜（种草兴奋），手机前置自拍视角手持微晃，环形灯正面平光，@SCN_HOME 明亮居家，口语化钩子台词前置利益点，真实原生非硬广。

[3.0s-7.0s]：痛点共鸣 + 产品真实测评——@CHAR_CREATOR 演示 @PROD_HERO 核心卖点，AU6+AU12 真诚微笑边用边说，26mm 手机视角特写产品，`[产品特写镜 AU 自动转为产品物理动力学]`（质地流动/开合结构/光泽反射），口语化真实测评。

[7.0s-12.0s]：效果见证——前后对比/使用感呈现，@CHAR_CREATOR 惊喜反应 AU1+AU2+AU26 张口惊叹，@PROD_HERO 效果可视化，快节奏卡点切换，真实见证感。

[12.0s-15.0s]：CTA 行动号召——@CHAR_CREATOR 指向购物车/评论区，AU6+AU12 真诚微笑，口语化号召台词，产品与创作者同框定格，去广告化信任收尾。

[FACS/AU 表演微动作]：0.0s 为 @CHAR_CREATOR 的 AU1+AU2（挑眉惊喜）钩子兴奋，强度 C 级；3.0s 转 AU6+AU12（真诚微笑）边用边说 B 级；7.0s 效果见证升级 AU1+AU2+AU26（张口惊叹）D 级；12.0s CTA 回落 AU6+AU12 真诚微笑 B 级；视线 0.2s 先导直视镜头（对话感），AU45 自然眨眼保持真实交流，口语化种草非专业模特腔。

[CineDance 运镜与光学]：全程手机前置 26mm 自拍视角，手持微晃真实感，齐胸到齐眼高度 1.4m，正方位角 0°，竖屏 9:16 构图，产品特写切近景，快节奏卡点切换对齐 BGM，快门等效 180°，严禁稳定器电影运镜。

[光影角度量化]：主光环形灯正面平光 0° 4500K 柔和均匀讨喜；辅光自然窗光左侧 70° 光比 Key:Fill 1.5:1 通透低对比；无硬轮廓光；环境 practical 居家光；12 点钟环形圆形眼神光。

[色温显色]：主光环形灯 4500K CRI 92；窗光辅光 5500K CRI 90；白平衡 5000K 中性明亮；手机原生高饱和明亮干净调色。

[微观质感证据链]：真实皮肤毛孔细纹拒绝美颜塑料感；舒适针织面料自然起球；主推产品真实材质指纹；居家生活化杂乱真实；手机原生轻微噪点颗粒。

[大气体积介质]：明亮通透居家，自然窗光日光，真实生活化氛围，零电影雾霭，原生 UGC 手机质感。

[同步声锁与台词原语言保留]：No subtitles.（字幕/花字须后期硬压，绝不由模型生成）。屏幕花字信息层铁律——标题党钩子花字/卖点贴纸/价格标签须后期硬压并预留竖屏 UI 安全区（顶部 15% 与底部 20% 避让 TikTok 账号名/文案/购物车图标），信息层级为钩子花字 > 卖点贴纸 > 价格 CTA。TikTok 热门 BGM 卡点声场——真实人声口播（口语化中文/原语言）+ 环境同期声 + 音效点缀（叮/whoosh/弹出音），快节奏卡点对齐画面切换；台词保留原语言口语化，口型同步精准锁定。

[资产单一源铁律]：@CHAR_CREATOR 从基准创作者资产一次性生成所有状态（钩子→测评→见证→CTA），严禁链式修改导致面部/服装漂移；@PROD_HERO 在所有帧保持产品外观/Logo/材质基准一致，严禁产品变形。
[声音政策·默认无音乐] 不生成音乐 / no bgm —— 禁止任何 BGM/配乐/背景音乐；同期声（对白/环境音/动作音效/声音特效 Foley）须正常、准确、完整生成。
```

---

## 四、 黄金分镜画面完整拆解表（15-30 秒 UGC 带货版 · 下表为 15 秒紧凑基线，各段可弹性扩展至 30 秒）

| 时间 | 景别 | 画面内容 | AU 微表情 | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-3.0s | 自拍近景 | 3 秒钩子手持产品直视镜头利益前置 | AU1+AU2 | 手机 26mm 自拍 / 环形灯平光 | 热门 BGM 起 + 钩子口播 |
| 3.0-7.0s | 产品特写 | 痛点共鸣产品真实测评核心卖点演示 | AU6+AU12/[产品动力学] | 26mm 近景 / 窗光通透 | 口播测评 + 音效点缀 |
| 7.0-12.0s | 自拍中景 | 效果见证前后对比惊喜反应 | AU1+AU2+AU26 | 手机手持微晃 / 卡点切换 | BGM 卡点高潮 + 惊叹 |
| 12.0-15.0s | 自拍近景 | CTA 行动号召指购物车产品同框定格 | AU6+AU12 | 26mm 自拍 / 环形灯 | 号召口播 + BGM 收尾 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-tiktok-ugc-native-dna.md` | 构思美学时 | UGC 原生带货基因、去广告化真实感、手机原生质感 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 五段式钩子带货、3 秒黄金钩子、CTA 转化模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | TikTok 热门 BGM 卡点、口语化口播、音效点缀 |
| `references/cinedance-camera-optics.md` | 生成视频时 | 手机 26mm 自拍视角、手持微晃、竖屏 9:16 运镜 |
| `references/perf-acting-au-system.md` | 生成人物时 | AU6+AU12 真诚微笑、AU1+AU2 挑眉种草、产品物理动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | 手机自拍轨迹、产品物理动力学、居家空间白模 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
