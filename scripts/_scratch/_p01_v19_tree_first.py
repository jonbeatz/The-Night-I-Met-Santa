#!/usr/bin/env python3
"""P01 v19 — tree-FIRST composition (complete rich tree + window), v16 page frame lock."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
V16 = DEV / "v16" / "art.png"
V11 = DEV / "v11" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

PROMPT = (
    "Create a SINGLE square children's-book TITLE PAGE painting — ART ONLY, no text. "
    "Image 1 = watercolor/gouache paint STYLE lock. "
    "Image 2 = mood/window DNA only (moon, snow, curtains) — do NOT copy a cropped tree from it. "
    "PROMPT ORDER IS CRITICAL — build in this order: "
    "FIRST: paint a FULL traditional Christmas TREE as the priority hero on the RIGHT side of the plate. "
    "The tree must be COMPLETE from star/tip to base — NOT cropped, NOT cut off by any edge, "
    "NOT fading, NOT a peek. Entire tree visible with breathing space around it. "
    "Rich DEEP forest green needles, warm golden string lights, red and gold ornaments, "
    "wrapped presents clearly visible at the base. Traditional Christmas richness — "
    "NOT pastel, NOT washed out, NOT pale mint. "
    "SECOND: on the LEFT, add the winter WINDOW scene that complements the tree "
    "(not the other way around): four-pane window, full moon, falling snow, "
    "faint tiny Santa sleigh+reindeer silhouette on the moon, cream curtains tied back, "
    "holly on sill. Cream/ivory interior. "
    "COMPOSITION: wide enough to show COMPLETE tree AND COMPLETE window side by side "
    "with breathing room between them. Widen the vignette if needed so neither is clipped. "
    "Soft watercolor/gouache, luminous but RICH traditional colors — deep greens, warm golds, soft reds. "
    "Soft FRAME ON dissolving to cream paper around the paired scene. "
    "Open cream above/below for live title/copyright later. No people, no baked text."
)
NEGATIVE = (
    "cropped tree, cut-off tree, partial tree, tree peek, faded tree, dissolving tree, "
    "pastel tree, washed-out green, pale mint, desaturated tree, "
    "text, letters, typography, title, copyright, watermark, "
    "people, faces, hands, child, photorealistic, blue wash behind art, hard black border"
)


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def fal_key() -> str:
    key = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    if not key:
        raise SystemExit("Missing FAL_KEY")
    return key


def upload_bytes(key: str, name: str, data: bytes, content_type: str) -> str:
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": name, "content_type": content_type}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        meta = json.loads(resp.read().decode())
    put = urllib.request.Request(
        meta["upload_url"], data=data, headers={"Content-Type": content_type}, method="PUT"
    )
    with urllib.request.urlopen(put, timeout=180) as resp:
        resp.read()
    return meta["file_url"]


def prepare_upload(path: Path, name: str, key: str) -> str:
    im = Image.open(path).convert("RGB")
    im.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, Path(name).with_suffix(".png").name, buf.getvalue(), "image/png")


def fal_req(key: str, url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Authorization": f"Key {key}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:2000]}") from e


def wait_result(key: str, submitted: dict) -> dict:
    for i in range(120):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def download(url: str, dest: Path) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return Image.open(io.BytesIO(data)).convert("RGB")


def scrub_scene_text(scene: Image.Image) -> Image.Image:
    im = scene.convert("RGBA")
    w, h = im.size
    blob = Image.new("L", (w, h), 0)
    bd = ImageDraw.Draw(blob)
    bd.rectangle([int(w * 0.05), 0, int(w * 0.95), int(h * 0.20)], fill=255)
    bd.ellipse([int(w * 0.10), 0, int(w * 0.90), int(h * 0.24)], fill=255)
    bd.rectangle([int(w * 0.08), int(h * 0.84), int(w * 0.92), h], fill=255)
    blob = blob.filter(ImageFilter.GaussianBlur(40))
    cream = Image.new("RGBA", (w, h), (*CREAM, 255))
    cream.putalpha(blob)
    return Image.alpha_composite(im, cream).convert("RGB")


def soft_vignette_keep_tree(rgb: Image.Image, feather: int = 55) -> Image.Image:
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    inset = max(4, feather // 4)
    draw.rounded_rectangle(
        [inset, inset, w - inset - 1, h - inset - 1],
        radius=int(min(w, h) * 0.035),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    px = mask.load()
    x0 = int(w * 0.45)
    for y in range(h):
        for x in range(x0, w - inset):
            t = (x - x0) / max(1, w - inset - x0)
            px[x, y] = max(px[x, y], int(255 * (0.85 + 0.15 * min(1.0, t))))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=5))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def gold_page_margins(page: Image.Image) -> Image.Image:
    page = page.convert("RGBA")
    margin = int(SIZE * 0.08)
    cut = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(cut).rounded_rectangle(
        [margin, margin, SIZE - margin - 1, SIZE - margin - 1], radius=28, fill=255
    )
    cut = cut.filter(ImageFilter.GaussianBlur(radius=36))
    gold_a = Image.eval(cut, lambda p: max(0, min(255, int((255 - p) * 0.38))))
    gold_a = gold_a.filter(ImageFilter.GaussianBlur(radius=12))
    g1 = Image.new("RGBA", (SIZE, SIZE), (218, 180, 115, 255))
    g1.putalpha(gold_a)
    g2 = Image.new("RGBA", (SIZE, SIZE), (235, 200, 145, 255))
    g2.putalpha(gold_a.point(lambda p: int(p * 0.35)).filter(ImageFilter.GaussianBlur(20)))
    return Image.alpha_composite(Image.alpha_composite(page, g1), g2).convert("RGB")


def compose_page(scene: Image.Image) -> Image.Image:
    page = Image.new("RGBA", (SIZE, SIZE), (*CREAM, 255))
    art_w = int(SIZE * 0.70)  # wider plate — complete tree + window priority
    scene_r = scene.resize((art_w, art_w), Image.Resampling.LANCZOS)
    scene_rgba = soft_vignette_keep_tree(scene_r, feather=50)
    ax = (SIZE - art_w) // 2
    ay = int(SIZE * 0.18)
    page.alpha_composite(scene_rgba, (ax, ay))
    return gold_page_margins(page)


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(seed, req_id: str) -> None:
    text = f"""# RECIPE — P01-title / v19

