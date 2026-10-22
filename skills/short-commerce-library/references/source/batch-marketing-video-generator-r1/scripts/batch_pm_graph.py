
#!/usr/bin/env python3
"""Requirement-graph core for batch marketing video production.

This is a clean implementation of the agreed model:

* the graph starts at a never-completing GOAL;
* one dependency is one conditional edge plus one requirement node;
* a conditional edge that cannot yet be evaluated returns ``None``;
* graph construction evaluates every dependency slot and never stops at the
  first unfinished requirement;
* dependency-slot order affects focus scheduling only and never creates
  sibling-to-sibling graph edges;
* ready and inactive are projections, not persisted node states;
* cardinality and conditions are both dependency-rule evaluation.

The module intentionally contains no compatibility code for the previous PM.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
import unicodedata
from typing import Any, Callable, Iterable, Mapping, Sequence


MIN_VIDEO_DURATION_MS = 4_000
MAX_RUNTIME_PARTS = 64
MAX_PROJECT_MEMO_LENGTH = 4_000
ROUTE_A_MODELS = frozenset({
    "gpt_image_2", "gpt_image_2_5_flare", "gpt_image_2_5_sunburst", "seedream_5.0_pro",
})


class ModelError(ValueError):
    """The declared business model or its typed evidence is inconsistent."""


@dataclass(frozen=True)
class Evidence:
    resolution: str
    data: Mapping[str, Any] = field(default_factory=dict)
    based_on: Mapping[str, int] = field(default_factory=dict)


@dataclass
class Facts:
    """Output of event aggregation; graph construction never mutates it."""

    values: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def evidence_for(self, requirement_id: str) -> Evidence | None:
        return self.evidence.get(requirement_id)

    def evidence_version(self, requirement_id: str) -> int:
        versions = self.values.get("evidence_versions", {})
        if not isinstance(versions, Mapping):
            return 0
        value = versions.get(requirement_id, 0)
        return int(value) if isinstance(value, int) else 0


@dataclass(frozen=True)
class Event:
    """Immutable input consumed by the fact reducer."""

    kind: str
    subject: str
    data: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UnchangedFact:
    """Successful retry of a currently effective report; never an event."""

    sequence: int
    event: Event


def same_json_value(left: Any, right: Any) -> bool:
    """Exact payload comparison: unordered object keys, ordered lists, strict types."""
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return left.keys() == right.keys() and all(same_json_value(left[k], right[k]) for k in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(same_json_value(a, b) for a, b in zip(left, right))
    return type(left) is type(right) and left == right


@dataclass(frozen=True)
class ReducedState:
    """Event replay output with graph facts separate from recovery notes."""

    facts: Facts
    memos: tuple[str, ...]
    history: Mapping[str, Evidence] = field(default_factory=dict)


class EventReducer:
    """Aggregate the complete event stream before graph construction."""

    def reduce(self, events: Sequence[Event]) -> ReducedState:
        facts = Facts(values={
            "project_cycle": "01",
            "project_slots": {},
            "project_states": {},
            "evidence_versions": {},
        })
        memos: dict[str, list[str]] = defaultdict(list)
        rejected_frames: dict[str, Mapping[str, Any]] = {}
        history: dict[str, Evidence] = {}

        for version, event in enumerate(events, start=1):
            if event.kind == "project_created":
                if facts.get("active_project") is not None:
                    raise ModelError("cannot create a project while another project is active")
                project = graph_segment_id(
                    event.data.get("project"), "project_created.project"
                )
                cycle = str(facts.values.get("project_cycle", "01"))
                expected_subject = f"start_new_project/{cycle}"
                if event.subject != expected_subject:
                    raise ModelError(
                        f"project creation must satisfy {expected_subject}: {event.subject}"
                    )
                if project in facts.values["project_states"]:
                    raise ModelError(f"project already exists: {project}")
                facts.values["active_project"] = project
                facts.values["project_slots"][cycle] = project
                facts.values["project_states"][project] = {
                    "preparation_round": "01",
                    "execution_round": "01",
                    "continuation_round": "01",
                    "lifecycle": "active",
                }
                facts.evidence[expected_subject] = Evidence(
                    resolution="created",
                    data={"project": project},
                    based_on=dict(event.data.get("based_on", {})),
                )
                facts.values["evidence_versions"][expected_subject] = version
                facts.values["project_cycle"] = f"{int(cycle) + 1:02d}"
                continue

            if event.kind == "project_resumed":
                if facts.get("active_project") is not None:
                    raise ModelError("cannot resume a project while another project is active")
                project = graph_segment_id(
                    event.data.get("project"), "project_resumed.project"
                )
                cycle = str(facts.values.get("project_cycle", "01"))
                expected_subject = f"start_new_project/{cycle}"
                if event.subject != expected_subject:
                    raise ModelError(
                        f"project resume must satisfy {expected_subject}: {event.subject}"
                    )
                state = facts.values["project_states"].get(project)
                if not isinstance(state, dict):
                    raise ModelError(f"cannot resume unknown project: {project}")
                facts.values["active_project"] = project
                facts.values["project_slots"][cycle] = project
                continuation = str(state["continuation_round"])
                if f"continuation_decision/{project}/{continuation}" in facts.evidence:
                    state["continuation_round"] = f"{int(continuation) + 1:02d}"
                state["lifecycle"] = "active"
                facts.evidence[expected_subject] = Evidence(
                    resolution="resumed",
                    data={"project": project},
                    based_on=dict(event.data.get("based_on", {})),
                )
                facts.values["evidence_versions"][expected_subject] = version
                facts.values["project_cycle"] = f"{int(cycle) + 1:02d}"
                continue

            if event.kind == "requirement_resolved":
                resolution = required_text(
                    event.data.get("resolution"),
                    f"{event.kind}.resolution",
                )
                payload = event.data.get("evidence", {})
                if not isinstance(payload, Mapping):
                    raise ModelError(f"{event.kind}.evidence must be a mapping")
                based_on = event.data.get("based_on")
                if not isinstance(based_on, Mapping) or any(
                    not isinstance(key, str) or not key
                    or type(value) is not int or not 0 < value < version
                    for key, value in based_on.items()
                ):
                    raise ModelError(f"{event.kind}.based_on must contain prior fact versions")
                facts.evidence[event.subject] = Evidence(
                    resolution=resolution,
                    data=dict(payload),
                    based_on=dict(based_on),
                )
                history[event.subject] = facts.evidence[event.subject]
                facts.values["evidence_versions"][event.subject] = version
                rejected_frames.pop(event.subject, None)
                self._derive_evidence(facts, event.subject, version)
                self._apply_continuation(facts, event.subject, payload)
                continue

            if event.kind == "requirement_erased":
                facts.evidence.pop(event.subject, None)
                facts.values["evidence_versions"].pop(event.subject, None)
                rejected_frames.pop(event.subject, None)
                if event.subject.startswith("direction_set/"):
                    self._clear_directions(facts, event.subject.split("/", 1)[1])
                continue

            if event.kind == "frame_rejected":
                rejected_frames[event.subject] = dict(event.data)
                continue

            if event.kind == "frame_retry_authorized":
                rejected_frames.pop(event.subject, None)
                continue

            if event.kind == "memo_recorded":
                project = facts.get("active_project")
                if project is None:
                    raise ModelError("cannot record a memo without an active project")
                if event.subject != f"project/{project}":
                    raise ModelError(
                        f"memo does not belong to active project: {event.subject}"
                    )
                message = required_text(event.data.get("message"), "memo.message")
                if len(message) > MAX_PROJECT_MEMO_LENGTH:
                    raise ModelError(
                        f"memo.message exceeds {MAX_PROJECT_MEMO_LENGTH} characters"
                    )
                memos[project].append(message)
                continue

            if event.kind in {"project_finished", "project_paused"}:
                project = facts.get("active_project")
                if project is None:
                    raise ModelError("cannot close a project when none is active")
                if event.subject != f"project_goal/{project}":
                    raise ModelError(f"project close does not belong to active project: {event.subject}")
                state = facts.values["project_states"][project]
                state["lifecycle"] = (
                    "paused" if event.kind == "project_paused" else "finished"
                )
                # The same event deterministically seals the current round's
                # project_close node: its evidence binds the continuation fact
                # version that authorized the close, and stays valid after the
                # active project is cleared.
                continuation_round = str(state.get("continuation_round", "01"))
                close_node = f"project_close/{project}/{continuation_round}"
                continuation_node = f"continuation_decision/{project}/{continuation_round}"
                continuation_version = facts.values["evidence_versions"].get(
                    continuation_node, 0
                )
                facts.evidence[close_node] = Evidence(
                    resolution="closed",
                    data={"lifecycle": state["lifecycle"]},
                    based_on={continuation_node: continuation_version}
                    if continuation_version else {},
                )
                history[close_node] = facts.evidence[close_node]
                facts.values["evidence_versions"][close_node] = version
                facts.values.pop("active_project", None)
                facts.values.pop("continuation_choice", None)
                facts.values.pop("continuation_subject", None)
                continue

            raise ModelError(f"unknown event kind: {event.kind}")

        facts.values["rejected_frames"] = rejected_frames
        active = facts.get("active_project")
        return ReducedState(
            facts=facts,
            memos=tuple(memos.get(str(active), ())) if active else (),
            history=history,
        )

    @staticmethod
    def _apply_continuation(
        facts: Facts,
        subject: str,
        payload: Mapping[str, Any],
    ) -> None:
        if not subject.startswith("continuation_decision/"):
            return
        parts = subject.split("/")
        if len(parts) != 3:
            raise ModelError(f"invalid continuation requirement ID: {subject}")
        project = facts.get("active_project")
        if project != parts[1]:
            raise ModelError(f"continuation does not belong to active project: {subject}")
        state = facts.values["project_states"][project]
        choice = continuation_choice(payload.get("choice"))
        facts.values["continuation_choice"] = choice
        facts.values["continuation_subject"] = subject
        if choice in {"prepare", "extend"}:
            current = positive_integer(
                state.get("preparation_round", "01"),
                "preparation_round",
            )
            state["preparation_round"] = f"{current + 1:02d}"
        elif choice == "execute":
            current = positive_integer(
                state.get("execution_round", "01"),
                "execution_round",
            )
            state["execution_round"] = f"{current + 1:02d}"
        elif choice not in {"finish", "pause"}:
            raise ModelError(f"invalid continuation choice: {choice}")
        if choice not in {"finish", "pause"}:
            current = positive_integer(
                state.get("continuation_round", "01"),
                "continuation_round",
            )
            state["continuation_round"] = f"{current + 1:02d}"

    @staticmethod
    def _clear_directions(facts: Facts, project: str) -> None:
        for node_id in list(facts.evidence):
            if node_id.startswith(f"direction/{project}/"):
                facts.evidence.pop(node_id)
                facts.values["evidence_versions"].pop(node_id, None)

    @staticmethod
    def _derive_evidence(facts: Facts, subject: str, version: int) -> None:
        """Derive typed business-object evidence, never topology."""

        if not subject.startswith("direction_set/"):
            return
        direction_set = facts.evidence[subject]
        if direction_set.resolution != "confirmed":
            return
        project = subject.split("/", 1)[1]
        directions = direction_entries(direction_set.data.get("directions"), subject)
        EventReducer._clear_directions(facts, project)
        for video_id, direction in directions.items():
            facts.evidence[f"direction/{project}/{video_id}"] = Evidence(
                resolution="confirmed",
                data=dict(direction),
                based_on={subject: version},
            )
            facts.values["evidence_versions"][f"direction/{project}/{video_id}"] = version


@dataclass(frozen=True)
class EvidenceContract:
    name: str
    resolutions: frozenset[str]

    def is_satisfied_by(self, evidence: Evidence | None) -> bool:
        return evidence is not None and evidence.resolution in self.resolutions


INPUT_USE_MODES = frozenset({
    "read_content",
    "structured_fact",
    "tool_argument",
    "present",
    "reference_only",
})


@dataclass(frozen=True)
class InputUse:
    """Consumer-side instructions for one prerequisite evidence payload.

    Input use is orthogonal to dependency scheduling. It tells the renderer how
    a consumer must use evidence after that evidence has become current; it
    never creates readiness, satisfaction, or revision semantics by itself.
    """

    mode: str
    purpose: str
    fields: tuple[str, ...] = ()
    target: str | None = None
    required: bool = True
    resolutions: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.mode not in INPUT_USE_MODES:
            raise ModelError(f"unknown input-use mode: {self.mode}")
        if not isinstance(self.purpose, str) or not self.purpose.strip():
            raise ModelError("input-use purpose must be non-empty")
        if any(not isinstance(item, str) or not item.strip() for item in self.fields):
            raise ModelError("input-use fields must be non-empty strings")
        if self.mode in {"read_content", "tool_argument", "present"} and len(self.fields) != 1:
            raise ModelError(f"{self.mode} input use requires exactly one source field")
        if self.mode == "tool_argument" and (
            not isinstance(self.target, str) or not self.target.strip()
        ):
            raise ModelError("tool_argument input use requires a target")
        if self.mode != "tool_argument" and self.target is not None:
            raise ModelError(f"{self.mode} input use cannot declare a tool target")
        if any(
            not isinstance(item, str) or not item.strip()
            for item in self.resolutions
        ):
            raise ModelError("input-use resolutions must be non-empty strings")

    def applies_to(self, resolution: str) -> bool:
        return not self.resolutions or resolution in self.resolutions


def read_content(
    field_name: str,
    *,
    purpose: str,
    resolutions: Sequence[str] = (),
    required: bool = True,
) -> InputUse:
    return InputUse(
        mode="read_content",
        purpose=purpose,
        fields=(field_name,),
        required=required,
        resolutions=frozenset(resolutions),
    )


def structured_fact(
    *field_names: str,
    purpose: str,
    resolutions: Sequence[str] = (),
    required: bool = True,
) -> InputUse:
    return InputUse(
        mode="structured_fact",
        purpose=purpose,
        fields=tuple(field_names),
        required=required,
        resolutions=frozenset(resolutions),
    )


def tool_argument(
    field_name: str,
    *,
    target: str,
    purpose: str,
    resolutions: Sequence[str] = (),
    required: bool = True,
) -> InputUse:
    return InputUse(
        mode="tool_argument",
        purpose=purpose,
        fields=(field_name,),
        target=target,
        required=required,
        resolutions=frozenset(resolutions),
    )


def present(
    field_name: str,
    *,
    purpose: str,
    resolutions: Sequence[str] = (),
    required: bool = True,
) -> InputUse:
    return InputUse(
        mode="present",
        purpose=purpose,
        fields=(field_name,),
        required=required,
        resolutions=frozenset(resolutions),
    )


@dataclass(frozen=True)
class InputBinding:
    """A non-gating current input owned by one consumer requirement."""

    requirement_id: str
    uses: tuple[InputUse, ...] = ()


@dataclass(frozen=True)
class EdgeTarget:
    requirement_id: str
    context: Mapping[str, Any] = field(default_factory=dict)
    input_uses: tuple[InputUse, ...] = ()


@dataclass(frozen=True)
class Evaluation:
    """A dependency rule result.

    ``None`` from a resolver is represented by ``known=False``. An explicitly
    false condition is ``known=True`` with zero targets.
    """

    known: bool
    targets: tuple[EdgeTarget, ...] = ()

    @classmethod
    def unknown(cls) -> "Evaluation":
        return cls(known=False)

    @classmethod
    def of(cls, targets: Iterable[EdgeTarget] = ()) -> "Evaluation":
        return cls(known=True, targets=tuple(targets))


Resolver = Callable[[Facts], Evaluation]


@dataclass(frozen=True)
class Dependency:
    name: str
    resolver: Resolver
    fact_producers: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionGroup:
    """Business-declared execution unit; never a dependency or readiness rule."""

    id: str
    expand_ready_peers: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)
    what_lines: tuple[str, ...] = ()


@dataclass(frozen=True)
class ActionSpec:
    """Finite business command descriptor, shared by declaration and execution."""

    prefix: str
    resolution: str
    command: str
    operation: str = "apply"
    schema_ref: str | None = "references/evidence-and-commands.md"
    notes: tuple[str, ...] = ()

    def accepts(self, subject: str) -> bool:
        return subject == self.prefix or subject.startswith(f"{self.prefix}/")


ACTIONS: dict[str, ActionSpec] = {
    name: ActionSpec(prefix, resolution, name)
    for name, prefix, resolution in (
        ("report-language", "communication_language", "reported"),
        ("confirm-information", "information_understanding", "confirmed"),
        ("provide-research", "creative_research", "provided"),
        ("waive-research", "creative_research", "waived"),
        ("confirm-story", "story_master", "confirmed"),
        ("confirm-directions", "direction_set", "confirmed"),
        ("select-preparation", "preparation_scope", "selected"),
        ("report-image-model", "image_model", "reported"),
        ("provide-frame-spec-definition", "frame_spec_definition", "provided"),
        ("provide-video-spec-definition", "video_spec_definition", "provided"),
        ("confirm-product-state-coverage", "product_state_coverage", "confirmed"),
        ("select-storyboard-mode", "storyboard_mode", "selected"),
        ("provide-image", "image", "provided"),
        ("provide-audio", "audio", "provided"),
        ("provide-video", "video", "provided"),
        ("delegate-image", "image", "auto"),
        ("delegate-audio", "audio", "auto"),
        ("delegate-video", "video", "auto"),
        ("waive-image", "image", "waived"),
        ("waive-audio", "audio", "waived"),
        ("waive-video", "video", "waived"),
        ("provide-frame", "frame", "provided"),
        ("provide-storyboard-manifest", "storyboard_manifest", "provided"),
        ("derive-storyboard-overview", "storyboard_overview", "derived"),
        ("provide-video-blueprint", "video_blueprint", "provided"),
        ("confirm-package", "package_confirmation", "confirmed"),
        ("select-execution", "execution_scope", "selected"),
        ("report-video-model", "generation_model", "reported"),
        ("provide-direct-payload", "direct_payload", "provided"),
        ("provide-runtime-manifest", "runtime_manifest", "provided"),
        ("confirm-part-spec", "part_spec", "confirmed"),
        ("provide-runtime-anchor", "runtime_anchor", "provided"),
        ("derive-part-sheet", "part_sheet", "derived"),
        ("provide-part-input", "part_input", "provided"),
        ("report-continuity-choice", "continuity_choice", "reported"),
        ("provide-last-frame", "last_frame", "provided"),
        ("pass-part-preflight", "part_preflight", "passed"),
        ("pass-preflight", "preflight", "passed"),
        ("record-direct-result", "direct_result", "generated"),
        ("record-part-result", "part_result", "generated"),
        ("record-assembled-result", "assembled_result", "generated"),
        ("present-delivery", "delivery", "presented"),
        ("select-continuation", "continuation_decision", "selected"),
    )
}
ACTIONS.update({
    "project-create": ActionSpec(
        "start_new_project", "created", "project create --project-id <new-project-id>",
        operation="project", schema_ref=None,
    ),
    "project-resume": ActionSpec(
        "start_new_project", "resumed", "project resume --project-id <paused-project-id>",
        operation="project", schema_ref=None,
    ),
    **{
        f"project-{decision}": ActionSpec(
            "project_close", "closed", f"python3 scripts/batch_pm.py project {decision}",
            operation="project", schema_ref=None,
            notes=("Then refresh project get-next-action.",),
        ) for decision in ("finish", "pause")
    },
})


@dataclass(frozen=True)
class InputSelection:
    """An already selected producer field/entry; never an edge or evidence."""

    producer_id: str
    producer_version: int | None
    path: tuple[str | int, ...]
    label: str
    qualifiers: Mapping[str, Any] = field(default_factory=dict)
    display_data: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Requirement:
    id: str
    kind: str
    subject: str
    contract: EvidenceContract | None
    deps: tuple[Dependency, ...] = ()
    focusable: bool = True
    never_complete: bool = False
    guidance: Mapping[str, Any] = field(default_factory=dict)
    supplemental_inputs: tuple[InputBinding, ...] = ()
    display_group: str | None = None
    execution_group: ExecutionGroup | None = None
    actions: tuple[ActionSpec, ...] = ()
    input_selections: tuple[InputSelection, ...] = ()
    what_lines: tuple[str, ...] = ()
    execution_order_lines: tuple[str, ...] = ()


@dataclass(frozen=True)
class Edge:
    consumer: str
    prerequisite: str
    slot: int
    rule: str
    context: Mapping[str, Any] = field(default_factory=dict)
    input_uses: tuple[InputUse, ...] = ()


@dataclass
class Graph:
    root: str
    nodes: dict[str, Requirement] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    pending_rules: list[tuple[str, int, str]] = field(default_factory=list)

    def outgoing(self) -> dict[str, list[Edge]]:
        result: dict[str, list[Edge]] = defaultdict(list)
        for edge in self.edges:
            result[edge.consumer].append(edge)
        for edges in result.values():
            edges.sort(key=lambda edge: (edge.slot, edge.prerequisite))
        return dict(result)


def edge(
    requirement_id: str,
    *,
    input_uses: Sequence[InputUse] = (),
    **context: Any,
) -> EdgeTarget:
    return EdgeTarget(
        requirement_id=requirement_id,
        context=context,
        input_uses=tuple(input_uses),
    )


def requires(
    name: str,
    *requirement_ids: str,
    input_uses: Sequence[InputUse] = (),
) -> Dependency:
    return Dependency(
        name=name,
        resolver=lambda _facts: Evaluation.of(
            edge(item, input_uses=input_uses) for item in requirement_ids
        ),
    )


def conditional(
    name: str,
    *,
    fact_producers: Sequence[str],
    resolver: Resolver,
) -> Dependency:
    return Dependency(name=name, resolver=resolver, fact_producers=tuple(fact_producers))


def contract(name: str, *resolutions: str) -> EvidenceContract:
    return EvidenceContract(name=name, resolutions=frozenset(resolutions))


class Compiler:
    """Build the active graph by evaluating all reachable dependency rules."""

    def __init__(self, facts: Facts, declare: Callable[[str], Requirement]):
        self.facts = facts
        self.declare = declare

    def build(self, root: str = "GOAL") -> Graph:
        graph = Graph(root=root)
        evaluated: list[tuple[str, int, Dependency]] = []

        def visit(requirement_id: str) -> None:
            if requirement_id in graph.nodes:
                return
            requirement = self.declare(requirement_id)
            graph.nodes[requirement_id] = requirement
            for slot, dependency in enumerate(requirement.deps):
                evaluation = (
                    Evaluation.unknown()
                    if any(self.facts.evidence_for(producer) is None
                           for producer in dependency.fact_producers)
                    else dependency.resolver(self.facts)
                )
                evaluated.append((requirement_id, slot, dependency))
                if not evaluation.known:
                    graph.pending_rules.append((requirement_id, slot, dependency.name))
                    continue
                seen: set[str] = set()
                for target in evaluation.targets:
                    if target.requirement_id in seen:
                        raise ModelError(
                            f"{requirement_id}:{dependency.name} produced duplicate "
                            f"requirement {target.requirement_id}"
                        )
                    seen.add(target.requirement_id)
                    graph.edges.append(
                        Edge(
                            consumer=requirement_id,
                            prerequisite=target.requirement_id,
                            slot=slot,
                            rule=dependency.name,
                            context=dict(target.context),
                            input_uses=tuple(target.input_uses),
                        )
                    )
                    visit(target.requirement_id)

        visit(root)
        self._check_fact_producers(graph, evaluated)
        self._check_cycles(graph)
        self._check_input_uses(graph)
        return graph

    @staticmethod
    def _check_input_uses(graph: Graph) -> None:
        def validate(
            consumer: str,
            prerequisite: str,
            uses: Sequence[InputUse],
        ) -> None:
            if not uses:
                return
            prerequisite_node = graph.nodes.get(prerequisite)
            if prerequisite_node is None:
                raise ModelError(
                    f"{consumer} declares an input binding for unknown requirement {prerequisite}"
                )
            contract = prerequisite_node.contract
            for use in uses:
                if use.resolutions and contract is None:
                    raise ModelError(
                        f"{consumer} input binding for contractless {prerequisite} "
                        "cannot select evidence resolutions"
                    )
                if contract is not None and not use.resolutions.issubset(contract.resolutions):
                    unknown = sorted(use.resolutions - contract.resolutions)
                    raise ModelError(
                        f"{consumer} input binding for {prerequisite} selects unsupported "
                        f"resolutions: {unknown}"
                    )

        for active_edge in graph.edges:
            validate(
                active_edge.consumer,
                active_edge.prerequisite,
                active_edge.input_uses,
            )
        for requirement in graph.nodes.values():
            for binding in requirement.supplemental_inputs:
                validate(requirement.id, binding.requirement_id, binding.uses)

    @staticmethod
    def _check_fact_producers(
        graph: Graph,
        evaluated: Sequence[tuple[str, int, Dependency]],
    ) -> None:
        for owner, _slot, dependency in evaluated:
            for producer in dependency.fact_producers:
                if producer not in graph.nodes:
                    raise ModelError(
                        f"{owner}:{dependency.name} reads evidence from {producer}, but "
                        "that producer is hidden behind the edge it controls"
                    )

    @staticmethod
    def _check_cycles(graph: Graph) -> None:
        outgoing = graph.outgoing()
        visiting: list[str] = []
        visited: set[str] = set()

        def walk(node_id: str) -> None:
            if node_id in visiting:
                start = visiting.index(node_id)
                cycle = visiting[start:] + [node_id]
                raise ModelError(f"dependency cycle: {' -> '.join(cycle)}")
            if node_id in visited:
                return
            visiting.append(node_id)
            for active_edge in outgoing.get(node_id, []):
                walk(active_edge.prerequisite)
            # Evaluation dependencies must be acyclic too, even for zero/unknown edges.
            for dependency in graph.nodes[node_id].deps:
                for producer in dependency.fact_producers:
                    walk(producer)
            visiting.pop()
            visited.add(node_id)

        walk(graph.root)


class Scheduler:
    """Project ready nodes from a complete active graph.

    It follows the first dependency slot that still contains an unsatisfied
    active requirement. It does not add structural edges between slots.
    """

    def __init__(self, graph: Graph, facts: Facts):
        self.graph = graph
        self.facts = facts
        self.outgoing = graph.outgoing()
        self._satisfied: dict[str, bool] = {}
        self.pending = {owner for owner, _slot, _rule in graph.pending_rules}

    def prerequisite_ids(self, requirement_id: str) -> set[str]:
        return {
            edge.prerequisite for edge in self.outgoing.get(requirement_id, [])
        } | {
            producer
            for dependency in self.graph.nodes[requirement_id].deps
            for producer in dependency.fact_producers
        }

    def basis(self, requirement_id: str) -> dict[str, int]:
        """Snapshot prerequisite facts, including selectors with zero targets."""
        result: dict[str, int] = {}
        visited: set[str] = set()

        def collect(node_id: str) -> None:
            if node_id in visited:
                return
            visited.add(node_id)
            if self.graph.nodes[node_id].contract is not None:
                version = self.facts.evidence_version(node_id)
                if version:
                    result[node_id] = version
            else:
                for prerequisite in self.prerequisite_ids(node_id):
                    collect(prerequisite)

        for prerequisite in self.prerequisite_ids(requirement_id):
            collect(prerequisite)
        return result

    def satisfied(self, requirement_id: str) -> bool:
        if requirement_id in self._satisfied:
            return self._satisfied[requirement_id]
        requirement = self.graph.nodes[requirement_id]
        prerequisites = self.prerequisite_ids(requirement_id)
        dependencies_satisfied = all(
            self.satisfied(prerequisite) for prerequisite in prerequisites
        )
        if requirement.never_complete or requirement_id in self.pending:
            result = False
        elif requirement.contract is not None:
            evidence_valid = requirement.contract.is_satisfied_by(
                self.facts.evidence_for(requirement_id)
            )
            evidence = self.facts.evidence_for(requirement_id)
            result = (
                dependencies_satisfied
                and evidence_valid
                and evidence is not None
                and dict(evidence.based_on) == self.basis(requirement_id)
            )
        else:
            result = dependencies_satisfied
        self._satisfied[requirement_id] = result
        return result


    def ready(self) -> list[Requirement]:
        ready: list[Requirement] = []
        emitted: set[str] = set()
        walking: set[str] = set()

        def descend(requirement_id: str) -> None:
            if self.satisfied(requirement_id):
                return
            if requirement_id in walking:
                raise ModelError(f"scheduler cycle at {requirement_id}")
            walking.add(requirement_id)
            requirement = self.graph.nodes[requirement_id]
            slots: dict[int, list[Edge]] = defaultdict(list)
            for active_edge in self.outgoing.get(requirement_id, []):
                slots[active_edge.slot].append(active_edge)

            current: list[Edge] | None = None
            for slot in sorted(slots):
                unresolved = [
                    active_edge
                    for active_edge in slots[slot]
                    if not self.satisfied(active_edge.prerequisite)
                ]
                if unresolved:
                    current = unresolved
                    break

            if current:
                for active_edge in current:
                    descend(active_edge.prerequisite)
            elif (
                requirement.focusable and requirement_id not in emitted
                and requirement_id not in self.pending
                and all(self.satisfied(item)
                        for item in self.prerequisite_ids(requirement_id))
            ):
                ready.append(requirement)
                emitted.add(requirement_id)
            walking.remove(requirement_id)

        descend(self.graph.root)
        return ready


def evaluate_effective_facts(
    candidates: Facts,
    declaration_factory: Callable[[Facts], Callable[[str], Requirement]],
    *,
    seed_values: Mapping[str, Any],
    root: str = "GOAL",
) -> tuple[Graph, Facts]:
    """Grow effective facts using declarations made only from the current closure.

    The adapter explicitly supplies non-evidence values and a fresh declaration
    callable for each pass. Historical candidates are visible only to validation,
    never to declarations or conditional resolvers. All reachable slots take
    part on every pass; their scheduling order does not affect this closure.
    """
    visible = Facts(values={**seed_values, "evidence_versions": {}})
    for _pass in range(len(candidates.evidence) + 2):
        graph = Compiler(visible, declaration_factory(visible)).build(root)
        scheduler = Scheduler(graph, candidates)
        effective = {
            node_id: candidates.evidence[node_id]
            for node_id in graph.nodes
            if graph.nodes[node_id].contract is not None
            and node_id in candidates.evidence and scheduler.satisfied(node_id)
        }
        if effective == visible.evidence:
            return graph, visible
        visible = Facts(
            values={**seed_values, "evidence_versions": {
                node_id: candidates.evidence_version(node_id) for node_id in effective
            }},
            evidence=effective,
        )
    raise ModelError("effective fact evaluation did not converge")


def apply_batch_frame_recovery(
    scheduler: Scheduler,
    ready: Sequence[Requirement],
    rejected_frames: Mapping[str, Mapping[str, Any]],
) -> tuple[Requirement, ...]:
    """Keep current batch safety failures and prioritize one READY rejected frame.

    This business policy runs after effective-fact evaluation and generic
    scheduling. It does not alter topology, satisfaction or dependency versions.
    """
    facts = scheduler.facts
    # Safety failures only apply to the dependency versions under which they occurred.
    facts.values["rejected_frames"] = {
        node_id: reason
        for node_id, reason in rejected_frames.items()
        if node_id in scheduler.graph.nodes
        and node_id not in scheduler.pending
        and all(scheduler.satisfied(dep) for dep in scheduler.prerequisite_ids(node_id))
        and reason.get("based_on") == scheduler.basis(node_id)
        and facts.evidence_for(node_id) is None
    }
    rejected_ready = [item for item in ready if item.id in facts.values["rejected_frames"]]
    return tuple(rejected_ready[:1] if rejected_ready else ready)


@dataclass(frozen=True)
class ProjectionContext:
    """Already bound header fields; labels and values are opaque to VIEW."""

    index_fields: tuple[tuple[str, str], ...] = ()
    detail_fields: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Projection:
    facts: Facts
    memos: tuple[str, ...]
    graph: Graph
    ready: tuple[Requirement, ...]
    history: Mapping[str, Evidence] = field(default_factory=dict)
    context: ProjectionContext = field(default_factory=ProjectionContext)


@dataclass(frozen=True)
class EraseEligibility:
    """Read-only eligibility for withdrawing a fact; reason explains rejection."""

    allowed: bool
    reason: str | None = None


class RequirementService:
    """Batch application service validating mutations against its current projection.

    Public CLI handlers may wrap this service with domain-specific arguments,
    but no handler may bypass its requirement contract or readiness checks.
    """

    def __init__(self, events: Sequence[Event] = ()):
        self.events = list(events)

    def projection(self) -> Projection:
        reduced = EventReducer().reduce(self.events)
        graph, facts = BatchMarketingGraph(reduced.facts).project()
        scheduler = Scheduler(graph, facts)
        ready = apply_batch_frame_recovery(
            scheduler, scheduler.ready(), reduced.facts.get("rejected_frames", {}),
        )
        from batch_pm_presentation import bind_presentation
        return bind_presentation(Projection(
            facts=facts,
            memos=reduced.memos,
            graph=graph,
            ready=ready,
            history=reduced.history,
        ))

    def resolve(
        self,
        requirement_id: str,
        resolution: str,
        evidence: Mapping[str, Any] | None = None,
    ) -> Event | UnchangedFact:
        projection = self.projection()
        candidate = Evidence(resolution=resolution, data=dict(evidence or {}))
        current = projection.facts.evidence_for(requirement_id)
        version = projection.facts.evidence_version(requirement_id)
        if current is not None and 0 < version <= len(self.events):
            original = self.events[version - 1]
            # Effective evidence already passed current dependency/version checks.
            # Exclude derived and bootstrap facts, even if their payloads match.
            if (original.kind == "requirement_resolved" and original.subject == requirement_id
                    and current.resolution == candidate.resolution
                    and same_json_value(current.data, candidate.data)):
                return UnchangedFact(version, original)
        ready_ids = {item.id for item in projection.ready}
        if requirement_id not in ready_ids:
            raise ModelError(
                f"requirement is not ready: {requirement_id}; run project get-next-action. "
                "To replace an accepted fact, erase its semantic owner first, then follow READY."
            )
        requirement = projection.graph.nodes[requirement_id]
        if requirement_id in projection.facts.get("rejected_frames", {}):
            raise ModelError(
                f"{requirement_id} has a safety rejection; obtain the user's safe-retry "
                "choice and use frame retry, or erase storyboard_mode and choose script_only"
            )
        if requirement.contract is None:
            raise ModelError(f"requirement has no evidence contract: {requirement_id}")
        if not requirement.contract.is_satisfied_by(candidate):
            allowed = ", ".join(sorted(requirement.contract.resolutions))
            raise ModelError(
                f"{requirement_id} does not accept resolution {resolution!r}; allowed: {allowed}"
            )
        validate_requirement_evidence(requirement, candidate, projection.facts)
        event = Event(
            kind="requirement_resolved",
            subject=requirement_id,
            data={
                "resolution": resolution,
                "evidence": dict(evidence or {}),
                "based_on": Scheduler(projection.graph, projection.facts).basis(requirement_id),
            },
        )
        self.events.append(event)
        try:
            self.projection()
        except Exception:
            self.events.pop()
            raise
        return event

    def erase_eligibility(self, requirement_id: str) -> EraseEligibility:
        return self.erase_eligibilities((requirement_id,))[requirement_id]

    def erase_eligibilities(self, requirement_ids: Iterable[str]) -> dict[str, EraseEligibility]:
        """Inspect active or inactive subjects without mutating or probing erase."""
        reduced = EventReducer().reduce(self.events)
        return {node_id: self._erase_eligibility(node_id, reduced) for node_id in requirement_ids}

    @staticmethod
    def _erase_eligibility(requirement_id: str, reduced: ReducedState) -> EraseEligibility:
        raw = reduced.facts
        active = raw.get("active_project")
        if active is None:
            return EraseEligibility(False, "erase requires an active project; resume it first")
        try:
            owner, kind = requirement_owner(requirement_id)
        except ModelError as error:
            return EraseEligibility(False, str(error))
        if kind == "unknown":
            return EraseEligibility(False,
                f"unknown requirement type; cannot erase: {requirement_id}. "
                "No event was written."
            )
        if kind == "lifecycle":
            return EraseEligibility(False,
                "lifecycle control facts are not erasable through the generic "
                f"erase command: {requirement_id}. No event was written."
            )
        if owner != active:
            return EraseEligibility(False,
                f"Cannot erase {requirement_id} while project {active} is active. "
                "No event was written. Refresh project get-next-action and use "
                "the current project's requirement IDs. Resuming another project "
                "requires explicit user intent."
            )
        if requirement_id not in reduced.history or raw.evidence_for(requirement_id) is None:
            return EraseEligibility(False, f"no accepted fact to erase: {requirement_id}")
        return EraseEligibility(True)

    def erase(self, requirement_id: str, reason: str) -> Event:
        """Withdraw one accepted fact without deleting its files or downstream history."""
        self.projection()
        reduced = EventReducer().reduce(self.events)
        eligibility = self._erase_eligibility(requirement_id, reduced)
        if not eligibility.allowed:
            raise ModelError(eligibility.reason)
        raw = reduced.facts
        reason = required_text(reason, "erase.reason")
        event = Event(
            kind="requirement_erased",
            subject=requirement_id,
            data={"reason": reason, "withdrawn_version": raw.evidence_version(requirement_id)},
        )
        self.events.append(event)
        try:
            self.projection()
        except Exception:
            self.events.pop()
            raise
        return event

    def reject_frame(self, requirement_id: str, reason: Mapping[str, Any]) -> Event:
        projection = self.projection()
        ready_ids = {item.id for item in projection.ready}
        if not requirement_id.startswith("frame/") or requirement_id not in ready_ids:
            raise ModelError(f"frame is not ready: {requirement_id}")
        event = Event(
            kind="frame_rejected", subject=requirement_id,
            data={**reason, "based_on": Scheduler(projection.graph, projection.facts).basis(requirement_id)},
        )
        self.events.append(event)
        return event

    def authorize_frame_retry(self, requirement_id: str) -> Event:
        projection = self.projection()
        rejected = projection.facts.get("rejected_frames", {})
        if not isinstance(rejected, Mapping) or requirement_id not in rejected:
            raise ModelError(f"frame has no active rejection: {requirement_id}")
        event = Event(kind="frame_retry_authorized", subject=requirement_id)
        self.events.append(event)
        return event


MATERIALS: dict[str, str] = {"images": "image", "audios": "audio", "videos": "video"}


def material_entries(facts: Facts, project: str, video: str) -> dict[str, Mapping[str, Any]]:
    """Single identity source for cardinality expansion AND consumer input bindings."""
    definition = facts.evidence_for(f"video_spec_definition/{project}/{video}")
    if definition is None:
        return {}
    return {
        f"{kind}/{project}/{video}/{identity}": entry
        for group, kind in MATERIALS.items()
        for identity, entry in definition.data[group].items()
    }


def material_entry(facts: Facts, requirement_id: str) -> Mapping[str, Any]:
    kind, project, video, identity = requirement_id.split("/")
    entries = material_entries(facts, project, video)
    if requirement_id not in entries:
        raise ModelError(f"undeclared media requirement: {requirement_id}")
    return entries[requirement_id]


def coverage_products(facts: Facts, project: str, video: str) -> dict[str, Mapping[str, Any]]:
    return {node: entry for node, entry in material_entries(facts, project, video).items()
            if entry.get("product_coverage", False)}


def frame_spec_items(facts: Facts, project: str, video: str) -> list[Mapping[str, Any]]:
    """Effective per-shot frame entries; blueprint.shots owns the count.

    Historical, erased, or otherwise ineffective frame-spec evidence expands
    nothing: the resolver never sees stale candidates. Without an effective
    frame spec no concrete frame is executable even though the blueprint
    already declares the shot count.
    """
    spec = facts.evidence_for(f"frame_spec_definition/{project}/{video}")
    if spec is None:
        return []
    return list(spec.data.get("frames", []))


SEMANTIC_KNOWLEDGE: dict[str, tuple[str, ...]] = {
    "start_new_project": ("references/project-lifecycle.md",),
    "project_close": ("references/project-lifecycle.md",),
    "communication_language": ("references/user-communication.md",),
    "information_understanding": (
        "references/information-understanding-template.md",
        "references/deliverable-contract.md",
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "creative_research": (
        "references/creative-research.md",
        "references/marketing-creative-guidance.md",
        "references/user-communication.md",
    ),
    "story_master": (
        "references/marketing-creative-guidance.md",
        "references/marketing-proof-playbook.md",
        "references/performance-timing-craft.md",
        "references/storyboard-template.md",
        "references/deliverable-contract.md",
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "direction_set": (
        "references/marketing-creative-guidance.md",
        "references/marketing-proof-playbook.md",
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "direction": (
        "references/marketing-creative-guidance.md",
        "references/marketing-proof-playbook.md",
    ),
    "preparation_scope": (
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "package_confirmation": (
        "references/deliverable-contract.md",
        "references/revision-routing.md",
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "image_model": (
        "references/visual-workflow.md",
        "references/user-communication.md",
    ),
    "frame_spec_definition": (
        "references/frame-spec-template.md",
        "references/visual-workflow.md",
        "references/reference-action-craft.md",
        "references/revision-routing.md",
    ),
    "storyboard_mode": (
        "references/visual-workflow.md",
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "product_state_coverage": (
        "references/asset-anchor-gates.md",
        "references/dynamic-questionnaire-guide.md",
        "references/deliverable-contract.md",
        "references/user-communication.md",
    ),
    "video_spec_definition": (
        "references/video-spec-contract.md",
        "references/asset-anchor-gates.md",
        "references/voice-anchor-gates.md",
    ),
    "image": (
        "references/media-requirements.md",
        "references/reference-action-craft.md",
        "references/common-knowledge.md",
        "references/external-knowledge.md",
        "references/asset-anchor-gates.md",
        "references/payload-route-gates.md",
        "references/user-communication.md",
    ),
    "audio": (
        "references/media-requirements.md",
        "references/common-knowledge.md",
        "references/voice-anchor-gates.md",
        "references/payload-route-gates.md",
        "references/user-communication.md",
    ),
    "video": (
        "references/media-requirements.md",
        "references/common-knowledge.md",
        "references/payload-route-gates.md",
        "references/user-communication.md",
    ),
    "storyboard_manifest": (
        "references/storyboard-source-contract.md",
        "references/storyboard-grid-template.md",
    ),
    "storyboard_overview": (
        "references/storyboard-grid-template.md",
        "references/deliverable-contract.md",
        "references/user-communication.md",
    ),
    "video_blueprint": (
        "references/common-knowledge.md",
        "references/marketing-creative-guidance.md",
        "references/marketing-proof-playbook.md",
        "references/reference-action-craft.md",
        "references/performance-timing-craft.md",
        "references/video-blueprint-template.md",
        "references/deliverable-contract.md",
        "references/revision-routing.md",
        "references/voice-anchor-gates.md",
        "references/user-communication.md",
    ),
    "frame": (
        "references/common-knowledge.md",
        "references/storyboard-source-contract.md",
        "references/reference-action-craft.md",
        "references/external-knowledge.md",
        "references/visual-workflow.md",
        "references/asset-anchor-gates.md",
        "references/payload-route-gates.md",
        "references/revision-routing.md",
    ),
    "execution_scope": (
        "references/dynamic-questionnaire-guide.md",
        "references/user-communication.md",
    ),
    "generation_model": (
        "references/execution-lowering.md",
        "references/user-communication.md",
    ),
    "direct_payload": (
        "references/common-knowledge.md",
        "references/reference-action-craft.md",
        "references/video-blueprint-template.md",
        "references/payload-route-gates.md",
        "references/execution-lowering.md",
    ),
    "runtime_manifest": (
        "references/common-knowledge.md",
        "references/execution-lowering.md",
        "references/runtime-lowering-grid-contract.md",
        "references/video-blueprint-template.md",
    ),
    "part_spec": (
        "references/execution-lowering.md",
        "references/runtime-lowering-grid-contract.md",
    ),
    "runtime_anchor": (
        "references/runtime-anchor-contract.md",
        "references/common-knowledge.md",
    ),
    "part_sheet": (
        "references/runtime-lowering-grid-contract.md",
        "references/storyboard-grid-template.md",
    ),
    "part_input": (
        "references/part-continuity.md",
        "references/runtime-anchor-contract.md",
        "references/reference-action-craft.md",
        "references/performance-timing-craft.md",
        "references/common-knowledge.md",
        "references/runtime-lowering-grid-contract.md",
        "references/video-blueprint-template.md",
        "references/payload-route-gates.md",
    ),
    "preflight": (
        "references/runtime-anchor-contract.md",
        "references/common-knowledge.md",
        "references/payload-route-gates.md",
        "references/voice-anchor-gates.md",
        "references/execution-lowering.md",
        "references/runtime-lowering-grid-contract.md",
    ),
    "direct_result": (
        "references/common-knowledge.md",
        "references/video-blueprint-template.md",
        "references/payload-route-gates.md",
        "references/user-communication.md",
    ),
    "part_result": (
        "references/part-continuity.md",
        "references/runtime-anchor-contract.md",
        "references/common-knowledge.md",
        "references/video-blueprint-template.md",
        "references/payload-route-gates.md",
    ),
    "assembled_result": (
        "references/common-knowledge.md",
        "references/runtime-lowering-grid-contract.md",
        "references/user-communication.md",
    ),
    "delivery": (
        "references/common-knowledge.md",
        "references/deliverable-contract.md",
        "references/revision-routing.md",
        "references/user-communication.md",
        "references/payload-route-gates.md",
    ),
    "continuity_choice": ("references/part-continuity.md",),
    "last_frame": ("references/part-continuity.md", "references/common-knowledge.md"),
    "part_preflight": (
        "references/part-continuity.md",
        "references/common-knowledge.md",
        "references/payload-route-gates.md",
        "references/voice-anchor-gates.md",
        "references/runtime-anchor-contract.md",
    ),
    "continuation_decision": (
        "references/post-delivery-revision.md",
        "references/project-lifecycle.md",
        "references/user-communication.md",
    ),
}


class BatchMarketingGraph:
    """Business declarations agreed for batch marketing production."""

    def __init__(self, facts: Facts):
        self.facts = facts
        self._frame_groups: dict[tuple[str, str], tuple[ExecutionGroup, ...]] = {}

    def compile(self) -> Graph:
        return self.project()[0]

    def project(self) -> tuple[Graph, Facts]:
        """Supply batch lifecycle values and declarations to the generic evaluator."""
        lifecycle = {
            key: value for key, value in self.facts.values.items()
            if key not in {"evidence_versions", "rejected_frames"}
        }
        return evaluate_effective_facts(
            self.facts, lambda visible: BatchMarketingGraph(visible).requirement,
            seed_values=lifecycle,
        )

    def ready(self) -> list[Requirement]:
        graph, facts = self.project()
        return Scheduler(graph, facts).ready()

    def requirement(self, requirement_id: str) -> Requirement:
        prefix = requirement_id.split("/", 1)[0]
        declaration = getattr(self, f"_declare_{prefix}", None)
        if declaration is None:
            raise ModelError(f"unknown requirement: {requirement_id}")
        requirement = declaration(requirement_id)
        guidance = dict(requirement.guidance)
        knowledge = list(SEMANTIC_KNOWLEDGE.get(prefix, ()))
        if prefix == "audio" and not guidance.get("declaration", {}).get("voice_sample", False):
            knowledge.remove("references/voice-anchor-gates.md")
        if prefix == "runtime_anchor":
            kind = requirement_id.split("/")[4]
            knowledge.append("references/media-requirements.md")
            if guidance.get("anchor", {}).get("voice_sample", False):
                knowledge.append("references/voice-anchor-gates.md")
            elif kind == "image":
                knowledge.extend((
                    "references/asset-anchor-gates.md",
                    "references/reference-action-craft.md",
                    "references/external-knowledge.md",
                ))
        if prefix == "frame":
            group = requirement.execution_group
            if group is not None and group.metadata.get("route") == "route_a":
                knowledge.append("references/grid-prompt-template.md")
            else:
                knowledge.append("references/storyboard-frame-generation.md")
        if knowledge:
            guidance["knowledge_refs"] = tuple(dict.fromkeys(knowledge))
        supplemental_inputs = self._supplemental_inputs(requirement_id)
        actions = requirement.actions
        if not actions and requirement.contract is not None:
            actions = tuple(
                action for action in ACTIONS.values()
                if action.operation == "apply" and action.accepts(requirement_id)
                and action.resolution in requirement.contract.resolutions
            )
        # Business display scopes are declared here. Renderers treat these keys
        # as opaque and never recover project/video identity from node IDs.
        display_group = requirement.display_group
        if display_group is None:
            if prefix in {
                "frame_spec_definition", "video_blueprint", "video_spec_definition",
                "product_state_coverage", "storyboard_mode", "image_model",
                "storyboard_manifest", "storyboard_overview", "package_confirmation",
                "image", "audio", "video", "frame",
            }:
                display_group = "/".join(requirement_id.split("/")[:3])
            else:
                display_group = prefix
        if (
            guidance == requirement.guidance
            and supplemental_inputs == requirement.supplemental_inputs
            and display_group == requirement.display_group
            and actions == requirement.actions
        ):
            return requirement
        return replace(
            requirement,
            guidance=guidance,
            supplemental_inputs=supplemental_inputs,
            display_group=display_group,
            actions=actions,
        )

    def _supplemental_inputs(self, requirement_id: str) -> tuple[InputBinding, ...]:
        """Declare non-gating current inputs with consumer-side use semantics."""

        bindings: list[InputBinding] = []
        consumer_prefix = requirement_id.split("/", 1)[0]
        for input_id in self._supplemental_input_ids(requirement_id):
            input_prefix = input_id.split("/", 1)[0]
            uses: tuple[InputUse, ...] = ()
            if consumer_prefix == "continuation_decision":
                if input_prefix in {"video_blueprint", "runtime_manifest", "part_input", "direct_payload"}:
                    uses = (read_content(
                        "path", required=False,
                        purpose=("Initial-generation baseline: read the relevant content when "
                                 "needed for the user's requested edit; this is not a record "
                                 "of the latest freely revised output."),
                    ),)
                else:
                    uses = (structured_fact(
                        required=False,
                        purpose=("Initial-generation baseline and reusable sources. Select "
                                 "only what the current edit needs; consult verified project "
                                 "memos and actual files for subsequent revisions."),
                    ),)
            elif consumer_prefix in {"part_input", "part_preflight", "part_result"} and input_prefix == "runtime_anchor":
                anchor = self._declare_runtime_anchor(input_id).guidance["anchor"]
                if anchor["strategy"] == "generate":
                    uses = self._runtime_anchor_tool_uses(input_id.split("/")[4])
            elif consumer_prefix in {"part_preflight", "part_result"} and input_prefix in MATERIALS.values():
                uses = self._material_tool_uses(
                    input_prefix, tool="sandbox_generate_video",
                    allowed=material_entry(self.facts, input_id)["allowed_resolutions"],
                )
            elif consumer_prefix in {"part_preflight", "part_result"} and input_prefix == "last_frame":
                uses = (tool_argument(
                    "path", target="sandbox_generate_video.ImageList",
                    purpose=("Keep this selected previous end frame in this part's exact media "
                             "arguments at the position recorded by its executable input."),
                    resolutions=("provided",),
                ),)
            elif consumer_prefix == "part_result" and input_prefix == "part_input":
                uses = (read_content(
                    "path", purpose=("Use this part's complete current executable input and "
                                     "preserve the verified media order for the generation call."),
                    resolutions=("provided",),
                ),)
            elif consumer_prefix in set(MATERIALS.values()) | {"runtime_anchor"} and input_prefix == "video_blueprint":
                uses = (read_content(
                    "path", purpose="Read the story and material roles before fulfilling this requirement.",
                    resolutions=("provided",),
                ),)
            elif consumer_prefix == "video_blueprint" and input_prefix == "information_understanding":
                uses = (
                    read_content(
                        "path",
                        purpose=(
                            "Use the accepted campaign facts, supplied materials, market scope, "
                            "and batch intent when specializing this video's specification."
                        ),
                        resolutions=("confirmed",),
                    ),
                )
            elif consumer_prefix == "video_blueprint" and input_prefix == "creative_research":
                uses = self._creative_research_uses(
                    "Use accepted research findings and explored-direction constraints when "
                    "specializing this video's specification."
                )
            bindings.append(InputBinding(requirement_id=input_id, uses=uses))
        return tuple(bindings)

    @staticmethod
    def _creative_research_uses(provided_purpose: str) -> tuple[InputUse, ...]:
        return (
            read_content(
                "path",
                purpose=provided_purpose,
                resolutions=("provided",),
            ),
            structured_fact(
                "user_evidence",
                purpose=(
                    "Honor the explicit research waiver and continue without inventing or "
                    "assuming a research handoff."
                ),
                resolutions=("waived",),
            ),
        )

    def _supplemental_input_ids(self, requirement_id: str) -> tuple[str, ...]:
        """Select supplemental current-project inputs for one ready requirement.

        These IDs affect only next-action rendering. They do not create graph
        edges, satisfy requirements, or claim that a later tool call used the
        referenced artifact. Direct prerequisites are added by the renderer.
        """

        parts = requirement_id.split("/")
        prefix = parts[0]
        if prefix in {"GOAL", "start_new_project"} or len(parts) < 2:
            return ()
        project = parts[1]

        def project_node(name: str) -> str:
            return f"{name}/{project}"

        def video_node(name: str, video: str) -> str:
            return f"{name}/{project}/{video}"

        def video_context(video: str) -> list[str]:
            return [
                project_node("information_understanding"),
                project_node("creative_research"),
                project_node("story_master"),
                f"direction/{project}/{video}",
            ]

        def visual(video: str) -> bool:
            evidence = self.facts.evidence_for(video_node("storyboard_mode", video))
            return evidence is not None and evidence.data.get("mode") == "visual"

        selected: list[str] = []
        if prefix == "continuation_decision":
            execution_round = str(self._project_state(project)["execution_round"])
            execution = self.facts.evidence_for(f"execution_scope/{project}/{execution_round}")
            for video in ids(execution.data.get("videos")) if execution else ():
                selected.extend([video_node("video_blueprint", video),
                                 video_node("video_spec_definition", video),
                                 *self._video_material_requirements(video, project=project)])
                # Context only: never turn free-form revision work into new dependencies.
                for node_id in self.facts.evidence:
                    node_parts = node_id.split("/")
                    if (len(node_parts) >= 4 and node_parts[1:4] == [project, video, execution_round]
                            and node_parts[0] in {
                                "direct_payload", "direct_result", "runtime_manifest",
                                "runtime_anchor", "part_spec", "part_input", "part_sheet",
                                "part_result", "last_frame", "assembled_result",
                            }):
                        selected.append(node_id)
        if prefix == "runtime_anchor":
            selected.extend(video_context(parts[2]))
            selected.extend([video_node("video_spec_definition", parts[2]),
                             video_node("video_blueprint", parts[2])])
        if prefix in {"video_blueprint", "video_spec_definition"}:
            selected.extend(video_context(parts[2]))
        elif prefix in set(MATERIALS.values()):
            selected.extend(video_context(parts[2]))
            selected.append(video_node("video_blueprint", parts[2]))
        elif prefix == "storyboard_overview":
            selected.extend(self._frame_requirements(parts[2], project=project))
        elif prefix == "part_sheet":
            video, execution_round = parts[2], parts[3]
            selected.extend(
                [
                    f"runtime_manifest/{project}/{video}/{execution_round}",
                    *self._frame_requirements(video, project=project),
                ]
            )
        elif prefix == "preflight":
            video = parts[2]
            selected.extend(
                [video_node("video_blueprint", video),
                 *self._video_material_requirements(video, project=project)]
            )
            if visual(video):
                selected.append(video_node("storyboard_overview", video))
        elif prefix == "direct_result":
            selected.append(f"direct_payload/{project}/{parts[2]}/{parts[3]}")
        elif prefix in {"part_result", "part_preflight"}:
            video, execution_round, part = parts[2], parts[3], parts[4]
            part_spec = f"part_spec/{project}/{video}/{execution_round}/{part}"
            selected.extend(
                [
                    part_spec,
                    f"part_input/{project}/{video}/{execution_round}/{part}",
                    *self._part_material_requirements(video, part_spec, project=project),
                ]
            )
            if visual(video):
                selected.append(f"part_sheet/{project}/{video}/{execution_round}/{part}")
            if int(part) > 1:
                choice_id = f"continuity_choice/{project}/{video}/{execution_round}/{part}"
                selected.append(choice_id)
                choice = self.facts.evidence_for(choice_id)
                if choice is not None and choice.data.get("use_last_frame") is True:
                    selected.append(f"last_frame/{project}/{video}/{execution_round}/{int(part) - 1:02d}")
        if prefix in {"part_input", "part_result", "part_preflight"}:
            video, execution_round, part = parts[2:5]
            selected.extend([video_node("video_blueprint", video),
                             f"runtime_manifest/{project}/{video}/{execution_round}"])
            for key, entry in selected_runtime_anchors(
                self.facts, project, video, execution_round, part
            ).items():
                selected.append(f"runtime_anchor/{project}/{video}/{execution_round}/{key}")
                if entry.get("source"):
                    selected.append(entry["source"])
        return tuple(dict.fromkeys(selected))

    def _video_material_requirements(self, video: str, *, project: str | None = None) -> list[str]:
        project = project or self._project_required()
        return list(material_entries(self.facts, project, video))

    def _part_material_requirements(
        self, video: str, part_spec: str, *, project: str | None = None
    ) -> list[str]:
        project = project or self._project_required()
        evidence = self.facts.evidence_for(part_spec)
        materials = evidence.data.get("materials") if evidence else None
        if not isinstance(materials, Mapping):
            return []
        return [node for node in self._material_requirements(project, video, materials)
                if node in material_entries(self.facts, project, video)]

    @staticmethod
    def _material_requirements(
        project: str, video: str, mapping: Mapping[str, Any]
    ) -> list[str]:
        return [
            f"{prefix}/{project}/{video}/{material_id}"
            for field_name, prefix in MATERIALS.items()
            for material_id in ids(mapping.get(field_name))
        ]

    @staticmethod
    def _material_tool_uses(prefix: str, *, tool: str,
                            allowed: Sequence[str] = ("provided", "auto", "waived"),
                            bind_required: bool = True) -> tuple[InputUse, ...]:
        target = {"image": "ImageList", "audio": "AudioList", "video": "VideoList"}[prefix]
        if tool == "sandbox_generate_image" and prefix != "image":
            return (structured_fact(purpose=(
                "Use this media's semantic context only; do not pass audio/video evidence "
                "as an image-generation argument."
            )),)
        uses = (
            tool_argument(
                "paths", target=f"{tool}.{target}",
                purpose=("Select the references relevant to this shot/part from the blueprint "
                         "and material purpose. For selected files, preserve their actual ordered "
                         "one-based argument positions; dependency does not mean bind every file."),
                resolutions=("provided",), required=bind_required,
            ),
            structured_fact("user_evidence", purpose=(
                "Honor this explicit delegation or waiver and its constraints. It supplies no "
                "media file and does not waive a separately required runtime anchor."
            ), resolutions=("auto", "waived")),
        )
        return tuple(replace(use, resolutions=use.resolutions & frozenset(allowed))
                     for use in uses if use.resolutions & frozenset(allowed))

    @staticmethod
    def _runtime_anchor_tool_uses(kind: str) -> tuple[InputUse, ...]:
        target = {"image": "ImageList", "audio": "AudioList", "video": "VideoList"}[kind]
        return (tool_argument(
            "path", target=f"sandbox_generate_video.{target}",
            purpose=("Bind this concrete continuity anchor to this part's ordered media "
                     "arguments and keep the executable prompt's positional references aligned."),
            resolutions=("provided",),
        ),)

    def _media_dependency(self, project: str, video: str, *, tool: str | None = None,
                          presentation: bool = False) -> Dependency:
        definition = f"video_spec_definition/{project}/{video}"

        def resolve(facts: Facts) -> Evaluation:
            targets = []
            for node, entry in material_entries(facts, project, video).items():
                kind = node.split("/")[0]
                if presentation:
                    uses = (
                        present("paths", purpose="Present these accepted assets for package review.",
                                resolutions=("provided",)),
                        structured_fact("user_evidence", purpose=(
                            "Explain the accepted delegation/waiver and remaining creative freedom."
                        ), resolutions=("auto", "waived")),
                    )
                elif tool:
                    uses = self._material_tool_uses(kind, tool=tool, allowed=entry["allowed_resolutions"], bind_required=False)
                else:
                    uses = (structured_fact(purpose="Use this declared material's current evidence."),)
                uses = tuple(
                    replace(use, resolutions=use.resolutions & frozenset(entry["allowed_resolutions"]))
                    if use.resolutions else use
                    for use in uses
                    if not use.resolutions or use.resolutions & frozenset(entry["allowed_resolutions"])
                )
                # Semantic metadata travels alongside evidence, without being copied into its fact.
                uses = (structured_fact(purpose=(
                    f"Declared role: {entry['role']}. Requirement: {entry['description']}"
                )), *uses)
                targets.append(edge(node, input_uses=uses))
            return Evaluation.of(targets)

        return conditional("declared-media", fact_producers=(definition,), resolver=resolve)

    def _frame_requirements(self, video: str, *, project: str | None = None) -> list[str]:
        """The single frame-cardinality helper; the frame spec owns the count."""
        project = project or self._project_required()
        return [f"frame/{project}/{video}/{index:02d}"
                for index, _item in enumerate(frame_spec_items(self.facts, project, video), 1)]

    def _frame_spec_item(self, video: str, frame_index: int, *, project: str | None = None) -> Mapping[str, Any]:
        project = project or self._project_required()
        items = frame_spec_items(self.facts, project, video)
        if not 1 <= frame_index <= len(items):
            raise ModelError(
                f"frame/{project}/{video}/{frame_index:02d} has no matching frame spec item"
            )
        return items[frame_index - 1]

    def _active_project(self) -> str | None:
        value = self.facts.get("active_project")
        return str(value) if value else None

    def _project_state(self, project: str) -> Mapping[str, Any]:
        states = self.facts.get("project_states", {})
        if not isinstance(states, Mapping) or not isinstance(states.get(project), Mapping):
            raise ModelError(f"project state is unavailable: {project}")
        return states[project]

    def _scoped(self, prefix: str, *parts: object, project: str | None = None) -> str:
        owner = project or self._project_required()
        return "/".join([prefix, owner, *(str(part) for part in parts)])

    def _scoped_segments(self, requirement_id: str, prefix: str, tail: int) -> list[str]:
        parts = self._segments(requirement_id, prefix, tail + 2)
        if len(parts) != tail + 2:
            raise ModelError(f"invalid {prefix} requirement ID: {requirement_id}")
        return parts

    def _project_required(self) -> str:
        project = self._active_project()
        if project is None:
            raise ModelError("an active project is required")
        return project

    @staticmethod
    def _segments(requirement_id: str, prefix: str, count: int) -> list[str]:
        parts = requirement_id.split("/")
        if len(parts) < count or parts[0] != prefix:
            raise ModelError(f"invalid {prefix} requirement ID: {requirement_id}")
        return parts

    def _declare_GOAL(self, requirement_id: str) -> Requirement:
        if requirement_id != "GOAL":
            raise ModelError(f"invalid GOAL ID: {requirement_id}")
        cycle = str(self.facts.get("project_cycle", "01"))

        return Requirement(
            id="GOAL",
            kind="goal",
            subject="Continuously serve batch marketing video production intent",
            contract=None,
            deps=(requires("project-bootstrap", f"start_new_project/{cycle}"),),
            focusable=False,
            never_complete=True,
        )

    def _declare_start_new_project(self, requirement_id: str) -> Requirement:
        parts = self._segments(requirement_id, "start_new_project", 2)
        cycle = positive_integer(parts[1], f"{requirement_id}.cycle")
        dependencies: tuple[Dependency, ...] = ()
        if cycle > 1:
            slots = self.facts.get("project_slots", {})
            previous = slots.get(f"{cycle - 1:02d}") if isinstance(slots, Mapping) else None
            if previous is None:
                raise ModelError(f"missing project for previous start slot {cycle - 1:02d}")
            dependencies = (requires("previous-project", f"project_goal/{previous}"),)
        return Requirement(
            id=requirement_id,
            kind="question",
            subject="Create or resume a project",
            contract=contract("project-selection", "created", "resumed"),
            deps=dependencies,
            actions=(ACTIONS["project-create"],) + (
                (ACTIONS["project-resume"],) if self.facts.get("project_slots") else ()
            ),
        )

    def _declare_project_goal(self, requirement_id: str) -> Requirement:
        project = self._segments(requirement_id, "project_goal", 2)[1]
        state = self._project_state(project)
        prep_round = str(state.get("preparation_round", "01"))
        execution_round = str(state.get("execution_round", "01"))
        continuation_round = str(state.get("continuation_round", "01"))
        prep = f"preparation_scope/{project}/{prep_round}"
        execution = f"execution_scope/{project}/{execution_round}"
        continuation_node = f"continuation_decision/{project}/{continuation_round}"

        def pending_close(facts: Facts) -> Evaluation:
            """A finish/pause decision must be sealed by project_close before
            the project goal can count as complete."""
            choice = facts.evidence_for(continuation_node)
            if choice is None:
                return Evaluation.unknown()
            if choice.data.get("choice") in {"finish", "pause"}:
                return Evaluation.of([
                    edge(f"project_close/{project}/{continuation_round}")
                ])
            return Evaluation.of()

        def packages(facts: Facts) -> Evaluation:
            evidence = facts.evidence_for(prep)
            if evidence is None:
                return Evaluation.unknown()
            return Evaluation.of(
                edge(self._scoped("package_confirmation", video, project=project))
                for video in ids(evidence.data.get("videos"))
            )

        def deliveries(facts: Facts) -> Evaluation:
            evidence = facts.evidence_for(execution)
            if evidence is None:
                return Evaluation.unknown()
            return Evaluation.of(
                edge(self._scoped("delivery", video, execution_round, project=project))
                for video in ids(evidence.data.get("videos"))
            )

        return Requirement(
            id=requirement_id,
            kind="goal",
            subject=f"Produce the confirmed videos for project {project}",
            contract=None,
            focusable=False,
            deps=(
                requires("communication-language", f"communication_language/{project}"),
                requires("information-understanding", f"information_understanding/{project}"),
                requires("creative-research", f"creative_research/{project}"),
                requires("story-master", f"story_master/{project}"),
                requires("direction-set", f"direction_set/{project}"),
                requires("preparation-scope", prep),
                conditional(
                    "selected-packages",
                    fact_producers=(prep,),
                    resolver=packages,
                ),
                requires("execution-scope", execution),
                conditional(
                    "selected-deliveries",
                    fact_producers=(execution,),
                    resolver=deliveries,
                ),
                requires(
                    "continuation",
                    continuation_node,
                ),
                conditional(
                    "pending-close",
                    fact_producers=(continuation_node,),
                    resolver=pending_close,
                ),
            ),
        )

    def _declare_project_close(self, requirement_id: str) -> Requirement:
        _, project, continuation_round = self._scoped_segments(
            requirement_id, "project_close", 1
        )
        continuation_node = f"continuation_decision/{project}/{continuation_round}"

        def chosen_close(facts: Facts) -> Evaluation:
            choice = facts.evidence_for(continuation_node)
            if choice is None:
                return Evaluation.unknown()
            return Evaluation.of([edge(continuation_node, input_uses=(
                structured_fact(purpose=(
                    "The user's accepted finish/pause decision and its evidence; "
                    "this close implements that decision without asking again."
                )),
            ))] if choice.data.get("choice") in {"finish", "pause"} else [])

        choice = self.facts.evidence_for(continuation_node)
        decision = (choice.data.get("choice") if choice is not None else None) or "close"
        return Requirement(
            id=requirement_id,
            kind="action",
            subject=f"Seal the accepted {decision} decision for project {project}",
            contract=contract("project-close", "closed"),
            actions=(ACTIONS[f"project-{decision}"],) if decision in {"finish", "pause"} else (),
            what_lines=(
                f"The user has already selected {decision} for this project. Complete "
                "the pending lifecycle close; do not ask for confirmation again.",
                "Run the exact lifecycle command now, then refresh next-action. Until "
                "the close succeeds, do not create or resume another project.",
            ) if decision in {"finish", "pause"} else (),
            deps=(
                conditional(
                    "continuation-choice",
                    fact_producers=(continuation_node,),
                    resolver=chosen_close,
                ),
            ),
        )

    def _declare_communication_language(self, requirement_id: str) -> Requirement:
        return Requirement(
            id=requirement_id,
            kind="question",
            subject="Resolve the user communication language",
            contract=contract("communication-language", "reported"),
        )

    def _declare_information_understanding(self, requirement_id: str) -> Requirement:
        project = self._segments(requirement_id, "information_understanding", 2)[1]
        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject="Confirm product facts, materials, market and batch intent",
            contract=contract("information-understanding", "confirmed"),
            deps=(requires("communication-language", f"communication_language/{project}"),),
        )

    def _declare_creative_research(self, requirement_id: str) -> Requirement:
        project = self._segments(requirement_id, "creative_research", 2)[1]
        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject="Provide creative research or record an explicit user waiver",
            contract=contract("creative-research", "provided", "waived"),
            deps=(
                requires("information-understanding", f"information_understanding/{project}"),
            ),
        )

    def _declare_story_master(self, requirement_id: str) -> Requirement:
        project = self._segments(requirement_id, "story_master", 2)[1]
        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject="Confirm the shared mother story and exact shot count",
            contract=contract("story-master", "confirmed"),
            deps=(
                requires(
                    "information-understanding",
                    f"information_understanding/{project}",
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Use the accepted product facts, supplied materials, market "
                                "scope, and batch intent when authoring StoryMaster."
                            ),
                            resolutions=("confirmed",),
                        ),
                    ),
                ),
                requires(
                    "creative-research",
                    f"creative_research/{project}",
                    input_uses=self._creative_research_uses(
                        "Use the accepted research findings and explored-direction registry "
                        "when authoring StoryMaster."
                    ),
                ),
            ),
            guidance={"evidence_fields": ["shots", "duration_ms", "path"]},
        )

    def _declare_direction_set(self, requirement_id: str) -> Requirement:
        project = self._segments(requirement_id, "direction_set", 2)[1]
        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject="Confirm all concrete directions for the planned total",
            contract=contract("direction-set", "confirmed"),
            deps=(
                requires(
                    "information-understanding",
                    f"information_understanding/{project}",
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Use the accepted campaign facts and batch intent when defining "
                                "the concrete direction portfolio."
                            ),
                            resolutions=("confirmed",),
                        ),
                    ),
                ),
                requires(
                    "creative-research",
                    f"creative_research/{project}",
                    input_uses=self._creative_research_uses(
                        "Use accepted research findings and the explored-direction registry "
                        "when defining the concrete direction portfolio."
                    ),
                ),
                requires(
                    "story-master",
                    f"story_master/{project}",
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Use the confirmed shared story structure and its open "
                                "exploration slots when defining each direction."
                            ),
                            resolutions=("confirmed",),
                        ),
                    ),
                ),
            ),
        )

    def _declare_direction(self, requirement_id: str) -> Requirement:
        parts = self._segments(requirement_id, "direction", 3)
        project, video = parts[1], parts[2]
        return Requirement(
            id=requirement_id,
            kind="business-object",
            subject=f"Confirmed direction {video}",
            contract=contract("direction", "confirmed"),
            deps=(requires("direction-set", f"direction_set/{project}"),),
        )

    def _declare_preparation_scope(self, requirement_id: str) -> Requirement:
        parts = self._segments(requirement_id, "preparation_scope", 3)
        return Requirement(
            id=requirement_id,
            kind="question",
            subject=f"Select the videos for preparation round {parts[2]}",
            contract=contract("preparation-scope", "selected"),
            deps=(requires("direction-set", f"direction_set/{parts[1]}"),),
        )

    def _declare_package_confirmation(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "package_confirmation", 1)
        mode = f"storyboard_mode/{project}/{video}"

        def visual_overview(facts: Facts) -> Evaluation:
            answer = facts.evidence_for(mode).data["mode"]
            return Evaluation.of([edge(
                f"storyboard_overview/{project}/{video}",
                input_uses=(present("path", purpose=(
                    "Present the actual visual storyboard together with the blueprint and materials."
                ), resolutions=("derived",)),),
            )] if answer == "visual" else [])

        return Requirement(
            id=requirement_id, kind="decision", subject=f"Confirm the creative package for video {video}",
            contract=contract("package-confirmation", "confirmed"),
            deps=(
                requires("blueprint", f"video_blueprint/{project}/{video}", input_uses=(
                    present("path", purpose="Present the complete per-video story for package confirmation.",
                            resolutions=("provided",)),
                )),
                requires("video-spec", f"video_spec/{project}/{video}"),
                requires("definition", f"video_spec_definition/{project}/{video}"),
                self._media_dependency(project, video, presentation=True),
                requires("storyboard-mode", mode),
                conditional("visual-overview", fact_producers=(mode,), resolver=visual_overview),
            ),
            guidance={"presentation": "present_sandbox_file must succeed before user confirmation"},
        )

    def _declare_image_model(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "image_model", 1)
        return Requirement(
            id=requirement_id, kind="question",
            subject=f"Read the UI-injected storyboard image-model setting for video {video}",
            contract=contract("image-model", "reported"),
            deps=(requires("storyboard-mode", f"storyboard_mode/{project}/{video}"),),
            guidance={"evidence_fields": ["model", "source"]},
        )

    def _declare_frame_spec_definition(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "frame_spec_definition", 1)
        return Requirement(
            id=requirement_id, kind="decision",
            subject=f"Provide the per-shot visual descriptions for video {video}",
            contract=contract("frame-spec-definition", "provided"),
            deps=(
                requires(
                    "blueprint", f"video_blueprint/{project}/{video}",
                    input_uses=(read_content("path", purpose=(
                        "Read the complete script; every shot needs one representative "
                        "static instant with its required visual continuity."
                    ), resolutions=("provided",)),),
                ),
                requires(
                    "definition", f"video_spec_definition/{project}/{video}",
                    input_uses=(structured_fact("images", purpose=(
                        "Reference only stable semantic image IDs declared here; never file "
                        "paths or Image[N] positions."
                    ), resolutions=("provided",)),),
                ),
                requires("storyboard-mode", f"storyboard_mode/{project}/{video}"),
            ),
            guidance={"evidence_fields": ["frames"]},
        )

    def _declare_storyboard_mode(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "storyboard_mode", 1)
        return Requirement(
            id=requirement_id, kind="question", subject=f"Choose visual or script-only for video {video}",
            contract=contract("storyboard-mode", "selected"),
            deps=(
                requires("blueprint", f"video_blueprint/{project}/{video}", input_uses=(
                    read_content("path", purpose="Understand the completed story before choosing its presentation mode."),
                )),
                requires("video-spec", f"video_spec/{project}/{video}"),
                requires("definition", f"video_spec_definition/{project}/{video}"),
                self._media_dependency(project, video),
            ),
            guidance={"allowed": ["visual", "script_only"]},
        )

    def _declare_video_blueprint(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "video_blueprint", 1)
        return Requirement(
            id=requirement_id, kind="artifact",
            subject=f"Author the concrete story and semantic material identities for video {video}",
            contract=contract("video-blueprint", "provided"),
            deps=(
                requires("story-master", f"story_master/{project}", input_uses=(
                    read_content("path", purpose="Specialize the master story into this video's complete story."),
                )),
                requires("direction", f"direction/{project}/{video}", input_uses=(
                    structured_fact(purpose="Apply this video's accepted direction and target market."),
                )),
            ),
            guidance={"evidence_fields": ["path", "shots", "duration_ms", "ratio", "market_target"]},
        )

    def _declare_video_spec_definition(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "video_spec_definition", 1)
        return Requirement(
            id=requirement_id, kind="artifact",
            subject=f"Declare media requirements from video {video}'s blueprint",
            contract=contract("video-spec-definition", "provided"),
            deps=(requires("blueprint", f"video_blueprint/{project}/{video}", input_uses=(
                read_content("path", purpose=(
                    "Extract the complete media inventory using stable semantic IDs from the story. "
                    "Shot appearances stay in the blueprint; do not create a shot mapping here."
                )),
            )),),
            guidance={"evidence_fields": ["images", "audios", "videos"]},
        )

    def _declare_video_spec(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "video_spec", 1)
        definition = f"video_spec_definition/{project}/{video}"

        def coverage(facts: Facts) -> Evaluation:
            return Evaluation.of([edge(f"product_state_coverage/{project}/{video}")]
                                 if coverage_products(facts, project, video) else [])

        return Requirement(
            id=requirement_id, kind="collection", subject=f"All declared media requirements for video {video}",
            contract=None, focusable=False,
            deps=(
                requires("definition", definition),
                *(requires(group, f"{group}/{project}/{video}") for group in MATERIALS),
                conditional("product-state-coverage", fact_producers=(definition,), resolver=coverage),
            ),
        )

    def _declare_media_group(self, requirement_id: str) -> Requirement:
        group, project, video = requirement_id.split("/")
        definition = f"video_spec_definition/{project}/{video}"
        kind = MATERIALS[group]
        return Requirement(
            id=requirement_id, kind="collection", subject=f"Declared {group} for video {video}",
            contract=None, focusable=False,
            deps=(
                requires("definition", definition),
                conditional("children", fact_producers=(definition,), resolver=lambda facts: Evaluation.of(
                    edge(node) for node in material_entries(facts, project, video)
                    if node.startswith(kind + "/")
                )),
            ),
        )

    _declare_images = _declare_media_group
    _declare_audios = _declare_media_group
    _declare_videos = _declare_media_group

    def _declare_media(self, requirement_id: str) -> Requirement:
        kind, project, video, identity = requirement_id.split("/")
        entry = material_entry(self.facts, requirement_id)
        return Requirement(
            id=requirement_id, kind="asset", subject=f"{entry['role']}: {entry['description']} ({identity})",
            contract=contract("media-" + kind, *entry["allowed_resolutions"]),
            deps=(requires("definition", f"video_spec_definition/{project}/{video}"),),
            guidance={"declaration": dict(entry), "evidence_fields": ["paths", "user_evidence"]},
        )

    _declare_image = _declare_media
    _declare_audio = _declare_media
    _declare_video = _declare_media

    def _declare_product_state_coverage(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(requirement_id, "product_state_coverage", 1)
        definition = f"video_spec_definition/{project}/{video}"
        return Requirement(
            id=requirement_id, kind="decision", subject=f"Resolve required product view/state coverage for video {video}",
            contract=contract("product-state-coverage", "confirmed"),
            deps=(
                requires("blueprint", f"video_blueprint/{project}/{video}", input_uses=(
                    read_content("path", purpose="Check all product views and states required by the concrete story."),
                )),
                requires("definition", definition),
                conditional("declared-products", fact_producers=(definition,), resolver=lambda facts: Evaluation.of(
                    edge(node) for node in coverage_products(facts, project, video)
                )),
            ),
            guidance={"evidence_fields": ["products"]},
        )

    def _declare_storyboard_overview(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(
            requirement_id, "storyboard_overview", 1
        )
        return Requirement(
            id=requirement_id,
            kind="asset",
            subject=f"Compose the storyboard overview for video {video}",
            contract=contract("storyboard-overview", "derived"),
            deps=(requires(
                "storyboard-manifest",
                f"storyboard_manifest/{project}/{video}",
                input_uses=(
                    tool_argument(
                        "path",
                        target="compose_storyboard_sheet.py.ManifestPath",
                        purpose=(
                            "Pass the accepted semantic manifest to the compositor; do not "
                            "reconstruct its shot mapping from memory."
                        ),
                        resolutions=("provided",),
                    ),
                ),
            ),),
        )

    def _frame_execution_groups(self, project: str, video: str) -> tuple[ExecutionGroup, ...]:
        """Declare each frame's unit once per effective business projection."""
        key = (project, video)
        if key in self._frame_groups:
            return self._frame_groups[key]
        model = self.facts.evidence_for(f"image_model/{project}/{video}")
        if model is None:
            return ()
        route = image_route(model.data.get("model"))
        count = len(frame_spec_items(self.facts, project, video))
        groups: dict[str, ExecutionGroup] = {}
        frames: list[ExecutionGroup] = []
        for frame_index in range(1, count + 1):
            metadata: dict[str, Any] = {"route": route}
            if route == "route_a":
                batch = (frame_index - 1) // 9 + 1
                metadata.update(
                    group=f"batch-{batch:02d}",
                    batch_start=(batch - 1) * 9 + 1,
                    batch_end=min(batch * 9, count),
                )
            else:
                metadata["group"] = f"frame-{frame_index:02d}"
            group_id = f"frame/{project}/{video}/{route}/{metadata['group']}"
            if group_id not in groups:
                groups[group_id] = ExecutionGroup(
                    id=group_id, expand_ready_peers=route == "route_a", metadata=metadata,
                )
            frames.append(groups[group_id])
        self._frame_groups[key] = tuple(frames)
        return self._frame_groups[key]

    def _declare_storyboard_manifest(self, requirement_id: str) -> Requirement:
        _, project, video = self._scoped_segments(
            requirement_id, "storyboard_manifest", 1
        )
        model_node = f"image_model/{project}/{video}"
        story_node = f"video_blueprint/{project}/{video}"
        frame_spec_node = f"frame_spec_definition/{project}/{video}"

        def route_frames(expected_route: str) -> Resolver:
            def resolve(facts: Facts) -> Evaluation:
                model = facts.evidence_for(model_node)
                if model is None:
                    return Evaluation.unknown()
                route = image_route(model.data.get("model"))
                if route != expected_route:
                    return Evaluation.of()
                items = frame_spec_items(facts, project, video)
                groups = self._frame_execution_groups(project, video)
                targets: list[EdgeTarget] = []
                for frame_index, item in enumerate(items, 1):
                    if route == "route_a":
                        targets.append(
                            edge(
                                f"frame/{project}/{video}/{frame_index:02d}",
                                input_uses=(
                                    tool_argument(
                                        "path",
                                        target="compose_storyboard_sheet.py.FramePaths",
                                        purpose=(
                                            "Use the accepted frame file in the compositor's "
                                            "ordered storyboard row mapping."
                                        ),
                                        resolutions=("provided",),
                                    ),
                                ),
                                cell=(frame_index - 1) % 9 + 1,
                                **groups[frame_index - 1].metadata,
                            )
                        )
                    else:
                        targets.append(
                            edge(
                                f"frame/{project}/{video}/{frame_index:02d}",
                                input_uses=(
                                    tool_argument(
                                        "path",
                                        target="compose_storyboard_sheet.py.FramePaths",
                                        purpose=(
                                            "Use the accepted frame file in the compositor's "
                                            "ordered storyboard row mapping."
                                        ),
                                        resolutions=("provided",),
                                    ),
                                ),
                                **groups[frame_index - 1].metadata,
                            )
                        )
                return Evaluation.of(targets)

            return resolve

        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject=f"Provide the semantic storyboard manifest for video {video}",
            contract=contract("storyboard-manifest", "provided"),
            deps=(
                requires(
                    "video-blueprint",
                    story_node,
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Project the canonical shot semantics, annotations, and material "
                                "roles into the storyboard manifest rows."
                            ),
                            resolutions=("provided",),
                        ),
                    ),
                ),
                requires("video-spec", f"video_spec/{project}/{video}"),
                requires(
                    "frame-spec", frame_spec_node,
                    input_uses=(structured_fact("frames", purpose=(
                        "Align manifest rows and order with the accepted per-shot entries; "
                        "each row carries its frame's visual description basis."
                    ), resolutions=("provided",)),),
                ),
                requires("image-model", model_node),
                conditional(
                    "route-a-frames",
                    fact_producers=(model_node, frame_spec_node),
                    resolver=route_frames("route_a"),
                ),
                conditional(
                    "route-b-frames",
                    fact_producers=(model_node, frame_spec_node),
                    resolver=route_frames("route_b"),
                ),
            ),
        )

    def _declare_frame(self, requirement_id: str) -> Requirement:
        _, project, video, raw_index = self._scoped_segments(requirement_id, "frame", 2)
        frame_index = positive_integer(raw_index, f"{requirement_id}.frame_index")
        item = self._frame_spec_item(video, frame_index, project=project)
        frame_spec_node = f"frame_spec_definition/{project}/{video}"

        def frame_images(facts: Facts) -> Evaluation:
            current = frame_spec_items(facts, project, video)
            if not 1 <= frame_index <= len(current):
                raise ModelError(
                    f"{requirement_id} no longer matches the effective frame spec"
                )
            targets: list[EdgeTarget] = []
            for image_id in ids(current[frame_index - 1].get("image_ids")):
                node = f"image/{project}/{video}/{image_id}"
                entry = material_entry(facts, node)
                uses = self._material_tool_uses(
                    "image", tool="sandbox_generate_image",
                    allowed=entry["allowed_resolutions"], bind_required=False,
                )
                uses = tuple(
                    replace(use, resolutions=use.resolutions & frozenset(entry["allowed_resolutions"]))
                    if use.resolutions else use
                    for use in uses
                    if not use.resolutions or use.resolutions & frozenset(entry["allowed_resolutions"])
                )
                targets.append(edge(node, input_uses=(
                    structured_fact(purpose=(
                        f"Declared role: {entry['role']}. Requirement: {entry['description']}"
                    )), *uses,
                )))
            return Evaluation.of(targets)

        spec_version = self.facts.evidence_version(frame_spec_node)
        groups = self._frame_execution_groups(project, video)
        execution_group = groups[frame_index - 1] if groups else None
        return Requirement(
            id=requirement_id, kind="asset",
            subject=(f"Provide video {video} preview frame {frame_index:02d} "
                     f"for blueprint shot {frame_index}"),
            contract=contract("frame", "provided"),
            execution_group=execution_group,
            input_selections=(InputSelection(
                producer_id=frame_spec_node,
                producer_version=spec_version,
                path=("frames", frame_index - 1),
                label="FRAME TARGET",
                qualifiers={"frame": frame_index, "blueprint shot": frame_index},
                display_data={
                    "SELECTED ENTRY": {"visual_description": item.get("visual_description")},
                    "SELECTED image_ids": list(item.get("image_ids", [])),
                },
            ),),
            deps=(
                requires(
                    "frame-spec", frame_spec_node,
                    input_uses=(structured_fact("frames", purpose=(
                        "Use the entry selected by this frame's FRAME TARGET: its "
                        "visual_description is the direct picture requirement and its "
                        "image_ids are the only bound image references."
                    ), resolutions=("provided",)),),
                ),
                requires(
                    "blueprint", f"video_blueprint/{project}/{video}", input_uses=(
                        read_content("path", purpose=(
                            "Read the complete script for story, timing and continuity; the "
                            "current shot is identified by this frame's FRAME TARGET."
                        )),
                    ),
                ),
                requires("definition", f"video_spec_definition/{project}/{video}"),
                requires("image-model", f"image_model/{project}/{video}"),
                requires("storyboard-mode", f"storyboard_mode/{project}/{video}"),
                conditional(
                    "frame-images", fact_producers=(frame_spec_node,),
                    resolver=frame_images,
                ),
            ),
            guidance={
                "safety_rejection": "keeps this frame ready",
            },
        )

    def _declare_execution_scope(self, requirement_id: str) -> Requirement:
        parts = self._segments(requirement_id, "execution_scope", 3)
        project, execution_round = parts[1], parts[2]
        prep_round = self._project_state(project).get("preparation_round", "01")
        prep = f"preparation_scope/{project}/{prep_round}"

        def packages(facts: Facts) -> Evaluation:
            evidence = facts.evidence_for(prep)
            if evidence is None:
                return Evaluation.unknown()
            return Evaluation.of(
                edge(f"package_confirmation/{project}/{video}")
                for video in ids(evidence.data.get("videos"))
            )

        return Requirement(
            id=requirement_id,
            kind="question",
            subject=f"Select confirmed packages for execution round {execution_round}",
            contract=contract("execution-scope", "selected"),
            deps=(
                conditional("confirmed-packages", fact_producers=(prep,), resolver=packages),
            ),
        )

    def _declare_delivery(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "delivery", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        model_node = f"generation_model/{project}/{video}/{execution_round}"

        def result_branch(expected: str, target_id: str) -> Resolver:
            def resolve(facts: Facts) -> Evaluation:
                mode = execution_mode(facts, video, execution_round, project=project)
                if mode is None:
                    return Evaluation.unknown()
                return Evaluation.of([edge(target_id)]) if mode == expected else Evaluation.of()

            return resolve

        return Requirement(
            id=requirement_id,
            kind="action",
            subject=f"Present the finished result for video {video}",
            contract=contract("delivery", "presented"),
            deps=(
                requires("generation-model", model_node),
                conditional(
                    "direct-result",
                    fact_producers=(model_node,),
                    resolver=result_branch(
                        "direct", f"direct_result/{project}/{video}/{execution_round}"
                    ),
                ),
                conditional(
                    "lowered-result",
                    fact_producers=(model_node,),
                    resolver=result_branch(
                        "lowering", f"assembled_result/{project}/{video}/{execution_round}"
                    ),
                ),
            ),
            guidance={"evidence": "successful present_sandbox_file presentation"},
        )

    def _declare_generation_model(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "generation_model", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        return Requirement(
            id=requirement_id,
            kind="question",
            subject=f"Read the UI-injected video-model setting for video {video}",
            contract=contract("generation-model", "reported"),
            deps=(
                requires("confirmed-package", f"package_confirmation/{project}/{video}"),
                requires("execution-authorization", f"execution_scope/{project}/{execution_round}"),
            ),
        )

    def _declare_direct_result(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "direct_result", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        return Requirement(
            id=requirement_id,
            kind="asset",
            subject=f"Generate the direct result for video {video}",
            contract=contract("video-result", "generated"),
            deps=(requires(
                "preflight", f"preflight/{project}/{video}/{execution_round}"
            ),),
            guidance={"blocked": "records a blocker but does not satisfy this node"},
        )

    def _declare_assembled_result(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "assembled_result", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        count = part_count(self.facts, video, execution_round, project=project)
        return Requirement(
            id=requirement_id,
            kind="asset",
            subject=f"Assemble the lowered result for video {video}",
            contract=contract("assembled-result", "generated"),
            deps=(requires(
                "parts",
                *(f"part_result/{project}/{video}/{execution_round}/{part:02d}"
                  for part in range(1, count + 1)),
            ),),
        )

    def _declare_part_result(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "part_result", 3)
        project, video, execution_round = parts[1], parts[2], parts[3]
        part = positive_integer(parts[4], f"{requirement_id}.part")
        return Requirement(
            id=requirement_id,
            kind="asset",
            subject=f"Generate video {video} part {part:02d}",
            contract=contract("part-result", "generated"),
            deps=(requires(
                "part-preflight", f"part_preflight/{project}/{video}/{execution_round}/{part:02d}"
            ),),
        )

    def _declare_part_preflight(self, requirement_id: str) -> Requirement:
        _, project, video, execution_round, part = self._scoped_segments(
            requirement_id, "part_preflight", 3
        )
        return Requirement(
            id=requirement_id, kind="action",
            subject=f"Verify the exact executable input for video {video} part {part}",
            contract=contract("part-preflight", "passed"),
            deps=(
                requires("generation-model", f"generation_model/{project}/{video}/{execution_round}"),
                requires(
                    "part-input", f"part_input/{project}/{video}/{execution_round}/{part}",
                    input_uses=(read_content("path", purpose=(
                        "Verify this part's complete executable prompt against its actual ordered "
                        "media arguments, including the selected previous end frame."
                    ), resolutions=("provided",)),),
                ),
            ),
        )

    def _declare_continuity_choice(self, requirement_id: str) -> Requirement:
        _, project, video, execution_round, part = self._scoped_segments(
            requirement_id, "continuity_choice", 3
        )
        number = positive_integer(part, f"{requirement_id}.part")
        if number < 2:
            raise ModelError("the first part has no previous-frame choice")
        return Requirement(
            id=requirement_id, kind="decision",
            subject=f"Decide whether video {video} part {part} uses the previous part's end frame",
            contract=contract("continuity-choice", "reported"),
            deps=(
                requires("video-blueprint", f"video_blueprint/{project}/{video}",
                         input_uses=(read_content("path", purpose=(
                             "Decide whether the accepted transition needs actual end-frame "
                             "continuity; preserve the confirmed creative meaning."
                         ), resolutions=("provided",)),)),
                requires("runtime-manifest", f"runtime_manifest/{project}/{video}/{execution_round}",
                         input_uses=(read_content("path", purpose=(
                             "Read both adjacent part boundaries and their planned handoff "
                             "before deciding whether to use the previous end frame."
                         ), resolutions=("provided",)),)),
                requires("adjacent-part-specs",
                         f"part_spec/{project}/{video}/{execution_round}/{number - 1:02d}",
                         f"part_spec/{project}/{video}/{execution_round}/{part}"),
            ),
        )

    def _declare_last_frame(self, requirement_id: str) -> Requirement:
        _, project, video, execution_round, part = self._scoped_segments(
            requirement_id, "last_frame", 3
        )
        return Requirement(
            id=requirement_id, kind="asset",
            subject=f"Extract the actual final frame of video {video} part {part}",
            contract=contract("last-frame", "provided"),
            deps=(requires(
                "source-result", f"part_result/{project}/{video}/{execution_round}/{part}",
                input_uses=(tool_argument("path", target="frame-extraction.input_video",
                    purpose="Extract a decodable last frame from this exact current generated video.",
                    resolutions=("generated",)),),
            ),),
        )

    def _declare_preflight(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "preflight", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        model_node = f"generation_model/{project}/{video}/{execution_round}"

        def direct_payload(facts: Facts) -> Evaluation:
            mode = execution_mode(facts, video, execution_round, project=project)
            if mode is None:
                return Evaluation.unknown()
            if mode == "direct":
                return Evaluation.of([
                    edge(f"direct_payload/{project}/{video}/{execution_round}")
                ])
            return Evaluation.of()

        return Requirement(
            id=requirement_id,
            kind="action",
            subject=f"Verify the exact generation payload for video {video}",
            contract=contract("preflight", "passed"),
            deps=(
                requires("generation-model", model_node),
                conditional("direct-payload", fact_producers=(model_node,), resolver=direct_payload),
            ),
        )

    def _declare_direct_payload(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "direct_payload", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        spec = f"video_spec_definition/{project}/{video}"
        mode = f"storyboard_mode/{project}/{video}"

        def visual_overview(facts: Facts) -> Evaluation:
            evidence = facts.evidence_for(mode)
            if evidence is None:
                return Evaluation.unknown()
            answer = evidence.data.get("mode")
            if answer == "visual":
                return Evaluation.of([
                    edge(
                        f"storyboard_overview/{project}/{video}",
                        input_uses=(
                            tool_argument(
                                "path",
                                target="sandbox_generate_video.ImageList",
                                purpose=(
                                    "Bind the accepted storyboard overview as the visual "
                                    "structure input for the direct executable payload."
                                ),
                                resolutions=("derived",),
                            ),
                        ),
                    )
                ])
            if answer == "script_only":
                return Evaluation.of()
            raise ModelError(f"invalid storyboard mode: {answer!r}")

        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject=f"Bind the exact direct payload for video {video}",
            contract=contract("direct-payload", "provided"),
            deps=(
                requires("confirmed-package", f"package_confirmation/{project}/{video}"),
                requires(
                    "generation-model", f"generation_model/{project}/{video}/{execution_round}"
                ),
                requires(
                    "video-blueprint",
                    f"video_blueprint/{project}/{video}",
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Compile the video blueprint into one model-specific executable "
                                "prompt; never pass the video blueprint path directly as PromptPath."
                            ),
                            resolutions=("provided",),
                        ),
                    ),
                ),
                requires("definition", spec),
                self._media_dependency(project, video, tool="sandbox_generate_video"),
                conditional(
                    "visual-overview",
                    fact_producers=(mode,),
                    resolver=visual_overview,
                ),
            ),
        )

    def _declare_runtime_manifest(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "runtime_manifest", 2)
        project, video, execution_round = parts[1], parts[2], parts[3]
        mode = f"storyboard_mode/{project}/{video}"

        def visual_manifest(facts: Facts) -> Evaluation:
            evidence = facts.evidence_for(mode)
            if evidence is None:
                return Evaluation.unknown()
            answer = evidence.data.get("mode")
            if answer == "visual":
                return Evaluation.of([
                    edge(
                        f"storyboard_manifest/{project}/{video}",
                        input_uses=(
                            read_content(
                                "path",
                                purpose=(
                                    "Map the accepted storyboard shot/source annotations into "
                                    "the lowered part boundaries."
                                ),
                                resolutions=("provided",),
                            ),
                        ),
                    )
                ])
            if answer == "script_only":
                return Evaluation.of()
            raise ModelError(f"invalid storyboard mode: {answer!r}")

        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject=("Provide the "
                     f"{part_count(self.facts, video, execution_round, project=project)}-part "
                     "runtime manifest"),
            contract=contract("runtime-manifest", "provided"),
            deps=(
                requires("confirmed-package", f"package_confirmation/{project}/{video}"),
                requires(
                    "generation-model", f"generation_model/{project}/{video}/{execution_round}"
                ),
                requires(
                    "video-blueprint",
                    f"video_blueprint/{project}/{video}",
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Lower the video blueprint into contiguous model-bounded parts "
                                "without rewriting its creative semantics."
                            ),
                            resolutions=("provided",),
                        ),
                    ),
                ),
                conditional(
                    "visual-storyboard-manifest",
                    fact_producers=(mode,),
                    resolver=visual_manifest,
                ),
            ),
        )


    def _declare_runtime_materials(self, requirement_id: str) -> Requirement:
        _, project, video, execution_round = self._scoped_segments(requirement_id, "runtime_materials", 2)
        sources = tuple(material_entries(self.facts, project, video))
        return Requirement(
            id=requirement_id, kind="collection", subject="Prepare every declared runtime entity",
            focusable=False, contract=None,
            deps=(
                requires("definition", f"video_spec_definition/{project}/{video}"),
                requires("model", f"generation_model/{project}/{video}/{execution_round}"),
                self._media_dependency(project, video),
                conditional("runtime-entities", fact_producers=sources,
                    resolver=lambda facts: Evaluation.of(
                        edge(f"runtime_anchor/{project}/{video}/{execution_round}/{key}")
                        for key in runtime_required_anchors(facts, video, execution_round, project=project)
                    )),
            ),
        )


    def _declare_part_spec(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "part_spec", 3)
        project, video, execution_round, part = parts[1], parts[2], parts[3], parts[4]
        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject=f"Confirm duration and material bindings for video {video} part {part}",
            contract=contract("part-spec", "confirmed"),
            deps=(
                requires(
                    "runtime-manifest", f"runtime_manifest/{project}/{video}/{execution_round}",
                    input_uses=(read_content("path", purpose=(
                        "Read this part's mapped boundaries and semantic content to determine "
                        "which declared identities it actually uses."
                    ), resolutions=("provided",)),),
                ),
                requires(
                    "definition", f"video_spec_definition/{project}/{video}",
                    input_uses=(structured_fact("images", "audios", "videos", purpose=(
                        "Select this part's media IDs by reading the blueprint's narrative. "
                        "These are declared identities, not file paths or argument positions."
                    ), resolutions=("provided",)),),
                ),
                requires(
                    "video-blueprint", f"video_blueprint/{project}/{video}",
                    input_uses=(read_content("path", purpose=(
                        "Read the canonical creative content for the mapped part; use its "
                        "visual and speaking roles to select material identities without "
                        "changing the accepted story."
                    ), resolutions=("provided",)),),
                ),
            ),
        )

    def _declare_runtime_anchor(self, requirement_id: str) -> Requirement:
        _, project, video, execution_round, kind, identity = self._scoped_segments(requirement_id, "runtime_anchor", 4)
        key = f"{kind}/{identity}"
        entry = runtime_required_anchors(self.facts, video, execution_round, project=project).get(key)
        if entry is None:
            raise ModelError(f"{requirement_id} has no declared runtime identity")
        deps = [
            requires("source", entry["source"], input_uses=(structured_fact(
                purpose="Use this original media or auto authorization without requesting redundant approval."
            ),)),
            requires("blueprint", f"video_blueprint/{project}/{video}",
                     input_uses=(read_content("path", purpose="Materialize this declared object's identity and constraints."),)),
            requires("model", f"generation_model/{project}/{video}/{execution_round}"),
        ]
        reuse = entry["strategy"] == "reuse"
        return Requirement(
            id=requirement_id, kind="asset",
            subject=f"{'Reuse' if reuse else 'Materialize'} one {kind} anchor for {identity}",
            contract=None if reuse else contract("runtime-anchor", "provided"),
            deps=tuple(deps), focusable=not reuse,
            guidance={"anchor": dict(entry), "evidence_fields": ["path", "checks"]},
        )


    def _declare_part_sheet(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "part_sheet", 3)
        project, video, execution_round, part = parts[1], parts[2], parts[3], parts[4]
        return Requirement(
            id=requirement_id,
            kind="asset",
            subject=f"Compose the storyboard sheet for video {video} part {part}",
            contract=contract("part-sheet", "derived"),
            deps=(
                requires(
                    "part-spec", f"part_spec/{project}/{video}/{execution_round}/{part}"
                ),
                requires(
                    "storyboard-overview", f"storyboard_overview/{project}/{video}"
                ),
            ),
        )

    def _declare_part_input(self, requirement_id: str) -> Requirement:
        parts = self._scoped_segments(requirement_id, "part_input", 3)
        project, video, execution_round, part = parts[1], parts[2], parts[3], parts[4]
        part_spec = f"part_spec/{project}/{video}/{execution_round}/{part}"
        video_blueprint = f"video_blueprint/{project}/{video}"
        runtime_manifest = f"runtime_manifest/{project}/{video}/{execution_round}"

        storyboard_mode = f"storyboard_mode/{project}/{video}"
        continuity_deps: tuple[Dependency, ...] = ()
        if int(part) > 1:
            choice_id = f"continuity_choice/{project}/{video}/{execution_round}/{part}"

            def previous_frame(facts: Facts) -> Evaluation:
                choice = facts.evidence_for(choice_id)
                if choice is None:
                    return Evaluation.unknown()
                if choice.data.get("use_last_frame") is True:
                    return Evaluation.of([edge(
                        f"last_frame/{project}/{video}/{execution_round}/{int(part) - 1:02d}",
                        input_uses=(tool_argument(
                            "path", target="sandbox_generate_video.ImageList",
                            purpose=("Bind this actual previous end frame as a continuity image; "
                                     "assign its final one-based Image[N] position alongside "
                                     "this part's identity assets and optional storyboard sheet."),
                            resolutions=("provided",),
                        ),),
                    )])
                if choice.data.get("use_last_frame") is False:
                    return Evaluation.of()
                raise ModelError("continuity choice must provide a boolean use_last_frame")

            continuity_deps = (
                requires("continuity-choice", choice_id,
                         input_uses=(structured_fact(purpose=(
                             "Apply this part's accepted process choice; when false, compile "
                             "from the planned handoff without a previous generated frame."
                         )),)),
                conditional("previous-end-frame", fact_producers=(choice_id,), resolver=previous_frame),
            )

        def materials(facts: Facts) -> Evaluation:
            targets = []
            for key, entry in selected_runtime_anchors(facts, project, video, execution_round, part).items():
                if entry.get("source"):
                    source = entry["source"]
                    targets.append(edge(source, input_uses=self._material_tool_uses(
                        key.split("/")[0], tool="sandbox_generate_video",
                        allowed=material_entry(facts, source)["allowed_resolutions"],
                    )))
                if entry["strategy"] == "generate":
                    targets.append(edge(f"runtime_anchor/{project}/{video}/{execution_round}/{key}",
                                        input_uses=self._runtime_anchor_tool_uses(key.split("/")[0])))
            return Evaluation.of(targets)

        def sheet(facts: Facts) -> Evaluation:
            evidence = facts.evidence_for(storyboard_mode)
            if evidence is None:
                return Evaluation.unknown()
            if evidence.data.get("mode") == "visual":
                return Evaluation.of([
                    edge(
                        f"part_sheet/{project}/{video}/{execution_round}/{part}",
                        input_uses=(
                            tool_argument(
                                "path",
                                target="sandbox_generate_video.ImageList",
                                purpose=(
                                    "Bind the accepted part storyboard sheet as the visual "
                                    "structure input for this part's executable payload."
                                ),
                                resolutions=("derived",),
                            ),
                        ),
                    )
                ])
            return Evaluation.of()

        return Requirement(
            id=requirement_id,
            kind="artifact",
            subject=f"Provide the self-contained local input for video {video} part {part}",
            contract=contract("part-input", "provided"),
            deps=(
                requires(
                    "runtime-manifest",
                    runtime_manifest,
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Use this part's accepted boundary, local timeline, and handoff "
                                "mapping when compiling the executable input."
                            ),
                            resolutions=("provided",),
                        ),
                    ),
                ),
                requires("runtime-materials", f"runtime_materials/{project}/{video}/{execution_round}"),
                requires("part-spec", part_spec),
                *continuity_deps,
                requires(
                    "video-blueprint",
                    video_blueprint,
                    input_uses=(
                        read_content(
                            "path",
                            purpose=(
                                "Compile this part's final executable prompt from the canonical "
                                "plan and the accepted part boundary; do not invent a parallel "
                                "creative source."
                            ),
                            resolutions=("provided",),
                        ),
                    ),
                ),
                conditional("part-materials", fact_producers=(part_spec,), resolver=materials),
                conditional(
                    "visual-part-sheet",
                    fact_producers=(storyboard_mode,),
                    resolver=sheet,
                ),
            ),
        )

    def _declare_continuation_decision(self, requirement_id: str) -> Requirement:
        project = self._segments(requirement_id, "continuation_decision", 3)[1]
        execution_round = str(
            self._project_state(project).get("execution_round", "01")
        )
        execution = f"execution_scope/{project}/{execution_round}"

        def deliveries(facts: Facts) -> Evaluation:
            selection = facts.evidence_for(execution)
            if selection is None:
                return Evaluation.unknown()
            return Evaluation.of(
                edge(
                    f"delivery/{project}/{video}/{execution_round}",
                    input_uses=(structured_fact(
                        "path", purpose=("Identify the initial delivery baseline, not the latest "
                                         "free-form revision. Use the actual latest output for "
                                         "presentation and user acceptance."),
                    ),),
                )
                for video in ids(selection.data.get("videos"))
            )

        return Requirement(
            id=requirement_id,
            kind="question",
            subject="Review delivered results, freely revise here, or choose the next project action",
            contract=contract("continuation", "selected"),
            deps=(
                requires("execution-scope", execution),
                conditional("delivered-results", fact_producers=(execution,), resolver=deliveries),
            ),
        )


