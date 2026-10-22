
# VideoSpec Definition Contract

At READY `video_spec_definition/<project>/<video>`, read the complete current video blueprint. Extract every object that may appear, whether supplied, delegated or still to be created, by media type. PM expands named children only after this declaration is accepted. `video_spec` and `images/audios/videos` are structural collections; never report facts to them.

Use `provide-video-spec-definition` with exactly three mappings: `images`, `audios`, `videos`. Explicitly empty mappings mean no requirement of that type. Keys are stable, unique single-segment semantic IDs, not file paths or Image[N] positions. Preserve IDs introduced in the blueprint. A material may appear in any number of shots; appearances and adoption instructions remain in the blueprint's prose, not a structured shot-to-material mapping.

Each entry requires:

- `role`: semantic use, such as product, character, scene, style, voice identity, narration, music or motion reference. This is descriptive, not a separate node class.
- `description`: complete content constraints, intended use, adopted/ignored reference dimensions and relevant market implications.
- `allowed_resolutions`: a non-empty subset of provided, auto, waived. This declares permitted evidence; it does not grant authorization or satisfy the child.

Declare these boolean process constraints where applicable:

- `product_coverage`: required product view/state coverage. Only valid for images with allowed_resolutions=["provided"]. This expands the product coverage gate.
- `review_required`: provided media must carry successful present_sandbox_file presentation and user acceptance evidence. Enable for assets requiring individual user acceptance under the asset/voice guides. It does not force extra review for an explicit auto/waived fact; those need their own actual user authority.
- `continuity`: optional descriptive metadata; it never controls runtime entity creation. Lowering materializes every auto object before any part input.
- `voice_sample`: neutral timbre reference; requires audio. Generated runtime samples retain the 3000 ms limit. Narration and music are not automatically timbre samples.

Waived is permitted only for optional supplemental product image references. Such an entry must set `supplemental_to` to a distinct image ID declared with product_coverage=true. The product base stays provided-only. Characters, scenes and voices use provided/auto, never waived. Free-text role labels do not grant waiver permission.

Derive policies from the story, accepted user intent and the asset/voice guides. Do not relax them merely to advance the graph. A speaking character's visual identity and timbre are separate media requirements. Product consistency cannot be delegated away. A background track and a timbre reference may both be audio, but must describe different uses.

The blueprint owns shots, duration_ms, ratio and market_target (language, country_region, audience, platform). Do not repeat those facts here. Declaration does not require its own user confirmation; independently required asset reviews and final package confirmation remain explicit gates.

See evidence-and-commands.md for the report shape, and media-requirements.md for fulfilling children.