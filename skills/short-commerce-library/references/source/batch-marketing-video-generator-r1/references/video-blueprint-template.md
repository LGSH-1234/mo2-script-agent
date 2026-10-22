
# video-blueprint-XX.md Template

This reference defines the content and quality of one video's model-independent creative blueprint. It is a complete, user-reviewable story, not an executable video prompt or `PromptPath`. Naming an intended material does not mean that an asset exists or has been accepted.

## Language Layers

Apply [user-communication.md](user-communication.md) to the entire user-visible document, not just its title. The English labels below illustrate semantic structure; they are not literal keys to copy.

- Write the business title, section headings, table headers, shot labels, explanatory prose, and human-readable values such as speech types or “None” in `COMMUNICATION LANGUAGE`.
- Write actual narration, dialogue, and monologue in this video's `market_target.language`. A different document language must not translate or replace those lines. Preserve confirmed brand/SKU names and factual packaging text.
- Preserve machine identifiers, stable semantic material IDs, paths, and PM evidence keys exactly. For example, a localized duration label in Markdown does not rename `duration_ms` in a PM report.

For example, with French communication and English video content, write headings such as “Durée”, “Plan 1”, and “Dialogue”, while the spoken line remains “Find your everyday fit.” Keep `audio/narrator` unchanged. Do not add bilingual duplicate headings unless requested.

## Authoring Inputs and Scope

Use the actual information, creative research, Storyboard Master and this video's concrete Direction supplied in CURRENT INPUTS. Specialize the shared story into a full per-video narrative; do not merely copy the master or a sibling video's treatment.

Apply [marketing-proof-playbook.md](marketing-proof-playbook.md) to the chosen proof, [reference-action-craft.md](reference-action-craft.md) to each reference's adopted/ignored dimensions and supported action, and [performance-timing-craft.md](performance-timing-craft.md) to performance and speech budgets. Express the results in the fields below.

Describe the complete story regardless of whether storyboard images will be produced. Use stable semantic IDs such as `image/hero`, `image/product_front` and `audio/narrator` for intended material identities and roles. Describe appearance, sound, purpose and allowed creative freedom without claiming that undeclared or unprovided references are available. Do not assign tool argument positions, sandbox paths, runtime parts or model-specific constraints.

## Document Structure

Localize the template below and replace its instructional placeholders with concrete creative content. Do not copy authoring instructions or workflow notes into the finished document.

