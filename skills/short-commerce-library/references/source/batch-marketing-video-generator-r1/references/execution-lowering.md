
# Execution and Runtime Lowering

## Model Fact Before Branching

`generation_model/<project>/<video>/<round>` must become ready and receive its fact before the PM materializes the direct or lowering subgraph. Do not call the legacy capability command first or let the LLM report `direct-supported` or `max-duration` independently.

Read the exact model from this system reminder:

```text
<system-reminder>
[User Setting]
- Video model: Seedance_2.5
- Supported duration per generated video: 4-30 seconds
- Aspect ratio: 9:16
</system-reminder>
```

If the latest UI-injected block contains `Video model`, report that exact value to PM with `source="system-reminder"`. Otherwise ask, in the user's communication language: "Please select a video model in the chat settings and let me know when you are done. If you are unsure, you can simply say you do not know." Do not ask the user to name, copy or transcribe the model.

Wait for the reply, then read the latest injected `Video model` setting again. The reply only tells you to check the settings; it does not supply the model fact. Use the injected value if available, even if the user is unsure. Only if the setting is still missing, report `model="unknown"` with `source="conservative-fallback"`. Do not ask repeatedly or fall back before giving the user this opportunity. `unknown` is an internal PM value, not a word the user must type.

A model name in ordinary user prose never substitutes for the injected setting. The LLM reads and reports the model; the user only selects it in the UI and notifies completion.

## PM-owned Capability

The PM determines the model family through fuzzy matching:

- Contains both `seedance` and `2.5`: `[4000, 30000]ms` per part;
- Contains both `seedance` and `2.0`: `[4000, 15000]ms` per part;
- Other or unknown: conservatively use `[4000, 15000]ms`.

If video_blueprint's `duration_ms` does not exceed the family's maximum, use direct; otherwise use lowering. The LLM does not report this decision or the part count.

## Mapping Invariant

`video_blueprint` is the single model-independent creative source. Neither branch executes it directly:

- Direct means one-to-one compilation: `direct_payload` reads the complete plan, resolves current concrete materials and the visual overview when applicable, assigns final media positions, and writes one self-contained executable prompt/payload.
- Lowering means one-to-many compilation: `runtime_manifest` maps the complete plan into contiguous semantic parts, then each `part_input` resolves that part's concrete anchors, optional part sheet, and final media positions into one self-contained executable prompt.

Do not use `video-blueprint-XX.md` as `sandbox_generate_video.PromptPath`. A target model change remaps the same accepted plan; it does not authorize rewriting creative meaning.

## PM Constraints and Semantic Partition

The lowering part count is:

```text
ceil(video_duration_ms / model_max_duration_ms)
```

Allow at most 64 parts. PM supplies the fixed count, total duration, and inclusive per-part model bounds; it does not allocate durations. Read the video blueprint and choose natural boundaries around complete speech, action beats, and shot transitions. A long shot may span parts when necessary, preserving its meaning and continuity. Do not mechanically equalize durations or choose additional parts.

The 15-second, 9-shot example in `evidence-and-commands.md` fits a 15000ms model maximum and uses the direct route; shot count alone does not require splitting.

Report integer-millisecond durations in an ordered `parts` array numbered `1..N`. PM checks exactly N parts, each within the model's limits, with their sum exactly equal to video_blueprint's duration. The following is **PM evidence (`--data-json`), not the contents of the artifact at `path`**. To illustrate lowering separately, a 20000ms video with a 15000ms maximum needs two parts and can use this allocation. This is a calculation example, not a default or recommended finished-video duration:

```json
{
  "path": ".../runtime-manifest.json",
  "parts": [
    {"part": 1, "duration_ms": 12000},
    {"part": 2, "duration_ms": 8000}
  ]
}
```

Before reporting, write the actual file using [runtime-lowering-grid-contract.md](runtime-lowering-grid-contract.md). Visual files require source `shots`, common annotations, and `runtime_shots` with per-part local/global timecodes; their `parts` is an object keyed by part number. Project its durations into the PM evidence array shown above. Script-only files do not go to the compositor. A duration-only report must never be used as a visual compositor input.

The manifest file and submitted evidence must describe the same allocation, not have identical JSON shapes. Once accepted, that manifest is the duration source: each `part_spec.duration_ms` must equal its corresponding manifest part. Later inputs, sheets, preflight, and calls preserve those boundaries. Change an allocation by revising the manifest at a new path, not by silently changing a part spec or rounding a tool duration.

If no suitable semantic partition fits the fixed count and limits, report the conflict and obtain a legitimate model or creative revision through the current PM workflow. Do not invent a different count, bypass mapping, or rewrite the accepted story. Arithmetic validation does not certify the quality of semantic cuts or audit media calls.

## Lowering Graph

```text
delivery/<project>/<video>/<round>
└── assembled_result/<project>/<video>/<round>
    ├── part_result/<project>/<video>/<round>/01
    ├── part_result/<project>/<video>/<round>/02
    └── ...

part_result/<project>/<video>/<round>/N
└── part_preflight/N
    ├── generation_model
    └── part_input/N
        ├── runtime_manifest
        ├── runtime_materials                   # full original inventory; auto → concrete
        ├── part_spec                           # final per-part ID selection
        ├── continuity_choice/N                 # N > 1; LLM reports true or false
        ├── [choice=true] last_frame/N-1
        │   └── part_result/N-1
        ├── video_blueprint
        ├── concrete selected media             # original provided or materialized auto
        └── part_sheet                          # visual only

runtime_manifest
├── confirmed package
├── generation_model
├── video_blueprint
└── storyboard_manifest                          # visual only
```

For N > 1, the LLM reports a planned `continuity_choice/N`; PM evaluates a conditional dependency from `part_input/N` to `last_frame/N-1` only when true. The extracted frame depends on the actual previous result. Unknown keeps the choice reachable and the input unresolved; false removes the previous-result dependency. Follow `part-continuity.md`. Every part has its own preflight, so revising a later executable input preserves earlier results. Part numbers alone do not imply an execution dependency.

Before any part input, runtime_materials completes the entire original inventory: reuse provided sources, materialize every auto, and omit waived supplemental references. Original auto facts stay unchanged; original runtime entities do not depend on part specs. Part specs select original IDs from the blueprint and manifest; no independent content or missing-object assessment is required. Both visual and script-only lowering use this layer; direct execution does not. See runtime-anchor-contract.md.

Each part input must be compiled from the current video blueprint and self-contained. It translates stable semantic material IDs into that call's actual one-based media mappings; it does not create a parallel script. If the execution environment cannot bind a required reference type, disclose that limitation and obtain an execution or creative choice; merely expressing identity in prose does not replace the required asset. Do not claim that the underlying video API has bound fields it does not support.

## Direct Graph

The direct path is:

```text
delivery
└── direct_result
    └── preflight
        ├── generation_model
        └── direct_payload
            ├── confirmed package
            ├── generation_model
            ├── video_blueprint
            ├── concrete materials
            └── storyboard_overview              # visual only
```

Both the direct payload and lowering manifest must be based on the package already presented to and confirmed by the user. Direct still creates a new executable prompt/payload with final mappings; it never aliases the video blueprint path.

## Delivery

After this initial delivery, the READY continuation_decision hosts free-form edits and repeated presentations under [post-delivery-revision.md](post-delivery-revision.md); do not restart the generation graph for each requested edit.

Record `presented` evidence for `delivery` only after presenting the actual result file through `present_sandbox_file`. The model may report objective checks such as file existence, duration, resolution, and audio tracks, and may suggest changes. It must not claim to have confirmed visual, timbre, or overall aesthetic quality on the user's behalf.