#!/usr/bin/env python3
"""P01 v14 — restore tree + soft vertical-rectangle plate (from v12 frame / v11 scene)."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
V11 = DEV / "v11" / "art.png"
V12 = DEV / "v12" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

PROMPT = (
    "Create a SINGLE square children's-book TITLE PAGE painting — ART ONLY, no text. "
    "Image 1 = watercolor/gouache paint STYLE lock. "
    "Image 2 = COMPLETE SCENE to preserve (priority): winter WINDOW on the left/center AND "
    "Christmas TREE with warm lights and a few ornaments on the RIGHT side of the window — "
    "same as this reference. Also keep: full moon, faint tiny Santa sleigh+reindeer silhouette "
    "crossing the moon, falling snow, cream curtains tied back, optional holly on sill / presents. "
    "The tree is REQUIRED — do not crop it out, do not replace it with empty wash. "
    "Image 3 = QUIET FRAME treatment reference only (ignore its missing tree / blotchy outer shape): "
    "borrow only the soft off-white inner glow near the art and the cool winter-toned watercolor "
    "dissolve into cream paper — NOT a peachy blotch cloud. "
    "COMPOSITION SHAPE (critical): the overall art plate must read as a gentle VERTICAL RECTANGLE — "
    "taller than wide — a softly painted rectangular plate with organic irregular watercolor edges. "
    "NOT a random amorphous blotch, NOT a cloud, NOT a circle, NOT an oval splat. "
    "Window + tree form a natural vertical composition; the watercolor frame FOLLOWS that rectangular "
    "shape and bleeds softly into the cream page on all sides. "
    "Place the rectangular plate centered, upper-middle, about 60–70% of page width. "
    "Rich detailed art inside: window left/center, tree right, moon and sleigh above. "
    "Soft off-white/warm ivory inner glow around the scene; outward dissolve in cool soft winter "
    "tones into cream (pale blue-gray / cool ivory washes — quiet, not loud peach). "
    "Organic hand-painted soft edge = watercolor paint bleed only — NO bird feathers, NO plumes, "
    "NO hard border, NO geometric black frame, NO sticker cutout. "
    "Open luminous cream above and below for live title/copyright later. No people, no text."
)
NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, logo, "
    "missing Christmas tree, no tree, tree removed, empty right side, "
    "amorphous blotch, cloud shape, circular splat, oval blob, random wash blob, "
    "feathers, feather, plume, quill, feather wreath, "
    "hard border, black frame, geometric hard rectangle border, sticker cutout, "
    "loud peach blotch, neon wash, photorealistic, people, faces, hands, child"
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
    for i in range(100):
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


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(seed, req_id: str) -> None:
    text = f"""# RECIPE — P01-title / v14

| Field | Value |
|-------|--------|
| **name** | Winter Window — tree restored · soft vertical rectangle |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v14 |
| **date** | {DAY} |
| **lane** | A2 Qwen 2 Pro Edit |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · tree kept · vertical-rectangle plate · cool dissolve |
| **FRAME** | ON — soft rectangular watercolor edge (not blotch) |
| **source scene** | `Media/development/P01-title/v11/art.png` |
| **frame ref** | `Media/development/P01-title/v12/art.png` (glow/dissolve only) |
| **style** | `Media/approved/style-refs/style-lock-v2.png` |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png (art-only for InDesign) |
| **type** | NONE — live Cormorant in InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Fixes vs v12

1. Christmas tree with warm lights restored on the right (from v11).
2. Overall plate shape = gentle vertical rectangle with organic soft edges — not amorphous blotch.

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v12-v14-board.png`
- Script: `scripts/_scratch/_p01_v14_tree_rect_plate.py`
"""
    out = DEV / "v14"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v14: Image.Image) -> Path:
    v12 = Image.open(V12).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v12 (blotch, no tree) vs v14 (tree + vertical rectangle)",
        fill=(40, 30, 28),
        font=board_font(24),
    )
    draw.text(
        (margin, 68),
        "v11 scene priority · v12 quiet glow · cool winter dissolve · Qwen 2 Pro Edit · art only",
        fill=(90, 70, 60),
        font=board_font(14),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v12, "v12 — CURRENT", "No tree · amorphous / blotchy wash"),
            (v14, "v14 — FIXED", "Tree restored · soft vertical-rectangle plate"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(20))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v12-v14-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    v11_url = prepare_upload(V11, "v11-scene-with-tree.png", key)
    v12_url = prepare_upload(V12, "v12-frame-glow-only.png", key)

    print("submit v14")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, v11_url, v12_url],
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

    out_dir = DEV / "v14"
    out_dir.mkdir(parents=True, exist_ok=True)
    art = download(url, out_dir / "art.png")
    art.save(out_dir / "page.png", "PNG")
    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source_scene": "v11/art.png",
        "frame_ref": "v12/art.png",
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
