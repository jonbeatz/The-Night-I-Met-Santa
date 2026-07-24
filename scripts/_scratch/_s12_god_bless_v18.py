#!/usr/bin/env python3
"""S12-god-bless v18 — v17 layout lock + v06 Santa/sleigh/reindeer look; moon backlight."""
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

V17 = OUT / "v17" / "art.png"  # layout / 9 ahead / star / house
V06 = OUT / "v06" / "art.png"  # look: chuckling Santa, open shirt, reindeer paint, sleigh
V06L = OUT / "v06" / "art-left.png"  # Santa close look (if full missing)

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Merge two Christmas spreads into one MASTER. Wide ~2:1. NO baked text.

IMAGE 1 = LAYOUT LOCK (v17): Keep this composition almost exactly.
Nine reindeer IN FRONT of the sleigh pulling it in a curved arc toward the house.
Sleigh behind the team. Moon left. North Star right with CLEAR OPEN dark sky BELOW it.
Victorian house lower-right, snowman, lamp, evergreens, cream vignette all sides.
Do NOT put any reindeer behind the sleigh. Do NOT copy IMAGE 2's wrong rear-deer layout.

IMAGE 2 = LOOK & FEEL LOCK (v06): Restyle Santa, sleigh, and reindeer paint to match v06.
- Santa: more chuckling / warm joyful smile, open red coat with striped shirt and suspenders
  visible (like v06). Eyes open. Grandfatherly warmth.
- Sleigh: ornate red with rich gold filigree like v06.
- Reindeer: use v06 reindeer ART QUALITY (fur, antlers, proportions) — but keep IMAGE 1
  POSITIONS (all nine ahead pulling). Only Rudolph (frontmost) faint soft red nose.
  All other noses brown.

ALSO:
- Raise Santa and the sleigh so they sit OVER / IN FRONT OF the full moon (moon behind them
  as backlight). Adjust the flight curve slightly if needed; keep nine ahead.
- North Star BIG and gleaming — warm golden-yellow with strong cross rays and halo.
  Keep open sky below for text.
- Count reindeer: 1-2-3-4-5-6-7-8-9. Four pairs + Rudolph leading.

Rich oil-painting storybook finish. NO text. NO duplicate Santa.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, only 8 reindeer, "
    "two glowing noses, laser nose, covering North Star, tiny North Star, "
    "Santa below the moon with empty moon above, closed coat only, "
    "text, God bless, letters, boy, duplicate Santa"
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
    style_path = V06 if V06.is_file() else V06L
    if not V17.is_file():
        raise SystemExit(f"missing: {V17}")
    if not style_path.is_file():
        raise SystemExit(f"missing: {style_path}")

    base = Image.open(V17).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp17 = OUT / "_tmp-v18-v17.png"
    base.save(tmp17)

    style = Image.open(style_path).convert("RGB")
    if style.size[0] / style.size[1] < 1.5:
        # art-left only — pad to 2:1 so upload is consistent
        canvas = Image.new("RGB", (2048, 1024), (30, 40, 70))
        s = style.resize((1024, 1024), Image.Resampling.LANCZOS)
        canvas.paste(s, (0, 0))
        style = canvas
    else:
        style = style.resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp06 = OUT / "_tmp-v18-v06.png"
    style.save(tmp06)

    urls = [
        fal_client.upload_file(str(tmp17)),
        fal_client.upload_file(str(tmp06)),
    ]
    print("=== Qwen S12-god-bless v18 · v17 layout + v06 look ===")
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
    tmp_q = OUT / "_tmp-v18-qwen.png"
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

    for t in (tmp17, tmp06, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v18"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    w, h = final.size
    final.crop((int(w * 0.10), int(h * 0.05), int(w * 0.92), int(h * 0.58))).resize(
        (1800, 650), Image.Resampling.LANCZOS
    ).save(vdir / "_flight-crop.png")

    recipe = f"""# RECIPE — S12-god-bless / v18

| Field | Value |
|-------|--------|
| **version** | **v18** |
| **date** | {DAY} |
| **layout** | v17 (9 ahead, star pocket, house) |
| **look** | v06 (chuckling Santa, open shirt, reindeer paint, sleigh) |
| **extras** | raise Santa/sleigh over moon · big gleaming North Star |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v18",
                "status": "working",
                "layout": "v17",
                "look": "v06",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v18", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v18-final-{DAY}.png",
        unit="S12-god-bless",
        version="v18",
        day=DAY,
        tech="Qwen 2 Pro /edit · v17 layout + v06 look · 9 ahead · moon backlight",
        subtitle="Chuckling open-coat Santa · v06 reindeer paint · gleaming North Star",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v18 · v17 layout + v06 look · 9 ahead · moon backlight · "
        "board S12-god-bless-v18-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v18",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v18",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v18", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v18", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v18", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
