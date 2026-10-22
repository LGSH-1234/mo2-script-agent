
"""Read-only requirement selection over an already computed PM projection.

No declarations, scheduling, fact acceptance, or event writes belong here.
Without a requirement selection the view is an active requirement index.
Explicit requirement IDs select complete execution guidance for currently
READY work.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import hashlib
import os
from pathlib import Path
import shlex
import tempfile
import time
from typing import Callable, Mapping, Sequence

from batch_pm_graph import ModelError, Projection, Scheduler


BEGIN = "<<<BATCH_PM_NEXT_ACTION_V1>>>"
END = "<<<END_BATCH_PM_NEXT_ACTION_V1>>>"
DEFAULT_MAX_BYTES = 12_000
MIN_MAX_BYTES = 4_000
MAX_MAX_BYTES = 24_000
WORKSPACE_ROOT = Path("/workspace")
VIEW_CACHE_DIRECTORY = "batch_pm_views"
VIEW_CACHE_MAX_AGE_SECONDS = 24 * 60 * 60
VIEW_CACHE_MAX_FILES = 64


def size(text: str) -> int:
    return len(text.encode("utf-8"))


def command(requirement_ids: Sequence[str] = ()) -> str:
    args = ["python3", str(Path(__file__).with_name("batch_pm.py"))]
    args += ["project", "get-next-action"]
    for requirement_id in requirement_ids:
        args += ["--requirement-id", requirement_id]
    return shlex.join(args)


def checked_max_bytes(max_bytes: int) -> None:
    if type(max_bytes) is not int or not MIN_MAX_BYTES <= max_bytes <= MAX_MAX_BYTES:
        raise ModelError(f"view max-bytes must be {MIN_MAX_BYTES}..{MAX_MAX_BYTES}")


def finish(lines: list[str], max_bytes: int) -> str:
    result = "\n".join([BEGIN, *lines, END])
    if size(result) + 1 > max_bytes:
        raise ModelError("view metadata exceeds output budget; use shorter requirement IDs")
    return result


def default_view_root(
    *,
    workspace_root: Path = WORKSPACE_ROOT,
    system_temp: Path | None = None,
) -> Path:
    """Keep derived views outside replaceable Skill and source directories."""

    if workspace_root.is_dir():
        return workspace_root / ".tmp" / VIEW_CACHE_DIRECTORY
    return (system_temp or Path(tempfile.gettempdir())) / VIEW_CACHE_DIRECTORY


def _prune_view_cache(root: Path, current: Path) -> None:
    """Best-effort cleanup of derived views; never affect PM facts or commands."""

    try:
        now = time.time()
        candidates = [path for path in root.glob("*.txt") if path != current]
        for path in candidates:
            try:
                if now - path.stat().st_mtime > VIEW_CACHE_MAX_AGE_SECONDS:
                    path.unlink()
            except OSError:
                pass
        survivors = sorted(
            (path for path in root.glob("*.txt") if path != current),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        for path in survivors[VIEW_CACHE_MAX_FILES - 1:]:
            try:
                path.unlink()
            except OSError:
                pass
    except OSError:
        pass


def _write_complete_view(content: str, root: Path | None = None) -> tuple[Path, str, int]:
    payload = content.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    target_root = (root or default_view_root()).expanduser().resolve()
    target_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    target_root.chmod(0o700)
    target = target_root / f"{digest}.txt"

    target_is_valid = (
        target.is_file()
        and not target.is_symlink()
        and hashlib.sha256(target.read_bytes()).hexdigest() == digest
    )
    if not target_is_valid:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{digest}.",
            suffix=".tmp",
            dir=target_root,
        )
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                descriptor = -1
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
            target.chmod(0o600)
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
    target.chmod(0o600)
    _prune_view_cache(target_root, target)
    return target, digest, len(payload)


def materialized_view(content: str, content_view: str, max_bytes: int,
                      root: Path | None = None) -> str:
    path, digest, content_bytes = _write_complete_view(content, root)
    lines = [
        "VIEW: file",
        f"CONTENT VIEW: {content_view}",
        f"VIEW TOKEN: {digest[:24]}",
        f"CONTENT PATH: {path}",
        f"CONTENT BYTES: {content_bytes}",
        f"CONTENT SHA256: {digest}",
        "ACTION: Read CONTENT PATH completely with sandbox_read before acting. If a read is "
        "partial, continue from the next offset until EOF. The file contains one complete "
        "BATCH_PM_NEXT_ACTION_V1 envelope; a path, summary, or partial read is not enough.",
        "AUTHORITY: This locator is not execution guidance. Execute only from the complete "
        "file. If the file is unavailable, call project get-next-action again to regenerate it.",
    ]
    return finish(lines, max_bytes)


def read_materialized_view(locator: str) -> str:
    """Resolve a PM-owned locator for local adapters such as Graph Lab."""

    if "\nVIEW: file\n" not in f"\n{locator}\n":
        return locator
    fields: dict[str, str] = {}
    for line in locator.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            fields[key] = value
    required = {"CONTENT PATH", "CONTENT BYTES", "CONTENT SHA256"}
    if not required.issubset(fields):
        raise ModelError("materialized view locator is incomplete")
    try:
        expected_bytes = int(fields["CONTENT BYTES"])
    except ValueError as exc:
        raise ModelError("materialized view byte count is invalid") from exc
    try:
        payload = Path(fields["CONTENT PATH"]).read_bytes()
    except OSError as exc:
        raise ModelError("materialized view is unavailable; refresh get-next-action") from exc
    if len(payload) != expected_bytes:
        raise ModelError("materialized view byte count mismatch; refresh get-next-action")
    if hashlib.sha256(payload).hexdigest() != fields["CONTENT SHA256"]:
        raise ModelError("materialized view checksum mismatch; refresh get-next-action")
    try:
        content = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ModelError("materialized view is not valid UTF-8; refresh get-next-action") from exc
    if not content.startswith(BEGIN + "\n") or not content.endswith("\n" + END):
        raise ModelError("materialized view is not a complete next-action envelope")
    return content


class ProjectView:
    def __init__(self, projection: Projection):
        self.projection = projection
        self.ready = {node.id: node for node in projection.ready}
        self.scheduler = Scheduler(projection.graph, projection.facts)
        self.items = [node.id for node in projection.graph.nodes.values()
                      if node.focusable and node.contract is not None and not node.never_complete]
        self.item_set = set(self.items)

    def state(self, node: str) -> str:
        if node in self.ready:
            return "ready"
        return "satisfied" if self.scheduler.satisfied(node) else "waiting"

    def counts(self) -> str:
        counts = Counter(self.state(node) for node in self.items)
        return ", ".join(f"{key}={counts[key]}" for key in ("ready", "waiting", "satisfied"))

    def nodes_in_state(self, state: str):
        if state == "ready":
            return tuple(node for node in self.projection.ready if node.id in self.item_set)
        return tuple(self.projection.graph.nodes[node] for node in self.items
                     if self.state(node) == state)

    def select(self, requested: Sequence[str]) -> tuple:
        if isinstance(requested, (str, bytes)):
            raise ModelError("requirement_ids must be a sequence, not one string")
        requested = list(requested)
        if not all(isinstance(item, str) and item for item in requested):
            raise ModelError("requirement IDs must be non-empty strings")
        ordered = list(dict.fromkeys(requested))
        unavailable = [item for item in ordered if item not in self.ready]
        if unavailable:
            raise ModelError(
                "requirement is not currently READY: " + ", ".join(unavailable)
                + "; refresh get-next-action without --requirement-id and select only listed IDs"
            )

        # Business declarations own expansion. Only service-provided READY
        # peers participate; IDs, incoming consumers and metadata are opaque.
        selected_ids: list[str] = []
        for item in ordered:
            group = self.ready[item].execution_group
            peers = [node.id for node in self.projection.ready
                     if group is not None and group.expand_ready_peers
                     and node.execution_group is not None
                     and node.execution_group.id == group.id]
            for candidate in peers or [item]:
                if candidate not in selected_ids:
                    selected_ids.append(candidate)
        return tuple(self.ready[item] for item in selected_ids)


def _requirement_index(
    projection: Projection,
    *,
    max_bytes: int,
    view_root: Path | None,
) -> str:
    view = ProjectView(projection)
    header = [
        *(f"{label}: {value}" for label, value in projection.context.index_fields),
        "VIEW: requirement-index",
        f"PROJECT STATUS: {view.counts()}",
        f"ACTIVE REQUIREMENTS: {len(view.items)}",
        f"READY IN PROJECT: {len(projection.ready)}",
        "This is the current active requirement graph, not execution guidance. READY, WAITING and "
        "SATISFIED are listed for discovery; only query READY IDs with --requirement-id to obtain "
        "complete REQUIRED SPECS, CURRENT INPUTS, EXECUTION ORDER, WHY, WHAT and RECORD WITH "
        "instructions.",
        "For multiple requirements, repeat --requirement-id once for each selected READY ID.",
    ]
    if projection.ready:
        header.append(
            "EXAMPLE DETAIL QUERY: "
            + command([projection.ready[0].id])
        )
    if len(projection.ready) >= 2:
        header.append(
            "EXAMPLE MULTIPLE DETAIL QUERY: "
            + command(
                [projection.ready[0].id, projection.ready[1].id],
            )
        )
    sections = []
    for state in ("ready", "waiting", "satisfied"):
        nodes = view.nodes_in_state(state)
        heading = state.upper()
        sections.append(
            f"{heading}: none" if not nodes else "\n".join(
                [f"{heading}:", *(f"- {node.id} [{state}] — {node.subject}" for node in nodes)]
            )
        )
    content = "\n".join(sections)
    complete = "\n".join([BEGIN, *header, content, END])
    if size(complete) + 1 <= max_bytes:
        return complete
    return materialized_view(
        complete,
        "requirement-index",
        max_bytes,
        view_root,
    )


def render_project(projection: Projection, detail: Callable,
                   *, requirement_ids: Sequence[str] = (),
                   max_bytes: int = DEFAULT_MAX_BYTES,
                   view_root: Path | None = None) -> str:
    checked_max_bytes(max_bytes)
    if not requirement_ids:
        return _requirement_index(
            projection,
            max_bytes=max_bytes,
            view_root=view_root,
        )

    selected = ProjectView(projection).select(requirement_ids)
    selected_ids = [node.id for node in selected]
    payload = detail(replace(projection, ready=selected))
    body = payload.removeprefix(BEGIN + "\n").removesuffix("\n" + END)
    header = [
        "VIEW: detail",
        "REQUESTED REQUIREMENT IDS: " + ", ".join(dict.fromkeys(requirement_ids)),
        "DETAIL REQUIREMENT IDS: " + ", ".join(selected_ids),
        f"READY IN PROJECT: {len(projection.ready)}",
    ]
    # The detail renderer already owns PROJECT and COMMUNICATION LANGUAGE.
    complete = "\n".join([BEGIN, *header, body, END])
    if size(complete) + 1 <= max_bytes:
        return complete
    return materialized_view(
        complete,
        "detail",
        max_bytes,
        view_root,
    )