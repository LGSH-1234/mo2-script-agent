
#!/usr/bin/env python3
"""估算口播/旁白时长：支持多语言，并按场景语速分档（douyin/fast/normal/slow）。

核心思路（对齐语言学事实）：
- 不同语言并不共用同一个"字/秒"速率。信息率大致恒定（Pellegrino 等 2011），
  但音节/词速与信息密度成反比，因此每种语言要用各自的计量单位与基准速率：
  * 汉语/日语/韩语等 CJK 系：以"字/音节块"计，用 字·音节/秒；
  * 英语/西语/法语/德语等拉丁系：以"词"计，用 词/秒（WPM/60）。
- 速率必须先按场景分档再评估，而不是用一个固定值：
  * douyin 抖音原生：短句、快停顿、强立场与动作声交替；
  * fast   高语速：广告冲刺、卡点、促销催单；
  * normal 正常：常规讲解、对话、种草、教程；
  * slow   慢语速：情感/品牌片、吟诵、强调、ASMR、庄重旁白。
  用法：先根据场景选定语速档位，再用该档位评估文案是否放得进目标时长。

数据来源（多方联网核对）：
- 汉语普通话：常速约 240 音节/分，播音约 300 字/分；短视频/种草口播实测语速通常还要更快，
  分档 慢 180-222 / 常 264-312 / 快 318-360 字/分（贴近偏快的口播/带货腔）。
- 英语按语境：慢读 100-120、演讲 120-140、对话 130-150、
  短视频/TTS 140-160、有声书 150-160、播客 150-170、新闻 150-175、
  解说 160-190、促销/带货可达 190-210 WPM；normal 取偏快的短视频口播主力带 156-192 WPM。
- 语言均速参考：英语约 150、西语 170-180、日语 200+ 音节、汉语约 120-130 WPM（此为均速基线，
  营销口播普遍快于该基线，故 normal 档在其上上浮）。
速率以"单位/秒"存储（分档给出 min~max 以反映自然波动，从而输出时长区间）。

可选的目标时长（--target 秒）：
- 传入后，脚本在合计时长之外再给一行"预期耗时"分析：把当前(合计)时长区间
  和目标秒数比对，若超时则按"时长与单位数成正比"折算出大致需要删减多少字/词。
- 删减量同样给区间：念快(下限)才放得下时的最小删减 ~ 念慢(上限)也要保证放下时的
  稳妥删减；已在目标内则提示无需删减。
"""

import math
import sys
import unicodedata
from typing import NamedTuple


# 每种语言 -> 计量单位类型：char = 按字/音节块；word = 按词
UNIT_KIND = {
    "zh": "char",
    "ja": "char",
    "ko": "char",
    "en": "word",
    "es": "word",
    "fr": "word",
    "de": "word",
}

# 每种语言 -> 场景档位 -> (min_rate, max_rate)，单位为"单位/秒"。
# 时长下限 = 单位数 / max_rate（念得快），上限 = 单位数 / min_rate（念得慢）。
RATES = {
    # 汉语：字/秒。慢 180-222、常 264-312、快 318-360 字/分 -> /60
    "zh": {
        "douyin": (5.5, 6.5),
        "fast": (5.3, 6.0),
        "normal": (4.4, 5.2),
        "slow": (3.0, 3.7),
    },
    # 日语:音节(mora)/秒，语速偏高
    "ja": {"douyin": (8.0, 9.1), "fast": (7.8, 8.8), "normal": (6.6, 7.6), "slow": (4.5, 5.5)},
    # 韩语:音节块/秒
    "ko": {"douyin": (7.4, 8.5), "fast": (7.2, 8.2), "normal": (6.0, 7.1), "slow": (4.0, 5.0)},
    # 英语:词/秒。慢 102-132、常 156-192、快 198-228 WPM -> /60
    "en": {"douyin": (3.4, 4.0), "fast": (3.3, 3.8), "normal": (2.6, 3.2), "slow": (1.7, 2.2)},
    # 西语:语速偏快
    "es": {"douyin": (4.2, 4.8), "fast": (4.1, 4.6), "normal": (3.3, 4.0), "slow": (2.2, 2.8)},
    # 法语
    "fr": {"douyin": (3.6, 4.2), "fast": (3.5, 4.0), "normal": (2.9, 3.4), "slow": (1.9, 2.4)},
    # 德语
    "de": {"douyin": (3.4, 4.0), "fast": (3.3, 3.8), "normal": (2.6, 3.2), "slow": (1.7, 2.2)},
}

