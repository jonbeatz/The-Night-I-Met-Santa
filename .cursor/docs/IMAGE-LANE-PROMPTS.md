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

## Lane B — Finals master (unchanged)

Use full master from `ILLUSTRATION-STYLE.md` + Banana/Gemini `/edit` with style refs + locked cover / Boy G0 / Santa G0.

```
Traditional children's Christmas picture-book illustration, heirloom storybook quality,
heavily painted in rich gouache and soft watercolor …
```

(See `ILLUSTRATION-STYLE.md` for full block + negatives.)

---

## Agent rule

1. If Jon says **dial / Klein / cheap mock** → Lane A only.  
2. If Jon says **final / Banana / Gemini / print / lock** → Lane B only.  
3. Boy wardrobe always oatmeal/taupe + holly (cover lock) on both lanes.