def validate_requirement_evidence(
    requirement: Requirement,
    evidence: Evidence,
    facts: Facts,
) -> None:
    """Validate the evidence payload owned by one requirement type.

    Graph contracts decide which resolution can close a node. This function
    decides whether the payload actually proves that resolution. Keeping the
    checks here prevents a generic ``provided`` event from becoming a closure
    backdoor for unrelated requirement types.
    """

    prefix = requirement.id.split("/", 1)[0]
    data = evidence.data

    def text_field(name: str) -> str:
        return required_text(data.get(name), f"{requirement.id}.{name}")

    def path_field() -> None:
        text_field("path")

    if prefix == "communication_language":
        text_field("language")
        return

    if prefix == "information_understanding":
        path_field()
        return

    if prefix == "creative_research":
        if evidence.resolution == "provided":
            path_field()
            text_field("async_task_id")
            if data.get("terminal") is not True:
                raise ModelError(f"{requirement.id}.terminal must be true")
            terminal_status = text_field("terminal_status")
            if terminal_status != "succeeded":
                raise ModelError(
                    f"{requirement.id}.terminal_status must be succeeded; "
                    "failed and non-final async task states cannot satisfy creative research"
                )
            text_field("attestation")
        else:
            text_field("user_evidence")
        return

    if prefix == "story_master":
        positive_integer(data.get("shots"), f"{requirement.id}.shots")
        duration = positive_integer(data.get("duration_ms"), f"{requirement.id}.duration_ms")
        if duration < MIN_VIDEO_DURATION_MS:
            raise ModelError(f"{requirement.id}.duration_ms must be at least 4000")
        path_field()
        return

    if prefix == "direction_set":
        planned = positive_integer(data.get("planned_total"), f"{requirement.id}.planned_total")
        directions = direction_entries(data.get("directions"), requirement.id)
        if len(directions) != planned:
            raise ModelError(
                f"{requirement.id}.planned_total is {planned}, but directions has "
                f"{len(directions)} entries"
            )
        return

    if prefix in {"preparation_scope", "execution_scope"}:
        selected = ids(data.get("videos"))
        if not selected:
            raise ModelError(f"{requirement.id}.videos must select at least one video")
        parts = requirement.id.split("/")
        project = parts[1]
        if prefix == "preparation_scope":
            direction_set = facts.evidence_for(f"direction_set/{project}")
            directions = direction_set.data.get("directions") if direction_set else None
            if not isinstance(directions, Mapping):
                raise ModelError(f"direction_set/{project}.directions is unavailable")
            unknown = sorted(set(selected) - direction_entries(directions, f"direction_set/{project}").keys())
            if unknown:
                raise ModelError(
                    f"{requirement.id}.videos contains unknown directions: {unknown}"
                )
        else:
            states = facts.get("project_states", {})
            state = states.get(project, {}) if isinstance(states, Mapping) else {}
            prep_round = str(state.get("preparation_round", "01"))
            preparation = facts.evidence_for(f"preparation_scope/{project}/{prep_round}")
            prepared = set(ids(preparation.data.get("videos"))) if preparation else set()
            unknown = sorted(set(selected) - prepared)
            if unknown:
                raise ModelError(
                    f"{requirement.id}.videos contains unprepared packages: {unknown}"
                )
        return

    if prefix in {"image_model", "generation_model"}:
        model = text_field("model")
        source = text_field("source")
        allowed_sources = {"system-reminder", "conservative-fallback"}
        if source not in allowed_sources:
            raise ModelError(
                f"{requirement.id}.source must be system-reminder or conservative-fallback"
            )
        if source == "conservative-fallback" and model != "unknown":
            raise ModelError(
                f"{requirement.id} conservative-fallback must report model='unknown'"
            )
        return

    if prefix == "storyboard_mode":
        mode = text_field("mode")
        if mode not in {"visual", "script_only"}:
            raise ModelError(f"{requirement.id}.mode must be visual or script_only")
        return

    if prefix == "video_blueprint":
        path_field()
        validate_blueprint(data, requirement.id)
        return

    if prefix == "video_spec_definition":
        validate_media_definition(data, requirement.id)
        return

    if prefix == "frame_spec_definition":
        _, project, video = requirement.id.split("/")
        validate_frame_spec_definition(data, facts, project, video, requirement.id)
        return

    if prefix in MATERIALS.values():
        entry = requirement.guidance["declaration"]
        if evidence.resolution == "provided":
            paths = data.get("paths")
            if not isinstance(paths, list) or not paths:
                raise ModelError(f"{requirement.id}.paths must be a non-empty list")
            text_values(paths, f"{requirement.id}.paths")
            if entry.get("review_required", False):
                text_field("user_evidence")
                if text_field("presentation_tool") != "present_sandbox_file":
                    raise ModelError("present the actual media before recording user approval")
        else:
            text_field("user_evidence")
            if evidence.resolution == "waived":
                text_field("reason")
        return

    if prefix == "product_state_coverage":
        _, project, video = requirement.id.split("/")
        expected = {node.rsplit("/", 1)[1] for node in coverage_products(facts, project, video)}
        products = data.get("products")
        if not isinstance(products, Mapping):
            raise ModelError(f"{requirement.id}.products must be a mapping")
        actual = {
            graph_segment_id(product_id, f"{requirement.id}.product ID")
            for product_id in products
        }
        if actual != expected:
            raise ModelError(
                f"{requirement.id}.products must cover exactly the VideoSpec products"
            )
        allowed = {"covered", "reference_confirmed", "risk_accepted"}
        for product_id, result in products.items():
            if not isinstance(result, Mapping):
                raise ModelError(
                    f"{requirement.id}.products[{product_id!r}] must be a mapping"
                )
            status = required_text(
                result.get("status"),
                f"{requirement.id}.products[{product_id!r}].status",
            )
            if status not in allowed:
                raise ModelError(
                    f"{requirement.id}.products[{product_id!r}].status must be "
                    "covered, reference_confirmed or risk_accepted"
                )
            required_text(
                result.get("assessment"),
                f"{requirement.id}.products[{product_id!r}].assessment",
            )
            if status in {"reference_confirmed", "risk_accepted"}:
                required_text(
                    result.get("user_evidence"),
                    f"{requirement.id}.products[{product_id!r}].user_evidence",
                )
            if status == "reference_confirmed" and (
                result.get("presentation_tool") != "present_sandbox_file"
            ):
                raise ModelError(
                    f"{requirement.id}.products[{product_id!r}].presentation_tool "
                    "must be present_sandbox_file"
                )
        return

    if prefix in {
        "frame",
        "storyboard_overview",
        "storyboard_manifest",
        "video_blueprint",
        "direct_payload",
        "part_sheet",
        "part_input",
        "direct_result",
        "part_result",
        "last_frame",
        "assembled_result",
    }:
        path_field()
        return

    if prefix == "runtime_manifest":
        path_field()
        parts = requirement.id.split("/")
        project, video, execution_round = parts[1], parts[2], parts[3]
        validate_runtime_parts(data.get("parts"), runtime_constraints(
            facts, video, execution_round, project=project
        ), requirement.id)
        return

    if prefix in {"package_confirmation", "delivery"}:
        if text_field("presentation_tool") != "present_sandbox_file":
            raise ModelError(
                f"{requirement.id}.presentation_tool must be present_sandbox_file"
            )
        if prefix == "delivery":
            path_field()
        else:
            text_field("user_evidence")
        return

    if prefix == "part_spec":
        duration = positive_integer(data.get("duration_ms"), f"{requirement.id}.duration_ms")
        parts = requirement.id.split("/")
        project, video, execution_round = parts[1], parts[2], parts[3]
        part = positive_integer(parts[4], f"{requirement.id}.part")
        durations = runtime_durations(
            facts, video, execution_round, project=project
        )
        if part > len(durations) or duration != durations[part - 1]:
            raise ModelError(
                f"{requirement.id}.duration_ms must equal the accepted runtime manifest part duration"
            )
        if not isinstance(data.get("materials"), Mapping):
            raise ModelError(f"{requirement.id}.materials must be a mapping")
        spec = facts.evidence_for(f"video_spec_definition/{project}/{video}")
        if set(data["materials"]) != set(MATERIALS):
            raise ModelError("part materials must explicitly declare images, audios and videos")

        for field_name in MATERIALS:
            declared = set(spec.data[field_name])
            selected = set(ids(data["materials"].get(field_name)))
            for identity in selected & set(spec.data[field_name]):
                source = facts.evidence_for(f"{MATERIALS[field_name]}/{project}/{video}/{identity}")
                if source and source.resolution == "waived":
                    raise ModelError("part materials cannot reference waived optional media")
            if selected - declared:
                raise ModelError(f"{requirement.id}.materials references undeclared {field_name}")
        return


    if prefix == "runtime_anchor":
        path_field()
        checks = data.get("checks")
        if not isinstance(checks, Mapping) or not checks or any(value is not True for value in checks.values()):
            raise ModelError(f"{requirement.id}.checks must be a non-empty all-true mapping")
        if requirement.guidance["anchor"].get("voice_sample", False):
            duration = positive_integer(data.get("duration_ms"), f"{requirement.id}.duration_ms")
            if duration != 3000:
                raise ModelError("generated runtime voice anchor must be exactly 3000ms")
        return


    if prefix == "continuity_choice":
        if type(data.get("use_last_frame")) is not bool:
            raise ModelError(f"{requirement.id}.use_last_frame must be a boolean")
        text_field("reason")
        return

    if prefix in {"preflight", "part_preflight"}:
        checks = data.get("checks")
        if (
            not isinstance(checks, Mapping)
            or not checks
            or any(value is not True for value in checks.values())
        ):
            raise ModelError(f"{requirement.id}.checks must be a non-empty all-passing mapping")
        return

    if prefix == "continuation_decision":
        choice = continuation_choice(data.get("choice"))
        if choice == "finish":
            text_field("user_evidence")
        return

    if prefix == "start_new_project":
        text_field("project")
        return

    if prefix in {"direction"}:
        return

    raise ModelError(f"no typed evidence validator for {requirement.id}")


