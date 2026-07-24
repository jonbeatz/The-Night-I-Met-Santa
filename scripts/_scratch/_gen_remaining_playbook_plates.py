#!/usr/bin/env python3
"""Generate playbook gaps: back cover, pastedown, p34–36 + Cover/P01 print-scale.

Uses Qwen 2 Pro /edit for illustrated plates. Pillow for solid burgundy + blank.
SeedVR → 2625 for Cover + P01 review plates (does NOT overwrite KEEP art.png).
"""
from __future__ import annotations

import io
import json
import os
import urllib.request
from datetime import date
from pathlib import Path

import fal_client
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
COVER = ROOT / "Media/development/Cover/art.png"
P01 = ROOT / "Media/development/P01-title/art.png"
P30 = ROOT / "Media/development/P-thank-you/art.png"
QUIET_R = ROOT / "Media/development/P-quiet-close/art-right.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
PAGE = 2625
CREAM = (252, 246, 238)
# Deep burgundy sampled from style-lock wall family (AGENT-RUNBOOK pastedown)
BURGUNDY = (90, 22, 18)
DAY = date.today().isoformat()
NEG = (
    "text, letters, words, title, ISBN barcode, watermark, logo, signature, "
    "photoreal photo, CGI, 3D render, book mockup, 3D book, hardcover prop, "
    "readable typography, caption, blurb text"
)

BACK_PROMPT = """\
Back cover art for a children's Christmas picture book — flat poster square ONLY
(not a 3D book mockup). Painted gouache / soft watercolor heirloom storybook quality.

IMAGE 1 = FRONT COVER keep — match the SAME night street mood, palette, snow, warm
window glow, and paint language. Companion scene, not a clone of the front.

IMAGE 2 = style-lock paint atmosphere — rich gouache warmth (Santore-adjacent).

COMPOSITION:
- Soft snowy Christmas Eve street or quiet night vignette continuing the cover world.
- Large soft EMPTY region in the CENTER or LOWER half (snowdrift / soft sky / quiet wall)
  for later ISBN + short blurb type in InDesign — do NOT paint any letters.
- Soft empty band near the BOTTOM for small credit line later.
- No large hero faces dominating; atmospheric and calm.
- Flat illustration filling the square — never a photographed book or 3D cover wrap.
- NO letters, NO words, NO barcode, NO watermark.

Output: square Christmas storybook back-cover illustration, print-ready composition.
"""

P34_PROMPT = """\
Optional quiet closing page (padding) for a children's Christmas picture book.
Single square plate. Painted gouache / soft watercolor.

IMAGE 1 = quiet-close ornament / mantel mood reference — match calm glow and paint feel.
IMAGE 2 = style-lock atmosphere.
IMAGE 3 = cream watercolor FRAME language — soft irregular cream vignette at edges (FRAME ON).

COMPOSITION:
- A single golden glass Christmas ornament (or soft holly + candle glow) as a gentle hero,
  hanging or resting quietly — intimate, peaceful, gift-book closing mood.
- Generous soft cream watercolor paper around the subject; edges dissolve to cream.
- Open quiet space for optional tiny type later — do NOT paint text.
- NO letters, NO words, NO watermark, NO logos.
- Not clip-art stickers; atmospheric depth, warm/cool light, painted soft edges.

Output: square FRAME ON quiet ornament plate.
"""

