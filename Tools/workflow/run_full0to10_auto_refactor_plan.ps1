param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_auto_refactor_plan",
    [switch]$WritePatchSpecs
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

$Json = Join-Path $OutputPath "full0to10_auto_refactor_plan.json"
$Md = Join-Path $OutputPath "full0to10_auto_refactor_plan.md"
$Specs = Join-Path $OutputPath "full0to10_auto_refactor_patch_specs.json"

$Args = @(
    "--repo-root", $RepoRoot,
    "--output", $Json,
    "--markdown-output", $Md
)

if ($WritePatchSpecs) {
    $Args += @("--patch-specs-output", $Specs)
}

& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_auto_refactor_plan.py") @Args

Write-Host "[OK] Auto-refactor plan JSON: $Json"
Write-Host "[OK] Auto-refactor plan MD: $Md"
if ($WritePatchSpecs) {
    Write-Host "[OK] Patch specs JSON: $Specs"
}
