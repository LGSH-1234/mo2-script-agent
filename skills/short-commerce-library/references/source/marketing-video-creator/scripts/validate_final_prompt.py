
#!/usr/bin/env python3
"""扫描实际的《视频生成Prompt.md》，做确定性结构、冲突与 Hook 验收检查。

设计原则（本轮重构）：**脚本只保留“正确产物一定能通过”的确定性检查**，
不再做任何“必须出现某个措辞/关键词/句式”的正向关键词匹配，也不做需要语义
理解的分类判断（静态收尾 vs 真实动作、开场留白、尺寸类比等）。原因：那类
检查依赖有限的关键词表，而一个写法正确的 Prompt 换个说法就会永远匹配不上，
导致 Agent 反复改写却始终过不了校验、无限卡死。那些语义/创意层面的约束改由
Agent 依据各 `contract-*.md` 正文自行保证，不再交给脚本裁决。对用户本次明确
选中的 Hook，例外使用项目内 `hook_acceptance_contract` 的字面证据和时间窗口做确定性回看，
不使用全局关键词表。

保留的检查都属于两类不会误伤正确产物的判定：
1. **结构/格式**：能否解析出带时间戳的分镜节拍（正确产物本来就有）。
2. **禁止项缺席 + 自相矛盾**：某个明确的禁用词不能出现、互斥指令不能同时出现
   （正确产物本来就不会踩，属于确定性回归网）。

校验不通过时，errors 里返回自然语言问题描述（中文），直接说清哪里出了问题、
该怎么改。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TIME_RANGE = re.compile(
    r"(?P<start>\d+(?:\.\d+)?)\s*(?:s|秒)?\s*[-–—~至]\s*"
    r"(?P<end>\d+(?:\.\d+)?)\s*(?:s|秒)",
    re.IGNORECASE,
)
NO_TEXT_TERMS = ("无字幕", "不要字幕", "不出现任何文字", "无画面文字", "no subtitles")
ADD_TEXT_TERMS = ("花字", "字幕出现", "出现字幕", "底部字幕", "屏幕文字", "on-screen text")
CONTRACT_KEYS = ("forbidden_sku_terms", "unsupported_claim_terms", "forbidden_imports")


class ContractInputError(Exception):
    """--contract 入参本身有问题（路径不存在 / JSON 不合法 / 顶层不是对象）。"""


def _load_contract(raw: str | None) -> dict[str, Any]:
    """加载 --contract。三种写法都接受，调用方不必先落盘：

    1. 省略不传：等价于三个禁止项列表都为空，仍跑结构门与字幕冲突门。
    2. JSON 文件路径：`--contract _internal/final_prompt_contract.json`
    3. 内联 JSON 字符串：`--contract '{"forbidden_sku_terms": ["钢丝球"]}'`

    任何失败都抛 ContractInputError（中文自然语言），由 main() 打印成
    `{"ok": false, "errors": [...]}`，不再抛 traceback。
    """
    if raw is None:
        return {}
    text = raw.strip()
    if not text:
        return {}

    if text.startswith("{") or text.startswith("["):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ContractInputError(
                f"--contract 传的内联 JSON 解析失败（{exc.msg}，第 {exc.lineno} 行第 {exc.colno} 列）："
                "请检查引号/逗号是否完整。内联写法示例："
                "--contract '{\"forbidden_sku_terms\": [\"钢丝球\"]}'。"
            ) from None
    else:
        path = Path(text)
        if not path.exists():
            raise ContractInputError(
                f"--contract 指定的文件不存在：{text}。"
                "三种写法都可以：① 省略 --contract（禁止项按空处理，仍跑结构门与字幕冲突门）；"
                "② 先把禁止项写成 JSON 文件再传它的路径（相对路径是相对当前工作目录，跨目录时用绝对路径）；"
                "③ 不落盘，直接传内联 JSON，例如 --contract '{\"forbidden_sku_terms\": [\"钢丝球\"]}'。"
            )
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ContractInputError(
                f"--contract 文件 {text} 里的 JSON 解析失败（{exc.msg}，第 {exc.lineno} 行第 {exc.colno} 列）："
                "请修正该文件内容。"
            ) from None

    if not isinstance(data, dict):
        raise ContractInputError(
            "--contract 的内容必须是一个 JSON 对象，形如 "
            "{\"forbidden_sku_terms\": [], \"unsupported_claim_terms\": [], \"forbidden_imports\": []}，"
            f"当前是 {type(data).__name__}。"
        )
    for key in CONTRACT_KEYS:
        if key in data and not isinstance(data[key], (list, str)):
            raise ContractInputError(
                f"--contract 里的 `{key}` 必须是字符串数组（可为空数组），"
                f"当前是 {type(data[key]).__name__}。"
            )
    return data


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    # 容错：单个禁用词允许直接写成字符串，等价于只有一项的数组。
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def _contains_any(text: str, terms: list[str] | tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(_norm(term) in lowered for term in terms if _norm(term))


def parse_timeline(prompt: str) -> list[dict[str, Any]]:
    timeline_start = 0
    for marker in ("各个分镜", "分镜具体内容", "timestamped beats"):
        position = prompt.lower().find(marker.lower())
        if position >= 0:
            timeline_start = max(timeline_start, position)
    timeline_text = prompt[timeline_start:]
    matches = list(TIME_RANGE.finditer(timeline_text))
    beats: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = float(match.group("start"))
        end = float(match.group("end"))
        block_end = (
            matches[index + 1].start() if index + 1 < len(matches) else len(timeline_text)
        )
        beats.append(
            {
                "start": start,
                "end": end,
                "duration": max(0.0, end - start),
                "text": timeline_text[match.start():block_end],
            }
        )
    return beats


def _flatten_forbidden_imports(value: Any) -> list[str]:
    terms: list[str] = []
    for item in _as_list(value):
        if isinstance(item, str):
            terms.append(item)
        elif isinstance(item, dict):
            terms.extend(str(term) for term in _as_list(item.get("terms")))
    return terms


def _hook_acceptance_warnings(
    beats: list[dict[str, Any]], contract: dict[str, Any]
) -> list[str]:
    """回看最终 Prompt 是否保留了本次选中 Hook 的字面证据与顺序。

    返回的是 **warnings（提示）而非 errors（硬门）**：证据词是否逐字命中属于语义判断，
    字符串匹配会误伤只是换了措辞的正确 Prompt。这里只提示「合同承诺过、Prompt 里没
    照面」的点，不阻断 ok。结构门、禁用词门、字幕矛盾门仍是硬门。
    """
    acceptance = contract.get("hook_acceptance_contract") or {}
    if acceptance.get("selected") is not True:
        return []

    warnings: list[str] = []
    first_hits: dict[str, tuple[float, int]] = {}
    for requirement in _as_list(acceptance.get("signature_requirements")):
        if not isinstance(requirement, dict):
            continue
        requirement_id = str(requirement.get("id") or "unnamed")
        opening_required = bool(requirement.get("opening_required"))
        deadline = float(
            requirement.get("deadline_seconds")
            or acceptance.get("opening_deadline_seconds")
            or 3.0
        )
        candidates = [
            beat for beat in beats if not opening_required or float(beat.get("start", 999)) < deadline
        ]
        searchable = "\n".join(str(beat.get("text") or "") for beat in candidates).lower()
        evidence = requirement.get("evidence") or {}
        all_of = [_norm(item) for item in _as_list(evidence.get("all_of")) if _norm(item)]
        any_of = [_norm(item) for item in _as_list(evidence.get("any_of")) if _norm(item)]
        missing_all = [item for item in all_of if item not in searchable]
        any_ok = not any_of or any(item in searchable for item in any_of)
        if missing_all or not any_ok:
            missing = missing_all or any_of
            scope = f"前 {deadline:g} 秒" if opening_required else "全片"
            warnings.append(
                f"提示：最终 Prompt 可能丢失 Hook 验收项 {requirement_id}——{scope}内没找到证据"
                f"「{' / '.join(missing)}」。原始要求：{requirement.get('source_text') or ''}。"
                "请确认是漏了，还是换了等价说法（换了说法可忽略本提示）。"
            )
            continue

        terms = all_of + any_of
        for beat in candidates:
            candidate_text = str(beat.get("text") or "").lower()
            positions = [candidate_text.find(term) for term in terms if term in candidate_text]
            if positions:
                first_hits[requirement_id] = (float(beat.get("start", 999)), min(positions))
                break

    if _norm(acceptance.get("sequence_policy")) in {"mechanism_order_required", "user_locked"}:
        ordered_ids = [str(item) for item in _as_list(acceptance.get("ordered_requirement_ids"))]
        observed = [first_hits.get(item) for item in ordered_ids]
        if all(item is not None for item in observed):
            concrete = [item for item in observed if item is not None]
            if concrete != sorted(concrete):
                warnings.append(
                    "提示：最终 Prompt 的 Hook 核心动作/状态顺序与 ordered_requirement_ids 不一致——"
                    f"合同期望 {' → '.join(ordered_ids)}。若是有意调整请自行确认无碍。"
                )
    return warnings


def validate_prompt(prompt: str, contract: dict[str, Any]) -> tuple[list[str], list[str]]:
    """返回 (errors, warnings)。

    errors 是确定性硬门（结构、禁用词、字幕自相矛盾），命中即 ok:false；
    warnings 是 Hook 证据/顺序这类语义提示，不影响 ok，只提醒阅读者自查。
    """
    errors: list[str] = []
    warnings: list[str] = []
    lowered = prompt.lower()
    beats = parse_timeline(prompt)

    # 1. 结构门（硬）：必须能解析出带时间戳的分镜节拍。正确产物本来就有。
    if not beats:
        errors.append("最终 Prompt 里找不到可解析的分镜时间轴：必须写成「0-3秒」这样的带时间戳的分镜节拍。")
    else:
        # Hook 证据/顺序只作为提示，不进 errors。
        warnings.extend(_hook_acceptance_warnings(beats, contract))

    # 2. 禁止项缺席门（硬）：这些是明确列出的禁用词，正确产物本来就不会出现。
    #    只做“不能出现”判定，不做“必须出现某措辞”的正向匹配（后者会误伤正确产物）。
    for term in _as_list(contract.get("forbidden_sku_terms")):
        if _norm(term) in lowered:
            errors.append(f"最终 Prompt 里出现了禁用的 SKU 变体/材质术语「{term}」:请删掉，它和锁定的 SKU 不符。")
    for term in _as_list(contract.get("unsupported_claim_terms")):
        if _norm(term) in lowered:
            errors.append(f"最终 Prompt 里出现了无证据支撑的宣称「{term}」:没有证据的功效话术不能写。")

    forbidden_imports = _flatten_forbidden_imports(contract.get("forbidden_imports"))
    for term in forbidden_imports:
        if _norm(term) in lowered:
            errors.append(f"最终 Prompt 里混入了被禁止的方案外来元素「{term}」:请删掉，它不属于选定方案。")

    # 3. 自相矛盾门（硬）:字幕指令不能既要“无字幕”又要“出现字幕/花字”。
    if _contains_any(prompt, NO_TEXT_TERMS) and _contains_any(prompt, ADD_TEXT_TERMS):
        errors.append("字幕/画面文字指令自相矛盾：Prompt 里既要求「无字幕」又要求「出现字幕/花字」，二者只能留一个。")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="Path to the actual 视频生成Prompt Markdown")
    parser.add_argument(
        "--contract",
        default=None,
        help="内部禁止项合同：可传 JSON 文件路径，也可直接传内联 JSON，如 "
             "'{\"forbidden_sku_terms\": [\"钢丝球\"]}'；省略时按空禁止项处理，"
             "仍执行时间轴结构门与字幕冲突门",
    )
    args = parser.parse_args()

    prompt_path = Path(args.prompt)
    if not prompt_path.exists():
        print(json.dumps({
            "ok": False,
            "errors": [f"要校验的 Prompt 文件不存在：{args.prompt}。"
                       "请确认路径（相对路径是相对当前工作目录，跨目录时用绝对路径）。"],
        }, ensure_ascii=False, indent=2))
        return 1

    try:
        contract = _load_contract(args.contract)
    except ContractInputError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1

    prompt = prompt_path.read_text(encoding="utf-8")
    errors, warnings = validate_prompt(prompt, contract)
    result: dict[str, Any] = {"ok": not errors, "errors": errors, "warnings": warnings}
    if warnings:
        result["warnings_note"] = (
            "warnings 是提示、不阻塞通过：这些是合同承诺过、但 Prompt 里没逐字照面的 Hook 证据或顺序。"
            "请逐条判断——确属漏写就补进对应分镜；只是换了等价说法就忽略。"
        )
    if args.contract is None:
        result["note"] = ("未传 --contract：本次只跑了时间轴结构门与字幕冲突门，"
                          "三类禁止项（SKU 变体/无依据宣称/他程序元素）未被检查。"
                          "若本项目存在需要拦的禁用词，请补传 --contract 后重跑。")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())