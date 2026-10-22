
> **Node knowledge:** This file defines only the semantics and format of the `story_master` artifact. The PM determines when it is ready and validates the actual consecutively numbered row count against the shot count in evidence.

# storyboard.md Template

Use the semantic structure below for `storyboard.md`. Keep that filename, but localize the user-visible document. It is the single reusable mother story for the batch, not a list of every video version and not one video's final storyboard.

## Language Layers

Apply [user-communication.md](user-communication.md) to the entire document, not just its title or table cells. The English template labels specify field meanings; they are not literal keys to copy.

- Write the title, every table header, shot references, descriptions, and human-readable labels such as "exploration item", "narration", or "None" in `COMMUNICATION LANGUAGE`. For Chinese communication, use a title such as **故事母版** and headers such as **镜头**, **时间**, and **已确认内容**. Do not leave the headers in English above localized rows or add bilingual duplicate headers unless requested.
- Describe spoken-content intent in `COMMUNICATION LANGUAGE`. If actual narration, dialogue, or monologue is included, preserve its confirmed video-content language; do not translate it merely to match the document. When content language varies across batch directions or is still open, retain that distinction as an exploration item rather than assuming one language for every video.
- Preserve machine identifiers, stable material IDs, filenames, paths, and PM evidence keys exactly. Localizing a Markdown header does not rename `shots` or `duration_ms` in PM evidence. Preserve confirmed brand/SKU names, factual quotations, and packaging text.

## Document Structure

`storyboard.md` should contain only its localized title and storyboard table. Localize the following template before filling its rows; do not copy these authoring instructions into the artifact. Keep discussion in conversation and complete per-video directions in the direction-set evidence. Do not put PM evidence in this file.

```markdown
# story master

| Shot | Time | Confirmed content | Exploration items / left blank | Picture | Action/Camera | Speaking character and spoken-content intent | Product presence | Material references | Notes |
|---|---|---|---|---|---|---|---|---|---|
```

The code block intentionally contains no sample data rows. Add exactly one numbered row for every creatively justified shot in the complete finished video, starting at `1` and continuing without gaps.

Rules:

- This is the final shared story-master table, not a planning log.
- The table itself is the reusable story structure: put already confirmed elements in `Confirmed content`, and leave the parts meant to differ blank or mark them as `exploration item` in `Exploration items / left blank`.
- Keep only one copy of the shot sequence. Do not add a `video` column, video numbers, or repeated rows for every video version.
- Do not add separate sections for fixed content, exploration directions, rationale, status, or logs.
- Use confirmed facts and exploration constraints from `information-understanding.md`, explicit conversation choices, the accepted creative-assistant handoff, and the bundled `marketing-creative-guidance.md`. Accepted information is authoritative for facts; searched inspiration may improve story expression but may not add product claims. Do not cite the internal handoff, URLs, search history, or research reasoning inside `storyboard.md`.
- Product/SKU, character, and scene can be exploration items. Keep them open in this table when they are meant to differ across videos.
- There is no default shot count. Determine the count from the user's target finished-video duration, actual narrative beats, pacing, and the bundled `marketing-creative-guidance.md`. Never copy the planned video total into the shot count: `6 videos` means six batch directions, not six shots in each video. This template controls the artifact format and user-confirmation semantics.
- Before the `confirm-story` action, count the actual numbered table rows and submit that exact value as `shots`. PM rejects a value that differs from the artifact.
- Do not resolve, mention, or mark the selected video model's per-call duration limit here. This table describes the complete finished video and is independent of later runtime splitting.
- The image route does not control the story count. For a complete video with `S` confirmed shots, PM derives `ceil(S / 9)` contact-sheet calls for the exact UI-injected `Image model` values listed under Route A in [visual-workflow.md](visual-workflow.md); every other value and the conservative unknown fallback derive `S` one-shot image calls. A contact sheet always renders all nine cells; cells after the first `K` real shots are individually described diagnostic film-leader pictures, never blank cells or story shots. `sandbox_generate_image` cannot receive a `Model` argument.
- Keep the confirmed complete duration, timing, and shot count aligned with every video blueprint. For opted-in visual-mode videos, project each plan into an aligned raw-frame set, source manifest, and full storyboard sheet.
- Do not mark future video-call boundaries or add local call timecodes. Those are derived internally only after the complete per-video resources are confirmed.
- `Speaking character and spoken-content intent` describes spoken audio only. Identify the intended speaker and whether the beat is narration, dialogue, or monologue; when the speaker itself is an exploration item, mark it clearly instead of silently defaulting to narrator. Do not plan generated subtitles, captions, dialogue bubbles, or title cards unless the user explicitly changes the no-subtitle requirement.
- Do not create separate `storyboard-01.md` files unless the user explicitly asks.
- Do not include asset audit details, tool arguments, or generation prompt text.
- After this table is confirmed, present each video's concrete exploration direction in conversation. Do not add those video-specific choices to this file.
- Present the actual `storyboard.md` through `present_sandbox_file`, using its localized shared-story display name when the runtime schema supports one, then show the table or a compact readable version in conversation.
- After presentation succeeds, explain in `COMMUNICATION LANGUAGE` that one shared story master serves the whole planned batch: confirmed content remains shared and exploration items will be filled differently for each video, so this does not mean the workflow will make only one video.
- Keep that explanation in conversation, not inside `storyboard.md`. Launch a closed `dynamic_questionnaire` only after presentation, using localized labels meaning "Confirm story master" / "Needs revision" and no custom/other option or generic text question. If modification is selected, collect the concrete change request in a focused follow-up. If revised, re-present the actual revised file before launching the form again. After recording confirmation, return to PM next-action instead of predicting the downstream workflow from this template.