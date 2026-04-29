param(
    [string]$OutputDir = "output/smoke_tests/npu_validation_bridge",
    [string]$Manifest = "Tools/npu/npu_code_manifest.json"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

Write-Host "=== NPU Validation Bridge Smoke Tests ==="
Write-Host "Repo: $RepoRoot"
Write-Host "Output: $OutputDir"
Write-Host "Manifest: $Manifest"

python "Tools/smoke_tests/run_npu_validation_bridge_smoke_tests.py" --output-dir $OutputDir --manifest $Manifest

Write-Host ""
Write-Host "Share these files if review is needed:"
Write-Host "- $OutputDir/npu_validation_bridge_smoke_report.json"
Write-Host "- $OutputDir/npu_validation_bridge_smoke_report.md"
