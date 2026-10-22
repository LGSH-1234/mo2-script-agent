
# Storyboard Sheet Composition

This file defines semantic formats and deterministic composition methods for the `storyboard_manifest` and `storyboard_overview` nodes. The PM determines readiness and stores typed evidence. The LLM reads the current video blueprint and accepted frame sources, writes a faithful manifest projection, calls the compositor, checks the result, and then reports each node separately.

The user-visible visual deliverable is the complete annotated storyboard overview, such as `storyboard-grid-01.png`. A raw frame or unannotated 3×3 contact sheet is not this deliverable.

## Semantic Manifest

Use UTF-8 JSON:

```json
{
  "video_ratio": "9:16",
  "shots": [
    {
      "number": 1,
      "frame_id": "frame/P01/01/01",
      "blueprint_shots": [1],
      "timecode": "00:00-00:02",
      "shot_size": "Full shot",
      "purpose": "Establish the setting",
      "visual": "Complete picture description",
      "action": "Subject action; empty only when absent",
      "product": "Product presence and state; empty only when absent",
      "camera": "Camera movement; empty only when absent",
      "transition": "Transition or handoff",
      "audio": "Environment and music",
      "voiceover": "Speaker | Narration/Dialogue/Monologue | complete line"
    }
  ],
  "global_info": {
    "Characters and consistency": "Identities and features that must remain stable",
    "Visuals and mood": "Style, palette, lighting, texture, and pacing",
    "Technical specs": "Shot count, duration, ratio, and no-subtitle rule"
  }
}
```

Required fields are `timecode`, `shot_size`, `visual`, `transition`, `audio`, and `voiceover`, plus the row identity `frame_id` and its fixed `blueprint_shots` (`[number]`). `purpose`, `action`, `product`, and `camera` are useful optional fields. `voiceover` describes spoken audio only; use `None` for a silent row and `; ` between several lines. It never specifies screen text or subtitles.

The `shots` transport key carries one storyboard row per blueprint shot, aligned one-to-one with the accepted `frame_spec_definition`: `number` is strictly consecutive `1..N` in shot order, `frame_id` references the same-numbered frame, and `blueprint_shots` is fixed to `[number]` (no many-to-many mapping). Every annotation must project that blueprint shot and its frame's `visual_description` basis and remain consistent with VideoSpec and the accepted frame; the manifest must not invent, simplify, or reinterpret creative meaning. Save to a new immutable path, then record the manifest only while `storyboard_manifest/<project>/<video>` is ready:

```bash
python3 scripts/batch_pm.py apply provide-storyboard-manifest \
  --subject storyboard_manifest/<project>/<video> \
  --data-json '{"path":"/absolute/_internal/storyboard-sheet-01.json"}'
```

## Deterministic Composition

Use `scripts/compose_storyboard_sheet.py`; do not ask an image model to redraw annotations or hand-assemble an approximation.

Route B uses ordered individual images:

```bash
python3 scripts/compose_storyboard_sheet.py \
  --manifest /absolute/_internal/storyboard-sheet-01.json \
  --images /absolute/shot-01.png /absolute/shot-02.png \
  --output /absolute/storyboard-grid-01.png
```

Route A uses ordered raw 3×3 sheets and the number of real preview-frame cells in each sheet. Diagnostic tail cells are excluded by `--grid-shot-counts`:

```bash
python3 scripts/compose_storyboard_sheet.py \
  --manifest /absolute/_internal/storyboard-sheet-01.json \
  --grid-images /absolute/route-a-sheet-01.png /absolute/route-a-sheet-02.png \
  --grid-shot-counts 9 3 \
  --output /absolute/storyboard-grid-01.png
```

Verify exit status, non-empty output, decodability, output shot count/order, annotations and source mapping. The output path must be new; never overwrite the accepted source or a previous overview. When `storyboard_overview/<project>/<video>` is ready, record the verified compositor output:

The compositor returns an `execution_hint` in its command result but never writes it into the accepted manifest. Treat the manifest as an immutable input snapshot. Recovery uses the recorded `storyboard_overview` or `part_sheet` facts, not a mutable hint inside that file.

```bash
python3 scripts/batch_pm.py apply derive-storyboard-overview \
  --subject storyboard_overview/<project>/<video> \
  --data-json '{"path":"/absolute/storyboard-grid-01.png"}'
```

## Revisions

A semantic annotation change requires revising the video blueprint first, then a new manifest path and new composed output. A meaning-preserving frame replacement keeps the plan, writes a new manifest/output version using the replacement source, and recomposes. Technical composition success is not package approval; present both the video blueprint and actual overview at the later package confirmation gate.

For runtime lowering, `--split-by-part` creates one same-part overview per call from `runtime_shots` or part-tagged shots. Read `runtime-lowering-grid-contract.md` before producing those internal sheets.