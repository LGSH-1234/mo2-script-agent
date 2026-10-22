
#!/usr/bin/env python3
"""直接校验实际交付的《故事脚本.md》。

设计原则（本轮重构）：脚本只保留“正确产物一定能通过”的确定性结构/格式检查，
不再做任何“首镜必须体现某关键词/某自明钩子”“开场留白与台词是否矛盾”“场景是否
回访”等需要语义理解或依赖有限关键词表的判断——那类检查一个写法正确的脚本换个
说法就永远匹配不上，会让 Agent 反复改写却过不了校验、无限卡死。开场钩子是否成立、
场景是否回访这类泛化创意/语义约束，改由 Agent 依据 `contract-*.md`
正文自行保证。唯一例外是用户本次明确选中的 Hook：它会被编译成带来源文本、
时间窗口和字面证据的 `hook_acceptance_contract`，校验器只按这份项目内合同验收，
不使用全局关键词表猜测创意。

校验不通过时，errors 里返回自然语言问题描述（中文），直接告诉阅读者哪里出了
问题、该怎么改。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_COLUMNS = ["镜号", "时长", "画面描述", "景别", "光影氛围", "对白·旁白", "音效", "运镜"]
INTERNAL_PATTERNS = (
    ("Hook Scope", re.compile(r"\bHook\s*Scope\b", re.I)),
    ("Bridge", re.compile(r"\bBridge\b", re.I)),
    ("Body takeover", re.compile(r"\bBody\s*takeover\b", re.I)),
    ("内部机制编号", re.compile(r"(?<![A-Za-z0-9])(?:BH|SO|S|D|R|H|P)\d{2}(?![A-Za-z0-9])")),
    ("内部字段", re.compile(r"\b(?:selected_content_program|program_lock|opening_hook_contract)\b", re.I)),
)
DURATION_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:s|秒)", re.I)


class ContractInputError(Exception):
    """--contract 入参本身有问题（路径不存在 / JSON 不合法 / 顶层不是对象）。"""
def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _hook_evidence_errors(
    rows: list[list[str]], durations: list[float], contract: dict[str, Any]
) -> tuple[list[str], list[dict[str, Any]]]:
    """回看本次选中 Hook 的字面证据与顺序。

    注意：返回的第一项是 **warnings（提示）而非 errors（硬门）**。证据词是否逐字
    命中属于语义层判断，字符串匹配会误伤写法正确、只是换了措辞的脚本，因此不再
    阻断 ok。这里只把「你在合同里承诺过、但脚本里没照面的点」如实提示给阅读者，
    让它自己判断是漏了还是有意换了说法。结构/时长/泄漏等确定性检查仍是硬门。
    """
    acceptance = contract.get("hook_acceptance_contract") or {}
    if acceptance.get("selected") is not True:
        return [], []

    starts: list[float] = []
    cursor = 0.0
    for duration in durations:
        starts.append(cursor)
        cursor += duration

    column_indexes = {name: index for index, name in enumerate(EXPECTED_COLUMNS)}
    warnings: list[str] = []
    checked: list[dict[str, Any]] = []
    first_hits: dict[str, tuple[float, int]] = {}

    for requirement in _as_list(acceptance.get("signature_requirements")):
        if not isinstance(requirement, dict):
            continue
        requirement_id = str(requirement.get("id") or "unnamed")
        deadline = float(
            requirement.get("deadline_seconds")
            or acceptance.get("opening_deadline_seconds")
            or 3.0
        )
        opening_required = bool(requirement.get("opening_required"))
        evidence = requirement.get("evidence") or {}
        requested_fields = [str(item) for item in _as_list(evidence.get("fields"))]
        field_indexes = [column_indexes[item] for item in requested_fields if item in column_indexes]
        if not field_indexes:
            warnings.append(f"Hook 验收项 {requirement_id} 没有可用的脚本字段，请检查 evidence.fields。")
            continue

        candidates: list[tuple[float, str]] = []
        for row_index, row in enumerate(rows):
            row_start = starts[row_index] if row_index < len(starts) else 999.0
            if opening_required and row_start >= deadline:
                continue
            candidates.append((row_start, " ".join(row[index] for index in field_indexes)))
        searchable = "\n".join(text for _, text in candidates).lower()
        all_of = [_norm(item) for item in _as_list(evidence.get("all_of")) if _norm(item)]
        any_of = [_norm(item) for item in _as_list(evidence.get("any_of")) if _norm(item)]
        missing_all = [item for item in all_of if item not in searchable]
        any_ok = not any_of or any(item in searchable for item in any_of)
        passed = not missing_all and any_ok
        checked.append(
            {
                "id": requirement_id,
                "passed": passed,
                "deadline_seconds": deadline if opening_required else None,
                "fields": requested_fields,
            }
        )
        if not passed:
            source_text = str(requirement.get("source_text") or "")
            scope = f"前 {deadline:g} 秒" if opening_required else "全片"
            missing = missing_all or any_of
            warnings.append(
                f"提示：Hook 验收项 {requirement_id} 可能未落地——{scope}的"
                f"{'/'.join(requested_fields)} 里没找到你在合同里承诺的证据「{' / '.join(missing)}」。"
                f"原始要求：{source_text}。请确认是漏写了，还是换了等价说法（换了说法可忽略本提示）。"
            )
            continue

        # 记录该要求在候选镜头中的最早出现位置，用于保序验收。
        terms = all_of + any_of
        hit: tuple[float, int] | None = None
        for row_start, candidate_text in candidates:
            lowered = candidate_text.lower()
            positions = [lowered.find(term) for term in terms if term in lowered]
            if positions:
                hit = (row_start, min(positions))
                break
        if hit is not None:
            first_hits[requirement_id] = hit

    if _norm(acceptance.get("sequence_policy")) in {"mechanism_order_required", "user_locked"}:
        ordered_ids = [str(item) for item in _as_list(acceptance.get("ordered_requirement_ids"))]
        observed = [first_hits.get(item) for item in ordered_ids]
        if all(item is not None for item in observed):
            concrete = [item for item in observed if item is not None]
            if concrete != sorted(concrete):
                warnings.append(
                    "提示：Hook 核心动作/状态的出现顺序与 ordered_requirement_ids 不一致——"
                    f"合同期望 {' → '.join(ordered_ids)}。如果是为了剧情顺滑而有意调整，请自行确认无碍。"
                )

    return warnings, checked


def _quality_evidence_errors(
    rows: list[list[str]], contract: dict[str, Any]
) -> tuple[list[str], list[dict[str, Any]]]:
    """按本项目编译的质量验收合同，回查最终分镜中的真实文本证据。

    注意：返回的第一项是 **warnings（提示）而非 errors（硬门）**。这里的「证据词
    在不在、顺序对不对」本质是对语义/创意的判断，用字符串匹配会误伤只是换了措辞的
    正确脚本，并把 Agent 拖进「为迁就词表反复改写」的空转。因此本函数不再阻断 ok，
    只把「Step 3 承诺过、但实际分镜里没照面的证据」如实提示出来，供阅读者自查是漏了
    还是换了等价说法。真正决定 ok 的是结构/时长/泄漏等确定性硬门。
    """
    acceptance = contract.get("quality_acceptance_contract") or {}
    requirements = _as_list(acceptance.get("requirements"))
    if not requirements:
        return [], []

    column_indexes = {name: index for index, name in enumerate(EXPECTED_COLUMNS)}
    warnings: list[str] = []
    checked: list[dict[str, Any]] = []
    first_hits: dict[str, tuple[int, int]] = {}

    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        requirement_id = str(requirement.get("id") or "unnamed")
        role = str(requirement.get("role") or "unspecified")
        requested_fields = [str(item) for item in _as_list(requirement.get("fields"))]
        field_indexes = [column_indexes[item] for item in requested_fields if item in column_indexes]
        if not field_indexes:
            warnings.append(
                f"说服质量验收项 {requirement_id} 没有可用的脚本字段，"
                "请检查 fields。"
            )
            continue

        candidates = [" ".join(row[index] for index in field_indexes).lower() for row in rows]
        searchable = "\n".join(candidates)
        all_of = [_norm(item) for item in _as_list(requirement.get("all_of")) if _norm(item)]
        any_of = [_norm(item) for item in _as_list(requirement.get("any_of")) if _norm(item)]
        missing_all = [item for item in all_of if item not in searchable]
        any_ok = not any_of or any(item in searchable for item in any_of)
        passed = bool(all_of or any_of) and not missing_all and any_ok
        checked.append(
            {
                "id": requirement_id,
                "role": role,
                "passed": passed,
                "fields": requested_fields,
            }
        )
        if not passed:
            missing = missing_all or any_of or ["未配置可验收文本"]
            source_text = str(requirement.get("source_text") or "")
            warnings.append(
                f"提示：说服质量验收项 {requirement_id}（{role}）可能未落地——"
                f"{'/'.join(requested_fields)} 里没找到证据「{' / '.join(missing)}」。"
                f"本项目要求：{source_text}。请确认是漏写了，还是换了等价说法（换了说法可忽略本提示）。"
            )
            continue

        terms = all_of + any_of
        for row_index, candidate_text in enumerate(candidates):
            positions = [candidate_text.find(term) for term in terms if term in candidate_text]
            if positions:
                first_hits[requirement_id] = (row_index, min(positions))
                break

    ordered_ids = [str(item) for item in _as_list(acceptance.get("ordered_requirement_ids"))]
    if ordered_ids:
        observed = [first_hits.get(item) for item in ordered_ids]
        if all(item is not None for item in observed):
            concrete = [item for item in observed if item is not None]
            if concrete != sorted(concrete):
                # 把实际先后（含镜号）摊开，便于阅读者一眼看出哪两项错位，无需去读校验器源码。
                actual = " → ".join(
                    f"{rid}(第{first_hits[rid][0] + 1}镜)"
                    for rid in ordered_ids
                    if first_hits.get(rid) is not None
                )
                warnings.append(
                    "提示：说服质量证据的出现顺序可能不理想——一般应先有产品动作，再出现可观察"
                    f"变化与结果/任务改变，最后才下判断或 CTA。合同期望 {' → '.join(ordered_ids)}，"
                    f"脚本里实际先后是 {actual}。若确有叙事需要如此安排，可忽略本提示。"
                )

    return warnings, checked


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def _load_contract(raw: str | None) -> dict[str, Any]:
    """加载 --contract。同时接受两种写法，调用方不必先落盘：

    1. JSON 文件路径：`--contract _internal/story_contract.json`
    2. 内联 JSON 字符串：`--contract '{"duration_seconds": 15}'`

    任何失败都抛 ContractInputError（中文自然语言），由 main() 打印成
    `{"ok": false, "errors": [...]}`，不再抛 traceback。
    """
    if raw is None:
        return {}
    text = raw.strip()
    if not text:
        return {}

    # 写法 2：内联 JSON。以 { 或 [ 开头即按内联解析，不去当路径找文件。
    if text.startswith("{") or text.startswith("["):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ContractInputError(
                f"--contract 传的内联 JSON 解析失败（{exc.msg}，第 {exc.lineno} 行第 {exc.colno} 列）："
                "请检查引号/逗号是否完整。内联写法示例："
                "--contract '{\"duration_seconds\": 15}'。"
            ) from None
        if not isinstance(data, dict):
            raise ContractInputError(
                "--contract 的内容必须是一个 JSON 对象（形如 {\"duration_seconds\": 15}），"
                f"当前是 {type(data).__name__}。"
            )
        return data

    # 写法 1：文件路径。
    path = Path(text)
    if not path.exists():
        raise ContractInputError(
            f"--contract 指定的文件不存在：{text}。"
            "两种写法都可以：① 先把合同写成 JSON 文件再传它的路径（注意相对路径是相对当前工作目录，"
            "跨目录时用绝对路径）；② 不落盘，直接传内联 JSON，例如 "
            "--contract '{\"duration_seconds\": 15}'。"
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
            f"--contract 文件 {text} 的顶层必须是 JSON 对象（形如 {{\"duration_seconds\": 15}}），"
            f"当前是 {type(data).__name__}。"
        )
    return data


def validate_story_text(text: str, contract: dict[str, Any] | None = None) -> dict[str, Any]:
    contract = contract or {}
    errors: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {}
    lines = text.splitlines()

    h1_lines = [line.strip() for line in lines if line.startswith("# ")]
    if h1_lines != ["# 故事脚本"]:
        errors.append("标题不对：全文有且只能有一个一级标题，且必须是「# 故事脚本」。")

    header_indexes = [i for i, line in enumerate(lines) if line.lstrip().startswith("|") and _cells(line) == EXPECTED_COLUMNS]
    if len(header_indexes) != 1:
        errors.append(
            "分镜表结构不对：全文必须有且只有一张 8 列表格，表头必须是「"
            + " | ".join(EXPECTED_COLUMNS)
            + "」。"
        )
        return {"ok": False, "errors": errors, "warnings": warnings, "details": details}

    header_index = header_indexes[0]
    if header_index + 1 >= len(lines) or not _is_separator(_cells(lines[header_index + 1])):
        errors.append("分镜表缺少合法的表头分隔行（表头下面那行 |---|---| 格式不对）。")

    table_indexes: set[int] = {header_index, header_index + 1}
    rows: list[list[str]] = []
    cursor = header_index + 2
    while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
        row = _cells(lines[cursor])
        table_indexes.add(cursor)
        if len(row) != len(EXPECTED_COLUMNS):
            errors.append(f"第 {cursor + 1} 行分镜的列数不对：必须正好是 {len(EXPECTED_COLUMNS)} 列。")
        else:
            rows.append(row)
        cursor += 1

    if not rows:
        errors.append("分镜表里没有任何镜头行。")

    bgm_indexes = [i for i, line in enumerate(lines) if line.strip().startswith("**全片 BGM**")]
    if len(bgm_indexes) != 1:
        errors.append("必须有且只有一行「**全片 BGM**」说明。")

    allowed_indexes = {i for i, line in enumerate(lines) if not line.strip()}
    allowed_indexes.update(table_indexes)
    allowed_indexes.update(bgm_indexes)
    allowed_indexes.update(i for i, line in enumerate(lines) if line.strip() == "# 故事脚本")
    extras = [lines[i].strip() for i in range(len(lines)) if i not in allowed_indexes and lines[i].strip()]
    if extras:
        errors.append("故事脚本里混入了多余的、用户不该看到的段落：这个文件只能包含「# 故事脚本」标题、那张分镜表和「**全片 BGM**」一行，请删掉其它内容。")
        details["extra_sections"] = extras[:8]

    for label, pattern in INTERNAL_PATTERNS:
        if pattern.search(text):
            errors.append(f"泄漏了内部工作流标签「{label}」:面向用户的故事脚本不能出现内部机制名/编号/字段名，请删除或改写。")
            details.setdefault("internal_labels", []).append(label)

    durations: list[float] = []
    for row in rows:
        match = DURATION_RE.search(row[1])
        if not match:
            errors.append(f"镜号 {row[0] or '?'} 的时长格式不对：时长列必须写成「数字+秒」或「数字+s」。")
            continue
        durations.append(float(match.group(1)))
    total = round(sum(durations), 3)
    details["duration_seconds"] = total
    expected_duration = contract.get("duration_seconds")
    if expected_duration is not None and abs(total - float(expected_duration)) > 0.2:
        errors.append(f"总时长对不上：各镜头时长加起来是 {total:g} 秒，但要求是 {float(expected_duration):g} 秒。")

    # 回看本次用户选中 Hook 派生的明确验收项，以及说服质量合同的证据落地情况。
    # 这两类都属于「语义是否落地」的判断——字符串匹配会误伤只是换了措辞的正确脚本，
    # 因此只作为 warnings（提示）返回，不参与 ok 判定，避免 Agent 为迁就词表反复空转。
    if len(durations) == len(rows):
        hook_warnings, hook_checked = _hook_evidence_errors(rows, durations, contract)
        warnings.extend(hook_warnings)
        if hook_checked:
            details["hook_requirements_checked"] = hook_checked

        quality_warnings, quality_checked = _quality_evidence_errors(rows, contract)
        warnings.extend(quality_warnings)
        if quality_checked:
            details["quality_requirements_checked"] = quality_checked

    errors = list(dict.fromkeys(errors))
    warnings = list(dict.fromkeys(warnings))
    return {"ok": not errors, "errors": errors, "warnings": warnings, "details": details}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("story_script")
    parser.add_argument(
        "--contract",
        help="内部合同：可传 JSON 文件路径，也可直接传内联 JSON，如 '{\"duration_seconds\": 15}'",
    )
    args = parser.parse_args()

    story_path = Path(args.story_script)
    if not story_path.exists():
        print(json.dumps({
            "ok": False,
            "errors": [f"要校验的故事脚本文件不存在：{args.story_script}。"
                       "请确认路径（相对路径是相对当前工作目录，跨目录时用绝对路径）。"],
        }, ensure_ascii=False, indent=2))
        return 1

    try:
        contract = _load_contract(args.contract)
    except ContractInputError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1

    text = story_path.read_text(encoding="utf-8")
    result = validate_story_text(text, contract)
    if result.get("warnings"):
        result["warnings_note"] = (
            "warnings 是提示、不阻塞通过：这些是合同里承诺过、但脚本里没逐字照面的证据点或顺序。"
            "请逐条判断——确属漏写就补进对应分镜；只是换了等价说法就忽略。不要为了字面命中把好句子改生硬。"
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())