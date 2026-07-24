#!/usr/bin/env python3
"""S12-god-bless v13b — open coat + Rudolph-only nose on v13 lock (keep harness)."""
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

V13 = OUT / "v13" / "art.png"
FACE = ROOT / "Images/styles1/santa-G0-face.png"
G0V2 = ROOT / "Images/styles1/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit of this Christmas spread. KEEP almost everything identical.

KEEP LOCKED (do not change):
- Reindeer RULE already correct: nine harnessed in pairs IN FRONT of the sleigh, pulling
  like horses, harnesses back to the sleigh, clean curved team, sleigh behind all of them.
  Do NOT move, scatter, add, or remove any reindeer. Do NOT put any deer behind the sleigh.
- Moon left, North Star right, house/snowman/lamp/evergreens, vignette, composition, sleigh path.
- NO text.

CHANGE ONLY:
1) Santa wardrobe → open red coat like IMAGE 3 (G0 v2): show striped shirt and brown
   suspenders under the open coat. Keep Santa looking back with warm smile, eyes OPEN
   matching IMAGE 2 face.
2) Nose glow → ONLY the front lead Rudolph has a faint soft red nose. Remove any other
   reindeer nose glow completely. No second glowing nose.

Everything else unchanged. Wide ~2:1.
"""

NEG = (
    "closed coat only, buttoned coat covering shirt, reindeer behind sleigh, "
    "moved reindeer, new reindeer, two glowing noses, three glowing noses, "
    "laser nose, neon nose, eyes closed, text, God bless, letters, boy"
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
    for p in (V13, FACE, G0V2):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(V13).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v13b-base.png"
    base.save(tmp)

    urls = [
        fal_client.upload_file(str(tmp)),
        fal_client.upload_file(str(FACE)),
        fal_client.upload_file(str(G0V2)),
    ]
    print("=== Qwen S12-god-bless v13b · open coat + Rudolph only ===")
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
    tmp_q = OUT / "_tmp-v13b-qwen.png"
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

    vdir = OUT / "v13b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v13b

| Field | Value |
|-------|--------|
| **version** | **v13b** |
| **date** | {DAY} |
| **base** | v13 (harness lock) |
| **fix** | open coat G0 v2 + Rudolph-only faint nose |
| **face** | Images/styles1/santa-G0-face.png |
| **wardrobe** | Images/styles1/santa-G0-v2.png |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v13b",
                "status": "working",
                "base": "v13",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v13b", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v13b-final-{DAY}.png",
        unit="S12-god-bless",
        version="v13b",
        day=DAY,
        tech="Qwen 2 Pro /edit · v13 harness lock · open coat + Rudolph only",
        subtitle="Surgical wardrobe/nose pass — team formation frozen",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v13b · harness from v13 · open coat + Rudolph faint only · "
        "board S12-god-bless-v13b-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v13b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v13b",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v13b", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v13b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v13b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
