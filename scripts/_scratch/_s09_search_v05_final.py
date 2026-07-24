#!/usr/bin/env python3
"""S9 Search v05 FINAL — character-close search + chair-back-to-fireplace discovery."""
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
V05 = UNIT / "v05"
P20 = V05 / "p20"
P21 = V05 / "p21"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
POSTURE1 = ROOT / "Images/styles2/page-10-the-search.png"
POSTURE2 = ROOT / "Images/styles2/p19-beat10-the-search2.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
V04_P21 = UNIT / "v04" / "p21" / "art.png"
V04_P20 = UNIT / "v04" / "p20" / "art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (2625, 2625)
DAY = "2026-07-23"

PROMPT_P20 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 v07 (image 3).

IMAGE 1 = TWO POSTURE REFERENCES (side-by-side strip) — match search posture + LOW CAMERA ANGLE \
exactly: hands and knees / crouching among gifts, kid-level camera.

IMAGE 2 = Boy G0 CHARACTER LOCK — oatmeal/taupe holly pajamas with green holly leaves and red \
berries, red trim on collar/cuffs/hems, tousled light-brown hair, large brown eyes, rosy cheeks. \
NOT blue PJs, NOT polka dots, NOT stripes.

COMPOSITION — p20 CHARACTER SHOT (critical):
The boy FILLS THE FRAME — large in the composition, close to camera, low angle at his level. \
We see HIM first, the room second. This is a CHARACTER shot, not a room establishing shot. \
He is on hands and knees among scattered wrapped gifts, actively searching / looking around.

Background SECONDARY only: Christmas tree with warm lights; fireplace with DYING EMBERS and soft \
wispy smoke ONLY inside the fireplace opening. Wooden chair with folded cream note PARTIALLY \
visible in the background near the fireplace — chair BACK faces toward the fireplace. Burgundy \
walls. Soft watercolor vignette dissolve to cream edges.

HARD RULE: NO fire, flames, or embers anywhere except INSIDE the fireplace. No floating sparks, \
no flame effects on gifts or floor.

NO Santa. NO baked text/letters.
"""

PROMPT_P21 = """\
Square children's book page 2625x2625. Rich oil-painting quality matching S3 finish.

IMAGE 1 = discovery plate base — keep close-up wooden chair + note + side table language, burgundy \
room, tree peeking at right edge, dying fireplace.

IMAGE 2 = STANDARD FRAME vignette to cream edges.
IMAGE 3 = quality bar.

COMPOSITION — p21 DISCOVERY CLOSE-UP:
Wooden chair near the fireplace — turned so the BACK of the chair faces the fireplace (seat faces \
away from hearth toward the room). Folded cream note on the seat catches a subtle glow (moonlight \
or firelight on the edge). Small wooden side table: white cocoa cup with steam + half-eaten cookie \
on a plate. Window with snow, full moon, and soft MOONLIGHT STREAKS spilling onto the floor. \
Christmas tree partially visible at the RIGHT edge only. Dying embers with soft smoke INSIDE \
fireplace only. Burgundy walls, patterned rug, a few gifts in foreground.

Same chair orientation as the search page (back toward fireplace). NO boy. NO Santa. NO baked text. \
NO fire/flames/embers outside the fireplace.
"""

NEG = (
    "text, letters, typography, watermark, readable writing, "
    "Santa Claus, blue pajamas, polka dot pajamas, striped pajamas, "
    "wide empty room shot, tiny distant boy, roaring fire, bright flames outside fireplace, "
    "embers on floor, floating sparks, hard border, geometric frame"
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


def posture_strip() -> Path:
    a = Image.open(POSTURE1).convert("RGB")
    b = Image.open(POSTURE2).convert("RGB")
    h = 1024
    a = a.resize((int(a.width * h / a.height), h), Image.Resampling.LANCZOS)
    b = b.resize((int(b.width * h / b.height), h), Image.Resampling.LANCZOS)
    strip = Image.new("RGB", (a.width + b.width + 12, h), (252, 248, 240))
    strip.paste(a, (0, 0))
    strip.paste(b, (a.width + 12, 0))
    out = UNIT / "_tmp-v05-posture-strip.png"
    strip.save(out)
    return out


def write_meta(out_dir: Path, page_id: str, label: str, seed, url: str, intent: str, refs: list[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / {page_id} / v05

| Field | Value |
|-------|--------|
| **name** | S9 Search — {label} |
| **unit** | S09-search |
| **book page** | Flow v2 {page_id} SPLIT |
| **version** | **v05** |
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
                "version": "v05",
                "status": "working",
                "lock_candidate": True,
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
    final = upscale(raw, UNIT / f"_tmp-{page_id}-v05-qwen.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    final.save(out_dir / "art.png", optimize=True)
    write_meta(
        out_dir,
        page_id,
        label,
        seed,
        url,
        intent,
        [str(p.relative_to(ROOT)).replace("\\", "/") if p.is_relative_to(ROOT) else p.name for p in refs],
    )
    return final


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import split_board  # type: ignore

    for p in (POSTURE1, POSTURE2, BOY, S3, FRAME, V04_P21):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    strip = posture_strip()

    # Character-first: posture strip + Boy G0 + S3 quality (room described; avoid room plate dominating)
    p20 = gen(
        P20,
        "p20",
        PROMPT_P20,
        [strip, BOY, S3],
        "boy fills frame · low-angle search · holly PJs",
        "Character shot: boy large/close; posture from both styles2 search refs; chair+note secondary bg.",
    )

    p21 = gen(
        P21,
        "p21",
        PROMPT_P21,
        [V04_P21, FRAME, S3],
        "chair back to fireplace · note glow · moonlight streaks · cookie",
        "Discovery close-up; chair oriented back-to-fireplace; moonlight streaks; cookie+cocoa.",
    )

    strip.unlink(missing_ok=True)

    (V05 / "RECIPE.md").write_text(
        f"""# RECIPE — S09-search / v05 (SPLIT FINAL candidate)

| Page | Path | Role |
|------|------|------|
| **p20** | `v05/p20/art.png` | Boy fills frame · hands/knees · low angle |
| **p21** | `v05/p21/art.png` | Chair back→fireplace · note · cookie · moonlight streaks |

**Posture:** `page-10-the-search.png` + `p19-beat10-the-search2.png`  
**{DAY}** · 2625² · Qwen v06 · promote on Jon OK
""",
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    out = INDEX / f"S09-search-v05-split-{DAY}.png"
    split_board(
        p20,
        p21,
        out,
        unit="S09-search",
        version="v05",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 2625×2625 SPLIT · character-close search · chair discovery",
        subtitle="p20 boy fills frame · p21 chair back to fireplace · FINAL candidate",
        side=700,
    )
    print("BOARD", out)


if __name__ == "__main__":
    main()
