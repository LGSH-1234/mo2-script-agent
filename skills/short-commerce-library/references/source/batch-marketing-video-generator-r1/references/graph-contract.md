
# Graph Contract

## Direction

Graph edges point from consumers to prerequisite requirements. `GOAL` never completes. Build the active graph determined by current facts through depth-first expansion from `GOAL`, then calculate its ready frontier.

```text
GOAL
└── start_new_project/<cycle>
    └── project_goal/<previous-project>     # absent for cycle 01
        ├── communication_language/<project>
        ├── information_understanding/<project>
        ├── creative_research/<project>
        ├── story_master/<project>
        ├── direction_set/<project>
        ├── preparation_scope/<project>/<round>
        ├── package_confirmation/<project>/<video> × N
        ├── execution_scope/<project>/<round>
        ├── delivery/<project>/<video>/<round> × N
        └── continuation_decision/<project>/<round>
```

Creating or resuming a project satisfies the current startup node and advances `GOAL` to the next startup cycle. That next startup depends on the active project's goal, so it remains waiting until the project is actually closed. A finish/pause continuation decision first materializes `project_close/<project>/<round>` (an internal lifecycle node sealed only by the `project finish`/`project pause` command, never by an LLM fact): while it is pending, the startup is not READY and create/resume are rejected under the store lock. The close event deterministically writes the close node's evidence bound to the continuation fact version, updates the lifecycle and clears the active project in one replayable step; resuming later opens a new continuation round with its own close node. This serial spine prevents parallel projects and unreplayable streams without hiding the active project's graph.

## Dependency Evaluation

Each dependency rule returns one of three outcomes:

- unknown: facts needed by the condition are not yet closed; build no edge in this pass;
- known + 0 targets: the condition is definitively false;
- known + 1..N targets: build edges to the corresponding requirements; the same mechanism expresses cardinality.

Graph construction must evaluate all dependency slots of a node rather than stop at the first incomplete node. Each fact producer read by a condition must be reachable through other edges not governed by that condition. Otherwise the producer is hidden by the edge it controls, and compilation reports a modeling error.

The reducer first separates latest candidate evidence from withdrawn facts and historical payloads. Effective facts start empty. Each pass declares the graph using only effective facts, without calling a conditional resolver whose producers are not yet effective. Valid candidate evidence then expands the effective set until a fixed point. All dependency slots are visited on every pass. Historical selectors and cardinalities are never evaluated provisionally. Unknown rules block their owner's satisfaction, not the discovery of independently reachable questions.

Validate cycles in both structural edges and producer-evaluation dependencies before recursive satisfaction checks. Producer dependencies affect evaluation and version snapshots; ordered sibling slots still do not become edges.

## Ordered Scheduling

The relative order of `deps` is a scheduling constraint: a later active slot enters the ready frontier only after earlier active slots are satisfied. This order is not a structural tree; adjacent siblings must not automatically compile into `A → B`.

Explicit business dependencies remain real edges. The blueprint precedes definition; definition expands media children; storyboard_mode depends on the completed video_spec collection. Sibling slot order creates no edges.

## Satisfaction and Revision

Satisfying a node with a contract requires all of the following:

1. All current active prerequisites are satisfied;
2. The evidence resolution belongs to the set allowed by the node;
3. The evidence payload passes schema validation for that requirement type;
4. Every dependency rule has a known result;
5. Its PM-recorded `based_on` snapshot exactly matches the current prerequisite fact versions, including each conditional rule's producers even when it returns zero targets.

Events carry one stream-wide monotonic sequence, not business dependencies. On acceptance, RequirementService rebuilds the graph and verifies that the requested subject is in the current ready frontier. PM captures prerequisite node IDs and their fact sequences; the caller supplies neither. Contractless structural prerequisites expand to their prerequisite facts. Derived Direction evidence binds the DirectionSet sequence. Frames explicitly depend on blueprint, definition, image model, mode and all declared media.