P35_PROMPT = """\
Colophon / reprint-note page art for a children's Christmas picture book.
Single square plate. Almost blank soft cream watercolor paper.

IMAGE 1 = Thank You cream paper page — match this exact paper cream, soft vignette,
and quiet matter-page language.
IMAGE 2 = style-lock warmth (subtle only).
IMAGE 3 = cream FRAME language.

COMPOSITION:
- Soft cream / warm parchment watercolor wash filling the page.
- Very subtle painted vignette / edge dissolve to cream (FRAME ON).
- Almost empty center — large open zone for tiny colophon type in InDesign.
- At most a whisper of holly leaf or soft snow sparkle in a FAR corner — optional, tiny.
- NO letters, NO words, NO watermark, NO logos, NO busy scene.

Output: square quiet colophon paper plate, FRAME ON.
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


def download(url: str, tries: int = 4) -> Image.Image:
    last: Exception | None = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as resp:
                return Image.open(io.BytesIO(resp.read())).convert("RGB")
        except Exception as e:  # noqa: BLE001
            last = e
            print("retry", i, e)
    assert last is not None
    raise last


def prep_square(src: Path, dest: Path, side: int = 1536, bg=CREAM) -> Path:
    im = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (side, side), bg)
    scale = min(side / im.width, side / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(im2, ((side - nw) // 2, (side - nh) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest)
    return dest


def qwen_edit(prompt: str, ref_paths: list[Path], out_path: Path) -> tuple[Image.Image, object]:
    load_env()
    urls = [fal_client.upload_file(str(p)) for p in ref_paths]
    print(f"=== Qwen 2 Pro /edit -> {out_path.relative_to(ROOT)} ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": prompt,
            "negative_prompt": NEG,
            "image_urls": urls,
            "image_size": {"width": 2048, "height": 2048},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": False,
        },
        with_logs=True,
    )
    seed = result.get("seed")
    art = download(result["images"][0]["url"]).resize((PAGE, PAGE), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    art.save(out_path, "PNG")
    print("saved", out_path, art.size, "seed", seed)
    return art, seed


def seedvr_square(src: Path, dest: Path, factor: float) -> Image.Image:
    load_env()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_tmp-seedvr-{dest.stem}.png"
    Image.open(src).convert("RGB").save(tmp)
    print(f"=== SeedVR x{factor} -> {dest.relative_to(ROOT)} ===")
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": fal_client.upload_file(str(tmp)),
            "upscale_mode": "factor",
            "upscale_factor": factor,
            "noise_scale": 0.08,
            "output_format": "png",
        },
        with_logs=True,
    )
    u = up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"]
    out = download(u).resize((PAGE, PAGE), Image.Resampling.LANCZOS)
    out.save(dest, "PNG")
    tmp.unlink(missing_ok=True)
    print("saved", dest, out.size)
    return out


def solid_burgundy(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (PAGE, PAGE), BURGUNDY).save(dest, "PNG")
    print("saved pastedown", dest, BURGUNDY)


def blank_cream(dest: Path, soft_vignette: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", (PAGE, PAGE), CREAM)
    if soft_vignette:
        # Very subtle edge darken for printer blank that still feels like paper
        overlay = Image.new("RGB", (PAGE, PAGE), (245, 238, 228))
        mask = Image.new("L", (PAGE, PAGE), 0)
        d = ImageDraw.Draw(mask)
        pad = int(PAGE * 0.04)
        d.ellipse([pad, pad, PAGE - pad, PAGE - pad], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=int(PAGE * 0.08)))
        im = Image.composite(im, overlay, mask)
    im.save(dest, "PNG")
    print("saved blank", dest)


def write_recipe(unit: str, ver: str, path: Path, seed: object, model: str, prompt: str) -> None:
    recipe = path.parent / "RECIPE.md"
    recipe.write_text(
        f"""# RECIPE — {unit} / {ver}

| Field | Value |
|-------|--------|
| **name** | {unit} — remaining playbook plate |
| **unit** | {unit} |
| **version** | {ver} |
| **date** | {DAY} |
| **lane** | Development mock |
| **service** | fal.ai / Pillow |
| **model** | `{model}` |
| **size** | 2625×2625 |
| **seed** | {seed} |
| **FRAME** | ON for matter; N/A cover wrap |
| **verdict** | pending — Jon review |
| **status** | working |
| **output** | `{path.relative_to(ROOT).as_posix()}` |

## Prompt

{prompt}

## Negative

