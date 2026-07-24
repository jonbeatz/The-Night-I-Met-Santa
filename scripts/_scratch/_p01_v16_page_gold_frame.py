#!/usr/bin/env python3
"""P01 v16 — window+tree on clean cream; warm gold watercolor on PAGE edges only.

Pillow builds the correct structure (Qwen kept framing the art). Optional Qwen polish
softens the gold perimeter into watercolor without moving the frame onto the vignette.
"""
from __future__ import annotations

import io
import json
import os
import random
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
V15 = DEV / "v15" / "art.png"
V11 = DEV / "v11" / "art.png"  # clean window+tree plate (no page frame)
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

PROMPT = (
    "Edit image 2 ONLY — the LAYOUT is LOCKED and already correct. Image 1 = paint style. "
    "Image 2 structure (do not change): "
    "(1) Winter WINDOW + Christmas TREE vignette floating on CLEAN CREAM in the upper-middle. "
    "(2) Wide open CLEAN CREAM above the window for a title and below the tree for copyright. "
    "(3) A barely-there WARM GOLD / soft amber watercolor whisper ONLY on the outermost PAGE margins "
    "(top, bottom, left, right edges of the full square page) — like a soft picture-frame border "
    "for the whole 8.5x8.5 page. The gold must stay at the extreme outer edges and must NOT form "
    "a second frame around the window+tree. "
    "YOUR JOB: only soften the outer-edge gold so it looks like quiet hand-painted watercolor "
    "bleeding into cream (fireplace / tree-light warmth). Keep it extremely subtle. "
    "FORBIDDEN: blue frame, cool wash, any colored wash behind or around the art vignette, "
    "moving gold inward into the title/copyright cream fields, hard borders, text, people."
)
NEGATIVE = (
    "blue frame, cool gray frame, wash behind window, wash behind tree, "
    "frame around art vignette, halo around window, colored background under scene, "
    "loud gold, thick ornate frame, hard border, text, letters, people"
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


def prepare_upload_im(im: Image.Image, name: str, key: str) -> str:
    im = im.convert("RGB")
    im.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, name, buf.getvalue(), "image/png")


def prepare_upload(path: Path, name: str, key: str) -> str:
    return prepare_upload_im(Image.open(path), name, key)


