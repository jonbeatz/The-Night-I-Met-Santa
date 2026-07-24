#!/usr/bin/env python3
"""S12-god-bless v14 — v06 look/feel + v13b pull direction (9 ahead, Rudolph only)."""
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

V06 = OUT / "v06" / "art.png"  # look / feel / Santa / sleigh / reindeer paint
V13B = OUT / "v13b" / "art.png"  # direction — team ahead toward house
FACE = ROOT / "Images/styles1/santa-G0-face.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Create one Christmas night storybook spread by COMBINING two versions. Wide ~2:1. NO TEXT.

IMAGE 1 = DIRECTION LOCK (v13b): Keep this COMPOSITION PATH only.
Reindeer are IN FRONT of the sleigh PULLING it toward the Victorian house (lower-right).
Sleigh is BEHIND the whole team. Clean curved harnessed formation. Do NOT put any deer
behind the sleigh. Do NOT scatter deer on the moon. Keep moon left, North Star right with
open sky below, house/snowman/lamp/evergreens, cream vignette all sides.

IMAGE 2 = LOOK & FEEL LOCK (v06): Restyle to match v06 art quality — rich painterly
atmosphere, Santa face and body, ornate red gold sleigh with presents, and especially the
reindeer PAINT STYLE from v06 (best fur, antlers, warmth). Santa eyes OPEN looking back
toward us with a warm gentle smile. Match v06 color richness and brushwork.

IMAGE 3 = Santa G0 face lock — warm smile, open eyes, rosy cheeks, full soft beard.

REINDEER RULE (must obey):
- Exactly NINE reindeer: 4 pairs + Rudolph leading solo at the front. COUNT them.
- All nine AHEAD of the sleigh, harnessed, pulling like horses pull a carriage.
- ONLY Rudolph (front, farthest) has a faint soft red nose glow. NO other nose glow.
- Use v06 reindeer LOOK painted into the v13b pull DIRECTION.

Keep deep blue sky. NO baked text. NO duplicate Santa. NO boy.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, deer on the moon, "
    "scattered reindeer, only 8 reindeer, 10 reindeer, 11 reindeer, "
    "two glowing noses, three glowing noses, laser nose, neon nose, "
    "eyes closed, text, God bless, letters, watermark, boy, duplicate Santa"
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
    for p in (V06, V13B, FACE):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Start FROM v13b so pull-ahead direction is baked into the canvas
    base = Image.open(V13B).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp13 = OUT / "_tmp-v14-v13b.png"
    base.save(tmp13)
    style = Image.open(V06).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp06 = OUT / "_tmp-v14-v06.png"
    style.save(tmp06)

    urls = [
        fal_client.upload_file(str(tmp13)),
        fal_client.upload_file(str(tmp06)),
        fal_client.upload_file(str(FACE)),
    ]
    print("=== Qwen S12-god-bless v14 · v06 look + v13b direction ===")
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
    tmp_q = OUT / "_tmp-v14-qwen.png"
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

    for t in (tmp13, tmp06, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v14"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v14

| Field | Value |
|-------|--------|
| **version** | **v14** |
| **date** | {DAY} |
| **look** | Media/development/S12-god-bless/v06 (Santa, sleigh, reindeer paint, atmosphere) |
| **direction** | Media/development/S12-god-bless/v13b (9 ahead pulling toward house) |
| **face** | Images/styles1/santa-G0-face.png |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v14",
                "status": "working",
                "look": "v06",
                "direction": "v13b",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v14", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v14-final-{DAY}.png",
        unit="S12-god-bless",
        version="v14",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · v06 look + v13b direction · 9 ahead · Rudolph only",
        subtitle="Best of v06 paint on v13b pull path toward house",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v14 · v06 look/feel + v13b direction · 9 harnessed ahead · "
        "Rudolph faint only · board S12-god-bless-v14-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v14",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v14",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v14", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v14", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v14", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
