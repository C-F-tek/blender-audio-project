param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/startup_check_guard",
    [string]$TrackName = "current",
    [switch]$StrictExit,
    [switch]$RequireTrackInputs
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

$TrackOutputDir = Join-Path $OutputPath "track_inputs"
$TrackArgs = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $TrackOutputDir,
    "--track-name", $TrackName,
    "--output", (Join-Path $TrackOutputDir "full0to10_track_input_contract.from_startup_guard.json")
)
if ($RequireTrackInputs) {
    $TrackArgs += "--require-inputs"
}

& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_track_input_contract.py") @TrackArgs
$TrackExitCode = $LASTEXITCODE
if ($TrackExitCode -ne 0) {
    throw "Track input contract failed with exit code $TrackExitCode"
}

if ($StrictExit) {
    $Report = Get-Content $JsonOutput -Raw | ConvertFrom-Json
    if ($Report.passed -ne $true) {
        throw "Startup check failed in strict mode. See: $JsonOutput"
    }
}

Write-Host "[OK] Startup check JSON: $JsonOutput"
Write-Host "[OK] Startup check text: $TextOutput"
Write-Host "[OK] Track input contract: $(Join-Path $TrackOutputDir 'full0to10_track_input_contract.from_startup_guard.json')"
