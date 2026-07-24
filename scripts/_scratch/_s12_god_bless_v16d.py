#!/usr/bin/env python3
"""S12-god-bless v16d — ONLY add 9th reindeer to v15b (no other changes)."""
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

V15B = OUT / "v15b" / "art.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
ONE CHANGE ONLY to this Christmas spread. Do not redesign anything else.

ADD exactly ONE more reindeer into the existing flying harnessed team so the total becomes
NINE. Place the new reindeer in the curve IN FRONT of the sleigh, as a missing pair-mate
near the middle/front of the team (4 pairs + Rudolph leading). Match the same paint style,
size, brown fur, antlers, and harness as the neighboring reindeer.

KEEP everything else identical: Santa pose/face, sleigh, moon, North Star with open sky
below, house, snowman, lamp, vignette, flying altitude, composition.
ONLY Rudolph (the frontmost) keeps the faint red nose — the new deer has a normal nose.
NO text. Wide ~2:1.

Final count must be nine reindeer heads. Count them.
"""

NEG = (
    "redesigned scene, moved Santa, lowered sleigh, only 8 reindeer, "
    "two glowing noses, covering North Star, text, God bless, letters, new background"
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


def save_version(final: Image.Image, version: str, seed, qurl: str, note: str) -> None:
    vdir = OUT / version
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / {version}

| Field | Value |
|-------|--------|
| **version** | **{version}** |
| **date** | {DAY} |
| **base** | v15b |
| **change** | add 9th reindeer only |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {"version": version, "status": "working", "base": "v15b", "seed": seed, "fal_url": qurl, "size": list(SPREAD)},
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": version, "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-{version}-final-{DAY}.png",
        unit="S12-god-bless",
        version=version,
        day=DAY,
        tech="Qwen 2 Pro /edit · v15b + 9th deer only",
        subtitle=note,
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    full_note = f"S12-god-bless {version} · {note} · board S12-god-bless-{version}-final-{DAY}.png"
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": version,
                    "status": "working",
                    "date": DAY,
                    "notes": full_note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · {version}",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": f"merged-{version}", "status": "merged", "date": DAY, "notes": "Absorbed — " + full_note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": version, "status": "working", "date": DAY, "notes": full_note})
        if d.get("page") == "28|29":
            d.update({"version": f"merged-{version}", "status": "merged", "date": DAY, "notes": "MERGED — " + full_note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    load_env()
    if not V15B.is_file():
        raise SystemExit(f"missing: {V15B}")

    base = Image.open(V15B).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v16d-base.png"
    base.save(tmp)

    print("=== Qwen S12-god-bless v16d · add 9th deer ONLY ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [fal_client.upload_file(str(tmp))],
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
    tmp_q = OUT / "_tmp-v16d-qwen.png"
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

    save_version(final, "v16d", seed, qurl, "9th deer only on v15b · then moon raise next if count ok")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
