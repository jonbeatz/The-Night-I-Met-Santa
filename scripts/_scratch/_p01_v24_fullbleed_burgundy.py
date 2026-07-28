#!/usr/bin/env python3
"""P01 v24 — from v23: full-bleed burgundy, NO cream frame/vignette (Qwen 2 Pro /edit)."""
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
DEV = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
SRC = DEV / "v23" / "art.png"
OUT = DEV / "v24"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-28"
SIZE = 2048

PROMPT = (
    "Edit Image 2 into a children's-book TITLE PAGE illustration — ART ONLY, no text, no letters. "
    "Image 1 = paint STYLE + burgundy wall color lock. "
    "Image 2 = KEEP this scene: winter WINDOW with cream curtains, moon, snow, Santa sleigh silhouette, "
    "holly on sill, COMPLETE Christmas TREE on the right with ALL gifts fully visible, deep burgundy walls. "
    "REQUIRED CHANGE — remove the cream/ivory FRAME and vignette entirely. "
    "NO soft cream border, NO feathered white margin, NO oval vignette, NO page-edge wash. "
    "The ENTIRE square canvas must be continuous deep house BURGUNDY painted wall (#4A0E17 / wine-red "
    "watercolor like Image 1 walls), edge to edge, with the window + tree + gifts sitting ON that full-bleed "
    "burgundy interior. Soft painterly gouache/watercolor texture on the burgundy, but solid coverage to all "
    "four edges — not fading to cream. Keep window, curtains, tree, gifts composition. No people, no faces."
)
NEGATIVE = (
    "cream border, ivory frame, white vignette, soft white margin, oval vignette, feathered cream edges, "
    "page frame, beige mat, pale wash around scene, cropped tree, cut-off gifts, pale walls, "
    "photorealistic, people, faces, text, letters, hard black border, white background"
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
    recipe = f"""# RECIPE — P01-title / v24

| Field | Value |
|-------|--------|
| **name** | Winter Window — full-bleed burgundy · no frame |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | `single` |
| **version** | v24 |
| **date** | {DAY} |
| **lane** | Qwen 2 Pro Edit (mock/development) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 2 image_urls |
| **FRAME** | **OFF** — full-bleed burgundy to all edges |
| **seed** | {seed} |
| **status** | dial — awaiting Jon eye |
| **source** | Image1 style-lock-v2 · Image2 `P01-title/v23/art.png` |

## Change vs v23

- Remove cream vignette / page frame entirely.
- Continuous deep burgundy wall (`#4A0E17`) edge-to-edge around window + full tree + gifts.

## Notes

- Board: `Media/generated/mocks/_INDEX/P01-title-v23-v24-board.png`
- Script: `scripts/_scratch/_p01_v24_fullbleed_burgundy.py`
- Does **not** auto-replace `art.png` until Jon KEEP.
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    meta = {
        "unit": "P01-title",
        "version": "v24",
        "date": DAY,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "seed": seed,
        "status": "dial",
        "image_urls": urls,
        "result_url": result_url,
        "changes": ["no cream frame", "full-bleed burgundy walls"],
        "source": "v23",
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def build_board(v24: Image.Image) -> Path:
    v23 = Image.open(SRC).convert("RGB")
    v23.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
    pad = 24
    label_h = 72
    w = SIZE * 2 + pad * 3
    h = SIZE + pad * 2 + label_h
    board = Image.new("RGB", (w, h), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
        font_sm = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font
    draw.text(
        (pad, 16),
        "P01 Title — v23 (cream vignette)  vs  v24 (full-bleed burgundy, no frame)",
        fill=(40, 40, 40),
        font=font,
    )
    board.paste(v23, (pad, label_h))
    board.paste(v24.resize((SIZE, SIZE), Image.Resampling.LANCZOS), (pad * 2 + SIZE, label_h))
    draw.text((pad, h - 28), "v23", fill=(80, 80, 80), font=font_sm)
    draw.text((pad * 2 + SIZE, h - 28), "v24 dial", fill=(80, 80, 80), font=font_sm)
    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / "P01-title-v23-v24-board.png"
    board.save(out, optimize=True)
    return out


def main() -> None:
    load_env()
    key = fal_key()
    if not SRC.is_file():
        raise SystemExit(f"missing {SRC}")
    OUT.mkdir(parents=True, exist_ok=True)

    print("upload style-lock + v23")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    src_url = prepare_upload(SRC, "p01-v23-src.png", key)
    urls = [style_url, src_url]

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
            "image_size": {"width": SIZE, "height": SIZE},
        },
    )
    print("request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    result_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = int(result.get("seed") or 0)

    art_path = OUT / "art.png"
    download(result_url, art_path)
    print("saved", art_path)

    im = Image.open(art_path).convert("RGB")
    write_docs(seed, urls, result_url)
    board = build_board(im)
    print("board", board)
    print("DONE v24 seed", seed)


if __name__ == "__main__":
    main()
