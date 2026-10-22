
# 平台执行与创意规格契约（SKU/程序锁 · 平台执行底线 · 首秒可读 · 卖点预算 · 抖音节奏 · 主张分级）

> 本文件是以下约束的**唯一权威正文**：current_sku_lock、program_lock、平台执行底线、opening_hook_contract（首秒信息可读）、时长—卖点—信息节拍预算、speech_rhythm_contract、主张表达分级。SKILL.md 只做激活与调度，遇到这些主题以本文件为准。

### 当前 SKU 锁与品类变体隔离

创意编译前先建立 `current_sku_lock`，它只描述本次实际要拍的那一个 SKU，不是整个品类的功能总表：

```yaml
current_sku_lock:
  product_identity:
  product_form:
  handle_or_interface:
  material:
  working_surface:
  confirmed_capabilities: []
  category_options_not_current_sku: []
  exact_dimensions: []
  allowed_scale_descriptions: []
  evidence_sources: []
  unresolved_conflicts: []
```

- 用户同时介绍了软/硬、长/短、干/湿等多个品类变体，而产品图只指向其中一款时，其余放入 `category_options_not_current_sku`，不得混入当前脚本。
- 图上可见规格、款式或材质文字可作当前 SKU 依据；与用户明确文字冲突时仍以用户表述为先，但冲突会改变卖点或用法时只问一个最小问题。
- 精确尺寸已知时优先直接写数值与真实人手/身体比例；不自创生活物件类比。类比与数值明显不一致属阻塞项。

### 独占证明程序与导入预算

候选选定后立即生成 `program_lock`；它是内部执行合同，不向用户暴露名称或编号：

```yaml
program_lock:
  selected_content_program:
  current_sku_match: exact | adjacent | extrapolated
  source_coverage:
    exact_sku_form: exact | adjacent | extrapolated
    duration_fit: exact | compressed | extrapolated
    evidence_basis: observed_cluster | general_mechanism
  persuasion_job:
  main_proof_loop:
  required_signature: []
  minimum_main_proof_seconds:
  auxiliary_beat:
  auxiliary_seconds:
  forbidden_imports: []
  ending_in_task: true
```

- 20 秒内只能有一个 `selected_content_program`。它的主证明动作可用不同景别、方向、接触点或前/中/后状态重复，但不能借“节奏丰富”导入另一套卖点程序。
- **动作密度 ≠ 卖点密度。** 动作密度是同一证明回路被更近、更真、更连续地观察；卖点密度是把起泡、材质、多用法、冲洗、收纳等排成清单。后者不得冒充前者。
- 15 秒默认主证明回路占全片至少 8 秒，或占去 Hook 之后时长的至少 60%；辅助证明最多一个、不超过 1.2 秒。用法教程等无法压缩的内容应延长时长，不变成走马灯。
- `source_coverage` 为 `adjacent/extrapolated`时，只提供可验证假设，不能声称已复刻精确款式与时长的标杆效果。用户要求高保真复刻时，应优先请其提供精确 SKU 和相近时长的参考。
- 只能导入一个与主回路同因果的辅助节拍；冲洗/悬挂/静态商品定妆默认不是通用收尾。CTA 覆盖在正在发生的使用、验证或完成动作上。

### 平台执行底线与 Style 原生适配

当平台为抖音、TikTok、TikTok Shop，或用户明确要求抖音感/手机 UGC 时，先锁定平台执行底线，再把 Style 编译为该底线内的原生变体。Style 可以改变色板、光线、材质观感、表演幅度与剪辑气质，不能降低主动作占比、切断任务连续、把收尾变成长静帧或让手机观看关系消失。

内部优先级为：**商品事实与安全 > 用户明确硬约束 > 主证明可成立性 > 目标平台执行底线 > 模板核心机制 > Style 表层美术**。用户同时锁定互不相容的精致品牌片与纯原生抖音外观时，只问一个最小问题；否则自动做原生适配，不把裁决丢给用户。

### 首秒信息可读合同（20 秒内平台短视频硬性）

“首帧有动作”不等于“Hook 已经成立”。写脚本前必须建立下面的开场合同，使观众无需等待解释就知道第一拍为什么值得看：

