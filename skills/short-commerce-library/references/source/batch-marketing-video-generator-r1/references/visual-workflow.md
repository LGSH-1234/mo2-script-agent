
# Visual Workflow

## Storyboard Mode

Choose visual or script_only only when the mode node is READY, after the blueprint and all declared media requirements (including applicable product coverage) are satisfied. Both modes keep the same story and assets. Visual adds storyboard images; script_only does not. Mode does not rewrite the blueprint.

## Storyboard Image Model Fact

This question appears only after visual is selected. It selects the storyboard production route. Earlier material generation follows its own node's media guidance.


First read `<system-reminder>`:

```text
<system-reminder>
[User Setting]
- Image model: ...
</system-reminder>
```

If the latest UI-injected block contains `Image model`, report that exact value to PM with `source="system-reminder"`. Otherwise ask, in the user's communication language: "Please select an image model in the chat settings and let me know when you are done. If you are unsure, you can simply say you do not know." Do not ask the user to name, copy or transcribe the model.

Wait for the reply, then read the latest injected `Image model` setting again. The reply only tells you to check the settings; it does not supply the model fact. Use the injected value if available, even if the user is unsure. Only if the setting is still missing, report `model="unknown"` with `source="conservative-fallback"`. Do not ask repeatedly or fall back before giving the user this opportunity. `unknown` is an internal PM value, not a word the user must type.

A model name in ordinary user prose never substitutes for the injected setting. The LLM reads and reports the model; the user only selects it in the UI and notifies completion.

## Route Selection

Only the exact values `gpt_image_2`, `gpt_image_2_5_flare`, `gpt_image_2_5_sunburst`, and `seedream_5.0_pro` use Route A. Case variants, aliases, other versions, and `unknown` all use Route B.

The branch is expressed directly in the conditional-edge context from `storyboard_manifest/<project>/<video>` to each `frame/<project>/<video>/<frame-index>`. It does not create closable `route_a_template`, `route_b_frame_call`, or other intermediate task nodes.

- Route A: batch up to 9 preview frames; edge context provides `group`, `cell`, `batch_start`, and `batch_end`.
- Route B: one independent generation call per preview frame; edge context's `group` is that frame.

Both routes use `frame/<project>/<video>/<frame-index>` as the actual asset requirement. The canonical `video_blueprint/<project>/<video>` is authored before definition, material fulfillment and storyboard mode, and frames appear as `[ready]` only after the blueprint, definition, mode, the accepted `frame_spec_definition` and the storyboard model are resolved. Each frame consumes its matching entry's `visual_description` as the direct picture requirement, uses the blueprint as its canonical script context, and binds exactly that entry's `image_ids`; `provide-frame` records the actual image path.

## Route A 3x3 Contract

Every generation must describe visible content for all 9 cells. Place required cells in frame-spec order. If the final batch has fewer than 9 frames, fill its remaining cells with recognizable film-style diagnostic images.

Do not introduce concepts such as "leave blank," "empty cell," or "unused cell" to the image model. All 9 cells must contain visible images to avoid layout collapse caused by empty-space semantics.

Diagnostic cells are not frame requirements, do not enter the storyboard manifest, and must not be treated as actual shots in later video generation.

## Cardinality

Frame count equals the blueprint's `shots`: one frame per shot, `frame N` for `shot N`, made executable only after `frame_spec_definition/<project>/<video>` provides its N-entry descriptions array. Do not infer counts from Markdown rows, filenames, or directory contents, and never default to a fixed number.

## Safety Rejection

For a safety-review failure, use:

```bash
python3 scripts/batch_pm.py frame reject \
  --subject frame/<project>/<video>/<shot> \
  --reason-json '{"reason":"safety-review"}'
```

This event records only the blocker, not frame evidence. The frame remains `[ready]` and becomes the current exclusive focus. At that point:

1. Preserve the current video blueprint; do not improvise a replacement image with a different meaning;
2. Explain to the user which specific frame was blocked;
3. Ask the user to choose a retry preserving the original meaning or switch that video to `script_only`;
4. After the user authorizes a retry, use `frame retry` to clear the current rejection focus, then regenerate;
5. If the user chooses script-only, erase `storyboard_mode/<project>/<video>` with the reason and refresh next-action. Select `script_only` when that question is ready; the visual subgraph leaves the active graph.

## Presentation

When showing a storyboard, frame, or overview to the user, present the actual file through `present_sandbox_file`. You may identify observable issues such as composition, continuity, or text readability and suggest changes, but must not treat the model's subjective judgment as user confirmation.