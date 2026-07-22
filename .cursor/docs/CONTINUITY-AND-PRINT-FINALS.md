# CONTINUITY + PRINT FINALS — Plan (locked approach)

**Status:** Recommended operating plan · 2026-07-15  
**Why:** Approved art today is **composition / vibe lock**, often ~1K dial size — **not** Lulu print plates yet. Boy + Santa must stay the same people across 35-40 pages.

---

## 1) Two-pass art pipeline (resolution)

### Pass A — Composition lock (what we do now)

| Location | Role |
|----------|------|
| `Media/approved/` Tier B | Jon says “approved” — layout, pose, Easter eggs, mood |
| `Media/approved/style-refs/` | Moodboard / near-keepers |
| `Media/generated/` | Experiments |

**Accept that Pass A files may be wrong pixel size.** Do **not** stretch them blindly for PDF.

### Pass B — Print finals (when book art is composition-complete)

| Location | Role |
|----------|------|
| **`Media/approved/print/`** *(create at finals time)* | Only print-ready plates |
| `…/print/pages/` | **2625 × 2625** @ 300 DPI (8.75" with bleed) |
| `…/print/spreads/` | **5250 × 2625** masters → split L/R |
| `…/print/covers/` | Front/back per Lulu wrap template after page count |

**How to remake “exactly the same” at high res**

1. Keep the **approved Pass A PNG** as the primary `image_urls[0]` for Banana `/edit`.
2. Add **character sheets** + 1–2 style north stars in `image_urls`.
3. Prompt pattern:

```
Remake this exact approved illustration at print quality.
Preserve composition, poses, camera angle, props (including baseball glove + bat if present), lighting, and title treatment if on cover.
Same painted gouache style. Do not redesign the scene.
No extra text unless already in the approved image.
If this is a two-page SPREAD: keep a seamless continuous scene — remove any fake book gutter, vertical fold line, or center spine shadow.
```

4. Request **`resolution: 2K`** (or higher if needed), then **crop/resize** in Pillow to exact 2625² / 5250×2625.
5. Promote only after Jon eyeballs Pass A vs Pass B side-by-side.
6. **Watermark gate:** confirm no AI/service watermarks, logos, or corner badges. If any appear, **Jon cleans them in Photoshop** before print promote / InDesign link. Agent must flag — do not treat watermarked files as print-ready.

**Do not** rely on generic AI “upscale only” as the sole finals path — composition remake **from the approved file as ref** is more faithful for this stack.

---

## 2) Prompt / recipe sidecar (so remakes match)

For **every** mock version and every Tier B approved file:

| Kind | Path |
|------|------|
| Mock try | `Media/generated/mocks/{unit}/vNN/RECIPE.md` |
| Template | `Media/generated/mocks/_RECIPE-TEMPLATE.md` |
| Approved lock | `Media/approved/…/{name}.recipe.md` |

**Standard (LOCKED 2026-07-21):** full field table + **Prompt** + refs + negatives + gotchas — see `.cursor/docs/PAGE-BUILD-WORKFLOW.md` §6.  
Use `n/a` / `—` when unknown; **never omit Prompt**. Include `script_text` (poem/title lines) and `type_zone` when the page has type.

**Minimum was** (superseded — still OK on old thin locks until backfilled):

| Field | Example |
|-------|---------|
| `approved_file` | `covers/cover-front.png` |
| `source_batch` | `cover-d-santa-peek/…/E-glove-at-sack-b.png` |
| `beat_or_role` | front cover |
| `print_target_px` | cover wrap TBD / or 2625² draft |
| `fal_endpoint` | `fal-ai/nano-banana-pro/edit` |
| `prompt` | full text used (or bible beat id) |
| `refs` | paths to character sheets + style-refs used |
| `notes` | “glove left of sack; bat at fireplace; no Santa face” |
| `jon_approved_date` | 2026-07-15 |

Optional: `Media/approved/MANIFEST.json` listing all Tier B rows for a scripted finals batch later.

**Agent rule:** When promoting to Tier B, **write/update the recipe the same day** — don’t wait until PDF week. New mocks: copy `_RECIPE-TEMPLATE.md` and fill completely before showing Jon.

---

## 3) Character continuity (boy + Santa)

PAGE-PROMPT-BIBLE already says match **G0 sheets** — those sheets must be **locked before print finals**.

### Lock sheets first (before mass Pass B)

| Sheet | Path (target) | Content |
|-------|----------------|---------|
| **Boy G0 full** | `Media/approved/characters/boy-narrator-G0.png` | **LOCKED** — `boy-solo-B` · age ~7–9 · oatmeal holly PJs |
| **Boy G0 face** | `Media/approved/characters/boy-narrator-G0-face.png` | **LOCKED** — `boy-solo-C` · likeness close-up |
| **Santa G0** | `Media/approved/characters/santa-G0.png` | **LOCKED** — `santa-solo-C` · suspenders / kind face |
| Jack (done) | `characters/jack-farrell-portrait.png` | Author only — not story boy |

**Pilot spread locked:** `Media/approved/spreads/spread-eyes-met.png` (`eyes-met-SPREAD-v3B`) — style + cast reference for other beats.

### Wardrobe bible (LOCKED 2026-07-15)

| Role | Default (locked) | Allowed variants |
|------|------------------|------------------|
| Boy | Oatmeal/taupe PJs + tiny holly (cover + G0 B/C) | Face from G0-face; full from G0 body |
| Santa | Red coat/robe + **suspenders** + kind face (santa-solo-C) | Boots; suspenders visible on face-forward beats |

**Rule:** Face + body type + age lock hard. Boy PJs stay the oatmeal-holly family across the book unless Jon unlocks a change.

### Every finals generation call

```
image_urls = [
  approved_pass_A_composition,   # must stay #1
  boy_G0_sheet,
  santa_G0_sheet,                # omit if Santa absent that beat
  optional_style_north_star,
]
```

Plus continuity line in prompt:

```
Same boy as character sheet (face, hair, age). Same oatmeal/taupe holly pajamas as locked cover.
Same Santa as character sheet (beard, coat, suspenders).
Do not invent a new child, new Santa, or new pajama design.
```

### Continuity QA gate (before `print/` promote)

- [ ] Boy face matches G0 (side-by-side)
- [ ] Santa matches G0 when present
- [ ] Room family consistent (tree / fireplace language)
- [ ] Quiet zone still open for text
- [ ] Exact print pixel size

---

## 4) Recommended timeline

| Phase | When | What |
|-------|------|------|
| Now | Composition sprint | Approve covers + pages at dial/1K; write recipes on promote |
| Soon | **Character sheet lock** | Boy G0 + Santa G0 before more Banana spend |
| After compositions done | Pass B weekend | Batch remake → `Media/approved/print/` @ 2625 / 5250 |
| Then | Composite | Pillow text → `Pages/` → Typst → Lulu |

**Do not** Pass-B every page while still changing story beats — remake once per locked composition.

---

## 5) Folder end-state (target)

```
Media/approved/
  characters/          boy-G0, santa-G0, jack…
  covers/              cover-front.png (+ .recipe.md)
  pages/               composition locks
  spreads/
  style-refs/          moodboard
  print/               ← finals only (create later)
    covers/
    pages/
    spreads/
    INDEX.md
```

---

## Related

- Sizes: `BOOK-PLAN.md` / `PAGE-PROMPT-BIBLE.md` (2625² · 5250×2625)
- Lanes: `BOOK-PRODUCTION-SYSTEM.md` §2
- Jack: `CHARACTER-JACK-FARRELL.md`
- Cover now: `Media/approved/covers/cover-front.png`
