
# 配音与字幕

## 生成完整配音

最终旁白只允许一个完整生成源。将最终讲稿全文一次交给 `sandbox_generate_audio`，全文一次生成，保持同一音色与表达；重试或改稿时整体替换，不拼接不同生成结果。

调用前检查 `narration.txt` 已包含完整开头、解释和结尾。Text 只含需朗读的文字与自然标点，不含镜头编号、时间码、舞台提示。示例：

```json
{
  "Type": "tts",
  "Text": "<narration.txt 的完整内容，替换此占位后一次提交>",
  "VoiceDesc": "普通话自然科普讲解，清晰温和，语速从容，按完整语义停顿，术语读清；整篇声音、距离与表达稳定",
  "Lang": "zh",
  "OutputPath": "assets/topic-explainer/audio/narration-master.mp3"
}
```

按实际 schema 调用，不添加不存在的 rate、seed、voice ID 等字段。保存完整请求与工具返回到 `narration-request.json`、`narration-result.json`，后续使用真实返回路径。

### 重试与时长处理

- 明确失败后先检查实际返回及文件，不把工具等待状态当成失败重复提交。确认失败才完整重试一次。
- 重试仍失败就停止配音，保留工程并说明失败；不改为分段生成。
- 未指定时长时，起稿保持约 30 秒的一条核心解释；明确指定长片时不能暗中缩成短片。完整稿无法在当前能力下生成时，让用户选择缩短范围或提供整段录音。
- 时长不合适但生成成功时，调整全文信息量和自然停顿，再整体重做。不要在已生成的不同版本间挑句拼接，不截句、不加速塞入目标时长。
- 生成成功后立即用 ffprobe 检查时长，先处理与用户目标的偏差，再对齐、分镜和渲染。文件扩展名不代表真实编码；以解码后的媒体为准。自然语速不靠加速处理，目标时长也不能在交付时悄悄放宽。
- 已有用户配音使用该连续文件，不重新生成。

## 无字幕视频

用户明确不要字幕时，省略转写，只绑定一份完整主旁白和讲稿：

```bash
python3 "$SKILL_DIR/references/scripts/audio_pipeline.py" import-master \
  --audio "$PROJECT_DIR/audio/narration-master.mp3" \
  --without-subtitles --transcript "$PROJECT_DIR/narration.txt" \
  --output-dir "$AUDIO_DIR"

python3 "$SKILL_DIR/references/scripts/audio_pipeline.py" mux \
  --video "$PROJECT_DIR/silent.mp4" \
  --voice "$AUDIO_DIR/narration.wav" --timing "$AUDIO_DIR/timing.json" \
  --no-subtitles --output "$PROJECT_DIR/final.mp4"
```

该路线没有语音短句时间，不能声称完成字幕或精准句级对齐。按完整音轨实测时长编排画面，听辨关键动作的对应关系；最终仍抽帧、播放检查。无字幕 timing 不能用于默认烧字幕模式。用户需要字幕但对齐尚未完成时，不能擅自使用此路线交付。

## 选择字幕时间来源

生成新配音前，确认至少一种字幕时间来源可用：

1. **本次 TTS 实际提供句/词时间戳**：保存原始返回，按真实字段与单位转换成 SRT，保留每条的来源索引。只含全文、URL、DurationMs 的返回不具备此能力；词级时间按语义合并，使用首词起点、末词终点，不按字符比例拆分句子。
2. **已有与完整音频匹配的字幕/对齐结果**：核对音频版本、语言、内容和时长。优先复用环境中已有的字幕对齐能力，按实际接口获取结果。
3. **实际听辨标注**：能访问并听辨原音时，按下一节测量短句时间。能执行 FFmpeg、打开波形或取得媒体文字摘要，不等于具有听辨能力。没有听辨能力时不能声称走通此路线。

均不可用时，保留工程并说明缺少句级时间依据，请用户提供匹配 SRT，或选择无字幕版本。字幕要求不变时保留待对齐状态；已有主旁白继续复用。

## 听辨与波形辅助

配音始终保留为一条连续主音轨。听辨时可在同一文件上 seek 和循环播放，不逐句调用 TTS，不将试听区间拼接为成片。先通听全文，确认实际读词与讲稿一致，然后逐句测量起止。

用仅依赖 Python 标准库和 FFmpeg 的 [audio_timing_review.py](scripts/audio_timing_review.py) 生成轻量辅助材料：

```bash
python3 "$SKILL_DIR/references/scripts/audio_timing_review.py" \
  --audio "$PROJECT_DIR/audio/narration-master.mp3" \
  --output-dir "$PROJECT_DIR/audio-review"
```

