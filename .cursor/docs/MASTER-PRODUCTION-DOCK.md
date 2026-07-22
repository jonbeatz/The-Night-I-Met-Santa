# MASTER PRODUCTION DOCK — The Night I Met Santa
**Created:** July 21, 2026 · **Status:** AUTHORITATIVE for **prompts and generation**
**Page map SoT:** `BOOK-PAGE-WORKFLOW.md` (page numbers, filenames, poem placement) — this dock does **not** replace it  
**Supersedes (prompts only):** `POEM-IMAGE-PROMPT-DOCK.md` · `PAGE-PROMPT-BIBLE.md` → stubs redirect here

> **Single source of truth for image generation prompts.** Every spread has ready-to-paste prompts, backup alternatives, variety rules, and quiet zone maps. Copy a block, add the style tags, generate. For which page gets which poem lines / temp filenames, always follow **BOOK-PAGE-WORKFLOW.md**.

---

## Quick Reference

| What | Where |
|------|-------|
| **Poem text** | `Transcription/poem-clean.txt` |
| **Page map** | `BOOK-PAGE-WORKFLOW.md` (page numbers, filenames) — **locked map SoT** |
| **Build loop** | `PAGE-BUILD-WORKFLOW.md` (PS → InDesign) |
| **Style master** | `ILLUSTRATION-STYLE.md` |
| **Image lanes** | `IMAGE-LANE-PROMPTS.md` (Klein D2 vs finals) |
| **Print specs** | `AGENT-RUNBOOK.md` §4 (Lulu 8.5×8.5", sRGB, 0.125" bleed) |
| **Approved art** | `Media/approved/INDEX.md` |
| **Page count** | **35–40** locked · working target **36** (per BOOK-PAGE-WORKFLOW) |

---

## ⚡ Generation Cheat Sheet

```powershell
# Lane A1 — Dial (spread) — PRIMARY
npm run image:fal:klein9 -- "<SCENE>. <Dial D2>. seamless continuous two-page spread, NO fake book gutter, NO center spine shadow."

# Lane A1 — Dial (single page)
npm run image:fal:page -- "<SCENE>. <master style>. FRAME ON"

# Lane B — Finals (after Jon approves composition)
npm run image:fal:gemini-edit -- "<SCENE>. <master style>. <spread add-on if spread>. NO fake gutter." --image_url "<ref>"
```

---

## 🎨 Style Tags (append to every prompt)

### Master Style (Lane B Finals)
```
Traditional children's Christmas picture-book illustration, heirloom storybook quality, heavily painted in rich gouache and soft watercolor with visible soft brushstrokes and gentle blended edges, NOT colored pencil NOT crayon NOT scratchy sketch lines, warm fireplace glow mixed with cool moonlight, golden ember highlights, deep crimson and forest green palette with warm cream and muted earth tones, nostalgic Golden Age painted realism, intimate cozy magical atmosphere, Charles Santore–inspired storybook painting, classic Clement C. Moore Christmas book feel, highly detailed but soft and painterly, print-ready composition, no text, no letters, no watermark
```

### Klein Dial D2 (Lane A1/A3)
```
KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated.
```

### Spread Add-On (every SPREAD)
```
seamless continuous two-page storybook spread across the full width, one unbroken painted scene through the center, NO fake book gutter, NO vertical fold line, NO center spine shadow, NO page-split seam, NO mockup binding crease down the middle
```

---

## 🔒 Continuity Locks (Applies to Every Plate)

| Lock | Rule |
|------|------|
| **Boy** | Match `Media/approved/characters/boy-narrator-G0.png` · oatmeal/taupe holly pajamas **ONLY** — **NOT** a red coat, **NOT** a Santa suit, **NOT** a Santa costume |
| **Santa** | Match `Media/approved/characters/santa-G0.png` · white hair/beard · red coat with suspenders |
| **Room** | Same cozy Christmas Eve living room (tree, hearth, gifts) unless beat requires hall/door/roof |
| **Text in art** | NEVER bake poem words into the illustration. No readable words, logos, handwriting on clothes/notes |
| **Gutter** | Seamless — no fold line/shadow on spread finals (orange guide = PSD only) |
| **Quiet zones** | Each spread specifies where text will go — keep those areas soft/clear |
| **Hard append (all story gens)** | `Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume.` |
| **Hard append (S11 Wish)** | Also: `NO readable letters, NO text, NO handwriting anywhere in the image.` |

