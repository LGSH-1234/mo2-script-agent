
# Conditional Part Continuity

Each lowered part has its own `part_input`, `part_preflight`, and `part_result`. For every part after the first, PM also requires a `continuity_choice`. Decide this process choice yourself from the accepted video blueprint, runtime manifest and adjacent part specs. Read the complete relevant narrative and boundary mapping before deciding the opening/ending handoff. No new user confirmation is needed for a choice that preserves the accepted content.

## Choice

Report `use_last_frame: true` when the transition should match the previous generated part's actual final composition, pose, object placement, or action state. Report `false` for an independent cut where the planned opening and existing identity references are sufficient. Include a concrete `reason`. This choice concerns an actual generated end frame; it does not waive any storyboard sheet or required identity asset.

Decide from the planned transition before generating the previous part. An unanswered choice keeps the conditional dependency unknown; it is not a default false. The first part has no such choice. Example evidence for `report-continuity-choice`:

```json
{"use_last_frame": true, "reason": "The next slice continues the same hand movement and camera composition"}
```

When false, the part input has no dependency on the previous generated result. When true, PM requires `last_frame` of the preceding part before the next input can be provided. Multiple READY parts are independent unless the active graph connects them; their numeric order alone does not establish an execution dependency.

## Actual Last Frame

At a READY `last_frame/<project>/<video>/<round>/<source-part>`, extract the final decodable frame from the exact current `part_result` video in CURRENT INPUTS, using an available video-processing tool or a local decoder such as FFmpeg. Write a new immutable image path and verify existence and decodability. Do not redraw it, select a planned storyboard frame, or invent a substitute. Record `{"path":"/absolute/part-01-last-frame-v01.png"}` through `provide-last-frame`.

The `frame-extraction.input_video` INPUT USE names the source role, not a new tool. Supply that source video to the actual extraction tool available in the runtime.

## Executable Input and Local Preflight

When the following `part_input` becomes READY, read the video blueprint and its boundary mapping. For a true choice, include the listed last-frame image in that call's ordered `ImageList`, give it an exact one-based `Image[N]` reference, and describe the matching starting state in the new executable prompt. It complements the required product/entity anchors and visual part sheet. For false, use the planned handoff and do not claim access to a previous generated frame.

At `part_preflight/<project>/<video>/<round>/<part>`, check that part's current executable prompt, duration, media mapping, required assets, optional storyboard sheet, selected last frame, and audio budget. Record a non-empty all-true `checks` map via `pass-part-preflight`. This gates only the corresponding result. Direct execution continues to use `pass-preflight` on its direct `preflight` node.

## Revisions

The following applies before initial delivery. After delivery, use the open continuation node under [post-delivery-revision.md](post-delivery-revision.md), without reopening the original generation chain merely for an edit.

To change the process choice, erase its `continuity_choice`, refresh next-action, and report a new decision when READY. To correct a frame extraction, revise `last_frame`; to change only executable wording or media positions, revise `part_input`. Never edit accepted paths in place. These changes invalidate that part's input/preflight/result and consumers that actually depend on it, while preserving the preceding result. Switching to false removes the last-frame dependency; any historical frame is no longer current input merely because its file still exists.

Replacing a previous result invalidates its extracted frame and following parts that selected it. Independent false-branch parts keep their facts. If the generated end state cannot support the confirmed next scene without changing creative meaning, follow `revision-routing.md` for the creative owner before continuing; the continuity choice does not grant permission to rewrite the story.