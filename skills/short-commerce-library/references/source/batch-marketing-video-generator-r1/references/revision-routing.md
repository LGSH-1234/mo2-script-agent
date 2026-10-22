
> **Node knowledge:** First distinguish editing a delivered output from correcting an accepted workflow fact. Never edit the event store directly.

# Revision Routing

## Delivered Output or Workflow Fact

When the current READY node is continuation_decision and the user wants to edit a delivered video, follow [post-delivery-revision.md](post-delivery-revision.md). Keep that node open, work with new files, and do not erase the initial blueprint, materials or delivery merely for that edit. The owner rules below apply to corrections within the structured generation workflow, not to every post-delivery change.

## Recovery First

After context compaction, tool failure, a retry, or a thread change, first call `project get-next-action`, then query the relevant READY requirement IDs. Read the recent project memos from that complete detail for recovery hints, then restore only the references and project facts named by the envelope whose contents are incomplete in the current context. Do not infer current state from filenames, chat memory, or old summaries.

A memo is not bound to a node; its message describes its subject. It is not a fact, user authorization, tool result, or completion evidence. Before recovery, verify it against the current active graph, PM facts, actual files, and tool state. A memo saying "complete" does not justify reporting the corresponding requirement as complete.

Keep historical files immutable. Before changing an accepted owner, call `erase --subject <owner> --reason '<change>'`, then `project get-next-action`. Use a new versioned path for edits, replacements, regeneration, or recomposition, and report through the owner's typed action only when it is ready. There is no direct-overwrite exception for selectors, assets, or artifacts.

If PM already exposes a downstream node as ready after an upstream change, no extra erase is required. Verify or redo the work against `CURRENT INPUTS`. `HISTORY` and memos can help find previous work but do not supply current confirmation or authorization. Never bulk-copy old facts to refill the workflow.

In the owner list below, “revise” always means this erase-and-ready protocol for an accepted fact. If work has not yet been accepted, keep the current ready node open and correct it before providing evidence.

## Semantic Owner

- Product facts, campaign-wide allowed/fixed markets, audiences, platforms, content language, planned total, asset identity, or CTA boundaries change: revise `information_understanding/<project>`, then present and confirm the corresponding file again.
- Shared story beats, shot count, order, timing, or speaking intent change: revise `story_master/<project>`; do not hide a StoryMaster change by editing only a downstream script.
- A batch direction's market/audience/language/platform selection, hook, proof, character relationships, or scene intent change within the accepted campaign scope: revise the corresponding direction in `direction_set/<project>`.
- A video's storyboard coverage changes between visual and script-only: revise `storyboard_mode/<project>/<video>` so conditional edges naturally add or remove the visual subgraph, including its frame spec, frames, manifest and overview.
- A video's materialized `market_target`, story, timing, shot count or creative roles need correction within unchanged upstream intent: revise `video_blueprint/<project>/<video>`. A change to upstream scope or Direction must first revise that actual owner.
- The media declaration misrepresents an unchanged blueprint (IDs, descriptions, permitted resolutions or process constraints): revise `video_spec_definition/<project>/<video>`. Do not use definition to change story intent or introduce a second shot mapping.
- Accepted product images change without changing the VideoSpec identity/state requirements: revise the corresponding `image/<project>/<video>/<id>` fact. PM then reopens `product_state_coverage/<project>/<video>`; re-audit every declared product and record fresh coverage before re-answering the storyboard-mode question. If the planned required state itself changes, revise video_blueprint and then its definition.
- An accepted declared material is replaced: erase its own requirement, refresh focus, and report the new path through the matching `provide-image/audio/video` action when ready; do not substitute one material type for another. A file replacement does not invalidate its upstream blueprint or definition; follow the reopened coverage, mode, visual/package and execution nodes.
- A generated frame is replaced for safety or rendering quality without changing the preview plan: revise only that `frame` fact. The frame spec, video blueprint and sibling frames remain current; PM reopens the manifest, overview, confirmation, and executable mappings. If the requested change alters a shot's visual_description or its image identities, revise `frame_spec_definition/<project>/<video>` with the complete new N-entry array instead of editing individual frames.
- A frame fails safety review: use `frame reject`, then follow PM focus to ask the user to choose a safe retry preserving the meaning or a switch to script-only. Do not freely rewrite the meaning and treat the result as the original frame.
- Storyboard source mappings or purely presentational annotations change without changing shot meaning: revise the manifest and deterministically recompose the overview. A semantic annotation change belongs to `video_blueprint` first; a change to a shot's representative instant or per-frame material selection belongs to `frame_spec_definition` first. Unchanged raw frames do not imply that the old overview remains valid.
- One video's script wording, delivery, shot action, camera, sound, timing, or semantic material role changes within unchanged StoryMaster/Direction intent: revise `video_blueprint/<project>/<video>` at a new path. PM then invalidates frames, manifest, overview, package confirmation, and executable mappings. If the change affects StoryMaster or Direction, revise that actual upstream owner first.
- Only final `Image[N]` / `Audio[N]` / `Video[N]`, model-specific wording, PromptPath, or ordered tool arguments change: preserve `video_blueprint` and revise `direct_payload` or the affected `part_input`. A generation-model change likewise remaps execution artifacts without rewriting the plan.
- Runtime semantic splits, part boundaries, or local prompts change: revise the runtime manifest / part spec / part input and regenerate affected part sheets, preflight checks, and results. Lowering alone must not change the accepted creative meaning.
- Previous-end-frame process choice changes: revise `continuity_choice/<project>/<video>/<round>/<part>`; extraction changes: revise its source `last_frame`; only final binding changes: revise that `part_input`. Per-part preflight limits invalidation to the changed part and its actual consumers, preserving earlier results. Follow `part-continuity.md` for true/false branch behavior.

## Confirmation and Authorization

Original runtime entity requirements come from the entire video_spec_definition, not part membership. Before initial delivery, revise part_spec to change selected IDs; correct the blueprint or definition when those original declarations are wrong. Generated files belong to runtime_anchor/<project>/<video>/<round>/<kind>/<identity>. Reuse nodes are structural: revise their original source. Original runtime entities survive downstream binding-only revisions. Follow runtime-anchor-contract.md and refresh affected consumers using current facts.

For a Route B meaning-preserving frame correction, erase that frame alone; unaffected sibling frames and the video blueprint remain accepted. If a Route A correction regenerates a shared 3x3 source sheet, erase every accepted frame backed by that source before generating its replacement. Follow the returned group and register each ready frame's new source path. Do not silently change a source shared by other accepted frames or reuse their old confirmation. Recompose the manifest/overview from the unchanged plan when those downstream nodes become ready.

After any user-visible package content changes, present the affected actual files again and obtain new package confirmation. Package confirmation is not execution authorization; a package revision invalidates the old execution scope, payload, and preflight. Purely mechanical retries during execution still use new output paths and report the actual terminal state through the current ready result node.

If a requested change would alter creative meaning, add paid image calls, reduce consistency, lose speaking identities, or exceed the selected model's capabilities, explain the impact and obtain the corresponding business choice first. The model must not make these decisions for the user through internal runtime rewrites.