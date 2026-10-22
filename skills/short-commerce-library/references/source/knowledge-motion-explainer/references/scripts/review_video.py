
#!/usr/bin/env python3
"""Sparse, timestamp-aware final-video review frames. stdlib + ffmpeg/ffprobe only.

Produces evidence, never an automatic aesthetic or speech-sync verdict.
See ../review.md for the checkpoints format and the review/repair loop.
"""
import argparse
import bisect
import collections
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(command, timeout=300):
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise ValueError(f"Command failed ({command[0]}): {result.stderr[-4000:]}")
    return result.stdout


def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number in seconds")
    return float(value)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(video):
    # Decode metadata to index actual presentation timestamps, including VFR.
    # Only selected images are exported below; this is not dense image sampling.
    data = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                           "-show_frames", "-show_streams", "-show_format", "-show_entries",
                           "frame=best_effort_timestamp_time:stream=width,height,avg_frame_rate,duration:format=duration",
                           "-of", "json", str(video)]))
    if not data.get("streams"):
        raise ValueError("Input contains no video stream")
    raw = data.get("frames", [])
    if not raw or any("best_effort_timestamp_time" not in f for f in raw):
        raise ValueError("Cannot obtain a complete frame timestamp index")
    pts = [float(f["best_effort_timestamp_time"]) for f in raw]
    if any(not math.isfinite(t) for t in pts) or any(a >= b for a, b in zip(pts, pts[1:])):
        raise ValueError("Frame timestamps must be finite and strictly increasing")
    origin = pts[0]
    pts = [t - origin for t in pts]
    stream = data["streams"][0]
    duration = float(stream.get("duration") or data.get("format", {}).get("duration") or pts[-1])
    if not math.isfinite(duration) or duration < pts[-1]:
        duration = pts[-1]
    return pts, {"width": stream["width"], "height": stream["height"],
                 "avg_frame_rate": stream.get("avg_frame_rate"), "duration": duration,
                 "frame_count": len(pts), "first_pts": origin, "last_frame_time": pts[-1]}


def captions_from(data):
    if not isinstance(data, dict):
        raise ValueError("Timing JSON must be an object")
    field = "display_captions" if "display_captions" in data else "captions"
    if not isinstance(data.get(field), list):
        raise ValueError("Timing JSON must contain display_captions or captions: [{start, end, text}, ...]")
    cues = []
    for i, row in enumerate(data[field]):
        if not isinstance(row, dict):
            raise ValueError(f"Caption {i + 1} must be an object")
        a, b = number(row.get("start"), f"caption {i + 1} start"), number(row.get("end"), f"caption {i + 1} end")
        text = row.get("text")
        if a < 0 or b <= a or not isinstance(text, str) or not text.strip():
            raise ValueError(f"Invalid caption {i + 1}: need 0 <= start < end and non-empty text")
        if cues and a < cues[-1]["start"]:
            raise ValueError("Captions must be ordered by start time")
        cues.append({"start": a, "end": b, "text": text})
    return cues



def mux_captions(report, video_hash, timing_hash):
    if not isinstance(report, dict) or report.get("output_sha256") != video_hash:
        raise ValueError("Mux report output_sha256 does not match this final video")
    if report.get("input_sha256", {}).get("timing") != timing_hash:
        raise ValueError("Mux report timing hash does not match the supplied canonical timing JSON")
    subtitles = report.get("subtitles", {})
    mode = subtitles.get("mode")
    if mode == "explicitly_disabled":
        return []
    if mode != "ffmpeg_libass_burned" or not isinstance(subtitles.get("captions"), list):
        raise ValueError("Mux report must describe burned ASS captions or explicitly disabled subtitles")
    cues = []
    for i, item in enumerate(subtitles["captions"]):
        if not isinstance(item, dict) or not isinstance(item.get("display"), dict):
            raise ValueError(f"Invalid mux report caption {i + 1}")
        cues.append({"start": item.get("ass_start"), "end": item.get("ass_end"),
                     "text": item["display"].get("text")})
    return captions_from({"captions": cues})


