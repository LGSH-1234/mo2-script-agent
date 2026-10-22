
> **Node knowledge:** This file guides the parent agent's orchestration of creative research. The child's System Prompt is a tool input, not a research handbook for the parent agent to read and execute itself.

# Creative Research

## Execution Boundary

Once `creative_research/<project>` is ready, perform creative research through a stateful async child by default. The parent agent must not duplicate the child's work by directly calling search tools or loading the child prompt into its own context and acting as the child.

Resolve the current skill root to an absolute sandbox path, and pass the following absolute path only as `async_task_create.system_prompt_file`:

```text
{skill_root}/references/agents/creative-assistant.md
```

For initial research without a usable task ID, call `async_task_create` with a concise user-facing `description`, a complete `prompt`, the absolute `system_prompt_file` above, and metadata containing at least `purpose: batch_marketing_video_creative_research`, the accepted information version, and target markets. When `HISTORY (not current evidence)` shows previously provided creative research evidence that needs refreshing, deepening, or correction based on new facts, prefer `async_task_resume` with its `async_task_id`, passing the changed objective and complete current inputs through a follow-up prompt or `resume_data_v2`. Poll a running task first; do not resume it. Do not create parallel creative-assistant tasks for the same accepted information version. Create a replacement only if the previous task is missing, expired, killed with no usable state, or has a malformed handoff and the user chooses to retry.

The async task description, progress text, and final summary may be user-visible. Use natural business language in `COMMUNICATION LANGUAGE` to explain which audience preferences or creative directions are being explored. Do not expose async tasks, System Prompts, paths, handoffs, search types, or internal states.

## Create Or Resume Prompt

Every create/resume prompt must explicitly provide:

- Absolute sandbox paths for `skill_root` and the current `project_root`;
- The absolute path and version of the accepted `information-understanding.md`, stating that it is the sole authority for product facts;
- `COMMUNICATION LANGUAGE`, with target markets, video audience language, and priority platforms specified separately;
- This round's research objective, key questions, planned total, target duration/ratio, and accepted exploration constraints;
- A new, versioned internal `output_handoff_path`;
- The previous `previous_handoff_path`, checked against current inputs, or `none` for the initial round; label superseded product facts as historical and give the current information file precedence;
- Creative requirements added after information confirmation, or `none` if there are none.

For follow-up research, emphasize the changed objectives while still providing complete current factual inputs, the previous handoff, and the new output path. Explicitly instruct the child to read the previous handoff first, avoid its accumulated directions, and write the updated deduplication registry into the new handoff. Do not infer the current time for the child; it must obtain it through `sandbox_bash` as instructed by its System Prompt.

## Recovery And Polling

Async work spans multiple tool calls and waits. Immediately after create returns a task ID, record a project memo containing at least the task ID, output handoff path, current stage, and next poll step. Append a memo whenever the task status, output path, or next step materially changes. Memos support recovery after compaction and cannot close requirements.

Follow the same task by repeatedly calling `async_task_poll` until `state.status` is exactly `succeeded` or `failed`. A successful create/resume call, a non-final poll response, progress text, partial output, or any `created`, `running`, or `killing` status is only progress and must not end the research step or the parent agent's turn. Continue polling the same `async_task_id`; do not switch to StoryMaster, report PM evidence, or tell the user that research is complete while the status is non-final.

Between two non-final polls, the parent may actively pace the loop by calling `sandbox_bash` once with `sleep 30`; after that call returns, invoke `async_task_poll` again. This wait is only polling cadence: do not run it after `succeeded` or `failed`, stack multiple waits before the next poll, launch a background polling loop, or treat the wait as permission to end the current research step.

`succeeded` and `failed` are the actual async-task status values; do not normalize them to `success`, `completed`, or another synonym. A `killed` or `expired` task cannot become a valid research result by further polling: treat it as an unusable task and follow the retry-or-waive path below. After context recovery, retrieve the task ID and paths from PM next-action's memos and `HISTORY`, then verify actual task/file state before continuing the same polling loop.

## Terminal Validation

Only `state.status == "succeeded"` may enter handoff validation. Report `provide-research` only after that status is observed and the expected handoff exists, is non-empty, and reports `complete`. A `failed` poll result ends polling for that attempt but does not satisfy the PM node: preserve the task ID and error in a project memo, then follow the retry-or-waive path below. The parent agent must verify at least the following:

- The handoff references this round's accepted information version and records the system time independently obtained by the child and its raw output;
- It includes actual search summaries, explicit date windows, platform distinctions, and available heat evidence; insufficient evidence is clearly marked rather than presenting old examples as current trends;
- Sourced patterns are separated from inference, and online content has not been recast as facts about the current product;
- Creative directions are not derived from deaths, disasters, violence, serious illness, victims' experiences, or other harmful negative events;
- A successor round names the previous handoff, preserves the cumulative explored-direction registry, and explains how new directions materially differ from earlier ones, or explicitly identifies a user-requested continuation;
- Research follows the confirmed target markets, audience languages, and priority platforms rather than deployment region or agent-user communication language; cross-market references are clearly labeled.

After validation, record:

```json
{
  "path": "/sandbox/<project>/_internal/creative-research-v2.md",
  "async_task_id": "<actual task id>",
  "terminal": true,
  "terminal_status": "succeeded",
  "attestation": "validated complete handoff against accepted information and research gates"
}
```

Do not present the internal handoff to the user through `present_sandbox_file`. Briefly share only the one or two most promising directions, why they fit the accepted selling points, audience, and recent platform expression, and where evidence remains weak. Then let the PM advance to StoryMaster.

## Blocked Or Waived

If create/resume/poll returns an error, polling reaches `failed`, the task becomes `killed` or `expired`, or the System Prompt file, search capabilities, or handoff are unavailable or malformed, do not silently perform equivalent lengthy research in the parent context. Follow `dynamic-questionnaire-guide.md` to ask the user to choose `Retry creative search (recommended)` or `Continue with existing creative knowledge`. On retry, resume the same failed task when its state remains usable; otherwise create one replacement and poll that attempt to `succeeded` or `failed`. Only explicit user authorization for the latter can close the node through `waive-research`; tool failures, timeouts, memos, or the parent agent's own judgment are not waiver evidence.