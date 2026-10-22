
#!/usr/bin/env python3
"""Local, provider-neutral narration timing, muxing and focused media checks."""

import argparse
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unicodedata
import wave

RATE = 48000
MAX_CAPTION_CHARS = 32
MAX_CAPTION_SECONDS = 8.0
MAX_DURATION_DIFFERENCE = 1.0
MAX_TAIL_OVERRUN = 0.25


def run(args, cwd=None):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True, cwd=cwd)
    if result.returncode:
        raise ValueError(f"{args[0]} failed ({result.returncode}): {result.stderr[-4000:]}")
    return result.stdout, result.stderr


def require_tool(name):
    tool = shutil.which(name)
    if not tool:
        raise ValueError(f"Required executable not found: {name}")
    return tool


def local_file(value, base=None):
    path = Path(value).expanduser()
    if not path.is_absolute() and base:
        path = base / path
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"Input file does not exist: {path}")
    return path


def probe(path):
    out, _ = run([require_tool("ffprobe"), "-v", "error", "-show_streams",
                  "-show_format", "-of", "json", path])
    return json.loads(out)


def stream(info, kind):
    found = next((s for s in info.get("streams", []) if s.get("codec_type") == kind), None)
    if found is None:
        raise ValueError(f"No {kind} stream in media")
    return found


def duration(info, kind=None):
    preferred = stream(info, kind) if kind else {}
    for value in (preferred.get("duration"), info.get("format", {}).get("duration")):
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number) and number > 0:
            return number
    raise ValueError("Media duration unavailable or non-positive")


def number(value, name, minimum=0):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number >= {minimum}")
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a finite number >= {minimum}") from None
    if not math.isfinite(result) or result < minimum:
        raise ValueError(f"{name} must be a finite number >= {minimum}")
    return result


def fresh(paths):
    for path in paths:
        if path.exists() or path.is_symlink():
            raise ValueError(f"Refusing to overwrite: {path}")


def publish(source, target):
    # Same-filesystem hard link makes publication fail if a competing file appeared.
    os.link(source, target)


def seconds(frames):
    return round(frames / RATE, 6)


def timestamp(value):
    ms = round(value * 1000)
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def inspect_env(args):
    items = {}
    for name in ("ffmpeg", "ffprobe"):
        path = shutil.which(name)
        items[name] = {"available": bool(path), "path": path}
        if path:
            out, _ = run([path, "-version"])
            items[name]["version"] = out.splitlines()[0]
    subtitles = False
    if items["ffmpeg"]["available"]:
        out, err = run([items["ffmpeg"]["path"], "-hide_banner", "-filters"])
        subtitles = bool(re.search(r"\bsubtitles\s+V->V", out + err))
    font = local_file(args.font_file) if args.font_file else None
    return {"ok": all(v["available"] for v in items.values()) and subtitles,
            "python": sys.version.split()[0], "tools": items,
            "libass_subtitles_filter": subtitles,
            "font": {"path": str(font), "families": font_families(font), "sha256": sha256(font)} if font else None,
            "note": "Pass --font-file to inspect embedded family names without installing dependencies. Actual glyph availability is checked from libass render diagnostics. TTS/ASR providers are not bundled."}


def read_srt(path):
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    pattern = re.compile(r"^(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})$")
    cues = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = block.strip().splitlines()
        if lines and lines[0].strip().isdigit():
            lines = lines[1:]
        match = pattern.fullmatch(lines[0].strip()) if lines else None
        if not match or len(lines) < 2:
            raise ValueError("Invalid SRT block; expected timestamps and non-empty caption text")
        values = list(map(int, match.groups()))
        for offset in (0, 4):
            if values[offset + 1] >= 60 or values[offset + 2] >= 60:
                raise ValueError("SRT minutes and seconds must be below 60")
        a = (values[0] * 3600000 + values[1] * 60000 + values[2] * 1000 + values[3]) / 1000
        b = (values[4] * 3600000 + values[5] * 60000 + values[6] * 1000 + values[7]) / 1000
        caption = "\n".join(lines[1:]).strip()
        if not caption or b <= a or (cues and a < cues[-1]["end"]):
            raise ValueError("SRT cues must contain text, be ordered, positive-length and non-overlapping")
        cues.append({"start": a, "end": b, "text": caption})
    if not cues:
        raise ValueError("SRT contains no captions")
    return cues


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def display_intervals(cues, total, reported_duration):
    """Preserve observations; only bound a small final display overrun to media end."""
    warnings = []
    tolerance = min(MAX_DURATION_DIFFERENCE, max(0.25, total * 0.02))
    if reported_duration is not None:
        difference = reported_duration - total
        if abs(difference) > tolerance + 0.000001:
            raise ValueError(f"ASR heading duration differs too much from decoded audio ({reported_duration:.3f}s versus {total:.6f}s; limit {tolerance:.3f}s). Preserve the original response and verify its audio source; do not change the heading to pass validation.")
        if abs(difference) > 0.001:
            warnings.append({"code": "asr_duration_difference", "reported_seconds": reported_duration,
                             "decoded_seconds": total, "difference_seconds": round(difference, 6),
                             "message": "ASR heading retained verbatim. Decoded audio controls media duration; cue times are not scaled or shifted."})
    display = []
    for i, cue in enumerate(cues):
        item = dict(cue)
        if cue["start"] >= total:
            raise ValueError(f"Caption {i + 1} starts at or beyond decoded media end; cannot preserve its visible text")
        if cue["end"] > total:
            overrun = cue["end"] - total
            if i != len(cues) - 1 or overrun > MAX_TAIL_OVERRUN + 0.000001:
                raise ValueError(f"Caption {i + 1} extends beyond media by {overrun:.3f}s. Only a final display overrun up to {MAX_TAIL_OVERRUN:.2f}s is allowed; obtain verified timing for all other cases.")
            item["end"] = total
            warnings.append({"code": "final_caption_display_clamped", "caption_index": i + 1,
                             "observed_start": cue["start"], "observed_end": cue["end"],
                             "display_end": total, "overrun_seconds": round(overrun, 6),
                             "message": "Only display end is bounded to media end. Original speech timestamps remain in observed_captions and the source response; inspect the final spoken word."})
        if ass_centiseconds(item["end"]) <= ass_centiseconds(item["start"]):
            raise ValueError(f"Caption {i + 1} has no positive display duration at ASS centisecond precision")
        display.append(item)
    return display, warnings


