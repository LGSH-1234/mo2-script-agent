#!/usr/bin/env python3
"""有界文本读取器：读一批就返回，并**明确告诉你是否已经读到文件末尾**。

存在意义：内置 Read 工具只返回 `cat -n` 行号，不会告诉你「读完没有」——
读 548 行文件的前 5 行，与读一个只有 5 行的文件，返回形态完全相同。
本脚本把「是否读完」直接算好返回，省掉模型自己 `wc -l` 再比对的额外一轮。

用法:
  python3 scripts/read_file.py <file> [--offset N] [--limit 300] [--max-chars 40000]
    --offset    从第几行开始读（1 基，默认 1）
    --limit     本批最多读多少行（默认 300）
    --max-chars 本批返回正文的字符硬上限（默认 40000）

输出:
  先按 `行号<TAB>内容` 打印本批正文，然后打印一行机器可读状态，形如:
  [read_status] total_lines=548 returned_lines=300 start_line=1 end_line=300 next_offset=301 read_complete=false char_capped=false
  - read_complete=true  → 已覆盖到文件末尾，可登记为「已读」
  - read_complete=false → 还有后续内容，必须用 next_offset 继续读，不得当读完
  - char_capped=true    → 本批因字符上限提前截断（未满 limit 行），继续用 next_offset 读剩余

  当 read_complete=false 时，状态行之后再打印一段**自然语言续读提示**，用大白话讲清
  「本文件还没读完、还剩多少行、下一条该怎么读」，并把可直接复制的续读命令填好——
  目的是让模型不会把半截内容当全文，读到 read_complete=true 为止。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="有界文本读取器，返回是否已读到末尾")
    parser.add_argument("file", help="要读取的文本文件路径")
    parser.add_argument("--offset", type=int, default=1, help="起始行（1 基，默认 1）")
    parser.add_argument("--limit", type=int, default=300, help="本批最多行数（默认 300）")
    parser.add_argument("--max-chars", type=int, default=40000, help="本批正文字符上限（默认 40000）")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"[read_status] error=file_not_found path={args.file}")
        return 2

    offset = max(1, args.offset)
    limit = max(1, args.limit)
    max_chars = max(1, args.max_chars)

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    total = len(lines)

    if offset > total:
        # 起点已越过末尾：无正文，直接判读完
        print(
            f"[read_status] total_lines={total} returned_lines=0 "
            f"start_line={offset} end_line={offset - 1} next_offset={total + 1} "
            f"read_complete=true char_capped=false"
        )
        return 0

    start = offset                      # 1 基
    hard_end = min(total, start + limit - 1)

    out: list[str] = []
    chars = 0
    char_capped = False
    last_line = start - 1
    for ln in range(start, hard_end + 1):
        rendered = f"{ln}\t{lines[ln - 1]}"
        # +1 预留换行
        if out and chars + len(rendered) + 1 > max_chars:
            char_capped = True
            break
        out.append(rendered)
        chars += len(rendered) + 1
        last_line = ln

    end_line = last_line
    read_complete = end_line >= total
    next_offset = total + 1 if read_complete else end_line + 1

    if out:
        sys.stdout.write("\n".join(out) + "\n")
    print(
        f"[read_status] total_lines={total} returned_lines={len(out)} "
        f"start_line={start} end_line={end_line} next_offset={next_offset} "
        f"read_complete={'true' if read_complete else 'false'} "
        f"char_capped={'true' if char_capped else 'false'}"
    )

    if not read_complete:
        remaining = total - end_line
        next_cmd = (
            f"python3 scripts/read_file.py {args.file} "
            f"--offset {next_offset} --limit {limit}"
        )
        # 自然语言续读提示：故意放在最末尾（最近性），用大白话而非机器标志，
        # 逼停「把半截当全文」——这是漏读的最高频形态。
        print(
            "\n"
            f"⚠️ 本文件还没读完：全文共 {total} 行，本批只读到第 {end_line} 行，"
            f"后面还剩 {remaining} 行没读。现在你手里的只是这个文件的一部分，"
            "不是全文，绝不能据此当作已读、也不能据此下判断或过任何门。"
            "请立刻用下面这条命令接着往下读（可直接复制），"
            "并一直重复到看见 read_complete=true 为止：\n"
            f"    {next_cmd}"
        )
        if char_capped:
            print(
                "（提示：本批是因为字符上限提前截断的，没读满 limit 行；"
                "如仍嫌单批太大可把 --limit 调小些，但无论如何都要读到末尾。）"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
