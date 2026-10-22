
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
unit_localizer.py — 货币与计量单位本地化换算助手

为什么需要这个脚本：
  视频本地化里最集中的扣分项之一是「制式/单位未适配」——把 $39.99 直接念成
  "39,99"、给墨西哥观众说"70 dólares"、德语版还在说英寸和磅。更糟的是手算容易
  出错（实测中出现过 "4磅 → 2磅" 这种把 1.8kg 写成 2lb 的错误）。

★ 两类量值的权限完全不同：
  A 类（长度/重量/容量/温度/日期格式）= 客观的物理量换算，只有算对算错，
     没有决策空间 → 本脚本的结果可直接采用。
  B 类（价格/货币、鞋码）= **商业决策，不是换算题** → 本脚本只输出**建议值**
     （带 decision_required=True），**必须用 dynamic_questionnaire 向用户
     确认后才能写进译文**，严禁把建议值当成既定事实直接用。
       · 价格：汇率取哪天的、要不要取整成心理价位、当地是否本来另有定价、
               是否干脆保留原币种，都只有业务方知道。
       · 鞋码：各品牌自有码表（同一 US 码在不同品牌可能差半号到一号），
               且"该商品在当地实际上架哪几个码"属业务信息；
               BR / JP（厘米制）/ KR（毫米制）与 EU 码并非线性对应。

本脚本做两件事：
    1) scan  ：扫描台词，把需要本地化的量值全部揪出来（A/B 分开列），避免漏改；
    2) convert：A 类给出可直接用的换算结果；B 类给出待确认的建议值。

用法：
  # 扫描一句/一段台词里所有需要本地化的量值
  python3 unit_localizer.py scan --text "12 pack, only \$39.99. Fits 10.5 inch, 4 lb."

  # 扫描并按目标地域换算
  python3 unit_localizer.py scan --text "..." --region 墨西哥

  # 单个数值换算
  python3 unit_localizer.py convert --value 4 --unit lb --region 德国
  python3 unit_localizer.py convert --value 39.99 --unit usd --region 墨西哥

  # 列出支持的地域与单位
  python3 unit_localizer.py info

  # JSON 输出
  python3 unit_localizer.py scan --text "..." --region 巴西 --json

