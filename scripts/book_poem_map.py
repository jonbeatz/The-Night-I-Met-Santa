#!/usr/bin/env python3
"""Poem / caption map for comparison boards — source: JON-BOOK-FLOW-v2-FINAL.md."""
from __future__ import annotations

from typing import TypedDict


class BeatPoem(TypedDict, total=False):
    unit: str
    layout: str  # seamless | split | text_image | single
    left_page: int
    right_page: int
    page: int
    left: str
    right: str
    right_kind: str  # poem | context | none
    single: str
    title: str


# Poem lines use " / " between verses (board display). Source: Flow v2.
BEATS: dict[str, BeatPoem] = {
    "P01-title": {
        "unit": "P01-title",
        "layout": "single",
        "page": 1,
        "single": "The Night I Met Santa · Written by Jack Farrell",
        "title": "P01 Title",
    },
    "P02-about-spread": {
        "unit": "P02-about-spread",
        "layout": "seamless",
        "left_page": 2,
        "right_page": 3,
        "left": "About This Story",
        "right": "For my family, with love. — Jack Farrell",
        "right_kind": "poem",
        "title": "P02 About + Dedication",
    },
    "S01-approach": {
        "unit": "S01-approach",
        "layout": "split",
        "left_page": 4,
        "right_page": 5,
        "left": (
            "I searched and I peeked when I first heard the noise. / "
            "Something or someone was in with the toys. / "
            "I slithered and crawled for a peek of a glimpse. / "
            "It must be some fairies or holiday imps."
        ),
        "right": (
            "I got up the nerve to go to the door, / "
            "a door that was decorated, bolted and locked."
        ),
        "right_kind": "poem",
        "title": "S1 Approach",
    },
    "S02-threshold": {
        "unit": "S02-threshold",
        "layout": "seamless",
        "left_page": 6,
        "right_page": 7,
        "left": (
            "I didn't know it when I entered the room / "
            "to surprise the amazement or even the shock."
        ),
        "right": (
            "Now I'm usually calm, not very loud, / "
            "or even known to be a ranter. / "
            "But what do you say when you sneak up on Santa?"
        ),
        "right_kind": "poem",
        "title": "S2 Threshold",
    },
    "S03-eyes-met": {
        "unit": "S03-eyes-met",
        "layout": "seamless",
        "left_page": 8,
        "right_page": 9,
        "left": (
            "My jaw dropped when our eyes finally met. / "
            "I knew right then, it was a moment I would never forget."
        ),
        "right": (
            "For there he was in all his splendor, / "
            "brilliant white hair, red coat with suspenders."
        ),
        "right_kind": "poem",
        "title": "S3 Eyes Met",
    },
    "S04-sit-here": {
        "unit": "S04-sit-here",
        "layout": "text_image",
        "left_page": 10,
        "right_page": 11,
        "left": (
            "He was down on the floor between boxes, gifts and ribbons galore. / "
            "I couldn't move, I stayed very still. / "
            'Finally he whispered, "Sit over here. / Have a moment to kill."'
        ),
        "right": (
            "Santa on the floor among gifts and ribbons, gesturing the boy to sit beside him."
        ),
        "right_kind": "context",
        "title": "S4 Sit Here",
    },
    "S05-chat": {
        "unit": "S05-chat",
        "layout": "seamless",
        "left_page": 12,
        "right_page": 13,
        "left": (
            "Oh, what a feeling, such a thrill. / "
            "We chatted and laughed what seemed like an hour."
        ),
        "right": (
            "But with laughs, stories and chatter, / "
            "who cares, it didn't much matter."
        ),
        "right_kind": "poem",
        "title": "S5 Chat",
    },
    "S06-cocoa": {
        "unit": "S06-cocoa",
        "layout": "text_image",
        "left_page": 14,
        "right_page": 15,
        "left": (
            "He spoke of many places, people and things. / "
            "From toys to music to bright diamond rings. / "
            "Coats made of wool, ties made of silk."
        ),
        "right": "He even revealed his passion for hot cocoa instead of cold milk.",
        "right_kind": "poem",
        "title": "S6 Cocoa",
    },
    "S07-proof": {
        "unit": "S07-proof",
        "layout": "seamless",
        "left_page": 16,
        "right_page": 17,
        "left": (
            "When I heard all the noise up in the roof, / "
            "it hit me right then. I needed some proof."
        ),
        "right": (
            "Where can I go? What can I get? / "
            "I know, a photo. That's my best bet."
        ),
        "right_kind": "poem",
        "title": "S7 Proof",
    },
    "S08-gone": {
        "unit": "S08-gone",
        "layout": "seamless",
        "left_page": 18,
        "right_page": 19,
        "left": (
            "I flew out the door and was back in a flash. / "
            "But oh no, the hour had already passed."
        ),
        "right": (
            "And from the noise on top of the roof / "
            "I realized that I was still without proof."
        ),
        "right_kind": "poem",
        "title": "S8 Gone",
    },
    "S09-search": {
        "unit": "S09-search",
        "layout": "split",
        "left_page": 20,
        "right_page": 21,
        "left": (
            "I turned around slowly. I needed to know, / "
            "did he leave me a hint, a tip or a clue? / "
            "Did he forget his hat or maybe a shoe? / "
            "Now what am I supposed to do?"
        ),
        "right": (
            "I know, I'll look up the flue. / "
            "I dashed to the flue but nothing was there. / "
            "I looked over here and I looked over there. / "
            "When I saw something on top of the chair, / "
            "my proof I thought was just laying right there."
        ),
        "right_kind": "poem",
        "title": "S9 Search",
    },
    "S10-note": {
        "unit": "S10-note",
        "layout": "text_image",
        "left_page": 22,
        "right_page": 23,
        "left": (
            "It wasn't a shoe, hat or a coat. / "
            "I couldn't believe it, the old guy. He left me a note. / "
            "I fell on the chair and started to stare. / "
            "What it said, I didn't care."
        ),
        "right": "Boy on his knees at the chair, letter in his hands, wonder on his face.",
        "right_kind": "context",
        "title": "S10 Note",
    },
    "S11-wish": {
        "unit": "S11-wish",
        "layout": "text_image",
        "left_page": 24,
        "right_page": 25,
        "left": (
            "I tore open the note that Santa had wrote. / "
            "The words jumped out as to get my attention. / "
            "And there was one thing he told me to mention. / "
            "More than cakes, cocoa or milk. / "
            "Shirts made of cotton or ties made of silk. / "
            "Hats, stockings or a new coat. / "
            "What he wants is simply a note."
        ),
        "right": "IMAGE ONLY — boy with glowing letter · silent beat lands the final line.",
        "right_kind": "context",
        "title": "S11 Wish",
    },
    "S12-god-bless": {
        "unit": "S12-god-bless",
        "layout": "text_image",
        "left_page": 26,
        "right_page": 27,
        "left": (
            "He said I've had enough eggnogs, cider and soups. / "
            "My belt's getting harder to fit in the loops. / "
            "And one last thing, please do me a favor. / "
            "Always love Christmas, act like a kid and pray to your Savior."
        ),
        "right": "God bless. — under the North Star (text in InDesign).",
        "right_kind": "poem",
        "title": "S12 God Bless",
    },
    # Back matter — poem / copy inventory (Jon correction 2026-07-23):
    # "God bless." lives on S12 R only (under North Star). NOT on p32.
    "P-thank-you": {
        "unit": "P-thank-you",
        "layout": "single",
        "page": 30,
        "single": (
            "Thank You (Draft A) — family note; ends God bless. — Jack Farrell "
            "(BOOK-COPY-DRAFTS.md). InDesign type on cream paper."
        ),
        "title": "P30 Thank You",
    },
    "P-author": {
        "unit": "P-author",
        "layout": "single",
        "page": 31,
        "single": (
            "IMAGE — Jack Farrell portrait (LOCKED). Optional credits under/beside: "
            "Written by Jack Farrell · Design/produced by Jon Farrell © DigitalStudioz 2026"
        ),
        "title": "P31 Author",
    },
    "P-quiet-close": {
        "unit": "P-quiet-close",
        "layout": "split",
        "left_page": 32,
        "right_page": 33,
        "left": "Merry Christmas.",
        "right": "May the magic of this night stay in your heart, long after the season has gone.",
        "right_kind": "poem",
        "title": "P32|33 Quiet Close",
    },
}


