#!/usr/bin/env python3
"""S12-god-bless v08c — START from IMG_2811 (correct pull) → restyle to book + house."""
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

DIR_REF = ROOT / "Images/styles1/IMG_2811.PNG"
SCENE = OUT / "v07" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Transform IMAGE 1 into our children's book FINAL STORY IMAGE (wide ~2:1 oil painting).

IMAGE 1 = MASTER for flight physics: reindeer are IN FRONT of the sleigh PULLING it; sleigh at BACK;
curve through the sky. KEEP this harness order absolutely. Never put deer behind the sleigh.

IMAGE 2 = our preferred night SCENE: add/merge the Victorian house lower-right (warm golden windows,
snowman, lamp, fence, evergreens), full moon left, North Star upper-right with OPEN dark sky below it,
deep blue atmospheric night, soft cream vignette. Match this story layout.

IMAGE 3 = Santa G0 v2 LOCK: open red coat, cream striped shirt, brown suspenders, warm smile,
kind eyes, rosy cheeks, full white beard — same Santa as every spread.

Restyle IMAGE 1 into OUR book oil style (burgundy/gold, deep shadows, visible brushwork) — do NOT
keep photo-real reference look. Soft cream vignette dissolve.

Expand the team to exactly NINE reindeer still IN FRONT pulling: 4 pairs + Rudolph leading solo
(smallest, furthest). ONLY Rudolph has a VERY FAINT soft warm red nose hint; all other noses brown.
Santa in ornate red/gold sleigh with presents at the BACK. Curve upper-left toward house lower-right.

NO TEXT. NO duplicate Santa. COUNT nine reindeer ahead of the sleigh.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, only 4 reindeer, "
    "text, God bless, laser nose, neon nose, closed coat only, photo realistic, "
    "hard white border, missing house, missing moon, boy, duplicate Santa"
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
    # Widen IMG_2811 to 2:1 canvas as edit base so model starts from correct pull order
    src = Image.open(DIR_REF).convert("RGB")
    base = Image.new("RGB", (2048, 1024), (245, 240, 230))
    # fit width
    w, h = 2048, int(2048 * src.height / src.width)
    if h > 1024:
        h = 1024
        w = int(1024 * src.width / src.height)
    fitted = src.resize((w, h), Image.Resampling.LANCZOS)
    base.paste(fitted, ((2048 - w) // 2, (1024 - h) // 2))
    tmp_base = OUT / "_tmp-v08c-base.png"
    base.save(tmp_base)

    scene = Image.open(SCENE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_scene = OUT / "_tmp-v08c-scene.png"
    scene.save(tmp_scene)

    urls = [
        fal_client.upload_file(str(tmp_base)),
        fal_client.upload_file(str(tmp_scene)),
        fal_client.upload_file(str(SANTA)),
    ]
    print("=== Qwen S12 v08c · edit FROM IMG_2811 canvas ===")
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
    tmp_q = OUT / "_tmp-v08c-qwen.png"
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
    for t in (tmp_base, tmp_scene, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v08c"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    (vdir / "RECIPE.md").write_text(
        f"# RECIPE — S12-god-bless / v08c\n\nEdited FROM IMG_2811 canvas (pull order) + v07 scene + G0.\n\nseed={seed}\n{qurl}\n",
        encoding="utf-8",
    )
    (vdir / "meta.json").write_text(
        json.dumps({"version": "v08c", "seed": seed, "fal_url": qurl, "status": "working"}, indent=2),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v08c", "status": "working"}, indent=2),
        encoding="utf-8",
    )
    (OUT / "RECIPE.md").write_text((vdir / "RECIPE.md").read_text(encoding="utf-8"), encoding="utf-8")

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v08c-final-{DAY}.png",
        unit="S12-god-bless",
        version="v08c",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · FROM IMG_2811 canvas · v07 house/moon · G0 v2",
        subtitle="Pull order from styles1 · book oil restyle · 9 deer ahead",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v08c · edited FROM IMG_2811 (pull order) + v07 scene + Santa G0 v2 · "
        "board S12-god-bless-v08c-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v08c",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v08c",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v08c", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v08c", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v08c", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", seed)


if __name__ == "__main__":
    main()
