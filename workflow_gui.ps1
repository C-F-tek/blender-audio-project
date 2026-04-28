param(
    [switch]$DebugMode,
    [switch]$SkipStartupCheck
)

$ErrorActionPreference = "Stop"
$Project = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Project
$NpuPython = Join-Path $Root "venvs\blender-npu-ai\Scripts\python.exe"
$GuiScript = Join-Path $Project "Tools\workflow\gui\workflow_gui_with_push.py"
$StartupPreflight = Join-Path $Project "Tools\workflow\startup_preflight.ps1"

if (Test-Path -LiteralPath $NpuPython) {
    $null = & $NpuPython -c "print('ok')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $Python = $NpuPython
    } else {
        Write-Host "NPU Python presente ma non avviabile; uso python di sistema per la shell GUI." -ForegroundColor Yellow
        $Python = "python"
    }
} else {
    $Python = "python"
}

if ($DebugMode) {
    Write-Host "Python: $Python"
    Write-Host "GUI   : $GuiScript"
}

if (-not $SkipStartupCheck -and (Test-Path -LiteralPath $StartupPreflight)) {
    . $StartupPreflight
    $null = Invoke-SpaziotempoStartupCheck -Project $Project -Root $Root -Python $Python
}

& $Python $GuiScript
