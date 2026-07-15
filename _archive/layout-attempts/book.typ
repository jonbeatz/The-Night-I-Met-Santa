// "The Night I Met Santa" — Professional Children's Book
// Built with Typst 0.15.0
// 8.5 × 8.5 inches, 32 pages, print-ready

#let page-w = 8.5in
#let page-h = 8.5in
#let bleed = 0.125in
#let margin-inner = 0.75in
#let margin-outer = 0.65in
#let margin-top = 0.7in
#let margin-bottom = 0.7in

#set page(
  width: page-w,
  height: page-h,
  margin: (top: margin-top, bottom: margin-bottom, inside: margin-inner, outside: margin-outer),
)

// ── FONTS ────────────────────────────────────────────────
#set text(font: "EB Garamond", size: 14pt, lang: "en")
// Fallback if EB Garamond not installed
#show: it => {
  set text(font: ("EB Garamond", "Garamond", "Georgia", "Times New Roman"))
  it
}

// ── COLORS ───────────────────────────────────────────────
#let red-title = rgb("#B41E1E")
#let dark-text = rgb("#1A1A1A")
#let medium-text = rgb("#4A4A4A")
#let light-text = rgb("#888888")
#let gold = rgb("#D4A843")

// ── POEM TEXT ────────────────────────────────────────────
#let poem-stanza(lines, sz: 14pt, clr: dark-text) = {
  set text(size: sz, fill: clr)
  set par(leading: 0.55em, justify: false)
  for line in lines {
    if line == "" {
      v(0.4em)
    } else {
      [#line]
      linebreak()
    }
  }
}

// ── FULL-PAGE ILLUSTRATION (bleeds to edges) ─────────────
#let full-bleed-image(path) = {
  // Temporarily set zero margins for full bleed
  place(top + left, dx: -margin-inner, dy: -margin-top,
    image(path, width: page-w, height: page-h, fit: "cover")
  )
}

// ── HALF-TITLE PAGE ──────────────────────────────────────
#set align(center)
#v(2.2in)
#set text(size: 26pt, weight: "bold", fill: red-title)
[The Night]
#v(0.3in)
[I Met Santa]

// ── BLANK PAGE ───────────────────────────────────────────
#pagebreak()
// Blank

// ── TITLE PAGE ───────────────────────────────────────────
#pagebreak()
#set align(center)
#v(1.6in)
#set text(size: 30pt, weight: "bold", fill: red-title)
[The Night]
#v(0.25in)
[I Met Santa]

#v(0.7in)
#set text(size: 16pt, style: "italic", fill: medium-text)
[Written by Jack Farrell]

#v(0.6in)
#set text(size: 11pt, style: "italic", fill: light-text)
[Illustrations created with AI]
#v(0.1in)
[First Edition, 2026]

// ── COPYRIGHT PAGE ───────────────────────────────────────
#pagebreak()
#set align(left)
#v(5.5in)
#set text(size: 9pt, fill: light-text, style: "normal")
Copyright © Jack Farrell. All rights reserved.

No part of this book may be reproduced or transmitted in any form
or by any means without written permission from the author.

Illustrations created using AI image generation.

Printed in the United States of America.
First Edition, 2026.

// ── DEDICATION ───────────────────────────────────────────
#pagebreak()
#set align(center)
#v(2.5in)
#set text(size: 18pt, style: "italic", fill: medium-text)
[For my family, with love.]
#v(0.4in)
#set text(size: 14pt, fill: dark-text)
[— Jack Farrell]

// ── ABOUT THE AUTHOR ─────────────────────────────────────
#pagebreak()
#set align(center)
#v(0.3in)
#set text(size: 20pt, weight: "bold", fill: red-title)
[About the Author]

#v(0.4in)
#set align(center)
#image("Media/jack-writing-at-desk-PORTRAIT.png", width: 70%, fit: "contain")

#v(0.3in)
#set text(size: 12pt, fill: medium-text, style: "normal")
#set align(center)
Jack Farrell wrote "The Night I Met Santa" for his family,
capturing the wonder of a child who sneaks downstairs on
Christmas Eve and meets Santa Claus face to face.
A father and grandfather, Jack's poem has been treasured
by his family for decades. This book brings his words to
life so that children everywhere can share in the magic.

// ── POEM BEGINS ──────────────────────────────────────────
// Pattern: text on LEFT (even) page, illustration on RIGHT (odd) page
// Some spreads use landscape images that span the full spread

// SPREAD 1: Stanza 0+1 — The Sneak + At the Door
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "I searched and I peeked",
  "when I first heard the noise.",
  "Something or someone",
  "was in with the toys.",
  "",
  "I slithered and crawled",
  "for a peek of a glimpse.",
  "It must be some fairies",
  "or holiday imps.",
))

#pagebreak()
#full-bleed-image("Media/scene-01-the-sneak-LANDSCAPE.png")

// SPREAD 2: Stanza 1-2 — At the Door + Sneak Up
#pagebreak()
#set align(left)
#v(1.6in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "I got up the nerve",
  "to go to the door,",
  "a door that was decorated,",
  "bolted and locked.",
  "",
  "I didn't know it",
  "when I entered the room",
  "to surprise the amazement",
  "or even the shock.",
))

#pagebreak()
#full-bleed-image("Media/scene-02-at-the-door.png")

// SPREAD 3: Stanza 2 — Sneak Up on Santa
#pagebreak()
#set align(left)
#v(2.0in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "Now I'm usually calm,",
  "not very loud,",
  "or even known to be a ranter.",
  "",
  "But what do you say",
  "when you sneak up on Santa?",
))

#pagebreak()
#full-bleed-image("Media/scene-02b-sneak-up-santa-LANDSCAPE.png")

