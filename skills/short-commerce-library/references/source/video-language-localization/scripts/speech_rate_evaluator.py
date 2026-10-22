
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
speech_rate_evaluator.py — 语速评估 + 目标语言译文长度预算

本地化视频配音时最常见的两个失败点：
  1) 译文太长 → 角色"说不完"，或语速被迫拉快、听感突兀；
  2) 译文太短 → 出现长时间停顿，画面和口型对不上。

本脚本用两步来规避这两个问题：

  第一步 evaluate：以"标准中文语速"为基准，判断原片这句台词的说话人
                    是 慢 / 正常 / 快。评判依据是「有效字数 ÷ 时长」。

  第二步 budget：  根据 原时长 + 上一步得到的语速档位 + 目标语言的
                    正常发音速率，给出目标语言译文的"长度预算区间"
                    （英语按词数、日语按拍数/假名、其他语言给相应单位）。
                    翻译时把译文长度落在这个区间内，即可既不拖沓也不赶。

用法：
  # 评估一句中文台词的语速
  python3 speech_rate_evaluator.py evaluate --text "你到底想干什么" --duration 1.8

  # 给出译文长度预算（可先 evaluate 再把档位传进来，或直接让脚本内部评估）
  python3 speech_rate_evaluator.py budget --text "你到底想干什么" --duration 1.8 --lang en

  # 一步到位：同时输出语速档位和译文预算
  python3 speech_rate_evaluator.py plan --text "你到底想干什么" --duration 1.8 --lang ja

  # JSON 输出（供程序消费）
  python3 speech_rate_evaluator.py plan --text "..." --duration 1.8 --lang en --json

所有速率均为「配音/画外音」场景下的经验值，可按需在 LANG_PROFILES 里微调。
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# 标准中文语速基准（单位：有效字/秒，不含标点与空格）
# 依据配音与口播经验：正常会话约 4~6 字/秒，口播约 4.5 字/秒。
# ---------------------------------------------------------------------------
ZH_SLOW_MAX = 3.5      # < 3.5 字/秒 视为慢
ZH_FAST_MIN = 5.5      # > 5.5 字/秒 视为快
                       # 3.5 ~ 5.5 之间视为正常

# 语速档位对目标语言"正常速率"的缩放系数：
#   慢   → 目标语言也放慢，用更少的音节把话说清楚
#   正常 → 用目标语言的正常速率
#   快   → 目标语言也说得密一些，但不建议超过 1.3，否则听感失真
PACE_FACTOR = {
    "slow":   0.80,
    "normal": 1.00,
    "fast":   1.25,
}

PACE_LABEL_ZH = {
    "slow": "慢",
    "normal": "正常",
    "fast": "快",
}

