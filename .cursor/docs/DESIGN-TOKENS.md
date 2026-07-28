# DESIGN-TOKENS.md — \"The Night I Met Santa\"

**Purpose:** Single source of truth for all visual decisions in the book. Every Hermes review, Cursor generation, and Banana Pro finals pass checks against these tokens.

**Last updated:** 2026-07-25
**Status:** LOCKED — do not change without Jon approval

---

## Colors

### Wall & Room
| Token | Hex | Usage |
|-------|-----|-------|
| `--wall-burgundy` | `#4A0E17` | Primary wall color — every interior scene |
| `--wall-burgundy-shadow` | `#2D080F` | Dark corners, shadow areas |
| `--wall-burgundy-light` | `#6B1623` | Firelight hitting walls |

### Santa
| Token | Hex | Usage |
|-------|-----|-------|
| `--santa-coat` | `#CC2936` | Open red coat |
| `--santa-coat-trim` | `#F5F0E8` | White fur trim on coat |
| `--santa-shirt` | `#F5F0E8` | Cream striped shirt underneath |
| `--santa-suspenders` | `#5C3A1E` | Brown leather suspenders |
| `--santa-pants` | `#CC2936` | Red pants |
| `--santa-boots` | `#1A1A1A` | Black boots |

### Boy (Narrator)
| Token | Hex | Usage |
|-------|-----|-------|
| `--boy-pjs-base` | `#D4C5A9` | Oatmeal/taupe holly pajamas |
| `--boy-pjs-trim` | `#CC2936` | Red trim on collar, cuffs, hem |
| `--boy-pjs-holly` | `#2E5E2E` | Green holly leaves on PJs |
| `--boy-pjs-berries` | `#CC2936` | Red holly berries on PJs |
| `--boy-pjs-buttons` | `#CC2936` | Red buttons |

### Christmas Elements
| Token | Hex | Usage |
|-------|-----|-------|
| `--tree-green` | `#2E5E2E` | Christmas tree, evergreen foliage |
| `--firelight` | `#F4A236` | Fireplace glow, warm ambient |
| `--firelight-ember` | `#D4781A` | Dying embers |
| `--gold-light` | `#FFD700` | Tree lights, candle glow |
| `--moonlight` | `#C8D6E5` | Moonlight beams through window |
| `--moonlight-cool` | `#8EAEC4` | Cool moonlight on snow |
| `--sky-night` | `#1A2744` | Deep blue night sky |
| `--sky-night-light` | `#2E4073` | Lighter sky near horizon |
| `--star-gold` | `#FFE57F` | North Star gleam |
| `--star-white` | `#FFFFFF` | General stars |
| `--snow` | `#F0F4F8` | Snow on ground, rooftops |
| `--snow-shadow` | `#C8D6E5` | Moonlight shadows on snow |
| `--gift-red` | `#CC2936` | Red gift wrapping |
| `--gift-green` | `#2E5E2E` | Green gift wrapping |
| `--gift-gold` | `#FFD700` | Gold ribbon/bow |
| `--rug-warm` | `#8B6914` | Patterned rug base |
| `--rug-accent` | `#A0522D` | Rug accent color |
| `--wood-floor` | `#6B4226` | Hardwood floor |
| `--fireplace-stone` | `#8B8682` | Fireplace stone/brick |
| `--mantel-wood` | `#5C3A1E` | Wooden mantel |

### Text & Background
| Token | Hex | Usage |
|-------|-----|-------|
| `--page-cream` | `#FDFBF7` | Standard cream page background |
| `--text-primary` | `#1A1A1A` | Body text color |
| `--text-light` | `#FFFFFF` | Text on dark backgrounds |
| `--vignette-edge` | `#FDFBF7` | Vignette dissolve color (matches cream) |

---

## Typography

| Role | Font | Weight | Notes |
|------|------|--------|-------|
| **Title page** | Cinzel Decorative | 36pt+ | Title and cover only |
| **Poem body** | Cormorant Garamond | Regular | All poem text on pages |
| **Thank You** | Cormorant Garamond | Regular | Match poem body |
| **"God bless."** | Cormorant Garamond | Bold | Standalone on S12 right page |
| **Draft note** | Cormorant Garamond Italic | Italic | Only Draft quote text |
| **Page numbers** | Cormorant Garamond | Regular | Small, subtle, bottom corners |

---

## Spacing & Dimensions

| Spec | Value | Notes |
|------|-------|-------|
| **Trim size** | 8.5 × 8.5 inches | Square format |
| **Bleed** | 0.125 inches | All sides |
| **Safe zone** | 0.5 inches | From trim edge — no critical content |
| **Gutter** | 0.25 inches | Center fold — no faces or important elements |
| **Text margin (top)** | 1.0 inch | From top trim |
| **Text margin (bottom)** | 1.0 inch | From bottom trim |
| **Text margin (sides)** | 1.25 inches | From side trim (wider for binding) |
| **Single page resolution** | 2625 × 2625 px | 300 DPI |
| **Spread resolution** | 5250 × 2625 px | 300 DPI |
| **Cover resolution** | 2625 × 2625 px | Front only (spine + back separate) |

---

## Image Rules

| Rule | Applies To |
|------|-----------|
| Santa: open red coat, cream striped shirt visible, brown suspenders OVER shirt | All Santa appearances |
| Boy: oatmeal/taupe holly PJs, green holly with red berries, red trim on collar/cuffs/hem, red buttons | All boy appearances |
| Burgundy walls in every interior scene | S1–S11 |
| Santa G0 v2 face: warm smile, laugh lines, rosy cheeks, grandfatherly | All Santa close-ups |
| Boy G0 face: 5-7 years old, defined features, NOT toddler | All boy close-ups |
| Standard watercolor vignette on all single pages | P01, text pages, quiet close pages |
| No baked text in any image | ALL pages |
| No faces or key elements crossing the gutter | All spreads |
| Santa on RIGHT side of room (near tree) | S2, S3, S4, S5 |
| Frame treatment: soft dissolve to cream on ALL sides (not one-sided) | All singles/text pages |
| Rich oil-painting quality matching S3 v07 | Quality bar for ALL images |
| NO skylights | All interior scenes |
| NO phones or modern devices | Era-neutral (vintage camera only) |
| Fireplace: dying embers when Santa has left, active fire when Santa present | Per beat |

---

## Model & Pipeline

| Stage | Model | Resolution | Notes |
|-------|-------|-----------|-------|
| **Mock dial** | Qwen 2 Pro Edit v06 | 2625² / 5250×2625 | Composition lock |
| **Finals** | Nano Banana Pro /edit | 2625² / 5250×2625 | Style-lock + character refs |
| **Upscale** | SeedVR ×2 | Target resolution | When source is sub-2625 |
| **Frame** | Pillow | N/A | Vignette dissolve (not regen) |

---

## Frame Treatment Policy

| Page Type | Frame | How Applied |
|-----------|-------|-------------|
| Full spreads | Optional — frame deferred to finals | Pillow or Banana native |
| Single pages | MANDATORY — standard watercolor vignette | Pillow, not regen |
| Text pages | MANDATORY — standard watercolor vignette | Pillow, not regen |
| Cover | MANDATORY — front/back/spine have own treatments | Per cover spec |
