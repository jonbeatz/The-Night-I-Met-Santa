# Cover prompts — dial-in kit

**Refs saved:**  
`Images/references/cover/ref-cover-santa-shush.png`  
`Images/references/cover/ref-cover-snow-house.png`

**Required cover type:**
- Title (full): **The Night I Met Santa**
- Credit: **Written by Jack Farrell**
- Style: locked ILLUSTRATION-STYLE — **painted gouache** (not colored pencil); Santore / Golden Age- Prefer **square 1:1** for Lulu 8.5×8.5 front panel (`--ar 1:1` on Midjourney)

**Tip:** AI often misspells titles. Use **Prompt A** (with text) for mood tests; if type is wrong, regenerate with **Prompt B** (art only) and we’ll set clean title/author in `build_cover_v2.py`.

---

## 1) SANTA type (shush / secret) — REVISED 2026-07-14

**Feedback locked:** Flat poster / cover art only — **not** a 3D book mockup.  
Title type like candidate B: festive gold display serif with flourishes (not plain flat sans/simple).  
Refs: `candidate-santa-A-simple-type.png` (type too plain) · `candidate-santa-B-festive-type.png` (type direction OK, still kill mockup).

### Prompt A — flat cover + best title + softer illustration (USE THIS)

**Locked from tests:** Title treatment like `candidate-santa-D-best-title.png` (ornate gold + star sparkles). Dial **art** less photo-real / more painted storybook.

```
Flat square poster illustration for a children's Christmas book cover, full-bleed edge-to-edge painted artwork only, front-facing flat 2D design, NOT a 3D book mockup, no spine, no drop shadow, no product photo

Slightly stylized storybook Santa Claus, chest-up, warm kind expression, finger to lips in a gentle shush, round gold wire glasses, soft painted rosy cheeks, fluffy white beard rendered with soft watercolor and gouache brushstrokes not individual photo hairs, classic red coat and floppy hat with soft white fur and holly berries, cozy night scene with gently painted Christmas trees, warm lantern glow, soft falling snowflakes, magical but clearly illustrated not photographic

KEEP THIS TITLE TREATMENT: ornate festive metallic gold display serif with decorative flourishes, curls, and tiny star sparkles on the lettering, thin gold ornamental line with a small starburst above the title, title reading exactly: The Night I Met Santa
Below title, smaller clean white classic serif reading exactly: Written by Jack Farrell
Text only in the upper sky — do not cover Santa's face

IMPORTANT STYLE: traditional children's picture-book illustration, painted gouache and watercolor look, visible soft brushwork, gentle blended edges, heirloom Golden Age storybook, Charles Santore–inspired but NOT photoreal, NOT hyperrealistic skin pores, NOT CGI, NOT 3D render, soft illustrated holiday magic, print-ready flat cover art
```

### Negatives (Santa) — add / strengthen

```
3D book mockup, hardcover book photo, spine, drop shadow, product photography,
photorealistic, hyperrealistic, skin pores, extreme detail face, DSLR photo, Unreal Engine, Octane render, 3D CGI plastic, too realistic,
plain boring typography, misspelled title, gibberish letters, watermark, anime, cartoon sticker
```

### Prompt B — flat art only (if title spelling breaks)

```
Flat square poster illustration for a children's Christmas book cover, full-bleed edge-to-edge artwork only, front-facing flat 2D design, NOT a 3D book mockup, no spine, no hardcover edges, no drop shadow, no product photo

Close-up chest-up Santa Claus, warm eyes, finger to lips shushing, gold wire glasses, fluffy white beard, red coat and hat with white fur and holly berries, soft bokeh Christmas trees and warm lights behind him, leave open dark sky space at the top for a festive title later, no text, no letters, no watermark

Traditional children's Christmas picture-book illustration, heirloom gouache and watercolor, Charles Santore–inspired Golden Age style, print-ready flat cover art
```

### Negatives (Santa) — critical