---

## Page Layout (35–40 locked · working target 36)

| Pages | Form | Unit | Poem Cue | Art Status |
|---|---|---|---|---|
| 1 | SINGLE | P01 Title | — | 🔒 v22 locked provisional |
| 2 | SINGLE | P02 Copyright | — | Optional ornament |
| 3 | SINGLE | P03 Dedication | — | Soft vignette |
| 4|5 | MATTER | About | — | Need vignette R |
| **6|7** | **SPREAD** | **S1 Approach** | Noise / peek / door | 🎯 Need |
| **8|9** | **SPREAD** | **S2 Threshold** | Enter / sneak on Santa | 🎯 Need |
| **10|11** | **SPREAD** | **S3 Eyes Met** | Eyes locked / splendor | 🔒 HAS ART |
| **12|13** | **SPREAD** | **S4 Sit Here** | Gifts on floor / sit here | 🎯 Need |
| **14|15** | **SPREAD** | **S5 Chat** | Chat & laugh | Need |
| **16|17** | **SPREAD** | **S6 Cocoa** | Stories / cocoa not milk | Need |
| **18|19** | **SPREAD** | **S7 Proof** | Roof noise / photo idea | Need |
| **20|21** | **SPREAD** | **S8 Gone** | Dash back / Santa gone | Need |
| **22|23** | **SPREAD** | **S9 Search** | Flue / chair / something there | Need |
| **24|25** | **SPREAD** | **S10 Note** | Note found / torn open | 🎯 Need |
| **26|27** | **SPREAD** | **S11 Wish** | What he wants is a note | Need |
| **28|29** | **SPREAD** | **S12 Blessing** | God bless / closing | 🎯 Need |
| 30|31 | MATTER | Thanks + Jack | — | 🔒 Portrait locked |
| 32-36 | SINGLES | Quiet close | Optional padding | Need |

🎯 = priority spreads · 🔒 = don't regenerate

---

## 🎬 Variety Charter — Anti-Standing-Portrait

**Rotate camera and subject so the book feels cinematic, not a cast lineup.**

| Mode | Use On |
|------|--------|
| **Crawl / low POV** | S1, S4 |
| **Over-shoulder** | S2 |
| **Prop hero** (mug, note, camera, gifts) | S4, S6, S7, S10, S11 |
| **Empty / afterimage** (Santa gone) | S8, S12 option |
| **Intimate close** (hands, eyes, letter) | S3 (locked), S10, S11 |
| **Search / motion** (crouch, dash, look-up) | S1, S7, S8, S9 |
| **Seated warmth** (floor, not standing) | S4, S5, S6 |
| **Environment / doorway / light spill** | S1, S2, S8 |

**NEVER as default:** Both figures standing face-forward mid-room with empty hands.

---

# 🖼️ FRONT MATTER PROMPTS

---

## P01 — Title · p1 · SINGLE · 🔒 LOCKED

**File:** `Media/approved/pages/p01-title.png` (v22)
Do not regenerate unless Jon unlocks. Cream TOP for Cinzel/Cormorant type.

---

## P02 — Copyright · p2 · SINGLE

**Prompt:**
```
Soft abstract Christmas ornament vignette on warm cream watercolor paper, tiny holly sprig and faint pine shadow only, large open quiet center for later text, no people, no Santa, no readable words, painted gouache storybook, FRAME ON
```
+ master style

---

## P03 — Dedication · p3 · SINGLE

**Prompt:**
```
Quiet Christmas Eve vignette: empty wooden chair near a softly glowing fireplace, distant tree lights bokeh, large soft quiet center for dedication text, no people, intimate hush, watercolor paper vignette, FRAME ON
```
+ master style

**Backup:**
```
Cozy hearth with two stockings hanging from mantel, soft warm light, open cream space above for dedication text, no people, gentle gouache, FRAME ON
```

---

## P05 — About Vignette · p5 · SINGLE (p4 = type)

**Prompt:**
```
Snowy nighttime window from inside a cozy living room, frost lace on glass, Christmas tree reflected faintly, empty gift room hush, quiet open wall for breathing room, no people, soft gouache, FRAME ON
```
+ master style

**Backup:**
```
Soft watercolor paper texture with tiny scattered holly and pine sprigs, warm cream, large open center, no people, no text in art, gentle heirloom feel, FRAME ON
```

