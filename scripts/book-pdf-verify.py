"""Verify / optionally set MediaBox TrimBox BleedBox on an interior PDF (pikepdf)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PDF = ROOT / "Output" / "The-Night-I-Met-Santa-INTERIOR-img2pdf.pdf"
TRIM_IN = 8.5
BLEED_IN = 0.125
MEDIA_IN = TRIM_IN + 2 * BLEED_IN  # 8.75


def in_to_pt(inches: float) -> float:
    return inches * 72.0


def main() -> int:
    try:
        import pikepdf
        from pikepdf import Array, Name, Rectangle
    except ImportError:
        print("pikepdf not installed. Run: python -m pip install img2pdf pikepdf", file=sys.stderr)
        return 1

    p = argparse.ArgumentParser(description="Verify POD page boxes with pikepdf")
    p.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    p.add_argument("--apply-boxes", action="store_true", help="Write TrimBox/BleedBox for 8.5\" trim + 0.125\" bleed")
    p.add_argument("--output", type=Path, default=None, help="Write path when --apply-boxes (default: overwrite)")
    args = p.parse_args()

    pdf_path: Path = args.pdf
    if not pdf_path.is_file():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        print("Tip: npm run book:pdf:from-pages  (after Pages/ exist)", file=sys.stderr)
        return 1

    media_pt = in_to_pt(MEDIA_IN)
    bleed_pt = in_to_pt(BLEED_IN)
    trim_pt = in_to_pt(TRIM_IN)

    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        n = len(pdf.pages)
        print(f"PDF: {pdf_path}")
        print(f"Pages: {n}")
        ok = True
        for i, page in enumerate(pdf.pages, start=1):
            mb = page.mediabox
            w = float(mb[2]) - float(mb[0])
            h = float(mb[3]) - float(mb[1])
            # allow 1pt tolerance
            size_ok = abs(w - media_pt) < 1.0 and abs(h - media_pt) < 1.0
            if not size_ok:
                ok = False
            if i <= 3 or i == n or not size_ok:
                print(f"  p{i:02d} MediaBox={w:.1f}x{h:.1f} pt  ({'OK' if size_ok else 'CHECK'} expect ~{media_pt:.1f})")

            if args.apply_boxes:
                # Origin bottom-left; bleed = full media; trim inset 0.125"
                page.mediabox = Rectangle(0, 0, media_pt, media_pt)
                page.bleedbox = Rectangle(0, 0, media_pt, media_pt)
                page.trimbox = Rectangle(bleed_pt, bleed_pt, bleed_pt + trim_pt, bleed_pt + trim_pt)

        if args.apply_boxes:
            out = args.output or pdf_path
            pdf.save(out)
            print(f"Applied TrimBox/BleedBox → {out}")

    print("RESULT:", "PASS" if ok else "REVIEW sizes (may still print if Lulu accepts)")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
