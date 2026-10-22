
---
name: depth_video
display_name: 深度视频复刻
description: "提取参考视频的空间深度，生成呈现远近层次的灰度深度视频；也可保留原片的运镜和动作，替换为新的人物或场景制作同款视频。适用于深度视频生成、镜头运动复现、动作复刻、换人物或换场景重拍，让原片的运动方式与新的视觉内容结合。"
tools: ["sandbox_generate_video", "sandbox_generate_image"]
---

# 深度视频复刻 Skill

两步交付：**① 源视频 → 前置 720p 压缩 → 深度视频**（ffmpeg 预压缩降载 + 脚本本地推理，非生成工具）；**② 深度视频 → 运镜复刻**（`sandbox_generate_video`，用户确认后才做）。

本 Skill 的参考文件路径：`/workspace/.skills/depth_video/references/`

```text
references/
├── depth-replicate.md        # 复刻 Prompt 句式 + 生视频参数清单 + 常见问题（进入复刻前必读）
└── scripts/
    └── depth_video.py        # 深度视频生成脚本（自动下载模型、内置 720p 兜底、保留 BGM、去闪烁）
```

## 一、任务边界

1. **输入必须有视频**。用户未上传视频时，请用户上传后再开始，不要用生成视频代替源视频。
2. **深度视频只由脚本产出**。禁止用生成工具、ffmpeg 滤镜（如 `edgedetect`/灰度化）伪造"深度视频"——脚本失败就如实报告并停在该步。
3. **复刻是可选步骤**：深度视频交付后由用户决定要不要复刻；用户明确只要深度视频时不推销复刻。
4. **脚本 stdout 即产物凭证**：末行 `wrote <路径> ... BGM=<路径或 no>` 出现即成功，禁止再用 `ffprobe`/`ls` 校验产物；需要元信息用 `sandbox_read`。
5. **生成工具返回产物即视为成功（红线）**：`sandbox_generate_image` / `sandbox_generate_video` 返回产物路径后，禁止用 `ffprobe` / `ls` / `cat` 校验文件大小或时长，禁止以"文件太小/时长不符/像是坏文件"为由重试、降参数重试或改换 VideoList 诊断。复刻调用**最多发起一次**，产物直接进入步骤 4 音频处理（该步的 ffmpeg 是既定加工步骤，不属于校验，正常执行）并 present 交由用户判断；只有工具本身返回明确错误信息时才可重试，且同参数至多一次。

## 二、执行流程

### 步骤 0：安装依赖（进入本 skill 后第一件事，每次会话一次，幂等）

sandbox 预装依赖较少，先装再跑：

```bash
pip3 install --quiet onnxruntime numpy || pip3 install --quiet --break-system-packages onnxruntime numpy
```

### 步骤 1：前置 720p 压缩与深度视频生成

#### 步骤 1.1：前置压缩至 720p（必做，防模型推理超时）

用户上传的原视频可能分辨率过大（如 1080p/2K/4K）或码率过高，直接软解与推理极其缓慢、容易触发 600s 超时。**进入推理前，先用 ffmpeg 将视频压缩为 720p**：

```bash
ffmpeg -y -i upload/用户视频.mp4 \
  -vf "scale='if(gt(a,1),-2,min(720,iw))':'if(gt(a,1),min(720,ih),-2)'" \
  -c:v libx264 -crf 23 -preset veryfast -pix_fmt yuv420p -c:a copy \
  upload/用户视频_720p.mp4
```

- **规格自适应**：短边自适应限制在 720p 以内（横竖屏自适应，偶数对齐；原片短边已 ≤720p 时保持原画不放大）；
- **音轨无损**：`-c:a copy` 快速无损保留原视频音轨（若报错音频流问题，降级为 `-c:a aac` 重试一次）；
- **后续基准**：**后续所有操作（时长裁剪、深度推理脚本等）统一使用该压缩后的 `upload/用户视频_720p.mp4`**。

#### 步骤 1.2：运行深度视频生成脚本

```bash
python3 /workspace/.skills/depth_video/references/scripts/depth_video.py \
  upload/用户视频_720p.mp4 output/depth/用户视频_depth.mp4
```

- **`sandbox_bash` 调用必须传 `Timeout: 600000`**：CPU 逐帧推理，30 秒视频约需 3~8 分钟。执行前先告知用户"深度提取处理中，预计需要几分钟"。
- 模型（约 26MB）首次运行自动下载到 `/tmp/depth_video/`（同会话复用，无需手动下载）；模型与中间产物都在 `/tmp` 下，不落 `/workspace`，不会展示给用户。脚本已内置 720p 兜底防护，未压缩的大视频会自动在 `/tmp` 下预降载。
- 输出规格由脚本保证：短边 ≤720p（不放大）、≤30fps、近亮远暗灰度。**深度视频是静音的**；源视频的 BGM 由脚本自动提取到同目录 `<输出名>_bgm.m4a`（stdout 末行 `BGM=<路径>`），复刻成片后再回填。
- **画质参数（仅当用户明确要求更精细/更清晰的深度视频时才调整，默认不传）**：
  - `--crf N`：编码质量，默认 14；用户反馈灰度渐变有色带/压缩痕迹 → 传 `--crf 10`（文件更大，耗时基本不变）。
  - `--infer-size N`：推理分辨率短边，默认 378；用户反馈主体边缘不够精细 → 传 `--infer-size 504`（**耗时约 2.5 倍**，调整前先告知用户）。
  - 两个参数解决的问题不同：色带/块状感调 `--crf`，边缘轮廓糊调 `--infer-size`，不要一起无脑拉满。
