#!/usr/bin/env python3
"""
Create TNIMS one-piece cover wrap Photoshop template (book-style art + live type).

Canvas matches current InDesign cover: 18.25" × 8.75" @ 300 DPI
  = BACK 8.75" | SPINE 0.75" | FRONT 8.75"  →  5475 × 2625 px

Workflow (same as interior pages):
  1. Duplicate / Save As working cover PSD
  2. Place real art into ART - BACK / ART - SPINE / ART - FRONT
  3. Dial MOCK-TYPE (Cinzel / Cormorant) — preview only
  4. Rebuild live type in InDesign cover doc for print PDF

Requires: Photoshop open + adobepy broker (:8766).
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from adobe.photoshop import Photoshop

OUT = Path(
    r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop"
    r"\cover-wrap-template.psd"
)
MCP = "http://127.0.0.1:8766/v1/call"

# Geometry @ 300 DPI — matches TNIMS-Cover-FINAL.indd
W, H, DPI = 5475, 2625, 300
BACK_W, SPINE_W, FRONT_W = 2625, 225, 2625  # 8.75 + 0.75 + 8.75
BLEED = 37.5  # 0.125"
SAFE = 150.0  # 0.5" from trim
HINGE = 75.0  # 0.25"

# Panel origins (left edges)
BACK_L = 0.0
SPINE_L = float(BACK_W)
FRONT_L = float(BACK_W + SPINE_W)

# 300 ppi type API quirk: Character N pt → pass N * (300/72)
PT = 300.0 / 72.0


def mcp(tool: str, args: dict, timeout: int = 180):
    body = json.dumps({"tool_slug": tool, "arguments": args}).encode()
    req = urllib.request.Request(
        MCP, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def bp(app, cmds, name="TNIMS cover wrap"):
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
    for sl, st, sr, sb in (
        (l, t, r, t + thickness),
        (l, b - thickness, r, b),
        (l, t, l + thickness, b),
        (r - thickness, t, r, b),
    ):
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


def panel_trim_safety(origin_x: float, panel_w: float):
    """Trim + safety boxes relative to a panel's left edge on the wrap."""
    tl = origin_x + BLEED
    tr = origin_x + panel_w - BLEED
    tt, tb = BLEED, H - BLEED
    sl = tl + SAFE
    sr = tr - SAFE
    st, sb = tt + SAFE, tb - SAFE
    return tl, tt, tr, tb, sl, st, sr, sb


def add_guides(app):
    cmds = [{"_obj": "clearAllGuides"}]
    # Panel joins
    cmds.append(guide("vertical", SPINE_L))
    cmds.append(guide("vertical", FRONT_L))
    # Per-panel trim + safety (back, front) + shared H
    for ox, pw in ((BACK_L, BACK_W), (FRONT_L, FRONT_W)):
        tl, tt, tr, tb, sl, st, sr, sb = panel_trim_safety(ox, pw)
        for x in (tl, sl, sr, tr):
            cmds.append(guide("vertical", x))
    for y in (BLEED, BLEED + SAFE, H - BLEED - SAFE, H - BLEED):
        cmds.append(guide("horizontal", y))
    # Hinge hints: back near spine (right of back trim), front near spine (left of front trim)
    cmds.append(guide("vertical", SPINE_L - BLEED - HINGE))  # back hinge
    cmds.append(guide("vertical", FRONT_L + BLEED + HINGE))  # front hinge
    bp(app, cmds, "cover wrap guides")
    print("guides", len(cmds))


def create_doc():
    r = mcp(
        "photoshop_image__create_document",
        {
            "name": "cover-wrap-template",
            "width": W,
            "height": H,
            "resolution": DPI,
            "color_mode": "rgb",
            "bit_depth": 8,
            "fill": "white",
        },
    )
    print("create", r.get("output", r))
    return r


def text_layer(
    content: str,
    name: str,
    x: float,
    y: float,
    *,
    font: str,
    size_pt: float,
    color: str = "#2C2C2C",
    alignment: str = "center",
):
    # Pass API size with 300ppi quirk so Character panel shows size_pt
    api_size = round(size_pt * PT, 2)
    r = mcp(
        "photoshop_text__create_text_layer",
        {
            "content": content,
            "name": name,
            "x": x,
            "y": y,
            "font": font,
            "size": api_size,
            "color": color,
            "alignment": alignment,
        },
    )
    print("text", name, r.get("output", r))
    return r


