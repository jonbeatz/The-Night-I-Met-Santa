#!/usr/bin/env python3
"""Lock S10 Note v02 + generate S11 Wish seamless spread v01."""
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
S10 = ROOT / "Media/development/S10-note"
S11 = ROOT / "Media/development/S11-wish"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

P22 = S10 / "v02" / "p22" / "art.png"
P23 = S10 / "v02" / "p23" / "art.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
S8 = ROOT / "Media/development/S08-gone/art.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
S3_FALLBACK = ROOT / "Media/development/S03-eyes-met/art.png"
GLOW = ROOT / "Images/styles3/scene-12b-tearing-open-PORTRAIT.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625. NO fake gutter, NO spine shadow, NO text.

IMAGE 1 = continuity from S10 reading beat — same Boy G0 (holly PJs), burgundy room, glowing letter energy.
IMAGE 2 = room/window continuity (S8 Gone spread) — night window, moonlight, burgundy walls, patterned rug language.
IMAGE 3 = glowing letter expression/light reference — soft golden letter glow illuminating the face.

Rich oil-painting quality matching S3 Eyes Met. Continuous ONE room across both halves.

LEFT half (p24): Quiet night WINDOW with moonlight coming in through glass — snowy night / full moon \
mood. Establishing quiet. Soft moonlight beams. Burgundy walls. No boy on this half (or boy only \
barely if continuous — prefer window-focused left). Faces off the gutter.

RIGHT half (p25): Boy sitting Indian-style / cross-legged on the patterned rug, reading the letter. \
Slightly glowing envelope/letter lighting his face with soft golden glow. Ripped paper pieces \
scattered around him on the floor (he tore the note open). Holly pajamas with red trim. Wonder \
softened into absorbed reading (still emotional, not laughing). Intimate floor-level camera. \
Christmas tree / room warmth may continue from left. Continuous seamless scene with the window side.

NO Santa in the room. NO baked text or readable writing on the letter. Five fingers only.
"""

NEG = (
    "text, letters, typography, watermark, readable writing, fake gutter, spine shadow, "
    "Santa Claus in room, toddler, blue pajamas, hard page split line"
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


def promote_s10() -> None:
    for p in (P22, P23):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    locked = S10 / "_LOCKED-v02"
    locked.mkdir(parents=True, exist_ok=True)

    for src, name in ((P22, "art-left.png"), (P23, "art-right.png")):
        im = Image.open(src).convert("RGB")
        im.save(S10 / name, optimize=True)
        im.save(locked / name, optimize=True)
        print("promoted", name)

    shutil.copy2(P22, locked / "p22.png")
    shutil.copy2(P23, locked / "p23.png")

    recipe = f"""# RECIPE — S10-note LOCKED v02

| Page | Path | KEEP |
|------|------|------|
| **p22 L** | `art-left.png` · `v02/p22/art.png` | Candle + holly · cream center |
| **p23 R** | `art-right.png` · `v02/p23/art.png` | Glowing letter · stunned silence |

**Locked:** {DAY} · Jon OK · archive `_LOCKED-v02/`
"""
    (S10 / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (locked / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (S10 / "meta.json").write_text(
        json.dumps(
            {
                "status": "keep",
                "version": "v02",
                "locked_date": DAY,
                "layout": "text_image",
                "paths": {
                    "art_left": "Media/development/S10-note/art-left.png",
                    "art_right": "Media/development/S10-note/art-right.png",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # FLOW — surgical replacements on known-good blocks
    data = json.loads(FLOW.read_text(encoding="utf-8"))
    for page in data.get("pages", data if isinstance(data, list) else []):
        pass

    # Prefer pages array structure
    root = json.loads(FLOW.read_text(encoding="utf-8"))
    pages = root.get("pages") or root.get("flow") or []
    # Find structure
    if "pages" not in root:
        # try top-level list keys
        for key in root:
            if isinstance(root[key], list) and root[key] and isinstance(root[key][0], dict) and "id" in root[key][0]:
                pages_key = key
                pages = root[key]
                break
        else:
            pages_key = None
            pages = []
    else:
        pages_key = "pages"

    def upd_page(pid: str, **kw):
        for p in pages:
            if p.get("id") == pid:
                p.update(kw)
                return True
        return False

    upd_page(
        "p22",
        caption="p22 · S10 text · v02 KEEP",
        path="Media/development/S10-note/art-left.png",
        version="v02",
        model="Qwen 2 Pro /edit v06 · 2625×2625",
        status="keep",
        date=DAY,
        notes="LOCKED v02 · candle + holly · cream center · _LOCKED-v02/",
        development_path="Media/development/S10-note/art-left.png",
    )
    upd_page(
        "p23",
        caption="p23 · S10 Note R · v02 KEEP",
        path="Media/development/S10-note/art-right.png",
        version="v02",
        model="Qwen 2 Pro /edit v06 · 2625×2625",
        status="keep",
        date=DAY,
        notes="LOCKED v02 · glowing letter · stunned silence · _LOCKED-v02/",
        development_path="Media/development/S10-note/art-right.png",
    )

    decisions = root.get("decisions") or root.get("beats") or []
    dec_key = "decisions" if "decisions" in root else ("beats" if "beats" in root else None)
    if dec_key:
        for d in root[dec_key]:
            if d.get("beat") == "S10 Note" or d.get("page") == "22|23":
                d.update(
                    {
                        "page": "22|23",
                        "beat": "S10 Note",
                        "version": "v02",
                        "model": "Qwen 2 Pro /edit v06 · 2625×2625",
                        "status": "keep",
                        "decided_by": "Jon",
                        "date": DAY,
                        "notes": "LOCKED v02 · candle/holly text + glowing letter stun · Media/development/S10-note/_LOCKED-v02/ · board S10-note-v02-text-image-2026-07-23.png",
                    }
                )
                break

    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("S10 FLOW keep OK")

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board

    text_image_board(
        Image.open(S10 / "art-left.png"),
        Image.open(S10 / "art-right.png"),
        INDEX / f"S10-note-LOCKED-v02-{DAY}.png",
        unit="S10-note",
        version="LOCKED v02",
        day=DAY,
        tech="KEEP · candle/holly text · glowing letter stun · 2625×2625",
        subtitle="Jon lock · poem in InDesign",
        side=700,
    )


def park_s11() -> None:
    arch = S11 / "_archive-pre-v01"
    if arch.exists():
        return
    has = any((S11 / n).is_file() for n in ("art.png", "art-left.png", "art-right.png"))
    if not has:
        return
    arch.mkdir(parents=True, exist_ok=True)
    for n in ("art.png", "art-left.png", "art-right.png", "meta-p24.json", "meta-p25.json"):
        src = S11 / n
        if src.is_file():
            shutil.move(str(src), str(arch / n))
            print("parked S11", n)


def gen_s11() -> None:
    park_s11()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    s3 = S3 if S3.is_file() else S3_FALLBACK
    # 3 refs: S10 reading continuity, S8 room/window, glow expression
    refs = [P23, S8, GLOW if GLOW.is_file() else BOY]
    for p in refs:
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen S11 Wish spread ===")
    print("refs:", [p.name for p in refs])
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
    tmp = S11 / "_tmp-v01-qwen.png"
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
    final = up_im.resize(SPREAD, Image.Resampling.LANCZOS)
    tmp.unlink(missing_ok=True)

    v01 = S11 / "v01"
    v01.mkdir(parents=True, exist_ok=True)
    final.save(v01 / "art.png", optimize=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    left.save(v01 / "art-left.png", optimize=True)
    right.save(v01 / "art-right.png", optimize=True)
    # primary working mirrors
    final.save(S11 / "art.png", optimize=True)
    left.save(S11 / "art-left.png", optimize=True)
    right.save(S11 / "art-right.png", optimize=True)

    (v01 / "RECIPE.md").write_text(
        f"""# RECIPE — S11-wish / v01

