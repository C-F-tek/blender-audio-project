<#
.SYNOPSIS
  Run focused validation for app-agnostic NPU pipeline helper modules.

.DESCRIPTION
  This workflow is intentionally local and safe. It runs only deterministic
  helper smoke checks, unit tests, documentation alignment checks and
  observability-only runtime-output manifest generation.

  It does not execute Blender, NPU, GPU, Ollama, FFmpeg or provider calls.
  It does not commit or push automatically.
#>

param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation",
    [string]$TrackStem = "Feel The Light-Luca Vera_Master"
)

Set-StrictMode -Version Latest
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
$PythonEnvScript = Join-Path $PSScriptRoot "python_env.ps1"
. $PythonEnvScript

function Resolve-RepoRoot {
    param([string]$Path)
    return (Resolve-Path -LiteralPath $Path).Path
}

function Invoke-ValidationStep {
    param(
        [string]$Name,
        [string[]]$Arguments
    )

    Write-Host "`n=== $Name ===" -ForegroundColor Cyan
    & $WorkflowPythonExe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Validation step failed: $Name with exit code $LASTEXITCODE"
    }
}

$repo = Resolve-RepoRoot $RepoRoot
Set-Location $repo
$NpuHelperPythonExe = Use-WorkflowPython -RepoRoot $repo

if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
}

Invoke-ValidationStep -Name "NPU pipeline module smoke" -Arguments @(
    "-m", "Tools.validation", "check_npu_pipeline_modules",
    "--repo-root", ".",
    "--output", ".\output\validation\npu_pipeline_modules.json"
)

Invoke-ValidationStep -Name "NPU pipeline helper unit tests" -Arguments @(
    "-m", "Tools.validation", "check_npu_pipeline_helper_tests",
    "--repo-root", ".",
    "--output", ".\output\validation\npu_pipeline_helper_tests.json"
)

Invoke-ValidationStep -Name "NPU pipeline documentation alignment" -Arguments @(
    "-m", "Tools.validation", "check_npu_pipeline_docs",
    "--repo-root", ".",
    "--output", ".\output\validation\npu_pipeline_docs.json"
)

Invoke-ValidationStep -Name "NPU runtime output manifest" -Arguments @(
    "-m", "Tools.npu", "build_runtime_output_manifest",
    "--repo-root", ".",
    "--track-stem", $TrackStem,
    "--output", ".\output\validation\npu_runtime_output_manifest.json"
)

Invoke-ValidationStep -Name "Python syntax validation" -Arguments @(
    "-m", "Tools.validation", "check_python_syntax",
    "--repo-root", ".",
    "--output", ".\output\validation\python_syntax.json"
)

Write-Host "`nNPU pipeline helper validation completed." -ForegroundColor Green
Write-Host "Reports:"
Write-Host "- .\output\validation\npu_pipeline_modules.json"
Write-Host "- .\output\validation\npu_pipeline_helper_tests.json"
Write-Host "- .\output\validation\npu_pipeline_docs.json"
Write-Host "- .\output\validation\npu_runtime_output_manifest.json"
Write-Host "- .\output\validation\python_syntax.json"
