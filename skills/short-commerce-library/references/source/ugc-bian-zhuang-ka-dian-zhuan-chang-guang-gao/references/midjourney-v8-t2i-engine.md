# Midjourney v8 电影级文生图大师提示词精进心法与引擎指南 (midjourney-v8-t2i-engine.md)

> 本手册为全流程 AI 影像的**殿堂级文生图母本资产中枢**。深度融合顶级商业摄影与历史电影质感密码，用于生成 `@CHAR` 核心人物定妆卡、`@PROD` 道具器物卡、`@SCN` 空间场景大画及 8K 展陈母版。
>
> **V4.1 增强层**：新增「极致准确顶级光影角度 / 视角 / 质感」工业级量化描述层（§三），所有文生图提示词**必须**携带该层，否则视为不合格打回。

---

## 一、 Midjourney v8 六大核心精进支柱（Mastery Pillars）

### 1. 社会学与阶层微距校准 (Sociological & Status Precision)
- **破除二元极端通病**：严防 AI 生成"平民即破衣烂衫乞丐、富贵即金碧辉煌帝王"的廉价网游感。
- **微距阶层限定词**：
  - *舒适雅致但非贵族*：`Comfortable and refined but clearly below aristocratic status`；
  - *得体服务人员*：`Clearly service staff, simpler than elite performers, professional hospitality posture`；
  - *自带清贵气场但非官员*：`Subtly authoritative quasi-aristocratic presence – not an official or true nobleman`；
  - *真实生产工具而非奇幻兵器*：`Feels dangerous as a real working tool, not a fantasy weapon`。

### 2. 微观物理使用痕迹证据链 (Physical Evidence Chain of Wear & Patina)
- **金属与兵器**：`hand forged irregularities`（手工锻打微观凹凸）、`dark cold gray iron`（冷铁深灰）、`fine sharpening marks`（细微开刃痕迹）、`small scratches`（细微划痕）、`light oxidation`（轻微氧化包浆）、`subtle working oil finish, no blood`（工具油润感且无血迹）。
- **木质与器皿**：`sturdy dark hardwood naturally polished from use`（经年使用自然摩擦形成的温润微光）、`restrained metal collar`（克制无装饰的金属箍圈）。
- **织物与面料**：`fine silk linen blend, dense weave, soft sheen, subtle woven patterns, understated brocade trim`（高密丝麻混纺、低调暗纹肌理、克制织锦镶边、真实下垂重力感）。

### 3. 电影动机光与暗部负补光 (Motivated Light & Deep Negative Fill)
- **定向穿透体积光**：`Thin directional daylight filters through lattice, gauze and leaves, creating layered light bands in humid interior air`。
- **暗部负补光（Negative Fill）**：`architecture in deep blue-green negative fill`（以深青墨色作为暗部负向补光，杜绝数码死黑或塑料反光）。
- **微观反光与漫射**：`Ink dark corners, pale luminous fabric, muted amber reflections on lacquer and bronze, delicate halation, soft bloom, atmospheric perspective`。
- **曝光控制**：`slight underexposure`（轻微欠曝，沉淀高反差影调与高光细节）。

### 4. 顶级电影机与柔光镜组光学配方 (Master Cine Optics & Filtration)
- **摄影机**：`ARRI ALEXA 35`（顶级电影数字摄影机色彩科学与宽容度）；
- **镜头**：`Cooke Panchro/i Classic 50mm T2.3` / `vintage Cooke Speed Panchro 75mm`（经典库克镜头柔和肤质与呼吸感）；
- **电影滤镜**：`Black Pro Mist 1/8`（黑柔 1/8 柔化数码锐利感）、`Glimmerglass 1`（微光柔焦镜 1 级，营造高光珠光扩散）；
- **胶片颗粒**：`subtle Kodak Vision3 500T film response, organic cinema grain`。

### 5. 时代形制与反庸俗防御防火墙 (Anachronism & Anti-Slop Firewall)
- **严防朝代与时代穿越**：`No Song/Ming/Qing clothing, no palace maid uniform`；
- **严防玄幻网游化**：`NO jianghu, NO peasant, NO modern waiter, NO xianxia fantasy, no fantasy sword, no oversized cleaver, no text`；
- **严防塑料与CG假人**：`No CG, no illustration, no cosplay, no plastic skin, no red gold luxury, no duplicated faces`。

