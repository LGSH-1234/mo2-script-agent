---
name: "ugc-wang-hong-tan-dian-vlog-guang-gao-feng-ge"
description: "第一人称沉浸式手持探店，真实环境光与探店表情，打造高转化到店种草Vlog。"
version: "4.1"
display_name: "网红探店Vlog广告风格"
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
> 1. **默认强制性**：在图生视频（I2V）与多参视频生成阶段，涉及**角色**（如探店达人 `@CHAR_INFLUENCER`）的提示词**必须默认带有角色 FACS/AU 精准微动作描述词**（AU 编号、解剖学肌肉位移、`A~E` 级量化强度、`0.2s 视线先导`、`AU45 眨眼抑制`）。
> 2. **豁免条件**：**除非用户在交互中明确声明"不需要表情"或"无微表情"**，否则默认所有涉及有人格属性的角色镜头均**无条件全量携带**。
> 3. **特异性智能转译（店铺环境/产品专属）**：店铺环境/招牌菜品/陈列商品无人类面部主体，故该类镜头 AU 规则**强制转译为"环境与产品动力学"**（招牌菜品热气/摆盘呈现/商品陈列/空间氛围/上菜动作），并显式声明 `[本镜无角色面部主体，AU 自动转为环境与产品动力学]`；纯街景/门头空镜同理转译。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：探店达人（`@CHAR_INFLUENCER`）、场景（`@SCN_STORE`）、招牌产品（`@PROD_STORE`）、道具（`@PROP_VLOG`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成（达人须同一面部骨相；店铺须同一空间、同招牌、同装修风格 100% 一致，严禁店铺漂移换店）。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **真实到店沉浸铁律**：网红探店 Vlog 广告的核心是"用真实到店体验 + 第一人称沉浸感把线下店铺转化为可见的探店种草"——必须通过店内真实环境光、第一人称手持 Vlog 运镜、达人真实惊艳反应、招牌产品呈现，制造沉浸代入，严禁虚假好评/刷单炒信、恰饭不标注、虚假优惠与误导到店。
> ### 🚨 【钢人论证补丁 · 探店 Vlog 合规铁律（Bidirectional Steelmanning Fix · 虚假好评与恰饭暗广双高发品类）】
> 1. **严禁虚假好评/刷单炒信（法律红线）**：严守《反不正当竞争法》第八条与《消费者权益保护法》——探店评价须基于真实到店体验，**严禁收钱发虚假好评、虚构排队人气、夸大体验、刷单炒信、雇水军控评**，误导消费者即违法。
> 2. **软广依法标注义务**：严守《互联网广告管理办法》——通过体验分享/探店形式推销商品或服务并附购物链接、引导到店的，**须显著标明"广告"**；恰饭探店/商务合作/免费招待须主动披露利益关系，严禁"暗广"隐瞒。
> 3. **餐饮食品安全与反浪费**：餐饮探店须核验商家资质（食品经营许可/卫生），严禁推荐无证经营或卫生不合格店铺；严守《反食品浪费法》，严禁"大胃王/点一大桌吃不完/暴饮暴食"式浪费粮食探店。
> 4. **商家授权与顾客隐私**：探店拍摄须获商家拍摄授权，尊重商标/装潢权益，严禁恶意差评勒索；拍摄须保护店内其他顾客肖像/隐私（打码或获同意），不得侵犯第三方合法权益。
> 5. **价格优惠真实·主观声明**：团购/优惠/人均价格须真实有效、明码标价（《价格法》），严禁虚构原价/虚假折扣/误导到店；探店评价须标注"个人主观体验仅供参考"，不得以偏概全绝对化，带货须合规。


# 网红探店 Vlog 广告全流程创作系统 V4.1

> **定位**：以 TikTok/抖音/小红书爆款网红探店 Vlog 为标杆，用真实到店体验、第一人称手持沉浸运镜、达人真实惊艳反应与招牌产品呈现，把线下店铺转化为可见的沉浸式探店种草欲望。核心信条：**到店即真实，沉浸即代入，招牌即种草。**

---

## 一、 核心美学基因（Influencer Store Visit Vlog DNA）

