# Mem0 LM Studio preflight — delegates to JonBeatz (VRAM-safe 16384/parallel 1 + smart-load).
param([switch]$Quiet)

$jonPreflight = 'D:\Hermes\projects\JonBeatz\scripts\mem0-preflight.ps1'
if (Test-Path $jonPreflight) {
    $args = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $jonPreflight)
    if ($Quiet) { $args += '-Quiet' }
    & powershell @args
    exit $LASTEXITCODE
}

# Fallback when JonBeatz repo unavailable — env-driven, VRAM-safe defaults.
$ErrorActionPreference = 'Continue'
$Mem0Model = if ($env:HERMES_LM_MODEL) { $env:HERMES_LM_MODEL } elseif ($env:LMSTUDIO_MODEL) { $env:LMSTUDIO_MODEL } else { 'qwen3-4b-instruct-2507' }
$Mem0Context = if ($env:HERMES_LM_CONTEXT) { [int]$env:HERMES_LM_CONTEXT } elseif ($env:LMSTUDIO_CONTEXT_LENGTH) { [int]$env:LMSTUDIO_CONTEXT_LENGTH } else { 16384 }
$Mem0Parallel = if ($env:HERMES_LM_PARALLEL) { [int]$env:HERMES_LM_PARALLEL } else { 1 }
$LmsApi = 'http://127.0.0.1:1234/v1/models'

function Write-Mem0Log {
    param([string]$Message, [string]$Color = 'Cyan')
    if (-not $Quiet) { Write-Host "[Mem0] $Message" -ForegroundColor $Color }
}

if (-not (Get-Command lms -ErrorAction SilentlyContinue)) {
    Write-Mem0Log 'lms CLI not found.' 'Red'
    exit 1
}

function Get-LoadedLlmState {
    $raw = & lms ps --json 2>&1
    if ($LASTEXITCODE -ne 0 -or -not $raw) { return $null }
    try {
        $items = $raw | ConvertFrom-Json
        if (-not $items) { return $null }
        if ($items -is [System.Array]) {
            return @($items | Where-Object { $_.type -eq 'llm' } | Select-Object -First 1)
        }
        return $items
    } catch { return $null }
}

$loaded = Get-LoadedLlmState
if ($loaded) {
    $ctx = [int]$loaded.contextLength
    $par = [int]$loaded.parallel
    if ($ctx -gt $Mem0Context -or $par -gt $Mem0Parallel) {
        Write-Mem0Log "Reloading $($loaded.identifier): ctx $ctx/$Mem0Context parallel $par/$Mem0Parallel" 'Yellow'
        & lms unload $loaded.identifier 2>&1 | Out-Null
        $loaded = $null
    }
}

if (-not $loaded) {
    & lms load $Mem0Model -c $Mem0Context --parallel $Mem0Parallel 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { Write-Mem0Log "Load failed." 'Red'; exit 1 }
}

try {
    $null = Invoke-RestMethod -Uri $LmsApi -TimeoutSec 10
    Write-Mem0Log "Ready: $Mem0Model ctx $Mem0Context parallel $Mem0Parallel" 'Green'
    exit 0
} catch {
    Write-Mem0Log "LM Studio not reachable at $LmsApi" 'Red'
    exit 1
}
