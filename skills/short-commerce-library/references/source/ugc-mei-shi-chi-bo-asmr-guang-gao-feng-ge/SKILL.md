---
name: "ugc-mei-shi-chi-bo-asmr-guang-gao-feng-ge"
description: "以暖调食欲微距与极致真实咀嚼ASMR声场，展现爆汁拉丝与陶醉表情，引爆屏幕食欲种草。"
version: "4.1"
display_name: "美食吃播ASMR广告风格"
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
> 3. **特异性智能转译**：若画面为纯食物/质地/空镜（无角色主体），AU 规则自动转译为"食物质地动力学"（爆汁飞溅、拉丝垂坠、热气升腾、油亮流动、酥脆掉渣），并显式声明 `[本镜无角色主体，AU 自动转为食物质地动力学]`。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：角色（`@CHAR`）、场景（`@SCN`）、食物（`@FOOD`）、道具（`@PROP`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用。
> 2. **绝对禁止链式修改**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成（食物特写与吃播须同一份食物、同一张脸）。
> ### 🚨 【V4.1 增强铁律 · 极致准确顶级光影角度/视角/质感工业量化层】
> 1. **文生图强制携带**：所有文生图提示词**必须**显式携带五个量化子层——光源角度、色温显色、视角机位、微观质感证据链、大气体积介质。
> 2. **多图参考生视频中文描述铁律**：图生视频阶段（I2V）与多图参考生视频阶段（Multi-Ref I2V），提示词**除台词（Dialogue）外，整体描述必须用中文表示**。
> 3. **食欲沉浸铁律**：美食吃播 ASMR 广告的核心是"用真实食物质感 + ASMR 声场把食欲转化为可见的种草欲望"——必须通过暖调食欲光显油亮质感、微距断面爆汁特写、真实咀嚼酥脆音、满足吃播微表情，制造"隔着屏幕都闻到香味"的沉浸，严禁食物失真塑料感、声画脱节与假吃摆拍。
> ### 🚨 【钢人论证补丁 · 美食吃播合规铁律（Bidirectional Steelmanning Fix · 严禁浪费造假 + 食品带货落点）】
> 1. **严禁浪费粮食式暴食**：吃播须"适量真实享用/光盘"，**严禁大胃王猎奇暴食、暴饮暴食、浪费粮食式堆量**（平台明令严打），严禁以"能吃多少"为噱头，食欲吸引靠食物品质与享用满足感而非进食量。
> 2. **严禁假吃造假**：吃播须真实咀嚼吞咽，**严禁假吃、催吐、剪辑造假、借位偷换食物**（欺骗消费者、危害健康），ASMR 咀嚼音须与真实进食声画同步。
> 3. **食品安全与宣传合规**：严禁生食野味/过期/不洁等危险食物演示，严禁"最"字绝对化用语，严禁夸大保健/减肥/治病功效与伪科学养生宣称，食品须符合卫生与安全规范。
> 4. **食品带货落点铁律**：美食广告的商业目的是卖食品/引流——须明确带货落点（食品/零食包装 SKU、店铺到店引流、厨具/调味品），享用镜头须露出可识别商品包装/品牌/购买锚点，严禁纯吃播内容而无商品转化落点。


# 美食吃播 ASMR 广告全流程创作系统 V4.1

> **定位**：以 TikTok/抖音爆款美食吃播 ASMR 为标杆，用极致食物微距特写、真实咀嚼酥脆 ASMR 声场、大口爆汁拉丝断面与满足吃播表情，把美食转化为可见的食欲种草欲望。核心信条：**食欲即钩子，声音即沉浸，爆汁即高潮。**

---

## 一、 核心美学基因（Food Mukbang ASMR DNA）

