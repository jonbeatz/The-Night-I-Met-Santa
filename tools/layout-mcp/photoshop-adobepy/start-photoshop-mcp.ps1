# Start adobepy broker + dcc-mcp-photoshop for Cursor
# Requires: Photoshop running + UXP plugin Loaded (see PHOTOSHOP-SETUP.md)
#
# Modes:
#   (default)     Foreground MCP (blocks) - interactive / debug
#   -Background   Start broker + MCP detached, probe ports, exit (session:start)
param(
    [switch]$Background
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Adobepy = Join-Path $Root "adobepy-0.5.2-windows-x64\bin\adobepy.exe"
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$McpPort = if ($env:DCC_MCP_PHOTOSHOP_PORT) { $env:DCC_MCP_PHOTOSHOP_PORT } else { "8766" }
$Token = if ($env:ADOBEPY_TOKEN) { $env:ADOBEPY_TOKEN } else { "dev-token" }
$BrokerUrl = "http://127.0.0.1:47391"
$McpUrl = "http://127.0.0.1:$McpPort"

function Test-Port([int]$Port) {
    return [bool](Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)
}

if (-not (Test-Path $Adobepy)) { throw "Missing adobepy.exe - extract release under photoshop-adobepy\" }
if (-not (Test-Path $Py)) { throw "Missing venv - run setup once (uv venv + pip install)" }

$env:ADOBEPY_TOKEN = $Token
$env:ADOBEPY_BROKER_URL = $BrokerUrl

# Broker
$brokerUp = $false
try {
  $h = Invoke-RestMethod "$BrokerUrl/health" -TimeoutSec 1
  if ($h.status -eq "ok") { $brokerUp = $true }
} catch { }

if (-not $brokerUp) {
  Write-Host "[photoshop-mcp] Starting adobepy broker on :47391 ..."
  Start-Process -FilePath $Adobepy -ArgumentList @("broker", "--token", $Token) -WindowStyle Hidden
  Start-Sleep -Seconds 2
} else {
  Write-Host "[photoshop-mcp] Broker :47391 already online"
}

# MCP HTTP
$mcpUp = Test-Port -Port ([int]$McpPort)
if ($mcpUp) {
  Write-Host "[photoshop-mcp] MCP :$McpPort already online ($McpUrl/mcp)"
} elseif ($Background) {
  Write-Host "[photoshop-mcp] Starting MCP HTTP on :$McpPort (background) ..."
  $argList = @(
    "-m", "dcc_mcp_photoshop",
    "--mcp-port", $McpPort,
    "--broker-url", $BrokerUrl
  )
  Start-Process -FilePath $Py -ArgumentList $argList -WindowStyle Hidden `
    -WorkingDirectory $Root
  $deadline = (Get-Date).AddSeconds(12)
  while ((Get-Date) -lt $deadline) {
    if (Test-Port -Port ([int]$McpPort)) { break }
    Start-Sleep -Milliseconds 400
  }
  if (Test-Port -Port ([int]$McpPort)) {
    Write-Host "[photoshop-mcp] MCP online -> $McpUrl/mcp" -ForegroundColor Green
  } else {
    Write-Host "[photoshop-mcp] WARNING: :$McpPort not listening yet - check venv / logs" -ForegroundColor Yellow
  }
} else {
  Write-Host "[photoshop-mcp] Starting MCP HTTP on :$McpPort (broker :47391) ..."
  Write-Host "[photoshop-mcp] Cursor URL: $McpUrl/mcp"
  Write-Host "[photoshop-mcp] Load UXP plugin first: bridges\photoshop\manifest.json via UDT"
  & $Py -m dcc_mcp_photoshop --mcp-port $McpPort --broker-url $BrokerUrl @args
  return
}

# Session hint (background / already-up path)
$sessions = 0
try {
  $h = Invoke-RestMethod "$BrokerUrl/health" -TimeoutSec 2
  if ($null -ne $h.sessions) { $sessions = [int]$h.sessions }
} catch { }

$psRunning = [bool](Get-Process -Name "Photoshop" -ErrorAction SilentlyContinue)
Write-Host "[photoshop-mcp] Cursor URL: $McpUrl/mcp"
if ($sessions -lt 1) {
  Write-Host "[photoshop-mcp] Bridge sessions=$sessions - UDT Reload 'Adobe Python Bridge' (Photoshop), then refresh Cursor MCP if red." -ForegroundColor Yellow
  if (-not $psRunning) {
    Write-Host "[photoshop-mcp] Photoshop not running - open PS 2026 before Reload." -ForegroundColor Yellow
  }
} else {
  Write-Host "[photoshop-mcp] Bridge sessions=$sessions (UXP connected)" -ForegroundColor Green
}
