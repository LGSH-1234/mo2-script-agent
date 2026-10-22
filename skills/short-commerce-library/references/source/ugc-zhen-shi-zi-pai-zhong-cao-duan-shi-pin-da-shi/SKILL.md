---
name: "ugc-zhen-shi-zi-pai-zhong-cao-duan-shi-pin-da-shi"
description: "告别AI塑料假面：模拟手机前置微晃与真实微瑕皮质，打造小红书与抖音爆款UGC自拍种草。"
version: "4.0"
display_name: "真实自拍种草短视频大师"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
---

> ### 🚨 【系统默认铁律 · 视频提示词 AU 角色微表情强制注入准则】
> 1. **默认强制性**：在图生视频（I2V）与多参视频生成阶段，提示词**必须默认带有角色 FACS/AU 精准微动作描述词**（包括 AU 编号如 `AU1/AU2/AU4/AU12/AU17/AU23/AU45`、解剖学肌肉位移、`A~E` 级量化强度、`0.2s 视线先导` 与 `AU45 眨眼抑制`）。
> 2. **豁免条件**：**除非用户在交互中明确声明“不需要表情”或“无微表情”**，否则默认所有涉及有人格属性的角色/生物镜头均**无条件全量携带**，作为系统级底线规则。
> 3. **特异性智能转译**：若画面为纯风景、纯静物、纯微观粒子或纯建筑无人类主体，AU 规则自动转译为“镜头呼吸动态与环境物理微扰动”，并显式声明 `[本镜无角色主体，AU 自动转为环境动力学]`。
> ### 🚨 【系统默认铁律 · 资产 @ 引用与单一源禁止链式修改公理】
> 1. **固定 @ 资产引用一致性锁**：角色（`@CHAR`）、场景（`@SCN`）、道具（`@PROP`）必须在项目初期完成基准资产锁定，并在后续所有生图与生视频提示词中强制以 `@形式` 显式引用，严禁凭空重新描述导致资产漂移。
> 2. **绝对禁止链式修改 (Ban Chained Modification — 资产漂移之源)**：
>    - ❌ **严禁链式修改**：`基准资产 → (修改) → 受伤态 → (再修改) → 重伤态 → (再修改) → 战损态`（每多一次 pass 就多毁一次纹理、多漂一次颜色，三次修改脸必变对称塑料死气）。
>    - ✅ **单一源点修改铁律 (Single-Source Axiom)**：所有状态必须**无条件以最初锁定的基准资产为唯一底图**一次性修改生成：
>      - `基准资产 ──点修改──> @CHAR_角色_受伤`
>      - `基准资产 ──点修改──> @CHAR_角色_重伤`
>      - `基准资产 ──点修改──> @CHAR_角色_战损 (受伤+换装+湿 一次性从基准改出)`
>    - 场景与道具同理：`@SCN_基准 ──点修改──> @SCN_夜景/雨景`，`@PROP_基准 ──点修改──> @PROP_损坏态`。

# 真实感自拍感种草视频创作大师系统 V4.0

> **定位**：拒绝“广告味”的顶级 UGC 种草引擎。用真实手机自拍视听语言与人类微表情心理学，打造让消费者毫不设防的爆款转化视频。

---

## 一、 真实感自拍的核心视觉三法则

1. **去棚拍化生活光学 (Anti-Studio Natural Lighting)**：
   - 绝不用昂贵三点商业布光；采用卧室窗边自然侧光、化妆镜环形灯倒影或咖啡馆散射日光；
   - 镜头允许轻微过曝或微弱噪点，模拟 iPhone 前置镜头真实色调与自然景深。
2. **真实微瑕生理皮肤 (Authentic Imperfect Skin)**：
   - 保留自然的皮肤毛孔纹理、细微眼袋与鼻翼红血丝，严禁磨皮塑料感与假面；
   - 面部具有真实表情牵拉褶皱，笑时眼角有笑纹，惊讶时眉心有自然的动态位移。
3. **真实口播节奏与眼神停顿**：
   - 真人说话必定有轻微的思考停顿（AU43 视线瞬时下移 0.1s）、自然眨眼（AU45 正常频率每分钟 15-20 次）；
   - 遇到惊喜时瞳孔微微放大，身体轻微前倾靠近屏幕，制造与观众的“亲密距离感”。

---