```
3D book mockup, hardcover book photo, visible spine, book edges, page stack, drop shadow under book, angled perspective book, product photography, floating book,
plain boring sans-serif title, thin flat undetailed typography, misspelled title, gibberish letters, watermark, cartoon sticker, anime, 3D CGI plastic Santa, photoreal selfie
```

---

## 2) HOUSE type (snowy Victorian / snowman / moon sleigh) — REVISED

**Title lock:** Same treatment as Santa winner `candidate-santa-D-best-title.png` — ornate gold + flourishes + star sparkles + ornamental line/starburst.  
**Layout:** Flat poster only · painted storybook (not photo-real).

### Prompt A — flat house cover + matching festive title (USE THIS)

```
Flat square poster illustration for a children's Christmas book cover, full-bleed edge-to-edge painted artwork only, front-facing flat 2D design, NOT a 3D book mockup, no spine, no hardcover edges, no page block, no drop shadow, no angled book, no product photo, no mockup stand

Magical Christmas Eve night storybook scene, grand two-story Victorian house with wraparound porch and peaked tower, warm golden light glowing softly from every window, green shutters, evergreen wreaths with bright red bows, gentle Christmas lights along the roofline, thick soft snow on roof and yard, friendly painted snowman in the front yard with black top hat and long red scarf, large snow-dusted pine trees framing left and right, deep midnight blue starry sky, large glowing full moon behind the house peak, silhouette of Santa's sleigh and reindeer flying across the moon, cozy heirloom wonder, clearly illustrated not photographic

KEEP THIS TITLE TREATMENT (same as the best Santa cover): ornate festive metallic gold display serif with decorative flourishes, curls, and tiny star sparkles on the lettering, thin gold ornamental line with a small starburst above the title, elegant Christmasy storybook logo lettering, title reading exactly: The Night I Met Santa
Directly beneath the title, smaller clean white classic serif credit reading exactly: Written by Jack Farrell
Place the title in the upper night sky near the moon — do not cover the moon face or the house windows; keep lettering clear and centered

IMPORTANT STYLE: traditional children's picture-book illustration, painted gouache and watercolor look, visible soft brushwork, gentle blended edges, heirloom Golden Age storybook, Charles Santore–inspired but NOT photoreal, NOT hyperrealistic, NOT CGI, NOT 3D render, soft illustrated holiday magic, print-ready flat cover art
```

### Prompt B — flat art only (if title spelling breaks)

```
Flat square poster illustration for a children's Christmas book cover, full-bleed edge-to-edge painted artwork only, front-facing flat 2D design, NOT a 3D book mockup, no spine, no drop shadow, no product photo

Magical Christmas Eve storybook scene, Victorian house with glowing windows and wreaths, snowy yard, friendly snowman with top hat and red scarf, pine trees framing the sides, deep blue starry sky, full moon with Santa sleigh silhouette, leave clear open sky space at the top for a festive gold title later and open snow space at the bottom for author credit, no text, no letters, no watermark

Traditional children's Christmas picture-book illustration, painted gouache and watercolor, Charles Santore–inspired Golden Age style, NOT photoreal, print-ready flat cover art
```

### Negatives (House)

```
3D book mockup, hardcover book photo, visible spine, book edges, page stack, drop shadow under book, angled perspective book, product photography, floating book,
photorealistic, hyperrealistic, DSLR photo, Unreal Engine, 3D CGI, too realistic,
plain boring sans-serif title, thin flat undetailed typography, misspelled title, gibberish letters, watermark,
modern suburban house, anime, cartoon sticker, neon cyberpunk sky, text covering the moon or windows
```

---

## Midjourney quick flags

```
--ar 1:1 --stylize 150 --v 6
--no misspelled text gibberish watermark anime cartoon 3d cgi
```

## After you pick a winner

Drop the PNG into `Media/` (e.g. `cover-santa-shush-FINAL.png` or `cover-house-lights-FINAL.png`) and tell me which one — we’ll lock it for `build_cover_v2.py` and add crisp title type if you used Prompt B.
