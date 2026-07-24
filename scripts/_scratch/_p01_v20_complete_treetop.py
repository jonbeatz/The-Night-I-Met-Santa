#!/usr/bin/env python3
"""P01 v20 — v19 lock + complete treetop (star/topper fully visible, nothing cropped)."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
V19 = DEV / "v19" / "art.png"
V19_SCENE = DEV / "v19" / "art-scene.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

PROMPT = (
    "Edit image 2 ONLY — almost everything is LOCKED. Image 1 = watercolor/gouache paint style. "
    "Image 2 is the title-page scene to preserve: rich deep-green Christmas TREE on the RIGHT with "
    "warm golden lights, red and gold ornaments, wrapped presents at the base; winter WINDOW on the LEFT "
    "with moon, falling snow, faint Santa sleigh silhouette, cream curtains, holly on sill; cream interior; "
    "soft vignette to cream. "
    "ONE FIX ONLY: the TREETOP is slightly cut off — make the Christmas tree COMPLETE from the VERY TOP "
    "to the presents at the base. The star or tree-topper and uppermost branches must be FULLY VISIBLE "
    "with a small margin of open cream/space ABOVE the treetop. Nothing cropped at the top. "
    "Nothing cropped at the bottom (presents fully visible). "
    "If needed, shift or scale the composition slightly taller / pull the camera back a touch so the "
    "entire tree fits inside the painted plate with breathing room above the tip. "
    "Keep rich traditional colors (deep greens, warm golds, soft reds) — NOT pastel. "
    "Do NOT change the window, moon, sleigh, presents richness, or overall layout otherwise. "
    "No people, no baked text."
)
NEGATIVE = (
    "cropped treetop, cut-off star, missing topper, truncated tree tip, tree tip off-frame, "
    "cropped presents, faded tree, pastel tree, washed out, "
    "text, letters, people, faces, hands, photorealistic, blue wash behind art"
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


def download(url: str, dest: Path) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return Image.open(io.BytesIO(data)).convert("RGB")


def scrub_scene_text(scene: Image.Image) -> Image.Image:
    im = scene.convert("RGBA")
    w, h = im.size
    blob = Image.new("L", (w, h), 0)
    bd = ImageDraw.Draw(blob)
    bd.rectangle([int(w * 0.05), 0, int(w * 0.95), int(h * 0.16)], fill=255)
    bd.rectangle([int(w * 0.08), int(h * 0.86), int(w * 0.92), h], fill=255)
    blob = blob.filter(ImageFilter.GaussianBlur(36))
    cream = Image.new("RGBA", (w, h), (*CREAM, 255))
    cream.putalpha(blob)
    return Image.alpha_composite(im, cream).convert("RGB")


def soft_vignette_full_tree(rgb: Image.Image, feather: int = 45) -> Image.Image:
    """Soft edge but protect TOP and RIGHT so star + full tree stay opaque."""
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    inset = max(4, feather // 5)
    draw.rounded_rectangle(
        [inset, inset, w - inset - 1, h - inset - 1],
        radius=int(min(w, h) * 0.03),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    px = mask.load()
    # Protect top 35% and right 55%
    for y in range(h):
        for x in range(w):
            boost = 0
            if y < int(h * 0.35):
                boost = max(boost, int(255 * (0.9 - y / (h * 0.35) * 0.15)))
            if x > int(w * 0.42):
                boost = max(boost, 230)
            if y > int(h * 0.75):  # presents
                boost = max(boost, 220)
            if boost:
                px[x, y] = max(px[x, y], boost)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=4))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def gold_page_margins(page: Image.Image) -> Image.Image:
    page = page.convert("RGBA")
    margin = int(SIZE * 0.08)
    cut = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(cut).rounded_rectangle(
        [margin, margin, SIZE - margin - 1, SIZE - margin - 1], radius=28, fill=255
    )
    cut = cut.filter(ImageFilter.GaussianBlur(radius=36))
    gold_a = Image.eval(cut, lambda p: max(0, min(255, int((255 - p) * 0.38))))
    gold_a = gold_a.filter(ImageFilter.GaussianBlur(radius=12))
    g1 = Image.new("RGBA", (SIZE, SIZE), (218, 180, 115, 255))
    g1.putalpha(gold_a)
    g2 = Image.new("RGBA", (SIZE, SIZE), (235, 200, 145, 255))
    g2.putalpha(gold_a.point(lambda p: int(p * 0.35)).filter(ImageFilter.GaussianBlur(20)))
    return Image.alpha_composite(Image.alpha_composite(page, g1), g2).convert("RGB")


def compose_page(scene: Image.Image) -> Image.Image:
    """Slightly smaller / lower plate than v19 so treetop has cream margin above."""
    page = Image.new("RGBA", (SIZE, SIZE), (*CREAM, 255))
    art_w = int(SIZE * 0.66)  # a touch smaller than v19 70% → more margin around full tree
    scene_r = scene.resize((art_w, art_w), Image.Resampling.LANCZOS)
    scene_rgba = soft_vignette_full_tree(scene_r, feather=42)
    ax = (SIZE - art_w) // 2
    ay = int(SIZE * 0.19)  # room above for title + treetop margin inside plate
    page.alpha_composite(scene_rgba, (ax, ay))
    return gold_page_margins(page)


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(seed, req_id: str) -> None:
    text = f"""# RECIPE — P01-title / v20

| Field | Value |
|-------|--------|
| **name** | Complete tree tip-to-base (star visible) |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v20 |
| **date** | {DAY} |
| **lane** | Qwen 2 Pro Edit (treetop fix on v19) + Pillow page lock |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · full tree tip-to-base · rich colors · ~66% plate |
| **FRAME** | ON — warm gold page margins |
| **source** | `Media/development/P01-title/v19/art-scene.png` |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Fix vs v19

Treetop / star-topper and uppermost branches fully visible with margin above. Presents still complete at base. Nothing cropped top or bottom.

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v19-v20-board.png`
- Script: `scripts/_scratch/_p01_v20_complete_treetop.py`
"""
    out = DEV / "v20"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v20: Image.Image) -> Path:
    v19 = Image.open(V19).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v19 (treetop clipped) vs v20 (complete tip-to-base)",
        fill=(40, 30, 28),
        font=board_font(20),
    )
    draw.text(
        (margin, 68),
        "Same gold frame · rich tree · window/moon/sleigh · star + uppermost branches fully visible",
        fill=(90, 70, 60),
        font=board_font(13),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v19, "v19 — ALMOST", "Rich complete body · treetop slightly cut off"),
            (v20, "v20 — FULL TREE", "Star/topper + tip-to-base · margin above tip"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(18))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v19-v20-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    out_dir = DEV / "v20"
    out_dir.mkdir(parents=True, exist_ok=True)

    src = V19_SCENE if V19_SCENE.is_file() else DEV / "v19" / "art-scene-raw.png"
    print("refs upload", src.name)
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    scene_url = prepare_upload(src, "v19-scene.png", key)

    print("submit v20")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, scene_url],
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

    raw = download(url, out_dir / "art-scene-raw.png")
    scene = scrub_scene_text(raw)
    scene.save(out_dir / "art-scene.png", "PNG")
    art = compose_page(scene)
    art.save(out_dir / "art.png", "PNG")
    art.save(out_dir / "page.png", "PNG")

    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source": str(src.relative_to(ROOT)).replace("\\", "/"),
        "fix": "complete treetop / star with margin above",
        "prompt": PROMPT,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id)
    board = build_board(art)
    print(f"saved {out_dir / 'art.png'} {art.size} seed {seed}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
