# gen-image-fal.ps1 — The-Night-I-Met-Santa fal.ai image generation
param(
    [Parameter(Mandatory = $true, Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$PromptParts,
    [string]$OutputPath = '',
    [int]$Width = 0,
    [int]$Height = 0,
    [string]$Model = '',
    [ValidateSet('', 'page', 'spread', 'cover')]
    [string]$Preset = '',
    [switch]$Open
)

$Prompt = ($PromptParts -join ' ').Trim()
if (-not $Prompt) {
    Write-Host '[gen-image-fal] Usage:' -ForegroundColor Yellow
    Write-Host '  npm run image:fal -- "prompt"' -ForegroundColor DarkGray
    Write-Host '  npm run image:fal:page -- "prompt"     # 2625x2625 Lulu bleed page' -ForegroundColor DarkGray
    Write-Host '  npm run image:fal:spread -- "prompt"   # 5250x2625 two-page spread' -ForegroundColor DarkGray
    Write-Host '  npm run image:fal:cover -- "prompt"    # ~2048 draft (upscale later)' -ForegroundColor DarkGray
    exit 1
}

$ErrorActionPreference = 'Stop'
$Root = Split-Path $PSScriptRoot -Parent
$loadEnv = Join-Path $PSScriptRoot 'load-env.ps1'
if (Test-Path $loadEnv) { & $loadEnv -Root $Root | Out-Null }

switch ($Preset) {
    'page'   { if ($Width -le 0) { $Width = 2625 }; if ($Height -le 0) { $Height = 2625 } }
    'spread' { if ($Width -le 0) { $Width = 5250 }; if ($Height -le 0) { $Height = 2625 } }
    'cover'  { if ($Width -le 0) { $Width = 2048 }; if ($Height -le 0) { $Height = 2048 } }
}

$py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
$script = Join-Path $PSScriptRoot 'generate-image-fal.py'
$argsList = @('--prompt', $Prompt)
if ($OutputPath) { $argsList += @('--output', $OutputPath) }
if ($Width -gt 0) { $argsList += @('--width', $Width) }
if ($Height -gt 0) { $argsList += @('--height', $Height) }
if ($Model) { $argsList += @('--model', $Model) }

$raw = & $py $script @argsList 2>&1 | Out-String
$result = $raw.Trim() | ConvertFrom-Json

if (-not $result.success) {
    Write-Host "[gen-image-fal] ERROR: $($result.error)" -ForegroundColor Red
    exit 1
}

Write-Host "[gen-image-fal] Saved: $($result.file_path)" -ForegroundColor Green
Write-Host "  Provider: fal.ai  Model: $($result.model)  $($result.width)x$($result.height)" -ForegroundColor DarkGray

if ($Open -and (Test-Path $result.file_path)) {
    Start-Process $result.file_path
}

exit 0
