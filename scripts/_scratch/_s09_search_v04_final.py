#!/usr/bin/env python3
"""S9 Search v04 FINAL — boy searching (posture refs) + v03 chair discovery + cookie."""
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
V04 = UNIT / "v04"
P20 = V04 / "p20"
P21 = V04 / "p21"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
POSTURE1 = ROOT / "Images/styles2/page-10-the-search.png"
POSTURE2 = ROOT / "Images/styles2/p19-beat10-the-search2.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
V03_P20 = UNIT / "v03" / "p20" / "art.png"
V03_P21 = UNIT / "v03" / "p21" / "art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT_P20 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 finish.

IMAGE 1 = POSTURE + LOW CAMERA LOCK — boy on hands and knees among gifts, searching, low angle \
at his level. Match that crouch / crawl / scanning body language ("where did he go?").

IMAGE 2 = Boy G0 CHARACTER LOCK — oatmeal/taupe holly pajamas with green holly leaves + red berries, \
red trim on collar/cuffs, tousled light-brown hair, large expressive brown eyes, rosy cheeks. NOT \
blue PJs, NOT stripes.

IMAGE 3 = ROOM CONTINUITY from prior S9 plate — burgundy walls, patterned rug, Christmas tree, \
dying embers with soft wispy smoke in fireplace, wrapped gifts on rug. Chair with folded cream note \
visible in the BACKGROUND near the fireplace — he has NOT found it yet (note small in depth, not \
the hero). Standard soft watercolor vignette dissolve to cream edges.

COMPOSITION — p20: The BOY IS the subject. Low camera at kid height. Hands and knees among scattered \
gifts, actively searching / looking around / scanning the room. Chair + folded note in background \
near fireplace (clue waiting). Dark hallway / room continuity OK. Soft golden ambient light.

NO Santa figure. NO baked text, letters, or watermark.
"""

PROMPT_P21 = """\
Square children's book page 2625x2625. Rich oil-painting quality.

IMAGE 1 = KEEP this COMPOSITION — close-up wooden chair centered with folded cream note on the seat; \
small wooden side table with white cocoa cup and saucer + tiny steam; dying embers + soft smoke in \
fireplace; window with snow + full moon; Christmas tree peeking from the RIGHT EDGE only; a few \
wrapped gifts on the rug in the foreground; burgundy walls; patterned rug. Same chair position near \
fireplace as the search page.

IMAGE 2 = STANDARD FRAME TREATMENT — soft watercolor vignette dissolve to cream edges.

IMAGE 3 = quality/oil finish guide.