---

# 📖 STORY SPREADS — POEM + PROMPTS + BACKUPS

---

## S1 — Approach · p6|7 · SPREAD · 🎯 PRIORITY

| | LEFT (p6) | RIGHT (p7) |
|---|---|---|
| **Poem** | I searched and I peeked when I first heard the noise. / Something or someone was in with the toys. / I slithered and crawled for a peek of a glimpse. / It must be some fairies or holiday imps. | I got up the nerve to go to the door, / a door that was decorated, bolted and locked. |
| **Camera** | Low crawl POV · child small in dark hall · toys glow through crack | Continuous → decorated door wreath/bolt hero · warm light under door |
| **Quiet zones** | Lower-left cream/wall | Lower-right / outer door wall |

### Primary Prompt
```
Wide cinematic Christmas Eve storybook spread: LEFT — dim hallway, curious child in oatmeal holly pajamas crawling low toward a glowing living-room doorway, silhouette and wonder, faint toys and wrapping paper shapes beyond the light, magical hush; RIGHT — continuous same space ending on a decorated wooden door with wreath, red bow, old bolt and lock, warm golden light spilling under and around the door into the darker hall, no Santa face yet. Leave soft quiet lower corners for later text.
```
+ Dial D2 + spread add-on

### Backup Prompt (simpler composition)
```
Christmas Eve hallway spread: curious child in pajamas peeking around a corner toward warm light spilling from a living room doorway, toys visible through the crack, decorated door with wreath in the distance, magical anticipation. Simple strong composition — child on left, glowing door on right.
```
+ Dial D2 + spread add-on

**Temp:** `art-S01-approach-SPREAD-5250x2625.png`

---

## S2 — Threshold · p8|9 · SPREAD · 🎯 PRIORITY

| | LEFT (p8) | RIGHT (p9) |
|---|---|---|
| **Poem** | I didn't know it when I entered the room / to surprise the amazement or even the shock. | Now I'm usually calm, not very loud, / or even known to be a ranter. / But what do you say when you sneak up on Santa? |
| **Camera** | Over-shoulder of child entering · gift landscape opens | Half-seen Santa — red coat, boots, suspenders hint among boxes — face not full hero yet |
| **Quiet zones** | Upper wall / outer left | Lower outer right |

### Primary Prompt
```
Wide cinematic Christmas living-room spread from the doorway: child peeking in from the threshold (back and shoulder toward viewer), living room opens into a sea of gifts ribbons and tree glow; farther in, Santa Claus only half-seen — red coat, boots, brilliant white beard edge among boxes — not a full face-to-face portrait yet, comedy of almost getting caught, hush and wonder. Leave quiet outer bands for later text.
```
+ Dial D2 + spread add-on

### Backup Prompt (Santa in shadows · holly PJs hard lock)
```
Christmas living room spread: child at doorway edge looking into a room filled with gifts, warm tree glow; Santa is partially visible in the background shadows among stacked presents — just his red coat and white beard visible, face turned away. Mystery and wonder — not a reveal yet. Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume.
```
+ Dial D2 + spread add-on + hard append

**Temp:** `art-S02-threshold-SPREAD-5250x2625.png`

---

## S3 — Eyes Met · p10|11 · SPREAD · 🔒 HAS ART

| | LEFT (p10) | RIGHT (p11) |
|---|---|---|
| **Poem** | My jaw dropped when our eyes finally met. / I knew right then, it was a moment I would never forget. | For there he was in all his splendor, / brilliant white hair, red coat with suspenders. |
| **Art** | LOCKED `Media/approved/spreads/spread-eyes-met.png` | — |
| **Notes** | Do not regenerate. Promote naming → `art-S03-eyes-met-SPREAD-5250x2625.png` | |

**Prompt (only if Jon unlocks remake):**
```
Wide cinematic two-page Christmas storybook spread, child and Santa Claus meeting eyes for the first time, intimate magical moment, Santa in all his splendor brilliant white hair and beard, red coat with suspenders clearly visible, gifts ribbons and boxes around them on the living room floor, warm hearth light and soft tree glow, wonder on the child's face. Leave soft quiet outer corners for later text.
```
+ master + spread add-on

---

## S4 — Sit Here · p12|13 · SPREAD · 🎯 PRIORITY

