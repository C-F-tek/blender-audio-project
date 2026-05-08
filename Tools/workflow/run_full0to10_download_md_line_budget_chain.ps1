param(
    [string]$RepoRoot = ".",
    [string]$DownloadsDir = "$env:USERPROFILE\Downloads",
    [switch]$ApplyDocSplit,
    [switch]$UseAllInOne
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
$RepoRoot = (Resolve-Path $RepoRoot).Path
$Bundle = Join-Path $RepoRoot "output\validation\patch_bundles\full0to10_chained_md_budget_repo_quality_patch_bundle\run_patch_bundle.py"

if (-not (Test-Path $Bundle)) {
    throw "Chained patch bundle runner not found: $Bundle"
}

$Args = @(
    $Bundle,
    "--chain-download-md-budget",
    "--downloads-dir",
    $DownloadsDir
)

if ($ApplyDocSplit) { $Args += "--apply-doc-split" }
if ($UseAllInOne) { $Args += "--use-all-in-one" }

& $WorkflowPythonExe @Args
$ExitCode = $LASTEXITCODE
if ($ExitCode -ne 0) {
    throw "Download Markdown line-budget chain failed with exit code $ExitCode"
}