def choose_points(pts, duration, cues, board, limit, mode="visual"):
    if mode not in ("visual", "captions", "full", "checkpoints"):
        raise ValueError("Unknown review mode")
    requests, issues = [], []

    def nearest(t):
        j = bisect.bisect_left(pts, t)
        if j == 0:
            return 0
        if j >= len(pts):
            return len(pts) - 1
        return j - 1 if t - pts[j - 1] <= pts[j] - t else j

    def add(t, kind, source, label, priority, frame=None):
        t = number(t, label)
        if t < 0 or t > duration + 0.001:
            issues.append({"code": "point_outside_video", "source": source, "time": t})
            return
        requests.append({"kind": kind, "source": source, "label": str(label),
                         "requested_time": t, "frame_index": nearest(t) if frame is None else frame,
                         "priority": priority})

    add(0, "endpoint", "video", "first frame", 0, 0)
    add(pts[-1], "endpoint", "video", "last frame", 0, len(pts) - 1)
    for i, c in enumerate(cues):
        cid = f"caption-{i + 1:03d}"
        if c["end"] > duration + 0.001:
            issues.append({"code": "caption_beyond_video", "source": cid, "end": c["end"]})
        if i and c["start"] < cues[i - 1]["end"]:
            issues.append({"code": "overlapping_captions", "source": cid})
        if mode not in ("captions", "full"):
            continue
        add((c["start"] + c["end"]) / 2, "caption_midpoint", cid, cid + " midpoint", 3)
        for side in ("start", "end"):
            t = c[side]
            if t > duration + 0.001:
                continue
            j = bisect.bisect_left(pts, t)
            # Actual adjacent presentation frames around the boundary, not t +/- an estimated fps.
            if j > 0:
                add(t, "caption_boundary", cid, cid + " " + side + " before", 4, j - 1)
            if j < len(pts):
                add(t, "caption_boundary", cid, cid + " " + side + " at-or-after", 4, j)
    scenes = board.get("scenes", [])
    points = board.get("checkpoints", [])
    if not isinstance(scenes, list) or not isinstance(points, list):
        raise ValueError("scenes and checkpoints must be arrays")
    if not scenes and mode in ("visual", "full"):
        issues.append({"code": "no_scene_representatives", "message": "No scenes supplied; checkpoints or caption samples do not establish per-scene review coverage."})
    scene_ids = set()
    for i, scene in enumerate(scenes):
        if not isinstance(scene, dict) or not isinstance(scene.get("events", []), list):
            raise ValueError("Each scene must be an object with an events array")
        sid = scene.get("id")
        if not isinstance(sid, str) or not sid.strip():
            raise ValueError("Each scene id must be a non-empty string")
        if sid in scene_ids:
            raise ValueError(f"Duplicate scene id: {sid}")
        scene_ids.add(sid)
        a, b = number(scene.get("start"), sid + " start"), number(scene.get("end"), sid + " end")
        if a < 0 or b <= a:
            raise ValueError(f"Invalid scene interval: {sid}")
        if mode == "captions":
            continue
        if "review_at" not in scene:
            issues.append({"code": "missing_scene_review_at", "source": sid,
                           "message": "Choose a settled representative frame manually; no scene-start or midpoint fallback."})
        else:
            t = number(scene["review_at"], sid + " review_at")
            if not a <= t < b:
                raise ValueError(f"review_at must satisfy scene.start <= review_at < scene.end: {sid}")
            label = scene.get("expectation", sid + " representative; inspect actual pixels")
            add(t, "scene_representative", sid, label, 1)
            actual = pts[nearest(t)]
            if not a <= actual < b:
                issues.append({"code": "representative_frame_outside_scene", "source": sid, "time": actual})
            if cues and not any(c["start"] <= actual < c["end"] for c in cues):
                issues.append({"code": "representative_without_expected_caption", "source": sid, "time": actual,
                               "message": "Canonical timing expects no caption here; inspect and reselect if this scene needs one."})
        for j, event in enumerate(scene.get("events", [])):
            if not isinstance(event, dict):
                raise ValueError("Each event must be an object")
            eid = sid + "/" + str(event.get("id", f"event-{j + 1}"))
            times = [number(event.get(k), eid + " " + k) for k in ("start", "peak", "end")]
            if not (a <= times[0] <= times[1] <= times[2] <= b):
                raise ValueError(f"Event must satisfy scene.start <= start <= peak <= end <= scene.end: {eid}")
            for role, t in zip(("before", "key", "after"), times):
                add(t, "mechanism", eid, eid + " " + role, 2)
    for i, point in enumerate(points):
        if not isinstance(point, dict):
            raise ValueError("Each checkpoint must be an object")
        add(point.get("time"), "checkpoint", str(point.get("id", f"point-{i + 1}")),
            point.get("label", f"checkpoint {i + 1}"), 2)
    candidates = collections.defaultdict(list)
    for r in requests:
        candidates[r["frame_index"]].append(r)
    selected = set()
    for priority in range(5):
        group = sorted(n for n, reasons in candidates.items()
                       if n not in selected and min(r["priority"] for r in reasons) == priority)
        space = limit - len(selected)
        if len(group) <= space:
            selected.update(group)
        elif space:
            # Spread any partial priority tier over the timeline, rather than only checking its beginning.
            selected.update(group[min(len(group) - 1, int((j + 0.5) * len(group) / space))] for j in range(space))
        if len(selected) == limit:
            break
    coverage = {}
    for kind in sorted({r["kind"] for r in requests}):
        rs = [r for r in requests if r["kind"] == kind]
        indices = {r["frame_index"] for r in rs}
        coverage[kind] = {"requested_events": len(rs), "covered_events": sum(r["frame_index"] in selected for r in rs),
                          "unique_frames": len(indices), "selected_frames": len(indices & selected)}
    frames, omitted = [], []
    for n in sorted(candidates):
        item = {"frame_index": n, "time": pts[n], "reasons": candidates[n]}
        if n not in selected:
            omitted.append(item)
            continue
        order = len(frames) + 1
        item.update({"id": f"F{order:03d}", "image": f"frames/frame-{order:03d}.png",
                     "thumbnail": f"thumbs/frame-{order:03d}.png",
                     "expected_caption": [c["text"] for c in cues if c["start"] <= pts[n] < c["end"]]})
        frames.append(item)
    return frames, omitted, coverage, issues


