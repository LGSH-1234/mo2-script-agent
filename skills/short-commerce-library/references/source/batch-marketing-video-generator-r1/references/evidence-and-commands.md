
# Evidence and Commands

## Command Shape

All ordinary requirements use the finite action set:

```bash
python3 scripts/batch_pm.py apply <action> \
  --subject <requirement-id> \
  --data-json '<evidence-object>'
```

Use dedicated commands for frame safety-review facts:

```bash
python3 scripts/batch_pm.py frame reject \
  --subject frame/<project>/01/02 \
  --reason-json '{"reason":"safety-review"}'

python3 scripts/batch_pm.py frame retry --subject frame/<project>/01/02
```

Successful and rejected mutations both return only `BATCH_PM_RECEIPT_V1`. When evidence is already determined for several subjects listed `READY` by the same complete detail view, submit those fact mutations consecutively and append one next-action command after the last report:

```bash
python3 scripts/batch_pm.py apply <action-1> --subject <ready-1> --data-json '<evidence-1>' && \
python3 scripts/batch_pm.py apply <action-2> --subject <ready-2> --data-json '<evidence-2>' && \
python3 scripts/batch_pm.py project get-next-action
```

Do not insert a next-action call merely between those already determined reports. Stop the batch and refresh immediately if a receipt is rejected or the remaining evidence/readiness becomes uncertain. This batching rule is for providing facts already authorized by that detail view; it does not remove the explicit refresh required after `erase` or other branch-changing recovery.

Ordinary commands do not select a project. The PM replays its single event stream, derives the sole active project, and verifies the project segment embedded in each requirement ID. Only `project create` and `project resume` take `--project-id`, because satisfying a READY startup node establishes the next project identity. View options never belong on mutation commands.

New facts can be provided only to a currently `READY` requirement. Out-of-order submissions and attempts to overwrite a different effective fact are rejected without appending an event. An exact retry of a currently effective, directly reported fact succeeds without a write: same subject, resolution and full payload. JSON object-key order is ignored; list order and value types are preserved. This compares recorded evidence, not file contents or semantic similarity.

Such a retry returns `accepted: true`, `event: "unchanged"`, `unchanged: true`, `appended: false`, and the existing fact's `sequence` inside the usual receipt delimiters. It neither increments the sequence nor updates based_on or downstream facts. Do not erase, change paths, or redo work just to make a duplicate append. Continue any other already determined reports in the batch, then refresh next-action once; exit code 0 allows the command chain to proceed.

Erased, stale or inactive historical evidence never qualifies for unchanged, even when its payload matches. Follow READY and the usual evidence checks before reusing any historical artifact.

Erase is scoped to the active project: a subject owned by another project is rejected without writing an event, and lifecycle control facts (`continuation_decision`, `project_close`, startup and goal nodes) are never erasable through the generic command. Historical facts of the current project that have left the active graph remain erasable while the project is active; resuming a paused project restores that right. PM assigns new event sequences and dependency-version snapshots; do not submit versions or edit JSONL. Independently listed parallel ready nodes may be reported in either order. Report all of their already determined facts first, then refresh focus once; PM still validates readiness and dependency versions on every mutation. Lifecycle commands are described in [project-lifecycle.md](project-lifecycle.md) and are used only when next-action directs them.

## Next-action Requirement Selection

Without `--requirement-id`, next-action returns the current project's active requirement index. It groups the focusable requirements currently present in the active graph as READY, WAITING, or SATISFIED and intentionally contains no executable processing instructions. Select one or more exact IDs only from READY and repeat the option for each selection:

```bash
python3 scripts/batch_pm.py project get-next-action \
  --requirement-id image/<project>/01/S01 \
  --requirement-id style_reference/<project>/01/apparel_style
```

