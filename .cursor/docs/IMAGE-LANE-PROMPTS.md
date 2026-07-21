# Image lanes + watercolor frame (LOCKED)

**Dual style prompts for dual jobs — don’t mix them.**  
**Frame is a toggle** — default ON for matter/title vignettes; OFF for full-bleed print plates when Jon asks.

### Provider priority (Jon 2026-07-21)

| # | Provider | Role |
|---|----------|------|
| **1** | **fal.ai** | **First choice** for all image lanes (dial + finals). Best endpoint coverage (Klein 9B/4B, Qwen, Gemini edit @ 2K). |
| **2** | **OpenRouter** | **Second** — when fal is down, key missing, or Jon asks. Overlap is strongest on **Gemini image** (+ Klein **4B**). Not a full mirror of fal’s catalog. |
| **3** | TBD | Only if fal + OpenRouter both unavailable (local/HF later — decide then). |

Credits snapshot (operator 2026-07-21): **fal ~$15.99** · **OpenRouter ~$15.69** · DeepSeek ~$20 topped (LLM stack, not image lanes).

### Model priority (Jon 2026-07-21)

| Priority | Lane | Model | ~Cost (dial ~1K) | Use for |
|:--------:|------|--------|----------------:|---------|
| **1** | **A1 — Dial primary** | Klein **9B** · fal `flux-2/klein/9b` *(edit: `…/9b/edit`)* | **~$0.011** | **Default mockup / testing** — best dial for the penny |
| **2** | **A2 — Dial alt** | fal `qwen-image-2/text-to-image` *(edit: `…/edit`)* | **~$0.035** | Second opinion / alt compare against A1 |
| **3** | **A3 — Dial light** | Klein **4B** · fal `flux-2/klein/4b` | **~$0.009** | Only when **hi-res batch**, rough layout, or **low-detail** (not a detailed type/comp dial) |
| **4** | **B — Finals** | fal `gemini-3-pro-image-preview/edit` *(Nano Banana Pro)* · fallback OpenRouter `google/gemini-3-pro-image` | **~$0.14–0.15** | **Production-ready** keepers / print / character lock |

**Style prompts:** A1 + A3 → **Klein Dial D2**. A2 → short master OK. **B** → **ILLUSTRATION-STYLE master** + optional **FRAME ON/OFF**.

**Same models?** Same *family* when both list it (Gemini image, Klein 4B). **Not identical menus:** Klein **9B** + Qwen Image 2 edit/T2I are **fal-first** in our stack; OpenRouter is mainly the Gemini (and Klein 4B) backup. Pricing units can differ (fal $/MP or $/img vs OpenRouter token or $/MP schemes).

**Speed?** Neither is always faster. fal = direct image queue (usually snappier for our edit workflows). OpenRouter = extra hop + may route Gemini to Vertex vs AI Studio (latency can swing a lot). Prefer fal for day-to-day; OpenRouter when fal fails.

**Visual north stars:** locked cover `Media/approved/covers/cover-front.png` (beige-v2).  
**Klein D2 proof:** `Media/approved/style-refs/covers/klein-mockup-style-LOCKED-D2.png`  
**Watercolor frame refs (Jon 2026-07-21):** `Images/styles2/` — see § Frame below.

**npm shortcuts:**
```powershell
npm run image:fal:klein9 -- "scene prompt…"   # A1 default dial (fal)
npm run image:fal:klein4 -- "scene prompt…"   # A3 light only (fal)
npm run image:or -- "scene prompt…"           # OpenRouter Gemini finals (backup)
```

---

## Lane A — Klein Dial D2 append (9B primary · 4B light only)

**Settings (OpenRouter Klein 4B):** `--guidance 4.6 --steps 30`  
**fal Klein 9B/4B:** paste the same text block after the scene prompt (fal caps steps lower — OK).

```
KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast,
rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous
but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare.
Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges.
NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated.
```

**Formula:** `[scene / beat]` + **Dial D2** + optional **FRAME ON** + ref image when editing.  
Do **not** put the long Gemini master on Klein (or D2 on Banana/Gemini).

| Pick | Endpoint | Notes |
|------|----------|--------|
| **Default dial** | `fal-ai/flux-2/klein/9b` | Primary mockup (~1.1¢/MP) |
| Default dial edit | `fal-ai/flux-2/klein/9b/edit` | Style/layout edits from a ref |
| Alt compare | `fal-ai/qwen-image-2/text-to-image` | ~3.5¢/img — second test |
| Light / batch | `fal-ai/flux-2/klein/4b` | ~0.9¢/MP — hi-res volume or low-detail only |

