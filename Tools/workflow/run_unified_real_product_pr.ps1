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

  Architectural lane selection is internal to the profile. Runtime sizing,
  provider budget, observer and review-PR controls remain operator-facing
  parameters.

  It does not merge, forced ref updates, rewrite history, delete branches locally, deploy,
  touch secrets or run Blender/FFmpeg.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TaskFile,

    [string]$RepoRoot = ".",
    [string]$TaskBranch = "",
    [string]$Stamp = "",

    [ValidateSet("quick", "balanced", "deep", "custom")]
    [string]$RunIntensity = "deep",

    [string]$Model = "gpt-oss:20b",
    [string]$PythonExe = "",

    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [string]$KeepAlive = "35m",

    [ValidateSet('startup', 'deferred', 'live-seed-only', 'peer', 'post-gpu-provider', 'disabled')]
    [string]$NpuMicroStartMode = "peer",

    [int]$ProviderMaxContextChars = 0,
    [int]$ContextPackMaxTotalChars = 64000,
    [int]$ContextPackMaxFileChars = 4000,
    [int]$AgentStateMaxMemoryChars = 24000,
    [int]$MaxRecommendations = 20,
    [int]$MaxPatchPlans = 20,
    [int]$OfficialAdapterTimeoutSeconds = 1800,

    [switch]$OpenObserverConsoles,
    [switch]$OpenExtendedObserverConsoles,
    [int]$ObserverRefreshSeconds = 2,

    [switch]$UseGeneratedPatchSpecs,
    [int]$ReviewPrMaxAppliedPatches = 5,

    [switch]$Push,
    [switch]$CreatePr,
    [switch]$DraftPr,

    [switch]$AllowDirty,
    [switch]$SkipGitSync,
    [int]$PreflightTimeoutSeconds = 120,
    [switch]$DryRun
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

function Add-LauncherArg {
    param(
        [string]$Name,
        [string]$Value
    )
    $script:LauncherArgs += @($Name, $Value)
}

function Add-OptionalLauncherArg {
    param(
        [string]$Name,
        [string]$Value
    )
    if (-not [string]::IsNullOrWhiteSpace($Value)) {
        Add-LauncherArg -Name $Name -Value $Value
    }
}

function Add-LauncherSwitch {
    param(
        [string]$Name,
        [bool]$Enabled
    )
    if ($Enabled) {
        $script:LauncherArgs += $Name
    }
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

$PreflightGate = Join-Path $ResolvedRepoRoot "Tools/validation/run_real_product_preflight_gate.py"
if (-not (Test-Path -LiteralPath $PreflightGate -PathType Leaf)) {
    throw "Mandatory real product preflight gate missing: $PreflightGate"
}

$ResolvedPythonExe = $PythonExe
if ([string]::IsNullOrWhiteSpace($ResolvedPythonExe)) {
    if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON)) {
        $ResolvedPythonExe = $env:IA_CARMINE_PYTHON
    }
    elseif (Test-Path -LiteralPath (Join-Path $ResolvedRepoRoot ".venv/Scripts/python.exe") -PathType Leaf) {
        $ResolvedPythonExe = Join-Path $ResolvedRepoRoot ".venv/Scripts/python.exe"
    }
    else {
        $ResolvedPythonExe = "python"
    }
}

$PreflightOutput = Join-Path $ResolvedRepoRoot "output/validation/real_product_profile_preflight_$Stamp.json"
$PreflightMarkdown = Join-Path $ResolvedRepoRoot "output/validation/real_product_profile_preflight_$Stamp.md"

Write-Host "=== IA-Carmine mandatory real product preflight ==="
Write-Host "Preflight gate: $PreflightGate"
Write-Host "Preflight timeout seconds: $PreflightTimeoutSeconds"
Write-Host "Python: $ResolvedPythonExe"
& $ResolvedPythonExe $PreflightGate `
    --repo-root $ResolvedRepoRoot `
    --output $PreflightOutput `
    --markdown-output $PreflightMarkdown `
    --timeout-seconds $PreflightTimeoutSeconds

if ($LASTEXITCODE -ne 0) {
    throw "Mandatory real product preflight failed. See $PreflightOutput"
}

Write-Host "[OK] Mandatory real product preflight passed: $PreflightOutput"
Write-Host ""

