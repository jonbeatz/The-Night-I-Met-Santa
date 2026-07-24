#!/usr/bin/env python3
"""P02-about-spread v04 — LAST panorama: connect approved SPLIT hearth + tree."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/generated/mocks/P02-about-spread/v04"
FIRE = ROOT / "Media/generated/mocks/P02-fireplace/v01/art.png"
TREE = ROOT / "Media/generated/mocks/P03-tree/v01/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
W, H = 2048, 1024

PROMPT = (
    "Edit image 2 — KEEP this exact wide-room layout and full ceiling height. "
    "Image 1 = watercolor/gouache paint style only (style-lock). "
    "Image 3 = collage of the approved fireplace (left) and tree+door (right) for scene accuracy — "
    "match stockings, wreaths, presents, fire, door bow. "
    "ONE continuous living room at night: fireplace owns the LEFT page, Christmas tree + door own the RIGHT page. "
    "CENTER (page gutter): open soft burgundy wall + wooden floor + gentle golden firelight wash only — "
    "no furniture, no ornaments cluster, breathing room for About (left-center) and Dedication (right-center) text. "
    "Same burgundy walls, same warm golden light, same wood floor throughout. Ceiling and upper walls visible. "
    "Seamless — no gutter seam, no page fold, no hard join. Soft feathered vignette (FRAME ON). "
    "Art only — no letters, no title, no watermark, no people."
)

NEGATIVE = (
    "text, letters, typography, watermark, people, gutter line, page fold, hard seam, "
    "duplicate fireplace, duplicate tree, busy center wall, furniture in middle, "
    "squished to bottom, cream top third only, pale walls"
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
    im.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
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
        print(f"[{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def sample_wall(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    px = []
    for x in range(int(w * 0.55), int(w * 0.85), 10):
        for y in range(int(h * 0.15), int(h * 0.45), 10):
            px.append(im.getpixel((x, y)))
    r = sum(p[0] for p in px) // len(px)
    g = sum(p[1] for p in px) // len(px)
    b = sum(p[2] for p in px) // len(px)
    return (r, g, b)


def build_prep() -> tuple[Path, Path]:
    """Wide room: fireplace L third, open center, tree+door R third. Full height."""
    fire = Image.open(FIRE).convert("RGB")
    tree = Image.open(TREE).convert("RGB")
    burgundy = sample_wall(fire)
    print("burgundy", burgundy)

    # Fit each single into landscape band height H, keep subject side
    def fit_height(im: Image.Image) -> Image.Image:
        scale = H / im.height
        return im.resize((int(im.width * scale), H), Image.Resampling.LANCZOS)

    fire_h = fit_height(fire)
    tree_h = fit_height(tree)

    # Use left ~55% of fireplace plate (hearth + some wall) and right ~60% of tree plate
    fw = fire_h.width
    fire_panel = fire_h.crop((0, 0, int(fw * 0.62), H))
    tw = tree_h.width
    tree_panel = tree_h.crop((int(tw * 0.08), 0, tw, H))

    # Target widths ~32% each side → open center ~36%
    left_w = int(W * 0.32)
    right_w = int(W * 0.34)
    fire_panel = fire_panel.resize((left_w, H), Image.Resampling.LANCZOS)
    tree_panel = tree_panel.resize((right_w, H), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (W, H), burgundy)

    # Center wall with soft firelight wash from left
    glow = (170, 110, 65)
    center = Image.new("RGB", (W, H), burgundy)
    cd = ImageDraw.Draw(center)
    for x in range(W):
        # firelight stronger toward left-center, softer toward right
        dist_l = abs(x - W * 0.38) / (W * 0.35)
        dist_l = max(0.0, min(1.0, dist_l))
        mix = 0.18 * (1.0 - dist_l)
        # also a little tree warmth from right
        dist_r = abs(x - W * 0.62) / (W * 0.35)
        dist_r = max(0.0, min(1.0, dist_r))
        mix += 0.10 * (1.0 - dist_r)
        mix = min(0.28, mix)
        r = int(burgundy[0] * (1 - mix) + glow[0] * mix)
        g = int(burgundy[1] * (1 - mix) + glow[1] * mix)
        b = int(burgundy[2] * (1 - mix) + glow[2] * mix)
        cd.line([(x, 0), (x, H)], fill=(r, g, b))
    center = center.filter(ImageFilter.GaussianBlur(radius=16))
    canvas.paste(center, (0, 0))

    # Floor strip continuity
    floor_y0 = int(H * 0.72)
    fl = fire.getpixel((fire.width // 3, int(fire.height * 0.88)))
    floor = Image.new("RGB", (W, H - floor_y0), fl)
    floor = ImageEnhance.Brightness(floor).enhance(1.05)
    canvas.paste(floor, (0, floor_y0))
    # soft blur floor into wall
    band = canvas.crop((0, floor_y0 - 40, W, min(H, floor_y0 + 80)))
    band = band.filter(ImageFilter.GaussianBlur(12))
    canvas.paste(band, (0, floor_y0 - 40))

    def feather_paste(dst: Image.Image, panel: Image.Image, x0: int, from_left: bool, feather: int = 100) -> Image.Image:
        base = dst.convert("RGBA")
        rgba = panel.convert("RGBA")
        alpha = Image.new("L", panel.size, 255)
        ad = ImageDraw.Draw(alpha)
        pw, ph = panel.size
        if from_left:
            for i in range(feather):
                t = i / max(1, feather - 1)
                a = int(255 * (1 - (t * t * (3 - 2 * t))))
                ad.line([(pw - 1 - i, 0), (pw - 1 - i, ph)], fill=a)
        else:
            for i in range(feather):
                t = i / max(1, feather - 1)
                a = int(255 * (1 - (t * t * (3 - 2 * t))))
                ad.line([(i, 0), (i, ph)], fill=a)
        alpha = alpha.filter(ImageFilter.GaussianBlur(8))
        rgba.putalpha(alpha)
        base.paste(rgba, (x0, 0), rgba)
        return base.convert("RGB")

    canvas = feather_paste(canvas, fire_panel, 0, from_left=True)
    canvas = feather_paste(canvas, tree_panel, W - right_w, from_left=False)

    # Outer vignette
    cream = (248, 242, 230)
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).rounded_rectangle([20, 20, W - 20, H - 20], radius=64, fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(20))
    canvas = Image.composite(canvas, Image.new("RGB", (W, H), cream), vig)

    OUT.mkdir(parents=True, exist_ok=True)
    prep = OUT / "_prep-connect-splits.png"
    canvas.save(prep, "PNG")

    # Identity collage for slot 3 (both approved singles side by side)
    collage = Image.new("RGB", (2048, 1024), cream)
    fl = fire.resize((1024, 1024), Image.Resampling.LANCZOS)
    tr = tree.resize((1024, 1024), Image.Resampling.LANCZOS)
    collage.paste(fl, (0, 0))
    collage.paste(tr, (1024, 0))
    col_path = OUT / "_ref-split-collage.png"
    collage.save(col_path, "PNG")
    print("prep", prep, "collage", col_path)
    return prep, col_path


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)

    prep, collage = build_prep()
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    prep_url = prepare_upload(prep, "p02-v04-prep.png", key)
    col_url = prepare_upload(collage, "p02-v04-collage.png", key)

    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, prep_url, col_url],
            "image_size": {"width": 2048, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "enable_safety_checker": True,
        },
    )
    req_id = submitted["request_id"]
    print("request_id", req_id)
    (OUT / "job.json").write_text(json.dumps(submitted, indent=2), encoding="utf-8")

    result = wait_result(key, submitted)
    (OUT / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    images = result["images"]
    img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    art = OUT / "art.png"
    urllib.request.urlretrieve(img_url, art)
    print("saved", art, Image.open(art).size, "seed", seed)

    recipe = f"""# RECIPE — P02-about-spread / v04

