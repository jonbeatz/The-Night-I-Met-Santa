# IMAGE LANE SYSTEM v2 — The Night I Met Santa
**Created:** July 22, 2026 · **Status:** LOCKED (model tiers)  
**Supersedes:** IMAGE-LANE-PROMPTS.md lane configuration (v1)

> Model tiers locked 2026-07-22 after S4 style-lock + Banana pipeline tests. Do not reopen casually.

---

## 🔒 Locked character references

| Role | File | Source | Rule |
|------|------|--------|------|
| **Santa (definitive)** | `Media/approved/characters/santa-G0-v2.png` (+ `santa-G0.png` wardrobe sheet) | S4 **v08** + standing sheet | Continuity lock — open coat |
| **Boy (definitive)** | `boy-narrator-G0.png` + `boy-narrator-G0-face.png` | G0 confirmed 2026-07-22 | Continuity lock — holly PJs + face |
| Style / atmosphere | `Media/approved/style-refs/style-lock-v2.png` | S4 **v11** Krea regen (was v07) | Use on dials + finals |
| **Mock-up quality target (S1 door)** | `Media/development/_quality-targets/S01-approach-R-quality-target.jpg` | **S01 v01** Klein 9B chop (best-of 2026-07-21) | Composition + rim-light quality for Qwen mocks |
| **Mock-up quality target (S1 hall)** | `Media/development/_quality-targets/S01-approach-L-quality-target.jpg` | same v01 Klein chop | Crawl POV / warm doorway spill |

### Boy G0 lock (CONFIRMED 2026-07-22 — no drift)

**Refs (attach on every gen with the boy):** `boy-narrator-G0.png` · `boy-narrator-G0-face.png`

| Detail | Rule |
|--------|------|
| PJ base | **Oatmeal/taupe** — warm beige · **NOT** white · **NOT** cream · **NOT** bright |
| Pattern | **Green holly leaves + red berries** — clearly visible across fabric, not subtle |
| Trim | **Red trim** on collar, sleeve cuffs, and pant hems |
| Buttons | **Red buttons** down the front of the shirt |
| Cut | Classic **button-up** pajama set |
| Hair | Tousled **light brown** with **golden highlights** |
| Eyes | Large expressive **brown eyes** |
| Skin | **Rosy cheeks**, soft peachy complexion |
| Expression | Varies by scene (wonder / surprise / awe / joy) — identity never changes |

Both Boy G0 refs **and** Santa G0 v2 are locked characters. Attach both families on every story gen that includes either figure (within the model’s max image_urls — prioritize style-lock + active characters).

### Santa continuity lock (not a preference)

**LOCKED 2026-07-22** — replaces prior “black suspenders over the coat.”

| Detail | Rule |
|--------|------|
| Coat | Red coat worn **OPEN and unbuttoned** — not closed, not a solid red block |
| Shirt | Cream/off-white **vertically striped** button-down visible underneath |
| Suspenders | **Brown leather** suspenders over the **striped shirt** — **NOT** over the coat fabric |
| Lower | Red pants · black boots · white fur trim on cuffs and hem |
| Presence | Relaxed, approachable, grandfather-like — **not** a formal costume |
| Pose | Sitting/kneeling on the floor among gifts when the beat allows |

**Refs:** `santa-G0-v2.png` (definitive) · `santa-G0.png` (standing wardrobe sheet — same outfit).  
Prior “suspenders over coat” language is **retired**. New gens must match open-coat / suspenders-on-shirt.

---

## ⚡ Locked model tiers

### Dial / mock-up tier (pre-viz · flow passes · composition)

| Role | Model | Cost | Notes |
|------|--------|------|-------|
| **Primary dial** | Klein 9B (`fal-ai/flux-2/klein/9b`) | ~$0.01 | Cheap baseline / control · also source of S1 quality targets |
| **Favorite mock look** | Qwen 2 Pro `/edit` | ~$0.08 | Detail + edge for mocks |
| **Atmosphere ref** | `style-lock-v2.png` (Krea) | — | Always attach |
| **Quality / lighting ref** | `mockup-quality/S01-approach-*-quality-target.jpg` | — | **Always attach on Qwen mocks** when a beat has a quality target (start with S1 door/hall) |

**Mock-up dual-lock rule:** Qwen `/edit` mock-ups use **both** `style-lock-v2` (paint atmosphere) **and** the beat’s mock-up quality target (composition + lighting). S1 door target = fuller wreath · tree peek right · presents at base · dramatic rim light on frame.

**Quality target provenance:** Best-of chops from `S01-approach/v01` — **Klein 9B** · 1536×768 landscape dial · Dial D2 · flow-pass **keep** 2026-07-21 (`_INDEX/best-of-mockup-2026-07-21.md`).

### Finals tier (production keepers for the real book)

| Role | Model | Cost | Notes |
|------|--------|------|-------|
| **Primary finals** | Nano Banana Pro `/edit` (`fal-ai/gemini-3-pro-image-preview/edit`) | ~$0.15 | **v10 approach**: style-lock-v2 + **santa-G0-v2** + **boy-narrator-G0** (+ face when slots allow) |
| **Alternate finals** | Pure Krea blend (`krea/v2/medium/…`) | ~$0.03 | Atmospheric / emotional spreads where soft watercolor > character micro-detail |
| **Hero pillars** | GPT Image 2 High 4K | ~$0.40 | **Only** S3 Eyes Met · S12b God Bless (test first; Jon-marked in Flow + `_FLOW-CURRENT`) |

### Finals consistency rule (LOCKED)

Every finals image **must** use:

1. **`style-lock-v2.png`** — style / atmosphere reference  
2. **`santa-G0-v2.png`** — Santa character reference (when Santa is in the beat)  
3. **`boy-narrator-G0.png`** (+ **`boy-narrator-G0-face.png`** when slots allow) — Boy character reference (when the boy is in the beat)

