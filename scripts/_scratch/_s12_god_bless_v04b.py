#!/usr/bin/env python3
"""S12-god-bless v04b — strip baked text · angled flight · 9 reindeer · cream vignette."""
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

# Prefer v03 (no baked text) as composition base; use v04 only for smile/face if needed
BASE = OUT / "v03" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Create a seamless Christmas FINAL STORY IMAGE spread (wide 2:1). Rich oil painting. NO TEXT ANYWHERE.

IMAGE 1 = prior closing scene mood (moon, house, North Star, snow).
IMAGE 2 = Santa G0 v2 — open red coat, striped shirt, warm SMILING face angled toward viewer.
IMAGE 3 = soft cream watercolor vignette frame — soft dissolve to cream/paper, NOT hard white border,
NOT dark navy matte border.

CRITICAL — NO LETTERS / NO WORDS / NO \"God bless\" painted in the sky. Empty sky only under the star.

PERSPECTIVE:
Santa + sleigh CLOSER and LARGER. Flying at an ANGLE from UPPER-LEFT toward the Victorian house in the
LOWER-RIGHT (not a flat horizontal parade). Santa angled toward viewer — face and smile readable.
Reindeer lead AWAY into distance: near Santa = larger; front/lead = smaller. Proper depth.

REINDEER — exactly NINE: four pairs (two-by-two) + Rudolph solo in front (smallest).
Warm brown fur, visible antlers, painted not silhouettes.
Rudolph soft subtle warm red nose glow — NOT laser / NOT neon.

NORTH STAR upper RIGHT — golden-white cross shimmer. OPEN dark blue EMPTY sky below it (text goes later).
HOUSE lower-right LARGER — warm golden windows, snowman scarf, snow evergreens.
MOON left behind Santa — soft glow.
ONE Santa. ONE sleigh. Soft cream vignette dissolve.
"""

NEG = (
    "text, letters, typography, words, God bless, watermark, caption, "
    "hard white border, hard rectangular matte, dark navy hard vignette edge, "
    "duplicate Santa, second sleigh, silhouette reindeer, laser nose, neon nose, "
    "flat horizontal deer parade, only 2 reindeer, only 4 reindeer, boy"
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
    if not BASE.is_file():
        BASE2 = OUT / "art.png"
        base_path = BASE2 if BASE2.is_file() else None
        if not base_path:
            raise SystemExit("missing base")
    else:
        base_path = BASE

    base_in = Image.open(base_path).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_base = OUT / "_tmp-v04b-base.png"
    base_in.save(tmp_base)
    refs = [tmp_base, SANTA]
    if FRAME.is_file():
        refs.append(FRAME)
    urls = [fal_client.upload_file(str(p)) for p in refs]

    print("=== Qwen S12-god-bless v04b (no text, angled, 9 deer) ===")
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
            "enable_prompt_expansion": False,  # avoid model inventing God bless text
        },
        with_logs=True,
    )
    print(result)
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    tmp_q = OUT / "_tmp-v04b-qwen.png"
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
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)
    tmp_base.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v04b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S12-god-bless / v04b

Corrective pass: NO baked text · angled flight · 9 reindeer · cream vignette.

| Field | Value |
|-------|--------|
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **base** | v03 (avoided v04 baked God bless) |
| **prompt_expansion** | off |
""",
        encoding="utf-8",
    )
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v04b",
                "status": "working",
                "no_baked_text": True,
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S12-god-bless",
                "status": "working",
                "version": "v04b",
                "pages": "26|27",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "RECIPE.md").write_text((vdir / "RECIPE.md").read_text(encoding="utf-8"), encoding="utf-8")

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v04b-perspective-{DAY}.png",
        unit="S12-god-bless",
        version="v04b",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · NO baked text · angled · 9 deer · cream vignette",
        subtitle="Upper-L → house lower-R · Rudolph soft nose · open sky under star",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v04b · NO baked text · Santa angled toward house · 9 reindeer+Rudolph · "
        "cream vignette · board S12-god-bless-v04b-perspective-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v04b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v04b",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update(
                {
                    "version": "merged-v04b",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v04b — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v04b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v04b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", seed)


if __name__ == "__main__":
    main()
