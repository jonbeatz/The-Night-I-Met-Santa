#!/usr/bin/env python3
"""Cover v07 — from v06 + original: no hallway poster · Santa face hidden · boy lean right · keep deep paint.
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
COVER = DEV / "art.png"  # original: Santa face hidden, boy lean into frame
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
OUT = DEV / "v07-no-poster-santa-back"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625

PROMPT = (
    "Edit these references into one children's book COVER — ART ONLY, square. "
    "Image 2 = v06 BEST BASE — KEEP its deep rich burgundy/plum painted walls, warm tree glow, "
    "fireplace, armchair, window, presents, Santa with red hat kneeling at the sack, "
    "no title text, no swinging white door leaf. Keep that SAME deep dark painted color palette. "
    "Image 1 = ORIGINAL COVER — copy EXACTLY: (A) Santa's HEAD orientation — turned away so you "
    "barely see his face (mostly back/side of head and hat, beard edge only — NOT a clear profile "
    "face looking left into the room); (B) the boy's peek lean — body and head leaning MORE into "
    "the lit doorway so his head sits further RIGHT in the frame (more of his head/shoulders "
    "visible inside the room light), still mostly back/side view, hand on doorframe. "
    "Image 3 = Boy G0 identity (messy dark-brown hair, oatmeal holly PJs with red cuffs). "
    "REQUIRED CHANGES vs Image 2: "
    "1) REMOVE the framed poster/photo from the dark hallway wall — plain empty wall, no picture. "
    "2) Turn Santa's head MORE toward the RIGHT / away from camera so his face is mostly hidden "
    "like Image 1 (do not show a clear facial profile). "
    "3) Shift the boy lean so his head is more in-frame toward the room, like Image 1. "
    "Keep Image 2's deep rich paint. Scrub any title lettering. No typography."
)
NEGATIVE = (
    "hallway poster, framed picture on hallway wall, photo on wall beside boy, "
    "Santa face clearly visible, Santa profile face looking left, Santa looking at boy, "
    "boy facing camera full frontal, boy too far left only half head, "
    "title text, gold letters, Written By, pale washed color, cream walls, open white door leaf"
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
        f"""# RECIPE — Cover / v07-no-poster-santa-back

| Field | Value |
|-------|--------|
| **version** | v07-no-poster-santa-back |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | {seed} |
| **print** | **{PRINT}×{PRINT}** @ 300 DPI |
| **status** | dial |
| **refs** | Image1 original cover · Image2 v06 · Image3 boy-G0 |

## Changes vs v06

- Remove hallway poster/photo
- Santa head turned further right — face mostly hidden (like original)
- Boy lean more into frame (head further right)
- Keep v06 deep rich paint
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "Cover",
                "version": "v07-no-poster-santa-back",
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
    keep.thumbnail((GEN, GEN), Image.Resampling.LANCZOS)
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
        "Cover — beige-v2 KEEP  vs  v07 (no poster · Santa face hidden · boy lean · deep paint)",
        fill=(40, 40, 40),
        font=font,
    )
    board.paste(keep.resize((GEN, GEN), Image.Resampling.LANCZOS), (pad, label_h))
    board.paste(alt_s, (pad * 2 + GEN, label_h))
    draw.text((pad, h - 26), "beige-v2 KEEP", fill=(80, 80, 80), font=font_sm)
    draw.text((pad * 2 + GEN, h - 26), "v07 dial", fill=(80, 80, 80), font=font_sm)
    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / "Cover-beige-v2-vs-v07-board.png"
    board.save(out, optimize=True)
    return out


def main() -> None:
    load_env()
    key = fal_key()
    for p in (COVER, V06, BOY):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    OUT.mkdir(parents=True, exist_ok=True)

    print("upload original + v06 + boy G0")
    urls = [
        prepare_upload(COVER, "cover-original.png", key),
        prepare_upload(V06, "cover-v06.png", key),
        prepare_upload(BOY, "boy-G0.png", key),
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
    print("DONE v07 seed", seed)


if __name__ == "__main__":
    main()