**Both characters are locked** — no drift, no variation. Attach Boy G0 refs alongside Santa G0 v2 on every story generation that includes either figure.

Santa must always match the **open-coat wardrobe lock**: red coat open/unbuttoned · cream striped shirt · brown leather suspenders **over the shirt** · red pants · black boots · white fur trim · relaxed grandfather presence.

Boy must always match the **Boy G0 lock**: oatmeal/taupe holly PJs (visible holly + red berries, red trim, red buttons) · tousled light-brown hair with golden highlights · brown eyes · rosy cheeks.

### Text pages

FLUX.2 LoRA paper @ scale ~**0.35** (retrain on paper-only crops before production scale-up).

---

## 🔒 Locked production workflow rules (2026-07-22)

**Canonical (fleet):** `_core-scripts/shared-profile-content/docs/PICTURE-BOOK-PRODUCTION-RULES.md`

### Current-plate SoT
`Media/generated/mocks/_FLOW-CURRENT.json` — path · status · `decided_by` · `date` · tier flags.  
**Flipbook reads this file only.**

### 1. Three-Panel Comparison Boards — **one board per decision**
Left = Klein 9B · Center = new model · Right = current favorite.  
Save: `Media/generated/mocks/{unit}/_INDEX/{unit}-comparison-{date}.png`  
Retroactive multi-round boards = **ARCHIVE**.

### 2. Full-Book Flipbook PDF
`npm run book:flipbook` → `Output/flipbook-{date}.pdf` from `_FLOW-CURRENT` only.  
Review artifact — **not** Lulu print.

### 3. Verdict Card
Statuses: `keep` · `keep-leaning` · `reject` · `locked` + **`decided_by` + `date`**.

### 4. Where to document (do not spam project-log)
| Artifact | Job |
|----------|-----|
| `Media/generated/mocks/{unit}/vNN/RECIPE.md` | How that version was made (model · refs · seed · prompt notes) |
| `_FLOW-CURRENT.json` | What’s on the page *now* + verdict |
| `{unit}/_INDEX/*-comparison-*.png` | What you compared |
| `.cursor/docs/CONTINUE-HERE.md` · `ReCall.md` | Mid-session resume (“where we left off”) |
| `.cursor/docs/project-log.md` | **Milestones / decisions only** |

**Log to `project-log.md` only when:** a spread is **locked**, a character reference is **promoted**, or a production **phase completes**.  
Model tests and comparison boards do **not** go in `project-log` — they live in RECIPE + `_FLOW-CURRENT` + the board.

### Always-open docs (4)
1. `JON-BOOK-FLOW-v2-FINAL.md`  
2. `MASTER-PRODUCTION-DOCK.md`  
3. `IMAGE-LANE-SYSTEM-v2.md` (this file)  
4. `AGENT-RUNBOOK.md`

**Scripts:** `scripts/book-comparison-board.py` · `scripts/book-flipbook-assemble.py`

---

## ✅ Test Day Results — 2026-07-22

| Decision | Winner |
|----------|--------|
| Style lock atmosphere | Krea blend → `style-lock-v2` (regen v11 with santa-G0-v2) |
| Santa character | **v08** Banana Pro → `santa-G0-v2.png` |
| Dial favorite look | Qwen 2 Pro edit (v06 class) |
| Primary finals | Banana Pro `/edit` + style-lock + santa-G0-v2 (v10 approach) |
| Hero GPT | S3 · S12b only |
| Text paper LoRA | usable @ scale 0.35 |

S4 Banana board (archive): `_INDEX/S04-sit-here-comparison-banana-2026-07-22.png`

---

## 📊 Decision Matrix (LOCKED)

| Decision | Winner |
|---|---|
| Dial model | **Klein 9B** (~$0.01) |
| Mock favorite look | **Qwen 2 Pro /edit** (~$0.08) |
| Style lock | **Krea → style-lock-v2** |
| Santa lock | **santa-G0-v2** (v08 Banana Pro) |
| Primary finals | **Banana Pro /edit + lock + santa-G0-v2** (~$0.15) |
| Alt finals | **Pure Krea** (~$0.03) atmospheric |
| Hero finals | **GPT High 4K** pillars only (~$0.40) |
| Text pages | **FLUX.2 LoRA** @ ~0.35 |

---

## 💰 Budget (updated)

| Path | Notes | ~Total art gen |
|------|-------|----------------|
| Dial-heavy | 30× Klein + style refs | low |
| Finals | ~26× Banana Pro @ $0.15 + 2–4 GPT pillars | ~$4–6 |
| Alt atmospheric | swap some finals to Krea @ $0.03 | lower |

Exact count follows Flow page map + Jon approvals.

---

## Gotchas (2026-07-22 harvest)

| Issue | Rule |
|-------|------|
| **Open top cream / push scene down** | Qwen alone won’t hard-recompose. **Pillow prep** (scene in lower ~⅔ on cream) → Qwen polish. See `ISSUES-RESOLVED.md` · P02-about-spread v02 |
| **Baked title from ref** | If the composition ref has type, expect glyphs → scrub pass or art-only ref |
| **Qwen Pro Edit URL cap** | Max **3** `image_urls` — lock + primary + continuity; extras in prompt + RECIPE note |
| **Double-door contamination** | Never feed a failed split-door plate as lead ref when fixing that failure |

---

## 🔄 Fallback

If Banana Pro fails a beat: Pure Krea + style-lock-v2 + santa-G0-v2 prompt language.  
If Krea fails continuity: Banana Pro `/edit` with G0 + lock (primary path anyway).  
Legacy Nano Banana / Klein-only finals — last resort only.