| 维度 | 网红探店 Vlog 范式 |
|---|---|
| **叙事结构** | 四段式探店：①到店门口悬念开场（排队王/网红店）→ ②店内环境氛围沉浸探店 → ③招牌产品试吃试用高潮 → ④探店总结地址种草 CTA |
| **主角设定** | 探店达人（时尚、活力、真实），第一人称视角主导 + 店铺"第二主角"，绝非摆拍硬广 |
| **光影配方** | 店内真实环境光，窗光 + practical 店内暖灯，右侧 40° 4200K，Key:Fill 1.8:1 氛围真实 |
| **焦段/机位** | 手机竖屏 9:16，第一人称手持 Vlog（自拍杆/稳定器）+ 环境广角（24mm 等效）+ 招牌特写（50mm 等效） |
| **AU 微表情** | 探店期待 AU1+AU2 + 招牌惊艳 AU26 张口 + 满足 AU6+AU12，店铺转"环境与产品动力学" |
| **节奏** | 轻快沉浸，Vlog 跳切/甩镜转场，招牌高潮，20-30 秒探店弧 |
| **声场** | 店内真实环境音（人声/餐具/氛围）+ 轻快 Vlog BGM + 达人探店口播 |
| **调色** | 真实氛围暖调，店铺质感通透，拒绝过度滤镜失真，还原真实到店感 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: Influencer store visit vlog ad vertical still, 9:16 phone-shot aesthetic, first-person immersive store visit, authentic ambient store light, genuine arrival experience, signature dish reveal. A stylish influencer vlogging inside a popular restaurant, warm ambient light, excited anticipatory gaze, authentic store atmosphere, vertical framing, immersive vlog mood::3.0 
[LIGHT ANGLE] Key Light window + practical warm pendant 40° camera-right 4200K authentic ambient shaping, Fill bounce 45° camera-left Key:Fill ratio 1.8:1 natural store mood, Rim warm tungsten 150° behind +0.6 stop cozy halo, practical neon sign accent, catchlight soft warm at 10 o'clock in both eyes::2.5. 
[COLOR TEMP] Key 4200K CRI 93 warm ambient, Fill 4000K CRI 91, tungsten practical bias, white balance 4200K cozy, phone-native authentic store grading::1.5. 
[CAMERA] First-person selfie-stick POV height 1.5m, azimuth 10° slight angle, 24mm wide store environment + 50mm phone-equiv signature dish T2.0 vertical 9:16, focus plane on influencer face and dish, shallow DOF store bokeh::2.0. 
[MICRO-TEXTURE] Signature dish steam fresh glisten; authentic store interior textures; influencer skin pores real no airbrush; tableware material detail; ambient dust in light beam::3.0. 
[ATMOSPHERE] Authentic popular store bustling vibe, warm ambient haze, immersive genuine presence, zero studio zero fake, real store-visit trustworthy immersive::1.5. 
iPhone 15 Pro, 24mm wide equiv, native phone processing, authentic warm store, 9:16 --ar 9:16 --style raw --v 8 --s 250 --c 5 --no studio light, no fake set, no over-filtered, distorted anatomy, blurry face
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
网红探店 Vlog 广告竖屏关键帧，9:16，手机拍摄质感，第一人称沉浸式探店，真实店内环境光，真实到店体验，招牌菜品呈现。一位时尚达人于人气餐厅内手持 Vlog，暖调环境光，兴奋期待目光，真实店铺氛围，竖屏构图，沉浸 Vlog 感。
【光影角度量化】：主光为窗光 + practical 暖调吊灯，位于摄影机右侧 40°、4200K、真实环境塑形；辅光为反光补光，位于摄影机左侧 45°，光比 Key:Fill = 1.8:1 自然店内氛围；轮廓光为暖调钨丝逆光，位于后方 150°、过曝 +0.6 档温馨光晕；环境 practical 霓虹招牌点缀；达人眼中 10 点钟方向存在柔和暖调眼神光。
【色温显色】：主光 4200K CRI 93 暖调环境；辅光 4000K CRI 91；钨丝 practical 偏置；白平衡 4200K 温馨；手机原生真实店铺调色。
【视角机位】：第一人称自拍杆视角高度 1.5 米，方位角 10° 微侧，环境广角 24mm + 招牌菜品 50mm 手机等效 T2.0 竖屏 9:16，焦平面锁定达人面部与菜品，浅景深店铺虚化。
【微观质感证据链】：招牌菜品热气新鲜油亮；真实店铺室内材质；达人皮肤毛孔真实拒绝磨皮；餐具材质细节；光束中氛围尘埃。
【大气体积介质】：真实人气店铺热闹氛围，暖调环境雾霭，沉浸真实在场感，零影棚零虚假，真实探店可信沉浸。
iPhone 15 Pro，24mm 广角等效，手机原生处理，真实暖调店铺，9:16 竖屏。

