
# 视频 Prompt 文法

> 本文件规定全片 prompt 结构、风格标签、镜头语言关键词与材质还原关键词。落 prompt 前必读。

## 目录
1. [Prompt 结构](#prompt-结构)
2. [统一风格标签](#统一风格标签)
3. [光影色彩](#光影色彩)
4. [镜头语言（按镜头类型）](#镜头语言按镜头类型)
5. [010核心广告帧专属补充](#010核心广告帧专属补充)
6. [材质还原关键词](#材质还原关键词)
7. [参考图引用格式](#参考图引用格式)
8. [运动描述规范](#运动描述规范)
9. [负向提示词](#负向提示词)
10. [落 prompt 前自检](#落-prompt-前自检)

---

## Prompt 结构

```
[风格标签] + [主体描述] + [镜头语言] + [光影色彩] + [质感情绪] + [负向提示词]
```

---

## 统一风格标签

```
cinematic film still, analog photography, 35mm film grain,
editorial fashion photography, natural candid moment
```

---

## 光影色彩

从 `[Environment_Input]` 提取色温与光线方向，转化为 prompt 语言。基准描述：
```
natural side lighting, [环境色温描述], low contrast highlights,
visible skin texture, no harsh flash, no studio lighting
```

示例：
- 热带正午强光 → `harsh tropical noon side light, warm ivory and amber tones`
- 室内柔光 → `soft diffused interior light, cool neutral tones, window-lit`

---

## 镜头语言（按镜头类型）

### 001 / 010 · ECU特写类
```
macro lens, f/1.4 extreme shallow depth of field,
soft bokeh, jewelry/accessory catchlight visible
```

### 002 / 007 / 009 · MS中景类
```
50mm lens, slight foreground obstruction,
environmental context from reference, natural atmosphere
```

### 005 · 剪影类
```
strong backlight, silhouette, underexposed -1.5 stops,
swirly bokeh background, female figure outline only
```

### 003 · 低角度类
```
ground level POV, extreme low angle, environmental ground details foreground,
legs in slight motion blur
```

### 004 · 情绪类
```
anamorphic lens flare, warm light leak, slight motion blur,
optical aberration, side profile, hand-held feel
```

### 012 · 背影远景类
```
focus on background environment, subject defocused foreground,
woman walking away, rear view, depth leading lines
```

---

## 010核心广告帧专属补充

```
jewelry/accessory in sharp focus as hero element,
product as primary subject, face partially visible below chin,
metal/stone surface catchlight, product structure clearly defined,
skin softly lit, face not fully revealed
```

---

## 材质还原关键词

依据 `[Jewelry_Input]` 提取的材质选用：

| 材质 | 关键词 |
|---|---|
| 银色金属 | sterling silver, cool metallic sheen, mirror polish |
| 黄金 | 18k gold, warm metallic glow, polished surface |
| 玫瑰金 | rose gold, warm pink metallic tone |
| 宝石镶嵌 | pavé setting, gemstone sparkle, point light reflections |
| 皮革/织物 | leather texture, fabric weave detail, matte surface |

---

## 参考图引用格式

```
图[1] [Character_Main 正面/侧面元素图]
图[2] [该镜头关键帧图]
```

---

## 运动描述规范

- **静帧：** `camera static, subtle natural movement only (hair, breath, fabric)`
- **推镜：** `slow imperceptible dolly push in`
- **严禁使用 zoom，一律替换为 dolly 或 tracking shot**

---

## 负向提示词

```
no direct eye contact with camera, no advertising pose,
no heavy makeup, no over-smoothed skin, no completely blurred background,
no subtitles, no watermark, no text overlay, no music, no sound effects
```

---

## 落 prompt 前自检

- [ ] 风格标签已包含
- [ ] 主体描述来自输入图提取（非套用固定描述）
- [ ] 镜头语言与当前镜头类型匹配
- [ ] 光影色彩参照 Environment_Input 提取
- [ ] 材质关键词与 Jewelry_Input 一致
- [ ] 负向提示词已附加
- [ ] 运动描述未出现 zoom
- [ ] 参考图已正确引用