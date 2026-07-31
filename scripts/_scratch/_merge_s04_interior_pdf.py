"""Merge isolated S04 page PDFs into final interior PDF."""
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter

root = Path(r"Output/interiors/_s04_pages")
rest = PdfReader(str(root / "rest.pdf"))
p10 = PdfReader(str(root / "p10.pdf"))
p11 = PdfReader(str(root / "p11.pdf"))

print(f"rest pages={len(rest.pages)} (expect 28 = 1-9 + 12-30)")
print(f"p10 pages={len(p10.pages)} p11 pages={len(p11.pages)}")

if len(rest.pages) != 28:
    raise SystemExit(f"Unexpected rest page count: {len(rest.pages)}")
if len(p10.pages) != 1 or len(p11.pages) != 1:
    raise SystemExit("p10/p11 must be single-page PDFs")

w = PdfWriter()
# pages 1-9
for i in range(9):
    w.add_page(rest.pages[i])
# page 10, 11
w.add_page(p10.pages[0])
w.add_page(p11.pages[0])
# pages 12-30 (19 pages) from rest[9:]
for i in range(9, 28):
    w.add_page(rest.pages[i])

out = Path(r"Output/interiors/TNIMS-Interior-FINAL-Lulu.pdf")
with out.open("wb") as f:
    w.write(f)

final = PdfReader(str(out))
print(f"wrote {out} pages={len(final.pages)} size={out.stat().st_size}")
box = final.pages[9].mediabox
print(f"p10 mediabox in={float(box.width)/72:.4f}x{float(box.height)/72:.4f}")
box11 = final.pages[10].mediabox
print(f"p11 mediabox in={float(box11.width)/72:.4f}x{float(box11.height)/72:.4f}")