| | LEFT (p12) | RIGHT (p13) |
|---|---|---|
| **Poem** | He was down on the floor between boxes, gifts and ribbons galore. / I couldn't move, I stayed very still. | Finally he whispered, "Sit over here. / Have a moment to kill." |
| **Camera** | Low angle gift sea · Santa seated on floor · child frozen mid-step | Beckoning hand · open sit-spot · dialogue quiet zone |
| **Quiet zones** | Outer left wall | Side panel for whisper lines |

### Primary Prompt
```
Wide cinematic Christmas gift-room spread, low camera among wrapping paper: Santa Claus sitting on the floor between boxes gifts and ribbons galore, kind face, red coat with suspenders visible; nearby a child in oatmeal holly pajamas frozen mid-step in awe; RIGHT continues as Santa gently gesturing to an open spot beside him inviting the child to sit, cozy tree and fireplace glow. Leave quiet side areas for later dialogue text. Not a stiff standing portrait.
```
+ Dial D2 + spread add-on

### Backup Prompt (focus on Santa invitation)
```
Cozy Christmas floor spread: Santa seated comfortably among a sea of wrapped gifts and ribbons, warm smile, gesturing to an empty spot beside him inviting the child to join; foreground shows the child's pajama-clad legs and feet frozen hesitantly — point of view from the child's perspective. Intimate floor-level composition.
```
+ Dial D2 + spread add-on

**Temp:** `art-S04-sit-here-SPREAD-5250x2625.png`  
**Refs:** style-refs / prior “sit here” dials if any

---

## S5 — Chat · p14|15 · SPREAD

| | LEFT (p14) | RIGHT (p15) |
|---|---|---|
| **Poem** | Oh, what a feeling, such a thrill. / We chatted and laughed what seemed like an hour. | But with laughs, stories and chatter, / who cares, it didn't much matter. |
| **Camera** | Both seated on floor · animated hands · soft laugh | Continuous warmth · gift clutter as frame |
| **Quiet zones** | Bottom band | Bottom / outer right |

### Primary Prompt
```
Wide cozy Christmas spread: Santa and child sitting together on the living room floor among gifts, laughing warmly with animated friendly gestures, storytelling hands, tree lights and soft fireplace glow, intimate heirloom mood, figures seated not standing. Leave quiet bottom band for later text. Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume.
```
+ Dial D2 + spread add-on + hard append

### Backup Prompt (one Santa only · no twin)
```
Wide cozy Christmas spread: ONE Santa Claus and ONE child sitting together on the living room floor among gifts, laughing warmly with animated friendly gestures, storytelling hands, tree lights and soft fireplace glow, intimate heirloom mood, figures seated not standing — NOT mirrored, NOT two Santas, NOT phones or modern devices. Leave quiet bottom band for later text. Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume.
```
+ Dial D2 + spread add-on + hard append

**Temp:** `art-S05-chat-SPREAD-5250x2625.png`  
**Refs:** `style-refs/spread/spread-chat-laugh-WIDE.png`

---

## S6 — Cocoa · p16|17 · SPREAD

| | LEFT (p16) | RIGHT (p17) |
|---|---|---|
| **Poem** | He spoke of many places, people and things. / From toys to music to bright diamond rings. | Coats made of wool, ties made of silk. / He even revealed his passion for hot cocoa instead of cold milk. |
| **Camera** | Prop hero: steaming cocoa mug + soft story echoes — Santa mid-tale | Child listening · firelight on steam |
| **Quiet zones** | Upper left wall | Outer right |

### Primary Prompt
```
Wide cinematic Christmas storytelling spread: hero prop is a steaming mug of hot cocoa in Santa's hands, soft steam catching firelight; Santa mid-tale with storytelling gesture; nearby child listening in pajamas; background softly suggests toys music and gift sparkle without cluttering faces; cozy lantern and hearth glow. Leave quiet upper areas for later text. Mug and steam read clearly. Not a standing lineup.
```
+ Dial D2 + spread add-on

### Backup Prompt (cozy close)
```
Intimate Christmas fireside scene: Santa with a steaming mug of cocoa, warm smile mid-story, child tucked nearby listening with wide eyes, soft firelight on faces, tree glowing in background, cozy gentle atmosphere. Focus on the warmth between them, not the room.
```
+ Dial D2 + spread add-on

**Temp:** `art-S06-cocoa-SPREAD-5250x2625.png`

---

## S7 — Proof · p18|19 · SPREAD (can go SINGLE if needed)

