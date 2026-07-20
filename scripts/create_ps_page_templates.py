"""
Create TNIMS Photoshop blanks matching InDesign / Lulu:
  - single-page-template.psd  (2625×2625)
  - book-covers-template.psd  (2625×2625 front/back art blank)

No spine-only PSD: Lulu sets spine width after interior upload; spine lives
in the one-piece casewrap, not a separate working file.

Requires: Photoshop open + adobepy broker + dcc-mcp-photoshop (:8766).
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from adobe.photoshop import Photoshop

OUT_DIR = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop")
MCP = "http://127.0.0.1:8766/v1/call"

# Lulu 8.5" square @ 300 DPI
PAGE = 2625  # 8.75" full-bleed
TRIM = 37.5  # 0.125"
SAFE = 150.0  # 0.5" from trim


def mcp(tool: str, args: dict):
    body = json.dumps({"tool_slug": tool, "arguments": args}).encode()
    req = urllib.request.Request(MCP, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode())


def bp(app, cmds, name="TNIMS template"):
    return app.action.batch_play(
        cmds,
        {"synchronousExecution": True},
        modal=True,
        command_name=name,
        timeout_ms=180000,
    )


def make_layer(name: str):
    return [
        {"_obj": "make", "_target": [{"_ref": "layer"}]},
        {
            "_obj": "set",
            "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
            "to": {"_obj": "layer", "name": name},
        },
    ]


def select_rect(l, t, r, b):
    return {
        "_obj": "set",
        "_target": [{"_ref": "channel", "_property": "selection"}],
        "to": {
            "_obj": "rectangle",
            "top": {"_unit": "pixelsUnit", "_value": float(t)},
            "left": {"_unit": "pixelsUnit", "_value": float(l)},
            "bottom": {"_unit": "pixelsUnit", "_value": float(b)},
            "right": {"_unit": "pixelsUnit", "_value": float(r)},
        },
    }


def fill_rgb(r, g, b):
    return {
        "_obj": "fill",
        "using": {"_enum": "fillContents", "_value": "color"},
        "color": {"_obj": "RGBColor", "red": float(r), "grain": float(g), "blue": float(b)},
        "opacity": {"_unit": "percentUnit", "_value": 100},
        "mode": {"_enum": "blendMode", "_value": "normal"},
    }


def deselect():
    return {
        "_obj": "set",
        "_target": [{"_ref": "channel", "_property": "selection"}],
        "to": {"_enum": "ordinal", "_value": "none"},
    }


def box_border(l, t, r, b, color, thickness=3.0):
    rr, gg, bb = color
    cmds = []
    strips = [
        (l, t, r, t + thickness),
        (l, b - thickness, r, b),
        (l, t, l + thickness, b),
        (r - thickness, t, r, b),
    ]
    for sl, st, sr, sb in strips:
        cmds.append(select_rect(sl, st, sr, sb))
        cmds.append(fill_rgb(rr, gg, bb))
    cmds.append(deselect())
    return cmds


def guide(orientation: str, position: float):
    return {
        "_obj": "make",
        "_target": [{"_ref": "guide"}],
        "new": {
            "_obj": "guide",
            "position": {"_unit": "pixelsUnit", "_value": float(position)},
            "orientation": {"_enum": "orientation", "_value": orientation},
        },
    }


def close_named(app, needle: str):
    for d in list(app.documents):
        name = getattr(d, "name", "")
        if needle in name:
            bp(
                app,
                [
                    {
                        "_obj": "close",
                        "_target": [{"_ref": "document", "_enum": "ordinal", "_value": "targetEnum"}],
                        "saving": {"_enum": "yesNo", "_value": "no"},
                    }
                ],
                f"close {needle}",
            )
            print("closed", name)


def create_doc(name: str, w: int, h: int):
    r = mcp(
        "photoshop_image__create_document",
        {
            "name": name,
            "width": w,
            "height": h,
            "resolution": 300,
            "color_mode": "rgb",
            "bit_depth": 8,
            "fill": "white",
        },
    )
    print("create", name, r.get("output", r))
    return r


def add_square_guides(app):
    """Bleed/trim/safety guides for a 2625² page (no fold)."""
    cmds = [{"_obj": "clearAllGuides"}]
    # vertical: bleed=0/edge, trim, safety, safety far, trim far
    for x in (TRIM, TRIM + SAFE, PAGE - TRIM - SAFE, PAGE - TRIM):
        cmds.append(guide("vertical", x))
    for y in (TRIM, TRIM + SAFE, PAGE - TRIM - SAFE, PAGE - TRIM):
        cmds.append(guide("horizontal", y))
    bp(app, cmds, "square guides")
    print("guides ok", len(cmds))


def rename_bg(app):
    doc = app.active_document
    layers = [getattr(x, "name", str(x)) for x in doc.layers]
    if layers and layers[-1] in ("Background", "Layer 1", "white-bg"):
        try:
            mcp("photoshop_layers__rename_layer", {"name": layers[-1], "new_name": "white-bg"})
        except Exception as e:
            print("rename bg:", e)


def save_psd(app, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = app.active_document
    try:
        doc.save_as(str(path))
    except Exception as e:
        print("save_as err", e)
        print(mcp("photoshop_image__export_document", {"path": str(path), "format": "psd"}))
    print("saved", path, "exists", path.exists(), "bytes", path.stat().st_size if path.exists() else 0)


def build_single_page(app):
    """Interior single page — poem/art at full bleed."""
    name = "single-page-template"
    out = OUT_DIR / f"{name}.psd"
    close_named(app, name)
    create_doc(name, PAGE, PAGE)
    add_square_guides(app)
    rename_bg(app)

    cmds: list = []
    cmds += make_layer("paper-base")
    cmds.append(select_rect(0, 0, PAGE, PAGE))
    cmds.append(fill_rgb(252, 250, 245))
    cmds.append(deselect())

    cmds += make_layer("ART - full-bleed scene here")

    cmds += make_layer("TRIM 8.5in")
    cmds += box_border(TRIM, TRIM, PAGE - TRIM, PAGE - TRIM, (0, 180, 220))

    cmds += make_layer("SAFETY 0.5in from trim")
    cmds += box_border(TRIM + SAFE, TRIM + SAFE, PAGE - TRIM - SAFE, PAGE - TRIM - SAFE, (220, 40, 160))

    for layer_name in [
        "CLOUD - watercolor wash optional",
        "TYPE zone - live Cormorant in InDesign",
    ]:
        cmds += make_layer(layer_name)

    print("single overlays", len(cmds))
    bp(app, cmds, "TNIMS single-page overlays")

    for overlay in ("TRIM 8.5in", "SAFETY 0.5in from trim"):
        try:
            mcp("photoshop_layers__set_layer_opacity", {"name": overlay, "opacity": 85})
        except Exception as e:
            print("opacity", overlay, e)

    save_psd(app, out)
    doc = app.active_document
    print(
        "final",
        doc.name,
        doc.width,
        "x",
        doc.height,
        "@",
        doc.resolution,
        [getattr(l, "name", l) for l in doc.layers],
    )


def build_covers(app):
    """
    Front OR back cover art blank (same 2625² geometry as interior page).
    Final casewrap + exact spine = Lulu template after interior upload — not this file.
    Duplicate → Save As as cover-front-*.psd or cover-back-*.psd.
    """
    name = "book-covers-template"
    out = OUT_DIR / f"{name}.psd"
    close_named(app, name)
    create_doc(name, PAGE, PAGE)
    add_square_guides(app)
    rename_bg(app)

    cmds: list = []
    cmds += make_layer("paper-base")
    cmds.append(select_rect(0, 0, PAGE, PAGE))
    cmds.append(fill_rgb(252, 250, 245))
    cmds.append(deselect())

    cmds += make_layer("ART - cover scene here (front OR back)")

    cmds += make_layer("TRIM 8.5in")
    cmds += box_border(TRIM, TRIM, PAGE - TRIM, PAGE - TRIM, (0, 180, 220))

    cmds += make_layer("SAFETY 0.5in from trim")
    cmds += box_border(TRIM + SAFE, TRIM + SAFE, PAGE - TRIM - SAFE, PAGE - TRIM - SAFE, (220, 40, 160))

    # Soft hint: hinge area near spine edge when this panel is front (right of wrap)
    # and when back (left of wrap) — 0.25" hinge from spine = 75px inside trim on spine side.
    # Mark both edges lightly so Jon knows either orientation.
    cmds += make_layer("HINGE hint 0.25in - mock only hide for finals")
    cmds.append(select_rect(TRIM + 75 - 1, TRIM, TRIM + 75 + 1, PAGE - TRIM))
    cmds.append(fill_rgb(255, 140, 0))
    cmds.append(deselect())
    cmds.append(select_rect(PAGE - TRIM - 75 - 1, TRIM, PAGE - TRIM - 75 + 1, PAGE - TRIM))
    cmds.append(fill_rgb(255, 140, 0))
    cmds.append(deselect())

    for layer_name in [
        "TITLE zone FRONT - Cinzel live in InDesign (hide on back)",
        "CREDITS zone BACK - live type in InDesign (hide on front)",
        "NOTE - final wrap+spine from Lulu after interior upload",
    ]:
        cmds += make_layer(layer_name)

    print("cover overlays", len(cmds))
    bp(app, cmds, "TNIMS cover overlays")

    for overlay in (
        "TRIM 8.5in",
        "SAFETY 0.5in from trim",
        "HINGE hint 0.25in - mock only hide for finals",
    ):
        try:
            mcp("photoshop_layers__set_layer_opacity", {"name": overlay, "opacity": 85})
        except Exception as e:
            print("opacity", overlay, e)

    save_psd(app, out)
    doc = app.active_document
    print(
        "final",
        doc.name,
        doc.width,
        "x",
        doc.height,
        "@",
        doc.resolution,
        [getattr(l, "name", l) for l in doc.layers],
    )


def main():
    app = Photoshop(token="dev-token")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_single_page(app)
    build_covers(app)
    print("DONE")
    print("single", (OUT_DIR / "single-page-template.psd").exists())
    print("covers", (OUT_DIR / "book-covers-template.psd").exists())
    print("spine: SKIPPED (Lulu casewrap after interior — see docs)")


if __name__ == "__main__":
    main()
