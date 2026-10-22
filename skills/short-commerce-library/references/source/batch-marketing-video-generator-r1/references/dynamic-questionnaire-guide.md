
> **Node knowledge:** This file defines form semantics for user choices, confirmations, and missing-information collection. Use it only when PM next-action lists the corresponding decision, question, or confirmation as ready.

# Dynamic Questionnaire Guide

Use `dynamic_questionnaire` whenever the workflow pauses for a user decision, confirmation, correction, or material missing answer. Use plain conversation only when the tool is unavailable. Apply `user-communication.md` before creating or presenting a form. All quoted decision gates, titles, and examples below specify decision meanings, not a fixed display language.

## Form Contract

- Keep `title` concise and no more than 20 words.
- Use stable unique IDs for questions and options and stable `value` meanings for the same decision/scope. Localize `title`, `label`, `placeholder`, help text, and supported `skip_button_text`, never `id`, `value`, or schema keys. Treat the returned canonical decision/value, subject IDs, and presented artifact versions as the semantic evidence required by the matching PM command. A translated label alone is not confirmation evidence.
- Let required user input determine the question count. A confirmation, authorization, or routing decision is normally one closed `radio` or `checkbox` question; never pad it with a text question.
- Use `radio` for one decision and `checkbox` when multiple selections are valid.
- Put the recommended choice first and label it clearly, for example `6 videos (recommended)`, `Prepare 1 proposal first (recommended)`, or `Generate 1 video first (recommended)`.
- Do not add options named `Custom`, `Other`, `Other option`, `Other quantity`, `Enter your own`, or equivalents. The form supplies its own custom option.
- Use `text` only when a concrete text answer is required for the current semantic decision. The current tool contract has no question-level optional flag, so wording such as `optional` or `may be left blank` does not make a text question optional. If the workflow can proceed without the answer, omit the text question.
- Never append a generic `custom_input`, `additional notes`, `anything else to add or adjust`, or equivalent text question to every form. The built-in custom-option capability already covers an unlisted closed choice.
- The questionnaire has no conditional show/hide contract. When a closed answer such as `Needs revision`, `Adjust first`, or `Specific videos only` requires details, submit the routing form first and launch a focused follow-up form containing the required `text`, `media`, or other fields. Do not ask those branch-only fields unconditionally in the routing form.
- A payload-collection form must not contain a radio option that abandons or switches that payload's branch. Such an option would still require completing the fields being abandoned. When supported, use the form-level `skip_button_text: "Choose a different handling"` as a separate escape. An explicit skip or conversation branch-change request abandons the old branch without completing its gate. If the user names a valid destination, such as `Switch to uploading real shots`, record that branch and go directly to its required collection form; do not ask the same routing question again. Only an unspecified or ambiguous destination needs the closed router. Never require dummy text or fake attachments to escape. Without a working form-level escape, explain that the user can request a different route in conversation.
- A required follow-up is complete only when its returned payload contains the requested non-empty, usable answer. An empty submission does not resolve the pending decision; ask again with only the still-missing field.
- Combine related decisions in one form when practical. Do not create a long sequence of one-question interruptions.
- When the form contains only one `radio` question, provide exactly one emoji for every option as required by the runtime schema. Never add a dummy text question merely to avoid this requirement.
- For file confirmation, call `present_sandbox_file` first, summarize the content in conversation, and only then launch this form.

Before every call, preflight the final `questions` array: every question must be either an independent closed decision needed now or a concrete required payload field needed now. Remove generic, optional, duplicated, and unselected-branch questions. For a one-question `radio` form, verify every option has one emoji. Verify that display text uses the communication language, IDs/values retain their intended decision meanings, and localization has not broadened authorization or added required questions.

## Standard Confirmation Shape

Choose stable question/option IDs for the decision and scope; do not change them merely because the communication language changes. Adapt display wording to the language and actual business decision. Do not copy a generic option when a business-specific choice would be clearer.

```json
{
  "title": "Confirm information understanding",
  "questions": [
    {
      "id": "information_decision",
      "title": "Can this information understanding proceed?",
      "type": "radio",
      "options": [
        {
          "id": "confirm_information",
          "label": "Confirm and continue",
          "value": "confirm",
          "emoji": "✅",
          "selected": false
        },
        {
          "id": "revise_information",
          "label": "Needs revision",
          "value": "revise",
          "emoji": "✏️",
          "selected": false
        }
      ]
    }
  ]
}
```

If the returned choice is `revise`, launch a focused follow-up instead of advancing:

```json
{
  "title": "Provide revision details",
  "questions": [
    {
      "id": "information_revision",
      "title": "Describe what needs to be revised or added",
      "type": "text",
      "placeholder": "Describe the facts, selling points, quantity, language, or material notes to revise"
    }
  ]
}
```

## Stage Choices

