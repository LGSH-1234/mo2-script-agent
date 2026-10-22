
> **Node knowledge:** This file defines only the semantics and format of the `information_understanding` node. PM next-action determines its readiness, dependencies, and evidence-recording procedure.

# information-understanding.md Template

Use this fixed structure for `information-understanding.md`. This is a user-visible business deliverable. Keep it concise and readable. Under `user-communication.md`, localize its human-readable headings and descriptions while preserving every required semantic field and confirmed fact.

```markdown
# Information Understanding

## 1. Product and Goals
| Item | Content |
|---|---|
| Product/Brand |  |
| SKU/Variant/Bundle |  |
| Target audience |  |
| Use cases |  |
| Video goals |  |
| Planned total (number of videos, never shots per video) | User specified and confirmed N videos / user did not specify; recommended and confirmed 6 |
| Video-content language |  |
| Placement market (country/region) |  |
| Placement platforms |  |
| Ratio/Duration |  |
| Audio and subtitles | May use narration, character dialogue, and character monologue; do not generate subtitles |
| Known speaking characters and voice direction | Record narration/character voice requirements the user already specified; for creative characters not yet designed, mark "to be confirmed after story design" and do not invent them during the facts stage |

## 2. Selling Points and Available Facts
| Information | Content | Source | Usage boundary |
|---|---|---|---|
| Core selling points |  |  |  |
| Proof points / effect demonstrations |  |  |  |
| Specs/Materials/Parameters |  |  |  |
| Price/Offer |  |  |  |

## 3. Hook and CTA
| Item | Content | Confirmed |
|---|---|---|
| Available hook directions |  | Yes / No |
| CTA tone |  | Yes / No |
| CTA specific channel/landing page |  | Confirmed / Unconfirmed, use generic CTA |

## 4. Fixed Content and Exploration Directions
| Type | Content | Confirmed | Notes |
|---|---|---|---|
| Fixed content | Product facts / core selling points / explicitly fixed market, audience, language or platform / CTA rules / visual baseline / duration & ratio | Yes / No |  |
| Market exploration | Allowed country/region, audience, content-language and platform combinations per branch; distinguish fixed fields from fields open to variation | Yes / No / N/A |  |
| Product/SKU exploration | Multiple products / multiple SKUs / colors / flavors / bundles / price tiers | Yes / No / N/A |  |
| Character exploration | Same character / different characters / hand model / creator / customer types | Yes / No / N/A |  |
| Scene exploration | Use cases / audience / location / time / emotion | Yes / No / N/A |  |
| Expression exploration | Hook / selling-point angle / proof method / CTA tone / style & pacing | Yes / No |  |
| Recommended test portfolio |  | Pending user confirmation / confirmed |  |

## 5. Material Check
| Material | Corresponding content | Purpose | Directly usable | Notes |
|---|---|---|---|---|
| A01 |  | Product / Character / Scene / Style / Unclear | Yes / No / Needs confirmation |  |

## 6. Entity and Visual References
| Check item | Source and conclusion | Notes |
|---|---|---|
| Product/packaging reference | User-provided, reuse directly / must generate / not needed | When the user already has a usable product image, generating a product baseline is forbidden; keep the actual material state and cite it directly |
| Product angles/states the storyboard is expected to need | Front / Back / Side / Top / Bottom / Open-Close / Disassembly / Contents / In-use / Other | Record per product/SKU; list only what the creatives are expected to use |
| Product-state material coverage | Covered / Partially missing / Not provided | List angles, states, and details already covered and still missing; after this round's directions are decided, finish the precise check and gap handling first, then ask whether to generate the storyboard overview image |
| Missing-state handling | Wait for user-shot uploads / generate a state reference after details are supplied / user accepts the skip risk / not needed | Generating a reference or skipping both require explicit user confirmation |
| Character reference | User-provided, reuse directly / accepted anchor exists / must generate / not needed | Every identifiable appearing character must have a character-image anchor; reuse the user's usable character image directly, otherwise generate and confirm one baseline before the corresponding video package is finalized or related images are generated; only anonymous background crowds may be marked not needed |
| Scene reference | User-provided, reuse directly / must generate / not needed | Generate one empty-scene baseline only when the agent creates a new scene that must stay consistent across shots |
| Prop reference | User-provided, reuse directly / must generate / not needed | Generate one baseline only when the agent creates a key prop that must stay consistent across shots |
| Style/Lighting/Palette reference |  | Record separately from entity references |
| Whether derived-state references are needed |  | E.g. opened product, ongoing liquid level, specific placement; must not overwrite user-original material or accepted agent-generated baselines |
| References that must actually be attached for per-shot generation | User-original material / generated anchor / style / accepted derived state |  |

## 7. Pending Confirmations
| Question | Why confirmation is needed | Handling if unconfirmed |
|---|---|---|
|  |  |  |
```

Rules:

- Do not include status/logs, workflow history, internal file decisions, tool details, or long reasoning.
- Write and confirm this factual boundary before launching the creative assistant. Do not use network inspiration or a creative-assistant handoff to author or revise product facts in this file; the handoff belongs only to later story-master and direction work.
- Record only facts useful for storyboard and script writing.
- Record the user's intended duration for each finished video under `Ratio/Duration`. This creative target is separate from the selected video model's per-call maximum and must not be silently shortened to fit one tool call.
- Mark unknown or conflicting product facts plainly. Do not turn them into claims.
- Explicitly separate fixed content from exploration directions. Batch generation should not move to storyboard until the exploration direction is confirmed.
- Exploration directions can be product/SKU, character, scene, audience, Hook, selling-point angle, proof method, CTA tone, rhythm, or style.
- If the input contains multiple products/SKUs/variants/bundles/colors/flavors/price tiers, treat product/SKU as a possible exploration direction and ask whether the user wants to compare them, combine them, or focus on one.
- If the user did not specify what to explore, use `dynamic_questionnaire` to recommend a compact mix and request confirmation through closed choices. Include `your recommended portfolio` as an acceptable business choice, but do not add a custom/other option or a generic text question. If the returned custom choice is still underspecified, collect its required details in a focused follow-up.
- Put asset checking here, but keep it to conclusions: usable materials, missing materials, role ambiguity, which user images will be reused directly, and whether any new agent-created identity genuinely requires a generated reference.
- Preserve every relevant user image as a separate material entry with its product/SKU, entity, scene, prop, or visual-style role. Do not keep only one representative image when the remaining images can add useful identity, angle, packaging, environment, or style information to later storyboard-frame calls.
- Record known or anticipated product views and states separately for each SKU. Examples include device front/back/ports/screens, bottle cap-on/cap-off/seal/liquid level, cosmetics closed/opened/dispensed, packaging sealed/torn/content-visible, apparel front/back/fastened/worn, footwear side/sole/laced, bags zipped/open/interior, appliances closed/open/attachment/display, furniture folded/unfolded/drawer-open, and vehicles with doors/trunk/charging-port open or closed. Do not request states the creative direction will not use.
- If current materials are likely insufficient, record the conclusion and the three permissible next choices: upload real views (recommended), describe and confirm hidden/state details before generating a product state reference, or explicitly skip with consistency risk. Do not invent the user's selection in this file.
- A usable user-provided product or entity image is the direct reference. Do not prescribe or generate a second clean, isolated, neutral, redrawn, or same-state confirmation baseline for it, even when its background or state is not ideal. A supplementary product state reference is permitted only for a confirmed-story view/state that the source does not show, after the user chooses generation and confirms its missing details and paid calls; it never replaces the source. Ask for a cleaner user source or disclose the limitation when necessary.
- Inventory every distinct identifiable character planned to appear in the batch and state whether its anchor is user-provided, already accepted, or must be generated before the applicable current-round package is finalized or any related image/video generation begins. A hand model, presenter, customer, creator, spokesperson, or other recognizable role requires an anchor; only anonymous background crowds may omit one.
- Generate a canonical entity reference when a required consistency-critical identity lacks a usable user-provided image. For every identifiable appearing character this is mandatory; for other entities it remains limited to genuinely necessary new identities. The first accepted generated reference is its baseline; do not generate a baseline of that baseline. Confirm the reason and paid image call first.
- Apply placement, interaction, opening, pouring, damage, occupancy, and other shot-specific states only in shot-level image or video generation. If an altered state must persist, record a separate derived-state/continuity reference without replacing the canonical anchor.
- When image calls are independent, identify the actual user-provided direct references, agent-generated anchors, and accepted derived references that must be reused across calls. Reusing user assets costs no extra generation call; generate only genuinely new consistency-critical identities and confirm their cost before image generation.
- Resolve planned total before storyboard work. If it is missing, use `dynamic_questionnaire` with `6 videos (recommended)` and a few useful closed quantities; do not add `another quantity` or a separate notes question, because the built-in custom option covers another quantity. Wait for explicit confirmation and do not silently assume the default. Planned total controls only the number of exploration directions; it must never be reused as the storyboard shot count.
- Record planned total in this file. Do not record preparation-round or video-generation-round quantity here; those are separate `preparation_scope` and `execution_scope` requirement evidence.
- Clearly total-scoped wording supplies planned total. `prepare N proposals first` supplies only preparation-round quantity; `generate N videos in this round first` supplies only video-generation-round quantity. If wording such as `do N first` or bare `generate N` is ambiguous for the intended scope, ask which scope it refers to. Never copy one quantity into another.
- CTA channel-specific routes must come from the user or be confirmed by the user. If not confirmed, use a generic CTA and do not invent platform/store/search/link/QR/private-message details.
- Preserve user-specified target languages and voice requirements. In this factual file, list only speaking identities already supplied or required by the user; do not invent creative characters before the story is designed. Mark unresolved creative speaking roles as `to be confirmed after story design`. After the story master and concrete per-video directions establish the actual cast, inventory narrator, on-screen dialogue roles, character monologues, and off-screen voices under this skill's later speaking-identity gate without reopening this factual file solely because the creative treatment introduced a role. Distinct speaking characters are distinct voices by default, including one-line roles, while an explicitly confirmed same-performer choice may share one voice. Keep visual character identity and speaking identity separate. Never put neutral TTS sample text, anchor paths, tool parameters, or generation status in this file. The default batch requirement is no generated subtitles, captions, dialogue bubbles, title cards, or added screen text; packaging text objectively present in confirmed reference material may remain.
- Record video-content language, placement market, and placement platform as separate facts. Communication language is resolved separately under `user-communication.md`, not in this creative-facts table; a request to change conversation language does not revise these facts. A language never proves a country/region, audience, cultural context, or platform. For a multi-market request, map each market to its intended audience, platform, language, and any confirmed market-specific constraints instead of writing one blended global label. If market is genuinely unspecified, say so explicitly; do not infer it from language, currency, product appearance, or user location.
- Complete information collection first; use `dynamic_questionnaire` for every pause that needs user answers and follow `dynamic-questionnaire-guide.md`: closed confirmation/routing forms do not carry generic text questions, while concrete missing facts use focused required fields. Never add a custom/other option. Do not repeatedly write and present partial versions as each answer arrives. Once the material information and planned total are sufficiently resolved, create and check the consolidated file, present the actual `information-understanding.md` through `present_sandbox_file`, then show the key content in conversation. Launch its closed confirmation questionnaire only after presentation succeeds. If the user selects revision, collect concrete changes in a focused follow-up; after revising, re-present the actual file before confirming again.