【English Prompt】：
Influencer store visit vlog ad vertical still, 9:16 phone-shot, first-person immersive store visit, authentic ambient store light, genuine arrival experience, signature dish reveal. Stylish influencer vlogging inside popular restaurant, warm ambient light, excited anticipatory gaze, authentic store atmosphere, vertical, immersive vlog. Key window + practical warm pendant 40° camera-right 4200K authentic, Fill bounce 45° camera-left Key:Fill 1.8:1 natural, Rim warm tungsten 150° +0.6 stop cozy halo, neon sign accent, catchlight soft warm 10 o'clock both eyes. Key 4200K CRI 93 warm, Fill 4000K CRI 91, tungsten bias, WB 4200K cozy, phone-native authentic store. Camera first-person selfie-stick POV 1.5m, azimuth 10° slight, 24mm wide store + 50mm phone-equiv dish T2.0 vertical 9:16, focus influencer face dish, shallow DOF bokeh. Signature dish steam glisten; authentic store interior; influencer skin pores no airbrush; tableware detail; ambient dust in beam. Authentic popular store bustling, warm ambient haze, immersive genuine. iPhone 15 Pro, 24mm wide equiv, 9:16.

【负向提示词 (Negative Prompt)】：
studio light, fake set, over-filtered, distorted anatomy, blurry face, plastic skin, empty fake store, text, watermark, low resolution, 2.39:1 widescreen.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；探店达人 `@CHAR_INFLUENCER` 用标准 10 格 Model Card；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_INFLUENCER 探店达人】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 165cm, WEIGHT 48kg, BODY RATIO 7.4 heads, BIRTHDAY 1999.03.22, NATIONALITY Chinese, STYLE trendy/energetic/authentic, SPECIALTY store visit/food review. Column 2 headless front full-body standing pose cropped below chin trendy energetic posture, fashionable street outfit complete neckline-to-shoe framing. Column 3 full back view standing pose with head head-to-toe showcasing outfit back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, hairstyle A trendy waves. Columns 4-6 bottom row same three-view, hairstyle B casual ponytail variant. Bottom row 2 panels props close-up: signature dish plating macro, handheld gimbal selfie stick macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm authentic no airbrush; hair strands distinct trendy; signature dish fresh glisten; gimbal metal detail; no plastic skin::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, plastic skin, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 165cm、体重 48kg、身材比例 7.4 头身、生日 1999.03.22、国籍 中国、风格 时尚/活力/真实、特长 探店/美食探店。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图达人时尚活力站姿，领口到鞋底完整入画，潮流街拍着装。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示着装背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）造型 A 时尚波浪；下排造型 B 休闲马尾变体。底部横排 2 格**道具特写**：格 1 招牌菜品摆盘微距；格 2 手持稳定器自拍杆微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、真实拒绝磨皮；发丝根根分明时尚；招牌菜品新鲜油亮；稳定器金属细节；拒绝塑料皮肤。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, plastic skin, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_INFLUENCER` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相/身材比例 100% 一致（同一张脸）；正面全身栏严禁头部入画，背面全身栏严禁缺头。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_INFLUENCER : references/assets/influencer.png （探店达人，全片同一面部骨相，时尚活力真实）
- @SCN_STORE : references/assets/store_scene.png （店铺场景母版，同一空间同招牌同装修，真实人气氛围）
- @PROD_STORE : references/assets/signature_product.png （招牌产品/菜品母版，店铺招牌爆品）
- @PROP_VLOG : references/assets/vlog_props.png （Vlog 道具母版，手持稳定器/自拍杆）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 26 秒的网红探店 Vlog 广告竖屏序列，画幅 9:16 / 30fps / 手机原生质感。

[0.0s-6.0s]：到店门口悬念开场——@CHAR_INFLUENCER 于 @SCN_STORE 门口手持 Vlog（自拍杆视角），门头招牌/排队人气入画，达人 AU1+AU2 挑眉期待"这家终于来了"，环境 [环境与产品动力学]（门头/排队/招牌亮相），手机竖屏 24mm 环境广角，4 秒探店钩子。

[6.0s-14.0s]：店内环境氛围沉浸探店——@CHAR_INFLUENCER 第一人称走进 @SCN_STORE 店内，环境广角扫过装修/氛围/客座，达人 AU1 好奇环视，环境 [环境与产品动力学]（空间氛围/陈列/上菜），甩镜/跳切 Vlog 转场，沉浸到店感。

[14.0s-21.0s]：招牌产品试吃试用高潮——@SCN_STORE 招牌 @PROD_STORE 呈现（热气/摆盘），@CHAR_INFLUENCER 试吃试用惊艳反应 AU26 张口 + AU6+AU12 满足眯眼，产品 [环境与产品动力学]（招牌热气/摆盘呈现），50mm 招牌特写，探店高潮顶点。

[21.0s-26.0s]：探店总结地址种草 CTA——@CHAR_INFLUENCER 真实口播探店总结（推荐指数/人均/地址），达人 AU6+AU12 满足真诚，店铺招牌与地址自然露出，沉浸探店种草收尾。

[FACS/AU 表演微动作]：@CHAR_INFLUENCER 探店达人——0.0s 起 AU1+AU2（挑眉期待到店），强度 B 级（真实期待）；6.0s 进店 AU1 内眉上提（好奇环视），强度 B 级；14.0s 招牌惊艳 AU26 下颌下降张口（惊艳）+ AU6+AU12 满足眯眼（好吃好用），强度 C 级（真实惊艳反应）；21.0s CTA AU6+AU12 满足真诚（推荐），强度 B 级；视线 0.2s 先导自然扫视环境与招牌（沉浸探店），AU45 自然眨眼；@PROD_STORE/@SCN_STORE——[环境与产品动力学] 门头招牌/排队人气/空间氛围/招牌热气/摆盘呈现/上菜动作，并声明 `[本镜无角色面部主体，AU 自动转为环境与产品动力学]`。

[CineDance 运镜与光学]：手机竖屏第一人称手持 Vlog（自拍杆/稳定器），环境广角 24mm 等效（到店/店内空间）+ 招牌特写 50mm 等效 T2.0（试吃），自拍杆视角高度 1.5m，方位角 10° 微侧，浅景深店铺虚化，Vlog 跳切/甩镜转场/遮挡转场，招牌高潮缓推，竖屏 9:16 构图，快门等效 180°，运动轻快真实手持感。

[光影角度量化]：主光窗光 + practical 暖调吊灯右侧 40° 4200K 真实环境塑形；辅光反光补光左侧 45° 光比 Key:Fill 1.8:1 自然店内氛围；轮廓光暖调钨丝逆光后方 150° +0.6 档温馨光晕；环境 practical 霓虹招牌点缀；达人眼中 10 点钟柔和暖调眼神光。

[色温显色]：主光 4200K CRI 93 暖调环境；辅光 4000K CRI 91；钨丝 practical 偏置；白平衡 4200K 温馨；手机原生真实店铺调色。

[微观质感证据链]：招牌菜品热气新鲜油亮；真实店铺室内材质；达人皮肤毛孔真实拒绝磨皮；餐具材质细节；光束中氛围尘埃。

[大气体积介质]：真实人气店铺热闹氛围，暖调环境雾霭，沉浸真实在场感，零影棚零虚假，真实探店可信沉浸。

[同步声锁与台词原语言保留]：No subtitles.（字幕/地址信息/探店花字须后期硬压，绝不由模型生成）。探店声场——店内真实环境音（人声/餐具/氛围）+ 轻快 Vlog BGM + 达人探店口播，声画同步精准，26 秒探店弧；台词保留原语言口语化真实自然，口型同步精准锁定。

[资产单一源铁律]：@CHAR_INFLUENCER 从基准达人资产一次性生成所有镜头状态，**面部骨相 100% 一致（同一张脸）**；@SCN_STORE 店铺须同一空间、同招牌、同装修风格 100% 一致（严禁换店/改装修）；@PROD_STORE 招牌产品保持基准一致；严禁链式修改导致达人/店铺/产品漂移。
[声音政策·默认无音乐] 不生成音乐 / no bgm —— 禁止任何 BGM/配乐/背景音乐；同期声（对白/环境音/动作音效/声音特效 Foley）须正常、准确、完整生成。
```

