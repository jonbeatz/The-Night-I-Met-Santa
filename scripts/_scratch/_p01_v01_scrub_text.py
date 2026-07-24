#!/usr/bin/env python3
"""Scrub baked title text from P01-title v01; rebuild comparison board."""
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
BASE = ROOT / "Media/generated/mocks/P01-title"
V01 = BASE / "v01"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"

PROMPT = (
    "Edit image 2 only: remove ALL text, letters, titles, typography, and signatures completely. "
    "Leave open soft cream watercolor space in the center of the wreath where the title was — "
    "ready for live type later. Keep the wreath, village glow, lamppost with red bow, "
    "optional sleigh silhouette, soft feathered vignette, and watercolor/gouache style from image 1. "
    "Do not add new objects. Art only — no letters anywhere."
)
NEGATIVE = "text, letters, typography, title, watermark, logo, signature, words"


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
    if path.suffix.lower() == ".png":
        im.save(buf, format="PNG", optimize=True)
        ctype = "image/png"
    else:
        im.save(buf, format="JPEG", quality=92)
        ctype = "image/jpeg"
        name = Path(name).with_suffix(".jpg").name
    return upload_bytes(key, name, buf.getvalue(), ctype)


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


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def rebuild_board() -> None:
    panel, label_h = 720, 96
    gap, margin, header = 24, 32, 88
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), (245, 240, 230))
    draw = ImageDraw.Draw(board)
    draw.text((margin, 28), "P01 Title — openbook concepts (one ref each + style-lock-v2)", fill=(40, 30, 28), font=font(28))
    draw.text((margin, 58), "Qwen 2 Pro Edit · FRAME ON · no baked text · do not blend", fill=(90, 70, 60), font=font(16))
    slots = [
        (BASE / "v01/art.png", "v01 WREATH FRAME", "Ref2 reimagine · title space inside wreath"),
        (BASE / "v02/art.png", "v02 SNOWMAN LANTERN", "Ref3 reimagine · circular vignette"),
        (BASE / "v03/art.png", "v03 QUIET LANDSCAPE", "Ref1 reimagine · fence bow · open cream"),
    ]
    for i, (path, title, sub) in enumerate(slots):
        meta = json.loads((path.parent / "meta.json").read_text(encoding="utf-8"))
        x = margin + i * (panel + gap)
        y = margin + header
        im = Image.open(path).convert("RGB").resize((panel, panel), Image.Resampling.LANCZOS)
        board.paste(im, (x, y))
        draw.rectangle([x, y + panel, x + panel, y + panel + label_h], fill=(235, 228, 215))
        draw.text((x + 12, y + panel + 14), title, fill=(30, 24, 22), font=font(18))
        draw.text((x + 12, y + panel + 44), sub, fill=(80, 60, 50), font=font(14))
        draw.text((x + 12, y + panel + 68), f"seed {meta.get('seed')}", fill=(110, 90, 80), font=font(13))
    out = ROOT / "Media/generated/mocks/_INDEX/P01-title-openbook-v01-v03-board.png"
    board.save(out, "PNG")
    print("BOARD", out)


def main() -> None:
    load_env()
    key = fal_key()
    # keep first bake
    src = V01 / "art.png"
    bak = V01 / "art-with-baked-text.png"
    if not bak.exists():
        bak.write_bytes(src.read_bytes())

    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    art_url = prepare_upload(bak, "v01-baked.png", key)
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, art_url],
            "image_size": {"width": 2048, "height": 2048},
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
    urllib.request.urlretrieve(img_url, src)
    print("saved scrubbed", src, "seed", seed)

    meta = json.loads((V01 / "meta.json").read_text(encoding="utf-8"))
    meta["scrub_request_id"] = req_id
    meta["scrub_seed"] = seed
    meta["seed"] = seed
    meta["fal_image_url"] = img_url
    meta["note"] = "first bake had title text; scrubbed via Qwen edit → art.png; original in art-with-baked-text.png"
    (V01 / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    recipe = (V01 / "RECIPE.md").read_text(encoding="utf-8")
    if "scrub" not in recipe.lower():
        recipe += f"""

## Text scrub (pass 2)

| Field | Value |
|-------|--------|
| **why** | First bake baked title into wreath center |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **kept** | `art-with-baked-text.png` (pre-scrub) |
| **output** | `art.png` (no text) |

### Scrub prompt

{PROMPT}
"""
        (V01 / "RECIPE.md").write_text(recipe, encoding="utf-8")

    rebuild_board()


if __name__ == "__main__":
    main()
