#!/usr/bin/env python3
"""Recover S12-closing v02 from known Qwen URL after SeedVR 500."""
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
QWEN_URL = "https://v3b.fal.media/files/b/0aa36f8d/26lbb026U3AiSRfWN6FJd_0ivyJX0q.png"
SEED = 1062821389
SPREAD = (5250, 2625)
PAGE = 2625


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
            print("download retry", i, e)
    assert last is not None
    raise last


def main() -> None:
    load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = download(QWEN_URL)
    print("qwen", raw.size)
    tmp = OUT / "_tmp-v02-qwen.png"
    raw.save(tmp)

    final: Image.Image
    try:
        up = fal_client.subscribe(
            "fal-ai/seedvr/upscale/image",
            arguments={
                "image_url": fal_client.upload_file(str(tmp)),
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
        print("seedvr ok", up_im.size)
    except Exception as e:  # noqa: BLE001
        print("SeedVR failed, LANCZOS fallback:", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    tmp.unlink(missing_ok=True)
    vdir = OUT / "v02"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT, S12A, S12B):
        dest.mkdir(parents=True, exist_ok=True)
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S12-closing / v02

| Field | Value |
|-------|--------|
| **fix** | Remove duplicate Santa · **9 reindeer** (lead + 4 pairs) |
| **date** | {DAY} |
| **seed** | {SEED} |
| **fal_url** | `{QWEN_URL}` |
| **status** | working |
""",
        encoding="utf-8",
    )
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v02",
                "status": "working",
                "reindeer_count": 9,
                "seed": SEED,
                "fal_url": QWEN_URL,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-closing-v02-nine-reindeer-{DAY}.png",
        unit="S12-closing",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · NO duplicate · 9 reindeer (lead+4 pairs)",
        subtitle="One Santa · nine deer two-by-two · moon L · North Star R · house+snowman",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-closing v02 · ONE Santa only (duplicate removed) · 9 reindeer lead+4 pairs · "
        "moon L · North Star R · house+snowman · Media/development/S12-closing/ · "
        "board S12-closing-v02-nine-reindeer-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v02",
                    "date": DAY,
                    "status": "working",
                    "notes": note,
                    "path": f"Media/development/S12-closing/art-{side}.png",
                    "development_path": "Media/development/S12-closing/art.png",
                    "caption": (
                        "p26 · S12 Closing L · v02 · 9 reindeer"
                        if p["id"] == "p26"
                        else "p27 · S12 Closing R · v02 · North Star"
                    ),
                }
            )
        if p["id"] in ("p28", "p29"):
            p["notes"] = "Absorbed into S12-closing v02 — " + note
            p["date"] = DAY
            p["version"] = "merged-v02"
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "version": "v02",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if d.get("page") == "28|29":
            d["notes"] = "MERGED into S12-closing v02 — " + note
            d["date"] = DAY
            d["version"] = "merged-v02"
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png")


if __name__ == "__main__":
    main()
