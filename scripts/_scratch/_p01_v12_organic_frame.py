#!/usr/bin/env python3
"""P01 v12 — winter window with organic watercolor frame (edge DNA from p08 + p28)."""
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
SRC = DEV / "v11" / "art.png"
REF_DOOR = ROOT / "Images/styles3/p08-beat02-the-door.png"
REF_HEARTH = ROOT / "Images/styles3/p28-family-hearth.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048
CREAM = (245, 240, 230)

PROMPT = (
    "Create a SINGLE square children's-book TITLE PAGE painting — ART ONLY, no text. "
    "Image 1 = watercolor/gouache paint STYLE lock (warm soft brush, paper grain). "
    "Image 2 = the SUBJECT to keep: winter window scene — four-pane window, full moon with "
    "faint tiny Santa sleigh+reindeer silhouette crossing the moon, falling snow, cream curtains "
    "tied back, Christmas tree edge with warm lights, optional holly on sill / presents, "
    "cream/ivory interior. Preserve this window composition as the clear focal point, "
    "centered about 60–70% of the page width in the UPPER-MIDDLE of the page. "
    "Image 3 = EDGE / VIGNETTE DNA ONLY (do not copy people, doors, fireplaces, room layouts, "
    "or any decorative objects from it): study ONLY how paint softens at the margins — "
    "organic irregular watercolor bleeds, wet soft edges dissolving into the paper, "
    "a subtle off-white/warm ivory luminous wash near the art (inner glow), then outward dissolve "
    "into soft peachy-gold / warm cream luminous warmth — NOT stark pure white. "
    "APPLY that painted-edge treatment to image 2: rich detailed window at center; around it a subtle "
    "off-white/warm ivory inner glow wash; then soft watercolor continuing outward dissolving into "
    "luminous warm cream-gold; at the very page edges the softest suggestion of painted color — "
    "hint of warm cream-gold, maybe a whisper of distant burgundy wash, watercolor paper texture. "
    "CRITICAL: soft EDGE means watercolor paint bleed / dissolve — NOT bird feathers, NOT plumes, "
    "NOT quills, NOT feather decorations, NOT oval feather wreath, NOT any feather motif. "
    "The WHOLE PAGE is one cohesive painting that breathes. Organic hand-painted soft edge — "
    "NO hard border, NO geometric frame, NO rectangle cutout, NO sticker vignette, NO feathers. "
    "Open soft luminous areas above and below the window for live title/copyright later. "
    "No people, no faces, no hands, no baked text."
)
NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, logo, signature, "
    "feathers, feather, plume, quill, feather wreath, feather frame, bird feathers, "
    "hard border, black frame, geometric rectangle frame, sticker cutout, hard vignette mask, "
    "stark pure white empty page, photorealistic, child, boy, person, door scene copy, "
    "full fireplace room copy, busy crowded scene, clip art"
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


def build_edge_dna() -> Path:
    """Side-by-side of both edge refs for Qwen slot 3 (max 3 image_urls)."""
    a = Image.open(REF_DOOR).convert("RGB")
    b = Image.open(REF_HEARTH).convert("RGB")
    h = 1024
    a.thumbnail((1024, h), Image.Resampling.LANCZOS)
    b.thumbnail((1024, h), Image.Resampling.LANCZOS)
    gap = 16
    board = Image.new("RGB", (a.width + b.width + gap + 32, max(a.height, b.height) + 80), CREAM)
    board.paste(a, (16, 48))
    board.paste(b, (16 + a.width + gap, 48))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.text((16, 12), "EDGE DNA ONLY — soft watercolor bleed / luminous dissolve (ignore subjects)", fill=(60, 50, 45), font=font)
    out = DEV / "_tmp_edge_dna_p08_p28.png"
    DEV.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


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


def write_recipe(seed, req_id: str) -> None:
    text = f"""# RECIPE — P01-title / v12

| Field | Value |
|-------|--------|
| **name** | Winter Window — organic watercolor frame |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v12 |
| **date** | {DAY} |
| **lane** | A2 Qwen 2 Pro Edit |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · cream page · organic feathered frame |
| **FRAME** | ON — painted edge DNA (not Pillow mask) |
| **source** | `Media/development/P01-title/v11/art.png` |
| **edge refs** | `Images/styles3/p08-beat02-the-door.png` · `Images/styles3/p28-family-hearth.png` |
| **style** | `Media/approved/style-refs/style-lock-v2.png` |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png (art-only plate for InDesign) |
| **type** | NONE — live Cormorant in InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Compare: v11 (Pillow cream vignette) vs v12 (painted breathing frame)
- Board: `Media/generated/mocks/_INDEX/P01-title-v11-v12-board.png`
- Script: `scripts/_scratch/_p01_v12_organic_frame.py`
"""
    out = DEV / "v12"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v12: Image.Image) -> Path:
    v11_page = Image.open(DEV / "v11" / "page.png").convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text((margin, 28), "P01 Title — v11 (no frame) vs v12 (organic watercolor frame)", fill=(40, 30, 28), font=board_font(26))
    draw.text(
        (margin, 68),
        "Same winter window + sleigh · edge DNA from p08 door + p28 hearth · Qwen 2 Pro Edit · art only",
        fill=(90, 70, 60),
        font=board_font(14),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v11_page, "v11 — ART ONLY (current)", "Pillow soft vignette on cream · no painted frame"),
            (v12, "v12 — ORGANIC FRAME", "Hand-painted feather + luminous dissolve · whole page breathes"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(20))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v11-v12-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    edge = build_edge_dna()
    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    src_url = prepare_upload(SRC, "v11-winter-window.png", key)
    edge_url = prepare_upload(edge, "edge-dna-p08-p28.png", key)

    print("submit v12")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, src_url, edge_url],
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

    out_dir = DEV / "v12"
    out_dir.mkdir(parents=True, exist_ok=True)
    art = download(url, out_dir / "art.png")
    # Full-page plate for InDesign — same as art when Qwen already painted the cream field
    art.save(out_dir / "page.png", "PNG")
    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source": "v11/art.png",
        "edge_refs": ["p08-beat02-the-door.png", "p28-family-hearth.png"],
        "prompt": PROMPT,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id)
    board = build_board(art)
    print(f"saved {out_dir / 'art.png'} {art.size} seed {seed}")
    print(f"BOARD {board}")
    try:
        edge.unlink(missing_ok=True)
    except OSError:
        pass


if __name__ == "__main__":
    main()
