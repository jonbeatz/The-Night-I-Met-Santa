#!/usr/bin/env python3
"""P02 v02b — force top cream via Pillow prep from v01, then Qwen polish."""
from __future__ import annotations

import io
import json
import math
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/generated/mocks/P02-about-spread/v02"
V01 = ROOT / "Media/generated/mocks/P02-about-spread/v01/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"

# Keep prior fal v02 as failed-layout attempt
PRIOR_FAL = OUT / "art-fal-first-pass.png"

PROMPT = (
    "Edit image 2 — keep this EXACT layout and camera: top third is soft warm ivory/cream watercolor wash "
    "for text; bottom two-thirds hold the living room. "
    "Use image 1 for watercolor/gouache paint quality only. "
    "Preserve fireplace LEFT, Christmas tree center-right, presents, door with wreath RIGHT, "
    "deep burgundy walls in the lower room, golden firelight. "
    "Refine the upward fade: burgundy walls dissolve softly into cream; "
    "fire and tree lights cast a gentle warm glow into the cream (light reaches, walls fade). "
    "Soft feathered vignette (FRAME ON). Seamless spread, no gutter. "
    "Art only — no text, no letters, no watermark, no people. Do NOT raise the scene back up."
)

NEGATIVE = (
    "text, letters, typography, watermark, people, gutter line, "
    "scene filling the top, chimney touching top edge, tree crown at top of frame, busy upper third"
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


def build_prep() -> Path:
    """Push v01 into lower ~2/3 on cream; soft dissolve into top wash."""
    src = Image.open(V01).convert("RGB")
    W, H = 2048, 1024
    # cream paper
    cream = (248, 242, 230)
    canvas = Image.new("RGB", (W, H), cream)

    # Scale scene slightly and place so its top sits ~1/3 down
    # Use lower 68% of height for the painted scene
    target_h = int(H * 0.72)
    scale = target_h / src.height
    tw = int(src.width * scale)
    th = target_h
    if tw < W:
        # scale to width instead, then we'll crop/place vertically
        scale = W / src.width
        tw, th = W, int(src.height * scale)
    scene = src.resize((tw, th), Image.Resampling.LANCZOS)

    # Center horizontally; pin bottom to canvas bottom with small margin feel
    x0 = (W - tw) // 2
    y0 = H - th + int(H * 0.02)  # slight overshoot bottom OK; push down
    if y0 > int(H * 0.32):
        y0 = int(H * 0.32)  # ensure top third free
    if y0 + th < H:
        # extend by aligning bottom
        y0 = H - th

    # Build alpha mask: full opacity in lower region, fade across transition band
    rgba = scene.convert("RGBA")
    fade_start = 0
    fade_end = int(th * 0.28)  # top 28% of the placed scene dissolves
    alpha = Image.new("L", (tw, th), 255)
    ad = ImageDraw.Draw(alpha)
    for y in range(fade_end):
        # smoothstep
        t = y / max(1, fade_end - 1)
        a = int(255 * (t * t * (3 - 2 * t)))  # 0 at top → 255 at fade_end
        ad.line([(0, y), (tw, y)], fill=a)
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=8))
    rgba.putalpha(alpha)

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(rgba, (x0, y0), rgba)
    out = canvas_rgba.convert("RGB")

    # Soft vignette toward cream at outer edges (mild)
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    # white = keep, black = cream — use radial-ish rectangle fade
    margin = 36
    vd.rounded_rectangle([margin, margin, W - margin, H - margin], radius=80, fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=28))
    cream_img = Image.new("RGB", (W, H), cream)
    out = Image.composite(out, cream_img, vignette)

    prep = OUT / "_prep-push-down.png"
    OUT.mkdir(parents=True, exist_ok=True)
    out.save(prep, "PNG")
    print("prep", prep, out.size, "y0", y0, "scene", (tw, th))
    return prep


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)

    art_path = OUT / "art.png"
    if art_path.exists() and not PRIOR_FAL.exists():
        art_path.replace(PRIOR_FAL)
        print("kept first fal pass as", PRIOR_FAL.name)

    prep = build_prep()

    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    prep_url = prepare_upload(prep, "p02-v02-prep.png", key)
    print("submit polish")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, prep_url],
            "image_size": {"width": 2048, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "enable_safety_checker": True,
        },
    )
    req_id = submitted["request_id"]
    print("request_id", req_id)
    result = wait_result(key, submitted)
    (OUT / "result-polish.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    images = result["images"]
    img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    urllib.request.urlretrieve(img_url, art_path)
    print("saved", art_path, Image.open(art_path).size, "seed", seed)

    recipe = f"""# RECIPE — P02-about-spread / v02

| Field | Value |
|-------|--------|
| **name** | About + Dedication — same scene, pushed down for top cream text wash |
| **unit** | P02-about-spread |
| **book page** | 2\\|3 · About + Dedication · FULL SPREAD |
| **page role** | spread |
| **spread side** | wide-master |
| **version** | v02 |
| **date** | {DAY} |
| **lane** | A2 + local prep (Pillow push-down) → Qwen polish |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · prep from v01 lower ~2/3 · polish refs: style-lock-v2 + prep |
| **FRAME** | ON |
| **concept** | Keep v01 beauty; top third cream for About/Dedication text clouds |
| **changes** | First fal-only pass failed to open top (`art-fal-first-pass.png`). Final = Pillow push-down prep + Qwen polish. |
| **size** | 2048×1024 dial |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 polish (+ earlier fal attempt) |
| **output** | art.png |
| **script_text** | L: About · R: Dedication — InDesign later |
| **type_zone** | Top third cream wash across spread |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- style: `Media/approved/style-refs/style-lock-v2.png`
- base scene: `Media/generated/mocks/P02-about-spread/v01/art.png`
- prep: `_prep-push-down.png` (this folder)
- failed layout attempt: `art-fal-first-pass.png`

## Prompt (polish)

{PROMPT}

## Negative / constraints

{NEGATIVE}

## Gotchas

- Pure Qwen recompose from v01 kept scene height — forced layout with Pillow first.

## Related

- Scripts: `_p02_about_spread_v02.py` · `_p02_about_spread_v02_polish.py`
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "request_id": req_id,
                "seed": seed,
                "fal_image_url": img_url,
                "prep": str(prep),
                "prior_fal": str(PRIOR_FAL),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
