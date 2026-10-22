---
name: "ugc-random-art-duan-shi-pin"
description: "将角色送入随机艺术风格空间，并设计一段视觉风格各异的15秒短视频。"
display_name: "Random Art 短视频"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
video_model: "Seedance_2.5"
image_model: "seedream_5.0_pro"
---

# Random Art Portal Theater

Randomness is part of the product promise. This package contains no scripts or executable files. Use the bundled 60-card style deck and the reproducible draw rule below; never pretend the result came from an external random service.

## Check the character asset

Extract a character identity lock: face, silhouette, hair, outfit, palette, accessories, proportions, outline, and non-negotiable IP marks. Classify the asset as full body, half body, portrait, layered, or flat. Use a portrait-safe story if legs, hands, or costume details are unavailable.

Read [continuity-locks.md](references/continuity-locks.md). Separate immutable identity geometry from style-adaptable surface treatment. The chosen movement may change line, shading, pigment, texture, and environmental light, but it must not change facial geometry, hairstyle structure, proportions, outfit design, accessories, or signature marks.

## Select the art space

Perform the draw without code:

1. Before opening the style deck, use the user's integer seed or commit to a six-digit model-generated creative seed. Normalize negative values and preserve leading zeroes for display.
2. Calculate `remainder = seed mod 60` and `style number = remainder + 1`.
3. Verify the arithmetic in the receipt as `seed = 60 × quotient + remainder`.
4. Only now read the exact numbered card in [style-deck.md](references/style-deck.md). Do not swap it for a preferred style.
5. Calculate `mode number = (quotient mod 12) + 1` and select the matching A–L pattern in [action-and-camera-patterns.md](references/action-and-camera-patterns.md).

The deck contains 60 character-compatible movements with self-contained visual layers, transition grammar, and world rules; the skill does not depend on the user's local vault at runtime. Example: `450010 = 60 × 7500 + 10`, so seed `450010` selects card `11`; `7500 mod 12 = 0`, so it selects mode `1/A`, Impact Battle.

Tell the user: `本次为创作型伪随机抽取：Seed <seed>；<seed> = 60 × <quotient> + <remainder>；命中风格 <number>「<movement>」；动作模式 <mode number>「<pattern>」。` This is reproducible creative pseudorandomness, not cryptographic randomness.

For a reroll, use `new seed = (previous seed + 104729) mod 1000000`, recalculate, and retain both receipts. If a selected movement conflicts with the asset or a recent exclusion, reroll at most three times; disclose every rejected result and reason. Never silently substitute a movement.

If the local art vault is available, it may enrich the selected card, but the bundled card remains authoritative and sufficient. Any added layers must be conflict-checked and must not change the disclosed selection.

## Resolve style conflicts

Read [portal-grammar.md](references/portal-grammar.md). Keep the character's identity and shape language locked while the environment, material, light, color, and camera adopt the selected movement.

Check negative-prompt conflicts before generation. Remove any negative term that forbids the character, its required material, or the selected transition. If the chosen movement cannot support a readable character even after conflict repair, use the deterministic reroll rule above and disclose the rejected movement and reason.

## Design a varied 15-second mini theater

Read [action-and-camera-patterns.md](references/action-and-camera-patterns.md). Use the mode derived from the seed when it fits the asset. If the asset cannot support it, advance cyclically to the next compatible pattern and disclose the original mode, replacement mode and limitation. Modes include physical comedy, intense non-graphic battle, chase, dance, puzzle, stealth, sport, rescue, transformation, ritual performance, object encounter and reality glitch.

Do not force every result into the same five beats. Use a pattern appropriate to the action and selected movement. A result normally contains 5–7 shots, at least four distinct shot sizes or angles, one motivated transition, and one clearly held final image. Vary among macro detail, extreme close-up, medium action, wide geography, low angle, overhead, POV, tracking, arc, crane, snap pan, rack focus, locked tableau, and style-native split panels. Every cut must reveal new action, space, scale, or consequence.

Keep the art-space sequence governed by one visual cause-and-effect, at most two locations, one world rule, and one carried-back motif. The threshold must be native to the selected movement; avoid generic glowing portals.

For battle mode, make intensity come from speed changes, readable attack-and-counterattack, environmental reaction, strong impacts, rapid spatial reversals, camera acceleration, and a decisive non-lethal finish. Use 6–7 shots, establish both sides before close combat, keep the user's face readable in at least two shots, and avoid gore, injury detail, cruelty, or chaotic limb overlap. The opponent may be a style-native construct, shadow, creature, or abstract force, but must not resemble a real person unless supplied and authorized.

For battle mode, read [battle-example.md](references/battle-example.md) as a specificity and pacing reference. Replace its Surrealist world, opponent and actions with the selected card's own light, medium, spatial rule and transition; never reuse the example as a fixed story template.

Write one production-ready, tool-neutral 15-second prompt with exact time ranges, shot size, camera move, character action, style behavior, environmental response, transition, sound cue, and continuity locks. It must be more specific than a plot summary and must fit entirely within 15 seconds.

## Return or generate

Deliver:

1. draw receipt: seed, quotient, remainder, numbered result, category, and any rejected movement
2. character identity lock and asset limitations
3. selected style card and style-lock sentence
4. selected action mode, camera pattern, and one-sentence mini-theater premise
5. timecoded 5–7-shot plan
6. one self-contained 15-second generation prompt plus negative-conflict cleanup
7. continuity anchors for the character, selected style, opponent if present, and carried-back motif
8. sound and impact cue line
9. QA using [quality-gates.md](references/quality-gates.md)

Generate with available media tools when requested. Otherwise return prompts that keep the random choice and seed explicit. Do not request, create, or execute helper scripts as part of this skill.