### 6. 角色跨时空骨相与面容继承 (Character Bone Structure Lock)
- 显式声明：`same character identity as established... Preserve exact same face, bone structure, hairstyle, body proportions and lively intelligent eyes`，仅随着剧情演进改变服装剪裁、生活处境与岁月神态。

---

## 二、 文生图双版本即用黄金公式

### 🎨 ⭐ Midjourney v8 专属版本 (MJ v8)
$$\text{Prompt} = \text{[Subject \& Status Precision]} + \text{[Material \& Patina Evidence :: 3.0]} + \text{[Motivated Light \& Negative Fill :: 2.0]} + \text{[ARRI Alexa 35 \& Cooke Optics :: 1.5]} + \text{[MJ v8 Flags]}$$

```text
/imagine prompt: Masterpiece cinematic film still, shot on ARRI ALEXA 35, vintage Cooke Speed Panchro 75mm lens, T2.3, Glimmerglass 1, slight underexposure. A refined character standing in a historical interior, comfortable and refined but clearly below aristocratic status, holding a crafted hero prop with hand forged irregularities, fine sharpening marks, dark cold gray metal and working patina::3.0 Pale celadon and smoke blue textiles contrasting with dark warm timber, thin directional daylight filtering through lattice creating layered light bands in humid air, architecture in deep blue-green negative fill::2.0 Velvety cyan-black shadows, muted amber reflections, delicate halation, subtle Kodak Vision3 film response, organic grain, 8k resolution --ar 16:9 --style raw --v 8 --s 250 --c 3 --no plastic skin, flat studio flash, cheap fantasy armor, modern clothing, cg 3d render, blurry, distorted fingers
```

### 🌐 常规通用版本 (nano banana/GPT image2)
```text
【中文提示词】：
殿堂级电影质感关键帧，ARRI ALEXA 35 摄影机，复古库克 50mm 电影定焦镜头，T2.3 光圈，1/8 柔焦镜，轻微欠曝。画面呈现一位气质沉静内敛的人物，身着剪裁考究但形制简约的深青色暗纹丝麻长袍，质感垂坠真实。手中的器物呈现冷铁手工锻打肌理与微细划痕包浆，绝无浮夸奇幻装饰。细碎的定向日光穿过窗棂纱幔，在湿润空气中形成层层体积光带，暗部以深青墨色作为负向补光，阴影深邃温润，泛着琥珀色微光。眼神坚定聚焦，自然微表情，柯达 Vision3 胶片颗粒与呼吸感，8k 渲染画质。

【English Prompt】：
Museum-grade cinematic film still, ARRI ALEXA 35, vintage Cooke 50mm prime lens, T2.3, Black Pro Mist 1/8, slight underexposure. A dignified character in finely tailored dark teal silk-linen robe with subtle woven patterns, understated and refined. Holding a handcrafted tool showing cold forged iron texture and working patina. Directional sunlight slicing through window screens creating volumetric light bands in humid air, shadows in deep blue-green negative fill. Intensely focused gaze, authentic micro-expressions, rich organic Kodak film grain, 8k resolution.

【负向提示词 (Negative Prompt)】：
nsfw, cheap 3D digital CGI, plastic skin, flat flash lighting, fantasy glow, anachronistic modern clothes, distorted anatomy, blurry.
```

---

## 三、 ⭐ V4.1 极致准确顶级光影角度 / 视角 / 质感工业量化层（MANDATORY）

> **铁律**：自 V4.1 起，**所有**文生图提示词（MJ v8 专属版与常规通用版）**必须**在主体描述之后、风格 flag 之前，显式携带以下五个量化子层。缺任意一层即视为不合格，必须打回重写。

### 3.1 光源角度量化子层 (Light Angle Quantification)
必须写明每盏灯的**方位角（clock position 或 degree）+ 俯仰角（above/below eye-line）+ 距离主体米数 + 光质（soft/hard）+ 修饰器（modifier）**：

| 灯位 | 标准命名 | 角度范式 | 光质与修饰器 |
|---|---|---|---|
| 主光 Key | `Key Light` | `45° camera-left, 30° above eye-line, 1.8m from subject` | `120cm octa softbox + 1-layer diffusion, soft wrap` |
| 辅光 Fill | `Fill Light` | `30° camera-right, eye-level, 2.5m` | `4x4ft ultrabounce white, Key:Fill = 2:1` |
| 轮廓光 Rim/Hair | `Rim Light` | `150° behind subject, 45° above, 1.2m` | `grid-snoot 20°, hard edge, +1.5 stop over key` |
| 底光 Under | `Under Light` | `0° below chin, 0.6m` | `LED panel bounced off foamcore, subtle lift` |
| 背景光 BG | `Background Light` | `180° behind, wall wash` | `cyc strip, gradient fall-off 60% top → 20% bottom` |
| 眼神光 Catch | `Catchlight` | `co-located with key` | `single specular highlight at 10 o'clock in iris` |