- Only currently READY IDs can be expanded. Unknown, waiting, satisfied, inactive, and historical IDs are rejected; refresh the index instead of guessing.
- Selection changes only the display. It does not change dependencies, READY, fact acceptance, or project identity. `--requirement-id` is a get-next-action option, never an `apply`, `erase`, or other mutation option.
- A selected Route A frame includes same-video, same-batch READY peers because they form one physical image call. `DETAIL REQUIREMENT IDS` makes this expansion explicit; each frame retains its own `REQUIREMENT CONTEXT`, while the shared `WHAT` names the execution group once.
- For `VIEW: file`, read [next-action-views.md](next-action-views.md), then use `sandbox_read` on `CONTENT PATH` through EOF. The locator is not execution guidance; act only from the complete envelope stored in the file.
- From one complete detail view, batch already determined facts for listed READY subjects, then refresh next-action without `--requirement-id` once after that batch.

Read [next-action-views.md](next-action-views.md) for selection, output budgets, materialized views, and truncation recovery. A missing end delimiter or sandbox truncation is incomplete input, not permission to execute from the fragment.

## Next-action Inputs

`RECORD WITH` names the permitted actions and routes typed submissions to this command reference. Its first occurrence prints the schema path; later groups reuse that entry within the same complete detail view. Read or restore the full reference if it is absent from the current context. Lifecycle commands use their own current-node reference instead. Command syntax does not replace the fixed knowledge contract in `REQUIRED SPECS (MUST BE UNDERSTOOD FIRST)`.

In a complete next-action detail view, `REQUIRED SPECS (MUST BE UNDERSTOOD FIRST)` lists the mandatory type-level knowledge and delivery standards. A listed file need not be reopened when its actual relevant content is already available and understood in the current context; otherwise read it in full before beginning the requirement. Each `REQUIREMENT CONTEXT` owns its `CURRENT INPUTS (USE AFTER SPECS)`, `HISTORY`, `WHY`, and requirement-specific `WHAT`; never carry an input or consumer into another context unless that context explicitly lists it. An indented `INPUT USE` belongs to that consumer and must still be followed when the payload line is deduplicated as reused evidence. Required `read_content` means the actual referenced file content must be present and complete in the current context before performing or recording that requirement. The first occurrence of a shared fact shows its requirement ID, current resolution and complete evidence payload; later contexts reference the first owning context at the same version, for example:

```text
- information_understanding/P01 [confirmed] {"path":"/sandbox/P01/information-understanding.md"}
- information_understanding/P01 [reuse evidence from image/<project>/01/S01] (fact version 3)
```

The `EXECUTION ORDER` section requires the spec knowledge first, then directs you to apply it separately to each context's `CURRENT INPUTS`. These inputs are dynamic information sources or production/tool materials. Follow an explicit `INPUT USE`; when none is declared, the current node spec decides whether a `.md` file is a factual source to read, a deliverable to present through `present_sandbox_file`, or an executable prompt. The current node spec also determines whether images, audio, and video enter tool arguments and how they are numbered. In particular, `video_blueprint` is canonical source content and is never `sandbox_generate_video.PromptPath`; only a `direct_payload` or `part_input` executable file may be transported. Finalize ordered media arguments before compiling that executable Markdown, then verify its one-based position mappings. If an executable mapping is stale, erase its payload/input owner, refresh next-action, and provide a corrected artifact at a new path when ready. Filenames, extensions, and sandbox paths do not determine handling.

## Project Memo

For long-running work, multiple tool calls, async waits, or multiple checkpoints, append a project-scoped memo before starting and after significant progress changes:

```bash
python3 scripts/batch_pm.py memo record \
  --message 'V01 Route A batch submitted as task abc; output target ...; next verify all 9 cells, then provide frames 01..09.'

python3 scripts/batch_pm.py memo list
```

The message expresses the memo's subject, related nodes, paths, task IDs, completed steps, and next step; the interface takes no node argument. A complete requirement detail shows the latest 5 memos; the active requirement index does not. `memo list` returns the latest 20 by default, adjustable with `--limit 1..100`.

A memo is only an opaque recovery note from the LLM. It does not satisfy requirements, update evidence versions, or change the active graph, and cannot prove user authorization, tool success, file existence, or factual correctness. Verify it against the current graph, facts, tool state, and files during recovery. Each message must be non-empty single-line text of at most 4000 characters.