```text
# Script: Video XX

Creative purpose: {the intended marketing effect of this video}
Duration: {full finished-video duration within the accepted brief}
Ratio: {target ratio, e.g. 9:16 or 16:9}
Audio: Use narration, character dialogue, and/or character monologue as scripted, with environment sound and music; do not generate subtitles. Each speaking character has an explicit desired timbre and executes the tone, emotion, and pace defined by this video's creative direction.

Title: "..."

Exploration direction for this video:
- What this video explores:
- Key differences from the other videos:

Product and marketing information:
- Product/Brand/SKU:
- Core selling points:
- Available proof points:
- Target audience/Use case:
- Target country/region:
- Placement platform:
- Price/Offer: confirmed specifics / unconfirmed, do not mention

Semantic material usage:
- User-provided product/character/scene/prop material: stable IDs such as `image/product_front`, `image/host`, `image/kitchen`; adopted dimensions, ignored dimensions, and purpose
- Required product-state references: stable IDs, covered states, and purpose
- Desired entity references (to be fulfilled after declaration): stable IDs and purpose
- Style references: stable IDs and concrete traits
- Required derived state/continuity references: stable IDs and purpose
- Speaking-character voice roles: intended stable IDs such as `audio/narrator`; any later accepted sample may hold only that role's timbre, never its words or timing
- Material intentionally unused or represented only through written semantics:

Common requirements:
- Product/Brand/SKU:
- Target output language:
- CTA rule:
- Must stay consistent:
- Prohibited: subtitles, explanatory on-screen text, dialogue bubbles, title cards, and any unconfirmed content

Style and camera:
- Style reference (director/film/studio/art style):
- Reference traits (not just names):
- Palette:
- Lighting:
- Overall tone:
- Camera language:
- Editing rhythm:
- Sound direction:

Speaking characters and timbres:
| Semantic voice ID | Speaking character | Type | Desired timbre / existing authorized reference | Baseline tone/emotion/energy/pacing |
|---|---|---|---|---|
| audio/narrator | Narrator / character name | Narration / dialogue / monologue, multiple allowed |  |  |
| audio/character-name | Character name | Dialogue / monologue |  |  |

Rule: one recurring speaking identity maps to one semantic voice ID. When one voice is shared by multiple characters, state that this is the user-confirmed same-performer setup.

Storyboard script:

Shot 1 | {time in the finished video}
- Shot purpose:
- Shot size:
- Picture and action:
- Camera movement:
- Product presence:
- Spoken content: none / list one or more lines in order of occurrence: (1) {speaking character} | Narration / Dialogue / Monologue | {complete line}; (2) ...
- Delivery: for each numbered line above, specify tone, emotion, emphasis, and pacing; write "None" when there are no lines
- Sound effects/Music:
- Transition:

Repeat the shot block for every concrete shot in this video's story. Give the last shot its closing method and CTA. The number of blocks must match the reported blueprint shot count; no fixed default count applies. `shots` counts script shots and therefore also how many preview frames visual mode will generate: `frame N` visualizes `shot N` via the later frame spec's per-shot descriptions.

Full-video requirements:
- Use only the product facts explicitly written in this script's "Product and marketing information".
- Execute this script's storyboard strictly; do not add unconfirmed selling points, prices, offers, SKUs, channels, or proof.
- Keep only the narration, character dialogue, character monologue, environment sound, and music explicitly specified in this script; do not generate subtitles, auto captions, explanatory on-screen text, dialogue bubbles, or title cards.
- Spoken words are exactly the written lines, not the speaker labels, material IDs, or speech-type labels. Preserve speaker assignments and the delivery specified for each line.
- Text that objectively exists on product packaging in confirmed reference material may remain naturally, but the model must not rewrite or add to it.
- If the CTA channel is unconfirmed, use only a generic spoken CTA and state which speaking character delivers it; do not mention platforms, stores, live rooms, shopping carts, product cards, links, search terms, DMs, comments, QR codes, coupons, official websites, apps, or account information.
```

## Content Quality

- Populate the video's content language, country/region, audience and platform from its own `market_target`. Translate market implications into concrete casting, setting, proof, voice delivery and CTA choices without inventing product or channel facts. Do not substitute the project-wide union, conversation language or another video's target. Surface materially limiting unspecified information rather than guessing.
- Include every concrete shot needed for the full duration, with contiguous timing and no fixed default count. The document's count, duration, ratio and market must agree with the reported blueprint evidence.
- Give each shot its purpose, shot size, composition, subject action, product state/presence, camera behavior, transition, complete spoken lines, per-line delivery, music and environmental sound. Keep all needed creative meaning inside this document instead of directing its reader to another file.
- Inventory every speaking identity, including one-line or off-screen roles. Keep visual and speaking identities distinct; describe desired timbre and baseline tone, emotion, energy and pace. One recurring speaking identity has one stable voice ID; any shared-performer setup must reflect actual user intent. Voice reference words and timing never replace the authored lines and timing.
- State concrete palette, lighting, texture, contrast and mood alongside any named style reference. A famous name alone is not an actionable visual description.
- Distinguish user-provided references, desired entities, style references, product-state references and derived references. Preserve actual source identity and describe which dimensions are adopted or ignored. Do not invent a separate clean product baseline when usable product references already exist.
- A product-state reference supplements rather than replaces direct product references. Specify the SKU and confirmed views/states it constrains; do not guarantee hidden details unsupported by accepted facts. A shot-specific composition is not a canonical identity reference.
- Keep substantive product, price, offer, proof and CTA claims within accepted information. Missing facts are not creative freedom. Preserve the no-added-subtitles/text requirement unless explicitly overridden; objectively present packaging text may remain unchanged, not be translated or embellished.