| Field | Value |
|-------|--------|
| **name** | S11 Wish — moonlight window + boy cross-legged reading |
| **layout** | FULL SPREAD seamless |
| **version** | v01 |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** triplet |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | S10 p23 KEEP · S8 Gone · scene-12b glow |

## Intent

L: night window + moonlight. R: boy cross-legged, glowing letter, ripped paper on floor. Continuous room.
""",
        encoding="utf-8",
    )
    (v01 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v01",
                "status": "working",
                "layout": "seamless_spread",
                "size": list(SPREAD),
                "seed": seed,
                "fal_url": url,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    seamless_board(
        final,
        INDEX / f"S11-wish-v01-spread-{DAY}.png",
        unit="S11-wish",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · S10+S8 continuity · glow letter",
        subtitle="Window moonlight L · cross-legged reading + ripped paper R",
    )

    # FLOW S11
    root = json.loads(FLOW.read_text(encoding="utf-8"))
    pages = root.get("pages")
    if pages is None:
        for key, val in root.items():
            if isinstance(val, list) and val and isinstance(val[0], dict) and "id" in val[0]:
                pages = val
                break
    for p in pages or []:
        if p.get("id") == "p24":
            p.update(
                {
                    "caption": "p24 · S11 Wish L · v01 window",
                    "path": "Media/development/S11-wish/art-left.png",
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "date": DAY,
                    "notes": "Night window + moonlight · seamless with p25",
                    "development_path": "Media/development/S11-wish/art.png",
                    "pixel_size": "2625x2625",
                    "spread_side": "L",
                }
            )
        if p.get("id") == "p25":
            p.update(
                {
                    "caption": "p25 · S11 Wish R · v01 reading",
                    "path": "Media/development/S11-wish/art-right.png",
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "date": DAY,
                    "notes": "Cross-legged · glowing letter · ripped paper · seamless with p24",
                    "development_path": "Media/development/S11-wish/art.png",
                    "pixel_size": "2625x2625",
                    "spread_side": "R",
                }
            )
    for key in ("decisions", "beats"):
        if key not in root:
            continue
        for d in root[key]:
            if d.get("beat") == "S11 Wish" or d.get("page") == "24|25":
                d.update(
                    {
                        "page": "24|25",
                        "beat": "S11 Wish",
                        "version": "v01",
                        "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                        "status": "working",
                        "decided_by": "Jon",
                        "date": DAY,
                        "notes": "Seamless spread · window L · boy reading R · board S11-wish-v01-spread-2026-07-23.png · Media/development/S11-wish/v01/",
                    }
                )
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("S11 FLOW OK")
    print("S11", S11 / "art.png")


def main() -> None:
    load_env()
    INDEX.mkdir(parents=True, exist_ok=True)
    promote_s10()
    gen_s11()
    cont = ROOT / ".cursor/docs/CONTINUE-HERE.md"
    if cont.is_file():
        t = cont.read_text(encoding="utf-8")
        import re

        t2 = re.sub(
            r"## One-line status \(2026-07-23\)\n\n[\s\S]*?(?=\n---)",
            "## One-line status (2026-07-23)\n\n"
            "**S10 Note v02 LOCKED** · **S11 Wish v01** spread dial ready  \n"
            "**S9 Search** KEEP · **S8 Gone v09** KEEP · **S3 v07** quality bar  \n"
            "**SoT:** `_FLOW-CURRENT.json` · **NEXT:** Jon eye on S11 → S12a Blessing.\n",
            t,
            count=1,
        )
        cont.write_text(t2, encoding="utf-8")
    print("DONE")


if __name__ == "__main__":
    main()
