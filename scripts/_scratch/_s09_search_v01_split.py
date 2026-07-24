#!/usr/bin/env python3
"""S9 Search — SPLIT singles p20 + p21 at 2625×2625. Qwen 2 Pro Edit v06."""
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
V01 = UNIT / "v01"
P20 = V01 / "p20"
P21 = V01 / "p21"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
S8 = ROOT / "Media/development/S08-gone/art.png"
S8L = ROOT / "Media/development/S08-gone/art-left.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT_P20 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07.

IMAGE 1 = ROOM CONTINUITY from S8 Gone (same burgundy living room, patterned rug, Christmas tree, \
gifts, interior doorway to dark hallway) — but QUIET now. The running energy is gone. This is the \
search: recently vacated, still warm, still magical, occupant gone.

IMAGE 2 = QUALITY BAR (S3 Eyes Met v07) — deep saturation, crisp detail, warm painterly finish. \
NOT soft. NOT muted.

IMAGE 3 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream/ivory at the \
edges. Art richest in center; gentle cream fade at borders. No hard border, no geometric frame.

COMPOSITION — LEFT page (p20) SEARCH POV:
Over-the-shoulder / first-person point of view scanning the full room. We see what the boy sees. \
The BOY IS NOT VISIBLE — this is his POV only. NO person, NO child, NO figure in frame.
Christmas tree with warm lights and wrapped gifts on one side. Dark hallway through the open \
interior doorway on the other side — Santa's exit route. Wrapped presents scattered on the \
patterned rug. Deep burgundy walls. Soft golden ambient light. Empty, searching stillness.

NO Santa. NO boy. NO text, letters, or watermark.
"""

PROMPT_P21 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07.

IMAGE 1 = ROOM CONTINUITY from S8 (same burgundy walls, patterned rug, fireplace area) — quiet \
after Santa left. Same house, same night, discovery moment.

IMAGE 2 = QUALITY BAR (S3 Eyes Met v07) — deep saturation, crisp detail, warm painterly finish. \
NOT soft. NOT muted.

IMAGE 3 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream/ivory at edges. \
No hard border.

COMPOSITION — RIGHT page (p21) DISCOVERY:
THE CHAIR is the hero. An old wooden chair positioned near the fireplace. Fireplace has NO active \
fire — only soft wispy smoke rising from dying embers, faint orange glow fading. On the chair \
seat: a small folded cream note / letter catching the last light in the room (blank paper — no \
readable writing). Nearby on a small wooden side table: a ceramic cocoa cup, half-full, tiny wisp \
of steam. Santa was JUST here. Intimate discovery moment. Christmas tree may be partially visible \
in soft background. Deep burgundy walls, patterned rug continuity.

NO Santa figure. NO boy. NO text baked into the art (note is blank paper only). No letters on page.
"""

NEG = (
    "text, letters, typography, watermark, readable writing on note, poem text, "
    "Santa Claus, Santa in room, boy, child, person, figure, running motion blur, "
    "magical swirl trail, roaring fire, bright flames, cream walls, hard border, "
    "geometric frame, phone, six fingers"
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


def park_old_spread() -> None:
    """Park prior spread/halves so SPLIT singles own the unit."""
    archive = UNIT / "_archive-pre-split-v01"
    if archive.exists():
        return
    has = any((UNIT / n).is_file() for n in ("art.png", "art-left.png", "art-right.png"))
    if not has:
        return
    archive.mkdir(parents=True, exist_ok=True)
    for n in ("art.png", "art-left.png", "art-right.png", "meta-p20.json", "meta-p21.json"):
        src = UNIT / n
        if src.is_file():
            shutil.move(str(src), str(archive / n))
            print("parked", n, "→ _archive-pre-split-v01/")


def gen_page(
    *,
    out_dir: Path,
    page_id: str,
    prompt: str,
    room_path: Path,
    label: str,
) -> Image.Image:
    out_dir.mkdir(parents=True, exist_ok=True)
    urls = [
        fal_client.upload_file(str(room_path)),
        fal_client.upload_file(str(S3)),
        fal_client.upload_file(str(FRAME)),
    ]
    print(f"=== Qwen {page_id} {label} ===")
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
    tmp = UNIT / f"_tmp-{page_id}-qwen.png"
    raw.save(tmp)

    print(f"=== SeedVR {page_id} ===")
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
    final = up_im.resize(TARGET, Image.Resampling.LANCZOS)
    tmp.unlink(missing_ok=True)
    final.save(out_dir / "art.png", optimize=True)

    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / {page_id} / v01

| Field | Value |
|-------|--------|
| **name** | S9 Search — {label} |
| **unit** | S09-search |
| **book page** | Flow v2 {page_id} SPLIT single |
| **version** | v01 |
| **date** | {DAY} |
| **status** | working — pending Jon eye |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **room continuity** | S8 Gone v09 LOCK |
| **quality bar** | S03-eyes-met/v07 |
| **frame** | `Media/approved/style-refs/frame-reference.png` (standard vignette) |

## Intent

{label}. Quiet room after Santa left. No boy, no Santa in frame. Poem text in InDesign later.
""",
        encoding="utf-8",
    )
    (out_dir / "meta.json").write_text(
        json.dumps(
            {
                "page": page_id,
                "version": "v01",
                "status": "working",
                "layout": "split_single",
                "size": list(TARGET),
                "seed": seed,
                "fal_url": url,
                "room_continuity": "S08-gone/v09",
                "quality_bar": "S03-eyes-met/v07",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return final


def board(p20: Image.Image, p21: Image.Image) -> None:
    """Must use split_board — poem captions under each side (Jon 2026-07-22 rule)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board  # type: ignore

    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / f"S09-search-v01-split-{DAY}.png"
    split_board(
        p20,
        p21,
        out,
        unit="S09-search",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 SPLIT · S8 room · S3 v07 · frame vignette",
        subtitle="p20 search POV · p21 chair/note · no boy/Santa",
        side=700,
    )
    print("BOARD", out)


def main() -> None:
    load_env()
    for p in (S8, S8L, S3, FRAME):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    park_old_spread()

    p20 = gen_page(
        out_dir=P20,
        page_id="p20",
        prompt=PROMPT_P20,
        room_path=S8,
        label="p20 over-shoulder room search POV",
    )
    p21 = gen_page(
        out_dir=P21,
        page_id="p21",
        prompt=PROMPT_P21,
        room_path=S8L,  # fireplace side continuity
        label="p21 chair/note discovery by dying fireplace",
    )

    # FLOW convenience mirrors at unit root
    shutil.copy2(P20 / "art.png", UNIT / "art-left.png")
    shutil.copy2(P21 / "art.png", UNIT / "art-right.png")
    # Unit-level RECIPE pointer
    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search (SPLIT)

| Page | Path | Role |
|------|------|------|
| **p20 L** | `v01/p20/art.png` (= `art-left.png`) | Search POV — empty room, no boy |
| **p21 R** | `v01/p21/art.png` (= `art-right.png`) | Chair + cream note + dying embers + cocoa |

**Layout:** SPLIT singles (not a seamless spread) · **2625×2625** each · **v01** {DAY}  
**Continuity:** S8 Gone v09 · **Quality:** S3 v07 · **Frame:** standard vignette  
See each page RECIPE for seeds/fal URLs.
""",
        encoding="utf-8",
    )

    board(p20, p21)
    print("DONE p20", P20 / "art.png")
    print("DONE p21", P21 / "art.png")


if __name__ == "__main__":
    main()