def resolve_unit(path_or_name: str) -> str | None:
    s = path_or_name.replace("\\", "/")
    for key in BEATS:
        if key in s or key.lower() in s.lower():
            return key
    # loose aliases
    aliases = {
        "S01": "S01-approach",
        "S02": "S02-threshold",
        "S03": "S03-eyes-met",
        "S04": "S04-sit-here",
        "S05": "S05-chat",
        "S06": "S06-cocoa",
        "S07": "S07-proof",
        "S08": "S08-gone",
        "S09": "S09-search",
        "S10": "S10-note",
        "S11": "S11-wish",
        "S12a": "S12-god-bless",
        "S12b": "S12-god-bless",
        "S12c": "S12-god-bless",
        "S12": "S12-god-bless",
        "S12-closing": "S12-god-bless",
        "P01": "P01-title",
        "P02": "P02-about-spread",
        "P-thank-you": "P-thank-you",
        "P-author": "P-author",
        "P-quiet-close": "P-quiet-close",
        "thank-you": "P-thank-you",
        "quiet-close": "P-quiet-close",
    }
    for a, u in aliases.items():
        if a in s:
            return u
    return None


def captions(unit: str) -> tuple[str, str]:
    """Return (left_caption, right_caption) for board footer labels."""
    b = BEATS[unit]
    layout = b.get("layout")
    if layout == "single":
        return (f'p{b["page"]} — "{b["single"]}"', "")
    lp, rp = b["left_page"], b["right_page"]
    left = f'LEFT p{lp} — "{b["left"]}"'
    if layout == "text_image":
        if b.get("right_kind") == "context":
            right = f'RIGHT p{rp} — IMAGE — "{b["right"]}"'
        else:
            right = f'RIGHT p{rp} — "{b["right"]}"'
    else:
        right = f'RIGHT p{rp} — "{b["right"]}"'
    return left, right


def footer_lines(unit: str) -> list[str]:
    left, right = captions(unit)
    if not right:
        return [left]
    return [left, right]