## 二、 文生图双版本核心提示词标准

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8)
```text
/imagine prompt: Authentic smartphone front camera selfie shot, casual UGC vlog aesthetic. A genuine charismatic 24-year-old female lifestyle influencer in a cozy sunlit bedroom, holding a sleek minimalist skincare serum bottle next to her glowing cheek::3.0 Natural bare-skin texture with visible micro-pores, soft blush, authentic enthusiastic smile (AU12_C + AU6_C), sincere bright eyes looking right into camera lens::2.5 Handheld slight angle, messy casual hair bun, soft morning window light, subtle real-world lens distortion of iPhone 15 Pro front camera, 8k --ar 9:16 --style raw --v 8 --s 200 --c 3 --no studio lighting, heavy makeup, plastic smooth doll skin, commercial billboard look, professional studio backdrop, blurry
```

### 🌐 常规通用版本 (nano banana/GPT image2)
```text
【中文提示词】：
真实生活化智能手机前置自拍画面，竖屏 9:16 构图，23mm 广角镜头，UGC 种草生活 Vlog 质感。一位 24 岁面容亲切自然的女性美妆博主，身穿宽松灰色棉质家居服，坐在采光充足的温馨卧室中。博主一手拿着手机自拍，另一只手拿着一瓶极简半透明精华液贴近自己透亮的脸颊。素颜质感皮肤，微观毛孔与自然光泽清晰可见，眼轮匝肌收缩带着真诚灿烂的微笑（AU12_C + AU6_C），眼神真诚地直视手机镜头。窗外柔和的晨光漫射，画面带有轻微的手机前置镜头边缘透视，真实生活质感，8k。

【English Prompt】：
Authentic smartphone front camera selfie video still, vertical 9:16 aspect ratio, 23mm wide angle, casual UGC social media aesthetic. A natural charismatic 24-year-old female content creator sitting in a cozy sunlit bedroom. She is taking a handheld selfie while holding a transparent skincare serum bottle next to her glowing cheek. Bare skin texture with visible pores and natural dewiness, genuine warm smile with crinkled eye corners, looking directly into camera lens. Soft morning window light, subtle iPhone front camera lens characteristics, 8k resolution.

【负向提示词 (Negative Prompt)】：
nsfw, artificial studio lighting, plastic porcelain skin, airbrushed, commercial TVC billboard, stiff pose, creepy dead eyes, distorted hands, blurry.
```

---

## 三、 多图参考图生视频核心提示词标准 (Multi-Ref I2V Engine)

```text
【多参考素材锁定层】：
- @CHAR_UGC : references/assets/real_ugc_girl.png (素颜带有自然雀斑与真实皮肤毛孔的年轻女性博主)
- @PROD_UNBOX : references/assets/unboxed_skincare_tube.png (刚撕开密封锡纸膜的高性价比护肤软管)
- @SCN_BEDROOM : references/assets/sunlit_messy_bedroom.png (自然生活化真实卧室与窗台晨光)

【提示词正文 (11-Step Multi-Ref I2V Prompt)】：
(Multi-Reference Video Generation): An authentic 5-second iPhone selfie UGC testimonial shot.
[0.0s-1.8s]: Handheld iPhone front camera (23mm wide) with natural micro-shakes. @CHAR_UGC leans into the lens, pointing to a small acne breakout on her left cheek, talking candidly to the camera.
[1.8s-3.5s]: She unscrews the cap of @PROD_UNBOX, squeezes a pea-sized dot of soothing gel onto her clean fingertip, and gently dabs it directly onto the blemish.
[3.5s-5.0s]: The cooling gel melts clear on her skin; she looks directly into the camera lens with sincere relieved eyes, breaking into a warm spontaneous smile.
[FACS/AU 表演微动作]: AU4 (眉心微蹙展示皮肤困扰) → AU12_C+AU6_B (涂上后眉舒目展由衷真诚微笑) + 自然说话带动嘴唇真实起伏 + 真实生活眨眼 (AU45 每秒 1 次)。
[CineDance 运镜与光学]: 模拟 iPhone 15 Pro 前置摄像头 23mm 广角手持微晃与自动对焦拉风箱微呼吸感，自然未调色日光。
[台词与声音 Foley ASMR]: “家人们谁懂啊！昨天熬夜爆的大红痘，抹上真的立刻退红！” + 软管挤压噗的一声清脆音 + 真实卧室无修音环境人声。
[全局负向禁止项]: No studio ring light reflections, no airbrushed smooth plastic beauty filter, no mechanical robotic speech.
```


