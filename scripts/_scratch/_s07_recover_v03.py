#!/usr/bin/env python3
"""Recover S7 Proof v03 KEEP from fal CDN (mocks/v03 is old dial, not the locked plate)."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S07-proof"
KEEP_ARCHIVE = ROOT / "Media/development/S07-proof/_LOCKED-v03"
# From v03 Qwen job 2026-07-23
FAL_URL = "https://v3b.fal.media/files/b/0aa36025/QPqfVK1OSYna5Led8ewr1_ImN7imhI.png"
SEED = 1379047022
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
DAY = "2026-07-23"


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
    UNIT.mkdir(parents=True, exist_ok=True)
    KEEP_ARCHIVE.mkdir(parents=True, exist_ok=True)

    print("download v03 fal raw", FAL_URL[:60], "...")
    raw = download(FAL_URL)
    print("raw", raw.size)
    tmp = UNIT / "_tmp-v03-recover.png"
    raw.save(tmp)

    print("SeedVR upscale → print")
    up_url = fal_client.upload_file(str(tmp))
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": up_url,
            "upscale_mode": "factor",
            "upscale_factor": 2,
            "noise_scale": 0.1,
            "output_format": "png",
        },
        with_logs=True,
    )
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    final = up_im.resize(TARGET, Image.Resampling.LANCZOS)
    tmp.unlink(missing_ok=True)

    # Write keepers + immutable archive copy (never overwrite for tests)
    final.save(UNIT / "art.png", optimize=True)
    final.crop((0, 0, 2625, 2625)).save(UNIT / "art-left.png", optimize=True)
    final.crop((2625, 0, 5250, 2625)).save(UNIT / "art-right.png", optimize=True)
    final.save(KEEP_ARCHIVE / "art.png", optimize=True)
    print("restored", UNIT / "art.png", final.size)
    print("archive", KEEP_ARCHIVE / "art.png")

    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v03 KEEP

| Field | Value |
|-------|--------|
| **name** | S7 Proof — LOCKED unframed |
| **unit** | S07-proof |
| **book page** | Flow v2 p16\\|17 SPREAD |
| **version** | **v03 KEEP** |
| **date** | {DAY} |
| **status** | **KEEP / LOCKED** — unframed |
| **model** | `fal-ai/qwen-image-2/pro/edit` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {SEED} |
| **fal_url** | `{FAL_URL}` |
| **composition lock** | `Media/generated/mocks/S07-proof/v06/art.png` |
| **archive copy** | `Media/development/S07-proof/_LOCKED-v03/art.png` |
| **rejected** | v04 Pillow frame (ghost artifact) — do not use |

## Locked content

Boy R look-up · vintage camera FG on floor · tree L · fireplace far L · burgundy walls · holly PJs · no Santa · no skylight. Hard edges (no mock-up frame).
""",
        encoding="utf-8",
    )
    (UNIT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v03",
                "status": "keep",
                "seed": SEED,
                "fal_url": FAL_URL,
                "size": list(TARGET),
                "framed": False,
                "archive": "Media/development/S07-proof/_LOCKED-v03/art.png",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (KEEP_ARCHIVE / "README.md").write_text(
        "Immutable KEEP plate for S7 Proof v03. Do not overwrite. Tests use new version numbers only.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
