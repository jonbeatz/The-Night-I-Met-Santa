from adobe.photoshop import Photoshop
from pathlib import Path

app = Photoshop()

def bp(cmds, name):
    return app.batch_play(cmds, modal=True, command_name=name)

bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], "Select p03")

# Hide overlays for clean art export
for name in [
    "TYPE zone - live Cormorant in InDesign",
    "CLOUD - watercolor wash optional",
    "SAFETY 0.5in from trim",
    "TRIM 8.5in",
]:
    bp([{
        "_obj": "select",
        "_target": [{"_ref": "layer", "_name": name}],
        "makeVisible": False,
    }, {
        "_obj": "hide",
        "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
    }], f"Hide {name}")

out = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Media\generated\dedication-smoke\art-P03-dedication-FROM-PSD.png")
out.parent.mkdir(parents=True, exist_ok=True)
doc = app.activeDocument
# export via document.export if available
try:
    r = doc.export(str(out))
    print("export", r)
except Exception as e:
    print("export method err", e)
    # fallback batchPlay save for web
    bp([{
        "_obj": "save",
        "as": {
            "_obj": "PNGFormat",
            "method": {"_enum": "PNGMethod", "_value": "quick"},
        },
        "in": {"_path": str(out), "_kind": "local"},
        "copy": True,
        "lowerCase": True,
    }], "Save PNG copy")

# restore visibility of guides for Jon working PSD
for name in [
    "TRIM 8.5in",
    "SAFETY 0.5in from trim",
    "CLOUD - watercolor wash optional",
    "TYPE zone - live Cormorant in InDesign",
]:
    bp([{
        "_obj": "select",
        "_target": [{"_ref": "layer", "_name": name}],
        "makeVisible": False,
    }, {
        "_obj": "show",
        "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
    }], f"Show {name}")

# save PSD
try:
    doc.save_as(str(Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p03-dedication.psd")))
    print("psd saved")
except Exception as e:
    print("save err", e)
    bp([{ "_obj": "save" }], "Save")

print("exists png", out.exists(), out.stat().st_size if out.exists() else 0)
