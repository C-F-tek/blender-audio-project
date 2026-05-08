param(
    [string]$RepoRoot = ".",
    [string]$PatchSpecs = "output/validation/full0to10_auto_refactor_plan/full0to10_auto_refactor_patch_specs.json",
    [string]$OutputDir = "output/validation/full0to10_auto_refactor_apply",
    [switch]$Apply,
    [int]$MaxSpecs = 0,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ForwardedArgs = @()
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "python_env.ps1")

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }
    return (Join-Path $Base $PathValue)
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$WorkflowPythonExe = Use-WorkflowPython -RepoRoot $RepoRoot
$PatchSpecsPath = Resolve-RepoPath -Base $RepoRoot -PathValue $PatchSpecs
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$Args = @(
    "--repo-root", $RepoRoot,
    "--patch-specs", $PatchSpecsPath,
    "--output-dir", $OutputPath
)

if ($Apply) {
    $Args += "--apply"
}
if ($MaxSpecs -gt 0) {
    $Args += @("--max-specs", $MaxSpecs)
}
if ($ForwardedArgs.Count -gt 0) {
    $Args += $ForwardedArgs
}

$ScriptPath = Join-Path $RepoRoot "Tools/ai/apply_full0to10_auto_refactor_patch_specs.py"
& $WorkflowPythonExe $ScriptPath @Args
$ExitCode = $LASTEXITCODE

if ($ExitCode -ne 0) {
    throw "Full0To10 controlled refactor applier failed with exit code $ExitCode"
}

Write-Host "[OK] Controlled refactor applier output: $OutputPath"
