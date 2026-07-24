#!/usr/bin/env python3
"""P01 v15 — clean cream center + soft watercolor PAGE-PERIMETER frame only."""
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
V14 = DEV / "v14" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)
PAGE = 2048


PROMPT = (
    "Create a SINGLE square children's-book TITLE PAGE painting — ART ONLY, no text. "
    "Image 1 = watercolor/gouache paint STYLE lock. "
    "Image 2 = the SCENE to preserve: winter WINDOW (moon, snow, faint Santa sleigh silhouette) "
    "plus Christmas TREE with warm lights, ornaments, and presents on the RIGHT. "
    "Keep that vertical rectangular window+tree composition as the focal plate, "
    "centered upper-middle on the page (~60–70% width). "
    "Image 3 = LAYOUT GUIDE ONLY: clean cream open center + soft watercolor wash ONLY along "
    "the outer page perimeter (a quiet picture-frame border). Copy that STRUCTURE — "
    "do not copy any extra objects from image 3. "
    "CRITICAL LAYOUT: "
    "1) Area BEHIND and AROUND the window+tree must be CLEAN CREAM PAPER — no bluish wash, "
    "no peachy glow, no colored background fill behind the art. The artwork floats on clean cream. "
    "2) ADD a soft watercolor FRAME only along the EDGES / MARGINS of the entire page — "
    "like a decorative painted picture frame around the whole page. About 1–2 inches wide "
    "(roughly 8–15% of the page edge). The frame does NOT fill the background behind the window and tree. "
    "3) Frame tones: very subtle quiet cool winter — soft gray-blue, pale silver, faintest winter green. "
    "Organic hand-painted soft edges bleeding into cream. Not loud, not dark, not peach. "
    "Window + tree centered on clean cream. Watercolor frame around page perimeter only. "
    "Nothing colored behind the art. No people, no baked text. "
    "Soft edge = watercolor bleed — NOT bird feathers."
)
NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, "
    "bluish wash behind art, blue background fill, peach glow behind art, colored wash under scene, "
    "full-page colored background, blotch behind window, cloud wash center, "
    "missing Christmas tree, no tree, "
    "feathers, feather, plume, hard black border, thick ornate baroque frame, "
    "photorealistic, people, faces, hands, child"
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


def build_frame_guide() -> Path:
    """Cream center + soft cool wash ONLY in outer perimeter (~12% margin)."""
    im = Image.new("RGB", (PAGE, PAGE), CREAM)
    # Soft perimeter wash in cool winter tones
    wash = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wash)
    margin = int(PAGE * 0.12)  # ~1" feel at 8.5" → ~12%
    # Outer full wash then punch center transparent via mask
    cool = (170, 185, 195, 90)  # soft gray-blue
    cool2 = (190, 200, 195, 55)  # pale silver / hint green
    draw.rectangle([0, 0, PAGE, PAGE], fill=cool)
    # Irregular inner soft edge
    mask = Image.new("L", (PAGE, PAGE), 0)
    md = ImageDraw.Draw(mask)
    inset = margin
    md.rounded_rectangle(
        [inset, inset, PAGE - inset - 1, PAGE - inset - 1],
        radius=40,
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=55))
    # Where mask is white (center) → remove wash; keep wash at edges
    wash_rgb = Image.new("RGBA", (PAGE, PAGE), (*CREAM[:3], 0))
    # Build edge-only alpha = inverse of center mask * wash strength
    edge_a = Image.eval(mask, lambda p: 255 - p)
    # Layer two soft cool tones
    layer1 = Image.new("RGBA", (PAGE, PAGE), (165, 180, 192, 110))
    layer1.putalpha(edge_a.point(lambda p: int(p * 0.85)))
    layer2 = Image.new("RGBA", (PAGE, PAGE), (185, 195, 190, 70))
    edge_a2 = edge_a.filter(ImageFilter.GaussianBlur(30))
    layer2.putalpha(edge_a2.point(lambda p: int(p * 0.55)))
    out = im.convert("RGBA")
    out = Image.alpha_composite(out, layer1)
    out = Image.alpha_composite(out, layer2)
    # Tiny label for the model
    d = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    d.text(
        (PAGE // 2 - 280, PAGE // 2 - 20),
        "LAYOUT GUIDE — clean cream CENTER · frame ONLY at page edges",
        fill=(140, 135, 125, 180),
        font=font,
    )
    path = DEV / "_tmp_v15_frame_guide.png"
    out.convert("RGB").save(path, "PNG")
    return path


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
    text = f"""# RECIPE — P01-title / v15

| Field | Value |
|-------|--------|
| **name** | Winter Window — clean cream center + page-perimeter frame |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v15 |
| **date** | {DAY} |
| **lane** | A2 Qwen 2 Pro Edit |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · clean cream behind art · cool perimeter frame only |
| **FRAME** | ON — page-edge watercolor border (~1–2 in), not background wash |
| **source** | `Media/development/P01-title/v14/art.png` |
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

## Fixes vs v14

- REMOVE bluish/peach wash filling behind window+tree → clean cream paper.
- ADD soft cool watercolor frame only along page perimeter (decorative border).
- KEEP window + moon/snow/sleigh + tree + vertical rectangular scene plate.

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v14-v15-board.png`
- Script: `scripts/_scratch/_p01_v15_cream_perimeter_frame.py`
"""
    out = DEV / "v15"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v15: Image.Image) -> Path:
    v14 = Image.open(V14).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v14 (wash background) vs v15 (clean cream + page frame)",
        fill=(40, 30, 28),
        font=board_font(22),
    )
    draw.text(
        (margin, 68),
        "Keep window+tree · clean cream behind art · cool watercolor frame at page edges only",
        fill=(90, 70, 60),
        font=board_font(14),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v14, "v14 — WASH BACKGROUND", "Bluish wash fills behind the art"),
            (v15, "v15 — CLEAN + PAGE FRAME", "Cream center · perimeter watercolor frame"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(18))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v14-v15-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    guide = build_frame_guide()
    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    scene_url = prepare_upload(V14, "v14-window-tree.png", key)
    guide_url = prepare_upload(guide, "v15-perimeter-frame-guide.png", key)

    print("submit v15")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, scene_url, guide_url],
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

    out_dir = DEV / "v15"
    out_dir.mkdir(parents=True, exist_ok=True)
    art = download(url, out_dir / "art.png")
    art.save(out_dir / "page.png", "PNG")
    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source": "v14/art.png",
        "prompt": PROMPT,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id)
    board = build_board(art)
    print(f"saved {out_dir / 'art.png'} {art.size} seed {seed}")
    print(f"BOARD {board}")
    try:
        guide.unlink(missing_ok=True)
    except OSError:
        pass


if __name__ == "__main__":
    main()
