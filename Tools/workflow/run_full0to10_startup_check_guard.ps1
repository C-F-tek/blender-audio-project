param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/startup_check_guard",
    [switch]$StrictExit
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }
    return (Join-Path $Base $PathValue)
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$JsonOutput = Join-Path $OutputPath "startup_check.json"
$TextOutput = Join-Path $OutputPath "startup_check.txt"
$ScriptPath = Join-Path $RepoRoot "Tools/workflow/startup_check.py"

& python $ScriptPath --repo-root $RepoRoot --output $JsonOutput --text-output $TextOutput
$ExitCode = $LASTEXITCODE
if ($ExitCode -ne 0) {
    throw "startup_check.py failed with exit code $ExitCode"
}

if ($StrictExit) {
    $Report = Get-Content $JsonOutput -Raw | ConvertFrom-Json
    if ($Report.passed -ne $true) {
        throw "Startup check failed in strict mode. See: $JsonOutput"
    }
}

Write-Host "[OK] Startup check JSON: $JsonOutput"
Write-Host "[OK] Startup check text: $TextOutput"
