
---
name: batch-marketing-video-generator-r1
description: Bootloader for batch marketing video creation. Use the PM's reverse dependency graph to select the current ready requirement, then load node-specific references for marketing creative, assets, storyboards, scripts, voices, and execution. Do not bypass the PM to orchestrate the workflow independently.
tools: ["todo_write", "dynamic_questionnaire", "present_sandbox_file", "sandbox_generate_image", "sandbox_generate_audio", "sandbox_generate_video", "sandbox_bash", "sandbox_read", "sandbox_write", "sandbox_edit", "sandbox_process_video", "render_video", "pippit_omni_search", "pippit_tool_ask_echo_search", "async_task_create", "async_task_poll", "async_task_resume", "async_task_kill", "load_skill"]
---

# Batch Marketing Video Generator Bootloader

This file only starts and restores the workflow. The PM controls the structured process; references named by the PM's current ready nodes explain how to complete those nodes. Do not treat `SKILL.md` as a complete creative handbook or maintain a separate workflow state in context.

## Bootstrap

The PM owns one durable event stream and permits one active batch project at a time. Project identity is carried by project-scoped requirement IDs, so ordinary commands do not select a project. Start with next-action for both a new session and recovery:

```bash
python3 scripts/batch_pm.py project get-next-action
```

Next-action is read-only. The active graph itself restores the current project and its exact requirement IDs after context compaction. Use the returned requirement index to understand READY, WAITING, and SATISFIED work, select a READY requirement, then query that exact ID for its REQUIRED SPECS, CURRENT INPUTS, and lifecycle instructions. A fresh stream exposes `start_new_project/01`; after each project is closed, the next serial startup node becomes available. Do not automatically create or resume before reading its detail, and do not read, edit, or generate the JSONL directly.

## Focus Loop

Read the entire `<<<BATCH_PM_NEXT_ACTION_V1>>>` envelope without truncating, filtering, or discarding it. For each focus, follow this order:

First inspect `VIEW`. A call without `--requirement-id` returns `requirement-index`: it discovers the READY, WAITING, and SATISFIED requirements in the current active graph but deliberately contains no execution guidance. Query one or more exact READY IDs by repeating `--requirement-id`; only a complete `detail` view supplies executable guidance. If the response says `VIEW: file`, the inline envelope is only a locator: use `sandbox_read` on `CONTENT PATH`, continue through EOF if the tool returns a partial read, and act only from the complete `BATCH_PM_NEXT_ACTION_V1` envelope stored there. If that file is unavailable, call next-action again to regenerate it. A missing end marker or tool truncation is incomplete input even with exit code 0. See [references/next-action-views.md](references/next-action-views.md) for requirement selection and materialized views.

1. `READY`: work only on the listed requirements; do not start unlisted work early.
2. `REQUIRED SPECS (MUST BE UNDERSTOOD FIRST)`: these paths identify the fixed knowledge contract and delivery standards for the current node. Before working, ensure the applicable spec content is present and understood in the current context. Opening a file is not itself the goal: skip rereading only when the actual relevant content is already available and sufficient to apply without guessing. A filename, summary, remembered gist, or claim that the file was read earlier is insufficient. If its content is absent, partial, uncertain, or lost after compaction, read the listed file in full from the actual skill root. Follow additional explicit links only when the current READY work requires them; do not load other nodes' specs incidentally.
3. `CURRENT INPUTS`: only after the required specs are known, inspect the current project evidence projected by the PM. Evidence payloads and single uses carry `E01…`/`U01…` labels within this one output; a `USE:` line in a REQUIREMENT CONTEXT applies exactly the referenced shared or specific uses to that requirement, and a COMMON CURRENT INPUTS section applies only to the consumers it lists. A frame's `FRAME TARGET` selects its exact frames entry. Each entry includes a requirement ID, resolution, and actual payload, such as paths, image lists, or structured facts. These are dynamic information sources or production/tool materials for the current node; they do not replace its required specs. In a multi-requirement detail, each `REQUIREMENT CONTEXT` owns its following `CURRENT INPUTS`, `HISTORY`, `WHY`, and requirement-specific `WHAT`; never transfer an input or downstream consumer to another context unless that context explicitly lists or reuses it. An indented `INPUT USE` is a consumer-specific instruction: obey its mode, source field, purpose, and required/optional strength for that enclosing requirement even when the payload was printed earlier and is shown here as reused evidence. For required `read_content`, proceed only when the actual referenced content is present and complete in the current context; otherwise read the file first. When an input has no `INPUT USE`, follow `EXECUTION ORDER` and the required specs to determine whether it must be read, presented, or passed as a tool argument. Do not infer handling from an extension or path.
4. `WHY` explains only the downstream consumers of its enclosing `REQUIREMENT CONTEXT`; it does not authorize executing those nodes or loading their references. `WHAT` defines either that requirement's work or an explicitly named frame execution group.
5. Before work spanning multiple tool calls, async waits, long media generation, or several recoverable checkpoints, record the objective, progress, key paths/task IDs, and a concrete next step in a project memo. Append a memo whenever recovery information materially changes. Do not mechanically record simple atomic actions.
6. Perform the semantic work, template completion, prompt writing, media generation, inspection, presentation, or user communication required by the references.
7. `RECORD WITH`: report evidence using only the listed typed action and the schema in [references/evidence-and-commands.md](references/evidence-and-commands.md).
8. Mutation receipts contain no next instructions. From one complete detail view, report every fact whose evidence is already determined for its currently listed `READY` subject; issue those fact mutations consecutively, then call `project get-next-action` without `--requirement-id` once after the batch to refresh the active requirement index. Stop the batch and refresh early if a receipt is rejected or the remaining evidence/readiness becomes uncertain. An `unchanged` receipt means an identical current fact was already effective: no event was appended, so continue the batch without erasing or redoing that work. Erase and other branch-changing recovery still require their explicit refresh step before fresh evidence is reported.

