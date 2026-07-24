#!/usr/bin/env python3
"""S9 Search v03 — chair+note right near fireplace; p20 wide / p21 close-up."""
from __future__ import annotations

import io
import json
import os
import sys
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S09-search"
V03 = UNIT / "v03"
P20 = V03 / "p20"
P21 = V03 / "p21"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
S8 = ROOT / "Media/development/S08-gone/art.png"
S8R = ROOT / "Media/development/S08-gone/art-right.png"
V02_P20 = UNIT / "v02" / "p20" / "art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT_P20 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07 (image 2).
IMAGE 1 = S8 room continuity (burgundy walls, patterned rug, gifts, snowy window language).
IMAGE 3 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream edges.

COMPOSITION — p20 WIDE ROOM SEARCH (boy NOT visible — empty POV scanning):
WIDE shot of the WHOLE living room.

LAYOUT (critical — do not flip):
- LEFT side of image: Christmas tree with warm lights + wrapped gifts on the rug
- CENTER: open space / patterned rug; dark hallway through an open interior doorway visible
- RIGHT side of image: fireplace with DYING EMBERS and soft wispy smoke (NO roaring fire)
- RIGHT side near the fireplace: an OLD WOODEN CHAIR clearly visible — same place the close-up will show
- On the chair SEAT: a FOLDED CREAM/WHITE NOTE must be VISIBLE even from across the room — the white \
paper catches the eye ("something on the chair" moment). Small wooden side table beside the chair \
(cocoa cup OK, readable at distance or not).

Burgundy walls. Soft golden ambient light. Quiet search. NO boy. NO Santa. NO text/letters on page \
(note is blank white paper only).
"""

PROMPT_P21 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching image 1.

IMAGE 1 = SAME ROOM LOCK from p20 wide plate — match the RIGHT-side chair position near the \
fireplace, the SAME folded cream note on the seat, the SAME side table, dying-embers fireplace, \
burgundy walls, patterned rug, gift wrapping colors. This is a CLOSER camera on that exact chair \
zone — not a different room, not a relocated chair.

IMAGE 2 = optional quality/detail guide. IMAGE 3 = STANDARD FRAME vignette to cream edges.

COMPOSITION — p21 CLOSE-UP DISCOVERY:
Camera moves in CLOSE. The wooden chair FILLS most of the frame — straight-on or slightly angled. \
THE folded cream note on the seat is the hero (blank paper, no readable writing). Small wooden side \
table beside the chair with ceramic cocoa cup and a tiny steam wisp.

Behind the chair: part of the fireplace with dying embers + soft wispy smoke.
Christmas tree only PARTIALLY visible at the very edge — hint of lights/branches only.
A few gifts on the rug in the foreground.
In the background: window with snow falling + moonlight (S8 window language).

Same chair position as image 1 (right side of room near fireplace). NO boy. NO Santa. NO text.
"""

NEG = (
    "text, letters, typography, watermark, readable writing on note, poem, "
    "boy, child, person, Santa, roaring fire, bright flames, magical swirl, "
    "chair on left side, tree on right only, empty chair with no note, "
    "wide full-room shot on close-up page, cream walls, hard border"
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


def write_meta(out_dir: Path, page_id: str, label: str, seed, url: str, intent: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / {page_id} / v03

| Field | Value |
|-------|--------|
| **name** | S9 Search — {label} |
| **unit** | S09-search |
| **book page** | Flow v2 {page_id} SPLIT |
| **version** | v03 |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |

## Intent

{intent}
""",
        encoding="utf-8",
    )
    (out_dir / "meta.json").write_text(
        json.dumps(
            {
                "page": page_id,
                "version": "v03",
                "status": "working",
                "layout": "split_single",
                "size": list(TARGET),
                "seed": seed,
                "fal_url": url,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def gen(out_dir: Path, page_id: str, prompt: str, refs: list[Path], label: str, intent: str) -> Image.Image:
    urls = [fal_client.upload_file(str(p)) for p in refs]
    print(f"=== Qwen {page_id}: {label} ===")
    print("refs:", [p.name for p in refs])
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
    final = upscale(raw, UNIT / f"_tmp-{page_id}-v03-qwen.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    final.save(out_dir / "art.png", optimize=True)
    write_meta(out_dir, page_id, label, seed, url, intent)
    return final


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board  # type: ignore

    for p in (S8, S3, FRAME):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # p20: S8 room + S3 quality + frame (layout enforced in prompt)
    p20 = gen(
        P20,
        "p20",
        PROMPT_P20,
        [S8, S3, FRAME],
        "wide: tree L · fireplace+chair+note R",
        "Wide whole-room search; chair+white note on RIGHT near dying fireplace; tree LEFT.",
    )

    # p21: lock to p20 + S8 window/tree edge hint + frame
    # Prefer p20 + frame + S8R (window/tree) for close crop language
    refs_p21 = [P20 / "art.png", FRAME, S8R if S8R.is_file() else S8]
    p21 = gen(
        P21,
        "p21",
        PROMPT_P21,
        refs_p21,
        "close-up: chair fills frame · note hero · tree edge only",
        "Close camera on same right-side chair/note/table; fireplace behind; tree partial edge; snow window.",
    )

    (V03 / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / v03 (SPLIT)

| Page | Path | Role |
|------|------|------|
| **p20** | `v03/p20/art.png` | Wide · tree L · chair+note R near fireplace |
| **p21** | `v03/p21/art.png` | Close-up chair fills frame · same position |

**{DAY}** · 2625² · Qwen v06 · p21 locked to p20 · mirrors unchanged until promote
""",
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / f"S09-search-v03-split-{DAY}.png"
    split_board(
        p20,
        p21,
        out,
        unit="S09-search",
        version="v03",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 SPLIT · chair R + note · close-up p21",
        subtitle="p20 wide (note visible) · p21 chair fills frame · same position",
        side=700,
    )
    print("BOARD", out)


if __name__ == "__main__":
    main()
