#!/usr/bin/env python3
"""P02 v02 — fix push-down prep (top third cream) + Qwen polish."""
from __future__ import annotations

import io
import json
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

PROMPT = (
    "Edit image 2 — KEEP this exact camera and layout: large soft cream/ivory watercolor wash "
    "across the TOP THIRD for text; living room occupies only the BOTTOM two-thirds. "
    "Image 1 = paint style only. Preserve fireplace LEFT, tree center-right, presents, "
    "door with wreath RIGHT, burgundy walls below, golden firelight. "
    "Blend the upper fade so burgundy dissolves into cream; soft warm glow may rise into the wash. "
    "FRAME ON soft vignette. No text, no letters, no people. Do NOT stretch the room back to the top."
)
NEGATIVE = (
    "text, letters, watermark, people, gutter, room filling full height, "
    "chimney at top edge, tree touching top, no cream band"
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
    src = Image.open(V01).convert("RGB")
    W, H = 2048, 1024
    cream = (248, 242, 230)
    canvas = Image.new("RGB", (W, H), cream)

    # Scene height = 68% of canvas; width fills full W (slight vertical compress OK for dial)
    scene_h = int(H * 0.68)
    scene = src.resize((W, scene_h), Image.Resampling.LANCZOS)
    y0 = H - scene_h  # top third (~32%) pure cream

    rgba = scene.convert("RGBA")
    fade_h = int(scene_h * 0.22)
    alpha = Image.new("L", (W, scene_h), 255)
    ad = ImageDraw.Draw(alpha)
    for y in range(fade_h):
        t = y / max(1, fade_h - 1)
        a = int(255 * (t * t * (3 - 2 * t)))
        ad.line([(0, y), (W, y)], fill=a)
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=10))
    rgba.putalpha(alpha)

    base = canvas.convert("RGBA")
    base.paste(rgba, (0, y0), rgba)
    out = base.convert("RGB")

    # Mild outer vignette into cream
    vignette = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vignette).rounded_rectangle([28, 28, W - 28, H - 28], radius=72, fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=24))
    out = Image.composite(out, Image.new("RGB", (W, H), cream), vignette)

    prep = OUT / "_prep-push-down.png"
    out.save(prep, "PNG")
    print("prep", prep, "y0", y0, "scene_h", scene_h, "cream_top_px", y0)
    return prep


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)

    prep = build_prep()
    # also save prep as visible checkpoint
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    prep_url = prepare_upload(prep, "p02-v02-prep.png", key)

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
    images = result["images"]
    img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    art = OUT / "art.png"
    urllib.request.urlretrieve(img_url, art)
    print("saved", art, Image.open(art).size, "seed", seed)

    # Update recipe/meta
    meta = {
        "request_id": req_id,
        "seed": seed,
        "fal_image_url": img_url,
        "prep": str(prep),
        "cream_top_fraction": 0.32,
        "method": "Pillow push-down from v01 + Qwen polish",
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (OUT / "result-polish.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    recipe_path = OUT / "RECIPE.md"
    recipe = recipe_path.read_text(encoding="utf-8") if recipe_path.exists() else ""
    if "cream_top_fraction" not in recipe:
        recipe = f"""# RECIPE — P02-about-spread / v02

| Field | Value |
|-------|--------|
| **name** | About + Dedication — pushed down · top cream text wash |
| **unit** | P02-about-spread |
| **book page** | 2\\|3 · About + Dedication · FULL SPREAD |
| **page role** | spread |
| **version** | v02 |
| **date** | 2026-07-22 |
| **lane** | Pillow prep (push-down) → Qwen 2 Pro Edit polish |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · scene in lower 68% · ~32% top cream · polish from prep |
| **FRAME** | ON |
| **concept** | Same v01 scene; top third open for About (L) / Dedication (R) text clouds |
| **changes** | vs v01: composition lower · burgundy fades to cream · glow may rise into wash |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 polish (+ earlier failed fal-only attempt) |
| **output** | art.png |
| **type_zone** | Top ~1/3 cream wash across spread |
| **verdict** | pending |
| **status** | working |

## Refs

- style-lock-v2
- base: `../v01/art.png`
- prep: `_prep-push-down.png`
- failed fal-only: `art-fal-first-pass.png`

## Prompt (polish)

{PROMPT}

## Negative

{NEGATIVE}

## Gotchas

- Pure Qwen recompose from v01 did not open the top; Pillow forced layout first.
"""
        recipe_path.write_text(recipe, encoding="utf-8")
    print("RECIPE updated")


if __name__ == "__main__":
    main()
