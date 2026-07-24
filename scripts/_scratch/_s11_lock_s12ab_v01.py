#!/usr/bin/env python3
"""Lock S11 Wish v01 + generate S12a Blessing + S12b God Bless seamless spreads."""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

S11 = ROOT / "Media/development/S11-wish"
S12A = ROOT / "Media/development/S12a-blessing"
S12B = ROOT / "Media/development/S12b-god-bless"

BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
HOUSE = ROOT / "Media/approved/style-refs/covers/A-front-snow-house.png"
HOUSE2 = ROOT / "Images/styles3/cover-front.png"
S8L = ROOT / "Media/development/S08-gone/art-left.png"
BLESS_REF = ROOT / "Images/styles3/spread-04-closing-blessing-LEFT.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

NEG = (
    "text, letters, typography, watermark, readable writing, fake gutter, spine shadow, "
    "duplicate mirrored panels, identical left and right halves, blue pajamas, toddler"
)

PROMPT_S12A = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625. NO fake gutter, NO spine shadow, NO text.

IMAGE 1 = LOCKED S11 Wish spread — same burgundy room, moonlit window language, Boy G0 holly pajamas, \
glowing letter energy, Christmas tree continuity. MATCH this room.
IMAGE 2 = moonlit window plate — night window with strong moonlight beams (sleigh will appear outside).
IMAGE 3 = Boy G0 identity lock — age 5–7, holly PJs with red trim.

Rich oil-painting quality. Continuous ONE room across both halves. Inside/outside contrast.

LEFT half (p26): Night WINDOW with moonlight coming in. Outside through the glass: Santa's sleigh and \
reindeer flying away into the distance — small silhouette against the moon/night sky (departure). \
Quiet establishing. Burgundy walls. Soft moon beams. Faces/subjects off the gutter.

RIGHT half (p27): Zoomed-out peaceful WIDE room shot. Boy still reading the letter (letter still in hands). \
Boy is SMALL in the wooden chair (or perched small in the room) — absorbed, peaceful, wonder softened. \
Warm room: Christmas tree glow, patterned rug, burgundy walls continuing from left. Intimate stillness. \
NO Santa inside the room.

NO baked text. Five fingers only. Holly pajamas only.
"""

PROMPT_S12B = """\
Wide seamless outdoor Christmas night storybook SPREAD 5250x2625. NO fake gutter, NO spine shadow, NO text.
NO duplicated mirrored panels — LEFT and RIGHT must be DIFFERENT continuous halves of ONE scene.

IMAGE 1 = decorative snow house / Christmas exterior style reference.
IMAGE 2 = style lock — rich oil painting Christmas book quality.
IMAGE 3 = Santa G0 identity — use for distant flying silhouette only (not a portrait close-up).

Epic grand farewell exterior. Continuous snowy yard + house across the spread.

LEFT half (p28): Santa flying past a large full moon in the deep blue night sky over the decorative \
Christmas house (warm windows, garlands, snow on roof). Epic departure silhouette — sleigh + reindeer \
crossing the moon. House fills lower/mid left.

RIGHT half (p29): Right side of the SAME house continuing seamlessly. Snowman in the front lawn \
(top hat, carrot nose, scarf). The North Star gleaming brightly in the sky (distinct bright star with rays). \
Snowy ground, quiet witness mood. Ground-level feel on the snowman side.

Same house, continuous snow, continuous night sky. Magical oil-painting quality.
NO readable text. NO identical left/right copies.
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


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def load_flow() -> dict:
    return json.loads(FLOW.read_text(encoding="utf-8"))


def save_flow(root: dict) -> None:
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))


def plate(root: dict, pid: str) -> dict:
    for p in root["plates"]:
        if p.get("id") == pid:
            return p
    raise KeyError(pid)


def verdict(root: dict, page: str) -> dict:
    for d in root["verdicts"]:
        if d.get("page") == page:
            return d
    raise KeyError(page)


def park_old(folder: Path, tag: str) -> None:
    arch = folder / f"_archive-{tag}"
    if arch.exists():
        return
    moved = False
    for n in ("art.png", "art-left.png", "art-right.png", "meta-p26.json", "meta-p27.json", "meta-p28.json", "meta-p29.json"):
        src = folder / n
        if src.is_file() and src.stat().st_size > 0:
            arch.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(arch / n))
            print("parked", folder.name, n)
            moved = True
    if not moved:
        print("no primary art to park in", folder.name)


