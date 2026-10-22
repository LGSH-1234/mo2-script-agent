
# 运行环境与制作流程

## 工作目录

本技能通常位于 `/workspace/.skills/knowledge-motion-explainer`，以加载时给出的实际目录为准。每条视频使用独立的 `/workspace/assets/<英文项目名>`。命令调用不假设变量跨进程保留：

```bash
SKILL_DIR=/workspace/.skills/knowledge-motion-explainer
PROJECT_DIR=/workspace/assets/topic-explainer
AUDIO_DIR="$PROJECT_DIR/audio-build"
mkdir -p "$PROJECT_DIR"
```

过程文件写入 PROJECT_DIR，不修改技能源码。保留完整讲稿、分镜、资料来源、素材、原始配音请求与返回、原始字幕时间来源、当前 timing/SRT/WAV、工程和渲染结果。音频重做时使用新的 AUDIO_DIR，避免覆盖后混用旧文件。交付时不逐个推送中间产物。

## 环境准备

```bash
python3 "$SKILL_DIR/references/scripts/audio_pipeline.py" inspect-env
command -v node
command -v hyperframes
hyperframes --help
```

确认当前 FFmpeg、ffprobe、Python、Node、HyperFrames、浏览器及实际可用的字体/GSAP。有声字幕合成需要 FFmpeg 的 `subtitles` 滤镜及本地字体；浏览器运行检查需要当前环境已安装的 Playwright/Puppeteer 和浏览器。使用已安装 CLI，并按其 help 确定参数；只有 npx 可用时先串行解析一次，后续复用已解析的版本。

字体和素材复制到项目相对路径：标题字体、正文字体都需真实存在，确认含所需中文字形。加载完成后再注册时间线，避免渲染时回退字体。渲染不依赖 CDN；缺必要依赖时说明具体错误，不静默换成空图或粗糙占位。

