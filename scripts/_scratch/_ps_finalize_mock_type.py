from adobe.photoshop import Photoshop
from pathlib import Path
app = Photoshop()
app.batch_play([{
  "_obj": "select",
  "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], modal=True, command_name="Select p03")

# Delete old agent MOCK layer id 10 if present
try:
    app.batch_play([
        {"_obj": "select", "_target": [{"_ref": "layer", "_id": 10}]},
        {"_obj": "delete", "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}]},
    ], modal=True, command_name="Delete old MOCK-TYPE")
    print("deleted old MOCK id 10")
except Exception as e:
    print("delete old MOCK:", e)

# Rename Jon's layer (id 11) to canonical MOCK-TYPE name
try:
    app.batch_play([
        {"_obj": "select", "_target": [{"_ref": "layer", "_id": 11}]},
        {"_obj": "set", "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
         "to": {"_obj": "layer", "name": "MOCK-TYPE - dedication (preview)"}},
    ], modal=True, command_name="Rename Jon type to MOCK-TYPE")
    print("renamed id 11")
except Exception as e:
    print("rename:", e)

# Set fill color to #2C2C2C via text style (best-effort batchPlay)
try:
    app.batch_play([{
        "_obj": "set",
        "_target": [{"_ref": "property", "_property": "textStyle"}, {"_ref": "textLayer", "_enum": "ordinal", "_value": "targetEnum"}],
        "to": {
            "_obj": "textStyle",
            "color": {
                "_obj": "RGBColor",
                "red": 44.0,
                "grain": 44.0,
                "blue": 44.0,
            },
            "size": {"_unit": "pointsUnit", "_value": 30.0},
        },
    }], modal=True, command_name="Set MOCK type color/size")
    print("styled color/size")
except Exception as e:
    print("style err (Jon can fix manually):", e)

app.activeDocument.save_as(str(Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p03-dedication.psd")))
print("saved")
for L in app.activeDocument.layers:
    print(repr(getattr(L,"name","")), getattr(L,"kind",None), "vis", getattr(L,"visible",None))
print("open docs:", [d.name for d in app.documents])
