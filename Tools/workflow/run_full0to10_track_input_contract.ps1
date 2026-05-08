param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_track_input_contract",
    [string]$TrackName = "current",
    [switch]$RequireInputs,
    [int]$MaxCandidates = 8
)

$ErrorActionPreference = "Stop"


# IA-CARMINE-REPO-PYTHON-POLICY-BEGIN
$RepoRootForWorkflowPython = (& git rev-parse --show-toplevel 2>$null)
if ([string]::IsNullOrWhiteSpace($RepoRootForWorkflowPython)) {
    $RepoRootForWorkflowPython = (Resolve-Path ".").Path
} else {
    $RepoRootForWorkflowPython = (Resolve-Path $RepoRootForWorkflowPython.Trim()).Path
}
. (Join-Path $RepoRootForWorkflowPython "Tools/workflow/python_env.ps1")
$WorkflowPythonExe = Use-WorkflowPython -RepoRoot $RepoRootForWorkflowPython
# IA-CARMINE-REPO-PYTHON-POLICY-END
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

$Summary = Join-Path $OutputPath "full0to10_track_input_contract.from_cli.json"
$Args = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $OutputPath,
    "--track-name", $TrackName,
    "--max-candidates", $MaxCandidates,
    "--output", $Summary
)

if ($RequireInputs) {
    $Args += "--require-inputs"
}

& $WorkflowPythonExe (Join-Path $RepoRoot "Tools/ai/build_full0to10_track_input_contract.py") @Args
$ExitCode = $LASTEXITCODE
if ($ExitCode -ne 0) {
    throw "Full0To10 track input contract failed with exit code $ExitCode"
}

Write-Host "[OK] Track input contract JSON: $Summary"
Write-Host "[OK] Track input contract MD: $(Join-Path $OutputPath 'full0to10_track_input_contract.md')"
Write-Host "[OK] Track input template: $(Join-Path $OutputPath 'full0to10_track_input_template.json')"