SCENES = ("douyin", "fast", "normal", "slow")

# 场景语义提示：给 Agent 选档位时的对照（不参与计算）。
SCENE_HINTS = {
    "douyin": "抖音原生：短句快说 / 0.15-0.35秒快停顿 / 立场与动作声交替",
    "fast": "高语速：广告冲刺 / 卡点 / 促销催单 / 快节奏达人口播",
    "normal": "正常语速：常规讲解 / 对话 / 种草 / 教程",
    "slow": "慢语速：情感与品牌片 / 吟诵强调 / ASMR / 庄重旁白",
}

LANG_NAMES = {
    "zh": "中文", "ja": "日语", "ko": "韩语",
    "en": "英语", "es": "西语", "fr": "法语", "de": "德语",
}

# 逃生枚举：文案语种不在上面 7 种之内时传 other。
# 脚本不去猜具体是哪门语言，而是看台词实际的 Unicode 书写体系粗分：
# CJK/表意字占多 -> 用 zh 字速代理；否则(拉丁字母系为主) -> 用 en 词速代理。
# 这是有意的近似：跨语言信息率大致恒定，"拉丁 vs CJK"这一粗分远比"zh 还是 ja"可靠，
# 且拉丁系各语言词速本在同一量级，故用 en/zh 代理给出粗估并显式标注，供 Agent/用户知情。
OTHER = "other"


def _resolve_lang(lang: str, units: "SpeechUnits"):
    """把 --lang 归结为实际用于取速率的语种。

    返回 (proxy_lang, approx)：
      - lang 为精确枚举 -> 原样返回，approx=False；
      - lang == other   -> 按台词书写体系粗分：CJK 字数 > 拉丁词数则 zh 代理，
                           否则 en 代理；approx=True，表示这是近似估算。
    """
    if lang in RATES:
        return lang, False
    # lang == OTHER：由台词文本自身的 Unicode 构成决定代理档
    if units.chars > units.english_words:
        return "zh", True
    return "en", True


class SpeechUnits(NamedTuple):
    chars: int          # CJK/假名/谚文等"字/音节块"数（unicodedata 类别 Lo）
    digits: int         # 数字
    english_words: int  # 拉丁文词（连续字母段）


def count_speech_units(text: str) -> SpeechUnits:
    """统计字（CJK/假名/谚文，类别 Lo）、数字、拉丁词。保持向后兼容。"""
    if not text:
        return SpeechUnits(0, 0, 0)

    chars = digits = english_words = 0
    in_word = False

    def flush_word() -> None:
        nonlocal english_words, in_word
        if in_word:
            english_words += 1
            in_word = False

    for char in text:
        category = unicodedata.category(char)
        if category.startswith("Lo"):
            flush_word()
            chars += 1
        elif category == "Nd":
            flush_word()
            digits += 1
        elif category.startswith("L"):
            in_word = True
        elif category.startswith("M") and in_word:
            continue
        elif char in ("'", "’") and in_word:
            continue
        else:
            flush_word()
    flush_word()
    return SpeechUnits(chars, digits, english_words)


