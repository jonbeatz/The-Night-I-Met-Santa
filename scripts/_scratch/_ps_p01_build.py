from adobe.photoshop import Photoshop
from pathlib import Path
import time

app = Photoshop()

def bp(cmds, name):
    return app.batch_play(cmds, modal=True, command_name=name)

# Wait for docs
names = []
for _ in range(20):
    try:
        names = [d.name for d in app.documents]
    except Exception:
        names = []
    if any("single-page-template" in n for n in names) and any("art-P01" in n or n.endswith(".png") for n in names):
        break
    time.sleep(0.5)

print("docs:", names)

# Select template
tmpl_name = next(n for n in names if "single-page-template" in n)
bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": tmpl_name}],
}], "Select template")

out = str(Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p01-title.psd"))
# Save As duplicate working file
app.activeDocument.save_as(out)
print("saved", out)

# Re-select in case name changed
bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p01-title.psd"}],
}], "Select p01")

# Find art doc
names = [d.name for d in app.documents]
art_name = next((n for n in names if "art-P01" in n or (n.lower().endswith(".png") and "p01" in n.lower())), None)
if not art_name:
    art_name = next((n for n in names if n.lower().endswith(".png")), None)
print("art doc:", art_name)

bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": art_name}],
}], "Select art")
bp([{
    "_obj": "set",
    "_target": [{"_ref": "channel", "_property": "selection"}],
    "to": {"_enum": "ordinal", "_value": "allEnum"},
}], "Select all")
bp([{ "_obj": "copyEvent" }], "Copy")

bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p01-title.psd"}],
}], "Select p01 again")
bp([{
    "_obj": "select",
    "_target": [{"_ref": "layer", "_name": "ART - full-bleed scene here"}],
    "makeVisible": True,
}], "Select ART")
bp([{ "_obj": "paste" }], "Paste art")

# Hide TYPE zone guide if present
try:
    bp([{
        "_obj": "select",
        "_target": [{"_ref": "layer", "_name": "TYPE zone - live Cormorant in InDesign"}],
    }, {
        "_obj": "hide",
        "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
    }], "Hide TYPE zone")
except Exception as e:
    print("hide type zone:", e)

# Create MOCK title text layer (Cinzel if available, else Cormorant)
title = "The Night I Met Santa"
credit = "Jack Farrell"
# Use make text layer via batchPlay
try:
    bp([{
        "_obj": "make",
        "_target": [{"_ref": "textLayer"}],
        "using": {
            "_obj": "textLayer",
            "textKey": title + "\r" + credit,
            "textStyleRange": [{
                "_obj": "textStyleRange",
                "from": 0,
                "to": len(title),
                "textStyle": {
                    "_obj": "textStyle",
                    "fontPostScriptName": "CinzelDecorative-Regular",
                    "fontName": "Cinzel Decorative",
                    "size": {"_unit": "pointsUnit", "_value": 48.0},
                    "color": {"_obj": "RGBColor", "red": 44.0, "grain": 44.0, "blue": 44.0},
                },
            }, {
                "_obj": "textStyleRange",
                "from": len(title) + 1,
                "to": len(title) + 1 + len(credit),
                "textStyle": {
                    "_obj": "textStyle",
                    "fontPostScriptName": "CormorantGaramond-Medium",
                    "fontName": "Cormorant Garamond",
                    "size": {"_unit": "pointsUnit", "_value": 22.0},
                    "color": {"_obj": "RGBColor", "red": 44.0, "grain": 44.0, "blue": 44.0},
                },
            }],
            "paragraphStyleRange": [{
                "_obj": "paragraphStyleRange",
                "from": 0,
                "to": len(title) + 1 + len(credit),
                "paragraphStyle": {
                    "_obj": "paragraphStyle",
                    "align": {"_enum": "alignmentType", "_value": "center"},
                },
            }],
            "layerName": "MOCK-TYPE - title (preview)",
        },
    }], "Make MOCK title")
except Exception as e:
    print("text make err, try simpler:", e)
    bp([{
        "_obj": "make",
        "_target": [{"_ref": "textLayer"}],
        "using": {
            "_obj": "textLayer",
            "textKey": title + "\r" + credit,
            "textStyleRange": [{
                "_obj": "textStyleRange",
                "from": 0,
                "to": len(title) + 1 + len(credit),
                "textStyle": {
                    "_obj": "textStyle",
                    "fontPostScriptName": "CormorantGaramond-Medium",
                    "size": {"_unit": "pointsUnit", "_value": 42.0},
                    "color": {"_obj": "RGBColor", "red": 44.0, "grain": 44.0, "blue": 44.0},
                },
            }],
        },
    }], "Make MOCK title fallback")
    # rename
    bp([{
        "_obj": "set",
        "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
        "to": {"_obj": "layer", "name": "MOCK-TYPE - title (preview)"},
    }], "Rename MOCK")

# Position text roughly upper-center (move layer)
try:
    bp([{
        "_obj": "select",
        "_target": [{"_ref": "layer", "_name": "MOCK-TYPE - title (preview)"}],
    }, {
        "_obj": "move",
        "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
        "to": {"_obj": "offset", "horizontal": {"_unit": "pixelsUnit", "_value": 0}, "vertical": {"_unit": "pixelsUnit", "_value": -400}},
    }], "Nudge MOCK up")
except Exception as e:
    print("nudge:", e)

app.activeDocument.save_as(out)
print("saved final")

# Close art PNG without saving
try:
    bp([{
        "_obj": "select",
        "_target": [{"_ref": "document", "_name": art_name}],
    }, {
        "_obj": "close",
        "_target": [{"_ref": "document", "_enum": "ordinal", "_value": "first"}],
        "saving": {"_enum": "yesNo", "_value": "no"},
    }], "Close art PNG")
    print("closed", art_name)
except Exception as e:
    print("close art:", e)

# Close template if still open separately
names = [d.name for d in app.documents]
print("still open:", names)
for L in app.activeDocument.layers:
    print(" layer", repr(getattr(L,"name","")), "vis", getattr(L,"visible",None))