| 维度 | 美食吃播 ASMR 范式 |
|---|---|
| **叙事结构** | 四段式吃播：①食物诱人特写开场（爆汁/拉丝/热气）→ ②大口吃播 ASMR（咀嚼/酥脆音）→ ③美食高潮（断面/爆浆/满足表情）→ ④食谱店铺种草 CTA |
| **主角设定** | 美食博主——亲和、真实、吃货感，享受食物的满足表情，绝非高冷美食广告腔 |
| **光影配方** | 暖调食欲光，主光 3800K 显油亮质感，热气逆光轮廓，Key:Fill 2:1 通透食欲 |
| **焦段/机位** | 手机竖屏 9:16，微距食物特写（100mm 等效）+ 面部吃播近景（50mm 等效），齐桌俯拍/平视 |
| **AU 微表情** | 咬下 AU26 张口 + 满足 AU6+AU12 眯眼微笑 + 回味 AU17，纯食物转译为"食物质地动力学" |
| **节奏** | 舒缓沉浸 ASMR 节奏，食物特写慢镜 + 吃播实时，断面高潮卡点 |
| **声场** | ASMR 咀嚼音/酥脆音/爆汁音/切菜音 + 轻柔 BGM + 满足口播 |
| **调色** | 暖调高饱和食欲色，油亮通透，热气氤氲，拒绝冷调失真 |

---

## 二、 文生图双版本核心提示词标准（V4.1 增强）

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8 · V4.1 增强)
```text
/imagine prompt: Food mukbang ASMR ad vertical still, 9:16 phone-shot aesthetic, extreme macro food close-up, juicy bite moment, steam rising, glossy appetite appeal, satisfied foodie creator. A food creator mid-bite into a glistening juicy dish, eyes closed in bliss, steam and sauce highlights, macro texture detail, vertical framing, warm appetizing tone::3.0 
[LIGHT ANGLE] Key Light warm softbox 40° camera-right 3800K appetite shaping glossy highlights, Fill bounce 50° camera-left Key:Fill ratio 2:1 appetizing, Rim 160° behind steam backlight +1.2 stop edge glow, practical warm accent, catchlight soft at 10 o'clock::2.5. 
[COLOR TEMP] Key 3800K CRI 95 warm, Fill 4000K CRI 92, warm amber bias, white balance 3900K appetite warm, phone-native high-saturation food grading::1.5. 
[CAMERA] Macro food 100mm equiv T2.8 focus sauce sheen, face 50mm equiv near, height table-level 0.9m, azimuth 20° three-quarter, vertical 9:16, focus plane on food texture and bite::2.0. 
[MICRO-TEXTURE] Juicy sauce gloss droplets; crispy golden crust crumbs; melting cheese pull strands; fresh ingredient pores; steam vapor wisps; realistic food surface no plastic::3.0. 
[ATMOSPHERE] Warm appetizing steam haze, cozy food immersion, glossy vibrant vibe, zero cold zero dull, mouth-watering ASMR immersive::1.5. 
iPhone 15 Pro, 100mm macro equiv, native phone processing, warm appetizing, 9:16 --ar 9:16 --style raw --v 8 --s 250 --c 4 --no plastic food, no cold tone, no fake styling, blurry texture, artificial garnish
```

