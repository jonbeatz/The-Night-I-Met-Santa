# Finish spread template overlays + save (guides already present).
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from adobe.photoshop import Photoshop

OUT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\spread-page-template.psd")
MCP = "http://127.0.0.1:8766/v1/call"

W, H = 5250, 2625
TRIM, SAFE, PAGE = 37.5, 150.0, 2625.0


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
    """Four thin filled strips forming a hollow rectangle."""
    rr, gg, bb = color
    cmds = []
    # top, bottom, left, right
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


app = Photoshop(token="dev-token")
doc = app.active_document
assert doc and "spread-page-template" in doc.name, doc.name if doc else None
print("working on", doc.name, f"{doc.width}x{doc.height}@{doc.resolution}")

# Rename background if present
layers = [getattr(x, "name", str(x)) for x in doc.layers]
print("layers before:", layers)
try:
    if layers and layers[-1] in ("Background", "Layer 1", "white-bg"):
        mcp(
            "photoshop_layers__rename_layer",
            {"name": layers[-1], "new_name": "white-bg"},
        )
except Exception as e:
    print("rename bg:", e)

cmds: list = []

# Paper base
cmds += make_layer("paper-base")
cmds.append(select_rect(0, 0, W, H))
cmds.append(fill_rgb(252, 250, 245))
cmds.append(deselect())

# ART placeholder (empty)
cmds += make_layer("ART - full-bleed scene here")

# TRIM cyan boxes L/R
cmds += make_layer("TRIM-L 8.5in")
cmds += box_border(TRIM, TRIM, PAGE - TRIM, H - TRIM, (0, 180, 220))
cmds += make_layer("TRIM-R 8.5in")
cmds += box_border(PAGE + TRIM, TRIM, W - TRIM, H - TRIM, (0, 180, 220))

# SAFETY magenta boxes L/R
cmds += make_layer("SAFETY-L 0.5in from trim")
cmds += box_border(TRIM + SAFE, TRIM + SAFE, PAGE - TRIM - SAFE, H - TRIM - SAFE, (220, 40, 160))
cmds += make_layer("SAFETY-R 0.5in from trim")
cmds += box_border(PAGE + TRIM + SAFE, TRIM + SAFE, W - TRIM - SAFE, H - TRIM - SAFE, (220, 40, 160))

# Fold (hide for finals) — may already exist from prior probe; recreate clean
cmds += make_layer("FOLD MOCK only - hide for finals")
cmds.append(select_rect(PAGE - 1, 0, PAGE + 1, H))
cmds.append(fill_rgb(255, 140, 0))
cmds.append(deselect())

for name in [
    "CLOUD - watercolor wash optional",
    "TYPE zone LEFT - live Cormorant in InDesign",
    "TYPE zone RIGHT - live Cormorant in InDesign",
]:
    cmds += make_layer(name)

print("running", len(cmds), "batchPlay cmds...")
bp(app, cmds, "TNIMS spread overlays")

# Hide overlay guide layers so ART is clean to paint; leave guides (rulers) visible
doc = app.active_document
for layer in doc.layers:
    name = getattr(layer, "name", "")
    if name.startswith(("TRIM-", "SAFETY-", "FOLD ", "paper-base")):
        try:
            mcp("photoshop_layers__set_layer_visibility", {"name": name, "visible": True})
        except Exception:
            pass
# Keep overlays visible so Jon sees the system; he can hide group later

# Opacity on overlays so art shows through borders
for name in [
    "TRIM-L 8.5in",
    "TRIM-R 8.5in",
    "SAFETY-L 0.5in from trim",
    "SAFETY-R 0.5in from trim",
    "FOLD MOCK only - hide for finals",
]:
    try:
        mcp("photoshop_layers__set_layer_opacity", {"name": name, "opacity": 85})
    except Exception as e:
        print("opacity", name, e)

# Save PSD
print("saving...", OUT)
try:
    doc.save_as(str(OUT))
except Exception as e:
    print("save_as err", e)
    print(mcp("photoshop_image__export_document", {"path": str(OUT), "format": "psd"}))

print("exists", OUT.exists(), "bytes", OUT.stat().st_size if OUT.exists() else 0)
doc = app.active_document
print("final", doc.name, doc.width, "x", doc.height, "@", doc.resolution, doc.mode)
print("layers:", [getattr(l, "name", l) for l in doc.layers])
