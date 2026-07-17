$ErrorActionPreference = 'Stop'

$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$Tools = Join-Path $Root 'tools\layout-mcp'

function Ensure-Repo {
    param([string]$Name, [string]$Url)
    $Path = Join-Path $Tools $Name
    if (-not (Test-Path $Path)) {
        git clone --depth 1 $Url $Path
    }
    return $Path
}

function Replace-Text {
    param([string]$Path, [string]$Old, [string]$New)
    $Text = Get-Content $Path -Raw -Encoding UTF8
    if ($Text.Contains($Old)) {
        $Text.Replace($Old, $New) | Set-Content $Path -Encoding UTF8 -NoNewline
    }
}

$Affinity = Ensure-Repo 'affinity-scripting' 'https://github.com/rabidgremlin/affinity-scripting.git'
$InDesignUxp = Ensure-Repo 'indesign-uxp-server' 'https://github.com/theloniuser/indesign-uxp-server.git'
$InDesignCom = Ensure-Repo 'indesign-scripting-mcp' 'https://github.com/MoebiusSt/indesign-scripting-mcp.git'

Push-Location $Affinity
npm install
Pop-Location

Push-Location $InDesignUxp
npm install
Push-Location 'bridge'
npm install
Pop-Location
Pop-Location

$Python = Join-Path $InDesignCom '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) {
    python -m venv (Join-Path $InDesignCom '.venv')
}
& $Python -m pip install -r (Join-Path $InDesignCom 'requirements.txt')

# The upstream UXP bridge uses 3000/3001, which conflicts with local web apps.
Replace-Text (Join-Path $InDesignUxp 'bridge\server.js') `
    "const WS_PORT = 3001;`nconst HTTP_PORT = 3000;" `
    "const WS_PORT = Number(process.env.INDESIGN_BRIDGE_WS_PORT || 19301);`nconst HTTP_PORT = Number(process.env.INDESIGN_BRIDGE_HTTP_PORT || 19300);"
Replace-Text (Join-Path $InDesignUxp 'plugin\index.js') `
    'const ws = new WebSocket("ws://127.0.0.1:3001");' `
    'const ws = new WebSocket("ws://127.0.0.1:19301");'
Replace-Text (Join-Path $InDesignUxp 'src\index.js') `
    'const BRIDGE_PORT = 3001;' `
    'const BRIDGE_PORT = Number(process.env.INDESIGN_BRIDGE_WS_PORT || 19301);'
Replace-Text (Join-Path $InDesignUxp 'src\core\scriptExecutor.js') `
    "const BRIDGE_URL = 'http://127.0.0.1:3000';" `
    "const BRIDGE_URL = process.env.INDESIGN_BRIDGE_HTTP_URL || 'http://127.0.0.1:19300';"

Write-Host ''
Write-Host '[layout-mcp] Installed Affinity helpers + InDesign UXP/COM servers.'
Write-Host '[layout-mcp] Next: install Adobe UXP Developer Tools from Creative Cloud, then load:'
Write-Host "  $InDesignUxp\plugin\manifest.json"
