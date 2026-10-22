
# 编译内部校验合同 JSON · 完整必填字段模版

> **本文件是三个 `validate_*.py` 校验器所需 JSON 合同的唯一权威字段模版。**
> 第 3 步 `validate_creative_contract.py`、第 4 步 `validate_story_script.py`、第 6 步 `validate_final_prompt.py` 在生成产物前都要喂一份内部 JSON 合同给对应校验器。照本文件的模版填字段即可。
>
> 用法:走到第 3/4/6 步、即将跑校验前,即时读本文件对应小节,把模版复制为一个真实 JSON 文件(内部文件,放 `_internal/`,不展示给用户),按当前项目实况填值,再执行校验。返回结果分两栏:`errors`(结构/时长/泄漏/禁用词/自相矛盾等确定性硬门)非零/`ok:false` 就按它改**产物**并重跑,不得展示失败版本、不得以"我自查通过了"代替真跑;`warnings`(证据词/顺序等语义提示)不阻塞 `ok`,逐条判断——漏了补进产物、只是换了等价说法就忽略,绝不为字面命中把好表达改生硬。
>
> **【禁止读校验器源码 · 本条为全 Skill 唯一权威,其它文件只指向此处、不再复述理由】** 无论是想反推字段、还是想看懂某条错误信息,**任何情况下都不允许 `Read`/`cat`/`grep` `scripts/validate_*.py`(三个校验器)源码**。原因:① 字段该怎么填,本文件模版已写全;② 校验器返回的每个 `errors[]` 都是一句**中文自然语言**,已直接写清「哪里出问题、改哪个产物、怎么改」,照着改产物、重跑即可;③ 读源码既浪费上下文,又会把内部实现当成用户可见内容泄漏,而且毫无必要。若某条错误信息一时看不懂,回到对应产物按其字面意思修正,仍不得读源码。
>
> 字段值语言:JSON 里的枚举/键名是内部机器标识,保持英文原样;它们只进校验器,绝不出现在给用户看的文本或最终产物里(见「用户可见语言隔离合同」)。

---

## 0. `--contract` 怎么传(三个校验器通用,跑校验前先看这节)

**`--contract` 同时接受「JSON 文件路径」和「内联 JSON 字符串」两种写法,任选其一,不必为了过校验先落一个临时文件。** 判定规则:参数值以 `{` 或 `[` 开头 → 按内联 JSON 解析;否则按文件路径读取。

```bash
# 写法 A(合同较长、需留档时):先写文件,再传路径
python3 scripts/validate_story_script.py <项目>/故事脚本.md \
    --contract <项目>/_internal/story_contract.json

# 写法 B(合同只有一两个字段时最省事):直接内联,不创建任何文件
python3 scripts/validate_story_script.py <项目>/故事脚本.md \
    --contract '{"duration_seconds": 15}'
python3 scripts/validate_final_prompt.py <项目>/视频生成Prompt.md \
    --contract '{"forbidden_sku_terms": ["钢丝球"], "unsupported_claim_terms": ["杀菌"], "forbidden_imports": []}'
```

**能不能省略 `--contract`,以本文件第 2、3 节的门为准**:一旦本项目有已选 Hook(`hook_acceptance_contract`)或说服质量合同(`quality_acceptance_contract`),`--contract` **必传且必须原样带上这些对象**,不得省略、不得删减——省略等于跳过 Hook 追溯门与说服质量追溯门。只有在这两类合同都不适用时才可省略:`validate_story_script.py` 省略时跳过总时长对齐;`validate_final_prompt.py` 省略时三类禁止项按空处理、仍跑时间轴结构门与字幕冲突门,并在返回里带 `note` 说明禁止项未被检查。

**入参错误一律返回 `{"ok": false, "errors": [中文说明]}` 并退出 1,不再抛 traceback / argparse usage。** 照 `errors` 字面修正即可,**不要因为看到报错就去读校验器源码**:

| 现象 | 含义与修法 |
| --- | --- |
| `--contract 指定的文件不存在：xxx` | 路径写错或文件还没写。注意**相对路径是相对当前工作目录**——`cd .skills/marketing-video-creator` 之后再传 `_internal/xxx.json`,找的是 skill 目录下的它、不是项目目录下的它;跨目录一律用**绝对路径**,或直接改用内联 JSON。 |
| `--contract 传的内联 JSON 解析失败` | 引号/逗号不完整。shell 里用**单引号包整个 JSON**,JSON 内部用双引号。 |
| `要校验的故事脚本/Prompt 文件不存在` | 被校验产物的路径写错,同样按绝对路径核对。 |

