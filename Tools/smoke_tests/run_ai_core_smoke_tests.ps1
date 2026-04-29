param(
    [string]$OutputDir = "output/smoke_tests/ai_core"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

Write-Host "=== AI Core Smoke Tests ==="
Write-Host "Repo: $RepoRoot"
Write-Host "Output: $OutputDir"

python "Tools/smoke_tests/run_ai_core_smoke_tests.py" --output-dir $OutputDir

Write-Host ""
Write-Host "Share these files if review is needed:"
Write-Host "- $OutputDir/ai_core_smoke_report.json"
Write-Host "- $OutputDir/ai_core_smoke_report.md"
