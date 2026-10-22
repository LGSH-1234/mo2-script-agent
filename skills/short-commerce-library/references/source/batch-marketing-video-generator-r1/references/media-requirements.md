
# Media Requirements

Each READY image/audio/video requirement is one declared creative need. For a runtime_anchor, use runtime-anchor-contract.md for its single path and process authorization instead of the source-node paths/auto/waived contract below. Read its definition entry and blueprint from CURRENT INPUTS. Its name and role identify its meaning; media type determines evidence and eligible tool-argument family.

Use only the node's permitted resolutions:

- provided: report a non-empty ordered `paths` list of actual files. Multiple files may represent views of the same entity. When review_required=true, first present the actual files with present_sandbox_file and obtain user acceptance; record presentation_tool and user_evidence.
- auto: record explicit user_evidence authorizing creative freedom and its limits. The need remains in the story but has no concrete reference file yet. Lowering requires a separate concrete runtime entity for every auto object before any part input.
- waived: only for a supplemental product image reference whose declaration names its product base in supplemental_to; record explicit user_evidence and reason accepting omission. This does not waive other requirements.

A permitted resolution is not an actual user decision. Do not infer subjective quality or user acceptance from generation success. Describe objective checks and propose revisions where useful.

For product, character, scene and other image semantics, apply asset-anchor-gates.md and reference-action-craft.md. For voice samples, apply voice-anchor-gates.md. Other audio may be actual narration, ambience or music: distinguish timbre-only use from sound intended to appear in the output. Video references must state adopted motion, composition or other dimensions.

If fulfillment involves generation, read the relevant current UI-injected model setting before the tool call. When missing, ask the user to select it in dialog settings and notify completion, then reread the injected setting; never ask them to transcribe a model name. Still missing means conservative unknown. This step does not require selecting storyboard_mode or satisfying the storyboard image_model node.

Consumers receive the declaration and current evidence. Dependency means the input must be resolved, not that every file must be attached to every call. Read the blueprint's shot/part semantics, select relevant references and map those files to the actual ordered ImageList/AudioList/VideoList. Use Image[N]/Audio[N]/Video[N] only in concrete executable prompts with matching one-based positions. Auto/waived evidence is semantic authority, never an attachment.

When several resolved image requirements reference the same selected path, keep their separate semantics but apply the [Image Attachment Identity Contract](payload-route-gates.md#image-attachment-identity-contract) when building generation arguments. A requirement is not an instruction to allocate another image slot.

To change an accepted asset or authorization, erase the media node and provide fresh evidence at new paths when READY. To change the inventory, erase video_spec_definition; to change the story, erase video_blueprint. Never mutate accepted artifacts in place.