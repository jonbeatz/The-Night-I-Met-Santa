# TNIMS session start - shared fleet ritual + Photoshop MCP warm (background).
# Keeps Cursor photoshop MCP from starting red when :8766 was never launched.
param(
    [switch]$Full,
    [switch]$WithDeepSeek,
    [switch]$WithNgrok,
    [switch]$SkipMem0,
    [switch]$SkipSkills,
    [switch]$Quiet,
    [switch]$SkipPhotoshop
)

$ErrorActionPreference = 'Continue'
$RepoRoot = Split-Path $PSScriptRoot -Parent
if (-not (Test-Path (Join-Path $RepoRoot 'package.json'))) {
    throw "TNIMS session-start: package.json not found above $PSScriptRoot"
}

$SharedStart = 'D:\Hermes\projects\_core-scripts\shared-profile-content\scripts\session-start.ps1'
$PsMcp = Join-Path $RepoRoot 'tools\layout-mcp\photoshop-adobepy\start-photoshop-mcp.ps1'

$startArgs = @()
if ($Full) { $startArgs += '-Full' }
if ($WithDeepSeek) { $startArgs += '-WithDeepSeek' }
if ($WithNgrok) { $startArgs += '-WithNgrok' }
if ($SkipMem0) { $startArgs += '-SkipMem0' }
if ($SkipSkills) { $startArgs += '-SkipSkills' }
if ($Quiet) { $startArgs += '-Quiet' }

& $SharedStart @startArgs
$sharedExit = $LASTEXITCODE

if (-not $SkipPhotoshop -and (Test-Path $PsMcp)) {
    if (-not $Quiet) {
        Write-Host ''
        Write-Host '[Session Start] Warming Photoshop MCP (broker :47391 + HTTP :8766) ...' -ForegroundColor Cyan
    }
    try {
        & $PsMcp -Background
    } catch {
        Write-Host "[Session Start] Photoshop MCP warm failed: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host '[Session Start] Manual: npm run layout:photoshop-mcp' -ForegroundColor Yellow
    }
    if (-not $Quiet) {
        Write-Host '[Session Start] If Cursor photoshop is red: refresh MCP. If tools fail: UDT Reload Adobe Python Bridge.' -ForegroundColor DarkGray
    }
}

exit $sharedExit