**下面三个错法是线上高频故障,已在脚本侧修好,不要再绕路**:
1. 想内联传合同却被当成路径 → 现已原生支持内联,不必再先 `sandbox_write` 写一个临时 contract 文件再传。
2. `validate_final_prompt.py` 漏传 `--contract` 吃到 argparse usage → 参数本身已改为可选(不再报 usage);但**有 Hook / 说服质量合同时仍必须传**,可选只是为了让报错变得可读,不是允许跳过验收门。
3. 报错后去 `grep`/`head` 校验器源码反推参数 → 依然禁止;参数写法本节已写全,错误信息本身也已写明修法。

---

## 1. 第 3 步 · `validate_creative_contract.py`(融合创意合同)

调用:`python3 scripts/validate_creative_contract.py <contract.json>`(或 stdin 传入)。校验融合规格、执行落地与本地化的结构完整性。

### 1.1 完整模版

```json
{
  "current_sku_lock": {
    "object_state": "physical",
    "unresolved_conflicts": []
  },
  "selected_content_program": "<所选内容程序名>",
  "program_lock": {
    "selected_content_program": "<与上一行逐字一致>",
    "source_coverage": {
      "exact_sku_form": true,
      "duration_fit": true,
      "evidence_basis": true
    },
    "main_proof_loop": "<主证明循环的一句话描述>",
    "minimum_main_proof_seconds": 4.0,
    "auxiliary_seconds": 1.0,
    "ending_in_task": true
  },
  "hook_claims": ["<开场主张1>"],
  "proof_answer_shot": "<回应开场主张的证明镜说明>",
  "sku_eligibility": true,
  "asset_eligibility": true,
  "eligibility_conflicts": [],
  "platform": "抖音",
  "duration_seconds": 15,
  "adaptive_fusion": {
    "product_specific_tension": "<该商品特有的张力>",
    "opening_event": "<开场事件>",
    "opening_state": "<开场状态>",
    "product_causal_action": "<商品导致的因果动作>",
    "proof_state": "<证明状态>",
    "end_state": "<结束状态>",
    "selected_modules": { "hook": true, "play": true, "style": true },
    "module_observable_effects": {
      "hook": "<hook 的可观察效果>",
      "play": "<play 的可观察效果>",
      "style": "<style 的可观察效果>"
    },
    "style_modulation": "<style 落地到执行的调制说明>",
    "generic_template_skin_only": false
  },
  "persuasion_quality_contract": {
    "brief_integrity": {
      "required_elements": [
        {"requirement": "<用户点名的人群/场景/商品/数量/固定动作等>", "status": "covered", "planned_shot": "S1"}
      ],
      "unresolved_conflicts": [],
      "unreadable_critical_assets": [],
      "unsupported_high_risk_claims": []
    },
    "product_exclusivity": {
      "irreplaceable_product_fact": "<当前商品独有或本条真实采用的事实>",
      "fact_source": "<权威来源>",
      "replacement_test_passed": true,
      "story_elements_requiring_rewrite_if_replaced": ["hook", "proof"]
    },
    "proof_chain": {
      "claim": "<本条唯一主证明主张>",
      "buyer_doubt": "<要回应的顾虑>",
      "baseline_state": "<动作前可见前态>",
      "product_action": "<当前商品具体动作>",
      "observable_change": "<同一对象上的可见变化>",
      "result_or_task_consequence": "<可核验结果或任务后果>",
      "evidence_basis": "<素材/商品事实依据>",
      "observable_result_before_judgment": true,
      "voiceover_only": false,
      "package_text_only": false,
      "unearned_reaction_only": false,
      "fantasy_only": false
    },
    "functional_durable_goods_guard": {
      "applicable": true,
      "applicability_reason": "<购买理由依赖硬件/耐用品完成具体任务>",
      "appearance_is_only_proof": false,
      "functional_action": "<真实功能动作>",
      "user_task_result": "<动作后的可观察任务结果>",
      "user_benefit": "<结果对应的具体使用收益>",
      "user_requested_variant_count": 8,
      "planned_distinct_variant_count": 8,
      "sku_variant_coverage_plan": "<如何在实际分镜中覆盖用户明确要求的 SKU/颜色/款式>",
      "not_applicable_reason": ""
    },
    "emotional_causality": {
      "required": true,
      "pressure_or_desire": "<人物的具体压力/欲望>",
      "choice_before_product": "<商品动作前人物的选择或判断>",
      "evidence_trigger": "<人物看见/听见/体验到的商品证据>",
      "changed_decision_or_relationship": "<证据导致的决定/关系改变>",
      "visible_payoff": "<可见回报>",
      "not_applicable_reason": ""
    },
    "novelty_mechanism": {
      "product_specific_mechanism": "<商品事实与叙事/视觉规则的独特组合>",
      "noncosmetic_state_change": "<不是换皮的状态变化>",
      "generic_sequence_only": false,
      "surface_swap_only": false
    },
    "conversion_closure": {
      "required": true,
      "witnessed_evidence": "<CTA 前观众已见证的证据>",
      "choice_reason": "<为什么选择当前商品>",
      "action": "<搜索/商品卡/预约/到店等明确动作>",
      "evidence_to_cta_connected": true,
      "not_applicable_reason": ""
    }
  },
  "quality_acceptance_contract": {
    "requirements": [
      {"id": "proof-action", "role": "product_action", "fields": ["画面描述"], "all_of": ["<当前商品具体动作>"], "any_of": []},
      {"id": "proof-result", "role": "observable_result", "fields": ["画面描述", "音效"], "all_of": ["<可观察结果>"], "any_of": []},
      {"id": "hardware-function", "role": "functional_action", "fields": ["画面描述"], "all_of": ["<功能动作>"], "any_of": []},
      {"id": "hardware-task-result", "role": "user_task_result", "fields": ["画面描述"], "all_of": ["<用户任务结果>"], "any_of": []},
      {"id": "hardware-benefit", "role": "user_benefit", "fields": ["画面描述", "对白·旁白"], "all_of": [], "any_of": ["<具体利益点表达 A>", "<具体利益点表达 B>"]},
      {"id": "sku-coverage", "role": "sku_coverage", "fields": ["画面描述"], "all_of": ["<覆盖全部用户明示款式的可验收描述>"], "any_of": []},
      {"id": "changed-outcome", "role": "changed_outcome", "fields": ["画面描述", "对白·旁白"], "all_of": [], "any_of": ["<任务后果>", "<人物决定改变>"]},
      {"id": "conversion-cta", "role": "cta", "fields": ["对白·旁白"], "all_of": ["<明确行动>"], "any_of": []}
    ],
    "ordered_requirement_ids": ["proof-action", "proof-result", "changed-outcome", "conversion-cta"]
  },
  "hook_acceptance_contract": {
    "selected": true,
    "hook_id": "<用户所选 Hook ID>",
    "hook_name": "<用户所选 Hook 名称>",
    "selection_source": "user_selected",
    "original_prompt": "<Hook 原始 Prompt，不要改写>",
    "opening_deadline_seconds": 3.0,
    "core_mechanism": "<触发—升级—结果的核心机制>",
    "product_binding": "<Hook 如何因果绑定当前商品>",
    "bridge_to_proof": "<Hook 最后一拍如何进入主证明>",
    "signature_requirements": [
      {
        "id": "hook-core-1",
        "source_text": "<对应的原始模板片段>",
        "kind": "composition",
        "critical": true,
        "opening_required": true,
        "deadline_seconds": 3.0,
        "evidence": {
          "fields": ["画面描述", "运镜"],
          "all_of": ["<必须逐个出现的证据>"],
          "any_of": ["<同强度可接受表达 A>", "<同强度可接受表达 B>"]
        }
      }
    ],
    "sequence_policy": "adaptable",
    "ordered_requirement_ids": [],
    "conflict_resolution": {
      "status": "compatible",
      "default_override_applied": false,
      "user_confirmation": ""
    }
  },
  "human_performance": {
    "required": true,
    "trigger_source": "<触发来源>",
    "observable_response": "<可观察反应>",
    "action_intent": "<动作意图>",
    "result_response": "<结果反应>",
    "emotion_labels_only": false
  },
  "spectacle_causality": {
    "required": false,
    "spectacle_mechanism": "",
    "product_relevant_force": "",
    "visible_effect_on_character_or_task": "",
    "counteraction_or_progression": "",
    "handoff_to_proof": ""
  },
  "content_budget": {
    "main_selling_points": 1,
    "supporting_selling_points": 1,
    "auxiliary_information_beats": 2,
    "active_selling_point_ids": ["SP1", "SP2"]
  },
  "product_entity_contract": {
    "instance_budget": 1,
    "multi_instance_authority": "none",
    "immutable_signature": ["<身份锚点1>", "<身份锚点2>"],
    "shot_entity_ledger": [
      {
        "shot": "S1",
        "instance_count": 1,
        "high_risk_interactions": [],
        "left_hand_job": "",
        "right_hand_job": "",
        "other_similar_objects": [],
        "occlusion_ratio": 0.0,
        "handoff_or_flip": false,
        "reanchor_after_occlusion": true
      }
    ]
  },
  "short_form_execution": {
    "first_event_at_seconds": 0.4,
    "product_in_real_task_at_seconds": 2.5,
    "effective_visual_beats": 6,
    "native_scores": [2, 2, 2, 2, 1, 2, 1, 2],
    "static_product_intro": false,
    "platform_execution_floor_preserved": true,
    "style_native_adapter": "<风格的平台原生适配说明>",
    "main_proof_seconds": 4.5,
    "scene_sequence": ["厨房", "厨房", "特写"],
    "causal_scene_revisits": [],
    "user_locked_circular_structure": false
  },
  "opening_hook_contract": {
    "hook_carrier": "spoken_line",
    "first_information_at_seconds": 0.4,
    "viewer_can_name_problem_or_desire_by_seconds": 0.9,
    "unframed_silence_seconds": 0.0,
    "silent_opening_authority": "none",
    "spoken_hook": "<口播 hook 原话>",
    "on_screen_hook": "",
    "visible_contrast_or_consequence": "",
    "distinctive_sound_and_causal_result": ""
  },
  "speech_rhythm_contract": {
    "language": "zh",
    "profile": "douyin_native",
    "target_rate": 6.0,
    "max_rate": 7.0,
    "line_budgets": [
      { "line": "L1", "rate": 6.0 }
    ]
  },
  "localization": {
    "target_market": "",
    "spoken_language": "",
    "character_reference_authority": "",
    "cast_localization": ""
  }
}
```

