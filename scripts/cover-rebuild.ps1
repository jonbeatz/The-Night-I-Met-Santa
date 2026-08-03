# Cover rebuild helpers — Local (TNIMS)
param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("rebuild-wrap", "art-notype", "reopen-sot")]
  [string]$Action
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Root "TRUTH.md"))) {
  $Root = "D:\Hermes\projects\The-Night-I-Met-Santa"
}
$PsExe = "C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe"
if (-not (Test-Path $PsExe)) { throw "Photoshop 2026 not found: $PsExe" }

function Invoke-Psx([string]$JsxRel, [string]$ResultRel, [int]$TimeoutMin = 10) {
  $jsx = Join-Path $Root $JsxRel
  $result = Join-Path $Root $ResultRel
  if (-not (Test-Path $jsx)) { throw "Missing JSX: $jsx" }
  if (Test-Path $result) { Remove-Item $result -Force }
  Write-Host "Running $JsxRel ..."
  & $PsExe -r $jsx
  $deadline = (Get-Date).AddMinutes($TimeoutMin)
  while (-not (Test-Path $result) -and (Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 2
  }
  if (-not (Test-Path $result)) { throw "No result log: $result" }
  Get-Content $result
  if (Select-String -Path $result -Pattern "^ERROR" -Quiet) {
    throw "JSX reported ERROR - see $result"
  }
}

Set-Location $Root

switch ($Action) {
  "rebuild-wrap" {
    Invoke-Psx "scripts\cover-rebuild-wrap-5700.jsx" "scripts\_scratch\_cover_rebuild_wrap_result.txt"
  }
  "art-notype" {
    Invoke-Psx "scripts\cover-export-art-notype-panels-5700.jsx" "scripts\_scratch\_cover_export_art_notype_result.txt"
    python (Join-Path $Root "scripts\cover-compose-art-notype-5700.py")
  }
  "reopen-sot" {
    Invoke-Psx "scripts\_scratch\_close_cover_temps_reopen_sot.jsx" "scripts\_scratch\_close_cover_temps_result.txt"
  }
}

Write-Host "OK ($Action)"
