
#!/usr/bin/env python3
"""Persistent command boundary and concise rendering for the graph PM.

The core module owns graph semantics. This module owns process concerns:

* append-only, locked JSONL event persistence;
* a finite action vocabulary instead of generic requirement closure;
* receipt-only mutation output;
* project-scoped recovery memos that never satisfy graph requirements;
* mandatory guide-first instructions with requirement-attributed inputs/what/why and stable delimiters.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import fcntl
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Callable, Mapping, Sequence

from batch_pm_graph import (
    ACTIONS as BUSINESS_ACTIONS,
    ActionSpec,
    Event,
    InputUse,
    MAX_PROJECT_MEMO_LENGTH,
    ModelError,
    Projection,
    RequirementService,
    Scheduler,
    UnchangedFact,
)
from batch_pm_view import DEFAULT_MAX_BYTES, render_project


EVENT_SCHEMA = "batch-pm-event/v3"
RECEIPT_BEGIN = "<<<BATCH_PM_RECEIPT_V1>>>"
RECEIPT_END = "<<<END_BATCH_PM_RECEIPT_V1>>>"
NEXT_BEGIN = "<<<BATCH_PM_NEXT_ACTION_V1>>>"
NEXT_END = "<<<END_BATCH_PM_NEXT_ACTION_V1>>>"
STATUS_BEGIN = "<<<BATCH_PM_STATUS_V1>>>"
STATUS_END = "<<<END_BATCH_PM_STATUS_V1>>>"
MEMOS_BEGIN = "<<<BATCH_PM_MEMOS_V1>>>"
MEMOS_END = "<<<END_BATCH_PM_MEMOS_V1>>>"
PROJECT_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")
MAX_MEMO_LENGTH = MAX_PROJECT_MEMO_LENGTH
NEXT_MEMO_LIMIT = 5
DEFAULT_MEMO_LIST_LIMIT = 20
MAX_MEMO_LIST_LIMIT = 100
WORKSPACE_ROOT = Path("/workspace")
SKILL_ROOT = Path(__file__).resolve().parents[1]
STATE_DIRECTORY = "_batch_pm"
RELEASE_IDENTITY_FILE = "release_identity.json"
RELEASE_LINE_RE = re.compile(r"r[1-9][0-9]*\Z")
STATE_NAMESPACE_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")


@dataclass(frozen=True)
class ReleaseIdentity:
    skill_name: str
    release_line: str
    channel: str
    state_namespace: str


def load_release_identity() -> ReleaseIdentity:
    """Load the immutable package identity before any state access."""
    path = SKILL_ROOT / RELEASE_IDENTITY_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ModelError(f"missing release identity: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ModelError(f"invalid release identity: {path}") from exc
    if not isinstance(raw, Mapping) or raw.get("schema_version") != 1:
        raise ModelError("release identity must be an object with schema_version 1")
    fields = {key: raw.get(key) for key in (
        "skill_name", "release_line", "channel", "state_namespace"
    )}
    if any(not isinstance(value, str) or not value for value in fields.values()):
        raise ModelError("release identity fields must be non-empty strings")
    if not RELEASE_LINE_RE.fullmatch(fields["release_line"]):
        raise ModelError("release identity release_line must match rN")
    if fields["channel"] not in {"production", "test", "development"}:
        raise ModelError("release identity channel is unsupported")
    if not STATE_NAMESPACE_RE.fullmatch(fields["state_namespace"]):
        raise ModelError("release identity state_namespace is unsafe")
    return ReleaseIdentity(**fields)


def default_state_root() -> Path:
    """State outlives skill installation and never depends on the caller's cwd."""
    identity = load_release_identity()
    if WORKSPACE_ROOT.is_dir():
        base = WORKSPACE_ROOT / STATE_DIRECTORY
    else:
        base = Path.home() / ".local" / "state" / "batch-marketing-video-generator"
    root = (base / identity.state_namespace).resolve()
    resolved_base = base.resolve()
    if resolved_base not in root.parents:
        raise ModelError("release identity state namespace escapes the state base")
    return root


def validate_state_location(path: Path | str) -> Path:
    resolved = Path(path).expanduser().resolve()
    for forbidden in (SKILL_ROOT.resolve(), (WORKSPACE_ROOT / ".skills").resolve()):
        if resolved == forbidden or forbidden in resolved.parents:
            raise ModelError(
                f"PM state cannot be stored inside a replaceable Skill directory: {resolved}. "
                "Use the environment default or an internal debug location outside Skills."
            )
    return resolved


def select_state_root(explicit: Path | None) -> Path:
    # A debug override changes only the final root. It must never hide a broken
    # or missing package identity.
    load_release_identity()
    root = validate_state_location(explicit if explicit is not None else default_state_root())
    if explicit is not None:
        return root
    return root


@dataclass(frozen=True)
class StoredEvent:
    sequence: int
    event: Event
    unchanged: bool = False


