#!/usr/bin/env python3
"""Cover v08 — fix v07 double-head · Santa face toward tree · deep saturated paint like v06.
Print 2625×2625 @ 300 DPI.
"""
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
DEV = ROOT / "Media/development/Cover"
COVER = DEV / "art.png"  # original: single boy lean + Santa face hidden toward tree
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"  # paint target
V07 = DEV / "v07-no-poster-santa-back" / "art.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
OUT = DEV / "v08-single-boy-santa-tree"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625

# Qwen edit max 3 image_urls — prioritize: original poses, v07 composition, v06 paint
PROMPT = (
    "Edit these into one children's book COVER — ART ONLY, square. Fix Image 2's errors. "
    "Image 2 = v07 BASE composition — KEEP burgundy room, Christmas tree, fireplace, armchair, "
    "presents, Santa in red hat kneeling at sack, dark hallway, white doorframe, NO hallway poster. "
    "CRITICAL BUG FIX — the boy currently has TWO heads (one behind the doorframe, one floating "
    "inside the room). Merge into ONE boy only: keep a single head and body, leaning FORWARD into "
    "the room so his head sits where the second/inner head is — more of his head visible in the "
    "lit doorway, like Image 1. Delete the duplicate head completely. No double exposure. "
    "Image 1 = ORIGINAL COVER pose lock — ONE boy peeking from behind (back/side), leaning into "
    "the doorway; Santa's head turned toward the TREE / away so you barely see his face "
    "(hat + back of head + beard edge, NOT a clear left-facing profile looking into the room). "
    "REQUIRED: turn Santa's HEAD more to the RIGHT so he faces the Christmas tree more — "
    "face mostly hidden like Image 1. Keep kneeling body and sack. "
    "Image 3 = v06 paint/color TARGET — match its DEEP RICH saturated oil/gouache paint: "
    "deeper burgundy, richer warm tree glow, thicker brush texture, more painting-like. "
    "Boy identity: messy dark-brown hair, oatmeal holly PJs with red cuffs (from Image 1/2). "
    "No title text, no typography, no hallway framed photo, no second boy head."
)
NEGATIVE = (
    "two heads, double head, duplicate boy head, twin faces, ghost head, double exposure, "
    "Santa clear left profile face, Santa looking left into room, Santa face fully visible, "
    "hallway poster, framed photo on hallway wall, title text, gold letters, Written By, "
    "pale washed color, flat digital, cream walls, open white door leaf"
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
    im.thumbnail((GEN, GEN), Image.Resampling.LANCZOS)
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


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as resp:
        dest.write_bytes(resp.read())


def write_docs(seed: int, urls: list[str], result_url: str) -> None:
    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — Cover / v08-single-boy-santa-tree

| Field | Value |
|-------|--------|
| **version** | v08-single-boy-santa-tree |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | {seed} |
| **print** | **{PRINT}×{PRINT}** @ 300 DPI |
| **status** | dial |
| **refs** | Image1 original · Image2 v07 · Image3 v06 paint |

## Changes vs v07

- Fix double boy head → one boy leaning into the inner-head position
- Santa head turned toward tree / face more hidden
- Deeper saturated paint like v06
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "Cover",
                "version": "v08-single-boy-santa-tree",
                "date": DAY,
                "seed": seed,
                "status": "dial",
                "print_px": [PRINT, PRINT],
                "dpi": 300,
                "image_urls": urls,
                "result_url": result_url,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def build_board(alt: Image.Image) -> Path:
    keep = Image.open(COVER).convert("RGB")
    keep = keep.resize((GEN, GEN), Image.Resampling.LANCZOS)
    alt_s = alt.resize((GEN, GEN), Image.Resampling.LANCZOS)
    pad, label_h = 20, 64
    w = GEN * 2 + pad * 3
    h = GEN + pad * 2 + label_h
    board = Image.new("RGB", (w, h), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
        font_sm = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font
    draw.text(
        (pad, 12),
        "Cover — beige-v2 KEEP  vs  v08 (single boy lean · Santa toward tree · v06 paint)",
        fill=(40, 40, 40),
        font=font,
    )
    board.paste(keep, (pad, label_h))
    board.paste(alt_s, (pad * 2 + GEN, label_h))
    draw.text((pad, h - 26), "beige-v2 KEEP", fill=(80, 80, 80), font=font_sm)
    draw.text((pad * 2 + GEN, h - 26), "v08 dial", fill=(80, 80, 80), font=font_sm)
    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / "Cover-beige-v2-vs-v08-board.png"
    board.save(out, optimize=True)
    return out


def main() -> None:
    load_env()
    key = fal_key()
    for p in (COVER, V07, V06):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    OUT.mkdir(parents=True, exist_ok=True)

    print("upload original + v07 + v06 paint")
    urls = [
        prepare_upload(COVER, "cover-original.png", key),
        prepare_upload(V07, "cover-v07.png", key),
        prepare_upload(V06, "cover-v06-paint.png", key),
    ]

    print("submit Qwen 2 Pro /edit")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE[:500],
            "image_urls": urls,
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "image_size": {"width": GEN, "height": GEN},
        },
    )
    print("request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    result_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = int(result.get("seed") or 0)

    raw = OUT / "art-2048.png"
    download(result_url, raw)
    im = Image.open(raw).convert("RGB")
    im.save(OUT / "art.png", optimize=True)
    im.resize((PRINT, PRINT), Image.Resampling.LANCZOS).save(
        OUT / "art-2625.png", optimize=True, dpi=(300, 300)
    )
    print("saved", OUT / "art-2625.png", PRINT)

    write_docs(seed, urls, result_url)
    board = build_board(im)
    print("board", board)
    print("DONE v08 seed", seed)


if __name__ == "__main__":
    main()
