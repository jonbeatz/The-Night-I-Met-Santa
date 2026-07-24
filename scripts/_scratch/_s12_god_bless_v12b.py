#!/usr/bin/env python3
"""S12-god-bless v12b — start FROM art11 (direction) + art6 style lock; kill rear deer."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-god-bless"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

ART6 = ROOT / "Images/styles1/art6.png"
ART11 = ROOT / "Images/styles1/art11.png"
FACE = ROOT / "Media/approved/characters/santa-G0-face.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit this Christmas night spread. Keep composition bones of IMAGE 1 (direction canvas).
Wide ~2:1. NO TEXT anywhere.

IMAGE 1 = DIRECTION canvas (art-eleven): KEEP this sleigh angle flying toward the house,
KEEP the reindeer path IN FRONT of the sleigh pulling forward/right toward the house.
ALL reindeer stay AHEAD of the sleigh. ZERO reindeer behind the sleigh. Delete any rear deer.
Dynamic curved team: 4 pairs + Rudolph leading (front, smallest) = exactly NINE. COUNT them.
ONLY Rudolph faint soft red nose. No other nose glow.

IMAGE 2 = PRIMARY STYLE (art-six): Restyle to match this quality — rich painterly oil look,
Santa face warm detailed correctly sized, EYES OPEN looking back toward us with gentle smile
(not squinted shut), best reindeer paint quality, warm yellow North Star with gleaming cross
rays and open dark sky below, Victorian house warm windows, snowman, lamp post, evergreens,
overall atmosphere. Match IMAGE 2 Santa/sleigh quality onto IMAGE 1's correct pull formation.

IMAGE 3 = Santa G0 face lock — soft kind open blue eyes, crow's feet, rosy cheeks, warm smile.

CRITICAL FIXES:
- No deer behind/left of sleigh. Team only in front pulling.
- Santa eyes OPEN looking back (like IMAGE 2), not closed.
- Full moon left, North Star right, cream vignette all sides.
- NO baked text. NO duplicate Santa.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, deer left of sleigh pulling nothing, "
    "eyes closed, squinted shut eyes, only 8 reindeer, two glowing noses, three glowing noses, "
    "laser nose, neon nose, text, God bless, letters, watermark, hard white border, boy"
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


def main() -> None:
    load_env()
    # Start FROM art11 so pull direction is baked into the canvas
    base = Image.open(ART11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v12b-art11.png"
    base.save(tmp11)
    style = Image.open(ART6).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp6 = OUT / "_tmp-v12b-art6.png"
    style.save(tmp6)

    urls = [
        fal_client.upload_file(str(tmp11)),
        fal_client.upload_file(str(tmp6)),
        fal_client.upload_file(str(FACE)),
    ]
    print("=== Qwen S12-god-bless v12b · art11 canvas + art6 style ===")
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
            "enable_prompt_expansion": False,
        },
        with_logs=True,
    )
    print(result)
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    print("qwen", raw.size)
    tmp_q = OUT / "_tmp-v12b-qwen.png"
    raw.save(tmp_q)
    try:
        up = fal_client.subscribe(
            SEEDVR,
            arguments={
                "image_url": fal_client.upload_file(str(tmp_q)),
                "upscale_mode": "factor",
                "upscale_factor": 2,
                "noise_scale": 0.1,
                "output_format": "png",
            },
            with_logs=True,
        )
        u = up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"]
        final = download(u).resize(SPREAD, Image.Resampling.LANCZOS)
        print("seedvr ok")
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    for t in (tmp6, tmp11, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v12b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v12b

| Field | Value |
|-------|--------|
| **version** | **v12b** |
| **date** | {DAY} |
| **canvas** | Images/styles1/art11.png (direction — edit start) |
| **style** | Images/styles1/art6.png (quality/Santa) |
| **face** | santa-G0-face.png |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **note** | v12 kept art6 formation; v12b starts from art11 to lock deer ahead |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v12b",
                "status": "working",
                "canvas": "Images/styles1/art11.png",
                "style_ref": "Images/styles1/art6.png",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v12b", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v12b-final-{DAY}.png",
        unit="S12-god-bless",
        version="v12b",
        day=DAY,
        tech="Qwen 2 Pro /edit · art11 canvas + art6 style · deer ahead lock",
        subtitle="Formation fix pass after v12 · eyes open · Rudolph faint only",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v12b · art11 canvas + art6 style · deer ahead · "
        "board S12-god-bless-v12b-final-2026-07-23.png (v12 kept for compare)"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v12b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v12b",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v12b", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v12b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v12b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
