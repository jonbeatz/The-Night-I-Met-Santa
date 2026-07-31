from pypdf import PdfReader
from pathlib import Path

interior = Path(r"Output/interiors/TNIMS-Interior-FINAL-Lulu.pdf")
r = PdfReader(str(interior))

for pi in [0, 9, 10, 14, 29]:
    p = r.pages[pi]
    res = p.get("/Resources")
    if not res:
        print(f"p{pi+1}: no resources")
        continue
    xo = res.get("/XObject")
    if not xo:
        print(f"p{pi+1}: no xobjects (maybe text-only)")
        continue
    for name in list(xo.keys())[:3]:
        obj = xo[name].get_object()
        if obj.get("/Subtype") != "/Image":
            continue
        cs = obj.get("/ColorSpace")
        filt = obj.get("/Filter")
        w = obj.get("/Width")
        h = obj.get("/Height")
        print(f"p{pi+1} {name}: {w}x{h} Filter={filt} CS={cs}")
        if isinstance(cs, list) and str(cs[0]) == "/ICCBased":
            icc = cs[1].get_object()
            n = icc.get("/N")
            raw = icc.get_data()
            print(f"   ICC N={n} bytes={len(raw)}")
            text = raw.decode("latin-1", errors="ignore")
            for key in ("sRGB", "Adobe RGB", "CMYK", "IEC61966", "Compat"):
                if key.lower() in text.lower():
                    print(f"   token: {key}")

# Cover FINAL color
cover = Path(r"Output/covers/TNIMS-Cover-FINAL-Lulu.pdf")
cr = PdfReader(str(cover))
p = cr.pages[0]
xo = p["/Resources"]["/XObject"]
cmyk = rgb = other = 0
for name in xo.keys():
    obj = xo[name].get_object()
    if obj.get("/Subtype") != "/Image":
        continue
    cs = obj.get("/ColorSpace")
    s = str(cs)
    if "CMYK" in s or s == "/DeviceCMYK":
        cmyk += 1
    elif "RGB" in s or "ICCBased" in s:
        rgb += 1
        if isinstance(cs, list) and str(cs[0]) == "/ICCBased":
            icc = cs[1].get_object()
            print("cover ICC N=", icc.get("/N"))
    else:
        other += 1
print(f"Cover-FINAL images: CMYK={cmyk} RGB/ICC={rgb} other={other}")
