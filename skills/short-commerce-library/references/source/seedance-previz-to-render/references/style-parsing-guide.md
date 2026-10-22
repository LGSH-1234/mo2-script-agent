
# Style Parsing Guide

Use this guide when the user uploads one or more visual references and wants the white-model or previs source to match a specific render style.

The purpose of this guide is to prevent shallow style analysis. Do not stop at labels like “高级感”, “电影感”, “很有氛围”, or “偏广告”. Instead, break style down into render-operational layers that can be transferred into a Seedance 2.5 prompt.

## Goal

You are not simply describing the reference. You are extracting the visual DNA that should drive the render proposal.

Your job is to identify:
- what the reference is doing visually,
- which parts are essential,
- which parts are optional,
- which parts are transferable to the user’s source material,
- which parts may conflict with the white-model content and must be adapted.

## Layered style reading

Always inspect the reference through the following layers.

### 1. Realism level
Describe where the reference sits on this spectrum:
- physically plausible realism,
- polished commercial realism,
- stylized realism,
- heavy CG stylization,
- design-forward abstraction.

Do not assume that “more realistic” is always better. Choose the level that best fits the uploaded source and user intent.

### 2. Image density
Check:
- how visually dense the frame feels,
- whether surfaces are clean and sparse or rich with detail,
- whether the frame relies on minimalism, precision, grit, or spectacle.

This affects how aggressively you should complete texture and scene detail.

### 3. Material language
Identify the dominant material families.
Examples:
- polished metal,
- brushed aluminum,
- glossy lacquer,
- satin plastic,
- smoked glass,
- soft fabric,
- matte concrete,
- warm wood,
- glossy ceramic,
- translucent acrylic.

Describe not just what the material is, but how it behaves visually.

### 4. Surface finish behavior
Inspect:
- gloss vs matte,
- roughness consistency,
- micro-scratches,
- edge sharpness,
- reflection quality,
- cleanliness vs wear,
- premium smoothness vs industrial toughness.

This is often what separates a generic render from a convincing one.

### 5. Texture density and scale
Describe:
- whether texture is obvious or subtle,
- whether detail sits at macro scale, micro scale, or both,
- whether the image uses fine-grain realism or broad graphic surface treatment.

Do not say “texture丰富” without saying where and how it is rich.

### 6. Lighting logic
Identify:
- key light direction,
- fill strategy,
- rim or separation light,
- practical light sources,
- whether the scene is driven by daylight, studio light, practicals, or mixed light,
- whether the light feels soft, hard, crisp, diffused, moody, clinical, warm, or sculptural.

Always explain how the light shapes the subject.

### 7. Contrast style
Check:
- global contrast,
- local contrast,
- highlight compression,
- shadow openness,
- black density,
- whether the image feels soft-rolloff, punchy, glossy, dramatic, or airy.

### 8. Color system
Identify:
- dominant palette,
- palette complexity,
- temperature bias,
- complementary color contrast,
- whether the image is neutral, warm, cool, desaturated, neon, premium monochrome, etc.

Do not treat color as decoration only. Color often signals the intended finish class.

### 9. Atmosphere treatment
Check whether the reference uses:
- haze,
- volumetric light,
- air perspective,
- suspended particles,
- fog,
- glow,
- environmental softness,
- crisp clarity.

Atmosphere should support the render direction, not be added blindly.

### 10. Lens and framing feel
Identify:
- perceived focal length,
- lens compression or expansion,
- depth-of-field strength,
- framing discipline,
- camera intimacy vs distance,
- whether the style feels handheld, stabilized, floating, locked-off, or premium-commercial controlled.

### 11. Post-finish signature
Describe:
- grade polish,
- grain or no grain,
- sharpening behavior,
- bloom,
- highlight bloom,
- edge crispness,
- premium clean finish vs cinematic texture.

## Transfer decision

After analyzing the reference, explicitly state:

### What to transfer directly
These are the style traits that should survive into the render proposal with minimal change.

### What to adapt
These are traits that matter, but need adjustment because the source domain, geometry, or use case is different.

### What not to copy blindly
These are reference traits that could hurt the result if copied literally.
Examples:
- shallow depth-of-field that would obscure product form,
- overly dramatic darkness in architecture,
- heavy grime on a premium product,
- hyper-stylized color that breaks spatial credibility.

## Reference conflict handling

When the user provides multiple references:
- identify what is common across them,
- identify where they conflict,
- decide which reference should dominate,
- explain the merge strategy.

If one reference controls lighting and another controls material finish, say so explicitly.

## Output pattern

When using this guide, your style section should usually answer:
- What kind of image system is this?
- What material and surface logic define it?
- What light and contrast logic define it?
- What atmosphere and post-finish define it?
- Which parts should be transferred into the current render?

## Bad analysis example

“这张参考图整体很高级，很有电影感，氛围比较到位，适合做高质感渲染。”

This is too vague and not operational.

## Better analysis pattern

“The reference uses polished commercial realism with controlled image density, premium clean surfaces, soft-but-directional studio lighting, tight reflection management, cool-neutral palette bias, restrained depth of field, and a crisp high-finish grade. The most transferable features are the smooth metallic finish, clean edge highlights, soft separation light, and controlled background simplification. The shallow DOF should be softened if the user needs stronger product legibility.”

## Final reminder

Your style analysis must help produce a better render prompt. If the analysis cannot be translated into texture, material, light, atmosphere, lens, or post instructions, it is not detailed enough.