from adobe.photoshop import Photoshop
app = Photoshop()
print("=== open docs ===")
for d in list(app.documents):
    print(d.id, d.name, getattr(d, "path", None))

# Close art PNG tabs (keep p03 + templates)
for d in list(app.documents):
    name = d.name
    if name.endswith(".png") or "art-P03-dedication-2625" in name:
        print("closing", name)
        app.batch_play([{
            "_obj": "select",
            "_target": [{"_ref": "document", "_name": name}],
        }], modal=True, command_name=f"Select {name}")
        app.batch_play([{
            "_obj": "close",
            "saving": {"_enum": "yesNo", "_value": "no"},
        }], modal=True, command_name=f"Close {name}")

app.batch_play([{
    "_obj": "select",
    "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], modal=True, command_name="Select p03")

print("=== layers on p03 ===")
for L in app.activeDocument.layers:
    print(repr(getattr(L,"name","")), getattr(L,"kind",None), "vis", getattr(L,"visible",None), "id", getattr(L,"id",None))

# Probe MOCK text via batchPlay get
r = app.batch_play([{
    "_obj": "get",
    "_target": [{"_ref": "layer", "_name": "MOCK-TYPE - dedication (preview)"}],
}], modal=True, command_name="Get MOCK-TYPE")
print("get MOCK", str(r)[:2000])