def qwen_spread(prompt: str, refs: list[Path], out_dir: Path, version: str) -> tuple[Image.Image, str, object]:
    for p in refs:
        if not p.is_file():
            raise SystemExit(f"missing ref: {p}")
    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen", out_dir.name, version, "===")
    print("refs:", [p.name for p in refs])
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": prompt,
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
    tmp = out_dir / f"_tmp-{version}-qwen.png"
    out_dir.mkdir(parents=True, exist_ok=True)
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

    vdir = out_dir / version
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, out_dir):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
    return final, url, seed


def promote_s11(root: dict) -> None:
    for name in ("art.png", "art-left.png", "art-right.png"):
        src = S11 / "v01" / name
        if not src.is_file():
            src = S11 / name
        if not src.is_file():
            raise SystemExit(f"missing S11 {name}")
        # ensure primary mirrors v01
        if (S11 / "v01" / name).is_file():
            shutil.copy2(S11 / "v01" / name, S11 / name)

    locked = S11 / "_LOCKED-v01"
    locked.mkdir(parents=True, exist_ok=True)
    for name in ("art.png", "art-left.png", "art-right.png"):
        shutil.copy2(S11 / name, locked / name)

    recipe = f"""# RECIPE — S11-wish LOCKED v01

| Page | Role | KEEP |
|------|------|------|
| **p24 L** | Moonlit window + beams | **ALL poem text** in InDesign (full stanza through \"simply a note.\") |
| **p25 R** | Boy cross-legged · glowing letter · ripped paper · tree | **IMAGE ONLY** — no text |

**Layout:** de facto TEXT + IMAGE · silent right lands the final line harder.

**Locked:** {DAY} · Jon OK · archive `_LOCKED-v01/`
"""
    (S11 / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (locked / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (S11 / "meta.json").write_text(
        json.dumps(
            {
                "status": "keep",
                "version": "v01",
                "locked_date": DAY,
                "layout": "text_image_defacto",
                "layout_note": "p24 carries ALL poem text in InDesign; p25 image-only",
                "paths": {
                    "art": "Media/development/S11-wish/art.png",
                    "art_left": "Media/development/S11-wish/art-left.png",
                    "art_right": "Media/development/S11-wish/art-right.png",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    layout_note = (
        "TEXT+IMAGE de facto · p24 ALL poem text in InDesign (full stanza thru 'simply a note') · "
        "p25 IMAGE ONLY · silent R lands final line · _LOCKED-v01/"
    )
    plate(root, "p24").update(
        {
            "caption": "p24 · S11 Wish L · v01 KEEP · ALL TEXT",
            "path": "Media/development/S11-wish/art-left.png",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "keep",
            "date": DAY,
            "notes": layout_note,
            "development_path": "Media/development/S11-wish/art.png",
            "layout": "text_image_defacto",
            "text_role": "all_poem_text",
            "pixel_size": "2625x2625",
            "spread_side": "L",
        }
    )
    plate(root, "p25").update(
        {
            "caption": "p25 · S11 Wish R · v01 KEEP · IMAGE ONLY",
            "path": "Media/development/S11-wish/art-right.png",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "keep",
            "date": DAY,
            "notes": "IMAGE ONLY · boy cross-legged · glowing letter · ripped paper · tree · " + layout_note,
            "development_path": "Media/development/S11-wish/art.png",
            "layout": "text_image_defacto",
            "text_role": "none",
            "pixel_size": "2625x2625",
            "spread_side": "R",
        }
    )
    verdict(root, "24|25").update(
        {
            "page": "24|25",
            "beat": "S11 Wish",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "keep",
            "decided_by": "Jon",
            "date": DAY,
            "notes": layout_note + " · board S11-wish-LOCKED-v01-2026-07-23.png",
            "layout": "text_image_defacto",
        }
    )
    print("S11 LOCKED keep OK")

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board

    text_image_board(
        Image.open(S11 / "art-left.png"),
        Image.open(S11 / "art-right.png"),
        INDEX / f"S11-wish-LOCKED-v01-{DAY}.png",
        unit="S11-wish",
        version="LOCKED v01",
        day=DAY,
        tech="KEEP · TEXT+IMAGE de facto · ALL text p24 · IMAGE ONLY p25 · 5250×2625",
        subtitle="Silent right lands: What he wants is simply a note.",
        side=700,
    )


def update_poem_map_s11() -> None:
    path = ROOT / "scripts/book_poem_map.py"
    text = path.read_text(encoding="utf-8")
    old = '''    "S11-wish": {
        "unit": "S11-wish",
        "layout": "seamless",
        "left_page": 24,
        "right_page": 25,
        "left": (
            "I tore open the note that Santa had wrote. / "
            "The words jumped out as to get my attention. / "
            "And there was one thing he told me to mention."
        ),
        "right": (
            "More than cakes, cocoa or milk. / "
            "Shirts made of cotton or ties made of silk. / "
            "Hats, stockings or a new coat. / "
            "What he wants is simply a note."
        ),
        "right_kind": "poem",
        "title": "S11 Wish",
    },'''
    new = '''    "S11-wish": {
        "unit": "S11-wish",
        "layout": "text_image",
        "left_page": 24,
        "right_page": 25,
        "left": (
            "I tore open the note that Santa had wrote. / "
            "The words jumped out as to get my attention. / "
            "And there was one thing he told me to mention. / "
            "More than cakes, cocoa or milk. / "
            "Shirts made of cotton or ties made of silk. / "
            "Hats, stockings or a new coat. / "
            "What he wants is simply a note."
        ),
        "right": "IMAGE ONLY — boy with glowing letter · silent beat lands the final line.",
        "right_kind": "context",
        "title": "S11 Wish",
    },'''
    if old not in text:
        if '"layout": "text_image"' in text and "S11-wish" in text:
            print("poem map S11 already updated")
            return
        raise SystemExit("S11 poem map block not found for replace")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print("poem map S11 → text_image")


def write_recipe(folder: Path, version: str, title: str, notes: str, url: str, seed: object, refs: list[Path]) -> None:
    (folder / version / "RECIPE.md").write_text(
        f"""# RECIPE — {folder.name} / {version}

| Field | Value |
|-------|--------|
| **name** | {title} |
| **layout** | FULL SPREAD seamless |
| **version** | {version} |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | {", ".join(p.name for p in refs)} |

## Intent

{notes}
""",
        encoding="utf-8",
    )
    (folder / version / "meta.json").write_text(
        json.dumps(
            {
                "version": version,
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


def gen_s12a(root: dict) -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    park_old(S12A, "pre-v01-qwen")
    refs = [S11 / "art.png", BLESS_REF if BLESS_REF.is_file() else S8L, BOY]
    final, url, seed = qwen_spread(PROMPT_S12A, refs, S12A, "v01")
    write_recipe(
        S12A,
        "v01",
        "S12a Blessing — sleigh departure window + wide room boy reading",
        "L: night window + distant sleigh departure. R: wide peaceful room, boy small with letter.",
        url,
        seed,
        refs,
    )
    seamless_board(
        final,
        INDEX / f"S12a-blessing-v01-spread-{DAY}.png",
        unit="S12a-blessing",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · S11 continuity · sleigh departure",
        subtitle="Window+sleigh L · wide room boy reading R · image-only R",
    )
    plate(root, "p26").update(
        {
            "caption": "p26 · S12a Blessing L · v01 window+sleigh",
            "path": "Media/development/S12a-blessing/art-left.png",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "working",
            "date": DAY,
            "notes": "Night window · sleigh+reindeer departure outside · poem text L",
            "development_path": "Media/development/S12a-blessing/art.png",
            "pixel_size": "2625x2625",
            "spread_side": "L",
        }
    )
    plate(root, "p26").pop("source_mock", None)
    plate(root, "p27").update(
        {
            "caption": "p27 · S12a Blessing R · v01 wide room",
            "path": "Media/development/S12a-blessing/art-right.png",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "working",
            "date": DAY,
            "notes": "IMAGE ONLY · boy small with letter · wide peaceful room",
            "development_path": "Media/development/S12a-blessing/art.png",
            "pixel_size": "2625x2625",
            "spread_side": "R",
            "text_role": "none",
        }
    )
    plate(root, "p27").pop("source_mock", None)
    verdict(root, "26|27").update(
        {
            "page": "26|27",
            "beat": "S12a Blessing",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "working",
            "decided_by": "Jon",
            "date": DAY,
            "notes": "Seamless · sleigh outside L · boy reading wide R · board S12a-blessing-v01-spread-2026-07-23.png",
        }
    )
    print("S12a FLOW OK")


def gen_s12b(root: dict) -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    park_old(S12B, "pre-v01-qwen")
    house = HOUSE if HOUSE.is_file() else HOUSE2
    refs = [house, STYLE, SANTA]
    final, url, seed = qwen_spread(PROMPT_S12B, refs, S12B, "v01")
    write_recipe(
        S12B,
        "v01",
        "S12b God Bless — Santa past moon + snowman / North Star",
        "L: Santa past moon over house. R: snowman lawn + North Star. gpt_pillar still true — Qwen dial for Jon eye.",
        url,
        seed,
        refs,
    )
    seamless_board(
        final,
        INDEX / f"S12b-god-bless-v01-spread-{DAY}.png",
        unit="S12b-god-bless",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · house+style+santa · gpt_pillar dial",
        subtitle="Santa past moon L · snowman + North Star R",
    )
    plate(root, "p28").update(
        {
            "caption": "p28 · S12b God Bless L · v01 moon+sleigh",
            "path": "Media/development/S12b-god-bless/art-left.png",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "working",
            "date": DAY,
            "notes": "Santa past moon over decorative house · gpt_pillar · Qwen dial (hero GPT later if needed)",
            "development_path": "Media/development/S12b-god-bless/art.png",
            "pixel_size": "2625x2625",
            "spread_side": "L",
            "gpt_pillar": True,
        }
    )
    plate(root, "p28").pop("source_mock", None)
    plate(root, "p29").update(
        {
            "caption": "p29 · S12b God Bless R · v01 snowman+star",
            "path": "Media/development/S12b-god-bless/art-right.png",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "working",
            "date": DAY,
            "notes": "Snowman front lawn · North Star · continuous house · gpt_pillar",
            "development_path": "Media/development/S12b-god-bless/art.png",
            "pixel_size": "2625x2625",
            "spread_side": "R",
            "gpt_pillar": True,
        }
    )
    plate(root, "p29").pop("source_mock", None)
    verdict(root, "28|29").update(
        {
            "page": "28|29",
            "beat": "S12b God Bless",
            "version": "v01",
            "model": "Qwen 2 Pro /edit v06 · 5250×2625",
            "status": "working",
            "decided_by": "Jon",
            "date": DAY,
            "notes": "Seamless exterior · moon+sleigh L · snowman+North Star R · gpt_pillar · board S12b-god-bless-v01-spread-2026-07-23.png",
        }
    )
    print("S12b FLOW OK")


def update_continue() -> None:
    cont = ROOT / ".cursor/docs/CONTINUE-HERE.md"
    if not cont.is_file():
        return
    t = cont.read_text(encoding="utf-8")
    t2 = re.sub(
        r"## One-line status \(2026-07-23\)\n\n[\s\S]*?(?=\n---)",
        "## One-line status (2026-07-23)\n\n"
        "**S11 Wish v01 LOCKED** (TEXT+IMAGE de facto) · **S12a + S12b v01** dials ready  \n"
        "**S10 Note** KEEP · **S9** KEEP · **S8 v09** KEEP · **S3 v07** quality bar  \n"
        "**SoT:** `_FLOW-CURRENT.json` · **NEXT:** Jon eye on S12a Blessing + S12b God Bless (final spreads).\n",
        t,
        count=1,
    )
    cont.write_text(t2, encoding="utf-8")


def main() -> None:
    load_env()
    INDEX.mkdir(parents=True, exist_ok=True)
    update_poem_map_s11()
    root = load_flow()
    promote_s11(root)
    save_flow(root)

    root = load_flow()
    gen_s12a(root)
    save_flow(root)

    root = load_flow()
    gen_s12b(root)
    save_flow(root)

    update_continue()
    print("DONE")


if __name__ == "__main__":
    main()
