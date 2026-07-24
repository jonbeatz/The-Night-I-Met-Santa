#!/usr/bin/env python3
"""S12-god-bless v17 — fresh FINAL prompt; v11 scene bones + G0 face/v2."""
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

V11 = OUT / "v11" / "art.png"  # flight / moon / star / house bones
FACE = ROOT / "Images/styles1/santa-G0-face.png"
G0V2 = ROOT / "Images/styles1/santa-G0-v2.png"
S03 = ROOT / "Media/development/S03-eyes-met/v07/art.png"  # style note only in prompt if unused

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
S12 God Bless — FINAL storybook FULL SPREAD. Wide ~2:1. Fresh clear scene. NO baked text.

IMAGE 1 = scene bones (flight path, moon left, North Star right, Victorian house lower-right).
Rebuild cleanly to match the brief below. IMAGE 2 = Santa G0 face lock. IMAGE 3 = Santa G0 v2
wardrobe lock (open coat, striped shirt, suspenders).

A simple, beautiful Christmas Eve scene. Santa Claus flies across the night sky in his sleigh,
pulled by nine reindeer, over a snowy house below. The full moon glows on the left. The North
Star gleams on the right. A snowman stands in the yard. Snow-covered evergreens frame the
peaceful winter landscape.

=== THE REINDEER — MOST IMPORTANT ===
Nine reindeer TOTAL. All nine are HARNESSED TOGETHER as one connected team, every single one
IN FRONT OF the sleigh, PULLING it through the sky. Think of horses pulling a carriage —
the horses lead, the carriage follows. The reindeer lead, the sleigh follows behind.
Arranged: four pairs flying side by side, plus one lead reindeer (Rudolph) at the very front.
The entire team curves gracefully in a dynamic arc across the sky toward the house.
Count before finishing: 1-2-3-4-5-6-7-8-9. All FLYING with clear air under their hooves —
NOT on the ground.
Only Rudolph (the very first one, smallest, at the front) has a FAINT soft red glow on his
nose — barely visible, a subtle warm hint. No other reindeer has any red nose. Brown noses only.

=== SANTA ===
Santa G0 v2 from IMAGE 3 — open red coat with cream striped shirt visible underneath, brown
suspenders over the shirt. Warm kind grandfatherly face from IMAGE 2 — soft eyes with laugh
lines, rosy cheeks, gentle smile. Eyes OPEN, looking back toward us / the viewer with warmth.
Sitting in an ornate red sleigh with gold decorative trim. Sleigh filled with wrapped presents
in reds, greens, and golds. A small lantern hangs from the sleigh with a warm golden glow.
Raise Santa and sleigh so the full moon sits partly BEHIND them as a soft backlight.

=== SKY ===
Deep blue night sky. Full moon on the LEFT — large, luminous. North Star on the RIGHT —
bright golden-yellow gleam with soft shimmering cross-shaped rays and a gentle halo.
CLEAR OPEN dark blue sky directly BELOW the star for later \"God bless\" text — unobstructed.
Do not cover the star with reindeer.

=== GROUND ===
Victorian house lower-right — larger and prominent. Warm golden-yellow light from multiple
windows. Snow on the roof. Snowman with a scarf in the front yard. Snow-covered evergreens.
Traditional lamp post near the house with a warm glow. Rolling snowy hills. Simple, peaceful.

=== STYLE ===
Rich oil-painting quality like S3 eyes-met v07 — warm painterly storybook. Soft watercolor
vignette dissolving to cream evenly on ALL four sides. NO baked text. NO duplicate Santa or
sleigh. ONE continuous painted scene.
"""

NEG = (
    "reindeer on the ground, walking on snow, reindeer behind the sleigh, "
    "only 8 reindeer, only 7 reindeer, 10 reindeer, scattered reindeer, "
    "two glowing noses, three glowing noses, laser nose, neon nose, bright red nose, "
    "eyes closed, closed coat only, covering North Star, text, God bless, letters, "
    "duplicate Santa, boy, hard white border"
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
    for p in (V11, FACE, G0V2):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")
    if not S03.is_file():
        print("note: S03 v07 missing for style mention only — continuing")

    base = Image.open(V11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v17-base.png"
    base.save(tmp)

    urls = [
        fal_client.upload_file(str(tmp)),
        fal_client.upload_file(str(FACE)),
        fal_client.upload_file(str(G0V2)),
    ]
    print("=== Qwen S12-god-bless v17 · fresh FINAL prompt ===")
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
    tmp_q = OUT / "_tmp-v17-qwen.png"
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

    vdir = OUT / "v17"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    # flight crop for count review
    w, h = final.size
    final.crop((int(w * 0.12), int(h * 0.08), int(w * 0.90), int(h * 0.58))).resize(
        (1800, 650), Image.Resampling.LANCZOS
    ).save(vdir / "_flight-crop.png")

    recipe = f"""# RECIPE — S12-god-bless / v17

| Field | Value |
|-------|--------|
| **version** | **v17** |
| **date** | {DAY} |
| **prompt** | Fresh FINAL operator brief (reindeer rule first) |
| **canvas** | v11 scene bones |
| **face** | Images/styles1/santa-G0-face.png |
| **wardrobe** | Images/styles1/santa-G0-v2.png |
| **style note** | S03-eyes-met/v07 oil quality (prompt) |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v17",
                "status": "working",
                "canvas": "v11",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v17", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v17-final-{DAY}.png",
        unit="S12-god-bless",
        version="v17",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · fresh FINAL prompt · v11 + G0 face/v2",
        subtitle="9 harnessed ahead · Rudolph faint · moon L · star text pocket R",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v17 · fresh FINAL prompt · 9 ahead · G0 open coat · "
        "board S12-god-bless-v17-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v17",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v17",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v17", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v17", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v17", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