- Planned total: use closed quantity choices headed by `6 videos (recommended)`. Do not offer `other quantity` or add a separate notes question; the built-in custom option covers another quantity. This is the number of batch directions only and must never seed the per-video storyboard shot count.
- Exploration direction: use the recommended combination and a few input-relevant directions as closed choices. `Follow your recommended portfolio` is a real business choice and is allowed. If the user chooses to describe a different direction through the built-in custom option, collect any still-missing specifics in a focused follow-up.
- Information understanding: use only `Confirm and continue` / `Needs revision`. After `Needs revision`, ask for the concrete corrections in a required follow-up text form and reconfirm the revised file.
- Creative research blocker, only after accepted information when `async_task_create`, `async_task_poll`, `async_task_resume`, the System Prompt file, search tool, or expected handoff is unavailable/blocked: use `Retry creative search (recommended)` / `Continue with existing creative knowledge`. Do not present the internal handoff or ask the user to approve the child's reasoning. Record the second choice as an explicit research skip for that accepted-information version.
- Story master (`storyboard.md`): after successful presentation and the shared-batch/next-step explanation, use only `Confirm story master` / `Needs revision`. After `Needs revision`, collect concrete shot/timing/speaking-role/narration/dialogue/monologue corrections in a focused follow-up. Use a localized name that clearly means the shared story structure, not an individual frame or visual overview.
- Concrete per-video directions: after mother-story confirmation, show every planned ID and its actual proposed direction, then use only `Confirm these video directions` / `Adjust some directions`. The latter opens a focused required correction form. Tie approval to the current direction-set content and report it through the ready `confirm-directions` typed action; story confirmation and a preparation quantity are not direction approval.
- Preparation round: use `Prepare 1 proposal first (recommended)`, useful larger choices, and `Prepare all remaining proposals` when applicable. This selects how many scripts/optional grids to prepare, not how many videos to generate. Do not offer `other quantity` or append a notes question.
- Product state coverage, when PM exposes `product_state_coverage/<project>/<video>` after VideoSpec and its concrete product assets: complete the router and its selected follow-up branch for every affected SKU, then report the final per-product result through `confirm-product-state-coverage`. Do not ask the visual-storyboard question before this typed node closes. Product consistency is required for script-only and visual-mode videos alike.
- Visual-storyboard coverage, only after product consistency is resolved and storyboard-frame cost is disclosed: for multiple videos use `Storyboard overview for the first video only (recommended)` / `Storyboard overview for all videos this round` / `Storyboard overview for specific videos only` / `Skip storyboard overviews this round; generate scripts only`. After `Storyboard overview for specific videos only`, collect the exact video IDs in a required follow-up text form. For one video use only `Generate storyboard overview` / `Skip storyboard overview; generate script only`, with the recommendation chosen from actual visual complexity and cost sensitivity. Record the answer per video and do not carry it into later rounds without explicit instruction.
- Complete actual packages: after presenting the blueprint and actual media (plus overview for visual mode), and explaining every auto/waived decision, use only `Confirm package content; proceed to generation planning` / `Revise first`. After `Revise first`, collect required revision details in a focused follow-up. This confirms package content only and never authorizes video calls or supplies a generation quantity.
- Video-generation round: after package confirmation and immediately before any capability check, target lowering, or video call, use `Generate 1 video first (recommended)`, useful larger quantities bounded by confirmed ready ungenerated packages, `Generate specific videos`, and `Generate all confirmed videos` when applicable. After `Generate specific videos`, collect exact ready video IDs in a required follow-up. Ask by default even when every grid and script already exists. Skip only for an explicit execution-scoped quantity; package confirmation, preparation quantity, prior execution quantity, or generic `continue` is insufficient.
- Next round: while confirmed ready packages remain, ask the next video-generation-round quantity with `Generate 1 video first (recommended)`, useful larger choices, `Generate specific videos`, `Generate all confirmed videos`, `Revise proposals first`, and `Pause`. Route `Generate specific videos` and `Revise proposals first` to focused follow-ups. When no ready package remains but planned directions remain unprepared, ask the next preparation-round quantity with `Prepare 1 proposal first (recommended)`, useful larger choices, `Prepare all remaining proposals`, `Revise directions first`, and `Finish`; route `Revise directions first` to a focused follow-up.
- Asset or anchor decision: user-provided usable product/entity images default to direct reuse and do not need a generated-baseline decision. Use `media`, `character`, `multi_character`, `radio`, or `checkbox` only to resolve a genuine gap or confirm a paid anchor for a new agent-created identity. Collect usage constraints or corrections only when that branch is selected and the information is required.
- Character-anchor market fit: before a paid generated character anchor, visibly summarize the target market, audience, placement platform when known, role, and recommended non-stereotyped casting/styling direction. Use only a grouped closed decision such as `Generate with the recommended character direction (recommended)` / `Adjust the character setup first`; after the adjustment choice, collect role-specific corrections in a required follow-up. A country name without the actual casting/styling recommendation is not enough, and generic confirmation does not fill a missing market. Never propose changing a user-provided person's identity as localization.
- Speaking-role anchors: when narration, dialogue, or monologue is planned and one or more roles lack accepted timbre anchors, list every speaking identity separately. Immediately before the form, visibly show a compact `character -> full recommended timbre` mapping for every affected role; never write `recommended timbres follow` unless those recommendations are actually present. Each recommendation must include voice texture plus role/campaign-relevant tone, energy, and rhythm. For several roles, use only a grouped closed confirmation such as `Generate voice samples for all characters with the recommended voices (recommended)` / `Adjust some character voices first`; after the adjustment choice, collect role-specific corrections in a required follow-up and never collapse all characters into one narrator voice. A generic submit or `I have confirmed the above` is not confirmation when any role-specific recommendation was omitted. After presenting each role-labeled neutral sample, use only `Confirm these characters' timbres and delivery` / `Adjust some characters`; after adjustment, ask which role and what to change. Explain that sample words are unrelated and never enter the video, sample performance fits its role, and actual narration/dialogue/monologue plus line-level delivery come from the script.
- Product state coverage router: when required product views or states are missing, use only `Upload more product shots (recommended)` / `Add details and generate a state reference image` / `Skip and accept the consistency risk`. This form only selects a branch. It does not collect the required branch payload and must not be treated as upload completion, factual detail, risk acceptance, or generation authorization. Block the later visual-storyboard form until this branch is fully complete.