脚本输出 `waveform.svg`、`candidates.json`，包含实际解码时长、音频 hash、能量曲线与低能量区间。它不识别文字、不输出 SRT、不把静音判成句界。只分析未混配乐的主旁白；噪声、呼吸、轻声和句内停顿均可能影响候选。必要时按 help 调整阈值，不能调到“候选数量恰好等于句数”就宣称对齐。

标注步骤：

1. 以原音为准逐句定位，在候选附近播放并测出第一字起点与末字终点；句内没有停顿时仍须听辨，不能硬吸附到最近静音。
2. 记录 `alignment-review.json`：原音 hash、方法 `manual-listening`、每句文字、start/end、实际回听区间、未解决项。只有真正听过才记录已核对；波形位置不能证明读了哪个词。
3. 每条控制在两行、32 个非标点/空白字符及 8 秒以内。需要更细分界时重新听辨测量；顺序覆盖全文，不跳字、不把相邻句的词搬过去。
4. 把核对后的文字和测量时间写入 `verified.srt`，标记 `--timing-source manual`。再次连续播放完整原音，对照所有字幕，检查首尾、数字、术语、跨镜头句及句内无停顿处。

仅能看波形不能完成第 1、4 步时，标记待对齐，不生成标称精确的 SRT。听辨记录是可追溯依据，不是脚本自动证明语音正确的证书。

## 导入已核对的字幕时间

按 [runtime.md](runtime.md) 设置本次路径，然后执行：

```bash
python3 "$SKILL_DIR/references/scripts/audio_pipeline.py" import-master \
  --audio "$PROJECT_DIR/audio/narration-master.mp3" \
  --srt "$PROJECT_DIR/audio/verified.srt" --timing-source manual \
  --transcript "$PROJECT_DIR/narration.txt" \
  --output-dir "$AUDIO_DIR"
```

音频路径换成真实返回位置，`--timing-source` 按来源选择 `tts`、`asr`、`forced-alignment` 或 `manual`；上例是实际听辨的结果。保存原始时间来源及转换记录，不能把估算值标为 manual。脚本会：

- 导入核对后的 SRT，不估算内部句界；以实际解码时长校验范围；
- 比较整篇转写和讲稿，忽略标点与空白，保留数字与文字差异供核对；
- 拒绝缺句、错文、重叠、明显越界及粒度过粗的字幕；末条轻微超出媒体终点时仅裁显示区间，原始观察时间保留并给出警告；
- 将唯一主旁白解码为连续 48 kHz mono WAV，不拼接、不重排、不变速；
- 输出同一批次 `narration.wav`、`captions.srt`、`timing.json`，记录输入和输出文件 hash。

`observed_captions` 保留导入字幕的原始文字和观察时间；`captions` 使用同样起止，文字可以包含已核对的识别纠错；`display_captions` 是最终显示区间，可能包含已记录的末尾裁切。三者不能冒充彼此。镜头可以覆盖多个短句，场景开始时间也不等于第一句开始时间；`c001` 等只是时间轴 ID，不代表独立音频文件。`timing.duration` 是音频实测时长。先完成导入，再确定镜头时序。

原始服务返回是只读证据；实际听辨的修正应更新测量记录并重新导入，不能仅为通过验证而改时间。不能删除不一致文字或搬动相邻句中的词。阅读所有 warnings；文件绑定、范围与全文覆盖通过，不等于已证明语音对齐。

### 常见问题处理

| 检查结果 | 正确处理 |
| --- | --- |
| 转写错别字、术语或数字不一致 | 对照真实读音核对。确认只是识别错误时，另存 `text-corrections.json`，通过下面的纠错参数导入；不编辑原始响应，不搬动相邻句中的词 |
| 实际口播漏字、读错或改了词 | 不用原稿覆盖缺失声音。接受实际说法时同步修订讲稿；必须纠正口播时全文重生成、重新对齐 |
| 单条过长 | 默认上限 32 个非标点/空白字符、8 秒。若服务已返回更细的真实时间，按其边界分条；或在能听辨时实测分界。不能按字符比例、平均时长或静音吸附猜时间，也不能扩大上限把整段讲稿挂屏 |
| 只有整段时间，没有可用短句时间 | 按 听辨与波形辅助 听辨测量；无听辨能力则保留主音轨并说明缺口 |
| 时间被脚本判为越界或来源不一致 | 核对音频和原始时间来源，必要时重新对齐正确文件；不能提高容差或改时间绕过。脚本允许的有限末尾显示裁切不改变观察时间 |
| 识别语言与口播不同 | 核对源文件与识别结果，不直接翻译成讲稿语言冒充原始转写 |

