---
name: "ugc-tiktok-bing-du-tiao-zhan-sai-guang-gao-feng-ge"
description: "以高燃洗脑卡点BGM与极简招牌动作，配合高饱和霓虹与UGC裂变，引爆全民病毒挑战赛。"
version: "4.1"
display_name: "TikTok病毒挑战赛广告风格"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
video_model: "Seedance_2.5"
image_model: "gpt_image_2"
---

> ### 🎵 【系统默认铁律 · 音乐核心技能 · 声音政策弹性条款（最高优先级）】
> 1. **音乐为作品本体**：本技能以音乐/歌舞/MV/卡点节拍为核心表达，**音乐照常生成**，不适用「默认无 BGM」一刀切；视频提示词应标注音乐属性（曲风/BPM/情绪/卡点节拍点）。
> 2. **同期声仍必须正常准确**：对白/环境音/动作音效/Foley 照常准确生成、与音乐并存，严禁削弱。
> 3. **非音乐本体镜头**：与音乐无关的纯展示/口播镜头，不额外铺无关 BGM。
> 4. **用户要求无音乐时**：用户明确「无音乐 / no bgm」则切纯同期声模式，视频提示词末尾追加 `不生成音乐 / no bgm`。


> ### 🚨 【系统默认铁律 · 视频提示词 AU 角色微表情强制注入准则】
> 1. **默认强制性**：在图生视频（I2V）与多参视频生成阶段，提示词**必须默认带有角色 FACS/AU 精准微动作描述词**（AU 编号、解剖学肌肉位移、`A~E` 级量化强度、`0.2s 视线先导`、`AU45 眨眼抑制`）。
> 2. **豁免条件**：**除非用户在交互中明确声明"不需要表情"或"无微表情"**，否则默认所有涉及有人格属性的角色镜头均**无条件全量携带**。
> 3. **特异性智能转译**：若画面为纯动作/品牌道具/霓虹场景静物，AU 规则自动转译为"舞蹈动力学"（招牌动作节拍、肢体律动、霓虹光脉冲、卡点闪光），并显式声明 `[本镜无角色主体，AU 自动转为舞蹈动力学]`。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：角色（`@CHAR`）、场景（`@SCN`）、道具（`@PROP`）、动作母版（`@MOVE`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **病毒可复制铁律**：TikTok 挑战赛广告的核心是"让招牌动作与洗脑 BGM 可被全民复制传播"——必须通过简单可复制的招牌动作、洗脑 BGM 强卡点、hashtag 召唤、UGC 二创混剪，把品牌转化为全民参与的病毒模因，严禁高难度不可复制动作、无卡点节奏与高冷品牌腔。
> 4. **平台合规铁律（钢人论证补丁 · Bidirectional Steelmanning Fix）**：病毒挑战赛涉及重大合规红线——① BGM 须用平台商用授权曲库或原创授权，严禁未授权热门神曲侵权；② 全民 UGC 二创混剪须获素人肖像授权；③ 品牌 hashtag 挑战赛须按平台规则报备，规避下架与法律风险。


# TikTok 病毒挑战赛广告全流程创作系统 V4.1

> **定位**：以 TikTok/抖音爆款 hashtag 病毒挑战赛为标杆，用可复制招牌动作、洗脑 BGM 强卡点、霓虹活力与全民 UGC 二创，把品牌转化为全民参与的可见病毒传播欲望。核心信条：**动作即模因，卡点即病毒，参与即传播。**

---

## 一、 核心美学基因（TikTok Viral Challenge DNA）

