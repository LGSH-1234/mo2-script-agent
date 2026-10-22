
#!/usr/bin/env python3
"""
video_splitter.py — 内置视频切分工具（本地化流程第 4 步用）

为什么内置：切分依赖 ffmpeg。本脚本**优先直接复用运行环境里已有的 ffmpeg**；只有当环境里
确实没有 ffmpeg 时，才自愈式地**自动安装一次** `imageio-ffmpeg`（它附带一份静态 ffmpeg 二进制，
免 sudo、覆盖 mp4/mov/mkv/webm/avi/flv/ts/3gp/ogg 等几乎所有主流容器）。因此**调用方（agent）
无需关心环境是否装过 ffmpeg，也无需先手动 pip install——直接调用切割即可**，脚本自己保证有
ffmpeg 可用，且安装最多只发生一次（不会反复 loop）。

ffmpeg 二进制解析顺序（命中即用，靠前优先）：
  1. 环境变量 IMAGEIO_FFMPEG_EXE 指向的二进制
  2. 环境里已有的系统 ffmpeg（PATH）—— 有就直接复用，免安装
  3. imageio-ffmpeg 已安装时自带的静态二进制
  4. 以上都没有 → 脚本内自动执行一次 `pip3 install imageio-ffmpeg` 再用其二进制
注意：imageio-ffmpeg 只带 ffmpeg、不带 ffprobe，故本脚本一律用 ffmpeg 读时长。

用法
----
按分段表切分（推荐，默认精确重编码，帧级精确、片段干净可直接喂生成模型）：
  python3 video_splitter.py split \
      --video /workspace/xxx/source.mp4 \
      --plan  /workspace/xxx/segments.json \
      --outdir /workspace/xxx/segments

单段临时切分（无需分段表，调试用）：
  python3 video_splitter.py cut --video src.mp4 --start 3.3 --end 6.7 --out seg.mp4

可选参数：
  --copy         用流拷贝(不重编码)：极快、无损，但切点只能落在关键帧，可能有零点几秒偏差；
                 默认关闭。喂 Seedance 用默认(重编码)更稳。
  --crf 18       重编码画质(越小越清晰、文件越大)，默认 18（视觉近无损）。
  --preset veryfast  重编码速度档，默认 veryfast。

输出
----
- 每段一个文件：{outdir}/seg_{index:03d}.mp4（H.264 + AAC，兼容性最好）
- stdout 打印一份结果 JSON：每段的 index / 期望时长 / 实际时长 / 输出路径 / 是否达标，
  以及 total_ok。调用方据此判断切分是否成功。
"""

import argparse
import json
import os
import re
import subprocess
import sys


# ----------------------------- ffmpeg 定位 ----------------------------- #
def _imageio_exe():
    """返回 imageio-ffmpeg 自带二进制路径；未安装或不可用返回 None。"""
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except Exception:
        pass
    return None


def resolve_ffmpeg() -> str:
    """
    定位可用的 ffmpeg（详见文件头 docstring 的解析顺序）：
      1) IMAGEIO_FFMPEG_EXE 环境变量
      2) 环境里已有的系统 ffmpeg（PATH）—— 优先复用，免安装
      3) imageio-ffmpeg 已装时自带的二进制
      4) 都没有 → 自动执行一次 `pip3 install imageio-ffmpeg` 再用（仅一次，不 loop）
    对调用方透明：agent 不必关心环境是否装过 ffmpeg，直接调用切割即可。
    """
    import shutil

    # 1) 显式环境变量
    env = os.environ.get("IMAGEIO_FFMPEG_EXE")
    if env and os.path.exists(env):
        return env

    # 2) 环境里已有的系统 ffmpeg —— 有就直接复用，免安装
    sys_ff = shutil.which("ffmpeg")
    if sys_ff:
        return sys_ff

    # 3) imageio-ffmpeg 已装则用其自带二进制
    exe = _imageio_exe()
    if exe:
        return exe

    # 4) 都没有 → 自动安装一次再用（按要求用 pip3 install imageio-ffmpeg）
    sys.stderr.write("[video_splitter] 环境中未找到 ffmpeg，自动安装 imageio-ffmpeg（仅此一次）…\n")
    try:
        subprocess.run(["pip3", "install", "imageio-ffmpeg"],
                       check=True, capture_output=True, text=True)
    except Exception as e:
        # pip3 不在 PATH 时退化到 python -m pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"],
                           check=True, capture_output=True, text=True)
        except Exception:
            sys.exit(
                "自动安装 imageio-ffmpeg 失败，且环境中也没有可用的 ffmpeg。\n"
                f"原始错误：{e}\n"
                "可手动执行：pip3 install imageio-ffmpeg"
            )

    exe = _imageio_exe()
    if exe:
        return exe
    sys.exit("已安装 imageio-ffmpeg，但仍未能定位其 ffmpeg 二进制，请检查安装环境。")


FFMPEG = None  # 延迟初始化


def ff() -> str:
    global FFMPEG
    if FFMPEG is None:
        FFMPEG = resolve_ffmpeg()
    return FFMPEG


# --------------------------- 时长解析（无 ffprobe） --------------------- #
_DUR_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)")