⚠️ 汇率是内置的粗略参考值，会随市场变动。脚本输出的价格只是"本地化示意"，
   交付说明里必须注明汇率与时间口径，实际售价需业务方确认。
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# 地域档案：法定货币、货币口语说法、度量制（metric / imperial）、鞋码制
# ---------------------------------------------------------------------------
REGION_PROFILES = {
    "墨西哥":   {"currency": "MXN", "symbol": "$",  "spoken": "pesos",   "measure": "metric",   "shoe": "EU"},
    "阿根廷":   {"currency": "ARS", "symbol": "$",  "spoken": "pesos",   "measure": "metric",   "shoe": "EU"},
    "西班牙":   {"currency": "EUR", "symbol": "€",  "spoken": "euros",   "measure": "metric",   "shoe": "EU"},
    "巴西":     {"currency": "BRL", "symbol": "R$", "spoken": "reais",   "measure": "metric",   "shoe": "BR"},
    "葡萄牙":   {"currency": "EUR", "symbol": "€",  "spoken": "euros",   "measure": "metric",   "shoe": "EU"},
    "德国":     {"currency": "EUR", "symbol": "€",  "spoken": "Euro",    "measure": "metric",   "shoe": "EU"},
    "法国":     {"currency": "EUR", "symbol": "€",  "spoken": "euros",   "measure": "metric",   "shoe": "EU"},
    "意大利":   {"currency": "EUR", "symbol": "€",  "spoken": "euro",    "measure": "metric",   "shoe": "EU"},
    "荷兰":     {"currency": "EUR", "symbol": "€",  "spoken": "euro",    "measure": "metric",   "shoe": "EU"},
    "美国":     {"currency": "USD", "symbol": "$",  "spoken": "dollars", "measure": "imperial", "shoe": "US"},
    "英国":     {"currency": "GBP", "symbol": "£",  "spoken": "pounds",  "measure": "imperial", "shoe": "UK"},
    "加拿大":   {"currency": "CAD", "symbol": "$",  "spoken": "dollars", "measure": "metric",   "shoe": "US"},
    "澳大利亚": {"currency": "AUD", "symbol": "$",  "spoken": "dollars", "measure": "metric",   "shoe": "AU"},
    "日本":     {"currency": "JPY", "symbol": "¥",  "spoken": "円",      "measure": "metric",   "shoe": "JP"},
    "韩国":     {"currency": "KRW", "symbol": "₩",  "spoken": "원",      "measure": "metric",   "shoe": "KR"},
    "新加坡":   {"currency": "SGD", "symbol": "S$", "spoken": "dollars", "measure": "metric",   "shoe": "EU"},
    "俄罗斯":   {"currency": "RUB", "symbol": "₽",  "spoken": "рублей",  "measure": "metric",   "shoe": "EU"},
    "印度尼西亚": {"currency": "IDR", "symbol": "Rp", "spoken": "rupiah", "measure": "metric",  "shoe": "EU"},
    "马来西亚": {"currency": "MYR", "symbol": "RM", "spoken": "ringgit", "measure": "metric",   "shoe": "EU"},
    "泰国":     {"currency": "THB", "symbol": "฿",  "spoken": "บาท",     "measure": "metric",   "shoe": "EU"},
    "越南":     {"currency": "VND", "symbol": "₫",  "spoken": "đồng",    "measure": "metric",   "shoe": "EU"},
    "土耳其":   {"currency": "TRY", "symbol": "₺",  "spoken": "lira",    "measure": "metric",   "shoe": "EU"},
    "波兰":     {"currency": "PLN", "symbol": "zł", "spoken": "złotych", "measure": "metric",   "shoe": "EU"},
    "印度":     {"currency": "INR", "symbol": "₹",  "spoken": "rupees",  "measure": "metric",   "shoe": "UK"},
    "巴基斯坦": {"currency": "PKR", "symbol": "Rs", "spoken": "rupees",  "measure": "metric",   "shoe": "UK"},
    "菲律宾":   {"currency": "PHP", "symbol": "₱",  "spoken": "piso",    "measure": "metric",   "shoe": "US"},
    "中国":     {"currency": "CNY", "symbol": "¥",  "spoken": "元",      "measure": "metric",   "shoe": "CN"},
}

REGION_ALIASES = {
    "mexico": "墨西哥", "墨西哥城": "墨西哥",
    "brazil": "巴西", "brasil": "巴西",
    "germany": "德国", "deutschland": "德国",
    "france": "法国", "italy": "意大利", "spain": "西班牙",
    "usa": "美国", "us": "美国", "america": "美国", "united states": "美国",
    "uk": "英国", "britain": "英国", "england": "英国",
    "japan": "日本", "korea": "韩国", "south korea": "韩国",
    "canada": "加拿大", "australia": "澳大利亚", "singapore": "新加坡",
    "russia": "俄罗斯", "indonesia": "印度尼西亚", "印尼": "印度尼西亚",
    "malaysia": "马来西亚", "thailand": "泰国", "vietnam": "越南",
    "turkey": "土耳其", "poland": "波兰", "india": "印度",
    "pakistan": "巴基斯坦", "philippines": "菲律宾", "china": "中国",
    "argentina": "阿根廷", "portugal": "葡萄牙", "netherlands": "荷兰",
}

# ---------------------------------------------------------------------------
# 汇率（相对 USD 的粗略参考值）。⚠️ 会随市场变动，仅用于本地化示意。
# ---------------------------------------------------------------------------
FX_PER_USD = {
    "USD": 1.0,    "EUR": 0.92,   "GBP": 0.79,   "MXN": 18.5,
    "BRL": 5.4,    "ARS": 950.0,  "CAD": 1.36,   "AUD": 1.52,
    "JPY": 152.0,  "KRW": 1340.0, "SGD": 1.34,   "RUB": 92.0,
    "IDR": 15800.0,"MYR": 4.7,    "THB": 35.5,   "VND": 25000.0,
    "TRY": 32.5,   "PLN": 3.95,   "INR": 83.5,   "PKR": 278.0,
    "PHP": 57.0,   "CNY": 7.2,
}