新配音使用 `sandbox_generate_audio`。按 [选择字幕时间来源](audio.md#选择字幕时间来源) 确认字幕时间来源，通过 SRT 导入同批音频与时间轴。

## 工程制作

按 [composition.md](composition.md) 写原生工程。依据主体质量选择 SVG、Canvas、本地图像或混合实现，不通过限制图形元素的模板决定整个视觉。

先做开场主视觉与核心机制帧，再扩展全片。字体、图片加载、根尺寸、时间控制和第一次实际抽帧均通过后再长时渲染。字幕与镜头共用本批次真实 timing，字幕在最终合成时叠加；样例的人工秒数只适用于其静音示范。

## 预览与渲染

以下命令以本机 CLI help 为准。抽帧点取本片开场、每个机制的变化前中后、切场边界和片尾；这些数值是命令示例：

```bash
hyperframes check "$PROJECT_DIR/project" --json
hyperframes snapshot "$PROJECT_DIR/project" --at 0,3.0,5.9 \
  --output "$PROJECT_DIR/review" --describe false
hyperframes render "$PROJECT_DIR/project" --quality standard --workers 1 \
  --output "$PROJECT_DIR/silent.mp4"
```

先解决运行和布局错误。读取检查报告的实际范围和 samples 数，`0` 次运行、未启用的检测或未检查的属性表示缺口，不是通过。对比度检查通过仍要看层级、主体与参考风格是否达到目标。

在长时渲染前，使用 [check_composition.mjs](scripts/check_composition.mjs) 对预览页面按帧率遍历完整时间线。先看 `node ... --help`，传入正在运行的本地预览 URL、实际 composition ID 与本地 Playwright/Puppeteer 模块和浏览器路径。必须加 `--layout-check` 同时检查实际文本布局，Canvas 文字先按 [文字排版](composition.md#文字排版) 接入测量。脚本捕获同步绘图异常、页面错误和资源失败，并按帧率检查当前可见文字框的越界、裁剪及相互碰撞；实际执行帧数应覆盖目标时长。它检查原生 `window.__timelines[id]` 时间线，不替代当前 HyperFrames 的渲染兼容性检查。

```bash
node "$SKILL_DIR/references/scripts/check_composition.mjs" \
  --url "$PREVIEW_URL" \
  --browser-module "$BROWSER_MODULE" \
  --executable "$BROWSER_EXECUTABLE" \
  --layout-check --output "$PROJECT_DIR/runtime-check.json"
```

三个变量分别替换为本次已启动的本地预览地址、已安装浏览器模块绝对路径、浏览器可执行文件绝对路径，不猜测路径或额外安装。默认文字安全边距为各边画幅 4%，文字组间距为 `12 × 高度 / 1080` 逻辑像素；确需按设计调整时使用 `--layout-inset-ratio` 和 `--layout-gap`，保留具体值，不以关闭检查处理错误。

检查报告必须分别显示布局采样与文本覆盖。Canvas 文字未测量、全片没有测到任何文字、坐标无法对应等不能视为通过；单帧确实没有文字不要求硬加文字凑计数。按问题时间、文字 ID、字框坐标修正实际排版，再复查相关动作全程；将这些时间加入最终视频的 `checkpoints` 看图确认。该检查不包含 FFmpeg 后加字幕、不做 OCR，也不能证明图像或粒子没有遮住文字；这些继续按最终帧审阅。

不要只查第 0 秒，或只跑 `node --check` 就声称动画可运行。全时间运行检查不逐帧截图，避免占用大量磁盘；视觉截图按关键事件采样。如果环境没有可调用的浏览器检查接口，用当前 CLI 确实支持的运行检查覆盖相同范围并记录样本数。没有等效能力时标记技术验证缺口，不能伪造通过结果。

关键机制看完整动作，不只看漂亮的末帧。随机前后 seek，确认首次跳到中段与倒回同一时刻的像素状态一致。Canvas 检查是否真的清空重画，是否依赖被抑制的 callback，粒子是否由固定输入决定。

预览帧用于提前纠正构图。合成后按 [review.md](review.md) 从最终 MP4 抽每镜代表帧，逐张看图，联系图作全片总览。复杂机制追加状态前中后；字幕专项检查另取句中及边界邻帧。不要用机械导出大量图片代替逐张判断。记录实际差异，修改后重查同点与受影响动作。只有媒体文字描述时，可以与预期对照检查被明确描述的内容，但细节、几何关系和美感仍未验收；给读取工具附上问题不代表后端确实会按该问题看图。

有声视频按 [audio.md](audio.md) 烧录字幕、合成 WAV，并绑定对应 timing。用户明确要求无字幕时按脚本 help 的无字幕选项执行；用户要求静音且无字幕时，渲染输出直接命名 final.mp4。

## 成片验证

```bash
ffprobe -v error -show_format -show_streams -of json "$PROJECT_DIR/final.mp4"
ffmpeg -v error -i "$PROJECT_DIR/final.mp4" -f null -
```

核对尺寸、帧率、实际时长、音轨与完整解码。额外检查每场代表句和跨场句：声音、短句字幕、当前机制是否一致。只有文本匹配、文件 hash 与容器检查时，不能宣称主观听感或准确同步已经通过。

自动检查不能证明字幕已在每一帧可读，也不能衡量美感。最终按 review 清单查看实际抽帧；检查结果对应成片 hash，重新合成后旧记录失效。

## 问题修复

| 现象 | 处理 |
| --- | --- |
| 全文配音失败 | 确认失败后只完整重试一次；仍失败保留工程并说明，不改多段生成 |
| 字幕缺能力或失败 | 保留主音轨与时间来源，按 audio 的可用路线完成对齐；能力缺失时说明尚未完成的部分 |
| 字幕提前讲下一场 | 回查原始字幕时间来源，按短句重排机制与切场；不只改字幕显示时长 |
| 字幕闪烁、停留或缺句 | 先比较讲稿、时间来源、派生字幕和最终画面，定位数据、显示或合成层；检查是否重复绘制字幕，重新从绑定时间轴合成，不添加随机延时掩盖问题 |
| 画面冻结或动作缺失 | 查全时间运行报告中的异常与失败时点，修复后重新覆盖完整时间范围；解码成功不能排除绘图执行失败 |
| 底部空带、主体太小 | 查 root/scene/素材实际尺寸、比例和 padding，再修构图；不是简单换背景色 |
| 所有画面像草图 | 回到主视觉质量、字体角色、材料与层级，先精修两张代表帧；不靠增加卡片或转场补偿 |
| 中文缺字 | 选择覆盖该字的本地字体，重新加载后抽同一帧 |
| 随机 seek 状态不同 | 去掉实时/累积状态，固定粒子初值并从时间重算 |
| 标题、标签越界或相互重叠 | 核对加载字体后的真实字框、最大文案与运动变换；移动/换侧、换行或分时显示并重算引线，重新逐帧布局检查及同点抽帧，不以裁字或抬高层级遮盖问题 |
| 标签和字幕重叠 | 核对最终合成字幕的实际范围，再调整图内文字位置或同时显示的信息；不修改真实字幕时间来迁就布局，不持续缩小字号 |
| 渲染长时无响应 | 查现有进程、日志和输出，确认失败才重跑；不要重复提交仍在执行的任务 |

长任务分为配音、字幕对齐、构建、渲染、合成，保留各阶段真实结果，不用一条命令重复整个流程。