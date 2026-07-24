#!/usr/bin/env python3
"""S6 Cocoa full-res regen: L v03 + R v02 at exact 2625×2625.

Pipeline: Banana Pro /edit @ 2K (composition lock) → Lanczos to 2625².
(Qwen caps ~2048² and prior dials landed at 512² — no more low-res development.)
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S06-cocoa"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
PAGE = 2625
DAY = "2026-07-22"
BANANA = "fal-ai/nano-banana-pro/edit"

# Existing CDN composition locks (same scenes)
L_COMP = "https://v3b.fal.media/files/b/0aa35e4b/KCHzcmPFdXWDTGnjzMcRL_AS6XjqN7.png"
R_COMP = "https://v3b.fal.media/files/b/0aa35dfa/xlfRd02Tj--ibj7I6dEjb_rz6lRbr0.png"

NEG = (
    "text, letters, typography, watermark, signature, logo, UI, frame border, "
    "photo, photoreal, 3d render, plastic, harsh contrast, muddy colors"
)

L_PROMPT = """\
Children's picture-book TEXT PAGE illustration, square 1:1, ART ONLY — no text, no letters.

PRESERVE the exact composition of image 1 (layout lock): faint distant snowy village \
atmosphere as a soft whisper (about 15–25% presence), soft dissolve-to-cream vignette \
edges matching image 3 frame treatment, generous open cream center for poem type.

Image 2 = village snow atmosphere reference (mood/palette only — do not copy as a full scene).
Image 3 = standard soft vignette dissolve → cream edges (frame treatment).

Painted gouache / soft watercolor. Quiet dreamy night village glow. Warm cream paper. \
Same quality bar as a premium gift picture book — clear soft edges, no muddy blur.
Output a clean high-resolution square plate ready for print.
"""

R_PROMPT = """\
Children's picture-book IMAGE PAGE illustration, square 1:1, ART ONLY — no text, no letters.

PRESERVE the exact composition of image 1 (layout lock): Santa holding a steaming cocoa mug \
with marshmallows as the prop hero — firelight and Christmas-tree glow, warm living-room mood.

Image 2 = Santa character lock (open coat, cream striped shirt, brown suspenders over shirt, \
kind face — match wardrobe and likeness).
Image 3 = painted gouache / soft watercolor quality + palette bar (warm firelight, rich but soft).

Keep the same frame treatment: soft dissolve vignette to cream edges. Same gift-book quality. \
Fewer gifts than a gift-sea plate. Cocoa mug readable with steam + marshmallows.
Output a clean high-resolution square plate ready for print.
"""


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


def key() -> str:
    k = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    if not k:
        raise SystemExit("FAL_KEY / FAL_API_KEY missing in .env.local")
    return k


def upload(path: Path) -> str:
    """fal storage initiate + PUT → file_url."""
    data = path.read_bytes()
    init_req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps(
            {"file_name": path.name, "content_type": "image/png"}
        ).encode(),
        headers={
            "Authorization": f"Key {key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(init_req, timeout=60) as resp:
        init = json.loads(resp.read().decode())
    put_url = init["upload_url"]
    put_req = urllib.request.Request(
        put_url, data=data, method="PUT", headers={"Content-Type": "image/png"}
    )
    with urllib.request.urlopen(put_req, timeout=180) as resp:
        resp.read()
    url = init.get("file_url") or init.get("fileUrl")
    if not url:
        raise SystemExit(f"upload missing file_url: {init}")
    print("uploaded", path.name, "->", url[:80], "...")
    return url


def submit(endpoint: str, payload: dict) -> str:
    req = urllib.request.Request(
        f"https://queue.fal.run/{endpoint}",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Key {key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode())
    rid = body.get("request_id")
    if not rid:
        raise SystemExit(json.dumps(body, indent=2)[:2000])
    return rid


def wait(endpoint: str, rid: str, max_wait: int = 600) -> dict:
    status_url = f"https://queue.fal.run/{endpoint}/requests/{rid}/status"
    t0 = time.time()
    while time.time() - t0 < max_wait:
        req = urllib.request.Request(
            status_url, headers={"Authorization": f"Key {key()}"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            st = json.loads(resp.read().decode())
        status = st.get("status")
        print(f"  {rid[:8]}… {status}")
        if status in ("COMPLETED", "OK", "completed"):
            rurl = st.get("response_url") or (
                f"https://queue.fal.run/{endpoint}/requests/{rid}"
            )
            req2 = urllib.request.Request(
                rurl, headers={"Authorization": f"Key {key()}"}
            )
            with urllib.request.urlopen(req2, timeout=120) as resp:
                return json.loads(resp.read().decode())
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:4000])
        time.sleep(4)
    raise SystemExit(f"timeout {rid}")


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def to_page(im: Image.Image) -> Image.Image:
    if im.size == (PAGE, PAGE):
        return im
    return im.resize((PAGE, PAGE), Image.Resampling.LANCZOS)


def save_side(
    ver: str,
    side: str,
    prompt: str,
    image_urls: list[str],
    seed: int | None = None,
) -> dict:
    out_dir = UNIT / ver
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "prompt": prompt,
        "image_urls": image_urls,
        "num_images": 1,
        "output_format": "png",
        "resolution": "2K",
        "aspect_ratio": "1:1",
        "limit_generations": True,
        "safety_tolerance": "4",
    }
    if seed is not None:
        payload["seed"] = seed
    print(f"\n=== {ver} {side} Banana Pro /edit @ 2K ===")
    rid = submit(BANANA, payload)
    print("request_id", rid)
    result = wait(BANANA, rid)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    raw = download(url)
    print("raw size", raw.size)
    page = to_page(raw)
    stem = f"art-{side}" if side in ("left", "right") else "art"
    raw_path = out_dir / f"{stem}-banana-2k.png"
    page_path = out_dir / f"{stem}.png"
    raw.save(raw_path)
    page.save(page_path, optimize=True)
    print("saved", page_path, page.size)
    meta = {
        "version": ver,
        "side": side,
        "model": BANANA,
        "resolution_setting": "2K",
        "raw_size": list(raw.size),
        "page_size": list(page.size),
        "request_id": rid,
        "fal_url": url,
        "seed": result.get("seed"),
        "image_urls": image_urls,
        "upscale": f"Lanczos → {PAGE}×{PAGE}",
    }
    (out_dir / f"meta-{side}.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    return meta


def write_recipe_l(meta: dict) -> None:
    text = f"""# RECIPE — S06-cocoa / v03 LEFT

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa L — faint village whisper (print res) |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p14 TEXT |
| **version** | v03 (LEFT) |
| **date** | {DAY} |
| **model** | `{BANANA}` @ 2K → Lanczos **2625×2625** |
| **composition lock** | v02 L (village whisper + cream vignette) |
| **refs** | E-back-village-snow · frame-reference |
| **seed** | {meta.get("seed")} |
| **request_id** | `{meta.get("request_id")}` |
| **fal_url** | `{meta.get("fal_url")}` |
| **raw → page** | {meta.get("raw_size")} → 2625² |
| **status** | working — full-res print plate |
| **paired_right** | v02 art-right |