An identical retry of a currently effective directly reported fact returns UnchangedFact, not an Event. Equality requires the same subject, resolution and full typed JSON payload; object order is irrelevant, list order and value types are significant. The current effective projection and original requirement_resolved event are required: raw history, derived facts and bootstrap lifecycle evidence cannot match. Persistence makes this decision under the same event-stream lock as replay and append, returns the existing sequence, and writes nothing. The receipt reports unchanged explicitly. No version/based_on refresh, graph change or downstream invalidation occurs. READY-only acceptance applies to new facts, not acknowledgement of this no-op.

To change an accepted fact, append `requirement_erased` for its owner, refresh focus, and provide fresh evidence when ready. Erase removes the current candidate only; it does not delete files, recursively write downstream erasures, or remove event history. Dependent historical evidence is ineffective. Reproviding even identical content after withdrawal or invalidation has a new sequence and cannot revive downstream snapshots. Direct overwrite/revision events are not supported.

Only directly reported facts are erasable; derived Direction is changed through DirectionSet. Bootstrap and continuation decisions are lifecycle operations, not erasable evidence. The schema is v3 with no legacy migration. Store replay, request validation, and append occur under one event-stream lock; rejected requests append nothing.

The execution model question explicitly depends on its round's execution scope, so withdrawing and re-answering authorization cannot revive old payloads or results. Continuation explicitly depends on current authorization and selected deliveries; redoing a delivery invalidates a finish/pause answer recorded before closing the project. Resuming a paused or finished project opens a new continuation round without discarding unchanged work. Preparation scope alone does not change the meaning of independent model settings or already-built content; do not mechanically turn every incoming branch selector into a target dependency.

## Project Memo Side Channel

`memo_recorded` is a project-scoped, append-only recovery side channel. The message describes its own subject, related nodes, task IDs, paths, progress, and next step; a memo is not bound to a requirement node.

EventReducer may aggregate memos for renderer output, but BatchMarketingGraph, Compiler, Scheduler, and RequirementService must not use memos to build edges, evaluate conditions, satisfy nodes, or advance evidence versions. A memo is not a fact, user authorization, tool result, or completion evidence; verify it against the current active graph, facts, actual files, and tool state before resuming execution.

## Consumer-side Input Bindings

Dependency scheduling and evidence consumption are orthogonal. A structural or conditional edge may carry typed `InputUse` metadata describing how its consumer must use the prerequisite's current evidence. The binding is consumer-owned: the same producer may be read as source content by one node, passed as a tool argument by another, and used only as structured provenance by a third.

Supported modes are `read_content`, `structured_fact`, `tool_argument`, `present`, and `reference_only`. A binding declares its source evidence fields, purpose, required/optional strength, optional tool target, and optional resolution filter. Resolution filters must belong to the prerequisite's evidence contract. This permits one creative-research edge to require `read_content` from `data.path` when the resolution is `provided`, but consume `data.user_evidence` as a `structured_fact` when the resolution is `waived`.

`InputUse` never creates an edge, changes slot order, satisfies a node, or proves that the LLM made an external tool call. The dependency still owns readiness and revision propagation. The renderer preserves the binding under the owning `REQUIREMENT CONTEXT`, including when a shared payload is deduplicated and displayed as reused evidence. Required `read_content` tells the executor to read the actual file whenever its complete content is absent, partial, uncertain, or lost after compaction.

Non-gating current inputs use the same typed binding through `Requirement.supplemental_inputs`; they remain presentation inputs and do not enter Compiler scheduling. This avoids turning contextual material into false business dependencies while retaining one consumption vocabulary.

## Current-input Projection

Knowledge routing is presentation metadata, never a prerequisite edge or a fact. CLI derives the command-schema reading instruction from the available typed actions and emits its path once per complete detail view. Business references remain in node knowledge: media materialization includes common knowledge, generated runtime images also include external image knowledge, content choices include questionnaire/communication knowledge, and both frame routes include the source contract before generation. Runtime user-review assets restore the review references at that node; delegated choices do not add a new review gate. Test the actual active requirement index and explicitly selected/deduplicated READY details, not just whether a reference is mentioned somewhere in the repository.