---

## Lane B — Finals master (Gemini / Banana Pro)

Use full master from `ILLUSTRATION-STYLE.md` + Gemini/Banana `/edit` with style refs + locked cover / Boy G0 / Santa G0.

**This is the production-ready lane** — not for cheap dials. Use after Jon likes an A1/A2 composition.

**Plus frame toggle** (§ below) — record `FRAME: ON` or `FRAME: OFF` in every `RECIPE.md`.

### Spreads (5250×2625) — REQUIRED add-on + negatives

Always append the **SPREAD master add-on** from `ILLUSTRATION-STYLE.md` and include gutter/fold terms in negatives when the plate must be **seamless full-bleed**.

If **FRAME ON** for a wide spread vignette (rare — usually matter/title), still say **no fake book gutter** unless Jon wants a mock binding crease for presentation only.

---

## Watercolor frame (toggle)

### North-star refs — `Images/styles2/`

| File | Why |
|------|-----|
| `spread-Frame-Style1.png` | Wide vignette + soft cream bleed (spread frame look Jon likes) |
| `p21-beat12-13-note-LEFT.png` | Soft top/bottom watercolor paper bleed · fireplace scene |
| `p08-beat02-the-door.png` | Irregular painted edge · door beat |
| `jack-farrell-style-match-B.png` | Full soft vignette around portrait |
| `07-qwen-image-2.png` | Peek doorway + watercolor frame |

### Default policy

| Page type | Default |
|-----------|---------|
| P01 title / dedication / about / quiet matter | **FRAME ON** |
| Story spreads for **Lulu print** (seamless bleed) | **FRAME OFF** (full-bleed) unless Jon asks for vignette comps |
| Dial mocks exploring layout | Match the brief — ask if unclear |

Operator phrases:
- **“with frame” / “watercolor frame” / “vignette”** → FRAME ON  
- **“full bleed” / “no frame” / “edge to edge”** → FRAME OFF  

### FRAME ON — append (copy-paste)

```
WATERCOLOR FRAME ON: soft irregular white/cream watercolor paper vignette around the scene —
feathered painted edges bleeding into open paper, hand-painted storybook plate (not a hard
rectangle crop, not full-bleed edge-to-edge). Match the soft frame aesthetic of our styles2
refs (spread-Frame-Style1 / p21 / door vignettes). Leave calm open paper where needed for
later typography. No hard photo border, no fake Polaroid frame.
```

### FRAME OFF — append (copy-paste)

```
WATERCOLOR FRAME OFF: full-bleed illustration to all edges of the canvas — continuous painted
scene, NO white paper vignette, NO feathered blank margin, NO floating plate on cream paper.
```

### Negatives when FRAME ON

```
full-bleed edge-to-edge photo crop, hard rectangular border, Polaroid frame, UI chrome,
perfect geometric matte, flat vector frame
```

### Negatives when FRAME OFF

```
white vignette, cream paper margin, floating illustration on blank page, watercolor frame border,
feathered blank edges, postcard matte
```

---

## Agent rule

1. **Provider:** **fal.ai first** · **OpenRouter second** (if fal down / Jon asks).  
2. **dial / mockup / testing** → Lane **A1 (Klein 9B)** + **Dial D2** by default.  
3. **alt / second opinion** → Lane **A2 (Qwen)** once to compare — don’t burn finals budget.  
4. **hi-res volume / rough / low-detail** → Lane **A3 (Klein 4B)** only.  
5. **final / Banana / Gemini / print / lock** → Lane **B** + master (never D2) — prefer fal Gemini edit; OpenRouter Gemini if fal unavailable.  
6. **with frame / vignette** → append **FRAME ON**; **full bleed / no frame** → **FRAME OFF**. Default matter/title = ON; print story spreads = OFF.  
7. Every **seamless print spread** → SPREAD add-on + gutter negatives. Orange FOLD in PSD = screen guide only.  
8. Boy wardrobe always oatmeal/taupe + holly (cover lock).  
9. Record in `RECIPE.md`: lane (**A1/A2/A3/B**) · **service (fal|openrouter)** · model id · D2 vs master · **FRAME ON/OFF** · styles2 refs if used · **full Prompt** · seed · script_text/type_zone. Use `Media/generated/mocks/_RECIPE-TEMPLATE.md` (complete form — PAGE-BUILD §6).