**MJ v8 提示词写法范例**：
```
Key Light 45° camera-left 30° above eye-line 1.8m through 120cm octa softbox with single diffusion layer::2.5, Fill 30° camera-right eye-level 2.5m ultrabounce Key:Fill ratio 2:1::1.5, Rim Light 150° behind 45° above grid-snoot 20° hard edge +1.5 stop::2.0, single catchlight at 10 o'clock in iris
```

**常规通用版（中文）写法范例**：
```
【光影角度量化】：主光位于摄影机左侧 45°、高于视线 30°、距主体 1.8 米，经 120cm 八角柔光箱 + 单层柔光布扩散，形成柔和包裹光；辅光位于摄影机右侧 30°、与视线平齐、距主体 2.5 米，使用 4×4 英尺白色反光板，光比 Key:Fill = 2:1；轮廓光位于主体后方 150°、高于主体 45°、距 1.2 米，使用 20° 蜂巢束光筒，硬边，比主光过曝 +1.5 档；虹膜 10 点钟方向存在单一镜面眼神光。
```

### 3.2 色温与显色子层 (Color Temperature & CRI)
- 必须写明**色温 Kelvin 值**（如 `3200K tungsten` / `4300K golden hour` / `5600K daylight` / `6500K cool white` / `8000K open shade`）；
- 必须写明**显色指数 CRI**（`CRI 95+` / `TLCI 98`）与**光谱特性**（`full-spectrum continuous` / `green-magenta shift`）；
- 必须写明**白平衡偏移**（`+1/4 CTO on key` / `1/2 CTB on fill` / `magenta bias 3`）。

**范例**：`Key 5600K daylight CRI 98 full-spectrum, Fill 5600K +1/4 CTO warm bias, Rim 3200K tungsten practical motivated, white balance 5200K with magenta bias 3`

### 3.3 视角与机位量化子层 (Camera Angle & Position Quantification)
必须写明：
- **摄影机高度**：`camera height 1.55m (eye-level of 170cm subject)` / `low angle 0.4m from ground, 15° tilt-up` / `high angle 2.8m, 30° tilt-down` / `top-down 90° bird's eye`；
- **方位角**：`camera at 3/4 left of subject (30° azimuth)` / `dead-on frontal (0° azimuth)` / `profile (90° azimuth)`；
- **焦段与光圈**：`35mm anamorphic T2.0 (2.39:1 squeeze)` / `85mm spherical T1.4` / `100mm macro T2.8`；
- **快门开角**：`180° shutter (1/48s @ 24fps)` / `45° shutter for staccato motion blur` / `90° shutter crisp action`；
- **焦平面与景深**：`focus plane locked on near eye, f/2.0 shallow DOF, bokeh balls 12mm diameter at f/1.4 equivalent`；
- **透视畸变**：`minimal pincushion distortion` / `anamorphic horizontal blue flares` / `barrel distortion controlled < 1.5%`。

**范例**：`Camera height 1.55m eye-level, 3/4 left azimuth 30°, 40mm anamorphic T2.0, 180° shutter 1/48s, focus plane on near eye, shallow DOF, horizontal blue anamorphic flares, barrel distortion < 1.5%`

### 3.4 微观质感证据链子层 (Micro-Texture Evidence Chain)
必须为画面中**每一种材质**写出至少 3 条微观物理证据，杜绝"plastic / smooth / shiny"等廉价 AI 通病词：

