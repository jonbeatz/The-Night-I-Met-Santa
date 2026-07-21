from adobe.photoshop import Photoshop
from adobe.dcc_mcp import action_result
import sys
sys.path.insert(0, r"D:\Hermes\projects\The-Night-I-Met-Santa\tools\layout-mcp\photoshop-adobepy\.venv\Lib\site-packages\dcc_mcp_photoshop")
from dcc_mcp_photoshop._color import solid_color_payload
from dcc_mcp_photoshop._layer_operations import rename_layer_by_id

app = Photoshop()
# ensure p03 active
app.batch_play([{
  "_obj": "select",
  "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], modal=True, command_name="Select p03")

# Hide guide TYPE zone so MOCK text is what Jon sees
app.batch_play([
  {"_obj": "select", "_target": [{"_ref": "layer", "_name": "TYPE zone - live Cormorant in InDesign"}], "makeVisible": False},
  {"_obj": "hide", "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}]},
], modal=True, command_name="Hide TYPE guide")

content = "For my family, with love.\r— Jack Farrell"
layer_name = "MOCK-TYPE - dedication (preview)"
# Center-ish of 2625 canvas; dedication sits in quiet cream zone
x, y = 1312.0, 1180.0
font_candidates = [
    "CormorantGaramond-Medium",
    "CormorantGaramondMedium",
    "CormorantGaramond-Regular",
    "EBGaramond-Medium",
    "Georgia",
]

last_err = None
result = None
font_used = None
for font_name in font_candidates:
    try:
        result = app.dom.app.activeDocument.createTextLayer(
            {
                "name": layer_name,
                "contents": content,
                "fontName": font_name,
                "fontSize": 20,
                "position": {"x": x, "y": y},
            },
            modal=True,
            command_name="Create MOCK dedication type",
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
text_item.set_character_style(
    {
        "font": font_used,
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

# Save PSD
from pathlib import Path
app.activeDocument.save_as(str(Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p03-dedication.psd")))
print("OK layer", layer_name, "font", font_used)
for L in list(app.activeDocument.layers)[:8]:
    print(getattr(L, "name", L), "vis", getattr(L, "visible", None))