If the runtime returns a built-in custom choice or the user's same-turn message contains a material correction, honor that content and route to the appropriate follow-up instead of treating a simultaneous generic confirmation as authorization.

## Product State Branch Forms

The questionnaire schema has no conditional show/hide rules. Therefore, after the product-state router is answered, the next user-facing action must be the selected branch's collection or risk confirmation, normally by launching the focused follow-up form immediately. If the same returned response already contains the complete matching payload, such as actual attached media for the upload branch, validate that payload and move only to that branch's follow-up decision (re-audit or factual-summary confirmation); do not ask for the same input twice. Do not move to skill loading, file preparation, paid image generation, storyboard generation, or any later workflow decision first.

### Upload branch

Use a payload-only form containing:

- a `media` question requesting the actual missing product images. Use `assets: []` when the runtime renders an empty media field as an upload/selection box; otherwise include available relevant media and explicitly ask the user to attach new images in conversation;
- a `text` question only when the SKU, angle, or state cannot be determined from the attached media and confirmed information.

Do not add submit/switch/skip radio questions. Normal form submission supplies the files; the form-level escape or an explicit conversation request reroutes under the Form Contract without requiring the abandoned branch's files or text.

Do not mark this branch complete when the user returns no actual media. A statement such as `uploaded`, a filename typed into text, or a selected submit option is not an image attachment. Stay at `awaiting upload`, or route to the newly selected branch. After files arrive, re-audit coverage and explicitly list any remaining gap before proceeding.

### Detail branch

Use a form containing actual text inputs for the fields that are missing, such as:

- `Missing angles and structure` - back, side, top/bottom, interior, connector, cap/nozzle, hinge, opening, or removable-part geometry;
- `Material, color, and markings` - materials, finish, transparency, exact colors, labels, Logo placement, and unchanged identity details;
- `State changes` - open/closed, cap-on/cap-off, sealed/opened, contents/fill level, folded/unfolded, assembled/disassembled, screen/interface, or in-use behavior.

This collection form contains only required payload fields. Do not add a radio question for submission, upload, or skipping. Use the separate form-level escape or an explicit conversation request to reroute under the Form Contract; no detail text is required to abandon this branch.

Ask only fields relevant to the actual SKU and confirmed shots. Empty or vague answers do not complete this branch. Repeat a smaller detail form for unresolved facts. Once sufficient, summarize every fact and assumption in conversation, disclose the exact planned image-call count, and launch a closed form with `Confirm details and generate` / `Add more details` / `Switch to uploading real shots` / `Switch to skipping and evaluate risk`. Collect more text only after `Add more details` is selected. Only `Confirm details and generate` authorizes the paid image call.

### Skip branch

First state the exact missing views/states and likely consequences, such as changing nozzle geometry, cap construction, back label, connector placement, liquid level, or opening mechanism. Then launch a closed form with `Return to uploading real shots (recommended)`, `Switch to adding details`, and `Accept the above consistency risk and continue`. Only the last explicit response completes the skip branch. The router's `skip` choice alone does not.

### Generated reference confirmation

After generation, call `present_sandbox_file` for the actual product state reference image, explain its panel/state order in conversation, then launch a closed form with `Confirm state reference image` / `Needs revision` / `Switch to uploading real shots` / `Switch to skipping and evaluate risk`. After `Needs revision`, collect concrete corrections in a focused follow-up. Do not use the reference downstream until `Confirm state reference image` is returned without a material correction.