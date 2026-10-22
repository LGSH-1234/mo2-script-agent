
# Post-delivery Review and Revision

Use at the current READY `continuation_decision/<project>/<round>`. This single open node covers feedback, any number of revisions, presentation, and the user's completion decision. The round identifies a batch lifecycle decision, not an editing attempt.

## Work Within the Open Node

Identify which delivered video and passage the user means, what should change, and what should remain. Use the current conversation and ask only about material ambiguity. Choose suitable tools and existing assets to edit, regenerate, supplement or splice the result. There is no mandatory revision-plan file, new-material declaration, per-attempt PM report, or revision subgraph.

Keep the node READY while work is underway, the user is dissatisfied, or a tool has failed. Do not submit a lifecycle choice just to acknowledge feedback. Editing this output does not mean starting another preparation or execution round.

Honor the requested scope and existing tool/spending authorization. Explain limitations when the tools cannot reliably preserve unaffected content; do not promise exact preservation without support. Do not infer wider creative changes from a narrow request.

## Inputs and Recovery

PM inputs are the **initial-generation baseline**, not an authoritative latest revision. Read the relevant blueprint, original executable prompt and part mapping when their actual content is needed and missing from context. Reuse the relevant image/audio/video files through the available tool's media arguments, not merely by mentioning their paths in a prompt. For generation calls, use the attachment visibility, media-index, deduplication and self-contained prompt rules in [payload-route-gates.md](payload-route-gates.md), not its initial-generation node sequence. Select references suitable for the revised content; an old storyboard depicting content the user changed is not a mandatory input to the new edit. For voice samples, apply [voice-anchor-gates.md](voice-anchor-gates.md). Map references to the final ordered arguments, deduplicating identical image paths while preserving all roles.

Preserve accepted files and write revisions to new paths. Do not erase the original delivery, blueprint or assets merely to edit the delivered result: that would reopen the initial generation workflow. New working prompts and temporary materials are not new PM requirements.

Use the existing project memo for recoverable multi-tool work: leave useful free-text notes about the user's request, latest outputs, task IDs and next step. No per-attempt schema or fixed logging cadence is required. After compaction, query this READY node again and verify recent memos against actual files and tool state. If the latest output cannot be established, ask or investigate; do not present the baseline as the latest revision.

## Present and Ask

Present the actual latest output through `present_sandbox_file` before asking for feedback. You may describe objective checks and propose improvements; subjective quality is the user's decision. Continue modifying and presenting within this same node until the user chooses what happens next. Intermediate presentations need no new delivery fact.

## Lifecycle Decisions

Distinguish accepting one video's edit from ending the whole batch project. Do not silently abandon remaining requested videos. If the user's intent is clear, follow it; otherwise clarify completion versus continuing the remaining work.

- `finish`: the user explicitly confirms that this project is complete. Record the actual confirmation in `user_evidence`; the PM then exposes `project_close` — complete it with `project finish` and refresh next-action. Do not ask the user to confirm the close again.
- `pause`: the user explicitly wants to pause. Record that choice, then seal it with `project pause`; do not claim that the results were accepted.
- `prepare`, `execute`, `extend`: only for explicitly requested other batch work, using the existing project lifecycle. They are not needed to revise the delivered output.

Use `select-continuation` and the exact current requirement ID under [evidence-and-commands.md](evidence-and-commands.md). There is no `revise` lifecycle choice. After a lifecycle mutation, refresh next-action; for finish/pause, complete the matching project command first.

A finish fact records the user's decision, not a structured registry of revised files. Present and identify the actual latest deliverables to the user, and leave useful recovery references in the project memo; the initial delivery paths remain historical baselines.