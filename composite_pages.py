"""
Direct composite: illustration + soft feathered light wash area + poem text.
No external wash images — Pillow draws the feathered gradient directly.
Clean, reliable, no transparency issues.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

from pathlib import Path
ROOT = Path(__file__).resolve().parent
MEDIA = str(ROOT / "Media")
OUTPUT = str(ROOT / "Pages")
os.makedirs(OUTPUT, exist_ok=True)

DPI = 300
TRIM_IN = 8.5
BLEED_IN = 0.125
PAGE_IN = TRIM_IN + (2 * BLEED_IN)  # 8.75" Lulu full-bleed page
PAGE_PX = int(PAGE_IN * DPI)  # 2625
# Spread masters (generate separately): 5250 x 2625 then split
JPEG_QUALITY = 92
# Keep text/faces >= 0.5" inside trim (= 0.625" from bleed edge)
SAFE_MARGIN_PX = int((BLEED_IN + 0.5) * DPI)  # ~187

try:
    font_path = "C:/Windows/Fonts/georgia.ttf"
    poem_font = ImageFont.truetype(font_path, 46)
except:
    poem_font = ImageFont.load_default()

spreads = [
    ("scene-01-the-sneak-LANDSCAPE.png", "bl", [
        "I searched and I peeked", "when I first heard the noise.",
        "Something or someone", "was in with the toys.", "",
        "I slithered and crawled", "for a peek of a glimpse.",
        "It must be some fairies", "or holiday imps.",
    ]),
    ("scene-02-at-the-door.png", "tr", [
        "I got up the nerve", "to go to the door,",
        "a door that was decorated,", "bolted and locked.", "",
        "I didn't know it", "when I entered the room",
        "to surprise the amazement", "or even the shock.",
    ]),
    ("scene-02b-sneak-up-santa-LANDSCAPE.png", "bl", [
        "Now I'm usually calm,", "not very loud,",
        "or even known to be a ranter.", "",
        "But what do you say", "when you sneak up on Santa?",
    ]),
    ("scene-04b-santas-splendor-LANDSCAPE.png", "bl", [
        "My jaw dropped", "when our eyes finally met.",
        "I knew right then,", "it was a moment", "I would never forget.", "",
        "For there he was", "in all his splendor,",
        "brilliant white hair,", "red coat with suspenders.",
    ]),
    ("scene-05-the-chat-PORTRAIT.png", "br", [
        "He was down on the floor", "between boxes, gifts",
        "and ribbons galore.", "", "I couldn't move,",
        "I stayed very still.", "Finally he whispered,",
        "\u201cSit over here.", "Have a moment to kill.\u201d",
    ]),
    ("scene-06-cocoa-reveal-SQUARE.png", "tl", [
        "Oh, what a feeling,", "such a thrill.",
        "We chatted and laughed", "what seemed like an hour.", "",
        "But with laughs, stories", "and chatter, who cares,",
        "it didn't much matter.",
    ]),
    ("scene-06b-santas-stories-LANDSCAPE.png", "bl", [
        "He spoke of many places,", "people and things.",
        "From toys to music", "to bright diamond rings.", "",
        "Coats made of wool,", "ties made of silk.",
        "He even revealed his passion", "for hot cocoa",
        "instead of cold milk.",
    ]),
    ("scene-07-camera-dash-PORTRAIT.png", "bc", [
        "When I heard all the noise", "up in the roof,",
        "it hit me right then.", "I needed some proof.", "",
        "Where can I go?", "What can I get?",
        "I know, a photo.", "That's my best bet.",
    ]),
    ("scene-08b-the-dash-santa-gone-PORTRAIT.png", "tr", [
        "I flew out the door", "and was back in a flash.",
        "But oh no, the hour", "had already passed.", "",
        "And from the noise", "on top of the roof",
        "I realized that I was", "still without proof.",
    ]),
    ("scene-08-the-search-PORTRAIT.png", "bl", [
        "I turned around slowly.", "I needed to know,",
        "did he leave me a hint,", "a tip or a clue?", "",
        "Did he forget his hat", "or maybe a shoe?",
        "Now what am I", "supposed to do?",
    ]),
    ("scene-10b-the-flue-and-chair-PORTRAIT.png", "br", [
        "I know, I'll look up the flue.", "I dashed to the flue",
        "but nothing was there.", "", "I looked over here",
        "and I looked over there.", "When I saw something",
        "on top of the chair,", "", "my proof I thought",
        "was just laying right there.",
    ]),
    ("scene-09-the-note-LANDSCAPE.png", "bl", [
        "It wasn't a shoe,", "hat or a coat.",
        "I couldn't believe it,", "the old guy.", "He left me a note.", "",
        "I fell on the chair", "and started to stare.",
        "What it said,", "I didn't care.",
    ]),
    ("scene-12b-tearing-open-PORTRAIT.png", "br", [
        "I tore open the note", "that Santa had wrote.",
        "The words jumped out", "as to get my attention.", "",
        "And there was one thing", "he told me to mention.",
    ]),
    ("scene-14b-what-he-wants-message-LANDSCAPE.png", "tl", [
        "More than cakes,", "cocoa or milk.",
        "Shirts made of cotton", "or ties made of silk.", "",
        "Hats, stockings", "or a new coat.",
        "What he wants", "is simply a note.",
    ]),
    ("scene-10-santas-message-LANDSCAPE.png", "bc", [
        "He said I've had enough", "eggnogs, cider and soups.",
        "My belt's getting harder", "to fit in the loops.", "",
        "And one last thing,", "please do me a favor.",
        "Always love Christmas,", "act like a kid",
        "and pray to your Savior.",
    ]),
]

def draw_feathered_wash(draw, x, y, w, h, feather=80):
    """Draw a soft cream wash with feathered edges using concentric rectangles."""
    cream = (252, 248, 240)  # warm ivory
    # Draw from smallest (opaque) to largest (transparent)
    steps = 20
    for i in range(steps):
        alpha = int(180 * (1 - i / steps))  # 180 → 0
        r, g, b = cream
        expand = int(feather * i / steps)
        color = (r, g, b, alpha)
        # Create a small overlay image for this rectangle
        overlay = Image.new("RGBA", (w + 2*expand, h + 2*expand), (0,0,0,0))
        odraw = ImageDraw.Draw(overlay)
        odraw.rectangle([0, 0, w + 2*expand - 1, h + 2*expand - 1], fill=(r, g, b, alpha))
        # Paste with alpha
        draw._image.paste(overlay, (x - expand, y - expand), overlay)

def add_soft_wash_and_text(result, position, lines):
    """Add a soft feathered wash area and text directly to the image."""
    # Calculate text block size
    line_height = 54
    max_line_w = 0
    draw_temp = ImageDraw.Draw(Image.new("RGB", (1,1)))
    for line in lines:
        if line:
            bbox = draw_temp.textbbox((0,0), line, font=poem_font)
            max_line_w = max(max_line_w, bbox[2] - bbox[0])
    
    text_w = max_line_w + 80
    text_h = len(lines) * line_height + 60
    feather = 120
    
    # Position — stay inside Lulu safety (outside trim+bleed danger zone)
    margin = SAFE_MARGIN_PX
    if position == "bl":
        wash_x = margin
        wash_y = PAGE_PX - text_h - margin
    elif position == "br":
        wash_x = PAGE_PX - text_w - margin
        wash_y = PAGE_PX - text_h - margin
    elif position == "tl":
        wash_x = margin
        wash_y = margin
    elif position == "tr":
        wash_x = PAGE_PX - text_w - margin
        wash_y = margin
    elif position == "bc":
        wash_x = (PAGE_PX - text_w) // 2
        wash_y = PAGE_PX - text_h - margin
    
    # Draw soft feathered wash using repeated rectangles with decreasing opacity
    cream = (252, 248, 240)
    for i in range(30):
        alpha = int(200 * (1 - i/30))
        expand = int(feather * i / 30)
        overlay = Image.new("RGBA", (text_w + 2*expand, text_h + 2*expand), (0,0,0,0))
        odraw = ImageDraw.Draw(overlay)
        odraw.rectangle([0, 0, text_w + 2*expand - 1, text_h + 2*expand - 1], 
                       fill=(cream[0], cream[1], cream[2], alpha))
        result.paste(overlay, (wash_x - expand, wash_y - expand), overlay)
    
    # Draw text
    draw = ImageDraw.Draw(result)
    dark = (26, 26, 26)
    tx = wash_x + 40
    ty = wash_y + 30
    for line in lines:
        if line == "":
            ty += 28
        else:
            draw.text((tx, ty), line, fill=dark, font=poem_font)
            ty += line_height

for idx, (ill_file, position, lines) in enumerate(spreads):
    ill_path = os.path.join(MEDIA, ill_file)
    if not os.path.exists(ill_path):
        print(f"SKIP {ill_file}")
        continue
    
    result = Image.open(ill_path).convert("RGBA").resize((PAGE_PX, PAGE_PX), Image.LANCZOS)
    add_soft_wash_and_text(result, position, lines)
    result = result.convert("RGB")
    
    out_name = f"page-{idx+1:02d}.jpg"
    out_path = os.path.join(OUTPUT, out_name)
    result.save(out_path, "JPEG", quality=JPEG_QUALITY)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"[{idx+1:2d}] {out_name} — {size_kb:.0f} KB — {lines[0]}")

print(f"\nDone! {len(spreads)} pages.")
