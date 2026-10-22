# Style Prefix 空白模板（项目级视觉锁）

> Style Prefix 是贴在**每一条**提示词末尾、全项目逐字复制不变的一段视觉设定，让不同镜头"像同一部电影"。
> 下方 12 字段按你项目填实，写死后全程逐字复制，不要因某一镜"感觉要更暗"临时改。
> 范例取自 *Hell Grind*（仅作字段结构参考，勿直接套用到别的项目）。完整说明见 references/07 第四节。

## 十二字段空白模板（复制填写）

```
Style: [画质基调，如 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic]
Cinematography: [运镜哲学，如 floating immersive camera that lives with the actors; natural motivated light; painterly composed frames, strong silhouettes]
Lighting: [唯一光源逻辑，如 Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze. Key light from sky/windows only]
Color: [60:30:10 — dominant / secondary / accent，写具体 HEX 或色名]
Camera: [镜头物理，如 Physical cine lens. 180° shutter motion blur]
Skin: [肤质，如 Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light]
Acting: [表演，如 Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with catch-lights, visible breath and chest rise]
Physics: [物理，如 Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props]
Composition: [构图，如 Rule of thirds + golden ratio. Every person moving from frame one]
Continuity: [连续性，如 Characters, props, environment identical across every cut. No identity drift]
Technical: [技术，如 24fps smooth motion. 8K detail. No jitter]
Audio: [声音，如 Environmental SFX only. No music. No subtitles]
```

## *Hell Grind* 原文范例（仅字段结构参考）

```
Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: floating immersive camera that lives with the actors; natural motivated light; painterly composed frames, strong silhouettes against the light.
Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze throughout. Key light from sky and windows only.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with catch-lights, visible breath and chest rise.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

## 使用纪律
```
· 写死后逐字复制进每镜提示词末尾；末尾再叠技术尾标：Photoreal. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.
· "SFX only. No music." 是硬性——音乐属后期，生成阶段自带配乐只添乱。
· 不要因单镜临时改动 Style Prefix——一致性 > 局部"更好看"。
```
