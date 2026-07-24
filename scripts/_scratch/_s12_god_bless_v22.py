#!/usr/bin/env python3
"""S12-god-bless v22 — LAST Qwen test. Best 3 of Jon's refs (API max 3)."""
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

# Jon's pool (Qwen max 3 — pick strongest combo)
V11 = OUT / "v11" / "art.png"  # nine ahead + flight toward house + star/house
V06L = OUT / "v06" / "art-left.png"  # chuckling open-coat Santa + sleigh paint
V16 = OUT / "v16" / "art.png"  # moon backlight + Rudolph + gleaming star + yard

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
S12 God Bless — FINAL last test. FULL SPREAD wide ~2:1. NO baked text.

Combine the BEST of three references:

IMAGE 1 (v11) = FORMATION + FLIGHT PATH LOCK (MOST IMPORTANT):
All reindeer IN FRONT OF Santa's sleigh, PULLING it through the sky like horses pull a
carriage. Sleigh BEHIND the team. Exactly NINE: four pairs side-by-side + Rudolph leading
at the front. Dynamic curved arc flying toward the house. Count: 1-2-3-4-5-6-7-8-9.
NEVER put reindeer behind the sleigh. NEVER leave deer on the ground.

IMAGE 2 (v06 left) = SANTA / SLEIGH LOOK: chuckling warm Santa, open red coat, cream
striped shirt, brown suspenders, ornate red/gold sleigh with presents. Apply this look
onto the flying scene. Eyes open, looking back with warmth. Soft lantern glow.

IMAGE 3 (v16) = SCENE FINISH: full moon LEFT behind/near Santa; BIG bright gleaming
North Star RIGHT with golden cross rays and halo; CLEAR open dark sky BELOW the star for
\"God bless\"; Victorian house lower-right warm windows, snowman, lamp post, evergreens,
cream vignette all sides. ONLY Rudolph (frontmost) faint soft red nose — brown noses else.

A simple beautiful Christmas Eve: Santa flies, nine reindeer pull ahead, over snowy house.
Rich oil-painting storybook. Soft cream watercolor vignette evenly on ALL sides.
NO text. NO duplicate Santa. ONE continuous painted scene.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, deer on the ground, "
    "only 6 reindeer, only 7, only 8, 10 reindeer, scattered reindeer on the moon, "
    "two glowing noses, three glowing noses, laser nose, tiny North Star, "
    "covering North Star, text, God bless, letters, boy, duplicate Santa"
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


def to_spread_temp(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h < 1.5:
        # square left page — place on 2:1 canvas left half
        canvas = Image.new("RGB", (2048, 1024), (25, 35, 65))
        s = im.resize((1024, 1024), Image.Resampling.LANCZOS)
        canvas.paste(s, (0, 0))
        canvas.save(dest)
    else:
        im.resize((2048, 1024), Image.Resampling.LANCZOS).save(dest)


def main() -> None:
    load_env()
    for p in (V11, V06L, V16):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Start FROM v11 so nine-ahead is in the pixels
    base = Image.open(V11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v22-v11.png"
    base.save(tmp11)
    tmp06 = OUT / "_tmp-v22-v06l.png"
    to_spread_temp(V06L, tmp06)
    tmp16 = OUT / "_tmp-v22-v16.png"
    to_spread_temp(V16, tmp16)

    urls = [
        fal_client.upload_file(str(tmp11)),
        fal_client.upload_file(str(tmp06)),
        fal_client.upload_file(str(tmp16)),
    ]
    print("=== Qwen S12-god-bless v22 LAST · v11 + v06L + v16 ===")
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
    tmp_q = OUT / "_tmp-v22-qwen.png"
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

    for t in (tmp11, tmp06, tmp16, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v22"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    w, h = final.size
    final.crop((int(w * 0.08), int(h * 0.05), int(w * 0.95), int(h * 0.62))).resize(
        (1800, 700), Image.Resampling.LANCZOS
    ).save(vdir / "_flight-crop.png")

    recipe = f"""# RECIPE — S12-god-bless / v22

| Field | Value |
|-------|--------|
| **version** | **v22** (LAST Qwen test before PS) |
| **date** | {DAY} |
| **model** | Qwen 2 Pro /edit v06 |
| **refs used (max 3)** | v11 formation · v06 art-left Santa look · v16 scene/star |
| **refs noted not attached** | v09 · v12 · v13 (API 3-slot) |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v22",
                "status": "working",
                "last_qwen_test": True,
                "refs": ["v11", "v06/art-left", "v16"],
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v22", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v22-final-{DAY}.png",
        unit="S12-god-bless",
        version="v22",
        day=DAY,
        tech="Qwen 2 Pro /edit LAST · v11 + v06L + v16 · 9 ahead emphasized",
        subtitle="Deer IN FRONT · Rudolph faint · gleaming North Star · PS master next",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v22 LAST Qwen test · v11+v06L+v16 · "
        "board S12-god-bless-v22-final-2026-07-23.png · Jon PS master next"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v22",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v22",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v22", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v22", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v22", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
