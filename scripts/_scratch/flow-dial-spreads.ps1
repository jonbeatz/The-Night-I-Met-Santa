# flow-dial-spreads.ps1 — Lane A1 Klein 9B landscape dials from MASTER-PRODUCTION-DOCK
$ErrorActionPreference = 'Stop'
$Root = 'D:\Hermes\projects\The-Night-I-Met-Santa'
$gen = Join-Path $Root 'scripts\gen-image-fal.ps1'

$D2 = 'KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated.'

$Spread = 'ONE continuous unbroken painted scene across the full width — same room, same moment, same lighting, like one wide painting with a fold in the middle, NOT two separate images. Seamless through the center: NO fake book gutter, NO vertical fold line, NO center spine shadow, NO page-split seam. Keep faces and critical props (eyes, hands, mug, note, camera) AWAY from the exact center fold — center band is background only (floor, wall, tree, gifts). WATERCOLOR FRAME OFF: full-bleed to all edges, NO white vignette, NO cream paper margin. No text, no letters, no watermark, no readable handwriting.'

$jobs = @(
  @{
    unit = 'S02-threshold'; slug = 'threshold'; pages = '8|9'
    script = 'L: entered room / amazement shock · R: calm / sneak up on Santa'
    zone = 'Upper outer left · lower outer right'
    scene = 'Wide cinematic Christmas living-room spread from the doorway: child peeking in from the threshold (back and shoulder toward viewer), living room opens into a sea of gifts ribbons and tree glow; farther in, Santa Claus only half-seen — red coat, boots, brilliant white beard edge among boxes — not a full face-to-face portrait yet, comedy of almost getting caught, hush and wonder. Leave quiet outer bands for later text.'
  },
  @{
    unit = 'S04-sit-here'; slug = 'sit-here'; pages = '12|13'
    script = 'L: floor gifts / stayed still · R: Sit over here / moment to kill'
    zone = 'Outer left wall · side panel for whisper'
    scene = 'Wide cinematic Christmas gift-room spread, low camera among wrapping paper: Santa Claus sitting on the floor between boxes gifts and ribbons galore, kind face, red coat with suspenders visible; nearby a child in oatmeal holly pajamas frozen mid-step in awe; RIGHT continues as Santa gently gesturing to an open spot beside him inviting the child to sit, cozy tree and fireplace glow. Leave quiet side areas for later dialogue text. Not a stiff standing portrait.'
  },
  @{
    unit = 'S05-chat'; slug = 'chat'; pages = '14|15'
    script = 'L: thrill / chatted laughed · R: laughs stories chatter'
    zone = 'Bottom band · bottom outer right'
    scene = 'Wide cozy Christmas spread: Santa and child sitting together on the living room floor among gifts, laughing warmly with animated friendly gestures, storytelling hands, tree lights and soft fireplace glow, intimate heirloom mood, figures seated not standing. Leave quiet bottom band for later text.'
  },
  @{
    unit = 'S06-cocoa'; slug = 'cocoa'; pages = '16|17'
    script = 'L: places people things / toys music rings · R: wool silk / cocoa not milk'
    zone = 'Upper left · outer right'
    scene = 'Wide cinematic Christmas storytelling spread: hero prop is a steaming mug of hot cocoa in Santa''s hands, soft steam catching firelight; Santa mid-tale with storytelling gesture; nearby child listening in pajamas; background softly suggests toys music and gift sparkle without cluttering faces; cozy lantern and hearth glow. Leave quiet upper areas for later text. Mug and steam read clearly. Not a standing lineup.'
  },
  @{
    unit = 'S07-proof'; slug = 'proof'; pages = '18|19'
    script = 'L: roof noise / needed proof · R: photo best bet'
    zone = 'Bottom left · bottom right'
    scene = 'Wide Christmas living-room spread: child looking sharply upward toward the ceiling as if hearing reindeer noise on the roof, startled playful urgency; continuous scene shows a plan forming — a simple classic camera resting nearby as the idea for proof (era-neutral camera body, NOT a modern phone UI, no glowing screen icons), warm interior light, Santa may be partly visible or already shifting away. Leave quiet bottom bands for later text. Dynamic look-up pose, not a static standing portrait.'
  },
  @{
    unit = 'S08-gone'; slug = 'gone'; pages = '20|21'
    script = 'L: flew out / hour passed · R: roof noise / still without proof'
    zone = 'Upper left · upper right'
    scene = 'Wide Christmas living-room spread of absence: empty spot among gifts where Santa sat, wrapping paper still, tree glowing; child rushing back holding a camera, disappointment and urgency, door still ajar behind, suggestion of noise from the roof by the child''s upward glance. No Santa figure present. Leave quiet upper areas for later text. Emphasize empty space and motion — not a posed duo.'
  },
  @{
    unit = 'S09-search'; slug = 'search'; pages = '22|23'
    script = 'L: clue tip hat shoe · R: flue empty / something on chair'
    zone = 'Outer left · corner near chair'
    scene = 'Wide Christmas mystery spread: LEFT — child searching the living room on hands and knees among ribbons and gifts, curious worried expression; RIGHT — continuous, dark empty chimney flue with child looking up into blackness, then composition leads the eye to an old wooden chair with something small resting on the seat (folded note shape, no readable writing). Soft dying fire and moonlight. Leave quiet corners for later text. Search energy, not standing portrait.'
  },
  @{
    unit = 'S10-note'; slug = 'note'; pages = '24|25'
    script = 'L: left me a note / stare · R: tore open note / one thing to mention'
    zone = 'Outer left · outer right'
    scene = 'Wide cinematic climax spread: child on or beside an old wooden chair discovering a small folded note from Santa, wonder and disbelief; continuous RIGHT — close intimate focus on child''s hands carefully tearing open the blank cream note paper (no readable writing, no letters), warm tree glow soft in background. Leave quiet outer edges for later text. Hands and note are the heroes.'
  },
  @{
    unit = 'S11-wish'; slug = 'wish'; pages = '26|27'
    script = 'L: cakes cocoa milk / silk coats · R: simply a note'
    zone = 'Top left · top outer'
    scene = 'Wide heartfelt Christmas spread: soft painted still-life suggestions of cocoa cake silk stockings and coats as gentle background memory (blurred, not photoreal product shots); focus on child holding Santa''s open note paper glowing softly in tree light (no readable letters), peaceful revelation mood, cozy heirloom atmosphere. Leave quiet top areas for later text. Emotional quiet, not standing cast shot.'
  },
  @{
    unit = 'S12-blessing'; slug = 'blessing'; pages = '28|29'
    script = 'L: eggnog belt favor · R: love Christmas / God bless'
    zone = 'Side bands · favor / God bless band'
    scene = 'Wide heartfelt closing Christmas spread: warm living room after Santa''s visit, empty chair with a small open note nearby, soft snow light at the window, tree and fireplace still glowing, child quietly holding the note near the tree with wonder and love (not a stiff posed portrait with Santa), deep heirloom Golden Age feeling. Leave quiet bands for later blessing text. Seamless painted scene. No readable writing on the note.'
  }
)