| 维度 | TikTok 病毒挑战赛范式 |
|---|---|
| **叙事结构** | 四段式病毒挑战赛：①挑战发起（品牌示范招牌动作）→ ②洗脑 BGM 卡点动作演示（可复制模因）→ ③全民参与 UGC 二创混剪 → ④hashtag 召唤参与（品牌定格） |
| **主角设定** | 活力挑战发起人——舞蹈达人、活力、潮流，招牌动作简单可复制，绝非高冷品牌腔 |
| **光影配方** | 手机竖屏动感明亮，霓虹彩色光 + 卡点闪光，高饱和活力，Key:Fill 2:1 |
| **焦段/机位** | 手机竖屏 9:16 全身舞蹈，广角 24mm 等效，固定机位 + 卡点甩动/推拉 |
| **AU 微表情** | 活力灿笑 AU6+AU12+AU25 张口笑 + AU26 喊，舞蹈活力，纯动作转译为"舞蹈动力学" |
| **节奏** | 洗脑 BGM 强卡点，动作同步 beat，15 秒循环可复制，病毒传播 |
| **声场** | 洗脑原创 BGM/热门神曲 + 节拍卡点 + 口号 chant + hashtag 口播 |
| **调色** | 高饱和活力，霓虹彩色，明亮通透，病毒 meme 感 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: TikTok viral dance challenge ad vertical still, 9:16 phone-shot aesthetic, energetic challenger, neon colorful light, catchy beat sync, copyable signature move, hashtag challenge vibe. A trendy energetic young dancer performing a simple copyable signature move in vibrant streetwear, joyful open-mouth laugh, neon-lit dynamic setting, vertical full-body framing, high-saturation viral energy::3.0 
[LIGHT ANGLE] Key Light neon ring 20° camera-right vibrant 5500K dynamic, Fill neon bounce 40° camera-left Key:Fill ratio 2:1 energetic, Rim 150° behind beat-sync strobe flash +1.5 stop colorful edge, practical neon ambient, catchlight bright at 12 o'clock::2.5. 
[COLOR TEMP] Key neon 5500K CRI 90, Fill 5000K CRI 88, neon accents magenta/cyan, white balance 5200K vibrant bias, phone-native high-saturation neon grading::1.5. 
[CAMERA] Height 1.3m full-body dance, azimuth 0° frontal, 24mm phone-equiv wide T2.0 vertical 9:16 full-body, fixed rig + beat-sync whip/push, focus plane on dancer full body::2.0. 
[MICRO-TEXTURE] Vibrant streetwear fabric stretch sheen; energetic skin glow sweat authentic; sneaker material scuffed real; neon light bloom; phone-native slight motion blur on beat::3.0. 
[ATMOSPHERE] Neon-lit dynamic energy, colorful light bloom, viral dance-floor vibe, zero moody dark, high-energy bright immersive::1.5. 
iPhone 15 Pro, 24mm equiv wide, native phone processing, vibrant neon, 9:16 --ar 9:16 --style raw --v 8 --s 250 --c 4 --no cinematic dark, no moody, no professional studio, no slow pace, blurry face
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
TikTok 病毒挑战赛广告竖屏关键帧，9:16，手机拍摄质感，活力挑战发起人，霓虹彩色光，洗脑节拍卡点，可复制招牌动作，hashtag 挑战赛氛围。一位潮流活力的年轻舞者身着鲜艳街头运动装，表演简单可复制的招牌动作，张口灿笑活力，霓虹动感场景，竖屏全身构图，高饱和病毒活力。
【光影角度量化】：主光为霓虹环形光，位于摄影机右侧 20°、5500K、动感鲜艳；辅光为霓虹反光，位于摄影机左侧 40°，光比 Key:Fill = 2:1 活力；轮廓光为卡点频闪，位于后方 150°、过曝 +1.5 档，彩色边缘光；环境 practical 霓虹光；12 点钟方向存在明亮眼神光。
【色温显色】：主光霓虹 5500K CRI 90；辅光 5000K CRI 88；霓虹点缀品红/青色；白平衡 5200K 鲜艳偏置；手机原生高饱和霓虹调色。
【视角机位】：摄影机高度 1.3 米全身舞蹈，正方位角 0°，24mm 手机等效广角 T2.0 竖屏 9:16 全身，固定机位 + 卡点甩动/推拉，焦平面锁定舞者全身。
【微观质感证据链】：鲜艳街头运动装面料弹性光泽；活力皮肤汗光真实；运动鞋材质磨损真实；霓虹光晕；手机原生卡点轻微运动模糊。
【大气体积介质】：霓虹动感活力，彩色光晕，病毒舞池氛围，零暗调，高能量明亮沉浸。
iPhone 15 Pro，24mm 等效广角，手机原生处理，鲜艳霓虹，9:16 竖屏。

【English Prompt】：
TikTok viral dance challenge ad vertical still, 9:16 phone-shot, energetic challenger, neon colorful light, catchy beat sync, copyable signature move, hashtag challenge. Trendy energetic young dancer vibrant streetwear simple copyable signature move, joyful open-mouth laugh, neon-lit dynamic, vertical full-body, high-saturation viral energy. Key neon ring 20° camera-right vibrant 5500K, Fill neon bounce 40° camera-left Key:Fill 2:1, Rim 150° beat-sync strobe +1.5 stop colorful, practical neon, catchlight bright 12 o'clock. Key neon 5500K CRI 90, Fill 5000K CRI 88, neon magenta/cyan, WB 5200K vibrant, phone-native high-saturation neon. Camera 1.3m full-body dance, azimuth 0°, 24mm phone-equiv wide T2.0 vertical 9:16, fixed rig beat-sync whip/push, focus dancer body. Vibrant streetwear stretch sheen; energetic skin glow sweat; sneaker scuffed; neon bloom; phone motion blur. Neon dynamic energy, colorful bloom, viral dance-floor, high-energy bright. iPhone 15 Pro, 24mm equiv, 9:16.

