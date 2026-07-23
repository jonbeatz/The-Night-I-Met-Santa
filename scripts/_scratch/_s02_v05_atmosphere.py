#!/usr/bin/env python3
"""S02 Threshold v05 — keep v04 composition; add cover oil-painting light/depth."""
from __future__ import annotations

import io
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S02-threshold"
MOCKS = ROOT / "Media/generated/mocks/S02-threshold"
V04 = DEV / "v04" / "art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
# approved/covers/cover-front.png missing on disk — locked beige-v2 winner
COVER = ROOT / "Media/generated/test-book-v1/covers/00-cover-front-APPROVED-beige-v2.png"
if not COVER.is_file():
    COVER = (
        ROOT
        / "Media/generated/mocks/archive/style-refs-pre-tier-reorg/covers/WINNER-cover-front-beige-pj-v2.png"
    )
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
VERSION = "v05"
SIZE = 2048

PROMPT = (
    "Edit image 1 ONLY — the S2 Threshold spread. Image 2 = watercolor/gouache paint style (style-lock). "
    "Image 3 = COVER oil-painting richness reference — match its warmth, depth, and luminous glow. "
    "KEEP the composition of image 1 EXACTLY: boy at open doorway on the LEFT (over-shoulder), "
    "Santa kneeling at ONE Christmas tree on the RIGHT, continuous burgundy living room, wood floor, "
    "gift landscape, faces off the gutter. Same poses, same wardrobe, same props, same one tree. "
    "Do NOT move, crop, or redesign the scene. Do NOT change characters. "
    "ATMOSPHERE ONLY — push image 1 toward the cover's oil-painting richness: "
    "deeper shadows in the corners of the room, richer more saturated burgundy walls, "
    "more luminous golden glow from the Christmas tree lights, warmer brighter hallway spill "
    "behind the boy, firelight-and-Christmas-lights mood with deep atmospheric shadows. "
    "The room should feel warm, deep, and glowing — heirloom oil-painting depth like the cover — "
    "while remaining soft gouache/watercolor storybook edges. Art only — no text."
)

NEGATIVE = (
    "flat lighting, washed out, pale walls, moved characters, different pose, second tree, "
    "new composition, crop, zoom, text, letters, watermark, redesign, shirtsleeves only, "
    "bright white pajamas, packing sack"
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


def prepare_upload(path: Path, name: str, key: str, max_side: int = SIZE) -> str:
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, Path(name).with_suffix(".png").name, buf.getvalue(), "image/png")


def prepare_upload_spread(path: Path, name: str, key: str) -> str:
    """Keep 2:1 spread aspect for composition base."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    target_w, target_h = 2048, 1024
    if (w, h) != (target_w, target_h):
        im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, name, buf.getvalue(), "image/png")


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
    for i in range(120):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}", flush=True)
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


def write_recipe(vdir: Path, seed: int, req_id: str, url: str, urls: dict) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S02-threshold / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S2 Threshold — cover oil-painting light/depth on v04 layout |
| **unit** | S02-threshold |
| **book page** | Flow v2 p6\\|7 · FULL SPREAD |
| **page role** | spread |
| **version** | {VERSION} |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · edit v04 + style-lock-v2 + cover beige-v2 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — atmosphere pass on kept v04 composition |
| **tier** | dial_mock |
| **previous** | v04 |

## Intent

KEEP v04 composition (boy door L · Santa tree R · burgundy · holly PJs · red coat).  
ADD cover oil-painting richness: deeper corner shadows, luminous golden tree + hallway glow, richer burgundy, firelight/Christmas-light warmth.

## Refs used

1. v04 art (composition lock) — `{urls["v04"]}`
2. style-lock-v2 — `{urls["style"]}`
3. cover beige-v2 — `{urls["cover"]}`

Character wardrobe inherited from v04 (boy G0 + santa-G0-v2 already locked there).
""",
        encoding="utf-8",
    )


def build_compare(v04: Image.Image, v05: Image.Image, out: Path) -> None:
    panel_h = 480
    sc = panel_h / v04.height
    w = int(v04.width * sc)
    a = v04.convert("RGB").resize((w, panel_h), Image.Resampling.LANCZOS)
    b = v05.convert("RGB").resize((w, panel_h), Image.Resampling.LANCZOS)
    margin, gap, header, label = 28, 20, 70, 40
    sheet_w = margin * 2 + w
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S2 Threshold — v04 vs v05 ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "v05 = same composition · cover oil-painting depth / glow / richer burgundy",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    d.text((margin, y + panel_h + 8), "v04 — KEEP composition", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(b, (margin, y2))
    d.text((margin, y2 + panel_h + 8), "v05 — atmosphere / oil richness pass", fill=(32, 28, 24), font=font(16))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def main() -> None:
    load_env()
    key = fal_key()
    for p in (V04, STYLE, COVER):
        if not p.is_file():
            raise SystemExit(f"missing {p}")

    print("upload…", flush=True)
    v04_url = prepare_upload_spread(V04, "s02-v04-base.png", key)
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    cover_url = prepare_upload(COVER, "cover-beige-v2.png", key)
    urls = {"v04": v04_url, "style": style_url, "cover": cover_url}
    for k, u in urls.items():
        print(k, u, flush=True)

    payload = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE,
        "image_urls": [v04_url, style_url, cover_url],
        "image_size": {"width": 2048, "height": 1024},
        "num_images": 1,
        "output_format": "png",
        "enable_safety_checker": True,
        "enable_prompt_expansion": False,
    }

    print("submit…", flush=True)
    try:
        submitted = fal_req(key, ENDPOINT, payload)
        req_id = submitted.get("request_id") or submitted.get("id") or ""
        print("request_id", req_id, flush=True)
        result = wait_result(key, submitted)
    except Exception as e:
        print("direct submit failed:", e, flush=True)
        # dump payload urls for MCP retry
        (ROOT / "scripts/_scratch/_s02_v05_payload.json").write_text(
            json.dumps({"payload": payload, "urls": urls}, indent=2), encoding="utf-8"
        )
        raise

    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:4000])
    url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed", 0)
    print("url", url, "seed", seed, flush=True)

    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()

    for vdir in (DEV / VERSION, MOCKS / VERSION):
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "art.png").write_bytes(data)
        write_recipe(vdir, seed, req_id, url, urls)
        meta = {
            "version": VERSION,
            "seed": seed,
            "request_id": req_id,
            "url": url,
            "model": "fal-ai/qwen-image-2/pro/edit",
            "refs": ["v04", "style-lock-v2", "cover-beige-v2"],
            "previous": "v04",
        }
        (vdir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    v04_im = Image.open(V04).convert("RGB")
    v05_im = Image.open(io.BytesIO(data)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S02-threshold-v04-vs-v05-{DAY}.png"
    build_compare(v04_im, v05_im, board)

    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    print("DONE", DEV / VERSION / "art.png")


if __name__ == "__main__":
    main()
