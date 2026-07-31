"""Merge isolated S04 page PDFs into FINAL-v2 burgundy-open interior PDF.

v2 layout: 32 pages. S04 text|image is on PDF pages 12|13 (was 10|11 in FINAL).
rest.pdf = pages 1-11 + 14-32 (30 pages).
"""
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter

root = Path(r"Output/interiors/_s04_pages_v2")
rest = PdfReader(str(root / "rest.pdf"))
p12 = PdfReader(str(root / "p12.pdf"))
p13 = PdfReader(str(root / "p13.pdf"))

print(f"rest pages={len(rest.pages)} (expect 30 = 1-11 + 14-32)")
print(f"p12 pages={len(p12.pages)} p13 pages={len(p13.pages)}")

if len(rest.pages) != 30:
    raise SystemExit(f"Unexpected rest page count: {len(rest.pages)}")
if len(p12.pages) != 1 or len(p13.pages) != 1:
    raise SystemExit("p12/p13 must be single-page PDFs")

w = PdfWriter()
# pages 1-11
for i in range(11):
    w.add_page(rest.pages[i])
# pages 12, 13 (S04 isolated)
w.add_page(p12.pages[0])
w.add_page(p13.pages[0])
# pages 14-32 (19 pages) from rest[11:]
for i in range(11, 30):
    w.add_page(rest.pages[i])

out = Path(r"Output/interiors/TNIMS-Interior-FINAL-v2-burgundy-open-Lulu.pdf")
with out.open("wb") as f:
    w.write(f)

final = PdfReader(str(out))
print(f"wrote {out} pages={len(final.pages)} size={out.stat().st_size}")
for n in (11, 12):  # 0-based = PDF pages 12, 13
    box = final.pages[n].mediabox
    print(
        f"p{n+1} mediabox in="
        f"{float(box.width)/72:.4f}x{float(box.height)/72:.4f}"
    )
