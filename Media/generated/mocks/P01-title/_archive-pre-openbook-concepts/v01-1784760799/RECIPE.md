# RECIPE — P01-title / v01

| Field | Value |
|-------|--------|
| **unit** | P01-title |
| **book page** | 1 (Title · SINGLE · right) |
| **version** | v01 |
| **date** | 2026-07-20 |
| **lane** | A dial |
| **service** | fal.ai |
| **model** | `fal-ai/flux-2/klein/4b` |
| **settings** | `num_inference_steps` **8** (fal max) · Dial D2 style text · `square_hd` 1024² |
| **prompt block** | Scene + Klein Dial D2 language (not Gemini master) |
| **size** | 1024×1024 dial → Pass B / 2625² later |
| **seed** | **1532280940** |
| **request_id** | `019f81b8-4e09-7a50-ba26-60c578634318` |
| **verdict** | pending Jon review |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a (quiet title vignette)
- santa: n/a
- style: cover mood via prompt only (beige-v2 heirloom feel)

## Prompt

Square storybook illustration, quiet winter holiday living room at night, soft fireplace glow, decorated evergreen tree with warm controlled lights, cozy empty foreground, gentle painted vignette. Large calm open space in the upper center for later typography. Heirloom gouache watercolor feel, rich saturated holiday colors, soft blended edges. No people, no faces, no text, no letters, no glyphs, no watermark. KLEIN STYLE: strong punchy contrast, opaque gouache feel, tree lights warm but CONTROLLED soft bloom, ornaments readable, NOT blown-out glare, NOT washed out, NOT pencil grain.

## Gotchas

- OpenRouter Klein (`flux.2-klein-4b`) returned **Protected Content** moderation on first tries — switched to **fal** Klein successfully.
- fal Klein 4B caps `num_inference_steps` at **8** (OpenRouter Dial D2 used 30 — different provider limits).

## Notes

- Sequential book order: **P01 first**.
- Awaiting Jon: keep / maybe / reject → then Lane B @ 2625² + PSD MOCK (Cinzel title preview).
