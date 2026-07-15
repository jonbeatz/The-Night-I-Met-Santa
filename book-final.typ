// "The Night I Met Santa" — Final Layout
// Pre-composited pages: illustration + wash + text already merged
// Simple full-bleed image per page — no layering, no transparency issues

#let page-w = 8.75in  // trim 8.5 + 0.125 bleed each side
#let page-h = 8.75in

#set page(width: page-w, height: page-h, margin: 0pt)
#set text(font: ("Georgia", "Times New Roman"), lang: "en")

#let red-title = rgb("#B41E1E")
#let medium-text = rgb("#4A4A4A")
#let light-text = rgb("#888888")
#let gold = rgb("#D4A843")
#let dark-text = rgb("#1A1A1A")

// Full-bleed page from pre-composited PNG
#let poem-page(n) = {
  place(
    dx: 0pt,
    dy: 0pt,
    image("Pages/page-" + n + ".jpg", width: page-w, height: page-h, fit: "cover"),
  )
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
#v(0.8in)
#set text(size: 20pt, weight: "bold", fill: red-title)
[About This Story]
#v(0.5in)
#set text(size: 12pt, fill: medium-text, style: "normal")
#set align(left)
#pad(x: 0.75in)[
  One Christmas Eve, a curious child hears a noise downstairs among the toys. What begins as a tiptoe peek turns into something unforgettable: a quiet hour with Santa himself — stories, laughter, hot cocoa instead of milk, and one small wish for Christmas that isn't gifts at all.

  #v(0.35in)

  Jack Farrell wrote _The Night I Met Santa_ for his family so that wonder would never grow old. This book brings his poem to life — page by page, picture by picture — for children, parents, and grandparents who still believe a little Christmas magic can find you when you least expect it.
]

// ═══════════════════════════════════════════════════════════
// POEM PAGES — pre-composited
// ═══════════════════════════════════════════════════════════

#pagebreak()
#poem-page("01")

#pagebreak()
#poem-page("02")

#pagebreak()
#poem-page("03")

#pagebreak()
#poem-page("04")

#pagebreak()
#poem-page("05")

#pagebreak()
#poem-page("06")

#pagebreak()
#poem-page("07")

#pagebreak()
#poem-page("08")

#pagebreak()
#poem-page("09")

#pagebreak()
#poem-page("10")

#pagebreak()
#poem-page("11")

#pagebreak()
#poem-page("12")

#pagebreak()
#poem-page("13")

#pagebreak()
#poem-page("14")

#pagebreak()
#poem-page("15")

// ── CLOSING / THANK YOU ───────────────────────────────────
#pagebreak()
#set align(center)
#v(1.2in)
#set text(size: 20pt, style: "italic", fill: gold)
[Always love Christmas,]
#v(0.3in)
[act like a kid and pray to your Savior.]
#v(0.5in)
#set text(size: 14pt, style: "italic", fill: medium-text)
[— Santa Claus]
#v(0.6in)
#set text(size: 13pt, fill: medium-text)
[God bless.]

#pagebreak()
#set align(center)
#v(1.0in)
#set text(size: 20pt, weight: "bold", fill: red-title)
[Thank You]
#v(0.5in)
#set text(size: 13pt, fill: medium-text, style: "normal")
#set align(left)
#pad(x: 0.75in)[
  Thank you to my family and loved ones — for keeping this poem, for believing in Christmas, and for sitting still long enough to hear a story about the night I met Santa.

  #v(0.4in)

  May you always find a little wonder downstairs when the house gets quiet.

  #v(0.4in)
  #set align(center)
  God bless.

  #v(0.25in)
  — Jack Farrell
]