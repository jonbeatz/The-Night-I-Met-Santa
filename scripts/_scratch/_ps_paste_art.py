from adobe.photoshop import Photoshop

app = Photoshop()

def bp(cmds, name):
    return app.batch_play(cmds, modal=True, command_name=name)

# Source art doc
bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "art-P03-dedication-2625.png"}],
}], "Select art doc")
bp([{
    "_obj": "set",
    "_target": [{"_ref": "channel", "_property": "selection"}],
    "to": {"_enum": "ordinal", "_value": "allEnum"},
}], "Select all")
bp([{ "_obj": "copyEvent" }], "Copy pixels")

# Target p03
bp([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], "Select p03")
bp([{
    "_obj": "select",
    "_target": [{"_ref": "layer", "_name": "ART - full-bleed scene here"}],
    "makeVisible": True,
}], "Select ART")
bp([{ "_obj": "paste" }], "Paste into ART")

print("active", app.activeDocument.name)
for L in list(app.activeDocument.layers)[:10]:
    print(getattr(L, "name", L))