### 1.2 关键约束(填值时先看这些,避免必然报错)

- `current_sku_lock.object_state`:实体商品填 `physical`;数字/虚拟/品牌本身填 `digital`/`virtual`/`brand`/`数字/虚拟`/`品牌本身` —— 非实体时整个 `product_entity_contract` 可省略。
- `program_lock.selected_content_program` 必须与顶层 `selected_content_program` **逐字一致**。
- `program_lock.source_coverage` 三个子项 `exact_sku_form`/`duration_fit`/`evidence_basis` **都要为 `true`**。
- `program_lock.minimum_main_proof_seconds` **> 0**;`auxiliary_seconds` **≤ 1.2**;`ending_in_task` 必须 `true`。
- `hook_claims` 非空时必须给 `proof_answer_shot`。
- `adaptive_fusion`:六个状态字段(`product_specific_tension`/`opening_event`/`opening_state`/`product_causal_action`/`proof_state`/`end_state`)缺一即报错;`selected_modules` 里为 `true` 的模块必须在 `module_observable_effects` 里有对应非空效果;`style` 为 `true` 还需 `style_modulation`;`generic_template_skin_only` 必须 `false`。
- `persuasion_quality_contract` 七个子合同缺一不可。`brief_integrity` 的冲突/不可读关键素材/无依据高风险主张必须为空；`required_elements` 每项状态只能是 `covered` 或 `user_waived`。`product_exclusivity.replacement_test_passed` 必须为 `true`，且替换普通同类后至少有两个关键故事元素需要重写。`proof_chain` 必须写完整“顾虑/前态—商品动作—可观察变化—结果”，结果必须先于判断，且不得仅靠口播、包装文字、无依据反应或纯幻想特效。`functional_durable_goods_guard` 必须明确是否适用；适用时外观不得是唯一证明，并填写功能动作、用户任务结果与具体利益点。用户明确要求 N 个 SKU/款式时，`planned_distinct_variant_count` 必须不少于 N 且提供覆盖计划；不适用时必须给理由。人物主导时 `emotional_causality.required=true` 并填完整因果；不适用时必须给理由。`novelty_mechanism` 不得只是通用序列或表层换皮。转化任务必须由已见证证据连接到选择理由和明确行动；不适用时给理由。
- `quality_acceptance_contract` 至少包含 `product_action`、`observable_result`、`changed_outcome` 三类验收项；`conversion_closure.required=true` 时还必须包含 `cta`。功能耐用品门适用时还必须包含 `functional_action`、`user_task_result`、`user_benefit`；用户明确要求多个 SKU/款式时再增加 `sku_coverage`。每项必须有唯一 `id`、合法 `role`、至少一个故事脚本字段及可验收的 `all_of/any_of` 字面证据。`ordered_requirement_ids` 必须包含全部验收项，并保证商品动作早于可观察结果、可观察结果早于改变后的结局，CTA（如有）最后出现。
- `hook_acceptance_contract`: `selected_modules.hook=true` 时必填。`selection_source` 只能是 `user_selected`/`ui_default`/`agent_selected`——用户明确点选填 `user_selected`；第 3.0 步因用户完全没带 Hook 而由 `pippit_omni_search` 检索补齐的填 `agent_selected`，不得混填成 `user_selected`；`hook_id`/`hook_name`/`original_prompt`/`core_mechanism`/`product_binding`/`bridge_to_proof` 均不得为空；`opening_deadline_seconds` 必须在 0–3 秒。`signature_requirements` 至少一项，且至少一项同时 `critical=true` 与 `opening_required=true`；每项保留 `source_text`、脚本验收字段和字面证据。`all_of` 必须逐个出现；`any_of` 只允许同强度同机制的表达变体，不得填「分屏或普通展示」这类降级备选。
- `signature_requirements[].kind` 只能是 `composition`/`visible_action`/`sound_source`/`timing`/`sequence`/`state_change`/`spoken_line`。`sequence_policy=mechanism_order_required` 或 `user_locked` 时，`ordered_requirement_ids` 至少列 2 项且都已定义。`conflict_resolution.status=unresolved` 不通过；`selection_source=user_selected` 时 `default_override_applied` 必须为 `false`。
- `human_performance.required=true` 时,`trigger_source`/`observable_response`/`action_intent`/`result_response` 都要非空,`emotion_labels_only` 必须 `false`(不能只堆情绪标签)。
- `spectacle_causality.required=true` 时,五个字段(`spectacle_mechanism`/`product_relevant_force`/`visible_effect_on_character_or_task`/`counteraction_or_progression`/`handoff_to_proof`)都要非空;不用奇观时 `required=false` 其余留空即可。
- `content_budget`:`main_selling_points` **恒为 1**;`main+supporting` 不超过时长预算(见下表);`active_selling_point_ids` 若给,其长度必须等于 `main+supporting`;时长 ≤15s 时 `auxiliary_information_beats` **≤ 2**。
- **卖点数量随时长上限**:≤8s→1;≤20s→2;≤30s→3;≤45s→4;≤60s→5;更长→`max(5, (时长+14)//15)`。
- `product_entity_contract`(实体商品必填):`instance_budget ≥ 1`;`instance_budget > 1` 时 `multi_instance_authority` 不能是 `none`;`immutable_signature` **至少 2 个**身份锚点;`shot_entity_ledger` 非空。每个 shot:`instance_count` 不超预算;`>1` 需授权;`high_risk_interactions` 最多 1 项;有交互必须给 `left_hand_job` 或 `right_hand_job`;`other_similar_objects` 每项要有 `name` 和 `role`;`occlusion_ratio > 0.4` 或 `handoff_or_flip=true` 时必须 `reanchor_after_occlusion=true`。
- **短平台短视频专属门**(平台含"抖音"/"tiktok" 且 `0 < duration ≤ 20`):
  - `first_event_at_seconds` **≤ 0.5**;`product_in_real_task_at_seconds` **≤ 3.0**;`static_product_intro` 必须 `false`。
  - 时长 ≤15s 时 `effective_visual_beats` **在 5–8 之间**。
  - `native_scores` **恰好 8 个**,每个 0–2,不能有 0,且**总和 ≥ 12**。
  - `platform_execution_floor_preserved` 必须 `true`;`style_native_adapter` 非空。
  - `main_proof_seconds` **≥** `program_lock.minimum_main_proof_seconds`。
  - `scene_sequence` 回到旧场景时，该场景必须列入 `causal_scene_revisits`，表示回访会完成此前埋下的因果回报、主证明或关系改变；仅重复背景/定格/呼应不算。用户明确锁定完整环形结构时可用 `user_locked_circular_structure=true`。
  - `opening_hook_contract`(短平台必填):`hook_carrier` ∈ `spoken_line`/`on_screen_text`/`self_evident_visual`/`distinctive_sound`;`first_information_at_seconds` **≤ 0.5**;`viewer_can_name_problem_or_desire_by_seconds` **≤ 1.0**;`unframed_silence_seconds > 0.4` 时 `silent_opening_authority` 必须 ∈ `user_locked_asmr`/`user_locked_visual_hook`/`user_locked_sound_hook`;carrier 与其配套字段绑定(`spoken_line`→`spoken_hook`;`on_screen_text`→`on_screen_hook`;`self_evident_visual`→`visible_contrast_or_consequence`;`distinctive_sound`→`distinctive_sound_and_causal_result`)。
  - `speech_rhythm_contract`(短平台必填):中文(`language` ∈ `zh`/`中文`/`chinese`)且 `profile=douyin_native` 时 `target_rate` **在 5.5–6.5**;`max_rate` **≤ 7.2**;每条 `line_budgets[].rate` 不超过 `max_rate`。