| | LEFT (p18) | RIGHT (p19) |
|---|---|---|
| **Poem** | When I heard all the noise up in the roof, / it hit me right then. I needed some proof. | Where can I go? What can I get? / I know, a photo. That's my best bet. |
| **Camera** | Child looking up — ceiling/roof cue · urgency | Idea spark · era-neutral **camera** on table or in hands — **not phone UI** |
| **Quiet zones** | Bottom left | Bottom right |

### Primary Prompt (spread)
```
Wide Christmas living-room spread: child looking sharply upward toward the ceiling as if hearing reindeer noise on the roof, startled playful urgency; continuous scene shows a plan forming — a simple classic camera resting nearby as the idea for proof (era-neutral camera body, NOT a modern phone UI, no glowing screen icons), warm interior light, Santa may be partly visible or already shifting away. Leave quiet bottom bands for later text. Dynamic look-up pose, not a static standing portrait.
```
+ Dial D2 + spread add-on

### Backup Prompt (strong single if spread feels thin)
```
Christmas living room scene: child looking urgently upward toward the ceiling, reindeer noise implied, a vintage camera on a nearby side table catching the child's eye — the idea dawning (classic camera, NOT phone UI). Single strong vertical composition. Warm interior, Christmas tree glow. Leave quiet area for text.
```
+ Dial D2 · FRAME ON (single)

### Optional SINGLE
If Jon decides this works better as one page: one 2625² plate — child look-up + camera idea, quiet bottom for all four lines.

**Temp:** `art-S07-proof-SPREAD-5250x2625.png` (or `art-P18-proof-2625.png` if single)

---

## S8 — Gone · p20|21 · SPREAD

| | LEFT (p20) | RIGHT (p21) |
|---|---|---|
| **Poem** | I flew out the door and was back in a flash. / But oh no, the hour had already passed. | And from the noise on top of the roof / I realized that I was still without proof. |
| **Camera** | Empty room · vacant gift spot · soft afterimage of where Santa was | Child returned with camera · door ajar · roof noise as ceiling attention |
| **Quiet zones** | Upper left | Upper right |

### Primary Prompt
```
Wide Christmas living-room spread of absence: empty spot among gifts where Santa sat, wrapping paper still, tree glowing; child rushing back holding a camera, disappointment and urgency, door still ajar behind, suggestion of noise from the roof by the child's upward glance. No Santa figure present. Leave quiet upper areas for later text. Emphasize empty space and motion — not a posed duo.
```
+ Dial D2 + spread add-on

### Backup Prompt (afterimage emphasis)
```
Christmas room spread: the warm space where Santa was sitting now empty — just scattered ribbons and a still-warm mug; child has just rushed back in holding a camera, face showing they missed him; the room feels full of his recent presence but he's gone. Soft melancholy with Christmas warmth.
```
+ Dial D2 + spread add-on

**Temp:** `art-S08-gone-SPREAD-5250x2625.png`

---

## S9 — Search · p22|23 · SPREAD

| | LEFT (p22) | RIGHT (p23) |
|---|---|---|
| **Poem** | I turned around slowly. I needed to know, / did he leave me a hint, a tip or a clue? / Did he forget his hat or maybe a shoe? / Now what am I supposed to do? | I know, I'll look up the flue. / I dashed to the flue but nothing was there. / I looked over here and I looked over there. / When I saw something on top of the chair, / my proof I thought was just laying right there. |
| **Camera** | Child crouching/searching under ribbons · no standing center | Fireplace dark flue empty → eye-line pulls to chair with small something on seat |
| **Quiet zones** | Outer left | Corner near chair |

### Primary Prompt
```
Wide Christmas mystery spread: LEFT — child searching the living room on hands and knees among ribbons and gifts, curious worried expression; RIGHT — continuous, dark empty chimney flue with child looking up into blackness, then composition leads the eye to an old wooden chair with something small resting on the seat (folded note shape, no readable writing). Soft dying fire and moonlight. Leave quiet corners for later text. Search energy, not standing portrait.
```
+ Dial D2 + spread add-on

### Backup Prompt (simpler — focus on chair reveal)
```
Christmas mystery spread: child searching through gift wrap and ribbons on the floor, then the composition pulls toward an old wooden chair where something small rests on the seat catching the light — the discovery moment. Dark fireplace on one side, warm chair on the other. Cinematic search energy.
```
+ Dial D2 + spread add-on