def save_psd(app, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = app.active_document
    try:
        doc.save_as(str(path))
    except Exception as e:
        print("save_as err", e)
        print(mcp("photoshop_image__export_document", {"path": str(path), "format": "psd"}))
    print("saved", path, path.exists(), path.stat().st_size if path.exists() else 0)


def main():
    app = Photoshop(token="dev-token")
    close_named(app, "cover-wrap-template")
    create_doc()
    add_guides(app)

    # Rename background
    try:
        layers = [getattr(x, "name", str(x)) for x in app.active_document.layers]
        if layers and layers[-1] in ("Background", "Layer 1", "white-bg"):
            mcp("photoshop_layers__rename_layer", {"name": layers[-1], "new_name": "white-bg"})
    except Exception as e:
        print("rename bg", e)

    cmds: list = []

    # Paper base
    cmds += make_layer("paper-base")
    cmds.append(select_rect(0, 0, W, H))
    cmds.append(fill_rgb(252, 250, 245))
    cmds.append(deselect())

    # --- ART slots (place real art here; keep empty until Jon drops plates) ---
    # Soft tint per panel so zones are obvious
    cmds += make_layer("ART - BACK (place scene here)")
    cmds.append(select_rect(BACK_L, 0, SPINE_L, H))
    cmds.append(fill_rgb(235, 225, 220))
    cmds.append(deselect())

    cmds += make_layer("ART - SPINE (place spine art here)")
    cmds.append(select_rect(SPINE_L, 0, FRONT_L, H))
    cmds.append(fill_rgb(40, 40, 40))
    cmds.append(deselect())

    cmds += make_layer("ART - FRONT (place scene here)")
    cmds.append(select_rect(FRONT_L, 0, W, H))
    cmds.append(fill_rgb(235, 225, 220))
    cmds.append(deselect())

    # Panel divider marks (hide for finals)
    cmds += make_layer("GUIDE - panel joins (hide for finals)")
    cmds.append(select_rect(SPINE_L - 1, 0, SPINE_L + 1, H))
    cmds.append(fill_rgb(0, 200, 255))
    cmds.append(deselect())
    cmds.append(select_rect(FRONT_L - 1, 0, FRONT_L + 1, H))
    cmds.append(fill_rgb(0, 200, 255))
    cmds.append(deselect())

    # Trim / safety boxes per panel
    for label, ox, pw, color in (
        ("BACK", BACK_L, BACK_W, (0, 180, 220)),
        ("FRONT", FRONT_L, FRONT_W, (0, 180, 220)),
    ):
        tl, tt, tr, tb, sl, st, sr, sb = panel_trim_safety(ox, pw)
        cmds += make_layer(f"TRIM - {label} 8.5in (hide for finals)")
        cmds += box_border(tl, tt, tr, tb, color)
        cmds += make_layer(f"SAFETY - {label} 0.5in (hide for finals)")
        cmds += box_border(sl, st, sr, sb, (220, 40, 160))

    # Hinge hints
    cmds += make_layer("HINGE hint 0.25in (hide for finals)")
    cmds.append(select_rect(SPINE_L - BLEED - HINGE - 1, BLEED, SPINE_L - BLEED - HINGE + 1, H - BLEED))
    cmds.append(fill_rgb(255, 140, 0))
    cmds.append(deselect())
    cmds.append(select_rect(FRONT_L + BLEED + HINGE - 1, BLEED, FRONT_L + BLEED + HINGE + 1, H - BLEED))
    cmds.append(fill_rgb(255, 140, 0))
    cmds.append(deselect())

    cmds += make_layer("CLOUD - watercolor wash optional")
    cmds += make_layer(
        "NOTE - MOCK-TYPE preview only; rebuild live type in InDesign for Lulu Cover PDF"
    )

    print("overlays", len(cmds))
    bp(app, cmds, "TNIMS cover wrap overlays")

    for overlay in (
        "GUIDE - panel joins (hide for finals)",
        "TRIM - BACK 8.5in (hide for finals)",
        "SAFETY - BACK 0.5in (hide for finals)",
        "TRIM - FRONT 8.5in (hide for finals)",
        "SAFETY - FRONT 0.5in (hide for finals)",
        "HINGE hint 0.25in (hide for finals)",
    ):
        try:
            mcp("photoshop_layers__set_layer_opacity", {"name": overlay, "opacity": 70})
        except Exception as e:
            print("opacity", overlay, e)

    # --- LIVE / MOCK-TYPE (same fonts as book cover catalog) ---
    # Front panel center-ish
    fx = FRONT_L + FRONT_W / 2
    text_layer(
        "The Night I Met Santa",
        "MOCK-TYPE - FRONT title (Cinzel)",
        fx,
        BLEED + SAFE + 180,
        font="CinzelDecorative-Bold",
        size_pt=42,
        color="#C9A227",
        alignment="center",
    )
    text_layer(
        "Written By Jack Farrell",
        "MOCK-TYPE - FRONT author (Cinzel)",
        fx,
        BLEED + SAFE + 320,
        font="CinzelDecorative-Regular",
        size_pt=16,
        color="#FFFFFF",
        alignment="center",
    )

    # Back panel
    bx = BACK_L + BACK_W / 2
    text_layer(
        "The Night I Met Santa",
        "MOCK-TYPE - BACK title (Cinzel)",
        bx,
        BLEED + SAFE + 180,
        font="CinzelDecorative-Bold",
        size_pt=36,
        color="#C9A227",
        alignment="center",
    )
    text_layer(
        "Written By Jack Farrell",
        "MOCK-TYPE - BACK author (Cinzel)",
        bx,
        H - BLEED - SAFE - 220,
        font="CinzelDecorative-Regular",
        size_pt=14,
        color="#1A1A1A",
        alignment="center",
    )
    text_layer(
        "First illustrated edition, 2026. Book design by Jon Farrell.",
        "MOCK-TYPE - BACK credits (Cormorant)",
        bx,
        H - BLEED - SAFE - 140,
        font="CormorantGaramond-Regular",
        size_pt=11,
        color="#1A1A1A",
        alignment="center",
    )

    # Spine — horizontal placeholder; Jon rotates -90° for vertical spine type
    sx = SPINE_L + SPINE_W / 2
    text_layer(
        "The Night I Met Santa  ·  Jack Farrell",
        "MOCK-TYPE - SPINE (rotate -90 for vertical)",
        sx,
        H / 2,
        font="CinzelDecorative-Regular",
        size_pt=10,
        color="#C41E3A",
        alignment="center",
    )

    save_psd(app, OUT)
    doc = app.active_document
    names = [getattr(l, "name", str(l)) for l in doc.layers]
    print("final", doc.name, doc.width, "x", doc.height, "@", doc.resolution)
    print("layers top→bottom:", names)
    print("DONE", OUT)


if __name__ == "__main__":
    main()
