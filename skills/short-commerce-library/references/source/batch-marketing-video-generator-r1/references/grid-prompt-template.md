
> **Route-A-only node knowledge.** Use only when PM next-action groups the ready frames as Route A. For every other model or conservative fallback, use `storyboard-frame-generation.md`.

# Grid Prompt Template

This template produces a raw `3 x 3` contact sheet only. It is internal material, not the user-facing storyboard overview. PM later splits the used cells row-major, adds annotations, and composes `storyboard-grid-XX.png`.

## Before Using This Template

Read this video's `video_blueprint/<project>/<video>.market_target` from `CURRENT INPUTS`. Apply its accepted audience and market treatment through the shot's actual casting, setting and styling, preserving established anchors and product facts. Do not borrow another video's target or add visible text to express the content language.

1. Confirm from the current next-action that the video is visual mode and the ready frame group is Route A. Read the accepted `frame_spec_definition` and the current `video_blueprint` in every frame context and derive each used cell from its matching entry: `visual_description` gives the frozen instant, `frame N` addresses `shot N`.
2. Resolve every product view/state, character, and required scene anchor applicable to any used cell.
3. Resolve the plan's semantic material IDs to the accepted concrete assets listed by the frame contexts, then finalize the ordered `ImageList` union for this batch. The image model cannot see plan IDs, paths, or filenames; every attachment must receive a one-based semantic index.
4. Derive `K` from the frame-spec order and this batch's frame range: `1 <= K <= 9`. The first `K` cells carry preview frames. Every trailing cell is a diagnostic film-leader image, not an invented frame. Describe all nine cells individually; never ask the image model to leave a cell blank, empty, unused, or unrendered.
5. Keep the target video ratio as the cell ratio. If `sandbox_generate_image` does not support that exact `OutputRatio`, use the closest supported same-orientation ratio, say the intended target framing in the prompt, and let PM normalize deterministically before composition.
6. Use the Route A batch block in `project get-next-action` as the call grouping only. The frame spec supplies each cell's picture requirement and the blueprint its script context; the group names the current contiguous frame nodes and cell mapping. Generate one raw-grid request for that batch, then register the same output path to every covered frame node.

## Prompt

```text
Reference image notes: Image[1] ({object, source, view/state, purpose, features to preserve}); Image[2] ({object, source, view/state, purpose, features to preserve}); ...; Image[N] ({semantic information}).

One text-free raw contact sheet at {target video ratio, e.g. 9:16}, 3 columns x 3 rows, exactly 9 fully rendered cells, read left-to-right and top-to-bottom, each cell composed at the {same target video ratio}. Describe every cell explicitly and independently. The first {K, 1 to 9} cells are the preview frames in frame-spec order: cell 1, {pure picture description, stating which Image[N] images are used to preserve what}; ...; cell {K}, {pure picture description, stating which Image[N] images are used}. When K is less than 9, enumerate every remaining cell separately using this visual content: cell {K+1}, a single text-free neutral photographic film-leader still, dark charcoal exposure frame, subtle analog grain, small edge sprocket-perforation motifs, no people, product, environment, logo, symbol, letter, or number; ...; cell 9, the same clearly recognizable text-free neutral film-leader still. These diagnostic film-leader cells are ordinary rendered pictures used only to stabilize the 3 x 3 layout and make the frame boundary easy to inspect; they are not preview frames. The nine cells fit tightly with no divider lines, outer border, gutter, or gap. The film-leader design stays inside each diagnostic cell and must not become grid spacing. Adjacent actual-shot cells are distinguished naturally by different compositions; no image may merge or bleed across cells. The whole sheet must not contain shot numbers, timecodes, titles, subtitles, dialogue bubbles, annotations, info panels, watermarks, or other text. Keep the actual-frame cells visually consistent: {characters, product, scene, style, palette, lighting, texture, and composition baselines}. Keep the confirmed product appearance, packaging, character identity, wardrobe, scene space, and art style consistent across actual-frame cells as shown in Image[N]; do not add unconfirmed product text, prices, selling points, claims, or CTAs.
```

## Tool Call Rules

- `ImageList`: actual absolute paths for every applicable product, character, scene, prop, style, palette, lighting, or derived-state reference relevant to any used cell. Put required identity/continuity references before optional style references.
- `Prompt`: the completed template above with no unresolved `Image[N]`, path, filename, or "the attached image" language. It must spell out cells 1 through 9 individually; expand every ellipsis and cell range before the tool call. It must not instruct the model to leave any cell blank, empty, unused, or unrendered.
- `OutputPath`: a new immutable raw path such as `_internal/storyboard-01/route-a-sheet-01.png`; never overwrite an accepted source.
- `OutputRatio`: the exact target ratio when supported; otherwise the closest supported same-orientation value.
- `IsIntermediate`: `true`.
- `Model`: omit entirely; `sandbox_generate_image` cannot select a model.

Minor separator lines, imperfect diagnostic film-leader cells, or other cosmetic raw-sheet artifacts are acceptable. Only the first `K` row-major cells are registered as frame sources; trailing diagnostic cells are ignored by `--grid-shot-counts` and must never be registered as frame requirements. If a request is safety-rejected while fulfilling the current Route A frame focus, use the current project's `frame reject --subject frame/<project>/XX/YY --reason-json ...`; PM keeps the frame ready and makes it the exclusive recovery focus. An unreadable/corrupt sheet or collapsed/missing cells also leaves the affected frame requirements unresolved. Do not silently switch to Route B, rewrite confirmed meaning, or continue another batch; wait for the user's recovery decision.