# ---------------------------------------------------------------------------
# 各目标语言的"正常发音速率"（配音场景经验值）。
#   rate：每秒可舒适说出的 unit 数量
#   unit：该语言译文长度的计量单位（翻译时据此数长度）
# 注：syllable/mora 速率来自跨语言语音学研究的量级，可按项目微调。
# ---------------------------------------------------------------------------
LANG_PROFILES = {
    "zh": {"name": "中文",   "rate": 4.5, "unit": "字",   "note": "按汉字个数计（不含标点）"},
    "en": {"name": "英语",   "rate": 2.3, "unit": "词",   "note": "按英文单词数计，约合 138 词/分钟"},
    "ja": {"name": "日语",   "rate": 6.5, "unit": "拍",   "note": "按 mora/假名个数计（拗音算 1 拍）"},
    "ko": {"name": "韩语",   "rate": 5.3, "unit": "音节", "note": "按谚文音节块个数计"},
    "es": {"name": "西班牙语","rate": 5.4, "unit": "音节", "note": "按音节数计，约合 2.1 词/秒"},
    "fr": {"name": "法语",   "rate": 5.0, "unit": "音节", "note": "按音节数计"},
    "de": {"name": "德语",   "rate": 2.0, "unit": "词",   "note": "德语单词较长，按单词数计"},
    "pt": {"name": "葡萄牙语","rate": 2.2, "unit": "词",   "note": "按单词数计"},
    "it": {"name": "意大利语","rate": 5.6, "unit": "音节", "note": "按音节数计"},
    "ru": {"name": "俄语",   "rate": 2.0, "unit": "词",   "note": "俄语单词较长，按单词数计"},
    "id": {"name": "印尼语", "rate": 2.6, "unit": "词",   "note": "按单词数计"},
    "th": {"name": "泰语",   "rate": 4.8, "unit": "音节", "note": "按音节数计"},
    "vi": {"name": "越南语", "rate": 4.5, "unit": "音节", "note": "越南语多单音节，按音节/词数计"},
    "ar": {"name": "阿拉伯语","rate": 4.5, "unit": "音节", "note": "按音节数计"},
    # --- 以下为按评测表实际出现语种补充（含源语言与目标语言） ---
    "tr": {"name": "土耳其语","rate": 5.5, "unit": "音节", "note": "按音节数计；黏着语单词长，音节数比词数可靠"},
    "pl": {"name": "波兰语", "rate": 2.0, "unit": "词",   "note": "按单词数计；辅音簇密集、单词较长"},
    "ur": {"name": "乌尔都语","rate": 4.6, "unit": "音节", "note": "按音节数计；与印地语口语速率相近"},
    "hi": {"name": "印地语", "rate": 4.8, "unit": "音节", "note": "按音节数计"},
    "tl": {"name": "他加禄语","rate": 5.0, "unit": "音节", "note": "按音节数计；菲律宾语/Filipino 同档"},
    "ms": {"name": "马来语", "rate": 2.6, "unit": "词",   "note": "按单词数计；与印尼语同源，速率同档"},
    "nl": {"name": "荷兰语", "rate": 2.1, "unit": "词",   "note": "按单词数计"},
}

# 语言别名 → 标准 code，方便直接传中文/全称
LANG_ALIASES = {
    "中文": "zh", "汉语": "zh", "chinese": "zh", "mandarin": "zh", "zh-cn": "zh", "zh_cn": "zh",
    "普通话": "zh", "简体中文": "zh", "国语": "zh",
    "英语": "en", "英文": "en", "english": "en",
    "日语": "ja", "日文": "ja", "japanese": "ja", "jp": "ja",
    "韩语": "ko", "韩文": "ko", "korean": "ko", "kr": "ko", "朝鲜语": "ko",
    "西班牙语": "es", "西语": "es", "spanish": "es",
    "法语": "fr", "法文": "fr", "french": "fr",
    "德语": "de", "德文": "de", "german": "de",
    "葡萄牙语": "pt", "葡语": "pt", "portuguese": "pt",
    "意大利语": "it", "italian": "it", "意语": "it",
    "俄语": "ru", "俄文": "ru", "russian": "ru", "俄罗斯语": "ru",
    "印尼语": "id", "indonesian": "id",
    "印度尼西亚语": "id", "印度尼西亚文": "id", "indonesia": "id",
    "泰语": "th", "thai": "th",
    "越南语": "vi", "vietnamese": "vi", "越语": "vi",
    "阿拉伯语": "ar", "arabic": "ar", "阿语": "ar",
    # --- 补充语种的别名 ---
    "土耳其语": "tr", "土耳其文": "tr", "turkish": "tr",
    "波兰语": "pl", "波兰文": "pl", "polish": "pl",
    "乌尔都语": "ur", "乌尔都文": "ur", "urdu": "ur",
    "印地语": "hi", "hindi": "hi", "北印度语": "hi",
    "他加禄语": "tl", "菲律宾语": "tl", "tagalog": "tl", "filipino": "tl", "fil": "tl",
    "马来语": "ms", "malay": "ms", "malaysian": "ms",
    "荷兰语": "nl", "dutch": "nl",
}

