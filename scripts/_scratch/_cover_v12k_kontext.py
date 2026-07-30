#!/usr/bin/env python3
"""Cover v12k — Flux Kontext surgical on v06 (targeted local edits)."""
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
COVER = DEV / "art.png"
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"
OUT = DEV / "v12k-kontext-v06"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/flux-pro/kontext"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625

PROMPT = (
    "Keep the same painting and room. Remove the framed picture from the dark hallway wall. "
    "Turn Santa's head away so his face is mostly hidden (back of hat toward viewer, looking "
    "into the Christmas tree). Fix the peeking boy so he has only one head and leans further "
    "into the doorway. Keep deep rich burgundy paint colors. No text."
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


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)
    print("upload v06")
    url = prepare_upload(V06, "cover-v06.png", key)
    print("submit flux-pro/kontext")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "image_url": url,
            "num_images": 1,
            "output_format": "png",
            "guidance_scale": 3.5,
            "enhance_prompt": False,
            "aspect_ratio": "1:1",
        },
    )
    print("request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    result_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    raw = OUT / "art-raw.png"
    download(result_url, raw)
    im = Image.open(raw).convert("RGB")
    if im.size != (GEN, GEN):
        im = im.resize((GEN, GEN), Image.Resampling.LANCZOS)
    im.save(OUT / "art.png", optimize=True)
    im.resize((PRINT, PRINT), Image.Resampling.LANCZOS).save(
        OUT / "art-2625.png", optimize=True, dpi=(300, 300)
    )
    (OUT / "RECIPE.md").write_text(
        f"# RECIPE — Cover / v12k-kontext-v06\n\nmodel: fal-ai/flux-pro/kontext\nseed: {seed}\nbase: v06 surgical\n",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v12k-kontext-v06",
                "seed": seed,
                "model": "fal-ai/flux-pro/kontext",
                "result_url": result_url,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    # board vs v06
    v06 = Image.open(V06).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    pad, label_h = 20, 64
    board = Image.new("RGB", (GEN * 2 + pad * 3, GEN + pad * 2 + label_h), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.text((pad, 12), "v06  vs  v12k Flux Kontext surgical", fill=(40, 40, 40), font=font)
    board.paste(v06, (pad, label_h))
    board.paste(im.resize((GEN, GEN)), (pad * 2 + GEN, label_h))
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(INDEX / "Cover-v06-vs-v12k-board.png", optimize=True)
    im.crop((0, 400, 700, 1600)).resize((350, 600)).save(INDEX / "cover-v12k-boy-crop.png")
    im.crop((1100, 800, 1650, 1400)).resize((400, 400)).save(INDEX / "cover-v12k-santa-head.png")
    print("DONE v12k seed", seed)


if __name__ == "__main__":
    main()
