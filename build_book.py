#!/usr/bin/env python3
"""
"The Night I Met Santa" — Professional Children's Book PDF
8.5 x 8.5 inches, print-ready interior
"""

import os
from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
MEDIA = str(ROOT / "Media")
OUTPUT = str(ROOT / "Output")
os.makedirs(OUTPUT, exist_ok=True)

PAGE_W = 8.5
PAGE_H = 8.5

# Colors
RED_TITLE = (180, 30, 30)
DARK_TEXT = (30, 30, 30)
MEDIUM_TEXT = (60, 60, 60)
LIGHT_TEXT = (120, 120, 120)


class BookPDF(FPDF):
    def __init__(self):
        super().__init__(unit='in', format=(PAGE_W, PAGE_H))
        self.set_auto_page_break(False)
        self.set_margin(0)
        self.current_page_is_left = True  # Track spread layout

    def blank_page(self):
        self.add_page()

    # ── TEXT PAGES ──────────────────────────────────────

    def _poem_font(self):
        self.set_font('Times', '', 15)
        self.set_text_color(*DARK_TEXT)

    def text_page(self, lines, page_num=None):
        """A page with poem text, centered vertically-ish."""
        self.add_page()
        margin = 1.2
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_font('Times', '', 16)
        self.set_text_color(*DARK_TEXT)

        # Calculate text height to center
        line_height = 0.35
        total_lines = len(lines) + sum(1 for l in lines if l.strip() == '')
        text_h = total_lines * line_height
        start_y = max(1.5, (PAGE_H - text_h) / 2)

        self.set_y(start_y)
        for i, line in enumerate(lines):
            if line.strip() == '':
                self.ln(line_height)
            else:
                self.multi_cell(PAGE_W - 2 * margin, line_height, line.strip(), align='L')
                if i < len(lines) - 1:
                    self.ln(0.05)

    # ── IMAGE PAGES ─────────────────────────────────────

    def full_page_img(self, path):
        """Image filling entire trim area."""
        self.add_page()
        if os.path.exists(path):
            self.image(path, x=0, y=0, w=PAGE_W, h=PAGE_H)
        else:
            self.set_font('Helvetica', '', 10)
            self.set_text_color(200, 0, 0)
            self.set_y(4)
            self.cell(0, 0.5, f'[Missing: {os.path.basename(path)}]', align='C')

    def spread_img(self, path):
        """Landscape image that spans a full spread.
        We display it across two consecutive pages as best as fpdf allows.
        For now: place centered with letterboxing on one page, 
        then we show the companion text on the facing page."""
        self.add_page()
        if os.path.exists(path):
            # Place landscape image in upper portion
            img_h = 5.0
            self.image(path, x=0, y=0.5, w=PAGE_W, h=img_h)
        else:
            self.set_font('Helvetica', '', 10)
            self.set_text_color(200, 0, 0)
            self.set_y(3)
            self.cell(0, 0.5, f'[Missing: {os.path.basename(path)}]', align='C')

    def spot_img(self, path, x, y, w, h):
        """Small illustration placed on a text page."""
        if os.path.exists(path):
            self.image(path, x=x, y=y, w=w, h=h)

    # ── FRONT MATTER ────────────────────────────────────

    def half_title(self):
        self.add_page()
        self.set_font('Times', 'B', 22)
        self.set_text_color(*RED_TITLE)
        self.set_y(3.3)
        self.cell(0, 0.6, 'The Night', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 0.6, 'I Met Santa', align='C')

    def title_page(self):
        self.add_page()

        # Hands writing image as background element
        hands = os.path.join(MEDIA, "hands-writing-overhead-v3.png")
        if os.path.exists(hands):
            self.image(hands, x=0, y=0, w=PAGE_W, h=PAGE_H)

        # Semi-transparent overlay for text readability
        # (fpdf2 doesn't do transparency natively, so we place text over darker areas)

        # Title
        self.set_font('Times', 'B', 28)
        self.set_text_color(*RED_TITLE)
        self.set_y(1.2)
        self.cell(0, 0.7, 'The Night', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 0.7, 'I Met Santa', align='C', new_x="LMARGIN", new_y="NEXT")

        self.ln(0.5)
        self.set_font('Times', 'I', 16)
        self.set_text_color(*MEDIUM_TEXT)
        self.cell(0, 0.4, 'Written by Jack Farrell', align='C', new_x="LMARGIN", new_y="NEXT")

        self.ln(0.8)
        self.set_font('Times', 'I', 11)
        self.set_text_color(*LIGHT_TEXT)
        self.cell(0, 0.3, 'Illustrations generated with AI', align='C')

    def author_page(self):
        self.add_page()

        # Author portrait
        jack = os.path.join(MEDIA, "jack-writing-at-desk-PORTRAIT.png")
        if os.path.exists(jack):
            self.image(jack, x=1.5, y=0.8, w=5.5, h=5.5)

        self.set_y(6.8)
        self.set_font('Times', 'B', 16)
        self.set_text_color(*RED_TITLE)
        self.cell(0, 0.4, 'About the Author', align='C', new_x="LMARGIN", new_y="NEXT")

        self.ln(0.2)
        self.set_font('Times', '', 11)
        self.set_text_color(*MEDIUM_TEXT)
        self.set_left_margin(1.0)
        self.set_right_margin(1.0)
        bio = (
            'Jack Farrell wrote "The Night I Met Santa" for his family, '
            'capturing the wonder of a child who sneaks downstairs on '
            'Christmas Eve and meets Santa Claus face to face. '
            'A father and grandfather, Jack\'s poem has been treasured '
            'by his family for decades. This book brings his words to '
            'life so that children everywhere can share in the magic.'
        )
        self.multi_cell(PAGE_W - 2.0, 0.25, bio, align='C')

    # ── BACK MATTER ─────────────────────────────────────

    def closing_page(self):
        self.add_page()
        self.set_font('Times', 'I', 16)
        self.set_text_color(*MEDIUM_TEXT)
        self.set_y(3.0)
        self.cell(0, 0.5, '"Always love Christmas,', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 0.5, 'act like a kid and pray to your Savior."', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)
        self.set_font('Times', 'I', 13)
        self.cell(0, 0.4, '- Santa Claus', align='C')

        self.ln(1.2)
        self.set_font('Times', 'I', 12)
        self.set_text_color(*LIGHT_TEXT)
        self.cell(0, 0.3, 'For my family, with love.', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 0.3, '- Jack Farrell', align='C')

    def copyright_page(self):
        """Copyright / colophon."""
        self.add_page()
        self.set_font('Times', '', 9)
        self.set_text_color(*LIGHT_TEXT)
        self.set_y(6.5)
        text = (
            'Copyright (c) Jack Farrell. All rights reserved.\n'
            'No part of this book may be reproduced without permission.\n'
            'Illustrations created using AI image generation.\n'
            'Printed in the United States of America.\n'
            'First Edition, 2026.'
        )
        self.set_left_margin(1.5)
        self.multi_cell(PAGE_W - 3.0, 0.2, text, align='C')