## Intake and Story

| Action | Subject | Evidence |
|---|---|---|
| `report-language` | `communication_language/<project>` | `{"language":"zh-CN"}` |
| `confirm-information` | `information_understanding/<project>` | `{"path":".../information-understanding.md"}` |
| `provide-research` | `creative_research/<project>` | `{"path":".../creative-research-v2.md","async_task_id":"...","terminal":true,"terminal_status":"succeeded","attestation":"concise statement of completed handoff validation"}` |
| `waive-research` | `creative_research/<project>` | `{"user_evidence":"exact user statement or reference explicitly authorizing the skip"}` |
| `confirm-story` | `story_master/<project>` | `{"shots":9,"duration_ms":15000,"path":".../story.md"}` |
| `confirm-directions` | `direction_set/<project>` | `{"planned_total":2,"directions":{"01":{...},"02":{...}}}` |
| `select-preparation` | `preparation_scope/<project>/<round>` | `{"videos":["01","02"]}` |

`planned_total` must equal the actual number of `directions`. Direction keys must be unique canonical string IDs: nonempty single segments with no leading/trailing whitespace, slash, control characters, or `.`/`..` values. Noncanonical keys and aliases such as `"01"` plus `" 01 "` are rejected, never silently renamed. Preparation may select only IDs already present in DirectionSet.

Use the unit-bearing field `duration_ms` for all durations; unitless numbers are not accepted. When converting from seconds, explicitly calculate `seconds × 1000`, then submit integer milliseconds.

The 15-second, 9-shot story is an evidence-format example, not a default or required structure. Report the actual confirmed duration and authored shot count.

Creative research must run through an async child as described in `creative-research.md`. Repeatedly call `async_task_poll` on the same task until `state.status` is exactly `succeeded` or `failed`; create/resume receipts and non-final poll states do not finish the parent turn. Set `terminal=true` and call `provide-research` only for the exact `succeeded` status after successful handoff validation. A `failed` result is terminal for that attempt but cannot satisfy the node; preserve it in a project memo and follow the retry-or-waive guidance. Record the running task ID and next step in a project memo first; on node completion, include the task ID and terminal provenance in typed evidence. Direct searches or a handoff written by the parent agent cannot replace this evidence.

## Package Preparation

| Action | Subject | Evidence |
|---|---|---|
| provide-video-blueprint | video_blueprint/<project>/<video> | path, shots, duration_ms, ratio, market_target |
| provide-video-spec-definition | video_spec_definition/<project>/<video> | images, audios, videos mappings |
| provide-image / provide-audio / provide-video | image/audio/video/<project>/<video>/<id> respectively | {"paths":["/absolute/file"]}; review_required also needs presentation_tool and user_evidence |
| delegate-image / delegate-audio / delegate-video | corresponding media node | {"user_evidence":"explicit creative delegation and constraints"}; only if auto is allowed |
| waive-image / waive-audio / waive-video | corresponding media node | {"user_evidence":"explicit acceptance of omission","reason":"accepted reason"}; only for supplemental product image references with supplemental_to; audio/video cannot waive |
| confirm-product-state-coverage | product_state_coverage/<project>/<video> | products mapping for exactly the image IDs marked product_coverage |
| select-storyboard-mode | storyboard_mode/<project>/<video> | {"mode":"visual"} or {"mode":"script_only"} |
| report-image-model | image_model/<project>/<video> | {"model":"gpt_image_2","source":"system-reminder"}; visual storyboard only |
| provide-frame-spec-definition | frame_spec_definition/<project>/<video> | exactly `frames: [{"frame":1,"visual_description":"...","image_ids":["SKU-A"]}, ...]` with one entry per blueprint shot (`frame` strictly 1..N matching position and shot), non-empty text descriptions, unique declared image IDs (may be empty); no path, no blueprint mapping, no extra keys |
| provide-frame | frame/<project>/<video>/<frame-index> | {"path":"/absolute/frame.png"}; the index equals the blueprint shot number it visualizes |
| provide-storyboard-manifest | storyboard_manifest/<project>/<video> | {"path":"/absolute/manifest.json"} |
| derive-storyboard-overview | storyboard_overview/<project>/<video> | {"path":"/absolute/overview.png"} |
| confirm-package | package_confirmation/<project>/<video> | {"presentation_tool":"present_sandbox_file","user_evidence":"user accepts the presented story, materials and selected mode"} |

