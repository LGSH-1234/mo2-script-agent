
#!/usr/bin/env python3
"""Generate a depth video from an input video using DeepAnything v2 (ONNX).

Pipeline: ffmpeg decode (rawvideo pipe) -> per-frame ONNX depth inference ->
ffmpeg encode (grayscale, near=bright). The depth video is delivered silent;
the source audio track (BGM) is extracted to a standalone file so it can be
muxed back into the final replicated video.

Output is capped at 720p (short side <= 720, never upscaled) and 30 fps.

Dependencies: numpy + onnxruntime (pip) + ffmpeg/ffprobe (binary).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import onnxruntime as ort

MODEL_URL = "https://lf-xiaoyunque.jianying.com/obj/pippit-app-buz/deepanything_v2_uint8.onnx"
# model + intermediates live outside /workspace so they never show up in the user's file view
WORK_DIR = Path("/tmp/depth_video")
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], np.float32)


def probe(path: str) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True, check=True,
    ).stdout
    info = json.loads(out)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    if video is None:
        sys.exit(f"error: no video stream in {path}")
    num, den = (video.get("avg_frame_rate") or "30/1").split("/")
    fps = (float(num) / float(den)) if float(den) else 30.0
    return {
        "width": int(video["width"]),
        "height": int(video["height"]),
        "fps": fps if fps > 0 else 30.0,
        "duration": float(info["format"].get("duration") or 0),
        "has_audio": any(s["codec_type"] == "audio" for s in info["streams"]),
    }


def ensure_model(path: Path, url: str) -> Path:
    if path.is_file() and path.stat().st_size > 1_000_000:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    print(f"downloading model -> {path}", flush=True)
    with urllib.request.urlopen(url, timeout=60) as resp, open(tmp, "wb") as f:
        while chunk := resp.read(1 << 20):
            f.write(chunk)
    tmp.rename(path)
    print(f"model ready ({path.stat().st_size / 1e6:.0f} MB)", flush=True)
    return path


def fit(width: int, height: int, short_cap: int, multiple: int) -> tuple[int, int]:
    """Scale so the short side is <= short_cap (no upscale), both dims rounded to `multiple`."""
    scale = min(1.0, short_cap / min(width, height))
    rnd = lambda v: max(multiple, int(round(v * scale / multiple)) * multiple)
    return rnd(width), rnd(height)


def precompress_if_needed(input_path: str, src: dict, disabled: bool = False) -> tuple[str, bool]:
    """If video short side > 720, pre-compress to 720p via ffmpeg to avoid decoding/inference slowdowns."""
    short_side = min(src["width"], src["height"])
    if disabled or short_side <= 720:
        return input_path, False

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    temp_720p = WORK_DIR / f"{Path(input_path).stem}_pre720p.mp4"
    print(f"input short side ({short_side}p) > 720p, pre-compressing to 720p -> {temp_720p}...", flush=True)

    vf = "scale='if(gt(a,1),-2,min(720,iw))':'if(gt(a,1),min(720,ih),-2)'"
    cmd = [
        "ffmpeg", "-v", "error", "-y", "-i", input_path,
        "-vf", vf, "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-c:a", "copy", str(temp_720p),
    ]
    ret = subprocess.run(cmd, capture_output=True, text=True)
    if ret.returncode != 0:
        # Fallback if stream copy fails on odd audio codec/container
        cmd_fallback = [
            "ffmpeg", "-v", "error", "-y", "-i", input_path,
            "-vf", vf, "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-c:a", "aac", str(temp_720p),
        ]
        ret = subprocess.run(cmd_fallback, capture_output=True, text=True)

    if ret.returncode == 0 and temp_720p.is_file():
        print(f"pre-compressed to 720p ({temp_720p.stat().st_size / 1e6:.1f} MB)", flush=True)
        return str(temp_720p), True

    print(f"warn: pre-compression failed ({ret.stderr.strip()}), using original input", flush=True)
    return input_path, False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="source video")
    ap.add_argument("output", help="output depth video (.mp4)")
    ap.add_argument("--model", default=str(WORK_DIR / "deepanything_v2_uint8.onnx"),
                    help="ONNX model path (auto-downloaded when missing)")
    ap.add_argument("--model-url", default=MODEL_URL)
    ap.add_argument("--bgm", default=None,
                    help="extracted BGM path (default: <output dir>/<output stem>_bgm.m4a)")
    ap.add_argument("--crf", type=int, default=14,
                    help="x264 CRF quality, lower = higher quality/bitrate (default 14)")
    ap.add_argument("--infer-size", type=int, default=378,
                    help="inference short side, rounded to /14 (default 378; "
                         "504 for finer edges at ~2.5x the CPU cost)")
    ap.add_argument("--max-fps", type=float, default=30.0)
    ap.add_argument("--no-precompress", action="store_true",
                    help="disable automatic 720p pre-compression when input short side > 720")
    args = ap.parse_args()

    src = probe(args.input)
    actual_input, is_temp = precompress_if_needed(args.input, src, args.no_precompress)
    if is_temp:
        src = probe(actual_input)

    fps = min(src["fps"], args.max_fps)
    iw, ih = fit(src["width"], src["height"], args.infer_size, 14)
    ow, oh = fit(src["width"], src["height"], 720, 2)
    total = max(1, int(round(src["duration"] * fps)))
    print(f"source {src['width']}x{src['height']} {src['fps']:.1f}fps "
          f"{src['duration']:.1f}s audio={'yes' if src['has_audio'] else 'no'}", flush=True)
    print(f"infer {iw}x{ih} -> output {ow}x{oh} @{fps:.1f}fps ~{total} frames", flush=True)

    sess = ort.InferenceSession(str(ensure_model(Path(args.model), args.model_url)),
                                providers=["CPUExecutionProvider"])

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    video_only = WORK_DIR / (out_path.stem + "_noaudio.mp4")
    raw_cache = WORK_DIR / (out_path.stem + "_raw.tmp")

    # ---- pass 1: inference; cache per-frame-normalized uint8 depth + bounds ----
    decoder = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", actual_input,
         "-vf", f"fps={fps},scale={iw}:{ih}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    frame_bytes = iw * ih * 3
    bounds = []
    n, t0 = 0, time.time()
    with open(raw_cache, "wb") as cache:
        while True:
            buf = decoder.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            rgb = np.frombuffer(buf, np.uint8).reshape(ih, iw, 3).astype(np.float32) / 255.0
            x = ((rgb - IMAGENET_MEAN) / IMAGENET_STD).transpose(2, 0, 1)[None]
            depth = sess.run(None, {"pixel_values": x})[0][0]
            f_lo, f_hi = np.percentile(depth, (1, 99))
            span = max(f_hi - f_lo, 1e-6)
            cache.write(np.clip((depth - f_lo) / span * 255, 0, 255).astype(np.uint8).tobytes())
            bounds.append((f_lo, span))
            n += 1
            if n % 60 == 0:
                rate = n / (time.time() - t0)
                print(f"  infer {n}/{total}  {rate:.1f} fps  eta {(total - n) / rate:.0f}s", flush=True)
    decoder.stdout.close()
    decoder.wait()
    if n == 0:
        sys.exit("error: decoded zero frames")

    # ---- pass 2: remap to global bounds (kills normalization flicker), encode ----
    los = np.array([b[0] for b in bounds])
    his = np.array([b[0] + b[1] for b in bounds])
    g_lo, g_hi = float(np.percentile(los, 5)), float(np.percentile(his, 95))
    g_span = max(g_hi - g_lo, 1e-6)
    encoder = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{iw}x{ih}", "-r", f"{fps}", "-i", "-",
         "-vf", f"scale={ow}:{oh}", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", str(args.crf), "-pix_fmt", "yuv420p", str(video_only)],
        stdin=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    prev = None
    with open(raw_cache, "rb") as cache:
        for f_lo, span in bounds:
            frame = np.frombuffer(cache.read(iw * ih), np.uint8).reshape(ih, iw)
            depth = frame.astype(np.float32) / 255.0 * span + f_lo
            gray = np.clip((depth - g_lo) / g_span, 0, 1)
            if prev is not None:
                # temporal de-flicker gate: damp sub-threshold jitter, pass real motion through
                diff = gray - prev
                gray = prev + np.where(np.abs(diff) < 0.04, diff * 0.25, diff)
            prev = gray
            encoder.stdin.write((gray * 255).astype(np.uint8).tobytes())
    encoder.stdin.close()
    raw_cache.unlink()
    if encoder.wait() != 0 or not video_only.is_file():
        sys.exit("error: ffmpeg encode failed")
    shutil.move(str(video_only), out_path)  # move (not replace): /tmp may be a different fs

    # extract BGM alongside the depth video, to be muxed into the replicated video later
    bgm_path = Path(args.bgm) if args.bgm else out_path.with_name(out_path.stem + "_bgm.m4a")
    bgm_note = "no (source had no audio)"
    if src["has_audio"]:
        ext = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", actual_input,
             "-map", "0:a:0", "-vn", "-c:a", "aac", "-b:a", "128k", str(bgm_path)],
            capture_output=True, text=True,
        )
        if ext.returncode != 0 and is_temp:
            # retry with original input if temp input failed
            ext = subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", args.input,
                 "-map", "0:a:0", "-vn", "-c:a", "aac", "-b:a", "128k", str(bgm_path)],
                capture_output=True, text=True,
            )
        if ext.returncode != 0:
            print(f"warn: BGM extract failed\n{ext.stderr}", flush=True)
            bgm_note = "no (extract failed)"
        else:
            bgm_note = str(bgm_path)

    if is_temp:
        Path(actual_input).unlink(missing_ok=True)

    result = probe(str(out_path))
    print(f"wrote {out_path}  {result['width']}x{result['height']} "
          f"{result['duration']:.1f}s {n} frames  BGM={bgm_note}", flush=True)


if __name__ == "__main__":
    main()