# ---------------------------------------------------------------------------
# 地域 → 语言的推断表。
# 评测表里"目标语言"一列常被写成国家/地区名（如"墨西哥""巴西"），甚至写成
# "墨西哥语"这类并不存在的语种名。这里做一层兜底映射，避免直接报未知语言。
# 注意：只用于推断"该说哪种语言"，具体口音仍需按目标地域单独交代。
# ---------------------------------------------------------------------------
REGION_TO_LANG = {
    "墨西哥": "es", "西班牙": "es", "阿根廷": "es", "哥伦比亚": "es", "智利": "es",
    "秘鲁": "es", "拉美": "es", "拉丁美洲": "es", "墨西哥语": "es",
    "巴西": "pt", "葡萄牙": "pt",
    "美国": "en", "英国": "en", "加拿大": "en", "澳大利亚": "en", "新西兰": "en",
    "爱尔兰": "en", "新加坡": "en", "菲律宾": "tl", "印度": "hi",
    "德国": "de", "奥地利": "de", "瑞士": "de",
    "法国": "fr", "意大利": "it", "日本": "ja", "韩国": "ko",
    "俄罗斯": "ru", "俄国": "ru",
    "印度尼西亚": "id", "印尼": "id",
    "马来西亚": "ms", "泰国": "th", "越南": "vi",
    "土耳其": "tr", "波兰": "pl", "巴基斯坦": "ur", "荷兰": "nl",
    "沙特": "ar", "阿联酋": "ar", "埃及": "ar", "中东": "ar",
    "中国": "zh", "台湾": "zh", "香港": "zh",
}


def normalize_lang(lang: str) -> str:
    if not lang:
        return ""
    raw = lang.strip()
    key = raw.lower()
    if key in LANG_PROFILES:
        return key
    if key in LANG_ALIASES:
        return LANG_ALIASES[key]
    # 传入的是原样中文别名（未 lower 命中）
    if raw in LANG_ALIASES:
        return LANG_ALIASES[raw]
    # 兜底：传入的是国家 / 地区名（如"墨西哥""巴西"）时按地域推断语言
    if raw in REGION_TO_LANG:
        return REGION_TO_LANG[raw]
    if key in REGION_TO_LANG:
        return REGION_TO_LANG[key]
    return key  # 未知则原样返回，后续报错提示


def supported_langs_help() -> str:
    """列出全部受支持语种，供报错信息使用。"""
    items = [f"{code}({prof['name']})" for code, prof in LANG_PROFILES.items()]
    return ", ".join(items)


def count_zh_chars(text: str) -> int:
    """统计有效字数：中文汉字 + 字母数字串（每个连续串算 1），忽略标点空格。"""
    if not text:
        return 0
    han = len(re.findall(r"[一-鿿]", text))
    # 夹杂的英文单词/数字，每个连续串按 1 个"字"的时长近似计入
    latin_tokens = len(re.findall(r"[A-Za-z0-9]+", text))
    return han + latin_tokens


def classify_zh_pace(chars: int, duration: float):
    if duration <= 0:
        raise ValueError("duration 必须为正数（秒）")
    cps = chars / duration
    if cps < ZH_SLOW_MAX:
        pace = "slow"
    elif cps > ZH_FAST_MIN:
        pace = "fast"
    else:
        pace = "normal"
    return pace, cps


def evaluate(text: str, duration: float):
    chars = count_zh_chars(text)
    pace, cps = classify_zh_pace(chars, duration)
    return {
        "text": text,
        "duration": round(duration, 2),
        "effective_chars": chars,
        "chars_per_second": round(cps, 2),
        "pace": pace,
        "pace_zh": PACE_LABEL_ZH[pace],
    }


