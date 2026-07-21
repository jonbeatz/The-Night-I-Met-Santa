from adobe.photoshop import Photoshop
import json
app = Photoshop()
app.batch_play([{
  "_obj": "select",
  "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], modal=True, command_name="Select p03")

# Get Jon's visible text layer (id 11)
r = app.batch_play([{
    "_obj": "get",
    "_target": [{"_ref": "layer", "_id": 11}],
}], modal=True, command_name="Get Jon text layer")
# Write full dump for parsing
path = r"D:\Hermes\projects\The-Night-I-Met-Santa\Media\generated\dedication-smoke\jon-text-layer-dump.json"
# result may not be JSON serializable - stringify carefully
s = repr(r)
open(path, "w", encoding="utf-8").write(s)
print("wrote", path, "len", len(s))
# pull key fields from nested structure if dict-like
data = r[0] if isinstance(r, list) and r else r
if isinstance(data, dict):
    print("keys", list(data.keys())[:40])
    for k in ("name", "textKey", "typeUnit", "boundingBox"):
        if k in data:
            print(k, str(data[k])[:500])
