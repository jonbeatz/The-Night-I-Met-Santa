# gen-image.ps1 — The-Night-I-Met-Santa Hugging Face FLUX image generation
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
    Write-Host '[gen-image] Usage: npm run image:gen -- "prompt"' -ForegroundColor Yellow
    Write-Host '  npm run image:gen:page -- "prompt"   # 2625x2625' -ForegroundColor DarkGray
    Write-Host '  npm run image:gen:spread -- "prompt" # 5250x2625' -ForegroundColor DarkGray
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
$script = Join-Path $PSScriptRoot 'generate-image.py'
$argsList = @('--prompt', $Prompt)
if ($OutputPath) { $argsList += @('--output', $OutputPath) }
if ($Width -gt 0) { $argsList += @('--width', $Width) }
if ($Height -gt 0) { $argsList += @('--height', $Height) }
if ($Model) { $argsList += @('--model', $Model) }

$raw = & $py $script @argsList 2>&1 | Out-String
$result = $raw.Trim() | ConvertFrom-Json

if (-not $result.success) {
    Write-Host "[gen-image] ERROR: $($result.error)" -ForegroundColor Red
    exit 1
}

Write-Host "[gen-image] Saved: $($result.file_path)" -ForegroundColor Green
Write-Host "  Model: $($result.model)  $($result.width)x$($result.height)" -ForegroundColor DarkGray

if ($Open -and (Test-Path $result.file_path)) {
    Start-Process $result.file_path
}

exit 0
