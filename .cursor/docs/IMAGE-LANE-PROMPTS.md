# Dual image style lanes (LOCKED 2026-07-15)

**Yes — this works.** Two prompts for two jobs. Don’t mix them.

| Lane | Model(s) | Style prompt | Use for |
|------|----------|--------------|---------|
| **A — Dial / cheap mockups** | Klein 4B (`fal-ai/flux-2/klein/4b` **or** OpenRouter `black-forest-labs/flux.2-klein-4b`) | **Klein mockup append** below | Layout, pose, text-zone probes, fast A/B |
| **B — Finals / look lock** | Gemini 3 Pro Image (OpenRouter) **or** fal `nano-banana-pro/edit` | **Master style block** in `ILLUSTRATION-STYLE.md` | Approved covers/pages, print remakes, character lock |

**Visual north star (both lanes):** locked cover `Media/approved/covers/cover-front.png` (beige-v2 oatmeal holly PJs).  
**Klein style winner proof:** `Media/generated/openrouter-cover-pj-test/klein-dial-D2-sweetspot.png`

---

## Lane A — Klein mockup append (LOCKED = Dial D2)

**Settings (OpenRouter Klein):** `--guidance 4.6 --steps 30`  
**Also OK on fal Klein:** paste the same text block after the scene prompt.

```
KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast,
rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous
but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare.
Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges.
NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated.
```

**Formula:** `[scene / beat]` + **Klein append** + ref image when editing.  
Do **not** replace this with the long Gemini master on Klein (or vice versa).

---

## Lane B — Finals master (unchanged core)

Use full master from `ILLUSTRATION-STYLE.md` + Banana/Gemini `/edit` with style refs + locked cover / Boy G0 / Santa G0.

```
Traditional children's Christmas picture-book illustration, heirloom storybook quality,
heavily painted in rich gouache and soft watercolor …
```

(See `ILLUSTRATION-STYLE.md` for full block + negatives.)

### Spreads (5250×2625) — REQUIRED add-on + negatives

Always append the **SPREAD master add-on** from `ILLUSTRATION-STYLE.md` and include gutter/fold terms in negatives:

```
seamless continuous two-page storybook spread across the full width, one unbroken painted scene through the center, NO fake book gutter, NO vertical fold line, NO center spine shadow, NO page-split seam, NO mockup binding crease down the middle
```

**Negatives (spreads):** `fake book gutter, vertical fold line, center spine shadow, page crease, binding seam, mockup book fold, split-page line, gutter shadow overlay` (+ standard style negatives).

**Why:** Fake center fold is MOCK-only. Print plates must be seamless (Jon 2026-07-20). Playbook: `ISSUES-RESOLVED.md`.

---

## Agent rule

1. If Jon says **dial / Klein / cheap mock** → Lane A only → **Dial D2 append** (locked 2026-07-15 testing). Settings OpenRouter: `--guidance 4.6 --steps 30`. Model: **Klein 4B** (`fal-ai/flux-2/klein/4b` or OpenRouter `flux.2-klein-4b`).  
2. If Jon says **final / Banana / Gemini / print / lock** → Lane B only → **ILLUSTRATION-STYLE master** (never D2 on finals).  
3. If generating a **spread** (`image:fal:spread` / 5250×2625 / wide beat) → add **SPREAD add-on** + gutter negatives. **Never** bake a fake middle spine/fold into art. Orange FOLD in PSD = screen guide only.  
4. Boy wardrobe always oatmeal/taupe + holly (cover lock) on both lanes.  
5. Record lane + model + which prompt block (D2 vs master) in every `RECIPE.md`.
