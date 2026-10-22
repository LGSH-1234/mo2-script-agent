
> **Node knowledge:** This reference defines single-frame image generation semantics for Route B. PM next-action identifies the ready frame; for Route A, read `grid-prompt-template.md`.

# Storyboard Frame Generation

Use this reference for one-image-per-frame storyboard material. A raw frame image is internal material, not the user-facing storyboard overview. The later READY overview node instructs the LLM to compose frame sources into `storyboard-grid-XX.png`; `storyboard-grid-template.md` owns that composition.

Before the first image call, apply `external-knowledge.md`, load the complete applicable `image_generate` knowledge, and read the current `video_blueprint` path listed under this frame's `CURRENT INPUTS`. Reload knowledge later only when the applicable content is absent, partial, or uncertain.

## Non-Negotiable Boundary

Image models generate only the visual frame in the target video ratio. They must not generate shot numbers, timecodes, annotations, subtitles, dialogue bubbles, technical labels, info panels, watermarks, or other added text.

Every identifiable on-screen character must have an accepted visual anchor before the frame containing that character is generated. Reuse a usable user-provided image directly; otherwise use the exact character's accepted canonical anchor. A prose description or a prior storyboard frame does not satisfy this gate.

Before each raw-frame call, take the matching entry of the accepted `frame_spec_definition` — its `visual_description` is the direct picture requirement — and read the video blueprint for the shot's full action, dialogue context, timing and continuity (frame N addresses shot N). Bind exactly that entry's `image_ids` through the frame's `INPUT USE` lines into the actual `sandbox_generate_image.ImageList`; semantic IDs are not tool attachments and must be translated to that call's one-based `Image[N]` mappings. If projection reveals a genuinely new visible product angle/state, stop and revise the frame spec (and its owners when the story changed) so that the missing requirement becomes explicit before continuing.

## Route B: One Image Per Frame

Read this video's `video_blueprint/<project>/<video>.market_target` from `CURRENT INPUTS`. Apply its accepted audience and market treatment through the frame's actual casting, setting and styling, preserving established anchors and product facts. Do not borrow another video's target or add visible text to express the content language.

Use this route when PM records Route B. This is mandatory for `seedream_5.0`, every other non-Route-A identifier, ambiguous labels, and absent disclosure.

- Generate exactly one no-text image per shot; each call produces that shot's preview frame.
- Set `OutputRatio` to a schema-supported value. Use the exact target video ratio when supported; otherwise choose the closest supported same-orientation value, describe the intended target framing in Prompt, and let PM normalize deterministically before composition.
- Keep ordered immutable names such as `_internal/storyboard-01/frame-01.png` through `frame-NN.png`.
- On every frame call, reattach the declared `image_ids` of that frame-spec entry. Independent calls are stateless; never rely on references sent to a prior frame.
- A usable user-provided product or entity image is already the direct reference; never generate a cleaner duplicate. Apply placement, interaction, opening, pouring, damage, occupancy, and other changing states only in the storyboard-frame prompt. If an altered state must persist, store it separately under `assets/anchors/derived-states/` without replacing the canonical anchor.
- Repeat the accepted direct references, product state references, anchors, style sources, and relevant derived-state references declared for this frame in every prompt. A previous prompt, filename, or phrase such as `same as before` does not carry context into an independent call.
- Keep each prompt focused on one preview frame and preserve its accepted frame-spec meaning. Do not ask a weak multi-panel model to create a grid or use frame generation to rewrite the plan.
- If the model cannot accept a required reference image, block the call under `payload-route-gates.md`; generic risk acceptance never substitutes for required character, scene, or product pixels.
- Reject and regenerate any individual frame containing unwanted model-rendered labels, subtitles, or stray text before composition.
- If the generation tool itself rejects the request through safety review, do not rewrite the prompt, alter confirmed meaning, invent a substitute, skip the shot, or continue a different frame. Record `frame reject --subject frame/<project>/XX/YY --reason-json '{"reason":"safety-review"}'`. PM keeps that frame ready and exclusive. After the user chooses a meaning-preserving retry, call `frame retry`; if the user chooses script-only, erase `storyboard_mode/<project>/<video>` with the reason, refresh next-action, and select `script_only` through its typed action when ready.

Model-facing prompt shape:

```text
Reference image notes: Image[1] ({object, source, view/state, purpose, features to preserve}); ...; Image[N] ({semantic information}).

Generate one text-free individual preview-frame image at {target video ratio}; this is frame {frame index} of {total frames in the accepted frame spec}, covering blueprint shots {covered shot numbers}. Picture content: {subjects, environment, shot size, composition, action, camera intent, product presence, and required states, stating which Image[N] images preserve what}. Strictly preserve product appearance, packaging, Logo, SKU, character identity, wardrobe, scene structure, key props, style, palette, and lighting per the relevant Image[N] images. The image must not contain shot numbers, timecodes, titles, subtitles, dialogue bubbles, annotations, info panels, watermarks, or other added text; do not add unconfirmed prices, selling points, claims, or CTAs.
```

## Source Progress

Read `storyboard-source-contract.md` before the first frame call and when resuming raw generation. Record each completed ready frame through PM immediately. Complete raw coverage is required before composition readiness, but it is never completion of the user-facing storyboard; compose deterministically under `storyboard-grid-template.md` when PM exposes the manifest/overview nodes.