【负向提示词 (Negative Prompt)】：
cinematic dark, moody lighting, professional studio, slow pace, complex uncopyable move, dull colors, blurry face, distorted anatomy, extra limbs, text, watermark, low resolution, 2.39:1 widescreen.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_CHALLENGER 活力挑战发起人】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 172cm, WEIGHT 58kg, BODY RATIO 7.5 heads, BIRTHDAY 2000.08.12, NATIONALITY Chinese, STYLE energetic/trendy/dance-challenge, SPECIALTY dance/choreography. Column 2 headless front full-body standing pose cropped below chin energetic dancer posture, vibrant streetwear athleisure complete neckline-to-shoe framing showcasing dance silhouette. Column 3 full back view standing pose with head head-to-toe showcasing outfit back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, hairstyle A high ponytail. Columns 4-6 bottom row same three-view, hairstyle B space buns variant. Bottom row 2 panels wardrobe and props close-up: streetwear fabric stretch sheen macro, brand prop/logo macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm energetic glow no airbrush; hair strands distinct sporty; vibrant streetwear fabric stretch sheen; sneaker material scuffed real; brand prop authentic finish::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, plastic skin, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 172cm、体重 58kg、身材比例 7.5 头身、生日 2000.08.12、国籍 中国、风格 活力/潮流/舞蹈挑战、特长 舞蹈/编舞。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图舞者活力站姿，领口到鞋底完整入画，鲜艳街头运动装，展示舞蹈剪影。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示服装背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）造型 A 高马尾；下排造型 B 双丸子头变体。底部横排 2 格**着装道具特写**：格 1 街头运动面料弹性光泽微距；格 2 品牌道具/logo 微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、活力汗光拒绝磨皮；发丝根根分明运动感；鲜艳街头运动面料弹性光泽；运动鞋材质磨损真实；品牌道具真实质感。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, plastic skin, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_CHALLENGER` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相/身材比例 100% 一致；正面全身栏严禁头部入画，背面全身栏严禁缺头。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_CHALLENGER : references/assets/viral_challenger.png （活力挑战发起人，鲜艳街头运动装，AU6+AU12+AU25 活力灿笑）
- @MOVE_SIGNATURE : references/assets/signature_move.png （招牌病毒动作母版，简单可复制模因，卡点节拍）
- @SCN_CHALLENGE : references/assets/neon_challenge_scene.png （霓虹动感挑战赛场景，彩色光晕，舞池氛围）
- @PROP_BRAND : references/assets/brand_prop_logo.png （品牌道具/logo 母版，病毒传播锚点）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 15 秒的 TikTok 病毒挑战赛广告竖屏序列（可循环），画幅 9:16 / 30fps / 手机原生质感。

[0.0s-3.0s]：挑战发起——@CHAR_CHALLENGER 于 @SCN_CHALLENGE 霓虹场景亮相，手持 @PROP_BRAND 品牌道具，AU6+AU12 活力微笑直视镜头，手机竖屏 24mm 全身，霓虹环形光，口号 chant 发起挑战，病毒开场。

[3.0s-8.0s]：洗脑 BGM 卡点招牌动作演示——@CHAR_CHALLENGER 表演 @MOVE_SIGNATURE 简单可复制招牌动作，AU25+AU26 张口活力喊，动作同步 BGM 节拍卡点，霓虹卡点频闪，24mm 广角全身固定机位 + 卡点甩动，模因可复制。

[8.0s-12.0s]：全民参与 UGC 二创混剪——多人复制 @MOVE_SIGNATURE 招牌动作，不同场景/服饰快闪混剪，活力灿笑 AU6+AU12+AU25，快节奏卡点切换，`[混剪空镜 AU 自动转为舞蹈动力学]`，病毒传播裂变感。

[12.0s-15.0s]：hashtag 召唤参与——@CHAR_CHALLENGER 与 @PROP_BRAND 品牌定格，指向 hashtag，AU6+AU12 活力微笑召唤，口号 chant，品牌与动作同框，病毒参与收尾（可循环回钩子）。

[FACS/AU 表演微动作]：0.0s 为 @CHAR_CHALLENGER 的 AU6+AU12（活力微笑）发起，强度 B 级；3.0s 招牌动作升级 AU25+AU26（张口活力喊），强度 D 级（卡点爆发）；8.0s 全民混剪活力灿笑 AU6+AU12+AU25，强度 C 级；12.0s hashtag 召唤回落 AU6+AU12 微笑 B 级；视线 0.2s 先导直视镜头（号召感），AU45 眨眼随节拍，活力潮流非高冷。

[CineDance 运镜与光学]：手机竖屏 24mm 等效广角全身舞蹈，固定机位为主，3.0s-8.0s 招牌动作配卡点甩动/推拉对齐 BGM 节拍，8.0s-12.0s 全民混剪快闪卡点切换，竖屏 9:16 全身构图，快门等效 180°，动作同步 beat。

[光影角度量化]：主光霓虹环形光右侧 20° 5500K 动感鲜艳；辅光霓虹反光左侧 40° 光比 Key:Fill 2:1 活力；轮廓光卡点频闪后方 150° +1.5 档彩色边缘；环境 practical 霓虹光；12 点钟明亮眼神光。

[色温显色]：主光霓虹 5500K CRI 90；辅光 5000K CRI 88；霓虹点缀品红/青色；白平衡 5200K 鲜艳偏置；手机原生高饱和霓虹调色。

[微观质感证据链]：鲜艳街头运动装面料弹性光泽；活力皮肤汗光真实；运动鞋材质磨损真实；霓虹光晕；手机原生卡点轻微运动模糊。

[大气体积介质]：霓虹动感活力，彩色光晕，病毒舞池氛围，零暗调，高能量明亮沉浸。

[同步声锁与台词原语言保留]：No subtitles.（字幕/hashtag 花字须后期硬压，绝不由模型生成）。洗脑 BGM 声场——原创洗脑神曲/热门 BGM 强节拍卡点 + 口号 chant + hashtag 口播，动作同步 beat，15 秒循环可复制；台词/口号保留原语言口语化，口型同步精准锁定。BGM 须平台商用授权或原创授权（严禁未授权侵权）。

[资产单一源铁律]：@CHAR_CHALLENGER 从基准发起人资产一次性生成所有状态（发起→演示→召唤），严禁链式修改；@MOVE_SIGNATURE 招牌动作在全民混剪中保持动作节拍/姿态基准一致（可复制模因零漂移）；@PROP_BRAND 品牌道具在所有帧保持 Logo/外观一致。
[声音政策·音乐核心] 音乐为作品本体，照常生成并标注（曲风/BPM/情绪/卡点节拍）；同期声（对白/环境音/动作音效/Foley）须正常准确生成；若用户要求无音乐则末尾改为「不生成音乐 / no bgm」。
```