In addition to static `knowledge_refs`, a ready requirement may declare typed `supplemental_inputs`. The renderer exposes `knowledge_refs` as mandatory `REQUIRED SPECS (MUST BE UNDERSTOOD FIRST)` and exposes the read-only input projection as `CURRENT INPUTS (USE AFTER SPECS)`. The specs are a knowledge and delivery contract, not proof that a file-read tool call occurred: the executor may reuse actual relevant spec content already present in its current context, but must read the listed file when that content is absent, partial, uncertain, or lost after compaction. For each ready requirement independently, the renderer merges that requirement's supplemental inputs with its direct prerequisites from the current active graph, resolves their current evidence resolutions and complete payloads from Facts, and includes them in that requirement's attributed context. The LLM therefore receives actual file paths, image lists, or structured facts rather than abstract IDs without losing which ready requirement owns them. Shared payloads may be printed once and referenced later by explicit owner ID; consumer-specific input uses are repeated in every owning context even when the payload itself is deduplicated.

`CURRENT INPUTS` never presents stale or erased evidence as current. A ready node's previous payload is shown separately under `HISTORY (not current evidence)` for verified file/task recovery; it cannot satisfy the node or authorize new execution.

`supplemental_inputs` does not enter the Compiler's topology, create dependency edges, change ready/satisfied/stale decisions, or serve as requirement evidence. Relationships that affect readiness, revision propagation, or branch selection must still be modeled as dependency rules. Only information that supplements context for semantic work belongs in this projection.

The renderer must not infer transport from filenames, extensions, or paths. A declared `InputUse` takes precedence for that consumer. Without one, the same `.md` input may need to be read into context, presented to the user, or—only when it is an executable mapping artifact—passed as `PromptPath`; the current node's `REQUIRED SPECS` determine which. A canonical `video_blueprint` is never executable transport. Those specs also determine whether media enters `ImageList` / `AudioList` / `VideoList` and how it is semantically numbered. `EXECUTION ORDER` makes establishing the spec knowledge precede input handling; the dynamic inputs cannot substitute for those fixed standards.

## View Selection Boundary

`batch_pm_view.py` consumes the complete existing Projection and its service-provided ready frontier. It never filters the graph before compilation, calls `Scheduler.ready` on a filtered graph, changes ordered slots, or changes acceptance/based_on. Requirement selection is a view over the single active graph.

Business requirements declare their opaque `display_group` and optional `ExecutionGroup(id, expand_ready_peers, metadata)`. Display grouping uses only these declared keys. Selection expands a declared execution group only when `expand_ready_peers` is true, intersecting its ID with the service-provided READY frontier; it never parses requirement IDs, routes, frame positions, or incoming consumer edges to discover a group. Group metadata is business-owned presentation data, not a dependency, slot, fact, basis input, or readiness rule. The business factory derives globally scoped frame groups once from the effective image model and frame spec, also supplying the existing edge context from that same declaration. Reordering or adding incoming consumers cannot redefine those groups.

Each requirement binds its current `actions` to descriptors from the finite business-owned `ACTIONS` registry. The CLI exports only the registry's `apply` subset for fact commands; lifecycle descriptors remain dedicated project commands. Rendering consumes these bound commands, schema references and notes without matching node prefixes or re-reading lifecycle choices. When grouped requirements allow different actions, each requirement retains its own action list. A close declaration reads its exact continuation producer to bind both the finish/pause command and short `what_lines`; project IDs and subject wording cannot select the lifecycle action.

`InputSelection` declares an already selected producer ID/version, field/index path, display label, qualifiers and display data. The frame factory selects its effective frame-spec entry and matching blueprint shot; the generic renderer only formats that declaration, optionally replacing the exact producer/version with its envelope evidence label. It does not index frame arrays or derive shot relationships. These selections, action descriptors and short instructions do not add edges, slots, facts or basis inputs, and do not claim that an external tool was called.

Before VIEW receives a projection, the business presentation factory binds each node's `what_lines` and `execution_order_lines`, plus shared `ExecutionGroup.what_lines`, using effective facts and the service's current recovery decisions. Runtime limits and accepted part durations use the same helpers as evidence validation; waiting nodes with missing producers carry no invented numeric constraints. The full graph and READY tuple reference the same bound nodes. VIEW only formats these plain-text declarations: node instructions stay in their requirement context, and shared instructions explicitly name the selected execution-group members. It never re-evaluates routes, blueprint counts, lifecycle choices, research history, rejection policy or runtime constraints to author WHAT or EXECUTION ORDER.

