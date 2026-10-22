
# Next-action Views

Next-action has one query key: the real `requirement-id` emitted by PM. Querying changes only the displayed projection; it never changes the graph, READY frontier, facts, versions, or project identity.

## Active Requirement Discovery

Call next-action without a requirement ID after bootstrap, context recovery, and every mutation batch:

```bash
python3 scripts/batch_pm.py project get-next-action
```

`VIEW: requirement-index` is a discovery response over the current active graph. It groups focusable business requirements as `READY`, `WAITING`, or `SATISFIED`, but deliberately omits `REQUIRED SPECS`, `CURRENT INPUTS`, `EXECUTION ORDER`, `WHY`, `WHAT`, and `RECORD WITH`. It excludes the never-completing GOAL, structural nodes, inactive history, and conditional branches that have not materialized. The index is not executable guidance. Select work only from its latest `READY` group; `WAITING` and `SATISFIED` are visibility only.

If the requirement index exceeds the output budget, stdout returns `VIEW: file` instead of truncating or paginating it. The locator identifies a complete `requirement-index` envelope by absolute `CONTENT PATH`, byte count, SHA-256 and short view token. Use `sandbox_read` on that path and continue from the next offset until EOF if a read is partial. Select work only from the complete envelope in the file, never from the locator itself.

## Requirement Details

Pass one or more current READY IDs to obtain complete instructions:

```bash
python3 scripts/batch_pm.py project get-next-action \
  --requirement-id image/<project>/01/S01

python3 scripts/batch_pm.py project get-next-action \
  --requirement-id image/<project>/01/S01 \
  --requirement-id style_reference/<project>/01/apparel_style
```

Repeat `--requirement-id` to inspect several independently READY items in one detail envelope. PM may share `REQUIRED SPECS` and command schema by semantic type, but emits a separate `REQUIREMENT CONTEXT` for every selected item. Each context owns its `CURRENT INPUTS`, `HISTORY`, `WHY`, and requirement-specific `WHAT`; a repeated evidence payload is replaced by an explicit `reuse evidence from <requirement-id>` reference rather than losing that ownership. Do not mix inputs or consumers across contexts. IDs that are unknown, waiting, satisfied, inactive, or no longer READY are rejected; refresh the requirement index instead of guessing or using historical IDs.

Business nodes explicitly declare display groups and execution groups. A group's peer-expansion policy includes only members already present in the service's READY frontier. For Route A, the business declaration identifies one physical sheet call for the same project, video, and batch. Selecting any member explicitly includes those READY peers under `DETAIL REQUIREMENT IDS`; each frame still keeps its own `REQUIREMENT CONTEXT`, `CURRENT INPUTS`, and `WHY`, while the shared `WHAT` names the complete execution group once. Route B declares one independent group per frame. The view treats group IDs as opaque: incoming consumer order, additional consumers, and requirement ID spelling cannot redefine membership. This does not make non-READY frames executable and does not recompute the frontier.

`VIEW: detail` is executable guidance only after its closing delimiter is present. From one complete detail view, submit every already determined fact for its listed READY subjects, then refresh the requirement index once after that mutation batch. Stop and refresh early after a rejection or when readiness/evidence becomes uncertain.

## Use Labels and Self-contained Outputs

Inside one complete detail output, evidence payloads receive stable `E01…` labels and each single input use a `U01…` label. A group's COMMON CURRENT INPUTS section lists the evidence and uses shared by every requirement in that execution group with its explicit `[applies to …]` consumer list; each REQUIREMENT CONTEXT then references them via its `USE:` line and adds only its requirement-specific inputs. Identical uses may be referenced by label; a differing mode, source field, target, purpose, strength or resolution set always prints in full again. Labels are view markers within the single output that defines them: they are not events, are not persistent, and every detail or materialized file is self-contained — it never requires reading a previous request to resolve E/U references.

A frame context additionally prints its `FRAME TARGET`: the exact source expression (`E-label.frames[index]`), the one-based frame and blueprint shot numbers, the selected entry's `visual_description`, and its `image_ids`. Inputs without a declared use still print their fact once with an explicit no-declared-use note.

## Bounded and Materialized Detail

Each next-action response defaults to at most 12,000 UTF-8 bytes, including delimiters and final newline. `--max-bytes` may select 4,000..24,000 bytes. Each `CURRENT INPUTS` evidence payload is printed once per fact requirement ID and version within a detail response; later contexts reference its first owning context. `REQUIRED SPECS` paths are also emitted once.

When selected details do not fit, stdout returns a bounded `VIEW: file` locator. PM writes the exact complete `detail` envelope atomically to a content-addressed `.txt` file. Online runs use `/workspace/.tmp/batch_pm_views`; local runs use the operating system's temporary directory under `batch_pm_views`. The Skill installation and source directories remain immutable.

Read `CONTENT PATH` completely with `sandbox_read` before acting. If the tool returns only part of the file, continue with the next offset until EOF and verify that the reconstructed text contains both `<<<BATCH_PM_NEXT_ACTION_V1>>>` and `<<<END_BATCH_PM_NEXT_ACTION_V1>>>`. `CONTENT BYTES` and `CONTENT SHA256` identify the expected file. If the file is missing, incomplete or has been cleaned up, call next-action again; the same current view regenerates or reuses the same content-addressed path.

The locator is not executable guidance and does not contain a partial requirement. Materializing a view does not append an event, change facts, change the graph or persist focus. The cache is bounded and temporary; a later mutation can make an older file semantically stale in exactly the same way it makes an older inline Hint stale, so refresh next-action after mutation batches as usual.

The budget covers memos, HISTORY, WHY, and inputs as well as READY nodes. It never silently drops fact fields or recovery information. A sandbox truncation notice or missing `<<<END_BATCH_PM_NEXT_ACTION_V1>>>` means the response is incomplete; continue reading the materialized file through EOF rather than using `head`, `tail`, or output filtering.