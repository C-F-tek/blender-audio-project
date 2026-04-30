<#
.SYNOPSIS
  Run focused validation for app-agnostic NPU pipeline helper modules.

.DESCRIPTION
  This workflow is intentionally local and safe. It runs only deterministic
  helper smoke checks, unit tests and documentation alignment checks.

  It does not execute Blender, NPU, GPU, Ollama, FFmpeg or provider calls.
  It does not commit or push automatically.
#>

param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

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
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Validation step failed: $Name with exit code $LASTEXITCODE"
    }
}

$repo = Resolve-RepoRoot $RepoRoot
Set-Location $repo

if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
}

Invoke-ValidationStep -Name "NPU pipeline module smoke" -Arguments @(
    ".\Tools\validation\check_npu_pipeline_modules.py",
    "--repo-root", ".",
    "--output", ".\output\validation\npu_pipeline_modules.json"
)

Invoke-ValidationStep -Name "NPU pipeline helper unit tests" -Arguments @(
    ".\Tools\validation\check_npu_pipeline_helper_tests.py",
    "--repo-root", ".",
    "--output", ".\output\validation\npu_pipeline_helper_tests.json"
)

Invoke-ValidationStep -Name "NPU pipeline documentation alignment" -Arguments @(
    ".\Tools\validation\check_npu_pipeline_docs.py",
    "--repo-root", ".",
    "--output", ".\output\validation\npu_pipeline_docs.json"
)

Invoke-ValidationStep -Name "Python syntax validation" -Arguments @(
    ".\Tools\validation\check_python_syntax.py",
    "--repo-root", ".",
    "--output", ".\output\validation\python_syntax.json"
)

Write-Host "`nNPU pipeline helper validation completed." -ForegroundColor Green
Write-Host "Reports:"
Write-Host "- .\output\validation\npu_pipeline_modules.json"
Write-Host "- .\output\validation\npu_pipeline_helper_tests.json"
Write-Host "- .\output\validation\npu_pipeline_docs.json"
Write-Host "- .\output\validation\python_syntax.json"
