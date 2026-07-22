# backup-and-matter.ps1 — S2/S5/S11 backups + P02/P05/P32/P33 FRAME ON
$ErrorActionPreference = 'Stop'
$Root = 'D:\Hermes\projects\The-Night-I-Met-Santa'
$gen = Join-Path $Root 'scripts\gen-image-fal.ps1'

$PJ = 'Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume. Match boy G0 oatmeal holly PJs.'

$D2 = 'KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated.'

$Spread = 'ONE continuous unbroken painted scene across the full width — same room, same moment, same lighting, like one wide painting with a fold in the middle, NOT two separate images. Seamless through the center: NO fake book gutter, NO vertical fold line, NO center spine shadow. Keep faces and critical props AWAY from the exact center fold — center band is background only (floor, wall, tree, gifts). WATERCOLOR FRAME OFF: full-bleed to all edges. No text, no letters, no watermark.'

$Master = 'Traditional children''s Christmas picture-book illustration, heirloom storybook quality, heavily painted in rich gouache and soft watercolor with visible soft brushstrokes and gentle blended edges, NOT colored pencil NOT crayon NOT scratchy sketch lines, warm fireplace glow mixed with cool moonlight, golden ember highlights, deep crimson and forest green palette with warm cream and muted earth tones, nostalgic Golden Age painted realism, intimate cozy magical atmosphere, Charles Santore–inspired storybook painting, classic Clement C. Moore Christmas book feel, highly detailed but soft and painterly, print-ready composition, no text, no letters, no watermark'

$FrameOn = 'WATERCOLOR FRAME ON: soft irregular white/cream watercolor paper vignette around the scene — feathered painted edges bleeding into open paper, hand-painted storybook plate (not a hard rectangle crop, not full-bleed edge-to-edge). Leave calm open paper where needed for later typography. No hard photo border, no fake Polaroid frame. No people, no Santa, no characters.'

