param(
    [string]$RepoRoot = ".",
    [Parameter(Mandatory = $true)]
    [string]$PatchSpecs,
    [string]$OutputDir = "output/validation/full0to10_auto_refactor_apply",
    [int]$MaxSpecs = 200,
    [switch]$Apply
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
$PatchSpecsPath = Resolve-RepoPath -Base $RepoRoot -PathValue $PatchSpecs
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$Json = Join-Path $OutputPath "full0to10_controlled_refactor_apply.json"
$Md = Join-Path $OutputPath "full0to10_controlled_refactor_apply.md"

$Args = @(
    "--repo-root", $RepoRoot,
    "--patch-specs", $PatchSpecsPath,
    "--max-specs", $MaxSpecs,
    "--output", $Json,
    "--markdown-output", $Md
)

if ($Apply) {
    $Args += "--apply"
}

& python (Join-Path $RepoRoot "Tools/ai/apply_full0to10_auto_refactor_patch_specs.py") @Args

Write-Host "[OK] Controlled refactor JSON: $Json"
Write-Host "[OK] Controlled refactor MD: $Md"