@dataclass(frozen=True)
class ProjectedInput:
    requirement_id: str
    uses: tuple[InputUse, ...] = ()


class JsonlEventStore:
    """Append and replay immutable events under one cross-process lock."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.lock_path = self.path.with_name(f"{self.path.name}.lock")

    def load(self) -> list[Event]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_SH)
            try:
                return [stored.event for stored in self._read_unlocked()]
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    def transact(self, producer: Callable[[list[Event]], Event | UnchangedFact]) -> StoredEvent:
        """Project, validate, and append while holding the same exclusive lock."""

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                stored = self._read_unlocked()
                event = producer([item.event for item in stored])
                if isinstance(event, UnchangedFact):
                    return StoredEvent(event.sequence, event.event, unchanged=True)
                # Validate before append: replay the candidate event inside the
                # same critical section so a rejected candidate never reaches
                # the stream. Business rules live in the reducer/graph layer,
                # not in this persistence class.
                from batch_pm_graph import EventReducer as _Reducer
                _Reducer().reduce([*[item.event for item in stored], event])
                sequence = len(stored) + 1
                record = {
                    "schema": EVENT_SCHEMA,
                    "sequence": sequence,
                    "kind": event.kind,
                    "subject": event.subject,
                    "data": dict(event.data),
                }
                with self.path.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
                    stream.write("\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                return StoredEvent(sequence=sequence, event=event)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    def _read_unlocked(self) -> list[StoredEvent]:
        if not self.path.exists():
            return []
        result: list[StoredEvent] = []
        with self.path.open("r", encoding="utf-8") as stream:
            for line_number, raw_line in enumerate(stream, start=1):
                line = raw_line.strip()
                if not line:
                    raise ModelError(f"empty event-store line {line_number}")
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ModelError(f"invalid event-store JSON on line {line_number}") from exc
                if not isinstance(record, Mapping):
                    raise ModelError(f"event-store line {line_number} must be an object")
                if record.get("schema") != EVENT_SCHEMA:
                    raise ModelError(
                        f"unsupported event schema on line {line_number}; expected {EVENT_SCHEMA}. "
                        "Preserve this history and create a new project or state root; "
                        "do not edit or migrate the JSONL."
                    )
                expected = len(result) + 1
                if record.get("sequence") != expected:
                    raise ModelError(
                        f"event-store sequence mismatch on line {line_number}: expected {expected}"
                    )
                kind = record.get("kind")
                subject = record.get("subject")
                data = record.get("data", {})
                if not isinstance(kind, str) or not kind:
                    raise ModelError(f"event-store kind is invalid on line {line_number}")
                if not isinstance(subject, str) or not subject:
                    raise ModelError(f"event-store subject is invalid on line {line_number}")
                if not isinstance(data, Mapping):
                    raise ModelError(f"event-store data is invalid on line {line_number}")
                result.append(
                    StoredEvent(
                        sequence=expected,
                        event=Event(kind=kind, subject=subject, data=dict(data)),
                    )
                )
        return result


class ReadOnlyEventStore(JsonlEventStore):
    """Views do not create project directories, event streams or lock files."""

    def load(self) -> list[Event]:
        try:
            lock = self.lock_path.open("r", encoding="utf-8")
        except FileNotFoundError:
            # Imported snapshots can lack the sibling lock. Never repair them.
            return [stored.event for stored in self._read_unlocked()]
        with lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_SH)
            try:
                return [stored.event for stored in self._read_unlocked()]
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    def transact(self, producer):
        raise ModelError("read-only view store cannot append events")


def event_path(state_root: Path | str) -> Path:
    """Return the single event stream shared by the serial project graph."""

    return validate_state_location(Path(state_root) / "events.jsonl")


# Compatibility export for apply callers, parser choices, and debugger fixtures.
# Descriptors have one business-owned source; lifecycle commands cannot enter apply.
ACTIONS: dict[str, ActionSpec] = {
    name: action for name, action in BUSINESS_ACTIONS.items()
    if action.operation == "apply"
}


class CommandFacade:
    """The only persisted mutation boundary exposed to the CLI."""

    def __init__(self, store: JsonlEventStore):
        self.store = store

    def projection(self) -> Projection:
        return RequirementService(self.store.load()).projection()

    def create_project(self, project: str, *, resume: bool = False) -> StoredEvent:
        if not isinstance(project, str) or not PROJECT_ID_RE.fullmatch(project):
            raise ModelError("project ID must match [A-Za-z0-9][A-Za-z0-9_.-]{0,127}")
        def produce(events: list[Event]) -> Event:
            service = RequirementService(events)
            projection = service.projection()
            active = projection.facts.get("active_project")
            if active is not None:
                raise ModelError(
                    f"cannot {'resume' if resume else 'create'} a project while "
                    f"{active} is still active; complete its pending lifecycle "
                    "close first (see project get-next-action), then retry"
                )
            ready = projection.ready
            if len(ready) != 1 or not ready[0].id.startswith("start_new_project/"):
                raise ModelError("project bootstrap is not ready; run project get-next-action, not create/resume")
            states = projection.facts.get("project_states", {})
            established = isinstance(states, Mapping) and project in states
            if resume and not established:
                raise ModelError(f"cannot resume unknown project: {project}")
            if not resume and established:
                raise ModelError(f"project already exists: {project}")
            return Event(
                kind="project_resumed" if resume else "project_created",
                subject=ready[0].id,
                data={
                    "project": project,
                    "based_on": Scheduler(
                        projection.graph, projection.facts
                    ).basis(ready[0].id),
                },
            )

        return self.store.transact(produce)

    def close_project(self, *, pause: bool = False) -> StoredEvent:
        def produce(events: list[Event]) -> Event:
            projection = RequirementService(events).projection()
            project = projection.facts.get("active_project")
            if project is None:
                raise ModelError("no project is active")
            expected = "pause" if pause else "finish"
            choice = projection.facts.get("continuation_choice")
            if choice != expected:
                raise ModelError(
                    f"project {expected} has not been selected by continuation evidence"
                )
            scheduler = Scheduler(projection.graph, projection.facts)
            continuation_round = str(
                projection.facts.get("project_states", {})
                .get(project, {})
                .get("continuation_round", "01")
            )
            close_node = f"project_close/{project}/{continuation_round}"
            if close_node not in {item.id for item in projection.ready}:
                raise ModelError(
                    f"{close_node} is not ready; refresh project get-next-action "
                    "and follow the listed lifecycle step"
                )
            # The close node is READY: its prerequisites (the accepted
            # continuation decision) hold. The appended event is validated by
            # the store's replay-after-append transaction below.
            return Event(
                kind="project_paused" if pause else "project_finished",
                subject=f"project_goal/{project}",
            )

        return self.store.transact(produce)

    def apply(self, action: str, subject: str, evidence: Mapping[str, Any]) -> StoredEvent:
        spec = ACTIONS.get(action)
        if spec is None:
            raise ModelError(f"unknown typed action: {action}")
        if not spec.accepts(subject):
            raise ModelError(f"action {action} cannot resolve {subject}")

        def produce(events: list[Event]) -> Event | UnchangedFact:
            service = RequirementService(events)
            return service.resolve(subject, spec.resolution, evidence)

        return self.store.transact(produce)

    def erase(self, subject: str, reason: str) -> StoredEvent:
        return self.store.transact(
            lambda events: RequirementService(events).erase(subject, reason)
        )

    def reject_frame(self, subject: str, reason: Mapping[str, Any]) -> StoredEvent:
        return self.store.transact(
            lambda events: RequirementService(events).reject_frame(subject, reason)
        )

    def retry_frame(self, subject: str) -> StoredEvent:
        return self.store.transact(
            lambda events: RequirementService(events).authorize_frame_retry(subject)
        )

    def record_memo(self, message: str) -> StoredEvent:
        def produce(events: list[Event]) -> Event:
            projection = RequirementService(events).projection()
            project = projection.facts.get("active_project")
            if project is None:
                raise ModelError("cannot record a memo without an active project")
            if not isinstance(message, str) or not message.strip():
                raise ModelError("memo message must be non-empty")
            normalized = message.strip()
            if "\n" in normalized or "\r" in normalized:
                raise ModelError("memo message must be single-line text")
            if len(normalized) > MAX_MEMO_LENGTH:
                raise ModelError(
                    f"memo message exceeds {MAX_MEMO_LENGTH} characters"
                )
            return Event(
                kind="memo_recorded",
                subject=f"project/{project}",
                data={"message": normalized},
            )

        return self.store.transact(produce)


def render_receipt(stored: StoredEvent) -> str:
    payload = {
        "accepted": True,
        "sequence": stored.sequence,
        "event": stored.event.kind,
        "subject": stored.event.subject,
    }
    if stored.unchanged:
        payload["event"] = "unchanged"
        payload["unchanged"] = True
        payload["appended"] = False
    project = stored.event.data.get("project")
    if isinstance(project, str):
        payload["project"] = project
    return "\n".join(
        (RECEIPT_BEGIN, json.dumps(payload, ensure_ascii=False, sort_keys=True), RECEIPT_END)
    )


def render_rejection(message: str) -> str:
    payload = {"accepted": False, "reason": message}
    return "\n".join(
        (RECEIPT_BEGIN, json.dumps(payload, ensure_ascii=False, sort_keys=True), RECEIPT_END)
    )


def _project_inputs_for(projection: Projection, requirement) -> list[ProjectedInput]:
    ordered_ids: list[str] = []
    uses_by_id: dict[str, list[InputUse]] = {}

    def add(requirement_id: str, uses: Sequence[InputUse] = ()) -> None:
        if requirement_id not in uses_by_id:
            ordered_ids.append(requirement_id)
            uses_by_id[requirement_id] = []
        for use in uses:
            if use not in uses_by_id[requirement_id]:
                uses_by_id[requirement_id].append(use)

    for binding in requirement.supplemental_inputs:
        add(binding.requirement_id, binding.uses)
    for active_edge in projection.graph.edges:
        if active_edge.consumer == requirement.id:
            add(active_edge.prerequisite, active_edge.input_uses)
    return [
        ProjectedInput(requirement_id=item, uses=tuple(uses_by_id[item]))
        for item in ordered_ids
    ]


def _consumers_for(projection: Projection, requirement_id: str) -> list[str]:
    return sorted({
        edge.consumer
        for edge in projection.graph.edges
        if edge.prerequisite == requirement_id
    })




def render_next(projection: Projection, **view_options) -> str:
    return render_project(projection, _render_next_details, **view_options)


def _render_next_details(projection: Projection) -> str:
    lines = [NEXT_BEGIN]
    lines.extend(f"{label}: {value}" for label, value in projection.context.detail_fields)
    lines.append(
        "FACT UPDATES: from one complete detail view, submit all already determined facts for its "
        "listed READY nodes, then refresh next-action without --requirement-id once after the batch. "
        "Stop early on rejection "
        "or uncertainty. To change an accepted fact, use "
        "erase --subject <semantic-owner> --reason '<change>', then call project get-next-action. "
        "Use new artifact paths; do not overwrite accepted files or replay old downstream facts. "
        "An identical retry of a currently effective fact returns unchanged without a new event; "
        "continue the batch and do not erase merely to repeat a report."
    )
    if projection.memos:
        lines.append("PROJECT MEMOS:")
        lines.append(
            "- Recovery notes only; verify them against the current graph, facts, and files."
        )
        lines.extend(
            f"- {_envelope_json(message)}"
            for message in projection.memos[-NEXT_MEMO_LIMIT:]
        )
    if not projection.ready:
        lines.extend(("READY: none", "No ready requirement is selected for this view."))
        lines.append(NEXT_END)
        return "\n".join(lines)

    grouped: dict[tuple[str, str | None], list[Any]] = {}
    for requirement in projection.ready:
        group = requirement.execution_group
        key = (requirement.display_group or requirement.id, group.id if group else None)
        grouped.setdefault(key, []).append(requirement)

    emitted_knowledge: dict[tuple[str, ...], str] = {}
    emitted_refs: dict[str, tuple[str, int]] = {}
    emitted_inputs: dict[tuple[str, int], str] = {}
    # Labels identify one evidence/use across the complete detail envelope,
    # even when separate business groups repeat it in their own contexts.
    use_labels: dict[tuple, str] = {}
    evidence_labels: dict[tuple, str] = {}
    command_schema_owners: dict[str, str] = {}
    for requirements in grouped.values():
        group = requirements[0].execution_group
        lines.append("")
        lines.append("READY:")
        for requirement in requirements:
            lines.append(f"- {requirement.id} [ready] — {requirement.subject}")

        knowledge_refs: list[str] = []
        for requirement in requirements:
            configured = requirement.guidance.get("knowledge_refs", ())
            if isinstance(configured, Sequence) and not isinstance(configured, str):
                knowledge_refs.extend(str(item) for item in configured)
        knowledge_refs = list(dict.fromkeys(knowledge_refs))
        lines.append("REQUIRED SPECS (MUST BE UNDERSTOOD FIRST):")
        if knowledge_refs:
            fingerprint = tuple(knowledge_refs)
            first_owner = emitted_knowledge.get(fingerprint)
            if first_owner is None:
                shared: dict[str, list[int]] = {}
                for item in knowledge_refs:
                    if item in emitted_refs:
                        owner, position = emitted_refs[item]
                        shared.setdefault(owner, []).append(position)
                for owner, positions in shared.items():
                    lines.append("- Reuse reference entries "
                                 + ", ".join(map(str, positions))
                                 + f" from {owner}'s REQUIRED SPECS (count path entries only).")
                position = 0
                for item in knowledge_refs:
                    if item not in emitted_refs:
                        lines.append(f"- {item}")
                        position += 1
                        emitted_refs[item] = (requirements[0].id, position)
                emitted_knowledge[fingerprint] = requirements[0].id
            else:
                lines.append(
                    f"- Same semantic references as {first_owner}; do not reload them when "
                    "their complete content is still present in the current context."
                )
        else:
            lines.append("- No node-specific semantic reference; follow the PM action package.")

        inputs_by_requirement = {
            requirement.id: _project_inputs_for(projection, requirement)
            for requirement in requirements
        }

        # View-only folding at the single-InputUse level. Evidence content and
        # each use are deduplicated separately:
        #   EvidenceKey = (requirement_id, effective_fact_version)
        #   UseKey = (EvidenceKey, mode, fields, target, purpose, required, resolutions)
        # Graph, ready, based_on, and input order are untouched. A differing
        # mode/field/target/purpose/strength/resolution never merges.
        def evidence_key(item: ProjectedInput) -> tuple:
            return (item.requirement_id,
                    projection.facts.evidence_version(item.requirement_id))

        def use_key(item: ProjectedInput, use: InputUse) -> tuple:
            ek = evidence_key(item)
            return (ek, use.mode, use.fields, use.target,
                    use.purpose, use.required, frozenset(use.resolutions))

        def applicable_uses(item: ProjectedInput) -> list[InputUse]:
            evidence = projection.facts.evidence_for(item.requirement_id)
            resolution = evidence.resolution if evidence is not None else ""
            return [use for use in item.uses
                    if (evidence is None and not use.resolutions)
                    or (evidence is not None and use.applies_to(resolution))]

        consumers = [requirement.id for requirement in requirements]
        # consumer -> [(ProjectedInput, InputUse)]; inputs with no declared
        # applicable use still surface their fact content once (evidence-only).
        NO_USE = ("__evidence_only__",)

        def pairs_for(items: list[ProjectedInput]) -> list[tuple[ProjectedInput, object]]:
            pairs: list[tuple[ProjectedInput, object]] = []
            for item in items:
                uses = applicable_uses(item)
                if uses:
                    pairs.extend((item, use) for use in uses)
                else:
                    pairs.append((item, NO_USE))
            return pairs

        pairs_by_consumer = {
            requirement.id: pairs_for(inputs_by_requirement[requirement.id])
            for requirement in requirements
        }

        def pair_key(item: ProjectedInput, use: object) -> tuple:
            if use is NO_USE:
                return (evidence_key(item), NO_USE)
            return use_key(item, use)  # type: ignore[arg-type]

        keys_by_consumer = {
            consumer: [pair_key(item, use) for item, use in pairs]
            for consumer, pairs in pairs_by_consumer.items()
        }
        shared_keys = set.intersection(*[
            set(keys) for keys in keys_by_consumer.values()
        ]) if len(requirements) > 1 else set()

        # First-appearance ordering for evidence payloads and use labels.
        ordered_items: list[ProjectedInput] = []
        for requirement in requirements:
            for item in inputs_by_requirement[requirement.id]:
                if item not in ordered_items:
                    ordered_items.append(item)

        def label_for_evidence(item: ProjectedInput) -> str | None:
            key = evidence_key(item)
            return evidence_labels.get(key)

        def register_evidence(item: ProjectedInput) -> str:
            key = evidence_key(item)
            label = evidence_labels.get(key)
            if label is None:
                label = f"E{len(evidence_labels) + 1:02d}"
                evidence_labels[key] = label
            return label

        def evidence_header(item: ProjectedInput, label: str) -> str:
            evidence = projection.facts.evidence_for(item.requirement_id)
            resolution = evidence.resolution if evidence is not None else "no current evidence payload"
            return (
                f"{label}: {item.requirement_id} [{resolution}] "
                f"(fact version {projection.facts.evidence_version(item.requirement_id)})"
            )

        def register_use(item: ProjectedInput, use: InputUse) -> str:
            key = use_key(item, use)
            label = use_labels.get(key)
            if label is None:
                label = f"U{len(use_labels) + 1:02d}"
                use_labels[key] = label
            return label

        lines.append("EXECUTION ORDER:")
        lines.append(
            "- Before starting this work, ensure the applicable requirements from every path "
            "under REQUIRED SPECS (MUST BE UNDERSTOOD FIRST) are present and understood in the "
            "current context. These specs define delivery standards; they do not require a "
            "redundant file-read action when their relevant content is already in context."
        )
        lines.append(
            "- Skip opening a listed spec only when its actual relevant content is already "
            "available in the current context and is sufficient to apply without guessing. A "
            "path, summary, remembered gist, or claim that it was read earlier is not enough. "
            "If the content is absent, partial, uncertain, or lost after compaction, read the "
            "listed file in full before continuing."
        )
        lines.append(
            "- Only after the specs are known, apply the uses listed for each REQUIREMENT "
            "CONTEXT, including those shared through COMMON CURRENT INPUTS. Obey every "
            "consumer-specific INPUT USE; a use reference such as U01 identifies a use "
            "printed inside this same output only. When no INPUT USE is declared, decide "
            "from the specs whether the input must be read into context, presented, or "
            "passed through a tool argument as production material. Do not use one "
            "requirement's inputs for another unless an explicit use, the COMMON section, "
            "or a reuse line applies to that requirement. Do not infer handling from a "
            "filename, extension, or sandbox path."
        )

        def render_use_lines(item: ProjectedInput, use: InputUse, label: str,
                             applies_to: str) -> list[str]:
            evidence = projection.facts.evidence_for(item.requirement_id)
            missing = [field for field in use.fields
                       if evidence is not None and field not in evidence.data]
            if missing:
                raise ModelError(
                    f"{applies_to} input binding for {item.requirement_id} "
                    f"requires missing evidence fields: {missing}"
                )
            source = (
                ", ".join(f"data.{field}" for field in use.fields)
                if use.fields
                else "the complete evidence payload"
            )
            target = f" into {use.target}" if use.target else ""
            strength = "REQUIRED" if use.required else "OPTIONAL"
            result = [
                f"  {label}: {strength} {use.mode} from {source}{target} — {use.purpose}"
            ]
            if use.required and use.mode == "read_content":
                result.append(
                    "  ACTION: If the referenced content is absent, partial, uncertain, or lost "
                    f"after context compaction, read the actual file before performing or "
                    f"recording {applies_to}. A path, summary, remembered gist, or prior read "
                    "claim is not enough."
                )
            return result

        # Folding stays group-local so each group's uses retain their source
        # evidence context. Only label identity is shared across the envelope.
        printed_evidence: set[tuple] = set()
        printed_uses: set[tuple] = set()

        if shared_keys:
            lines.append("")
            lines.append(
                "COMMON CURRENT INPUTS [applies to "
                + ", ".join(consumers) + "]"
            )
            lines.append(
                "- Identical evidence and identical single uses shared by every requirement "
                "in this execution group; each context below applies them through its USE "
                "reference line."
            )
            for item in ordered_items:
                for use in applicable_uses(item) or [NO_USE]:
                    key = pair_key(item, use)
                    if key not in shared_keys or key in printed_uses:
                        continue
                    e_label = register_evidence(item)
                    if evidence_key(item) not in printed_evidence:
                        printed_evidence.add(evidence_key(item))
                        evidence = projection.facts.evidence_for(item.requirement_id)
                        lines.append(evidence_header(item, e_label))
                        if evidence is not None:
                            lines.append("     " + _envelope_json(dict(evidence.data)))
                    if use is not NO_USE:
                        u_label = register_use(item, use)
                        lines.extend(
                            render_use_lines(item, use, u_label,
                                             "any requirement in this group")
                        )
                    else:
                        lines.append(
                            f"     (no declared use; consult this node's REQUIRED SPECS "
                            "for how to apply this fact)"
                        )
                    printed_uses.add(key)

        for requirement in requirements:
            lines.append("")
            lines.append(f"REQUIREMENT CONTEXT: {requirement.id}")
            if requirement.execution_order_lines:
                lines.append("EXECUTION ORDER:")
                lines.extend(f"- {line}" for line in requirement.execution_order_lines)
            pairs = pairs_by_consumer[requirement.id]
            own_keys = {pair_key(item, use): (item, use) for item, use in pairs}
            use_refs: list[str] = []
            specific_lines: list[str] = []
            for key, (item, use) in own_keys.items():
                if key in shared_keys:
                    if use is not NO_USE:
                        use_refs.append(use_labels[key])
                    continue
                e_label = register_evidence(item)
                if use is not NO_USE:
                    u_label = register_use(item, use)
                    use_refs.append(u_label)
                if evidence_key(item) not in printed_evidence:
                    printed_evidence.add(evidence_key(item))
                    evidence = projection.facts.evidence_for(item.requirement_id)
                    specific_lines.append("- " + evidence_header(item, e_label))
                    if evidence is not None:
                        specific_lines.append(
                            "  " + _envelope_json(dict(evidence.data))
                        )
                if use is not NO_USE:
                    specific_lines.extend(
                        render_use_lines(item, use, u_label, requirement.id)
                    )
                else:
                    specific_lines.append(
                        "  (no declared use; consult this node's REQUIRED SPECS "
                        "for how to apply this fact)"
                    )
            lines.append("REQUIREMENT-SPECIFIC INPUTS (USE AFTER SPECS):")
            if specific_lines:
                lines.extend(specific_lines)
            elif use_refs:
                lines.append("- none beyond the shared uses referenced below")
            else:
                lines.append("- Use the current conversation and this requirement's subject.")
            if use_refs:
                lines.append("USE: " + ", ".join(use_refs))
            for selection in requirement.input_selections:
                e_label = evidence_labels.get(
                    (selection.producer_id, selection.producer_version)
                )
                source = e_label or selection.producer_id
                for component in selection.path:
                    source += f"[{component}]" if isinstance(component, int) else f".{component}"
                qualifiers = ", ".join(
                    f"{label}={value}" for label, value in selection.qualifiers.items()
                )
                lines.append(f"{selection.label}: {source}" + (f", {qualifiers}" if qualifiers else ""))
                for label, value in selection.display_data.items():
                    rendered = (
                        ", ".join(str(item) for item in value) or "(none)"
                        if isinstance(value, (list, tuple)) else _envelope_json(value)
                    )
                    lines.append(f"  {label}: {rendered}")

            if requirement.id in projection.history:
                old_evidence = projection.history[requirement.id]
                lines.append("HISTORY (not current evidence):")
                lines.append(
                    "- Recovery hint only. Check whether this old file/task ID still applies to "
                    "this requirement's current inputs; obtain required confirmation and report only "
                    "this READY requirement."
                )
                lines.append(
                    f"- {requirement.id} [{old_evidence.resolution}] "
                    f"{_envelope_json(dict(old_evidence.data))}"
                )

            requirement_consumers = _consumers_for(projection, requirement.id)
            lines.append("WHY:")
            lines.append(
                "- Required by " + ", ".join(requirement_consumers)
                if requirement_consumers
                else "- This is the current ordered requirement."
            )
            if requirement_consumers:
                lines.append(
                    "- Downstream context only: these consumers do not authorize executing "
                    "their work or reading their references. Follow this READY requirement "
                    "and the group's REQUIRED SPECS."
                )

            if requirement.what_lines:
                lines.append("WHAT:")
                lines.extend(f"- {line}" for line in requirement.what_lines)

        if group is not None and group.what_lines:
            lines.append("WHAT:")
            lines.append(
                "- Execution group covers: "
                + ", ".join(requirement.id for requirement in requirements)
                + "."
            )
            lines.extend(f"- {line}" for line in group.what_lines)

        actions = list(dict.fromkeys(
            action for requirement in requirements for action in requirement.actions
        ))
        lines.append("RECORD WITH:")
        if len(requirements) > 1:
            lines.append("- Record one fact for each READY requirement in this group.")
        if any(requirement.actions != requirements[0].actions for requirement in requirements[1:]):
            for requirement in requirements:
                lines.append(f"- {requirement.id}: " + ", ".join(action.command for action in requirement.actions))
        elif actions:
            lines.extend(f"- {action.command}" for action in actions)
        else:
            lines.append("- No recording action is declared for this requirement.")
        lines.extend(f"- {note}" for note in dict.fromkeys(
            note for action in actions for note in action.notes
        ))
        for schema_ref in dict.fromkeys(action.schema_ref for action in actions if action.schema_ref):
            command_schema_owner = command_schema_owners.get(schema_ref)
            if command_schema_owner is None:
                lines.append(
                    f"- Command schema: read {schema_ref} before recording. "
                    "Reread it if its complete contents are missing from the current context."
                )
                command_schema_owners[schema_ref] = requirements[0].id
            else:
                lines.append(f"- Command schema: reuse the reference in {command_schema_owner}'s "
                             "RECORD WITH; reread it if its complete contents are missing.")

    lines.append(NEXT_END)
    return "\n".join(lines)


def render_status(projection: Projection) -> str:
    satisfied = 0
    graph_scheduler = Scheduler(projection.graph, projection.facts)
    for requirement_id in projection.graph.nodes:
        if graph_scheduler.satisfied(requirement_id):
            satisfied += 1
    payload = {
        "active_project": projection.facts.get("active_project"),
        "active_nodes": len(projection.graph.nodes),
        "satisfied_nodes": satisfied,
        "ready": [item.id for item in projection.ready],
        "pending_rules": len(projection.graph.pending_rules),
        "memo_count": len(projection.memos),
    }
    return "\n".join(
        (STATUS_BEGIN, json.dumps(payload, ensure_ascii=False, sort_keys=True), STATUS_END)
    )


def _render_project_input(projection: Projection, requirement_id: str) -> str:
    evidence = projection.facts.evidence_for(requirement_id)
    if evidence is None:
        return f"- {requirement_id} [no current evidence payload]"
    return (
        f"- {requirement_id} [{evidence.resolution}] "
        f"{_envelope_json(dict(evidence.data))} "
        f"(fact version {projection.facts.evidence_version(requirement_id)})"
    )


def _render_input_uses(
    projection: Projection,
    consumer_id: str,
    project_input: ProjectedInput,
) -> list[str]:
    evidence = projection.facts.evidence_for(project_input.requirement_id)
    resolution = evidence.resolution if evidence is not None else ""
    lines: list[str] = []
    for use in project_input.uses:
        if evidence is None and use.resolutions:
            continue
        if evidence is not None and not use.applies_to(resolution):
            continue
        if evidence is not None:
            missing = [field for field in use.fields if field not in evidence.data]
            if missing:
                raise ModelError(
                    f"{consumer_id} input binding for {project_input.requirement_id} "
                    f"requires missing evidence fields: {missing}"
                )
        source = (
            ", ".join(f"data.{field}" for field in use.fields)
            if use.fields
            else "the complete evidence payload"
        )
        target = f" into {use.target}" if use.target else ""
        strength = "REQUIRED" if use.required else "OPTIONAL"
        lines.append(
            f"  INPUT USE: {strength} {use.mode} from {source}{target} — {use.purpose}"
        )
        if use.required and use.mode == "read_content":
            lines.append(
                "  ACTION: If the referenced content is absent, partial, uncertain, or lost "
                "after context compaction, read the actual file before performing or recording "
                f"{consumer_id}. A path, summary, remembered gist, or prior read claim is not enough."
            )
    return lines


def render_memos(
    projection: Projection,
    limit: int = DEFAULT_MEMO_LIST_LIMIT,
) -> str:
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ModelError("memo limit must be an integer")
    if limit < 1 or limit > MAX_MEMO_LIST_LIMIT:
        raise ModelError(f"memo limit must be between 1 and {MAX_MEMO_LIST_LIMIT}")
    payload = {
        "project": projection.facts.get("active_project"),
        "count": len(projection.memos),
        "memos": projection.memos[-limit:],
        "authority": "recovery-notes-only",
    }
    return "\n".join(
        (MEMOS_BEGIN, _envelope_json(payload), MEMOS_END)
    )


def _envelope_json(value: Any) -> str:
    """Keep user-authored text from imitating a stable envelope marker."""

    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def _json_mapping(raw: str, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ModelError(f"{label} must be valid JSON") from exc
    if not isinstance(value, Mapping):
        raise ModelError(f"{label} must be a JSON object")
    return value


def add_view_options(parser, *, selectable=True):
    if selectable:
        parser.add_argument(
            "--requirement-id",
            action="append",
            default=[],
            help=("currently READY requirement to expand; repeat for multiple requirements; "
                  "omit for the active requirement index"),
        )
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--state-root",
        type=Path,
        default=None,
        help=argparse.SUPPRESS,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_view_options(subparsers.add_parser("next"))
    add_view_options(subparsers.add_parser("get-next-action"))
    subparsers.add_parser("status")

    project = subparsers.add_parser("project")
    project.add_argument(
        "operation",
        choices=("create", "resume", "finish", "pause", "get-next-action", "status"),
    )
    project.add_argument("--project-id")
    add_view_options(project)

    apply = subparsers.add_parser("apply")
    apply.add_argument("action", choices=tuple(ACTIONS))
    apply.add_argument("--subject", required=True)
    apply.add_argument("--data-json", default="{}")

    erase = subparsers.add_parser("erase")
    erase.add_argument("--subject", required=True)
    erase.add_argument("--reason", required=True)

    frame = subparsers.add_parser("frame")
    frame.add_argument("operation", choices=("reject", "retry"))
    frame.add_argument("--subject", required=True)
    frame.add_argument("--reason-json", default="{}")

    memo = subparsers.add_parser("memo")
    memo.add_argument("operation", choices=("record", "list"))
    memo.add_argument("--message")
    memo.add_argument("--limit", type=int, default=DEFAULT_MEMO_LIST_LIMIT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.state_root = select_state_root(args.state_root)
        is_view = args.command in {"next", "get-next-action"} or (
            args.command == "project" and args.operation == "get-next-action")
        if is_view:
            path = event_path(args.state_root)
            projection = CommandFacade(ReadOnlyEventStore(path)).projection()
            print(render_next(
                projection,
                requirement_ids=args.requirement_id,
                max_bytes=args.max_bytes,
            ))
            return 0
        if args.command == "project" and (
            args.requirement_id or args.max_bytes != DEFAULT_MAX_BYTES
        ):
            raise ModelError("view options are only valid for get-next-action")
        facade = CommandFacade(JsonlEventStore(event_path(args.state_root)))
        if args.command == "status":
            print(render_status(facade.projection()))
            return 0
        if args.command == "project":
            if args.operation == "status":
                print(render_status(facade.projection()))
                return 0
            if args.operation in {"finish", "pause"}:
                if args.project_id is not None:
                    raise ModelError("finish/pause infer the active project; omit --project-id")
                stored = facade.close_project(pause=args.operation == "pause")
            else:
                if args.project_id is None:
                    raise ModelError(f"project {args.operation} requires --project-id")
                stored = facade.create_project(
                    args.project_id, resume=args.operation == "resume"
                )
            print(render_receipt(stored))
            return 0
        if args.command == "apply":
            stored = facade.apply(
                args.action,
                args.subject,
                _json_mapping(args.data_json, "--data-json"),
            )
            print(render_receipt(stored))
            return 0
        if args.command == "erase":
            stored = facade.erase(args.subject, args.reason)
            print(render_receipt(stored))
            return 0
        if args.command == "frame":
            if args.operation == "retry":
                stored = facade.retry_frame(args.subject)
            else:
                stored = facade.reject_frame(
                    args.subject,
                    _json_mapping(args.reason_json, "--reason-json"),
                )
            print(render_receipt(stored))
            return 0
        if args.command == "memo":
            if args.operation == "list":
                print(render_memos(facade.projection(), args.limit))
                return 0
            if args.message is None:
                raise ModelError("memo record requires --message")
            stored = facade.record_memo(args.message)
            print(render_receipt(stored))
            return 0
        raise AssertionError(args.command)
    except (ModelError, OSError) as exc:
        print(render_rejection(str(exc)))
        return 2


if __name__ == "__main__":
    sys.exit(main())