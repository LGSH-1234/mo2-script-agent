
# 指标计算方法

当用户要求计算、复核或比较 ROI、ROAS、CPA、CAC、CPC、CPM、CTR、CVR、毛利、利润、保本 CPA 或保本 ROAS 时，必须遵守本文件。

## 最高优先级规则

1. 口径未确认前，不给最终计算结论。
2. 有截图或表格时，先把可见字段整理成结构化数据，再计算。
3. 计算必须通过程序完成。不要用心算、语言模型估算或直接口头推导替代程序计算。
4. 程序计算前必须做字段映射、缺失值检查、分母为零检查和时间窗检查。
5. 结果必须标注公式、字段来源、未纳入成本和置信度。
6. 不同平台、不同后台、不同时间窗、不同归因口径的数据不能直接混算。
7. 计算完成后必须把口径和程序计算结果写回用户增长档案的“指标计算记录”。

## 计算前确认清单

至少确认以下信息：

- 平台：TikTok Shop、抖音电商 / 巨量千川、小红书或其他。
- 经营对象：店铺、商品、SKU、素材、计划、达人、直播间、笔记或短视频。
- 时间窗：今天、近 7 天、近 30 天、单条素材、单个计划、单场直播等。
- 数据来源：截图、表格、后台名称、用户口述或可读取公开信息。
- 币种和单位：人民币、美元、千次曝光、百分比、小数。
- 成交口径：GMV、支付金额、成交金额、结算金额、净销售额是否一致。
- 转化口径：订单、支付订单、线索、加购、商品点击、表单提交、新客等。
- 归因窗口：当天、7 天、平台默认归因或用户自定义口径。
- 成本口径：广告消耗、货品成本、达人佣金、平台佣金、优惠券、物流、退款、售后成本是否纳入。

如果无法确认全部信息，可以先做“平台口径初算”，但必须写清楚缺口，不能把它称为真实利润或真实经营 ROI。

## 常用公式

### 广告和投放指标

```text
ROAS / 平台投产 = attributed_revenue / ad_spend
CPA = ad_spend / conversions
CPC = ad_spend / clicks
CPM = ad_spend / impressions * 1000
CTR = clicks / impressions
CVR = conversions / clicks
```

### 获客指标

```text
CAC = acquisition_spend / new_customers
CPL = lead_spend / leads
```

只有当转化数明确是“新客”时，才使用 CAC。若只是订单、支付或线索，应使用 CPA 或 CPL。

### 经营利润和保本指标

```text
gross_profit = revenue * gross_margin_rate
variable_cost = commission + coupons + logistics + fulfillment + refund_loss + other_variable_cost
contribution_profit_before_ads = gross_profit - variable_cost
net_profit_after_ads = contribution_profit_before_ads - ad_spend
break_even_cpa = contribution_profit_before_ads / conversions
break_even_roas = revenue / contribution_profit_before_ads
```

如果已知的是单均口径，也可以使用：

```text
contribution_profit_per_order = average_order_value * gross_margin_rate - variable_cost_per_order
break_even_cpa = contribution_profit_per_order
break_even_roas = average_order_value / contribution_profit_per_order
```

当 `contribution_profit_before_ads <= 0` 或 `contribution_profit_per_order <= 0` 时，不应给出正向保本 ROAS；应提示该口径下广告前贡献利润已经不成立，需要先检查价格、毛利或成本。

## 程序化计算流程

1. 从用户材料中抽取字段，形成表格或列表。
2. 明确字段映射，例如 `ad_spend` 来自“消耗”，`attributed_revenue` 来自“成交金额”。
3. 编写小程序计算指标。
4. 运行程序，得到结果。
5. 解释结果，指出口径限制和下一步动作。
6. 写回 `/workspace/growth_profiles/project_or_shop_or_merchant/xxx.md`，记录计算对象、时间窗、指标、公式、字段来源、程序结果、未纳入成本和置信度。

程序可以是 Python、JavaScript 或当前 agent 环境可运行的其他语言。优先使用简单、可读、可复核的代码。

示例结构：

```python
rows = [
    {
        "name": "素材 A",
        "ad_spend": 1200.0,
        "attributed_revenue": 3600.0,
        "impressions": 80000,
        "clicks": 1600,
        "conversions": 48,
    }
]

def safe_div(numerator, denominator):
    if denominator in (0, None):
        return None
    return numerator / denominator

for row in rows:
    row["roas"] = safe_div(row["attributed_revenue"], row["ad_spend"])
    row["cpa"] = safe_div(row["ad_spend"], row["conversions"])
    row["ctr"] = safe_div(row["clicks"], row["impressions"])
    row["cvr"] = safe_div(row["conversions"], row["clicks"])

print(rows)
```

不要为了显得完整而隐藏代码逻辑。给用户输出时可以不展示全部代码，但必须说明“已用程序计算”，并列出公式、字段和结果。

## 截图场景

如果用户只上传截图：

- 先提取截图中能看清的字段。
- 对模糊字段标注“不确定”，不要自行补值。
- 把已识别字段整理成结构化数据，再用程序算。
- 若关键字段缺失，例如只有 ROI 没有消耗和成交金额，则只能复述平台给出的 ROI，不能反推出完整经营结果。

## 表格场景

如果用户上传 CSV、XLSX 或表格文本：

- 先识别每列含义、单位和每行粒度。
- 若同一列可能有不同口径，例如“成交”可能是订单数或成交金额，先问清楚。
- 多表合并前必须确认主键，例如日期、计划 ID、素材 ID、商品 ID、达人 ID。
- 计算后优先输出排序和异常，例如最高 CPA、最低 ROAS、CTR 高但 CVR 低的对象。

## 输出模板

```markdown
## 指标测算

### 1. 本次口径
- 平台：
- 对象：
- 时间窗：
- 数据来源：
- 成交口径：
- 转化口径：
- 成本口径：

### 2. 计算公式
- ROAS =
- CPA =
- CTR =
- CVR =

### 3. 程序计算结果
| 对象 | 消耗 | 成交金额 | 转化数 | ROAS | CPA | CTR | CVR |
|---|---:|---:|---:|---:|---:|---:|---:|

### 4. 结论
- ...

### 5. 未纳入口径 / 风险
- ...

### 6. 下一步
- ...
```

## 档案记录模板

计算完成后，在用户增长档案中追加或更新一行：

```markdown
## 6. 指标计算记录
| 计算对象 | 时间窗 | 指标 | 公式 | 字段来源 | 程序计算结果 | 未纳入成本 | 置信度 |
|---|---|---|---|---|---|---|---|
| [商品/素材/计划/店铺] | [时间窗] | [ROI/CPA/利润/保本点] | [公式] | [截图/表格/用户描述] | [程序输出结果] | [退款/佣金/优惠/物流等缺口] | [高/中/低] |
```

不要只在聊天中给出测算结果而不沉淀到档案。后续诊断、执行计划和视频 brief 应复用这条计算记录。

## 不确定性表达

- “这是平台投放口径 ROAS，不等于真实利润。”
- “当前 CPA 的转化定义是订单，不是新客，因此不称为 CAC。”
- “截图里没有退款、佣金和优惠信息，所以暂不能判断真实经营 ROI。”
- “这次计算的时间窗是近 7 天，不能直接外推到月度利润。”
- “不同后台字段可能存在归因差异，本次只按用户提供字段计算。”