def runtime_required_anchors(
    facts: Facts,
    video: str,
    execution_round: str,
    *,
    project: str | None = None,
) -> dict[str, dict[str, Any]]:
    """All original entities; existence never depends on part membership."""
    result = {}
    project = project or required_text(facts.get("active_project"), "active_project")
    for source, declaration in material_entries(facts, project, video).items():
        original = facts.evidence_for(source)
        if original is None or original.resolution == "waived":
            continue
        kind, _, _, identity = source.split("/")
        concrete = original.resolution == "provided"
        result[f"{kind}/{identity}"] = {
            "source": source,
            "strategy": "reuse" if concrete else "generate",
            "authorization": "existing" if concrete else "source_auto",
            "voice_sample": declaration.get("voice_sample", False),
            "declaration": dict(declaration),
        }
    return result


def selected_runtime_anchors(
    facts: Facts, project: str, video: str, execution_round: str, part: str,
) -> dict[str, dict[str, Any]]:
    spec = facts.evidence_for(f"part_spec/{project}/{video}/{execution_round}/{part}")
    if spec is None:
        return {}
    entries = runtime_required_anchors(facts, video, execution_round, project=project)
    selected = {f"{kind}/{identity}" for group, kind in MATERIALS.items()
                for identity in ids(spec.data["materials"].get(group))}
    return {key: entry for key, entry in entries.items() if key in selected}


