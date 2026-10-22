
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_images_grid.py — 通用图片合并拼图（多张图 → 少数几张合成 PNG）

用途（本 skill 的通用能力，不限定营销复刻路线）：
  当「分镜示意图」或「商品多视角参考图」数量过多、超过单次 `sandbox_generate_video`
  调用能接受的图片数量上限时，先用本脚本把多张小图合并成少数几张「拼图大图」，
  再把这几张拼图传进 ImageList。合并后单张拼图里用序号 / 视角标签区分每格，
  prompt 里用「@图片N 的第 X 格」这类说法引用具体分镜 / 视角。

两种模式（--mode）：
  storyboard     分镜图合并：每格 = 一张分镜图 + 序号/时间 + 景别/节拍 + 结构化字段
                 （画面动作/产品露出/镜头转场/声音/口播）。用于把逐分镜关键帧/示意图
                 拼成故事版大图。
  product-views  商品多视角合并：每格 = 一张商品视图 + 视角标签（正面/背面/侧面/顶/底/
                 内部/材质特写/使用状态等）+ 可选说明。用于把同一商品的多张真实视角图
                 拼成一张「多视图参考大图」。

关键特性 —— 按上限自动分页（--max-per-sheet）：
  无论多少张图，都会按每张拼图最多容纳 N 格自动切分成 sheet_1.png、sheet_2.png……，
  从而保证「合并后拼图张数」控制在视频模型单次调用图片上限之内。列数用 --cols 控制。

用法：
  python3 merge_images_grid.py --mode storyboard \
      --input storyboard.json --out-dir <dir> \
      [--cols 3] [--max-per-sheet 6] [--prefix storyboard] [--font /path/cjk.ttf]

  python3 merge_images_grid.py --mode product-views \
      --input product_views.json --out-dir <dir> \
      [--cols 3] [--max-per-sheet 9] [--prefix product_views] [--font /path/cjk.ttf]

输入 JSON（storyboard 模式）：
{
  "title": "整条视频标题",
  "consistency": "角色与一致性（跨镜形象/音色锚点）",   # 可选，末页底部总结块
  "visual_mood": "视觉与情绪：色调/光线/节奏",           # 可选
  "tech_spec": "技术规格：分镜数/总时长/画幅/字幕策略",    # 可选
  "tiles": [
    {
      "index": 1, "time_range": "00:00-00:02.5",
      "image": "assets/keyframe_1.png",
      "shot_size": "近景", "beat": "Hook 悬念提问",
      "action": "画面动作", "product": "产品露出",
      "transition": "镜头转场", "sound": "声音",
      "voiceover": "口播文案"
    }
  ]
}

输入 JSON（product-views 模式）：
{
  "title": "产品1 多视角参考",
  "product_id": "产品1",
  "note": "同一件商品的多张真实视角图，供视频模型统一参考外观真值",  # 可选，末页底部
  "tiles": [
    { "view": "正面", "image": "assets/p1_front.jpg", "desc": "Logo 居中，正标可读" },
    { "view": "背面", "image": "assets/p1_back.jpg",  "desc": "成分表 / 条码" },
    { "view": "侧面", "image": "assets/p1_side.jpg" }
  ]
}

输入 JSON 的字段别名容错（无需先读源码反推）：
  - 顶层可以是对象（推荐，能带 title/note 等页眉页脚），也可以直接是 tiles 数组。
  - 格子列表键：tiles（正式）| images | items | views | shots | list
  - 每格图片键：image（正式）| path | file | src | image_path | filepath
  - 每格标签键：view（正式）| label | name | title | caption
  - 每格说明键：desc（正式）| note | description | remark | text
  命中别名时脚本照常出图，并在 stderr 打 WARN 提示正式字段名；结构确实无法归一
  （没有任何格子 / 某格没有图片路径）时报中文 ERROR 并退出 2。

输出：<out-dir>/<prefix>_1.png、<prefix>_2.png …（每页一张拼图）
      并在 stdout 逐行打印生成的文件路径，最后一行打印 SHEETS=<页数>。
