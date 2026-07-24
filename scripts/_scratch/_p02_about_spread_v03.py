#!/usr/bin/env python3
"""P02 about-dedication v03 — widen L/R, open center for text (not push-down)."""
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
OUT = ROOT / "Media/generated/mocks/P02-about-spread/v03"
V01 = ROOT / "Media/generated/mocks/P02-about-spread/v01/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
W, H = 2048, 1024

PROMPT = (
    "Edit image 2 — KEEP this exact wide layout and full room height. "
    "Image 1 = watercolor/gouache style only. "
    "LEFT third: stone fireplace with green garland, stockings, fire — owns the left page. "
    "RIGHT third: Christmas tree with warm lights + presents + wooden door with wreath — owns the right page. "
    "CENTER (where pages meet): open soft burgundy wall with gentle golden firelight glow only — "
    "NO furniture, NO ornaments cluster, NO dense detail — breathing room for text clouds "
    "(About on left-center, Dedication on right-center). "
    "Ceiling and upper walls stay visible — full room, not cropped or squished down. "
    "Deep burgundy walls, wooden floor continuous across the spread, soft feathered vignette (FRAME ON). "
    "Unify seams so it reads as one seamless living room. "
    "Art only — no letters, no title, no watermark, no people."
)

NEGATIVE = (
    "text, letters, typography, watermark, people, gutter line, page fold, "
    "scene pushed to bottom, cream top third wash, squished room, "
    "fireplace in center, tree in center, busy middle wall, dense detail at gutter"
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


def sample_burgundy(src: Image.Image) -> tuple[int, int, int]:
    """Sample mid-upper wall between fireplace and tree (approx)."""
    # v01: wall above floor mid-spread
    px = []
    for x in range(int(W * 0.42), int(W * 0.58), 8):
        for y in range(int(H * 0.18), int(H * 0.45), 8):
            px.append(src.getpixel((min(x, src.width - 1), min(y, src.height - 1))))
    if not px:
        return (90, 35, 45)
    r = sum(p[0] for p in px) // len(px)
    g = sum(p[1] for p in px) // len(px)
    b = sum(p[2] for p in px) // len(px)
    return (r, g, b)


def build_widen_prep() -> Path:
    """Force L fireplace / open center / R tree+door while keeping full height."""
    src = Image.open(V01).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    burgundy = sample_burgundy(src)
    print("sampled burgundy", burgundy)

    # Source crops (v01 composition is fairly centered — take strong L and R thirds)
    left_src = src.crop((0, 0, int(W * 0.42), H))  # fireplace side
    right_src = src.crop((int(W * 0.48), 0, W, H))  # tree + door

    # Target bands: L ~0–34%, center open 34–66%, R 66–100%
    left_w = int(W * 0.34)
    right_w = int(W * 0.34)
    left = left_src.resize((left_w, H), Image.Resampling.LANCZOS)
    right = right_src.resize((right_w, H), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (W, H), burgundy)

    # Soft vertical gradient center: burgundy → warm glow → burgundy
    center = Image.new("RGB", (W, H), burgundy)
    cd = ImageDraw.Draw(center)
    glow = (180, 120, 70)  # warm golden hint
    cx0, cx1 = int(W * 0.30), int(W * 0.70)
    for x in range(cx0, cx1):
        # distance from true center
        t = abs((x - W / 2) / (W * 0.20))
        t = max(0.0, min(1.0, t))
        # near center = more glow wash (still soft wall, not bright)
        mix = 0.22 * (1.0 - t)  # max 22% glow at gutter
        r = int(burgundy[0] * (1 - mix) + glow[0] * mix)
        g = int(burgundy[1] * (1 - mix) + glow[1] * mix)
        b = int(burgundy[2] * (1 - mix) + glow[2] * mix)
        cd.line([(x, 0), (x, H)], fill=(r, g, b))
    # Soften + slight paper noise via blur
    center = center.filter(ImageFilter.GaussianBlur(radius=18))
    # Keep some vertical vignette darkness at top/bottom of center wall
    top_shade = Image.new("L", (W, H), 0)
    td = ImageDraw.Draw(top_shade)
    for y in range(int(H * 0.35)):
        a = int(40 * (1 - y / (H * 0.35)))
        td.line([(cx0, y), (cx1, y)], fill=a)
    for y in range(int(H * 0.75), H):
        a = int(50 * ((y - H * 0.75) / (H * 0.25)))
        td.line([(cx0, y), (cx1, y)], fill=a)
    shade_rgb = Image.new("RGB", (W, H), (40, 15, 20))
    center = Image.composite(shade_rgb, center, top_shade.filter(ImageFilter.GaussianBlur(12)))

    canvas.paste(center, (0, 0))

    # Feather L/R panels into center
    def feather_paste(dst: Image.Image, panel: Image.Image, x0: int, feather: int, from_left: bool) -> None:
        rgba = panel.convert("RGBA")
        alpha = Image.new("L", panel.size, 255)
        ad = ImageDraw.Draw(alpha)
        pw, ph = panel.size
        if from_left:
            for i in range(feather):
                t = i / max(1, feather - 1)
                a = int(255 * (1 - t * t * (3 - 2 * t)))  # fade on right edge
                ad.line([(pw - 1 - i, 0), (pw - 1 - i, ph)], fill=a)
        else:
            for i in range(feather):
                t = i / max(1, feather - 1)
                a = int(255 * (1 - t * t * (3 - 2 * t)))  # fade on left edge
                ad.line([(i, 0), (i, ph)], fill=a)
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=6))
        rgba.putalpha(alpha)
        base = dst.convert("RGBA")
        base.paste(rgba, (x0, 0), rgba)
        dst.paste(base.convert("RGB"))

    feather_paste(canvas, left, 0, feather=90, from_left=True)
    feather_paste(canvas, right, W - right_w, feather=90, from_left=False)

    # Mild floor continuity: darken lower center slightly so floor reads continuous
    floor = Image.new("L", (W, H), 0)
    ImageDraw.Draw(floor).rectangle([int(W * 0.28), int(H * 0.78), int(W * 0.72), H], fill=180)
    floor = floor.filter(ImageFilter.GaussianBlur(20))
    # sample floor tone from v01
    fl = src.getpixel((W // 2, int(H * 0.88)))
    floor_rgb = Image.new("RGB", (W, H), fl)
    canvas = Image.composite(floor_rgb, canvas, floor)

    # Outer cream vignette (FRAME ON hint)
    cream = (248, 242, 230)
    vignette = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vignette).rounded_rectangle([24, 24, W - 24, H - 24], radius=70, fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=22))
    canvas = Image.composite(canvas, Image.new("RGB", (W, H), cream), vignette)

    # Slight overall warmth match to style
    canvas = ImageEnhance.Color(canvas).enhance(1.05)

    OUT.mkdir(parents=True, exist_ok=True)
    prep = OUT / "_prep-widen-center.png"
    canvas.save(prep, "PNG")
    print("prep", prep)
    return prep


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)

    prep = build_widen_prep()
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    prep_url = prepare_upload(prep, "p02-v03-prep.png", key)

    # Also attach v01 as identity so polish keeps fireplace/tree fidelity (3-URL cap)
    v01_url = prepare_upload(V01, "p02-v01-keep.png", key)

    # Order: style, layout prep (camera), v01 (detail identity)
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": (
                "Image 1 = paint style. Image 2 = LAYOUT to keep (wide L/R, open center wall). "
                "Image 3 = detail identity for fireplace, tree, door, presents, lighting. "
                + PROMPT
            ),
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, prep_url, v01_url],
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

    recipe = f"""# RECIPE — P02-about-spread / v03

| Field | Value |
|-------|--------|
| **name** | About + Dedication — wide L/R · open center text wall |
| **unit** | P02-about-spread |
| **book page** | 2\\|3 · About + Dedication · FULL SPREAD |
| **page role** | spread |
| **spread side** | wide-master |
| **version** | v03 |
| **date** | {DAY} |
| **lane** | Pillow widen prep → Qwen 2 Pro Edit polish |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: style-lock + widen prep + v01 identity |
| **FRAME** | ON |
| **concept** | Full room height; fireplace owns left third; tree+door own right third; soft burgundy center for text |
| **changes** | vs v02: **not** push-down / cream top. vs v01: recompose wider with open gutter wall |
| **size** | 2048×1024 dial |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | About (L-center) · Dedication (R-center) — InDesign later |
| **type_zone** | Soft burgundy wall near spread center on each page half |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- image 1: `Media/approved/style-refs/style-lock-v2.png`
- image 2: `_prep-widen-center.png` (this folder) — forced L/R geometry
- image 3: `../v01/art.png` — keep scene detail
- base: v01 (not v02 squish)

## Prompt

Image 1 = paint style. Image 2 = LAYOUT to keep… Image 3 = detail identity…

{PROMPT}

## Negative / constraints

{NEGATIVE}

## Gotchas

- v02 push-down felt too squished — Jon rejected that text strategy.
- Geometry-first again (Pillow widen) so Qwen doesn’t ignore the open center.

## Related

- Script: `scripts/_scratch/_p02_about_spread_v03.py`
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "request_id": req_id,
                "seed": seed,
                "fal_image_url": img_url,
                "prep": str(prep),
                "base": str(V01),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