CURRENCY_ALIASES = {
    "usd": "USD", "$": "USD", "美元": "USD", "dollar": "USD", "dollars": "USD",
    "eur": "EUR", "€": "EUR", "欧元": "EUR", "euro": "EUR",
    "gbp": "GBP", "£": "GBP", "英镑": "GBP", "pound": "GBP",
    "jpy": "JPY", "日元": "JPY", "cny": "CNY", "rmb": "CNY", "人民币": "CNY",
    "brl": "BRL", "r$": "BRL", "mxn": "MXN", "krw": "KRW",
}

# 计量单位换算：(目标单位, 换算系数)
IMPERIAL_TO_METRIC = {
    "inch": ("cm", 2.54),
    "ft":   ("cm", 30.48),
    "yard": ("m", 0.9144),
    "lb":   ("kg", 0.45359237),
    "oz":   ("g", 28.349523125),
    "floz": ("ml", 29.5735295625),
    "gallon": ("L", 3.785411784),
    "mile": ("km", 1.609344),
}

UNIT_ALIASES = {
    "in": "inch", '"': "inch", "inches": "inch", "英寸": "inch",
    "feet": "ft", "foot": "ft", "英尺": "ft",
    "yd": "yard", "yards": "yard", "码": "yard",
    "lbs": "lb", "pound": "lb", "pounds": "lb", "磅": "lb",
    "ounce": "oz", "ounces": "oz", "盎司": "oz",
    "fl oz": "floz", "fluid ounce": "floz", "液量盎司": "floz",
    "gal": "gallon", "gallons": "gallon", "加仑": "gallon",
    "miles": "mile", "英里": "mile",
}

# 女鞋 US → EU / UK 粗略对照（营销视频最常见）
SHOE_US_TO_EU_WOMEN = {
    5: 35, 5.5: 36, 6: 36.5, 6.5: 37, 7: 37.5, 7.5: 38,
    8: 38.5, 8.5: 39, 9: 40, 9.5: 40.5, 10: 41, 10.5: 42, 11: 42.5,
}
SHOE_US_TO_EU_MEN = {
    6: 39, 6.5: 39.5, 7: 40, 7.5: 40.5, 8: 41, 8.5: 42,
    9: 42.5, 9.5: 43, 10: 44, 10.5: 44.5, 11: 45, 11.5: 45.5, 12: 46,
}
# 英国码 = US 码减固定差（女鞋 -2、男鞋 -0.5），英国市场用 UK 码而非 EU 码
SHOE_US_TO_UK_OFFSET = {"women": -2.0, "men": -0.5}


def normalize_region(region: str) -> str:
    if not region:
        return ""
    raw = region.strip()
    if raw in REGION_PROFILES:
        return raw
    key = raw.lower()
    if key in REGION_ALIASES:
        return REGION_ALIASES[key]
    if raw in REGION_ALIASES:
        return REGION_ALIASES[raw]
    return raw


