# BOOK PAGE WORKFLOW — Poem → Art → Pages

**Status:** Working draft **2026-07-20** — Jon reviews / tweaks before we lock  
**Purpose:** One accurate map of **every interior page**, the **poem words** on it, the **image to create**, and **temp filenames** so we know what to generate.  
**How to build each page (PSD / mocks / recipes):** **`PAGE-BUILD-WORKFLOW.md`**  
**Text of record:** `Transcription/poem-clean.txt`  
**Copy (About / Thank You / credits):** `BOOK-COPY-DRAFTS.md`  
**Build authority:** `AGENT-RUNBOOK.md`  
**Related (older proposals):** `SPREAD-STORY-MAP.md` · `PAGE-PROMPT-BIBLE.md`

---

## Rules (locked preferences)

| Preference | Rule |
|------------|------|
| **Story form** | **Spread-first** — continuous 5250×2625 art whenever the moment deserves it |
| **Singles** | Use when a beat is quieter, transitional, or text-heavy matter — not the default |
| **Page count** | **35–40** locked · this draft targets **36** (even, Lulu-friendly) |
| **Facing math** | Open book = **even LEFT \| odd RIGHT** (e.g. 6\|7, 10\|11). Story spreads always sit on those pairs |
| **Type** | Live **Cormorant** in InDesign — **no poem text baked into art** · poem MOCK in PS = **20/26** so preview matches |
| **Image size** | Page **2625²** · spread **5250×2625** — place full-bleed in ID (no habitual re-scale). See `PAGE-BUILD-WORKFLOW.md` §1b |
| **Spreads** | **No fake middle gutter/spine line** in art — seamless scene; orange fold = PSD guide only |
| **Klein dial** | Lane A = Klein 4B + **Dial D2** append only (`IMAGE-LANE-PROMPTS.md`) |
| **Watermarks** | Flag on finals; Jon removes in Photoshop before print promote |
| **Prototype caveat** | Current `eyes-met-prototype-v1.indd` page numbers are **mock layout**, not this final book map |
| **Docs triggers** | **`update docs`** = harvest into this map + build workflow · **`log fixes`** = ISSUES-RESOLVED incident card · see `PAGE-BUILD-WORKFLOW.md` §11 |

---

## Naming convention (temp → keepers)

| Kind | Pattern | Example |
|------|---------|---------|
| Spread master | `art-S{NN}-{slug}-SPREAD-5250x2625.png` | `art-S03-eyes-met-SPREAD-5250x2625.png` |
| Spread L / R chops | `art-S{NN}-{slug}-LEFT.png` · `…-RIGHT.png` | after PS export to `Images/chopz/` |
| Single page | `art-P{NN}-{slug}-2625.png` | `art-P04-about-vignette-2625.png` |
| Matter (no new art) | `—` or reuse locked plate | Jack portrait already locked |
| Working PSD | `Xtraz/Adobe-Photoshop/{slug}.psd` | from `spread-page-template` / `single-page-template` |
| Dial / rejects | `Media/generated/…` | never treat as print keepers |
| Approved print | `Media/approved/print/…` | after Pass B + watermark check |

**Slug list (story):** `approach` · `threshold` · `eyes-met` · `sit-here` · `chat` · `cocoa` · `proof` · `gone` · `search` · `note` · `wish` · `blessing`

---

## At-a-glance — full book (36 pages)

