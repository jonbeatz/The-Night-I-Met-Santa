#!/usr/bin/env python3
"""S12-closing v02d — from v02b (8 deer): ADD lead only + North Star. Do not remove deer."""
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
BASE = OUT / "v02b" / "art.png"  # best 8-deer pass

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit of this Christmas spread. PRESERVE every existing reindeer already painted —
there are already about eight deer in four pairs. DO NOT delete, merge, or reduce the team.

ADD exactly ONE more lead reindeer at the front of the team (ahead / to the right of the
existing pairs) so the total becomes NINE: 1 lead + 4 pairs. Same warm brown fur, clear antlers,
painted oil style, harnessed as leader.

ALSO ensure a bright golden North Star with soft cross gleam in the upper RIGHT (sacred hierarchy).
If a star is already there, strengthen its golden gleam; do not move the house.

KEEP: ONE Santa only (open red coat over striped shirt), ornate sleigh + gifts, full moon left,
Victorian house warm windows, snowman, evergreens, deep blue sky, soft vignette.
NO second Santa. NO duplicate sleigh over the house. NO text. NO boy.

Critical: additive edit only for reindeer — never subtract.
"""

NEG = (
    "remove reindeer, fewer deer, second Santa, duplicate sleigh, silhouette, text, boy"
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
    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_in = OUT / "_tmp-v02d-in.png"
    base.save(tmp_in)
    urls = [fal_client.upload_file(str(tmp_in))]
    print("=== Qwen S12-closing v02d additive 9th ===")
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
    tmp_q = OUT / "_tmp-v02d-qwen.png"
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
    tmp_in.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v02d"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT, S12A, S12B):
        dest.mkdir(parents=True, exist_ok=True)
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    (vdir / "meta.json").write_text(
        json.dumps({"version": "v02d", "target_reindeer": 9, "seed": seed, "fal_url": qurl}, indent=2),
        encoding="utf-8",
    )
    (vdir / "RECIPE.md").write_text(
        f"# RECIPE — S12-closing / v02d\n\nAdditive 9th lead from v02b + North Star.\n\nseed={seed}\n{qurl}\n",
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-closing-v02d-nine-reindeer-{DAY}.png",
        unit="S12-closing",
        version="v02d",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · additive 9th lead · no duplicate",
        subtitle="Preserve 8 + add lead = 9 · moon L · North Star R",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-closing v02d · ONE Santa · target 9 reindeer (additive from v02b) · "
        "board S12-closing-v02d-nine-reindeer-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            p["version"] = "v02d"
            p["notes"] = note
            p["date"] = DAY
            p["caption"] = (
                "p26 · S12 Closing L · v02d · 9 reindeer"
                if p["id"] == "p26"
                else "p27 · S12 Closing R · v02d · North Star"
            )
        if p["id"] in ("p28", "p29"):
            p["version"] = "merged-v02d"
            p["notes"] = "Absorbed into S12-closing v02d — " + note
            p["date"] = DAY
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v02d", "notes": note, "date": DAY, "status": "working"})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v02d", "notes": "MERGED into S12-closing v02d — " + note, "date": DAY})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", seed)


if __name__ == "__main__":
    main()
