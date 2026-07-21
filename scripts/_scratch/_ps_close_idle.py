from adobe.photoshop import Photoshop
app = Photoshop()
keep = "p03-dedication.psd"
closed = []
# Close non-working docs without saving (templates unchanged)
for name in list([d.name for d in app.documents]):
    if name == keep:
        continue
    try:
        app.batch_play([{
            "_obj": "select",
            "_target": [{"_ref": "document", "_name": name}],
        }], modal=True, command_name=f"Select {name}")
        app.batch_play([{
            "_obj": "close",
            "_target": [{"_ref": "document", "_enum": "ordinal", "_value": "first"}],
            "saving": {"_enum": "yesNo", "_value": "no"},
        }], modal=True, command_name=f"Close {name}")
        closed.append(name)
    except Exception as e:
        closed.append(f"{name} FAIL {e}")
print("closed:", closed)
print("still open:", [d.name for d in app.documents])
