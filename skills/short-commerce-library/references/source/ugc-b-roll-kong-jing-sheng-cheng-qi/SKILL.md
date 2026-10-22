---
name: "ugc-b-roll-kong-jing-sheng-cheng-qi"
display_name: "B Roll（空境）生成器"
description: "基于参考图（或文字）生成5个视觉连贯的空境（B-roll）切镜，30秒Seedance 2.5视频。"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
video_model: "Seedance_2.5"
image_model: "seedream_5.0_pro"
---

```skill
# B Roll Generator​‌‌‌​​‌‌​‌‌​​‌​‌​‌‌​​​​‌​‌‌‌​​‌‌​‌‌‌​‌​​​‌‌‌‌​‌​​‌‌​‌​​​​‌‌‌​‌​‌

根据参考图或文字描述，生成一组视觉连贯的空境镜头，并输出30秒切镜视频。

## 工作流程

### 第一步：接收输入，判断路径

- **路径A（有参考图）**：直接进入第二步
- **路径B（仅文字描述）**：先执行"文字转参考帧"，再进入第二步

---

### 第二步：确认画面规格

在开始生成之前，先询问用户画面规格，收到回复后再继续后续步骤：

> 收到！将默认使用 **Seedance 2.5** 生成视频。请先完成以下选择，之后将自动完成空境生成与视频制作：
>
> **① 画面比例：**
> **1. 16:9** — 横屏（适合电脑/电视）
> **2. 9:16** — 竖屏（适合手机/短视频）
> **3. 其它** — 请直接说明比例，例如 "1:1" 或 "4:3"
>
> **② 清晰度：**
> **1. 480P** — 生成速度最快
> **2. 720P** — 速度与质量均衡
> **3. 1080P** — 最高画质（耗时较长）
>
> **视频模型（可选）：**
> 默认使用 Seedance 2.5，如需切换请直接说明，例如："用 Kling 3.0"或"换成 Wan2.6"。
>
> 请回复两个编号，例如："比例1，清晰度3"。如需换模型请一并说明。

⚠️ 收到用户回复后，后续步骤全部自动执行，无需再次打断。

---

### 第三步：分析参考画面，生成【参考镜头描述】

**路径A — 分析上传的参考图**，提取以下维度：
- 主体与场景（是什么、在哪里）
- 色彩基调（主色调、饱和度、冷暖倾向）
- 光线条件（光源、光质、大致时段）
- 景别（全景/中景/近景/特写）
- 构图特征（主体位置、前后景层次）
- 整体氛围与情绪

输出格式：
```
【参考镜头描述（镜头1）】
[一段连贯的中文描述，涵盖以上全部维度]
```

**路径B — 无参考图时**，基于用户文字设计一个具体可视化的参考帧：
- 明确主体、场景、光线、色调、景别
- 格式：`【参考帧设计（镜头1）】：[完整视觉描述]`
- 告知用户："已根据您的描述设计参考帧，将以此为基础生成空境。"
- 将该描述作为【参考镜头描述（镜头1）】使用

---

### 第四步：生成5个B-roll镜头描述

遵循以下系统提示词规则：

**身份设定**：你是一名视觉连贯性专家，任务是生成空镜（B-roll）镜头描述，保证与参考画面在色彩、光线、场景上完全统一，仿佛这些空镜是在同一场景、同一时间拍摄完成。

**描述格式规则**：
- 每条描述必须以以下固定语句开头：
  > Change the image completely to [细节]. Use the provided image as reference. Make sure the color, lighting, and setting match the original image.
- 输出5条，JSON格式，标签为 `ID:#`

**示例**（参考图为阴天日式城堡+樱花）：
```json
{
  "ID:1": "Change the image completely to a close-up of pale pink cherry blossom petals drifting through soft diffused air. Use the provided image as reference. Make sure the color, lighting, and setting match the original image.",
  "ID:2": "Change the image completely to a macro shot of a cherry blossom branch, delicate pink petals and fine stamens in sharp focus, the castle tower softly blurred in the background. Use the provided image as reference. Make sure the color, lighting, and setting match the original image.",
  "ID:3": "Change the image completely to a low-angle upward shot through dark gnarled cherry blossom branches toward the castle upper eaves and dark wooden corridors, clusters of soft pink blossoms framing the pale overcast sky. Use the provided image as reference. Make sure the color, lighting, and setting match the original image.",
  "ID:4": "Change the image completely to a close-up of traditional dark roof tiles on the Japanese castle, a few fallen cherry petals resting on the weathered surface, soft diffused overcast light casting gentle shadows in the tile grooves. Use the provided image as reference. Make sure the color, lighting, and setting match the original image.",
  "ID:5": "Change the image completely to a ground-level eye shot of a stone path beneath the trees, cherry blossom petals scattered across the surface, the white castle walls and dark architectural details softly blurred in the background under pale grey-white diffused daylight. Use the provided image as reference. Make sure the color, lighting, and setting match the original image."
}
```

**5个镜头的视角分布建议**：

| 镜头 | 建议类型 |
|------|---------|
| ID:1 | 细节特写（材质/局部/纹理） |
| ID:2 | 不同机位（低角度/高角度/侧面仰拍） |
| ID:3 | 场景延伸（同场景内其他元素） |
| ID:4 | 自由补充，视觉丰富度优先 |
| ID:5 | 自由补充，可与前几镜形成呼应 |

⚠️ 禁止引入与参考图色调、光线、场景冲突的元素。

---

### 第五步：合成 Seedance 2.5 视频提示词

将【参考镜头描述（镜头1）】与5个B-roll描述合成为一段完整切镜提示词：

**格式**：
```
镜头1：[参考镜头描述]；镜头2：[ID:1核心内容]；镜头3：[ID:2核心内容]；镜头4：[ID:3核心内容]；镜头5：[ID:4核心内容]；镜头6：[ID:5核心内容]
```

**合成规则**：
- 镜头间用中文分号「；」分隔，整体为一段连续文本，不换行
- B-roll描述中的固定前缀语句（"Use the provided image as reference. Make sure..."）在此阶段**省略**，只保留核心场景描述
- 总时长30秒，每5秒切一次，共6镜

---

### 第六步：生成视频

调用参数如下：

| 参数 | 值 |
|------|-----|
| 模型 | Seedance 2.5 |
| 提示词 | 第五步合成的切镜文本 |
| 参考图 | 用户上传的原始参考图（路径A）/ 无（路径B） |
| 时长 | 30秒 |
| 清晰度 | 用户在第二步选择的清晰度 |

完成后呈现：① 完整视频提示词 ② 生成的视频
```