# ═══════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════

def build():
    pdf = BookPDF()

    # ── FRONT MATTER ──
    pdf.half_title()
    pdf.blank_page()
    pdf.title_page()
    pdf.copyright_page()
    pdf.author_page()

    # ── POEM BODY ──
    # Each stanza is paired with an illustration.
    # Layout: text on left page, image on right page (or spread across both)

    stanzas = [
        # 0: The Sneak
        [
            "I searched and I peeked",
            "when I first heard the noise.",
            "Something or someone",
            "was in with the toys.",
            "",
            "I slithered and crawled",
            "for a peek of a glimpse.",
            "It must be some fairies",
            "or holiday imps."
        ],
        # 1: At the Door
        [
            "I got up the nerve",
            "to go to the door,",
            "a door that was decorated,",
            "bolted and locked.",
            "",
            "I didn't know it",
            "when I entered the room",
            "to surprise the amazement",
            "or even the shock."
        ],
        # 2: Sneak up on Santa
        [
            "Now I'm usually calm,",
            "not very loud,",
            "or even known to be a ranter.",
            "",
            "But what do you say",
            "when you sneak up on Santa?"
        ],
        # 3: The Meeting
        [
            "My jaw dropped",
            "when our eyes finally met.",
            "I knew right then,",
            "it was a moment",
            "I would never forget.",
            "",
            "For there he was",
            "in all his splendor,",
            "brilliant white hair,",
            "red coat with suspenders."
        ],
        # 4: Santa on the Floor
        [
            "He was down on the floor",
            "between boxes, gifts",
            "and ribbons galore.",
            "",
            "I couldn't move,",
            "I stayed very still.",
            "Finally he whispered,",
            '"Sit over here.',
            'Have a moment to kill."'
        ],
        # 5: The Chat
        [
            "Oh, what a feeling,",
            "such a thrill.",
            "We chatted and laughed",
            "what seemed like an hour.",
            "",
            "But with laughs, stories",
            "and chatter, who cares,",
            "it didn't much matter."
        ],
        # 6: Santa's Stories
        [
            "He spoke of many places,",
            "people and things.",
            "From toys to music",
            "to bright diamond rings.",
            "",
            "Coats made of wool,",
            "ties made of silk.",
            "He even revealed his passion",
            "for hot cocoa",
            "instead of cold milk."
        ],
        # 7: The Camera Idea
        [
            "When I heard all the noise",
            "up in the roof,",
            "it hit me right then.",
            "I needed some proof.",
            "",
            "Where can I go?",
            "What can I get?",
            "I know, a photo.",
            "That's my best bet."
        ],
        # 8: The Dash
        [
            "I flew out the door",
            "and was back in a flash.",
            "But oh no, the hour",
            "had already passed.",
            "",
            "And from the noise",
            "on top of the roof",
            "I realized that I was",
            "still without proof."
        ],
        # 9: The Search
        [
            "I turned around slowly.",
            "I needed to know,",
            "did he leave me a hint,",
            "a tip or a clue?",
            "",
            "Did he forget his hat",
            "or maybe a shoe?",
            "Now what am I",
            "supposed to do?"
        ],
        # 10: The Flue
        [
            "I know, I'll look up the flue.",
            "I dashed to the flue",
            "but nothing was there.",
            "",
            "I looked over here",
            "and I looked over there.",
            "When I saw something",
            "on top of the chair,",
            "",
            "my proof I thought",
            "was just laying right there."
        ],
        # 11: The Note
        [
            "It wasn't a shoe,",
            "hat or a coat.",
            "I couldn't believe it,",
            "the old guy.",
            "He left me a note.",
            "",
            "I fell on the chair",
            "and started to stare.",
            "What it said,",
            "I didn't care."
        ],
        # 12: Tearing Open
        [
            "I tore open the note",
            "that Santa had wrote.",
            "The words jumped out",
            "as to get my attention.",
            "",
            "And there was one thing",
            "he told me to mention."
        ],
        # 13: What He Wants
        [
            "More than cakes,",
            "cocoa or milk.",
            "Shirts made of cotton",
            "or ties made of silk.",
            "",
            "Hats, stockings",
            "or a new coat.",
            "What he wants",
            "is simply a note."
        ],
        # 14: Final Message
        [
            "He said I've had enough",
            "eggnogs, cider and soups.",
            "My belt's getting harder",
            "to fit in the loops.",
            "",
            "And one last thing,",
            "please do me a favor.",
            "Always love Christmas,",
            "act like a kid",
            "and pray to your Savior."
        ],
    ]

    # Illustration mapping: (type, filename, stanza_index)
    # type: 'spread' (landscape across two pages), 'full' (single page), 'spot' (small)
    illustrations = [
        ('spread', 'scene-01-the-sneak-LANDSCAPE.png', 0),
        ('full',   'scene-02-at-the-door.png', 1),
        ('full',   'scene-03-the-meeting.png', 2),
        ('spread', 'scene-04b-santas-splendor-LANDSCAPE.png', 3),
        ('full',   'scene-05-the-chat-PORTRAIT.png', 4),
        ('spot',   'scene-06-cocoa-reveal-SQUARE.png', 5),
        # Stanza 6 = text only (Santa's stories), shown alongside spread
        ('full',   'scene-07-camera-dash-PORTRAIT.png', 7),
        ('full',   'scene-08-the-search-PORTRAIT.png', 9),
        ('spread', 'scene-09-the-note-LANDSCAPE.png', 11),
        ('spread', 'scene-10-santas-message-LANDSCAPE.png', 14),
    ]

    # Build spreads: text on left (even page), image on right (odd page)
    ill_idx = 0

    for si, stanza_lines in enumerate(stanzas):
        # Find if this stanza has an illustration
        current_ill = None
        if ill_idx < len(illustrations) and illustrations[ill_idx][2] == si:
            current_ill = illustrations[ill_idx]
            ill_idx += 1

        if current_ill:
            ill_type, ill_file, _ = current_ill
            img_path = os.path.join(MEDIA, ill_file)

            if ill_type == 'spread':
                # Spread: text first, then landscape image across next page
                pdf.text_page(stanza_lines)
                pdf.spread_img(img_path)

            elif ill_type == 'full':
                # Full page: text on left, image on right
                pdf.text_page(stanza_lines)
                pdf.full_page_img(img_path)

            elif ill_type == 'spot':
                # Spot: text page with small image
                pdf.add_page()
                pdf.spot_img(img_path, x=4.7, y=5.5, w=3.3, h=3.3)
                pdf.set_font('Times', '', 15)
                pdf.set_text_color(*DARK_TEXT)
                margin = 1.2
                pdf.set_left_margin(margin)
                pdf.set_right_margin(margin)
                pdf.set_y(1.3)
                for line in stanza_lines:
                    if line.strip() == '':
                        pdf.ln(0.35)
                    else:
                        pdf.multi_cell(PAGE_W - 2 * margin, 0.35, line.strip(), align='L')
                        pdf.ln(0.05)
        else:
            # Text-only page pair (for stanzas without their own illustration)
            pdf.text_page(stanza_lines)
            pdf.blank_page()

    # ── BACK MATTER ──
    pdf.closing_page()

    # Save
    output_path = os.path.join(OUTPUT, "The-Night-I-Met-Santa-INTERIOR.pdf")
    pdf.output(output_path)
    print(f"✅ Interior saved: {output_path}")
    print(f"📄 Total pages: {pdf.pages_count}")

    # Also output page count for spine calculation
    spine_path = os.path.join(OUTPUT, "page_count.txt")
    with open(spine_path, 'w') as f:
        f.write(str(pdf.pages_count))


if __name__ == '__main__':
    build()
