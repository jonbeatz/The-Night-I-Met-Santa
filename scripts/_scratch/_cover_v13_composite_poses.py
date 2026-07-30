#!/usr/bin/env python3
"""Cover v13 — Pillow regional composite: v06 paint base + original boy lean + original Santa head.
Then light Banana unify pass (color only). Print 2625×2625 @ 300 DPI.
"""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/Cover"
COVER = DEV / "art.png"
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"
OUT = DEV / "v13-composite-original-poses"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/nano-banana-pro/edit"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625


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


def prepare_upload(im: Image.Image, name: str, key: str) -> str:
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, name, buf.getvalue(), "image/png")


def fal_req(key: str, url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Authorization": f"Key {key}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:2000]}") from e


def wait_result(key: str, submitted: dict) -> dict:
    for i in range(180):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as resp:
        dest.write_bytes(resp.read())


def soft_rect_mask(size: tuple[int, int], box: tuple[int, int, int, int], feather: int) -> Image.Image:
    """White inside box, black outside, soft edges."""
    w, h = size
    l, t, r, b = box
    m = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(m)
    draw.rectangle([l, t, r, b], fill=255)
    if feather > 0:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return m


def build_composite() -> Image.Image:
    """v06 base; paste original boy strip + Santa head with soft masks; scrub hallway poster zone."""
    base = Image.open(V06).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    orig = Image.open(COVER).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)

    # 1) Boy + left doorway strip from original (single clean lean)
    # Original boy sits ~x 80–520, y 550–1750
    boy_box = (40, 480, 560, 1780)
    boy_mask = soft_rect_mask((GEN, GEN), boy_box, feather=28)
    out = Image.composite(orig, base, boy_mask)

    # 2) Santa head/upper torso from original (face more hidden)
    # Original Santa head ~x 1180–1580, y 780–1280
    santa_box = (1120, 720, 1620, 1320)
    santa_mask = soft_rect_mask((GEN, GEN), santa_box, feather=36)
    out = Image.composite(orig, out, santa_mask)

    # 3) Scrub hallway poster on original left wall — paint dark from nearby
    # Poster on original ~x 60–220, y 420–720 — sample wall color and fill softly
    poster_box = (50, 380, 240, 760)
    wall_sample = out.crop((80, 900, 200, 1100))
    # average color
    pixels = list(wall_sample.getdata())
    n = len(pixels)
    avg = tuple(sum(c[i] for c in pixels) // n for i in range(3))
    patch = Image.new("RGB", (poster_box[2] - poster_box[0], poster_box[3] - poster_box[1]), avg)
    # slight noise from wall crop resized
    wall_big = wall_sample.resize(patch.size, Image.Resampling.LANCZOS)
    patch = Image.blend(patch, wall_big, 0.55)
    pm = soft_rect_mask(patch.size, (0, 0, patch.size[0], patch.size[1]), feather=18)
    region = out.crop(poster_box)
    region = Image.composite(patch, region, pm)
    out.paste(region, poster_box[:2])

    # 4) Soften title area at top of original bleed if any gold remains from boy strip
    # Top band may have title from original in boy strip — cover with v06 ceiling
    top_box = (40, 0, 900, 220)
    top_mask = soft_rect_mask((GEN, GEN), top_box, feather=22)
    out = Image.composite(base, out, top_mask)

    return out


def unify_paint(comp: Image.Image, key: str) -> tuple[Image.Image, str, object]:
    """Light Banana pass: unify seams + deepen paint; DO NOT change poses."""
    url = prepare_upload(comp, "cover-v13-comp.png", key)
    v06_url = prepare_upload(
        Image.open(V06).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS),
        "cover-v06-paint.png",
        key,
    )
    prompt = (
        "This is already the correct composition. Do NOT change the boy's pose or head "
        "(exactly one head leaning into the doorway). Do NOT change Santa's head orientation "
        "(face mostly hidden toward the tree). Only: blend any seam edges so the painting looks "
        "seamless, remove any leftover hallway poster/frame, remove any title lettering, "
        "and deepen/saturate colors to match Image 2's rich burgundy painted look. ART ONLY."
    )
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": prompt,
            "image_urls": [url, v06_url],
            "num_images": 1,
            "output_format": "png",
            "resolution": "2K",
            "aspect_ratio": "1:1",
            "limit_generations": True,
        },
    )
    print("request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    result_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    raw = OUT / "art-unified-raw.png"
    download(result_url, raw)
    im = Image.open(raw).convert("RGB")
    if im.size != (GEN, GEN):
        im = im.resize((GEN, GEN), Image.Resampling.LANCZOS)
    return im, result_url, result.get("seed")


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)
    INDEX.mkdir(parents=True, exist_ok=True)

    print("build pillow composite (v06 + original boy + original Santa head)")
    comp = build_composite()
    comp.save(OUT / "art-composite.png", optimize=True)
    comp.crop((0, 400, 700, 1600)).resize((350, 600)).save(INDEX / "cover-v13-comp-boy.png")
    comp.crop((1100, 750, 1650, 1350)).resize((400, 400)).save(INDEX / "cover-v13-comp-santa.png")

    print("Banana unify seams + deepen paint (pose freeze)")
    im, result_url, seed = unify_paint(comp, key)
    im.save(OUT / "art.png", optimize=True)
    im.resize((PRINT, PRINT), Image.Resampling.LANCZOS).save(
        OUT / "art-2625.png", optimize=True, dpi=(300, 300)
    )

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — Cover / v13-composite-original-poses

| Field | Value |
|-------|--------|
| **version** | v13-composite-original-poses |
| **date** | {DAY} |
| **method** | Pillow composite (v06 base + original boy strip + original Santa head) → Banana unify |
| **seed** | {seed} |
| **print** | **{PRINT}×{PRINT}** @ 300 DPI |
| **status** | dial |

## Why

Full-scene edits (v07–v12) kept inventing a second boy head and left-facing Santa face.
v13 locks poses from the original cover via regional paste, then only unifies paint.
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v13-composite-original-poses",
                "seed": seed,
                "result_url": result_url,
                "method": "pillow_composite_then_banana_unify",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    keep = Image.open(COVER).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    pad, label_h = 20, 64
    board = Image.new("RGB", (GEN * 2 + pad * 3, GEN + pad * 2 + label_h), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.text(
        (pad, 12),
        "Cover — beige-v2 KEEP  vs  v13 (composite original poses onto v06 paint)",
        fill=(40, 40, 40),
        font=font,
    )
    board.paste(keep, (pad, label_h))
    board.paste(im.resize((GEN, GEN)), (pad * 2 + GEN, label_h))
    board.save(INDEX / "Cover-beige-v2-vs-v13-board.png", optimize=True)
    im.crop((0, 400, 700, 1600)).resize((350, 600)).save(INDEX / "cover-v13-boy-crop.png")
    im.crop((1100, 750, 1650, 1350)).resize((400, 400)).save(INDEX / "cover-v13-santa-head.png")
    print("saved", OUT / "art-2625.png")
    print("DONE v13 seed", seed)


if __name__ == "__main__":
    main()