"""
import argparse
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

# ---- 布局常量 ----
COL_W = 520          # 每格宽
PAD = 24             # 画布外边距
GAP = 16             # 格间距
HEADER_H = 60        # 序号+时间条 / 视角标签条
BEAT_H = 52          # 景别+节拍行（storyboard 专用）
BG = "#ffffff"
DARK = "#1f2430"
LABEL = "#6b7280"
ACCENT = "#b91c1c"
LINE = "#e5e7eb"
PLACEHOLDER = "#f3f4f6"

STORYBOARD_FIELDS = [("画面动作", "action"), ("产品露出", "product"),
                     ("镜头转场", "transition"), ("声音", "sound"), ("口播", "voiceover")]

# ---- --input JSON 归一化（字段别名容错）----
TILE_LIST_KEYS = ("tiles", "images", "items", "views", "shots", "list")
IMAGE_KEYS = ("image", "path", "file", "src", "image_path", "filepath")
LABEL_KEYS = ("view", "label", "name", "title", "caption")
DESC_KEYS = ("desc", "note", "description", "remark", "text")


class SpecError(Exception):
    """--input JSON 结构无法归一成 {tiles:[...]}。"""


def _pick(d, keys):
    """按候选键顺序取第一个非空字符串值，兼容调用方写的同义字段名。"""
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def normalize_spec(raw, mode):
    """把调用方给的 --input JSON 归一成 {title, tiles:[...]} 结构。

    容错（线上真实失败写法都在此收敛）：
      1. 顶层直接是数组 `[{...}, {...}]` → 视为 tiles 本身。
      2. 格子列表键写成 images/items/views/shots/list，而不是 tiles。
      3. 每格图片键写成 path/file/src，而不是 image。
      4. 每格标签键写成 label/name/title，而不是 view。
      5. 每格说明键写成 note/description，而不是 desc。
    归一后统一输出 image/view/desc/index，渲染层不必再关心别名。

    返回 (spec, warnings)；无法归一时抛 SpecError（中文可执行说明）。
    """
    warnings = []

    if isinstance(raw, list):
        spec = {"tiles": raw}
        warnings.append(
            "--input 顶层是 JSON 数组，已按「这就是 tiles 列表」处理。"
            "推荐写成对象 {\"title\": \"...\", \"tiles\": [...]}，可额外承载 title/note 等页眉页脚信息。"
        )
    elif isinstance(raw, dict):
        spec = dict(raw)
    else:
        raise SpecError(
            "--input 的 JSON 顶层必须是对象（推荐）或数组，当前是 %s。"
            "推荐结构：{\"title\": \"...\", \"tiles\": [{\"image\": \"/abs/a.png\", ...}]}。"
            % type(raw).__name__
        )

    if "tiles" not in spec:
        for key in TILE_LIST_KEYS:
            if key == "tiles":
                continue
            if isinstance(spec.get(key), list):
                spec["tiles"] = spec.pop(key)
                warnings.append(
                    "--input 里的格子列表写成了 `%s`，已按 `tiles` 处理；正式字段名是 `tiles`。" % key
                )
                break

    tiles_raw = spec.get("tiles")
    if not isinstance(tiles_raw, list) or not tiles_raw:
        raise SpecError(
            "--input 里没读到任何格子：需要一个非空的 `tiles` 数组（当前顶层键：%s）。"
            "product-views 正确结构：{\"title\": \"产品1 多视角参考\", \"tiles\": "
            "[{\"view\": \"正面\", \"image\": \"/abs/p1_front.jpg\", \"desc\": \"Logo 居中\"}]}；"
            "storyboard 把每格换成 {\"index\": 1, \"image\": \"/abs/kf1.png\", \"time_range\": \"00:00-00:03\"}。"
            % sorted(spec.keys())
        )

    alias_used = set()
    tiles = []
    for i, t in enumerate(tiles_raw, 1):
        if not isinstance(t, dict):
            raise SpecError(
                "`tiles` 第 %d 项必须是对象，当前是 %s；"
                "每格形如 {\"view\": \"正面\", \"image\": \"/abs/p1_front.jpg\", \"desc\": \"说明\"}。"
                % (i, type(t).__name__)
            )
        tile = dict(t)
        alias_used.update(
            k for k in tile
            if k in IMAGE_KEYS + LABEL_KEYS + DESC_KEYS and k not in ("image", "view", "desc")
        )

        image = _pick(tile, IMAGE_KEYS)
        if not image:
            raise SpecError(
                "`tiles` 第 %d 项没有图片路径：必须有 `image`（也接受 path/file/src），"
                "当前该项的键是 %s。" % (i, sorted(tile.keys()))
            )
        tile["image"] = image

        label = _pick(tile, LABEL_KEYS)
        if label is not None:
            tile["view"] = label
        elif mode == "product-views":
            warnings.append("`tiles` 第 %d 项缺视角标签 `view`，该格标签将留空。" % i)

        desc = _pick(tile, DESC_KEYS)
        if desc is not None:
            tile["desc"] = desc

        if mode == "storyboard" and not isinstance(tile.get("index"), int):
            tile["index"] = i
        tiles.append(tile)

    if alias_used:
        warnings.append(
            "格内字段名 %s 已按别名归一；正式字段名是 image（图片路径）、view（视角标签）、desc（说明）。"
            % sorted(alias_used)
        )

    spec["tiles"] = tiles
    return spec, warnings


def find_cjk_font():
    try:
        out = subprocess.run(["fc-list", ":lang=zh", "file"],
                             capture_output=True, text=True, timeout=15).stdout
        for line in out.splitlines():
            p = line.strip().rstrip(":")
            if p and os.path.exists(p):
                return p
    except Exception:
        pass
    for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf",
              "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
              "/usr/share/fonts/truetype/arphic/uming.ttc"):
        if os.path.exists(p):
            return p
    return None


def wrap(draw, text, font, max_w):
    """按像素宽逐字符换行（兼容无空格的中文）。"""
    lines = []
    for para in str(text or "").split("\n"):
        if not para:
            lines.append("")
            continue
        cur = ""
        for ch in para:
            if draw.textlength(cur + ch, font=font) <= max_w:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
        lines.append(cur)
    return lines


def text_h(draw, text, font, max_w, lh):
    return len(wrap(draw, text, font, max_w)) * lh


def load_fit(path):
    """打开图片并等比缩放到列宽，返回缩放后的 Image。"""
    im = Image.open(path).convert("RGB")
    h = round(im.height * COL_W / im.width)
    return im.resize((COL_W, h))


def paginate(tiles, max_per_sheet):
    if max_per_sheet and max_per_sheet > 0:
        return [tiles[i:i + max_per_sheet] for i in range(0, len(tiles), max_per_sheet)]
    return [tiles]


def make_fonts(font_path):
    return {
        "num": ImageFont.truetype(font_path, 28),
        "time": ImageFont.truetype(font_path, 22),
        "beat": ImageFont.truetype(font_path, 22),
        "label": ImageFont.truetype(font_path, 20),
        "body": ImageFont.truetype(font_path, 20),
        "title": ImageFont.truetype(font_path, 32),
        "view": ImageFont.truetype(font_path, 26),
    }


def measure_tile_body_h(probe, tile, fonts, inner_w, lh, mode):
    """计算单格「图以下」的文字区高度。"""
    h = 0
    if mode == "storyboard":
        h += BEAT_H + 16
        for _label, key in STORYBOARD_FIELDS:
            h += lh  # label 行
            h += text_h(probe, tile.get(key, ""), fonts["body"], inner_w, lh)
            h += 8
    else:  # product-views
        desc = tile.get("desc", "")
        if desc:
            h += 8 + text_h(probe, desc, fonts["body"], inner_w, lh) + 8
        else:
            h += 8
    return h


def render_sheet(tiles, spec, fonts, out_path, cols, page_idx, page_total,
                 mode, is_last, footer_specs):
    lh = 30
    inner_w = COL_W - 2 * 18
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

    n = len(tiles)
    cols = max(1, min(cols, n))
    rows = (n + cols - 1) // cols

    # 载入并缩放全部图片
    imgs = [load_fit(t["image"]) for t in tiles]

    # 每行图区高度 = 该行内最高图
    row_img_h = []
    row_body_h = []
    for r in range(rows):
        seg = list(range(r * cols, min((r + 1) * cols, n)))
        row_img_h.append(max(imgs[i].height for i in seg))
        row_body_h.append(max(
            measure_tile_body_h(probe, tiles[i], fonts, inner_w, lh, mode) for i in seg))

    W = PAD * 2 + cols * COL_W + (cols - 1) * GAP

    # 底部总结块（仅末页且有内容时）
    footer_h = 0
    if is_last and footer_specs:
        bw = W - PAD * 2
        for _label, key in footer_specs:
            val = spec.get(key, "")
            if val:
                footer_h += lh + text_h(probe, val, fonts["body"], bw - 16, lh) + 12
        if footer_h:
            footer_h += 2 * PAD

    title_h = 68
    H = title_h + PAD
    for r in range(rows):
        H += HEADER_H + row_img_h[r] + row_body_h[r] + GAP + 12
    H += footer_h

    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    # 标题
    d.text((PAD, 18), spec.get("title", ""), font=fonts["title"], fill=DARK)
    page_label = "拼图 %d/%d · 共 %d 格" % (page_idx, page_total, n)
    d.text((W - PAD - d.textlength(page_label, font=fonts["time"]), 26),
           page_label, font=fonts["time"], fill=LABEL)

    y = title_h
    for r in range(rows):
        seg = list(range(r * cols, min((r + 1) * cols, n)))
        for ci, i in enumerate(seg):
            x = PAD + ci * (COL_W + GAP)
            t = tiles[i]
            # 头条
            d.rectangle([x, y, x + COL_W, y + HEADER_H], fill=DARK)
            if mode == "storyboard":
                d.text((x + 14, y + 15), "%02d" % t.get("index", i + 1),
                       font=fonts["num"], fill="#ffffff")
                tr = t.get("time_range", "")
                if tr:
                    d.text((x + COL_W - 14 - d.textlength(tr, font=fonts["time"]), y + 19),
                           tr, font=fonts["time"], fill="#ffffff")
            else:  # product-views
                d.text((x + 14, y + 16),
                       "%02d  %s" % (i + 1, t.get("view", "")),
                       font=fonts["view"], fill="#ffffff")
            # 图（顶对齐，补白到本行图高）
            im = imgs[i]
            canvas.paste(im, (x, y + HEADER_H))
            if im.height < row_img_h[r]:
                d.rectangle([x, y + HEADER_H + im.height,
                             x + COL_W, y + HEADER_H + row_img_h[r]], fill=PLACEHOLDER)
            yb = y + HEADER_H + row_img_h[r]
            # 图下内容
            if mode == "storyboard":
                d.rectangle([x, yb, x + COL_W, yb + BEAT_H], fill="#f8fafc")
                d.text((x + 14, yb + 13), t.get("shot_size", ""), font=fonts["beat"], fill=DARK)
                beat = t.get("beat", "")
                d.text((x + COL_W - 14 - d.textlength(beat, font=fonts["beat"]), yb + 13),
                       beat, font=fonts["beat"], fill=ACCENT)
                yf = yb + BEAT_H + 16
                for label, key in STORYBOARD_FIELDS:
                    d.text((x + 18, yf), label, font=fonts["label"], fill=LABEL)
                    yf += lh
                    for line in wrap(d, t.get(key, ""), fonts["body"], inner_w):
                        d.text((x + 18, yf), line, font=fonts["body"], fill=DARK)
                        yf += lh
                    yf += 8
            else:
                desc = t.get("desc", "")
                if desc:
                    yf = yb + 8
                    for line in wrap(d, desc, fonts["body"], inner_w):
                        d.text((x + 18, yf), line, font=fonts["body"], fill=DARK)
                        yf += lh
        y += HEADER_H + row_img_h[r] + row_body_h[r] + GAP + 12

    # 底部总结块
    if is_last and footer_h:
        yf0 = H - footer_h + PAD
        d.rectangle([0, yf0 - PAD // 2, W, H], fill=DARK)
        yy = yf0
        bw = W - PAD * 2
        for label, key in footer_specs:
            val = spec.get(key, "")
            if not val:
                continue
            d.text((PAD, yy), label, font=fonts["label"], fill="#9ca3af")
            yy += lh
            for line in wrap(d, val, fonts["body"], bw - 16):
                d.text((PAD, yy), line, font=fonts["body"], fill="#f9fafb")
                yy += lh
            yy += 12

    canvas.save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["storyboard", "product-views"])
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--max-per-sheet", type=int, default=0,
                    help="每张拼图最多容纳的格数；>0 时按此上限自动分页。默认 0=不分页（全放一张）。")
    ap.add_argument("--prefix", default=None)
    ap.add_argument("--font", default=None)
    a = ap.parse_args()

    if not os.path.exists(a.input):
        print("ERROR: --input 指定的 JSON 文件不存在: %s"
              "（相对路径是相对当前工作目录，跨目录时请用绝对路径）" % a.input, file=sys.stderr)
        sys.exit(2)
    try:
        with open(a.input, encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError as exc:
        print("ERROR: --input 文件 %s 不是合法 JSON（%s，第 %d 行第 %d 列）"
              % (a.input, exc.msg, exc.lineno, exc.colno), file=sys.stderr)
        sys.exit(2)

    try:
        spec, warnings = normalize_spec(raw, a.mode)
    except SpecError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        sys.exit(2)
    for w in warnings:
        print("WARN: %s" % w, file=sys.stderr)

    tiles = spec["tiles"]
    missing = [t["image"] for t in tiles if not os.path.exists(t["image"])]
    if missing:
        print("ERROR: 下列图片在磁盘上不存在，请确认路径（相对路径是相对当前工作目录，"
              "跨目录时用绝对路径）后重跑: %s" % "、".join(missing), file=sys.stderr)
        sys.exit(2)

    font = a.font or find_cjk_font()
    if not font:
        print("ERROR: 找不到 CJK 字体，请用 --font 显式指定", file=sys.stderr)
        sys.exit(2)
    fonts = make_fonts(font)

    prefix = a.prefix or ("storyboard" if a.mode == "storyboard" else "product_views")
    footer_specs = ([("角色与一致性", "consistency"), ("视觉与情绪", "visual_mood"),
                     ("技术规格", "tech_spec")] if a.mode == "storyboard"
                    else [("说明", "note")])

    os.makedirs(a.out_dir, exist_ok=True)
    pages = paginate(tiles, a.max_per_sheet)
    total = len(pages)
    for pi, page in enumerate(pages, 1):
        out = os.path.join(a.out_dir, "%s_%d.png" % (prefix, pi))
        render_sheet(page, spec, fonts, out, a.cols, pi, total,
                     a.mode, is_last=(pi == total), footer_specs=footer_specs)
        print(out)
    print("SHEETS=%d" % total)


if __name__ == "__main__":
    main()