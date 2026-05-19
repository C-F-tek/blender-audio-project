param(
    [ValidateSet("Gui", "Shell")]
    [string]$Mode = "Shell",
    [switch]$DebugMode,
    [switch]$SkipStartupCheck
)

$ErrorActionPreference = "Stop"

$Project = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$Root = Split-Path -Parent $Project
$NpuPython = Join-Path $Root "venvs\blender-npu-ai\Scripts\python.exe"
$StartupPreflight = Join-Path $Project "Tools\workflow\startup_preflight.ps1"

function Resolve-WorkflowPython {
    param([string]$Candidate)

    if (Test-Path -LiteralPath $Candidate) {
        $null = & $Candidate -c "print('ok')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $Candidate
        }
        Write-Host "NPU Python presente ma non avviabile; uso python di sistema." -ForegroundColor Yellow
    }
    return "python"
}

$Python = Resolve-WorkflowPython -Candidate $NpuPython
$Tool = if ($Mode -eq "Gui") {
    "gui"
} else {
    "workflow_shell"
}

if ($DebugMode) {
    Write-Host "Python: $Python"
    Write-Host "Mode  : $Mode"
    Write-Host "Tool  : $Tool"
}

if (-not $SkipStartupCheck -and (Test-Path -LiteralPath $StartupPreflight)) {
    . $StartupPreflight
    $null = Invoke-SpaziotempoStartupCheck -Project $Project -Root $Root -Python $Python
}

Push-Location $Project
try {
    & $Python -m Tools.workflow $Tool
} finally {
    Pop-Location
}
