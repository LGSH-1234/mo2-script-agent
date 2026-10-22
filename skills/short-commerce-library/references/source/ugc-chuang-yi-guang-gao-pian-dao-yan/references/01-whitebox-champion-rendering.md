# ⭐ 01-白模参考视频冠军级渲染系统 (White-Box Champion Rendering System)

> **归属模块**：即梦 Seedance 2.5 3D 控制与视觉渲染引擎（模型无关通用系统；默认 Seedance 2.5，用户指定其他模型时按 [references/12](12-model-agnostic-system.md) 适配）
> **归属引擎**：视觉美学引擎 (E2) + 资产设计引擎 (E4) + 剪辑工程引擎 (E6)
> **顶级标准**：SIGGRAPH / Unreal Engine Challenge 国际顶级渲染大赛冠军水平  
> **核心定位**：将 Maya / Blender / C4D / UE5 的三维白模/灰模/黏土动画/预演 (Animatic) 视频，通过 AI 物理材质替换与电影光影重构，无损升级为 8K 光线追踪级实拍电影大片。
> **关联引擎**：六引擎 x 四机制 x 审美大师团体系见 [references/10](10-capability-engines.md)

---

## 一、 3D 白模控制的核心突破与物理公理

在传统文生视频或图生视频中，复杂的镜向调度（推拉摇移升降）、三维几何遮挡与角色走位往往依赖提示词的“文字盲猜”，极易产生空间塌陷、动作变形与镜头乱漂。

即梦 Seedance 2.5 深度集成了专业 3D 软件（Maya / Blender 等）插件及运动矢量算法，实现了 **“像素级 3D 空间轨迹与几何控制”**：

1. **三维运镜轨迹 100% 还原**：精准理解白模视频中的虚拟摄像机轨迹（FOV 变焦、推镜头、拉镜头、环绕升降、甩镜），还原真实的物理电影镜头语言。
2. **空间遮挡与物理几何锁定**：解析白模场景中物体的前后景深度、接触面与遮挡关系，确保生成的画面完全符合真实物理空间架构。
3. **角色走位与姿态动线追踪**：敏锐捕捉白模中虚拟角色/物体的站位、动作路线、碰撞关系与姿态时序。

---

## 二、 冠军级白模渲染六大核心要素 (Champion Hexad Formula)

为了达到国际顶级渲染大赛冠军水平，提示词编写必须同时包含以下六大要素：

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. 轨迹与动线继承 (Motion & Camera Inheritance): 指定@视频1 为运镜/走位/几何遮挡的唯一物理锚点              │
│ 2. PBR 微观物理材质替换 (PBR Material Mapping): 将灰模表面替换为 8K PBR 材质(毛孔/锈迹/磨损/织物纹理)   │
│ 3. HDR 电影级光影与介质 (HDR Lighting & Volumetrics): Chiaroscuro 强反差光影、体积雾/丁达尔光束、水汽尘埃  │
│ 4. 物理流体与动力学解算 (Physics & Dynamics): 真实重力感、脚下踩踏灰尘/水花、布料运动延迟与惯性反应       │
│ 5. 极性细节与去 3D 感 (Anti-3D/CGI Control): 彻底抹除 CG 游戏感，注入胶片颗粒、瞳孔高光、表皮微瑕瑕疵     │
│ 6. 1:1 结构收束与无缝防崩 (Structural Integrity): 保证全程无画质坍塌、无脸部漂移、无动作突变              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 二·五、 ⛔ 单段完整生成铁律 (Single Continuous Generation Mandate — 最高优先级)

**白模参考视频（@视频1）的成片必须是"一个完整、连续、不切割的视频"——单次生成、整段输出。此条为白模渲染的不可违反约束，优先级高于一切分镜/切片流程。**

- **❌ 禁止**：把 @视频1 按时间/分镜切成多个片段，分别加提示词渲染。
- **❌ 禁止**：将白模视频拆成几段、各配不同提示词分头生成，再拼接。
- **✅ 正确**：@视频1 整体作为单一参考视频上传，写一条完整渲染提示词，一次性生成整段成片。
- **时间标注的用法**：提示词内可对时间轴（如 0–7s / 7–14s）做**材质与光影的描述性标注**（如"0-7s 冷蓝色调，7s 后转暖光"），这仅用于引导渲染细节，**绝不是切分生成指令**。
- **为什么不可切割**：
  1. 运镜轨迹是连续的三维空间曲线，切割后各片段机位无法无缝衔接，拼接处必然跳轴/顿挫；
  2. 前后景遮挡与角色走位跨片段连续性依赖完整几何上下文，切割即断裂；
  3. 动作因果链（如"起身→助跑→跃起→落地"）必须整体可见，否则渲染出错误的中间态。
