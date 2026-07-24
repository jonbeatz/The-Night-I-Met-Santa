# RECIPE — P-author-bio / v01

| Field | Value |
|-------|--------|
| **name** | About the Author — Qwen 2 Pro mockup (portrait + open cream for bio) |
| **unit** | P-author-bio |
| **book page** | 31 · Author (bio mockup test) |
| **page role** | `single` |
| **version** | v01 |
| **date** | 2026-07-23 |
| **lane** | Development mock — **Qwen 2 Pro /edit ONLY** |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² edit → resize 2625² · FRAME ON · no baked text |
| **FRAME** | ON |
| **concept** | Author bio page look-test using locked Jack + style-lock + frame language |
| **changes** | Fresh mock for Jon walk review — does not replace FLOW locked `P-author/art.png` |
| **size** | 2625×2625 |
| **seed** | 1948655301 |
| **output** | art.png · art-MOCK-TYPE.png |
| **script_text** | About the Author · bio Draft · credits (MOCK only) |
| **type_zone** | Lower cream band |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- `Media/approved/characters/jack-farrell-portrait.png` (LOCKED)
- `Media/approved/style-refs/style-lock-v2.png`
- `Media/approved/style-refs/frame-reference.png`

## Prompt

About the Author page art for a children's Christmas picture book (single square plate).

IMAGE 1 = LOCKED Jack Farrell portrait — KEEP his exact face, smile, white swept-back hair,
cream cable-knit sweater, floral armchair, Christmas tree glow, mug on side table.
Do NOT change who he is. Preserve likeness carefully.

IMAGE 2 = style-lock paint atmosphere — rich gouache / soft watercolor heirloom storybook
paint quality (Santore-adjacent). Match this warmth and brush feel.

IMAGE 3 = cream watercolor FRAME language — soft irregular cream vignette dissolving at edges
(FRAME ON), like other matter pages in this book.

COMPOSITION for author BIO page mockup:
- Keep Jack portrait as the clear hero, seated warmly in the Christmas living room.
- Soft cream watercolor paper vignette on ALL sides (feathered painted edges).
- Leave a generous OPEN cream band in the LOWER third (and quiet margins) for later
  typography: page title, short author bio, and small credits — do NOT paint text.
- Calm, intimate, heirloom gift-book mood — not photoreal, not CGI.
- NO letters, NO words, NO watermark, NO logos, NO signature.

Output: square Christmas storybook illustration, FRAME ON, print-ready composition.


## Negative

text, letters, words, About the Author, Written by, watermark, logo, signature, photoreal photo, CGI, 3D render, wrong person, young face, heavy beard, brown age spots, hard rectangle crop, full-bleed edge with no cream vignette, Santa Claus, child in pajamas

## Copy used on MOCK-TYPE (not baked into art.png)

**Title:** About the Author

**Body (BOOK-COPY-DRAFTS About the Author):**
Jack Farrell is a father and grandfather who wrote The Night I Met Santa for the people he loves. His poem has been treasured by his family for years. This first illustrated edition (2026) was made so his words — and Santa's reminder to love Christmas, act like a kid, and keep faith — can stay close at hand every year.

**Credits (Flow p31):**
Written by Jack Farrell.  Design and produced by Jon Farrell  © DigitalStudioz 2026

## Notes

- Flow still lists p31 as portrait-led image page; this mock tests bio+credits overlay look.
- Live type in InDesign later — MOCK is preview only.
- Approved Jack source untouched.

## Follow-up (same session)
- Qwen baked gibberish into lower band despite negatives — cleaned to `art-clean-lower.png` + `art-MOCK-TYPE-clean.png`.
- Best likeness preview: `art-MOCK-TYPE-on-locked-framed.png` (FLOW locked framed plate + Draft bio MOCK type).
- PDF: `Output/P31-author-bio-MOCKUP-v2-2026-07-23.pdf`