The same factory binds `Projection.context` with ordered index/detail header fields, including actual project and communication-language values and their display fallbacks. VIEW and CLI format these supplied labels and values without deriving project state or constructing language fact IDs. Selection preserves this context, and materialized envelopes include it unchanged. Context is presentation metadata only; it adds no facts, graph edges or basis inputs.

Without a selection, the view lists every focusable business requirement in the current active graph, grouped by READY, WAITING, or SATISFIED. It excludes GOAL/structural nodes, inactive history, and unmaterialized conditional branches. With one or more explicit IDs, it validates every requested item against the unchanged READY frontier and selects their full detail. Semantic type groups may share required guides and action schema, but every requirement retains an attributed context for CURRENT INPUTS, HISTORY, WHY, and identity-dependent WHAT; evidence deduplication records the first owning context instead of merging input sets. Route A frame selection expands only same-video, same-batch READY peers because they form one physical call; each frame retains its context while the execution WHAT remains shared. This does not recompute readiness or include blocked peers. Oversized indexes and details are written atomically as complete content-addressed envelopes under `/workspace/.tmp/batch_pm_views` online or the system temporary directory locally; stdout returns only a bounded locator. Materialized views are derived caches, not events, facts, focus, or authorization. Requirement selection creates no events or persistent focus, and never infers unmaterialized conditional branches.

## Business Object Chain

`information_understanding` first aggregates product facts, existing assets, markets, and batch intent. StoryMaster then defines the shared story and exact shot count; DirectionSet produces the specific Direction for each video.

Each video_blueprint depends on Storyboard Master and a concrete Direction and owns its path, shots, duration_ms, ratio and market_target. video_spec_definition reads it and declares images/audios/videos mappings with runtime-chosen IDs, semantic roles, constraints and allowed resolutions. There is no structured shot-to-material mapping.

`frame_spec_definition` is the visual-only per-shot visual description set between the confirmed video_spec and storyboard generation. It depends on the blueprint, media definition and visual mode, never on the image model or concrete files; it records each shot's frozen representative instant and its stable semantic image IDs. The blueprint's `shots` owns the count: exactly one frame per shot, `frame N` describing `shot N`, and its effective evidence is the gate that makes concrete `frame/<video>/<N>` nodes executable — without it the visual downstream never materializes while the definition itself stays READY-reachable. Only after its evidence is effective does the PM expand concrete frames, Route A/B call groups, storyboard manifest and overview structures.

video_spec is a contractless collection. It depends on definition, the three media groups and applicable product coverage. Each group depends on definition and expands its children only after that fact is effective. Children depend on definition, never on their aggregate. Unknown definition is a pending rule, not an empty inventory. Definition and blueprint drafts are provided; final acceptance belongs to package_confirmation.

A shared material_entries resolver defines IDs for both group expansion and consumer edges. Frame inputs expose exactly that frame's declared `image_ids` with semantic descriptions and resolution-specific uses; audio/video and non-selected images never enter an image-generation call. The matching entry's `visual_description` is the direct picture requirement; the blueprint supplies that shot's full script context. Source evidence is paths for provided media or explicit user_evidence for auto/waived. Process policies govern legal closures. PM does not inspect external tool calls.

## Canonical Plan and Execution Mappings

The package's reverse dependencies are shown below. A parent requires its children; sibling order schedules earlier slots first, without adding sibling edges. Repeated names denote the same shared DAG node, not copies.