def estimate_speech(text: str, language: str, scene: str = "normal",
                    mode: str = None):
    """估算口播时长。

    参数：
      language : zh | ja | ko | en | es | fr | de（必传，由调用方按文案语种显式指定，不做自动识别）；
                 语种超出这 7 种时传 other，脚本按台词书写体系就近取 zh/en 代理档做近似估算。
      scene    : douyin | fast | normal | slow —— 先按场景选定语速档位。
      mode     : 兼容旧参数，slow -> scene=slow，normal -> scene=normal。

    返回 (units, lower, upper, proxy_lang, approx, effective)：
      单位统计、时长下限、时长上限（秒）、实际取速率的语种、是否为 other 近似估算、
      折合有效单位数（供目标时长删减折算用）。
    """
    if mode is not None:
        scene = "slow" if mode == "slow" else "normal"
    if scene not in SCENES:
        raise ValueError("scene must be one of douyin/fast/normal/slow")

    if language not in RATES and language != OTHER:
        raise ValueError(
            f"unsupported language: {language}；"
            f"请显式指定 zh/ja/ko/en/es/fr/de 之一，语种超出枚举时传 other"
        )

    units = count_speech_units(text)
    proxy_lang, approx = _resolve_lang(language, units)
    rate_min, rate_max = RATES[proxy_lang][scene]

    if UNIT_KIND[proxy_lang] == "char":
        # CJK 系：字与数字各按 1 个字时长；内嵌拉丁词约合 2 个字时长
        effective = units.chars + units.digits + units.english_words * 2
    else:
        # 拉丁系：词、数字各按 1 个词时长；内嵌 CJK 字约合 1 个词时长
        effective = units.english_words + units.digits + units.chars

    lower = effective / rate_max
    upper = effective / rate_min
    return units, round(lower, 1), round(upper, 1), proxy_lang, approx, effective


def format_units(units: SpeechUnits) -> str:
    parts = []
    if units.chars:
        parts.append(f"{units.chars}字")
    if units.digits:
        parts.append(f"{units.digits}数字")
    if units.english_words:
        parts.append(f"{units.english_words}英文词")
    return "+".join(parts) if parts else "0字"


def format_target_advice(lower: float, upper: float, effective: int,
                         target: float, unit_label: str) -> str:
    """把(合计)时长区间与目标时长比对，折算出大致需要删减多少字/词。

    原理：在同一语速档位下，时长与有效单位数成正比，故
      需要保留的单位数 = effective * target / 当前时长。
    删减量 = effective - 保留数。分别对下限(念快)与上限(念慢)折算：
      - 念快才放下：trim_min = effective * (1 - target/lower)（lower>target 时才为正）
      - 念慢也放下：trim_max = effective * (1 - target/upper)（upper>target 时才为正）
    upper>lower，故 trim_max >= trim_min，即"要连念慢也稳妥放下"需删得更多。
    删减量向上取整，宁可多删一点以留余量。
    """
    if effective <= 0 or target <= 0:
        return f"预期耗时：目标{_fmt_sec(target)}s —— 无有效文案或目标无效，无法折算。"

    # 已完全放得进目标（连念慢都不超）
    if upper <= target:
        margin = round(target - upper, 1)
        return (f"预期耗时：目标{_fmt_sec(target)}s [达标] 当前[{lower}s~{upper}s]已在目标内，"
                f"无需删减（最慢念完还余约{margin}s）。")

    trim_min = max(0, math.ceil(effective * (1 - target / lower))) if lower > 0 else 0
    trim_max = max(0, math.ceil(effective * (1 - target / upper))) if upper > 0 else 0

    # 念快放得下、只有念慢会超
    if lower <= target < upper:
        return (f"预期耗时：目标{_fmt_sec(target)}s [注意] 当前[{lower}s~{upper}s]——"
                f"念快勉强放得下(0删减)，但要连念慢也稳妥控制在{_fmt_sec(target)}s内，"
                f"约需删减 {trim_max} {unit_label}（现共{effective}{unit_label}）。")

    # 连念最快都超时
    return (f"预期耗时：目标{_fmt_sec(target)}s [超时] 当前[{lower}s~{upper}s]已超时——"
            f"约需删减 {trim_min}~{trim_max} {unit_label}"
            f"（下限=念快也要放下，上限=念慢也稳妥；现共{effective}{unit_label}）。")