---

## 四、 黄金分镜画面完整拆解表（15 秒病毒挑战赛循环版）

| 时间 | 景别 | 画面内容 | AU 微表情 | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-3.0s | 竖屏全身 | 挑战发起霓虹场景亮相手持品牌道具 | AU6+AU12 | 手机 24mm 全身 / 霓虹环形光 | 洗脑 BGM 起 + 口号 chant |
| 3.0-8.0s | 竖屏全身 | 洗脑 BGM 卡点招牌动作演示可复制 | AU25+AU26 | 24mm 固定机位 + 卡点甩动 | BGM 强卡点 + 活力喊 |
| 8.0-12.0s | 混剪快闪 | 全民参与 UGC 二创复制招牌动作 | AU6+AU12+AU25 | 多场景快闪 / 卡点切换 | BGM 卡点高潮 + 群喊 |
| 12.0-15.0s | 竖屏定格 | hashtag 召唤参与品牌动作同框定格 | AU6+AU12 | 24mm 定格 / 霓虹 | 号召 chant + BGM 循环点 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-tiktok-viral-challenge-dna.md` | 构思美学时 | 病毒挑战赛基因、可复制模因、洗脑 BGM 卡点 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 四段式挑战赛、招牌动作演示、hashtag 召唤模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | 洗脑原创 BGM 卡点、口号 chant、节拍同步 |
| `references/cinedance-camera-optics.md` | 生成视频时 | 手机 24mm 全身舞蹈、卡点甩动、竖屏 9:16 运镜 |
| `references/perf-acting-au-system.md` | 生成人物时 | AU6+AU12+AU25 活力灿笑、AU25+AU26 喊、舞蹈动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | 招牌动作轨迹、卡点节拍动力学、霓虹场景白模 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
