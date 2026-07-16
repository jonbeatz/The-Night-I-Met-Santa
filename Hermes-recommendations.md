# Hermes Recommendations — The Night I Met Santa

**Date:** 2026-07-15
**Author:** Hermes (jonbeatz profile)
**Purpose:** Honest assessment + prioritized recommendations for the book project.

---

## Overall Assessment

The project is in **strong shape**. The documentation system, approval workflow, and tool pipeline are better than most professional projects. The two-tier approval system alone eliminates the biggest source of confusion from v1–v5 (which version are we on?).

---

## ✅ What's Already Excellent

| Thing | Why It's Good |
|---|---|
| **Two-tier approval system** | `Media/approved/` with Tier A (moodboard) + Tier B (composition locks) = no more version chaos |
| **Character locks** | Jack, Boy G0, Santa G0 all locked with reference sheets — critical for consistency across 15+ pages |
| **Beat gap audit** | `BEAT-GAP-AUDIT.md` knows exactly which 5 beats are MISSING vs THIN — no guessing what to generate next |
| **Font catalog** | 13 OFL-licensed families installed, roles assigned: Cormorant Garamond for body, Cinzel Decorative for titles, Allura for flourishes |
| **`BOOK-PLAYBOOK.md`** | Future-proof master doc — anyone can spin up a new book from this single file |
| **Git + GitHub** | Already pushed to `github.com/jonbeatz/The-Night-I-Met-Santa` — off-machine backup |
| **Image lane lock** | Klein 4B dial → Qwen fallback → Banana /edit finals — proven with real beat-01 evidence |
| **TEXT-OVERLAY-POLICY.md** | Clear rules from Jon's mockup feedback — faces, zones, paint-fade recipe all defined |
| **CONTINUITY-AND-PRINT-FINALS.md** | Two-pass pipeline (Pass A composition lock → Pass B print finals) — smart separation |
| **Model compare evidence** | `Media/generated/model-compare-beat01/` — same prompt through all 3 models, Jon picked winners |

---

## ⚠️ Recommendations — Prioritized

### Priority 1: Rewrite `composite_pages.py` with cloud wash

**Blocks:** Entire book PDF. Nothing ships to Lulu without this.

`composite_pages.py` still uses v5 soft rectangles. The TEXT-OVERLAY-POLICY.md already defines the correct cloud wash recipe:

```python
color = (255, 250, 242)      # Warm white/ivory
opacity = 0.45–0.65           # Semi-transparent
blur = 80–160 px              # Gaussian-like feathered edge
shape = elliptical cloud       # NOT rectangle — organic irregular edge
font = "Cormorant Garamond"   # From FONT-CATALOG.md
```

**Approach:** Write `scripts/book-compositor-v6.py`. Generate ONE sample page. Jon approves. Batch all 15 stanzas.

### Priority 2: Fill the 5 missing + 2 thin beats

**Blocks:** Art completeness. From `BEAT-GAP-AUDIT.md`:

**MISSING:**
| Beat | Scene |
|------|-------|
| 3 | Sneak up on Santa ("what do you say?") |
| 5 | Santa on floor among gifts ("sit over here") |
| 9 | Dash back — Santa gone, child with camera |
| 10 | Search for clues (hat, shoe, hint) |
| 14 | What Santa really wants (the message) |

**THIN:**
| Beat | Scene |
|------|-------|
| 6 | Chat & laugh (needs better two-shot) |
| 8 | Camera idea (child looking up at roof noise) |

**Approach:** Klein 4B dial → Jon picks → Banana /edit finals with style-refs.

### Priority 3: Lock back cover

**Blocks:** Cover wrap PDF. INDEX.md shows `Back cover: (pending)`.

Candidates exist in `Media/approved/style-refs/back/` (A–E + jack-farrell-back.png). Pick one, lock to Tier B `covers/cover-back.png`.

### Priority 4: Commit all docs changes to Git

**Why:** 18 modified files + new docs are uncommitted. If the drive fails, you lose all the overnight work (AGENTS.md update, BEAT-GAP-AUDIT.md, CHARACTER-JACK-FARRELL.md, FONT-CATALOG.md, CONTINUITY-AND-PRINT-FINALS.md, BOOK-PLAYBOOK.md, etc.).

```powershell
cd D:\Hermes\projects\The-Night-I-Met-Santa
git add -A
git commit -m "checkpoint: approval system, character locks, beat audit, playbook"
git push
```

### Priority 5: Create `.recipe.md` sidecars for Tier B locks

**Why:** When you remake approved art at 2625² for print, you need the exact prompt + model + seed to reproduce it. Your INDEX.md says to create these but none exist yet.

Each locked file gets a sidecar like:

