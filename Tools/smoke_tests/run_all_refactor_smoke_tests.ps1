param(
    [string]$OutputDir = "output/smoke_tests",
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

Write-Host "=== Refactor Smoke Test Suite ==="
Write-Host "Repo: $RepoRoot"
Write-Host "Output: $OutputDir"
Write-Host "Python: $Python"

& $Python "Tools/smoke_tests/run_all_refactor_smoke_tests.py" --output-dir $OutputDir --python $Python

Write-Host ""
Write-Host "Primary files to share:"
Write-Host "- $OutputDir/refactor_summary/refactor_smoke_summary.json"
Write-Host "- $OutputDir/refactor_summary/refactor_smoke_summary.md"
Write-Host ""
Write-Host "If needed, also share:"
Write-Host "- $OutputDir/ai_core/ai_core_smoke_report.json"
Write-Host "- $OutputDir/ai_core/ai_core_smoke_report.md"
Write-Host "- $OutputDir/npu_validation_bridge/npu_validation_bridge_smoke_report.json"
Write-Host "- $OutputDir/npu_validation_bridge/npu_validation_bridge_smoke_report.md"
