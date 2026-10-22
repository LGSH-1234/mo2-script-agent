# 广告分镜与镜头工艺（适配指南）

已有创意时先把“希望用户感到什么”转成“画面中实际发生什么”。形容词不能代替动作、光线与镜头。

## 分镜最小契约

每镜交代主体、动作、景别/机位、运镜、光线/材质、声音及时间。一个镜头以一个主要动作或注意力变化为中心；复杂动作拆镜，优先保持因果可读。

先做文字 shot list，确定镜头顺序与商品出场，再决定是否需要多宫格分镜图。分镜图只是预览，不能因为图里有格子就认为每个镜头或视频已生成。

| 环节 | 具体做法 | 验证 |
|---|---|---|
| 商品身份 | 重用同一参考，明确轮廓、结构和材质 | 每镜都能辨认同一 SKU |
| 动作 | 起始状态 → 施力/触碰 → 结果 | 接触点与物理关系成立 |
| 表演 | 视线、呼吸、眉眼、嘴角、姿态和停顿 | 微表情与台词重音吻合 |
| 真实感 | 保留实物纹理，光照服从材质 | 不用“磨损”伪造真实性 |
| 节奏 | 全貌/细节/使用过程交替 | 每镜有新增信息，不只是换角度 |
| 转场 | 动作方向、遮挡、相似形状或声音连接 | 前后主体、轴线与空间可解释 |
| 收尾 | 商品可辨识的稳定画面 | 后期文字有安全区域 |

广告剧情里商品需要参与人物选择或结果，而不是在无关故事后面补一帧包装。原文导演风格、电影构图、艺术化或喜剧方法只在当前任务适合时采用，不强迫所有商品走电影短片。

## 工具落点

提示词写法复用 `seedance-prompting`，调用前检查当前模型的 schema、参考图数量、时长和比例。原文 Seedance 2.5 字段、MJ 参数、21:9 画幅、参考视频/音频输入不一定受支持。

短视频已进入 `short_video_produce` 时由它处理渲染和复用，不自行补一条脱离 brief 的视频。独立广告镜头只有在实际 schema 支持时使用 `gen_video`；短剧镜头继续走 `drama_render_shots`，本库不改变该规则。

## 原文入口

- `source/seedance-shot-design/SKILL`、`source/seedance-shotlist-director/SKILL`、`source/multi-grid-storyboard/SKILL`：镜头与预览。
- `source/character-realism-enhancer/SKILL`、`source/emotion-expression-director/SKILL`、`source/emotion-director/SKILL`：材质与表演。
- `source/cinema-dna-21x9x3/SKILL`、`source/ugc-b-roll-kong-jing-sheng-cheng-qi/SKILL`：构图与环境镜头。
- `source/ugc-chuang-yi-guang-gao-pian-dao-yan/SKILL`、`source/ugc-bian-ju-ju-ben-fen-jing-shi/SKILL`：创意与叙事参考。
- `source/seedance-previz-to-render/SKILL`：保留预演结构的思路；深度/白模视频渲染能力尚不能视为已接入。

其他编剧、表演、美术和分镜方法均列在 `source-index`；原文中的多专家指令是参考流程，不代表实际调用了独立专家。
