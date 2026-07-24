#!/usr/bin/env python3
"""Lock S9 Search pair + generate S10 Note TEXT+IMAGE v01."""
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
S09 = ROOT / "Media/development/S09-search"
S10 = ROOT / "Media/development/S10-note"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

P20 = S09 / "v06" / "p20" / "art.png"
P21 = S09 / "v05" / "p21" / "art.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
BOY_FACE = ROOT / "Media/approved/characters/boy-narrator-G0-face.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
S3L = ROOT / "Media/development/S03-eyes-met/art-left.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
S7L = ROOT / "Media/development/S07-proof/art-left.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)


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


def promote_s09() -> None:
    for p in (P20, P21):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    locked = S09 / "_LOCKED-pair-v06L-v05R"
    locked.mkdir(parents=True, exist_ok=True)
    # RGB promote
    for src, dest_name, lock_name in (
        (P20, "art-left.png", "art-left.png"),
        (P21, "art-right.png", "art-right.png"),
    ):
        im = Image.open(src).convert("RGB")
        im.save(S09 / dest_name, optimize=True)
        im.save(locked / lock_name, optimize=True)
        print("promoted", dest_name)

    # Also copy version folder arts into lock
    shutil.copy2(P20, locked / "p20-v06.png")
    shutil.copy2(P21, locked / "p21-v05.png")

    recipe = f"""# RECIPE — S09-search LOCKED

| Page | Version | Path |
|------|---------|------|
| **p20 L** | **v06 KEEP** | `art-left.png` · `v06/p20/art.png` |
| **p21 R** | **v05 KEEP** | `art-right.png` · `v05/p21/art.png` |

**Date locked:** {DAY} · Jon OK  
**p20:** Boy fills frame, low-angle hands/knees search, age 5–7, holly PJs, burgundy wall bg  
**p21:** Chair back to fireplace, note, cocoa + cookie, moonlight streaks, dying embers  

Archive: `_LOCKED-pair-v06L-v05R/` · also `_LOCKED-v05-p21/`
"""
    (S09 / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (locked / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (S09 / "meta.json").write_text(
        json.dumps(
            {
                "status": "keep",
                "locked_date": DAY,
                "p20": "v06",
                "p21": "v05",
                "paths": {
                    "art_left": "Media/development/S09-search/art-left.png",
                    "art_right": "Media/development/S09-search/art-right.png",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # FLOW pages + decisions
    text = FLOW.read_text(encoding="utf-8")
    text = re.sub(
        r'("id": "p20",[\s\S]*?"caption": ")[^"]*(")',
        r'\1p20 · S9 Search L · v06 KEEP\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p20",[\s\S]*?"path": ")[^"]*(")',
        r'\1Media/development/S09-search/art-left.png\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p20",[\s\S]*?"version": ")[^"]*(")',
        r"\1v06\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p20",[\s\S]*?"status": ")[^"]*(")',
        r"\1keep\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p20",[\s\S]*?"notes": ")[^"]*(")',
        r"\1LOCKED v06 · boy fills frame · age 5-7 · burgundy bg · _LOCKED-pair-v06L-v05R/\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p20",[\s\S]*?"development_path": ")[^"]*(")',
        r"\1Media/development/S09-search/art-left.png\2",
        text,
        count=1,
    )

    text = re.sub(
        r'("id": "p21",[\s\S]*?"caption": ")[^"]*(")',
        r'\1p21 · S9 Search R · v05 KEEP\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p21",[\s\S]*?"path": ")[^"]*(")',
        r'\1Media/development/S09-search/art-right.png\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p21",[\s\S]*?"version": ")[^"]*(")',
        r"\1v05\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p21",[\s\S]*?"status": ")[^"]*(")',
        r"\1keep\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p21",[\s\S]*?"notes": ")[^"]*(")',
        r"\1LOCKED v05 · chair/note/cookie/moonlight · _LOCKED-pair-v06L-v05R/\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p21",[\s\S]*?"development_path": ")[^"]*(")',
        r"\1Media/development/S09-search/art-right.png\2",
        text,
        count=1,
    )

    text, n = re.subn(
        r'("page": "20\|21",\s*"beat": "S9 Search",\s*"version": ")[^"]+(",\s*"model": "[^"]+",\s*"status": ")[^"]+(",\s*"decided_by": "Jon",\s*"date": "[^"]+",\s*"notes": ")[^"]*(")',
        r'\1v06L+v05R\2keep\3LOCKED · p20 v06 + p21 v05 · Media/development/S09-search/art-left|art-right · _LOCKED-pair-v06L-v05R/ · board S09-search-v06-p20-v05p21-'
        + DAY
        + r'.png\4',
        text,
        count=1,
    )
    FLOW.write_text(text, encoding="utf-8")
    print("FLOW S9 keep patch n=", n)

    # lock board
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board

    split_board(
        Image.open(S09 / "art-left.png"),
        Image.open(S09 / "art-right.png"),
        INDEX / f"S09-search-LOCKED-v06L-v05R-{DAY}.png",
        unit="S09-search",
        version="LOCKED",
        day=DAY,
        tech="KEEP · p20 v06 + p21 v05 · 2625×2625 SPLIT",
        subtitle="Boy search close-up · chair discovery · Jon lock",
        side=700,
    )
    print("S9 LOCKED")


def park_s10_old() -> None:
    arch = S10 / "_archive-pre-v01"
    if arch.exists():
        return
    has = any((S10 / n).is_file() for n in ("art.png", "art-left.png", "art-right.png"))
    if not has:
        return
    arch.mkdir(parents=True, exist_ok=True)
    for n in ("art.png", "art-left.png", "art-right.png", "meta-p22.json", "meta-p23.json"):
        src = S10 / n
        if src.is_file():
            shutil.move(str(src), str(arch / n))
            print("parked S10", n)


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


def gen(out_dir: Path, page_id: str, prompt: str, neg: str, refs: list[Path], label: str) -> Image.Image:
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
    final = upscale(raw, S10 / f"_tmp-{page_id}-qwen.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    final.save(out_dir / "art.png", optimize=True)
    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S10-note / {page_id} / v01

| Field | Value |
|-------|--------|
| **name** | S10 Note — {label} |
| **version** | v01 |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
""",
        encoding="utf-8",
    )
    (out_dir / "meta.json").write_text(
        json.dumps({"page": page_id, "version": "v01", "seed": seed, "fal_url": url, "size": list(TARGET)}, indent=2),
        encoding="utf-8",
    )
    return final


def gen_s10() -> None:
    park_s10_old()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board

    # cream base for text page
    cream = Image.new("RGB", (1536, 1536), (250, 244, 232))
    cream_path = S10 / "_tmp-cream.png"
    cream.save(cream_path)

    # optional lights hint - use S9 tree edge or S8 right crop
    lights_src = S09 / "art-right.png"
    if not lights_src.is_file():
        lights_src = P21

    prompt_l = """\
Square children's-book TEXT PAGE 2625x2625.
IMAGE 1 = cream watercolor paper base.
IMAGE 2 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream/ivory at edges.
IMAGE 3 = Christmas lights atmosphere only — use as a VERY FAINT hint of a string of warm Christmas \
lights peeking in from the RIGHT edge of the page (whisper only, ~15-25% presence).

Almost blank heirloom watercolor text page. LARGE OPEN quiet CENTER for live poem text. Soft cream/ivory \
paper texture. Soft vignette. NOT a full room illustration. NO boy. NO Santa. NO chair. NO fireplace. \
NO baked text or letters.
"""
    neg_l = (
        "busy full scene, strong opaque illustration, boy, Santa, chair, fireplace, tree filling page, "
        "dark muddy center, text, letters, watermark, hard border, geometric frame"
    )

    p22 = gen(
        S10 / "v01" / "p22",
        "p22",
        prompt_l,
        neg_l,
        [cream_path, FRAME, lights_src],
        "watercolor text page · lights whisper R edge",
    )
    cream_path.unlink(missing_ok=True)

    age_ref = S7L if S7L.is_file() else S3L
    boy_strip = hstrip([BOY, BOY_FACE], S10 / "_tmp-boy-strip.png")
    quality = S3 if S3.is_file() else age_ref

    prompt_r = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07 (image 3).

IMAGE 1 = Boy G0 LOCK (full + face) — 5–7 years old, defined features, oatmeal holly pajamas with \
green holly + red berries, red trim. Same boy as locked spreads. NOT toddler.

IMAGE 2 = CHAIR / ROOM CONTINUITY from S9 discovery — same wooden chair, burgundy walls, warm room. \
Boy is now at this chair reading.

IMAGE 3 = quality bar.

COMPOSITION — p23 IMAGE PAGE (intimate close):
Boy on his knees, elbows on the chair, letter/note held in both hands UP near his face, looking at \
the letter with wonder. Hands and note are the heroes. Intimate close-up. Burgundy walls soft behind. \
Standard soft watercolor vignette dissolve to cream edges. Holly PJs.

Note paper is blank or illegible scribbles only — NO readable text. NO Santa. NO baked poem text.
"""
    neg_r = (
        "text, letters, typography, readable writing, watermark, Santa, toddler, baby face, "
        "blue pajamas, wide empty room, hard border"
    )

    # Prefer chair continuity: P21 + boy + quality — but need boy. Stack: boy_strip, P21, quality
    p23 = gen(
        S10 / "v01" / "p23",
        "p23",
        prompt_r,
        neg_r,
        [boy_strip, P21, quality],
        "boy elbows on chair · letter near face · wonder",
    )
    boy_strip.unlink(missing_ok=True)

    # promote working mirrors
    p22.save(S10 / "art-left.png", optimize=True)
    p23.save(S10 / "art-right.png", optimize=True)

    (S10 / "v01" / "RECIPE.md").write_text(
        f"""# RECIPE — S10-note / v01 (TEXT + IMAGE)

| Page | Path | Role |
|------|------|------|
| **p22 L** | `v01/p22/art.png` (= art-left) | Watercolor text page · lights whisper |
| **p23 R** | `v01/p23/art.png` (= art-right) | Boy reading letter at chair |

**{DAY}** · 2625² · Qwen v06 · Continuity chair from S9 p21 KEEP
""",
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    text_image_board(
        p22,
        p23,
        INDEX / f"S10-note-v01-text-image-{DAY}.png",
        unit="S10-note",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 TEXT+IMAGE · S3 bar · S9 chair continuity",
        subtitle="p22 lights-whisper paper · p23 reading letter at chair",
    )
    print("S10 board done")

    # FLOW S10 update
    text = FLOW.read_text(encoding="utf-8")
    text = re.sub(
        r'("id": "p22",[\s\S]*?"caption": ")[^"]*(")',
        r'\1p22 · S10 text · v01\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"path": ")[^"]*(")',
        r'\1Media/development/S10-note/v01/p22/art.png\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"version": ")[^"]*(")',
        r"\1v01\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"model": ")[^"]*(")',
        r"\1Qwen 2 Pro /edit v06 · 2625×2625\2",
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
        r'("id": "p22",[\s\S]*?"date": ")[^"]*(")',
        r"\12026-07-23\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"notes": ")[^"]*(")',
        r"\1TEXT page · cream + lights whisper R · open center\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p22",[\s\S]*?"development_path": ")[^"]*(")',
        r"\1Media/development/S10-note/art-left.png\2",
        text,
        count=1,
    )

    text = re.sub(
        r'("id": "p23",[\s\S]*?"caption": ")[^"]*(")',
        r'\1p23 · S10 Note R · v01 reading\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"path": ")[^"]*(")',
        r'\1Media/development/S10-note/v01/p23/art.png\2',
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"version": ")[^"]*(")',
        r"\1v01\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"model": ")[^"]*(")',
        r"\1Qwen 2 Pro /edit v06 · 2625×2625\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"status": ")[^"]*(")',
        r"\1working\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"date": ")[^"]*(")',
        r"\12026-07-23\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"notes": ")[^"]*(")',
        r"\1Boy elbows on chair · letter near face · S9 chair continuity\2",
        text,
        count=1,
    )
    text = re.sub(
        r'("id": "p23",[\s\S]*?"development_path": ")[^"]*(")',
        r"\1Media/development/S10-note/art-right.png\2",
        text,
        count=1,
    )

    text, n = re.subn(
        r'("page": "22\|23",\s*"beat": "S10 Note",\s*"version": ")[^"]+(",\s*"model": "[^"]+",\s*"status": ")[^"]+(",\s*"decided_by": "Jon",\s*"date": "[^"]+",\s*"notes": ")[^"]*(")',
        r'\1v01\2working\3TEXT+IMAGE · p22 lights-whisper paper · p23 reading at chair · board S10-note-v01-text-image-'
        + DAY
        + r'.png · Media/development/S10-note/v01/\4',
        text,
        count=1,
    )
    # fix date in that block
    text = text.replace(
        '"page": "22|23",\n      "beat": "S10 Note",\n      "version": "v01",\n      "model": "Qwen 2 Pro /edit v06 · 2625×2625 TEXT+IMAGE · S3 bar · S9 chair continuity",',
        '"page": "22|23",\n      "beat": "S10 Note",\n      "version": "v01",\n      "model": "Qwen 2 Pro /edit v06 · 2625×2625",',
    )
    # simpler: rewrite decisions note was set; also set date
    text = re.sub(
        r'("page": "22\|23",\s*"beat": "S10 Note",[\s\S]*?"date": ")[^"]+(")',
        r"\12026-07-23\2",
        text,
        count=1,
    )
    FLOW.write_text(text, encoding="utf-8")
    print("FLOW S10 patch n=", n)


def main() -> None:
    load_env()
    INDEX.mkdir(parents=True, exist_ok=True)
    promote_s09()
    gen_s10()
    # CONTINUE-HERE
    cont = ROOT / ".cursor/docs/CONTINUE-HERE.md"
    if cont.is_file():
        t = cont.read_text(encoding="utf-8")
        old = "## One-line status (2026-07-23)"
        if old in t:
            # replace first status block lines loosely
            pass
        t2 = re.sub(
            r"## One-line status \(2026-07-23\)\n\n[\s\S]*?(?=\n---)",
            f"## One-line status (2026-07-23)\n\n"
            f"**S9 Search LOCKED** (p20 v06 + p21 v05) · **S10 Note v01** TEXT+IMAGE dial ready  \n"
            f"**S3 Eyes Met v07** = QUALITY BAR · **S8 Gone v09** KEEP  \n"
            f"**SoT:** `_FLOW-CURRENT.json` · **NEXT:** Jon eye on S10 → S11 Wish.\n",
            t,
            count=1,
        )
        cont.write_text(t2, encoding="utf-8")
    print("DONE")


if __name__ == "__main__":
    main()
