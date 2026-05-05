param(
    [string]$RepoRoot = ".",
    [Parameter(Mandatory = $true)]
    [string]$PatchSpecs,
    [string]$OutputDir = "output/validation/full0to10_markdown_split_shadow",
    [int]$MaxSpecs = 200,
    [switch]$ApplyShadow
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

$Json = Join-Path $OutputPath "full0to10_markdown_split_shadow.json"
$Md = Join-Path $OutputPath "full0to10_markdown_split_shadow.md"

$Args = @(
    "--repo-root", $RepoRoot,
    "--patch-specs", $PatchSpecsPath,
    "--max-specs", $MaxSpecs,
    "--output", $Json,
    "--markdown-output", $Md
)

if ($ApplyShadow) {
    $Args += "--apply-shadow"
}

& python (Join-Path $RepoRoot "Tools/ai/apply_full0to10_markdown_split_patch_specs.py") @Args
if ($LASTEXITCODE -ne 0) {
    throw "Markdown split shadow failed with exit code $LASTEXITCODE"
}

Write-Host "[OK] Markdown split shadow JSON: $Json"
Write-Host "[OK] Markdown split shadow MD: $Md"
