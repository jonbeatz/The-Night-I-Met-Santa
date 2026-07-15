# image-doctor.ps1 — The-Night-I-Met-Santa image workflow health check
param([switch]$Quiet)

$ErrorActionPreference = 'Continue'
$Tag = '[Santa Book Image Doctor]'
$Root = Split-Path $PSScriptRoot -Parent
$loadEnv = Join-Path $PSScriptRoot 'load-env.ps1'
if (Test-Path $loadEnv) { & $loadEnv -Root $Root | Out-Null }

function Write-Check {
    param([bool]$Ok, [string]$Label, [string]$Detail = '')
    if ($Quiet -and $Ok) { return }
    $color = if ($Ok) { 'Green' } else { 'Yellow' }
    $state = if ($Ok) { 'OK' } else { 'MISSING' }
    $extra = if ($Detail) { " - $Detail" } else { '' }
    Write-Host "  [$state] $Label$extra" -ForegroundColor $color
}

Write-Host ''
Write-Host "$Tag Book print image pipeline..." -ForegroundColor Cyan

$envPath = Join-Path $Root '.env.local'
Write-Check -Ok (Test-Path $envPath) -Label '.env.local' -Detail $(if (Test-Path $envPath) { 'present' } else { 'create from .env.local.example' })

$hfOk = $false
$falOk = $false
if (Test-Path $envPath) {
    $hfLine = Select-String -Path $envPath -Pattern '^HF_TOKEN=' | Select-Object -First 1
    if ($hfLine -and $hfLine.Line -notmatch 'hf_your|example|replace|REPLACE') { $hfOk = $true }
    $falLine = Select-String -Path $envPath -Pattern '^FAL_API_KEY=' | Select-Object -First 1
    if ($falLine -and $falLine.Line -notmatch 'your_|example|replace|REPLACE') { $falOk = $true }
}
Write-Check -Ok $hfOk -Label 'HF_TOKEN' -Detail 'npm run image:gen (drafts)'
Write-Check -Ok $falOk -Label 'FAL_API_KEY' -Detail 'npm run image:fal (paid finals) + fal MCP'

$outDir = if ($env:IMAGE_OUTPUT_DIR) { $env:IMAGE_OUTPUT_DIR } else { Join-Path $Root 'Media\generated' }
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}
Write-Check -Ok (Test-Path $outDir) -Label 'IMAGE_OUTPUT_DIR' -Detail $outDir

$w = if ($env:IMAGE_DEFAULT_WIDTH) { $env:IMAGE_DEFAULT_WIDTH } else { '?' }
$h = if ($env:IMAGE_DEFAULT_HEIGHT) { $env:IMAGE_DEFAULT_HEIGHT } else { '?' }
$pageOk = ($w -eq '2625' -and $h -eq '2625')
Write-Check -Ok $pageOk -Label 'Default size 2625x2625' -Detail "IMAGE_DEFAULT=${w}x${h} (Lulu single page @ 300 DPI w/ bleed)"

$media = Join-Path $Root 'Media'
Write-Check -Ok (Test-Path $media) -Label 'Media/' -Detail $media

$composite = Join-Path $Root 'composite_pages.py'
$bleedOk = $false
if (Test-Path $composite) {
    $bleedOk = [bool](Select-String -Path $composite -Pattern '2625|8\.75' | Select-Object -First 1)
}
Write-Check -Ok $bleedOk -Label 'composite_pages.py bleed size' -Detail $(if ($bleedOk) { '2625/8.75 present' } else { 'still 2550 — rewrite needed' })

Write-Host ''
Write-Host 'Presets:' -ForegroundColor Cyan
Write-Host '  image:fal:page   2625x2625  (one full page + bleed)' -ForegroundColor DarkGray
Write-Host '  image:fal:spread 5250x2625  (two-page spread master)' -ForegroundColor DarkGray
Write-Host '  image:fal:cover  2048x2048  (cover draft; upscale for wrap)' -ForegroundColor DarkGray
Write-Host ''

$ready = $falOk -and (Test-Path $outDir)
if ($ready) {
    Write-Host "$Tag READY for paid fal page/spread generation." -ForegroundColor Green
    exit 0
} else {
    Write-Host "$Tag Fix MISSING items above." -ForegroundColor Yellow
    exit 1
}