# Tiny built-in digits label contact cells without Pillow, drawtext or an installed font.
GLYPHS = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
    "F": ["111", "100", "110", "100", "100"], "S": ["111", "100", "111", "001", "111"],
    ".": ["000", "000", "000", "000", "010"], " ": ["000"] * 5,
}


def label_ppm(path, text, width=640, height=32):
    pixels = bytearray(bytes((20, 25, 33)) * width * height)
    for i, char in enumerate(text):
        for y, row in enumerate(GLYPHS[char]):
            for x, bit in enumerate(row):
                if bit == "1":
                    for dy in range(3):
                        for dx in range(3):
                            p = ((8 + y * 3 + dy) * width + 12 + i * 12 + x * 3 + dx) * 3
                            pixels[p:p + 3] = bytes((235, 237, 242))
    path.write_bytes(f"P6\n{width} {height}\n255\n".encode() + pixels)


def extract(video, output, frames, media):
    for name in ("frames", "thumbs"):
        (output / name).mkdir()
    selection = "+".join(f"eq(n\\,{f['frame_index']})" for f in frames)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(video), "-map", "0:v:0",
         "-vf", "select=" + selection, "-vsync", "0", "-frames:v", str(len(frames)),
         str(output / "frames/frame-%03d.png")])
    if len(list((output / "frames").glob("*.png"))) != len(frames):
        raise ValueError("Decoded output frame count differs from the planned review points")
    height = max(2, int(round(640 * media["height"] / media["width"] / 2) * 2))
    with tempfile.TemporaryDirectory(prefix="labels-", dir=output) as temp:
        for i, f in enumerate(frames, 1):
            label_ppm(Path(temp) / f"label-{i:03d}.ppm", f"{f['id']}  {f['time']:.3f}")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
             "-framerate", "1", "-i", str(output / "frames/frame-%03d.png"),
             "-framerate", "1", "-i", str(Path(temp) / "label-%03d.ppm"),
             "-filter_complex", f"[0:v]scale=640:{height},setsar=1[v];[v][1:v]vstack=inputs=2[out]",
             "-map", "[out]", "-frames:v", str(len(frames)), str(output / "thumbs/frame-%03d.png")])
    for page, first in enumerate(range(1, len(frames) + 1, 9), 1):
        count = min(9, len(frames) - first + 1)
        cols, rows = min(3, count), math.ceil(count / min(3, count))
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-framerate", "1",
             "-start_number", str(first), "-i", str(output / "thumbs/frame-%03d.png"),
             "-vf", f"tile={cols}x{rows}:nb_frames={count}:padding=12:margin=12:color=0x141921",
             "-frames:v", "1", "-q:v", "2", str(output / f"contact-{page:02d}.jpg")])


