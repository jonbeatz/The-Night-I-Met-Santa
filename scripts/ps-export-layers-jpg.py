"""Export each top-level Photoshop layer as its own JPG (solo-visibility loop).

Requires: Photoshop open + adobepy broker (npm run layout:photoshop-mcp).

Examples:
  python scripts/ps-export-layers-jpg.py
  python scripts/ps-export-layers-jpg.py --doc Pugicorn-Book-Refrence.psb --out Images/references/Pugicorn-Book-Refrence/cropped
  python scripts/ps-export-layers-jpg.py --doc My.psd --out D:\\out --start "Layer Name"
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from adobe.photoshop import Photoshop

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOC = "Pugicorn-Book-Refrence.psb"
DEFAULT_OUT = ROOT / "Images" / "references" / "Pugicorn-Book-Refrence" / "cropped"


def bp(app, cmds, name: str):
    return app.batch_play(cmds, modal=True, command_name=name)


def safe_filename(name: str) -> str:
    name = (name or "layer").strip()
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:120]


def set_layer_visible(app, layer_name: str, visible: bool):
    bp(
        app,
        [
            {
                "_obj": "select",
                "_target": [{"_ref": "layer", "_name": layer_name}],
                "makeVisible": visible,
            },
            {
                "_obj": "show" if visible else "hide",
                "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
            },
        ],
        f"{'Show' if visible else 'Hide'} {layer_name[:48]}",
    )


def resolve_doc_name(app, requested: str | None) -> str:
    names = [d.name for d in app.documents]
    if not names:
        raise SystemExit("No Photoshop documents open.")
    if requested:
        if requested in names:
            return requested
        # partial match
        for n in names:
            if requested.lower() in n.lower():
                return n
        raise SystemExit(f"Doc {requested!r} not open. Open: {names}")
    if DEFAULT_DOC in names:
        return DEFAULT_DOC
    if len(names) == 1:
        return names[0]
    raise SystemExit(f"Pass --doc. Open docs: {names}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Export each PS layer as JPG (solo eyeball)")
    ap.add_argument("--doc", default=None, help="Open document name (.psd/.psb)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output folder for JPGs")
    ap.add_argument(
        "--start",
        default=None,
        help="Layer name to start from (default: currently visible, else bottom)",
    )
    ap.add_argument(
        "--quality",
        type=int,
        default=10,
        help="JPEG quality 0-12 for export options (default 10)",
    )
    args = ap.parse_args()

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    app = Photoshop()
    doc_name = resolve_doc_name(app, args.doc)
    bp(
        app,
        [{"_obj": "select", "_target": [{"_ref": "document", "_name": doc_name}]}],
        "Select document",
    )
    doc = app.activeDocument
    print(f"active: {doc.name} {doc.width}x{doc.height}")
    print(f"out: {out_dir}")

    # top -> bottom (index 0 = top of Layers panel)
    layers = []
    for L in doc.layers:
        layers.append(
            {
                "name": getattr(L, "name", "") or "",
                "kind": str(getattr(L, "kind", "")),
                "visible": bool(getattr(L, "visible", False)),
            }
        )

    print(f"layers top->bottom ({len(layers)}):")
    for i, L in enumerate(layers):
        print(f"  {i:02d} vis={L['visible']} {L['kind']:12} {L['name']}")

    names = [L["name"] for L in layers if L["name"]]
    if not names:
        raise SystemExit("No named layers found.")

    start_idx = None
    if args.start:
        for i, L in enumerate(layers):
            if L["name"] == args.start or args.start.lower() in L["name"].lower():
                start_idx = i
                break
        if start_idx is None:
            raise SystemExit(f"Start layer not found: {args.start!r}")
    else:
        for i, L in enumerate(layers):
            if L["visible"]:
                start_idx = i
                break
        if start_idx is None:
            start_idx = len(layers) - 1

    # Walk UP the panel from start (toward top = decreasing index), then leftovers below
    order = list(range(start_idx, -1, -1)) + list(range(start_idx + 1, len(layers)))
    print(f"start: {layers[start_idx]['name']}")
    print("order:", [layers[i]["name"] for i in order])

    print("\nHiding all...")
    for name in names:
        try:
            set_layer_visible(app, name, False)
        except Exception as e:
            print(f"  hide warn {name}: {e}")

    exported: list[str] = []
    errors: list[str] = []

    for i in order:
        name = layers[i]["name"]
        if not name:
            continue
        out_path = out_dir / f"{safe_filename(name)}.jpg"
        print(f"\n=== {name} -> {out_path.name}")

        try:
            for n in names:
                set_layer_visible(app, n, n == name)
            time.sleep(0.15)

            try:
                doc.export(
                    str(out_path),
                    format="jpg",
                    options={"quality": args.quality},
                    as_copy=True,
                    modal=True,
                    command_name=f"Export {name[:40]}",
                )
            except Exception as e1:
                print(f"  export() failed ({e1}); trying save_as jpg...")
                doc.save_as(
                    str(out_path),
                    format="jpg",
                    options={"quality": args.quality},
                    as_copy=True,
                    modal=True,
                    command_name=f"SaveAs {name[:40]}",
                )

            if out_path.exists() and out_path.stat().st_size > 500:
                print(f"  OK {out_path.stat().st_size:,} bytes")
                exported.append(out_path.name)
            else:
                alts = list(out_dir.glob(safe_filename(name) + ".*"))
                print(f"  MISSING/empty primary; alts={alts}")
                if alts:
                    exported.append(alts[0].name)
                else:
                    errors.append(name)
        except Exception as e:
            print(f"  ERR {e}")
            errors.append(f"{name}: {e}")

    print(f"\nDone. exported={len(exported)}/{len(order)} errors={len(errors)}")
    for e in errors:
        print("  error:", e)
    print("JPGs:", sorted(p.name for p in out_dir.glob("*.jpg")))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