---

## 四、 黄金分镜画面完整拆解表（26 秒网红探店 Vlog 版）

| 时间 | 景别 | 画面内容 | 表演（AU/环境动力学） | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-6.0s | 环境广角 | 到店门口悬念开场 | 达人 AU1+AU2 期待 / 门头排队动力学 | 24mm 自拍杆 1.5m / 真实环境光 | 店内环境音 + Vlog BGM |
| 6.0-14.0s | 广角跟随 | 店内环境氛围沉浸探店 | 达人 AU1 好奇环视 / 空间氛围动力学 | 24mm 甩镜跳切 / practical 暖灯 | 环境音 + 探店口播 |
| 14.0-21.0s | 招牌特写 | 招牌产品试吃试用高潮 | 惊艳 AU26 / 满足 AU6+AU12 / 热气动力学 | 50mm 特写 / Key:Fill 1.8:1 | 试吃 ASMR + 惊艳口播 |
| 21.0-26.0s | 中景定格 | 探店总结地址种草 CTA | 达人 AU6+AU12 满足真诚 | 中景定格 / 暖调氛围 | 真实总结口播 + 地址 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-store-visit-vlog-dna.md` | 构思美学时 | 探店 Vlog 基因、店内真实环境光、第一人称沉浸探店 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 四段式探店、到店悬念钩子、招牌试吃高潮模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | 店内环境音、轻快 Vlog BGM、达人探店口播 |
| `references/cinedance-camera-optics.md` | 生成视频时 | 第一人称手持 Vlog 运镜、环境广角、招牌特写、竖屏 9:16 |
| `references/perf-acting-au-system.md` | 生成角色时 | 探店期待 AU1+AU2、招牌惊艳 AU26、环境与产品动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | 店内空间布局锁定、第一人称运镜轨迹、真实环境光渲染 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