```bash
python3 scripts/batch_pm.py apply <typed-action-1> \
  --subject <ready-requirement-id-1> --data-json '<typed-evidence-1>' && \
python3 scripts/batch_pm.py apply <typed-action-2> \
  --subject <ready-requirement-id-2> --data-json '<typed-evidence-2>' && \
python3 scripts/batch_pm.py project get-next-action
```

## Changing Accepted Facts

Follow the current READY node's revision policy first: work permitted within an open node need not change accepted upstream facts. When an accepted workflow fact itself must change, identify its semantic owner using [references/revision-routing.md](references/revision-routing.md). Withdraw that owner's fact first:

```bash
python3 scripts/batch_pm.py erase \
  --subject <owning-requirement-id> --reason '<requested correction>' && \
python3 scripts/batch_pm.py project get-next-action
```

Erase preserves files and history. Follow the new `READY` focus, use new artifact paths, obtain the required confirmations, and report through the listed typed action. Never directly overwrite an accepted fact or bulk-replay downstream evidence. If a downstream node is ready again, do not erase it mechanically: verify or redo its work against current inputs and provide fresh evidence. `HISTORY` contains old files/task IDs for recovery only, not accepted inputs or current authorization.

## Recovery

After context compaction, thread recovery, tool failure, or uncertainty about the next step, do not reconstruct the workflow or project identity from memory. Call `project get-next-action`, select the relevant READY IDs, and query their complete detail. Read the latest `PROJECT MEMOS` in that detail and restore the references and project facts named in the envelope whose contents are incomplete in the current context. Memos are project-scoped recovery hints left by the LLM. They are not bound to nodes and are not facts, authorization, or completion evidence; verify them against the current active graph, PM facts, and actual files before use.

If a required reference is not found, refresh `project get-next-action` and verify the exact listed path and actual skill root. Do not guess an alternate filename, create a substitute reference, or switch to a downstream node. If the required path is still unavailable, report the missing reference and stop the affected work.

## Hard Boundaries

- Apply [references/user-communication.md](references/user-communication.md) to all user-visible wording, including progress/tool descriptions and deliverable text. Never expose internal model names/IDs, modes, branches, or execution-path labels (such as Route A/B, script_only, visual, direct, or lowering); describe their creative meaning instead and preserve exact identifiers only where required for internal execution.
- The PM provides topology, readiness, typed evidence contracts, and scheduling. It cannot replace knowledge of marketing structure, templates, prompt craft, asset consistency, or voice semantics.
- Loading an external skill acquires domain knowledge for the current READY node; it does not transfer workflow control. Do not adopt that skill's independent workflow, stage order, or automatic next-step instructions.
- `CURRENT INPUTS` may carry a consumer-specific `INPUT USE`; when present, it defines that input's required consumption mode for the enclosing requirement. Without one, a `.md` file may need to be read into context, passed as `PromptPath`, or presented as a deliverable, as determined by the current node's REQUIRED SPECS. Video blueprints are model-independent read/presented inputs and are never executable `PromptPath`; direct/part mapping nodes produce executable prompt files. An input-use instruction guides execution but is not proof that an external tool call occurred.
- References provide node-specific processing knowledge. Their templates and examples cannot activate nodes, satisfy requirements, or change PM branches by themselves.
- Do not fabricate resolutions, invent a generic `asset provide`, or use an asset to close a mismatched requirement. To change an accepted workflow choice, erase its owner, read next-action, and record the dedicated choice only when ready.
- Revisions use new file paths and preserve history. Successfully call `present_sandbox_file` before asking the user to review or confirm actual files. The model may report objective checks and suggest changes, but cannot confirm subjective quality on the user's behalf.
- Read image/video model facts only from UI-injected `<system-reminder>[User Setting]`. If absent, follow the current focus to guide the user to select a model or record conservative unknown.

## Maintainer References

Read [references/graph-contract.md](references/graph-contract.md) only when modifying the PM itself. For normal creative work, establish only the specs listed under next-action's `REQUIRED SPECS (MUST BE UNDERSTOOD FIRST)` instead of scanning the references directory.