```text
package_confirmation/P/V
├── video_blueprint/P/V [provided draft]
│   ├── story_master/P
│   └── direction/P/V
├── video_spec/P/V [structural collection]
│   ├── video_spec_definition/P/V [provided declaration]
│   │   └── video_blueprint/P/V
│   ├── images/P/V [definition -> cardinality]
│   │   └── image/P/V/<declared-id> × N -> video_spec_definition/P/V
│   ├── audios/P/V [definition -> cardinality]
│   │   └── audio/P/V/<declared-id> × N -> video_spec_definition/P/V
│   ├── videos/P/V [definition -> cardinality]
│   │   └── video/P/V/<declared-id> × N -> video_spec_definition/P/V
│   └── [definition has product_coverage] product_state_coverage/P/V
│       ├── video_blueprint/P/V + video_spec_definition/P/V
│       └── declared product image nodes
├── video_spec_definition/P/V + all declared media [input/presentation edges]
├── storyboard_mode/P/V
│   └── blueprint + completed video_spec + definition + declared media
└── [mode=visual] storyboard_overview/P/V
    └── storyboard_manifest/P/V
        ├── blueprint + video_spec + frame_spec_definition/P/V + image_model/P/V
        ├── frame_spec_definition/P/V
        │   └── blueprint + definition + storyboard_mode (visual)
        ├── image_model/P/V
        │   └── storyboard_mode/P/V
        └── [image_model selects route A/B; frame spec supplies count and groups]
            frame/P/V/frame-index × len(frame_spec.frames)
            └── frame spec (matching entry) + blueprint (covered shots context)
                + definition + mode + image_model + image/P/V/id × entry.image_ids
```

No image_model, frame_spec_definition or frame branch exists in script_only. Unknown definition blocks expansion; an explicit empty media mapping resolves an empty collection. Without an effective frame spec the visual downstream never materializes while the frame spec itself stays READY-reachable; the manifest's ordered slots place the frame-spec question before the image model without adding an edge between them. Route A groups `ceil(M/9)` batches and Route B one group per frame, both by frame position. Blueprint revision invalidates definition, frame spec and their dependents; a frame-spec revision invalidates all frames of that video and the visual/package/execution consumers while preserving blueprint, definition and material evidence; a single frame revision reopens only that frame's consumers. Replacing only a material preserves blueprint/definition and the frame spec, while invalidating their downstream consumers under the current strict version chain. Package acceptance records presentation and user evidence for these current versions, not another generated document.

video_blueprint is the sole model-independent story source, authored before material definition and mode. Visual adds image_model, concrete frames, manifest and overview. Script-only adds none of them. Package confirmation consumes blueprint, all current media evidence and mode, conditionally the overview; it records user acceptance and successful presentation without creating another package document.

Stable material IDs in the plan are semantic references, not final tool positions. `direct_payload` is a one-to-one compiler node depending on the confirmed package, generation model, plan, concrete materials, and visual overview when active. `runtime_manifest` is a one-to-many compiler node depending on the confirmed package, generation model, plan, and visual storyboard manifest when active. Each `part_input` then depends on the plan, its part specification, concrete runtime anchors/materials, and visual part sheet when active. Only these executable mapping nodes assign final `Image[N]`, `Audio[N]`, and `Video[N]` positions.

These are structural edges, not current-input decoration. Consequently a plan revision invalidates frames and all visual/execution projections, while a meaning-preserving frame replacement leaves the plan current and invalidates only its visual/package/execution consumers. A generation-model revision preserves the plan and remaps the affected direct/lowering artifacts.

## Runtime Identity Dependencies

PM derives lowering cardinality and inclusive duration bounds from the model and video_blueprint. It does not allocate milliseconds. The LLM reports the semantic partition through runtime manifest evidence; PM validates ordered 1..N, exact count, each duration within bounds, and exact total. Before that fact is effective, per-part durations are unavailable (not defaulted to equal shares). PartSpec reads its duration from the accepted manifest. Revising that manifest invalidates downstream part specs and their consumers through the existing versioned dependencies.

Each `part_spec` directly depends on its runtime manifest, video_spec_definition, and video blueprint. Its input bindings require reading both mapped and canonical content and consuming definition's images/audios/videos as structured facts. `materials` selects declared identity IDs, not file paths or final media positions. These are real prerequisites with version snapshots, not optional context.

Contractless reuse nodes never contribute their own historical evidence to effective facts. When an auto-backed asset becomes structural reuse after a source revision, its former generated-file evidence stays historical; consumers bind the current source facts instead.

Runtime anchor input bindings follow the PM-derived `strategy`, not the presence of `source`: both reuse and generation may name an original source. Generated anchors bind their own provided path to AudioList for voices or ImageList for visual assets; reused anchors bind the original concrete source instead. Part input, local preflight, and result contexts preserve the binding only for that anchor's applicable parts. Original auto evidence remains content authority, not a file or an exemption from the generated anchor.

