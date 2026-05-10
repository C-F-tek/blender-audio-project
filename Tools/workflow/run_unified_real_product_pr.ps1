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
    [string]$TaskFile = "",
    [switch]$ProcessGateTask,
    [switch]$ValidateFinalReviewPrProduct,

    [string]$RepoRoot = ".",
    [string]$TaskBranch = "",
    [string]$Stamp = "",

    [ValidateSet("quick", "balanced", "deep", "custom")]
    [string]$RunIntensity = "deep",

    [string]$Model = "qwen2.5-coder:14b",
    [string]$PythonExe = "",

    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [string]$KeepAlive = "35m",

    [ValidateSet('startup', 'deferred', 'live-seed-only', 'peer', 'post-gpu-provider', 'disabled', 'final-provider')]
    [string]$NpuMicroStartMode = "startup",

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

    [switch]$ResetLocalAiArtifactsBeforeRun,
    [int]$ResetLocalAiArtifactsRetentionDays = 0,
    [switch]$ResetLocalAiMemoryBeforeRun,
    [switch]$ResetGeneratedIndexBeforeRun,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

class RealProductLauncherError {
    [string]$Code
    [string]$Message
    [int]$ExitCode

    RealProductLauncherError([string]$Code, [string]$Message, [int]$ExitCode) {
        $this.Code = $Code
        $this.Message = $Message
        $this.ExitCode = $ExitCode
    }
}

