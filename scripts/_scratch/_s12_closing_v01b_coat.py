#!/usr/bin/env python3
"""S12-closing v01b — open-coat Santa G0 v2 lock on epic closing spread."""
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
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

BASE = OUT / "v01" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit this seamless Christmas FINAL STORY IMAGE spread. KEEP overall composition: moon left, \
North Star right (sacred golden cross shimmer), Victorian house with warm windows, snowman with scarf, \
snow evergreens, deep blue starry sky, soft vignette frame, continuous L→R flight.

CRITICAL FIX — Santa identity: IMAGE 2 is Santa G0 v2 LOCK. Change Santa in the flying sleigh so his \
red coat is OPEN, revealing light blue-and-white striped shirt with brown suspenders — same wardrobe as \
the reference. Warm painted Santa, NOT a silhouette. Keep white beard. Soft moonlight on him.

Keep ONE continuous flight left→right: sleigh larger on left, smaller/receding toward right near the \
North Star. Reindeer warm brown fur, painted detail. Do NOT add a second separate Santa team.

NO boy. NO text. NO fake gutter. Rich oil painting.
"""

NEG = (
    "closed buttoned coat only, silhouette Santa, black cutout, second separate sleigh team, "
    "boy, child, text, watermark, fake gutter"
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


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def main() -> None:
    load_env()
    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_in = OUT / "_tmp-v01b-in.png"
    base.save(tmp_in)
    urls = [fal_client.upload_file(str(tmp_in)), fal_client.upload_file(str(SANTA))]
    print("=== Qwen S12-closing v01b open coat ===")
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
    url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(url)
    tmp_q = OUT / "_tmp-v01b-qwen.png"
    raw.save(tmp_q)
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
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    final = up_im.resize(SPREAD, Image.Resampling.LANCZOS)
    tmp_in.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v01b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    # Keep v01 untouched; primary = v01b. Also mirror to S12a/S12b paths.
    for folder in (
        ROOT / "Media/development/S12a-blessing",
        ROOT / "Media/development/S12b-god-bless",
    ):
        for name in ("art.png", "art-left.png", "art-right.png"):
            (folder / name).write_bytes((OUT / name).read_bytes())

    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S12-closing / v01b

Open-coat Santa G0 v2 pass on v01 epic closing.

| Field | Value |
|-------|--------|
| **date** | {DAY} |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **status** | working |
""",
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-closing-v01b-epic-{DAY}.png",
        unit="S12-closing",
        version="v01b",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · open-coat Santa G0 v2 · North Star",
        subtitle="FINAL STORY IMAGE · moon L · flight L→R · North Star R · house+snowman",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-closing v01b · open-coat Santa G0 v2 · moon L · flight L→R · North Star R · house+snowman · "
        "MERGED S12a+b · Media/development/S12-closing/ · board S12-closing-v01b-epic-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            p["version"] = "v01b"
            p["notes"] = note
            p["date"] = DAY
            p["caption"] = (
                "p26 · S12 Closing L · v01b open-coat"
                if p["id"] == "p26"
                else "p27 · S12 Closing R · v01b North Star"
            )
        if p["id"] in ("p28", "p29"):
            p["notes"] = "Absorbed into S12-closing v01b — " + note
            p["date"] = DAY
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d["version"] = "v01b"
            d["notes"] = note
            d["date"] = DAY
        if d.get("page") == "28|29":
            d["notes"] = "MERGED into S12-closing v01b — " + note
            d["date"] = DAY
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", seed)


if __name__ == "__main__":
    main()
