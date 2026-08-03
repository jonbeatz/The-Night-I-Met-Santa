#!/usr/bin/env python3
"""Build / apply type-inventory → InDesign live frames (emit JSX).

Does not require COM. Writes a self-contained JSX that:
  - forces POINTS units (pica gotcha)
  - ensures TYPE layer + style kit
  - creates text frames from inventory bounds_in / bbox
  - applies paragraph + character styles
  - labels frames so re-runs can replace

Usage:
  python scripts/apply_type_inventory_to_indd.py --inventory PATH
  python scripts/apply_type_inventory_to_indd.py --inventory PATH --page 10
  python scripts/apply_type_inventory_to_indd.py --inventory PATH --dry-run
  python scripts/apply_type_inventory_to_indd.py --ensure-styles-only

Then run the JSX via InDesign exec MCP `run_jsx` (paste file contents)
or File → Scripts → `_generated/apply-type-inventory.jsx`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.type_inventory_common import (  # noqa: E402
    BLEED_IN_DEFAULT,
    DPI_DEFAULT,
    px_box_to_page_inches,
)

DEFAULT_OUT = ROOT / "Xtraz/Adobe-inDesign/_generated/apply-type-inventory.jsx"
DEFAULT_INV = (
    ROOT / "Xtraz/Adobe-Finals/FINAL-Master-Chopz/_type-inventory.json"
)

STYLE_KIT_JS = r"""
function ensureStyleKit(doc) {
  function ensurePara(name, opts) {
    var s;
    try { s = doc.paragraphStyles.itemByName(name); if (s.isValid) return s; } catch (e) {}
    s = doc.paragraphStyles.add({ name: name });
    if (opts.font) {
      try { s.appliedFont = opts.font; } catch (e2) {}
    }
    if (opts.size != null) s.pointSize = opts.size;
    if (opts.leading != null) s.leading = opts.leading;
    if (opts.tracking != null) s.tracking = opts.tracking;
    if (opts.align != null) s.justification = opts.align;
    if (opts.spaceAfter != null) s.spaceAfter = opts.spaceAfter;
    return s;
  }
  function ensureChar(name) {
    var s;
    try { s = doc.characterStyles.itemByName(name); if (s.isValid) return s; } catch (e) {}
    return doc.characterStyles.add({ name: name });
  }
  var fontName = "Cormorant Infant";
  var center = Justification.CENTER_ALIGN;
  var left = Justification.LEFT_ALIGN;
  ensurePara("Poem-Body", { font: fontName, size: 20, leading: 26, tracking: 50, align: center, spaceAfter: 8 });
  ensurePara("Poem-Body-Tight", { font: fontName, size: 18, leading: 24, tracking: 40, align: center, spaceAfter: 6 });
  ensurePara("Poem-Display", { font: fontName, size: 28, leading: 34, tracking: 40, align: center, spaceAfter: 10 });
  ensurePara("Matter-Body", { font: fontName, size: 14, leading: 20, tracking: 20, align: center, spaceAfter: 8 });
  ensurePara("Matter-Signoff", { font: fontName, size: 14, leading: 20, tracking: 40, align: center, spaceAfter: 0 });
  ensurePara("Title-Main", { font: fontName, size: 36, leading: 42, tracking: 20, align: center, spaceAfter: 12 });
  ensureChar("Poem-Emph");
  ensureChar("Poem-Small");
  try { doc.characterStyles.itemByName("Poem-Emph").fontStyle = "Bold"; } catch (e3) {}
  try { doc.characterStyles.itemByName("Poem-Small").pointSize = 16; } catch (e4) {}
  return true;
}
"""


def js_escape(s: str) -> str:
    return (
        (s or "")
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def justification_const(align: str) -> str:
    a = (align or "center").lower()
    if a == "left":
        return "Justification.LEFT_ALIGN"
    if a == "right":
        return "Justification.RIGHT_ALIGN"
    if a.startswith("just"):
        return "Justification.FULLY_JUSTIFIED"
    return "Justification.CENTER_ALIGN"


def normalize_frames(data: dict | list) -> list[dict]:
    if isinstance(data, list):
        # legacy flat
        frames = []
        for i, t in enumerate(data, 1):
            local = t.get("bbox_page") or t.get("bbox_page_px")
            frames.append(
                {
                    "id": f"legacy-{i:02d}",
                    "group": t.get("group"),
                    "page": t.get("side") or t.get("page"),
                    "ps_layer": t.get("layer_name") or t.get("ps_layer"),
                    "text": t.get("text"),
                    "bbox_page_px": local,
                    "bounds_in": px_box_to_page_inches(local)
                    if local
                    else None,
                    "font": t.get("font"),
                    "size_pt": t.get("size_pt"),
                    "leading_pt": t.get("leading_pt"),
                    "tracking": t.get("tracking"),
                    "color": t.get("color") or "#2C1810",
                    "align": t.get("align") or "center",
                    "paragraph_style": t.get("paragraph_style") or "Poem-Body",
                    "runs": t.get("runs") or [],
                    "book_page": t.get("book_page"),
                }
            )
        return frames
    return list(data.get("frames") or [])


def load_inventory(path: Path) -> tuple[dict, list[dict]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    meta = raw if isinstance(raw, dict) else {"schema": "legacy-flat"}
    return meta, normalize_frames(raw)


def emit_jsx(
    frames: list[dict],
    *,
    book_pages: list[int] | None,
    groups: set[str] | None,
    ensure_styles_only: bool,
    replace_labeled: bool,
    layer_name: str,
) -> str:
    selected = []
    for f in frames:
        if groups and (f.get("group") not in groups) and (
            f.get("unit") not in groups
        ):
            continue
        if book_pages is not None:
            bp = f.get("book_page")
            if bp is None:
                # skip unless --allow-unmapped
                continue
            if int(bp) not in book_pages:
                continue
        selected.append(f)

    lines = [
        "// Generated by scripts/apply_type_inventory_to_indd.py",
        "// Assign result to __result for indesign-exec MCP.",
        "if (app.documents.length < 1) { throw new Error('Open an InDesign document first'); }",
        "var doc = app.activeDocument;",
        "var oldHU = doc.viewPreferences.horizontalMeasurementUnits;",
        "var oldVU = doc.viewPreferences.verticalMeasurementUnits;",
        "doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;",
        "doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;",
        STYLE_KIT_JS,
        "ensureStyleKit(doc);",
    ]
    if ensure_styles_only:
        lines += [
            "doc.viewPreferences.horizontalMeasurementUnits = oldHU;",
            "doc.viewPreferences.verticalMeasurementUnits = oldVU;",
            "__result = { ok: true, styles: true };",
        ]
        return "\n".join(lines)

    lines += [
        f'var layerName = "{js_escape(layer_name)}";',
        "var typeLayer;",
        "try { typeLayer = doc.layers.itemByName(layerName); if (!typeLayer.isValid) throw 0; } catch (eL) { typeLayer = doc.layers.add({ name: layerName }); }",
        "doc.activeLayer = typeLayer;",
        "var created = [];",
        "var errors = [];",
        """