```
Media/approved/characters/boy-narrator-G0.recipe.md
---
Model: fal-ai/nano-banana-pro/edit
Resolution: ~1K (dial)
Style refs: style-sneak-02.png, style-spread-06.png
Prompt: "A young boy narrator..."
Seed: (if available)
```

### Priority 6: Add Gemini as a 4th image lane

**Why:** Your AGENTS.md now mentions "Gemini/Banana finals". If you have a Google API key (the Google Workspace skill is already authenticated), Gemini Imagen 3 is exceptional at character consistency across multiple generations — exactly what you need for the 7 remaining beats.

**Cost:** ~$0.02–0.05/image.

**Check if key exists:**
```powershell
grep "GOOGLE_API_KEY\|GEMINI_API_KEY" "D:/Hermes/projects/JonBeatz/.env.local"
```

If present, add to `IMAGE-LANE-PROMPTS.md` as Lane 2B (between Qwen fallback and Banana finals).

### Priority 7: Build `scripts/lulu-preflight.ps1`

**Why:** The print checklist is currently a markdown doc — automate the verification.

**What it should check:**
- [ ] Page count is even (24–40)
- [ ] All page images are 2625×2625 px (300 DPI)
- [ ] Bleed zone: 0.125" accounted for
- [ ] Safety zone: text/faces ≥ 0.5" from trim
- [ ] No critical faces on center fold
- [ ] Interior PDF = single file, odd pages = right
- [ ] Cover PDF = separate wrap file
- [ ] Color mode = sRGB
- [ ] Spine width calculation from page count + paper type
- [ ] Output: pass/fail report

### Priority 8: Build `scripts/book-zip-for-lulu.ps1`

**Why:** Lulu upload needs interior PDF + cover PDF. A one-command script that packages everything into a timestamped zip with a manifest.

```powershell
npm run book:zip    # → Output/The-Night-I-Met-Santa-lulu-2026-07-15.zip
```

### Priority 9: Clean up `Media/generated/` (1.4 GB)

**Why:** 1.4 GB of generated experiments. Before the project ships, trim to essentials:

**Keep:**
- `test-batch-v2/` — style north stars (used as Banana /edit refs)
- `model-compare-beat01/` — lane evidence
- `jack-likeness/` — Jack consistency winners
- `beat-gap-dial-01/` — winners you'll promote
- `test-covers-v3/` — cover candidates

**Archive or delete:**
- `test-batch/` (v1 — superseded by v2/v3)
- `test-batch-v3/` (unless used for reference)
- `openrouter-cover-pj-test/` (experimental — keep winners only)
- `unify-eyes-met-test/` (keep winner, archive rest)

### Priority 10: Consider `ghostscript` for optional text-layer PDF

**Why:** Pillow text is raster (pixels baked into JPEG). That's fine for Lulu print. But if you ever want:
- Selectable/searchable text in the PDF
- eBook/EPUB conversion via Pandoc
- Accessibility (screen readers)

...you'd want a version with real text layers. Ghostscript or `pdfcpu` can add text layers to existing PDFs without re-rendering the artwork.

**Install:** `winget install ghostscript` (if wanted — not required for print).

---

## 🎯 Summary Priority Order

| # | Task | Blocks What | Effort |
|---|---|---|---|
| 1 | Rewrite `composite_pages.py` with cloud wash | Entire book PDF | High |
| 2 | Generate missing 5 beats + 2 thin beats | Art completeness | Medium |
| 3 | Lock back cover | Cover wrap PDF | Low |
| 4 | Commit all docs to Git | Disaster recovery | Low |
| 5 | Create `.recipe.md` sidecars | Print-resolution remakes | Low |
| 6 | Add Gemini image lane | Faster character consistency | Medium |
| 7 | Build `lulu-preflight.ps1` | Upload confidence | Medium |
| 8 | Build `book-zip-for-lulu.ps1` | Upload convenience | Low |
| 9 | Clean up 1.4GB generated folder | Disk space, clarity | Low |
| 10 | Ghostscript text-layer PDF | Accessibility, eBook | Optional |

---

## Timeline Check

| Milestone | Target | Status |
|-----------|--------|--------|
| Art consistency (Jack/Santa faces) | Jul 18–20 | ✅ Characters locked 7/15 |
| Fill missing beats | Jul 18–20 | ⚠️ 5 missing, 2 thin |
| Layout with bleed + cloud wash | Jul 21–23 | ❌ compositor rewrite pending |
| Cover lock + spine build | Jul 21–23 | ⚠️ back cover pending |
| Lulu proof order | Jul 24–25 | ❌ blocked on compositor + cover |
| Gift in hand | Aug 15 | 🎯 On track if compositor ships this week |

---

*Generated by Hermes (jonbeatz profile) — July 15, 2026*
