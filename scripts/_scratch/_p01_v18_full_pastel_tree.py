#!/usr/bin/env python3
"""P01 v18 — v16 page lock + complete pastel Christmas tree (full, not cropped/faded)."""
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
V16 = DEV / "v16" / "art.png"
V11 = DEV / "v11" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

PROMPT_SCENE = (
    "Create a SINGLE square children's-book TITLE PAGE scene — ART ONLY, no text. "
    "Image 1 = soft watercolor/gouache paint STYLE (luminous, light, gentle). "
    "Image 2 = composition DNA to keep: winter WINDOW with cream curtains, full moon, "
    "falling snow, faint tiny Santa sleigh+reindeer silhouette on the moon, holly on sill, "
    "cream/ivory interior, soft FRAME ON into cream. "
    "PRIORITY CHANGE — the Christmas TREE on the RIGHT must be a COMPLETE traditional "
    "Christmas tree, FULLY VISIBLE inside the painted plate: full cone silhouette from tip to "
    "base, warm golden string lights, a few soft ornaments, wrapped presents clearly visible "
    "underneath. NOT cropped, NOT cut off at the edge, NOT fading/dissolving into the background, "
    "NOT a partial peek. If needed, shift the composition slightly WIDER so window + FULL tree "
    "both fit comfortably (window left-of-center, complete tree right). "
    "STYLE for the tree: soft watercolor/gouache, LIGHTER tones — pastel greens, warm golden lights, "
    "muted ornament colors. NOT dark, NOT heavily saturated, NOT muddy. Translucent gentle luminous "
    "watercolor that belongs in the same soft world as the window. "
    "Open soft cream around the vignette for title above / copyright below later. "
    "No people, no faces, no baked text."
)
NEGATIVE = (
    "cropped tree, cut-off tree, partial tree, tree peek only, faded tree, dissolving tree, "
    "transparent ghost tree, dark saturated tree, muddy green, heavy opaque tree, "
    "neon ornaments, photorealistic, people, faces, hands, child, text, letters, "
    "blue wash behind art, hard black border"
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


def soft_vignette_keep_tree(rgb: Image.Image, feather: int = 70) -> Image.Image:
    """Gentle soft edge overall; protect right side so full tree stays visible."""
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    inset = max(6, feather // 4)
    draw.rounded_rectangle(
        [inset, inset, w - inset - 1, h - inset - 1],
        radius=int(min(w, h) * 0.04),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    # Keep right 45% near-full opacity (complete tree + presents)
    px = mask.load()
    x0 = int(w * 0.50)
    for y in range(h):
        for x in range(x0, w - inset):
            t = (x - x0) / max(1, w - inset - x0)
            px[x, y] = max(px[x, y], int(255 * (0.75 + 0.25 * min(1.0, t))))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=6))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def gold_page_margins(page: Image.Image) -> Image.Image:
    page = page.convert("RGBA")
    margin = int(SIZE * 0.08)
    cut = Image.new("L", (SIZE, SIZE), 0)
    cd = ImageDraw.Draw(cut)
    cd.rounded_rectangle(
        [margin, margin, SIZE - margin - 1, SIZE - margin - 1],
        radius=28,
        fill=255,
    )
    cut = cut.filter(ImageFilter.GaussianBlur(radius=36))
    gold_a = Image.eval(cut, lambda p: max(0, min(255, int((255 - p) * 0.38))))
    gold_a = gold_a.filter(ImageFilter.GaussianBlur(radius=12))
    g1 = Image.new("RGBA", (SIZE, SIZE), (218, 180, 115, 255))
    g1.putalpha(gold_a)
    g2 = Image.new("RGBA", (SIZE, SIZE), (235, 200, 145, 255))
    g2.putalpha(gold_a.point(lambda p: int(p * 0.35)).filter(ImageFilter.GaussianBlur(20)))
    page = Image.alpha_composite(page, g1)
    page = Image.alpha_composite(page, g2)
    return page.convert("RGB")


def compose_page(scene: Image.Image) -> Image.Image:
    """v16 page geometry, slightly wider plate so full tree fits."""
    page = Image.new("RGBA", (SIZE, SIZE), (*CREAM, 255))
    art_w = int(SIZE * 0.64)  # wider than v16's ~56% to fit complete tree
    scene_r = scene.resize((art_w, art_w), Image.Resampling.LANCZOS)
    scene_rgba = soft_vignette_keep_tree(scene_r, feather=65)
    ax = (SIZE - art_w) // 2
    ay = int(SIZE * 0.20)
    page.alpha_composite(scene_rgba, (ax, ay))
    return gold_page_margins(page)


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(seed, req_id: str) -> None:
    text = f"""# RECIPE — P01-title / v18

| Field | Value |
|-------|--------|
| **name** | Winter Window — complete pastel Christmas tree |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v18 |
| **date** | {DAY} |
| **lane** | Qwen 2 Pro Edit scene + Pillow page lock (v16 geometry, wider plate) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · full tree priority · pastel/light watercolor · ~64% plate width |
| **FRAME** | ON — warm gold page margins (same as v16) |
| **source** | `Media/development/P01-title/v11/art.png` (DNA) · page lock from v16 |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE — open cream above/below for InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Change vs v16

Complete traditional Christmas tree fully visible (not cropped/faded). Pastel greens, warm golden lights, muted ornaments — soft luminous watercolor matching the window. Composition may shift slightly wider to fit.

## Prompt

{PROMPT_SCENE}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v16-v18-board.png`
- Script: `scripts/_scratch/_p01_v18_full_pastel_tree.py`
"""
    out = DEV / "v18"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v18: Image.Image) -> Path:
    v16 = Image.open(V16).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v16 (tree cropped/fades) vs v18 (complete pastel tree)",
        fill=(40, 30, 28),
        font=board_font(20),
    )
    draw.text(
        (margin, 68),
        "Same gold page frame · cream center · window/moon/sleigh · full light watercolor tree",
        fill=(90, 70, 60),
        font=board_font(14),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v16, "v16 — KEEP", "Tree soft / incomplete on the right"),
            (v18, "v18 — FULL PASTEL TREE", "Complete tree · lights · ornaments · presents"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(18))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v16-v18-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    out_dir = DEV / "v18"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    # Use v11 for scene DNA (clean window+tree); style for pastel softness
    scene_url = prepare_upload(V11, "v11-window-tree-dna.png", key)

    print("submit v18 scene")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT_SCENE,
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

    scene = download(url, out_dir / "art-scene.png")
    art = compose_page(scene)
    art.save(out_dir / "art.png", "PNG")
    art.save(out_dir / "page.png", "PNG")

    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source_dna": "v11/art.png",
        "page_lock": "v16 gold margins + cream + wider ~64% plate",
        "prompt": PROMPT_SCENE,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id)
    board = build_board(art)
    print(f"saved {out_dir / 'art.png'} {art.size} seed {seed}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
