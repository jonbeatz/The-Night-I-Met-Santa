#!/usr/bin/env python3
"""S10 Note v02 — candle/holly text page + glowing letter stunned silence."""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S10-note"
V02 = UNIT / "v02"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"

CANDLE = ROOT / "Images/styles3/p31-quiet-ornament.png"
DEDICATION = ROOT / "Images/styles3/matter-dedication.png"
GLOW = ROOT / "Images/styles3/scene-12b-tearing-open-PORTRAIT.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
BOY_FACE = ROOT / "Media/approved/characters/boy-narrator-G0-face.png"
V01_P23 = UNIT / "v01" / "p23" / "art.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT_L = """\
Square children's-book TEXT PAGE 2625x2625.

IMAGE 1 = DESIGN GUIDE (candle + holly ornament page) — match this layout language: lit candle with \
soft warm golden glow on one side; holly sprig with red berries and red ribbon on the lower opposite \
corner; vast clean cream center (~95% open) for poem text; soft watercolor vignette dissolving to cream.

IMAGE 2 = optional second text-page mood (dedication frame) — soft holiday edge whispers only, do not \
fill the center.

IMAGE 3 = STANDARD FRAME TREATMENT — soft watercolor vignette to cream edges.

Create a quiet watercolor TEXT PAGE: two simple holiday elements framing the space — candle glow and \
holly are WHISPERS that set mood without competing. Clean cream center for InDesign poem. NO baked text. \
NO boy. NO Santa. NO busy room scene. Heirloom storybook paper feel.
"""

NEG_L = (
    "text, letters, typography, watermark, boy, Santa, chair, full room, busy illustration, "
    "dark muddy center, hard border, geometric frame, christmas lights string filling page"
)

PROMPT_R = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07.

IMAGE 1 = GLOWING LETTER + STUNNED EXPRESSION LOCK — letter/envelope emanates soft golden magical light \
illuminating the face from below; expression is overwhelmed stunned silence — eyes wide, mouth slightly \
open, frozen still. Emotional overload, NOT smiling, NOT curious wonder/curiosity grin. Match that glow \
and that stunned face energy.

IMAGE 2 = Boy G0 CHARACTER LOCK (body + face) — 5–7 years old, oatmeal holly pajamas with green holly \
+ red berries, red trim. Same boy as locked spreads. Keep holly PJs (do NOT switch to red sweater).

IMAGE 3 = POSE / CHAIR CONTINUITY from prior S10 plate — boy kneeling, elbows on wooden chair seat, \
letter held up near face. Burgundy walls. Soft Christmas lights may glow faintly in background.

COMPOSITION: Intimate close — hands and glowing letter are heroes. Letter casts soft golden light on \
his face from below. Stunned silence expression. Standard soft watercolor vignette to cream edges. \
NO readable writing on the letter. NO baked poem text. NO Santa.
"""

NEG_R = (
    "text, letters, typography, readable writing, watermark, smiling, happy grin, casual curiosity, "
    "toddler, baby face, blue pajamas, red sweater instead of holly PJs, Santa, hard border"
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
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


def gen(out_dir: Path, page_id: str, prompt: str, neg: str, refs: list[Path], label: str) -> tuple[Image.Image, int | None, str]:
    urls = [fal_client.upload_file(str(p)) for p in refs]
    print(f"=== Qwen {page_id}: {label} ===")
    print("refs:", [p.name for p in refs])
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": prompt,
            "negative_prompt": neg,
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
    final = upscale(raw, UNIT / f"_tmp-{page_id}-v02-qwen.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    final.save(out_dir / "art.png", optimize=True)
    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S10-note / {page_id} / v02

| Field | Value |
|-------|--------|
| **name** | S10 Note — {label} |
| **version** | v02 |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
""",
        encoding="utf-8",
    )
    (out_dir / "meta.json").write_text(
        json.dumps({"page": page_id, "version": "v02", "seed": seed, "fal_url": url, "size": list(TARGET)}, indent=2),
        encoding="utf-8",
    )
    return final, seed, url


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board  # type: ignore

    for p in (CANDLE, DEDICATION, GLOW, BOY, BOY_FACE, V01_P23, FRAME):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # p22: candle/holly design + dedication mood + frame
    p22, _, _ = gen(
        V02 / "p22",
        "p22",
        PROMPT_L,
        NEG_L,
        [CANDLE, DEDICATION, FRAME],
        "candle + holly text page · open cream center",
    )

    boy_strip = hstrip([BOY, BOY_FACE], UNIT / "_tmp-v02-boy.png")
    # p23: glow/stun ref + Boy G0 + v01 pose/chair
    p23, _, _ = gen(
        V02 / "p23",
        "p23",
        PROMPT_R,
        NEG_R,
        [GLOW, boy_strip, V01_P23],
        "glowing letter · stunned silence · elbows on chair",
    )
    boy_strip.unlink(missing_ok=True)

    # working mirrors
    p22.save(UNIT / "art-left.png", optimize=True)
    p23.save(UNIT / "art-right.png", optimize=True)

    (V02 / "RECIPE.md").write_text(
        f"""# RECIPE — S10-note / v02 (TEXT + IMAGE)

| Page | Path | Role |
|------|------|------|
| **p22** | `v02/p22/art.png` | Candle L + holly R · cream center |
| **p23** | `v02/p23/art.png` | Glowing letter · stunned silence |

**Refs:** `p31-quiet-ornament` · `matter-dedication` · `scene-12b-tearing-open-PORTRAIT` · Boy G0  
**{DAY}** · 2625² · Qwen v06
""",
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    text_image_board(
        p22,
        p23,
        INDEX / f"S10-note-v02-text-image-{DAY}.png",
        unit="S10-note",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 TEXT+IMAGE · candle/holly · glowing letter stun",
        subtitle="p22 open cream · p23 stunned glow · FINAL dial",
        side=700,
    )

    # FLOW update (careful — write full blocks)
    text = FLOW.read_text(encoding="utf-8")
    text = re.sub(
        r'("id": "p22",[\s\S]*?"caption": ")[^"]*(")',
        r'\1p22 · S10 text · v02 candle/holly\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"path": ")[^"]*(")',
        r'\1Media/development/S10-note/v02/p22/art.png\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"version": ")[^"]*(")',
        r"\1v02\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"status": ")[^"]*(")',
        r"\1working\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"notes": ")[^"]*(")',
        r"\1TEXT · candle L + holly R · 95% open cream · styles3 p31\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"caption": ")[^"]*(")',
        r'\1p23 · S10 Note R · v02 glowing letter\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"path": ")[^"]*(")',
        r'\1Media/development/S10-note/v02/p23/art.png\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"version": ")[^"]*(")',
        r"\1v02\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"notes": ")[^"]*(")',
        r"\1Glowing letter · stunned silence · Boy G0 holly PJs · scene-12b glow ref\2",
        text,
        count=1,
    )
    text, n = re.subn(
        r'("page": "22\|23",\s*"beat": "S10 Note",\s*"version": ")[^"]+(",\s*"model": "[^"]+",\s*"status": ")[^"]+(",\s*"decided_by": "Jon",\s*"date": "[^"]+",\s*"notes": ")[^"]*(")',
        r'\1v02\2working\3candle/holly text · glowing letter stun · board S10-note-v02-text-image-'
        + DAY
        + r'.png · Media/development/S10-note/v02/\4',
        text,
        count=1,
    )
    FLOW.write_text(text, encoding="utf-8")
    # validate
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("FLOW OK n=", n)
    print("P22", V02 / "p22" / "art.png")
    print("P23", V02 / "p23" / "art.png")


if __name__ == "__main__":
    main()