| 材质类别 | 必备微观证据（≥3 条） |
|---|---|
| **皮肤** | `visible pores 40μm`, `vellus hair (peach fuzz) catching rim light`, `subsurface scattering SSS radius 2.5mm`, `fine expression lines at AU4 glabella`, `natural sebum sheen on T-zone, not oily` |
| **金属（阳极氧化铝）** | `bead-blasted 120-grit micro texture`, `Type III hard anodize 25μm`, `chamfer 0.3mm diamond-cut specular line`, `subtle fingerprint oils` |
| **金属（不锈钢/钛）** | `brushed #4 finish directional grain 0.4μm Ra`, `PVD titanium nitride champagne shift`, `micro-scratches from daily use` |
| **玻璃** | `0.5mm edge greenish tint`, `internal refraction caustics`, `anti-reflective multi-coat residual magenta`, `dust motes on surface` |
| **织物（丝麻）** | `slub irregularities every 8mm`, `warp/weft 60/40 count`, `natural fiber fuzz halo under rim`, `gravity drape folds 3-5cm radius` |
| **织物（针织/羊毛）** | `12-gauge knit loop topology`, `fiber halo 0.3mm`, `pilling at friction zones`, `natural lanolin sheen` |
| **皮革** | `full-grain pebble 1.2mm`, `patina darker at fold lines`, `waxed thread 0.8mm SPI`, `edge paint micro-cracks` |
| **木器** | `quarter-sawn cathedral grain`, `hand-rubbed tung oil 3 coats`, `dowell marks`, `humid-swell micro-cracks` |
| **陶瓷/釉** | `underglaze bubble cluster 50-80μm`, `ice-crackle crazing 0.2mm spacing`, `iron oxide foot rim`, `reduction-fired copper red` |
| **液体** | `surface tension meniscus 2mm`, `caustic light pooling on table`, `micro-bubbles 0.3mm rising`, `viscosity index 1.4 (water-like) or 3.2 (syrup)` |
| **汗珠/水珠** | `individual droplet 1.5-3mm diameter`, `gravitational elongation teardrop`, `condensation micro-cluster 0.2mm`, `specular highlight at 2 o'clock each` |
| **塑料（高级）** | `injection mold parting line`, `gate vestige`, `UV-stabilizer yellowing index 1.2`, `soft-touch rubberized overmold` |
| **胶片颗粒** | `Kodak Vision3 500T 5219 dye clouds`, `RMS granularity 42`, `halation bloom 1.5mm around specular` |
| **食物** | `Maillard browning gradient`, `steam wisps 0.4mm`, `oil sheen iridescence`, `crumb structure alveoli 1-3mm` |

**范例**：`Skin: visible pores 40μm, vellus hair catching rim, SSS radius 2.5mm, natural sebum T-zone sheen. Anodized aluminum chassis: bead-blasted 120-grit, Type III hard anodize 25μm, 0.3mm diamond-cut chamfer specular line, subtle fingerprint oils. Glass lens: 0.5mm greenish edge tint, internal caustics, AR multi-coat magenta residual.`

### 3.5 大气与体积介质子层 (Atmosphere & Volumetric Medium)
- **空气湿度**：`relative humidity 65%, visible volumetric haze`；
- **粒子**：`dust motes 0.05mm drifting at 0.2m/s in key beam` / `fog density 0.3 extinction` / `smoke layer at 1.2m height`；
- **体积光**：`god rays through 5cm slit, 12° cone, Tyndall scattering`；
- **大气透视**：`aerial perspective, background desaturated 15%, contrast reduced 20% at 8m distance`。

---

## 四、 V4.1 增强版双版本黄金公式（MANDATORY TEMPLATE）

### 🎨 ⭐ Midjourney v8 专属版本 (V4.1 增强)
$$\text{Prompt}_{V4.1} = \text{[Subject]} + \text{[§3.1 Light Angle :: 2.5]} + \text{[§3.2 Color Temp :: 1.5]} + \text{[§3.3 Camera Angle :: 2.0]} + \text{[§3.4 Micro-Texture :: 3.0]} + \text{[§3.5 Atmosphere :: 1.5]} + \text{[Optics]} + \text{[MJ v8 Flags]}$$

```text
/imagine prompt: Masterpiece cinematic commercial key visual. [SUBJECT PRECISION]. 
[LIGHT ANGLE] Key Light 45° camera-left 30° above eye-line 1.8m through 120cm octa softbox single diffusion::2.5, Fill 30° camera-right eye-level 2.5m ultrabounce Key:Fill 2:1::1.5, Rim 150° behind 45° above grid-snoot 20° hard +1.5 stop::2.0, catchlight 10 o'clock iris. 
[COLOR TEMP] Key 5600K CRI 98 full-spectrum, Fill +1/4 CTO, Rim 3200K tungsten practical, WB 5200K magenta bias 3::1.5. 
[CAMERA] Height 1.55m eye-level, 3/4 left azimuth 30°, 40mm anamorphic T2.0, 180° shutter 1/48s, focus near eye, horizontal blue flares::2.0. 
[MICRO-TEXTURE] Skin visible pores 40μm vellus hair SSS 2.5mm; anodized aluminum bead-blasted 120-grit Type III 25μm 0.3mm chamfer; glass 0.5mm green edge internal caustics AR magenta residual::3.0. 
[ATMOSPHERE] RH 65% volumetric haze, dust motes 0.05mm in key beam, aerial perspective bg -15% sat::1.5. 
ARRI ALEXA 35, Cooke Panchro/i 40mm, Black Pro Mist 1/8, Kodak Vision3 500T grain, 8k --ar 16:9 --style raw --v 8 --s 250 --c 3 --no plastic skin, flat flash, CG render, blurry, distorted fingers
```

