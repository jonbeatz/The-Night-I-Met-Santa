"""Sample left/right edge colors on PDF pages 10-11 after S04 L/R replace."""
import numpy as np
from PIL import Image

try:
    import fitz
except ImportError:
    raise SystemExit("PyMuPDF (fitz) required")

pdf = fitz.open(r"Output/interiors/TNIMS-Interior-FINAL-Lulu.pdf")
print("pages", pdf.page_count)

for pi in [9, 10]:
    page = pdf[pi]
    mat = fitz.Matrix(150 / 72, 150 / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    w, h = im.size
    arr = np.asarray(im)
    left_strip = arr[:, :8].mean(axis=(0, 1))
    right_strip = arr[:, -8:].mean(axis=(0, 1))
    print(
        f"PDF p{pi + 1} {w}x{h}px (~{w / 150:.3f}in): "
        f"left_edge RGB={tuple(left_strip.round().astype(int))} "
        f"right_edge RGB={tuple(right_strip.round().astype(int))}"
    )
    out = rf"Output/interiors/_preview-p{pi + 1}-s04.png"
    im.save(out)
    print(" wrote", out)

print("Expect: p10 right ~cream (230+); p11 left ~burgundy (~90)")