runtime_materials expands the full original definition. Provided sources satisfy structural reuse nodes; every auto source requires its own concrete runtime_anchor regardless of continuity or part membership; waived supplemental product references produce no anchor. Original anchors depend on source, blueprint and generation model, not part specs.

There is no separate part_content or missing-anchor branch. Before initial delivery, an incomplete original inventory is corrected at its definition owner; part specs and final executable prompts read narrative and boundaries directly from the blueprint and runtime manifest.

part_input schedules runtime manifest, runtime_materials, final part_spec and continuity mapping. Ordered siblings do not become implicit edges. part_spec selects legal non-waived original IDs. InputUse binds actual files at input/preflight/result; runtime preparation does not mean every media file must enter every tool call.

Part membership revisions preserve original anchors and unrelated earlier results. True/false continuity round trips never resurrect stale evidence.

## Conditional Part Continuity

Every lowered result depends on its own `part_preflight`, which depends on that part's executable input. There is no shared lowering preflight. All results remain prerequisites of assembly without implicit sequential edges between siblings.

For N > 1, `part_input/N` unconditionally depends on `continuity_choice/N`. This LLM-reported process fact depends on the video blueprint, runtime manifest, and the two adjacent part specs, never on generated results or downstream inputs. Its `use_last_frame` must be a real boolean with a reason. Unknown leaves the conditional edge unresolved while the choice remains reachable; false produces no last-frame edge; true adds `part_input/N -> last_frame/N-1 -> part_result/N-1`. The first part has no choice or previous-frame dependency. Cross-part dependencies therefore point only toward smaller part numbers, including when all conditions are true.

The last frame is a concrete asset with its own provided path and source-result version. Its input use binds the source video to extraction and the resulting image to the following video's ImageList. Choice, frame, or input revisions preserve prior results; source-result revisions invalidate only active consumers of that result. Old downstream evidence cannot return merely by switching a condition back. PM supplies these contracts and does not audit external extraction or generation calls.

## Open Post-delivery Revision

The existing continuation_decision depends on execution_scope and its selected deliveries. It stays READY throughout free-form edits, presentation and feedback; no per-attempt fact, revision schema or revision round is added. Its supplemental inputs expose effective initial-generation artifacts as baseline context, not a latest-revision registry. Project memos provide optional recovery notes, not completion evidence.

Only an explicit lifecycle choice closes this requirement. finish requires nonempty actual user_evidence and the normal project finish command. pause remains a distinct lifecycle outcome. prepare/execute/extend concern other batch work; the former revise choice is rejected. Correcting workflow facts still uses erase, but freely editing an already delivered output does not erase its baseline dependencies.

## Program Layers

The implementation separates these layers:

1. `Event`: append-only input;
2. `EventReducer`: aggregates batch Facts, lifecycle and derived Direction evidence after a full replay;
3. `BatchMarketingGraph`: declares business requirements and supplies lifecycle seed values and a per-pass declaration factory to `evaluate_effective_facts`;
4. `evaluate_effective_facts`: computes the effective-fact fixed point from candidate Facts, an injected declaration factory, explicit non-evidence seed values and a root ID; it knows no batch node types, lifecycle keys or recovery rules;
5. `Compiler`: materializes each pass's active graph and checks for hidden fact producers, duplicate targets, and structural and producer-evaluation cycles;
6. `Scheduler`: calculates satisfaction, readiness and basis from slots and evidence versions;
7. `apply_batch_frame_recovery`: filters safety failures to their still-current dependency versions and prioritizes the first rejected frame in the generic READY frontier without changing topology or satisfaction;
8. `RequirementService`: remains the batch application service; it composes replay, the batch adapter, generic scheduling, recovery policy and then `bind_presentation`, and validates ready-only typed evidence, captures versions and withdraws facts;
9. `CommandFacade`: exposes only a finite set of business actions;
10. renderer: selects and formats the resulting projection and declared guidance without evaluating business routes or recovery policy.

The generic evaluator starts with no effective evidence, passes only the current effective facts to the declaration factory, and validates candidates against the resulting graph. It preserves the existing pass order, convergence limit and exact basis comparison. Seed values are supplied by the adapter, not copied or filtered by business key names inside the evaluator. Presentation binding runs only after effective facts and batch recovery have been established.