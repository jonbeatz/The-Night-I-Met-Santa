// "The Night I Met Santa" — Cover Design
// Typst 0.15.0 — Wrap-around cover (front + spine + back)
// 8.5 × 8.5" trim, 40 interior pages

#let page-w = 8.5in
#let page-h = 8.5in
#let bleed = 0.125in

// Spine calculation: 40 pages / 2 sheets × 0.004" per sheet (standard paper)
#let interior-pages = 40
#let sheets = interior-pages / 2
#let spine-pb = calc.max(0.08in, sheets * 0.004in)  // paperback
#let spine-hc = spine-pb + 0.125in  // hardcover (board thickness)

// Total cover width = back + spine + front
#let cover-w = page-w + spine-pb + page-w
#let cover-h = page-h

// Bleed dimensions
#let cover-w-bleed = cover-w + 2 * bleed
#let cover-h-bleed = cover-h + 2 * bleed

#set page(
  width: cover-w-bleed,
  height: cover-h-bleed,
  margin: 0pt,
)

// ── COLORS ───────────────────────────────────────────────
#let spine-red = rgb("#8B1515")
#let gold-text = rgb("#D4A843")
#let white = rgb("#FFFFFF")
#let dark-bg = rgb("#14192E")

// ── POSITIONS ────────────────────────────────────────────
#let back-x = bleed
#let spine-x = bleed + page-w
#let front-x = bleed + page-w + spine-pb
#let top-y = bleed

// ── BUILD COVER ──────────────────────────────────────────

// Background: dark navy behind everything
#rect(
  width: cover-w-bleed,
  height: cover-h-bleed,
  fill: dark-bg,
)

// BACK COVER (left) — illustration
#place(
  dx: back-x,
  dy: top-y,
  image("Media/back-cover-empty-chair-PORTRAIT.png", width: page-w, height: page-h, fit: "cover"),
)

// FRONT COVER (right) — illustration
#place(
  dx: front-x,
  dy: top-y,
  image("Media/cover-house-lights-snowman-PORTRAIT.png", width: page-w, height: page-h, fit: "cover"),
)

// SPINE — deep red
#place(
  dx: spine-x,
  dy: top-y,
  rect(width: spine-pb, height: page-h, fill: spine-red),
)

// SPINE TEXT — vertical, gold
// Place individual characters down the spine
#let spine-text = "THE NIGHT I MET SANTA  -  JACK FARRELL"
#let char-size = 8pt
#let char-spacing = 10pt
#let spine-chars = spine-text.len()
#let total-height = spine-chars * char-spacing

#for i in range(spine-chars) {
  let ch = spine-text.at(i)
  let y = top-y + (page-h - total-height) / 2 + i * char-spacing
  place(
    dx: spine-x + spine-pb / 2,
    dy: y,
    text(
      size: char-size,
      fill: gold-text,
      font: "Georgia",
      weight: "bold",
      ch,
    ),
  )
}

// FRONT COVER TEXT — Gold title
#place(
  dx: front-x + page-w / 2,
  dy: top-y + 0.6in,
  text(
    size: 34pt,
    fill: gold-text,
    font: "Georgia",
    weight: "bold",
  )[The Night],
)
#place(
  dx: front-x + page-w / 2,
  dy: top-y + 1.4in,
  text(
    size: 34pt,
    fill: gold-text,
    font: "Georgia",
    weight: "bold",
  )[I Met Santa],
)

// Author credit — bottom right of front cover
#place(
  dx: front-x + page-w - 0.6in,
  dy: top-y + page-h - 1.3in,
  text(
    size: 10pt,
    fill: rgb("#FFFFFFCC"),
    font: "Georgia",
    style: "italic",
    align(right),
  )[Written by],
)
#place(
  dx: front-x + page-w - 0.6in,
  dy: top-y + page-h - 1.0in,
  text(
    size: 12pt,
    fill: gold-text,
    font: "Georgia",
    align(right),
  )[Jack Farrell],
)

// BACK COVER TEXT — Book description
#let desc = (
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
  "\u201cAlways love Christmas,",
  "act like a kid and pray",
  "to your Savior.\u201d",
)

#for (i, line) in desc.enumerate() {
  place(
    dx: back-x + page-w / 2,
    dy: top-y + 1.2in + i * 16pt,
    text(
      size: 10pt,
      fill: white.with(alpha: 85%),
      font: "Georgia",
      style: if line.starts-with("\u201c") or line.starts-with("to") { "italic" } else { "normal" },
    )[#line],
  )
}