def checklist(manifest):
    m = manifest
    lines = ["# 成片检查清单", "", "状态：待实际看图与听音；生成检查材料不代表质量通过。", "",
             f"视频：{m['media']['width']}×{m['media']['height']}，{m['media']['duration']:.3f} 秒。",
             f"抽取 {len(m['frames'])} / {m['candidate_frames']} 个候选帧，上限 {m['max_frames']}；遗漏 {len(m['omitted'])} 个。", "",
             "**有遗漏：不能宣称字幕/机制全覆盖；用 omitted-points.json 补查。**" if m["omitted"] else "采样点已导出；仍需实际看图，且不代表逐帧审阅全片。", "",
             f"采样模式：{m['sampling_mode']}。优先保留首尾、每镜代表帧，再保留机制/指定点；字幕专项另加中点与边界。",
             "字幕时序未知：不能由空时间表推断画面无字幕或字幕合格。" if m["timing"]["caption_status"] == "unknown" else
             ("本版本明确无字幕。" if m["timing"]["caption_status"] == "disabled" else "expected_caption 来自字幕时间表，不是画面识别或同步验收。"), "",
             "| 类别 | 已覆盖事件 / 申请事件 |", "|---|---|"]
    for kind, c in m["coverage"].items():
        lines.append(f"| {kind} | {c['covered_events']} / {c['requested_events']} |")
    lines += ["", "## 逐镜检查", "", "联系图只作总览。逐张单独打开每镜代表帧，必要时放大；填写实际观察，不能只打勾或自评分。",
              "若主体还在入场、关键标签未到位或相关字幕不在屏，应人工重选 review_at 并重新抽帧；脚本不能判断动画到位。", "",
              "| 分镜 / 预期 | 代表帧 | 布局实际观察 | 文字实际观察 | 原理实际观察 | 风格实际观察 | 问题 / 修改 / 同点复查证据 | 状态 |",
              "|---|---|---|---|---|---|---|---|"]
    for scene in m["scene_reviews"]:
        def cell(value):
            return str(value).replace("|", "\\|").replace("\n", " ")
        frame = scene.get("frame")
        link = f"[{frame['id']} · {frame['time']:.3f}s]({frame['image']})" if frame else scene["status"]
        lines.append(f"| {cell(scene['id'])} / {cell(scene['expectation'])} | {link} | 未看图 | 未看图 | 未看图 | 未看图 | 待填写 | 未检查 |")
    if not m["scene_reviews"]:
        lines.append("| 未提供分镜；本轮不能确认逐镜覆盖 | — | — | — | — | — | 与首轮逐镜记录关联 | 未检查 |")
    lines += ["", "## 画面目视检查", "", "- [ ] 逐张看过所有分镜代表帧，四项实际观察及具体差距已记录；复杂机制再看前中后。",
              "- [ ] 对照主体、动作状态、关键标签预期；图中的方向、作用位置、比例和结果与已核实的知识一致。",
              "- [ ] 开场有主题相关的视觉锚点，入场及时且可追踪；每镜焦点明确，结尾完整。",
              "- [ ] 内部结构、动作方向、输入输出与同一对象接得上；动作前中后表达真实变化。",
              "- [ ] 字幕/标题/标签不叠压、不裁切，中文字体正常；缩略图下仍可读。",
              "- [ ] 首次有声字幕成片、修改字幕显示逻辑/时间轴或出现字幕闪烁遗漏时执行 captions（或 full）专项，对照边界邻帧检查出现与消失；普通视觉采样不能宣称字幕边界全覆盖。",
              "- [ ] 浏览器运行错误、资源加载、正反向 seek 另查；MP4 不含这些诊断。", "",
              "## 修改记录", "", "| 轮次 | 时间 / 帧 | 分镜预期 | 实际差距 | 修改 | 同点复查证据 | 状态 |",
              "|---|---|---|---|---|---|---|", "| 1 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 未检查 |",
              "| 2（需要返修时） | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 未检查 |", "",
              "先逐镜审阅，再返修、重渲染并同点复查。审美最多再做两轮聚焦优化，每轮处理 1–3 个具体问题；硬错或质量目标仍未满足时不得记录为通过。没有新问题不重复同一检查。", "",
              "## 成片播放检查", "",
              "- [ ] 静帧问题修复后，连续播放最后交付版本，实际核对转场、运动、阅读停留、口播完整性与字幕同步。",
              "播放版本 / SHA-256：待填写；实际观看与听音范围：待填写；发现问题与复查：待填写；状态：未检查。",
              "只有工具确实支持且已完成播放/听音才声明通过。无法播放或听音时，写明能力缺口；静帧、媒体摘要和命令成功都不能代替。之后再修改视频，须复查受影响画面并重新确认最后版本。", "",
              "没有看像素的能力：只报告机械检查和未完成的视觉验收；若有具体可执行反馈，可据此修改后重抽，仍不宣称审美合格。", "",
              "## 检查帧索引", "", "帧号和时间已写在缩略图下；以下预期内容不能代替看图。", ""]
    for f in m["frames"]:
        reasons = "; ".join(r["label"] for r in f["reasons"])
        lines.append(f"- [{f['id']} · {f['time']:.3f}s]({f['image']}) — {reasons}")
    if m["issues"]:
        lines += ["", "## 技术检查问题", "", "```json", json.dumps(m["issues"], ensure_ascii=False, indent=2), "```"]
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", required=True, type=Path, help="Final MP4 to review")
    p.add_argument("--timing", required=True, type=Path, help='Canonical JSON; prefer display_captions, fall back to captions. Use {"captions":[]} if silent')
    p.add_argument("--mux-report", type=Path, help="Optional matching mux report; validates video/timing hashes and uses actual quantized ASS boundaries")
    p.add_argument("--checkpoints", type=Path, help="Optional scenes/events and explicit checkpoints JSON; see ../review.md")
    p.add_argument("--mode", choices=("visual", "captions", "full"), default="visual", help="visual: authored scene representatives/events; captions: cue midpoints/boundaries; full: both")
    p.add_argument("--only-checkpoints", action="store_true", help="Supplemental review: only supplied checkpoints/scenes plus endpoints; do not resample captions")
    p.add_argument("--output", required=True, type=Path, help="New or empty directory; prior reviews are never overwritten")
    p.add_argument("--max-frames", type=int, default=48, help="2..240; default 48, omissions explicitly reported")
    args = p.parse_args()
    if args.only_checkpoints and not args.checkpoints:
        raise ValueError("--only-checkpoints requires --checkpoints")
    if not 2 <= args.max_frames <= 240:
        raise ValueError("--max-frames must be between 2 and 240")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise ValueError(f"Required tool not found: {tool}")
    video, timing = args.video.resolve(strict=True), args.timing.resolve(strict=True)
    output = args.output.resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Output must be a new or empty directory; use a new review-round directory")
    timing_data = load(timing)
    cues = captions_from(timing_data)
    caption_status = "timing_available" if cues else ("disabled" if timing_data.get("subtitle_mode") == "none" else "unknown")
    caption_field = "display_captions" if "display_captions" in timing_data else "captions"
    video_hash, timing_hash = digest(video), digest(timing)
    if args.mux_report:
        mux_report = load(args.mux_report)
        cues = mux_captions(mux_report, video_hash, timing_hash)
        caption_status = "disabled" if mux_report["subtitles"]["mode"] == "explicitly_disabled" else ("timing_available" if cues else "unknown")
        caption_field = "mux_report.subtitles.captions.ass_start/ass_end"
    board = load(args.checkpoints) if args.checkpoints else {}
    if not isinstance(board, dict):
        raise ValueError("Checkpoints JSON must be an object")
    pts, media = probe(video)
    mode = "checkpoints" if args.only_checkpoints else args.mode
    frames, omitted, coverage, issues = choose_points(pts, media["duration"], cues, board, args.max_frames, mode)
    if caption_status == "unknown":
        issues.append({"code": "caption_timing_unknown", "message": "No verified caption intervals; do not infer no subtitles or claim subtitle review passed."})
    scene_reviews = []
    for i, scene in enumerate(board.get("scenes", [])):
        sid = scene["id"]
        frame = next((f for f in frames if any(r["kind"] == "scene_representative" and r["source"] == sid for r in f["reasons"])), None)
        status = "not_in_mode" if mode == "captions" else ("missing_review_at" if "review_at" not in scene else ("extracted" if frame else "not_extracted"))
        scene_reviews.append({"id": sid, "review_at": scene.get("review_at"), "expectation": scene.get("expectation", "待填写主体、动作状态与关键标签"),
                              "status": status, "frame": {k: frame[k] for k in ("id", "time", "image")} if frame else None})
    output.mkdir(parents=True, exist_ok=True)
    manifest = {"schema_version": 2, "status": "extracting",
                "scope": "Sparse final-video pixel evidence only; no automated aesthetic, OCR, ASR, speech-sync or browser-runtime verdict.",
                "video": {"path": str(video), "sha256": video_hash},
                "timing": {"path": str(timing), "sha256": timing_hash, "caption_field": caption_field, "caption_status": caption_status,
                           "mux_report_verified": bool(args.mux_report),
                           "observation_source": timing_data.get("timing_source"),
                           "observed_captions": timing_data.get("observed_captions", timing_data.get("captions", []))}, "media": media,
                "sampling_mode": mode, "scene_reviews": scene_reviews,
                "max_frames": args.max_frames, "candidate_frames": len(frames) + len(omitted),
                "coverage": coverage, "issues": issues, "frames": frames, "omitted": omitted,
                "coverage_notice": "OMITTED POINTS: do not claim complete subtitle or mechanism coverage; use omitted-points.json." if omitted else "No candidate omitted by the cap; check input issues and inspect pixels before any verdict.",
                "sampling": "Actual presentation-frame index, deduplicated. Partial priority tiers spread across time. Frame metadata decoded once; only selected images exported."}
    if args.mux_report:
        manifest["mux_report"] = {"path": str(args.mux_report.resolve()), "sha256": digest(args.mux_report), "hash_bindings_verified": True}
    if args.checkpoints:
        manifest["checkpoints"] = {"path": str(args.checkpoints.resolve()), "sha256": digest(args.checkpoints)}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    extract(video, output, frames, media)
    if digest(video) != video_hash or digest(timing) != timing_hash:
        raise ValueError("Video or timing changed while review frames were being extracted; repeat with immutable final inputs")
    manifest["status"] = "awaiting_visual_and_audio_review"
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "checklist.md").write_text(checklist(manifest), encoding="utf-8")
    repeat = {"checkpoints": [{"id": f["id"], "time": f["time"], "label": "recheck " + f["id"] + ": " + "; ".join(r["label"] for r in f["reasons"])} for f in frames]}
    (output / "recheck-points.json").write_text(json.dumps(repeat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "omitted-points.json").write_text(json.dumps({"checkpoints": [{"time": f["time"], "label": "; ".join(r["label"] for r in f["reasons"])} for f in omitted]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "frames": len(frames), "candidates": len(frames) + len(omitted),
                      "omitted": len(omitted), "contact_sheets": len(list(output.glob("contact-*.jpg"))),
                      "status": manifest["status"], "coverage_notice": manifest["coverage_notice"], "mechanical_issues": issues}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)