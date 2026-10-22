
# Marketing Creative Guidance

This file explains how to do the current creative node well. It does not determine workflow order, readiness, or evidence. PM next-action governs structured progression.

## Fixed Core and Exploration Axes

Batch videos require more than swapping nouns in one script. Separate the content into two layers first:

- Fixed core: accepted product facts, brand boundaries, required selling points, evidence limits, allowed market/audience/language/platform scope and any explicitly fixed target, ratio/duration, CTA constraints, and prohibited content;
- Exploration axes: dimensions genuinely open to variation, such as hooks, pain points or desires, character relationships, usage scenarios, proof presentation, visual style, pacing, CTA tone, and SKUs/bundles.

Each specific Direction should state its marketing objective, main exploration axis, material differences from other Directions, and required product states, characters, scenes, voices, or style assets. Changing only wording, colors, or character names while retaining the same hook, conflict, proof, and narrative progression does not create an independent direction.

When market targeting varies across the batch, each Direction must identify its own country/region, intended audience, video-content language and placement platform within the accepted campaign scope. Preserve any explicitly fixed dimensions. The corresponding video blueprint must explicitly materialize that choice as `market_target`; never treat the campaign-wide union or conversation language as every video's target.

## Short-form Marketing Structure

Choose the structure based on the product, platform, and target duration rather than mechanically imposing a fixed shot count. A complete short marketing video typically covers the following functions. Adjacent functions may be combined, but must not be dropped simply because of a template or model-call limit:

1. **Hook**: establish a problem, desire, contrast, previewed outcome, or character conflict within the first few seconds so viewers immediately understand why to keep watching.
2. **Context / Tension**: place the product in a concrete audience and situation, showing why the problem is real; avoid empty slogans.
3. **Product reveal**: introduce the product and correct SKU naturally without inventing packaging, prices, features, or results.
4. **Proof / Demonstration**: substantiate the selling point through visible actions, before/after comparisons, steps, details, usage results, or other accepted evidence. Demonstrable selling points should not rely solely on voiceover claims.
5. **Payoff**: fulfill the opening promise and show the practical value for the target audience.
6. **CTA**: use confirmed channels. If the channel is uncertain, use only a generic CTA without inventing shopping carts, links, search terms, offers, or account details.

Every shot should serve a clear function and describe the image, action, shot size, camera intent, product state, audio/dialogue, and transition to the next beat. Remove or combine shots that serve no marketing or narrative function.

## Hook and Proof Quality

For story and direction authoring, apply [marketing-proof-playbook.md](marketing-proof-playbook.md) to the relevant buying concern, proof sequence, category examples, and information budget. For timing and executable performance, use [performance-timing-craft.md](performance-timing-craft.md) when authoring StoryMaster or scripts. Creative research uses the child's own reading instructions in its async task; the parent must not perform that research itself.

- Hooks must relate to accepted selling points and the target audience, without exploiting unrelated trends, exaggerated disasters, or false outcomes for attention.
- Proof must stay within user-provided materials or accepted facts. Search results may inspire expression and structure but cannot become facts about the current product.
- Product appearance and usage states must be visible and continuous. When a key selling point appears, the visual action, voiceover, and product state should reinforce one another.
- Batch directions should cover distinct testable hypotheses, such as pain-point hooks versus outcome hooks or expert proof versus UGC experience, rather than six structurally identical stories.

## Direction and Story Output

StoryMaster defines only the complete story structure, timing, and exploration units shared by the batch; do not turn it into a merged draft of multiple videos. Direction makes the exploration units concrete, after which video_blueprint specializes the complete story. video_spec_definition extracts its media requirements grouped by images, audios and videos. Shot appearances remain semantic content in the blueprint; definition has no shot mapping.

StoryMaster has no default shot count. Determine its actual row count from final duration, marketing functions, action complexity, dialogue density, and pacing. Planned video total, 3×3 grid capacity, and the video model's per-call duration must not determine the story's shot count.

## Prompt Craft

Image and video generation prompts must be self-contained and use visible, actionable descriptions: subject identity, environment, composition, shot size, action phase, camera, lighting, materials, colors, product state, and exclusions. Do not write only "premium feel," "keep consistent," or "see attachment"; specify which identity or structural features to preserve from each `Image[N]`.

Image prompts describe visual content only; do not ask the model to draw shot numbers, timecodes, annotations, subtitles, dialogue bubbles, or information panels. Video prompts must also specify the timeline, action changes, camera movement, audio, speaking roles, and line-by-line delivery. Pass all media attachments through the current call's `ImageList` / `AudioList` / `VideoList`; path text is not an attachment.

## Revision

Revision suggestions should identify the affected marketing function and artifact scope: hook, proof, shot content, character identity, product state, voice, CTA, or a purely technical issue. For semantic changes, revise the upstream StoryMaster/Direction/video_blueprint first. Purely technical rerenders use new paths and preserve original artifacts. The model may propose specific improvements but cannot confirm subjective quality on the user's behalf.