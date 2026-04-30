param(
    [string]$RepoRoot = ".",
    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "core",
    [string]$OutputDir = "output/ai_pipeline",
    [string]$Basename = "repository_update_suggestions",
    [string]$ProposalBasename = "repository_change_proposals",
    [string[]]$ContextFile = @(),
    [string[]]$ReportFile = @(),
    [switch]$UseOllama,
    [string]$Model = "",
    [int]$MaxContextChars = 6000
)

$ErrorActionPreference = "Stop"

$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath

Write-Host "=== Build post-validation AI work packet ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Profile: $Profile"
Write-Host "OutputDir: $OutputDir"
Write-Host "Basename: $Basename"
Write-Host "ProposalBasename: $ProposalBasename"

$ArgsList = @(
    ".\Tools\ai\suggest_repository_updates.py",
    "--repo-root", ".",
    "--profile", $Profile,
    "--output-dir", $OutputDir,
    "--basename", $Basename,
    "--max-context-chars", "$MaxContextChars"
)

foreach ($Path in $ContextFile) {
    $ArgsList += @("--context-file", $Path)
}

foreach ($Path in $ReportFile) {
    $ArgsList += @("--report-file", $Path)
}

if ($UseOllama) {
    $ArgsList += "--use-ollama"
}

if ($Model -ne "") {
    $ArgsList += @("--model", $Model)
}

python @ArgsList

$ProposalArgs = @(
    ".\Tools\ai\build_repository_change_proposals.py",
    "--repo-root", ".",
    "--profile", $Profile,
    "--output-dir", $OutputDir,
    "--basename", $ProposalBasename
)

foreach ($Path in $ReportFile) {
    $ProposalArgs += @("--report-file", $Path)
}

python @ProposalArgs

Write-Host ""
Write-Host "Generated:"
Write-Host "  $OutputDir\$Basename.json"
Write-Host "  $OutputDir\$Basename.md"
Write-Host "  $OutputDir\${Basename}_manifest.json"
Write-Host "  $OutputDir\$ProposalBasename.json"
Write-Host "  $OutputDir\$ProposalBasename.md"
Write-Host ""
Write-Host "These reports are advisory only. Review before applying changes."