- **源视频超过 {{.max_video_duration}} 秒时**（复刻受生视频时长上限约束）：
  - 用户要深度视频本身（或深度+复刻）→ 整段跑脚本正常交付；到复刻步骤再问复刻哪一段，**该段深度片段直接从成品深度视频里剪，禁止对片段二次跑脚本推理**：
    `ffmpeg -y -ss <起点> -t <时长> -i output/depth/xx_depth.mp4 -c:v libx264 -crf 18 -an output/depth/depth_clip.mp4`
  - 用户只要复刻不要整段深度视频 → 先问复刻哪一段，裁剪 `upload/用户视频_720p.mp4` 后只对该段跑脚本（整段推理浪费算力）：
    `ffmpeg -y -ss <起点> -t <时长> -i upload/用户视频_720p.mp4 -c copy upload/用户视频_clip.mp4`
  - 问卷选项的段长**尽量用满 {{.max_video_duration}} 秒**（如 34 秒源给"前 30 秒/后 30 秒/自定义"，不要自行缩成 15 秒小段）；**复刻范围以用户所选的这一段为准**，交付后不得自行续做其余段落——用户明确要求补另一段时才继续。
- 失败处理：报 `ModuleNotFoundError` → 回到步骤 0；报 `no video stream` / `decoded zero frames` → 请用户换一个视频文件；模型下载失败 → 重试一次，仍失败则如实告知网络问题。

### 步骤 2：交付深度视频

- stdout 末行 `BGM=<路径>` → BGM 已提取，路径留给步骤 4 回填；`BGM=no (source had no audio)` → 向用户说明源视频无音轨，复刻成片将是无声的。
- `present_sandbox_file(深度视频, interrupt=false)` 展示，一句话说明：这是深度视频，白色近、黑色远，保留了原视频的运镜与动作节奏（深度视频本身无声，原 BGM 会在复刻成片时加回），可作为运镜和动作模板。

### 步骤 3：引导复刻（与步骤 2 同轮）

紧接着用 `dynamic_questionnaire` 问是否复刻（用户已明确表达过复刻意愿则跳过问卷直接进步骤 4）。**发问卷前必须先向用户说明复刻边界（一句话，不可省略）**：深度视频只能复刻原视频的**运镜和动作**，**不能复刻环境**——原片的场景、背景、光线、色彩都不会保留，成片的环境由你提供的参考图（或描述）决定。

- **复刻素材来源**（单选）：用我上传的图片 / 帮我 AI 生成人物和场景（需简述想要的人物与场景）/ 只要深度视频不复刻
- 选"只要深度视频" → 一句话收尾，结束等待，**不重复 present**。
- 用户跳过问卷直接进步骤 4 时，上述复刻边界说明改在生成视频前的告知话术里给出（同样不可省略）。

### 步骤 4：运镜复刻（用户确认后）

1. 先读 `references/depth-replicate.md`；
2. 参考图就绪（用户上传的图，或按用户描述 `sandbox_generate_image` 生成人物图/场景图，比例与深度视频一致）；
3. `sandbox_generate_video` 复刻，核心 Prompt 句式（固定骨架，禁改"严格按照"四字）：

   > @视频1 严格按照深度视频的运镜和动作，使用@图片1 和 @图片2 的人物或场景进行视频复刻

   VideoList=[深度视频]、ImageList=[人物图, 场景图]、Duration=深度视频时长、Ratio 按深度视频宽高比就近选——完整参数清单与变体见 `depth-replicate.md`；
4. **音频处理（无论源视频有无音轨都要做，生成模型自带的音频一律丢弃）**：
   - 脚本提取过 BGM → 回填：`ffmpeg -y -i 复刻成片.mp4 -i output/depth/xx_bgm.m4a -map 0:v -map 1:a -c:v copy -c:a aac -shortest output/depth/成片_final.mp4`
     复刻的是片段时，先按该段相同起止裁 BGM（`ffmpeg -y -ss <起点> -t <时长> -i xx_bgm.m4a -c copy bgm_clip.m4a`）再回填。
   - 源视频无音轨（无 BGM 可回填）→ 剥掉生成模型音频，静音交付：`ffmpeg -y -i 复刻成片.mp4 -c:v copy -an output/depth/成片_final.mp4`
5. `present_sandbox_file(成片_final, interrupt=true)` 交付——**必须显式调用，是全流程最后一个动作**；交付的是步骤 4 音频处理后的 `成片_final.mp4`，不是生成工具的原始产物；生成工具返回里即使提示"产物已发送"，present 仍不可省略（它承担交付中断语义）。交付后用户若只回"确认/继续"，一句话复述产物路径并等待，不重试、不加做新版本。

## 三、Ref 加载总表

| Ref | 加载时机 |
|-----|---------|
| `depth-replicate.md` | 用户确认复刻后、构造任何生图/生视频调用之前 |