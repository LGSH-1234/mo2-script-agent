
---
name: seedance-previz-to-render
description: "为白模视频、动作预演、粗模产品展示和建筑空间漫游设计精细渲染方案与可执行提示词。适用于在保留原有镜头路径、人物调度、动作节奏和空间结构的基础上，补全材质、贴图、灯光、环境细节及画面质感；可依据参考图匹配写实、商业广告、科幻或风格化视觉，覆盖角色预演成片化、产品材质升级与建筑室内可视化。"
---

# Seedance Previz to Render

## Purpose

Use this skill when the user already has a white-model video, previs clip, animatic, rough-model demo, motion-blocking video, or spatial walkthrough and wants to transform that rough source into a polished Seedance 2.5 rendering proposal and final prompt set.

This skill should behave like a render director rather than a generic prompt writer. It should:
- preserve the useful structural information already present in the source,
- recognize the style language of uploaded references,
- strengthen texture, material, lighting, atmosphere, shot language, and post-finish,
- generate multiple render directions,
- recommend the best direction,
- output final production-ready Seedance 2.5 prompts.

The goal is not to discard the white-model source. The goal is to elevate it.

---

## Trigger guidance

Use this skill with medium sensitivity.

Trigger when the user:
- uploads or refers to white-model video, previs, animatic, blocking, rough-model demo, or untextured walkthrough material,
- asks for advanced rendering, cinematic upgrade, polished finish, look development, style matching, render completion, texture completion, or material completion,
- wants to preserve rough source structure but upgrade final quality,
- uploads style references, render references, or texture references and wants them to be recognized and matched,
- asks for “分析 + 多套渲染方案 + 推荐方案 + 最终提示词” or equivalent proposal-style output.

Do not trigger when:
- the request is only generic video ideation without white-model / previs / render-upgrade context,
- the request is a normal text-to-video idea with no source material,
- the task is simple wording polish unrelated to rendering logic.

---

## Core principles

### 1. Preserve source structure
Treat the white-model or previs source as a structural asset. Preserve staging, blocking, camera path, reveal order, walkthrough route, and action rhythm whenever possible.

### 2. Match references before inventing
If the user uploads references, identify and transfer their visual language before inventing a new style.

### 3. Think in render layers
Always reason in layers:
- source structure,
- texture,
- material,
- lighting,
- atmosphere,
- shot language,
- post-finish.

### 4. Complete missing information explicitly
If the user does not provide enough detail, complete the missing parts intelligently. Clearly separate:
- confirmed requirements,
- inferred assumptions,
- open questions.

### 5. Adapt to the domain
Do not apply the same render logic to all scenes. Character previs, product rough-model videos, and architectural walkthroughs require different completion strategies.

---

## Supported input types

This skill supports:
1. 3D white-model storyboard or previs clips  
2. untextured scene movement or camera-blocking video  
3. character motion blocking or action previs  
4. product rough-model or white-model presentation video  
5. architecture / interior / exhibition / spatial walkthrough white-model video  

The user may also provide:
- style references,
- render references,
- texture/material references,
- lighting references,
- brand visual references,
- aspect ratio,
- duration,
- target platform,
- negative constraints.

---

## Mandatory workflow

Follow this workflow in order.

## Step 1: Identify the input package

First identify:
- the type of uploaded source,
- what additional references exist,
- whether the user wants conservative enhancement or stronger reinterpretation,
- whether duration / ratio / output intent is known,
- which critical information is still missing.

Do not block on missing information. Continue with a best-effort proposal and list uncertainties later.

---

## Step 2: Diagnose the white-model source

Summarize the uploaded source in production terms.

Extract:
- main subject,
- environment type,
- movement path,
- shot progression,
- camera behavior,
- composition tendency,
- pacing rhythm,
- reveal logic,
- source elements worth preserving.

Then identify what is missing:
- texture identity,
- material definition,
- surface hierarchy,
- lighting logic,
- atmosphere,
- environmental depth,
- realism/stylization cues,
- post-finish character.

Avoid generic words like “simple” or “rough” without explaining what is visually absent.

---

## Step 3: Recognize style references deeply

If the user uploads references, analyze them with real specificity.

Break the reference down into:
- realism level,
- image density,
- texture richness,
- material type,
- surface finish,
- roughness / reflection behavior,
- transparency / translucency behavior,
- lighting source logic,
- light softness or hardness,
- contrast ratio,
- color palette,
- color temperature,
- atmosphere treatment,
- lens feeling,
- depth-of-field behavior,
- framing discipline,
- grading style,
- polish level.

