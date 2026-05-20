<#
.SYNOPSIS
  Console-style unified launcher for IA-Carmine local AI refactor workflows.

.DESCRIPTION
  One independent entrypoint for local repository refactor/review runs.

  The task Markdown input stays the same. The operator chooses phases from the
  command line or from an interactive console prompt, similar to a console
  installer.

  Safe execution order:
    baseline -> smoke -> reset -> validation -> md -> json -> python -> chunks -> context_pack -> agent_state -> official -> provider -> patch_specs -> evidence -> contract -> full_validation

  The script is report/proposal-only by default. It never applies patches,
  commits, pushes, merges, runs Blender or runs FFmpeg.

  Reset mode is safe by default: it writes a reset plan only. Real deletion
  requires -ApplyReset and -ConfirmResetText "DELETE LOCAL AI ARTIFACTS".

.EXAMPLES
  python -m Tools.workflow run_unified_local_ai_refactor -Interactive
  python -m Tools.workflow run_unified_local_ai_refactor -Mode smoke,md,python,contract,full_validation
  python -m Tools.workflow run_unified_local_ai_refactor -Mode reset -ResetBeforeDate 2026-05-03
  python -m Tools.workflow run_unified_local_ai_refactor -Mode all -UseOllamaAdvisory -UsePrimaryAdvisoryProvider -GeneratePatchSpecs
#>
[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string[]]$Mode = @(),
    [string]$TaskFile = ".\docs\README.md",
    [string]$TaskBranch = "",
    [string]$Stamp = "",
    [string]$OutputDir = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [string]$AiPacketsRoot = "",
    [string]$AiPacketsDir = "",
    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "docs",
    [string]$Model = "qwen2.5-coder:14b",
    [ValidateSet("quick", "balanced", "deep", "custom")]
    [string]$RunIntensity = "balanced",
    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [string]$KeepAlive = "35m",
    [int]$NpuAuditorEveryRounds = 3,
    [int]$NpuAuditorTimeoutSeconds = 420,
    [int]$NpuMaxContextChars = 8000,
    [int]$NpuMaxPromptChars = 1200,
    [int]$NpuMaxNewTokens = 384,
    [int]$NpuFinalWaitSeconds = 180,
    [ValidateSet('startup', 'deferred', 'live-seed-only', 'peer', 'post-gpu-provider', 'disabled', 'final-provider')]
    [string]$NpuMicroStartMode = 'startup',
    [int]$MinRecommendations = 1,
    [int]$MinPatchPlans = 1,
    [int]$MaxRecommendations = 20,
    [int]$MaxPatchPlans = 20,
    [int]$RepositoryConsistencyMapWorkers = 8,
    [int]$ProviderMaxContextChars = 0,
    [int]$ContextPackMaxTotalChars = 64000,
    [int]$ContextPackMaxFileChars = 4000,
    [int]$AgentStateMaxMemoryChars = 24000,
    [int]$MaxContextChars = 12000,
    [string]$PythonExe = "",
    [switch]$Interactive,
    [switch]$SkipGitSync,
    [switch]$NoBranch,
    [switch]$AllowDirty,
    [switch]$DryRun,
    [switch]$NoStrictRealRunActivation,
    [switch]$Prod,
    [switch]$NoExecutionTail,
    [switch]$BuildWorkloadQualityReport,
    [switch]$NoOllamaProbe,
    [switch]$NoNpuProbe,
    [switch]$NoMultistepProvider,
    [switch]$NoWorkloadQuality,
    [switch]$NoMemoryWrite,
    [switch]$NoEvidence,
    [switch]$NoPatchSpecs,
    [switch]$UseOllamaAdvisory,
    [switch]$UsePrimaryAdvisoryProvider,
    [switch]$RunMultistepProviderWorkflow,
    [switch]$RunLegacyFullToolboxIntegrated,
    [switch]$RunLegacyNpuAuditorProvider,
    [switch]$RunOllamaProbe,
    [switch]$RunNpuProbe,
    [switch]$BuildEvidence,
    [switch]$GeneratePatchSpecs,
    [switch]$FullContextGoldenPath,
    [switch]$ContinueOnValidationError,
    [datetime]$ResetBeforeDate = [datetime]::MinValue,
    [switch]$ApplyReset,
    [string]$ConfirmResetText = "",
    [switch]$IncludeMemoryReset,
    [switch]$IncludeGeneratedIndexReset,
    [string]$MemoryDb = ".\\indexAI\\agent_memory\\agent_memory.sqlite",
    [switch]$SaveInputsToMemoryDb,
    [int]$MatrixWorkers = 12,
    [int]$RepeatCases = 2,
    [int]$OfficialAdapterTimeoutSeconds = 1800,
    [switch]$SkipOfficialAdapter,
    [switch]$RunOpenVinoGpu0Workload,
    [switch]$PrepareReviewPr,
    [string]$ReviewPrBranch = "",
    [string]$ReviewPrBaseBranch = "master",
    [string]$ReviewPrRemote = "origin",
    [string]$ReviewPrTitle = "",
    [string]$ReviewPrCommitMessage = "",
    [string[]]$ReviewPrIncludePath = @(),
    [switch]$ReviewPrPush,
    [switch]$ReviewPrCreate,
    [switch]$ReviewPrApplyDeterministicSuggestions,
    [switch]$BuildTaskPatchSuggestionReport,
    [switch]$ReviewPrFromGeneratedPatchSpecs,
    [string]$ReviewPrPatchSpecManifest = "",
    [int]$ReviewPrMaxAppliedPatches = 5,
    [switch]$ReviewPrRequireAllValidators,
    [switch]$ReviewPrDraft,
    [switch]$BuildRuntimeEvidenceCorrelation,
    [switch]$OpenObserverConsoles,
    [switch]$OpenExtendedObserverConsoles,
    [string]$ObserverOutputDir = "",
    [int]$ObserverRefreshSeconds = 2
)

$UnifiedLauncherScriptRoot = Split-Path -Parent $PSScriptRoot
$UnifiedLauncherPartsRoot = Join-Path $UnifiedLauncherScriptRoot "run_unified_local_ai_refactor"
foreach ($UnifiedLauncherPart in @("part-001.ps1", "part-002.ps1", "part-003.ps1", "part-004.ps1", "part-005.ps1")) {
    $UnifiedLauncherPartPath = Join-Path $UnifiedLauncherPartsRoot $UnifiedLauncherPart
    if (-not (Test-Path -LiteralPath $UnifiedLauncherPartPath -PathType Leaf)) {
        throw "Unified launcher part missing: $UnifiedLauncherPartPath"
    }
    . $UnifiedLauncherPartPath
}
