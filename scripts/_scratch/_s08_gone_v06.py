#!/usr/bin/env python3
"""S8 Gone v06 — FINAL: keep v05 room; match v02-left swirl EXACTLY. Lock if match."""
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
UNIT = ROOT / "Media/development/S08-gone"
V02L = UNIT / "v02" / "art-left.png"
V02 = UNIT / "v02" / "art.png"
V05 = UNIT / "v05" / "art.png"
V06 = UNIT / "v06"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625.

IMAGE 1 = SWIRL LOCK (v02 left panel) — THIS IS THE ONLY CHANGE TARGET.
Copy that MAGICAL WISP SWIRL EXACTLY: subtle elegant translucent golden-white streaks, \
delicate magical whisper / visible gust of wind, graceful curve originating near the bottom of \
the open doorway, looping upward behind the boy's back, tapering into thin shimmering motion \
threads. Same intensity, same elegant curve, same scale relative to the boy. NOT a vortex. NOT \
a thick glowing cloud. NOT a massive cyclone. NOT a solid light blob. Match image 1 swirl \
LANGUAGE pixel-for-pixel in spirit.

IMAGE 2 = BASE PLATE (v05 full spread) — KEEP almost everything:
Preserve the room layout, fireplace with glow and stockings, moonlit window with Santa sleigh \
silhouette on the moon, patterned rug with wood showing at edges, boy mid-run with vintage camera, \
holly pajamas, burgundy walls, Christmas tree, interior door to dark hallway. Do not redesign \
the room.

IMAGE 3 = full v02 spread — reinforce the same wispy swirl energy language as image 1 across \
the doorway-to-boy path.

GIFT TWEAK ONLY: reduce presents by about 25% vs image 2 — a few less boxes; keep medium density \
with gifts under the tree AND a few near the fireplace (Santa was working there). Not sparse, \
not warehouse.