- `localization`:目标市场泰国(`target_market` ∈ `thailand`/`泰国`,或 `spoken_language` ∈ `thai`/`泰语` 且平台含 tiktok)时,若 `character_reference_authority` 不是 `locked_by_user`,则 `cast_localization` 必须 ∈ `thai`/`thai_local`/`thailand_local`。

---

## 2. 第 4 步 · `validate_story_script.py`(故事脚本合同)

调用:`python3 scripts/validate_story_script.py <故事脚本.md> --contract <contract.json 或内联 JSON>`。**它直接扫实际的 `故事脚本.md` 文本**。`--contract` **支持文件路径与内联 JSON 两种写法(见第 0 节)**,例如 `--contract '{"duration_seconds": 15}'`;但**已选 Hook 或存在说服质量合同时不可省略**,且合同体积通常较大,这种情况建议走文件路径写法。

> 本校验器保留确定性结构检查，并新增**本次选中 Hook 的项目内验收**：只用 `hook_acceptance_contract` 中从原始 Hook 派生的字面证据、脚本字段和时间窗口，不使用全局关键词表。其他首镜创意强度、场景回访等泛化语义仍由契约正文保证。

### 2.1 `--contract` JSON 模版

```json
{
  "duration_seconds": 15,
  "hook_acceptance_contract": "<若选了 Hook，原样复制第 1 节同名对象；未选 Hook 可省略>",
  "quality_acceptance_contract": "<原样复制第 1 节同名对象；不可省略>"
}
```