**Temp:** `art-S09-search-SPREAD-5250x2625.png`  
**Optional later:** split flue vs chair to SINGLE + SPREAD if crowded (Jon call).

---

## S10 — The Note · p24|25 · SPREAD · PRIORITY

| | LEFT (p24) | RIGHT (p25) |
|---|---|---|
| **Poem** | It wasn't a shoe, hat or a coat. / I couldn't believe it, the old guy. He left me a note. / I fell on the chair and started to stare. / What it said, I didn't care. | I tore open the note that Santa had wrote. / The words jumped out as to get my attention. / And there was one thing he told me to mention. |
| **Camera** | Child on/beside chair · note prop · wonder | Hands tearing open note · intimate close · no handwriting |
| **Quiet zones** | Outer left wall | Outer right |

### Primary Prompt
```
Wide cinematic climax spread: child on or beside an old wooden chair discovering a small folded note from Santa, wonder and disbelief; continuous RIGHT — close intimate focus on child's hands carefully tearing open the blank cream note paper (no readable writing, no letters), warm tree glow soft in background. Leave quiet outer edges for later text. Hands and note are the heroes.
```
+ Dial D2 + spread add-on

### Backup Prompt (emotional emphasis)
```
Christmas spread: child sitting beside a wooden chair holding a small folded note from Santa, face full of wonder and anticipation; the note glows softly in the tree light; intimate emotional moment, the room quiet and warm around them. Focus on the child's expression and the tiny folded paper — the whole world in that note.
```
+ Dial D2 + spread add-on

**Temp:** `art-S10-note-SPREAD-5250x2625.png`  
**Refs:** `style-refs/spread/spread-the-note-WIDE.png`

---

## S11 — Wish · p26|27 · SPREAD

| | LEFT (p26) | RIGHT (p27) |
|---|---|---|
| **Poem** | More than cakes, cocoa or milk. / Shirts made of cotton or ties made of silk. / Hats, stockings or a new coat. | What he wants is simply a note. |
| **Camera** | Soft still-life echo of gifts/cocoa/silk as gentle painted memory | Child holding glowing blank note · emotional reveal |
| **Quiet zones** | Top left | Top / outer for "simply a note" |

### Primary Prompt
```
Wide heartfelt Christmas spread: soft painted still-life suggestions of cocoa cake silk stockings and coats as gentle background memory (blurred, not photoreal product shots); focus on child holding Santa's open note paper glowing softly in tree light (BLANK paper only), peaceful revelation mood, cozy heirloom atmosphere. Leave quiet top areas for later text. Emotional quiet, not standing cast shot. Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume. NO readable letters, NO text, NO handwriting anywhere in the image.
```
+ Dial D2 + spread add-on + hard append + S11 text ban

### Backup Prompt (child + note intimacy · blank note)
```
Christmas spread: close warm scene of child sitting by the tree holding Santa's open note, the paper catching soft golden light; in the background, gentle blurred memories of cocoa, silk, and gifts from the poem — dreamy, not literal. Emotional revelation moment, peaceful and quiet. Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume. NO readable letters, NO text, NO handwriting anywhere in the image — blank cream note paper only.
```
+ Dial D2 + spread add-on + hard append + S11 text ban

**Temp:** `art-S11-wish-SPREAD-5250x2625.png`

---

## S12 — Blessing · p28|29 · SPREAD · 🎯 PRIORITY

| | LEFT (p28) | RIGHT (p29) |
|---|---|---|
| **Poem** | He said I've had enough eggnogs, cider and soups. / My belt's getting harder to fit in the loops. / And one last thing, please do me a favor. | Always love Christmas, act like a kid and pray to your Savior. / **God bless.** |
| **Camera** | Afterglow: empty chair + note + window snow OR child-with-note by tree | Reverent hopeful close |
| **Quiet zones** | Side for eggnog/belt lines | Band for favor / God bless |

### Primary Prompt (afterglow — preferred)
```
Wide heartfelt closing Christmas spread: warm living room after Santa's visit, empty chair with a small open note nearby, soft snow light at the window, tree and fireplace still glowing, child quietly holding the note near the tree with wonder and love (not a stiff posed portrait with Santa), deep heirloom Golden Age feeling. Leave quiet bands for later blessing text. Seamless painted scene. No readable writing on the note.
```
+ Dial D2 + spread add-on