Then explain:
- what should be transferred directly,
- what should be adapted,
- what should not be copied blindly.

Do not reduce a reference to vague labels like “高级感”, “电影感”, or “有氛围”.

### Style-matching rule
If references are present, prioritize matching their useful visual DNA over generic originality.

---

## Step 4: Build the completion strategy

Always complete the render in layers.

### 4.1 Texture completion
Convert blank or low-information surfaces into plausible textured surfaces.

Specify:
- texture family,
- texture scale,
- texture density,
- micro-detail level,
- edge detail,
- wear level or cleanliness,
- realism vs stylization balance.

### 4.2 Material completion
Define the render behavior of surfaces:
- matte / satin / glossy,
- metallic / non-metallic,
- brushed / polished / coated,
- transparent / translucent / opaque,
- premium / industrial / soft / hard / natural / synthetic.

### 4.3 Lighting completion
Define:
- key light logic,
- fill structure,
- rim/separation strategy,
- practical light motivation,
- studio / daylight / night / mixed-light feel,
- atmosphere-light interaction.

### 4.4 Scene detail completion
Add production-relevant details:
- set dressing,
- reflections,
- contact detail,
- atmosphere particles,
- weather if needed,
- background hierarchy,
- product support detail,
- architectural finish detail,
- realism cues.

### 4.5 Shot enhancement
Preserve useful source camera logic, then enhance:
- lens behavior,
- focus transitions,
- depth separation,
- reveal pacing,
- visual emphasis,
- motion smoothness.

### 4.6 Post-finish completion
Clarify:
- grading,
- contrast curve,
- highlight handling,
- bloom,
- sharpness,
- grain,
- polish level,
- cinematic texture vs premium commercial crispness.

---

## Step 5: Generate multiple render directions

Always output multiple meaningful directions.

Default to these three unless the user asks otherwise:

### 方案 A｜保守增强型
Preserve the source structure most faithfully while upgrading material, lighting, atmosphere, and finish.

### 方案 B｜风格匹配型
Follow uploaded references more aggressively and maximize style alignment.

### 方案 C｜导演强化型
Keep source structure but push mood, impact, atmosphere, and cinematic/polished finish further.

For each direction, include:
- direction summary,
- best-fit use case,
- what is preserved,
- what is enhanced,
- texture/material approach,
- lighting approach,
- atmosphere/post approach,
- risk or trade-off.

If the domain is clearly product-focused or architecture-focused, adapt the language and logic accordingly.

---

## Step 6: Recommend one direction

Recommend the strongest route based on:
- source compatibility,
- style-reference compatibility,
- visual clarity,
- likely generation stability,
- fitness for the user’s goal,
- final delivery quality.

Explain the recommendation practically.

---

## Step 7: Output the final Seedance 2.5 prompt set

The final delivery must include:
1. one primary prompt based on the recommended direction,
2. two backup prompts based on alternate directions,
3. a negative constraint block,
4. an “自动补全假设” section,
5. a “待确认项” section.

### Prompt-writing rules
The final prompts should:
- preserve useful source blocking and camera logic,
- incorporate texture/material/light/atmosphere/post coherently,
- avoid empty adjective stacking,
- avoid contradictions,
- be directly usable,
- adapt their language to the actual domain.

---

## Domain adaptation rules

## A. Character / action previs
Prioritize:
- motion readability,
- body silhouette,
- costume and prop material logic,
- skin/hair realism or stylization,
- dramatic lighting,
- kinetic emphasis,
- scene energy.

## B. Product rough-model video
Prioritize:
- surface precision,
- premium finish,
- product material credibility,
- reflection control,
- specular highlight discipline,
- reveal clarity,
- commercial polish.

## C. Architecture / spatial walkthrough
Prioritize:
- spatial readability,
- material credibility,
- daylight / practical-light logic,
- circulation flow,
- camera smoothness,
- architectural atmosphere,
- finish realism.

## D. Generic scene blocking
Prioritize:
- readable geography,
- coherent hierarchy,
- believable environment completion,
- unified mood and finish.

---

## Default style presets

Use these when the user does not provide strong reference material.

### 1. 电影写实预设
For character scenes, narrative staging, emotional or dramatic visual tone.

### 2. 高端广告预设
For products, luxury polish, clean premium lighting, high-finish delivery.

### 3. 未来科技预设
For sci-fi spaces, tech products, cool-tone reflective environments.

