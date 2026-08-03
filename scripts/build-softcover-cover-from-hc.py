"""
Build Lulu paperback (softcover) wrap PDF from hardcover Cover PDF.

Hardcover SoT: 19 x 10.25 in @ 300 = 5700 x 3075
  BACK 2813 | SPINE 75 | FRONT 2812

Paperback expected (8.5 sq, 34 pp, 0.125 bleed):
  spine = pages/444 + 0.06
  height = 8.75 in
  width  = 8.75 + spine + 8.75

Override exact inches via CLI after Lulu UI confirms.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
HC_PDF = ROOT / "Output" / "FINAL-Master-PDFs" / "TNIMS-Cover-FINAL.pdf"
OUT_DIR = ROOT / "Output" / "FINAL-Master-PDFs"
OUT_PNG = OUT_DIR / "TNIMS-Cover-SOFTCOVER-FINAL.png"
OUT_PDF = OUT_DIR / "TNIMS-Cover-SOFTCOVER-FINAL.pdf"
META = OUT_DIR / "TNIMS-Cover-SOFTCOVER-FINAL.meta.json"

# Hardcover panel map @ 300 ppi
HC_W, HC_H = 5700, 3075
HC_BACK_W, HC_SPINE_W, HC_FRONT_W = 2813, 75, 2812


def cover_fit(src: Image.Image, tw: int, th: int) -> Image.Image:
    """Scale to cover target, center-crop."""
    sw, sh = src.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width-in", type=float, default=None, help="Exact Lulu cover width inches")
    ap.add_argument("--height-in", type=float, default=None, help="Exact Lulu cover height inches")
    ap.add_argument("--spine-in", type=float, default=None, help="Exact Lulu spine inches")
    ap.add_argument("--pages", type=int, default=34)
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    spine_in = args.spine_in if args.spine_in is not None else (args.pages / 444.0) + 0.06
    height_in = args.height_in if args.height_in is not None else 8.75
    width_in = args.width_in if args.width_in is not None else (8.75 + spine_in + 8.75)

    dpi = args.dpi
    out_w = int(round(width_in * dpi))
    out_h = int(round(height_in * dpi))
    spine_px = int(round(spine_in * dpi))
    # Split remaining width into back/front (Lulu often 2625+2625 for 8.75")
    side = (out_w - spine_px) // 2
    front_w = out_w - spine_px - side
    back_w, front_w = side, front_w

    print(f"Target: {width_in:.5f} x {height_in:.5f} in | spine {spine_in:.5f} in")
    print(f"Pixels @{dpi}: {out_w} x {out_h} | BACK {back_w} | SPINE {spine_px} | FRONT {front_w}")

    doc = fitz.open(HC_PDF)
    page = doc[0]
    # Render hardcover page at exact 300 ppi pixel size
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    hc = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()
    if hc.size != (HC_W, HC_H):
        print(f"WARN: rendered HC size {hc.size}, expected {(HC_W, HC_H)} — resizing")
        hc = hc.resize((HC_W, HC_H), Image.Resampling.LANCZOS)

    back = hc.crop((0, 0, HC_BACK_W, HC_H))
    spine = hc.crop((HC_BACK_W, 0, HC_BACK_W + HC_SPINE_W, HC_H))
    front = hc.crop((HC_BACK_W + HC_SPINE_W, 0, HC_W, HC_H))

    back_fit = cover_fit(back, back_w, out_h)
    front_fit = cover_fit(front, front_w, out_h)
    spine_fit = cover_fit(spine, spine_px, out_h)

    wrap = Image.new("RGB", (out_w, out_h))
    wrap.paste(back_fit, (0, 0))
    wrap.paste(spine_fit, (back_w, 0))
    wrap.paste(front_fit, (back_w + spine_px, 0))
    wrap.save(OUT_PNG, "PNG")
    print(f"Wrote {OUT_PNG}")

    c = canvas.Canvas(str(OUT_PDF), pagesize=(width_in * 72, height_in * 72))
    c.drawImage(ImageReader(wrap), 0, 0, width=width_in * 72, height=height_in * 72)
    c.save()
    print(f"Wrote {OUT_PDF}")

    meta = {
        "source_hc_pdf": str(HC_PDF),
        "width_in": width_in,
        "height_in": height_in,
        "spine_in": spine_in,
        "dpi": dpi,
        "pixels": {"w": out_w, "h": out_h, "back": back_w, "spine": spine_px, "front": front_w},
        "out_pdf": str(OUT_PDF),
        "out_png": str(OUT_PNG),
        "method": "cover-fit panels from HC PDF render",
    }
    META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {META}")


if __name__ == "__main__":
    main()