def text_values(value: Any, label: str = "values") -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw = value.split(",")
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        raw = list(value)
    else:
        raise ModelError(f"{label} must be a list of strings")
    result: list[str] = []
    seen: set[str] = set()
    for item in raw:
        normalized = required_text(item, label)
        if normalized in seen:
            raise ModelError(f"{label} contains duplicate value: {normalized}")
        seen.add(normalized)
        result.append(normalized)
    return result


def graph_segment_id(value: Any, label: str) -> str:
    normalized = required_text(value, label)
    if (
        normalized in {".", ".."}
        or "/" in normalized
        or any(unicodedata.category(char).startswith("C") for char in normalized)
    ):
        raise ModelError(f"{label} must be a safe single-segment ID")
    return normalized


def direction_entries(value: Any, label: str) -> Mapping[str, Mapping[str, Any]]:
    """Preserve DirectionSet identity exactly; never rename accepted mapping keys."""
    if not isinstance(value, Mapping):
        raise ModelError(f"{label}.directions must be a mapping")
    canonical_ids: set[str] = set()
    for identity, direction in value.items():
        canonical = graph_segment_id(identity, f"{label}.direction ID")
        if canonical != identity or canonical in canonical_ids:
            raise ModelError("direction IDs must be unique canonical single segments")
        canonical_ids.add(canonical)
        if not isinstance(direction, Mapping):
            raise ModelError(f"{label}.directions[{identity!r}] must be a mapping")
    return value


