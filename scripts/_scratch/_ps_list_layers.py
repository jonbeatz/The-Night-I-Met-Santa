from adobe.photoshop import Photoshop
app = Photoshop()
doc = app.activeDocument
print("doc", doc.name)
for L in doc.layers:
    name = getattr(L, "name", "")
    kind = getattr(L, "kind", None)
    typename = getattr(L, "typename", None)
    has_c = getattr(L, "has_children", None)
    lid = getattr(L, "id", None)
    print("name=", repr(name), "kind=", kind, "typename=", typename, "hasChildren=", has_c, "id=", lid)