def budget(duration: float, pace: str, lang: str):
    code = normalize_lang(lang)
    if code not in LANG_PROFILES:
        raise ValueError(
            f"未知目标语言 '{lang}'。支持以下语种（可传 code、中文名或英文名，也可传国家/地区名）：\n"
            f"  {supported_langs_help()}"
        )
    if pace not in PACE_FACTOR:
        raise ValueError(f"未知语速档位 '{pace}'，应为 slow / normal / fast 之一。")

    prof = LANG_PROFILES[code]
    target_rate = prof["rate"] * PACE_FACTOR[pace]
    center = target_rate * duration          # 推荐中心长度
    low = center * 0.85                       # 舒适区间下限（留 15% 缓冲）
    high = center * 1.15                      # 舒适区间上限
    return {
        "lang": code,
        "lang_name": prof["name"],
        "unit": prof["unit"],
        "pace": pace,
        "pace_zh": PACE_LABEL_ZH.get(pace, pace),
        "duration": round(duration, 2),
        "recommended": round(center, 1),
        "range_low": max(1, round(low)),
        "range_high": round(high),
        "note": prof["note"],
    }


def fmt_evaluate(r):
    return (
        f"【语速评估】\n"
        f"  台词：{r['text']}\n"
        f"  时长：{r['duration']}s | 有效字数：{r['effective_chars']} | "
        f"语速：{r['chars_per_second']} 字/秒\n"
        f"  判定：{r['pace_zh']}（{r['pace']}）"
    )


def fmt_budget(r):
    return (
        f"【译文长度预算】\n"
        f"  目标语言：{r['lang_name']}（{r['lang']}） | 原时长：{r['duration']}s | "
        f"源语速档位：{r['pace_zh']}\n"
        f"  建议译文长度：约 {r['recommended']} {r['unit']}，"
        f"舒适区间 {r['range_low']}~{r['range_high']} {r['unit']}\n"
        f"  说明：{r['note']}。译文落在区间内即可避免拖沓或说不完；\n"
        f"        信息可合理增删，只需保证含义传达正确。"
    )


def main():
    p = argparse.ArgumentParser(description="语速评估与目标语言译文长度预算")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("evaluate", help="评估中文台词语速（慢/正常/快）")
    pe.add_argument("--text", required=True)
    pe.add_argument("--duration", type=float, required=True, help="该句台词时长（秒）")
    pe.add_argument("--json", action="store_true")

    pb = sub.add_parser("budget", help="给出目标语言译文长度预算")
    pb.add_argument("--duration", type=float, required=True)
    pb.add_argument("--lang", required=True, help="目标语言 code 或别名，如 en / 日语")
    pb.add_argument("--pace", help="语速档位 slow/normal/fast；省略则用 --text 现算")
    pb.add_argument("--text", help="若未提供 --pace，则用该原文现场评估语速")
    pb.add_argument("--json", action="store_true")

    pp = sub.add_parser("plan", help="一步到位：语速评估 + 译文预算")
    pp.add_argument("--text", required=True)
    pp.add_argument("--duration", type=float, required=True)
    pp.add_argument("--lang", required=True)
    pp.add_argument("--json", action="store_true")

    args = p.parse_args()

    try:
        if args.cmd == "evaluate":
            r = evaluate(args.text, args.duration)
            print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else fmt_evaluate(r))

        elif args.cmd == "budget":
            if args.pace:
                pace = args.pace
            elif args.text:
                pace = evaluate(args.text, args.duration)["pace"]
            else:
                p.error("budget 需要 --pace 或 --text 之一来确定语速档位")
            r = budget(args.duration, pace, args.lang)
            print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else fmt_budget(r))

        elif args.cmd == "plan":
            ev = evaluate(args.text, args.duration)
            bg = budget(args.duration, ev["pace"], args.lang)
            if args.json:
                print(json.dumps({"evaluate": ev, "budget": bg}, ensure_ascii=False, indent=2))
            else:
                print(fmt_evaluate(ev))
                print()
                print(fmt_budget(bg))
    except (ValueError, KeyError) as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()