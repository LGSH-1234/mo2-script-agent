# 08-大师级提示词模板库与实战范例 (Master Prompt Templates)

> **归属系统**：即梦 Seedance 2.5 终极提示词库（模型无关通用系统，默认 Seedance 2.5）
> **归属引擎**：视觉美学引擎 (E2) + 资产设计引擎 (E4) + 声音工程引擎 (E5)（六引擎体系见 [references/10](10-capability-engines.md)）
> **使用说明**：本模板库提供生产准备 (Production-Ready) 级别的即用 Prompt 框架，支持直接复制并替换变量使用。
> **@ 命名**：所有 @ 引用一律用中文角色/资产名，与用户资产命名严格一致（如 @CHAR_唐末 / @SCN_长安_宫城_夜 / @Asset_IMG_LibTV_Logo）；Logo 植入完整流程见 [references/11](11-user-asset-logo-placement.md)。

---

## ⚡ 全局 Style Prefix 常量 (Style Prefix Constant — 逐字复制到每个提示词末尾)

> **吸收自 HELL GRIND 制作简报**：Style Prefix 逐字复制进每个提示词的结尾，从不改动。`SFX only. No music.` 是强制行——音乐属于后期，生成配乐只会妨碍剪辑。

```text
Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: floating immersive camera that lives with the actors; natural motivated light; painterly composed frames, strong silhouettes against the light.
Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze throughout. Key light from sky and windows only.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with catch-lights, visible breath and chest rise.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

**收尾技术标签**：`Photoreal. NON-IP. [aspect ratio]. [duration]s. SFX only. NO CGI. Cinematic.`

---

## 模板 1：白模参考视频冠军级渲染模板 (White-Box Champion Render)

### 适用场景
上传 Maya / Blender / C4D / UE5 的 3D 白模/灰模/Animatic 预演视频作为 `@视频1`，结合角色/场景参考图进行 8K IMAX 电影级渲染。

### ⛔ 使用铁律（先读再写）
- **@视频1 必须单段完整生成**：白模视频作为整体参考，一次生成一个完整连续成片，**严禁按分镜切割成多个片段分别生成再拼接**。
- 提示词内的时间段标注（如 0-7s）仅描述材质/光影变化，不是切分指令。
- 若白模过长需分段，先与用户确认，且每段独立成完整动作弧、单独走确认门。

```text
对@视频1 的 3D 白模动画进行 8K IMAX 电影级物理渲染。

【参考素材锁定】
- 角色外观：参考@图片1（面部五官、发型、肤质、服饰细节严格还原，无脸部漂移）
- 场景环境：参考@图片2（场景架构、材质质感、环境氛围、打光方式保持一致）
- 道具细节：参考@图片3（材质表面、磨损痕迹、物理光感）

【三维空间与机位控制】
- 严格遵循@视频1 中的三维相机运镜轨迹、焦距变化与镜头视角，不得自行改变运镜速度或机位。
- 100% 还原白模中的空间几何关系、人物走位路线、前后景遮挡逻辑与视线方向。

【冠军级 PBR 材质与物理光影渲染】
- 材质细节：采用 8K PBR 物理渲染，呈现极度真实的表面肌理（毛孔瑕疵、汗水高光、织物缝线、金属氧化磨损）。
- 光影与介质：HDR 电影级采光，主光打入呈现清晰的体积光/丁达尔光束与深沉的 Chiaroscuro 阴影，空气中飘浮微小尘埃颗粒。
- 物理动力学：遵从真实重力与惯性，布料随运动自然褶皱飘动，踩踏扬起微尘/水花，接触点阴影精准附着。

【音效与收束控制】
- 保留环境音与动作同期声（碎石踩踏声、水花溅起声、呼吸声），禁止自动添加 BGM 或字幕。
- 画面无抖动、无失真、无脸部形变、无 3D 灰模感，呈现顶级电影实拍质感。
```

---

## 模板 2：14 区块全效连续分镜模板 (14-Block Continuous Take)

### 适用场景
生成高预算电影级长镜头，锁定角色、空间与光学焦段。

```text
SCENE CONTEXT
EXACT 1 CHARACTER — NO DUPLICATES: 角色名. SHOT SC01-SH01 (4.0s) — Interior abandoned ruin, night. Single continuous take.

