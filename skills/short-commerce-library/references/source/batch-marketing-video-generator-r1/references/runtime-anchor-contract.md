
# Runtime Identity Anchors

Use for original asset materialization and lowered part inputs/results. Concrete identity anchors are production requirements, not an optional user preference. The user's facts determine their content. An `auto` fact delegates that choice; it is not an asset.

## Process-owned Requirements

The complete video_spec_definition inventory is the source of runtime_materials. Before any part_input, PM requires every declared auto object to have a concrete runtime entity, even if it is not selected by any part yet. Part membership and continuity flags do not control whether these requirements exist.

- Provided sources are reused structurally from their original paths, without duplicate evidence.
- Auto sources require one independent runtime asset within the existing user delegation. Preserve the original auto fact and do not ask for redundant subjective approval.
- Waived supplemental product references are omitted, not materialized. Characters, scenes and voices cannot be waived; no supplied file means explicit auto authority.
- Missing source evidence must be resolved at its original READY requirement.



## Materialization

Fulfill with an existing suitable file or generate within authorization only when `runtime_anchor/<project>/<video>/<round>/<kind>/<identity>` is READY.

For PM-derived `source_auto`, select within the original authorization and perform objective checks; do not ask for the same subjective choice again or claim user approval of quality. Additional paid calls need existing spending authorization or separately disclosed approval; out-of-scope creative changes need a new decision.

For voices, follow the neutral-content, supported-language, timbre-only, decoding, non-silence and three-second rules in `voice-anchor-gates.md`. Delegation skips subjective consultation/listening approval, not technical or spending checks. Visual anchors retain the baseline and market-fit rules in `asset-anchor-gates.md`, with the same narrow exception for repeated subjective approval.

Report with `provide-runtime-anchor`, never auto:

```json
{
  "path": "/absolute/runtime/narrator-v1.wav",
  "duration_ms": 3000,
  "checks": {"decodable": true, "non_silent": true, "duration": true}
}
```

`checks` must be a non-empty mapping with every value boolean true. Generated voices require measured positive integer `duration_ms == 3000`. Other anchor kinds do not need duration. Replacements use new immutable paths.

## Part Payloads

`CURRENT INPUTS` supplies the effective runtime anchors and original sources. For structural reuse, bind the original file; otherwise bind the provided runtime file. Attach images through ImageList, audio through AudioList and video references through VideoList. Semantic role controls adoption: timbre samples are not narration or music. Use the same identity-to-file binding in every applicable part.

The source requirement identifies where an anchor's content or authorization came from; its presence does not imply reuse. When the original voice is `auto`, consume that fact only as content delegation and bind the generated runtime voice file through `AudioList`. The same concrete binding applies when compiling the part input, checking its preflight, and generating its result. Only anchors assigned to this part belong in that call.

Finalize ordered media arguments before writing one-based `Image[N]` / `Audio[N]` mappings in each self-contained prompt or PromptPath file. Apply the [Image Attachment Identity Contract](payload-route-gates.md#image-attachment-identity-contract) when original or runtime image roles share a path; preserve every role under the shared position. Voice samples remain timbre-only and obey the per-call audio budget. Visual parts also attach the same-part storyboard sheet; script-only has no sheets but still requires the identity assets.

There is no single-part auto exception within lowering. If the target cannot bind a required reference, disclose the limitation and obtain an execution or creative choice; prose does not replace an anchor.

## Revisions

Before initial delivery, original runtime entities depend on their source, blueprint and execution model, never on part specs. Revise part_spec only to change selected original IDs; revise the original blueprint or definition when its actual content is wrong or incomplete. Reuse nodes are structural: revise their original source. Generated files belong to their runtime_anchor. Use erase, refresh and fresh evidence at new paths.

The full inventory is a shared preparation gate. Each actual part uses only the current material IDs selected in its part_spec. Read its narrative from the blueprint and its boundaries from the runtime manifest; no separate part-content document is required.

After delivery, handle requested edits within the current continuation_decision under [post-delivery-revision.md](post-delivery-revision.md). Do not reopen the first-generation inventory merely to edit a delivered output.