Blueprint evidence example:

```json
{"path":"/workspace/video-projects/P01/video-blueprint-01.md","shots":9,"duration_ms":15000,"ratio":"9:16","market_target":{"language":"en-US","country_region":"United States","audience":"Urban commuters","platform":"TikTok"}}
```

The duration, shot count, ratio, and market target are examples, not defaults. Author the blueprint first from the accepted Master and Direction. Its reported count owns frame expansion; its narrative owns shot/material appearances.

Definition example:

```json
{
  "images": {
    "product_front": {"role":"product","description":"The same accepted SKU, front and opened views","allowed_resolutions":["provided"],"product_coverage":true},
    "hero": {"role":"character","description":"The recurring host's appearance","allowed_resolutions":["provided","auto"],"review_required":true,"continuity":true}
  },
  "audios": {
    "narrator": {"role":"voice","description":"Narrator timbre only; never use sample words","allowed_resolutions":["provided","auto"],"review_required":true,"continuity":true,"voice_sample":true}
  },
  "videos": {}
}
```

Names are runtime-declared semantic IDs. No shot mapping or duplicated duration/market facts belong in definition. video_spec and media groups are structural collections and have no reporting action. Consult video-spec-contract.md for process flags and media-requirements.md for evidence rules.

Coverage example:

```json
{"products":{"product_front":{"status":"covered","assessment":"Accepted references cover the blueprint's required views and states"}}}
```

Allowed coverage statuses: covered, reference_confirmed, risk_accepted. The latter two require actual user_evidence; reference_confirmed also requires presentation_tool=present_sandbox_file. Additional files for an existing requirement must be registered in that image node's paths before they can serve as downstream evidence; revise that node and refresh the graph if needed. Risk acceptance follows asset-anchor-gates.md and never creates missing media or authorizes unsupported product claims.

Optional supplemental product image declarations may set `supplemental_to` to a distinct product_coverage image ID and permit waived. Other objects use provided/auto; descriptions alone cannot grant waiver permission. Lowering materializes all auto objects regardless of continuity or part usage.

## Execution

| Action | Subject | Evidence |
|---|---|---|
| `select-execution` | `execution_scope/<project>/<round>` | `{"videos":["01"]}` |
| `report-video-model` | `generation_model/<project>/<video>/<round>` | `{"model":"Seedance_2.5","source":"system-reminder"}` |
| `provide-direct-payload` | `direct_payload/<project>/<video>/<round>` | `{"path":".../payload.json"}` |
| `provide-runtime-manifest` | `runtime_manifest/<project>/<video>/<round>` | `path` and ordered `parts: [{"part":1,"duration_ms":15000}, ...]` matching PM count/bounds; this evidence is not the artifact file schema. Write the mode-specific file under [runtime-lowering-grid-contract.md](runtime-lowering-grid-contract.md) first. |
| `provide-runtime-anchor` | `runtime_anchor/<project>/<video>/<round>/<kind>/<identity>` | Actual `path`, objective all-true `checks`; generated voice also needs `duration_ms == 3000` |
| `confirm-part-spec` | `part_spec/<project>/<video>/<round>/<part>` | Accepted manifest part's `duration_ms` and `materials` mapping; select original non-waived IDs declared in video_spec_definition |
| `derive-part-sheet` | `part_sheet/<project>/<video>/<round>/<part>` | `{"path":"..."}` |
| `provide-part-input` | `part_input/<project>/<video>/<round>/<part>` | `{"path":"..."}` |
| `pass-preflight` | `preflight/<project>/<video>/<round>` | `{"checks":{"bindings":true,"files":true}}` |
| `report-continuity-choice` | `continuity_choice/<project>/<video>/<round>/<part>` (part > 1) | `{"use_last_frame":true,"reason":"Continue the previous actual composition"}` |
| `provide-last-frame` | `last_frame/<project>/<video>/<round>/<source-part>` | `{"path":".../last-frame.png"}` |
| `pass-part-preflight` | `part_preflight/<project>/<video>/<round>/<part>` | `{"checks":{"bindings":true,"files":true}}` |
| `record-direct-result` | `direct_result/<project>/<video>/<round>` | `{"path":".../video.mp4"}` |
| `record-part-result` | `part_result/<project>/<video>/<round>/<part>` | `{"path":".../part.mp4"}` |
| `record-assembled-result` | `assembled_result/<project>/<video>/<round>` | `{"path":".../video.mp4"}` |
| `present-delivery` | `delivery/<project>/<video>/<round>` | `{"path":".../video.mp4","presentation_tool":"present_sandbox_file"}` |
| `select-continuation` | `continuation_decision/<project>/<round>` | `{"choice":"prepare|execute|extend|finish|pause"}`; finish also requires nonempty actual `user_evidence` |