{NEG}
""",
        encoding="utf-8",
    )


def upsert_flow_plates(new_plates: list[dict]) -> None:
    data = json.loads(FLOW.read_text(encoding="utf-8"))
    by_id = {p["id"]: i for i, p in enumerate(data["plates"])}
    for plate in new_plates:
        if plate["id"] in by_id:
            data["plates"][by_id[plate["id"]]] = plate
        else:
            data["plates"].append(plate)
    data["updated"] = DAY
    data["notes_session"] = (
        "Playbook gaps: back cover · pastedown burgundy · p34–36 working plates + "
        "Cover/P01 art-2625 print-scale (KEEP art.png untouched)"
    )
    FLOW.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("FLOW updated")


def main() -> None:
    load_env()
    tmp = ROOT / "Media/generated/mocks/_tmp-remaining"
    tmp.mkdir(parents=True, exist_ok=True)

    # --- 1) Back cover (Qwen) ---
    mock_back = ROOT / "Media/generated/mocks/Cover-back/v01"
    dev_back = ROOT / "Media/development/Cover/art-back.png"
    cover_ref = prep_square(COVER, tmp / "cover.png")
    style_ref = prep_square(STYLE, tmp / "style.png")
    art_back, seed_back = qwen_edit(BACK_PROMPT, [cover_ref, style_ref], mock_back / "art.png")
    dev_back.parent.mkdir(parents=True, exist_ok=True)
    art_back.save(dev_back, "PNG")
    write_recipe("Cover-back", "v01", mock_back / "art.png", seed_back, QWEN, BACK_PROMPT)

    # --- 2) Casewrap pastedown (Pillow solid) ---
    mock_paste = ROOT / "Media/generated/mocks/Cover-pastedown/v01/art.png"
    dev_paste = ROOT / "Media/development/Cover/pastedown-burgundy.png"
    solid_burgundy(mock_paste)
    solid_burgundy(dev_paste)
    write_recipe(
        "Cover-pastedown",
        "v01",
        mock_paste,
        "n/a",
        f"Pillow solid RGB{BURGUNDY}",
        "Solid deep burgundy matching style-lock wall family. No illustration.",
    )

    # --- 3) p34 quiet ornament (Qwen) ---
    mock_p34 = ROOT / "Media/generated/mocks/P34-padding/v01"
    dev_p34 = ROOT / "Media/development/P34-padding/art.png"
    quiet_ref = prep_square(QUIET_R, tmp / "quiet-r.png")
    frame_ref = prep_square(FRAME, tmp / "frame.png")
    art_p34, seed_p34 = qwen_edit(
        P34_PROMPT, [quiet_ref, style_ref, frame_ref], mock_p34 / "art.png"
    )
    dev_p34.parent.mkdir(parents=True, exist_ok=True)
    art_p34.save(dev_p34, "PNG")
    write_recipe("P34-padding", "v01", mock_p34 / "art.png", seed_p34, QWEN, P34_PROMPT)

    # --- 4) p35 colophon (Qwen cream) ---
    mock_p35 = ROOT / "Media/generated/mocks/P35-colophon/v01"
    dev_p35 = ROOT / "Media/development/P35-colophon/art.png"
    p30_ref = prep_square(P30, tmp / "p30.png")
    art_p35, seed_p35 = qwen_edit(
        P35_PROMPT, [p30_ref, style_ref, frame_ref], mock_p35 / "art.png"
    )
    dev_p35.parent.mkdir(parents=True, exist_ok=True)
    art_p35.save(dev_p35, "PNG")
    write_recipe("P35-colophon", "v01", mock_p35 / "art.png", seed_p35, QWEN, P35_PROMPT)

    # --- 5) p36 blank (Pillow) ---
    mock_p36 = ROOT / "Media/generated/mocks/P36-blank/v01/art.png"
    dev_p36 = ROOT / "Media/development/P36-blank/art.png"
    blank_cream(mock_p36, soft_vignette=False)
    blank_cream(dev_p36, soft_vignette=False)
    write_recipe(
        "P36-blank",
        "v01",
        mock_p36,
        "n/a",
        f"Pillow solid cream RGB{CREAM}",
        "Final blank — printer-friendly even end. No illustration.",
    )

    # --- 6) Cover + P01 print-scale (SeedVR) — KEEP art.png untouched ---
    cover_2625 = ROOT / "Media/development/Cover/art-2625.png"
    p01_2625 = ROOT / "Media/development/P01-title/art-2625.png"
    mock_cover_print = ROOT / "Media/generated/mocks/Cover-print/v01/art.png"
    mock_p01_print = ROOT / "Media/generated/mocks/P01-print/v01/art.png"
    # 1024×2.56≈2621; 2048×1.28≈2621
    c = seedvr_square(COVER, cover_2625, 2.56)
    c.save(mock_cover_print, "PNG")
    p = seedvr_square(P01, p01_2625, 1.28)
    p.save(mock_p01_print, "PNG")
    write_recipe(
        "Cover-print",
        "v01",
        mock_cover_print,
        "n/a",
        SEEDVR,
        "Print-scale of beige-v2 KEEP — art.png (1024) untouched.",
    )
    write_recipe(
        "P01-print",
        "v01",
        mock_p01_print,
        "n/a",
        SEEDVR,
        "Print-scale of P01 v16 KEEP — art.png (2048) untouched.",
    )

    # --- FLOW entries (optional / wrap extras) ---
    upsert_flow_plates(
        [
            {
                "id": "back-cover",
                "page": "Back",
                "beat": "Back Cover",
                "caption": "Back cover · v01 working (Qwen companion to beige-v2)",
                "path": "Media/development/Cover/art-back.png",
                "version": "v01",
                "model": QWEN,
                "status": "working",
                "decided_by": "pending",
                "date": DAY,
                "notes": "Open center/bottom for ISBN+blurb+credit in InDesign · no baked text",
                "gpt_pillar": False,
                "development_path": "Media/development/Cover/art-back.png",
                "tier": "development",
                "source_mock": "Media/generated/mocks/Cover-back/v01/art.png",
            },
            {
                "id": "pastedown",
                "page": "Casewrap",
                "beat": "Pastedown",
                "caption": "Casewrap pastedown · solid burgundy LOCKED fill",
                "path": "Media/development/Cover/pastedown-burgundy.png",
                "version": "v01",
                "model": f"Pillow RGB{BURGUNDY}",
                "status": "keep",
                "decided_by": "Jon",
                "date": "2026-07-22",
                "notes": "Inside front+back · casewrap only · not interior",
                "gpt_pillar": False,
                "development_path": "Media/development/Cover/pastedown-burgundy.png",
                "tier": "development",
                "source_mock": "Media/generated/mocks/Cover-pastedown/v01/art.png",
            },
            {
                "id": "p34",
                "page": "34",
                "beat": "Padding",
                "caption": "p34 · Optional quiet ornament · v01 working",
                "path": "Media/development/P34-padding/art.png",
                "version": "v01",
                "model": QWEN,
                "status": "working",
                "decided_by": "pending",
                "date": DAY,
                "notes": "Optional padding — cut if trimming · FRAME ON",
                "gpt_pillar": False,
                "development_path": "Media/development/P34-padding/art.png",
                "tier": "development",
                "source_mock": "Media/generated/mocks/P34-padding/v01/art.png",
            },
            {
                "id": "p35",
                "page": "35",
                "beat": "Colophon",
                "caption": "p35 · Optional colophon paper · v01 working",
                "path": "Media/development/P35-colophon/art.png",
                "version": "v01",
                "model": QWEN,
                "status": "working",
                "decided_by": "pending",
                "date": DAY,
                "notes": "Open cream for tiny reprint note · optional",
                "gpt_pillar": False,
                "development_path": "Media/development/P35-colophon/art.png",
                "tier": "development",
                "source_mock": "Media/generated/mocks/P35-colophon/v01/art.png",
            },
            {
                "id": "p36",
                "page": "36",
                "beat": "Blank",
                "caption": "p36 · Final blank cream · v01",
                "path": "Media/development/P36-blank/art.png",
                "version": "v01",
                "model": f"Pillow cream RGB{CREAM}",
                "status": "working",
                "decided_by": "pending",
                "date": DAY,
                "notes": "Printer-friendly even end · optional",
                "gpt_pillar": False,
                "development_path": "Media/development/P36-blank/art.png",
                "tier": "development",
                "source_mock": "Media/generated/mocks/P36-blank/v01/art.png",
            },
        ]
    )

    # Index board for quick look
    idx = ROOT / "Media/generated/mocks/_INDEX"
    idx.mkdir(parents=True, exist_ok=True)
    art_back.save(idx / "remaining-back-cover.png")
    art_p34.save(idx / "remaining-p34.png")
    art_p35.save(idx / "remaining-p35.png")
    Image.open(dev_paste).save(idx / "remaining-pastedown.png")
    Image.open(dev_p36).save(idx / "remaining-p36.png")
    Image.open(cover_2625).save(idx / "remaining-cover-2625.png")
    Image.open(p01_2625).save(idx / "remaining-p01-2625.png")
    print("DONE — review Media/generated/mocks/_INDEX/remaining-*.png")


if __name__ == "__main__":
    main()
