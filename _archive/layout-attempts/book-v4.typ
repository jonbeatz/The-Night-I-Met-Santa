// "The Night I Met Santa" — Integrated Spread Layout v4
// Text on watercolor washes — organic, feathered, no hard edges
// Each position uses a unique watercolor texture

#let page-w = 8.5in
#let page-h = 8.5in

#set page(width: page-w, height: page-h, margin: 0pt)
#set text(font: ("Georgia", "Times New Roman"), lang: "en")

#let red-title = rgb("#B41E1E")
#let dark-text = rgb("#1A1A1A")
#let medium-text = rgb("#4A4A4A")
#let light-text = rgb("#888888")
#let gold = rgb("#D4A843")

// ── WATERCOLOR WASH MAP ──────────────────────────────────
#let wash-map = (
  "bottom-left":  "Media/wc-trans-bl.png",
  "bottom-right": "Media/wc-trans-br.png",
  "top-left":     "Media/wc-trans-tl.png",
  "top-right":    "Media/wc-trans-tr.png",
  "center-bottom": "Media/wc-trans-bc.png",
)

// ── TEXT ON WATERCOLOR ───────────────────────────────────
// The watercolor wash stretches full-page, bleeding off all edges
// Text sits within the colored area, positioned to match the wash origin
#let text-on-wash(lines, position: "bottom-left") = {
  let wash-file = wash-map.at(position)

  // Full-bleed watercolor layer
  place(
    dx: 0pt,
    dy: 0pt,
    image(wash-file, width: page-w, height: page-h, fit: "cover"),
  )

  // Text position relative to the wash origin
  let (tx, ty) = if position == "bottom-left" {
    (0.7in, page-h - 2.8in)
  } else if position == "bottom-right" {
    (page-w - 4.5in, page-h - 2.8in)
  } else if position == "top-left" {
    (0.7in, 0.6in)
  } else if position == "top-right" {
    (page-w - 4.5in, 0.6in)
  } else if position == "center-bottom" {
    (1.5in, page-h - 2.5in)
  } else {
    (0.7in, page-h - 2.8in)
  }

  place(
    dx: tx,
    dy: ty,
    {
      set text(size: 13.5pt, fill: dark-text)
      set par(leading: 0.55em, justify: false)
      for line in lines {
        if line == "" {
          v(0.35em)
        } else {
          [#line]
          linebreak()
        }
      }
    }
  )
}

// ── ILLUSTRATION SPREAD ──────────────────────────────────
#let illustration-spread(image-path, stanza-lines, panel-pos: "bottom-left") = {
  // Full-bleed illustration
  place(
    dx: 0pt,
    dy: 0pt,
    image(image-path, width: page-w, height: page-h, fit: "cover"),
  )
  // Text on watercolor overlay
  text-on-wash(stanza-lines, position: panel-pos)
}

// ═══════════════════════════════════════════════════════════
// FRONT MATTER
// ═══════════════════════════════════════════════════════════

#set align(center)
#v(2.2in)
#set text(size: 26pt, weight: "bold", fill: red-title)
[The Night]
#v(0.3in)
[I Met Santa]

#pagebreak()

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

#pagebreak()
#set align(left)
#v(5.5in)
#set text(size: 9pt, fill: light-text, style: "normal")
Copyright © Jack Farrell. All rights reserved.
No part of this book may be reproduced or transmitted in any form
or by any means without written permission from the author.
Illustrations created using AI image generation.
Printed in the United States of America. First Edition, 2026.

#pagebreak()
#set align(center)
#v(2.5in)
#set text(size: 18pt, style: "italic", fill: medium-text)
[For my family, with love.]
#v(0.4in)
#set text(size: 14pt, fill: dark-text)
[— Jack Farrell]

#pagebreak()
#set align(center)
#v(0.3in)
#set text(size: 20pt, weight: "bold", fill: red-title)
[About the Author]
#v(0.4in)
#image("Media/jack-writing-at-desk-PORTRAIT.png", width: 60%, fit: "contain")
#v(0.3in)
#set text(size: 12pt, fill: medium-text, style: "normal")
Jack Farrell wrote "The Night I Met Santa" for his family,
capturing the wonder of a child who sneaks downstairs on
Christmas Eve and meets Santa Claus face to face.
A father and grandfather, Jack's poem has been treasured
by his family for decades. This book brings his words to
life so that children everywhere can share in the magic.

// ═══════════════════════════════════════════════════════════
// POEM SPREADS
// ═══════════════════════════════════════════════════════════

#pagebreak()
#illustration-spread("Media/scene-01-the-sneak-LANDSCAPE.png", (
  "I searched and I peeked",
  "when I first heard the noise.",
  "Something or someone",
  "was in with the toys.",
  "",
  "I slithered and crawled",
  "for a peek of a glimpse.",
  "It must be some fairies",
  "or holiday imps.",
), panel-pos: "bottom-left")

