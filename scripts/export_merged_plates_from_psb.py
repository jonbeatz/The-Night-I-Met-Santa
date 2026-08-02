#!/usr/bin/env python3
"""Export TNIMS Merged plates from Book-Master PSB -> FINAL-Master-Chopz.

Canonical export for Lulu + flipbook art (same PNGs feed both INDDs).

Why topil() not composite():
  Unit groups under TNIMS-Merged-Comps are usually hidden. psd_tools
  composite() respects visibility and returns blank; topil() reads raw
  stamped pixels (includes Stamp Visible glow/shadow shells).

Usage (from repo root):
  python scripts/export_merged_plates_from_psb.py --all
  python scripts/export_merged_plates_from_psb.py --only S03,S12,Back-Page
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from psd_tools import PSDImage

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
PSB = ROOT / "Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/TNIMS-Book-Master-FINAL.psb"
CHOPZ_ROOT = ROOT / "Xtraz/Adobe-Finals/FINAL-Master-Chopz"
OUT_INTERIOR = CHOPZ_ROOT / "TNIMS-Interior-FINAL-Chopz"
OUT_FLIPBOOK = CHOPZ_ROOT / "TNIMS-Flipbook-FINAL-Chopz"

MERGED_NAME_RE = re.compile(r"merged", re.I)

# Unit group name -> export basename (no extension)
UNIT_BASENAME = {
    "PO": "P0-spread",
    "P01": "P01-spread",
    "P02": "P02-spread",
    "S01": "S01-spread",
    "S02": "S02-spread",
    "S03": "S03-spread",
    "S04": "S04-spread",  # text|image — may need L/R split later
    "S05": "S05-spread",
    "S06": "S06-spread",
    "S07": "S07-spread",
    "S08": "S08-spread",
    "S09": "S09-spread",
    "S10": "S10-spread",
    "S11": "S11-spread",
    "S12": "S12-spread",
    "P-author-thank-you": "P-author-thank-you-spread",
    "Back-Page": "Back-Page-spread",  # p32|33
}


def safe_name(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*]', "_", s.strip())
    s = re.sub(r"\s+", "-", s)
    return s[:80]


def find_merged_comps(psd: PSDImage):
    for top in psd:
        if top.name.strip() == "TNIMS-Merged-Comps":
            return top
    raise SystemExit("TNIMS-Merged-Comps group not found")


def pick_export_layer(group):
    pixels = []
    merged = []
    for child in group:
        kind = getattr(child, "kind", "")
        name = child.name
        if kind == "group" and MERGED_NAME_RE.search(name):
            return ("group", child)
        if kind in ("pixel", "smartobject"):
            pixels.append(child)
            if MERGED_NAME_RE.search(name):
                merged.append(child)
    if merged:
        for m in merged:
            if "bg-art" not in m.name.lower():
                return ("pixel", m)
        return ("pixel", merged[0])
    for p in pixels:
        if "burgundy" not in p.name.lower():
            return ("pixel", p)
    return (None, None)


def layer_to_canvas(layer, canvas_size) -> Image.Image:
    if getattr(layer, "kind", "") == "group":
        pick = None
        for c in layer:
            if getattr(c, "kind", "") == "pixel" and MERGED_NAME_RE.search(c.name):
                pick = c
                break
        if pick is None:
            for c in layer:
                if getattr(c, "kind", "") in ("pixel", "smartobject"):
                    pick = c
                    break
        if pick is None:
            raise RuntimeError(f"no pixel inside group {layer.name}")
        layer = pick

    im = layer.topil()
    if im is None:
        raise RuntimeError(f"topil None for {layer.name}")
    im = im.convert("RGBA")
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    left = int(getattr(layer, "left", 0) or 0)
    top = int(getattr(layer, "top", 0) or 0)
    if left < 0 or top < 0:
        crop_l = max(0, -left)
        crop_t = max(0, -top)
        im = im.crop((crop_l, crop_t, im.width, im.height))
        left = max(0, left)
        top = max(0, top)
    canvas.alpha_composite(im, (left, top))
    return canvas


def is_blank(im: Image.Image) -> bool:
    rgb = im.convert("RGB")
    ex = rgb.getextrema()
    return ex in (((0, 0), (0, 0), (0, 0)), ((255, 255), (255, 255), (255, 255)))


def unit_basename(group_name: str) -> str:
    key = group_name.strip()
    if key in UNIT_BASENAME:
        return UNIT_BASENAME[key]
    # trim trailing spaces / normalize
    key2 = key.rstrip()
    if key2 in UNIT_BASENAME:
        return UNIT_BASENAME[key2]
    return f"{safe_name(key2)}-spread"


def main() -> int:
    ap = argparse.ArgumentParser(description="Export TNIMS Merged plates to FINAL-Master-Chopz")
    ap.add_argument("--all", action="store_true", help="Export every Merged unit")
    ap.add_argument("--only", default="", help="Comma unit names (default with --all: everything)")
    ap.add_argument("--no-flipbook-copy", action="store_true", help="Skip copy into Flipbook chopz")
    ap.add_argument("--psb", default=str(PSB))
    args = ap.parse_args()

    if not args.all and not args.only:
        args.all = True

    OUT_INTERIOR.mkdir(parents=True, exist_ok=True)
    OUT_FLIPBOOK.mkdir(parents=True, exist_ok=True)

    psb_path = Path(args.psb)
    print("opening", psb_path.name, flush=True)
    psd = PSDImage.open(psb_path)
    canvas = (psd.width, psd.height)
    print("canvas", canvas, flush=True)

    merged_root = find_merged_comps(psd)
    units = [g for g in merged_root if getattr(g, "kind", "") == "group"]
    print(f"unit groups: {len(units)}", flush=True)

    if args.all:
        targets = units
    else:
        want = {x.strip().lower() for x in args.only.split(",") if x.strip()}
        targets = [
            g
            for g in units
            if g.name.strip().lower() in want
            or any(w in g.name.strip().lower() for w in want)
        ]

    results = []
    for g in targets:
        kind, layer = pick_export_layer(g)
        base = unit_basename(g.name)
        if not layer:
            print(f"SKIP {base}: no art layer", flush=True)
            results.append({"unit": g.name, "file": None, "status": "SKIP"})
            continue
        print(f"EXPORT {base} <- [{kind}] {layer.name}", flush=True)
        try:
            rgba = layer_to_canvas(layer, canvas)
            if is_blank(rgba):
                print(f"  WARN blank {base}", flush=True)
                results.append({"unit": g.name, "file": None, "status": "BLANK", "source": layer.name})
                continue
            out_path = OUT_INTERIOR / f"{base}.png"
            rgba.convert("RGB").save(out_path, "PNG")
            print(f"  saved {out_path.name} {rgba.size}", flush=True)
            if not args.no_flipbook_copy:
                dest = OUT_FLIPBOOK / out_path.name
                shutil.copy2(out_path, dest)
            results.append(
                {
                    "unit": g.name.strip(),
                    "file": out_path.name,
                    "status": "OK",
                    "source_layer": layer.name,
                    "size": list(rgba.size),
                }
            )
        except Exception as e:
            print(f"  FAIL {base}: {e}", flush=True)
            results.append({"unit": g.name, "file": None, "status": f"FAIL:{e}"})

    ok = sum(1 for r in results if r["status"] == "OK")
    manifest = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "psb": str(psb_path),
        "canvas": list(canvas),
        "method": "psd_tools.topil from TNIMS-Merged-Comps *Merged* layers",
        "out_interior": str(OUT_INTERIOR),
        "out_flipbook": str(OUT_FLIPBOOK),
        "ok": ok,
        "total": len(results),
        "plates": results,
        "notes": [
            "Merged plates may include fill-0 type with glow/shadow shells for InDesign live-type overlay.",
            "Same PNGs feed Interior + Flipbook INDDs; PDF trim/bleed differs in InDesign export only.",
            "S04 may need left/right isolate for Lulu single-page PDF if cream|art split.",
        ],
    }
    man_path = OUT_INTERIOR / "_export-manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if not args.no_flipbook_copy:
        shutil.copy2(man_path, OUT_FLIPBOOK / "_export-manifest.json")

    print("\n=== SUMMARY ===", flush=True)
    for r in results:
        print(f"  {r['status']:8} {r.get('file') or r['unit']}", flush=True)
    print(f"{ok}/{len(results)} -> {OUT_INTERIOR}", flush=True)
    print("manifest", man_path, flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
