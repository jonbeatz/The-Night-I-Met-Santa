#!/usr/bin/env python3
"""
Build wrap-around cover for "The Night I Met Santa"
Front + Spine + Back as one wide PDF
Uses pypdf + Pillow — no GTK/Cairo dependencies.
"""
import os
from PIL import Image, ImageDraw, ImageFont

from pathlib import Path
ROOT = Path(__file__).resolve().parent
MEDIA = str(ROOT / "Media")
OUTPUT = str(ROOT / "Output")
os.makedirs(OUTPUT, exist_ok=True)

# Book specs
PAGE_W = 8.5
PAGE_H = 8.5
BLEED = 0.125
DPI = 300

# 40 interior pages → spine width
interior_pages = 40
sheets = interior_pages / 2
SPINE_PB = max(0.08, sheets * 0.004)    # paperback
SPINE_HC = SPINE_PB + 0.125              # hardcover

print(f"Pages: {interior_pages}, Spine PB: {SPINE_PB:.3f}\", Spine HC: {SPINE_HC:.3f}\"")

# Convert inches to pixels at DPI
def inch_to_px(inches):
    return int(inches * DPI)

# Cover dimensions
cover_w = PAGE_W + PAGE_W + SPINE_PB  # back + spine + front
cover_w_bleed = cover_w + 2 * BLEED
cover_h_bleed = PAGE_H + 2 * BLEED

px_w = inch_to_px(cover_w_bleed)
px_h = inch_to_px(cover_h_bleed)

# Positions in pixels
back_x = inch_to_px(BLEED)
spine_x = inch_to_px(BLEED + PAGE_W)
front_x = inch_to_px(BLEED + PAGE_W + SPINE_PB)
top_y = inch_to_px(BLEED)

spine_w = inch_to_px(SPINE_PB)
page_w_px = inch_to_px(PAGE_W)
page_h_px = inch_to_px(PAGE_H)

def build_cover(front_file, back_file, spine_width, output_name, is_hardcover=False):
    spine_w_px = inch_to_px(spine_width)
    total_w_bleed = page_w_px + spine_w_px + page_w_px + 2 * inch_to_px(BLEED)

    # Create canvas
    bg_color = (20, 25, 50)  # Dark navy
    img = Image.new("RGB", (total_w_bleed, px_h), bg_color)
    draw = ImageDraw.Draw(img)

    # Load and place front cover
    front_path = os.path.join(MEDIA, front_file)
    if os.path.exists(front_path):
        front_img = Image.open(front_path).resize((page_w_px, page_h_px), Image.LANCZOS)
        img.paste(front_img, (front_x, top_y))

    # Load and place back cover
    back_path = os.path.join(MEDIA, back_file)
    if os.path.exists(back_path):
        back_img = Image.open(back_path).resize((page_w_px, page_h_px), Image.LANCZOS)
        img.paste(back_img, (back_x, top_y))

    # Spine — deep red
    spine_red = (139, 21, 21)
    draw.rectangle([spine_x, top_y, spine_x + spine_w_px, top_y + page_h_px], fill=spine_red)

    # Try to load Georgia font for spine text
    try:
        font_path = "C:/Windows/Fonts/georgia.ttf"
        spine_font = ImageFont.truetype(font_path, 20)
        title_font = ImageFont.truetype(font_path, 72)
        author_font = ImageFont.truetype(font_path, 26)
        cover_desc_font = ImageFont.truetype(font_path, 22)
    except:
        spine_font = ImageFont.load_default()
        title_font = spine_font
        author_font = spine_font
        cover_desc_font = spine_font

    # Spine text — rotated 90 degrees
    spine_text = "THE NIGHT I MET SANTA  -  JACK FARRELL"
    # Create a separate image for rotated spine text
    from PIL import Image as PILImage

    # Measure text
    bbox = draw.textbbox((0, 0), spine_text, font=spine_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Create rotated text image
    text_img = PILImage.new("RGBA", (text_h + 20, text_w + 20), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((10, 10), spine_text, fill=(212, 168, 67), font=spine_font)  # Gold
    text_img = text_img.rotate(90, expand=True)

    # Place on spine
    text_ph = text_img.height
    text_pw = text_img.width
    tx = spine_x + (spine_w_px - text_pw) // 2
    ty = top_y + (page_h_px - text_ph) // 2
    if spine_w_px > 20:  # Only if spine is wide enough
        img.paste(text_img, (tx, ty), text_img)

    # Front cover title — gold
    title_color = (212, 168, 67)  # Gold
    white_color = (255, 255, 255)

    # "The Night" centered
    title1 = "The Night"
    bbox1 = draw.textbbox((0, 0), title1, font=title_font)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = front_x + (page_w_px - tw1) // 2
    draw.text((tx1, top_y + inch_to_px(0.6)), title1, fill=title_color, font=title_font)

    # "I Met Santa" centered below
    title2 = "I Met Santa"
    bbox2 = draw.textbbox((0, 0), title2, font=title_font)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = front_x + (page_w_px - tw2) // 2
    draw.text((tx2, top_y + inch_to_px(1.5)), title2, fill=title_color, font=title_font)

    # Author credit — bottom right
    author1 = "Written by"
    author2 = "Jack Farrell"
    abbox2 = draw.textbbox((0, 0), author2, font=author_font)
    aw2 = abbox2[2] - abbox2[0]
    ax = front_x + page_w_px - aw2 - inch_to_px(0.6)
    ay = top_y + page_h_px - inch_to_px(1.4)
    draw.text((ax, ay), author1, fill=(255, 255, 255, 200), font=cover_desc_font)
    draw.text((ax, ay + inch_to_px(0.3)), author2, fill=title_color, font=author_font)

    # Back cover description
    desc = [
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

    desc_y = top_y + inch_to_px(1.5)
    for line in desc:
        bbox = draw.textbbox((0, 0), line, font=cover_desc_font)
        lw = bbox[2] - bbox[0]
        lx = back_x + (page_w_px - lw) // 2
        color = white_color
        if line.startswith('"') or line.startswith("to your"):
            color = title_color
        draw.text((lx, desc_y), line, fill=color, font=cover_desc_font)
        desc_y += inch_to_px(0.25)

    # Save as PNG first (Pillow can't write multi-page PDFs natively)
    png_path = os.path.join(OUTPUT, f"{output_name}.png")
    img.save(png_path, dpi=(DPI, DPI))
    print(f"  Cover PNG: {png_path} ({os.path.getsize(png_path)//1024} KB)")

    # Convert to PDF using Pillow
    pdf_path = os.path.join(OUTPUT, output_name)
    img.convert("RGB").save(pdf_path, "PDF", resolution=DPI)
    print(f"  Cover PDF: {pdf_path} ({os.path.getsize(pdf_path)//1024} KB)")
    print(f"  Dimensions: {cover_w_bleed:.2f}\" x {cover_h_bleed:.2f}\" at {DPI} DPI")
    print(f"  Spine: {spine_width:.3f}\"")


# ── BUILD COVERS ──────────────────────────────────────────

# Best cover: house lights + snowman front, empty chair back
front_file = "cover-house-lights-snowman-PORTRAIT.png"
back_file = "back-cover-empty-chair-PORTRAIT.png"

# Paperback
build_cover(front_file, back_file, SPINE_PB, "The-Night-I-Met-Santa-COVER-pb-house.pdf")

# Hardcover
build_cover(front_file, back_file, SPINE_HC, "The-Night-I-Met-Santa-COVER-hc-house.pdf", is_hardcover=True)

print("\nDone!")
