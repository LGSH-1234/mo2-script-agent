
> **Node knowledge:** External image knowledge supplements image-generation expertise only. It cannot change the PM's active graph, user authorization, media binding, or deterministic composition rules.

# External Knowledge

This reference owns acquisition of external image knowledge. Marketing craft, intake, research interpretation, story/direction design, and script writing use this skill's bundled node references and project inputs; do not load an external marketing workflow for them.

## Required Sources

- `image_generate`: image-domain knowledge required for every kind of authorized `sandbox_generate_image` call, including product states, characters, scenes, raw frames, replacements, and hard-required runtime images. Load it once when image generation first becomes applicable; before each later image call, verify that the applicable knowledge remains complete in the current visible context and reload only when it is absent, partial, or uncertain. Deterministic inspection or composition does not require it.

## Image Knowledge

Before the first applicable image-generation call, load:

```json
{"SkillName": "image_generate"}
```

Use its complete returned knowledge and applicable supporting references for prompt quality, conditioning, consistency, framing, and disclosed capabilities. Before each later image call, retain that complete applicable knowledge in the current visible context; reload only if it is absent, partial, or uncertain. It cannot choose a model, alter PM graph nodes, bypass user authorization, or replace the exact `ImageList` / `Prompt` binding contract.

## Presence And Recovery

Initialization happens once as an audit event, but knowledge may need to be loaded again. Before each dependent action, the complete applicable source content and supporting references must remain in the current visible context.

None of the following proves presence:

- a prior successful load;
- a PM lifecycle annotation;
- a timestamp or version label;
- a conversation prefix;
- a compression summary;
- a quoted fragment;
- a filename or search match.

If required image content is absent, partial, truncated, or uncertain, call `load_skill` again for `image_generate`. If an authoritative installed path is disclosed, a complete direct read of that actual source may restore missing text; an arbitrary similarly named file cannot. Read its supporting image references as needed, but do not recursively load other skills or follow dependencies that launch an external workflow.

Do not repeat a load while its complete required knowledge is already visible. Reloading does not restart the project, invalidate unchanged approvals, repeat paid work, or rerun research. If retrieval fails or completeness cannot be established, stop the dependent action, tell the user what knowledge is unavailable, and leave the ready requirement open.

## Authority And Audit

- `batch-marketing-video-generator` and PM own workflow order, gates, quantities, authorization, deliverables, exact routing, media binding, and composition.
- Bundled node references own marketing craft and artifact templates.
- `image_generate` owns image-prompt craft and disclosed image capabilities.
- External image knowledge does not establish the active image-model identifier; only the latest UI-injected `<system-reminder>[User Setting]` does. If it remains absent after the settings-selection retry, PM records the explicit conservative unknown fallback.

Do not append PM events for reads/reloads and do not maintain knowledge-loaded flags. Current-context completeness controls whether the node can be executed safely.