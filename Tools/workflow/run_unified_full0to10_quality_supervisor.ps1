param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_quality_supervisor",
    [string]$PatchSpecs,
    [switch]$RunLauncher,
    [switch]$SkipLauncher,
    [switch]$NoExternalProbes,
    [switch]$AllowGitSyncBranching,
    [ValidateSet("quick", "balanced", "deep", "custom")]
    [string]$RunIntensity = "quick",
    [string]$Model = "gpt-oss:20b",
    [switch]$SkipGitSync,
    [switch]$NoBranch,
    [string[]]$ForwardedArgs = @()
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }
    return (Join-Path $Base $PathValue)
}

function Invoke-QualityStack {
    param(
        [string]$Phase,
        [string]$Root,
        [string]$OutDir,
        [string]$Specs,
        [bool]$DisableExternal
    )

    $Args = @("-RepoRoot", $Root, "-OutputDir", $OutDir)
    if ($Specs) {
        $Args += @("-PatchSpecs", $Specs)
    }
    if ($DisableExternal) {
        $Args += "-NoExternalProbes"
    }

    Write-Host "[Full0To10][$Phase] Running quality stack..."
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
        (Join-Path $Root "Tools/workflow/run_full0to10_quality_stack_preflight.ps1") @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Quality stack phase '$Phase' failed with exit code $LASTEXITCODE"
    }
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$PreflightDir = Join-Path $OutputPath "preflight"
$FinalDir = Join-Path $OutputPath "final"
$LauncherDir = Join-Path $OutputPath "launcher"
New-Item -ItemType Directory -Force -Path $PreflightDir, $FinalDir, $LauncherDir | Out-Null

$PatchSpecsPath = $null
if ($PatchSpecs) {
    $PatchSpecsPath = Resolve-RepoPath -Base $RepoRoot -PathValue $PatchSpecs
}

$EffectiveRunLauncher = [bool]$RunLauncher -and -not [bool]$SkipLauncher
if ($SkipLauncher) {
    Write-Host "[Full0To10] -SkipLauncher supplied; launcher disabled."
}
if (-not $RunLauncher) {
    Write-Host "[Full0To10] Safe default: launcher disabled. Pass -RunLauncher explicitly to run it."
}

Invoke-QualityStack -Phase "preflight" -Root $RepoRoot -OutDir $PreflightDir -Specs $PatchSpecsPath -DisableExternal ([bool]$NoExternalProbes)

if (-not $EffectiveRunLauncher) {
    Write-Host "[Full0To10] Quality-only mode; no provider/runtime launcher executed."
}
else {
    $Supervisor = Join-Path $RepoRoot "Tools/workflow/run_unified_full0to10_with_contract_gate.ps1"
    if (-not (Test-Path $Supervisor)) {
        throw "Missing supervisor wrapper: $Supervisor"
    }

    $SupervisorArgs = @(
        "-RepoRoot", $RepoRoot,
        "-RunIntensity", $RunIntensity,
        "-Model", $Model,
        "-GateOutputDir", (Join-Path $LauncherDir "contract_gate")
    )

    if ($SkipGitSync -or -not $AllowGitSyncBranching) {
        $SupervisorArgs += "-SkipGitSync"
    }
    if ($NoBranch -or -not $AllowGitSyncBranching) {
        $SupervisorArgs += "-NoBranch"
    }
    if ($ForwardedArgs.Count -gt 0) {
        $SupervisorArgs += @("-ForwardedArgs", $ForwardedArgs)
    }

    Write-Host "[Full0To10] Running unified supervisor with contract gate..."
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Supervisor @SupervisorArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Unified Full0To10 supervisor failed with exit code $LASTEXITCODE"
    }
}

Invoke-QualityStack -Phase "final" -Root $RepoRoot -OutDir $FinalDir -Specs $PatchSpecsPath -DisableExternal ([bool]$NoExternalProbes)

Write-Host "[OK] Quality supervisor output: $OutputPath"
Write-Host "[OK] Preflight: $PreflightDir"
Write-Host "[OK] Final: $FinalDir"