# Requirement prefixes whose ID carries the owning project as the segment
# immediately after the prefix. GOAL/start_new_project and other lifecycle
# nodes are deliberately absent: they are never erasable business facts.
PROJECT_SCOPED_PREFIXES = frozenset({
    "communication_language", "information_understanding", "creative_research",
    "story_master", "direction_set", "direction", "preparation_scope",
    "execution_scope", "video_blueprint", "video_spec_definition",
    "product_state_coverage", "storyboard_mode", "image_model",
    "frame_spec_definition", "storyboard_manifest", "storyboard_overview",
    "frame", "package_confirmation", "generation_model", "direct_payload",
    "runtime_manifest", "part_spec", "runtime_anchor", "part_sheet",
    "part_input", "continuity_choice", "last_frame", "preflight",
    "part_preflight", "direct_result", "part_result", "assembled_result",
    "delivery", "image", "audio", "video",
})
LIFECYCLE_PREFIXES = frozenset({
    "GOAL", "start_new_project", "project_goal", "project_close",
    "continuation_decision", "project",
})


def requirement_owner(requirement_id: str) -> tuple[str | None, str]:
    """Return (project, kind) for one requirement ID.

    ``project`` is None for lifecycle/control nodes and for unknown shapes.
    Parsing never depends on the node being currently materialized.
    """
    parts = requirement_id.split("/")
    prefix = parts[0]
    if prefix in LIFECYCLE_PREFIXES or prefix not in PROJECT_SCOPED_PREFIXES:
        return None, "lifecycle" if prefix in LIFECYCLE_PREFIXES else "unknown"
    if len(parts) < 2:
        raise ModelError(f"invalid {prefix} requirement ID: {requirement_id}")
    project = parts[1]
    if not project:
        raise ModelError(f"invalid {prefix} requirement ID: {requirement_id}")
    return project, "business"


