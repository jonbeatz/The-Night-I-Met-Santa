# RESEARCH-VERDICT.md — Deep research (Cursor session 2026-07-14)

> **2026-07-20 update:** Lulu **8.5×8.5"** casewrap still locked. **Layout primary is now InDesign UXP** (`AGENT-RUNBOOK.md`) — Pillow→Typst below is **historical / fallback only**. Living ops: `BOOK-PRODUCTION-SYSTEM.md` · `PAGE-BUILD-WORKFLOW.md`.

Source: Deep Firecrawl/Tavily + GitHub review before the project move.  
**Use this for early POD research.** Prefer runbook + production system when layout claims conflict.

---

## Locked decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Trim | **8.5×8.5"** | Matches art + kids’ picture-book feel |
| Gift book | **1 hardcover** now; more later if wanted | Birthday Aug 15 |
| Printer | **Lulu** casewrap HC | Real 8.5×8.5, 1-copy OK, ships to Dad |
| Backup printers | **Mixam** (8.5×8.5) · **Blurb** (often 7×7 — resize) | Quality backups |
| Avoid for this size | **Amazon KDP hardcover** | No 8.5×8.5 HC |
| Layout primary | **Pillow cloud pre-composite** → flat JPEG → Typst front matter | Agent-friendly; matches Jon’s overlay refs; avoids Typst alpha bugs |
| Layout optional upgrade | **Affinity Publisher** (~$70–80 one-time) | Best manual control for spreads/PDF/X if Jon wants GUI |
| LaTeX | **Not primary** | Fine for academic books; wrong tool for full-bleed picture book under deadline |

---

## Print services (1 copy, square HC gift)

| Service | 8.5×8.5 HC? | ~1-copy | Use? |
|---------|-------------|---------|------|
| **Lulu** | Yes | ~$25–40 + ship (verify calculator) | **Primary** |
| **Mixam** | Yes | ~$45–50 similar quote | Strong backup |
| **Blurb** | Usually 7×7 | ~$32–50 | Premium paper if resize OK |
| IngramSpark | Maybe | Author-copy model | Overkill for 1 gift |
| BookBaby | Varies | Higher / slower | Timing risk |
| **KDP** | HC square **no** | Cheap PB only | **Skip for gift HC** |
| Shutterfly / Walmart | ~8×8 photo books | Cheap/fast | Fallback only |
| PrintNinja | Custom | Min ~100+ | Later bulk only |

### POD specs (all printers)

- Bleed **0.125"** beyond trim  
- Safety **~0.25–0.375"** inside trim for text/faces  
- Images **300 DPI** (covers OK to 600)  
- Color: **sRGB** preferred (Lulu Oct 2024 — not CMYK); PDF single-page  
- Files: separate **interior PDF** + **cover PDF** (spine from page count + paper)  
- Page count: **even**  

**Order proof by ~July 25–28** for Aug 15 buffer.

---

## GitHub links graded (Jon pasted)

| Repo | Grade | Verdict | Use for dad book? |
|------|-------|---------|-------------------|
| [egeerardyn/awesome-LaTeX](https://github.com/egeerardyn/awesome-LaTeX) | A / 92 | **WATCH** | Reference only if ever doing LaTeX |
| [dspinellis/latex-advice](https://github.com/dspinellis/latex-advice) | A- / 90 | **WATCH** | Steal git/latexmk habits; not picture-book layout |
| [latexers/awesome-LaTeX](https://github.com/latexers/awesome-LaTeX) | D / 35 | **SKIP** | Stub / dead links |
| [ndpvt-web/latex-document-skill](https://github.com/ndpvt-web/latex-document-skill) | A- / 88 | **WATCH** | Optional Claude LaTeX skill later — **not** kids spread template |

---

## Toolchain

### Use now (Hermes)

| Tool | Role |
|------|------|
| `image:fal` / fal MCP | Final stills; **nano-banana-pro** for character lock |
| `image:gen` | Cheap drafts |
| ComfyUI (when asked) | Inpaint / upscale / style lock |
| Image-Workflow + Background-Removal | Cutouts / composites |
| `composite_pages.py` | **Rewrite** for cloud wash (next build) |
| `book-final.typ` | Front matter + place page JPEGs |
| `build_cover_v2.py` | Wrap covers |

### Optional later

| Tool | When |
|------|------|
| Affinity Publisher | If cloud Pillow still isn’t pretty enough |
| Scribus | Free Affinity substitute |
| MikTeX / latex-document-skill | Only if committing to LaTeX (not recommended) |
| InDesign | Only if already paying CC |
| Blurb BookWright | Only if switching to Blurb sizes |

### Hermes skill gaps (add as we go)

1. Picture-book spread map  
2. Print bleed/spine checklist → started in BOOK-PLAN  
3. Character style-lock recipe (fal + Jack refs)  
4. Lulu upload runbook  
5. Optional LaTeX kids starter — **skip unless requested**

---

## August timeline

| By | Do |
|----|-----|
| Jul 18–20 | Lock art consistency (Jack/Santa faces) |
| Jul 21–23 | Layout with bleed + Lulu spine cover |
| Jul 24–25 | Upload Lulu · order proof (or gift if time tight) |
| Aug 1–8 | Arrive / express reprint only if needed |
| **Aug 15** | Gift in hand |

---

## Recommended fork (decided)

**Do this:** Lulu + Pillow cloud composite (+ Typst binder)  
**Not this:** LaTeX Phase 4 as primary · Affinity-first (unless Jon buys Affinity and prefers GUI) · KDP for the square hardcover gift  

Affinity remains a fine “polish pass” tool later; it is not required to start.