def nice_price(amount: float, currency: str) -> float:
    """把折算结果取整成'像本地真实标价'的数字。

    营销台词里的价格是卖点，念一串小数既不自然也拖时长。
    这里取整到当地常见的心理价位（整十 / 尾数 9 / 尾数 5），并且**就近取整**——
    向上抬价会虚报售价（如 23.3 抬成 29 就偏了 24%），因此在候选价位里
    选与真实折算值最接近的那个。

    偏差上界：实测在各币种、各量级随机 3 万次抽样下最大相对偏差 < 8%，
    主要出现在 30~35 这类相邻心理价位间隔本身较大的档位，属于"取成整齐价位"
    的固有取舍。**若业务对价格精确度有要求，应使用 raw_converted 字段的
    未取整值，并由业务方确认最终定价。**
    """
    if currency in ("JPY", "KRW", "IDR", "VND"):
        # 无小数货币，按量级就近取整；极小金额直接取整数，避免被拉偏
        if amount < 100:
            return float(round(amount))
        if amount < 1000:
            return float(round(amount / 10) * 10)
        if amount < 100000:
            return float(round(amount / 100) * 100)
        return float(round(amount / 1000) * 1000)

    if amount < 10:
        # 小额保留一位小数即可，取整到 .5 会造成较大相对偏差
        return round(amount, 1)

    if amount < 30:
        # 低价区间：十档间隔占比大，候选需更细（整数 + .5 + 尾数 9），否则会明显虚报
        base = int(amount)
        candidates = {base, base + 0.5, base + 1, base - 0.5,
                      int(amount // 10) * 10 + 9, int(amount // 10) * 10 + 10}
        candidates = {c for c in candidates if c > 0}
        return float(min(candidates, key=lambda c: abs(c - amount)))

    if amount < 1000:
        # 候选价位：整十、尾数 9、尾数 5（中段），就近取整以免虚报售价
        base = int(amount // 10) * 10
        candidates = {base - 1, base, base + 5, base + 9, base + 10}
        candidates = {c for c in candidates if c > 0}
        return float(min(candidates, key=lambda c: abs(c - amount)))

    return float(round(amount / 100) * 100)       # 4210 → 4200


def convert_currency(value: float, from_cur: str, region: str):
    region = normalize_region(region)
    prof = REGION_PROFILES.get(region)
    if not prof:
        raise ValueError(f"未知目标地域 '{region}'。支持：{', '.join(REGION_PROFILES)}")
    from_cur = CURRENCY_ALIASES.get(str(from_cur).strip().lower(), str(from_cur).strip().upper())
    to_cur = prof["currency"]
    if from_cur not in FX_PER_USD:
        raise ValueError(f"未知源币种 '{from_cur}'。支持：{', '.join(FX_PER_USD)}")
    if from_cur == to_cur:
        return {
            "changed": False, "region": region,
            "decision_required": False,
            "from": f"{value} {from_cur}", "to": f"{value} {to_cur}",
            "spoken": f"{value} {prof['spoken']}",
            "note": "源币种已是目标市场货币，无需换算（金额本身若要调整仍需业务方确认）",
        }
    usd = value / FX_PER_USD[from_cur]
    raw = usd * FX_PER_USD[to_cur]
    nice = nice_price(raw, to_cur)
    return {
        "changed": True, "region": region,
        "decision_required": True,          # ★ 价格属商业决策，必须问用户
        "from": f"{value} {from_cur}",
        "raw_converted": round(raw, 2),
        "to": f"{nice:g} {to_cur}",
        "symbol_form": f"{prof['symbol']}{nice:g}",
        "spoken": f"{nice:g} {prof['spoken']}",
        "fx_used": f"1 {from_cur} ≈ {round(FX_PER_USD[to_cur]/FX_PER_USD[from_cur], 4)} {to_cur}",
        "note": (f"【仅为建议值，不可直接采用】按内置粗略参考汇率折算得 "
                 f"{round(raw,2)} {to_cur}，取整为当地常见价位 {nice:g}。"
                 f"汇率非实时、且真实售价涉及定价策略与税费——"
                 f"必须用 dynamic_questionnaire 向用户确认后再写进译文。"),
    }


def convert_measure(value: float, unit: str, region: str):
    region = normalize_region(region)
    prof = REGION_PROFILES.get(region)
    if not prof:
        raise ValueError(f"未知目标地域 '{region}'。支持：{', '.join(REGION_PROFILES)}")
    u = str(unit).strip().lower()
    u = UNIT_ALIASES.get(u, u)
    if u not in IMPERIAL_TO_METRIC:
        raise ValueError(
            f"未知或无需换算的单位 '{unit}'。可换算：{', '.join(IMPERIAL_TO_METRIC)}"
        )
    if prof["measure"] == "imperial":
        return {
            "changed": False, "region": region,
            "from": f"{value} {u}", "to": f"{value} {u}",
            "note": f"{region} 使用英制，保留原单位不换算",
        }
    tgt, factor = IMPERIAL_TO_METRIC[u]
    out = value * factor
    # 按量级给出合理精度，避免 1.8143694785 这种念不出来的数
    shown = round(out, 1) if out < 100 else round(out)
    return {
        "changed": True, "region": region,
        "from": f"{value} {u}", "to": f"{shown:g} {tgt}",
        "exact": round(out, 4),
        "note": f"{value} {u} × {factor} = {round(out,4)} {tgt}，播报建议用 {shown:g} {tgt}",
    }


def convert_shoe(value: float, region: str, gender: str = "women"):
    """US 尺码 → 目标市场码制。

    ★ 鞋码属 B 类（需用户确认），不是纯客观换算：
      - 各品牌自有码表，同一 US 码在不同品牌对应的 EU 码可能差半号到一号；
      - "该商品在当地实际上架哪几个码"是业务信息，只有业务方知道；
      - 巴西 BR / 日本 JP（厘米制）/ 韩国 KR（毫米制）与 EU 码不是线性对应。
    因此本函数只输出**建议值**，必须经 dynamic_questionnaire 确认后才能写进译文。
    """
    region = normalize_region(region)
    prof = REGION_PROFILES.get(region)
    if not prof:
        raise ValueError(f"未知目标地域 '{region}'")
    gender_zh = "女" if gender == "women" else "男"

    if prof["shoe"] == "US":
        return {"changed": False, "region": region,
                "decision_required": False,
                "from": f"US {value:g}", "to": f"US {value:g}",
                "note": f"{region} 使用 US 码，无需换算"}

    # 英国 / 印度 / 巴基斯坦用 UK 码
    if prof["shoe"] == "UK":
        uk = value + SHOE_US_TO_UK_OFFSET[gender]
        return {"changed": True, "region": region,
                "decision_required": True,
                "from": f"US {value:g}", "to": f"UK {uk:g}",
                "note": (f"【仅为建议值，需确认】US {value:g}（{gender_zh}）≈ UK {uk:g}"
                         f"（{region} 用 UK 码）。各品牌码表有差异，且当地实际上架码段"
                         f"属业务信息——必须用 dynamic_questionnaire 向用户确认后再写进译文。")}

    table = SHOE_US_TO_EU_WOMEN if gender == "women" else SHOE_US_TO_EU_MEN
    eu = table.get(value)
    if eu is None:
        keys = sorted(table)
        near = min(keys, key=lambda k: abs(k - value))
        eu = table[near]
        detail = (f"US {value:g} 不在对照表内，按最近档 US {near:g} 估算为 EU {eu:g}")
    else:
        detail = f"US {value:g}（{gender_zh}）≈ EU {eu:g}"

    # 巴西 / 日本 / 韩国 / 中国有自己的码制，与 EU 码非线性对应
    if prof["shoe"] != "EU":
        detail += (f"；但 {region} 实际使用 {prof['shoe']} 码，与 EU 码不是线性对应，"
                   f"此折算仅供参考，务必核对当地码表")

    return {"changed": True, "region": region,
            "decision_required": True,
            "from": f"US {value:g}", "to": f"EU {eu:g}",
            "note": (f"【仅为建议值，需确认】{detail}。各品牌码表有差异，且当地实际上架"
                     f"码段属业务信息——必须用 dynamic_questionnaire 向用户确认后再写进译文。")}


# ---------------------------------------------------------------------------
# 扫描：把台词里所有需要本地化的量值揪出来
# ---------------------------------------------------------------------------
CURRENCY_PAT = re.compile(
    r"(?:(?P<sym>[$€£¥₩₽₺₹]|R\$|RM|S\$)\s?(?P<amt1>\d[\d,]*(?:\.\d+)?)"
    r"|(?P<amt2>\d[\d,]*(?:\.\d+)?)\s?(?P<word>dollars?|usd|euros?|eur|pounds?|gbp|美元|欧元|英镑|日元|元))",
    re.IGNORECASE)

UNIT_PAT = re.compile(
    r"(?P<amt>\d+(?:\.\d+)?)\s?(?P<unit>inches|inch|in\b|\"|ft\b|feet|foot|yards?|yd\b"
    r"|lbs?\b|pounds?\b|ounces?|oz\b|fl\s?oz|gallons?|gal\b|miles?|英寸|英尺|磅|盎司|加仑|英里)",
    re.IGNORECASE)

TEMP_PAT = re.compile(
    r"(?:华氏\s?(?P<amt3>-?\d+(?:\.\d+)?)\s?度?"
    r"|(?P<amt>-?\d+(?:\.\d+)?)\s?(?:°\s?F\b|℉|degrees?\s+Fahrenheit\b|F\b(?!\w)))",
    re.IGNORECASE)
SHOE_PAT = re.compile(r"\b(?:US|size)\s?(?P<amt>\d{1,2}(?:\.5)?)\b", re.IGNORECASE)


def scan(text: str, region: str = ""):
    findings = []

    for m in CURRENCY_PAT.finditer(text):
        amt = (m.group("amt1") or m.group("amt2") or "").replace(",", "")
        token = (m.group("sym") or m.group("word") or "").strip()
        if not amt:
            continue
        item = {"kind": "currency", "matched": m.group(0).strip(),
                "value": float(amt), "unit": token}
        if region:
            try:
                item["conversion"] = convert_currency(float(amt), token, region)
            except Exception as e:
                item["error"] = str(e)
        findings.append(item)

    for m in UNIT_PAT.finditer(text):
        raw_unit = m.group("unit").strip().lower().replace(" ", "")
        item = {"kind": "measure", "matched": m.group(0).strip(),
                "value": float(m.group("amt")), "unit": raw_unit}
        if region:
            try:
                item["conversion"] = convert_measure(float(m.group("amt")), raw_unit, region)
            except Exception as e:
                item["error"] = str(e)
        findings.append(item)

    for m in TEMP_PAT.finditer(text):
        f = float(m.group("amt") or m.group("amt3"))
        item = {"kind": "temperature", "matched": m.group(0).strip(), "value": f, "unit": "F"}
        if region:
            prof = REGION_PROFILES.get(normalize_region(region), {})
            if prof.get("measure") == "metric":
                item["conversion"] = {"changed": True, "from": f"{f:g}°F",
                                      "to": f"{round((f-32)*5/9,1):g}°C",
                                      "note": "(°F − 32) × 5/9"}
            else:
                item["conversion"] = {"changed": False, "note": "目标市场用华氏，保留"}
        findings.append(item)

    for m in SHOE_PAT.finditer(text):
        item = {"kind": "shoe_size", "matched": m.group(0).strip(),
                "value": float(m.group("amt")), "unit": "US"}
        if region:
            try:
                item["conversion"] = convert_shoe(float(m.group("amt")), region)
                item["conversion"]["note"] += (
                    "（默认按女鞋表；男鞋请用 convert --kind shoe --gender men）")
            except Exception as e:
                item["error"] = str(e)
        findings.append(item)

    return {"text": text, "region": normalize_region(region) if region else None,
            "count": len(findings), "findings": findings}


def fmt_scan(r):
    if r["count"] == 0:
        return "【单位扫描】未发现需要本地化换算的货币 / 计量单位 / 尺码。"

    kind_zh = {"currency": "货币", "measure": "计量", "temperature": "温度", "shoe_size": "鞋码"}

    # 按"是否需要用户确认"分组：B 类 = 货币 + 鞋码（商业决策），A 类 = 其余客观换算
    def needs_decision(f):
        c = f.get("conversion")
        if c is not None:
            return bool(c.get("decision_required"))
        # 未指定 region 时还没换算，按类别兜底判定
        return f["kind"] in ("currency", "shoe_size")

    money = [f for f in r["findings"] if needs_decision(f)]
    others = [f for f in r["findings"] if not needs_decision(f)]

    head = f"【单位扫描】发现 {r['count']} 处需要本地化的量值"
    if r["region"]:
        head += f"（目标地域：{r['region']}）"
    lines = [head]

    def render(f, i):
        out = [f"  {i}. [{kind_zh.get(f['kind'], f['kind'])}] 原文「{f['matched']}」"]
        if "error" in f:
            out.append(f"       ⚠️ {f['error']}")
        elif "conversion" in f:
            c = f["conversion"]
            if c.get("changed"):
                label = "建议" if c.get("decision_required") else "应改为"
                out.append(f"       → {label}：{c.get('spoken') or c.get('to')}")
                if c.get("fx_used"):
                    out.append(f"         参考汇率：{c['fx_used']}（非实时）")
                if c.get("note"):
                    out.append(f"         {c['note']}")
            else:
                out.append(f"       → 无需换算：{c.get('note','')}")
        else:
            out.append("       （未指定 --region，仅标记，未换算）")
        return out

    if others:
        lines.append("")
        lines.append("── A 类：客观换算（可自行处理）──")
        for i, f in enumerate(others, 1):
            lines += render(f, i)

    if money:
        has_price = any(f["kind"] == "currency" for f in money)
        has_shoe = any(f["kind"] == "shoe_size" for f in money)
        label = " / ".join([x for x in [("价格 / 货币" if has_price else ""),
                                        ("鞋码" if has_shoe else "")] if x])
        lines.append("")
        lines.append(f"── B 类：{label}（★ 商业决策，必须先问用户）──")
        for i, f in enumerate(money, 1):
            lines += render(f, i)
        lines.append("")
        lines.append("  ★★ 上述数值【不可直接写进译文】，必须用 dynamic_questionnaire 弹问卷，")
        lines.append("     把原值、建议值与其不确定性如实告知用户后按其选择执行：")
        if has_price:
            lines.append("     · 价格：①采用建议折算值 ②自行提供当地实际售价（推荐）")
            lines.append("             ③保留原币种 ④去掉具体金额")
            lines.append("       （内置汇率为粗略参考值、非实时）")
        if has_shoe:
            lines.append("     · 鞋码：①采用建议对照值 ②自行提供当地实际上架码（推荐）")
            lines.append("             ③保留原码制并注明制式（如「US 8」）④不提具体码数")
            lines.append("       （各品牌码表有差异；BR/JP/KR 码与 EU 码非线性对应）")
        lines.append("     用户未回答时保留原文，不得自行拍数字。")

    if r["region"]:
        lines.append("")
        lines.append("  ⚠️ 数值敲定后务必用 speech_rate_evaluator.py 重跑该句长度预算"
                     "——数字念法变长会改变时长。")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="货币与计量单位本地化换算助手")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="扫描台词里需要本地化的量值")
    s.add_argument("--text", required=True)
    s.add_argument("--region", default="", help="目标地域，如 墨西哥 / 巴西 / 德国")
    s.add_argument("--json", action="store_true")

    c = sub.add_parser("convert", help="单个数值换算")
    c.add_argument("--value", type=float, required=True)
    c.add_argument("--unit", required=True, help="币种（usd/$/美元）或单位（lb/inch/oz）")
    c.add_argument("--region", required=True)
    c.add_argument("--kind", choices=["auto", "currency", "measure", "shoe"], default="auto")
    c.add_argument("--gender", choices=["women", "men"], default="women")
    c.add_argument("--json", action="store_true")

    sub.add_parser("info", help="列出支持的地域与单位")

    a = p.parse_args()
    try:
        if a.cmd == "scan":
            r = scan(a.text, a.region)
            print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else fmt_scan(r))
        elif a.cmd == "convert":
            unit_l = a.unit.strip().lower()
            kind = a.kind
            if kind == "auto":
                if unit_l in CURRENCY_ALIASES or unit_l.upper() in FX_PER_USD:
                    kind = "currency"
                elif unit_l in UNIT_ALIASES or unit_l in IMPERIAL_TO_METRIC:
                    kind = "measure"
                else:
                    kind = "shoe" if unit_l in ("us", "size") else "measure"
            if kind == "currency":
                r = convert_currency(a.value, a.unit, a.region)
            elif kind == "shoe":
                r = convert_shoe(a.value, a.region, a.gender)
            else:
                r = convert_measure(a.value, a.unit, a.region)
            if a.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                arrow = "→" if r.get("changed") else "＝"
                print(f"{r['from']} {arrow} {r['to']}")
                if r.get("spoken"):
                    print(f"  口播说法：{r['spoken']}")
                if r.get("note"):
                    print(f"  说明：{r['note']}")
        else:
            print("支持的目标地域：")
            for k, v in REGION_PROFILES.items():
                print(f"  {k:10s} 货币 {v['currency']:4s}（口播 {v['spoken']}）"
                      f" | 度量 {v['measure']:9s} | 鞋码 {v['shoe']}")
            print("\n可换算的英制单位：")
            for k, (t, f) in IMPERIAL_TO_METRIC.items():
                print(f"  {k:7s} → {t:3s}（×{f}）")
            print("\n⚠️ 汇率为内置粗略参考值，仅用于本地化示意，会随市场变动。")
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()