def _fmt_sec(value: float) -> str:
    """秒数展示：整数去掉小数点，否则保留一位。"""
    return str(int(value)) if float(value).is_integer() else str(round(value, 1))


def format_capacity(lang: str, scene: str, target: float) -> str:
    """不给台词、只给 --target 时的「容量反查」：该档位下目标秒数大致能装多少字/词。

    与正向核算共用同一套速率表：
      念慢(rate_min)也放得下的稳妥量 = target * rate_min；
      念到最快(rate_max)才刚好塞满的上限 = target * rate_max。
    向下取整（宁可少写，给停顿与呼吸留余量）。
    """
    rate_min, rate_max = RATES[lang][scene]
    unit_label = "字" if UNIT_KIND[lang] == "char" else "词"
    safe = int(target * rate_min)
    limit = int(target * rate_max)
    return "\n".join([
        f"[语言：{LANG_NAMES[lang]}｜场景语速档位：{scene}｜{SCENE_HINTS[scene]}]",
        f"容量反查：目标 {_fmt_sec(target)}s 在该档位下大约可容纳 {safe}~{limit} {unit_label}。",
        f"  {safe}{unit_label} = 念慢也放得下的稳妥量（有停顿/留白/音效时按这个写）；",
        f"  {limit}{unit_label} = 念到最快才刚好塞满的上限（不留呼吸，慎用）。",
        "下一步：把实际文案按段作为位置参数传进来做正向核算，例如",
        f'  python3 count_chars.py --lang {lang} --scene {scene} '
        f'--target {_fmt_sec(target)} "台词1" "台词2"',
    ])


def _print_usage() -> None:
    print('用法：python3 count_chars.py --lang zh|ja|ko|en|es|fr|de|other '
          '[--scene douyin|fast|normal|slow] [--target 目标秒数] "台词1" "台词2" ...')
    print("语言（必传，由调用方按文案语种显式指定，脚本不做自动识别）：")
    print("  zh 中文  ja 日语  ko 韩语  en 英语  es 西语  fr 法语  de 德语")
    print("  other 语种超出上面 7 种时传它，脚本按台词书写体系就近取 zh/en 代理档做近似估算")
    print("场景语速档位：")
    for scene in SCENES:
        print(f"  {scene:<6} {SCENE_HINTS[scene]}")
    print("可选 --target 目标秒数：给出后，除合计时长外再输出一行『预期耗时』，")
    print("  比对目标时长并折算若要控制在目标内大致需删减多少字/词。")
    print("只给 --lang/--scene/--target、不给任何台词时：输出『容量反查』——")
    print("  该语速档位下目标秒数大约能装多少字/词（稳妥量~上限），用于先定文案长度再写文案。")
    print("提示：先显式指定语种，再按场景确定语速档位，然后评估文案时长。")


def _pop_option(args, name):
    """从 args 中取出 --name value，返回 value 或 None。"""
    if name in args:
        index = args.index(name)
        if index + 1 >= len(args):
            return ValueError
        value = args[index + 1]
        del args[index:index + 2]
        return value
    return None


