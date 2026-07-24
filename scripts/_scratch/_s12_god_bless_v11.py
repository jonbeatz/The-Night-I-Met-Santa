#!/usr/bin/env python3
"""S12-god-bless v11 — ONE FIX: Santa face match to santa-G0-face.png. Rest locked from v10."""
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

BASE = OUT / "v10" / "art.png"
FACE = ROOT / "Media/approved/characters/santa-G0-face.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical FACE-ONLY edit of this Christmas FINAL STORY IMAGE. Change NOTHING else.

IMAGE 1 = LOCKED v10 spread — keep sleigh angle, Santa body pose/scale in sleigh, reindeer team
(nine deer ahead pulling), Rudolph faint red nose only, house, snowman, moon left, North Star right
with open sky below, cream vignette all sides, deep blue night, presents, lantern. DO NOT redesign
composition, camera, or lighting.

IMAGE 2 = Santa G0 FACE LOCK — match this face EXACTLY on the flying Santa:
same soft kind eyes with crow's feet and laugh lines, same rosy full cheeks, same warm gentle smile
beneath the mustache, same round full grandfatherly face shape, same white beard/mustache character.
The SAME Santa from every spread — only the flying-sleigh viewing angle differs.

ONE FIX ONLY: replace Santa's face (and immediate facial hair continuity) to match IMAGE 2 precisely.
Keep open coat / striped shirt / suspenders if already visible. Keep body smaller in the sleigh as in v10.

NO other changes. NO baked text. NO extra glowing noses. NO moving reindeer or house.
"""

NEG = (
    "new composition, redesigned scene, different sleigh angle, moving house, "
    "stern face, angular face, wrong Santa, young face, angry Santa, "
    "text, God bless, letters, watermark, second glowing nose, laser nose, "
    "reindeer behind sleigh, changing reindeer count, hard white border"
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
    for p in (BASE, FACE):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v11-base.png"
    base.save(tmp)
    urls = [fal_client.upload_file(str(tmp)), fal_client.upload_file(str(FACE))]

    print("=== Qwen S12-god-bless v11 face-only ===")
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
    tmp_q = OUT / "_tmp-v11-qwen.png"
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
    tmp.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v11"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v11

| Field | Value |
|-------|--------|
| **fix** | FACE ONLY — match santa-G0-face.png |
| **base** | v10 (composition locked) |
| **version** | **v11** |
| **date** | {DAY} |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v11",
                "status": "working",
                "fix": "santa_face_match_G0",
                "base": "v10",
                "face_ref": "Media/approved/characters/santa-G0-face.png",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v11", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v11-face-{DAY}.png",
        unit="S12-god-bless",
        version="v11",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · FACE ONLY · santa-G0-face · v10 locked",
        subtitle="Same grandfatherly face · composition unchanged",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v11 · FACE ONLY match santa-G0-face.png · v10 composition locked · "
        "board S12-god-bless-v11-face-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v11",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v11",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v11", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v11", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v11", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
