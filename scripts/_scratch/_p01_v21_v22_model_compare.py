#!/usr/bin/env python3
"""P01 model test: v21 Krea 2 Medium vs v22 Nano Banana Pro /edit — same prompt, style-lock-v2."""
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
V19 = DEV / "v19" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

KREA = "krea/v2/medium/text-to-image"
BANANA = "fal-ai/nano-banana-pro/edit"

PROMPT = (
    "Children's book TITLE PAGE painting, square 1:1, ART ONLY — no text, no letters, no watermark. "
    "Warm gold watercolor whisper frame along the OUTER PAGE edges only. Clean cream paper center. "
    "Composition: winter WINDOW on the LEFT (four-pane, cream curtains tied back, holly on sill, "
    "full moon, falling snow, faint tiny Santa sleigh and reindeer silhouette crossing the moon) "
    "AND a FULL traditional Christmas TREE on the RIGHT — COMPLETE from star/topper at the tip "
    "down to wrapped presents at the base, nothing cropped top or bottom, small margin of cream "
    "above the treetop, breathing room between window and tree. "
    "Rich traditional Christmas colors: deep forest greens, warm golden lights, soft reds and gold ornaments. "
    "Soft watercolor and gouache, luminous, heirloom storybook — NOT pastel washed-out, NOT photorealistic, "
    "NOT clip-art. Open cream space above for title and below for copyright later."
)
NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, logo, "
    "cropped tree, cut-off treetop, missing star, partial tree, faded tree, "
    "pastel washed-out, people, faces, hands, child, photorealistic, hard black border"
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
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:3000]}") from e


def submit(key: str, endpoint: str, payload: dict) -> dict:
    return fal_req(key, f"https://queue.fal.run/{endpoint}", payload)


def wait_result(key: str, submitted: dict) -> dict:
    for i in range(120):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:4000])
    raise SystemExit("timeout")


def download(url: str, dest: Path) -> Image.Image:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return Image.open(io.BytesIO(data)).convert("RGB")


def save_job(
    ver: str,
    name: str,
    model: str,
    cost: str,
    seed,
    req_id: str,
    art: Image.Image,
    result: dict,
    notes: str,
) -> None:
    out = DEV / ver
    out.mkdir(parents=True, exist_ok=True)
    art.save(out / "art.png", "PNG")
    art.save(out / "page.png", "PNG")
    meta = {
        "version": ver,
        "name": name,
        "model": model,
        "seed": seed,
        "request_id": req_id,
        "cost_note": cost,
        "prompt": PROMPT,
        "notes": notes,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out / "result.json").write_text(json.dumps(result, indent=2)[:25000], encoding="utf-8")
    recipe = f"""# RECIPE — P01-title / {ver}

| Field | Value |
|-------|--------|
| **name** | {name} |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | {ver} |
| **date** | {DAY} |
| **lane** | Model compare (same prompt) |
| **service** | fal.ai |
| **model** | `{model}` |
| **settings** | 1:1 · style-lock-v2 ref · NO text |
| **FRAME** | ON — warm gold page-edge whisper (in prompt) |
| **style** | `Media/approved/style-refs/style-lock-v2.png` |
| **size** | ~2048² / model native |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | {cost} |
| **output** | art.png |
| **type** | NONE |
| **verdict** | pending |
| **status** | working · model test |
| **tier** | development |
| **note** | {notes} |

## Prompt (shared with sibling compare)

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v19-v21-v22-model-board.png`
- Script: `scripts/_scratch/_p01_v21_v22_model_compare.py`
- Sibling: v19 = Qwen 2 Pro Edit baseline
"""
    (out / "RECIPE.md").write_text(recipe, encoding="utf-8")


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def build_board(v21: Image.Image, v22: Image.Image) -> Path:
    v19 = Image.open(V19).convert("RGB")
    panel, label_h, gap, margin, header = 720, 110, 28, 32, 110
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 24),
        "P01 Title — model compare: v19 Qwen · v21 Krea · v22 Banana Pro",
        fill=(40, 30, 28),
        font=board_font(22),
    )
    draw.text(
        (margin, 62),
        "Same prompt · style-lock-v2 · full tree tip-to-base · gold page frame · cream center · NO text",
        fill=(90, 70, 60),
        font=board_font(13),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v19, "v19 — Qwen 2 Pro Edit", "~$0.08 · current rich-tree baseline"),
            (v21, "v21 — Krea 2 Medium", "~$0.03 · T2I + style refs"),
            (v22, "v22 — Nano Banana Pro /edit", "~$0.15 · finals lane"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 10), title, fill=(40, 30, 28), font=board_font(16))
        draw.text((x, y + panel + 42), sub, fill=(90, 70, 60), font=board_font(12))
    out = INDEX / "P01-title-v19-v21-v22-model-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    print("upload style-lock")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)

    # --- v21 Krea ---
    print("submit v21 Krea 2 Medium")
    krea_payload = {
        "prompt": PROMPT + " Avoid: " + NEGATIVE,
        "aspect_ratio": "1:1",
        "creativity": "medium",
        "image_style_references": [{"image_url": style_url}],
    }
    krea_sub = submit(key, KREA, krea_payload)
    print("  request_id", krea_sub.get("request_id"))

    # --- v22 Banana (submit in parallel-ish after krea queued) ---
    print("submit v22 Nano Banana Pro /edit")
    banana_payload = {
        "prompt": PROMPT,
        "image_urls": [style_url],
        "num_images": 1,
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "output_format": "png",
        "limit_generations": True,
        "safety_tolerance": "4",
    }
    banana_sub = submit(key, BANANA, banana_payload)
    print("  request_id", banana_sub.get("request_id"))

    print("wait v21")
    krea_res = wait_result(key, krea_sub)
    krea_imgs = krea_res.get("images") or []
    if not krea_imgs:
        raise SystemExit("Krea no images: " + json.dumps(krea_res, indent=2)[:3000])
    krea_url = krea_imgs[0].get("url") if isinstance(krea_imgs[0], dict) else krea_imgs[0]
    krea_seed = krea_res.get("seed")
    krea_art = download(krea_url, DEV / "v21" / "_dl.png")
    # normalize square display
    krea_art = krea_art.resize((SIZE, SIZE), Image.Resampling.LANCZOS) if max(krea_art.size) != SIZE else krea_art
    save_job(
        "v21",
        "Model test — Krea 2 Medium",
        KREA,
        "~$0.03",
        krea_seed,
        krea_sub.get("request_id") or "",
        krea_art,
        krea_res,
        "Model compare only — not auto-promoted. Do not confuse with archived Gemini P01 v22 fireplace lock.",
    )
    print(f"saved v21 seed {krea_seed}")

    print("wait v22")
    banana_res = wait_result(key, banana_sub)
    banana_imgs = banana_res.get("images") or []
    if not banana_imgs:
        raise SystemExit("Banana no images: " + json.dumps(banana_res, indent=2)[:3000])
    banana_url = banana_imgs[0].get("url") if isinstance(banana_imgs[0], dict) else banana_imgs[0]
    banana_seed = banana_res.get("seed")
    banana_art = download(banana_url, DEV / "v22" / "_dl.png")
    if max(banana_art.size) != SIZE:
        banana_art = banana_art.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    save_job(
        "v22",
        "Model test — Nano Banana Pro /edit",
        BANANA,
        "~$0.15",
        banana_seed,
        banana_sub.get("request_id") or "",
        banana_art,
        banana_res,
        "Model compare only — NEW Banana test plate. Not the old Gemini fireplace title lock.",
    )
    print(f"saved v22 seed {banana_seed}")

    board = build_board(krea_art, banana_art)
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
