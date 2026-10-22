
> **Node knowledge:** The PM owns ordered `frame/<project>/<video>/<frame-index>` requirements expanded from the accepted frame spec. This file defines only the media semantics and coverage rules for each frame's evidence; it does not establish a parallel coverage sidecar.

# Storyboard Source Requirements

PM's frame requirements — one per blueprint shot, `frame N` for `shot N` — are the authoritative source inventory for visual mode:

```text
frame/{video}/01
frame/{video}/02
...
frame/{video}/N    (N = video_blueprint.shots)
```

## Fulfillment

After a source image exists, call:

```bash
python3 scripts/batch_pm.py apply provide-frame \
  --subject frame/<project>/01/01 \
  --data-json '{"path":"/absolute/source.png"}'
```

PM requires:

- an absolute, non-empty image path;
- the exact ready frame node in order;
- Route B: a distinct source image for every preview frame in this video;
- Route A: the same source image only for a contiguous block of at most nine frames; when the raw 3 x 3 sheet carries fewer than nine frames, only its first `K` row-major cells are frame sources and the trailing diagnostic film-leader cells are never registered;
- later recomposition through the PM-owned source paths.

The model does not create a parallel coverage sidecar and does not add
an extra per-image attestation; the later manifest attestation and user package
review own semantic review.

## Recovery

Run `project get-next-action` and fulfill only listed ready frames. Preserve existing media and the current video blueprint. If an accepted source is missing or the user rejects its rendering, erase the corresponding frame fact, refresh focus, and generate a meaning-preserving replacement at a new immutable path only when that frame is ready. If a new Route A sheet replaces a shared source, erase all accepted frames using that source and reprovide each ready frame in its group; never overwrite the shared file in place. For a frame already ready, no extra erase is needed. Do not regenerate usable sources merely to reconstruct coverage accounting. See `revision-routing.md` for rebuilding the affected manifest, overview, package confirmation, and executable mappings; revise the plan first only when requested creative meaning changes.

A filename pattern, directory count, prior summary, or “images done” claim never establishes coverage. Coverage is complete only when every registered frame requirement is closed and each referenced source path remains alive.