function Write-Recipe($path, $unit, $ver, $name, $pages, $role, $lane, $frame, $size, $script, $zone, $promptBody, $notes) {
  $md = @"
# RECIPE — $unit / $ver

| Field | Value |
|-------|--------|
| **name** | $name |
| **unit** | $unit |
| **book page** | $pages |
| **page role** | ``$role`` |
| **spread side** | $(if ($role -eq 'spread') { '``wide-master``' } else { '``n/a``' }) |
| **version** | $ver |
| **date** | 2026-07-21 |
| **lane** | $lane |
| **service** | fal.ai |
| **model** | ``fal-ai/flux-2/klein/9b`` |
| **settings** | $size |
| **FRAME** | $frame |
| **concept** | $name |
| **changes** | $notes |
| **size** | $size |
| **seed** | n/a |
| **request_id** | n/a |
| **cost_note** | ~`$0.01 dial |
| **output** | art.png |
| **script_text** | $script |
| **type_zone** | $zone |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Prompt

$promptBody

## Notes

$notes
"@
  Set-Content -Path $path -Value $md -Encoding UTF8
}

# --- S2 Backup ---
$s2 = 'Christmas living room spread: child at doorway edge looking into a room filled with gifts, warm tree glow; Santa is partially visible in the background shadows among stacked presents — just his red coat and white beard visible, face turned away. Mystery and wonder — not a reveal yet.'
$p2 = "$s2 $PJ $D2 $Spread"
$out = Join-Path $Root 'Media\generated\mocks\S02-threshold\v02\art.png'
Write-Host "`n=== S02 Backup v02 ===" -ForegroundColor Cyan
& $gen -Model 'fal-ai/flux-2/klein/9b' -Width 1536 -Height 768 -OutputPath $out $p2
Write-Recipe (Join-Path $Root 'Media\generated\mocks\S02-threshold\v02\RECIPE.md') 'S02-threshold' 'v02' 'Threshold Backup — half-seen Santa + holly PJs' '8|9 · S2 · SPREAD' 'spread' 'A1 dial (Klein 9B)' 'OFF' '1536x768' 'enter room / sneak on Santa' 'outer bands' $p2 'Backup after v01 maybe · PJ hard lock'

# --- S5 Backup (Master has no formal Backup — fixed two-shot) ---
$s5 = 'Wide cozy Christmas spread: ONE Santa Claus and ONE child sitting together on the living room floor among gifts, laughing warmly with animated friendly gestures, storytelling hands, tree lights and soft fireplace glow, intimate heirloom mood, figures seated not standing — NOT mirrored, NOT two Santas, NOT phones or modern devices. Leave quiet bottom band for later text.'
$p5 = "$s5 $PJ $D2 $Spread"
$out = Join-Path $Root 'Media\generated\mocks\S05-chat\v02\art.png'
Write-Host "`n=== S05 Backup v02 ===" -ForegroundColor Cyan
& $gen -Model 'fal-ai/flux-2/klein/9b' -Width 1536 -Height 768 -OutputPath $out $p5
Write-Recipe (Join-Path $Root 'Media\generated\mocks\S05-chat\v02\RECIPE.md') 'S05-chat' 'v02' 'Chat Backup — one Santa + child holly PJs' '14|15 · S5 · SPREAD' 'spread' 'A1 dial (Klein 9B)' 'OFF' '1536x768' 'chat & laugh' 'bottom band' $p5 'Backup after twin-Santa miss · PJ hard lock'

# --- S11 Backup ---
$s11 = 'Christmas spread: close warm scene of child sitting by the tree holding Santa''s open note, the paper catching soft golden light; in the background, gentle blurred memories of cocoa, silk, and gifts from the poem — dreamy, not literal. Emotional revelation moment, peaceful and quiet. NO readable letters, NO text, NO handwriting anywhere in the image — blank cream note paper only.'
$p11 = "$s11 $PJ $D2 $Spread"
$out = Join-Path $Root 'Media\generated\mocks\S11-wish\v02\art.png'
Write-Host "`n=== S11 Backup v02 ===" -ForegroundColor Cyan
& $gen -Model 'fal-ai/flux-2/klein/9b' -Width 1536 -Height 768 -OutputPath $out $p11
Write-Recipe (Join-Path $Root 'Media\generated\mocks\S11-wish\v02\RECIPE.md') 'S11-wish' 'v02' 'Wish Backup — blank note + holly PJs' '26|27 · S11 · SPREAD' 'spread' 'A1 dial (Klein 9B)' 'OFF' '1536x768' 'simply a note' 'top quiet' $p11 'Backup after baked letters · PJ + no-text hard lock'

# --- Matter singles FRAME ON ---
$singles = @(
  @{ unit='P02-copyright'; pages='2 · Copyright · SINGLE'; scene='Soft abstract Christmas ornament vignette on warm cream watercolor paper, tiny holly sprig and faint pine shadow only, large open quiet center for later text, no people, no Santa, no readable words, painted gouache storybook'; zone='large open center' ; script='copyright credits' },
  @{ unit='P05-about-vignette'; pages='5 · About vignette · SINGLE'; scene='Snowy nighttime window from inside a cozy living room, frost lace on glass, Christmas tree reflected faintly, empty gift room hush, quiet open wall for breathing room, no people, soft gouache'; zone='open wall / breathe' ; script='About This Story (R)' },
  @{ unit='P32-quiet-close'; pages='32 · Quiet close · SINGLE'; scene='Soft Christmas Eve quiet vignette, empty chair and faint tree glow, snow hush at window, large open cream for later text God bless Merry Christmas, no people, painted gouache'; zone='large open cream' ; script='quiet close / God bless' },
  @{ unit='P33-merry-christmas'; pages='33 · Merry · SINGLE'; scene='Matching Christmas close vignette: soft ornament resting on a mantel, warm gentle glow, peaceful quiet, open cream for last words, no people'; zone='open cream' ; script='Merry Christmas ornament' }
)

foreach ($s in $singles) {
  $prompt = "$($s.scene). $Master. $FrameOn"
  $dir = Join-Path $Root "Media\generated\mocks\$($s.unit)\v01"
  $out = Join-Path $dir 'art.png'
  Write-Host "`n=== $($s.unit) ===" -ForegroundColor Cyan
  & $gen -Model 'fal-ai/flux-2/klein/9b' -Width 1024 -Height 1024 -OutputPath $out $prompt
  Write-Recipe (Join-Path $dir 'RECIPE.md') $s.unit 'v01' "$($s.unit) FRAME ON matter" $s.pages 'single' 'A1 dial (Klein 9B)' 'ON' '1024x1024' $s.script $s.zone $prompt 'Matter dial · no characters · FRAME ON · master style'
}

Write-Host "`nDONE" -ForegroundColor Green