### 🌐 常规通用版本 (nano banana/GPT image2 · V4.1 增强)
```text
【中文提示词】：
美食吃播 ASMR 广告竖屏关键帧，9:16，手机拍摄质感，极致微距食物特写，爆汁咬下瞬间，热气升腾，油亮食欲感，满足吃货博主。一位美食博主正咬下一口油亮多汁的料理，满足眯眼陶醉，热气与酱汁高光，微距质感细节，竖屏构图，暖调食欲色。
【光影角度量化】：主光为暖调柔光箱，位于摄影机右侧 40°、3800K、食欲塑形显油亮高光；辅光为反光补光，位于摄影机左侧 50°，光比 Key:Fill = 2:1 通透食欲；轮廓光为热气逆光，位于后方 160°、过曝 +1.2 档边缘光晕；环境 practical 暖调点缀；10 点钟方向存在柔和眼神光。
【色温显色】：主光 3800K CRI 95 暖调；辅光 4000K CRI 92；暖琥珀偏置；白平衡 3900K 食欲暖调；手机原生高饱和美食调色。
【视角机位】：微距食物 100mm 等效 T2.8 焦点锁酱汁光泽，面部 50mm 等效近景，机位齐桌高度 0.9 米，方位角 20° 四分之三侧，竖屏 9:16，焦平面锁定食物质感与咬下瞬间。
【微观质感证据链】：多汁酱汁光泽油滴；酥脆金黄外皮碎屑；融化芝士拉丝；新鲜食材纹理气孔；热气氤氲丝缕；真实食物表面拒绝塑料感。
【大气体积介质】：暖调食欲热气雾霭，温馨美食沉浸，油亮鲜艳氛围，零冷调零平淡，令人垂涎 ASMR 沉浸。
iPhone 15 Pro，100mm 微距等效，手机原生处理，暖调食欲，9:16 竖屏。

【English Prompt】：
Food mukbang ASMR ad vertical still, 9:16 phone-shot, extreme macro food close-up, juicy bite moment, steam rising, glossy appetite, satisfied foodie. Food creator mid-bite glistening juicy dish, eyes closed bliss, steam sauce highlights, macro texture, vertical, warm appetizing. Key warm softbox 40° camera-right 3800K appetite glossy, Fill bounce 50° camera-left Key:Fill 2:1, Rim 160° steam backlight +1.2 stop, warm accent, catchlight soft 10 o'clock. Key 3800K CRI 95, Fill 4000K CRI 92, amber bias, WB 3900K warm, phone-native high-saturation food. Camera macro 100mm equiv T2.8 sauce sheen, face 50mm near, table-level 0.9m, azimuth 20° three-quarter, vertical 9:16, focus food texture bite. Juicy sauce gloss droplets; crispy golden crust crumbs; melting cheese pull; fresh ingredient pores; steam wisps; realistic no plastic. Warm appetizing steam haze, cozy food immersion, glossy vibrant. iPhone 15 Pro, 100mm macro equiv, 9:16.

【负向提示词 (Negative Prompt)】：
plastic fake food, cold tone, artificial garnish, fake styling, blurry texture, unappetizing, dull grey, distorted hands, extra fingers, text, watermark, low resolution, 2.39:1 widescreen.
```

### 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> 用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出本版本（与上方双版本并列的第三可选版本）；版面/光学/纪律详见 `references/midjourney-v8-t2i-engine.md` §七。

```text
【MJ v8 Model Card 版 · @CHAR_FOODIE 美食博主】
/imagine prompt: professional model card character asset sheet, 10-panel grid on pure white background. Left data bar: MODEL CARD, HEIGHT 168cm, WEIGHT 55kg, BODY RATIO 7.4 heads, BIRTHDAY 1998.05.20, NATIONALITY Chinese, STYLE warm/foodie/authentic, SPECIALTY mukbang/food-review. Column 2 headless front full-body standing pose cropped below chin relaxed foodie posture, cozy casual outfit complete neckline-to-shoe framing. Column 3 full back view standing pose with head head-to-toe showcasing outfit back detail. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head, hairstyle A neat casual. Columns 4-6 bottom row same three-view, hairstyle B relaxed variant. Bottom row 2 panels props close-up: signature dish glossy macro, hands holding chopsticks authentic macro::3.0 
[LIGHT ANGLE] Key 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock::2.5. 
[COLOR TEMP] Key 5600K CRI 99 neutral, WB 5600K zero bias::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin pores 40μm warm authentic no airbrush; hair strands distinct; signature dish sauce gloss realistic; hands skin texture authentic; chopsticks material real::3.0. 
[ATMOSPHERE] zero dust zero haze pure white infinite void no floor shadow::1.5. 
ARRI ALEXA 35, Zeiss Supreme 50mm T4.0, no filtration, Kodak Vision3 50D grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, plastic skin, inconsistent face between panels

【通用 Model Card 版 · 中文】
专业角色资产卡（Model Card），纯白背景 10 格拼图。左侧数据栏：MODEL CARD、身高 168cm、体重 55kg、身材比例 7.4 头身、生日 1998.05.20、国籍 中国、风格 亲和/吃货/真实、特长 吃播/美食鉴赏。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图博主松弛站姿，领口到鞋底完整入画，温馨休闲着装。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示着装背面细节。第 4-6 列上排头部三视角（正面胸像/左 90° 侧面/正背面后脑）造型 A 整洁休闲；下排造型 B 松弛变体。底部横排 2 格**道具特写**：格 1 招牌料理油亮微距；格 2 手持筷子真实微距。【光影角度量化】主光正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴 Key:Fill 1:1 零阴影；背景光 180° 纯白环形墙洗墙 100%；眼神光 12 点钟。【色温显色】5600K CRI 99 零偏置。【视角机位】全身两栏摄影机高度 1.2m 正/背方位角 0°/180° 50mm T4.0 深景深；头部六格 1.6m 方位角 0°/90°/180° 85mm T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈零畸变。【微观质感证据链】皮肤毛孔 40μm、暖调真实拒绝磨皮；发丝根根分明；招牌料理酱汁光泽真实；手部皮肤质感真实；筷子材质真实。【大气】零尘埃零雾霭纯白无限虚空、地面无阴影。
【负向】directional shadow, dramatic lighting, floor shadow, plastic skin, inconsistent face between panels, head visible in headless column, missing back view column, text typo, watermark.

【资产卡登记铁律】：产出后登记为 `@CHAR_FOODIE` 基准资产，后续所有分镜与 I2V 以 @ 显式引用；7 项数据单一源禁止链式修改；10 格面部骨相/身材比例 100% 一致（食物特写与吃播同一张脸）；正面全身栏严禁头部入画，背面全身栏严禁缺头。
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine · V4.1 中文描述)

```text
【多参考素材锁定层】：
- @CHAR_FOODIE : references/assets/foodie_creator.png （美食博主，食物特写与吃播同一面部骨相，亲和吃货感）
- @FOOD_HERO : references/assets/hero_dish.png （招牌料理母版，油亮多汁，爆汁拉丝质感基线）
- @SCN_TABLE : references/assets/dining_table.png （餐桌场景母版，暖调食欲氛围，温馨沉浸）
- @PROP_UTENSIL : references/assets/utensils.png （餐具道具母版，筷子/刀叉/器皿，真实质感）

