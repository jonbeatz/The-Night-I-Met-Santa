#!/usr/bin/env python3
"""Compose Cover INDD art-no-type PNG from Front/Back panel exports (no live type, no QR).

Expects Photoshop-exported panels (type + QR hidden, title logo + frames kept):
  scripts/_scratch/_panel-front-art-notype.png  (2812×3075)
  scripts/_scratch/_panel-back-art-notype.png   (2813×3075)

Writes:
  Xtraz/Adobe-inDesign/FINAL-Master-inDD/links/TNIMS-Cover-Wrap-FINAL-5700x3075-art-no-type.png

Run after: Photoshop JSX scripts/cover-export-art-notype-panels-5700.jsx
Then: relink Cover INDD → export Cover → rebake flipbook FRONT/BACK.
See: .cursor/docs/COVER-REBUILD-WORKFLOW.md
"""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
SCR = ROOT / "scripts/_scratch"
LINKS = ROOT / "Xtraz/Adobe-inDesign/FINAL-Master-inDD/links"
ART = LINKS / "TNIMS-Cover-Wrap-FINAL-5700x3075-art-no-type.png"
BAK = LINKS / "_Hold-bak"

BW, SW, WW, WH = 2813, 75, 5700, 3075
SPINE_RGB = (88, 18, 28)


def main() -> None:
    front = Image.open(SCR / "_panel-front-art-notype.png").convert("RGB")
    back = Image.open(SCR / "_panel-back-art-notype.png").convert("RGB")
    if front.size != (2812, 3075):
        raise SystemExit(f"front size {front.size}, expected 2812x3075")
    if back.size != (2813, 3075):
        raise SystemExit(f"back size {back.size}, expected 2813x3075")

    wrap = Image.new("RGB", (WW, WH), SPINE_RGB)
    wrap.paste(back, (0, 0))
    wrap.paste(front, (BW + SW, 0))

    BAK.mkdir(parents=True, exist_ok=True)
    if ART.exists():
        shutil.copy2(ART, BAK / f"{ART.stem}-pre-rebuild.bak.png")
    wrap.save(ART, "PNG")
    print(f"wrote {ART} ({ART.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