Change ONLY the swirl (and slight gift trim). Everything else from image 2 stays. NO text. \
NO Santa inside. NO skylight. Rich oil-painting quality. Faces off the gutter.
"""

NEG = (
    "text, letters, watermark, Santa inside, skylight, massive vortex, giant cyclone, "
    "thick white cloud swirl, heavy storm energy, solid glowing blob trail, tornado swirl, "
    "oversized motion blur filling the room, gift warehouse, wall-to-wall presents"
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


def save_triplet(final: Image.Image, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    final.save(folder / "art.png", optimize=True)
    final.crop((0, 0, PAGE, PAGE)).save(folder / "art-left.png", optimize=True)
    final.crop((PAGE, 0, TARGET[0], TARGET[1])).save(folder / "art-right.png", optimize=True)


def promote_to_primary(src_folder: Path) -> None:
    """Copy lock to unit root + archive previous primary if needed."""
    locked = UNIT / "_LOCKED-v06"
    locked.mkdir(parents=True, exist_ok=True)
    for name in ("art.png", "art-left.png", "art-right.png", "RECIPE.md", "meta.json"):
        s = src_folder / name
        if s.is_file():
            shutil.copy2(s, UNIT / name)
            shutil.copy2(s, locked / name)
    print("PROMOTED v06 → primary + _LOCKED-v06/")


def update_flow() -> None:
    text = FLOW.read_text(encoding="utf-8")
    # patch the decisions block note for S8
    old = None
    import re

    text2, n = re.subn(
        r'("page": "18\|19",\s*"beat": "S8 Gone",\s*"version": ")[^"]+(",\s*"model": "[^"]+",\s*"status": ")[^"]+(",\s*"decided_by": "Jon",\s*"date": "[^"]+",\s*"notes": ")[^"]*(")',
        r'\1v06\2keep\3LOCKED v06 · exact v02-left swirl wisp · v05 room (fire/moon/rug) · medium gifts −25% · Media/development/S08-gone/_LOCKED-v06/ · board S08-gone-v02L-vs-v06-'
        + DAY
        + r'.png\4',
        text,
        count=1,
    )
    # Also update p18/p19 captions/versions if present
    text2 = text2.replace(
        '"caption": "p18 · S8 Gone L · v01 boy+camera"',
        '"caption": "p18 · S8 Gone L · v06 LOCK"',
    )
    text2 = text2.replace(
        '"caption": "p19 · S8 Gone R · v01 empty room"',
        '"caption": "p19 · S8 Gone R · v06 LOCK"',
    )
    # version fields on p18/p19 — careful only those near S8
    text2 = re.sub(
        r'("id": "p18",[\s\S]*?"version": ")v01(")',
        r"\1v06\2",
        text2,
        count=1,
    )
    text2 = re.sub(
        r'("id": "p19",[\s\S]*?"version": ")v01(")',
        r"\1v06\2",
        text2,
        count=1,
    )
    text2 = re.sub(
        r'("id": "p18",[\s\S]*?"status": ")working(")',
        r"\1keep\2",
        text2,
        count=1,
    )
    text2 = re.sub(
        r'("id": "p19",[\s\S]*?"status": ")working(")',
        r"\1keep\2",
        text2,
        count=1,
    )
    FLOW.write_text(text2, encoding="utf-8")
    print("FLOW updated n_decisions_patch=", n)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    for p in (V02L, V02, V05):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Order: swirl lock first, then v05 base, then v02 full reinforce
    urls = [
        fal_client.upload_file(str(V02L)),
        fal_client.upload_file(str(V05)),
        fal_client.upload_file(str(V02)),
    ]
    print("refs: v02-left SWIRL + v05 BASE + v02 full")

    print("=== Qwen S8 Gone v06 FINAL ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": urls,
            "image_size": {"width": 2048, "height": 1024},
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
    tmp = UNIT / "_tmp-v06-qwen.png"
    raw.save(tmp)

    print("=== SeedVR ===")
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

    save_triplet(final, V06)

    (V06 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v06

| Field | Value |
|-------|--------|
| **name** | S8 Gone — FINAL (v05 room + exact v02-left swirl wisp) |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v06 |
| **date** | {DAY} |
| **status** | lock-if-swirl-matches |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **swirl lock** | `Media/development/S08-gone/v02/art-left.png` |
| **base** | v05 |

## Intent

Only fix: match v02-left elegant wispy swirl. Keep v05 room; gifts −25%.
""",
        encoding="utf-8",
    )
    (V06 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v06",
                "status": "lock_candidate",
                "swirl_lock": "v02/art-left.png",
                "base": "v05",
                "seed": seed,
                "fal_url": url,
                "size": list(TARGET),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    seamless_board(
        final,
        INDEX / f"S08-gone-v06-spread-{DAY}.png",
        unit="S08-gone",
        version="v06",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · FINAL · exact v02-left swirl",
        subtitle="Swirl wisp lock · v05 room · gifts −25%",
    )

    # Side-by-side: v02-left swirl vs v06 left
    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    ref = Image.open(V02L).convert("RGB")
    left = final.crop((0, 0, PAGE, PAGE))
    w, h = 900, 900
    a = ref.resize((w, h), Image.Resampling.LANCZOS)
    b = left.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 24, 20, 70
    sheet = Image.new(
        "RGB", (margin * 2 + w * 2 + gap, margin + header + h + 40), (252, 248, 240)
    )
    d = ImageDraw.Draw(sheet)
    f1, f2 = font(18), font(13)
    d.text((margin, 14), "S8 Gone SWIRL CHECK — v02-left LOCK  |  v06 left", fill=(35, 28, 22), font=f1)
    d.text(
        (margin, 42),
        "Must match elegant wispy whisper — not vortex/cloud",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v02 art-left — swirl LOCK", fill=(50, 40, 35), font=f2)
    d.text((margin + w + gap, y + h + 8), "v06 left — candidate", fill=(50, 40, 35), font=f2)
    board = INDEX / f"S08-gone-v02L-vs-v06-{DAY}.png"
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V06", V06 / "art.png")
    print("NOTE: promote only after visual swirl match (agent will inspect next)")


if __name__ == "__main__":
    main()
