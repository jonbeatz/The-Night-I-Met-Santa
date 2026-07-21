"""Reset P01 MOCK-TYPE to clean 36pt Cinzel at current visual center (no Free Transform)."""
from adobe.photoshop import Photoshop
from pathlib import Path
import json

PSD = r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p01-title.psd"
OUT_JSON = r"D:\Hermes\projects\The-Night-I-Met-Santa\Media\generated\mocks\P01-title\v01\mock-type-reset.json"

app = Photoshop()


def bp(cmds, name):
    return app.batch_play(cmds, modal=True, command_name=name)


# Select p01
bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p01-title.psd"}],
}], "Select p01")

doc = app.activeDocument
print("active", doc.name, doc.width, doc.height)

# List layers + find text layers
layers_info = []
text_layer_names = []
for L in doc.layers:
    name = getattr(L, "name", "")
    kind = str(getattr(L, "kind", ""))
    layers_info.append({"name": name, "kind": kind, "visible": getattr(L, "visible", None)})
    if "text" in kind.lower() or name.startswith("MOCK-TYPE") or "Night I Met" in name or "Jack Farrell" in name:
        text_layer_names.append(name)

print("layers:", json.dumps(layers_info, indent=2))
print("text candidates:", text_layer_names)

# Get bounds of first/top text-like layer via batchPlay get
bounds = None
anchor = None
old_name = text_layer_names[0] if text_layer_names else None

if old_name:
    try:
        r = bp([{
            "_obj": "get",
            "_target": [{"_ref": "layer", "_name": old_name}],
        }], "Get text layer")
        data = r[0] if isinstance(r, list) and r else r
        # bounds often under bounds / boundingBox
        raw = str(data)[:2000]
        print("get sample:", raw[:800])
        if isinstance(data, dict):
            b = data.get("bounds") or data.get("boundingBox")
            print("bounds field:", b)
            if isinstance(b, dict):
                # Photoshop bounds: top/left/bottom/right with _value
                def uv(k):
                    v = b.get(k)
                    if isinstance(v, dict):
                        return float(v.get("_value", 0))
                    return float(v or 0)
                left, top, right, bottom = uv("left"), uv("top"), uv("right"), uv("bottom")
                bounds = {"left": left, "top": top, "right": right, "bottom": bottom}
                # Point-text create position ≈ center-x, baseline ≈ bottom of glyphs approx
                cx = (left + right) / 2.0
                # Use mid-y of box as safer anchor for recreate; createTextLayer uses baseline-ish
                cy = (top + bottom) / 2.0 + (bottom - top) * 0.15
                anchor = {"x": cx, "y": cy}
                print("computed anchor px", anchor, "bounds", bounds)
    except Exception as e:
        print("get layer err:", e)

# Fallback: lower-center safety zone (matches dialed title placement)
if not anchor:
    # Canvas 2625; safety inset ~188px; title lower-middle ~ y 1550
    anchor = {"x": 1312.5, "y": 1550.0}
    print("using fallback anchor", anchor)