| Pages | Form | Unit | Title / role | Art status |
|------:|------|------|--------------|------------|
| — | COVER | Cover wrap | Front / spine / back (Lulu template later) | Front **LOCKED** beige-v2 |
| 1 | SINGLE | FM | Title | Need title treatment |
| 2 | SINGLE | FM | Copyright + edition credits | Type-led · soft ornament OK |
| 3 | SINGLE | FM | Dedication | Soft vignette |
| 4 \| 5 | MATTER OPEN | FM | About This Story (L) + soft vignette (R) | Need vignette R |
| 6 \| 7 | **SPREAD** | **S1** | Approach — noise / peek / door | **Need** |
| 8 \| 9 | **SPREAD** | **S2** | Threshold — enter / sneak up on Santa | **Need** |
| 10 \| 11 | **SPREAD** | **S3** | Eyes met / splendor | **HAS** Tier B + MOCK chops |
| 12 \| 13 | **SPREAD** | **S4** | Sit over here / gifts on floor | **Need** (style-refs exist) |
| 14 \| 15 | **SPREAD** | **S5** | Chat & laugh | **Need** |
| 16 \| 17 | **SPREAD** | **S6** | Stories / cocoa not milk | **Need** |
| 18 \| 19 | **SPREAD** | **S7** | Roof noise → need a photo | **Need** |
| 20 \| 21 | **SPREAD** | **S8** | Dash back — Santa gone | **Need** |
| 22 \| 23 | **SPREAD** | **S9** | Search / flue / something on the chair | **Need** |
| 24 \| 25 | **SPREAD** | **S10** | The note — found & torn open | **Need** (style-refs exist) |
| 26 \| 27 | **SPREAD** | **S11** | What he wants is simply a note | **Need** |
| 28 \| 29 | **SPREAD** | **S12** | Blessing — love Christmas / God bless | **Need** (style-refs exist) |
| 30 \| 31 | MATTER OPEN | BM | Thank You (L) + **Jack / Dad portrait** (R) | Portrait **LOCKED** |
| 32 \| 33 | MATTER OPEN | BM | Quiet close (L) + Merry Christmas (R) | Soft ornaments |
| 34 \| 35 | OPTIONAL | BM | Extra quiet / colophon — **cut if we trim to 34** | Optional |
| 36 | SINGLE | BM | Final blank or small ornament — **or cut** | Optional |

**Trim options:** Drop 34–36 → **33** (odd — add blank to **34**). Prefer keep **36** or trim to **32** by shortening front (merge 4\|5 into one About page) — Jon chooses.

---

## Cover (not an interior page)

| Piece | Copy / art | Temp / keeper name |
|-------|------------|--------------------|
| Front | Title *The Night I Met Santa* · oatmeal holly PJs · Santa face **hidden** | `Media/approved/covers/cover-front.png` **LOCKED** |
| Back | Blurb + small credit | Need final wrap after interior page count |
| Spine | Title + author (width from Lulu after interior upload) | No spine PSD — Lulu casewrap |

---

## Front matter (detail)

### Page 1 — Title (SINGLE · right)

| | |
|--|--|
| **Text** | *The Night I Met Santa* · Jack Farrell (credit line as designed) |
| **Imagery** | Quiet Christmas Eve living-room glow or tree — leave center/upper quiet for title type (Cinzel) |
| **Temp file** | `art-P01-title-2625.png` |
| **Notes** | Can echo cover mood without duplicating cover composition |

### Page 2 — Copyright (SINGLE · left)

| | |
|--|--|
| **Text (locked)** | First illustrated edition, 2026. / Written by Jack Farrell. / Book design by Jon Farrell. |
| **Imagery** | Minimal — soft wash or tiny ornament; mostly type |
| **Temp file** | `art-P02-copyright-ornament-2625.png` *(optional)* |

### Page 3 — Dedication (SINGLE · right)

| | |
|--|--|
| **Text (locked)** | For my family, with love. — Jack Farrell |
| **Imagery** | Soft hearth / chair / tree vignette; quiet center for dedication |
| **Temp file** | `art-P03-dedication-2625.png` |

### Pages 4 \| 5 — About This Story (MATTER OPEN)

| | LEFT (p4) | RIGHT (p5) |
|--|-----------|------------|
| **Text** | **About This Story** + Draft A body (`BOOK-COPY-DRAFTS.md`) | Little or no text — room to breathe |
| **Imagery** | Soft paper / cloud zone for copy | Quiet vignette — snowy window, tree, or empty gift room hush |
| **Temp files** | *(type in InDesign)* | `art-P05-about-vignette-2625.png` |
| **Alt (if Jon wants tighter front)** | Collapse to **one** About page and start S1 on **4\|5** instead | — |

---

## Story body — spreads (detail)

Poem lines assigned to **LEFT** / **RIGHT** pages. Art = **one continuous scene** across the gutter (no fake fold on finals).

### S1 — Approach · pages **6 \| 7** · SPREAD

| | LEFT (p6) | RIGHT (p7) |
|--|-----------|------------|
| **Poem** | I searched and I peeked when I first heard the noise. / Something or someone was in with the toys. / I slithered and crawled for a peek of a glimpse. / It must be some fairies or holiday imps. | I got up the nerve to go to the door, / a door that was decorated, bolted and locked. |
| **Imagery** | Child peeking from dim hall toward glowing living room; toys hint beyond | Same continuous scene → decorated door with wreath/bolt; warm light spill |
| **Temp master** | `art-S01-approach-SPREAD-5250x2625.png` |
| **Chops** | `art-S01-approach-LEFT.png` · `art-S01-approach-RIGHT.png` |
| **Quiet zones** | Lower / outer corners for cloud text | Outer / lower for remaining lines |

