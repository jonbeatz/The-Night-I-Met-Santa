#!/usr/bin/env python3
"""S12-god-bless v13 — REINDEER RULE first; G0 face + open coat; art11 canvas."""
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

ART11 = ROOT / "Images/styles1/art11.png"  # direction canvas — deer ahead (max 3 refs)
FACE = ROOT / "Images/styles1/santa-G0-face.png"
G0V2 = ROOT / "Images/styles1/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Christmas night storybook spread. Wide ~2:1. NO TEXT.

=== RULE #1 — REINDEER HARNESS (MOST IMPORTANT — DO THIS FIRST) ===
The reindeer are HARNESSED in pairs IN FRONT OF the sleigh.
They PULL the sleigh through the sky the way horses pull a carriage.
Harness traces/straps run FROM the reindeer BACK TO the sleigh.
ALL nine reindeer are AHEAD of the sleigh. The sleigh sits BEHIND the entire team.
None scattered. None behind the sleigh. None trailing after. None left of the sled alone.
None silhouetted separately against the moon. One connected team only.
Clean curved formation in pairs, flying toward the house (lower-right).
COUNT EXACTLY NINE: four pairs + Rudolph leading solo at the front (smallest, farthest ahead).
ONLY Rudolph has a faint soft red nose glow. No other nose glow. Count them before finishing.

=== IMAGE ROLES (max 3) ===
IMAGE 1 = DIRECTION canvas: keep sleigh angle flying toward the house; keep team AHEAD
pulling with visible harnesses. Rebuild any wrong deer into the front harness line.
Keep rich painterly night, moon left, North Star right, Victorian house lower-right.
IMAGE 2 = Santa G0 face: warm joyful smile, eyes OPEN, rosy cheeks, crow's feet, full beard.
IMAGE 3 = Santa G0 v2 wardrobe: open red coat, striped shirt, brown suspenders — apply to
Santa in the sleigh. Eyes open LOOKING BACK toward us with a gentle warm smile.

=== SCENE ===
Ornate red sleigh with gold trim, presents piled behind Santa.
Full moon left. North Star right — warm yellow-tinted gleam, long cross rays, open dark sky
below for later lettering. Victorian house lower-right, warm lit windows, snowman, lamp post,
snow evergreens. Deep blue night sky. Soft cream vignette evenly on ALL four sides.
NO baked text. NO duplicate Santa. NO boy.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, deer left of sleigh, "
    "deer silhouetted on the moon, deer orbiting the moon, scattered reindeer, "
    "unharnessed deer, deer flying free, only 8 reindeer, 10 reindeer, "
    "two glowing noses, three glowing noses, laser nose, neon nose, "
    "eyes closed, squinted shut eyes, closed coat only, boy, text, God bless, "
    "letters, watermark, hard white border, duplicate Santa"
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
    for p in (ART11, FACE, G0V2):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Start FROM art11 so pull-ahead is baked into the canvas (max 3 image_urls)
    base = Image.open(ART11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v13-art11.png"
    base.save(tmp11)

    urls = [
        fal_client.upload_file(str(tmp11)),
        fal_client.upload_file(str(FACE)),
        fal_client.upload_file(str(G0V2)),
    ]
    print("=== Qwen S12-god-bless v13 · REINDEER RULE first ===")
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
    tmp_q = OUT / "_tmp-v13-qwen.png"
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

    for t in (tmp11, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v13"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v13

| Field | Value |
|-------|--------|
| **version** | **v13** |
| **date** | {DAY} |
| **priority** | REINDEER RULE — harnessed pairs ahead, sleigh behind |
| **canvas** | Images/styles1/art11.png |
| **face** | Images/styles1/santa-G0-face.png |
| **wardrobe** | Images/styles1/santa-G0-v2.png (open coat) |
| **note** | fal max 3 refs — art6 omitted; art11 carries scene quality |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v13",
                "status": "working",
                "priority": "reindeer_harness_rule",
                "canvas": "Images/styles1/art11.png",
                "face": "Images/styles1/santa-G0-face.png",
                "wardrobe": "Images/styles1/santa-G0-v2.png",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v13", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v13-final-{DAY}.png",
        unit="S12-god-bless",
        version="v13",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · REINDEER RULE · art11 + G0 face + G0 v2 open coat",
        subtitle="9 harnessed ahead · Rudolph faint only · eyes open looking back",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v13 · REINDEER RULE first · 9 harnessed ahead · G0 face + open coat · "
        "board S12-god-bless-v13-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v13",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v13",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v13", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v13", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v13", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