function inchToPt(v) { return v * 72.0; }
function ensureColor(doc, hex) {
  var name = "TI-" + hex.replace("#", "");
  try {
    var sw = doc.colors.itemByName(name);
    if (sw.isValid) return sw;
  } catch (e) {}
  var r = parseInt(hex.substr(1,2), 16) / 255;
  var g = parseInt(hex.substr(3,2), 16) / 255;
  var b = parseInt(hex.substr(5,2), 16) / 255;
  return doc.colors.add({
    name: name,
    model: ColorModel.PROCESS,
    space: ColorSpace.RGB,
    colorValue: [r*255, g*255, b*255]
  });
}
function removeLabeled(doc, label) {
  var items = doc.allPageItems;
  for (var i = items.length - 1; i >= 0; i--) {
    try {
      if (items[i].label === label) items[i].remove();
    } catch (eR) {}
  }
}
function applyRuns(tf, runs) {
  if (!runs || !runs.length) return;
  var story = tf.parentStory;
  for (var i = 0; i < runs.length; i++) {
    var r = runs[i];
    try {
      var from = Math.max(0, r.start);
      var to = Math.min(story.characters.length, r.end);
      if (to <= from) continue;
      var st = doc.characterStyles.itemByName(r.character_style || "Poem-Emph");
      story.characters.itemByRange(from, to - 1).appliedCharacterStyle = st;
    } catch (eRun) {}
  }
}
""",
    ]

    if not selected and book_pages is None and not groups:
        selected = frames

    for f in selected:
        bounds = f.get("bounds_in")
        if not bounds and f.get("bbox_page_px"):
            bounds = px_box_to_page_inches(f["bbox_page_px"])
        if not bounds:
            continue
        text = clean_for_jsx_text(f.get("text") or "")
        if not text.strip():
            continue
        label = f"ti:{f.get('id') or f.get('ps_layer') or 'frame'}"
        book_page = f.get("book_page")
        # geometricBounds: [y1, x1, y2, x2] in POINTS after unit switch
        top = bounds["top"] * 72
        left = bounds["left"] * 72
        bottom = bounds["bottom"] * 72
        right = bounds["right"] * 72
        para = f.get("paragraph_style") or "Poem-Body"
        size = f.get("size_pt")
        leading = f.get("leading_pt")
        tracking = f.get("tracking")
        color = f.get("color") or "#2C1810"
        just = justification_const(f.get("align") or "center")
        font = f.get("font") or "Cormorant Infant"
        runs_json = json.dumps(f.get("runs") or [])

        page_resolve = (
            f"doc.pages.itemByName(\"{book_page}\")"
            if book_page is not None
            else "doc.layoutWindows[0].activePage"
        )

        lines.append(
            f"""