### 文字纠错与翻译

识别纠错用 JSON 对象保存，键是原始短句顺序编号，值是该句完整的修正文字：`{"c001":"<核对后的第一句全文>"}`。只填写确需修正的条目；映射不能含时间或新增短句。在 `import-master` 命令中加入：

```bash
--text-corrections "$PROJECT_DIR/audio/text-corrections.json"
```

原始服务返回与导入 SRT 均保持可追溯。脚本保留原文、修正文和映射文件绑定。每处修改另记核对依据；不能只因为讲稿不匹配，就假定音频一定读对、把识别结果全部替换为原稿。

用户明确要求翻译字幕时，先按原语言完成音轨与讲稿校验，再把所有句子的译文保存为 `subtitle-texts.json`，格式同上，必须覆盖 `c001` 到最后一句，不缺项、不多项。在最终 `mux` 命令中加入：

```bash
--subtitle-texts "$PROJECT_DIR/audio/subtitle-texts.json"
```

译文只替换显示文字，保留原句时间；脚本绑定译文文件，报告中同时保留原始、核验和显示文本。译文太长时精简译法或使用真实更细句界，不估算新时间、不通过缩成小字塞满画面。原语言字幕仍用于核对真实口播，不被译文覆盖。

## 根据字幕时间编排画面

一条字幕只覆盖当前说出的短句，不长时间展示完整段落。每条最多两行，1080p 通常从 40–52 px 起步；靠底部安全边距，衬底只包住文字，关键标签避开字幕。

从本次 timing 编排机制动作，最终字幕由脚本读取同批数据统一烧录，不手抄一套数组。画面讲到下一机制时，对应口播已进入该语义。完整音轨改动后，字幕和镜头时间一起更新。

语速自然优先。用完整稿的句法与标点组织停顿，核心变化完成后留观看时间；句内太快不能靠片尾补很多静音修复。片长略长于口播时可保留短暂结果画面，但差距过大应改讲稿或镜头节奏，不用几秒至十几秒静帧填满。

## 合成与验证

先渲染无音轨、无口播字幕的画面为 `silent.mp4`。确认 FFmpeg 有 `subtitles` 滤镜，准备含所需字形的本地字体文件及其真实 family name；缺失时先解决环境，不临时换成 HTML 字幕。使用同一批次文件：

```bash
python3 "$SKILL_DIR/references/scripts/audio_pipeline.py" mux \
  --video "$PROJECT_DIR/silent.mp4" \
  --voice "$AUDIO_DIR/narration.wav" --timing "$AUDIO_DIR/timing.json" \
  --font-file "$PROJECT_DIR/project/fonts/body.ttf" --font-family "<实际字体族名>" \
  --output "$PROJECT_DIR/final.mp4"
```

脚本核对 WAV、SRT 与 timing 的绑定，生成对应 ASS，统一烧录字幕并混入主旁白。没有匹配字幕的时段留空，不重复旧句；文字换行只改变排版，不推算新句界。保留 `<成片名>.captions.ass` 和 `<成片名>.mux-report.json` 供复查。工程不能提前烤入字幕，否则会出现双层字幕。

默认字幕样式以可读性为准；调整字体大小时先看脚本 help，并在最终帧核对中文、两行排版和遮挡。布局空间不足时调整图形工程或精简合法显示文，不绕过原语言覆盖校验。

配乐可选，用 `--bgm <实际音乐文件> --bgm-gain 0.7` 添加；低于旁白，不能盖住辅音。固定低音量混音和限幅不等于最终 LUFS 已测量。

```bash
python3 "$SKILL_DIR/references/scripts/audio_pipeline.py" verify \
  "$PROJECT_DIR/final.mp4" --duration 30 --width 1920 --height 1080
```

参数换成实际要求。继续执行 [review.md](review.md)：先在每镜代表帧检查字幕可读性与遮挡，并核对首句、跨镜头句和末句。首次使用或改动字幕生成/显示逻辑、修改时间轴，或出现闪烁、遗漏时，执行字幕专项模式，检查每条中点及出入点邻帧。机制变化时还需播放核对声画关系。

同一时间表可以保证工程使用一致的时序，不能独自证明口播边界识别准确、实际字幕同步或听感通过。保持一条完整生成的旁白，再取得它的真实句级时间；不能为了获得容易相加的时长重新分段生成配音。无法听辨时如实记录限制。