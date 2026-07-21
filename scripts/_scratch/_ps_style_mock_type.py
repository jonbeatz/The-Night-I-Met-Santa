from adobe.photoshop import Photoshop
from pathlib import Path
import sys
sys.path.insert(0, r"D:\Hermes\projects\The-Night-I-Met-Santa\tools\layout-mcp\photoshop-adobepy\.venv\Lib\site-packages")
from dcc_mcp_photoshop._color import solid_color_payload
from dcc_mcp_photoshop._layer_operations import rename_layer_by_id

app = Photoshop()
app.batch_play([{
  "_obj": "select",
  "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], modal=True, command_name="Select p03")

# Find the new text layer (id 10 or by contents)
target = None
for L in app.activeDocument.layers:
    name = str(getattr(L, "name", ""))
    kind = getattr(L, "kind", None)
    print("layer", repr(name), kind, getattr(L, "id", None))
    if kind == "text" or "family" in name.lower() or name.startswith("For my"):
        target = L

if target is None:
    raise SystemExit("no text layer found")

rename_layer_by_id(app, target.id, "MOCK-TYPE - dedication (preview)")

# Select that layer
app.batch_play([{
  "_obj": "select",
  "_target": [{"_ref": "layer", "_name": "MOCK-TYPE - dedication (preview)"}],
  "makeVisible": True,
}], modal=True, command_name="Select MOCK-TYPE")

text_item = app.activeLayer.text_item
print("text_item", text_item)
if text_item is None:
    # try via layer proxy
    for L in app.activeDocument.layers:
        if getattr(L, "name", "") == "MOCK-TYPE - dedication (preview)":
            text_item = L.text_item
            print("from layer", text_item)
            break

if text_item is not None:
    text_item.set_character_style(
        {
            "font": "CormorantGaramond-Medium",
            "size": 20,
            "fauxBold": False,
            "fauxItalic": False,
            "color": solid_color_payload("#2C2C2C"),
        },
        command_name="Style MOCK type",
    )
    text_item.set_paragraph_style(
        {"justification": "center"},
        command_name="Center MOCK type",
    )
    print("styled OK")
else:
    print("WARN: could not style; layer exists for Jon to tweak")

app.activeDocument.save_as(str(Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p03-dedication.psd")))
print("saved")
for L in list(app.activeDocument.layers)[:10]:
    print(getattr(L, "name", L), "vis=", getattr(L, "visible", None), "kind=", getattr(L, "kind", None))