```yaml
opening_hook_contract:
  hook_question:
  hook_carrier: spoken_line | on_screen_text | self_evident_visual | distinctive_sound
  first_information_at_seconds:
  viewer_can_name_problem_or_desire_by_seconds:
  spoken_hook:
  on_screen_hook:
  visible_contrast_or_consequence:
  distinctive_sound_and_causal_result:
  unframed_silence_seconds:
  silent_opening_authority: none | user_locked_asmr | user_locked_visual_hook | user_locked_sound_hook
  product_answer_at_seconds:
```

- **0.5 秒内必须出现可理解信息，1 秒内必须能说出问题、欲望、反差或观看收益。** 手在动、水在滴、人物在走、镜头在推等只有运动没有信息的画面不算 Hook。
- **未经明确机制授权，无信息留白最多 0.4 秒。** 首镜对白为空、无画面文字且只剩普通环境音时，默认失败；自动补一条短口播/短文字，或把画面改成一眼可懂的强失败、强结果或强反差。
- **无口播开场必须自证。** 只有用户锁定 ASMR/声音 Hook，或画面/特征声音脱离后文也能独立讲清问题时，才允许超过 0.4 秒不说话；普通水滴、环境底噪、轻微摩擦和“泡沫略少”不构成独立信息载体。
- **细微问题必须由语言框定。** 若失败或差异需要观众仔细观察才能理解，最迟在 0.8 秒前出现一句人的立场、疑问、命令或短文字；商品随后在同一任务中介入。不得让观众先看 2–3 秒普通动作，再解释刚才看到了什么。
- **“证明处让声”只能用于 Hook 已建立之后。** 中段可安排 0.3–0.8 秒无口播窗口，让摩擦、起泡、开合、冲洗等同期声突出证明；不能把这条规则机械搬到开场，制造无信息铺垫。
- 第一镜在 `故事脚本.md` 的对白栏为空时，必须在画面/音效中写明唯一的信息载体与可见因果，并在内部证明 `viewer_can_name_problem_or_desire_by_seconds ≤ 1.0`；否则对白栏不得为空。
- 第 6 步用 `validate_creative_contract.py` 校验内部 JSON 合同里的 `opening_hook_contract`(时间与载体字段可结构化断言,逐项核对)。**首秒是否真的成立、首镜画面/音效是否与对白栏一致、观众能否在 1 秒内说出问题——这类语义判定 `validate_final_prompt.py` 不做**(它只对实际 Prompt 做确定性禁止项/结构扫描);首秒信息可读由你依据本合同正文自行落进故事脚本与 Prompt 并自检。

### 时长—卖点—信息节拍预算

商品模型可以保留完整事实，但单条视频不得因为“都是真的”就全部输出。先按时长生成 `content_budget`，再建脚本：

| 整片时长 | 主打卖点 | 支撑卖点 | 其它信息节拍 | 默认总卖点上限 |
| --- | ---: | ---: | ---: | ---: |
| 6–8s | 1 | 0 | CTA | 1 |
| 9–15s | 1 | 0–1 | CTA；安全/限制/信任点最多择一 | 2 |
| 16–20s | 1 | 1 | CTA；最多 1 个信任或限制节拍 | 2 |
| 21–30s | 1 | 1–2 | CTA；最多 1 个教程/信任模块 | 3 |
| 31–45s | 1 | 2–3 | CTA；可分章展开证明 | 4 |
| 46–60s | 1 | 3–4 | CTA；可容纳教程、限制与信任 | 5 |

- “一个卖点”指一个独立购买理由，不是一个形容词。同一主张下的材质、结构和动作只要共同回答同一购买理由，就作为支撑事实，不机械分成多个卖点。
- 频率、禁忌、使用力度、价格、CTA 和搜索词虽不一定是卖点，但都占用**信息节拍**。同一 15 秒视频不能通过“这些不算卖点”绕过容量限制。
- 用户锁定的内容超预算时，给出延长版与当前时长精简版让用户拍板；Agent 自写内容则自动降级未入选卖点到商品模型/后续选题，不向用户追问。
- 60 秒以上按每 12–15 秒一个可闭环内容单元分章；每个新卖点必须有独立证明，不是延长口播清单。

