#!/usr/bin/env python3
"""S12-closing v02b — expand reindeer team to exactly 9 (lead + 4 pairs). Keep no-dupe."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-closing"
S12B = ROOT / "Media/development/S12b-god-bless"
S12A = ROOT / "Media/development/S12a-blessing"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

BASE = OUT / "v02" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit this seamless Christmas FINAL STORY IMAGE. KEEP composition almost identical:
ONE Santa in ornate sleigh (open red coat, striped shirt), full moon left, North Star golden gleam right,
Victorian house with warm windows, snowman, snow evergreens, deep blue sky, soft vignette.
NO second Santa. NO duplicate sleigh over the house. Sky above house stays clean except stars + North Star.

ONLY MAJOR CHANGE — REINDEER TEAM:
Expand the team to EXACTLY NINE (9) painted reindeer pulling the ONE sleigh.
Formation: 1 lead reindeer at the front (rightmost of the team) + 4 pairs behind it (two-by-two).
All warm brown fur, clear antlers, leather harnesses, full oil-painted detail — NOT silhouettes.
Stretch the team naturally across the sky from the sleigh toward the right so all nine are countable.
Do not hide reindeer behind each other so heavily that they cannot be counted as nine.

Keep Santa G0 v2 open-coat look (IMAGE 2). No boy. No text. No fake gutter.
"""

NEG = (
    "second Santa, duplicate sleigh over house, only 2 reindeer, only 3 reindeer, only 4 reindeer, "
    "silhouette deer, black cutouts, text, watermark, boy"
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
        raise SystemExit(f"missing {BASE}")
    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_in = OUT / "_tmp-v02b-in.png"
    base.save(tmp_in)
    urls = [fal_client.upload_file(str(tmp_in)), fal_client.upload_file(str(SANTA))]
    print("=== Qwen S12-closing v02b · force 9 reindeer ===")
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
            "enable_prompt_expansion": True,
        },
        with_logs=True,
    )
    print(result)
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    tmp_q = OUT / "_tmp-v02b-qwen.png"
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
        up_im = download(u)
        final = up_im.resize(SPREAD, Image.Resampling.LANCZOS)
        print("seedvr", up_im.size)
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    tmp_in.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v02b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT, S12A, S12B):
        dest.mkdir(parents=True, exist_ok=True)
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S12-closing / v02b

Force **9 reindeer** (lead + 4 pairs) on v02 (duplicate already removed).

| Field | Value |
|-------|--------|
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **date** | {DAY} |
""",
        encoding="utf-8",
    )
    (vdir / "meta.json").write_text(
        json.dumps(
            {"version": "v02b", "reindeer_count": 9, "seed": seed, "fal_url": qurl, "size": list(SPREAD)},
            indent=2,
        ),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-closing-v02b-nine-reindeer-{DAY}.png",
        unit="S12-closing",
        version="v02b",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · 9 reindeer forced · no duplicate",
        subtitle="Lead + 4 pairs · one Santa · moon L · North Star R",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-closing v02b · ONE Santa · 9 reindeer (lead+4 pairs) · no duplicate · "
        "board S12-closing-v02b-nine-reindeer-2026-07-23.png · Media/development/S12-closing/"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            p["version"] = "v02b"
            p["notes"] = note
            p["date"] = DAY
            p["caption"] = (
                "p26 · S12 Closing L · v02b · 9 reindeer"
                if p["id"] == "p26"
                else "p27 · S12 Closing R · v02b · North Star"
            )
        if p["id"] in ("p28", "p29"):
            p["notes"] = "Absorbed into S12-closing v02b — " + note
            p["version"] = "merged-v02b"
            p["date"] = DAY
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v02b", "notes": note, "date": DAY, "status": "working"})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v02b", "notes": "MERGED into S12-closing v02b — " + note, "date": DAY})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", seed)


if __name__ == "__main__":
    main()
