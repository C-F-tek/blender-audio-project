param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_quality_gate",
    [string]$PatchSpecs
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

$Json = Join-Path $OutputPath "full0to10_quality_gate.json"
$Md = Join-Path $OutputPath "full0to10_quality_gate.md"

$Args = @(
    "--repo-root", $RepoRoot,
    "--output", $Json,
    "--markdown-output", $Md
)

if ($PatchSpecs) {
    $PatchSpecsPath = Resolve-RepoPath -Base $RepoRoot -PathValue $PatchSpecs
    if (Test-Path $PatchSpecsPath) {
        $Args += @("--patch-specs", $PatchSpecsPath)
    }
}

& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_quality_gate.py") @Args
if ($LASTEXITCODE -ne 0) {
    throw "Full0To10 quality gate failed with exit code $LASTEXITCODE"
}

Write-Host "[OK] Quality gate JSON: $Json"
Write-Host "[OK] Quality gate MD: $Md"
