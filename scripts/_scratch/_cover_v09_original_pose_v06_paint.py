#!/usr/bin/env python3
"""Cover v09 — ORIGINAL pose lock (boy lean + Santa face hidden) + v06 deep paint restyle.
Avoids editing the broken v07/v08 double-head plates.
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
COVER = DEV / "art.png"  # pose/composition lock
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"  # paint lock
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
OUT = DEV / "v09-original-pose-v06-paint"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625

PROMPT = (
    "Children's book COVER — ART ONLY, square. "
    "Image 1 is the COMPOSITION LOCK — preserve its layout and poses almost exactly: "
    "ONE boy only (never two heads) peeking from the dark hallway, leaning FORWARD into the "
    "doorway so his head is well into the lit frame (back/side view, hand on doorframe); "
    "Santa kneeling at the sack with his HEAD turned toward the Christmas tree / away so his "
    "FACE is mostly hidden (hat + back of head — do NOT show a clear left profile face). "
    "REMOVE any gold title lettering and 'Written By' from Image 1 — blank painted ceiling/wall. "
    "REMOVE the framed picture/poster on the hallway wall — plain dark wall. "
    "Image 2 is the PAINT/COLOR LOCK — restyle Image 1's room into Image 2's deep rich saturated "
    "burgundy/plum walls, thick oil/gouache brush texture, warmer glowing tree light, fireplace "
    "glow — deeper and more painting-like like Image 2. Keep Christmas tree, presents, armchair, "
    "fireplace feeling of Image 2 where it fits Image 1's layout. "
    "Image 3 = Boy G0 identity (messy dark-brown hair, oatmeal holly PJs red cuffs) on Image 1's "
    "single peek pose. "
    "Priority order: (1) single boy lean like Image 1, (2) Santa face hidden toward tree like "
    "Image 1, (3) Image 2 deep paint, (4) no hallway poster, (5) no title text."
)
NEGATIVE = (
    "two heads, double head, duplicate boy, ghost head, twin faces, second head, "
    "Santa clear left profile face, Santa looking at boy, Santa face fully visible, "
    "title text, The Night I Met Santa, Written By, gold letters, typography, "
    "hallway poster, framed photo beside boy, pale washed color, cream walls"
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
        f"""# RECIPE — Cover / v09-original-pose-v06-paint

| Field | Value |
|-------|--------|
| **version** | v09-original-pose-v06-paint |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | {seed} |
| **print** | **{PRINT}×{PRINT}** @ 300 DPI |
| **status** | dial |
| **refs** | Image1 original (pose) · Image2 v06 (paint) · Image3 boy-G0 |
| **strategy** | Pose lock on original; paint restyle from v06 — skip broken v07/v08 |

## Goals

- Single boy leaning into doorway (original)
- Santa face mostly hidden toward tree (original)
- No hallway poster; no title text
- Deep saturated paint like v06
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "Cover",
                "version": "v09-original-pose-v06-paint",
                "date": DAY,
                "seed": seed,
                "status": "dial",
                "print_px": [PRINT, PRINT],
                "dpi": 300,
                "image_urls": urls,
                "result_url": result_url,
                "strategy": "original_pose_lock_v06_paint",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def build_board(alt: Image.Image) -> Path:
    keep = Image.open(COVER).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
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
        "Cover — beige-v2 KEEP  vs  v09 (original poses · v06 deep paint · no poster)",
        fill=(40, 40, 40),
        font=font,
    )
    board.paste(keep, (pad, label_h))
    board.paste(alt_s, (pad * 2 + GEN, label_h))
    draw.text((pad, h - 26), "beige-v2 KEEP", fill=(80, 80, 80), font=font_sm)
    draw.text((pad * 2 + GEN, h - 26), "v09 dial", fill=(80, 80, 80), font=font_sm)
    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / "Cover-beige-v2-vs-v09-board.png"
    board.save(out, optimize=True)
    return out


def main() -> None:
    load_env()
    key = fal_key()
    for p in (COVER, V06, BOY):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    OUT.mkdir(parents=True, exist_ok=True)

    print("upload original (pose) + v06 (paint) + boy G0")
    urls = [
        prepare_upload(COVER, "cover-original-pose.png", key),
        prepare_upload(V06, "cover-v06-paint.png", key),
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
    im.crop((0, 400, 700, 1600)).resize((350, 600)).save(
        INDEX / "cover-v09-boy-crop.png", optimize=True
    )
    im.crop((900, 700, 1800, 1800)).resize((450, 450)).save(
        INDEX / "cover-v09-santa-crop.png", optimize=True
    )
    print("board", board)
    print("DONE v09 seed", seed)


if __name__ == "__main__":
    main()
