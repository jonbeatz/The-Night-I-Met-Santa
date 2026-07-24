#!/usr/bin/env python3
"""S12-god-bless v19 — v18b look + exactly 9 (4 pairs+Rudolph) · smaller Santa · star · over house."""
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

V18B = OUT / "v18b" / "art.png"
V17 = OUT / "v17" / "art.png"  # nine-deer count / path hint

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit IMAGE 1 into the final Christmas spread. Keep IMAGE 1's LOOK — chuckling open-coat Santa,
ornate red/gold sleigh, same reindeer paint style, house/snowman/lamp, vignette, oil quality.
Wide ~2:1. NO baked text.

IMAGE 2 = nine-deer formation reference only (count + path). Do not copy IMAGE 2's Santa face.

MANDATORY CHANGES:
1) Exactly NINE reindeer. Formation: FOUR ROWS OF TWO (four pairs side-by-side) plus Rudolph
   alone at the very FRONT. Count heads: 1-2-3-4-5-6-7-8-9. All IN FRONT of the sleigh,
   harnessed, PULLING. Sleigh behind. Keep IMAGE 1 reindeer LOOK (fur/antlers).
   ONLY Rudolph (frontmost) faint soft red nose. All other noses brown.

2) Make Santa and the sleigh a LITTLE SMALLER so the team and sky have room.

3) Big gleaming North Star TOP-RIGHT — warm golden-yellow with strong cross rays and halo.
   Clear open dark sky BELOW the star for text. Do not cover the star.

4) Flight path: the team flies TOWARD the Victorian house as if they will fly OVER it
   (descending curve toward lower-right house). Moon still behind/near Santa on the left.

Keep flying (clear air under hooves). Cream vignette all sides. NO text. NO duplicate Santa.
"""

NEG = (
    "only 6 reindeer, only 7, only 8, five reindeer, six reindeer, "
    "reindeer behind sleigh, huge Santa, oversized sleigh, tiny North Star, "
    "missing North Star, covering North Star, two glowing noses, "
    "reindeer on ground, text, God bless, letters"
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
    for p in (V18B, V17):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(V18B).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp18 = OUT / "_tmp-v19-v18b.png"
    base.save(tmp18)
    ref = Image.open(V17).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp17 = OUT / "_tmp-v19-v17.png"
    ref.save(tmp17)

    urls = [
        fal_client.upload_file(str(tmp18)),
        fal_client.upload_file(str(tmp17)),
    ]
    print("=== Qwen S12-god-bless v19 · 9 deer (4 pairs+Rudolph) ===")
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
    tmp_q = OUT / "_tmp-v19-qwen.png"
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

    for t in (tmp18, tmp17, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v19"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    w, h = final.size
    final.crop((int(w * 0.08), int(h * 0.05), int(w * 0.95), int(h * 0.62))).resize(
        (1800, 700), Image.Resampling.LANCZOS
    ).save(vdir / "_flight-crop.png")

    recipe = f"""# RECIPE — S12-god-bless / v19

| Field | Value |
|-------|--------|
| **version** | **v19** |
| **date** | {DAY} |
| **base** | v18b look |
| **formation** | 4 pairs + Rudolph = 9 · v17 count hint |
| **also** | smaller Santa/sleigh · big North Star · path over house |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v19",
                "status": "working",
                "base": "v18b",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v19", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v19-final-{DAY}.png",
        unit="S12-god-bless",
        version="v19",
        day=DAY,
        tech="Qwen 2 Pro /edit · v18b + 4 pairs + Rudolph · smaller Santa · star · over house",
        subtitle="Nine ahead · Rudolph faint only · gleaming North Star top-right",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v19 · v18b look · 9=4 pairs+Rudolph · smaller Santa · over house · "
        "board S12-god-bless-v19-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v19",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v19",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v19", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v19", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v19", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