## 四、 15秒/30秒黄金分镜画面完整拆解表 (Storyboard Breakdown)

| 镜号 | 景别 | 运镜方式 | 时长 | 画面视觉内容 | 角色生活化微表情 / 互动 | 声音与同期音效 (Foley) |
|:---:|:---:|:---:|:---:|:---|:---|:---|
| **SH01** | 特写 (CU) | 手持前置怼脸 | 3.0s | 女孩穿着睡衣手持手机怼脸自拍，大光下清晰展现鼻翼两侧泛红与下巴熬夜痘，表情懊恼崩溃 | `AU4_C` 紧锁双眉，手指委屈戳戳痘痘 | “姐妹们听我句劝！千万别熬夜追剧，看我这大红痘！”口语叹气声 |
| **SH02** | 特写 (CU) | 手机摄像头移焦 | 2.5s | 手机镜头快速下压对准洗手台，博主单手利落拧开一支小绿管软管盖子，挤出一颗晶莹剔透的修护凝胶 | 单手单指操作，极具生活化随意感 | 塑料盖拧开的干脆咔嚓摩擦声 + 挤出凝胶细微空气噗声 |
| **SH03** | 大特写 (ECU) | 贴脸微距点涂 | 3.5s | 指腹将冰凉晶莹的凝胶点在红肿痘痘处，轻轻打圈推开，凝胶接触体温瞬间化为清爽水膜被毛孔吸收 | `AU43` 微闭单眼感受冰凉肤感，紧绷眉头瞬间舒展 | “抹上完全不粘腻，冰冰凉凉像给皮肤喝冰美式！”真实生活语气 |
| **SH04** | 特写 (CU) | 左右分屏对比 | 3.5s | 画面一分为二：左边是 3 天前红肿大脓包素颜，右边是使用 3 天后痘印彻底消退、平整白皙的健康脸颊 | 左右对比强烈，右边博主兴奋转头展示侧脸 | 快速转场刷的一声滑音 (Whoosh) + 惊喜笑声：“你们看！连印子都没留！” |
| **SH05** | 近景 (MCU) | 手持后退比心 | 2.5s | 博主开心地把产品贴在脸旁，对着镜头眨眼灿烂大笑，屏幕下方跳出小黄车链接与“限时买一赠一”气泡 | `AU12_D` 充满感染力的大笑，整张脸散发自然光泽 | “几十块钱管够三个月，赶紧去小黄车抢！”弹窗清脆叮咚声收尾 |


## 五、 📚 全量专业参考库索引（References Routing Map）

| 模块类别 | 核心参考文件 | 关键职责与标准 | 加载时机 |
|---|---|---|---|
| **视觉与镜头** | `references/01-ugc-selfie-aesthetic-dna.md` | 手机自拍镜头畸变、手持抖动与生活光影 | 画面风格设定必读 |
| **文案与转化** | `references/02-high-conversion-seeding-script.md` | 黄金 3 秒钩子、痛点场景化与心智种草 | 剧本台词设计必读 |
| **声音与ASMR** | `references/03-sound-design-natural-asmr.md` | 真实撕膜音、膏体按压脆响与无BGM沉浸拟音 | 声音设计时必读 |
| **⭐ 大师微表情** | `references/perf-acting-au-system.md` | 口播真诚微表情 AU12/AU6、0.2s 视线先导与眨眼控制 | 模特微动作必读 |
| **⭐ 双版本生图** | `references/midjourney-v8-t2i-engine.md` | 【🎨 MJ v8 专属版】与【🌐 常规通用版 (nano banana/GPT image2)】 | 生成关键帧时必读 |
| **⭐ 摄影光学** | `references/cinedance-camera-optics.md` | 手机广角 23-28mm、真实手持晃动与前置景深跟随 | 运镜提示词必读 |
| **⭐ 3D 白模轨迹** | `references/whitebox-3d-rendering-guide.md` | 开箱手势动作与拿取产品 3D 轨迹空间锁定 | 动作渲染前必读 |
| **⭐ 四层解耦多参** | `references/multiref-ensemble-acting.md` | 博主(@CHAR)、好物产品(@PROD)、生活空间(@SCN)四层解耦 | 多参视频生成必读 |