// SPREAD 4: Stanza 3 — The Meeting (Jaw Drop)
#pagebreak()
#set align(left)
#v(1.6in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "My jaw dropped",
  "when our eyes finally met.",
  "I knew right then,",
  "it was a moment",
  "I would never forget.",
  "",
  "For there he was",
  "in all his splendor,",
  "brilliant white hair,",
  "red coat with suspenders.",
))

#pagebreak()
#full-bleed-image("Media/scene-04b-santas-splendor-LANDSCAPE.png")

// SPREAD 5: Stanza 4 — Santa on Floor
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "He was down on the floor",
  "between boxes, gifts",
  "and ribbons galore.",
  "",
  "I couldn't move,",
  "I stayed very still.",
  "Finally he whispered,",
  "\"Sit over here.",
  "Have a moment to kill.\"",
))

#pagebreak()
#full-bleed-image("Media/scene-05-the-chat-PORTRAIT.png")

// SPREAD 6: Stanza 5 — The Chat
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "Oh, what a feeling,",
  "such a thrill.",
  "We chatted and laughed",
  "what seemed like an hour.",
  "",
  "But with laughs, stories",
  "and chatter, who cares,",
  "it didn't much matter.",
))

#pagebreak()
#full-bleed-image("Media/scene-06-cocoa-reveal-SQUARE.png")

// SPREAD 7: Stanza 6 — Santa's Stories
#pagebreak()
#set align(left)
#v(1.6in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "He spoke of many places,",
  "people and things.",
  "From toys to music",
  "to bright diamond rings.",
  "",
  "Coats made of wool,",
  "ties made of silk.",
  "He even revealed his passion",
  "for hot cocoa",
  "instead of cold milk.",
))

#pagebreak()
#full-bleed-image("Media/scene-06b-santas-stories-LANDSCAPE.png")

// SPREAD 8: Stanza 7 — Camera Idea
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "When I heard all the noise",
  "up in the roof,",
  "it hit me right then.",
  "I needed some proof.",
  "",
  "Where can I go?",
  "What can I get?",
  "I know, a photo.",
  "That's my best bet.",
))

#pagebreak()
#full-bleed-image("Media/scene-07-camera-dash-PORTRAIT.png")

// SPREAD 9: Stanza 8 — The Dash (Santa Gone)
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "I flew out the door",
  "and was back in a flash.",
  "But oh no, the hour",
  "had already passed.",
  "",
  "And from the noise",
  "on top of the roof",
  "I realized that I was",
  "still without proof.",
))

#pagebreak()
#full-bleed-image("Media/scene-08b-the-dash-santa-gone-PORTRAIT.png")

// SPREAD 10: Stanza 9 — The Search
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "I turned around slowly.",
  "I needed to know,",
  "did he leave me a hint,",
  "a tip or a clue?",
  "",
  "Did he forget his hat",
  "or maybe a shoe?",
  "Now what am I",
  "supposed to do?",
))

#pagebreak()
#full-bleed-image("Media/scene-08-the-search-PORTRAIT.png")

// SPREAD 11: Stanza 10 — The Flue & Chair
#pagebreak()
#set align(left)
#v(1.6in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
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
  "was just laying right there.",
))

#pagebreak()
#full-bleed-image("Media/scene-10b-the-flue-and-chair-PORTRAIT.png")

// SPREAD 12: Stanza 11 — The Note
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "It wasn't a shoe,",
  "hat or a coat.",
  "I couldn't believe it,",
  "the old guy.",
  "He left me a note.",
  "",
  "I fell on the chair",
  "and started to stare.",
  "What it said,",
  "I didn't care.",
))

#pagebreak()
#full-bleed-image("Media/scene-09-the-note-LANDSCAPE.png")

// SPREAD 13: Stanza 12 — Tearing Open
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "I tore open the note",
  "that Santa had wrote.",
  "The words jumped out",
  "as to get my attention.",
  "",
  "And there was one thing",
  "he told me to mention.",
))

#pagebreak()
#full-bleed-image("Media/scene-12b-tearing-open-PORTRAIT.png")

// SPREAD 14: Stanza 13 — What He Wants
#pagebreak()
#set align(left)
#v(1.8in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "More than cakes,",
  "cocoa or milk.",
  "Shirts made of cotton",
  "or ties made of silk.",
  "",
  "Hats, stockings",
  "or a new coat.",
  "What he wants",
  "is simply a note.",
))

#pagebreak()
#full-bleed-image("Media/scene-14b-what-he-wants-message-LANDSCAPE.png")

// SPREAD 15: Stanza 14 — Final Message
#pagebreak()
#set align(left)
#v(1.4in)
#set text(size: 15pt, fill: dark-text, style: "normal")
#poem-stanza((
  "He said I've had enough",
  "eggnogs, cider and soups.",
  "My belt's getting harder",
  "to fit in the loops.",
  "",
  "And one last thing,",
  "please do me a favor.",
  "Always love Christmas,",
  "act like a kid",
  "and pray to your Savior.",
))

#pagebreak()
#full-bleed-image("Media/scene-10-santas-message-LANDSCAPE.png")

// ── CLOSING ──────────────────────────────────────────────
#pagebreak()
#set align(center)
#v(2.0in)
#set text(size: 18pt, style: "italic", fill: gold)
["Always love Christmas,]
[act like a kid and pray to your Savior."]

#v(0.5in)
#set text(size: 14pt, style: "italic", fill: medium-text)
[— Santa Claus]

#v(0.8in)
#set text(size: 12pt, style: "italic", fill: light-text)
[For my family, with love.]
[— Jack Farrell]

#v(0.3in)
#set text(size: 11pt, fill: light-text)
[God bless.]

// ── FINAL BLANK ──────────────────────────────────────────
#pagebreak()