| Field | Value |
|-------|--------|
| **name** | About + Dedication — LAST panorama · connect approved SPLIT plates |
| **unit** | P02-about-spread |
| **book page** | 2\\|3 · About + Dedication · FULL SPREAD (attempt) |
| **page role** | spread |
| **spread side** | wide-master |
| **version** | v04 |
| **date** | {DAY} |
| **lane** | Pillow connect prep → Qwen 2 Pro Edit |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: style-lock + widen prep + split collage |
| **FRAME** | ON |
| **concept** | One natural wide room from approved P02-fireplace/v01 + P03-tree/v01 · open center for text |
| **changes** | Last panorama try. If fail → lock SPLIT singles and abandon continuous About/Dedication art |
| **size** | 2048×1024 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | About L-center · Dedication R-center |
| **type_zone** | Open burgundy near gutter on each half |
| **verdict** | pending — Jon: last attempt |
| **status** | working |
| **promoted_to** | — |

## Refs

- `P02-fireplace/v01/art.png`
- `P03-tree/v01/art.png`
- `style-lock-v2.png`
- `_prep-connect-splits.png` · `_ref-split-collage.png`

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Notes

- Jon: if this fails, lock SPLIT and move on.
- Script: `scripts/_scratch/_p02_about_spread_v04_connect_splits.py`
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "meta.json").write_text(
        json.dumps({"request_id": req_id, "seed": seed, "fal_image_url": img_url}, indent=2),
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
