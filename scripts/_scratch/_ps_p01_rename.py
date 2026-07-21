from adobe.photoshop import Photoshop
from pathlib import Path
app = Photoshop()
def bp(cmds, name):
    return app.batch_play(cmds, modal=True, command_name=name)

bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p01-title.psd"}],
}], "Select p01")

# Rename text layer to MOCK-TYPE
bp([{
    "_obj": "select",
    "_target": [{"_ref": "layer", "_name": "The Night I Met Santa Jack Farrell"}],
}, {
    "_obj": "set",
    "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
    "to": {"_obj": "layer", "name": "MOCK-TYPE - title (preview)"},
}], "Rename MOCK-TYPE")

# Ensure ART has content - count pixels rough via layer count
out = str(Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\p01-title.psd"))
app.activeDocument.save_as(out)
print("renamed + saved")
for L in app.activeDocument.layers:
    print(repr(getattr(L,"name","")), getattr(L,"kind",None))