(function() {{
  try {{
    var label = "{js_escape(label)}";
    {"removeLabeled(doc, label);" if replace_labeled else ""}
    var page = {page_resolve};
    if (!page.isValid) throw new Error("page not found");
    var gb = [{top:.4f}, {left:.4f}, {bottom:.4f}, {right:.4f}];
    var tf = page.textFrames.add({{ geometricBounds: gb, itemLayer: typeLayer }});
    tf.label = label;
    tf.contents = "{js_escape(text)}";
    try {{ tf.paragraphs.everyItem().appliedParagraphStyle = doc.paragraphStyles.itemByName("{js_escape(para)}"); }} catch (eP) {{}}
    try {{ tf.parentStory.appliedFont = "{js_escape(font)}"; }} catch (eF) {{}}
    {f"try {{ tf.parentStory.pointSize = {float(size)}; }} catch (eS) {{}}" if size else ""}
    {f"try {{ tf.parentStory.leading = {float(leading)}; }} catch (eL2) {{}}" if leading else ""}
    {f"try {{ tf.parentStory.tracking = {float(tracking)}; }} catch (eT) {{}}" if tracking is not None else ""}
    try {{ tf.parentStory.justification = {just}; }} catch (eJ) {{}}
    try {{
      var col = ensureColor(doc, "{js_escape(color)}");
      tf.parentStory.fillColor = col;
    }} catch (eC) {{}}
    var runs = {runs_json};
    applyRuns(tf, runs);
    created.push({{ id: label, page: page.name }});
  }} catch (err) {{
    errors.push(String(err));
  }}
}})();
"""
        )

    lines += [
        "doc.viewPreferences.horizontalMeasurementUnits = oldHU;",
        "doc.viewPreferences.verticalMeasurementUnits = oldVU;",
        "__result = { ok: errors.length === 0, created: created, errors: errors, count: created.length };",
    ]
    return "\n".join(lines)


def clean_for_jsx_text(raw: str) -> str:
    from lib.type_inventory_common import clean_text

    return clean_text(raw)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", type=Path, default=DEFAULT_INV)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument(
        "--page",
        default="",
        help="Comma-separated book page numbers (requires book_page on frames)",
    )
    ap.add_argument(
        "--group",
        default="",
        help="Comma-separated PSB groups / units (e.g. S01,S04)",
    )
    ap.add_argument(
        "--active-page",
        action="store_true",
        help="Place all selected frames on the active page (ignore book_page)",
    )
    ap.add_argument("--ensure-styles-only", action="store_true")
    ap.add_argument(
        "--no-replace",
        action="store_true",
        help="Do not remove existing frames with same ti: label",
    )
    ap.add_argument("--layer", default="TYPE")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary only; still write JSX unless --no-write",
    )
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument(
        "--map-pages",
        type=Path,
        default=None,
        help="Optional indesign-page-map.json to stamp book_page onto frames",
    )
    args = ap.parse_args()

    meta, frames = ({}, [])
    if not args.ensure_styles_only:
        if not args.inventory.is_file():
            print(f"ERROR: inventory not found: {args.inventory}", file=sys.stderr)
            return 1
        meta, frames = load_inventory(args.inventory)
        if args.map_pages and args.map_pages.is_file():
            frames = stamp_book_pages(frames, args.map_pages)

    book_pages = None
    if args.page.strip():
        book_pages = [int(x.strip()) for x in args.page.split(",") if x.strip()]
    groups = {g.strip() for g in args.group.split(",") if g.strip()} or None

    # active-page mode: clear book_page so JSX uses activePage
    if args.active_page:
        for f in frames:
            f["book_page"] = None
        book_pages = None

    jsx = emit_jsx(
        frames,
        book_pages=book_pages,
        groups=groups,
        ensure_styles_only=args.ensure_styles_only,
        replace_labeled=not args.no_replace,
        layer_name=args.layer,
    )

    if args.dry_run:
        print(
            f"inventory={args.inventory} frames={len(frames)} "
            f"groups={groups} pages={book_pages} meta_unit={meta.get('unit')}"
        )

    if not args.no_write:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(jsx, encoding="utf-8")
        print(f"Wrote JSX -> {args.out}", flush=True)
        print(
            "Next: open Interior INDD, then MCP run_jsx (paste file contents into code=) "
            "or File > Scripts > Apply-Type-Inventory.jsx",
            flush=True,
        )
    return 0


def stamp_book_pages(frames: list[dict], map_path: Path) -> list[dict]:
    data = json.loads(map_path.read_text(encoding="utf-8"))
    pages = data.get("pages") or []
    # Map group+side → book page
    lookup: dict[tuple[str, str], int] = {}
    for pg in pages:
        unit = pg.get("unit")
        side = pg.get("side")
        pnum = pg.get("page")
        if unit and side and pnum is not None:
            lookup[(unit, side)] = int(pnum)
            # also raw group aliases
            lookup[(unit.split("-")[0], side)] = int(pnum)
    for f in frames:
        side = f.get("page") or f.get("side")
        for key in (f.get("group"), f.get("unit")):
            if key and side and (key, side) in lookup:
                f["book_page"] = lookup[(key, side)]
                break
    return frames


if __name__ == "__main__":
    raise SystemExit(main())
