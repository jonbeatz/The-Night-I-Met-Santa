# Character lock — Jack Farrell (Dad / author portrait)

**Status:** LOCKED 2026-07-15 (Jon)  
**Winner file:** `Media/approved/characters/jack-farrell-portrait.png`  
(also `Images/jack/jack-farrell-portrait-LOCKED.png` · source gen `Media/generated/jack-likeness/v6d-armchair-tree-lights.png`)

**Person:** Jack Farrell — author of *The Night I Met Santa*; Jon’s dad.  
**Use in book:** Prefer **About the Author** or **Thank You** end page (full-bleed or soft-vignette under type). Optional small credit portrait — not a story-poem beat unless Jon asks.

**Gen model for remakes:** `fal-ai/nano-banana-pro/edit` @ 2K + `image_urls` (finals lane — not Klein 4B).

---

## Locked visual (what the winner is)

| Trait | Lock |
|-------|------|
| Face | Kind elderly man; high forehead; wispy bright white/silver hair swept back; warm open smile showing upper teeth; light eyes; soft crow’s feet and smile lines |
| Skin | Clean fair skin with *gentle* age lines only — **no brown age spots / liver spots** on face or hands |
| Body / pose | Seated in armchair, facing viewer, hands gently clasped in lap |
| Clothing | Thick **cream / off-white cable-knit** sweater, dark blue jeans/trousers |
| Setting (this plate) | Patterned terracotta/gold floral armchair; glowing Christmas tree left; mug on side table; warm tan wall; cool snowy window right |
| Style | Painted gouache / soft watercolor children’s Christmas picture-book — heirloom, not photoreal |

---

## Photo refs (likeness donors)

Use these with the LOCKED PNG when regenerating or adapting:

| Path | Role |
|------|------|
| `Media/approved/characters/jack-farrell-portrait.png` | **Primary** approved plate |
| `Images/jack/jack-farrell-portrait-LOCKED.png` | Mirror / backup path |
| `Images/jack/IMG_7537.jpg` | Strong real photo |
| `Images/jack/jackFace4.jpg` · `jackFace5.jpg` · `jackFace6.jpg` | Face crops |
| Likeness favorites that fed the lock | `Media/generated/jack-likeness/v4a-from-v3e-clean.png`, `v4c-from-v3c-clean.png`, `v4f-v3c-blue-sweater.png` |

---

## MASTER CHARACTER BLOCK (copy-paste)

```
Jack Farrell, elderly Caucasian man, author-grandfather portrait, kind warm smile showing upper teeth, high forehead, wispy bright white hair swept back from temples, light eyes with soft crow's feet, gentle smile lines, clean fair skin with soft age lines only NO brown age spots NO liver spots, thick cream cable-knit sweater, seated friendly storybook presence
```

### Full scene remake (match winner vibe)

```
Painted gouache soft watercolor children's Christmas picture-book illustration of Jack Farrell (elderly kind man with wispy bright white swept-back hair, warm open smile, light eyes, clean fair skin without brown age spots) sitting in a patterned terracotta and gold floral armchair, hands gently clasped in his lap, thick cream cable-knit sweater and dark blue jeans, glowing Christmas tree with warm fairy lights and colorful ornaments to his side, steaming mug on a small wooden side table, soft tan wall with a small framed landscape, cool snowy evening window opposite the tree, intimate joyful Christmas Eve living-room mood, heirloom Santore-inspired storybook painting, soft blended brushstrokes, NOT photoreal, NOT CGI, no text, no letters, no watermark
```

### Alternate scene / clothing (keep identity)

```
Same man Jack Farrell: [NEW SCENE + clothing]. Preserve exact facial likeness — high forehead, wispy bright white swept-back hair, warm smile, light eyes, clean fair skin NO brown age spots. Painted gouache soft watercolor Christmas picture-book illustration, NOT photoreal, no text.
```

### Negative / avoid

```
wrong person, generic grandpa, thick dark-silver wig hair, heavy beard, brown age spots, liver spots, mottled freckle patches on hands, photoreal photo, CGI, 3D render, text, watermark, logo, young face, sunglasses
```

---

## fal `/edit` recipe (remake or variant)

```
endpoint: fal-ai/nano-banana-pro/edit
resolution: 2K
aspect_ratio: 1:1
image_urls (order matters — face first):
  1. Images/jack/jack-farrell-portrait-LOCKED.png
  2. Images/jack/IMG_7537.jpg
  3. Images/jack/jackFace5.jpg
  4. (optional) v4f / v4c / v4a from Media/generated/jack-likeness/
prompt: [MASTER CHARACTER + scene] + MASTER STYLE from ILLUSTRATION-STYLE.md
```

---

## Book placement recommendation

| Option | Why |
|--------|-----|
| **About the Author** (recommended) | Portrait *is* the author — Draft A copy already exists |
| **Thank You** | Warm close; leave open zone (lower or side) for thank-you text |
| Closing ornament page | Small vignette only if full-bleed feels too large |

Poem story pages stay child/Santa beats — Jack portrait is **end matter**, not a mid-poem character unless requested.

---

## Related

- Style master: `ILLUSTRATION-STYLE.md`  
- Copy: `BOOK-COPY-DRAFTS.md` (About the Author / Thank You)  
- Gen history: `Media/generated/jack-likeness/INDEX.md`