| Field | Value |
|-------|--------|
| **name** | Tree-first — complete rich Christmas tree + window |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v19 |
| **date** | {DAY} |
| **lane** | Qwen 2 Pro Edit (tree-first prompt) + Pillow page lock |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · tree priority · rich traditional colors · ~70% plate width |
| **FRAME** | ON — warm gold page margins (v16 lock) |
| **source** | style-lock-v2 + v11 window DNA (tree not copied cropped) |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE — open cream above/below |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Prompt order

1. FULL traditional Christmas tree (complete, rich deep green)
2. Window scene complements the tree

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v16-v19-board.png`
- Script: `scripts/_scratch/_p01_v19_tree_first.py`
"""
    out = DEV / "v19"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v19: Image.Image) -> Path:
    v16 = Image.open(V16).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v16 vs v19 (tree-first, complete rich tree)",
        fill=(40, 30, 28),
        font=board_font(22),
    )
    draw.text(
        (margin, 68),
        "Same gold page frame · cream center · tree painted FIRST then window · deep greens / warm golds / soft reds",
        fill=(90, 70, 60),
        font=board_font(13),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v16, "v16 — KEEP", "Tree soft / incomplete on the right"),
            (v19, "v19 — TREE-FIRST", "Complete rich tree + window · wider plate"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(18))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v16-v19-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    out_dir = DEV / "v19"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    dna_url = prepare_upload(V11, "v11-window-dna-only.png", key)

    print("submit v19")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, dna_url],
            "image_size": {"width": SIZE, "height": SIZE},
            "num_images": 1,
            "output_format": "png",
        },
    )
    print("  request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or result.get("output", {}).get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:4000])
    url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = result.get("seed") or result.get("output", {}).get("seed")
    req_id = submitted.get("request_id") or ""

    raw = download(url, out_dir / "art-scene-raw.png")
    scene = scrub_scene_text(raw)
    scene.save(out_dir / "art-scene.png", "PNG")
    art = compose_page(scene)
    art.save(out_dir / "art.png", "PNG")
    art.save(out_dir / "page.png", "PNG")

    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "prompt_order": "tree first, window second",
        "page_lock": "v16 gold margins + cream",
        "prompt": PROMPT,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id)
    board = build_board(art)
    print(f"saved {out_dir / 'art.png'} {art.size} seed {seed}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
