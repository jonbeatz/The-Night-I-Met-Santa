#!/usr/bin/env python3
"""S9 Search p20 v06 ONLY — age-lock Boy G0 + S7; character-close. p21 v05 stays LOCKED."""
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
V06_P20 = UNIT / "v06" / "p20"
V05_P21 = UNIT / "v05" / "p21"
LOCKED_P21 = UNIT / "_LOCKED-v05-p21"
INDEX = ROOT / "Media/generated/mocks/_INDEX"

BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
BOY_FACE = ROOT / "Media/approved/characters/boy-narrator-G0-face.png"
S7L = ROOT / "Media/development/S07-proof/art-left.png"
S3L = ROOT / "Media/development/S03-eyes-met/art-left.png"
POSTURE1 = ROOT / "Images/styles2/page-10-the-search.png"
POSTURE2 = ROOT / "Images/styles2/p19-beat10-the-search2.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3/S7 locked plates.

IMAGE 1 = SEARCH POSTURE + LOW CAMERA (two refs side-by-side) — hands and knees among gifts, \
kid-level low angle, actively searching. Match that ACTION and CAMERA only — NOT the boy age/face \
from those refs (those refs show wrong pajamas/age).

IMAGE 2 = BOY G0 LOCK (full body + face sheet) — EXACT identity: 5–7 years old, more defined \
facial features, NOT a toddler, NOT 3–4, NOT cherubic baby face. Oatmeal/taupe holly pajamas with \
green holly leaves + red berries, red trim on collar/cuffs/hems, tousled light-brown hair, large \
expressive brown eyes, rosy cheeks. Same boy as every locked spread.

IMAGE 3 = AGE + APPEARANCE LOCK from a locked book plate where this boy already looks correct \
(S7 Proof). Match his face proportions, age, and painting treatment EXACTLY — no younger drift.

COMPOSITION — CHARACTER SHOT (critical):
The boy FILLS THE FRAME — close-up, low angle at his level, on hands and knees among scattered \
wrapped gifts. We see HIM first. Behind him: mostly deep BURGUNDY wall and patterned rug, soft and \
slightly out of focus. Christmas tree and fireplace barely visible at the extreme edges OR not \
visible at all. This hides chair-position mismatch with the facing page. Soft watercolor vignette \
dissolve to cream edges.