foreach ($j in $jobs) {
  $dir = Join-Path $Root "Media\generated\mocks\$($j.unit)\v01"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $out = Join-Path $dir 'art.png'
  $prompt = "$($j.scene) $D2 $Spread"
  Write-Host "`n=== $($j.unit) ===" -ForegroundColor Cyan
  & $gen -Model 'fal-ai/flux-2/klein/9b' -Width 1536 -Height 768 -OutputPath $out $prompt
  if ($LASTEXITCODE -ne 0) { throw "Failed $($j.unit)" }

  $recipe = @"
# RECIPE — $($j.unit) / v01

| Field | Value |
|-------|--------|
| **name** | $($j.slug) — Primary flow dial (continuous spread) |
| **unit** | $($j.unit) |
| **book page** | $($j.pages) · $($j.slug) · SPREAD |
| **page role** | ``spread`` |
| **spread side** | ``wide-master`` |
| **version** | v01 |
| **date** | 2026-07-21 |
| **lane** | A1 dial (Klein 9B) |
| **service** | fal.ai |
| **model** | ``fal-ai/flux-2/klein/9b`` |
| **settings** | 1536×768 landscape dial · T2I · continuous scene · faces off-center |
| **FRAME** | OFF |
| **concept** | Full-book flow pass — Primary from MASTER-PRODUCTION-DOCK · one wide painting |
| **changes** | First dial for this unit |
| **size** | 1536×768 |
| **seed** | n/a |
| **request_id** | n/a |
| **cost_note** | ~`$0.01 dial |
| **output** | art.png |
| **script_text** | $($j.script) |
| **type_zone** | $($j.zone) |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a (T2I this take)
- santa: n/a (T2I this take)
- jack: n/a
- style / frame: Dial D2 + continuous spread add-on · FRAME OFF
- base / edit source: n/a

## Prompt

$($j.scene)

$D2

$Spread

## Negative / constraints

- FRAME OFF · full bleed
- One continuous scene · no fake gutter · no center spine
- Faces/critical props off exact center fold
- No text / no letters / no watermark / no readable handwriting

## Notes

Flow pass after S1 keep. Jon reviews batch.
"@
  Set-Content -Path (Join-Path $dir 'RECIPE.md') -Value $recipe -Encoding UTF8
}

Write-Host "`nALL SPREADS DONE" -ForegroundColor Green
