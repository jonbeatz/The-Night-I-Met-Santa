# Text-page LoRA test results

## Verdict (2026-07-22)

**Usable with scale ~0.35 + blank-page prompt.** Scale 1.0 overfits to training *scene content* (fireplace/story art) because train refs were full illustrated pages captioned as "paper only".

| Sample | Scale | Result |
|---|---|---|
| v01, v02 | 1.0 | FAIL — illustrated scenes, not paper |
| v03, v04 | 0.35 | PASS — cream ivory paper + feathered edge wash |

## Paths
- Working: 03-scale035/art.png, 04-scale035/art.png (2625² Lanczos from 2048 native)
- LoRA weights: see lora-weights.json
- Contact: lora-paper-working-v03-v04.png

## Limits
- Endpoint max **2048²** (not native 2625)
- For production: retrain on **paper-only crops** (edge washes / blank margins) so scale 1.0 stays on texture
- Can replace PS cloud PNGs for S4 L / S6 L / S10 L / Thank You L **after** one approved master + seed lock; keep PS for exact hand-tuned clouds if needed