`hook_acceptance_contract` 必须与第 3 步通过的对象逐字一致，不得为适应当前脚本而重写或删减。

`quality_acceptance_contract` 也必须与第 3 步通过的对象逐字一致。它只使用当前项目派生的具体动作、结果、结局与 CTA 字面证据，不使用全局关键词表；不得为了让现有脚本通过而把证据词改成空泛的“使用产品/效果明显/人物感动”。

### 2.2 校验器对 `故事脚本.md` 正文的硬性结构要求(全部为确定性检查)

- 全文有且仅有一个一级标题,且必须是 `# 故事脚本`。
- 有且仅有一个 **8 列表格**,表头逐字为:`镜号 | 时长 | 画面描述 | 景别 | 光影氛围 | 对白·旁白 | 音效 | 运镜`;表头下一行是分隔行;每个数据行必须 8 列。
- 有且仅有一行以 `**全片 BGM**` 开头。
- **除**标题、这一个表格、这一行 BGM 之外,不得有任何其它用户可见段落。
- **禁止泄漏内部标签**:正文不得出现 `Hook Scope`/`Bridge`/`Body takeover`、内部机制编号(形如 `BH04`/`S03`/`R01` 等两位数字编号)、内部字段名(`selected_content_program`/`program_lock`/`opening_hook_contract`)。
- 每个数据行时长可解析(形如 `3s`/`3秒`);给了 `duration_seconds` 时,全片时长之和与它差 **≤ 0.2**。
- **说服质量提示（warnings，不阻塞 `ok`）**：回看 `quality_acceptance_contract` 每项证据词是否出现在指定脚本字段、`ordered_requirement_ids` 顺序是否合理（一般商品动作早于可观察结果，结果早于人物判断/CTA），命中不了只提示、不判 `ok:false`。逐字命中属语义判断，收到提示时自查是漏写还是换了等价说法，别为迁就词表反复空转。

