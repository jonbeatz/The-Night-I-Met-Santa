#!/usr/bin/env python3
"""Build a trim-only flipbook PDF from Lulu deliverables.

- Interior: crop each page to TrimBox (8.5x8.5) — strips bleed that breaks
  seamless gutters when a 3D flipbook tiles MediaBoxes side-by-side.
- Cover: extract FRONT and BACK panels from the one-piece wrap (trim 8.5x8.5).
- Order: Front → burgundy IFC → interior → burgundy IBC → Back
  so opening the cover shows blank burgundy LEFT | page 01 RIGHT,
  then the next flip is the first seamless spread.

Does NOT replace the Lulu print PDF (keep bleed there).
"""
from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
# Deliverable interior = v2 burgundy-open (32 pp). Rollback 30-pp FINAL kept separately.
INTERIOR = ROOT / "Output/interiors/TNIMS-Interior-FINAL-v2-burgundy-open-Lulu.pdf"
COVER = ROOT / "Output/covers/TNIMS-Cover-FINAL-Lulu.pdf"
OUT = ROOT / "Output/interiors/TNIMS-FLIPBOOK-trim.pdf"

# Cover wrap: BACK (8.75) | SPINE (0.75) | FRONT (8.75) = 18.25 x 8.75 in
BLEED = 0.125
PANEL = 8.75
SPINE = 0.75
TRIM = 8.5
# Casewrap / flipbook blank burgundy (LOCKED 2026-07-31 — Jon)
# Hex #4A0E17 = RGB(74, 14, 23). Supersedes older RGB(90,22,18)/#5A1612 pastedown fill.
BURGUNDY = (0x4A / 255, 0x0E / 255, 0x17 / 255)  # PDF RGB 0..1
BURGUNDY_HEX = "#4A0E17"
BURGUNDY_RGB = (0x4A, 0x0E, 0x17)


def _in_to_pt(inches: float) -> float:
    return inches * 72.0


def _trim_rect_on_panel(panel_left_in: float) -> fitz.Rect:
    """8.5x8.5 trim inside an 8.75 panel starting at panel_left_in."""
    x0 = _in_to_pt(panel_left_in + BLEED)
    y0 = _in_to_pt(BLEED)
    x1 = _in_to_pt(panel_left_in + BLEED + TRIM)
    y1 = _in_to_pt(BLEED + TRIM)
    return fitz.Rect(x0, y0, x1, y1)


def _page_from_clip(src_page: fitz.Page, clip: fitz.Rect, dpi: int = 150) -> fitz.Document:
    """Rasterize a clip to a single-page PDF at TRIM inches (good for flipbooks)."""
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = src_page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    img_doc = fitz.open()
    # page size in points = trim inches
    w_pt = _in_to_pt(TRIM)
    h_pt = _in_to_pt(TRIM)
    page = img_doc.new_page(width=w_pt, height=h_pt)
    page.insert_image(page.rect, pixmap=pix)
    return img_doc


def _crop_interior_page(src_page: fitz.Page) -> fitz.Document:
    """Prefer TrimBox crop via show_pdf_page (keeps text sharp)."""
    trim = src_page.trimbox
    if trim.is_empty or abs(trim.width - _in_to_pt(TRIM)) > 1:
        # fallback: inset MediaBox by bleed
        mb = src_page.mediabox
        trim = fitz.Rect(
            mb.x0 + _in_to_pt(BLEED),
            mb.y0 + _in_to_pt(BLEED),
            mb.x1 - _in_to_pt(BLEED),
            mb.y1 - _in_to_pt(BLEED),
        )
    out = fitz.open()
    page = out.new_page(width=_in_to_pt(TRIM), height=_in_to_pt(TRIM))
    page.show_pdf_page(page.rect, src_page.parent, src_page.number, clip=trim)
    return out


def _burgundy_page(pastedown: Path | None = None) -> fitz.Document:
    """Solid burgundy pastedown page at trim size (optional PNG fill)."""
    out = fitz.open()
    w_pt = _in_to_pt(TRIM)
    h_pt = _in_to_pt(TRIM)
    page = out.new_page(width=w_pt, height=h_pt)
    if pastedown and pastedown.is_file():
        page.insert_image(page.rect, filename=str(pastedown))
    else:
        page.draw_rect(page.rect, color=None, fill=BURGUNDY, width=0)
    return out


def main() -> None:
    if not INTERIOR.is_file():
        raise SystemExit(f"Missing interior: {INTERIOR}")
    if not COVER.is_file():
        raise SystemExit(f"Missing cover: {COVER}")

    pastedown = ROOT / "Media/development/Cover/pastedown-burgundy.png"
    interior = fitz.open(INTERIOR)
    cover = fitz.open(COVER)
    cover_page = cover[0]

    back_clip = _trim_rect_on_panel(0.0)
    front_clip = _trim_rect_on_panel(PANEL + SPINE)  # 9.5"

    # Cover panels: rasterize at 300 DPI so type stays crisp in flipbook
    front_doc = _page_from_clip(cover_page, front_clip, dpi=300)
    back_doc = _page_from_clip(cover_page, back_clip, dpi=300)
    ifc = _burgundy_page(pastedown)  # inside front cover (left after open)
    ibc = _burgundy_page(pastedown)  # inside back cover (before back)

    flip = fitz.open()
    # Front cover → burgundy IFC → page 01… → burgundy IBC → back cover
    # Open cover: LEFT=burgundy, RIGHT=interior page 1 (title)
    # Next flip: interior 2|3 (first seamless spread)
    flip.insert_pdf(front_doc)
    flip.insert_pdf(ifc)
    for i in range(interior.page_count):
        one = _crop_interior_page(interior[i])
        flip.insert_pdf(one)
        one.close()
    flip.insert_pdf(ibc)
    flip.insert_pdf(back_doc)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    flip.save(OUT, deflate=True, garbage=4)
    print(f"Wrote {OUT}")
    print(
        f"  pages: {flip.page_count} "
        f"(front + burgundy IFC + {interior.page_count} interior + burgundy IBC + back)"
    )
    print(f"  page size: {TRIM}\" x {TRIM}\" (trim only, no bleed)")
    print(f"  pastedown: {pastedown.name if pastedown.is_file() else f'solid {BURGUNDY_HEX}'}")
    print(f"  size: {OUT.stat().st_size / 1e6:.2f} MB")
    print("  open order: cover -> [burgundy | page01] -> [spread 2|3] ... -> [burgundy | back]")

    front_doc.close()
    back_doc.close()
    ifc.close()
    ibc.close()
    interior.close()
    cover.close()
    flip.close()


if __name__ == "__main__":
    main()