$script:LauncherArgs = @(
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

Add-OptionalLauncherArg -Name "-PythonExe" -Value $PythonExe
Add-LauncherArg -Name "-BudgetMinutes" -Value ([string]$BudgetMinutes)
Add-LauncherArg -Name "-MaxRounds" -Value ([string]$MaxRounds)
Add-LauncherArg -Name "-FilesPerRound" -Value ([string]$FilesPerRound)
Add-LauncherArg -Name "-MaxContextFiles" -Value ([string]$MaxContextFiles)
Add-LauncherArg -Name "-MaxCharsPerFile" -Value ([string]$MaxCharsPerFile)
Add-LauncherArg -Name "-MaxNewTokens" -Value ([string]$MaxNewTokens)
Add-LauncherArg -Name "-KeepAlive" -Value $KeepAlive
Add-LauncherArg -Name "-NpuMicroStartMode" -Value $NpuMicroStartMode
Add-LauncherArg -Name "-ProviderMaxContextChars" -Value ([string]$ProviderMaxContextChars)
Add-LauncherArg -Name "-ContextPackMaxTotalChars" -Value ([string]$ContextPackMaxTotalChars)
Add-LauncherArg -Name "-ContextPackMaxFileChars" -Value ([string]$ContextPackMaxFileChars)
Add-LauncherArg -Name "-AgentStateMaxMemoryChars" -Value ([string]$AgentStateMaxMemoryChars)
Add-LauncherArg -Name "-MaxRecommendations" -Value ([string]$MaxRecommendations)
Add-LauncherArg -Name "-MaxPatchPlans" -Value ([string]$MaxPatchPlans)
Add-LauncherArg -Name "-OfficialAdapterTimeoutSeconds" -Value ([string]$OfficialAdapterTimeoutSeconds)
Add-LauncherArg -Name "-ObserverRefreshSeconds" -Value ([string]$ObserverRefreshSeconds)

Add-LauncherSwitch -Name "-OpenObserverConsoles" -Enabled ([bool]$OpenObserverConsoles)
Add-LauncherSwitch -Name "-OpenExtendedObserverConsoles" -Enabled ([bool]$OpenExtendedObserverConsoles)

if ($UseGeneratedPatchSpecs) {
    $script:LauncherArgs += "-ReviewPrFromGeneratedPatchSpecs"
}
else {
    $script:LauncherArgs += "-ReviewPrApplyDeterministicSuggestions"
}

Add-LauncherSwitch -Name "-ReviewPrPush" -Enabled ([bool]$Push)
Add-LauncherSwitch -Name "-ReviewPrCreate" -Enabled ([bool]$CreatePr)
Add-LauncherSwitch -Name "-ReviewPrDraft" -Enabled ([bool]$DraftPr)
Add-LauncherSwitch -Name "-AllowDirty" -Enabled ([bool]$AllowDirty)
Add-LauncherSwitch -Name "-SkipGitSync" -Enabled ([bool]$SkipGitSync)
Add-LauncherSwitch -Name "-DryRun" -Enabled ([bool]$DryRun)

Write-Host "=== IA-Carmine real product profile ==="
Write-Host "Repo: $ResolvedRepoRoot"
Write-Host "Task: $TaskRel"
Write-Host "Branch: $TaskBranch"
Write-Host "Stamp: $Stamp"
Write-Host "Run intensity: $RunIntensity"
Write-Host "Model: $Model"
Write-Host "Budget minutes: $BudgetMinutes"
Write-Host "Max rounds: $MaxRounds"
Write-Host "Files per round: $FilesPerRound"
Write-Host "Max context files: $MaxContextFiles"
Write-Host "Max chars per file: $MaxCharsPerFile"
Write-Host "Max new tokens: $MaxNewTokens"
Write-Host "NPU micro start mode: $NpuMicroStartMode"
Write-Host "Provider max context chars: $ProviderMaxContextChars"
Write-Host "Context pack max total chars: $ContextPackMaxTotalChars"
Write-Host "Context pack max file chars: $ContextPackMaxFileChars"
Write-Host "Agent state max memory chars: $AgentStateMaxMemoryChars"
Write-Host "Max recommendations: $MaxRecommendations"
Write-Host "Max patch plans: $MaxPatchPlans"
Write-Host "Official adapter timeout seconds: $OfficialAdapterTimeoutSeconds"
Write-Host "Preflight timeout seconds: $PreflightTimeoutSeconds"
Write-Host "Observer consoles: $OpenObserverConsoles"
Write-Host "Extended observer consoles: $OpenExtendedObserverConsoles"
Write-Host "Observer refresh seconds: $ObserverRefreshSeconds"
Write-Host "Push: $Push"
Write-Host "Create PR: $CreatePr"
Write-Host "Draft PR: $DraftPr"
Write-Host "Use generated patch specs: $UseGeneratedPatchSpecs"
Write-Host ""
Write-Host "[RUN] powershell.exe $($script:LauncherArgs -join ' ')"

& powershell.exe @script:LauncherArgs
exit $LASTEXITCODE
