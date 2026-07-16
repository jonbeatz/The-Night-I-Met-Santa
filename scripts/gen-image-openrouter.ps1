# gen-image-openrouter.ps1 — OpenRouter Image API (text + optional refs)
param(
    [Parameter(Mandatory = $true, Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$PromptParts,
    [string]$OutputPath = '',
    [string]$Model = 'google/gemini-3-pro-image',
    [string]$Resolution = '1K',
    [string]$AspectRatio = '1:1',
    [string[]]$Ref = @(),
    [switch]$Open
)

$Prompt = ($PromptParts -join ' ').Trim()
if (-not $Prompt) {
    Write-Host '[gen-image-openrouter] Usage:' -ForegroundColor Yellow
    Write-Host '  npm run image:or -- "prompt"' -ForegroundColor DarkGray
    Write-Host '  npm run image:or -- -Ref Media/approved/covers/cover-front.png "edit prompt"' -ForegroundColor DarkGray
    exit 1
}

$ErrorActionPreference = 'Stop'
$Root = Split-Path $PSScriptRoot -Parent
$py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
$script = Join-Path $PSScriptRoot 'generate-image-openrouter.py'

$argsList = @('--prompt', $Prompt, '--model', $Model, '--resolution', $Resolution, '--aspect-ratio', $AspectRatio)
if ($OutputPath) { $argsList += @('--output', $OutputPath) }
foreach ($r in $Ref) { $argsList += @('--ref', $r) }

$raw = & $py $script @argsList 2>&1 | Out-String
Write-Host $raw
try {
    $result = ($raw.Trim() | ConvertFrom-Json)
} catch {
    Write-Host '[gen-image-openrouter] ERROR: non-JSON output' -ForegroundColor Red
    exit 1
}
if (-not $result.success) {
    Write-Host "[gen-image-openrouter] ERROR: $($result.error)" -ForegroundColor Red
    exit 1
}
Write-Host "[gen-image-openrouter] Saved: $($result.file_path)" -ForegroundColor Green
Write-Host "  Model: $($result.model)  cost: $($result.cost)  $($result.elapsed_s)s" -ForegroundColor DarkGray
if ($Open -and $result.file_path -and (Test-Path $result.file_path)) {
    Start-Process $result.file_path
}
exit 0