### 🌐 常规通用版本 (V4.1 增强 · nano banana/GPT image2)
```text
【中文提示词】：
[主体与身份精度描述]。
【光影角度量化】：主光位于摄影机左侧 45°、高于视线 30°、距主体 1.8 米，经 120cm 八角柔光箱 + 单层柔光布扩散；辅光位于右侧 30°、与视线平齐、距 2.5 米，4×4 英尺白色反光板，光比 Key:Fill = 2:1；轮廓光位于主体后方 150°、高于 45°、距 1.2 米，20° 蜂巢束光筒硬边，过曝 +1.5 档；虹膜 10 点钟单一镜面眼神光。
【色温显色】：主光 5600K 日光 CRI 98 全光谱连续；辅光 +1/4 CTO 暖偏；轮廓光 3200K 钨丝实用动机光；白平衡 5200K 偏品红 3。
【视角机位】：摄影机高度 1.55 米与主体视线平齐，方位角 3/4 左侧 30°，40mm 变形宽银幕镜头 T2.0，180° 快门开角（24fps 下 1/48s），焦平面锁定近侧眼，水平蓝色变形光晕，桶形畸变 < 1.5%。
【微观质感证据链】：皮肤可见毛孔 40μm、绒毛在轮廓光下发光、次表面散射半径 2.5mm、T 区自然皮脂微光非油腻；阳极氧化铝机身 120 目喷砂微观肌理、III 型硬质阳极氧化 25μm、0.3mm 钻石切割倒角高光线、轻微指纹油渍；玻璃镜片 0.5mm 边缘淡绿色调、内部折射焦散、多层增透膜残留品红反光。
【大气体积介质】：相对湿度 65% 可见体积雾霭，主光束中 0.05mm 尘埃以 0.2m/s 漂浮，大气透视背景去饱和 15%、8 米外对比度降低 20%。
ARRI ALEXA 35 摄影机，库克 Panchro/i 40mm 镜头，1/8 黑柔滤镜，柯达 Vision3 500T 胶片颗粒，8k 渲染画质。

【English Prompt】：
[Subject & status precision]. Key Light 45° camera-left 30° above eye-line 1.8m via 120cm octa softbox single diffusion, Fill 30° camera-right eye-level 2.5m ultrabounce Key:Fill 2:1, Rim 150° behind 45° above grid-snoot 20° hard +1.5 stop, single catchlight 10 o'clock iris. Key 5600K CRI 98 full-spectrum, Fill +1/4 CTO, Rim 3200K tungsten practical, WB 5200K magenta bias 3. Camera height 1.55m eye-level, 3/4 left azimuth 30°, 40mm anamorphic T2.0, 180° shutter 1/48s, focus near eye, horizontal blue flares. Skin visible pores 40μm vellus hair SSS 2.5mm; anodized aluminum bead-blasted 120-grit Type III 25μm 0.3mm chamfer; glass 0.5mm green edge internal caustics AR magenta residual. RH 65% volumetric haze, dust motes 0.05mm in key beam, aerial perspective bg -15% sat. ARRI ALEXA 35, Cooke Panchro/i 40mm, Black Pro Mist 1/8, Kodak Vision3 500T grain, 8k.

【负向提示词 (Negative Prompt)】：
nsfw, plastic skin, flat studio flash, generic softbox look, CG 3d render, illustration, cheap CGI, fake smooth airbrushed face, no pores, waxy skin, dead black shadows, blown highlights, distorted fingers, extra limbs, blurry, low resolution, text, watermark, logo distortion.
```

---

## 五、 反 AI 通病防火墙（Anti-AI-Slop Firewall · V4.1 强化）

