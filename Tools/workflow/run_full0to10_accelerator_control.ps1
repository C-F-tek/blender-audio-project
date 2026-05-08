param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_accelerator_control",
    [string]$Request = "Rendi GPU padrona del suo corpo e mente, con NPU auditor e GPU.0 diagnostic nel prodotto finale Full0To10.",
    [switch]$NoExternalProbes,
    [int]$TimeoutSeconds = 8
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
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$Summary = Join-Path $OutputPath "full0to10_accelerator_control.from_cli.json"
$Args = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $OutputPath,
    "--request", $Request,
    "--timeout-seconds", $TimeoutSeconds,
    "--output", $Summary
)

if ($NoExternalProbes) {
    $Args += "--no-external-probes"
}

& $WorkflowPythonExe (Join-Path $RepoRoot "Tools/ai/build_full0to10_accelerator_control.py") @Args
if ($LASTEXITCODE -ne 0) {
    throw "Full0To10 accelerator control failed with exit code $LASTEXITCODE"
}

Write-Host "[OK] Accelerator control JSON: $Summary"
Write-Host "[OK] Accelerator control MD: $(Join-Path $OutputPath 'full0to10_accelerator_control.md')"
