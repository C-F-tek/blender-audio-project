param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_effective_use_optimization",
    [string]$Request = "Ottimizza uso SQLite FTS5, runtime tools, GPU Ollama e NPU OpenVINO per Full0To10 senza run reale provider.",
    [string]$Db,
    [switch]$NoExternalProbes,
    [int]$TimeoutSeconds = 8
)

$ErrorActionPreference = "Stop"

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

$Summary = Join-Path $OutputPath "full0to10_effective_use_summary.from_cli.json"
$Args = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $OutputPath,
    "--request", $Request,
    "--timeout-seconds", $TimeoutSeconds,
    "--output", $Summary
)

if ($Db) {
    $Args += @("--db", (Resolve-RepoPath -Base $RepoRoot -PathValue $Db))
}
if ($NoExternalProbes) {
    $Args += "--no-external-probes"
}

& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_effective_use_optimization.py") @Args
if ($LASTEXITCODE -ne 0) {
    throw "Full0To10 effective use optimization failed with exit code $LASTEXITCODE"
}

Write-Host "[OK] Effective use summary: $Summary"
Write-Host "[OK] Quality product: $(Join-Path $OutputPath 'full0to10_effective_use_quality_product.md')"
