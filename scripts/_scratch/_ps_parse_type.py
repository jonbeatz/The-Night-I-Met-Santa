from adobe.photoshop import Photoshop
import re
app = Photoshop()
r = app.batch_play([{
    "_obj": "get",
    "_target": [{"_ref": "layer", "_id": 11}],
}], modal=True, command_name="Get Jon text")
data = r[0] if isinstance(r, list) else r
tk = data.get("textKey", {})
# Walk for size / color / font
s = repr(tk)

def find_all(pat):
    return re.findall(pat, s)

print("size values", find_all(r"'size': \{[^}]+'_value': ([0-9.]+)")[:10])
print("fontName", find_all(r"'fontName': '([^']+)'")[:10])
print("fontPostScript", find_all(r"'fontPostScriptName': '([^']+)'")[:10])
print("impliedFontSize", find_all(r"'impliedFontSize': \{[^}]+'_value': ([0-9.]+)")[:10])
# color rgb
print("red samples", find_all(r"'red': ([0-9.]+)")[:8])
print("grain/green", find_all(r"'grain': ([0-9.]+)")[:8])
print("blue", find_all(r"'blue': ([0-9.]+)")[:8])
# leading
print("leading", find_all(r"'leading': \{[^}]+'_value': ([0-9.]+)")[:8])
print("textKey text", repr(tk.get("text", tk.get("contents", "")))[:200])
