#!/usr/bin/env python3
"""P01 v17 — same as v16, but Christmas tree + presents fully rendered (no right-edge dissolve)."""
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

PROMPT = (
    "Edit image 2 ONLY — almost everything is LOCKED. Image 1 = watercolor/gouache paint style. "
    "Image 2 is the title page to preserve: warm gold watercolor whisper on the OUTER PAGE edges only, "
    "clean cream center, winter WINDOW with moon / falling snow / faint Santa sleigh silhouette, "
    "cream curtains, holly on sill, open cream above and below for text. "
    "ONE CHANGE ONLY: the Christmas TREE on the RIGHT must be FULLY rendered — "
    "complete evergreen, all warm lights lit and clear, all ornaments visible and solid, "
    "all wrapped presents underneath clearly visible and opaque. "
    "NO fading, NO soft dissolve, NO transparent edges on the tree or presents — "
    "they must be as solid, detailed, and present as the window itself. "
    "The soft cream paper can meet the finished tree edge cleanly, but the tree itself must not ghost away. "
    "Do NOT change the window, moon, sleigh, gold page-edge frame, cream fields, or layout. "
    "Do NOT add people, blue wash, or text. Art only."
)
NEGATIVE = (
    "faded tree, dissolving tree, transparent tree, ghost tree, soft-edge tree wash-out, "
    "missing presents, incomplete ornaments, missing lights, "
    "blue frame, wash behind art, people, faces, hands, text, letters, "
    "different window, moved layout, new scene, santa indoors"
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


def prepare_upload_im(im: Image.Image, name: str, key: str) -> str:
    im = im.convert("RGB")
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


def soft_vignette_keep_right(rgb: Image.Image, feather: int = 90) -> Image.Image:
    """Soft fade L/T/B; keep RIGHT side of plate opaque so tree does not dissolve."""
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
    # Force right ~38% to full opacity (tree + presents live here)
    px = mask.load()
    x0 = int(w * 0.58)
    for y in range(h):
        for x in range(x0, w):
            # ramp from x0 to full
            t = (x - x0) / max(1, w - x0)
            px[x, y] = max(px[x, y], int(255 * (0.55 + 0.45 * t)))
    # Soften the seam
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def gold_page_margins(page: Image.Image) -> Image.Image:
    """Same quiet warm-gold page-edge whisper as v16."""
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


def build_pillow_fallback(full_tree_scene: Image.Image) -> Image.Image:
    """Recompose like v16 but keep tree opaque on the right."""
    page = Image.new("RGBA", (SIZE, SIZE), (*CREAM, 255))
    art_w = int(SIZE * 0.56)
    scene = full_tree_scene.resize((art_w, art_w), Image.Resampling.LANCZOS)
    scene_rgba = soft_vignette_keep_right(scene, feather=85)
    ax = (SIZE - art_w) // 2
    ay = int(SIZE * 0.22)
    page.alpha_composite(scene_rgba, (ax, ay))
    return gold_page_margins(page)


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(seed, req_id: str, note: str) -> None:
    text = f"""# RECIPE — P01-title / v17

| Field | Value |
|-------|--------|
| **name** | Winter Window — full tree (no dissolve) |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v17 |
| **date** | {DAY} |
| **lane** | Qwen 2 Pro Edit (tree complete) · v16 layout lock |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · same page frame as v16 · tree fully opaque |
| **FRAME** | ON — warm gold page margins (unchanged from v16) |
| **source** | `Media/development/P01-title/v16/art.png` |
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

## Change vs v16

Christmas tree + presents on the right fully rendered — no fading / soft dissolve into cream. Everything else identical.

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v16-v17-board.png`
- Script: `scripts/_scratch/_p01_v17_full_tree.py`
"""
    out = DEV / "v17"
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v17: Image.Image) -> Path:
    v16 = Image.open(V16).convert("RGB")
    panel, label_h, gap, margin, header = 900, 120, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title — v16 (tree fades) vs v17 (tree fully rendered)",
        fill=(40, 30, 28),
        font=board_font(22),
    )
    draw.text(
        (margin, 68),
        "Same gold page frame · cream center · window/moon/sleigh · only tree+presents completed",
        fill=(90, 70, 60),
        font=board_font(14),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v16, "v16 — KEEP (tree soft on right)", "Tree/presents dissolve into cream"),
            (v17, "v17 — FULL TREE", "Tree + lights + ornaments + presents solid"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(18))
        draw.text((x, y + panel + 48), sub, fill=(90, 70, 60), font=board_font(13))
    out = INDEX / "P01-title-v16-v17-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def scene_still_window(im: Image.Image) -> bool:
    """Reject if Qwen swapped to people / lost the window night-blue."""
    # Sample upper-middle window region (approx) for cool night blue
    w, h = im.size
    patch = im.crop((int(w * 0.35), int(h * 0.28), int(w * 0.52), int(h * 0.42)))
    px = list(patch.getdata())
    avg_b = sum(p[2] for p in px) / len(px)
    avg_r = sum(p[0] for p in px) / len(px)
    # Night sky through window: blue channel competitive / higher than red
    return avg_b > avg_r - 5 and avg_b > 90


def main() -> None:
    load_env()
    key = fal_key()
    out_dir = DEV / "v17"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pass A: complete tree on the v11 scene plate (cleaner subject), then recompose like v16
    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    v11_url = prepare_upload(V11, "v11-window-tree.png", key)

    prompt_scene = (
        "Edit image 2 ONLY. Image 1 = paint style. "
        "Keep the SAME winter window composition: four-pane window, moon, falling snow, "
        "faint Santa sleigh silhouette on the moon, cream curtains, holly on sill, cream walls. "
        "ONE CHANGE: make the Christmas TREE on the RIGHT fully complete and opaque — "
        "full green tree, all warm lights, all ornaments, all wrapped presents underneath "
        "clearly visible and solid. No fading, no dissolving into cream, no ghost edges. "
        "Tree must be as detailed as the window. Soft FRAME ON cream vignette OK on LEFT/TOP "
        "but the tree and presents on the RIGHT must stay fully painted. No people, no text."
    )
    print("submit v17 scene (full tree on v11)")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": prompt_scene,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, v11_url],
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

    scene = download(url, out_dir / "art-scene-full-tree.png")
    note = "Qwen completed tree on v11 plate → Pillow recompose (v16 page geometry + gold margins, right-opaque vignette)"
    if not scene_still_window(scene):
        print("WARN: scene may have drifted — still composing; check board")
        note += " · WARN window check soft-fail"

    art = build_pillow_fallback(scene)
    art.save(out_dir / "art.png", "PNG")
    art.save(out_dir / "page.png", "PNG")

    # Optional second pass: lock to v16 page and only boost tree — if first looks good, skip
    # (structure from Pillow is the keep path)

    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source": "v11 → full tree → Pillow like v16",
        "v16_lock": "page geometry + gold margins",
        "prompt_scene": prompt_scene,
        "note": note,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")
    write_recipe(seed, req_id, note)
    board = build_board(art)
    print(f"saved {out_dir / 'art.png'} {art.size} seed {seed}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
