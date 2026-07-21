# FONT CATALOG — The Night I Met Santa

**Status:** Options installed on Jon’s PC (2026-07-15) · local files under `Xtraz/Fonts/` (**gitignored**)  
**License:** All families below ship with **OFL** (Open Font License) — free for print/gift books.  
**Source pack folder:** `Xtraz/Fonts/Allura,Cabin,Cinzel_Decorative,Cormorant_Garamond,Dancing_Script,etc/` (~97 `.ttf` files)

> Prefer pointing Pillow/Typst at these **static** TTFs (or system-installed copies) — don’t bake title/author spelling into AI art.

---

## Recommended roles (this book)

| Role | First pick | Strong alt | Avoid for long poem body |
|------|------------|------------|---------------------------|
| **Poem body** | **Cormorant Garamond Medium** | **EB Garamond** Medium | Fredoka, Quicksand, Six Caps, scripts |
| **Spread dialogue / emphasis** | Cormorant Garamond SemiBold / Italic | EB Garamond Italic | Display-only faces |
| **Cover title** | **Cinzel Decorative** Bold/Regular | **Mountains of Christmas** | Tiny decorative scripts |
| **Author credit / “Written By”** | Cinzel Decorative Regular (smaller) | Cabin SemiBold | All-caps Six Caps for long names |
| **Dedication / Thank You flourish** | **Allura** or **Great Vibes** | Pinyon Script · Rochester · Dancing Script | Don’t use for multi-stanza body |
| **Jack note / handwritten prop feel** | Pinyon Script or Rochester | Allura (softer) | Fredoka (too modern-kid) |
| **UI / web flipbook only** | Cabin or Quicksand | — | Not for print poem |

**Legacy default in docs:** Georgia — still fine if needed; prefer **Cormorant Garamond** once compositor is rewritten (closer to heirloom storybook).

### Poem body — LOCKED (Jon 2026-07-20)

| Spec | Value | InDesign |
|------|--------|----------|
| Family / style | **Cormorant Garamond Medium** | `Cormorant Garamond\tMedium` |
| Size | **20** | `pointSize = "20pt"` (rulers in inches) |
| Leading (vertical) | **26** | `leading = "26pt"` |
| Tracking (horizontal) | **+5** | `tracking = 5` |
| Alignment | **Center** | `Justification.CENTER_ALIGN` |
| Color | **#2C2C2C** | PoemCharcoal / Dark Charcoal |

Agents: use these defaults for all new poem text frames until Jon changes them.

### Photoshop MOCK-TYPE (preview mirrors InDesign)

| Role | PSD MOCK | InDesign live |
|------|----------|---------------|
| Poem body | **Same 20/26 +5 #2C2C2C** | Locked table above |
| Dedication / short matter | **30 / ~40 #2C2C2C** (p03 dial) | Match unless Jon changes |
| Title page (P01) | Cinzel **36/42** + Cormorant author **18/24** · `#2C2C2C` · lower-center SAFETY | Same pt + position live — **no Free Transform** in PS |

Points are physical — same pt size in PS and ID when docs are 8.5″/8.75″. Pixel art: **2625²** / **5250×2625** placed full-bleed = 300 DPI; ignore PS “72 dpi” tag. Full parity rules: `.cursor/docs/PAGE-BUILD-WORKFLOW.md` §1b.

### Sample stack (other roles)

```
Cover title:     Cinzel Decorative Bold
Cover credit:    Cinzel Decorative Regular
Poem page body:  Cormorant Garamond Medium @ 20/26 tracking +5, centered (LOCKED)
Thank You line:  Allura or Great Vibes
```

---

## Full inventory (13 families)

| Family | Styles (high level) | Best for | Notes |
|--------|---------------------|----------|-------|
| **Allura** | Regular | Signatures, dedication | Soft script; pair sparingly |
| **Cabin** | Regular→Bold + Condensed / SemiCondensed + italics; variable | Sans for flipbook UI / captions | Readable; not primary poem voice |
| **Cinzel Decorative** | Regular, Bold, Black | Titles, chapter labels, ornate cover | Display — short strings only |
| **Cormorant Garamond** | Light→Bold + italics; variable | **Primary poem body** | Elegant Garamond; great for long lines |
| **Dancing Script** | Regular→Bold; variable | Warm handwritten accents | More casual than Allura |
| **EB Garamond** | Regular→ExtraBold + italics; variable | Alt poem body / copyright | Classic book face; safe printable |
| **Fredoka** | Multiple widths + weights | Playful kid titles (future books) | Too rounded for this heirloom Christmas tone |
| **Great Vibes** | Regular | Elegant flourish / closings | Formal script |
| **Mountains of Christmas** | (pack includes family) | Festive cover / holiday titles | Christmas-specific; use if Cinzel feels too formal |
| **Pinyon Script** | Regular | Note-from-Santa handwritten prop | Fine calligraphy feel |
| **Quicksand** | (pack includes family) | Soft geometric sans (web) | Not for poem body |
| **Rochester** | Regular | Vintage script flourishes | Period Christmas card vibe |
| **Six Caps** | Regular | Tall condensed display single words | Hard for multi-line; avoid body |

Exact file paths live under each family folder (`static/*.ttf` preferred over variable fonts for print predictability).

---

## Paths for tooling

| Use | Path pattern |
|-----|----------------|
| Local pack (gitignored) | `Xtraz/Fonts/.../<Family>/static/<Face>.ttf` |
| System install | Jon already installed these on Windows — use family name in font pickers |
| Typst | `#set text(font: "Cormorant Garamond")` once installed, **or** `#let f = "/path/to/static.ttf"` |
| Pillow `ImageFont.truetype` | Point at **static** TTF absolute path |

---

## Related docs

- Text overlay rules: `TEXT-OVERLAY-POLICY.md`
- Compositor: `composite_pages.py` (rewrite pending)
- Future-book playbook: repo-root `BOOK-PLAYBOOK.md` · living ops: `BOOK-PRODUCTION-SYSTEM.md`