## Intent

Same composition as v02 L: distant snowy village whisper + soft dissolve-to-cream vignette; open center for poem. Resolution lock: no low-res dials.
"""
    (UNIT / "v03" / "RECIPE.md").write_text(text, encoding="utf-8")


def write_recipe_r(meta: dict) -> None:
    text = f"""# RECIPE — S06-cocoa / v02 RIGHT

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa R — cocoa prop hero (print res) |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p15 IMAGE |
| **version** | v02 (RIGHT) |
| **date** | {DAY} |
| **model** | `{BANANA}` @ 2K → Lanczos **2625×2625** |
| **composition lock** | v01 R KEEP (cocoa mug hero) |
| **refs** | santa-G0-v2 · style-lock-v2 |
| **seed** | {meta.get("seed")} |
| **request_id** | `{meta.get("request_id")}` |
| **fal_url** | `{meta.get("fal_url")}` |
| **raw → page** | {meta.get("raw_size")} → 2625² |
| **status** | working — full-res print plate |
| **paired_left** | v03 art-left |

## Intent

Same composition as v01 R: Santa holding steaming cocoa with marshmallows; firelight + tree glow; open-coat wardrobe; standard frame treatment. Resolution lock: no low-res dials.
"""
    (UNIT / "v02" / "RECIPE-right.md").write_text(text, encoding="utf-8")


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board  # type: ignore

    village = upload(ROOT / "Images/styles3/E-back-village-snow.png")
    frame = upload(ROOT / "Media/approved/style-refs/frame-reference.png")
    santa = upload(ROOT / "Media/approved/characters/santa-G0-v2.png")
    style = upload(ROOT / "Media/approved/style-refs/style-lock-v2.png")

    # L v03
    meta_l = save_side(
        "v03",
        "left",
        L_PROMPT,
        [L_COMP, village, frame],
        seed=2038430340,
    )
    write_recipe_l(meta_l)

    # R v02 (reuse v02 folder for right plate alongside any L leftovers)
    (UNIT / "v02").mkdir(parents=True, exist_ok=True)
    meta_r = save_side(
        "v02",
        "right",
        R_PROMPT,
        [R_COMP, santa, style],
        seed=916278999,
    )
    write_recipe_r(meta_r)

    left = Image.open(UNIT / "v03" / "art-left.png")
    right = Image.open(UNIT / "v02" / "art-right.png")
    INDEX.mkdir(parents=True, exist_ok=True)
    board_path = INDEX / f"S06-cocoa-L-v03-R-v02-fullres-{DAY}.png"
    tech = (
        "Banana Pro /edit · 2K→2625² · S3 v07 quality bar · resolution lock"
    )
    text_image_board(
        left,
        right,
        board_path,
        unit="S06-cocoa",
        version="L v03 + R v02 FULL RES",
        day=DAY,
        tech=tech,
        subtitle="LEFT p14 village whisper · RIGHT p15 cocoa hero · 2625²",
    )
    print("\nBOARD", board_path)

    # promote current-best pointers
    for name, src in (
        ("art-left.png", UNIT / "v03" / "art-left.png"),
        ("art-right.png", UNIT / "v02" / "art-right.png"),
    ):
        dest = UNIT / name
        Image.open(src).save(dest)
        print("promoted", dest)

    summary = {
        "left": meta_l,
        "right": meta_r,
        "board": str(board_path.relative_to(ROOT)),
        "page_px": PAGE,
    }
    (UNIT / "v03" / "meta-pair.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
