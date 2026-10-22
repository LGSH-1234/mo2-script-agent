
# Per-shot Visual Descriptions (frame_spec_definition)

> **Node knowledge:** This reference defines how to author the `frames` array reported through `provide-frame-spec-definition`. It is fixed processing knowledge — no per-project Markdown artifact is produced or read for this node.

## One Shot, One Frame

`video_blueprint.shots = N` is authoritative for both the script's shot count and the number of preview frames. In visual mode you must declare exactly N entries: `frame 1` corresponds to `shot 1`, `frame 2` to `shot 2`, and so on — consecutive, complete, and never reordered, padded or truncated.

A frame expresses one representative static instant of its shot: the frozen moment that best pre-visualizes that shot's screen result. The complete action, dialogue, duration and transitions stay in the blueprint; do not treat the still composition as a demand that the whole shot be static.

## Evidence Schema

Report the structured array directly while `frame_spec_definition/<project>/<video>` is READY:

```bash
python3 scripts/batch_pm.py apply provide-frame-spec-definition \
  --subject frame_spec_definition/<project>/<video> \
  --data-json '{"frames":[{"frame":1,"visual_description":"The host, jacket on, turns three-quarters toward the key light with the hem flaring; the silhouette reads clearly against the studio backdrop.","image_ids":["HOST","JACKET"]},{"frame":2,"visual_description":"...","image_ids":["HOST"]}]}'
```

Each entry contains exactly:

- `frame`: strict integer equal to its one-based position (`1..N`).
- `visual_description`: non-empty text in `COMMUNICATION LANGUAGE` describing the frozen instant — subjects and their poses, product presence and state, scene, composition and shot size, camera intent, necessary continuity with adjacent frames, and prohibitions. This text is stored in the event payload and is the direct picture requirement for the later frame generation.
- `image_ids`: unique stable semantic IDs declared in this video's `video_spec_definition.images` — the only image references bound to that frame. May be empty when the frame needs no identity references. Never file paths, `Image[N]` positions, audio/video IDs, or undeclared identities.

The payload top level contains exactly `frames`. Old `path`, `blueprint_shots` or count fields are rejected without an event.

## Authoring Guidance

- Read the blueprint fully first. Derive each description from that shot's purpose, action, camera and product state rather than inventing a parallel story.
- Choose the instant that carries the shot's meaning: the moment of demonstration, the reaction beat, the product reveal. Keep adjacent frames visually continuous (same identities, wardrobe, scene, style, palette, lighting) per the blueprint's common requirements.
- Respect anchor gates: every on-screen identity with a declared image reference must appear in that frame's `image_ids`; a frame whose shot introduces no bound identity may list none.
- PM validates structure, numbering, length and ID references only. Whether the description is faithful to the blueprint is judged against this guidance and the blueprint itself, not re-audited by PM.

## Revision Semantics

A description change to any entry revises the whole definition: erase `frame_spec_definition/<project>/<video>`, refresh next-action, and provide the complete new N-entry array. This intentionally invalidates all frames, the storyboard manifest, overview, package confirmation and execution mappings while preserving the blueprint, media definition and material facts. A single unsatisfactory rendered frame is revised by erasing only that `frame` fact.