#pagebreak()
#illustration-spread("Media/scene-02-at-the-door.png", (
  "I got up the nerve",
  "to go to the door,",
  "a door that was decorated,",
  "bolted and locked.",
  "",
  "I didn't know it",
  "when I entered the room",
  "to surprise the amazement",
  "or even the shock.",
), panel-pos: "top-right")

#pagebreak()
#illustration-spread("Media/scene-02b-sneak-up-santa-LANDSCAPE.png", (
  "Now I'm usually calm,",
  "not very loud,",
  "or even known to be a ranter.",
  "",
  "But what do you say",
  "when you sneak up on Santa?",
), panel-pos: "bottom-left")

#pagebreak()
#illustration-spread("Media/scene-04b-santas-splendor-LANDSCAPE.png", (
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
), panel-pos: "bottom-left")

#pagebreak()
#illustration-spread("Media/scene-05-the-chat-PORTRAIT.png", (
  "He was down on the floor",
  "between boxes, gifts",
  "and ribbons galore.",
  "",
  "I couldn't move,",
  "I stayed very still.",
  "Finally he whispered,",
  "\u201cSit over here.",
  "Have a moment to kill.\u201d",
), panel-pos: "bottom-right")

#pagebreak()
#illustration-spread("Media/scene-06-cocoa-reveal-SQUARE.png", (
  "Oh, what a feeling,",
  "such a thrill.",
  "We chatted and laughed",
  "what seemed like an hour.",
  "",
  "But with laughs, stories",
  "and chatter, who cares,",
  "it didn't much matter.",
), panel-pos: "top-left")

#pagebreak()
#illustration-spread("Media/scene-06b-santas-stories-LANDSCAPE.png", (
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
), panel-pos: "bottom-left")

#pagebreak()
#illustration-spread("Media/scene-07-camera-dash-PORTRAIT.png", (
  "When I heard all the noise",
  "up in the roof,",
  "it hit me right then.",
  "I needed some proof.",
  "",
  "Where can I go?",
  "What can I get?",
  "I know, a photo.",
  "That's my best bet.",
), panel-pos: "center-bottom")

#pagebreak()
#illustration-spread("Media/scene-08b-the-dash-santa-gone-PORTRAIT.png", (
  "I flew out the door",
  "and was back in a flash.",
  "But oh no, the hour",
  "had already passed.",
  "",
  "And from the noise",
  "on top of the roof",
  "I realized that I was",
  "still without proof.",
), panel-pos: "top-right")

#pagebreak()
#illustration-spread("Media/scene-08-the-search-PORTRAIT.png", (
  "I turned around slowly.",
  "I needed to know,",
  "did he leave me a hint,",
  "a tip or a clue?",
  "",
  "Did he forget his hat",
  "or maybe a shoe?",
  "Now what am I",
  "supposed to do?",
), panel-pos: "bottom-left")

#pagebreak()
#illustration-spread("Media/scene-10b-the-flue-and-chair-PORTRAIT.png", (
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
), panel-pos: "bottom-right")

#pagebreak()
#illustration-spread("Media/scene-09-the-note-LANDSCAPE.png", (
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
), panel-pos: "bottom-left")

#pagebreak()
#illustration-spread("Media/scene-12b-tearing-open-PORTRAIT.png", (
  "I tore open the note",
  "that Santa had wrote.",
  "The words jumped out",
  "as to get my attention.",
  "",
  "And there was one thing",
  "he told me to mention.",
), panel-pos: "bottom-right")

#pagebreak()
#illustration-spread("Media/scene-14b-what-he-wants-message-LANDSCAPE.png", (
  "More than cakes,",
  "cocoa or milk.",
  "Shirts made of cotton",
  "or ties made of silk.",
  "",
  "Hats, stockings",
  "or a new coat.",
  "What he wants",
  "is simply a note.",
), panel-pos: "top-left")

#pagebreak()
#illustration-spread("Media/scene-10-santas-message-LANDSCAPE.png", (
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
), panel-pos: "center-bottom")

// ── CLOSING ──────────────────────────────────────────────
#pagebreak()
#set align(center)
#v(1.5in)
#set text(size: 20pt, style: "italic", fill: gold)
[Always love Christmas,]
#v(0.3in)
[act like a kid and pray to your Savior.]
#v(0.6in)
#set text(size: 14pt, style: "italic", fill: medium-text)
[— Santa Claus]
#v(1.0in)
#set text(size: 13pt, style: "italic", fill: light-text)
[For my family, with love.]
[— Jack Farrell]
#v(0.2in)
[God bless.]
