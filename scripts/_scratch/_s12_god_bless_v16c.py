#!/usr/bin/env python3
"""S12-god-bless v16c — PIL raise v15b over moon, then Qwen add 9th deer + clean."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-god-bless"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

V15B = OUT / "v15b" / "art.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
This Christmas spread was shifted upward so Santa/sleigh sit more in front of the moon.
Clean it into a finished illustration. Wide ~2:1. NO TEXT.

KEEP: same look/feel, house, North Star with OPEN dark sky BELOW it for text, vignette,
flying path toward house/star, Santa looking back warm smile eyes open.

FIX:
1) Exactly NINE reindeer harnessed IN FRONT of the sleigh (4 pairs + Rudolph leading).
   Count heads: must be nine. Currently may be eight — ADD one into the curve.
   ONLY Rudolph (front) faint soft red nose. All FLYING with clear air under hooves.
2) Santa head + sleigh clearly overlapping the moon disk (moon behind them as backlight).
3) Heal any seam/stretch artifacts from the upward shift, especially along the lower sky/snow.

NO baked text. NO boy.
"""

NEG = (
    "only 8 reindeer, eight reindeer, seam line, stretched pixels, "
    "reindeer on ground, covering North Star, two glowing noses, text, God bless, letters"
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


def raise_flight(img: Image.Image, shift_frac: float = 0.10) -> Image.Image:
    """Shift whole image content upward; fill bottom from lower snow band (blurred)."""
    w, h = img.size
    shift = int(h * shift_frac)
    out = Image.new("RGB", (w, h))
    # fill bottom gap from snow near house
    band = img.crop((0, h - shift * 2, w, h - shift)).resize((w, shift), Image.Resampling.LANCZOS)
    band = band.filter(ImageFilter.GaussianBlur(radius=2))
    out.paste(band, (0, h - shift))
    out.paste(img, (0, -shift))
    return out


def main() -> None:
    load_env()
    if not V15B.is_file():
        raise SystemExit(f"missing: {V15B}")

    src = Image.open(V15B).convert("RGB")
    raised = raise_flight(src, 0.11)
    # edit at qwen res
    base = raised.resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v16c-raised.png"
    base.save(tmp)
    # also keep full raised for compare
    (OUT / "v16c").mkdir(parents=True, exist_ok=True)
    raised.save(OUT / "v16c" / "_raised-pre-qwen.png", optimize=True)

    urls = [fal_client.upload_file(str(tmp))]
    print("=== Qwen S12-god-bless v16c · PIL raise + 9 deer ===")
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
    tmp_q = OUT / "_tmp-v16c-qwen.png"
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

    for t in (tmp, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v16c"
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v16c

| Field | Value |
|-------|--------|
| **version** | **v16c** |
| **date** | {DAY} |
| **base** | v15b |
| **method** | PIL raise ~11% then Qwen clean + force 9 deer |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v16c",
                "status": "working",
                "base": "v15b",
                "method": "pil_raise_then_qwen",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v16c", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v16c-final-{DAY}.png",
        unit="S12-god-bless",
        version="v16c",
        day=DAY,
        tech="PIL raise v15b + Qwen · 9 deer · moon behind Santa",
        subtitle="Open sky under North Star · Rudolph only",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v16c · v15b raised over moon · 9 deer · star text pocket · "
        "board S12-god-bless-v16c-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v16c",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v16c",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v16c", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v16c", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v16c", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
