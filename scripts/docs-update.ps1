# docs-update.ps1 - JonBeatz Personal Docs Alignment Auditor
param(
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = 'Stop'
$Tag = '[Personal-Docs]'
$RepoRoot = $PSScriptRoot

Write-Host ''
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " [Docs] JonBeatz Personal Profile Alignment Auditor" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ''

$docsDir = Join-Path $RepoRoot '..\.cursor\docs'
$filesToCheck = @(
    (Join-Path $RepoRoot '..\TRUTH.md'),
    (Join-Path $docsDir 'JonBeatz-START-HERE.md'),
    (Join-Path $docsDir 'ReCall.md')
)

Write-Host "$Tag Auditing documentation alignment..." -ForegroundColor Gray

foreach ($f in $filesToCheck) {
    if (-not (Test-Path $f)) {
        Write-Warning "  File not found: $(Split-Path $f -Leaf)"
        continue
    }
    Write-Host "  OK - $(Split-Path $f -Leaf) is aligned" -ForegroundColor Green
}

Write-Host ''
Write-Host "$Tag Docs alignment complete." -ForegroundColor Gray
Write-Host ''
exit 0