def main() -> int:
    args = sys.argv[1:]

    scene = _pop_option(args, "--scene")
    if scene is ValueError:
        print("错误：--scene 需要取值 douyin/fast/normal/slow", file=sys.stderr)
        return 2
    lang = _pop_option(args, "--lang")
    if lang is ValueError:
        print("错误：--lang 需要取值 zh/ja/ko/en/es/fr/de（超出枚举传 other）",
              file=sys.stderr)
        return 2
    legacy_mode = _pop_option(args, "--mode")
    if legacy_mode is ValueError:
        print("错误：--mode 需要取值 normal/slow", file=sys.stderr)
        return 2
    target_raw = _pop_option(args, "--target")
    if target_raw is ValueError:
        print("错误：--target 需要一个目标秒数，如 --target 15", file=sys.stderr)
        return 2
    target = None
    if target_raw is not None:
        try:
            target = float(target_raw)
        except ValueError:
            print("错误：--target 取值必须是数字（秒），如 --target 15",
                  file=sys.stderr)
            return 2
        if target <= 0:
            print("错误：--target 目标秒数必须为正数", file=sys.stderr)
            return 2

    if legacy_mode is not None and scene is None:
        scene = "slow" if legacy_mode == "slow" else "normal"
    if scene is None:
        scene = "normal"

    if scene not in SCENES:
        print("错误：--scene 取值只能是 douyin / fast / normal / slow", file=sys.stderr)
        return 2
    if lang is None:
        print("错误：--lang 为必传参数，请显式指定 zh/ja/ko/en/es/fr/de 之一"
              "（语种超出枚举时传 other）", file=sys.stderr)
        return 2
    if lang not in RATES and lang != OTHER:
        print("错误：--lang 取值只能是 zh/ja/ko/en/es/fr/de，"
              "语种超出枚举时传 other", file=sys.stderr)
        return 2

    if not args:
        # 没给台词但给了 --target：视为「这个档位下目标秒数能装多少字」的容量反查，
        # 而不是参数错误。真实故障：Agent 用 `--scene fast --lang zh --target 20`
        # 想先问容量，却吃到 usage + exit 1，只能再补一次调用。
        if target is not None:
            if lang == OTHER:
                print("错误：容量反查需要明确语种以取速率档。--lang other 只能在传入实际台词时使用"
                      "（脚本靠台词书写体系选代理档）。请改传 zh/ja/ko/en/es/fr/de 之一，"
                      "或直接把台词作为位置参数传进来。", file=sys.stderr)
                return 2
            print(format_capacity(lang, scene, target))
            return 0
        _print_usage()
        return 1

    if lang == OTHER:
        print("[语言：other（超出枚举）｜将按各段台词的书写体系就近取 zh/en 代理档做近似估算"
              f"｜场景语速档位：{scene}｜{SCENE_HINTS[scene]}]")
    else:
        print(f"[语言：{LANG_NAMES[lang]}｜场景语速档位：{scene}｜{SCENE_HINTS[scene]}]")

    total = SpeechUnits(0, 0, 0)
    lower_total = upper_total = 0.0
    effective_total = 0
    any_approx = False
    proxy_for_label = lang
    for text in args:
        units, lower, upper, proxy_lang, approx, effective = estimate_speech(
            text, language=lang, scene=scene)
        total = SpeechUnits(
            total.chars + units.chars,
            total.digits + units.digits,
            total.english_words + units.english_words,
        )
        lower_total += lower
        upper_total += upper
        effective_total += effective
        proxy_for_label = proxy_lang
        label = text if len(text) <= 20 else text[:20] + "…"
        approx_note = (
            f" ⚠近似估算（语种超出枚举，按 {LANG_NAMES[proxy_lang]}/"
            f"{'字' if UNIT_KIND[proxy_lang] == 'char' else '词'}速代理）"
            if approx else ""
        )
        any_approx = any_approx or approx
        print(f"「{label}」{format_units(units)}，耗时[{lower}s~{upper}s]{approx_note}")

    lower_total = round(lower_total, 1)
    upper_total = round(upper_total, 1)
    if len(args) > 1:
        print(
            f"【合计】{len(args)}段共{format_units(total)}，"
            f"耗时累加[{lower_total}s~{upper_total}s]"
        )

    if target is not None:
        unit_label = "字" if UNIT_KIND[proxy_for_label] == "char" else "词"
        print(format_target_advice(
            lower_total, upper_total, effective_total, target, unit_label))

    if any_approx:
        print("提示：本次含 other 近似估算，结论按粗估看待，宁可估长为文案留余量；"
              "若该语种确需精确速率，请补充其专用速率或改用最接近的受支持语种。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())