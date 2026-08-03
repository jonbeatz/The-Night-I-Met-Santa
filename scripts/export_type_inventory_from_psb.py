#!/usr/bin/env python3
"""Export Photoshop type layers → type-inventory.json (PS → InDesign handoff).

Reads a book-master PSB via psd_tools, extracts text + bbox + font metrics +
optional bold runs, writes the schema from PS-TO-ID-TYPE-HANDOFF.md.

Usage (repo root):
  python scripts/export_type_inventory_from_psb.py
  python scripts/export_type_inventory_from_psb.py --unit S01,S04
  python scripts/export_type_inventory_from_psb.py --split-units
  python scripts/export_type_inventory_from_psb.py --psb PATH --out PATH
  python scripts/export_type_inventory_from_psb.py --visible-only
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.type_inventory_common import (  # noqa: E402
    BLEED_IN_DEFAULT,
    DPI_DEFAULT,
    UNIT_DEV_FOLDERS,
    bbox_side_and_page,
    clean_text,
    guess_paragraph_style,
    is_guide_layer,
    jsafe,
    metrics_and_runs,
    px_box_to_page_inches,
    type_text,
)

DEFAULT_PSB = (
    ROOT
    / "Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/TNIMS-Book-Master-FINAL.psb"
)
DEFAULT_OUT = (
    ROOT
    / "Xtraz/Adobe-Finals/FINAL-Master-Chopz/_type-inventory.json"
)


def find_scan_roots(psd):
    """Prefer TNIMS-Layer-Comps (live type); else top-level groups."""
    for L in psd:
        name = (L.name or "").strip()
        if L.kind == "group" and (
            "Layer-Comp" in name or name == "TNIMS-Layer-Comps"
        ):
            return list(L), name
    return [L for L in psd if L.kind == "group"], "top-groups"


def collect_frames(
    psd,
    *,
    units: set[str] | None,
    visible_only: bool,
    include_guides: bool,
    dpi: float,
    bleed_in: float,
) -> list[dict]:
    scan_roots, _src = find_scan_roots(psd)
    mid_w = float(psd.width)
    frames: list[dict] = []
    idx = 0

    for G in scan_roots:
        if G.kind != "group":
            continue
        gname = (G.name or "").strip()
        if units and gname not in units:
            # allow prefix match S01 vs S01-approach
            if not any(gname == u or gname.startswith(u) for u in units):
                continue
        for T in G.descendants():
            if getattr(T, "kind", "") != "type":
                continue
            lname = (T.name or "")[:160]
            if not include_guides and is_guide_layer(lname):
                continue
            vis = bool(getattr(T, "visible", True))
            if visible_only and not vis:
                continue

            bbox = list(T.bbox) if T.bbox else None
            side, local = bbox_side_and_page(bbox, mid_w)
            text = clean_text(type_text(T))
            m = metrics_and_runs(T, dpi=dpi)
            idx += 1
            fid = f"{gname}-{side}-{idx:02d}"

            frame: dict = {
                "id": fid,
                "unit": UNIT_DEV_FOLDERS.get(gname, gname),
                "group": gname,
                "ps_layer": lname,
                "page": side,
                "visible": vis,
                "opacity": float(getattr(T, "opacity", 255)),
                "bbox_px": {
                    "l": local[0] if local else None,
                    "t": local[1] if local else None,
                    "r": local[2] if local else None,
                    "b": local[3] if local else None,
                }
                if local
                else None,
                "bbox_spread_px": bbox,
                "bbox_page_px": local,
                "bounds_in": px_box_to_page_inches(local, dpi, bleed_in)
                if local
                else None,
                "font": m.get("font"),
                "style": m.get("style") or "Regular",
                "size_pt": m.get("size_pt"),
                "leading_pt": m.get("leading_pt"),
                "tracking": m.get("tracking"),
                "color": m.get("color") or "#2C1810",
                "align": m.get("align") or "center",
                "space_before_pt": 0,
                "space_after_pt": 8,
                "paragraph_style": guess_paragraph_style(gname, lname, text),
                "text": text,
                "runs": m.get("runs") or [],
            }
            # Keep raw debug fields for audits (agents may strip later)
            for k in (
                "faux_bold",
                "scale_x",
                "scale_y",
                "size_raw",
                "leading_raw",
                "metrics_err",
            ):
                if m.get(k) is not None:
                    frame[k] = jsafe(m[k])
            frames.append(frame)
    return frames


def dedupe_frames(frames: list[dict]) -> list[dict]:
    """Drop identical group+side+text+bbox duplicates (common PS 'copy' layers)."""
    seen: set[tuple] = set()
    out: list[dict] = []
    for f in frames:
        key = (
            f.get("group"),
            f.get("page"),
            (f.get("text") or "").strip(),
            tuple(f.get("bbox_page_px") or []),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def frames_to_unit_doc(
    unit_key: str,
    frames: list[dict],
    *,
    canvas: list[int],
    dpi: float,
    bleed_in: float,
    source: str,
) -> dict:
    return {
        "schema": "tnims-type-inventory/v1",
        "unit": unit_key,
        "source_psb": source,
        "canvas_px": canvas,
        "dpi": dpi,
        "bleed_in": bleed_in,
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "frames": frames,
        "notes": "Generated by scripts/export_type_inventory_from_psb.py",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--psb", type=Path, default=DEFAULT_PSB)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument(
        "--unit",
        default="",
        help="Comma-separated PSB group names (e.g. S01,S04,P02)",
    )
    ap.add_argument(
        "--split-units",
        action="store_true",
        help="Also write Media/development/{unit}/type-inventory.json per group",
    )
    ap.add_argument(
        "--dev-root",
        type=Path,
        default=ROOT / "Media/development",
    )
    ap.add_argument("--dpi", type=float, default=DPI_DEFAULT)
    ap.add_argument("--bleed", type=float, default=BLEED_IN_DEFAULT)
    ap.add_argument(
        "--visible-only",
        action="store_true",
        help="Skip hidden type layers (default: include all, flag visible)",
    )
    ap.add_argument(
        "--include-guides",
        action="store_true",
        help="Include guide/glow-shell layers",
    )
    ap.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Keep identical text+bbox duplicates (default: dedupe)",
    )
    ap.add_argument(
        "--legacy-flat",
        action="store_true",
        help="Also write legacy array-style type-inventory.next-to-out",
    )
    args = ap.parse_args()

    if not args.psb.is_file():
        print(f"ERROR: PSB not found: {args.psb}", file=sys.stderr)
        return 1

    units = {u.strip() for u in args.unit.split(",") if u.strip()} or None

    from psd_tools import PSDImage

    print(f"Opening {args.psb} ...", flush=True)
    psd = PSDImage.open(args.psb)
    print(f"size {psd.width}x{psd.height}", flush=True)
    roots, src_name = find_scan_roots(psd)
    print(f"scan: {src_name} ({len(roots)} groups)", flush=True)

    frames = collect_frames(
        psd,
        units=units,
        visible_only=args.visible_only,
        include_guides=args.include_guides,
        dpi=args.dpi,
        bleed_in=args.bleed,
    )
    if not args.keep_duplicates:
        before = len(frames)
        frames = dedupe_frames(frames)
        if before != len(frames):
            print(f"deduped {before} -> {len(frames)} frames", flush=True)

    payload = {
        "schema": "tnims-type-inventory/v1",
        "source_psb": str(args.psb).replace("\\", "/"),
        "canvas_px": [psd.width, psd.height],
        "dpi": args.dpi,
        "bleed_in": args.bleed,
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scan_root": src_name,
        "frame_count": len(frames),
        "frames": frames,
        "notes": "Master inventory — use --split-units for per-development folders",
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {len(frames)} frames -> {args.out}", flush=True)

    if args.legacy_flat:
        legacy = [
            {
                "group": f["group"],
                "text": f["text"],
                "bbox_spread": f.get("bbox_spread_px"),
                "bbox_page": f.get("bbox_page_px"),
                "side": f["page"],
                "layer_name": f["ps_layer"],
                "visible": f["visible"],
                "size_pt": f.get("size_pt"),
                "leading_pt": f.get("leading_pt"),
                "tracking": f.get("tracking"),
                "font": f.get("font"),
                "color": f.get("color"),
                "align": f.get("align"),
            }
            for f in frames
        ]
        leg_path = args.out.with_name(args.out.stem + "-legacy-flat.json")
        leg_path.write_text(
            json.dumps(legacy, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Legacy flat -> {leg_path}", flush=True)

    if args.split_units:
        by_group: dict[str, list] = {}
        for f in frames:
            by_group.setdefault(f["group"], []).append(f)
        for gname, gframes in sorted(by_group.items()):
            folder = UNIT_DEV_FOLDERS.get(gname, gname)
            dest_dir = args.dev_root / folder
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Re-id frames within unit
            unit_frames = []
            for i, f in enumerate(gframes, 1):
                nf = dict(f)
                nf["id"] = f"{folder}-{f['page']}-{i:02d}"
                unit_frames.append(nf)
            doc = frames_to_unit_doc(
                folder,
                unit_frames,
                canvas=payload["canvas_px"],
                dpi=args.dpi,
                bleed_in=args.bleed,
                source=payload["source_psb"],
            )
            dest = dest_dir / "type-inventory.json"
            dest.write_text(
                json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            print(f"  {gname:28} -> {dest} ({len(unit_frames)})", flush=True)

    for f in frames:
        preview = (f.get("text") or "")[:70].replace("\n", " / ")
        sz = f.get("size_pt") or 0
        print(
            f"{f['group']:28} {f['page']:5} "
            f"{sz:5.1f}pt tr={f.get('tracking')} "
            f"vis={f['visible']} {preview}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
