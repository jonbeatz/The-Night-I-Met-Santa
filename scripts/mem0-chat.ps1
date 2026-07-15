# J.A.R.V.I.S. Mem0 Integration Wrapper
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("add", "search", "list", "delete")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$Text,

    [Parameter(Mandatory=$false)]
    [string]$Query,

    [Parameter(Mandatory=$false)]
    [string]$Id,

    [switch]$SkipPreflight
)

$RepoRoot = Split-Path $PSScriptRoot -Parent
$pythonPath = "C:\Users\JONBEATZ\AppData\Local\Programs\Python\Python312\python.exe"
$scriptPath = Join-Path $PSScriptRoot 'mem0_integration.py'
$preflightPath = Join-Path $PSScriptRoot 'mem0-preflight.ps1'

if (-not $SkipPreflight -and (Test-Path $preflightPath)) {
    & powershell -ExecutionPolicy Bypass -File $preflightPath -Quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "J.A.R.V.I.S.: Mem0 preflight failed. LM Studio may be offline or qwen3-4b could not load."
        if (Get-Command speak -ErrorAction SilentlyContinue) {
            speak "Excuse me, Jon. Mem0 preflight failed. Please ensure LM Studio is available on port 12 34." 2>$null
        }
        return
    }
}

# Build the command arguments
if ($Action -eq "add") {
    if (-not $Text) {
        Write-Error "The -Text parameter is required when adding memories."
        return
    }
    $argsList = @("--action", "add", "--text", $Text)
} elseif ($Action -eq "search") {
    if (-not $Query) {
        Write-Error "The -Query parameter is required when searching memories."
        return
    }
    $argsList = @("--action", "search", "--query", $Query)
} elseif ($Action -eq "list") {
    $argsList = @("--action", "list")
} elseif ($Action -eq "delete") {
    if (-not $Id) {
        Write-Error "The -Id parameter is required when deleting memories."
        return
    }
    $argsList = @("--action", "delete", "--id", $Id)
}

# Run the Python script and capture the stdout
$responseRaw = & $pythonPath $scriptPath $argsList 2>$null

# Check if the output is warning text or empty
if (-not $responseRaw) {
    Write-Warning "J.A.R.V.I.S.: No response received from Mem0 integration layer. Please verify that your local LM Studio is running on http://127.0.0.1:1234/v1."
    return
}

# If the output contains LM Studio Warning message, display and speak it
if ($responseRaw -match "Warning") {
    Write-Host $responseRaw -ForegroundColor Yellow
    if (Get-Command speak -ErrorAction SilentlyContinue) {
        speak "Excuse me, Jon. I was unable to access local memory because LM Studio is currently offline. Please ensure it is running on port 12 34." 2>$null
    }
    return
}

try {
    # Parse JSON output from the Python script
    $response = $responseRaw | ConvertFrom-Json
} catch {
    Write-Host "[Raw Output] $responseRaw" -ForegroundColor Red
    Write-Error "Failed to parse JSON response from Mem0 integration."
    return
}

if ($response -and $response.success) {
    if ($Action -eq "add") {
        $msg = "Memory recorded, Jon. I have updated my local memory banks."
        Write-Host "[J.A.R.V.I.S.] $msg" -ForegroundColor Green
        
        # Call speak function from profile
        if (Get-Command speak -ErrorAction SilentlyContinue) {
            speak $msg 2>$null
        }
    } else {
        # Format search results
        $memories = $response.data.results
        if ($memories -and $memories.Count -gt 0) {
            $memText = ""
            Write-Host "------------ J.A.R.V.I.S. RECALL ------------" -ForegroundColor Cyan
            foreach ($m in $memories) {
                Write-Host " - $($m.memory)" -ForegroundColor White
                $memText += "$($m.memory). "
            }
            Write-Host "---------------------------------------------" -ForegroundColor Cyan
            
            $speakText = "Here is what I recall, Jon: $memText"
            if (Get-Command speak -ErrorAction SilentlyContinue) {
                speak $speakText 2>$null
            }
        } else {
            $msg = 'I''m sorry, Jon, but I found no memories matching your request.'
            Write-Host "[J.A.R.V.I.S.] $msg" -ForegroundColor Yellow
            if (Get-Command speak -ErrorAction SilentlyContinue) {
                speak $msg 2>$null
            }
        }
    }
} else {
    $err = $response.error
    Write-Host "[J.A.R.V.I.S. Error] $err" -ForegroundColor Red
    if (Get-Command speak -ErrorAction SilentlyContinue) {
        speak "Excuse me, Jon. I encountered an error while accessing my memory layer." 2>$null
    }
}