### 抖音口播节奏档

命中抖音/快节奏带货时，不只写“语速偏快”，而是把速度、停顿和句子职责写进分镜：

```yaml
speech_rhythm_contract:
  language:
  profile: conversational | douyin_native | promo_burst | safety_explainer
  target_rate:
  max_rate:
  pause_range_seconds:
  line_budgets: []
```

- 中文 `douyin_native` 默认 5.5–6.5 有效字/秒，句间停顿 0.15–0.35 秒；首句可短促、实操段回到自然节奏。`promo_burst` 可短时到 6.5–7.2 字/秒，但不贯穿全片；安全/用法说明保持 4.5–5.5 字/秒。
- 加快的前提是句子口语化、一句只一个意思。不允许用 7.2 字/秒以上的机械语速硬塞超额卖点。
- 对每一句分别核算 `有效字数 ÷ 实际可说时长`；不用整片平均值掩盖某一句过快或大段无职责空白。
- 口播说立场、不易从画面看出的因果和 CTA；画面已能证明的动作不再用口播逐字重复。

### 主张表达分级

创意检索不是商品事实来源，但**证据门不等于功效词禁用门**。按以下三级处理用户提供的商品主张：

- **A级｜可直接表达的商品功能与即时物理结果**：用户已明确提供、且可由商品结构或当场动作直接支持时，可以写入卖点和口播；例如完成清洁、切割、收纳、触达、起泡、连接、遮挡、照明、加热、降温或减少步骤等具体任务。用当前商品真实动作和可观察结果证明，不因这些词带有“效果”就自动删除或改成纯外观展示。
- **B级｜体验、感受或外观改善**：可按用户提供的主张使用“帮助改善、使用后感觉、看起来更、日常护理、操作更省事”等经验性表达；画面以即时状态、感官代理、动作、覆盖或体验反应承接，不得伪造长期真人记录。若用户提供真实同主体、同条件材料，可升级为相应证明。
- **C级｜生理机制、医疗、金融、安全或其它强结果**：用户明确提供的主张不自动删除，按行业风险使用帮助性、非绝对表达，并保留必要条件、正确用法和禁忌。治疗、治愈、减脂、收入保证、绝对安全、永久有效等强结论必须有相应依据；没有依据时只降低证明强度和措辞，不能伪造成检测、临床、测量、收益或保证性结果。

任何真人前后对比、测量数字、第三方背书、长期使用结果仍必须有真实素材。缺证据时改变的是**证明强度和措辞**，不是把 A 级核心卖点整体规避。不得生成伪造的真人实测、评论截图、测量数据或前后对比。

### 交付范围路由

> 完整正文的唯一权威是 [contract-interaction-products-delivery.md](contract-interaction-products-delivery.md) 的「交付范围路由」节（`script_only / creative_only`、`prompt_only`、`generate / edit / extend / assemble` 四类范围如何决定读不读 Seedance 指导、创不创建 `视频生成Prompt.md`、进不进素材与视频确认）；走到该主题时读那里，本文件不复制正文。

### Hook 脚本合同

> 完整正文的唯一权威是 [contract-creative-and-script.md](contract-creative-and-script.md) 的「Hook 脚本合同」节（传播职责、因果机制、标志性线索、实现变量、用户锁定元素、商品化方式、场景职责与六项融合检查）；走到该主题时读那里，本文件不复制正文。

### 15 秒内部职责预算

15 秒视频默认把时间优先给一个购买理由：约 0-3 秒完成首屏信息与商品化触发，约 3-11.5 秒完成主证明及必要的专项推进，约 11.5-15 秒完成结果变化与 CTA/品牌记忆。这是信息预算，不是强制模板退出点。

面向用户的 `故事脚本.md` 不输出 `Hook Scope / Bridge / Body takeover` 等工作流标签，也不展示 USP、P00 或评分回执；把传播职责、因果机制、标志性线索和商品证明自然落进镜头动作与台词。

Hook 的世界规则、运动、声音或母题可以贯穿，只要每次出现都新增商品证据、人物判断、任务状态、关系变化或品牌记忆。若只是重复奇观、展示模板编舞或挤压主证明，重写实现变量。