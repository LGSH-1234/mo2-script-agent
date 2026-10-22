
> **Node knowledge:** This file defines artifact roles, naming, and presentation boundaries. The PM determines node readiness; this file cannot create or close requirements itself.

# Deliverable Contract

## User-visible Deliverables

Keep a project's regular user deliverables concise:

1. `information-understanding.md`: accepted product facts, assets, markets, audiences, platforms, languages, quantities, and creative boundaries;
2. `storyboard.md`: the StoryMaster table shared by the batch, not a specific video's final visual storyboard;
3. `video-blueprint-XX.md`: the complete, self-contained, model-independent video blueprint for video `XX`; it is reviewable but never used directly as video `PromptPath`;
4. `storyboard-grid-XX.png`: the complete storyboard overview, present only in visual mode and paired one-to-one with the video blueprint sharing its suffix;
5. The final video file: the direct or assembled result, presented to the user after objective checks.

A voice anchor is a reusable execution asset for a speaking identity, presented only for timbre confirmation rather than as an additional marketing deliverable. Direction sets, creative research handoffs, raw frames, raw 3×3 sheets, composition manifests, runtime manifests, part sheets, part inputs, and part results are internal materials. Do not present them individually as business deliverables unless the user explicitly requests diagnostics.

## Project-scoped Paths

Multiple serial projects may retain artifacts in the same sandbox; this PM permits only one active project at a time. All artifacts must live in a separate absolute directory chosen by the caller for that project; matching filenames do not permit reuse across projects. PM evidence stores exact absolute paths. Do not omit project identity from paths or infer it from the current working directory.

The following internal project roles are recommended. Directory names may depend on the runtime environment, but user-visible filenames and the meaning of the `XX` suffix remain stable:

```text
<project-artifact-root>/
  information-understanding.md
  storyboard.md
  video-blueprint-01.md
  storyboard-grid-01.png          # visual mode only
  assets/anchors/...              # product/character/scene/voice
  outputs/video-01-v01.mp4
  _internal/
    creative-research-*.md
    directions-*.md
    storyboard-01/...             # raw sheets/frames
    storyboard-manifest-01.json
    runtime/video-01/...          # executable direct/lowered mappings
```

Do not pre-create all files merely to fill out the directory. Create them only after the PM exposes the corresponding ready node. Use a new versioned path for every revision, retry, replacement, recomposition, or rerender; do not overwrite accepted files.

## Presentation Boundary

Before requesting review or confirmation, present the actual user deliverables through `present_sandbox_file`:

- Present `information-understanding.md` before information confirmation;
- Present `storyboard.md` before StoryMaster confirmation;
- Before package confirmation, present both `video-blueprint-XX.md` and `storyboard-grid-XX.png` in visual mode. In script-only mode, present the blueprint and declared actual media, explain auto/waived decisions, and explicitly state that no storyboard overview is included;
- Present the actual final video before recording delivery evidence;
- Present the actual sample before voice acceptance, explaining that it is for timbre/baseline delivery only.

File paths, Markdown links, pasted contents, probe results, and chat summaries cannot replace presentation. User confirmation is still required after successful presentation: technical generation success, passing objective checks, successful presentation, and the user's subjective acceptance are four separate facts.

When presenting a file, also provide its key points in a scannable chat summary so the user can understand the decision without relying solely on opening it. Internal raw/runtime files are not presented by default and cannot replace complete user deliverables.

## Package Confirmation Inputs

At package_confirmation, present the current blueprint and every provided media asset (paths lists), plus the overview in visual mode. Explain auto/waived items and their remaining creative freedom or accepted omission. Obtain actual user acceptance covering these current inputs and record presentation_tool plus user_evidence; no extra package document is required. Draft blueprint/definition reports are not final package approval. All current dependency versions bind the confirmation; revisions reopen it.