def ids(value: Any) -> list[str]:
    return [graph_segment_id(item, "ID") for item in text_values(value, "IDs")]


def required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ModelError(f"{label} must be non-empty single-line text")
    return value.strip()


def continuation_choice(value: Any) -> str:
    """Use the exact stored enum in validation, replay, and graph evaluation."""
    if not isinstance(value, str) or value not in {"prepare", "execute", "extend", "finish", "pause"}:
        raise ModelError(f"invalid continuation choice: {value!r}")
    return value


def positive_integer(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ModelError(f"{label} must be a positive integer")
    if isinstance(value, str) and not value.isdigit():
        raise ModelError(f"{label} must be a positive integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ModelError(f"{label} must be a positive integer") from exc
    if number <= 0:
        raise ModelError(f"{label} must be a positive integer")
    return number


def image_route(model: Any) -> str:
    normalized = str(model or "unknown").strip()
    return "route_a" if normalized in ROUTE_A_MODELS else "route_b"


def validate_blueprint(data: Mapping[str, Any], label: str) -> None:
    duration = positive_integer(data.get("duration_ms"), f"{label}.duration_ms")
    if duration < MIN_VIDEO_DURATION_MS:
        raise ModelError(f"{label}.duration_ms must be at least 4000")
    positive_integer(data.get("shots"), f"{label}.shots")
    required_text(data.get("ratio"), f"{label}.ratio")
    market = data.get("market_target")
    if not isinstance(market, Mapping):
        raise ModelError(f"{label}.market_target must be a mapping")
    for field_name in ("language", "country_region", "audience", "platform"):
        required_text(market.get(field_name), f"{label}.market_target.{field_name}")


def validate_frame_spec_definition(
    data: Mapping[str, Any],
    facts: Facts,
    project: str,
    video: str,
    label: str,
) -> None:
    """One shot, one frame: N entries, entry N describes shot N.

    The blueprint's effective `shots` owns the count; the evidence only
    supplies each representative instant's description and image bindings.
    PM validates structure and references, never aesthetic quality.
    """
    if set(data) != {"frames"}:
        raise ModelError(
            f"{label} must contain exactly frames; no path, count field, "
            "blueprint mapping or extra keys"
        )
    frames = data.get("frames")
    if not isinstance(frames, list) or not frames:
        raise ModelError(f"{label}.frames must be a non-empty list")
    blueprint = facts.evidence_for(f"video_blueprint/{project}/{video}")
    if blueprint is None:
        raise ModelError(f"{label} requires the current video blueprint")
    shot_count = positive_integer(
        blueprint.data.get("shots"), f"video_blueprint/{project}/{video}.shots"
    )
    if len(frames) != shot_count:
        raise ModelError(
            f"{label}.frames must have exactly {shot_count} entries to match the "
            f"blueprint's shots; received {len(frames)}. One frame per shot, no filling, "
            "truncation or reordering."
        )
    definition = facts.evidence_for(f"video_spec_definition/{project}/{video}")
    if definition is None:
        raise ModelError(f"{label} requires the current video_spec_definition")
    declared_images = set(definition.data["images"])
    for position, item in enumerate(frames, start=1):
        if not isinstance(item, Mapping):
            raise ModelError(f"{label}.frames[{position - 1}] must be a mapping")
        if set(item) != {"frame", "visual_description", "image_ids"}:
            raise ModelError(
                f"{label}.frames[{position - 1}] must contain exactly frame, "
                "visual_description and image_ids"
            )
        frame_number = item.get("frame")
        if isinstance(frame_number, bool) or not isinstance(frame_number, int):
            raise ModelError(f"{label}.frames[{position - 1}].frame must be a strict integer")
        if frame_number != position:
            raise ModelError(
                f"{label}.frames must be consecutively numbered 1..M in order; "
                f"position {position} declares frame {frame_number}"
            )
        description = item.get("visual_description")
        if not isinstance(description, str) or not description.strip():
            raise ModelError(
                f"{label}.frames[{position - 1}].visual_description must be non-empty text "
                "describing the frozen representative instant for this shot"
            )
        image_ids_field = item.get("image_ids")
        if not isinstance(image_ids_field, list):
            raise ModelError(
                f"{label}.frames[{position - 1}].image_ids must be a list"
            )
        seen_ids: set[str] = set()
        for image_id in image_ids_field:
            normalized = graph_segment_id(image_id, f"{label}.frames[{position - 1}].image ID")
            if normalized in seen_ids:
                raise ModelError(
                    f"{label}.frames[{position - 1}].image_ids contains duplicate: {normalized}"
                )
            seen_ids.add(normalized)
            if normalized not in declared_images:
                raise ModelError(
                    f"{label}.frames[{position - 1}].image_ids references undeclared "
                    f"image identity: {normalized}"
                )


def validate_media_definition(data: Mapping[str, Any], label: str) -> None:
    if set(data) != set(MATERIALS):
        raise ModelError(f"{label} must declare exactly images, audios and videos mappings; no shot mapping")
    for group, entries in data.items():
        if not isinstance(entries, Mapping):
            raise ModelError(f"{label}.{group} must be an ID-to-declaration mapping")
        normalized_ids: set[str] = set()
        for identity, entry in entries.items():
            normalized = graph_segment_id(identity, f"{label}.{group}.ID")
            if normalized != identity or normalized in normalized_ids:
                raise ModelError("material IDs must be unique canonical single segments")
            normalized_ids.add(normalized)
            if not isinstance(entry, Mapping):
                raise ModelError(f"{identity} declaration must be a mapping")
            allowed_fields = {"role", "description", "allowed_resolutions", "product_coverage",
                              "review_required", "continuity", "voice_sample", "supplemental_to"}
            if set(entry) - allowed_fields:
                raise ModelError(f"{identity} has unknown declaration fields")
            required_text(entry.get("role"), f"{identity}.role")
            required_text(entry.get("description"), f"{identity}.description")
            resolutions = entry.get("allowed_resolutions")
            if (not isinstance(resolutions, list) or not resolutions
                    or any(not isinstance(value, str) for value in resolutions)
                    or len(set(resolutions)) != len(resolutions)
                    or set(resolutions) - {"provided", "auto", "waived"}):
                raise ModelError(f"{identity}.allowed_resolutions must list provided/auto/waived")
            for flag in ("product_coverage", "review_required", "continuity", "voice_sample"):
                if flag in entry and type(entry[flag]) is not bool:
                    raise ModelError(f"{identity}.{flag} must be boolean")
            if entry.get("product_coverage"):
                if group != "images" or resolutions != ["provided"]:
                    raise ModelError("product coverage requires a concrete image; auto/waived is not allowed")
            if entry.get("voice_sample") and group != "audios":
                raise ModelError("voice samples must be audio")
            # Waivers are process policy, not inferred from a free-text role label.
            parent_id = entry.get("supplemental_to")
            if parent_id is not None:
                parent_id = graph_segment_id(parent_id, f"{identity}.supplemental_to")
                parent = data["images"].get(parent_id) if group == "images" else None
                if not isinstance(parent, Mapping) or not parent.get("product_coverage") or parent_id == identity:
                    raise ModelError("supplemental_to must name a distinct product_coverage image")
                if entry.get("product_coverage") or entry.get("voice_sample"):
                    raise ModelError("product/voice identity cannot be an optional supplemental reference")
            if "waived" in resolutions and parent_id is None:
                raise ModelError("waived is only allowed for supplemental product references with supplemental_to")


def generation_family(model: Any) -> str:
    normalized = str(model or "unknown").casefold()
    if "seedance" in normalized and "2.5" in normalized:
        return "seedance_2_5"
    if "seedance" in normalized and "2.0" in normalized:
        return "seedance_2_0"
    return "unknown"


def generation_max_duration_ms(model: Any) -> int:
    return 30_000 if generation_family(model) == "seedance_2_5" else 15_000


def execution_mode(
    facts: Facts,
    video: str,
    execution_round: str,
    *,
    project: str | None = None,
) -> str | None:
    project = project or required_text(facts.get("active_project"), "active_project")
    model = facts.evidence_for(
        f"generation_model/{project}/{video}/{execution_round}"
    )
    spec = facts.evidence_for(f"video_blueprint/{project}/{video}")
    if model is None or spec is None:
        return None
    duration = positive_integer(
        spec.data.get("duration_ms"), f"video_blueprint/{project}/{video}.duration_ms"
    )
    if duration < MIN_VIDEO_DURATION_MS:
        raise ModelError(
            f"video_blueprint/{project}/{video}.duration_ms must be at least 4000"
        )
    maximum = generation_max_duration_ms(model.data.get("model"))
    return "direct" if duration <= maximum else "lowering"


def part_count(
    facts: Facts,
    video: str,
    execution_round: str,
    *,
    project: str | None = None,
) -> int:
    project = project or required_text(facts.get("active_project"), "active_project")
    if execution_mode(facts, video, execution_round, project=project) != "lowering":
        raise ModelError(f"{video}/{execution_round} is not a lowering execution")
    model = facts.evidence_for(
        f"generation_model/{project}/{video}/{execution_round}"
    )
    spec = facts.evidence_for(f"video_blueprint/{project}/{video}")
    assert model is not None and spec is not None
    duration = positive_integer(
        spec.data.get("duration_ms"), f"video_blueprint/{project}/{video}.duration_ms"
    )
    maximum = generation_max_duration_ms(model.data.get("model"))
    count = (duration + maximum - 1) // maximum
    if count > MAX_RUNTIME_PARTS:
        raise ModelError(f"lowering would create {count} parts, above {MAX_RUNTIME_PARTS}")
    if duration < count * MIN_VIDEO_DURATION_MS:
        raise ModelError(f"{count} parts cannot all satisfy the 4000ms minimum")
    return count


def runtime_constraints(
    facts: Facts,
    video: str,
    execution_round: str,
    *,
    project: str | None = None,
) -> dict[str, int]:
    """PM owns count and bounds, not the semantic allocation of part durations."""

    project = project or required_text(facts.get("active_project"), "active_project")
    count = part_count(facts, video, execution_round, project=project)
    spec = facts.evidence_for(f"video_blueprint/{project}/{video}")
    assert spec is not None
    duration = positive_integer(
        spec.data.get("duration_ms"), f"video_blueprint/{project}/{video}.duration_ms"
    )
    maximum = generation_max_duration_ms(
        facts.evidence_for(
            f"generation_model/{project}/{video}/{execution_round}"
        ).data.get("model")
    )
    return {"part_count": count, "total_duration_ms": duration,
            "min_duration_ms": MIN_VIDEO_DURATION_MS, "max_duration_ms": maximum}


def validate_runtime_parts(parts: Any, constraints: Mapping[str, int], label: str) -> list[int]:
    """Validate the LLM's allocation without reading files or judging semantic cut quality."""
    if not isinstance(parts, list):
        raise ModelError(f"{label}.parts must be a list")
    if len(parts) != constraints["part_count"]:
        raise ModelError(f"{label}.parts must contain exactly {constraints['part_count']} parts")
    durations = []
    for index, item in enumerate(parts, start=1):
        if not isinstance(item, Mapping):
            raise ModelError(f"{label}.parts[{index}] must be a mapping")
        if positive_integer(item.get("part"), f"{label}.parts[{index}].part") != index:
            raise ModelError(f"{label}.parts must be ordered 1..N")
        duration = positive_integer(item.get("duration_ms"), f"{label}.parts[{index}].duration_ms")
        if not constraints["min_duration_ms"] <= duration <= constraints["max_duration_ms"]:
            raise ModelError(f"{label}.parts[{index}].duration_ms must be within "
                             f"[{constraints['min_duration_ms']}, {constraints['max_duration_ms']}]ms")
        durations.append(duration)
    if sum(durations) != constraints["total_duration_ms"]:
        raise ModelError(f"{label}.parts durations must sum to {constraints['total_duration_ms']}ms")
    return durations


def runtime_durations(
    facts: Facts, video: str, execution_round: str, *, project: str | None = None,
) -> list[int]:
    """Read the accepted allocation; never invent durations before the manifest closes."""
    project = project or required_text(facts.get("active_project"), "active_project")
    manifest_id = f"runtime_manifest/{project}/{video}/{execution_round}"
    manifest = facts.evidence_for(manifest_id)
    if manifest is None:
        raise ModelError(f"{manifest_id} must be satisfied before reading part durations")
    return validate_runtime_parts(manifest.data.get("parts"), runtime_constraints(
        facts, video, execution_round, project=project
    ), manifest_id)