### S2 — Threshold · pages **8 \| 9** · SPREAD

| | LEFT (p8) | RIGHT (p9) |
|--|-----------|------------|
| **Poem** | I didn't know it when I entered the room / to surprise the amazement or even the shock. | Now I'm usually calm, not very loud, / or even known to be a ranter. / But what do you say when you sneak up on Santa? |
| **Imagery** | Child at doorway; living room opens; **half-seen** Santa among gifts (face not full hero yet) | Continuous — more of Santa’s red coat / gifts; child still at threshold wonder |
| **Temp master** | `art-S02-threshold-SPREAD-5250x2625.png` |
| **Chops** | `art-S02-threshold-LEFT.png` · `art-S02-threshold-RIGHT.png` |

### S3 — Eyes met · pages **10 \| 11** · SPREAD · **HAS ART**

| | LEFT (p10) | RIGHT (p11) |
|--|-----------|------------|
| **Poem** | My jaw dropped when our eyes finally met. / I knew right then, it was a moment I would never forget. | For there he was in all his splendor, / brilliant white hair, red coat with suspenders. |
| **Imagery** | Face-to-face hero — child + Santa eye contact; suspenders visible; gifts / tree |
| **Keepers** | `Media/approved/spreads/spread-eyes-met.png` · chops in `Images/chopz/spread-01-eyes-met-*` |
| **Temp / final names** | Promote naming → `art-S03-eyes-met-SPREAD-5250x2625.png` (alias OK) |
| **Notes** | InDesign prototype matched this beat — **remap** to book pages 10\|11 when building full doc |

### S4 — Sit here · pages **12 \| 13** · SPREAD

| | LEFT (p12) | RIGHT (p13) |
|--|-----------|------------|
| **Poem** | He was down on the floor between boxes, gifts and ribbons galore. / I couldn't move, I stayed very still. | Finally he whispered, "Sit over here. / Have a moment to kill." |
| **Imagery** | Santa on floor among gifts/ribbons; child frozen; wide gift field | Santa beckoning; warm invitation; space for dialogue cloud |
| **Temp master** | `art-S04-sit-here-SPREAD-5250x2625.png` |
| **Chops** | `art-S04-sit-here-LEFT.png` · `art-S04-sit-here-RIGHT.png` |
| **Refs** | Style-refs / prior “sit here” dials if any |

### S5 — Chat · pages **14 \| 15** · SPREAD

| | LEFT (p14) | RIGHT (p15) |
|--|-----------|------------|
| **Poem** | Oh, what a feeling, such a thrill. / We chatted and laughed what seemed like an hour. | But with laughs, stories and chatter, / who cares, it didn't much matter. |
| **Imagery** | Warm two-shot — child + Santa laughing together by tree/gifts |
| **Temp master** | `art-S05-chat-SPREAD-5250x2625.png` |
| **Chops** | `art-S05-chat-LEFT.png` · `art-S05-chat-RIGHT.png` |
| **Refs** | `style-refs/spread/spread-chat-laugh-WIDE.png` |

### S6 — Cocoa · pages **16 \| 17** · SPREAD

| | LEFT (p16) | RIGHT (p17) |
|--|-----------|------------|
| **Poem** | He spoke of many places, people and things. / From toys to music to bright diamond rings. | Coats made of wool, ties made of silk. / He even revealed his passion for hot cocoa instead of cold milk. |
| **Imagery** | Storytelling beat — cocoa mug as hero prop; cozy firelight; Santa mid-tale |
| **Temp master** | `art-S06-cocoa-SPREAD-5250x2625.png` |
| **Chops** | `art-S06-cocoa-LEFT.png` · `art-S06-cocoa-RIGHT.png` |

### S7 — Proof · pages **18 \| 19** · SPREAD

| | LEFT (p18) | RIGHT (p19) |
|--|-----------|------------|
| **Poem** | When I heard all the noise up in the roof, / it hit me right then. I needed some proof. | Where can I go? What can I get? / I know, a photo. That's my best bet. |
| **Imagery** | Child looks up (roof cue); idea spark; camera / phone era-neutral “photo” prop |
| **Temp master** | `art-S07-proof-SPREAD-5250x2625.png` |
| **Chops** | `art-S07-proof-LEFT.png` · `art-S07-proof-RIGHT.png` |

