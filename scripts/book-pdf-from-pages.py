"""Build a Lulu-oriented interior PDF from Pages/*.jpg via img2pdf (lossless)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PAGES = ROOT / "Pages"
DEFAULT_OUT = ROOT / "Output" / "The-Night-I-Met-Santa-INTERIOR-img2pdf.pdf"
PAGE_IN = 8.75  # trim 8.5 + 0.125" bleed each side @ 300 DPI assets


def main() -> int:
    try:
        import img2pdf
    except ImportError:
        print("img2pdf not installed. Run: python -m pip install img2pdf pikepdf", file=sys.stderr)
        return 1

    p = argparse.ArgumentParser(description="Pages/*.jpg → interior PDF (img2pdf)")
    p.add_argument("--pages-dir", type=Path, default=DEFAULT_PAGES)
    p.add_argument("--output", type=Path, default=DEFAULT_OUT)
    p.add_argument("--page-inches", type=float, default=PAGE_IN, help="Square page size in inches")
    args = p.parse_args()

    pages_dir: Path = args.pages_dir
    if not pages_dir.is_dir():
        print(f"Pages dir missing: {pages_dir}", file=sys.stderr)
        return 1

    files = sorted(pages_dir.glob("page-*.jpg")) + sorted(pages_dir.glob("page-*.jpeg"))
    files += sorted(pages_dir.glob("page-*.png"))
    # de-dupe while preserving order
    seen: set[str] = set()
    ordered: list[Path] = []
    for f in files:
        key = f.name.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(f)

    if not ordered:
        print(f"No page-*.{{jpg,png}} in {pages_dir} — run book:composite first.", file=sys.stderr)
        return 1

    out: Path = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    side = img2pdf.in_to_pt(args.page_inches)
    layout = img2pdf.get_layout_fun(pagesize=(side, side))

    with open(out, "wb") as fh:
        fh.write(img2pdf.convert([str(f) for f in ordered], layout_fun=layout))

    print(f"Wrote {out} ({len(ordered)} pages @ {args.page_inches}\" square)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