- **例外**：仅当用户明确要求"拆分为 N 段独立渲染"时允许，且每段需单独走确认门并在该段内自成完整动作弧。

---

## 三、 白模类型与提示词适配策略

在实际制作中，白模视频分为**粗颗粒度白模**与**细颗粒度白模**两类：

### 1. 粗颗粒度白模 (Rough Low-Poly / Blockout)
- **特点**：由简单几何体（立方体、球体、圆柱体）拼搭而成的运动预演，无复杂肌肉与面部细节。
- **控制核心**：将白模作为**运动骨架与几何构图**。提示词中需要明确几何体与实体角色/道具的映射关系。
- **避坑硬轨**：若几何体带有细微肢体或线稿，提示词中必须写出肢体的完整动作；若希望 AI 自动解算自然肢体，**建议上传不带细微肢体的纯几何块**。

### 2. 细颗粒度白模 (High-Poly Mesh / 3D Animatic)
- **特点**：在 Blender/Maya 中已完成精细建模与角色动画，仅缺少高阶材质、光影与实拍质感。
- **控制核心**：直接进行 **PBR 物理渲染与电影光影烘焙**。
- **避坑硬轨**：上传前**必须擦除 3D 软件中的网格线、坐标轴、Camera Cone 标记**，防止 AI 误将辅助线渲染为画面元素。

---

## 四、 大师级白模渲染标准模板 (Master Templates)

### 模板 1：影视级 CG 灰模转实拍电影 (3D Blockout to Photorealistic Live-Action)

#### 中文渲染指令
```text
对@视频1 的 3D 白模动画进行 8K IMAX 电影级物理渲染。

【素材与角色锁定】
- 角色外观：参考@图片1（面部五官、发型、皮肤纹理、黑色粗羊毛夹克严格还原，无脸部漂移）。
- 场景环境：参考@图片2（废弃观星台内部，圆形石砌穹顶，中央黄铜望远镜，地面碎玻璃，月光斜射）。
- 道具材质：参考@图片3（发光的橄榄石晶石，表面微裂纹，金属氧化质感）。

【三维空间与机位继承】
- 100% 继承@视频1 中的 3D 摄像机运镜轨迹（低机位缓慢后退跟拍）、焦段视角（84°广角）与镜头速度。
- 严格遵循@视频1 中的三维空间几何关系、人物走位动线与前后景遮挡逻辑。

【冠军级 PBR 材质与 HDR 光影渲染】
- 材质细节：采用 8K PBR 物理渲染，呈现极度真实的表面肌理（皮孔微瑕、汗水高光、织物磨损缝线、黄铜锈斑）。
- 光影与介质：HDR 电影级采光，主光为右上角 45 度打入的冷蓝色月光，呈现清晰的体积光/丁达尔光束，空气中飘浮微妙的尘埃颗粒，面部保持 70% 的 Chiaroscuro 深沉阴影。
- 物理动力学：遵从真实重力与惯性，角色抬臂时袖口有微小延迟，手持晶石呈现真实的物理重量感与接触阴影。

【音效与收束控制】
- 仅保留环境音与动作同期声（风吹穿孔声、碎石踩踏声、低沉呼吸声），禁止自动添加 BGM 或字幕。
- 画面无抖动、无失真、无 CG 游戏感，呈现绝对真实的物理胶片质感。
```

#### 英文 Seedance 2.5 运行版
```text
Render the 3D blockout animation in @video1 into an 8K IMAX photorealistic cine shot.

SCENE CONTEXT & ACTIVE REFERENCES
- Character: Reference @image1 for facial features, dark grey coarse wool jacket, skin texture, micro-scars.
- Location: Reference @image2 for circular stone dome observatory, central rusted brass telescope, shattered floor glass.
- Prop: Reference @image3 for glowing olivine micro-crystal with PBR surface micro-cracks.

CAMERA & GEOMETRY INHERITANCE
- 100% inherit the 3D camera trajectory, focal length (Cuarón 84° wide angle), camera speed, and spatial movement from @video1.
- Retain exact spatial layout, character walking path, and foreground/background occlusion from @video1.

PBR MATERIALS & CINEMATIC LIGHTING
- 8K PBR physical render: skin pore-level realism, sweat sheen, garment weave, oxidation patina on metal.
- HDR cinematic lighting: single cool-blue moonlight beam from top-right arch with volumetric Tyndall effect, airborne dust motes, 70% chiaroscuro shadow on character's shadow side.
- Physics: gravity and inertia respected; realistic weight on crystal prop; correct contact shadows.

TECHNICAL CONSTRAINTS & AUDIO
- Environmental SFX only: howling wind through stone cracks, floor debris crunch, heavy breathing. No music. No subtitles.
- Photorealistic. 8K IMAX quality. Zero jitter. No 3D render feel. No CGI look.
```

