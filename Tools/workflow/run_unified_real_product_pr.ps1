<#
.SYNOPSIS
  Run the IA-Carmine unified real product profile from a task Markdown file.

.DESCRIPTION
  This wrapper is the operator-facing product lane for the current architecture.
  It keeps PowerShell as a Windows launcher and delegates the real work to
  run_unified_local_ai_refactor.ps1.

  The profile enables the complete chain:

    task Markdown ingress
    heap/exchange entry
    GPU1 primary advisory planner
    GPU0 companion OpenVINO/tool worker
    NPU microoperation/efficiency peer
    shared memory / AI-to-AI evidence
    deterministic/script closure audit
    patch suggestion product
    prepare_review_pr product
    optional push and GitHub PR creation

  It does not merge, force-push, rewrite history, delete branches locally, deploy,
  touch secrets or run Blender/FFmpeg.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TaskFile,

    [string]$TaskBranch = "",
    [string]$Stamp = "",
    [string]$RepoRoot = ".",

    [ValidateSet("quick", "balanced", "deep", "custom")]
    [string]$RunIntensity = "deep",

    [string]$Model = "gpt-oss:20b",

    [switch]$Push,
    [switch]$CreatePr,
    [switch]$DraftPr,
    [switch]$UseGeneratedPatchSpecs,
    [switch]$AllowDirty,
    [switch]$SkipGitSync,
    [switch]$DryRun,

    [int]$ReviewPrMaxAppliedPatches = 5
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    param([string]$Root)
    Push-Location $Root
    try {
        $resolved = (& git rev-parse --show-toplevel 2>$null)
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($resolved)) {
            throw "This command must be run inside a Git repository checkout."
        }
        return (Resolve-Path $resolved.Trim()).Path
    }
    finally {
        Pop-Location
    }
}

function Get-RepoRelativePath {
    param(
        [string]$Root,
        [string]$PathValue
    )
    $full = [System.IO.Path]::GetFullPath($PathValue)
    $rootFull = [System.IO.Path]::GetFullPath($Root)
    if (-not $rootFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $rootFull += [System.IO.Path]::DirectorySeparatorChar
    }
    if ($full.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($rootFull.Length).Replace("\", "/")
    }
    return $full.Replace("\", "/")
}

function New-SafeSlug {
    param([string]$Value)
    $slug = [regex]::Replace($Value.ToLowerInvariant(), "[^a-z0-9._-]+", "-").Trim("-", ".", "_")
    if ([string]::IsNullOrWhiteSpace($slug)) { return "task" }
    return $slug
}

if ($CreatePr -and -not $Push) {
    throw "-CreatePr requires -Push because prepare_review_pr.py needs the branch on the remote"
}
if ($DraftPr -and -not $CreatePr) {
    throw "-DraftPr requires -CreatePr"
}

$ResolvedRepoRoot = Resolve-RepoRoot -Root $RepoRoot
Set-Location $ResolvedRepoRoot

$TaskPath = if ([System.IO.Path]::IsPathRooted($TaskFile)) {
    Resolve-Path -LiteralPath $TaskFile
}
else {
    Resolve-Path -LiteralPath (Join-Path $ResolvedRepoRoot $TaskFile)
}
$TaskRel = Get-RepoRelativePath -Root $ResolvedRepoRoot -PathValue $TaskPath.Path

if ([string]::IsNullOrWhiteSpace($Stamp)) {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

$Slug = New-SafeSlug ([System.IO.Path]::GetFileNameWithoutExtension($TaskPath.Path))
if ([string]::IsNullOrWhiteSpace($TaskBranch)) {
    $TaskBranch = "CARMINEai/real-product-$Slug-$Stamp"
}

$Launcher = Join-Path $ResolvedRepoRoot "Tools/workflow/run_unified_local_ai_refactor.ps1"
if (-not (Test-Path -LiteralPath $Launcher -PathType Leaf)) {
    throw "Unified launcher missing: $Launcher"
}

$Args = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", $Launcher,
    "-RepoRoot", $ResolvedRepoRoot,
    "-TaskFile", $TaskRel,
    "-TaskBranch", $TaskBranch,
    "-Stamp", $Stamp,
    "-Mode", "all",
    "-RunIntensity", $RunIntensity,
    "-Model", $Model,
    "-UseOllamaAdvisory",
    "-UsePrimaryAdvisoryProvider",
    "-RunMultistepProviderWorkflow",
    "-RunOllamaProbe",
    "-RunNpuProbe",
    "-RunNpuDecodeSmoke",
    "-RunOpenVinoGpu0Workload",
    "-BuildEvidence",
    "-GeneratePatchSpecs",
    "-BuildTaskPatchSuggestionReport",
    "-PrepareReviewPr",
    "-ReviewPrBranch", $TaskBranch,
    "-ReviewPrBaseBranch", "master",
    "-ReviewPrTitle", "feat(ai): real product review $Slug $Stamp",
    "-ReviewPrCommitMessage", "feat(ai): prepare real product review",
    "-ReviewPrMaxAppliedPatches", ([string]$ReviewPrMaxAppliedPatches),
    "-SaveInputsToMemoryDb"
)

if ($UseGeneratedPatchSpecs) {
    $Args += "-ReviewPrFromGeneratedPatchSpecs"
}
else {
    $Args += "-ReviewPrApplyDeterministicSuggestions"
}

if ($Push) { $Args += "-ReviewPrPush" }
if ($CreatePr) { $Args += "-ReviewPrCreate" }
if ($DraftPr) { $Args += "-ReviewPrDraft" }
if ($AllowDirty) { $Args += "-AllowDirty" }
if ($SkipGitSync) { $Args += "-SkipGitSync" }
if ($DryRun) { $Args += "-DryRun" }

Write-Host "=== IA-Carmine real product profile ==="
Write-Host "Repo: $ResolvedRepoRoot"
Write-Host "Task: $TaskRel"
Write-Host "Branch: $TaskBranch"
Write-Host "Stamp: $Stamp"
Write-Host "Run intensity: $RunIntensity"
Write-Host "Push: $Push"
Write-Host "Create PR: $CreatePr"
Write-Host "Use generated patch specs: $UseGeneratedPatchSpecs"
Write-Host ""
Write-Host "[RUN] powershell.exe $($Args -join ' ')"

& powershell.exe @Args
exit $LASTEXITCODE