---

## 3. 第 6 步 · `validate_final_prompt.py`(最终方案合同)

调用:`python3 scripts/validate_final_prompt.py <视频生成Prompt.md> --contract <contract.json>`(`--contract` **必填**)。**它直接扫实际的 `视频生成Prompt.md` 文本**。

> 本校验器的硬门只有确定性结构、禁止项和自相矛盾检查（`errors`）。它另用同一份 `hook_acceptance_contract` 回看所选 Hook 是否在最终 Prompt 的开场窗和顺序中保留，但这属于 `warnings`(提示、不阻塞 `ok`)——不恢复全局关键词表或魔法措辞。

### 3.1 `--contract` JSON 模版

```json
{
  "forbidden_sku_terms": ["<禁止出现的错误型号/材质1>"],
  "unsupported_claim_terms": ["<无依据的夸大宣称词1>"],
  "forbidden_imports": ["<禁止串入的他程序元素1>"],
  "hook_acceptance_contract": "<若选了 Hook，原样复制第 1 节同名对象；未选 Hook 可省略>"
}
```

前三个字段是**禁止项列表**(可为空数组或省略)。`hook_acceptance_contract` 不是全局措辞清单，它只能原样继承当次用户选中 Hook 的项目内验收对象。

### 3.2 校验器对 `视频生成Prompt.md` 正文的硬性要求(全部为确定性检查)