| AI 通病 | 病理 | V4.1 强制反制词 |
|---|---|---|
| 塑料假人脸 | 模型过度平滑皮肤 | `visible pores 40μm, vellus hair, SSS 2.5mm, natural sebum T-zone, NO airbrushed` |
| 廉价柔光箱感 | 主光无方向性 | `Key 45° camera-left 30° above, 120cm octa single diffusion, catchlight 10 o'clock` |
| 死黑暗部 | 无负补光 | `deep blue-green negative fill, shadow detail retained, +1/4 stop lift` |
| 高光过曝 | 无 halation 控制 | `highlight roll-off filmic, halation bloom 1.5mm, Kodak 2383 print emulation` |
| 畸变手指 | 模型解剖学失败 | `anatomically correct 5 fingers per hand, knuckle creases, nail cuticle detail` |
| 重复脸 | 多角色同质化 | `distinct facial bone structure per character, unique nose bridge, ear shape, asymmetry 3%` |
| 无质感金属 | 塑料感反光 | `bead-blasted 120-grit, Type III anodize 25μm, brushed #4 directional grain 0.4μm Ra` |
| 假水珠 | 贴图感 | `individual droplet 1.5-3mm, gravitational teardrop elongation, specular 2 o'clock each` |

---

## 七、 🃏 Model Card 角色资产卡版本（可选第三版本 · V4.1 增强）

> **功能定位**：当用户需要为 `@CHAR` 角色锁定**多角度一致性基准资产**时，文生图提示词可额外输出本版本（与 §四 双版本并列的第三可选版本）。产出物为一张**多视角角色资产卡拼图**，供后续 I2V / Multi-Ref I2V 阶段作为角色一致性锚点。

### 7.1 资产卡版面规范（10 格拼图布局 · MANDATORY LAYOUT · V4.2 修订）

| 区域 | 内容 | 规格 |
|---|---|---|
| **左侧数据栏** | `MODEL CARD` 标题 + 7 项角色档案：身高 HEIGHT / 体重 WEIGHT / 身材比例 BODY RATIO（头身）/ 生日 BIRTHDAY / 国籍 NATIONALITY / 风格 STYLE / 特长 SPECIALTY | 纯白底 + 黑字，中英双语标签，数据逐项换行 |
| **第 2 列（通栏竖图）** | **正面全身立姿·不带头**（headless front full body）：自下颌/领口以下裁切构图，专注展示全套着装、身材比例与鞋履 | 头部不入画，领口到鞋底完整入画，占栏高 100% |
| **第 3 列（通栏竖图）** | **背面全身立姿·带头**（full back view with head）：后脑发型 + 背面服装剪裁/背部细节/鞋跟完整展示 | 头顶到鞋底完整入画，占栏高 100% |
| **第 4-6 列上排** | 头部三视角：正面胸像 / 左侧 90° 侧面 / 正背面（后脑） | 造型 A（默认发型），肩部以上构图 |
| **第 4-6 列下排** | 头部三视角：正面胸像 / 左侧 90° 侧面 / 正背面（后脑） | 造型 B（第二发型/束发/盘发等变体），肩部以上构图 |
| **底部横排（2 格）** | **着装道具特写**（wardrobe & props close-up）：格 1 服装面料/缝线/五金微距；格 2 核心道具（@PROP）微距 | 100mm macro T2.8 焦点堆栈，微观质感证据链全开 |

### 7.2 资产卡专用光学规范（无影平光 · 保资产精度）
- **光源角度**：`Key Light 0° frontal 180cm octa softbox double diffusion eye-level 2.0m shadowless wrap` + `Fill co-axial ultrabounce Key:Fill ratio 1:1 zero shadow` + `BG Light 180° behind pure white cyc wall wash even 100%`；**资产卡版本严禁方向性硬阴影**，确保面部骨相/发型/服装细节在所有视角精准可读；
- **色温显色**：`Key 5600K CRI 99 full-spectrum neutral, Fill 5600K CRI 99, WB 5600K zero bias`（零偏置，保肤色与服装色准）；
- **视角机位**：正面全身不带头栏与背面全身带头栏 `camera height 1.2m dead-on frontal/back 0°/180° azimuth, 50mm spherical T4.0 deep DOF full body in frame`；头部六格 `camera height 1.6m, azimuth 0°/90°/180°, 85mm spherical T4.0, focus plane on face center`；着装道具特写两格 `100mm macro T2.8 focus stack to T8 equivalent, focus plane on fabric weave / prop surface`；
- **微观质感**：同 §3.4 证据链（皮肤毛孔 40μm / 绒毛 / SSS 2.5mm / 织物经纬 / 发丝根根分明），**资产卡版本质感证据只增不减**；
- **大气介质**：`zero dust, zero volumetric haze, pure white infinite void background`（零尘埃零雾霭纯白无限背景，杜绝介质污染资产卡）。

