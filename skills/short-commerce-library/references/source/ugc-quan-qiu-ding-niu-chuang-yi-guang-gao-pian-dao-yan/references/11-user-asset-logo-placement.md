# 11-user-asset-logo-placement.md · 用户资产定制与 Logo/品牌植入系统 (User Asset & Logo Placement)

> **归属系统**：即梦 Seedance 2.5 终极 AI 电影大师全流程制作系统 V8.0（0818多参版·模型无关通用系统）
> **归属引擎**：资产设计引擎 (E4) + 视觉美学引擎 (E2) + 叙事与导演引擎 (E1)
> **关键词**：用户资产定制 / @Asset_IMG 图像引用 / @CharID_AUDIO 声音引用 / Logo 植入三铁律 / 载体分析 / 透视锁定 / 绿幕合成 / 双重指定 / LibTV 实战
> **相对路径关联**：`SKILL.md` | `references/05-lira-asset-generation.md` | `references/10-capability-engines.md` | `references/12-model-agnostic-system.md`

---

## 一、资产识别与意图解析 (Asset Recognition & Intent Parsing)

用户上传任何自定义素材，先识别意图，再决定锚定策略：

```
用户上传 Logo 图片   → 意图：将 Logo 以不违和的方式植入特定场景载体（品牌植入定制）
用户上传角色照片     → 意图：后续所有生成中，该角色的外貌形象与此照片保持高度一致（角色资产锁定）
用户上传声音样本     → 意图：后续所有该角色的对白/语气词，均使用此音色（音色锁定）
用户上传场景/道具图  → 意图：作为 @SCN / @PROP 资产锚定（场景/道具资产锁定）
```

**用户资产绝对服从原则**：用户提供的 Logo/照片/声音样本，其外观与音色在全部生成中保持高度一致，不擅自改动、不擅自改造。@ 名称一律用中文，与用户资产命名严格一致。

---

## 二、资产锚定与引用规范 (Asset Anchoring & Reference Spec)

### 1. 图像资产引用格式 (Image Asset Reference)
```
@Asset_IMG_[中文名/代号]  — 全项目统一引用
例：@Asset_IMG_LibTV_Logo（LibTV 品牌 Logo）
```

- 上传后立即锚定：在 Gate G2 资产锁定门登记，描述符逐字进入每个引用它的提示词。
- 与角色资产（@CHAR_唐末）、场景资产（@SCN_长安_宫城）、道具资产（@PROP_古圣晶石）并列管理，同入 @命名字典。

### 2. 声音资产引用格式 (Audio Asset Reference)
```
@CharID_AUDIO_[中文角色名]  — 该角色所有对白/语气词锁定此音色
例：@CharID_AUDIO_唐末
```

- 结合六维音色建模（音域/语速/口音/音色质感/情绪倾向/音量动态范围）与 VOX LOCK 跨镜一致性锁定（见 [references/06](references/06-audio-driven-sound-engineering.md)）。
- 声音样本 4-8s 为佳；同一角色在争吵/突变场景下：语气词变化 + 声调升高，但音色指纹不变。

### 3. 锚定流程（两阶段强确认）
```
阶段一：上传 + 意图解析 → 输出锚定方案（引用名/控制维度/使用范围）→ ⏸️ 用户确认
阶段二：压测验证（如角色照片：生成 5 张不同姿势/灯光/背景的姿态图，10/10 可识别即通过）→ 登记 @命名字典 → ⏸️ 用户确认
```

---

## 三、Logo 与品牌植入分镜流程 (Logo & Brand Placement)

### ⚠️ 核心警告：图生视频模型会自动改写文字与 Logo！
Seedance 2.5 及同类视频模型在生成时，经常自动改写/重绘画面中的文字与 Logo。要在视频中植入固定 Logo，必须使用以下任一方案：

### 方案一：后期/绿幕合成（最高保真，推荐用于关键露出）
1. 视频生成时**画面不含 Logo**（干净画面），预留植入位置与透视角度。
2. 后期用绿幕合成/抠像工具将 Logo 贴入，匹配运动跟踪（Tracking）与光照。
3. 优势：Logo 100% 保真；劣势：需后期环节。

### 方案二：参考图 + 提示词双重指定锁定（图生视频直接植入）
1. **参考图中先写好 Logo**：在参考图片上精确放置 Logo（位置/透视/光照/大小）。
2. **提示词显式锁定**：`@Asset_IMG_LibTV_Logo — the logo on the radio cabinet stays EXACTLY as in the reference image: same position, same perspective, same lighting, same size. DO NOT redraw, DO NOT restyle, DO NOT move the logo.`
3. 双重指定：图片与提示词双重约束，最大限度防改写。

### 方案三：图片生成阶段植入（文生图/图生图）
- 生成含 Logo 的关键帧图片时，图片最好**不包含文字与 Logo**（模型会自动往关键帧中执行写文字或改写 Logo）。
- 若必须在图片中含 Logo：先在参考图写好 → 提示词锁定 → 双重指定。