def spoken_text(text):
    # Ignore punctuation and spacing only. Do not hide changed digits or words.
    return "".join(char for char in text if not char.isspace() and not unicodedata.category(char).startswith("P"))


def mapped_texts(cues, path, complete=False):
    """A text-only map cannot edit observed cue boundaries or omit translated cues."""
    mapping = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(mapping, dict):
        raise ValueError("Subtitle text map must be a JSON object of cue IDs to non-empty strings, e.g. {\"c001\": \"text\"}")
    valid = {f"c{i + 1:03d}" for i in range(len(cues))}
    if set(mapping) - valid or (complete and set(mapping) != valid):
        raise ValueError("Subtitle text map has unknown cue IDs or is missing required translations; preserve every original cue exactly once")
    if not mapping or any(not isinstance(text, str) or not spoken_text(text) for text in mapping.values()):
        raise ValueError("Subtitle text map values must be non-empty text strings, never timestamps or nested objects")
    return [{**cue, "text": mapping.get(f"c{i + 1:03d}", cue["text"])} for i, cue in enumerate(cues)], mapping


def validate_transcript(cues, transcript):
    expected = spoken_text(transcript.read_text(encoding="utf-8-sig"))
    actual = spoken_text("".join(cue["text"] for cue in cues))
    if not expected:
        raise ValueError("Narration transcript is empty")
    if expected != actual:
        changes = []
        for action, a, b, c, d in difflib.SequenceMatcher(None, expected, actual, autojunk=False).get_opcodes():
            if action != "equal":
                changes.append({"kind": action, "script": expected[a:b][:160], "recognized": actual[c:d][:160],
                                "script_offset": a, "recognized_offset": c})
        raise ValueError("Subtitle text differs from the full narration transcript after removing punctuation/whitespace: " +
                         json.dumps(changes[:12], ensure_ascii=False) +
                         ". Check the actual spoken words. Correct only verified transcription errors and preserve observed times; never replace missing speech with the script or guess timing.")


def validate_caption_size(cues, max_chars, max_seconds):
    if max_chars < 1 or max_seconds <= 0 or not math.isfinite(max_seconds):
        raise ValueError("Caption limits must be positive")
    if max_chars > MAX_CAPTION_CHARS or max_seconds > MAX_CAPTION_SECONDS:
        raise ValueError(f"Caption limits may only be lowered: maximum {MAX_CAPTION_CHARS} characters and {MAX_CAPTION_SECONDS:g} seconds. Obtain finer verified timing instead of raising the limits.")
    for i, cue in enumerate(cues, 1):
        chars = len(spoken_text(cue["text"]))
        span = cue["end"] - cue["start"]
        if chars > max_chars or span > max_seconds:
            raise ValueError(f"Caption {i} is too coarse ({chars} characters, {span:.3f}s; limits {max_chars}, {max_seconds}s). Obtain verified finer speech boundaries and import the updated SRT.")


def limiter_filter(ffmpeg):
    # FFmpeg 4.4 has alimiter but does not expose automatic latency compensation.
    stdout, stderr = run([ffmpeg, "-hide_banner", "-h", "filter=alimiter"])
    supported = bool(re.search(r"^\s*latency\s+", stdout + stderr, re.MULTILINE))
    base = "alimiter=limit=0.891251:level=false"
    return base + (":latency=true" if supported else ""), supported


