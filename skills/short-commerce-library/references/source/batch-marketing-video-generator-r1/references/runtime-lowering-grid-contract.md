
# Runtime Lowering Artifact Contract

This file defines how to prepare manifests, part specs, part sheets, and part inputs in the lowering branch. PM determines whether lowering is needed, the fixed part count, total duration, and per-part model bounds. The LLM chooses semantic cut points and each part's integer-millisecond duration within those constraints.

## Runtime Manifest

Create `_internal/runtime/video-XX/runtime-manifest.json` by reading the current video blueprint and mapping its complete ordered semantics into contiguous target parts. Choose durations around natural action, speech, and shot boundaries. Number parts `1..N` with the exact PM-specified count; each `duration_ms` must satisfy the inclusive model bounds, and their sum must exactly cover the final video. Lowering may split or slice semantics but may not add, remove, or rewrite creative meaning. If no suitable allocation fits, report the conflict rather than changing the count or silently rounding durations.

The artifact file and the PM report are different JSON contracts. Write the complete artifact first, then report its path and a duration projection; do not save the PM report as the manifest file.

### Visual Artifact File

The file passed to `compose_storyboard_sheet.py --manifest` must contain:

- `shots`: the complete non-empty storyboard row array from the accepted storyboard manifest — one row per blueprint shot with `number` consecutive 1..N, same-numbered `frame_id`, fixed `blueprint_shots` `[number]`, global timecodes, and annotations. Preserve any `replacement_image` overrides and source-image associations. Read [storyboard-grid-template.md](storyboard-grid-template.md) for the source schema. Runtime parts select or reuse source rows by `source_shot_number` (the row equals that shot's frame): a runtime part number never assumes a same-numbered shot/frame, and one shot's frame is reused across two parts when a part boundary falls inside that shot.
- `global_info` and `video_ratio`: the accepted common annotations and ratio. Keep at most three common footer sections, or include `Part Continuity` for the compositor to replace.
- `parts`: an **object** keyed by string part numbers (`"1"`, `"2"`, ...). Each value records `duration_ms` and meaningful `label`/`handoff` text. This is not the array sent to PM.
- `runtime_shots`: a non-empty array mapping source shots into the selected parts, with each slice's own annotations. This mapping, not the `parts` metadata, controls composition.

For a visual package, also derive `runtime_shots` jointly from the video blueprint and accepted complete storyboard manifest:

- Preserve the original order of source shots;
- Assign each entry a positive `part` number, with part numbers contiguous;
- Start each part's local timecodes at `00:00` and keep them contiguous;
- Include `global_timecode` for every slice: it must stay within its source shot, have the same duration as the local `timecode`, and collectively cover the source timeline without gaps or overlaps. The local end of each part must equal that part's `duration_ms`;
- If a boundary falls within a long shot, split it into slices referencing the same `source_shot_number`, without duplicating semantics or dialogue;
- Describe each part's opening state, handoff, and continuity needed by the next part.

Complete illustrative visual file: a 20-second blueprint with two source shots, a 15-second model maximum, and two parts of 15 and 5 seconds. Source shot 2 crosses the boundary, so it appears in both parts without replaying its action. This demonstrates the format, not a default shot count or allocation; use the actual accepted blueprint, frames, and PM constraints.

```json
{
  "video_ratio": "9:16",
  "shots": [
    {
      "number": 1, "frame_id": "frame/P01/01/01", "blueprint_shots": [1],
      "timecode": "00:00-00:08", "shot_size": "Medium shot",
      "visual": "The presenter holds the jacket front toward the camera.",
      "transition": "Cut to the sleeve", "audio": "Soft instrumental music", "voiceover": "None"
    },
    {
      "number": 2, "frame_id": "frame/P01/01/02", "blueprint_shots": [2],
      "timecode": "00:08-00:20", "shot_size": "Close-up",
      "visual": "The presenter slowly rolls the sleeve, then holds the finished cuff toward the camera.",
      "transition": "End on the finished cuff", "audio": "Soft instrumental music", "voiceover": "None"
    }
  ],
  "global_info": {
    "Identity": "Keep the same presenter and jacket.",
    "Style": "Soft studio light; no on-screen text."
  },
  "parts": {
    "1": {"duration_ms": 15000, "label": "Part 1 of 2", "handoff": "End with the sleeve partly rolled."},
    "2": {"duration_ms": 5000, "label": "Part 2 of 2", "handoff": "Start with the sleeve partly rolled; finish the roll and hold the cuff."}
  },
  "runtime_shots": [
    {
      "source_shot_number": 1, "part": 1,
      "timecode": "00:00-00:08", "global_timecode": "00:00-00:08",
      "shot_size": "Medium shot", "visual": "The presenter holds the jacket front toward the camera.",
      "transition": "Cut to the sleeve", "audio": "Soft instrumental music", "voiceover": "None"
    },
    {
      "source_shot_number": 2, "part": 1,
      "timecode": "00:08-00:15", "global_timecode": "00:08-00:15",
      "shot_size": "Close-up", "visual": "Begin slowly rolling the sleeve; end with the roll incomplete.",
      "transition": "Continue the unfinished roll in part 2", "audio": "Soft instrumental music", "voiceover": "None"
    },
    {
      "source_shot_number": 2, "part": 2,
      "timecode": "00:00-00:05", "global_timecode": "00:15-00:20",
      "shot_size": "Close-up", "visual": "From the partly rolled sleeve, finish the roll and hold the cuff toward the camera.",
      "transition": "End on the finished cuff", "audio": "Soft instrumental music", "voiceover": "None"
    }
  ]
}
```

### Script-only Artifact File

A script-only package does not invent frames or call the storyboard compositor. Its file can use an ordered `parts` array containing `part`, `duration_ms`, and the self-contained semantic allocation for each part. It needs no `shots`, `global_info`, or `runtime_shots`.

### PM Evidence Report

For either mode, the PM evidence contains `path` plus an ordered `parts` **array** of `{part, duration_ms}`. For a visual file, project each numerically ordered object key to integer `part` and copy its exact duration. Do not send the compositor's `parts` object as PM evidence. For the visual example above, report only while `runtime_manifest/<project>/<video>/<round>` is ready:

```bash
python3 scripts/batch_pm.py apply provide-runtime-manifest \
  --subject runtime_manifest/<project>/01/01 \
  --data-json '{"path":"/absolute/runtime-manifest.json","parts":[{"part":1,"duration_ms":15000},{"part":2,"duration_ms":5000}]}'
```



## Part Spec

Each `part_spec` uses its exact accepted runtime-manifest `duration_ms` and lists only original declared material IDs actually used by that part:

First read the current runtime manifest and video blueprint, unless their complete relevant contents are already in context. Use the definition images/audios/videos inventory and blueprint narrative in CURRENT INPUTS to match the part's visual and speaking roles to declared identities. A material ID such as `C01` or `narrator` names an entity; it is not a file path, requirement ID, or `Image[N]` / `Audio[N]` position. Concrete paths and tool positions are resolved when compiling `part_input`. Include a used voice even if its current source is `auto`; lowering will require its concrete anchor separately.

```json
{
  "duration_ms": 15000,
  "materials": {
    "images": ["SKU-A", "C01", "S01"],
    "audios": ["narrator"],
    "videos": []
  }
}
```

Never select a waived reference. Do not reference undeclared materials, mechanically copy another part's materials, or falsely claim materials are bound merely because attachment mechanisms are limited.

## Visual Part Sheets

The shared runtime_materials gate covers the full original inventory: reuse provided, materialize all auto, omit waived supplemental product references. Follow runtime-anchor-contract.md; part specs select usage, they do not create or remove original runtime entity requirements.

Visual lowering must deterministically compose a matching storyboard sheet for each part. Use the complete runtime manifest and original frame sources:

```bash
python3 scripts/compose_storyboard_sheet.py \
  --manifest /absolute/runtime-manifest.json \
  --split-by-part \
  --images /absolute/shot-01.png /absolute/shot-02.png \
  --output /absolute/storyboard-input.png
```

One invocation writes **all** mapped `storyboard-input-part-YY.png` files. Consume the returned `outputs` mapping; changing `--output` or appending `ls` for a particular part does not select that part. For Route B, supply one image per original source shot, in source order, not one per runtime slice. The compositor reuses a source frame when a shot spans parts.

Route A may instead use `--grid-images` and `--grid-shot-counts`. For the two-source-shot example above:

```bash
python3 scripts/compose_storyboard_sheet.py \
  --manifest /absolute/runtime-manifest.json \
  --split-by-part \
  --grid-images /absolute/route-a-sheet.png \
  --grid-shot-counts 2 \
  --output /absolute/storyboard-input.png
```

Grid shot counts describe valid **source rows (preview frames)** per grid, excluding filler cells; their sum must equal `len(shots)`, not the number of parts or runtime slices. Check output count, order, local timecodes against accepted durations, non-empty files, and decodability, then record each actual path through the ready `derive-part-sheet` action. Script-only lowering creates no part sheet unless another accepted hard input constraint explicitly requires one.

If composition rejects the input, inspect the actual JSON and error. A duration-only PM report is not a visual manifest; adding `shots` alone is also insufficient without common annotations and the accepted runtime mapping. Do not substitute the complete storyboard manifest or drop `--split-by-part` to bypass the failure: a full overview does not replace the same-part sheet. If the accepted runtime artifact is incomplete or wrong, follow [revision-routing.md](revision-routing.md): erase its owning fact, refresh next-action, then provide the corrected complete file at a new path when READY. Preserve valid source shots and the accepted allocation unless a legitimate revision requires changing them. Renaming the output does not repair a malformed input.

The compositor returns the part-path mapping in its command result and does not modify the accepted runtime manifest. Record each returned path immediately through its ready `part_sheet` requirement; later recovery reads those PM facts rather than looking for an `execution_hint` written into the manifest.

## Self-contained Part Inputs

Each `generation-input-part-YY.md` is compiled from the video blueprint plus the runtime manifest and part spec, runtime anchors, and optional part sheet. It must be independently executable and include:

- Part duration, ratio, and local timeline;
- All product facts, constraints, and the no-subtitle rule needed by the current part;
- Visuals, action, camera, product state, audio, speaking role, complete lines, and delivery for each local shot/slice;
- Opening state, handoff from the previous part, ending state, and continuity for the next part;
- Exact `Image[N]` / `Audio[N]` / `Video[N]` binding semantics for the current part, translated from the plan's stable semantic IDs only after final ordered media arguments are fixed;
- An explicit description of the matching part sheet in visual mode.

Do not write `same as before`, `continue previous part`, `see video-blueprint-XX.md`, semantic IDs without concrete positional mappings, or path placeholders. Follow [part-continuity.md](part-continuity.md): for each part after the first, report whether its planned transition uses the previous actual end frame. A true choice requires the extracted `last_frame` asset before this input is compiled; false uses the planned opening without a previous-result dependency. The frame cannot replace original product, character, scene, or other identity references. `part_input` is an executable mapping, not a second creative authoring step.

When `part_input/<project>/<video>/<round>/<part>` is ready, record the new path through `provide-part-input`.

### Part Input Template

This is an internal executable prompt template for `part_input`, not a section of the user-visible video blueprint. Use the exact accepted part duration and local timeline; keep the finished-video absolute range only in the runtime manifest. Preserve this video's content language and market. Populate the media mappings from the final ordered arguments under [payload-route-gates.md](payload-route-gates.md); the example voice positions are placeholders, not fixed assignments.

```text
# Runtime generation input: video XX, part YY of ZZ

Task: independently generate part YY of this finished video.
Part duration: ... seconds; this call starts timing at 00:00
Part position: part YY of ZZ; this is not a timecode
Finished-video ratio: {target ratio, e.g. 9:16 or 16:9}
Finished-video market target: {content language; country/region; audience; placement platform, unchanged for this part}

Speaking characters and timbres for this part:
| Voice reference | Speaking character | Part type | Timbre purpose |
|---|---|---|---|
| Audio[1] | {character name} | Narration / Dialogue / Monologue | Hold this character's timbre only |
| Audio[2] | {character name} | Dialogue / Monologue | Hold this character's timbre only |

Each neutral voice sample actually attached with this call is only for the timbre of its mapped character in the table. Do not repeat, transcribe, or borrow sample words, and do not reuse sample timing; the actual speakers, lines, and timing for this part come from this file, while tone, emotion, emphasis, and pacing follow this part's requirements and stay consistent with each character's confirmed baseline direction.

Part opening:
- Explicit starting state of subjects, product, scene, composition, lighting, action, and sound: ...

Continuing from the previous part:
- Part 1 writes "This part opens the finished video; there is no previous part"; later parts with use_last_frame=true state the actual extracted end-frame state to match and its exact image binding; false uses the planned transition without claiming a previous generated frame: ...

Handoff to the next part:
- The final part writes "This part closes the finished video; there is no next part"; other parts state the fixed ending frame, action trend, camera direction, and sound continuation point: ...
```

Complete this skeleton with the full part-local shot timeline, product facts and limits, style, reference usage, no-subtitle rule, complete spoken lines and delivery. Reproduce applicable creative semantics, not workflow instructions. In visual mode, add a concrete same-part storyboard reference with its actual `Image[N]` binding; script-only omits that reference, not required identity media. Include all required direct sources, product-state references, identity anchors and derived references with their actual positions. No section may delegate to another prompt or use “same as before”.

An actual previous end frame complements rather than replaces identity media and complete text. If its state differs materially, follow [revision-routing.md](revision-routing.md): a corrected executable mapping must preserve the accepted creative intent; otherwise revise the creative owner. Internal part inputs are not regular user-facing deliverables.

## Exact Payload and Preflight

Each video call attaches only the media that part actually needs. A visual split attaches the matching part sheet, not the complete overview. Script-only attaches no sheet. Bind concrete voice anchors through ordered `AudioList` under `runtime-anchor-contract.md` and the duration budget in `voice-anchor-gates.md`. Every voice used in lowering needs an asset, even when it speaks in only one part; auto is content delegation, not an attachment.

The `checks` in each `pass-part-preflight` evidence must be a non-empty set of objective results, all `true`, such as files, duration, bindings, part-sheet, continuity-frame, and audio-budget. Any wrong-part input, missing path, stale path, duration mismatch, or omitted attachment keeps that part's preflight open. Each check gates only its corresponding result; there is no shared lowering preflight depending on all part inputs.

## Revisions

These owner rules apply before initial delivery. For edits to an already delivered result, stay in the current continuation_decision under [post-delivery-revision.md](post-delivery-revision.md); do not reopen the initial graph for each revision.

When split boundaries, durations, shot membership/order, material bindings, or handoffs change, use new manifest, part-sheet, and part-input paths and satisfy affected nodes again. A generation-model change remaps these runtime artifacts while preserving the video blueprint. Purely mechanical recomposition before initial delivery does not require the user to reconfirm the complete package. Changes to the canonical story or visual meaning shared with existing frames require revising video_blueprint and its dependent visual/package artifacts first.