ENRICH ONLY:
- Add a HALF-EATEN COOKIE on a small plate next to the cocoa — Santa's abandoned snack.
- The cream note catches a subtle glow (firelight or moonlight on its edge) so it feels discovered.
- Keep note blank (no readable writing). NO boy. NO Santa. NO baked text.
"""

NEG = (
    "text, letters, typography, watermark, readable writing on note, "
    "Santa Claus figure, blue pajamas, striped pajamas, roaring bright fire, "
    "hard border, geometric frame, phone, six fingers"
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


def write_meta(out_dir: Path, page_id: str, label: str, seed, url: str, intent: str, refs: list[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / {page_id} / v04

| Field | Value |
|-------|--------|
| **name** | S9 Search — {label} |
| **unit** | S09-search |
| **book page** | Flow v2 {page_id} SPLIT |
| **version** | **v04** |
| **date** | {DAY} |
| **status** | working — FINAL candidate |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **2625×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | {", ".join(refs)} |

## Intent

{intent}
""",
        encoding="utf-8",
    )
    (out_dir / "meta.json").write_text(
        json.dumps(
            {
                "page": page_id,
                "version": "v04",
                "status": "working",
                "lock_candidate": True,
                "layout": "split_single",
                "size": list(TARGET),
                "seed": seed,
                "fal_url": url,
                "refs": refs,
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
    final = upscale(raw, UNIT / f"_tmp-{page_id}-v04-qwen.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    final.save(out_dir / "art.png", optimize=True)
    write_meta(out_dir, page_id, label, seed, url, intent, [str(p.relative_to(ROOT)).replace("\\", "/") for p in refs])
    return final


def make_posture_strip() -> Path:
    """Combine the two search posture refs into one image (Qwen max 3 urls)."""
    a = Image.open(POSTURE1).convert("RGB")
    b = Image.open(POSTURE2).convert("RGB")
    h = 1024
    a = a.resize((int(a.width * h / a.height), h), Image.Resampling.LANCZOS)
    b = b.resize((int(b.width * h / b.height), h), Image.Resampling.LANCZOS)
    strip = Image.new("RGB", (a.width + b.width + 16, h), (252, 248, 240))
    strip.paste(a, (0, 0))
    strip.paste(b, (a.width + 16, 0))
    out = UNIT / "_tmp-v04-posture-strip.png"
    strip.save(out)
    print("posture strip", strip.size, "→", out.name)
    return out


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board  # type: ignore

    for p in (POSTURE1, POSTURE2, BOY, V03_P20, V03_P21, FRAME):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    posture_strip = make_posture_strip()

    p20 = gen(
        P20,
        "p20",
        """\
Square children's book page 2625x2625. Rich oil-painting quality.

IMAGE 1 = TWO POSTURE REFERENCES side-by-side — match the boy's SEARCH POSTURE and LOW CAMERA ANGLE: \
on hands and knees / crouching among gifts, actively looking around, kid-level camera. Body language: \
"where did he go?"

IMAGE 2 = Boy G0 CHARACTER LOCK — oatmeal/taupe holly pajamas with green holly + red berries, red trim \
on collar/cuffs, tousled light-brown hair, large brown eyes, rosy cheeks. NOT blue PJs, NOT stripes.

IMAGE 3 = ROOM CONTINUITY — burgundy walls, patterned rug, Christmas tree, gifts, fireplace with DYING \
EMBERS and soft wispy smoke. Wooden chair with folded cream note visible in the BACKGROUND near the \
fireplace — he has NOT found it yet. Soft watercolor vignette dissolve to cream edges.

The BOY IS the subject in the foreground/midground. Low camera at his level. Searching among scattered \
gifts. NO Santa. NO baked text.
""",
        [posture_strip, BOY, V03_P20],
        "boy hands/knees search · low angle · chair/note in bg",
        "Boy G0 searching; dual posture refs (page-10 + search2 strip); room from v03; note not found yet.",
    )

    p21 = gen(
        P21,
        "p21",
        PROMPT_P21,
        [V03_P21, FRAME, S3 if S3.is_file() else V03_P21],
        "chair close-up · note glow · cookie + cocoa",
        "Keep v03 chair composition; add half-eaten cookie; subtle glow on note; frame vignette.",
    )

    posture_strip.unlink(missing_ok=True)

    (V04 / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / v04 (SPLIT FINAL candidate)

| Page | Path | Role |
|------|------|------|
| **p20** | `v04/p20/art.png` | Boy searching hands/knees · low angle · note in bg |
| **p21** | `v04/p21/art.png` | Chair close-up · note glow · cookie + cocoa |

**Posture refs:** `Images/styles2/page-10-the-search.png` · `Images/styles2/p19-beat10-the-search2.png` (combined strip for Qwen 3-slot)  
**{DAY}** · 2625² · Qwen v06 · promote mirrors on Jon OK
""",
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / f"S09-search-v04-split-{DAY}.png"
    split_board(
        p20,
        p21,
        out,
        unit="S09-search",
        version="v04",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 SPLIT · Boy G0 search · v03 chair + cookie",
        subtitle="p20 low-angle search · p21 discovery close-up · FINAL candidate",
        side=700,
    )
    print("BOARD", out)
    print("P20", P20 / "art.png")
    print("P21", P21 / "art.png")


if __name__ == "__main__":
    main()