def soft_vignette_rgba(rgb: Image.Image, feather: int = 100) -> Image.Image:
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    inset = max(8, feather // 3)
    draw.rounded_rectangle(
        [inset, inset, w - inset - 1, h - inset - 1],
        radius=int(min(w, h) * 0.05),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def build_page_base() -> Image.Image:
    """Clean cream page + window/tree floating + warm gold PAGE-edge wash only."""
    page = Image.new("RGBA", (SIZE, SIZE), (*CREAM, 255))

    # Scene from v11 — upper-middle; leave open cream for title (top) + copyright (bottom)
    scene = Image.open(V11).convert("RGB")
    art_w = int(SIZE * 0.56)
    scene = scene.resize((art_w, art_w), Image.Resampling.LANCZOS)
    scene_rgba = soft_vignette_rgba(scene, feather=95)
    ax = (SIZE - art_w) // 2
    ay = int(SIZE * 0.22)
    page.alpha_composite(scene_rgba, (ax, ay))

    # Warm gold ONLY in outer ~7–9% (≈0.6–0.75" on 8.5") — whisper, not a band eating type space
    margin = int(SIZE * 0.08)
    cut = Image.new("L", (SIZE, SIZE), 0)
    cd = ImageDraw.Draw(cut)
    cd.rounded_rectangle(
        [margin, margin, SIZE - margin - 1, SIZE - margin - 1],
        radius=28,
        fill=255,
    )
    # Soft falloff: gold lives outside the soft-rect, fading quickly so title/copyright stay cream
    cut = cut.filter(ImageFilter.GaussianBlur(radius=36))
    gold_a = Image.eval(cut, lambda p: max(0, min(255, int((255 - p) * 0.38))))
    gold_a = gold_a.filter(ImageFilter.GaussianBlur(radius=12))
    noise = Image.effect_noise((SIZE, SIZE), 10).convert("L")
    gold_a = Image.blend(gold_a, Image.composite(gold_a, Image.new("L", (SIZE, SIZE), 0), noise), 0.10)

    g1 = Image.new("RGBA", (SIZE, SIZE), (218, 180, 115, 255))
    g1.putalpha(gold_a)
    g2 = Image.new("RGBA", (SIZE, SIZE), (235, 200, 145, 255))
    g2.putalpha(gold_a.point(lambda p: int(p * 0.35)).filter(ImageFilter.GaussianBlur(20)))

    page = Image.alpha_composite(page, g1)
    page = Image.alpha_composite(page, g2)
    return page.convert("RGB")


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
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def download(url: str, dest: Path) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return Image.open(io.BytesIO(data)).convert("RGB")


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(seed, req_id: str, note: str) -> None:
    text = f"""# RECIPE — P01-title / v16

| Field | Value |
|-------|--------|
| **name** | Winter Window — clean cream + warm gold PAGE-edge frame |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v16 |
| **date** | {DAY} |
| **lane** | Pillow structure lock + Qwen 2 Pro Edit polish |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · cream center · warm gold page-perimeter only |
| **FRAME** | ON — page margins (~1″), NOT around art vignette |
| **source scene** | `Media/development/P01-title/v11/art.png` |
| **compare** | v15 framed the art; v16 frames the page |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE — open cream above/below for InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |
| **note** | {note} |

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v15-v16-board.png`
- Script: `scripts/_scratch/_p01_v16_page_gold_frame.py`
"""
    out = DEV / "v16"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v16: Image.Image) -> Path:
    v15 = Image.open(V15).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v15 (frame around ART) vs v16 (warm gold frame around PAGE)",
        fill=(40, 30, 28),
        font=board_font(20),
    )
    draw.text(
        (margin, 68),
        "Clean cream center · open type space · soft amber/gold at outer page edges only",
        fill=(90, 70, 60),
        font=board_font(14),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v15, "v15 — FRAME AROUND ART", "Cool wash hugs the window+tree vignette"),
            (v16, "v16 — FRAME AROUND PAGE", "Warm gold whisper on page margins · cream center"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(18))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v15-v16-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    out_dir = DEV / "v16"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("build pillow page base")
    base = build_page_base()
    base.save(out_dir / "art-pillow-base.png", "PNG")

    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    base_url = prepare_upload_im(base, "v16-page-structure-lock.png", key)

    print("submit v16 polish")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, base_url],
            "image_size": {"width": SIZE, "height": SIZE},
            "num_images": 1,
            "output_format": "png",
        },
    )
    print("  request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or result.get("output", {}).get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:4000])
    url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = result.get("seed") or result.get("output", {}).get("seed")
    req_id = submitted.get("request_id") or ""

    art = download(url, out_dir / "art-qwen.png")
    # Heuristic: title band (upper cream) must stay near paper cream — if Qwen pulls gold inward, keep Pillow
    title = art.crop((SIZE // 2 - 100, int(SIZE * 0.10), SIZE // 2 + 100, int(SIZE * 0.16)))
    px = list(title.getdata())
    avg_b = sum(p[2] for p in px) / len(px)
    avg_r = sum(p[0] for p in px) / len(px)
    # Cream paper ~ (245,240,230); gold-tinted is much lower blue & higher red gap
    creamish = avg_b > 210 and (avg_r - avg_b) < 35
    if creamish:
        final = art
        note = "Qwen polish kept; title cream zone OK"
    else:
        final = base
        note = "Qwen pulled gold inward — kept Pillow page-structure lock as art.png"
        print("FALLBACK to pillow base:", note, f"title_avg RGB~({avg_r:.0f},?,{avg_b:.0f})")
    final.save(out_dir / "art.png", "PNG")
    final.save(out_dir / "page.png", "PNG")
    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "structure": "Pillow page lock (v11 scene + gold page margins)",
        "prompt": PROMPT,
        "note": note,
        "title_zone_creamish": creamish,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id, note)
    board = build_board(final)
    print(f"saved {out_dir / 'art.png'} {final.size} seed {seed} | {note}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