### Backup Prompt (Santa farewell)
```
Christmas blessing spread: soft farewell moment — Santa gently rising toward the chimney, a warm fond look backward, child in foreground holding the note near the tree, blessedly peaceful. Golden light, snow at window, deep love. Not a posed museum portrait — a living moment.
```
+ Dial D2 + spread add-on

**Temp:** `art-S12-blessing-SPREAD-5250x2625.png`  
**Refs:** `style-refs/spread/spread-04-closing-blessing-*`

---

# BACK MATTER PROMPTS

---

## Pages 30|31 — Thanks + Jack Portrait

| | LEFT (p30) | RIGHT (p31) |
|---|---|---|
| **Text** | Thank You + Draft A body · ends God bless — Jack Farrell | Optional small "About the Author" line |
| **Art** | Soft open zone / cloud for type | 🔒 LOCKED `Media/approved/characters/jack-farrell-portrait.png` |

No new generation needed unless Jon requests a print remake of the portrait.

---

## Pages 32|33 — Quiet Close · SINGLES

### P32 Prompt
```
Soft Christmas Eve quiet vignette, empty chair and faint tree glow, snow hush at window, large open cream for later text God bless Merry Christmas, no people, painted gouache, FRAME ON
```
+ master style

### P33 Prompt
```
Matching Christmas close vignette: soft ornament resting on a mantel, warm gentle glow, peaceful quiet, open cream for last words, no people, FRAME ON
```
+ master style

---

## Pages 34-36 — Optional Padding

Soft ornament repeats or blanks. Generate only if keeping these pages. Trim if going shorter.

---

# 🚀 HOW TO GENERATE

### Step 1: Pick your spread
Find the spread above. Read the poem lines. Check the camera direction and quiet zones.

### Step 2: Copy the Primary Prompt
Each spread has a ready-to-paste prompt block. Copy it exactly.

### Step 3: Add style tags
- **Lane A1 (Klein 9B dial):** `+ Dial D2 + spread add-on`
- **Lane A2 (Qwen alt):** `+ master style (short) + spread add-on`
- **Lane B (Finals):** `+ master style + spread add-on`

### Step 4: Run
```powershell
npm run image:fal:klein9 -- "<PROMPT>. <Dial D2>. seamless continuous two-page spread..."
```

### Step 5: Record
Every mock gets a `RECIPE.md` under `Media/generated/mocks/{unit}/vNN/` — include: prompt, model, lane, frame, refs, verdict.

### Step 6: If the first prompt misses
Use the Backup Prompt. Same process. If both miss, simplify — reduce to 3-4 key elements per side.

---

# ✅ DECISION GATES (Jon confirms)

| # | Decision | Current |
|---|---|---|
| 1 | Page count | **35–40** locked · working target **36** (BOOK-PAGE-WORKFLOW) |
| 2 | All story beats as spreads? | Yes (S1-S12) · S7 can go single · S9 may split later |
| 3 | S12 afterglow or Santa farewell? | Afterglow preferred |
| 4 | Generate in order? | Sequential: P01 → P02 → P03 → 4|5 → S1...S12 → BM |
| 5 | This dock's scope | **Authoritative for prompts + generation** — page map stays BOOK-PAGE-WORKFLOW |

---

# DOCUMENT INDEX

| Doc | Role |
|-----|------|
| **THIS FILE** | **Master Production Dock** — authoritative **prompts + generation** |
| `BOOK-PAGE-WORKFLOW.md` | **Page map SoT** — page numbers, filenames, poem placement |
| `PAGE-BUILD-WORKFLOW.md` | PS → InDesign build loop |
| `IMAGE-LANE-PROMPTS.md` | Klein D2 vs finals + frame system |
| `ILLUSTRATION-STYLE.md` | Master style reference |
| `AGENT-RUNBOOK.md` | Print specs, Lulu rules, design standards |
| `Transcription/poem-clean.txt` | Poem text of record |
| `Media/approved/INDEX.md` | Approved art tracking |
| `POEM-IMAGE-PROMPT-DOCK.md` | Stub → redirects here |
| `PAGE-PROMPT-BIBLE.md` | Stub → redirects here |

---

*Authoritative for prompts and generation. Page numbers / filenames / poem placement: BOOK-PAGE-WORKFLOW.md. Update this dock when prompt decisions change.*
