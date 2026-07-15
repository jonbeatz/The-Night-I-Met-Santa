#!/usr/bin/env python3
"""
Build the WRAP-AROUND cover for "The Night I Met Santa"
Front + Spine + Back as one wide PDF
"""

import os
from fpdf import FPDF

from pathlib import Path
ROOT = Path(__file__).resolve().parent
MEDIA = str(ROOT / "Media")
OUTPUT = str(ROOT / "Output")
os.makedirs(OUTPUT, exist_ok=True)

# Book specs
PAGE_W = 8.5   # trim width
PAGE_H = 8.5   # trim height
BLEED = 0.125  # bleed on all sides

# Read interior page count to calculate spine
page_count_path = os.path.join(OUTPUT, "page_count.txt")
with open(page_count_path) as f:
    interior_pages = int(f.read().strip())

# Spine width calculation:
# Standard children's book paper: ~0.004" per sheet
# Sheets = pages / 2
sheets = interior_pages / 2
SPINE = max(0.08, sheets * 0.004)
# For hardcover, spine is slightly wider due to board thickness
SPINE_HARDCOVER = SPINE + 0.125

print(f"Interior pages: {interior_pages}")
print(f"Sheets: {sheets}")
print(f"Spine width (paperback): {SPINE:.3f}\"")
print(f"Spine width (hardcover): {SPINE_HARDCOVER:.3f}\"")

# Total cover width = back + spine + front + bleed on both sides
COVER_W = PAGE_W + SPINE + PAGE_W
COVER_W_BLEED = COVER_W + 2 * BLEED
COVER_H_BLEED = PAGE_H + 2 * BLEED


class CoverPDF(FPDF):
    def __init__(self, spine):
        super().__init__(unit='in', format=(COVER_W + 2 * BLEED, PAGE_H + 2 * BLEED))
        self.spine = spine
        self.set_auto_page_break(False)
        self.set_margin(0)

    def build(self, front_img, back_img, output_name):
        self.add_page()

        # ── BACKGROUND (solid dark color for bleed area) ──
        self.set_fill_color(20, 25, 50)
        self.rect(0, 0, COVER_W_BLEED, COVER_H_BLEED, 'F')

        # ── BACK COVER (left) ──
        bx = BLEED
        by = BLEED
        if os.path.exists(back_img):
            self.image(back_img, x=bx, y=by, w=PAGE_W, h=PAGE_H)

        # ── FRONT COVER (right) ──
        fx = BLEED + PAGE_W + self.spine
        fy = BLEED
        if os.path.exists(front_img):
            self.image(front_img, x=fx, y=fy, w=PAGE_W, h=PAGE_H)

        # ── SPINE ──
        sx = BLEED + PAGE_W
        sy = BLEED
        self.set_fill_color(120, 20, 20)  # Deep red spine
        self.rect(sx, sy, self.spine, PAGE_H, 'F')

        # Spine text (vertical — rotated)
        if self.spine > 0.1:
            self.set_font('Times', 'B', 10)
            self.set_text_color(255, 255, 255)
            # fpdf2 doesn't do rotation natively in the simple way,
            # so we skip spine text for now or use a tiny font horizontally
            # For spine > 0.15", place small horizontal text centered
            if self.spine > 0.15:
                self.set_font('Times', 'B', 7)
                # Write vertically by placing characters
                spine_text = "THE NIGHT I MET SANTA  -  JACK FARRELL"
                char_h = 0.2
                start_y = sy + (PAGE_H - len(spine_text) * char_h) / 2
                for i, ch in enumerate(spine_text):
                    self.set_xy(sx + 0.02, start_y + i * char_h)
                    self.cell(self.spine - 0.04, char_h, ch, align='C')

        # ── TRIM MARKS (optional guide lines) ──
        # We'll skip for now — Lulu/Blurb add their own

        # ── FRONT COVER TEXT ──
        # Title on front cover
        self.set_font('Times', 'B', 36)
        self.set_text_color(255, 220, 100)  # Gold
        title_y = fy + 0.6

        self.set_xy(fx, title_y)
        self.cell(PAGE_W, 0.8, 'The Night', align='C')
        self.set_xy(fx, title_y + 0.7)
        self.cell(PAGE_W, 0.8, 'I Met Santa', align='C')

        # Author
        self.set_font('Times', 'I', 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(fx + PAGE_W - 3.5, fy + PAGE_H - 1.2)
        self.cell(3.0, 0.4, 'Written by', align='R')
        self.set_xy(fx + PAGE_W - 3.5, fy + PAGE_H - 0.8)
        self.cell(3.0, 0.4, 'Jack Farrell', align='R')

        # ── BACK COVER TEXT ──
        self.set_font('Times', 'I', 12)
        self.set_text_color(255, 255, 255)

        # Book description on back
        desc_y = by + PAGE_H * 0.15
        self.set_xy(bx + 0.8, desc_y)
        desc_lines = [
            "A young child sneaks downstairs",
            "on Christmas Eve and discovers",
            "Santa Claus in the living room.",
            "",
            "What follows is a magical",
            "conversation, a frantic dash",
            "for a camera, and a note",
            "left behind that reveals",
            "the true meaning of Christmas.",
            "",
            '"Always love Christmas,',
            'act like a kid and pray',
            'to your Savior."',
        ]
        for line in desc_lines:
            self.set_x(bx + 0.8)
            self.cell(PAGE_W - 1.6, 0.3, line, align='C', new_x="LMARGIN", new_y="NEXT")

        # Save
        out = os.path.join(OUTPUT, output_name)
        self.output(out)
        print(f"✅ Cover saved: {out}")
        print(f"   Dimensions: {COVER_W_BLEED:.2f}\" x {COVER_H_BLEED:.2f}\"")
        print(f"   Spine: {self.spine:.3f}\"")


# ═══════════════════════════════════════════
# BUILD BOTH COVERS
# ═══════════════════════════════════════════

# Best cover options
covers = [
    # (front_img, back_img, label)
    ('cover-house-lights-snowman-PORTRAIT.png', 'back-cover-empty-chair-PORTRAIT.png', 'house'),
    ('cover-santa-shush-PORTRAIT.png', 'back-cover-empty-chair-PORTRAIT.png', 'santa'),
    ('cover-child-santa-tree-PORTRAIT.png', 'back-cover-empty-chair-PORTRAIT.png', 'child'),
]

for front_file, back_file, label in covers:
    front = os.path.join(MEDIA, front_file)
    back = os.path.join(MEDIA, back_file)

    # Paperback cover
    pdf = CoverPDF(SPINE)
    pdf.build(front, back, f"The-Night-I-Met-Santa-COVER-pb-{label}.pdf")

    # Hardcover cover (wider spine)
    pdf = CoverPDF(SPINE_HARDCOVER)
    pdf.build(front, back, f"The-Night-I-Met-Santa-COVER-hc-{label}.pdf")

print("\n✅ All covers built!")