- **时间轴结构门**:正文必须含**可解析的时间戳分镜节拍**(形如 `0-3s`/`3s-6秒`);解析不到就报错。
- **Hook 提示（warnings，不阻塞 `ok`）**:有 `hook_acceptance_contract` 时，回看每个身份性要求是否在指定开场窗内出现、需保序时是否与 `ordered_requirement_ids` 一致；命中不了只提示、不判 `ok:false`，自查是漏写还是换了等价说法。
- **禁止项缺席门**:`forbidden_sku_terms`、`unsupported_claim_terms`、`forbidden_imports` 里的词一个都不能出现。(注意:不再校验 `required_sku_terms`/身份锚点等"必须出现"项——那些改由你按契约正文自行保证。)
- **字幕冲突门**:不得同时出现"无字幕/不要字幕"与"花字/字幕出现/屏幕文字"。

---

## 4. 通用执行须知

1. **三个合同 JSON 都是内部文件**:建议写到 `video-projects/<项目目录>/_internal/` 下,不进任何用户可见产物,不在对话里贴出来。
2. **先写产物、再填合同、再校验**:合同 JSON 是对产物的断言;`故事脚本.md`/`视频生成Prompt.md` 的字段(如时长、首镜台词、SKU 术语)必须与合同值真实对应,不能为了过校验而在合同里瞎填。
3. **`errors` 即改产物,`warnings` 自查**:返回 `ok:false`/非零时,按 `errors` 定位**产物**哪里不达标,改产物(或必要时改合同以如实反映产物)再重跑,直到 `ok:true`,不得展示未过硬门的版本;`warnings` 不阻塞 `ok`,逐条判断漏写就补、等价说法就忽略,不为字面命中把好表达改生硬。
4. **字段值缺证据就别编**:凡涉及商品尺寸/材质/型号/卖点等关键事实,合同里要么填已确认的真值,要么把上游标 `unknown` 并回到第 2/5 步问用户——绝不为过校验而臆造。