def import_master(args):
    """Keep one continuous narration recording; import independently obtained timing."""
    audio, transcript = local_file(args.audio), local_file(args.transcript)
    corrections = local_file(args.text_corrections) if args.text_corrections else None
    if args.without_subtitles:
        if args.timing_source or corrections:
            raise ValueError("--without-subtitles cannot declare a timing provider or subtitle text corrections")
        if not spoken_text(transcript.read_text(encoding="utf-8-sig")):
            raise ValueError("Narration transcript is empty")
        cue_source, cues, reported_duration, timing_source = None, [], None, "none"
    else:
        if not args.timing_source:
            raise ValueError("--srt requires --timing-source {tts,asr,forced-alignment,manual}")
        cue_source = local_file(args.srt)
        cues, reported_duration = read_srt(cue_source), None
        timing_source = args.timing_source
    observed_cues = [dict(cue) for cue in cues]
    if corrections:
        cues, _ = mapped_texts(cues, corrections)
    if cues:
        validate_transcript(cues, transcript)
        validate_caption_size(cues, args.max_caption_chars, args.max_caption_seconds)
    original_hashes = {"audio": sha256(audio), "cue_source": sha256(cue_source) if cue_source else None, "transcript": sha256(transcript), "text_corrections": sha256(corrections) if corrections else None}
    output = Path(args.output_dir).expanduser().resolve()
    names = ["narration.wav", "timing.json"] + (["captions.srt"] if cues else [])
    targets = [output / name for name in names]
    fresh(targets)
    output.mkdir(parents=True, exist_ok=True)
    warnings = []
    with tempfile.TemporaryDirectory(prefix=".audio-master-", dir=output) as temp:
        stage = Path(temp)
        wav = stage / "narration.wav"
        run([require_tool("ffmpeg"), "-nostdin", "-v", "error", "-n", "-i", audio,
             "-map", "0:a:0", "-vn", "-ac", "1", "-ar", str(RATE), "-c:a", "pcm_s16le", wav])
        with wave.open(str(wav), "rb") as source:
            total = seconds(source.getnframes())
        if total <= 0:
            raise ValueError("Decoded narration is empty")
        display_cues, warnings = display_intervals(cues, total, reported_duration)
        segments = []
        for i, cue in enumerate(cues):
            sid = f"c{i + 1:03d}"
            segments.append({"id": sid, "start": cue["start"],
                             "end": cue["end"],
                             "scene_start": cue["start"] if i else 0.0,
                             "scene_end": cues[i + 1]["start"] if i + 1 < len(cues) else total,
                             "text": cue["text"]})
        blocks = [f"{i}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['text']}\n"
                  for i, c in enumerate(cues, 1)]
        if cues:
            (stage / "captions.srt").write_text("\n".join(blocks), encoding="utf-8")
        if original_hashes != {"audio": sha256(audio), "cue_source": sha256(cue_source) if cue_source else None, "transcript": sha256(transcript), "text_corrections": sha256(corrections) if corrections else None}:
            raise ValueError("An input changed during import; retry with immutable input files")
        bindings = {"source_audio": {"path": str(audio), "sha256": original_hashes["audio"]},
                    "transcript": {"path": str(transcript), "sha256": original_hashes["transcript"]},
                    "narration": {"path": "narration.wav", "sha256": sha256(wav)}}
        if cues:
            bindings.update({"cue_source": {"path": str(cue_source), "sha256": original_hashes["cue_source"]},
                             "captions": {"path": "captions.srt", "sha256": sha256(stage / "captions.srt")}})
        if corrections:
            bindings["text_corrections"] = {"path": str(corrections), "sha256": original_hashes["text_corrections"]}
        timing = {"schema_version": 3, "sample_rate": RATE, "duration": total,
                  "audio_source": str(audio), "timing_source": timing_source,
                  "subtitle_mode": "observed" if cues else "none",
                  "has_text_corrections": bool(corrections),
                  "asr_reported_duration": reported_duration,
                  "segments": segments, "captions": cues, "observed_captions": observed_cues,
                  "display_captions": display_cues, "warnings": warnings,
                  "bindings": bindings,
                  "text_validation": "Transcript matches after removing punctuation/whitespace; this does not establish ASR accuracy or audible synchronization." if cues else "No subtitles requested: transcript file is bound, but spoken content and timing were not transcribed or checked.",
                  "alignment": "observed_captions preserves original text and speech boundaries; captions permits only separately bound text corrections. display_captions may clamp a bounded final overrun. segments.scene_start/scene_end are visual coverage, never subtitle times. Audio remains one continuous recording, never split or retimed." if cues else "No ASR or subtitle timing exists. The full narration is one continuous recording; only an explicitly subtitle-free mux is permitted."}
        (stage / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fresh(targets)
        for target in targets:
            publish(stage / target.name, target)
    return {"ok": True, "duration": total, "audio_files": 1, "segments": len(cues),
            "files": {p.stem: str(p) for p in targets}, "warnings": warnings}



def verify_bindings(timing_path, voice):
    data = json.loads(timing_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 3:
        raise ValueError("Mux requires schema_version 3 timing.json from import-master; import the original master and matching SRT again")
    bindings = data.get("bindings")
    if not isinstance(bindings, dict):
        raise ValueError("timing.json lacks audio/subtitle hash bindings; run import-master first")
    subtitle_mode = data.get("subtitle_mode", "observed")
    if subtitle_mode not in ("observed", "none"):
        raise ValueError("Unsupported subtitle_mode in timing.json")
    required = ("source_audio", "transcript", "narration") if subtitle_mode == "none" else ("source_audio", "cue_source", "transcript", "narration", "captions")
    if data.get("has_text_corrections"):
        if subtitle_mode == "none":
            raise ValueError("A no-subtitle master cannot claim subtitle corrections")
        required += ("text_corrections",)
    if set(bindings) != set(required):
        raise ValueError("Hash bindings do not match the declared subtitle mode; import the master again")
    checked = {}
    for name in required:
        entry = bindings.get(name)
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str) or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", ""))):
            raise ValueError(f"Missing or invalid {name} hash binding")
        path = local_file(entry["path"], timing_path.parent)
        actual = sha256(path)
        if actual != entry["sha256"]:
            raise ValueError(f"{name} changed after subtitle import; refuse stale audio/subtitle pairing and rerun import-master using the final master")
        checked[name] = {"path": str(path), "sha256": actual}
    if sha256(voice) != checked["narration"]["sha256"]:
        raise ValueError("--voice does not match the master WAV bound to this timing.json; refuse old or replacement audio with stale subtitles")
    if subtitle_mode == "none":
        if (data.get("timing_source") != "none" or data.get("asr_reported_duration") is not None or
                any(data.get(key) != [] for key in ("captions", "observed_captions", "display_captions", "segments", "warnings"))):
            raise ValueError("No-subtitle timing must contain no observed or display timestamps, cues or ASR claims")
        if not spoken_text(Path(checked["transcript"]["path"]).read_text(encoding="utf-8-sig")):
            raise ValueError("Narration transcript is empty")
        number(data.get("duration"), "timing duration", 0.001)
        return data, checked
    if read_srt(Path(checked["captions"]["path"])) != data.get("captions"):
        raise ValueError("timing.json captions differ from its bound SRT; do not edit either timeline independently")
    if data.get("timing_source") not in ("tts", "asr", "forced-alignment", "manual"):
        raise ValueError("Unsupported timing source; import the matching SRT with its actual source")
    original_cues, original_duration = read_srt(Path(checked["cue_source"]["path"])), None
    if original_cues != data.get("observed_captions") or original_duration != data.get("asr_reported_duration"):
        raise ValueError("Canonical timing differs from its bound source SRT; reimport the matching source files")
    canonical_cues = mapped_texts(original_cues, Path(checked["text_corrections"]["path"]))[0] if data.get("has_text_corrections") else original_cues
    if canonical_cues != data["captions"]:
        raise ValueError("Canonical captions do not match original observations plus their bound text corrections")
    validate_transcript(canonical_cues, Path(checked["transcript"]["path"]))
    validate_caption_size(canonical_cues, MAX_CAPTION_CHARS, MAX_CAPTION_SECONDS)
    expected_display, expected_warnings = display_intervals(canonical_cues, number(data.get("duration"), "timing duration", 0.001), original_duration)
    if data.get("display_captions") != expected_display or data.get("warnings") != expected_warnings:
        raise ValueError("Display timeline or diagnostics differs from deterministic import rules; import again instead of editing timestamps")
    return data, checked


def font_families(path):
    """Read OpenType family names without installing another Python dependency."""
    raw = path.read_bytes()
    try:
        offsets = [0]
        if raw[:4] == b"ttcf":
            count = struct.unpack_from(">I", raw, 8)[0]
            if not 0 < count <= 128:
                raise ValueError("Invalid OpenType collection face count")
            offsets = list(struct.unpack_from(f">{count}I", raw, 12))
        families = set()
        for offset in offsets:
            if raw[offset:offset + 4] not in (b"\x00\x01\x00\x00", b"OTTO", b"true"):
                raise ValueError("--font-file must be a local OpenType/TrueType font, not WOFF, CSS or a URL")
            count = struct.unpack_from(">H", raw, offset + 4)[0]
            for index in range(count):
                tag, _, table, size = struct.unpack_from(">4sIII", raw, offset + 12 + index * 16)
                if table + size > len(raw):
                    raise ValueError("Invalid font table extent")
                if tag != b"name":
                    continue
                _, names, strings = struct.unpack_from(">HHH", raw, table)
                for n in range(names):
                    platform, encoding, _, name_id, length, start = struct.unpack_from(">6H", raw, table + 6 + n * 12)
                    if name_id not in (1, 16):
                        continue
                    data = raw[table + strings + start:table + strings + start + length]
                    codec = "utf-16-be" if platform in (0, 3) else "mac_roman" if platform == 1 and encoding == 0 else None
                    if codec:
                        families.add(data.decode(codec).strip())
        if not families:
            raise ValueError("Font has no readable family name")
        return sorted(families)
    except (struct.error, UnicodeError):
        raise ValueError("Invalid or unsupported OpenType font metadata") from None


def text_units(text):
    return sum(0 if unicodedata.combining(c) else 1.0 if unicodedata.east_asian_width(c) in ("W", "F") else 0.55 for c in text)


def caption_lines(text, limit):
    """Use at most two stable lines, with no per-word animation or time subdivision."""
    text = re.sub(r"\s+", " ", text).strip()
    if text_units(text) <= limit:
        return [text]
    candidates = []
    for i in range(1, len(text)):
        left, right = text[:i].rstrip(), text[i:].lstrip()
        if not left or not right or max(text_units(left), text_units(right)) > limit:
            continue
        # Keep Latin words and punctuation attached whenever another split fits.
        inside_word = text[i - 1].isascii() and text[i].isascii() and text[i - 1].isalnum() and text[i].isalnum()
        penalty = 100 if inside_word else 0
        penalty += 20 if right[0] in "，。！？；：、,.!?;:)]}）】》" else 0
        candidates.append((penalty + abs(text_units(left) - text_units(right)), left, right))
    if not candidates:
        raise ValueError("Caption cannot fit two readable lines. Obtain shorter verified cues or choose a font size that remains readable; do not truncate text.")
    _, left, right = min(candidates)
    return [left, right]


def ass_text(text):
    # ASS has no portable literal escape for every override character. Use visible
    # fullwidth equivalents only for its three control characters, never omit them.
    return text.translate(str.maketrans({"\\": "＼", "{": "｛", "}": "｝"}))


def ass_time(centiseconds):
    hours, remainder = divmod(centiseconds, 360000)
    minutes, remainder = divmod(remainder, 6000)
    secs, cs = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def ass_centiseconds(value):
    # Shared boundaries must quantize identically; opposing ceil/floor creates gaps.
    return math.floor(value * 100 + 0.5 + 1e-7)


def compile_ass(timing, width, height, family, fontsize):
    if not family or any(c in family for c in ",\r\n{}\\"):
        raise ValueError("Font family contains ASS control characters")
    if not math.isfinite(fontsize) or not 0.035 * height <= fontsize <= 0.065 * height:
        raise ValueError("Subtitle font size must be between 3.5% and 6.5% of frame height")
    side, bottom = round(width * 0.06), round(height * 0.055)
    line_limit = min(22.0, (width - 2 * side) / (fontsize * 1.05))
    if line_limit < 8:
        raise ValueError("Video is too narrow for readable two-line subtitles")
    header = ("[Script Info]\nScriptType: v4.00+\n"
              f"PlayResX: {width}\nPlayResY: {height}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
              "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
              f"Style: Narration,{family},{fontsize:.2f},&H00FFFFFF,&H00FFFFFF,&H00121212,&H80000000,0,0,0,0,100,100,0,0,1,{max(1.0, height / 360):.2f},0,2,{side},{side},{bottom},1\n\n"
              "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    events, review = [], []
    for index, cue in enumerate(timing["display_captions"], 1):
        start = ass_centiseconds(cue["start"])
        end = ass_centiseconds(cue["end"])
        if end <= start:
            raise ValueError(f"Caption {index} disappears at ASS precision")
        lines = caption_lines(cue["text"], line_limit)
        rendered = "\\N".join(ass_text(line) for line in lines)
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Narration,,0,0,0,,{rendered}\n")
        review.append({"caption_index": index, "observed": timing["observed_captions"][index - 1],
                       "canonical": timing["captions"][index - 1],
                       "display": cue, "ass_start": start / 100, "ass_end": end / 100,
                       "lines": lines, "control_characters_rendered_fullwidth": any(c in cue["text"] for c in "\\{}")})
    return header + "".join(events), review


def mux(args):
    ffmpeg = require_tool("ffmpeg")
    filter_list, filter_errors = run([ffmpeg, "-hide_banner", "-filters"])
    if not args.no_subtitles and not re.search(r"\bsubtitles\s+V->V", filter_list + filter_errors):
        raise ValueError("FFmpeg lacks the subtitles/libass filter. Use an available build with libass; do not substitute handwritten HTML subtitle timing.")
    video, voice = local_file(args.video), local_file(args.voice)
    timing_path = local_file(args.timing)
    timing, bindings = verify_bindings(timing_path, voice)
    if timing.get("subtitle_mode") == "none" and not args.no_subtitles:
        raise ValueError("This master was imported without subtitle timestamps. --no-subtitles is required for an explicitly subtitle-free video; otherwise obtain real timing and import again.")
    subtitle_texts = local_file(args.subtitle_texts) if args.subtitle_texts else None
    if subtitle_texts and args.no_subtitles:
        raise ValueError("--subtitle-texts cannot be used with --no-subtitles")
    subtitle_timing = timing
    if subtitle_texts:
        translated, _ = mapped_texts(timing["display_captions"], subtitle_texts, complete=True)
        subtitle_timing = {**timing, "display_captions": translated}
    if not args.no_subtitles and (not args.font_file or not args.font_family):
        raise ValueError("Default subtitle rendering requires --font-file and --font-family. Use --no-subtitles only when the user explicitly requests no subtitles.")
    font = local_file(args.font_file) if not args.no_subtitles else None
    families = font_families(font) if font else []
    if font and args.font_family not in families:
        raise ValueError("--font-family does not match the supplied font. Available names: " + json.dumps(families, ensure_ascii=False))
    output = Path(args.output).expanduser().resolve()
    if output.suffix.lower() != ".mp4":
        raise ValueError("Mux output must have an .mp4 extension")
    ass_output = output.with_name(output.stem + ".captions.ass")
    report_output = output.with_name(output.stem + ".mux-report.json")
    targets = [output, report_output] + ([ass_output] if font else [])
    fresh(targets)
    vinfo, ainfo = probe(video), probe(voice)
    if any(s.get("codec_type") == "audio" for s in vinfo.get("streams", [])):
        raise ValueError("--video must be a visual-only render with no audio stream. Use the bound single master WAV as --voice; also remove any HTML/canvas subtitles before rendering.")
    vstream = stream(vinfo, "video")
    video_seconds, voice_seconds = duration(vinfo, "video"), duration(ainfo, "audio")
    expected_duration = number(timing.get("duration"), "timing duration", 0.001)
    if abs(voice_seconds - expected_duration) > 0.001:
        raise ValueError("Narration duration differs from timing.json; import the actual final master before mux")
    target = max(video_seconds, voice_seconds)
    pad = max(0, voice_seconds - video_seconds)
    if pad > 0.25 + 0.000001:
        raise ValueError(f"Visual render is {pad:.3f}s shorter than narration. Re-render the visual timeline to cover the full master; only a tail difference up to 0.25s may repeat the final frame.")
    gain = number(args.bgm_gain, "bgm_gain")
    if gain > 1:
        raise ValueError("bgm_gain must be <= 1; this helper keeps music below narration")
    bgm = local_file(args.bgm) if args.bgm else None
    if bgm:
        duration(probe(bgm), "audio")
    width, height = int(vstream["width"]), int(vstream["height"])
    if width % 2 or height % 2:
        raise ValueError("H.264 yuv420p requires even width and height; render even dimensions first")
    output.parent.mkdir(parents=True, exist_ok=True)
    fontsize = args.font_size if args.font_size is not None else height * 0.047
    ass_content, caption_review = compile_ass(subtitle_timing, width, height, args.font_family, fontsize) if font else (None, [])
    input_hashes = {"video": sha256(video), "voice": sha256(voice), "timing": sha256(timing_path), "font": sha256(font) if font else None, "subtitle_texts": sha256(subtitle_texts) if subtitle_texts else None}
    warnings = list(timing["warnings"])
    if any(c["control_characters_rendered_fullwidth"] for c in caption_review):
        warnings.append({"code": "ass_control_characters_visible", "message": "Literal backslashes and braces are rendered as visible fullwidth equivalents to prevent ASS override injection; source text remains unchanged."})
    limiter, latency_compensated = limiter_filter(ffmpeg)
    if not latency_compensated:
        warnings.append({"code": "limiter_latency_not_compensated",
                         "message": "This FFmpeg lacks alimiter latency compensation; default lookahead can add about 5 ms. Check final sync."})
    if pad > 0.05:
        warnings.append({"code": "video_padded", "seconds": round(pad, 6),
                         "message": "Last video frame extended to preserve all narration; check whether the ending should be redesigned."})
    with tempfile.TemporaryDirectory(prefix=".audio-mux-", dir=output.parent) as temp:
        stage = Path(temp)
        staged = stage / "output.mp4"
        ass = stage / "captions.ass"
        if font:
            ass.write_text(ass_content, encoding="utf-8")
            (stage / "fonts").mkdir()
            shutil.copyfile(font, stage / "fonts" / ("subtitle" + font.suffix.lower()))
        command = [ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "info", "-n",
                   "-i", video, "-i", voice]
        if bgm:
            command += ["-stream_loop", "-1", "-i", bgm]
        subtitle_filter = ",subtitles=filename=captions.ass:fontsdir=fonts" if font else ""
        filters = [f"[0:v:0]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={pad:.6f}{subtitle_filter}[v]",
                   f"[1:a:0]asetpts=PTS-STARTPTS,aresample={RATE},aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=duration={target:.6f}[vo]"]
        if bgm:
            filters += [f"[2:a:0]asetpts=PTS-STARTPTS,aresample={RATE},aformat=channel_layouts=stereo,loudnorm=I=-28:TP=-3:LRA=11,volume={gain:.6f},atrim=duration={target:.6f}[bg]",
                        f"[vo][bg]amix=inputs=2:duration=first:normalize=0,{limiter}[a]"]
        else:
            filters += [f"[vo]{limiter}[a]"]
        command += ["-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
                    "-t", f"{target:.6f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", str(RATE),
                    "-movflags", "+faststart", staged]
        _, render_log = run(command, cwd=stage)
        if re.search(r"Glyph\s+0x[0-9A-Fa-f]+\s+not found|failed to find any fallback|Error opening|Unable to open", render_log, re.IGNORECASE):
            raise ValueError("Subtitle rendering reported missing glyphs or missing resources. Supply a font covering the actual narration; no final MP4 was published.")
        final_info = probe(staged)
        actual = duration(final_info)
        actual_audio = duration(final_info, "audio")
        if actual_audio + 0.05 < voice_seconds:
            raise ValueError(f"Encoded audio is shorter than narration: {actual_audio} < {voice_seconds}")
        verify_bindings(timing_path, voice)
        if input_hashes != {"video": sha256(video), "voice": sha256(voice), "timing": sha256(timing_path), "font": sha256(font) if font else None, "subtitle_texts": sha256(subtitle_texts) if subtitle_texts else None}:
            raise ValueError("An input changed during mux; rerun with immutable final inputs")
        report = {"ok": True, "output": str(output), "duration": actual,
                  "narration_duration": voice_seconds, "video_input_duration": video_seconds,
                  "audio_duration": actual_audio, "warnings": warnings, "bindings": bindings,
                  "input_sha256": input_hashes,
                  "subtitles": {"mode": "ffmpeg_libass_burned" if font else "explicitly_disabled", "ass_file": str(ass_output) if font else None,
                                "sha256": sha256(ass) if font else None, "font_file": str(font) if font else None, "font_family": args.font_family if font else None,
                                "font_size": fontsize, "captions": caption_review,
                                "subtitle_texts": {"path": str(subtitle_texts), "sha256": input_hashes["subtitle_texts"], "scope": "Complete cue text replacement only; original language transcript validation and observed times remain unchanged. Translation quality needs review."} if subtitle_texts else None,
                                "gaps": "Empty between observed intervals; no fades, fallback text, repeated last cue, karaoke or per-word animation.",
                                "precision": "ASS uses nearest-centisecond boundaries (at most 5 ms error). A shared cue boundary maps to one identical value, never a newly introduced gap; original timestamps remain unchanged. Sub-centisecond gaps may disappear at format precision."},
                  "output_sha256": sha256(staged),
                  "verification_scope": "Declared subtitle mode and exact input hashes are checked. When burning subtitles, canonical observed text/times, ASS event construction and successful libass encode are checked. Existing text in input video, visual beauty, audible synchronization and true ASR accuracy still require frame/listening review.",
                  "audio_processing": {"voice_target_lufs": -16, "bgm_target_lufs": -28 if bgm else None,
                                       "bgm_gain": gain if bgm else None, "ducking": False,
                                       "limiter_latency_compensated": latency_compensated,
                                       "note": "Single-pass loudnorm targets; final measured LUFS and true peak are not asserted."}}
        staged_report = stage / "report.json"
        staged_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fresh(targets)
        if font:
            publish(ass, ass_output)
        publish(staged_report, report_output)
        publish(staged, output)
    return {"ok": True, "output": str(output), "duration": actual, "warnings": warnings,
            "ass": str(ass_output) if font else None, "report": str(report_output), "subtitle_count": len(caption_review)}


def verify(args):
    media = local_file(args.input)
    info = probe(media)
    vs = stream(info, "video")
    audio = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    actual = duration(info)
    tolerance = number(args.tolerance, "tolerance")
    checks = []
    def check(name, passed, observed, expected):
        checks.append({"check": name, "ok": bool(passed), "actual": observed, "expected": expected})
    if args.duration is not None:
        expected = number(args.duration, "duration", 0.001)
        check("duration", abs(actual - expected) <= tolerance, actual,
              {"seconds": expected, "tolerance": tolerance})
    for key in ("width", "height"):
        expected = getattr(args, key)
        if expected is not None:
            check(key, vs.get(key) == expected, vs.get(key), expected)
    check("audio_present", bool(audio) or args.allow_no_audio, bool(audio), not args.allow_no_audio)
    check("video_codec", vs.get("codec_name") == "h264", vs.get("codec_name"), "h264")
    check("pixel_format", vs.get("pix_fmt") == "yuv420p", vs.get("pix_fmt"), "yuv420p")
    if audio:
        check("audio_codec", audio.get("codec_name") == "aac", audio.get("codec_name"), "aac")
    diagnostics = {}
    if args.detect_black:
        _, stderr = run([require_tool("ffmpeg"), "-nostdin", "-hide_banner", "-i", media,
                         "-map", "0:v:0", "-vf", "blackdetect=d=0.15:pix_th=0.10:pic_th=0.98",
                         "-an", "-f", "null", "-"])
        diagnostics["black_intervals"] = [dict(zip(("start", "end", "duration"), map(float, m)))
            for m in re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)", stderr)]
    if args.detect_silence and audio:
        _, stderr = run([require_tool("ffmpeg"), "-nostdin", "-hide_banner", "-i", media,
                         "-map", "0:a:0", "-af", "silencedetect=noise=-45dB:d=0.25", "-vn", "-f", "null", "-"])
        diagnostics["silence_events"] = [
            {"event": kind, "seconds": float(value)}
            for kind, value in re.findall(r"silence_(start|end|duration):\s*(-?[\d.]+)", stderr)]
    return {"ok": all(c["ok"] for c in checks), "input": str(media), "duration": actual,
            "width": vs.get("width"), "height": vs.get("height"), "checks": checks,
            "diagnostics": diagnostics,
            "scope": "Container/codec/timing checks only. Intentional dark frames and pauses need human review; semantics, legibility, lip sync and final loudness are not verified."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("inspect-env", help="Report local ffmpeg/ffprobe availability")
    p.add_argument("--font-file", help="Optional local OpenType font; report embedded family names")
    p.set_defaults(func=inspect_env)
    p = commands.add_parser("import-master", help="Import one continuous narration with real subtitle timing; never splits audio or estimates cue times")
    p.add_argument("--audio", required=True)
    sources = p.add_mutually_exclusive_group(required=True)
    sources.add_argument("--srt", help="Existing SRT with independently verified speech timestamps")
    sources.add_argument("--without-subtitles", action="store_true", help="Only when no subtitles are requested: bind the full master and transcript without ASR or invented timestamps")
    p.add_argument("--transcript", required=True, help="The full, final plain-text narration script")
    p.add_argument("--text-corrections", help="Optional JSON cue-ID to text map for independently verified transcription corrections; original subtitle text/times are preserved")
    p.add_argument("--timing-source", choices=("tts", "asr", "forced-alignment", "manual"), help="Required for --srt: actual origin of its timestamps")
    p.add_argument("--output-dir", required=True)
    p.add_argument("--max-caption-chars", type=int, default=MAX_CAPTION_CHARS, help="May only lower the 32-character maximum")
    p.add_argument("--max-caption-seconds", type=float, default=MAX_CAPTION_SECONDS, help="May only lower the 8-second maximum")
    p.set_defaults(func=import_master)
    p = commands.add_parser("mux", help="Burn canonical ASS captions into a visual-only render and encode one master narration")
    p.add_argument("--video", required=True, help="Visual-only video: no audio stream, no HTML/canvas subtitles")
    p.add_argument("--voice", required=True)
    p.add_argument("--timing", required=True, help="timing.json from the same import-master bundle; verifies narration and SRT hashes")
    p.add_argument("--font-file", help="Required unless --no-subtitles: local TTF/OTF/TTC file covering subtitle text")
    p.add_argument("--font-family", help="Required unless --no-subtitles: exact family name embedded in --font-file")
    p.add_argument("--font-size", type=float, help="Subtitle size in pixels; defaults to 4.7%% of frame height")
    p.add_argument("--no-subtitles", action="store_true", help="Explicit opt-out only when requested by the user; still verifies canonical narration/timing")
    p.add_argument("--subtitle-texts", help="Optional complete JSON cue-ID to translated subtitle text map; changes displayed text only, never source speech times")
    p.add_argument("--bgm")
    p.add_argument("--bgm-gain", type=float, default=1.0)
    p.add_argument("--output", required=True)
    p.set_defaults(func=mux)
    p = commands.add_parser("verify", help="Check expected media properties; optional black/silence diagnostics")
    p.add_argument("input")
    p.add_argument("--duration", type=float)
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--tolerance", type=float, default=0.1)
    p.add_argument("--allow-no-audio", action="store_true")
    p.add_argument("--detect-black", action="store_true")
    p.add_argument("--detect-silence", action="store_true")
    p.set_defaults(func=verify)
    args = parser.parse_args()
    try:
        result = args.func(args)
    except (ValueError, OSError, wave.Error, json.JSONDecodeError) as exc:
        result = {"ok": False, "error": str(exc), "command": args.command}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())