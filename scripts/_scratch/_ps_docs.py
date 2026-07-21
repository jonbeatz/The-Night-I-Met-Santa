from adobe.photoshop import Photoshop
from pathlib import Path
app = Photoshop()
for d in app.documents:
    print(d.id, d.name, getattr(d, "path", None), "saved=", getattr(d, "saved", None))
print("active", app.activeDocument.name, app.activeDocument.path)
