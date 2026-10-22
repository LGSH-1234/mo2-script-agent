
#!/usr/bin/env python3
"""Compose model-generated storyboard frames into a deterministic annotated sheet."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from contextlib import ExitStack
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - environment-specific guidance
    raise SystemExit(
        "Pillow is required. Install it in the active Python environment with: "
        "python3 -m pip install Pillow"
    ) from exc


LANDSCAPE_FRAME_HEIGHT = 576
LANDSCAPE_ANNOTATION_WIDTH = 1024
PORTRAIT_CARD_WIDTH = 648
PORTRAIT_ANNOTATION_HEIGHT = 720
PORTRAIT_HEADER_HEIGHT = 104
FOOTER_HEIGHT = 320
# Divider widths follow meaning, not axis: shots are strongly separated while
# each shot's frame and annotation remain visually paired.
SHOT_DIVIDER = 10
CONTENT_DIVIDER = 6
SAFE_MAX_DIMENSION = 5992
MULTIPLE = 8
RESAMPLING = getattr(Image, "Resampling", Image)

COLORS = {
    "frame_bg": "#171b1d",
    "annotation_bg": "#f7f8f6",
    "annotation_head": "#e8ebe8",
    "ink": "#202528",
    "muted": "#6a7377",
    "line": "#d8dcda",
    "overlay": "#15191c",
    "footer": "#171b1d",
    "footer_line": "#454c50",
    "footer_title": "#aeb7bb",
    "divider": "#30383c",
    "white": "#ffffff",
}

FONT_CANDIDATES = (
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Medium.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/msyh.ttc",
)

RATIO_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*$")
TIMECODE_PATTERN = re.compile(
    r"([0-9]{2,}):([0-5][0-9])(?:\.([0-9]{1,3}))?-"
    r"([0-9]{2,}):([0-5][0-9])(?:\.([0-9]{1,3}))?"
)
SHOT_INSTRUCTION_FIELDS = ("shot_size", "visual", "transition", "audio", "voiceover")


def parse_video_ratio(value: Any) -> tuple[float, float, str]:
    text = str(value or "").strip()
    match = RATIO_PATTERN.fullmatch(text)
    if not match:
        raise ValueError("video ratio must use positive width:height notation, for example 16:9")
    width = float(match.group(1))
    height = float(match.group(2))
    if width <= 0 or height <= 0:
        raise ValueError("video ratio width and height must both be positive")

    def clean(number: float) -> str:
        if number.is_integer():
            return str(int(number))
        return f"{number:.6g}"

    return width, height, f"{clean(width)}:{clean(height)}"


def rounded_multiple(value: float) -> int:
    return max(MULTIPLE, round(value / MULTIPLE) * MULTIPLE)


def layout_for_ratio(width: float, height: float) -> str:
    return "vertical-list" if width >= height else "horizontal-strip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compose a ratio-aware annotated storyboard sheet. Landscape frames use "
            "vertical rows with notes on the right; portrait frames use a horizontal "
            "strip with notes below."
        )
    )
    parser.add_argument("--manifest", required=True, type=Path, help="UTF-8 JSON manifest")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    parser.add_argument(
        "--video-ratio",
        help="Override manifest video_ratio using width:height notation; defaults to 16:9",
    )
    parser.add_argument(
        "--split-by-part",
        action="store_true",
        help=(
            "Group runtime_shots (or shots when absent) by their 'part' field and write one "
            "-part-YY PNG per independent video-generation call"
        ),
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--images",
        nargs="+",
        type=Path,
        help="Individual frame images in storyboard order",
    )
    source.add_argument(
        "--grid-image",
        type=Path,
        help="One row-major contact sheet containing up to rows*cols used cells",
    )
    source.add_argument(
        "--grid-images",
        nargs="+",
        type=Path,
        help="Ordered contact sheets, each containing up to rows*cols used cells",
    )
    parser.add_argument("--grid-rows", type=int, default=3)
    parser.add_argument("--grid-cols", type=int, default=3)
    parser.add_argument(
        "--grid-margin",
        type=int,
        default=0,
        help="Outer margin in source-grid pixels before equal splitting",
    )
    parser.add_argument(
        "--grid-gap",
        type=int,
        default=0,
        help="Separator width in source-grid pixels before equal splitting",
    )
    parser.add_argument(
        "--grid-trim-ratio",
        type=float,
        default=0.008,
        help="Trim this fraction from every split cell edge to remove generated separators",
    )
    parser.add_argument(
        "--grid-shot-counts",
        nargs="+",
        type=int,
        help=(
            "Used row-major cells in each contact sheet. Counts must be positive, "
            "must not exceed rows*cols, and must sum to the manifest shot count. "
            "Trailing cells are treated as diagnostic non-shot film-leader cells."
        ),
    )
    parser.add_argument(
        "--fit",
        choices=("contain", "cover"),
        default="contain",
        help="How each source frame fits its target-ratio area",
    )
    parser.add_argument("--font", type=Path, help="CJK-capable .ttf/.otf/.ttc font")
    dimension = parser.add_mutually_exclusive_group()
    dimension.add_argument(
        "--max-dimension",
        type=int,
        default=SAFE_MAX_DIMENSION,
        help="Final width and height cap; runtime video inputs must keep this below 6000",
    )
    dimension.add_argument(
        "--no-max-dimension",
        action="store_true",
        help=(
            "Do not downscale the complete creative preview. Direct video input "
            "still requires checking actual target limits; do not use this for "
            "internal runtime sheets."
        ),
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON manifest: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Manifest must be a JSON object")
    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("Manifest must contain a non-empty 'shots' array")
    frame_ids: set[str] = set()
    for index, shot in enumerate(shots, start=1):
        if not isinstance(shot, dict):
            raise ValueError(f"Shot {index} must be a JSON object")
        required = ("timecode", *SHOT_INSTRUCTION_FIELDS)
        missing = [key for key in required if key not in shot]
        if missing:
            raise ValueError(f"Shot {index} is missing fields: {', '.join(missing)}")
        # Storyboard rows align one-to-one with blueprint shots and their
        # representative frames: number is strictly consecutive 1..N, each row
        # carries a unique frame_id for the same-numbered frame, and
        # blueprint_shots is fixed to [number] (no many-to-many mapping).
        number = shot.get("number")
        if isinstance(number, bool) or not isinstance(number, int) or number != index:
            raise ValueError(
                f"Shot {index} 'number' must be the strictly consecutive integer {index}"
            )
        frame_id = shot.get("frame_id")
        if not isinstance(frame_id, str) or not frame_id.strip():
            raise ValueError(f"Shot {index} needs a non-empty 'frame_id' string")
        if frame_id.rsplit("/", 1)[-1] != f"{number:02d}":
            raise ValueError(
                f"Shot {index} 'frame_id' must reference the same-numbered frame "
                f"(ending /{number:02d}) but got: {frame_id}"
            )
        if frame_id in frame_ids:
            raise ValueError(f"Duplicate frame_id in storyboard rows: {frame_id}")
        frame_ids.add(frame_id)
        blueprint_shots = shot.get("blueprint_shots")
        if blueprint_shots != [number]:
            raise ValueError(
                f"Shot {index} 'blueprint_shots' must be exactly [{number}] under the "
                "one-shot-one-frame contract"
            )

    global_info = data.get("global_info")
    if not isinstance(global_info, dict) or not 1 <= len(global_info) <= 4:
        raise ValueError("'global_info' must be an object containing 1 to 4 titled sections")
    video_ratio = data.get("video_ratio")
    if video_ratio is not None:
        parse_video_ratio(video_ratio)
    parts = data.get("parts")
    if parts is not None:
        if not isinstance(parts, dict):
            raise ValueError("'parts' must be an object keyed by positive part number")
        for raw_part, part_info in parts.items():
            try:
                part_number = int(raw_part)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid part key: {raw_part}") from exc
            if part_number < 1 or not isinstance(part_info, dict):
                raise ValueError("Every part key must be positive and map to an object")
            handoff = part_info.get("handoff")
            if handoff is not None and not isinstance(handoff, str):
                raise ValueError(f"Part {part_number} handoff must be text")
    if "runtime_shots" in data:
        validate_runtime_shots(data)
    return data


def complete_sheet_execution_hint(output: Path) -> dict[str, Any]:
    return {
        "path": str(output.resolve()),
        "instruction": (
            "This command result identifies the compositor-produced storyboard overview "
            "for this video. "
            "For direct visual execution, attach this exact path as the first ImageList "
            "entry of sandbox_generate_video. Mentioning the path in Prompt or PromptPath "
            "is not an attachment. If this package is later split into multiple video "
            "calls, use the recorded part_sheet facts produced by the split compositor run."
        ),
    }


def part_sheet_execution_hint(outputs: list[dict[str, Any]]) -> dict[str, Any]:
    part_paths = {
        str(result["part"]): result["output"]
        for result in sorted(outputs, key=lambda result: int(result["part"]))
    }
    return {
        "part_paths": part_paths,
        "instruction": (
            "This command result identifies the compositor-produced part sheets for this "
            "runtime manifest. Record each path through its ready part_sheet requirement. "
            "For generation-input-part-YY.md, attach only that part's recorded sheet as "
            "the first storyboard ImageList entry of sandbox_generate_video. Do not attach "
            "the complete source grid or any other part sheet to a split call."
        ),
    }


def resolve_font(font_path: Path | None) -> Path:
    if font_path:
        if not font_path.is_file():
            raise ValueError(f"Font not found: {font_path}")
        return font_path
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            return path
    raise ValueError("No CJK-capable font found. Pass one explicitly with --font")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size, index=0)


def open_rgb(path: Path) -> Image.Image:
    if not path.is_file():
        raise ValueError(f"Image not found: {path}")
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGBA")
    background = Image.new("RGBA", image.size, COLORS["frame_bg"])
    background.alpha_composite(image)
    return background.convert("RGB")


def split_grid(
    path: Path,
    rows: int,
    cols: int,
    margin: int,
    gap: int,
    trim_ratio: float,
) -> list[Image.Image]:
    if rows < 1 or cols < 1:
        raise ValueError("Grid rows and columns must be positive")
    if margin < 0 or gap < 0:
        raise ValueError("Grid margin and gap cannot be negative")
    if not 0 <= trim_ratio < 0.2:
        raise ValueError("--grid-trim-ratio must be between 0 and 0.2")

    image = open_rgb(path)
    available_width = image.width - (2 * margin) - ((cols - 1) * gap)
    available_height = image.height - (2 * margin) - ((rows - 1) * gap)
    if available_width <= 0 or available_height <= 0:
        raise ValueError("Grid margin/gap leaves no usable image area")

    cell_width = available_width / cols
    cell_height = available_height / rows
    cells: list[Image.Image] = []
    for row in range(rows):
        for col in range(cols):
            left = margin + (col * gap) + round(col * cell_width)
            top = margin + (row * gap) + round(row * cell_height)
            right = margin + (col * gap) + round((col + 1) * cell_width)
            bottom = margin + (row * gap) + round((row + 1) * cell_height)
            trim_x = round((right - left) * trim_ratio)
            trim_y = round((bottom - top) * trim_ratio)
            crop = (left + trim_x, top + trim_y, right - trim_x, bottom - trim_y)
            if crop[2] <= crop[0] or crop[3] <= crop[1]:
                raise ValueError("Grid trim removed an entire cell")
            cells.append(image.crop(crop))
    return cells


def source_images(args: argparse.Namespace, manifest: dict[str, Any]) -> tuple[list[Image.Image], str]:
    shot_count = len(manifest["shots"])
    grid_paths = [args.grid_image] if args.grid_image else args.grid_images
    if grid_paths:
        capacity = args.grid_rows * args.grid_cols
        if args.grid_shot_counts:
            used_counts = args.grid_shot_counts
            if len(used_counts) != len(grid_paths):
                raise ValueError(
                    "--grid-shot-counts must provide one count for each contact sheet"
                )
            if any(count < 1 or count > capacity for count in used_counts):
                raise ValueError(
                    f"Every grid shot count must be between 1 and {capacity}"
                )
            if sum(used_counts) != shot_count:
                raise ValueError(
                    "Grid shot counts must sum exactly to the manifest shot count "
                    f"({shot_count})"
                )
        else:
            expected_grids = math.ceil(shot_count / capacity)
            if len(grid_paths) != expected_grids:
                raise ValueError(
                    f"Shot count {shot_count} requires {expected_grids} contact sheet(s) "
                    f"at {capacity} cells each; received {len(grid_paths)}. Use "
                    "--grid-shot-counts when diagnostic non-shot tail cells occur before the "
                    "final source sheet."
                )
            used_counts = [capacity] * (expected_grids - 1)
            used_counts.append(shot_count - sum(used_counts))

        images = []
        for grid_path, used_count in zip(grid_paths, used_counts):
            cells = split_grid(
                grid_path,
                args.grid_rows,
                args.grid_cols,
                args.grid_margin,
                args.grid_gap,
                args.grid_trim_ratio,
            )
            images.extend(cells[:used_count])
        source_mode = "grid" if len(grid_paths) == 1 else "grids"
    elif args.images:
        if args.grid_shot_counts:
            raise ValueError("--grid-shot-counts requires --grid-image or --grid-images")
        images = [open_rgb(path) for path in args.images]
        source_mode = "individual"
    else:
        if args.grid_shot_counts:
            raise ValueError("--grid-shot-counts requires --grid-image or --grid-images")
        paths = [shot.get("image") for shot in manifest["shots"]]
        if any(not value for value in paths):
            raise ValueError(
                "Provide --grid-image, --images, or an 'image' path for every manifest shot"
            )
        images = [open_rgb(Path(value)) for value in paths]
        source_mode = "manifest"

    if len(images) != shot_count:
        raise ValueError(
            f"Image count ({len(images)}) must exactly match shot count ({shot_count})"
        )
    return images, source_mode


def wrap_text(
    draw: ImageDraw.ImageDraw,
    value: Any,
    text_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return ["None"]

    lines: list[str] = []
    paragraphs = re.split(r"\r?\n", text)
    for paragraph in paragraphs:
        paragraph = re.sub(r"[ \t]+", " ", paragraph.strip())
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and draw.textlength(candidate, font=text_font) > max_width:
                lines.append(current.rstrip())
                current = char.lstrip()
            else:
                current = candidate
        if current or not lines:
            lines.append(current.rstrip())
    return lines


def joined(*values: Any) -> str:
    parts = [str(value).strip() for value in values if str(value or "").strip()]
    return "; ".join(parts)


def annotation_fields(shot: dict[str, Any]) -> list[tuple[str, str]]:
    fields = [
        ("Visual Action", joined(shot.get("visual"), shot.get("action"))),
    ]
    if str(shot.get("product") or "").strip():
        fields.append(("Product Presence", str(shot["product"]).strip()))
    fields.extend(
        [
            ("Camera / Transition", joined(shot.get("camera"), shot.get("transition"))),
            ("Audio", str(shot.get("audio") or "None").strip()),
            ("Voiceover", str(shot.get("voiceover") or "None").strip()),
        ]
    )
    return fields


def field_layout(
    draw: ImageDraw.ImageDraw,
    fields: Iterable[tuple[str, str]],
    font_path: Path,
    font_size: int,
    max_width: int,
) -> tuple[list[tuple[str, list[str]]], int, int]:
    value_font = font(font_path, font_size)
    line_height = math.ceil(font_size * 1.34)
    gap = max(10, math.ceil(font_size * 0.38))
    layout: list[tuple[str, list[str]]] = []
    total_height = 0
    for label, value in fields:
        lines = wrap_text(draw, value, value_font, max_width)
        layout.append((label, lines))
        total_height += max(1, len(lines)) * line_height
        total_height += gap
    if layout:
        total_height -= gap
    return layout, total_height, line_height


def draw_multiline_fields(
    draw: ImageDraw.ImageDraw,
    shot: dict[str, Any],
    font_path: Path,
    origin_x: int,
    origin_y: int,
    width: int,
    height: int,
    shot_number: int,
) -> None:
    label_width = 174
    label_gap = 18
    content_width = width - label_width - label_gap
    fields = annotation_fields(shot)
    chosen: tuple[int, list[tuple[str, list[str]]], int, int] | None = None
    for font_size in range(38, 27, -2):
        layout, total_height, line_height = field_layout(
            draw, fields, font_path, font_size, content_width
        )
        if total_height <= height:
            chosen = (font_size, layout, total_height, line_height)
            break
    if chosen is None:
        raise ValueError(
            f"Shot {shot_number} annotation is too long for the safe 28px minimum. "
            "Shorten it to executable shot information before composing."
        )

    font_size, layout, total_height, line_height = chosen
    label_font = font(font_path, max(22, round(font_size * 0.72)))
    value_font = font(font_path, font_size)
    field_gap = max(10, math.ceil(font_size * 0.38))
    y = origin_y + max(0, (height - total_height) // 2)
    for label, lines in layout:
        draw.text((origin_x, y + 4), label, fill=COLORS["muted"], font=label_font)
        value_x = origin_x + label_width + label_gap
        for line in lines:
            draw.text((value_x, y), line, fill=COLORS["ink"], font=value_font)
            y += line_height
        y += field_gap


def fit_frame(image: Image.Image, mode: str, size: tuple[int, int]) -> Image.Image:
    if mode == "cover":
        return ImageOps.fit(image, size, method=RESAMPLING.LANCZOS, centering=(0.5, 0.5))
    contained = ImageOps.contain(image, size, method=RESAMPLING.LANCZOS)
    result = Image.new("RGB", size, COLORS["frame_bg"])
    x = (size[0] - contained.width) // 2
    y = (size[1] - contained.height) // 2
    result.paste(contained, (x, y))
    return result


def apply_replacement_images(
    images: list[Image.Image], shots: list[dict[str, Any]], fit_mode: str
) -> tuple[list[Image.Image], list[int]]:
    resolved = list(images)
    replaced_shots: list[int] = []
    for index, shot in enumerate(shots):
        raw_path = shot.get("replacement_image")
        if raw_path is None:
            continue
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError(
                f"Shot {index + 1} replacement_image must be a non-empty image path"
            )
        replacement = open_rgb(Path(raw_path.strip()))
        resolved[index] = fit_frame(replacement, fit_mode, resolved[index].size)
        replaced_shots.append(int(shot.get("number") or (index + 1)))
    return resolved, replaced_shots


def draw_overlay(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    text_font: ImageFont.FreeTypeFont,
    anchor: str,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pad_x, pad_y = 18, 11
    box_width = text_width + (2 * pad_x)
    box_height = text_height + (2 * pad_y)
    left = x if anchor == "left" else x - box_width
    draw.rectangle((left, y, left + box_width, y + box_height), fill=COLORS["overlay"])
    draw.text(
        (left + pad_x, y + pad_y - bbox[1]),
        text,
        fill=COLORS["white"],
        font=text_font,
    )


def shot_number_label(shot: dict[str, Any], index: int) -> str:
    number = int(shot.get("number") or (index + 1))
    if shot.get("part") is None:
        return f"{number:02d}"
    part_number = int(shot["part"])
    local_number = int(shot.get("part_shot_number") or (index + 1))
    return f"P{part_number:02d}-{local_number:02d}"


def draw_shot_row(
    sheet: Image.Image,
    image: Image.Image,
    shot: dict[str, Any],
    index: int,
    font_path: Path,
    fit_mode: str,
    frame_width: int,
    row_height: int,
    canvas_width: int,
) -> None:
    row_top = index * row_height
    sheet.paste(fit_frame(image, fit_mode, (frame_width, row_height)), (0, row_top))
    draw = ImageDraw.Draw(sheet)

    overlay_font = font(font_path, 28)
    number = int(shot.get("number") or (index + 1))
    draw_overlay(draw, shot_number_label(shot, index), 38, row_top + 36, overlay_font, "left")
    draw_overlay(
        draw,
        str(shot.get("timecode") or ""),
        frame_width - 38,
        row_top + 36,
        overlay_font,
        "right",
    )

    annotation_left = frame_width
    head_width = 196
    draw.rectangle(
        (annotation_left, row_top, canvas_width, row_top + row_height),
        fill=COLORS["annotation_bg"],
    )
    draw.rectangle(
        (annotation_left, row_top, annotation_left + head_width, row_top + row_height),
        fill=COLORS["annotation_head"],
    )
    draw.line(
        (annotation_left + head_width, row_top, annotation_left + head_width, row_top + row_height),
        fill=COLORS["line"],
        width=2,
    )
    shot_size_font = font(font_path, 43)
    purpose_font = font(font_path, 27)
    draw.text(
        (annotation_left + 34, row_top + 60),
        str(shot.get("shot_size") or "Shot"),
        fill=COLORS["ink"],
        font=shot_size_font,
    )
    purpose = str(shot.get("purpose") or "").strip()
    purpose_lines = wrap_text(draw, purpose or "Shot progression", purpose_font, head_width - 68)[:3]
    purpose_y = row_top + row_height - 54 - (len(purpose_lines) * 37)
    for line in purpose_lines:
        draw.text(
            (annotation_left + 34, purpose_y),
            line,
            fill=COLORS["muted"],
            font=purpose_font,
        )
        purpose_y += 37

    body_x = annotation_left + head_width + 42
    body_y = row_top + 40
    body_width = canvas_width - body_x - 42
    body_height = row_height - 80
    draw_multiline_fields(
        draw,
        shot,
        font_path,
        body_x,
        body_y,
        body_width,
        body_height,
        number,
    )

    divider_left = frame_width - (CONTENT_DIVIDER // 2)
    draw.rectangle(
        (
            divider_left,
            row_top,
            divider_left + CONTENT_DIVIDER - 1,
            row_top + row_height - 1,
        ),
        fill=COLORS["divider"],
    )


def portrait_annotation_layout(
    draw: ImageDraw.ImageDraw,
    shot: dict[str, Any],
    font_path: Path,
    font_size: int,
    max_width: int,
) -> tuple[list[tuple[str, list[str]]], int, int, int]:
    value_font = font(font_path, font_size)
    label_size = max(18, font_size - 4)
    label_height = math.ceil(label_size * 1.25)
    line_height = math.ceil(font_size * 1.34)
    gap = max(10, math.ceil(font_size * 0.48))
    layout: list[tuple[str, list[str]]] = []
    total_height = 0
    for label, value in annotation_fields(shot):
        lines = wrap_text(draw, value, value_font, max_width)
        layout.append((label, lines))
        total_height += label_height + 4 + (len(lines) * line_height) + gap
    if layout:
        total_height -= gap
    return layout, total_height, line_height, label_height


def draw_portrait_card(
    sheet: Image.Image,
    image: Image.Image,
    shot: dict[str, Any],
    index: int,
    left: int,
    font_path: Path,
    fit_mode: str,
    frame_height: int,
) -> None:
    frame_size = (PORTRAIT_CARD_WIDTH, frame_height)
    sheet.paste(fit_frame(image, fit_mode, frame_size), (left, 0))
    draw = ImageDraw.Draw(sheet)
    overlay_font = font(font_path, 26)
    draw_overlay(draw, shot_number_label(shot, index), left + 28, 28, overlay_font, "left")
    draw_overlay(
        draw,
        str(shot.get("timecode") or ""),
        left + PORTRAIT_CARD_WIDTH - 28,
        28,
        overlay_font,
        "right",
    )

    annotation_top = frame_height
    annotation_bottom = annotation_top + PORTRAIT_ANNOTATION_HEIGHT
    draw.rectangle(
        (left, annotation_top, left + PORTRAIT_CARD_WIDTH - 1, annotation_bottom - 1),
        fill=COLORS["annotation_bg"],
    )
    draw.rectangle(
        (
            left,
            annotation_top,
            left + PORTRAIT_CARD_WIDTH - 1,
            annotation_top + PORTRAIT_HEADER_HEIGHT,
        ),
        fill=COLORS["annotation_head"],
    )
    draw.rectangle(
        (
            left,
            annotation_top - (CONTENT_DIVIDER // 2),
            left + PORTRAIT_CARD_WIDTH - 1,
            annotation_top + (CONTENT_DIVIDER // 2) - 1,
        ),
        fill=COLORS["divider"],
    )

    shot_size_font = font(font_path, 34)
    purpose_font = font(font_path, 22)
    draw.text(
        (left + 28, annotation_top + 30),
        str(shot.get("shot_size") or "Shot"),
        fill=COLORS["ink"],
        font=shot_size_font,
    )
    purpose = str(shot.get("purpose") or "Shot progression").strip()
    purpose_x = left + 180
    purpose_lines = wrap_text(
        draw,
        purpose,
        purpose_font,
        PORTRAIT_CARD_WIDTH - (purpose_x - left) - 28,
    )[:2]
    purpose_y = annotation_top + 31
    for line in purpose_lines:
        draw.text((purpose_x, purpose_y), line, fill=COLORS["muted"], font=purpose_font)
        purpose_y += 29

    body_left = left + 28
    body_top = annotation_top + PORTRAIT_HEADER_HEIGHT + 24
    body_width = PORTRAIT_CARD_WIDTH - 56
    body_height = PORTRAIT_ANNOTATION_HEIGHT - PORTRAIT_HEADER_HEIGHT - 48
    chosen: tuple[int, list[tuple[str, list[str]]], int, int, int] | None = None
    for font_size in range(26, 19, -2):
        layout, total_height, line_height, label_height = portrait_annotation_layout(
            draw, shot, font_path, font_size, body_width
        )
        if total_height <= body_height:
            chosen = (font_size, layout, total_height, line_height, label_height)
            break
    if chosen is None:
        number = int(shot.get("number") or (index + 1))
        raise ValueError(
            f"Shot {number} annotation is too long for the portrait layout's safe "
            "20px minimum. Shorten it before composing."
        )

    font_size, layout, total_height, line_height, label_height = chosen
    label_font = font(font_path, max(18, font_size - 4))
    value_font = font(font_path, font_size)
    field_gap = max(10, math.ceil(font_size * 0.48))
    y = body_top + max(0, (body_height - total_height) // 2)
    for label, lines in layout:
        draw.text((body_left, y), label, fill=COLORS["muted"], font=label_font)
        y += label_height + 4
        for line in lines:
            draw.text((body_left, y), line, fill=COLORS["ink"], font=value_font)
            y += line_height
        y += field_gap

def footer_layout(
    draw: ImageDraw.ImageDraw,
    title: str,
    value: str,
    font_path: Path,
    width: int,
    height: int,
) -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, list[str], int]:
    for body_size in range(32, 23, -2):
        body_font = font(font_path, body_size)
        title_font = font(font_path, max(22, body_size - 6))
        lines = wrap_text(draw, value, body_font, width)
        line_height = math.ceil(body_size * 1.35)
        title_height = math.ceil((body_size - 6) * 1.35)
        total_height = title_height + 18 + (len(lines) * line_height)
        if total_height <= height:
            return title_font, body_font, lines, line_height
    raise ValueError(f"Footer section '{title}' is too long; shorten it before composing")


def draw_footer(
    sheet: Image.Image,
    global_info: dict[str, Any],
    font_path: Path,
    top: int,
) -> None:
    draw = ImageDraw.Draw(sheet)
    canvas_width = sheet.width
    draw.rectangle((0, top, canvas_width, top + FOOTER_HEIGHT), fill=COLORS["footer"])
    items = list(global_info.items())
    cell_width = canvas_width / len(items)
    for index, (title, value) in enumerate(items):
        left = round(index * cell_width)
        right = round((index + 1) * cell_width)
        if index:
            draw.line((left, top + 34, left, top + FOOTER_HEIGHT - 34), fill=COLORS["footer_line"], width=2)
        pad_x, pad_y = 42, 38
        content_width = right - left - (2 * pad_x)
        content_height = FOOTER_HEIGHT - (2 * pad_y)
        title_font, body_font, lines, line_height = footer_layout(
            draw,
            str(title),
            str(value or "None"),
            font_path,
            content_width,
            content_height,
        )
        draw.text((left + pad_x, top + pad_y), str(title), fill=COLORS["footer_title"], font=title_font)
        y = top + pad_y + 52
        for line in lines:
            draw.text((left + pad_x, y), line, fill=COLORS["white"], font=body_font)
            y += line_height


def draw_row_dividers(
    sheet: Image.Image,
    shot_count: int,
    row_height: int,
    canvas_width: int,
) -> None:
    """Draw strong shot boundaries across a vertical-list layout."""
    draw = ImageDraw.Draw(sheet)
    half = SHOT_DIVIDER // 2
    for index in range(1, shot_count):
        boundary = index * row_height
        draw.rectangle(
            (0, boundary - half, canvas_width, boundary + half - 1),
            fill=COLORS["divider"],
        )


def draw_column_dividers(
    sheet: Image.Image,
    shot_count: int,
    card_width: int,
    start_x: int,
    content_height: int,
) -> None:
    """Draw strong shot boundaries across a horizontal-strip layout."""
    draw = ImageDraw.Draw(sheet)
    half = SHOT_DIVIDER // 2
    for index in range(1, shot_count):
        boundary = start_x + (index * card_width)
        draw.rectangle(
            (boundary - half, 0, boundary + half - 1, content_height - 1),
            fill=COLORS["divider"],
        )


def resize_to_safe_limit(
    image: Image.Image, max_dimension: int | None
) -> tuple[Image.Image, bool]:
    if max_dimension is None:
        return image, False
    if max_dimension >= 6000:
        raise ValueError("--max-dimension must be strictly less than 6000")
    if max_dimension < 512:
        raise ValueError("--max-dimension is too small for a readable storyboard sheet")
    if max(image.size) <= max_dimension:
        return image, False

    scale = max_dimension / max(image.size)
    new_width = max(MULTIPLE, math.floor((image.width * scale) / MULTIPLE) * MULTIPLE)
    new_height = max(MULTIPLE, math.floor((image.height * scale) / MULTIPLE) * MULTIPLE)
    resized = image.resize((new_width, new_height), RESAMPLING.LANCZOS)
    return resized, True


def render_landscape_sheet(
    images: list[Image.Image],
    shots: list[dict[str, Any]],
    global_info: dict[str, Any],
    output: Path,
    font_path: Path,
    fit_mode: str,
    max_dimension: int | None,
    source_mode: str,
    ratio_width: float,
    ratio_height: float,
    video_ratio: str,
) -> tuple[Image.Image, dict[str, Any]]:
    shot_count = len(shots)
    row_height = LANDSCAPE_FRAME_HEIGHT
    frame_width = rounded_multiple(row_height * ratio_width / ratio_height)
    canvas_width = frame_width + LANDSCAPE_ANNOTATION_WIDTH
    rows_height = shot_count * row_height
    canvas_height = rows_height + FOOTER_HEIGHT
    sheet = Image.new("RGB", (canvas_width, canvas_height), COLORS["white"])

    for index, (image, shot) in enumerate(zip(images, shots)):
        draw_shot_row(
            sheet,
            image,
            shot,
            index,
            font_path,
            fit_mode,
            frame_width,
            row_height,
            canvas_width,
        )
    draw_row_dividers(sheet, shot_count, row_height, canvas_width)
    draw_footer(sheet, global_info, font_path, rows_height)

    sheet, resized = resize_to_safe_limit(sheet, max_dimension)
    return sheet, {
        "output": str(output.resolve()),
        "size": list(sheet.size),
        "shots": shot_count,
        "source_mode": source_mode,
        "video_ratio": video_ratio,
        "layout": "vertical-list",
        "frame_size": [frame_width, row_height],
        "resized_for_limit": resized,
        "max_dimension": max_dimension,
    }


def render_portrait_sheet(
    images: list[Image.Image],
    shots: list[dict[str, Any]],
    global_info: dict[str, Any],
    output: Path,
    font_path: Path,
    fit_mode: str,
    max_dimension: int | None,
    source_mode: str,
    ratio_width: float,
    ratio_height: float,
    video_ratio: str,
) -> tuple[Image.Image, dict[str, Any]]:
    shot_count = len(shots)
    frame_height = rounded_multiple(PORTRAIT_CARD_WIDTH * ratio_height / ratio_width)
    column_count = max(shot_count, len(global_info), 3)
    canvas_width = column_count * PORTRAIT_CARD_WIDTH
    content_height = frame_height + PORTRAIT_ANNOTATION_HEIGHT
    canvas_height = content_height + FOOTER_HEIGHT
    sheet = Image.new("RGB", (canvas_width, canvas_height), COLORS["white"])
    shots_width = shot_count * PORTRAIT_CARD_WIDTH
    start_x = (canvas_width - shots_width) // 2

    for index, (image, shot) in enumerate(zip(images, shots)):
        draw_portrait_card(
            sheet,
            image,
            shot,
            index,
            start_x + (index * PORTRAIT_CARD_WIDTH),
            font_path,
            fit_mode,
            frame_height,
        )
    draw_column_dividers(
        sheet,
        shot_count,
        PORTRAIT_CARD_WIDTH,
        start_x,
        content_height,
    )
    draw_footer(sheet, global_info, font_path, content_height)

    sheet, resized = resize_to_safe_limit(sheet, max_dimension)
    return sheet, {
        "output": str(output.resolve()),
        "size": list(sheet.size),
        "shots": shot_count,
        "source_mode": source_mode,
        "video_ratio": video_ratio,
        "layout": "horizontal-strip",
        "frame_size": [PORTRAIT_CARD_WIDTH, frame_height],
        "resized_for_limit": resized,
        "max_dimension": max_dimension,
    }


def render_sheet(
    images: list[Image.Image],
    shots: list[dict[str, Any]],
    global_info: dict[str, Any],
    output: Path,
    font_path: Path,
    fit_mode: str,
    max_dimension: int | None,
    source_mode: str,
    video_ratio: str,
) -> tuple[Image.Image, dict[str, Any]]:
    ratio_width, ratio_height, normalized_ratio = parse_video_ratio(video_ratio)
    if layout_for_ratio(ratio_width, ratio_height) == "horizontal-strip":
        return render_portrait_sheet(
            images,
            shots,
            global_info,
            output,
            font_path,
            fit_mode,
            max_dimension,
            source_mode,
            ratio_width,
            ratio_height,
            normalized_ratio,
        )
    return render_landscape_sheet(
        images,
        shots,
        global_info,
        output,
        font_path,
        fit_mode,
        max_dimension,
        source_mode,
        ratio_width,
        ratio_height,
        normalized_ratio,
    )


def preflight_output_paths(outputs: Iterable[Path]) -> None:
    seen: set[Path] = set()
    for output in outputs:
        if os.path.lexists(output):
            raise FileExistsError(f"Refusing to overwrite existing output: {output}")
        resolved = output.resolve()
        if resolved in seen:
            raise ValueError(f"Duplicate output path: {output}")
        seen.add(resolved)


def save_sheets_exclusive(sheets: list[tuple[Path, Image.Image]]) -> None:
    preflight_output_paths(output for output, _ in sheets)
    created: list[tuple[Path, os.stat_result]] = []
    with ExitStack() as stack:
        try:
            handles = []
            # Reserve every destination before encoding any PNG; xb also rejects symlinks.
            for output, sheet in sheets:
                output.parent.mkdir(parents=True, exist_ok=True)
                handle = stack.enter_context(output.open("xb"))
                created.append((output, os.fstat(handle.fileno())))
                handles.append((handle, sheet))
            for handle, sheet in handles:
                sheet.save(handle, format="PNG", optimize=True)
                handle.flush()
        except BaseException:
            # Keep handles open during rollback so owned inode identities cannot be reused.
            for output, identity in reversed(created):
                try:
                    if os.path.samestat(output.lstat(), identity):
                        output.unlink()
                except OSError:
                    pass
            raise


def compose_sheet(
    images: list[Image.Image],
    shots: list[dict[str, Any]],
    global_info: dict[str, Any],
    output: Path,
    font_path: Path,
    fit_mode: str,
    max_dimension: int | None,
    source_mode: str,
    video_ratio: str,
) -> dict[str, Any]:
    preflight_output_paths([output])
    sheet, result = render_sheet(
        images, shots, global_info, output, font_path, fit_mode,
        max_dimension, source_mode, video_ratio,
    )
    save_sheets_exclusive([(output, sheet)])
    return result


def parse_timecode(value: Any, field: str) -> tuple[int, int]:
    match = TIMECODE_PATTERN.fullmatch(value.strip()) if isinstance(value, str) else None
    if not match:
        raise ValueError(f"{field} must use mm:ss[.mmm]-mm:ss[.mmm] notation")
    start_minutes, start_seconds, start_ms, end_minutes, end_seconds, end_ms = match.groups()
    start = ((int(start_minutes) * 60) + int(start_seconds)) * 1000 + int((start_ms or "0").ljust(3, "0"))
    end = ((int(end_minutes) * 60) + int(end_seconds)) * 1000 + int((end_ms or "0").ljust(3, "0"))
    if end <= start:
        raise ValueError(f"{field} must have positive duration")
    return start, end


def validate_runtime_shots(manifest: dict[str, Any]) -> None:
    rows = manifest["runtime_shots"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("'runtime_shots' must be a non-empty array")
    sources: dict[int, tuple[int, int]] = {}
    previous_end = 0
    for index, shot in enumerate(manifest["shots"], start=1):
        number = shot.get("number")
        if type(number) is not int or number < 1 or number in sources:
            raise ValueError("Source shots need unique positive integer 'number' values for runtime_shots")
        start, end = parse_timecode(shot["timecode"], f"Source shot {index} timecode")
        if start != previous_end:
            raise ValueError("Source shot timecodes must form a contiguous ordered timeline starting at zero")
        sources[number] = (start, end)
        previous_end = end

    global_cursor = 0
    local_cursor = 0
    previous_part = None
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"Runtime shot {index} must be a JSON object")
        number = row.get("source_shot_number")
        if type(number) is not int or number < 1 or number not in sources:
            raise ValueError(f"Runtime shot {index} source_shot_number must reference a source shot number")
        for field in SHOT_INSTRUCTION_FIELDS:
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"Runtime shot {index} needs its own non-empty text '{field}'")
        for field in ("action", "product", "camera"):
            if field in row and not isinstance(row[field], str):
                raise ValueError(f"Runtime shot {index} {field} must be text")
        part = row.get("part")
        if type(part) is not int or part < 1:
            raise ValueError(f"Runtime shot {index} needs a positive integer 'part'")
        if part != previous_part:
            if part != (previous_part or 0) + 1:
                raise ValueError("Runtime shot parts must form contiguous ordered blocks starting at 1")
            local_cursor = 0
            previous_part = part
        start, end = parse_timecode(row.get("timecode"), f"Runtime shot {index} timecode")
        global_start, global_end = parse_timecode(
            row.get("global_timecode"), f"Runtime shot {index} global_timecode"
        )
        if start != local_cursor:
            raise ValueError(f"Runtime shot {index} local timecodes must start at zero and be contiguous per part")
        if end - start != global_end - global_start:
            raise ValueError(f"Runtime shot {index} local and global durations must match")
        source_start, source_end = sources[number]
        if not source_start <= global_start < global_end <= source_end:
            raise ValueError(f"Runtime shot {index} global_timecode must stay within its source shot range")
        if global_start != global_cursor:
            raise ValueError(f"Runtime shot {index} global slices must cover the source timeline without gaps or overlaps")
        global_cursor = global_end
        local_cursor = end
    if global_cursor != previous_end:
        raise ValueError("Runtime global slices must cover the entire source timeline")


def grouped_part_indexes(manifest: dict[str, Any]) -> list[tuple[int, list[int]]]:
    part_numbers: list[int] = []
    rows = manifest["runtime_shots"] if "runtime_shots" in manifest else manifest["shots"]
    for index, shot in enumerate(rows, start=1):
        raw_part = shot.get("part")
        if isinstance(raw_part, bool) or not isinstance(raw_part, int) or raw_part < 1:
            raise ValueError(
                f"Shot {index} needs a positive integer 'part' for --split-by-part"
            )
        part_number = raw_part
        part_numbers.append(part_number)

    unique_parts: list[int] = []
    for part_number in part_numbers:
        if not unique_parts or unique_parts[-1] != part_number:
            unique_parts.append(part_number)
    expected = list(range(1, len(unique_parts) + 1))
    if unique_parts != expected:
        raise ValueError(
            "Shot parts must form contiguous ordered blocks starting at 1; "
            f"received block order {unique_parts}"
        )

    return [
        (part_number, [index for index, value in enumerate(part_numbers) if value == part_number])
        for part_number in unique_parts
    ]


def part_output_path(output: Path, part_number: int) -> Path:
    suffix = output.suffix or ".png"
    return output.with_name(f"{output.stem}-part-{part_number:02d}{suffix}")


def part_global_info(manifest: dict[str, Any], part_number: int, total_parts: int) -> dict[str, Any]:
    global_info = dict(manifest["global_info"])
    raw_info = (manifest.get("parts") or {}).get(str(part_number), {})
    label = str(raw_info.get("label") or f"Part {part_number} of {total_parts}").strip()
    handoff = str(raw_info.get("handoff") or "Generate this part independently from its script while keeping visual consistency across the full video.").strip()
    continuity = joined(label, handoff)
    if "Part Continuity" not in global_info and len(global_info) >= 4:
        raise ValueError(
            "Split output needs a 'Part Continuity' footer section; keep common global_info "
            "to at most 3 sections or include that key for replacement"
        )
    global_info["Part Continuity"] = continuity
    return global_info


def compose(args: argparse.Namespace) -> dict[str, Any]:
    if args.split_by_part and args.no_max_dimension:
        raise ValueError(
            "--no-max-dimension is only for the complete creative preview and cannot "
            "be combined with --split-by-part runtime outputs"
        )
    manifest = load_manifest(args.manifest)
    if "runtime_shots" in manifest and not args.split_by_part:
        raise ValueError("'runtime_shots' requires --split-by-part")
    font_path = resolve_font(args.font)
    images, source_mode = source_images(args, manifest)
    images, replacement_shots = apply_replacement_images(
        images, manifest["shots"], args.fit
    )
    if replacement_shots:
        source_mode = f"{source_mode}+replacements"
    max_dimension = None if args.no_max_dimension else args.max_dimension
    ratio_width, ratio_height, video_ratio = parse_video_ratio(
        args.video_ratio or manifest.get("video_ratio") or "16:9"
    )
    layout = layout_for_ratio(ratio_width, ratio_height)
    if not args.split_by_part:
        result = compose_sheet(
            images,
            manifest["shots"],
            manifest["global_info"],
            args.output,
            font_path,
            args.fit,
            max_dimension,
            source_mode,
            video_ratio,
        )
        result["replacement_shots"] = replacement_shots
        result["execution_hint"] = complete_sheet_execution_hint(args.output)
        return result

    groups = grouped_part_indexes(manifest)
    rows = manifest["runtime_shots"] if "runtime_shots" in manifest else manifest["shots"]
    source_indexes = (
        {shot["number"]: index for index, shot in enumerate(manifest["shots"])}
        if "runtime_shots" in manifest else {}
    )
    paths = [part_output_path(args.output, part_number) for part_number, _ in groups]
    preflight_output_paths(paths)
    plans = []
    for (part_number, indexes), output in zip(groups, paths):
        shots = []
        part_images = []
        for local_index, row_index in enumerate(indexes, start=1):
            shot = dict(rows[row_index])
            source_index = row_index
            if "runtime_shots" in manifest:
                source_index = source_indexes[shot["source_shot_number"]]
                shot["number"] = shot["source_shot_number"]
            shot["part_shot_number"] = local_index
            shots.append(shot)
            part_images.append(images[source_index])
        plans.append((
            part_number, shots, part_images, output,
            part_global_info(manifest, part_number, len(groups)),
            [int(shot.get("number") or 0) for shot in shots],
        ))

    outputs: list[dict[str, Any]] = []
    rendered = []
    for part_number, shots, part_images, output, global_info, source_numbers in plans:
        sheet, result = render_sheet(
            part_images,
            shots,
            global_info,
            output,
            font_path,
            args.fit,
            max_dimension,
            source_mode,
            video_ratio,
        )
        result["part"] = part_number
        result["global_shot_numbers"] = source_numbers
        outputs.append(result)
        rendered.append((output, sheet))
    save_sheets_exclusive(rendered)
    result = {
        "split_by_part": True,
        "parts": len(outputs),
        "source_mode": source_mode,
        "replacement_shots": replacement_shots,
        "video_ratio": video_ratio,
        "layout": layout,
        "outputs": outputs,
    }
    result["execution_hint"] = part_sheet_execution_hint(outputs)
    return result


def main() -> int:
    args = parse_args()
    try:
        result = compose(args)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())