### 7.3 🎨 ⭐ Midjourney v8 专属版本模板 (Model Card · V4.1 增强)
```text
/imagine prompt: professional model card character asset sheet, 10-panel grid layout on pure white background. Left column data bar with black text: MODEL CARD, HEIGHT [身高], WEIGHT [体重], BODY RATIO [头身], BIRTHDAY [生日], NATIONALITY [国籍], STYLE [风格关键词], SPECIALTY [特长]. Column 2 headless front full-body standing pose cropped below chin natural posture hands in pockets complete neckline-to-shoe framing showcasing full wardrobe and silhouette. Column 3 full back view standing pose with head complete head-to-toe framing showcasing back hairstyle and back garment tailoring. Columns 4-6 top row head three-view: frontal bust / left 90° profile / back of head, hairstyle A. Columns 4-6 bottom row head three-view: frontal bust / left 90° profile / back of head, hairstyle B variant. Bottom row 2 panels wardrobe and props close-up: panel 1 fabric weave stitching hardware macro, panel 2 hero prop macro::3.0 
[LIGHT ANGLE] Key Light 0° frontal 180cm octa softbox double diffusion eye-level 2.0m shadowless wrap, Fill co-axial ultrabounce Key:Fill ratio 1:1 zero shadow, BG 180° pure white cyc wall wash even 100%, catchlight 12 o'clock in iris::2.5. 
[COLOR TEMP] Key 5600K CRI 99 full-spectrum neutral, Fill 5600K CRI 99, WB 5600K zero bias true skin tone and fabric color accuracy::1.5. 
[CAMERA] body columns height 1.2m dead-on azimuth 0°/180° 50mm spherical T4.0 deep DOF; head panels height 1.6m azimuth 0°/90°/180° 85mm spherical T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion::2.0. 
[MICRO-TEXTURE] skin visible pores 40μm vellus hair SSS 2.5mm natural sebum T-zone; hair individual strands distinct root-to-tip; garment fabric warp/weft count visible stitching 4mm spacing gravity drape metal hardware micro scratches oxidation patina; hero prop surface patina evidence chain full open::3.0. 
[ATMOSPHERE] zero dust zero volumetric haze pure white infinite void background, no shadow on floor::1.5. 
ARRI ALEXA 35, Cooke Panchro/i 50mm T4.0 + 100mm macro T2.8, no filtration, Kodak Vision3 50D fine grain, 8k --ar 16:9 --style raw --v 8 --s 100 --c 0 --no directional shadow, no dramatic lighting, no colored gel, no background props, plastic skin, CG render, blurry, distorted fingers, inconsistent face between panels, head visible in headless column
```