【提示词正文（11 段式 · 中文描述 + 台词例外）】：
（多图参考视频生成）：一段 20 秒的美食吃播 ASMR 广告竖屏序列，画幅 9:16 / 30fps / 手机原生质感。

[0.0s-4.0s]：食物诱人特写开场——@FOOD_HERO 招牌料理于 @SCN_TABLE，微距 100mm 等效特写，热气升腾、酱汁油亮流动，`[本镜无角色主体，AU 自动转为食物质地动力学]`，暖调食欲光，3 秒钩子锁住食欲。

[4.0s-9.0s]：大口吃播 ASMR——@CHAR_FOODIE 用 @PROP_UTENSIL 夹起 @FOOD_HERO 大口咬下，AU26 张口咬合，咀嚼酥脆 ASMR 音，面部 50mm 近景满足神态，暖调食欲光显油亮。

[9.0s-15.0s]：美食高潮断面爆浆——@FOOD_HERO 断面微距特写，爆汁飞溅/芝士拉丝垂坠/酥脆掉渣，`[食物质地动力学]`，@CHAR_FOODIE 满足眯眼 AU6+AU12 陶醉回味，食欲高潮顶点。

[15.0s-20.0s]：种草 CTA——@CHAR_FOODIE 满足回味 AU17，口播推荐食谱/店铺，@FOOD_HERO 与品牌定格，暖调食欲光，真实吃货种草收尾。

[FACS/AU 表演微动作]：4.0s 咬下为 @CHAR_FOODIE 的 AU26 下颌下降张口（咬合），强度 C 级（大口真实）；9.0s 满足转 AU6+AU12（眯眼陶醉微笑），强度 D 级（食欲高潮）；15.0s 回味 AU17 颏肌微收（满足回味），强度 B 级；视线 0.2s 先导在食物与镜头间切换（吃货对话感），AU45 自然眨眼，享受食物的真实满足表演。

[CineDance 运镜与光学]：手机竖屏微距 100mm 等效食物特写（焦点锁酱汁光泽）+ 面部 50mm 等效吃播近景，机位齐桌高度 0.9m 方位角 20° 四分之三侧，食物特写慢镜 + 吃播实时，断面高潮卡点缓推，竖屏 9:16 构图，快门等效 180°。

[光影角度量化]：主光暖调柔光箱右侧 40° 3800K 食欲塑形显油亮高光；辅光反光补光左侧 50° 光比 Key:Fill 2:1 通透食欲；轮廓光热气逆光后方 160° +1.2 档边缘光晕；环境 practical 暖调点缀；10 点钟柔和眼神光。