HARD: NO fire/flames/embers except optionally a tiny hint INSIDE a barely-visible fireplace. \
Prefer fireplace not visible. NO Santa. NO baked text. NO toddler face.
"""

NEG = (
    "toddler, baby face, cherubic, 3 year old, 4 year old, chubby baby cheeks exaggerated, "
    "text, letters, watermark, Santa, blue pajamas, polka dots, striped pajamas, "
    "wide room establishing shot, tiny distant boy, roaring fire, bright flames, "
    "embers on floor, hard border"
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


def hstrip(paths: list[Path], out: Path, height: int = 1024) -> Path:
    imgs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im = im.resize((int(im.width * height / im.height), height), Image.Resampling.LANCZOS)
        imgs.append(im)
    gap = 12
    w = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    sheet = Image.new("RGB", (w, height), (252, 248, 240))
    x = 0
    for im in imgs:
        sheet.paste(im, (x, 0))
        x += im.width + gap
    sheet.save(out)
    print("strip", out.name, sheet.size)
    return out


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


def lock_p21() -> None:
    """Archive v05 p21 as locked; do not regenerate."""
    LOCKED_P21.mkdir(parents=True, exist_ok=True)
    for name in ("art.png", "RECIPE.md", "meta.json"):
        src = V05_P21 / name
        if src.is_file():
            shutil.copy2(src, LOCKED_P21 / name)
    # mark recipe
    note = LOCKED_P21 / "LOCK.txt"
    note.write_text(
        f"LOCKED {DAY} — S9 Search RIGHT (p21) v05. Do not regenerate. Continuity for p20 dials.\n",
        encoding="utf-8",
    )
    print("LOCKED p21 →", LOCKED_P21)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board  # type: ignore
    from book_poem_map import captions  # type: ignore
    from PIL import ImageDraw, ImageFont

    age_ref = S7L if S7L.is_file() else S3L
    for p in (BOY, BOY_FACE, age_ref, POSTURE1, POSTURE2, V05_P21 / "art.png"):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    lock_p21()

    posture = hstrip([POSTURE1, POSTURE2], UNIT / "_tmp-v06-posture.png")
    boy_sheet = hstrip([BOY, BOY_FACE], UNIT / "_tmp-v06-boy-g0.png")

    urls = [
        fal_client.upload_file(str(posture)),
        fal_client.upload_file(str(boy_sheet)),
        fal_client.upload_file(str(age_ref)),
    ]
    print("=== Qwen p20 v06 ===")
    print("refs: posture strip + Boy G0+face +", age_ref.name)
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
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
    final = upscale(raw, UNIT / "_tmp-p20-v06-qwen.png")

    V06_P20.mkdir(parents=True, exist_ok=True)
    final.save(V06_P20 / "art.png", optimize=True)
    posture.unlink(missing_ok=True)
    boy_sheet.unlink(missing_ok=True)

    (V06_P20 / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / p20 / v06

| Field | Value |
|-------|--------|
| **name** | S9 Search L — age-locked character close-up |
| **unit** | S09-search |
| **book page** | p20 SPLIT |
| **version** | **v06** |
| **date** | {DAY} |
| **status** | working — pair with **p21 v05 LOCKED** |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | posture strip (`page-10-the-search` + `p19-beat10-the-search2`) · Boy G0 + face · `{age_ref.relative_to(ROOT).as_posix()}` age lock |
| **facing** | `v05/p21` / `_LOCKED-v05-p21` — NO changes |

## Fixes

1. Age 5–7 matching Boy G0 + locked S7/S3 plate (not toddler).
2. Camera: boy fills frame; burgundy wall/rug soft bg; tree/fireplace barely or not visible.
""",
        encoding="utf-8",
    )
    (V06_P20 / "meta.json").write_text(
        json.dumps(
            {
                "page": "p20",
                "version": "v06",
                "status": "working",
                "pairs_with": "v05/p21 LOCKED",
                "seed": seed,
                "fal_url": url,
                "age_ref": age_ref.name,
                "size": list(TARGET),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Unit RECIPE
    (UNIT / "v06" / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / v06

| Page | Version | Path | Status |
|------|---------|------|--------|
| **p20 L** | v06 | `v06/p20/art.png` | working (age + camera fix) |
| **p21 R** | **v05 LOCKED** | `v05/p21/art.png` · `_LOCKED-v05-p21/` | **keep** |

Do not regenerate p21.
""",
        encoding="utf-8",
    )

    # Board: v06 p20 + locked v05 p21 with poems
    p21 = Image.open(V05_P21 / "art.png").convert("RGB")
    out = INDEX / f"S09-search-v06-p20-v05p21-{DAY}.png"
    split_board(
        final,
        p21,
        out,
        unit="S09-search",
        version="v06L+v05R",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · p20 age-lock Boy G0+S7 · p21 v05 LOCKED",
        subtitle="LEFT v06 character close-up · RIGHT v05 discovery LOCKED",
        side=700,
    )
    # also v05 vs v06 left compare
    v05_l = UNIT / "v05" / "p20" / "art.png"
    if v05_l.is_file():
        def font(sz: int):
            for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
                if Path(p).is_file():
                    return ImageFont.truetype(p, sz)
            return ImageFont.load_default()

        a = Image.open(v05_l).convert("RGB").resize((700, 700), Image.Resampling.LANCZOS)
        b = final.resize((700, 700), Image.Resampling.LANCZOS)
        margin, gap, header = 24, 20, 70
        sheet = Image.new("RGB", (margin * 2 + 700 * 2 + gap, margin + header + 700 + 36), (252, 248, 240))
        d = ImageDraw.Draw(sheet)
        d.text((margin, 14), "S9 p20 — v05 (too young)  |  v06 age-lock + character close-up", fill=(35, 28, 22), font=font(18))
        d.text((margin, 42), "Boy G0 + face + S7 age lock · posture strip · fills frame", fill=(100, 90, 75), font=font(12))
        sheet.paste(a, (margin, margin + header))
        sheet.paste(b, (margin + 700 + gap, margin + header))
        d.text((margin, margin + header + 708), "v05", fill=(50, 40, 35), font=font(12))
        d.text((margin + 700 + gap, margin + header + 708), "v06", fill=(50, 40, 35), font=font(12))
        cmp = INDEX / f"S09-search-p20-v05-vs-v06-{DAY}.png"
        sheet.save(cmp)
        print("COMPARE", cmp)

    print("BOARD", out)
    print("P20", V06_P20 / "art.png")
    print("P21 LOCKED", V05_P21 / "art.png")


if __name__ == "__main__":
    main()