### S8 — Gone · pages **20 \| 21** · SPREAD

| | LEFT (p20) | RIGHT (p21) |
|--|-----------|------------|
| **Poem** | I flew out the door and was back in a flash. / But oh no, the hour had already passed. | And from the noise on top of the roof / I realized that I was still without proof. |
| **Imagery** | Empty living room; child returned with camera; Santa’s place vacant; roof noise implied |
| **Temp master** | `art-S08-gone-SPREAD-5250x2625.png` |
| **Chops** | `art-S08-gone-LEFT.png` · `art-S08-gone-RIGHT.png` |

### S9 — Search · pages **22 \| 23** · SPREAD

| | LEFT (p22) | RIGHT (p23) |
|--|-----------|------------|
| **Poem** | I turned around slowly. I needed to know, / did he leave me a hint, a tip or a clue? / Did he forget his hat or maybe a shoe? / Now what am I supposed to do? | I know, I'll look up the flue. / I dashed to the flue but nothing was there. / I looked over here and I looked over there. / When I saw something on top of the chair, / my proof I thought was just laying right there. |
| **Imagery** | Searching living room → chimney/flue empty → **focus pulls to chair** with something on it |
| **Temp master** | `art-S09-search-SPREAD-5250x2625.png` |
| **Chops** | `art-S09-search-LEFT.png` · `art-S09-search-RIGHT.png` |
| **Optional SINGLE later** | If this open feels too crowded, split flue vs chair into a single + spread — Jon call |

### S10 — The note · pages **24 \| 25** · SPREAD

| | LEFT (p24) | RIGHT (p25) |
|--|-----------|------------|
| **Poem** | It wasn't a shoe, hat or a coat. / I couldn't believe it, the old guy. He left me a note. / I fell on the chair and started to stare. / What it said, I didn't care. | I tore open the note that Santa had wrote. / The words jumped out as to get my attention. / And there was one thing he told me to mention. |
| **Imagery** | Note on chair → child opening letter; **no readable handwriting in art** |
| **Temp master** | `art-S10-note-SPREAD-5250x2625.png` |
| **Chops** | `art-S10-note-LEFT.png` · `art-S10-note-RIGHT.png` |
| **Refs** | `style-refs/spread/spread-the-note-WIDE.png` |

### S11 — Wish · pages **26 \| 27** · SPREAD

| | LEFT (p26) | RIGHT (p27) |
|--|-----------|------------|
| **Poem** | More than cakes, cocoa or milk. / Shirts made of cotton or ties made of silk. / Hats, stockings or a new coat. | What he wants is simply a note. |
| **Imagery** | Soft letter / tree glow; emotional reveal; still **no readable note text** in paint |
| **Temp master** | `art-S11-wish-SPREAD-5250x2625.png` |
| **Chops** | `art-S11-wish-LEFT.png` · `art-S11-wish-RIGHT.png` |

### S12 — Blessing · pages **28 \| 29** · SPREAD

| | LEFT (p28) | RIGHT (p29) |
|--|-----------|------------|
| **Poem** | He said I've had enough eggnogs, cider and soups. / My belt's getting harder to fit in the loops. / And one last thing, please do me a favor. | Always love Christmas, act like a kid and pray to your Savior. / **God bless.** |
| **Imagery** | Closing blessing mood — warm, reverent, hopeful; child + Santa or afterglow of visit |
| **Temp master** | `art-S12-blessing-SPREAD-5250x2625.png` |
| **Chops** | `art-S12-blessing-LEFT.png` · `art-S12-blessing-RIGHT.png` |
| **Refs** | `style-refs/spread/spread-04-closing-blessing-*` |

---

## Back matter (detail)

### Pages 30 \| 31 — Thank You + Dad / Jack portrait

| | LEFT (p30) | RIGHT (p31) |
|--|-----------|------------|
| **Role** | **Thank You** (Draft A) | **Jack Farrell portrait** (Dad) |
| **Text** | Thank You + Draft A body · ends God bless — Jack Farrell | Optional small “About the Author” line under/ beside portrait — or image-led |
| **Art** | Soft open zone / cloud for type | **LOCKED** `Media/approved/characters/jack-farrell-portrait.png` |
| **Temp** | — | Keeper already · optional `art-P31-jack-portrait-2625.png` print remake |

### Pages 32 \| 33 — Quiet close

