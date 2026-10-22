
# Reference And Action Craft

Use this guide while determining necessary material evidence, preparing visual assets/frames, or binding references in a complete or lowered prompt. It complements the existing asset and payload contracts; it does not authorize new assets, product changes, or edits to accepted content.

## Assign Authority By Dimension

After finalizing the current call's ordered attachments, name both the subject and the information each source contributes. Where leakage is plausible, state what to ignore. Separate identity, shape, color/material, label placement, view/state, environment, composition, light, and style rather than asking the model to "follow all references."

Example, only when these are the actual attached inputs:

```text
Image[1] defines presenter Maya's face, hair, and accepted wardrobe.
Do not adopt its background or incidental handheld objects as the advertised product.
Image[2] defines the advertised bag's visible geometry, material, color,
hardware, and logo placement. Do not adopt the person or background in this source.
Image[3] defines the room layout and furniture; ignore people in that image.
Maya uses this one bag in that room. Preserve the respective identities.
```

Two views of the same SKU describe one continuous object, not two products. Name the common identity and each view's role. Use stable subject names when pronouns could confuse ownership, especially in handoffs between people.

One image can support several roles when the accepted evidence actually covers them. Follow the [Image Attachment Identity Contract](payload-route-gates.md#image-attachment-identity-contract): attach the path once, then explain each supported role using the same final index. For example, when one accepted image depicts both the presenter and advertised bag:

```text
Image[1] defines presenter Maya's face, hair, and wardrobe.
The bag held by Maya in Image[1] defines the advertised SKU's visible shape,
material, color, and logo placement. Preserve both identities.
Do not adopt this image's background; use the setting specified in this prompt.
```

This is two semantic roles, not two image parameters. Do not duplicate the path to give the bag another image number. Conversely, sharing a file does not authorize treating an incidental bag as the advertised SKU without supporting accepted facts.

For an authorized local edit, specify the source/base, target region, operation (`keep/change/add/remove`), the source of each changed dimension, and preserved dimensions. A style reference may affect lighting or composition without replacing product geometry. A supplied person's outfit or accessory is not the advertised SKU unless explicitly identified as such.

If sources conflict on a material attribute and the accepted facts do not resolve it, seek the existing clarification/revision path. Do not choose a new SKU or redesign an identity merely to reconcile references. Unreadable lettering is not permission to invent text.

These examples use the current tool's positional `Image[N]` syntax. Rebuild indices when attachment order changes. Carry the resulting semantic mapping into the actual Prompt or PromptPath contents under `payload-route-gates.md`; internal asset IDs and paths are not substitutes. Keep all audio examples consistent with `voice-anchor-gates.md`: neutral voice samples control timbre only, never words or timing.

## State Evidence Versus Motion Evidence

A still image establishes a visible state, not the unseen path into that state. An open container image can anchor an already-open presentation; it does not establish its hinge, seal removal, required force, or complete opening motion.

When the requested demonstration depends on those mechanics, identify available motion evidence: an applicable reference video or ordered state images, with confirmed details for invisible directions or timing. Describe only supported stages, such as:

`Start state -> hand/tool contact -> motion direction -> intermediate state -> observable endpoint`

This is an authoring aid, not a required number of images. Do not demand a reference video or a full set of views for every simple action. If the accepted idea can start from a supported completed state without changing its meaning, do so. If it promises the opening or transformation itself, do not silently replace it with a beauty shot; resolve the missing basis through the owning requirement.

For VideoSpec, distinguish which source establishes identity, which supports a required state, and which supports an essential action. Use definition IDs and blueprint shot semantics; this guide adds no per-shot mapping.

## Make Physical Interaction Legible

Describe relevant hand/tool contact, support, size, orientation, direction, and endpoint. A soft pouch, rigid box, pump, cap, garment, or interface has different mechanics. Avoid action verbs that leave the model to invent how this specific object works.

For a raw storyboard frame, choose one readable phase of the accepted action; do not cram the entire transformation into a single still. For Route A, assign references and action phases per real cell, without changing the existing film-leader treatment of trailing cells. For Route B, keep the same identity and state semantics across independent calls.

Preserve gravity, contact, quantity, prop ownership, and supported material behavior. A frame or a generated endpoint may supply continuity guidance, but it cannot become new factual evidence of product performance or replace the original identity source.