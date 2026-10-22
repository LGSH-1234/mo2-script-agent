
> **Shared node knowledge:** This file contains only invariants shared across media-processing nodes. The PM controls the structured workflow, readiness, and evidence.

# Common Knowledge

This file contains only rules that apply across workflow nodes. Loading and context-presence checks are owned by the bootloader; do not duplicate workflow routing or node-specific procedures here.

## DO

- Treat every generated image, video, and audio file path as immutable once the output is created. Every retry, regeneration, revision, replacement, or re-render must use a new filename and path. When changing an accepted workflow fact, erase its owning fact and refresh `project get-next-action`; report the replacement only when its owner is ready. First follow the current node's revision policy: work inside an open post-delivery review uses new files without withdrawing its initial-generation baseline. If the node is already ready, correct its work without a redundant erase. Preserve previous files and follow `revision-routing.md` for semantic ownership.
- Treat each `sandbox_generate_image` and `sandbox_generate_video` call as isolated. A sandbox media file is available to that tool only when the exact current call passes its path through the matching file-bearing argument. For `sandbox_generate_image`, reference images must be in `ImageList` and prompt content must be in `Prompt`. For `sandbox_generate_video`, reference images, videos, and audio must be in `ImageList`, `VideoList`, and `AudioList`; provide prompt text either directly in `Prompt` or through one `PromptPath` file, according to the focused contract. Reattach every required file on every independent call.
- `sandbox_generate_video` expands only the single text file passed directly through `PromptPath`. It does not recursively open another text file named, linked, or referenced inside that file. Whether using direct `Prompt` or `PromptPath`, the resulting model-facing prompt must therefore be complete and self-contained; nested file references and instructions to read another `.md` or text file are invalid.
- A path or filename mentioned in `Prompt`, conversation, Markdown, manifest, prior tool arguments, or inspection/read output does not attach that file. Before either generation call, compare every file-dependent instruction with the exact intended arguments; if a required file is absent from its matching parameter, stop and repair the payload before calling the tool.

<!-- Reserved for rules that apply in every workflow node. -->

## DO NOT

<!-- Reserved for prohibitions that apply in every workflow node. -->

## Stop Conditions

<!-- Reserved for stop conditions that apply in every workflow node. -->