def probe_duration(path: str):
    """用 ffmpeg 自身解析容器时长（秒）。解析不到返回 None。"""
    r = subprocess.run(
        [ff(), "-hide_banner", "-i", path],
        capture_output=True, text=True,
    )
    m = _DUR_RE.search(r.stderr)
    if not m:
        return None
    h, mnt, s = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(s)


# ------------------------------- 单段切分 ------------------------------- #
def cut_one(video, start, end, out, copy=False, crf=18, preset="veryfast"):
    dur = round(float(end) - float(start), 3)
    if dur <= 0:
        raise ValueError(f"片段时长非正：start={start} end={end}")
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    if copy:
        # 流拷贝：-ss 放在 -i 前做快速定位；切点吸附到最近关键帧，可能有偏差
        cmd = [ff(), "-hide_banner", "-loglevel", "error",
               "-ss", str(start), "-to", str(end), "-i", video,
               "-c", "copy", "-avoid_negative_ts", "make_zero", out, "-y"]
    else:
        # 精确重编码：帧级精确、片段干净，兼容性最好，适合喂生成模型
        cmd = [ff(), "-hide_banner", "-loglevel", "error",
               "-ss", str(start), "-to", str(end), "-i", video,
               "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
               "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "128k",
               "-movflags", "+faststart", out, "-y"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"切分失败 {out}:\n{r.stderr.strip()}")
    actual = probe_duration(out)
    # 容差：重编码 0.15s，流拷贝因关键帧对齐放宽到 0.5s
    tol = 0.5 if copy else 0.15
    ok = actual is not None and abs(actual - dur) <= tol
    return {"expected": dur, "actual": actual, "ok": ok, "out": out}


# ------------------------------ 按分段表切 ------------------------------ #
# 单段硬下限：低于该秒数的片段绝不允许单独送视频生成工具（Seedance 对过短片段生成效果不稳定）。
MIN_SEGMENT_SECONDS = 4.0


def split_by_plan(video, plan_path, outdir, copy, crf, preset):
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    segments = plan.get("segments", [])
    if not segments:
        sys.exit("分段表里没有 segments。")
    os.makedirs(outdir, exist_ok=True)

    # 只有分成多段时才校验下限：单段（整片一段）本就是原视频，不受 4 秒下限约束。
    if len(segments) > 1:
        short = [
            s["index"] for s in segments
            if (s["end"] - s["start"]) < MIN_SEGMENT_SECONDS
        ]
        if short:
            sys.exit(
                "分段表存在低于 {}s 的片段（index={}）。"
                "禁止把低于 {}s 的片段单独送视频生成工具，请将其与相邻片段合并"
                "（不切断台词）后重试。".format(
                    MIN_SEGMENT_SECONDS, short, MIN_SEGMENT_SECONDS
                )
            )

    src_dur = probe_duration(video)
    results = []
    for seg in segments:
        idx = seg["index"]
        out = os.path.join(outdir, f"seg_{idx:03d}.mp4")
        res = cut_one(video, seg["start"], seg["end"], out, copy, crf, preset)
        res.update({
            "index": idx,
            "start": seg["start"],
            "end": seg["end"],
            "has_dialogue": seg.get("has_dialogue"),
        })
        results.append(res)

    covered = sum(r["expected"] for r in results)
    summary = {
        "video": video,
        "ffmpeg": ff(),
        "mode": "copy" if copy else "reencode",
        "source_duration": src_dur,
        "planned_coverage": round(covered, 3),
        "segment_count": len(results),
        "all_ok": all(r["ok"] for r in results),
        "segments": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["all_ok"] else 2


# --------------------------------- CLI --------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="内置视频切分工具（基于 imageio-ffmpeg 自带二进制）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("split", help="按分段表 JSON 批量切分")
    sp.add_argument("--video", required=True, help="源视频路径（/workspace 完整路径）")
    sp.add_argument("--plan", required=True, help="分段表 JSON 路径")
    sp.add_argument("--outdir", required=True, help="片段输出目录")
    sp.add_argument("--copy", action="store_true", help="流拷贝(无损极快、切点吸附关键帧)")
    sp.add_argument("--crf", type=int, default=18)
    sp.add_argument("--preset", default="veryfast")

    cp = sub.add_parser("cut", help="单段临时切分")
    cp.add_argument("--video", required=True)
    cp.add_argument("--start", required=True, type=float)
    cp.add_argument("--end", required=True, type=float)
    cp.add_argument("--out", required=True)
    cp.add_argument("--copy", action="store_true")
    cp.add_argument("--crf", type=int, default=18)
    cp.add_argument("--preset", default="veryfast")

    pr = sub.add_parser("probe", help="打印视频时长(秒)")
    pr.add_argument("--video", required=True)

    args = ap.parse_args()
    if args.cmd == "split":
        sys.exit(split_by_plan(args.video, args.plan, args.outdir,
                               args.copy, args.crf, args.preset))
    elif args.cmd == "cut":
        res = cut_one(args.video, args.start, args.end, args.out,
                      args.copy, args.crf, args.preset)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0 if res["ok"] else 2)
    elif args.cmd == "probe":
        d = probe_duration(args.video)
        print(json.dumps({"video": args.video, "duration": d}, ensure_ascii=False))
        sys.exit(0 if d is not None else 1)


if __name__ == "__main__":
    main()