### 植入三铁律 (Placement Three Laws)
1. **载体分析**：Logo 必须植入选定的剧情载体——收音机/电视/海报/石碑/旗帜/包装/招牌——载体与剧情自洽，绝不凭空悬浮。
2. **透视与光照一致**：Logo 的透视、光照、阴影与载体表面物理一致（贴在平面、跟随运动、随光变向）。
3. **用户确认植入分镜**：植入分镜（载体/位置/透视/大小/时长）必须在 Gate G3 输出并经用户确认，绝不擅自植入。

---

## 四、Logo 植入分镜模板 (Logo Placement Shot Template)

```
【植入镜】[镜头号] | 时长：Xs | 时间码：XX:XX – XX:XX
载体: [收音机/电视/海报/石碑/旗帜/包装…]  @PROP_XX
Logo 引用: @Asset_IMG_LibTV_Logo
植入方式: [方案一 后期绿幕 / 方案二 双重指定 / 方案三 图片阶段]
位置: [载体表面区域：如收音机正面铭牌区，中下部]
透视: [正面平视 / 30° 侧视 / 俯视…] + [随镜头运动跟随]
光照: [主光源方向 / Logo 表面高光与阴影随载体]
大小: [占载体表面 X% / 相对镜头 X cm]
锁定句: The LibTV logo stays EXACTLY as referenced: same shape, same colors, same proportions, glued to the cabinet surface, no redraw, no restyle, no drift.
```

---

## 五、实战示例：LibTV Logo 植入 (LibTV Case Study)

### 场景设定
80 年代科幻短片，主角在老式收音机店。品牌方要求植入 LibTV Logo（图形化标志）。

### 植入决策
- **载体**：老式木质收音机正面铭牌区（复古 + 品牌自然露出，不违和）。
- **植入方案**：方案二（参考图双重指定）为主镜 + 方案一（绿幕后期）为特写补强。
- **@ 命名**：`@Asset_IMG_LibTV_Logo`、`@PROP_收音机_老式木壳`。

### 分镜提示词（图生视频 · 主镜）
```
SCENE CONTEXT
SHOT SC02-SH04 (5.0s) — Retro radio shop interior, dusk. Continuance of SC02-SH03.

ACTIVE REFERENCES
@CHAR_店主 — [60s Chinese man, grey cardigan, reading glasses, weathered face]
@PROP_收音机_老式木壳 — [vintage wooden cabinet radio, brass knobs, fabric speaker grille]
@Asset_IMG_LibTV_Logo — [LibTV logo printed on the cabinet nameplate area, lower-middle, facing camera, warm tungsten light]

FIRST FRAME AND SPATIAL BLOCKING
SHOT (0-1.0s) — Medium shot: the shopkeeper's hand turns the brass volume knob. The radio cabinet's nameplate with the LibTV logo is clearly visible screen-right, lit by warm tungsten.

FORMAT MODE
SINGLE CONTINUOUS TAKE.

LOGO LOCK (植入锁定)
The LibTV logo on the radio nameplate stays EXACTLY as in the reference: same shape, same red-white colors, same proportions, glued flat to the wooden surface, perspective fixed to the cabinet, no redraw, no restyle, no move, no drift. The logo receives the same warm tungsten light as the cabinet.

OPTICS & LIGHTING
47° standard lens, warm tungsten key from screen-left, amber shadows, subtle dust particles in the light beam.

ACTION TIMING
0.0-1.0s — hand turns knob; 1.0-3.0s — radio crackles to life; 3.0-5.0s — shopkeeper smiles, leans back.

AUDIO & DIALOGUE
SFX only: radio static, knob click, distant street sound. No music. No BGM.
```

### 特写镜（方案一 绿幕后期）
- 生成干净画面（Logo 区留空/纯色板）→ 后期绿幕合成 Logo + 运动跟踪 → 与主镜无缝衔接。

---

## 六、用户资产定制完整清单 (User Asset Checklist)

- [ ] 上传素材已识别意图并分类（Logo/角色照片/声音样本/场景道具）
- [ ] 引用名已锚定（@Asset_IMG_XX / @CharID_AUDIO_XX）且为中文，与用户命名一致
- [ ] 已登记 @命名字典，描述符逐字进入每个引用提示词
- [ ] 角色照片已过压测（5 姿态图 10/10 可识别）
- [ ] 声音样本已做六维音色建模 + VOX LOCK
- [ ] Logo 植入已选载体 + 方案 + 透视/光照/大小锁定
- [ ] 植入分镜已经用户确认（Gate G3）
- [ ] 图生视频提示词含锁定句（no redraw / no restyle / no drift）
- [ ] 图生视频音频块含 `SFX only. No music.`（同期声锁）

---

## 全网系统交叉关联地图 (System Cross-Reference Map)
- 根架构文件: `SKILL.md`
- 资产生成与状态资产: `references/05-lira-asset-generation.md`
- 能力引擎与质量门: `references/10-capability-engines.md`
- 声音工程与 VOX LOCK: `references/06-audio-driven-sound-engineering.md`
- 模型无关适配层: `references/12-model-agnostic-system.md`

---

*11-user-asset-logo-placement.md v7.2 · 用户资产定制与 Logo/品牌植入系统*
