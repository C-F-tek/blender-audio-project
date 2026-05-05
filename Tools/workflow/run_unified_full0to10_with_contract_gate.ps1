param(
    [string]$RepoRoot = ".",
    [ValidateSet("quick", "balanced", "deep", "custom")]
    [string]$RunIntensity = "quick",
    [string]$Model = "gpt-oss:20b",
    [switch]$SkipGitSync,
    [switch]$NoBranch,
    [switch]$DryRun,
    [switch]$SkipLauncher,
    [string]$Bundle,
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [string]$GateOutputDir = "output/validation/unified_full0to10_contract_gate",
    [string[]]$ForwardedArgs = @()
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Base,
        [Parameter(Mandatory = $true)]
        [string]$PathValue
    )

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }

    return (Join-Path $Base $PathValue)
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$Launcher = Join-Path $RepoRoot "Tools/workflow/run_unified_local_ai_refactor.ps1"
$Gate = Join-Path $RepoRoot "Tools/workflow/run_full0to10_manifest_contract_gate.ps1"

if (-not (Test-Path $Gate)) {
    throw "Required gate script not found: $Gate"
}

$LauncherExitCode = 0

if (-not $SkipLauncher) {
    if (-not (Test-Path $Launcher)) {
        throw "Required launcher script not found: $Launcher"
    }

    $LauncherArgs = @(
        "-Full0To10",
        "-RunIntensity", $RunIntensity,
        "-Model", $Model
    )

    if ($SkipGitSync) {
        $LauncherArgs += "-SkipGitSync"
    }
    if ($NoBranch) {
        $LauncherArgs += "-NoBranch"
    }
    if ($DryRun) {
        $LauncherArgs += "-DryRun"
    }
    if ($ForwardedArgs.Count -gt 0) {
        $LauncherArgs += $ForwardedArgs
    }

    Write-Host "[Full0To10] Launching unified local AI refactor..."
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Launcher @LauncherArgs
    $LauncherExitCode = $LASTEXITCODE
    Write-Host "[Full0To10] Launcher exit code: $LauncherExitCode"
}
else {
    Write-Host "[Full0To10] SkipLauncher enabled; running gate only."
}

$GateArgs = @(
    "-RepoRoot", $RepoRoot,
    "-EvidenceDir", $EvidenceDir,
    "-OutputDir", $GateOutputDir
)

if ($Bundle) {
    $GateArgs += @("-Bundle", $Bundle)
}

Write-Host "[Full0To10] Running manifest contract gate..."
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Gate @GateArgs
$GateExitCode = $LASTEXITCODE
Write-Host "[Full0To10] Gate exit code: $GateExitCode"

if ($LauncherExitCode -ne 0) {
    exit $LauncherExitCode
}

exit $GateExitCode