[色温显色]：主光 3800K CRI 95 暖调；辅光 4000K CRI 92；暖琥珀偏置；白平衡 3900K 食欲暖调；手机原生高饱和美食调色。

[微观质感证据链]：多汁酱汁光泽油滴；酥脆金黄外皮碎屑；融化芝士拉丝；新鲜食材纹理气孔；热气氤氲丝缕；真实食物表面拒绝塑料感。

[大气体积介质]：暖调食欲热气雾霭，温馨美食沉浸，油亮鲜艳氛围，零冷调零平淡，令人垂涎 ASMR 沉浸。

[同步声锁与台词原语言保留]：No subtitles.（字幕/食谱/店铺花字须后期硬压，绝不由模型生成）。ASMR 声场——真实咀嚼音/酥脆音/爆汁音/切菜音 + 轻柔 BGM + 满足口播，声画同步精准，20 秒沉浸；台词保留原语言口语化，口型同步精准锁定。

[资产单一源铁律]：@CHAR_FOODIE 从基准博主资产一次性生成开场/吃播/高潮/CTA 所有状态，**面部骨相 100% 一致（食物特写与吃播同一张脸）**；@FOOD_HERO 招牌料理在特写与吃播保持基准一致（同一份食物）；严禁链式修改导致面部/食物漂移。
[声音政策·默认无音乐] 不生成音乐 / no bgm —— 禁止任何 BGM/配乐/背景音乐；同期声（对白/环境音/动作音效/声音特效 Foley）须正常、准确、完整生成。
```

---

## 四、 黄金分镜画面完整拆解表（20 秒美食吃播 ASMR 版）

| 时间 | 景别 | 画面内容 | AU 微表情 | 光影/机位 | 音效/台词 |
|---|---|---|---|---|---|
| 0.0-4.0s | 微距特写 | 招牌料理热气升腾酱汁油亮开场 | [食物质地动力学] | 100mm 微距 / 暖调食欲光 | 热气滋滋 + 轻 BGM 铺垫 |
| 4.0-9.0s | 面部近景 | 大口咬下咀嚼满足吃播 | AU26 张口咬合 | 50mm 近景齐桌 / 暖调光 | 咀嚼酥脆 ASMR 音 |
| 9.0-15.0s | 微距特写 | 断面爆汁芝士拉丝食欲高潮 | AU6+AU12 陶醉 | 100mm 微距卡点缓推 / 热气逆光 | 爆汁音 + BGM 高潮 |
| 15.0-20.0s | 面部近景 | 满足回味口播种草 CTA 定格 | AU17 回味 | 50mm 近景 / 暖调食欲光 | 满足口播 + 店铺/食谱 |

---

## 五、 📚 全量专业参考库索引（References Routing Map）

| 参考文件 | 加载时机 | 核心作用 |
|---|---|---|
| `references/01-food-mukbang-asmr-dna.md` | 构思美学时 | 吃播 ASMR 基因、暖调食欲光、食物质感沉浸 |
| `references/02-viral-script-hooks.md` | 编写剧本时 | 四段式吃播、爆汁钩子、种草 CTA 模板 |
| `references/03-sound-design-asmr.md` | 设计音效时 | 咀嚼酥脆 ASMR、爆汁音、声画同步 |
| `references/cinedance-camera-optics.md` | 生成视频时 | 微距食物特写、面部吃播近景、竖屏 9:16 运镜 |
| `references/perf-acting-au-system.md` | 生成人物时 | 咬下 AU26/满足 AU6+AU12、食物质地动力学 |
| `references/whitebox-3d-rendering-guide.md` | 3D 白模锁定时 | 食物质感解算、热气拉丝动力学、暖调食欲光渲染 |
| `references/midjourney-v8-t2i-engine.md` | MJ v8 生图时 | V4.1 极致准确顶级光影角度/视角/质感工业量化层五子层 |
| `references/multiref-ensemble-acting.md` | 多参视频时 | 资产 @ 引用体系 / 11 段骨架 / 中文描述铁律 / 单一源公理 |
