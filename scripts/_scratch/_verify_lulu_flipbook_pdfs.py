"""Verify Lulu + flipbook PDF deliverables."""
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(".")


def summarize(path: Path, expect_pages=None, expect_w=None, expect_h=None):
    r = PdfReader(str(path))
    data = path.read_bytes()
    p0 = r.pages[0]
    w = float(p0.mediabox.width) / 72
    h = float(p0.mediabox.height) / 72
    tw = th = None
    try:
        tw = float(p0.trimbox.width) / 72
        th = float(p0.trimbox.height) / 72
    except Exception:
        pass
    cmyk = data.count(b"DeviceCMYK")
    icc = data.count(b"ICCBased")
    sizes = {
        (round(float(p.mediabox.width) / 72, 3), round(float(p.mediabox.height) / 72, 3))
        for p in r.pages
    }
    ok = True
    notes = []
    if expect_pages is not None and len(r.pages) != expect_pages:
        ok = False
        notes.append(f"pages {len(r.pages)}!={expect_pages}")
    if expect_w and abs(w - expect_w) > 0.01:
        ok = False
        notes.append(f"w {w}!={expect_w}")
    if expect_h and abs(h - expect_h) > 0.01:
        ok = False
        notes.append(f"h {h}!={expect_h}")
    print(f"{'PASS' if ok else 'FAIL'} {path.name}")
    print(f"  pages={len(r.pages)} Media={w:.3f}x{h:.3f}", end="")
    if tw:
        print(f" Trim={tw:.3f}x{th:.3f}", end="")
    print(f"  CMYK={cmyk} ICC={icc} size={path.stat().st_size/1e6:.2f}MB")
    print(f"  unique sizes={sizes}")
    if notes:
        print(f"  issues: {notes}")
    # cover RGB check
    if "Cover" in path.name:
        xo = p0["/Resources"]["/XObject"]
        for name in list(xo.keys())[:1]:
            obj = xo[name].get_object()
            if obj.get("/Subtype") == "/Image":
                cs = obj.get("/ColorSpace")
                print(f"  first image CS={cs}")
                if isinstance(cs, list) and str(cs[0]) == "/ICCBased":
                    print(f"  ICC N={cs[1].get_object().get('/N')}")
    return ok


oks = []
oks.append(
    summarize(
        ROOT / "Output/interiors/TNIMS-Interior-FINAL-Lulu.pdf",
        expect_pages=30,
        expect_w=8.75,
        expect_h=8.75,
    )
)
oks.append(
    summarize(
        ROOT / "Output/covers/TNIMS-Cover-FINAL-Lulu.pdf",
        expect_pages=1,
        expect_w=18.25,
        expect_h=8.75,
    )
)
oks.append(
    summarize(
        ROOT / "Output/interiors/TNIMS-FLIPBOOK-trim.pdf",
        expect_pages=34,
        expect_w=8.5,
        expect_h=8.5,
    )
)
print("ALL PASS" if all(oks) else "SOME FAILED")