ACTIVE REFERENCES
@CHAR_角色名 — [Tall build, dark coarse coat, left cheek scar, natural skin texture. 100% matches the reference]
@SCN_场景名 for location reference — take only the space and the texture: [Stone archways, broken pillars, blue moonlight beam, airborne dust motes]. Do not use as a starting frame, do not inherit the composition, the angle or the color.
@PROP_道具名 — [Glowing olivine crystal, worn brass metal casing]

LOCATION MAP
- ARCHWAY: Background center.
- CHAR_角色名: Frame-left third, standing 1.5m from archway.

GEO SPATIAL LAYOUT
— CAMERA ZONE = South side of the hall, 180-degree axis strictly respected.
— LIGHT DIRECTION = Single moonlight beam coming from top-right arch, 45-degree angle.

FIRST FRAME AND SPATIAL BLOCKING
SHOT 1 (~1.0s) — Fixed position wide shot: Character stands motionless in frame-left third, facing right. Right hand holds @PROP_道具名 at hip level. No camera move on frame one. The first visible frame already contains the required character in correct position — no empty establishing frame.

FORMAT MODE
SINGLE CONTINUOUS TAKE.

OPTICS
Cuarón intimate wide lens, 84° diagonal field of view, camera distance 1.5m, deep depth of field.

CAMERA
Chest-height fixed position. Calm breathing handheld. Zero drift.

ACTION TIMING
0.0s – 1.0s — Spatial position locked. Character breathes, chest rises 2cm.
1.0s – 3.0s — Character slowly raises right hand 15cm; thumb presses edge of @PROP_道具名. Faint green light illuminates palm and jawline.
3.0s – 4.0s — Character turns head 30 degrees to right rear. Double blink. Eyeline locks to doorframe before head movement.

PHYSICS & WEIGHT
Gravity active. Wrist angle reflects crystal mass. Coat material shows slight inertial delay.

LIGHTING PRIORITIES
Single cool blue moonlight from top-right arch. Character stays on shadow side; 70% deep chiaroscuro shadow on face.

AUDIO & DIALOGUE
Environmental SFX only — wind through stone cracks, floor gravel shift at 3.2s. Dialogue: "They found us." (Voice: low dry baritone, slow pacing, going quieter as things get serious). Everyone speaks ONLY the line in quotes. No music. No subtitles.

ACTING & MICRO-BEHAVIOR
Restrained tension. Jaw clenches once at 3.0s. Eyeline locks before head movement. States not transitions.

STYLE PREFIX
[完整 Style Prefix 常量 — 逐字复制见文件顶部，含 "SFX only. No music."]

QUALITY
8K detail, pore-level skin, no jitter, no flicker; the face stays exactly its reference at every distance. Photoreal. NON-IP. 16:9. 4s. SFX only. NO CGI. Cinematic.
```

---

## 模板 3：多角色独立混战模板 (Multi-Character Action Combat)

```text
SCENE CONTEXT
EXACT 3 CHARACTERS — NO DUPLICATES: @图片1 的光头拳手、@图片2 的红发女格斗家、@图片3 的亚裔搏击手，在@图片4 场景内三方混战。Single continuous 8-second take, real time.

ACTIVE REFERENCES
@图片1 for character reference — 光头拳手, broad-shouldered, bare-knuckle stance. 100% matches the reference.
@图片2 for character reference — 红发女格斗家, lean, high guard. 100% matches the reference.
@图片3 for character reference — 亚裔搏击手, compact, southpaw. 100% matches the reference.
@图片4 for location reference — take only the space and the texture. Do not use as a starting frame, do not inherit the composition, the angle or the color.

【角色独立与防串脸】
三位角色外貌、服装、体型严格独立保持，参考各自的图片展板，全程不串脸、不交换服装、不大脑融合。Exactly three people in the frame, and no one else.