The continuation `choice` must be one of the exact lowercase tokens above; whitespace and case variants are rejected without recording a fact. `{"choice":"pause"}` is valid without `user_evidence`; the close node consumes the complete accepted payload.

At READY continuation_decision, follow [post-delivery-revision.md](post-delivery-revision.md). Editing and presenting revisions keep the same node open; do not record a lifecycle choice per attempt. For example, only after explicit project completion: `{"choice":"finish","user_evidence":"The user confirmed the latest presented outputs and ended this project."}`. Then call `project finish` and refresh next-action. Pause similarly requires `project pause`; it is not acceptance.

Execution may select only prepared videos with completed package confirmation. Direct `preflight.checks` and lowered `part_preflight.checks` must contain a non-empty set of objective check results, all true; subjective quality confirmation is outside preflight. Follow [part-continuity.md](part-continuity.md) for LLM-owned boolean continuity choices, conditional end-frame assets, and per-part checks. An unanswered choice is not false; it must be reported before that part's input can close.

## Revision

Use `erase → project get-next-action → ready typed action`, not a direct overwrite:

```bash
python3 scripts/batch_pm.py erase \
  --subject frame/<project>/01/02 --reason 'User requested a composition change' && \
python3 scripts/batch_pm.py project get-next-action
```

Erase withdraws one previously reported fact, including an old fact no longer in the active branch. It preserves files, other facts, and event history. Unknown, already-erased, and PM-derived subjects are rejected. To change a derived Direction, erase its `direction_set/<project>` owner. Project bootstrap and continuation lifecycle decisions use their dedicated workflow, not erase.

After `project pause` or `project finish`, use `project resume` to continue the same project; PM opens a fresh continuation question. If work changes before closing the project, follow any reopened delivery and continuation nodes rather than reusing a previous finish/pause answer.

Affected downstream evidence is no longer current. Do not submit old confirmations, execution selections, paths, or tool results in bulk to restore progress. Follow `READY`, inspect each node's current inputs, reuse an unchanged artifact only after checking it still satisfies that node, and obtain the confirmations or authorizations required by its reference. Reproviding identical upstream content after erase or invalidation still creates a new fact version and does not automatically revive downstream evidence; this is distinct from retrying an already effective fact.

`CURRENT INPUTS` contains only current effective inputs. A separate `HISTORY (not current evidence)` section may show the ready node's prior payload, such as an old path or async task ID. Use it to locate and verify recoverable work, never as proof that the current node is already satisfied.

To switch from visual to script-only after the user chooses it, erase `storyboard_mode/<project>/<video>`, refresh focus, then use `select-storyboard-mode` with `{"mode":"script_only"}` when ready. Visual-only frames, manifests, and overviews leave the active graph. Switching back requires fresh frame evidence; old images do not automatically become accepted again.

The event store uses schema v3. If an old test project is rejected as unsupported, preserve its files and start a new project ID or state root. Do not rewrite its JSONL to imitate the new schema.