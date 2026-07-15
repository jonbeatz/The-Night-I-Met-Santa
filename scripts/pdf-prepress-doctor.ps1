# pdf-prepress-doctor.ps1 — img2pdf + pikepdf ready for POD picture books
param([switch]$Quiet)

$ErrorActionPreference = 'Continue'
$Tag = '[PDF Prepress Doctor]'
$Root = if ($PSScriptRoot -match 'shared-profile-content') {
    (Get-Location).Path
} else {
    Split-Path $PSScriptRoot -Parent
}

function Write-Check {
    param([bool]$Ok, [string]$Label, [string]$Detail = '')
    if ($Quiet -and $Ok) { return }
    $color = if ($Ok) { 'Green' } else { 'Yellow' }
    $state = if ($Ok) { 'OK' } else { 'MISSING' }
    $extra = if ($Detail) { " - $Detail" } else { '' }
    Write-Host "  [$state] $Label$extra" -ForegroundColor $color
}

Write-Host ''
Write-Host "$Tag img2pdf + pikepdf..." -ForegroundColor Cyan

$py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
$raw = & $py -c "import img2pdf,pikepdf; print(img2pdf.__version__+'|'+pikepdf.__version__)" 2>&1
$ok = $LASTEXITCODE -eq 0
if ($ok) {
    $parts = ($raw | Out-String).Trim().Split('|')
    Write-Check -Ok $true -Label 'img2pdf' -Detail $parts[0]
    Write-Check -Ok $true -Label 'pikepdf' -Detail $parts[1]
} else {
    Write-Check -Ok $false -Label 'img2pdf+pikepdf' -Detail 'python -m pip install img2pdf pikepdf'
    Write-Host $raw -ForegroundColor DarkGray
}

Write-Host ''
Write-Host 'Commands (The-Night-I-Met-Santa):' -ForegroundColor Cyan
Write-Host '  npm run book:pdf:from-pages' -ForegroundColor DarkGray
Write-Host '  npm run book:pdf:verify' -ForegroundColor DarkGray
Write-Host '  npm run book:pdf:verify:boxes' -ForegroundColor DarkGray
Write-Host ''

if ($ok) {
    Write-Host "$Tag READY" -ForegroundColor Green
    exit 0
}
Write-Host "$Tag NOT READY" -ForegroundColor Yellow
exit 1
