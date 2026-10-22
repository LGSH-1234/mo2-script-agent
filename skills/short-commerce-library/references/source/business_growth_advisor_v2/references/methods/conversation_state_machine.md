
# 对话状态机

对话状态机用于帮助 agent 判断每一轮应该做什么：继续收集信息、对齐口径、诊断、出计划，还是转视频 brief。状态不一定要展示给用户，除非用户要求查看工作过程。

## 状态列表

| 状态 | 进入条件 | 下一步 |
|---|---|---|
| `intake` | 用户只给泛问题、零散描述或入口咨询 | 询问平台、对象、目标、资料类型 |
| `pain_point_entry` | 用户表达素材不转化、不知道拍什么、投流亏钱、ROI 掉、同行卷价格、门店客流少、产品专业但客户看不懂等具体痛点 | 归因到痛点入口，先给初步判断和 1-3 个素材/视频方向 |
| `profile_resolution` | 用户提供了足以识别项目、店铺、商家、账号或商品的信息，或即将开始诊断/计划/视频 brief | 解析并读取 `/workspace/growth_profiles/project_or_shop_or_merchant/xxx.md` |
| `profile_update` | 本轮产生了新事实、口径、计算、判断、计划摘要、视频机会或用户纠正 | 合并写回同一用户增长档案 |
| `metric_alignment` | 用户提供截图/表格/指标，但时间窗或口径不清 | 对齐平台、时间窗、指标含义、对象 |
| `metric_calculation` | 用户要求测算 ROI、CPA、利润、保本点，且字段和口径已足够 | 编写并运行程序计算，输出公式、结果和限制 |
| `diagnosis` | 已有足够事实支持初步判断 | 输出已知事实、初步判断、缺口 |
| `hypothesis` | 诊断指向多个可能原因 | 列假设、证据、验证方式 |
| `execution_planning` | 用户要方案或已有可行动结论 | 输出 Markdown 执行计划 |
| `video_opportunity` | 商品、卖点、素材、数据或参考足以判断视频机会 | 判断是否适合做视频，给方向 |
| `video_brief_handoff` | 已具备生成视频的最小信息 | 输出视频 brief，并交给当前 agent 可用视频能力 |

## 状态转移原则

- `intake` 不能无限追问。用户资料不足时，给“初步判断 + 最小补充清单”。
- `pain_point_entry` 优先于泛经营诊断。只要用户的痛点可归类，就先说明“你现在卡在哪里”，再决定是否进入数据口径、计划或视频 brief。
- `profile_resolution` 要尽早发生。只要能识别项目、店铺或商家，就先读取档案，避免重复询问已知信息。
- `profile_update` 要跟随事实变化发生。新资料、程序计算、诊断、计划和视频 brief 都应沉淀到同一档案；不同商家或无关项目不能混写。
- `metric_alignment` 的目标是避免误判，不是阻止行动。
- `metric_calculation` 必须用程序计算，不用心算或语言模型估算替代。
- `diagnosis` 必须标注证据强度。
- `hypothesis` 必须给验证方法，不能停在猜测。
- `execution_planning` 必须输出可执行 Markdown，不只聊天建议。
- `video_opportunity` 必须说明视频解决哪个经营问题。
- `video_brief_handoff` 不负责平台投放，只负责视频创作信息交接。

## 常见路径

### 泛问题到计划

```text
intake -> pain_point_entry -> profile_resolution -> metric_alignment -> metric_calculation -> diagnosis -> hypothesis -> execution_planning -> profile_update
```

### 数据截图到视频 brief

```text
profile_resolution -> metric_alignment -> metric_calculation -> diagnosis -> video_opportunity -> video_brief_handoff -> profile_update
```

### 用户明确要做视频

```text
intake -> pain_point_entry -> profile_resolution -> video_opportunity -> video_brief_handoff -> profile_update
```

如果商品、平台、人群、卖点或素材缺失，先补齐最小信息，不要直接生成泛视频。

## 最小补充问题

每次最多优先问 3-5 个关键问题：

- 这是哪个平台/地区的数据？
- 这组数据对应哪个商品、账号或素材？
- 时间窗是什么？
- 你当前最想优化成交、ROI、点击、播放还是起量？
- 你希望我先看素材为什么不转化、拆 3 条视频方向，还是整理完整执行计划？