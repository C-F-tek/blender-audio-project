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
    agent_review_prepare_pr product
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

$WorkflowRoot = Split-Path -Parent $PSScriptRoot
$PartsRoot = Join-Path $WorkflowRoot "run_unified_real_product_pr"
. (Join-Path $PartsRoot "support.ps1")
. (Join-Path $PartsRoot "process_gate_task.ps1")
. (Join-Path $PartsRoot "launcher_helpers.ps1")
. (Join-Path $PartsRoot "main.ps1")