---

### 模板 2：流体与复杂大场面白模渲染 (Fluid & Dynamic Sea Storm Rendering)

```text
将[视频1]的白模动画渲染成最终成片。

0–7s： 写实海洋夜景渲染。深灰蓝色暴风雨海面，巨浪持续翻涌，整体采用冷色调与低饱和电影级氛围；海浪具有真实体积感、流体细节和泡沫层次，漂浮的红白相间灯塔保持金属与磨损漆面材质，随海浪自然起伏倾斜；天空布满厚重乌云，伴随细密降雨，远处偶尔出现微弱闪电补光；整体采用 HDR 光照、体积雾、真实环境反射、湿润高光和动态阴影，强化海浪与灯塔的受光变化，保证镜头运动过程中材质和光影连续稳定。

【场景处理】
以暴风雨海域为唯一场景，海面占据主体画面，远处地平线与阴云自然衔接；海浪保持连续流动与起伏节奏，灯塔始终漂浮于海面中央附近，受浪涌驱动产生真实的俯仰、侧倾运动，不发生形变或尺寸变化；雨滴、浪花飞沫、环境雾气保持统一风向和物理逻辑，镜头可轻微跟随海浪上下浮动，增强沉浸感。

【整体收束】
保持暴风雨海域场景不变，整体渲染风格、灯塔材质、海浪流体效果和光影表现保持一致；无人物。
音频处理：保留持续的海浪拍击声、狂风呼啸声、雨声及偶发低沉雷鸣，环境声随镜头距离自然变化，不添加背景音乐或旁白。
```

---

### 模板 3：绿幕 + 3D 白模无缝合成渲染 (Green Screen + White-Box Composite)

```text
对@视频1 的白模场景与@视频2 的绿幕真人表演进行无缝融合渲染。

【角色与运动融合】
- 将@视频2 中的真人角色完美合成到@视频1 的三维白模走位动线上。
- 彻底消除@视频2 绿幕边缘溢色与绿边残影，角色的发丝细节、衣服轮廓与@视频1 场景的光影色调完美匹配。

【环境与落地阴影】
- 场景渲染为@图片1 的古战场废墟环境，逆光环境。
- 角色脚下踩踏古战场地面，生成符合逆光角度的精准接触阴影 (Contact Shadow) 与脚下扬尘。
- 严格保持@视频1 中的三维镜头运动路线与空间视线逻辑。

【收束控制】
- 8K 电影级写实画质，光影真实融合，无浮空感，无绿幕贴图感。
```

---

## 五、 冠军级渲染品质自检表 (Champion Quality Inspection Checklist)

在交付或提交白模渲染任务前，必须通过以下 6 项硬核质检：

- [ ] **1. 机位与轨迹**：生成的视频是否 100% 继承了白模中的相机推拉摇移速度与角度？
- [ ] **2. 空间遮挡**：角色在经过柱子、门框或道具后方时，是否有正确的物理遮挡，而不是穿模闪烁？
- [ ] **3. PBR 材质**：材质表面是否有真实粗糙度、反射高光、磨损与肌理？是否抹除了平滑的塑料 3D 感？
- [ ] **4. 光影介质**：空气中是否有体积雾、光束与飘浮尘埃？暗部是否有深沉的电影级层次？
- [ ] **5. 重力与物理**：角色的脚步、道具的提握、布料的摆动是否符合物理重力与惯性逻辑？
- [ ] **6. 声音卡点**：是否只有纯净的同期动作音效，且完全移除了无意义的 BGM？（同期声锁：`SFX only. No music.`）
- [ ] **7. 模型确认**：生成前是否已确认模型/分辨率/画幅/风格/时长？（⏸️ 确认协议，见 [references/12](12-model-agnostic-system.md)）

---
*01-白模参考视频冠军级渲染系统 · 即梦 Seedance 2.5 专属指南（模型无关通用系统）*
