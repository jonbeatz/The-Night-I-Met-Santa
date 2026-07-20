# Start adobepy broker + dcc-mcp-photoshop for Cursor
# Requires: Photoshop running + UXP plugin Loaded (see PHOTOSHOP-SETUP.md)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Adobepy = Join-Path $Root "adobepy-0.5.2-windows-x64\bin\adobepy.exe"
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$McpPort = if ($env:DCC_MCP_PHOTOSHOP_PORT) { $env:DCC_MCP_PHOTOSHOP_PORT } else { "8766" }
$Token = if ($env:ADOBEPY_TOKEN) { $env:ADOBEPY_TOKEN } else { "dev-token" }

if (-not (Test-Path $Adobepy)) { throw "Missing adobepy.exe - extract release under photoshop-adobepy\" }
if (-not (Test-Path $Py)) { throw "Missing venv - run setup once (uv venv + pip install)" }

$env:ADOBEPY_TOKEN = $Token
$env:ADOBEPY_BROKER_URL = "http://127.0.0.1:47391"

# Broker
$brokerUp = $false
try {
  $h = Invoke-RestMethod "http://127.0.0.1:47391/health" -TimeoutSec 1
  if ($h.status -eq "ok") { $brokerUp = $true }
} catch { }

if (-not $brokerUp) {
  Write-Host "[photoshop-mcp] Starting adobepy broker on :47391 ..."
  Start-Process -FilePath $Adobepy -ArgumentList @("broker", "--token", $Token) -WindowStyle Hidden
  Start-Sleep -Seconds 2
}

Write-Host "[photoshop-mcp] Starting MCP HTTP on :$McpPort (broker :47391) ..."
Write-Host "[photoshop-mcp] Load UXP plugin first: bridges\photoshop\manifest.json via UDT"
Write-Host "[photoshop-mcp] Cursor URL: http://127.0.0.1:$McpPort/mcp"
& $Py -m dcc_mcp_photoshop --mcp-port $McpPort --broker-url $env:ADOBEPY_BROKER_URL @args
