#!/usr/bin/env python3
"""S12a v02b — add tiny sleigh through left window glass; keep absence exterior R."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
S12A = ROOT / "Media/development/S12a-blessing"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

BASE = S12A / "v02" / "art.png"
S8L = ROOT / "Media/development/S08-gone/art-left.png"  # sleigh-in-sky language if useful

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit this seamless Christmas storybook SPREAD. KEEP composition, lighting, vignette, colors.

CRITICAL FIX — LEFT half only: Through the frosted window panes, ADD a TINY distant silhouette of \
Santa's sleigh and reindeer flying away across the bright full moon / deep blue night sky. \
Very small — a speck of departure seen from inside looking OUT. Do NOT enlarge Santa. \
Keep burgundy walls, moonlight beams, dark quiet empty room, no boy, no furniture clutter.

RIGHT half: KEEP the pure exterior night — moon, stars, snow evergreens, house with warm golden \
windows, sleigh already distant in the sky. Soft vignette. NO boy.

IMAGE 2 (if present) = sleigh silhouette reference only — use for tiny distant shape language.

NO text. NO fake gutter. Rich oil painting. Absence / departure mood.
"""

NEG = (
    "boy, child, person in room, large Santa, Santa inside, letter, glowing envelope, "
    "text, watermark, fake gutter, remove vignette"
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
    if not BASE.is_file():
        raise SystemExit(f"missing {BASE}")

    # Downscale for edit input then upscale final
    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_in = S12A / "_tmp-v02b-in.png"
    base.save(tmp_in)

    refs = [tmp_in]
    if S8L.is_file():
        refs.append(S8L)

    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen S12a v02b add sleigh ===")
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
    tmp_q = S12A / "_tmp-v02b-qwen.png"
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

    vdir = S12A / "v02b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, S12A):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    # Also promote into v02 as latest working (Jon asked v02 approach)
    v02 = S12A / "v02"
    for name in ("art.png", "art-left.png", "art-right.png"):
        shutil_copy = final if name == "art.png" else (left if "left" in name else right)
        # already saved primary; copy primary into v02 overwrite
    for name in ("art.png", "art-left.png", "art-right.png"):
        (v02 / name).write_bytes((S12A / name).read_bytes())

    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S12a-blessing / v02b

Edit of v02 — add tiny sleigh through LEFT window glass.

| Field | Value |
|-------|--------|
| **date** | {DAY} |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **status** | working |
| **note** | Primary mirrors = v02b (also written to v02/) |
""",
        encoding="utf-8",
    )
    (v02 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v02b",
                "status": "working",
                "parent": "v02",
                "fix": "add_tiny_sleigh_through_window",
                "seed": seed,
                "fal_url": url,
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
        INDEX / f"S12a-blessing-v02b-absence-{DAY}.png",
        unit="S12a-blessing",
        version="v02b",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · tiny sleigh through window · NO boy",
        subtitle="Window OUT + tiny sleigh L · exterior almost-gone R · poem all p26",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "v02b absence · NO boy · L frosted window looking OUT + tiny sleigh · R pure exterior · "
        "poem ALL p26 · board S12a-blessing-v02b-absence-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            p["version"] = "v02b"
            p["date"] = DAY
            p["status"] = "working"
            p["notes"] = note if p["id"] == "p27" else ("ALL poem text · " + note)
            p["path"] = f"Media/development/S12a-blessing/art-{'left' if p['id']=='p26' else 'right'}.png"
            p["development_path"] = "Media/development/S12a-blessing/art.png"
            p["caption"] = (
                "p26 · S12a Blessing L · v02b window+sleigh"
                if p["id"] == "p26"
                else "p27 · S12a Blessing R · v02b exterior absence"
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "version": "v02b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("DONE", S12A / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
