param(
    [string]$RepoRoot = ".",
    [switch]$UseOllama,
    [string]$Model = "",
    [int]$MaxContextChars = 6000
)

$ErrorActionPreference = "Stop"

$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath

Write-Host "=== Build post-validation AI work packet ==="
Write-Host "Repo: $RepoRootPath"

$ArgsList = @(
    ".\Tools\ai\suggest_repository_updates.py",
    "--repo-root", ".",
    "--max-context-chars", "$MaxContextChars"
)

if ($UseOllama) {
    $ArgsList += "--use-ollama"
}

if ($Model -ne "") {
    $ArgsList += @("--model", $Model)
}

python @ArgsList

Write-Host ""
Write-Host "Generated:"
Write-Host "  output\ai_pipeline\repository_update_suggestions.json"
Write-Host "  output\ai_pipeline\repository_update_suggestions.md"
Write-Host ""
Write-Host "These reports are advisory only. Review before applying changes."
