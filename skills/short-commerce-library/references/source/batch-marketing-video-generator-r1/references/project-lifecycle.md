
# Project Lifecycle

Read this reference for a READY `start_new_project/<cycle>` or `continuation_decision/<project>/<round>`. Ordinary startup and context recovery begin with `project get-next-action`, not a lifecycle mutation. The PM owns one event stream and permits one active project at a time.

## New Project

When the startup detail lists `project create`, choose a stable project ID, create it, then refresh:

```bash
python3 scripts/batch_pm.py project create --project-id <project-id> && \
python3 scripts/batch_pm.py project get-next-action
```

Creation satisfies the current `start_new_project/<cycle>` fact. Every project-scoped requirement ID then contains that project ID, for example `information_understanding/<project-id>` and `video_spec/<project-id>/01`. Use those exact IDs from PM output; do not reconstruct or shorten them.

## Existing Project

When a project is active, next-action directly returns its active graph. Do not create or resume another project. Context compaction is not a lifecycle event: recover by calling next-action without remembering or supplying a project ID.

A paused or finished project may be resumed only when a later READY startup detail lists `project resume`. First establish that the user's current intent is to continue that same project. A clear request to continue suffices; otherwise ask before reopening.

```bash
python3 scripts/batch_pm.py project resume --project-id <paused-project-id> && \
python3 scripts/batch_pm.py project get-next-action
```

Resume preserves unchanged evidence and opens a fresh continuation round. Never use create over an existing project's history.

## Open Delivery Review

At continuation_decision, follow [post-delivery-revision.md](post-delivery-revision.md). Keep the same node READY throughout edits and repeated presentations. A local revision is not a lifecycle selection. Finish requires the user's explicit project-completion evidence; pause is not acceptance. Prepare/execute/extend select other batch work, not editing attempts.

## Pending Close

Recording a finish/pause decision does not close the project by itself: the next READY node becomes `project_close/<project>/<round>`. At that point the user's decision is already made — do not ask again, do not create or resume another project, and do not report an LLM fact for the close. Run the exact listed lifecycle command (`project finish` or `project pause`), then refresh next-action; only after its receipt does `start_new_project/<next-cycle>` become READY and the startup detail apply. If a fresh context shows the close node READY, the same rule recovers the correct action from next-action alone. Resuming a closed project opens a new continuation round with its own future close node.

## Serial Project Spine

Projects do not run in parallel. `start_new_project/01` is initially READY. After it creates project `P01`, `start_new_project/02` exists but depends on `project_goal/P01`; it becomes READY only after that project is finished or paused through its continuation decision. Creating or resuming the next project then advances the same pattern.

Pause and finish are lifecycle operations guided by the continuation decision, not consequences of context loss. After any lifecycle mutation, refresh next-action before deciding what work is allowed. Never edit or replay JSONL to establish, resume, or close a project; PM owns event order, dependency versions, and the current frontier.

The local graph debugger is separate: it consumes browser-owned events through an in-memory store while exercising the same graph and command logic.