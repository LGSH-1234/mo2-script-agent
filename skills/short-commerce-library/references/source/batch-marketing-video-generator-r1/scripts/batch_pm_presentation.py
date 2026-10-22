
"""Business presentation factory for effective batch-marketing snapshots.

The service binds semantic instructions before any view selection or rendering.
This factory cannot change topology, evidence, scheduling or acceptance.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Mapping

from batch_pm_graph import Projection, ProjectionContext, Requirement, runtime_constraints, runtime_durations


MAPPING_EXECUTION_ORDER = (
    "This mapping node must finalize ordered media arguments before compiling its "
    "new executable PromptPath file. Verify that every media reference in that file "
    "uses the matching one-based argument position. Never use video_blueprint as "
    "PromptPath. If the executable mapping is stale, erase this direct_payload or "
    "part_input fact, refresh next-action, and compile a new path; never edit an "
    "accepted artifact in place.",
)

FRAME_TARGET_INSTRUCTION = (
    "Use the FRAME TARGET selection: frames[N-1] is this frame's direct static "
    "picture requirement (its visual_description). Read the blueprint's shot N "
    "and global description for action context, shot purpose and continuity; the "
    "frozen preview instant does not mean the whole shot must be static. Resolve "
    "the selected image_ids through this frame's INPUT USE lines and the actual "
    "ordered ImageList; semantic IDs and paths are not attached media. Do not "
    "rewrite the blueprint."
)


def bind_presentation(projection: Projection) -> Projection:
    """Bind the full snapshot, including waiting nodes with absent producers."""
    project = projection.facts.get("active_project")
    language_evidence = (
        projection.facts.evidence_for(f"communication_language/{project}") if project else None
    )
    language = (
        str(language_evidence.data.get("language", "not established"))
        if language_evidence is not None else "not established"
    )
    language_field = ("COMMUNICATION LANGUAGE", language)
    projection_context = ProjectionContext(
        index_fields=(("PROJECT", str(project or "not established")), language_field),
        detail_fields=(("ACTIVE PROJECT", str(project or "none")), language_field),
    )
    nodes = {}
    for node_id, requirement in projection.graph.nodes.items():
        prefix = node_id.split("/", 1)[0]
        group = requirement.execution_group
        if prefix == "frame" and group is not None:
            context = group.metadata
            if context.get("route") == "route_a":
                start, end = context["batch_start"], context["batch_end"]
                instructions = (
                    f"Generate route_a group {context['group']} as a stable 3x3 sheet for "
                    f"preview frames {start}..{end}; describe all nine cells. Every cell must "
                    f"contain visible imagery; cells after frame {end} use film-style "
                    "diagnostic images.",
                )
            else:
                instructions = ("Use one independent image-generation call per listed frame.",)
            group = replace(group, what_lines=(FRAME_TARGET_INSTRUCTION, *instructions))
        nodes[node_id] = replace(
            requirement,
            what_lines=_instruction_lines(projection, requirement),
            execution_order_lines=(
                MAPPING_EXECUTION_ORDER if prefix in {"direct_payload", "part_input"}
                else requirement.execution_order_lines
            ),
            execution_group=group,
        )
    return replace(
        projection,
        graph=replace(projection.graph, nodes=nodes),
        ready=tuple(nodes[node.id] for node in projection.ready),
        context=projection_context,
    )


def _instruction_lines(projection: Projection, requirement: Requirement) -> tuple[str, ...]:
    """Resolve business semantics once, before handing the snapshot to VIEW."""
    prefix = requirement.id.split("/", 1)[0]
    lines: list[str] = []
    if requirement.what_lines:
        return requirement.what_lines
    if prefix == "start_new_project":
        slots = projection.facts.get("project_slots", {})
        if not slots:
            lines.append("No project has been established in this store. Follow references/project-lifecycle.md "
                         "to create this project, then refresh get-next-action.")
        else:
            lines.append("The previous project's lifecycle is settled. Create a distinct project only for "
                         "a new batch, or resume an existing paused project only when the user explicitly "
                         "asks to continue it. If a pending project close is listed as READY, complete it "
                         "first. Follow references/project-lifecycle.md, then refresh get-next-action.")
    elif prefix == "frame":
        if requirement.execution_group is None:
            lines.append(FRAME_TARGET_INSTRUCTION)
        rejected = projection.facts.get("rejected_frames", {})
        if isinstance(rejected, Mapping) and requirement.id in rejected:
            lines.append(
                "Safety review did not satisfy the frame. Ask the user to choose a "
                "meaning-preserving retry or erase storyboard_mode, refresh focus, and "
                "select script_only when ready; do not improvise a replacement."
            )
    elif prefix == "frame_spec_definition":
        _, project, video = requirement.id.split("/")
        blueprint = projection.facts.evidence_for(f"video_blueprint/{project}/{video}")
        if blueprint is None:
            return ("Read the effective video blueprint before declaring one frame per shot.",)
        shots = int(blueprint.data["shots"])
        lines.append(
            f"Read the current video blueprint and media definition. Provide exactly "
            f"one frame entry for every blueprint shot, in the same order: the blueprint "
            f"reports {shots} shot(s), so the frames array must have exactly {shots} "
            "entr(ies)."
        )
        lines.append(
            "Describe one representative static instant of each shot in "
            "visual_description, and reference only declared image IDs in image_ids. "
            "Report the frames array directly through the typed action; do not create a "
            "separate frame-spec file and do not add path, blueprint mapping or count "
            "fields."
        )
    elif prefix == "package_confirmation":
        lines.append(
            "Present the actual video blueprint and, in visual mode, the actual storyboard "
            "overview, together with all provided media and explicit auto/waived decisions, "
            "with present_sandbox_file before asking for confirmation or recording "
            "presentation evidence. Do not self-approve multimedia quality; objective checks "
            "and revision suggestions are allowed."
        )
    elif prefix == "delivery":
        lines.append(
            "Present the actual sandbox artifact with present_sandbox_file before asking "
            "for confirmation or recording presentation evidence. Do not self-approve "
            "multimedia quality; objective checks and revision suggestions are allowed."
        )
    elif prefix in {"image_model", "generation_model"}:
        lines.append(
            "Read the corresponding model setting only from the latest UI-injected "
            "<system-reminder>[User Setting]. If missing, ask the user in their communication "
            "language to select it in the dialog settings and let you know when done, or "
            "say they do not know. Do not ask them to name or transcribe the model. "
            "Wait for their reply, then re-read the injected setting; the reply is only a "
            "completion notification, not model-setting evidence. Report the exact injected "
            "value to PM with source='system-reminder'; only if the setting is still missing, "
            "record model='unknown' with source='conservative-fallback'. "
            "The token unknown is an internal PM value, not a required user reply."
        )
    elif prefix == "video_spec_definition":
        lines.append(
            "Read the blueprint and declare images/audios/videos by stable semantic ID. "
            "Keep role, description, allowed resolutions and process constraints with each "
            "material. Shot appearances stay in the blueprint, not in a second shot mapping."
        )
    elif prefix == "product_state_coverage":
        lines.append(
            "Audit every declared product against the accepted product images and this "
            "video's exact planned states before asking about visual versus script-only. "
            "For each product, record covered only when its required views/states are "
            "supported; otherwise complete the upload, confirmed reference-image, or "
            "explicit risk-acceptance branch from REQUIRED SPECS first."
        )
    elif prefix == "video_blueprint":
        lines.append(
            "Author the single model-independent creative source for this video from the "
            "accepted StoryMaster and Direction, before material definition and storyboard mode. "
            "Record this video's shots, duration_ms, ratio and market_target. "
            "Write document headings, table headers, shot labels and explanatory prose in "
            "COMMUNICATION LANGUAGE; write actual spoken lines in this video's market_target.language. "
            "Preserve machine evidence keys and stable material IDs unchanged. "
            "Use stable semantic material IDs; do not assign final Image[N]/Audio[N]/Video[N], "
            "do not depend on a storyboard overview, and never use this file as video PromptPath."
        )
    elif prefix == "storyboard_manifest":
        lines.append(
            "Read the current video blueprint and project its ordered shot semantics "
            "onto the accepted frame sources. The manifest may annotate and map those sources but "
            "must not become a second creative source."
        )
    elif prefix == "direct_payload":
        lines.append(
            "Compile the confirmed video blueprint one-to-one into a new self-contained "
            "model-specific executable prompt and payload. Finalize the actual ordered media "
            "arguments, translate semantic IDs to matching one-based positions, and bind the "
            "visual overview when listed. Never alias the video-blueprint path as PromptPath."
        )
    elif prefix in {"image", "audio", "video"}:
        lines.append(
            "Satisfy the declared media requirement using only an allowed resolution. "
            "Provide paths for real assets, or explicit user_evidence for auto/waived; "
            "waived also requires a reason. Present files before required user review. "
            "The declaration is not itself evidence or permission to skip the requirement."
        )
    elif prefix == "creative_research":
        lines.append(
            "Run the bundled creative assistant through async_task_create/resume/poll as "
            "specified by REQUIRED SPECS. Pass the child prompt as system_prompt_file; do not "
            "perform the child's research in the main context."
        )
        lines.append(
            "Keep calling async_task_poll on the same task until state.status is exactly "
            "succeeded or failed. created/running/killing, progress text and partial output "
            "are not completion. Only succeeded plus a validated handoff may be recorded "
            "with provide-research; failed follows REQUIRED SPECS' retry-or-waive path."
        )
        lines.append(
            "After a non-final poll, you may call sandbox_bash with sleep 30 once before "
            "polling the same task again. The wait only paces polling and does not end the "
            "research step."
        )
        if requirement.id in projection.history:
            lines.append(
                "The creative_research item in HISTORY is prior-round provenance for "
                "resume or replacement decisions; it does not satisfy this READY node."
            )

    elif prefix == "continuation_decision":
        lines.extend((
            "Keep this same READY requirement open while reviewing or revising delivered "
            "videos. Use the user's feedback, relevant baseline inputs and available tools "
            "to edit, regenerate or assemble a new output, present it through "
            "present_sandbox_file, and ask for feedback. No revision plan, new material "
            "facts, per-attempt report or new PM round is required.",
            "CURRENT INPUTS describe initial-generation baselines, not the latest revision. "
            "Preserve accepted paths; use new output paths and project memos for recovery. "
            "Do not erase the original generation chain merely to revise a delivered video.",
            "Record finish with actual user_evidence only when the user explicitly ends "
            "this project; liking one video is not automatically project completion. "
            "Record prepare/execute/extend only for explicitly requested other batch work, "
            "or pause for an explicit pause. A revision request is not a lifecycle choice. "
            "After recording finish or pause, call the matching project finish/pause "
            "command and refresh next-action.",
        ))
    elif prefix == "runtime_anchor":
        lines.append(
            "Provide one reusable concrete entity for the listed identity. Follow the original source "
            "auto authorization: perform objective checks without asking for redundant subjective "
            "approval. Resolve any additional cost "
            "or out-of-scope choice before calling tools. Report the actual path, never auto."
        )
    elif prefix in {"runtime_manifest", "part_spec"}:
        first = requirement.id.split("/")
        project, video, execution_round = first[1], first[2], first[3]
        if prefix == "runtime_manifest":
            producers = (f"video_blueprint/{project}/{video}",
                         f"generation_model/{project}/{video}/{execution_round}")
            if not all(projection.facts.evidence_for(node) for node in producers):
                return ("Complete the declared prerequisites before determining runtime constraints.",)
            limits = runtime_constraints(projection.facts, video, execution_round, project=project)
            lines.append(
                f"PM requires exactly {limits['part_count']} ordered parts, each within "
                f"[{limits['min_duration_ms']}, {limits['max_duration_ms']}]ms inclusive, "
                f"summing exactly to {limits['total_duration_ms']}ms. Choose integer-ms durations "
                "and natural cuts from the video blueprint's actions, speech and shot transitions; "
                "do not change the count or mechanically assume equal durations. Report the same "
                "parts and durations in the manifest file and evidence. If no suitable cut fits, "
                "report the constraint conflict rather than invent another execution route."
            )
            lines.append(
                "Map the complete video blueprint one-to-many into contiguous semantic parts. "
                "Preserve every creative instruction; in visual mode align boundaries with the "
                "accepted storyboard manifest. This manifest is a lowering map, not a rewritten plan."
            )
        else:
            producers = (f"video_blueprint/{project}/{video}",
                         f"generation_model/{project}/{video}/{execution_round}",
                         f"runtime_manifest/{project}/{video}/{execution_round}")
            if not all(projection.facts.evidence_for(node) for node in producers):
                return ("Complete the declared prerequisites before reading this part's accepted duration.",)
            durations = runtime_durations(projection.facts, video, execution_round, project=project)
            lines.append(
                f"Use this part's accepted runtime manifest duration: part {first[4]}="
                f"{durations[int(first[4]) - 1]}ms. Do not redistribute durations in part_spec."
            )
            lines.append(
                "Read the current runtime manifest and video blueprint, then select "
                "only the identities this part uses from video_spec_definition. "
                "Use blueprint prose for shot appearances. Report those IDs in materials, "
                "not file paths or Image[N]/Audio[N] "
                "positions. An auto voice still belongs in materials when used; its concrete "
                "runtime anchor supplies the concrete media; never select waived references."
            )
    elif prefix == "continuity_choice":
        lines.append(
            "Decide use_last_frame yourself from the accepted plan, adjacent part boundaries, "
            "and adjacent part specs; "
            "report a boolean and reason. Use true for a transition that needs the previous actual "
            "end state, false for an independent cut. This process choice does not change creative "
            "meaning and does not require a new user questionnaire. Do not wait for a generated "
            "result to answer this planning question."
        )
    elif prefix == "last_frame":
        lines.append(
            "Extract the actual final frame from the CURRENT INPUTS source video to a new image "
            "path. Check file existence and decodability, then provide that asset; do not redraw "
            "or substitute a planned storyboard frame."
        )
    elif prefix == "part_preflight":
        lines.append(
            "Verify only this part's current executable input and exact ordered media arguments. "
            "Include the selected previous end frame when listed, then report non-empty all-true "
            "objective checks. Do not wait for other parts' inputs or results."
        )
    elif prefix == "part_input":
        lines.append(
            "Compile this part's executable prompt from the current video blueprint, exact part "
            "spec, concrete material/anchor bindings and listed part sheet. Translate semantic IDs "
            "to this call's final one-based media positions. When continuity_choice is true, "
            "bind the listed last_frame and describe its actual handoff without changing creative "
            "meaning; when false, use the planned transition without a previous result reference."
        )
    else:
        target = requirement.id
        lines.append(f"Satisfy the typed {prefix} evidence contract for {target}.")
    return tuple(lines)