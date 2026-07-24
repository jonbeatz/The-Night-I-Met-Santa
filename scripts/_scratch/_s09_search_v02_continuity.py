#!/usr/bin/env python3
"""S9 Search v02 — room continuity: wide search (chair visible) + close discovery."""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S09-search"
V02 = UNIT / "v02"
P20 = V02 / "p20"
P21 = V02 / "p21"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
S8 = ROOT / "Media/development/S08-gone/art.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
V01_P21 = UNIT / "v01" / "p21" / "art.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT_P20 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07 (image 2).

IMAGE 1 = ROOM CONTINUITY from S8 Gone — same burgundy living room, patterned rug, Christmas tree, \
gifts, interior doorway to dark hallway, snowy window language. QUIET search beat — no running energy.

IMAGE 3 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream/ivory at edges.

COMPOSITION — p20 WIDE SEARCH POV (boy NOT visible — first-person / empty POV):
Wide view scanning the full room. Christmas tree with warm lights and wrapped gifts. Dark hallway \
through the open interior doorway (Santa's exit). Burgundy walls, patterned rug, soft golden ambient \
light.

CRITICAL CONTINUITY BEATS:
- Fireplace shows DYING EMBERS with soft wispy smoke ONLY — NO roaring fire, NO bright flames.
- An OLD WOODEN CHAIR must be VISIBLE in frame near the fireplace — partially shown on the right \
side of this image (near the hearth). NOT the focal point — a clue waiting to be found. Viewer's \
eye should notice it. Chair is empty (no note yet on this wide shot, or note tiny/unread if present).
- Same room that the close-up page will show later.

NO Santa figure. NO boy. NO text. NO letters.
"""

PROMPT_P21 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07 (image 2).

IMAGE 1 = SAME ROOM LOCK from p20 wide search — match EXACTLY: burgundy walls, patterned rug, \
fireplace dying-embers state, Christmas tree shape/lights, gift wrapping colors and placement, \
overall palette. This is a CLOSER view of the chair area in THAT same room — not a different room.

IMAGE 3 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream edges.

COMPOSITION — p21 CLOSE DISCOVERY:
Hero: old wooden chair near the fireplace with a small folded cream note/envelope on the seat \
(blank paper — no readable writing) catching the last light. Small wooden side table with ceramic \
cocoa cup half-full and a tiny steam wisp. Fireplace: dying embers + soft wispy smoke (same state \
as image 1). Christmas tree and gifts VISIBLE in the soft background — same tree, same gifts as \
image 1. A window with snow falling outside matching S8's snowy night window. Burgundy walls, \
patterned rug continuity.

NO Santa. NO boy. NO text baked into art.
"""

NEG = (
    "text, letters, typography, watermark, readable writing, poem text, "
    "Santa Claus, boy, child, person, figure, roaring fire, bright flames, "
    "magical motion swirl, running blur, cream walls, hard border, geometric frame"
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


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def upscale(raw: Image.Image, tmp: Path) -> Image.Image:
    raw.save(tmp)
    up_url = fal_client.upload_file(str(tmp))
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": up_url,
            "upscale_mode": "factor",
            "upscale_factor": 2,
            "noise_scale": 0.1,
            "output_format": "png",
        },
        with_logs=True,
    )
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    tmp.unlink(missing_ok=True)
    return up_im.resize(TARGET, Image.Resampling.LANCZOS)