【空间与动作时序】
- [00:00 - 00:02] 开场三人呈三角站位在@图片4 场景中央对峙，脚步踩踏地面扬起微尘。
- [00:02 - 00:05] @图片1 光头拳手率先冲向@图片2 红发女打出重拳；@图片2 侧身闪避，顺势一记鞭腿反击。
- [00:05 - 00:08] @图片3 亚裔搏击手从侧翼切入摆拳，三人动作在同一空间内交错爆发，肢体碰撞符合真实重力与物理遮挡。

【特写与物理烘托】
关键特写：@图片1 拳手下巴被击中，汗水飞溅，咬肌紧绷。灯光摇晃，逆光中尘埃与汗水形成清晰的体积光。

【收束控制】
写实电影级动作画质，画面流畅自然，仅保留物理打击声与喘息声，禁止 BGM 与字幕。Photoreal. NON-IP. 16:9. 8s. SFX only. NO CGI. Cinematic.
```

---

## 模板 4：视频延长与续写模板 (Video Extension & Continuance)

```text
参考@视频1 的内容向后延长 5 秒 (12s - 17s)。

【一镜到底要求】
要求延长自然连贯，动作与@视频1 完美衔接。保持镜头呼吸感与相同空间轴线，一镜到底，禁止生硬切镜，禁止物体凭空出现。

【动作时序】
角色@图片1 维持往前走的步态，在 14 秒处转头看向右侧水面。水面受某种力量冲击开始剧烈翻涌，从水中缓慢升起@图片2 的巨大发光样本舱。

【声音与环境】
音效与@视频1 的海浪声与风声衔接，在 14 秒水面翻涌时加入低沉的水浪爆裂声音。无背景音乐，无字幕。
```

---

## 模板 5：局部消除与智能编辑模板 (Inpainting & Erasing)

```text
消除@视频1 中圈选标注的背景人群与杂物。

【修补指令】
保留主体@图片1 角色与其物理走位，将原本有杂人的背景区域平滑修补渲染为@图片2 的寂静雪山废墟环境。

【光影匹配】
修补区域的光影色调、颗粒度与镜头深度与@视频1 的原角色保持 100% 融合，无合成边缘与画质断层。
```

---

## 模板 6：Logo/品牌植入模板 (Logo & Brand Placement)

> **完整流程与三铁律见 [references/11-user-asset-logo-placement.md](11-user-asset-logo-placement.md)**。核心：图生视频模型会自动改写 Logo → 采用"参考图双重指定锁定"或"绿幕后期合成"。

```text
SCENE CONTEXT
SHOT SC02-SH04 (5.0s) — Retro radio shop interior, dusk. Continuance of SC02-SH03.

ACTIVE REFERENCES
@CHAR_店主 — [60s Chinese man, grey cardigan, reading glasses, weathered face]
@PROP_收音机_老式木壳 — [vintage wooden cabinet radio, brass knobs, fabric speaker grille]
@Asset_IMG_LibTV_Logo — [LibTV logo on the radio nameplate area, lower-middle, facing camera]

FIRST FRAME AND SPATIAL BLOCKING
SHOT (0-1.0s) — Medium shot: the shopkeeper's hand turns the brass volume knob. The radio nameplate with the LibTV logo is clearly visible screen-right, lit by warm tungsten.

LOGO LOCK (植入锁定 — 防改写铁律)
The LibTV logo on the radio nameplate stays EXACTLY as in the reference: same shape, same colors, same proportions, glued flat to the wooden surface, perspective fixed to the cabinet, no redraw, no restyle, no move, no drift.

FORMAT MODE
SINGLE CONTINUOUS TAKE.

OPTICS & LIGHTING
47° standard lens, warm tungsten key from screen-left, amber shadows, dust particles in the light beam.

ACTION TIMING
0.0-1.0s — hand turns knob; 1.0-3.0s — radio crackles to life; 3.0-5.0s — shopkeeper smiles, leans back.

AUDIO & DIALOGUE
SFX only: radio static, knob click, distant street sound. No music. No BGM. No subtitles.
```

**特写镜替代方案**：若需要 Logo 特写且要求 100% 保真 → 生成干净画面（Logo 区留空）→ 后期绿幕合成 + 运动跟踪。

---

*08-大师级提示词模板库与实战范例 · 即梦 Seedance 2.5 专属指南（模型无关通用系统）*