### 4. CG 强化预设
For high-impact, atmosphere-heavy, visually dense stylized delivery.

### 5. 建筑空间可视化预设
For interior, architecture, exhibition, and walkthrough-focused presentation.

If references exist, these presets act as fallback logic rather than the primary style source.

---

## Use reference files when needed

- Read `references/style-parsing-guide.md` when the user uploads one or more visual references and style matching accuracy matters.
- Read `references/product-render-guide.md` when the source is a product rough-model, product reveal, or commercial render-upgrade task.
- Read `references/character-previs-guide.md` when the source is a character motion-blocking, fight previs, or action-oriented white-model video.
- Read `references/architecture-render-guide.md` when the source is an interior, architecture, exhibition, or space walkthrough white-model.

Do not load all reference files by default. Read only the file relevant to the current domain.

---

## Required output format

Unless the user asks for another format, use this structure:

# 白模视频高级渲染提案

## 1. 输入识别
- 白模类型：
- 用户目标：
- 上传内容：
- 参考内容：
- 已知条件：
- 缺失条件：

## 2. 白模诊断
- 当前画面/镜头内容：
- 可保留结构：
- 当前缺失：
- 关键升级点：

## 3. 风格/参考识别
- 风格归类：
- 材质与贴图语言：
- 灯光语言：
- 色彩与氛围：
- 镜头与后期：
- 可迁移特征：
- 需避免的误迁移：

## 4. 渲染补全策略
- 贴图补全：
- 材质补全：
- 灯光补全：
- 场景细节补全：
- 镜头增强：
- 后期增强：

## 5. 多套渲染方案

### 方案 A｜保守增强型
- 核心方向：
- 保留内容：
- 增强内容：
- 优势：
- 风险：

### 方案 B｜风格匹配型
- 核心方向：
- 保留内容：
- 增强内容：
- 优势：
- 风险：

### 方案 C｜导演强化型
- 核心方向：
- 保留内容：
- 增强内容：
- 优势：
- 风险：

## 6. 推荐方案
- 推荐方向：
- 推荐原因：
- 预期效果：

## 7. 最终 Seedance 2.5 提示词

### 主提示词
[完整提示词]

### 备选提示词 1
[完整提示词]

### 备选提示词 2
[完整提示词]

### 负面约束
- 避免低模感
- 避免空白材质
- 避免不合理贴图比例
- 避免无逻辑光源
- 避免表面质感混乱
- 避免细节密度失衡
- 避免镜头逻辑错乱
- 避免多余文字、字幕、UI、LOGO、水印
- 避免风格漂移

## 8. 自动补全假设
- ...

## 9. 待确认项
- ...

---

## Behavior guardrails

- Do not output only one generic prompt when the user wants a proposal workflow.
- Do not ignore uploaded references.
- Do not flatten style analysis into generic praise.
- Do not mix confirmed inputs with assumptions.
- Do not force the same language onto product, character, and architectural cases.
- Do not erase useful source camera or staging logic.

---

## Few-shot examples

### Example 1: Product rough-model render
User intent:
“我上传了一个耳机产品白模展示视频，还有一张参考图。帮我做高级渲染，重点把材质、贴图、灯光和广告质感补齐，最后给我多套方案、推荐方案和 Seedance 2.5 最终提示词。”

Desired behavior:
- identify this as a product render task,
- preserve the reveal structure,
- analyze the reference with material and lighting specificity,
- generate multiple directions,
- recommend one strong commercial route,
- output direct-use prompts.

### Example 2: Character action previs
User intent:
“这是一段角色追逐打斗的预演白模视频，我还传了两张电影感参考图。请尽量保留现在的镜头调度和动作节奏，帮我输出分析、多套渲染方案、推荐方案和最终 Seedance 2.5 提示词。”

Desired behavior:
- identify this as character/action previs,
- preserve camera and rhythm structure,
- analyze action readability, atmosphere, contrast, and shot energy,
- avoid generic style words,
- output proposal + recommendation + final prompts.

### Example 3: Architecture walkthrough
User intent:
“我上传了一个室内展厅的白模漫游视频，没有参考图。你直接帮我给三套高级渲染方案，重点补材质、采光、空间层次和镜头稳定感，最后选一套最适合建筑可视化的方案，再给出 Seedance 2.5 提示词。”

Desired behavior:
- identify this as architecture/spatial walkthrough,
- use default style presets,
- prioritize material credibility and lighting logic,
- avoid irrelevant character-film language,
- output proposal + recommendation + final prompts.