function Stop-RealProductLauncher {
    param(
        [string]$Code,
        [string]$Message,
        [int]$ExitCode = 2,
        [string]$Root = "",
        [string]$StampValue = "",
        [string]$DetailPath = ""
    )

    $ErrorObject = [RealProductLauncherError]::new($Code, $Message, $ExitCode)

    $EffectiveRoot = $Root
    if ([string]::IsNullOrWhiteSpace($EffectiveRoot)) {
        try {
            $MaybeRoot = (& git rev-parse --show-toplevel 2>$null)
            if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($MaybeRoot)) {
                $EffectiveRoot = $MaybeRoot.Trim()
            }
        }
        catch {
            $EffectiveRoot = ""
        }
    }
    if ([string]::IsNullOrWhiteSpace($EffectiveRoot)) {
        $EffectiveRoot = (Get-Location).Path
    }

    $EffectiveStamp = $StampValue
    if ([string]::IsNullOrWhiteSpace($EffectiveStamp)) {
        $EffectiveStamp = Get-Date -Format "yyyyMMdd-HHmmss"
    }

    $OutputDir = Join-Path $EffectiveRoot "output/validation"
    $JsonPath = Join-Path $OutputDir ("real_product_wrapper_error_{0}.json" -f $EffectiveStamp)
    $MarkdownPath = Join-Path $OutputDir ("real_product_wrapper_error_{0}.md" -f $EffectiveStamp)

    $Report = [ordered]@{
        schema_version = 1
        kind = "real_product_wrapper_error"
        generated_at = (Get-Date).ToString("s")
        repo_root = $EffectiveRoot.Replace("\", "/")
        stamp = $EffectiveStamp
        passed = $false
        error_code = $ErrorObject.Code
        message = $ErrorObject.Message
        detail_path = $DetailPath
        provider_execution_performed = $false
        patch_application_performed = $false
        source_writes_performed = $false
        exit_code = $ErrorObject.ExitCode
        errors = @($ErrorObject.Message)
        warnings = @()
    }

    try {
        New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
        ($Report | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $JsonPath -Encoding UTF8

        $Markdown = @(
            "# Real Product Wrapper Error",
            "",
            "- Passed: ``False``",
            "- Error code: ``$($ErrorObject.Code)``",
            "- Message: $($ErrorObject.Message)",
            "- Detail path: ``$DetailPath``",
            "- JSON report: ``$JsonPath``",
            "- Exit code: ``$($ErrorObject.ExitCode)``",
            ""
        ) -join "`n"
        Set-Content -LiteralPath $MarkdownPath -Value ($Markdown + "`n") -Encoding UTF8

        Write-Host "[ERROR] $($ErrorObject.Code): $($ErrorObject.Message)" -ForegroundColor Red
        Write-Host "[ERROR] Structured wrapper report: $JsonPath" -ForegroundColor Red
    }
    catch {
        Write-Host "[ERROR] $($ErrorObject.Code): $($ErrorObject.Message)" -ForegroundColor Red
        Write-Host "[ERROR] Failed to write structured wrapper report: $($_.Exception.Message)" -ForegroundColor Red
    }

    exit $ErrorObject.ExitCode
}

function Resolve-RepoRoot {
    param([string]$Root)
    Push-Location $Root
    try {
        $resolved = (& git rev-parse --show-toplevel 2>$null)
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($resolved)) {
            Stop-RealProductLauncher -Code "not_git_repository" -Message "This command must be run inside a Git repository checkout." -Root $Root -StampValue $Stamp
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

function New-HeapExchangeProcessGateTask {
    param(
        [string]$Root,
        [string]$StampValue
    )

    $TaskDir = Join-Path $Root "output/local_ai_task_inputs"
    New-Item -ItemType Directory -Force -Path $TaskDir | Out-Null

    $TaskPath = Join-Path $TaskDir ("heap-exchange-process-gate-{0}.md" -f $StampValue)

    $TaskContent = @"
# Heap Exchange Process Gate - $StampValue

## Objective

Run the complete IA-Carmine local-AI orchestration as a real process-product gate.

The run must prove that the system can enter the heap/exchange runtime layer, allow the internal runtime lanes to operate dynamically, and exit with observable exchange evidence plus concrete reviewable code/document changes.

This gate runs before implementing or enabling the runtime_debug_lab broker tool.

## Architecture rule

Do not guide the internal heap/exchange route step by step.

The center of the run is dynamic.

Inside the heap/exchange layer, the following runtime lanes may cooperate according to their current contracts and routing logic:

- GPU.0 workload support lane;
- GPU.1 reserved/provider lane when visible;
- NPU diagnostics/probe/decode lane;
- Ollama/provider advisory lane;
- official local AI adapter;
- context pack and agent-state packet;
- generated patch-spec proposal path;
- review-PR bridge.

The task defines the entry contract and exit contract only.

## Entry contract

The run must start from the unified launcher with:

- repository RepoPy only;
- clean working tree;
- Markdown task input;
- JSON/report validation;
- Python/tool inventory;
- semantic chunks;
- context pack;
- agent state;
- official local AI adapter;
- provider workflow;
- Ollama advisory/provider path;
- NPU diagnostic path selected by the launcher;
- OpenVINO GPU.0 workload evidence;
- workload quality routing;
- generated patch specs;
- review-PR bridge;
- unified heap/exchange chain contract;
- product separation;
- prepare_review_pr;
- GitHub draft PR creation.

## Exit contract

The run is successful only if all of these are true:

1. the official adapter completes successfully;
2. the GPU.0 workload report passes;
3. the provider/Ollama path completes successfully;
4. the heap/exchange layer emits observable exchange evidence;
5. generated patch specs are current-stamp and concrete;
6. at least one concrete deterministic operation is available for review;
7. product separation classifies the output as reviewable product, not supplemental telemetry only;
8. prepare_review_pr creates a draft PR with real source/doc changes;
9. the review PR final product contract validates the remote PR product.

Concrete patch operations may use only safe deterministic operations such as:

- replace_once;
- append_once;
- insert_after_once;
- insert_before_once;
- write_file.

Metadata-only patch specs are not acceptable as final product.

Evidence-only reports are not acceptable as final product.

## Preferred output

Prefer one small, safe, code-driven enhancement that improves the orchestration itself.

Good targets:

- heap/exchange event emission;
- exchange evidence manifest;
- generated patch-spec concreteness;
- review PR evidence summary;
- context-pack input/output contract;
- memory/context namespace manifest;
- broker/tool capability map for future runtime_debug_lab integration.

Do not implement or auto-enable runtime_debug_lab in this run.

## Hard failure policy

Do not soft-fail.

Do not continue past a broken gate.

If the run cannot produce exchange evidence or concrete patch specs, stop at the unified chain contract with a structured error.

If the run cannot create a real review PR product, stop before creating a misleading PR.

## Guardrails

Do not:

- merge to master;
- delete files;
- force-push;
- rewrite history;
- deploy;
- modify secrets, permissions, billing or visibility;
- execute Blender runtime;
- execute FFmpeg runtime;
- commit output/**;
- commit indexAI/code_chunks/**;
- commit *.db or *.sqlite;
- activate runtime_debug_lab automatically;
- create a fake patch_suggestion_json block just to pass validation;
- create docs-only filler changes unrelated to the detected process need.

## Validation expected in the generated PR

The generated PR body must include:

- touched files;
- line counts for touched code/scripts;
- PowerShell parser command for touched ps1 files;
- python -m py_compile command for touched Python files;
- relevant smoke validator command;
- git diff --check.

## Operator gate

Create only a draft PR.

Do not merge automatically.

If no concrete product emerges from the heap/exchange run, fail honestly.
"@

    Set-Content -LiteralPath $TaskPath -Value $TaskContent -Encoding UTF8
    return $TaskPath
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

function Invoke-LocalAiArtifactReset {
    param(
        [string]$Root,
        [string]$LauncherPath,
        [int]$RetentionDays,
        [bool]$IncludeMemory,
        [bool]$IncludeGeneratedIndex,
        [string]$PythonPath
    )

    if ($RetentionDays -lt 0) {
        Stop-RealProductLauncher -Code "invalid_reset_retention_days" -Message "-ResetLocalAiArtifactsRetentionDays must be zero or greater." -Root $Root -StampValue $Stamp
    }

    $ResetBefore = if ($RetentionDays -gt 0) {
        (Get-Date).AddDays(-$RetentionDays).Date
    }
    else {
        (Get-Date).AddSeconds(1)
    }

    $ResetTool = Join-Path $Root "Tools/workflow/run_local_ai_artifact_reset.py"
    if (-not (Test-Path -LiteralPath $ResetTool -PathType Leaf)) {
        Stop-RealProductLauncher -Code "bounded_reset_tool_missing" -Message "Bounded pre-run reset helper missing: $ResetTool" -Root $Root -StampValue $Stamp -DetailPath $ResetTool
    }

    $ResetJson = Join-Path $Root ("output/validation/prerun_local_ai_reset_{0}.json" -f $Stamp)
    $ResetMd = Join-Path $Root ("output/validation/prerun_local_ai_reset_{0}.md" -f $Stamp)

    $ResetArgs = @(
        $ResetTool,
        "--repo-root", $Root,
        "--before-date", $ResetBefore.ToString("s"),
        "--active-stamp", $Stamp,
        "--output", $ResetJson,
        "--markdown-output", $ResetMd
    )

    if (-not $DryRun) {
        $ResetArgs += @("--apply", "--confirm-reset-text", "DELETE LOCAL AI ARTIFACTS")
    }
    if ($IncludeMemory) {
        $ResetArgs += "--include-memory-reset"
    }
    if ($IncludeGeneratedIndex) {
        $ResetArgs += "--include-generated-index-reset"
    }

    Write-Host "=== IA-Carmine bounded pre-run local AI reset ==="
    Write-Host "Reset before: $($ResetBefore.ToString("s"))"
    Write-Host "Retention days: $RetentionDays"
    Write-Host "Include memory reset: $IncludeMemory"
    Write-Host "Include generated index reset: $IncludeGeneratedIndex"
    Write-Host "Active stamp: $Stamp"
    Write-Host "Report: $ResetJson"
    Write-Host "[RUN] $PythonPath $($ResetArgs -join ' ')"

    & $PythonPath @ResetArgs
    if ($LASTEXITCODE -ne 0) {
        Stop-RealProductLauncher -Code "local_ai_prerun_reset_failed" -Message "Pre-run local AI reset failed with exit code $LASTEXITCODE. See $ResetJson" -Root $Root -StampValue $Stamp -DetailPath $ResetJson
    }

    Write-Host "[OK] Bounded pre-run local AI reset completed: $ResetJson"
    Write-Host ""
}


if ($CreatePr -and -not $Push) {
    Stop-RealProductLauncher -Code "create_pr_requires_push" -Message "-CreatePr requires -Push because prepare_review_pr.py needs the branch on the remote" -Root $RepoRoot -StampValue $Stamp
}
if ($DraftPr -and -not $CreatePr) {
    Stop-RealProductLauncher -Code "draft_pr_requires_create_pr" -Message "-DraftPr requires -CreatePr" -Root $RepoRoot -StampValue $Stamp
}
if (($ResetLocalAiMemoryBeforeRun -or $ResetGeneratedIndexBeforeRun) -and -not $ResetLocalAiArtifactsBeforeRun) {
    Stop-RealProductLauncher -Code "reset_flags_require_artifact_reset" -Message "-ResetLocalAiMemoryBeforeRun and -ResetGeneratedIndexBeforeRun require -ResetLocalAiArtifactsBeforeRun." -Root $RepoRoot -StampValue $Stamp
}
if ($ResetLocalAiArtifactsRetentionDays -lt 0) {
    Stop-RealProductLauncher -Code "invalid_reset_retention_days" -Message "-ResetLocalAiArtifactsRetentionDays must be zero or greater." -Root $RepoRoot -StampValue $Stamp
}

if ($CreatePr) { $ValidateFinalReviewPrProduct = $true }

$ResolvedRepoRoot = Resolve-RepoRoot -Root $RepoRoot
Set-Location $ResolvedRepoRoot

if ([string]::IsNullOrWhiteSpace($Stamp)) {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

$GeneratedProcessGateTask = $false
if ([string]::IsNullOrWhiteSpace($TaskFile)) {
    if (-not $ProcessGateTask) {
        Stop-RealProductLauncher -Code "task_file_required" -Message "-TaskFile is required unless -ProcessGateTask is used." -Root $ResolvedRepoRoot -StampValue $Stamp
    }

    $TaskFile = New-HeapExchangeProcessGateTask -Root $ResolvedRepoRoot -StampValue $Stamp
    $GeneratedProcessGateTask = $true
}
elseif ($ProcessGateTask) {
    Write-Warning "-ProcessGateTask was provided together with -TaskFile; using the explicit task file."
}

$TaskPath = if ([System.IO.Path]::IsPathRooted($TaskFile)) {
    Resolve-Path -LiteralPath $TaskFile
}
else {
    Resolve-Path -LiteralPath (Join-Path $ResolvedRepoRoot $TaskFile)
}
$TaskRel = Get-RepoRelativePath -Root $ResolvedRepoRoot -PathValue $TaskPath.Path

if ($GeneratedProcessGateTask -and -not $AllowDirty) {
    $DirtyAfterGeneratedTask = (& git status --short)
    if (-not [string]::IsNullOrWhiteSpace($DirtyAfterGeneratedTask)) {
        Write-Host "[ERROR] Generated process gate task dirtied the repository:" -ForegroundColor Red
        Write-Host $DirtyAfterGeneratedTask
        Stop-RealProductLauncher -Code "generated_task_dirty_tree" -Message "Generated process gate task must live under ignored output/**." -Root $ResolvedRepoRoot -StampValue $Stamp
    }
}

$Slug = New-SafeSlug ([System.IO.Path]::GetFileNameWithoutExtension($TaskPath.Path))
if ([string]::IsNullOrWhiteSpace($TaskBranch)) {
    $TaskBranch = "CARMINEai/real-product-$Slug-$Stamp"
}

$Launcher = Join-Path $ResolvedRepoRoot "Tools/workflow/run_unified_local_ai_refactor.ps1"
if (-not (Test-Path -LiteralPath $Launcher -PathType Leaf)) {
    Stop-RealProductLauncher -Code "unified_launcher_missing" -Message "Unified launcher missing: $Launcher" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $Launcher
}

$PreflightGate = Join-Path $ResolvedRepoRoot "Tools/validation/run_real_product_preflight_gate.py"
if (-not (Test-Path -LiteralPath $PreflightGate -PathType Leaf)) {
    Stop-RealProductLauncher -Code "mandatory_preflight_missing" -Message "Mandatory real product preflight gate missing: $PreflightGate" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $PreflightGate
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

if ($ResetLocalAiArtifactsBeforeRun) {
    Invoke-LocalAiArtifactReset `
        -Root $ResolvedRepoRoot `
        -LauncherPath $Launcher `
        -RetentionDays $ResetLocalAiArtifactsRetentionDays `
        -IncludeMemory ([bool]$ResetLocalAiMemoryBeforeRun) `
        -IncludeGeneratedIndex ([bool]$ResetGeneratedIndexBeforeRun) `
        -PythonPath $ResolvedPythonExe
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
    Stop-RealProductLauncher -Code "mandatory_preflight_failed" -Message "Mandatory real product preflight failed. See $PreflightOutput" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $PreflightOutput
}

Write-Host "[OK] Mandatory real product preflight passed: $PreflightOutput"
Write-Host ""

$RealProductPostPreflightModes = "smoke,reset,md,json,python,chunks,context_pack,agent_state,official,provider,patch_specs,evidence,contract,full_validation"

$script:LauncherArgs = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", $Launcher,
    "-RepoRoot", $ResolvedRepoRoot,
    "-TaskFile", $TaskRel,
    "-TaskBranch", $TaskBranch,
    "-Stamp", $Stamp,
    "-Mode", $RealProductPostPreflightModes,
    "-RunIntensity", $RunIntensity,
    "-Model", $Model,
    "-Profile", "core",

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
    "-BuildRuntimeEvidenceCorrelation",
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

# IA-CARMINE-REAL-PRODUCT-OFFICIAL-MAX-CONTEXT-BEGIN
$OfficialAdapterMaxContextChars = $ProviderMaxContextChars
if ($OfficialAdapterMaxContextChars -le 0) {
    $OfficialAdapterMaxContextChars = 14000
}
Add-LauncherArg -Name "-MaxContextChars" -Value ([string]$OfficialAdapterMaxContextChars)
# IA-CARMINE-REAL-PRODUCT-OFFICIAL-MAX-CONTEXT-END
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
Write-Host "Official adapter max context chars: $OfficialAdapterMaxContextChars"
Write-Host "Context pack max total chars: $ContextPackMaxTotalChars"
Write-Host "Context pack max file chars: $ContextPackMaxFileChars"
Write-Host "Agent state max memory chars: $AgentStateMaxMemoryChars"
Write-Host "Max recommendations: $MaxRecommendations"
Write-Host "Max patch plans: $MaxPatchPlans"
Write-Host "Official adapter timeout seconds: $OfficialAdapterTimeoutSeconds"
Write-Host "Preflight timeout seconds: $PreflightTimeoutSeconds"
Write-Host "Pre-run local AI reset: $ResetLocalAiArtifactsBeforeRun"
Write-Host "Pre-run reset retention days: $ResetLocalAiArtifactsRetentionDays"
Write-Host "Pre-run memory reset: $ResetLocalAiMemoryBeforeRun"
Write-Host "Pre-run generated index reset: $ResetGeneratedIndexBeforeRun"
Write-Host "Observer consoles: $OpenObserverConsoles"
Write-Host "Extended observer consoles: $OpenExtendedObserverConsoles"
Write-Host "Observer refresh seconds: $ObserverRefreshSeconds"
Write-Host "Push: $Push"
Write-Host "Create PR: $CreatePr"
Write-Host "Draft PR: $DraftPr"
Write-Host "Use generated patch specs: $UseGeneratedPatchSpecs"
Write-Host "Post-preflight modes: $RealProductPostPreflightModes"
Write-Host ""
Write-Host "[RUN] powershell.exe $($script:LauncherArgs -join ' ')"

& powershell.exe @script:LauncherArgs
$LauncherExitCode = $LASTEXITCODE
if ($LauncherExitCode -ne 0) {
    exit $LauncherExitCode
}

if ($ValidateFinalReviewPrProduct -and -not $DryRun) {
    $FinalProductContract = Join-Path $ResolvedRepoRoot "Tools/validation/check_review_pr_final_product_contract.py"
    if (-not (Test-Path -LiteralPath $FinalProductContract -PathType Leaf)) {
        Stop-RealProductLauncher -Code "final_product_contract_missing" -Message "Review PR final product contract missing: $FinalProductContract" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $FinalProductContract
    }

    $ReviewReportCandidates = @()
    $ReviewReportCandidates += Get-ChildItem -Path (Join-Path $ResolvedRepoRoot "output/validation") -Filter ("review_pr_prepare_*_{0}.json" -f $Stamp) -File -ErrorAction SilentlyContinue
    $ReviewReportCandidates += Get-ChildItem -Path (Join-Path $ResolvedRepoRoot "output/validation") -Filter ("*review_pr_prepare*{0}*.json" -f $Stamp) -File -ErrorAction SilentlyContinue
    $ReviewReport = $ReviewReportCandidates |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($null -eq $ReviewReport) {
        Stop-RealProductLauncher -Code "review_pr_prepare_report_missing" -Message "review_pr_prepare report not found for stamp $Stamp" -Root $ResolvedRepoRoot -StampValue $Stamp
    }

    $FinalProductJson = Join-Path $ResolvedRepoRoot ("output/validation/review_pr_final_product_contract_remote_{0}.json" -f $Stamp)
    $FinalProductMd = Join-Path $ResolvedRepoRoot ("output/validation/review_pr_final_product_contract_remote_{0}.md" -f $Stamp)

    $FinalProductArgs = @(
        $FinalProductContract,
        "--repo-root", $ResolvedRepoRoot,
        "--review-pr-report", $ReviewReport.FullName,
        "--output", $FinalProductJson,
        "--markdown-output", $FinalProductMd
    )

    if ($CreatePr) {
        $FinalProductArgs += "--require-remote-pr"
    }

    & $ResolvedPythonExe @FinalProductArgs
    $FinalProductExitCode = $LASTEXITCODE
    if ($FinalProductExitCode -ne 0) {
        Stop-RealProductLauncher -Code "review_pr_final_product_contract_failed" -Message "Review PR final product contract failed. See $FinalProductJson" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $FinalProductJson
    }

    $ReviewPrReport = Get-Content -LiteralPath $ReviewReport.FullName -Raw | ConvertFrom-Json
    Write-Host "[OK] Review PR final product contract passed: $FinalProductJson"
    if (-not [string]::IsNullOrWhiteSpace([string]$ReviewPrReport.github_pr_url)) {
        Write-Host "[OK] Review PR URL: $($ReviewPrReport.github_pr_url)"
    }
    if (-not [string]::IsNullOrWhiteSpace([string]$ReviewPrReport.product_commit)) {
        Write-Host "[OK] Product commit: $($ReviewPrReport.product_commit)"
    }
}

exit 0