| | LEFT (p32) | RIGHT (p33) |
|--|-----------|------------|
| **Text (locked quiet page)** | God bless. / Merry Christmas. / May the magic of this night stay in your heart, long after the season has gone. | Can split lines L/R or keep all on one side with ornament opposite |
| **Imagery** | Soft ornament / snow / empty chair peace | Matching close vignette |
| **Temp files** | `art-P32-quiet-close-2625.png` | `art-P33-merry-christmas-2625.png` |

### Pages 34 \| 35 \| 36 — Optional padding

| Page | Role | Keep? |
|-----:|------|-------|
| 34 | Extra quiet ornament or blank | Optional — cut if trimming |
| 35 | Colophon / tiny reprint note | Optional |
| 36 | Final blank (printer-friendly even end) | Optional |

If Jon wants **exactly 32:** drop About vignette open (merge About onto p3 or p4 alone), drop 34–36, and start S1 on **4\|5** (remap all story page numbers −2). Say the word and this table gets a “32-page” sibling section.

---

## Image creation checklist (story)

| ID | Temp master | Form | Priority | Status |
|----|-------------|------|----------|--------|
| S1 | `art-S01-approach-SPREAD-5250x2625.png` | Spread | High | ☐ Need |
| S2 | `art-S02-threshold-SPREAD-5250x2625.png` | Spread | High | ☐ Need |
| S3 | `art-S03-eyes-met-SPREAD-5250x2625.png` | Spread | — | ☑ Has |
| S4 | `art-S04-sit-here-SPREAD-5250x2625.png` | Spread | High | ☐ Need |
| S5 | `art-S05-chat-SPREAD-5250x2625.png` | Spread | Mid | ☐ Need |
| S6 | `art-S06-cocoa-SPREAD-5250x2625.png` | Spread | Mid | ☐ Need |
| S7 | `art-S07-proof-SPREAD-5250x2625.png` | Spread | Mid | ☐ Need |
| S8 | `art-S08-gone-SPREAD-5250x2625.png` | Spread | Mid | ☐ Need |
| S9 | `art-S09-search-SPREAD-5250x2625.png` | Spread | Mid | ☐ Need |
| S10 | `art-S10-note-SPREAD-5250x2625.png` | Spread | High | ☐ Need |
| S11 | `art-S11-wish-SPREAD-5250x2625.png` | Spread | Mid | ☐ Need |
| S12 | `art-S12-blessing-SPREAD-5250x2625.png` | Spread | High | ☐ Need |
| P01 | `art-P01-title-2625.png` | Single | Mid | ☐ Need |
| P03 | `art-P03-dedication-2625.png` | Single | Low | ☐ Need |
| P05 | `art-P05-about-vignette-2625.png` | Single | Low | ☐ Need |
| P31 | Jack portrait | Single | — | ☑ Locked |
| P32–33 | Quiet / Merry | Single | Low | ☐ Need |

**Production loop per unit:** Lane A dial (Klein) → Jon pick → Lane B finals (Gemini/Banana) → watermark check → PS MOCK + chops → InDesign live Cormorant.

---

## Where singles still fit (if we break a spread)

Jon preference = spreads. Candidates to demote to **SINGLE** only if a spread feels forced:

| Beat | Why a single might win |
|------|-------------------------|
| S7 Proof | Idea/camera beat can be one strong vertical |
| S9 Search | Flue vs chair could be two quieter pages |
| Matter | Title / copyright / dedication stay singles |

Mark changes here when Jon decides — don’t silently change the map.

---

## Decision gates for Jon

1. **Confirm 36** as working page count (or request 32 / 40 remap).  
2. **Confirm** About as pages **4\|5** (text + vignette) vs thinner front.  
3. **Confirm** Thank You \| Jack portrait as **30\|31** facing pair.  
4. **Confirm** all story units stay spreads (S1–S12) for now.  
5. After confirm → generate art in checklist order (S1/S2 next after eyes-met polish, or S4).

---

## Doc index

| Doc | Role |
|-----|------|
| **This file** | Page-accurate workflow + filenames + poem placement |
| `SPREAD-STORY-MAP.md` | Earlier 32-page / 12-spread proposal (superseded for numbering by this draft) |
| `PAGE-PROMPT-BIBLE.md` | Detailed generation prompts (update beat forms → Spread when this locks) |
| `BOOK-COPY-DRAFTS.md` | Locked About / Thank You / dedication / credits |
| `CHARACTER-JACK-FARRELL.md` | Dad portrait remake kit |
| `CONTINUITY-AND-PRINT-FINALS.md` | Pass B sizes + watermark gate |