### 7.4 🌐 常规通用版本模板 (Model Card · V4.1 增强 · nano banana/GPT image2)
```text
【中文提示词】：
专业角色资产卡（Model Card），纯白背景 10 格拼图布局。左侧数据栏黑字：MODEL CARD、身高 [XXcm]、体重 [XXkg]、身材比例 [X.X 头身]、生日 [YYYY.MM.DD]、国籍 [XX]、风格 [XX/XX/XX]、特长 [XX/XX/XX]。第 2 列**正面全身立姿不带头**：自下颌/领口以下裁切构图，自然站姿双手插兜，领口到鞋底完整入画，专注展示全套着装与身材比例。第 3 列**背面全身立姿带头**：头顶到鞋底完整入画，展示后脑发型与背面服装剪裁。第 4-6 列上排头部三视角：正面胸像 / 左侧 90° 侧面 / 正背面后脑，造型 A。第 4-6 列下排头部三视角：正面胸像 / 左侧 90° 侧面 / 正背面后脑，造型 B 变体。底部横排 2 格**着装道具特写**：格 1 服装面料/缝线/五金微距；格 2 核心道具微距。[角色身份与服装描述]。
【光影角度量化】：主光位于正前方 0° 180cm 八角柔光箱双层扩散与视线平齐距 2.0 米无影包裹；辅光同轴超反射白板光比 Key:Fill = 1:1 零阴影；背景光 180° 纯白环形墙均匀洗墙 100%；虹膜 12 点钟单一镜面眼神光。资产卡版本严禁方向性硬阴影。
【色温显色】：主光 5600K CRI 99 全光谱中性；辅光 5600K CRI 99；白平衡 5600K 零偏置，保肤色与服装色准。
【视角机位】：全身两栏摄影机高度 1.2 米正/背方位角 0°/180°，50mm 球面镜头 T4.0 深景深全身入画；头部六格摄影机高度 1.6 米，方位角 0°/90°/180°，85mm 球面镜头 T4.0 焦平面锁定面部中心；特写两格 100mm 微距 T2.8 焦点堆栈，零畸变。
【微观质感证据链】：皮肤可见毛孔 40μm、绒毛、次表面散射半径 2.5mm、T 区自然皮脂微光；发丝根根分明从发根到发梢；服装面料经纬支数可见、缝线 4mm 间距、重力垂坠、五金微观划痕氧化包浆；核心道具表面包浆证据链全开。
【大气体积介质】：零尘埃、零体积雾霭、纯白无限虚空背景，地面无阴影。
ARRI ALEXA 35 摄影机，库克 Panchro/i 50mm T4.0 + 100mm 微距 T2.8 镜头，无滤镜，柯达 Vision3 50D 细颗粒，8k 渲染画质。

【English Prompt】：
professional model card character asset sheet, pure white background 10-panel grid. Left data bar black text: MODEL CARD, HEIGHT, WEIGHT, BODY RATIO, BIRTHDAY, NATIONALITY, STYLE, SPECIALTY. Column 2 headless front full-body standing pose cropped below chin hands in pockets neckline-to-shoe framing showcasing full wardrobe. Column 3 full back view standing pose with head head-to-toe framing showcasing back hairstyle and tailoring. Columns 4-6 top row head three-view frontal bust / left 90° profile / back of head hairstyle A. Columns 4-6 bottom row same three-view hairstyle B variant. Bottom row 2 panels wardrobe and props close-up: fabric stitching hardware macro, hero prop macro. [Character identity and wardrobe]. Key Light 0° frontal 180cm octa double diffusion eye-level 2.0m shadowless wrap, Fill co-axial Key:Fill 1:1 zero shadow, BG 180° white cyc wash 100%, catchlight 12 o'clock. Key 5600K CRI 99 neutral, WB 5600K zero bias. Body columns height 1.2m azimuth 0°/180° 50mm T4.0 deep DOF; head panels 1.6m azimuth 0°/90°/180° 85mm T4.0 focus face center; close-up panels 100mm macro T2.8 focus stack zero distortion. Skin pores 40μm vellus hair SSS 2.5mm; hair strands distinct; fabric warp/weft stitching 4mm gravity drape hardware micro scratches patina; hero prop patina evidence chain. Zero dust zero haze pure white infinite void, no floor shadow. ARRI ALEXA 35, Cooke Panchro/i 50mm T4.0 + 100mm macro T2.8, no filtration, Kodak Vision3 50D grain, 8k.

【负向提示词 (Negative Prompt)】：
nsfw, directional shadow, dramatic lighting, colored gel light, background props, floor shadow, plastic skin, CG render, illustration, blurry, distorted fingers, inconsistent face between panels, mismatched hairstyle within same row, head visible in headless column, missing back view column, text typo, watermark.
```

### 7.5 使用纪律
- **可选性**：本版本为**第三可选版本**，用户显式要求"角色资产卡 / Model Card / 多视角定妆卡"时输出；默认仍输出 §四 双版本；
- **锚点用途**：资产卡产出后必须登记为 `@CHAR` 基准资产，后续所有分镜关键帧与 I2V 提示词以 `@CHAR` 显式引用，面部骨相/发型/身材比例严禁漂移；
- **数据栏铁律**：7 项档案数据一经锁定即为单一源，禁止链式修改；中英双语标签格式固定；
- **一致性铁律**：10 格内同一角色面部骨相/身材比例 100% 一致，造型 A/B 仅发型/束发变化，服装除数据栏声明外不得变化；正面全身栏**严禁头部入画**，背面全身栏**严禁缺头**。

---

## 六、 加载时机与引用纪律
- **加载时机**：生成任何 `@CHAR` / `@PROP` / `@SCN` / `@MAT` 基准资产卡之前**必读**；
- **引用纪律**：所有下游分镜关键帧提示词必须**显式复用**本文件 §三 五子层，禁止凭空省略；
- **验收标准**：交付前用 §五 反 AI 通病防火墙逐条自检，任意一条不合格即打回重写。