# Delete ALL text candidates (clean slate)
for name in text_layer_names:
    try:
        bp([
            {"_obj": "select", "_target": [{"_ref": "layer", "_name": name}], "makeVisible": True},
            {"_obj": "delete", "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}]},
        ], f"Delete {name}")
        print("deleted", name)
    except Exception as e:
        print("delete fail", name, e)

# Create clean MOCK-TYPE via createTextLayer API
title = "The Night I Met Santa"
credit = "Jack Farrell"
content = title + "\r" + credit
layer_name = "MOCK-TYPE - title (preview)"

from dcc_mcp_photoshop._color import solid_color_payload
from dcc_mcp_photoshop._layer_operations import rename_layer_by_id
import sys
sys.path.insert(0, r"D:\Hermes\projects\The-Night-I-Met-Santa\tools\layout-mcp\photoshop-adobepy\.venv\Lib\site-packages")

font_candidates = [
    "CinzelDecorative-Regular",
    "Cinzel-Regular",
    "CinzelDecorative",
    "CormorantGaramond-Medium",
]

result = None
font_used = None
last_err = None
for font_name in font_candidates:
    try:
        result = app.dom.app.activeDocument.createTextLayer(
            {
                "name": layer_name,
                "contents": content,
                "fontName": font_name,
                "fontSize": 36,
                "position": {"x": float(anchor["x"]), "y": float(anchor["y"])},
            },
            modal=True,
            command_name="Create clean P01 MOCK-TYPE",
        )
        font_used = font_name
        print("created with", font_name, result)
        break
    except Exception as e:
        last_err = e
        print("fail", font_name, e)

if not result or not isinstance(result, dict) or result.get("id") is None:
    raise SystemExit(f"createTextLayer failed: {last_err}")

rename_layer_by_id(app, result["id"], layer_name)
text_item = app.activeLayer.text_item

# Style title+credit: set whole layer to 36 first, then try smaller credit via batchPlay ranges
text_item.set_character_style(
    {
        "font": font_used,
        "size": 36,
        "fauxBold": False,
        "fauxItalic": False,
        "color": solid_color_payload("#2C2C2C"),
    },
    command_name="Style P01 MOCK 36pt",
)
text_item.set_paragraph_style(
    {"justification": "center"},
    command_name="Center P01 MOCK",
)

# Soften credit line to ~18pt Cinzel/Cormorant if possible
try:
    # Select credit line characters and resize — best-effort via full rewrite with ranges
    bp([{
        "_obj": "set",
        "_target": [{"_ref": "textLayer", "_enum": "ordinal", "_value": "targetEnum"}],
        "to": {
            "_obj": "textLayer",
            "textKey": {
                "_obj": "textKey",
                "textKey": content,
                "textStyleRange": [
                    {
                        "_obj": "textStyleRange",
                        "from": 0,
                        "to": len(title),
                        "textStyle": {
                            "_obj": "textStyle",
                            "fontPostScriptName": font_used,
                            "size": {"_unit": "pointsUnit", "_value": 36.0},
                            "color": {"_obj": "RGBColor", "red": 44.0, "grain": 44.0, "blue": 44.0},
                        },
                    },
                    {
                        "_obj": "textStyleRange",
                        "from": len(title) + 1,
                        "to": len(content),
                        "textStyle": {
                            "_obj": "textStyle",
                            "fontPostScriptName": "CormorantGaramond-Medium",
                            "size": {"_unit": "pointsUnit", "_value": 18.0},
                            "color": {"_obj": "RGBColor", "red": 44.0, "grain": 44.0, "blue": 44.0},
                        },
                    },
                ],
                "paragraphStyleRange": [{
                    "_obj": "paragraphStyleRange",
                    "from": 0,
                    "to": len(content),
                    "paragraphStyle": {
                        "_obj": "paragraphStyle",
                        "align": {"_enum": "alignmentType", "_value": "center"},
                    },
                }],
            },
        },
    }], "Apply title 36 / credit 18 ranges")
    print("applied dual sizes")
except Exception as e:
    print("range style skip:", e)

# Re-read bounds after create
new_bounds = None
try:
    r = bp([{
        "_obj": "get",
        "_target": [{"_ref": "layer", "_name": layer_name}],
    }], "Get new MOCK")
    data = r[0] if isinstance(r, list) and r else r
    if isinstance(data, dict):
        b = data.get("bounds") or data.get("boundingBox")
        if isinstance(b, dict):
            def uv(k):
                v = b.get(k)
                if isinstance(v, dict):
                    return float(v.get("_value", 0))
                return float(v or 0)
            new_bounds = {
                "left": uv("left"), "top": uv("top"),
                "right": uv("right"), "bottom": uv("bottom"),
            }
except Exception as e:
    print("reget err", e)

doc.save_as(PSD)
print("saved", PSD)

# Convert px (full-bleed canvas) → InDesign page inches (trim origin)
# Canvas 0,0 = top-left of bleed; page 0,0 = trim; bleed = 0.125"
BLEED_IN = 0.125
PPI = 300.0

def px_to_page_in(px):
    return (px / PPI) - BLEED_IN

payload = {
    "font": font_used,
    "title_pt": 36,
    "credit_pt": 18,
    "color": "#2C2C2C",
    "anchor_px": anchor,
    "old_bounds_px": bounds,
    "new_bounds_px": new_bounds,
    "indesign_frame_in": None,
}
if new_bounds:
    payload["indesign_frame_in"] = {
        "top": px_to_page_in(new_bounds["top"]),
        "left": px_to_page_in(new_bounds["left"]),
        "bottom": px_to_page_in(new_bounds["bottom"]),
        "right": px_to_page_in(new_bounds["right"]),
    }

Path(OUT_JSON).write_text(json.dumps(payload, indent=2), encoding="utf-8")
print("wrote", OUT_JSON)
print(json.dumps(payload, indent=2))
