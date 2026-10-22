
# Asset Consistency

## Contents

1. Trigger
2. Decision order
3. State and logic check
4. Asset-specific rules
5. Reference mapping
6. Prompt handoff

## Trigger

Run only after a Hook is selected and before compiling the Seedance Prompt. Prepare a continuity asset only when all are true:

1. the element appears in the Hook
2. the same identifiable element is expected in the immediately following product video
3. visible or audible drift would break continuity
4. text alone is unlikely to preserve it

Typical anchors are the actual product/package, a recognizable recurring character, a distinctive key prop, a reused room/set, a continuous visual style, or a recurring voice identity supported by the runtime.

Because the following segment is a product video, treat the actual product/package as recurring whenever it is visible in the Hook. Do not ask whether it should stay consistent.

Do not create continuity assets for anonymous background people, generic hands, disposable weather/crowds, replaceable decoration, one-shot fantasy spaces, or a product that is absent from the Hook and does not control its style.

Keep this as orchestration state. Never add asset status, upload history or downstream notes to the Seedance Prompt.

## Decision Order

For each required anchor:

1. **Reuse supplied asset**: prefer the user's authorized image, video or audio.
2. **Generate fictional baseline**: create a canonical reference when the element is fictional and safe to design.
3. **Request upload**: require an asset for a real person, real commercial product, branded package, copyrighted design or proprietary location that cannot be invented faithfully.
4. **Remove dependency**: if unavailable and nonessential, revise the Hook so the element is generic, hidden or absent.

Do not silently generate a substitute for a real product or person.

## State And Logic Check

Reduce the selected Hook to:

```text
start state → peak state → end state
```

Verify for every recurring subject:

- the reference covers the angle and starting state required by the action
- the action does not invent controls, hinges, openings, accessories or packaging
- the peak preserves one stable recognizable product view
- the end can connect to the next segment without a second unrelated action
- action, camera, dialogue and exclusions are compatible

Rewrite contradictions before preparing assets. Do not solve them by adding more references.

Examples of contradictions: demanding a bite while hiding all mouth/face areas; opening a mechanism whose only reference is already fully open; preserving a front label while covering it for the entire reveal; requiring one continuous take across incompatible locations.

## Asset-Specific Rules

### Product And Key Prop

- Use the actual product image or uploaded asset for a real/branded product.
- Prefer one clean hero or three-quarter view as the primary reference.
- Request another angle only when the Hook needs an unseen surface, mechanism or state.
- Inspect sealed/torn, locked/open, folded/unfolded, off/on, full/empty and assembled/disassembled needs.
- Preserve shape, color, material, package structure, label placement and included accessories.
- Treat dense multi-view boards as inspection material; select or crop a canonical view to avoid leaking alternate SKUs, refills or accessories.
- Keep exact package text out of the attention event when the runtime cannot preserve it reliably.

Generate a clean canonical design only for a fictional or generic recurring prop. Avoid unauthorized logos and decorative text.

### Character

Use authorized supplied images for a real recurring character. Prefer a clear face reference for identity and a three-quarter/full-body reference when outfit and silhouette matter.

For a fictional recurring character, generate a neutral, well-lit canonical image with unobstructed face, fixed hairstyle, outfit, silhouette and signature accessories. Use separate face and full-body references when both matter; do not rely on a dense three-view sheet alone.

### Scene

Require a scene reference only when both segments share an identifiable space or continuous take.

Reuse a supplied wide image/frame, or generate one canonical wide reference for a fictional set. Preserve layout, doors/windows, major furniture, palette, time of day and light direction. Do not generate a scene asset for a background that ends with the Hook.

### Voice And Sound Identity

Reuse an authorized audio reference only when the same voice or distinctive sound must continue and the runtime supports audio reference. Do not imitate a real person's voice without permission.

## Reference Mapping

Upload only required assets and reuse valid handles. Preserve user-established labels; otherwise assign stable `@图片N`、`@视频N`、`@音频N` labels in first-use order.

Do not invent a label until the asset exists and is attached. Stay within runtime limits and prefer the smallest control set that preserves continuity.

## Prompt Handoff

After assets exist:

1. load and follow `seedance-reprompt-skill`
2. bind each recurring subject to its actual label
3. separate face, outfit, product, scene, motion and audio reference roles when needed
4. describe only states supported by the references
5. mention only attached assets in the Prompt
6. keep filenames, upload IDs, asset-generation history and continuity decisions outside the Prompt
7. return reusable paths, handles or mappings only when new assets were generated or uploaded