def write_recipe(
    out_dir: Path,
    *,
    page_id: str,
    label: str,
    seed,
    url: str,
    intent: str,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / {page_id} / v02

| Field | Value |
|-------|--------|
| **name** | S9 Search — {label} |
| **unit** | S09-search |
| **book page** | Flow v2 {page_id} SPLIT single |
| **version** | v02 |
| **date** | {DAY} |
| **status** | working — room continuity dial |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **continuity** | p20↔p21 same room · S8 Gone v09 · S3 v07 · frame vignette |

## Intent

{intent}
""",
        encoding="utf-8",
    )
    (out_dir / "meta.json").write_text(
        json.dumps(
            {
                "page": page_id,
                "version": "v02",
                "status": "working",
                "layout": "split_single",
                "size": list(TARGET),
                "seed": seed,
                "fal_url": url,
                "continuity_pair": "v02",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def gen(
    *,
    out_dir: Path,
    page_id: str,
    prompt: str,
    image_paths: list[Path],
    label: str,
    intent: str,
) -> Image.Image:
    urls = [fal_client.upload_file(str(p)) for p in image_paths]
    print(f"=== Qwen {page_id}: {label} ===")
    print("refs:", [p.name for p in image_paths])
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": prompt,
            "negative_prompt": NEG,
            "image_urls": urls,
            "image_size": {"width": 1024, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": True,
        },
        with_logs=True,
    )
    print(result)
    url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(url)
    print("qwen raw", raw.size)
    final = upscale(raw, UNIT / f"_tmp-{page_id}-v02-qwen.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    final.save(out_dir / "art.png", optimize=True)
    write_recipe(out_dir, page_id=page_id, label=label, seed=seed, url=url, intent=intent)
    return final


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board  # type: ignore

    for p in (S8, S3, FRAME):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    p20 = gen(
        out_dir=P20,
        page_id="p20",
        prompt=PROMPT_P20,
        image_paths=[S8, S3, FRAME],
        label="p20 wide search — chair visible near fireplace, dying embers",
        intent="Wide POV search; chair partially visible near hearth; dying fire; tree/gifts/hallway.",
    )

    # p21 locked to fresh p20 for same-room continuity; v01 p21 for chair/note/cocoa language
    p21_refs = [P20 / "art.png", S3, FRAME]
    # Prefer continuity over old p21 — if we have room for chair language, swap FRAME... 
    # Max 3: p20 lock + S3 + FRAME. Chair/note described in prompt; optional replace FRAME with v01 p21
    if V01_P21.is_file():
        p21_refs = [P20 / "art.png", V01_P21, FRAME]
        # Drop S3 to keep chair discovery language + frame; quality via prompt + p20 oil finish
        prompt_p21 = PROMPT_P21.replace(
            "matching S3 v07 (image 2)",
            "matching the oil finish of image 1; image 2 = chair/note/cocoa discovery language from prior dial",
        )
    else:
        prompt_p21 = PROMPT_P21

    p21 = gen(
        out_dir=P21,
        page_id="p21",
        prompt=prompt_p21,
        image_paths=p21_refs,
        label="p21 close discovery — same room as p20, chair/note/cocoa",
        intent="Closer view of p20 chair zone; note + cocoa; same tree/gifts/fire/rug/window.",
    )

    # Do NOT overwrite unit art-left/right until Jon promotes — keep v01 mirrors unless absent
    # Still write v02 unit RECIPE pointer
    (V02 / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / v02 (SPLIT continuity)

| Page | Path | Role |
|------|------|------|
| **p20 L** | `v02/p20/art.png` | Wide search · chair visible · dying embers |
| **p21 R** | `v02/p21/art.png` | Close chair/note · same room as p20 |

**Date:** {DAY} · **2625×2625** · Qwen v06 · Continuity: p21 refs p20 plate  
**Primary mirrors** (`art-left`/`art-right`) stay on prior keep until Jon promotes v02.
""",
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / f"S09-search-v02-split-{DAY}.png"
    split_board(
        p20,
        p21,
        out,
        unit="S09-search",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 SPLIT · room continuity · dying embers",
        subtitle="p20 wide (chair visible) · p21 close (same room) · poem under each",
        side=700,
    )
    # also v01 vs v02 compare optional
    v01_l = UNIT / "v01" / "p20" / "art.png"
    v01_r = UNIT / "v01" / "p21" / "art.png"
    if v01_l.is_file() and v01_r.is_file():
        from PIL import ImageDraw, ImageFont

        def font(sz: int):
            for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
                if Path(p).is_file():
                    return ImageFont.truetype(p, sz)
            return ImageFont.load_default()

        cells = [
            (Image.open(v01_l).convert("RGB"), "v01 p20"),
            (p20, "v02 p20"),
            (Image.open(v01_r).convert("RGB"), "v01 p21"),
            (p21, "v02 p21"),
        ]
        w, h = 480, 480
        margin, gap, header = 24, 14, 64
        sheet = Image.new(
            "RGB",
            (margin * 2 + w * 4 + gap * 3, margin + header + h + 36),
            (252, 248, 240),
        )
        d = ImageDraw.Draw(sheet)
        d.text(
            (margin, 12),
            "S9 Search — v01 vs v02 continuity",
            fill=(35, 28, 22),
            font=font(18),
        )
        d.text(
            (margin, 38),
            "v02: chair visible on p20 · dying fire both · p21 locked to p20 room",
            fill=(100, 90, 75),
            font=font(12),
        )
        y = margin + header
        for i, (im, lab) in enumerate(cells):
            x = margin + i * (w + gap)
            sheet.paste(im.resize((w, h), Image.Resampling.LANCZOS), (x, y))
            d.text((x, y + h + 8), lab, fill=(50, 40, 35), font=font(12))
        cmp = INDEX / f"S09-search-v01-vs-v02-{DAY}.png"
        sheet.save(cmp, "PNG")
        print("COMPARE", cmp)

    print("BOARD", out)
    print("P20", P20 / "art.png")
    print("P21", P21 / "art.png")


if __name__ == "__main__":
    main()
