"""Deep audit Phase 1 — stitch / promote / spine placeholder. No content regen."""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PAGE = 2625
SPREAD = (5250, 2625)


def main() -> None:
    report: list[str] = []

    # --- 1. P-quiet-close stitch ---
    qc = ROOT / "Media/development/P-quiet-close"
    left = Image.open(qc / "art-left.png").convert("RGB")
    right = Image.open(qc / "art-right.png").convert("RGB")
    assert left.size == (PAGE, PAGE), left.size
    assert right.size == (PAGE, PAGE), right.size
    spread = Image.new("RGB", SPREAD)
    spread.paste(left, (0, 0))
    spread.paste(right, (PAGE, 0))
    out = qc / "art.png"
    spread.save(out, optimize=True)
    report.append(f"1 OK stitch {out.relative_to(ROOT)} → {spread.size}")

    # --- 2. Cover promote 2625 ---
    cover = ROOT / "Media/development/Cover"
    src = cover / "art-2625.png"
    art = cover / "art.png"
    bak = cover / "art-1024-backup.png"
    assert src.is_file() and Image.open(src).size == (PAGE, PAGE)
    if not bak.exists():
        shutil.copy2(art, bak)
        report.append(f"2 OK backup {bak.name} ({Image.open(bak).size})")
    else:
        report.append(f"2 note backup already exists {bak.name}")
    shutil.copy2(src, art)
    report.append(f"2 OK promote art-2625 → art.png now {Image.open(art).size}")

    # --- 3. P01 promote 2625 ---
    p01 = ROOT / "Media/development/P01-title"
    p01_src = p01 / "art-2625.png"
    p01_art = p01 / "art.png"
    if p01_src.is_file():
        before = Image.open(p01_art).size
        bak01 = p01 / "art-2048-backup.png"
        if not bak01.exists():
            shutil.copy2(p01_art, bak01)
            report.append(f"3 OK backup {bak01.name} ({before})")
        else:
            report.append(f"3 note backup already exists {bak01.name}")
        shutil.copy2(p01_src, p01_art)
        report.append(
            f"3 OK promote art-2625 → art.png was {before} now {Image.open(p01_art).size}"
        )
    else:
        sz = Image.open(p01_art).size if p01_art.exists() else None
        report.append(f"3 FLAG no art-2625; art.png={sz}")

    # --- 4. Spine placeholder ---
    # Provisional ~0.75" @ 300dpi = 225px; exact width from Lulu calculator after page count lock
    spine_w = 225
    spine_h = PAGE
    cream = (245, 236, 220)
    burgundy = (90, 22, 18)
    dark = (44, 44, 44)
    spine = Image.new("RGB", (spine_w, spine_h), cream)
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 36)
        font_name = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 28)
    except OSError:
        font_title = ImageFont.load_default()
        font_name = font_title

    tmp = Image.new("RGBA", (spine_h, spine_w), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    title = "The Night I Met Santa"
    author = "Jon Beatz"
    bb1 = td.textbbox((0, 0), title, font=font_title)
    bb2 = td.textbbox((0, 0), author, font=font_name)
    tw1, th1 = bb1[2] - bb1[0], bb1[3] - bb1[1]
    tw2, th2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
    gap = 40
    total_w = tw1 + gap + tw2
    x0 = (spine_h - total_w) // 2
    y_mid = spine_w // 2
    td.text((x0, y_mid - th1 // 2), title, fill=dark, font=font_title)
    td.text((x0 + tw1 + gap, y_mid - th2 // 2), author, fill=burgundy, font=font_name)
    rotated = tmp.rotate(90, expand=True).convert("RGB")
    # After 90° expand: expect (spine_w, spine_h)
    if rotated.size != (spine_w, spine_h):
        rotated = rotated.resize((spine_w, spine_h), Image.Resampling.LANCZOS)
    spine.paste(rotated, (0, 0))
    draw = ImageDraw.Draw(spine)
    draw.rectangle([0, spine_h - 40, spine_w, spine_h], fill=burgundy)

    spine_path = cover / "art-spine.png"
    spine.save(spine_path, optimize=True)
    report.append(
        f"4 OK spine placeholder {spine_path.relative_to(ROOT)} "
        f"{spine.size} (provisional {spine_w}px ≈ 0.75in @300dpi — Lulu calc TBD)"
    )

    print("\n".join(report))


if __name__ == "__main__":
    main()
