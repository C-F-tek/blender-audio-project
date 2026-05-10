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
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Interactive
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Mode smoke,md,python,contract,full_validation
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Mode reset -ResetBeforeDate 2026-05-03
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Mode all -UseOllamaAdvisory -UsePrimaryAdvisoryProvider -GeneratePatchSpecs
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
    [string]$Model = "gpt-oss:20b",
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
    [ValidateSet('startup', 'deferred', 'live-seed-only', 'peer', 'post-gpu-provider', 'disabled')]
    [string]$NpuMicroStartMode = 'deferred',
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
    [switch]$Full0To10,
    [switch]$NoStrictRealRunActivation,
    [switch]$Prod,
    [switch]$NoExecutionTail,
    [switch]$BuildWorkloadQualityReport,
    [switch]$NoOllamaProbe,
    [switch]$NoNpuProbe,
    [switch]$NoNpuDecodeSmoke,
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
    [switch]$RunNpuDecodeSmoke,
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
    [int]$RepeatCases = 2
,
    [switch]$LightFull0To10,
    [string]$LightFull0To10OutputDir = "output/validation/unified_run_light_legacy_alias",
    [switch]$LightFull0To10NoExternalProbes,
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

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Script:UnifiedLauncherCurrentPhase = "startup"
$Script:UnifiedLauncherFailureMessage = ""

if ($ContinueOnValidationError) {
    [Console]::Error.WriteLine("-ContinueOnValidationError is forbidden for unified launcher runs. Fix the failing phase instead of allowing a soft-failed run to complete.")
    exit 2
}

# IA-CARMINE-UNIFIED-PHASE-VISIBILITY-IMPORT-BEGIN
$UnifiedPhaseVisibilityScript = Join-Path $PSScriptRoot "unified_phase_visibility.ps1"
if (Test-Path -LiteralPath $UnifiedPhaseVisibilityScript -PathType Leaf) {
    . $UnifiedPhaseVisibilityScript
} else {
    Write-Warning "Unified phase visibility helper not found: $UnifiedPhaseVisibilityScript"
}
# IA-CARMINE-UNIFIED-PHASE-VISIBILITY-IMPORT-END

# IA-CARMINE-UNIFIED-RUN-OBSERVER-IMPORT-BEGIN
$UnifiedRunObserverScript = Join-Path $PSScriptRoot "unified_run_observer.ps1"
if (Test-Path -LiteralPath $UnifiedRunObserverScript -PathType Leaf) {
    . $UnifiedRunObserverScript
} else {
    Write-Warning "Unified run observer helper not found: $UnifiedRunObserverScript"
}
# IA-CARMINE-UNIFIED-RUN-OBSERVER-IMPORT-END
# IA-CARMINE-HEAP-EXCHANGE-REVIEW-BRIDGE-IMPORT-BEGIN
$UnifiedHeapExchangeReviewBridgeScript = Join-Path $PSScriptRoot "heap_exchange_review_bridge.ps1"
if (Test-Path -LiteralPath $UnifiedHeapExchangeReviewBridgeScript -PathType Leaf) {
    . $UnifiedHeapExchangeReviewBridgeScript
} else {
    Write-Warning "Heap exchange review bridge helper not found: $UnifiedHeapExchangeReviewBridgeScript"
}
# IA-CARMINE-HEAP-EXCHANGE-REVIEW-BRIDGE-IMPORT-END
# IA-CARMINE-LIGHTFULL0TO10-DISPATCH-BEGIN
if ($LightFull0To10) {
    $LightProfileScript = Join-Path $PSScriptRoot "run_unified_light_full0to10_profile.ps1" # legacy filename; compatibility wrapper only
    if (-not (Test-Path $LightProfileScript)) {
        throw "LightFull0To10 legacy compatibility wrapper not found: $LightProfileScript"
    }

    if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
        $ResolvedLightRepoRoot = (Resolve-Path ".").Path
    } else {
        $ResolvedLightRepoRoot = (Resolve-Path $RepoRoot).Path
    }

    $LightArgs = @(
        "-RepoRoot", $ResolvedLightRepoRoot,
        "-OutputDir", $LightFull0To10OutputDir
    )

    if (-not $PSBoundParameters.ContainsKey("LightFull0To10NoExternalProbes") -or $LightFull0To10NoExternalProbes) {
        $LightArgs += "-NoExternalProbes"
    }

    Write-Host "[UnifiedRun][LegacyAlias:LightFull0To10] Dispatching evidence-only compatibility wrapper..."
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $LightProfileScript @LightArgs
    exit $LASTEXITCODE
}
# IA-CARMINE-LIGHTFULL0TO10-DISPATCH-END

$ModeOrder = @(
    "smoke", "reset", "validation", "md", "json", "python", "chunks", "context_pack",
    "agent_state", "official", "provider", "patch_specs", "evidence", "contract", "full_validation"
)

$ModeDescriptions = [ordered]@{
    smoke = "Fast smoke checks: git diff --check and startup_check.py when available."
    reset = "Plan cleanup for old local artifacts/output; deletion requires explicit confirmation."
    validation = "Run broad local validation after refactor when the project wrapper exists."
    md = "Build Markdown inventory, docs link report and Markdown cleanup evidence."
    json = "Validate task-scoped JSON/report contracts for reports produced in this run."
    python = "Build full script/tool inventory with CSV/Markdown review surfaces."
    chunks = "Build/select semantic chunks for focused code/document context."
    context_pack = "Build bounded AI context pack for backend/core/provider work."
    agent_state = "Build local agent-state packet and optional memory handoff context."
    official = "Run the official project-owned local AI task pipeline adapter."
    provider = "Run explicit advisory/provider path; Ollama remains advisory."
    patch_specs = "Generate review-only patch specs from proposals. No apply."
    evidence = "Build compact GitHub evidence bundle when explicitly requested."
    contract = "Run current task-scoped report-contract validation."
    full_validation = "Final git diff/status and post-run consistency checks."
    all = "Run every available phase in safe order."
}

$ModeAliases = @{
    py = "python"; ps1 = "python"; scripts = "python"; script = "python"
    markdown = "md"; docs = "md"; documentazione = "md"
    report = "json"; reports = "json"; json_contract = "json"
    provider_advisory = "provider"; ollama = "provider"; gpu = "provider"; npu = "provider"
    planner = "official"; patch_planner = "patch_specs"; patch_plan = "patch_specs"
    tests = "validation"; test = "validation"; validate = "validation"; validate_all = "full_validation"
    clean = "reset"; cleanup = "reset"; purge = "reset"; pulizia = "reset"
    full = "all"
}

function Show-LauncherIntro {
    Write-Host ""
    Write-Host "IA-Carmine Unified Local AI Refactor Launcher" -ForegroundColor Cyan
    Write-Host "================================================"
    Write-Host "One task Markdown input; selectable phases; report/proposal-only by default."
    Write-Host ""
    Write-Host "Capabilities:"
    Write-Host "  - Markdown inventory, link validation, long/corrupt MD review;"
    Write-Host "  - script/tool inventory for Python, PowerShell, shell, batch files;"
    Write-Host "  - JSON/report-contract validation;"
    Write-Host "  - smoke and full local validation wrappers;"
    Write-Host "  - semantic chunks, context packs and agent-state packets;"
    Write-Host "  - official local AI pipeline adapter;"
    Write-Host "  - optional Ollama/provider advisory and review-only patch specs;"
    Write-Host "  - reset planning for old local artifacts, output, memory and generated context."
    Write-Host ""
    Write-Host "Guardrails: no patch apply, no commit, no push, no merge, no Blender, no FFmpeg."
    Write-Host "Reset guardrail: no delete unless -ApplyReset and exact -ConfirmResetText are supplied."
    Write-Host "Python policy: set PYTHONPATH to repo root; use -PythonExe, IA_CARMINE_PYTHON, .venv, venv; auto-bootstrap .venv with py -3.12/3.13 before fallback."
    Write-Host "Unified run: -Full0To10 is a legacy compatibility alias for the full unified lane set; use explicit lanes/-No* flags for precise control."
    Write-Host "Debug tail: enabled by default; use -Prod to disable transcript and execution-tail evidence."
    Write-Host "Startup check output: Tools/workflow/startup_check.py supports --output, --text-output and --repo-root."
    Write-Host "AI packets output: use -AiPacketsRoot/-AiPacketsDir; default is output/ai_packets/<DataStamp>."
    Write-Host "Strict real-run activation: every non-smoke/non-reset real run enters the unified heap/exchange model unless explicit -No* flags disable lanes."
    Write-Host "Full run lanes include provider probes, advisory, workload quality, evidence, patch specs and memory input persistence when allowed."
    Write-Host ""
}

function Show-ModeCatalog {
    Write-Host "Available modes:" -ForegroundColor Cyan
    foreach ($name in $ModeDescriptions.Keys) {
        Write-Host ("  {0,-15} {1}" -f $name, $ModeDescriptions[$name])
    }
    Write-Host ""
    Write-Host "Examples: smoke,md,python,contract,full_validation | reset | md,json,python,official,patch_specs | all"
    Write-Host ""
}

function Normalize-ModeList {
    param([string[]]$Values)
    $items = @()
    foreach ($value in $Values) {
        if ([string]::IsNullOrWhiteSpace($value)) { continue }
        foreach ($part in ([string]$value).Split(",")) {
            $item = $part.Trim().ToLowerInvariant()
            if ([string]::IsNullOrWhiteSpace($item)) { continue }
            if ($ModeAliases.ContainsKey($item)) { $item = $ModeAliases[$item] }
            $items += $item
        }
    }
    if ($items.Count -eq 0) { return @() }
    if ($items -contains "all") { return @($ModeOrder) }
    $unknown = @($items | Where-Object { $ModeDescriptions.Keys -notcontains $_ })
    if ($unknown.Count -gt 0) { throw "Unknown mode(s): $($unknown -join ', '). Use -Interactive to list modes." }
    $ordered = @()
    foreach ($known in $ModeOrder) {
        if ($items -contains $known -and $ordered -notcontains $known) { $ordered += $known }
    }
    return $ordered
}

function Read-InteractiveModes {
    Show-ModeCatalog
    $answer = Read-Host "Select modes"
    return Normalize-ModeList @($answer)
}

function Invoke-Git {
    param([string[]]$GitArgs)
    Write-Host "[git] git $($GitArgs -join ' ')"
    if ($DryRun) { return }
    & git @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "git command failed: git $($GitArgs -join ' ')" }
}

function Invoke-Checked {
    param([string]$Label, [scriptblock]$Block, [switch]$SoftFail)
    Write-Host ""
    Write-Host "=== $Label ==="
    $Script:UnifiedLauncherCurrentPhase = $Label

    if (Get-Command Write-UnifiedRunProgressEvent -ErrorAction SilentlyContinue) {
        Write-UnifiedRunProgressEvent -Phase $Label -Status "started"
    }

    if ($DryRun) {
        Write-Host "[DRY-RUN] Skipped execution."
        if (Get-Command Write-UnifiedRunProgressEvent -ErrorAction SilentlyContinue) {
            Write-UnifiedRunProgressEvent -Phase $Label -Status "dry_run_skipped"
        }
        return $true
    }

    & $Block

    if ($LASTEXITCODE -ne 0) {
        if (Get-Command Write-UnifiedRunProgressEvent -ErrorAction SilentlyContinue) {
            Write-UnifiedRunProgressEvent -Phase $Label -Status "failed" -Message ("exit_code={0}" -f $LASTEXITCODE)
        }
        $Script:UnifiedLauncherFailureMessage = "$Label failed with exit code $LASTEXITCODE"
        if ($SoftFail) {
            Write-Warning "$Label failed with exit code $LASTEXITCODE"
            return $false
        }
        throw "$Label failed with exit code $LASTEXITCODE"
    }

    if (Get-Command Write-UnifiedRunProgressEvent -ErrorAction SilentlyContinue) {
        Write-UnifiedRunProgressEvent -Phase $Label -Status "passed"
    }

    return $true
}

function Get-UnifiedLauncherErrorAction {
    param([string]$Message)

    if ([string]::IsNullOrWhiteSpace($Message)) {
        return "Inspect the preceding launcher phase output and rerun with a clean working tree."
    }

    if ($Message -match "working tree is not clean") {
        return "Commit, stash, restore generated files, or rerun with -AllowDirty only when the dirty tree is intentional."
    }

    if ($Message -match "Rejected non-repository Python|RepoPy|IA_CARMINE_PYTHON") {
        return "Use repository .venv only: `$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path; pass -PythonExe `$RepoPy."
    }

    if ($Message -match "Ollama|ollama|provider|advisory") {
        return "Check Ollama service/model availability and provider logs before rerunning the full orchestration."
    }

    if ($Message -match "patch spec|patch_specs|generated patch") {
        return "Inspect current-stamp output/patch_specs manifest and generated patch-spec apply report."
    }

    if ($Message -match "Prepare review branch|review PR|no staged product changes") {
        return "Inspect review_pr_prepare report and verify generated patch specs produced concrete source/doc changes."
    }

    return "Inspect the reported file, line, phase report, and stderr/stdout logs for this phase."
}

function Write-UnifiedLauncherStructuredError {
    param([object]$ErrorRecord)

    $message = ""
    $location = ""
    $stack = ""

    if ($null -ne $ErrorRecord) {
        if ($null -ne $ErrorRecord.Exception) {
            $message = [string]$ErrorRecord.Exception.Message
        }

        if ($null -ne $ErrorRecord.InvocationInfo) {
            $location = "{0}:{1}" -f $ErrorRecord.InvocationInfo.ScriptName, $ErrorRecord.InvocationInfo.ScriptLineNumber
        }

        if (-not [string]::IsNullOrWhiteSpace($ErrorRecord.ScriptStackTrace)) {
            $stack = [string]$ErrorRecord.ScriptStackTrace
        }
    }

    if ([string]::IsNullOrWhiteSpace($message)) {
        $message = $Script:UnifiedLauncherFailureMessage
    }

    $action = Get-UnifiedLauncherErrorAction -Message $message

    [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] Phase: $Script:UnifiedLauncherCurrentPhase")
    [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] Message: $message")

    if (-not [string]::IsNullOrWhiteSpace($location)) {
        [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] Location: $location")
    }

    if (-not [string]::IsNullOrWhiteSpace($action)) {
        [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] Action: $action")
    }

    if (-not [string]::IsNullOrWhiteSpace($stack)) {
        [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] Stack: $stack")
    }
}

function Resolve-RepoRoot {
    $root = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) { throw "Run inside a Git repository checkout." }
    return (Resolve-Path $root.Trim()).Path
}

function Assert-FileExists {
    param([string]$PathValue)
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) { throw "required file missing: $PathValue" }
}

function Test-ModeEnabled {
    param([string]$Name)
    return $ResolvedModes -contains $Name
}

function Add-ExistingContextFile {
    param([string[]]$Current, [string]$PathValue)
    if ([string]::IsNullOrWhiteSpace($PathValue)) { return $Current }
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) { return $Current }
    $normalized = $PathValue.Replace("\", "/").TrimStart("./")
    if ($Current -contains $normalized) { return $Current }
    return @($Current + $normalized)
}

function Add-OptionalModeWarning {
    param([string]$ModeName, [string]$ToolPath, [ref]$Warnings)
    if ((Test-ModeEnabled $ModeName) -and -not (Test-Path -LiteralPath $ToolPath -PathType Leaf)) {
        $Warnings.Value += "Mode '$ModeName' requested but tool is missing: $ToolPath"
    }
}

function Split-ReviewPrIncludePaths {
    param([string[]]$Values)
    $items = @()
    foreach ($value in @($Values)) {
        foreach ($part in ([string]$value -split ",")) {
            $normalized = $part.Trim().Trim("'").Trim('"')
            if (-not [string]::IsNullOrWhiteSpace($normalized) -and $items -notcontains $normalized) {
                $items += $normalized
            }
        }
    }
    return $items
}

function Convert-ToRepoRelativePath {
    param([string]$Root, [string]$PathValue)
    $full = [System.IO.Path]::GetFullPath($PathValue)
    $rootFull = [System.IO.Path]::GetFullPath($Root)
    if (-not $rootFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) { $rootFull += [System.IO.Path]::DirectorySeparatorChar }
    if ($full.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($rootFull.Length).Replace("\", "/")
    }
    return $full.Replace("\", "/")
}

function Get-ResetCandidates {
    param([string]$Root, [datetime]$BeforeDate, [switch]$IncludeMemory, [switch]$IncludeGeneratedIndex)
    $patterns = @(
        @{ category = "local_ai_runs"; path = "output/local_ai_runs" },
        @{ category = "ai_pipeline"; path = "output/ai_pipeline" },
        @{ category = "validation_reports"; path = "output/validation" },
        @{ category = "ai_context_packs"; path = "output/ai_context_packs" },
        @{ category = "patch_specs"; path = "output/patch_specs" }
    )
    if ($IncludeMemory) {
        $patterns += @{ category = "agent_memory"; path = "indexAI/agent_memory" }
    }
    if ($IncludeGeneratedIndex) {
        $patterns += @{ category = "generated_index_context"; path = "indexAI/code_chunks" }
        $patterns += @{ category = "generated_project_chunks"; path = "indexAI/project_code_chunks" }
    }

    $items = @()
    foreach ($entry in $patterns) {
        $rootPath = Join-Path $Root $entry.path
        if (-not (Test-Path -LiteralPath $rootPath)) { continue }
        $files = Get-ChildItem -LiteralPath $rootPath -Recurse -File -Force -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            if ($BeforeDate -ne [datetime]::MinValue -and $file.LastWriteTime -ge $BeforeDate) { continue }
            $items += [ordered]@{
                path = Convert-ToRepoRelativePath $Root $file.FullName
                category = $entry.category
                last_write_time = $file.LastWriteTime.ToString("o")
                size_bytes = $file.Length
            }
        }
    }
    return @($items | Sort-Object category, path)
}

function Write-ResetPlan {
    param(
        [object[]]$Candidates,
        [string]$OutputJson,
        [string]$OutputMd,
        [datetime]$BeforeDate,
        [bool]$Apply,
        [string]$Root
    )

    $totalBytes = 0
    foreach ($item in @($Candidates)) {
        $totalBytes += [int64]$item.size_bytes
    }

    $resetBefore = $null
    $resetBeforeText = "not set"
    if ($BeforeDate -ne [datetime]::MinValue) {
        $resetBefore = $BeforeDate.ToString("o")
        $resetBeforeText = $resetBefore
    }

    $report = [ordered]@{
        schema_version = 1
        kind = "local_ai_reset_plan"
        repo_root = $Root
        passed = $true
        apply_reset = $Apply
        reset_before_date = $resetBefore
        candidate_count = @($Candidates).Count
        total_size_bytes = $totalBytes
        candidates = $Candidates
        warnings = @("Reset mode is report-only unless -ApplyReset and exact -ConfirmResetText are supplied.")
        errors = @()
    }

    ($report | ConvertTo-Json -Depth 8) |
        Set-Content -LiteralPath $OutputJson -Encoding UTF8

    $lines = New-Object System.Collections.Generic.List[string]
    [void]$lines.Add("# Local AI Reset Plan")
    [void]$lines.Add("")
    [void]$lines.Add(("- Apply reset: ``{0}``" -f $Apply))
    [void]$lines.Add(("- Candidate count: ``{0}``" -f @($Candidates).Count))
    [void]$lines.Add(("- Total bytes: ``{0}``" -f $totalBytes))
    [void]$lines.Add(("- Reset before date: ``{0}``" -f $resetBeforeText))
    [void]$lines.Add("")
    [void]$lines.Add("| Path | Category | Last write time | Size bytes |")
    [void]$lines.Add("|---|---|---|---:|")

    foreach ($item in @($Candidates)) {
        [void]$lines.Add((
            "| ``{0}`` | ``{1}`` | ``{2}`` | {3} |" -f
            $item.path,
            $item.category,
            $item.last_write_time,
            $item.size_bytes
        ))
    }

    $lines | Set-Content -LiteralPath $OutputMd -Encoding UTF8
}



function Resolve-PythonExe {
    param(
        [string]$Requested,
        [string]$Root
    )

    $candidates = @()

    if (-not [string]::IsNullOrWhiteSpace($Requested)) {
        $candidates += $Requested
    }

    if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON)) {
        $candidates += $env:IA_CARMINE_PYTHON
    }

    $localVenv = Join-Path $Root ".venv"
    $localVenvPython = Join-Path $localVenv "Scripts/python.exe"

    $candidates += @(
        $localVenvPython,
        (Join-Path $Root "venv/Scripts/python.exe"),
        (Join-Path $Root ".venv314/Scripts/python.exe")
    )

    foreach ($candidate in $candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }

        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    if (-not (Test-Path -LiteralPath $localVenvPython -PathType Leaf)) {
        $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
        if ($pyLauncher) {
            Write-Host "[INFO] Local .venv not found; attempting bootstrap with py -3.12."
            & py -3.12 -m venv $localVenv

            if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $localVenvPython -PathType Leaf)) {
                Write-Host "[INFO] py -3.12 bootstrap failed or unavailable; attempting py -3.13."
                & py -3.13 -m venv $localVenv
            }

            if (Test-Path -LiteralPath $localVenvPython -PathType Leaf) {
                return (Resolve-Path -LiteralPath $localVenvPython).Path
            }
        }
    }
    throw "No repository-owned Python interpreter found. Set -PythonExe or IA_CARMINE_PYTHON to a Python executable under the repository, or create .venv/Scripts/python.exe."
}

function Invoke-Python {
    param([string[]]$PythonArgs)
    & $ResolvedPythonExe @PythonArgs
}


function Get-OptionalPropertyValue {
    param(
        [object]$Object,
        [string]$Name,
        [object]$Default = ""
    )

    if ($null -eq $Object) {
        return $Default
    }

    $Property = $Object.PSObject.Properties[$Name]
    if ($null -eq $Property) {
        return $Default
    }

    if ($null -eq $Property.Value) {
        return $Default
    }

    return $Property.Value
}

function Write-ProviderWorkloadReportsFromProbe {
    param(
        [string]$ProbeReport,
        [string]$OllamaReport,
        [string]$NpuReport
    )

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OllamaReport) | Out-Null

    if (-not (Test-Path -LiteralPath $ProbeReport -PathType Leaf)) {
        throw "Provider probe report missing: $ProbeReport"
    }

    $Probe = Get-Content -LiteralPath $ProbeReport -Raw | ConvertFrom-Json
    $Ollama = @($Probe.lane_reports | Where-Object { $_.lane -eq "ollama" } | Select-Object -First 1)
    $Npu = @($Probe.lane_reports | Where-Object { $_.lane -eq "npu" } | Select-Object -First 1)

    if ($Ollama.Count -gt 0 -and [bool](Get-OptionalPropertyValue -Object $Ollama[0] -Name "passed" -Default $false)) {
        $OllamaLines = @(
            "# Ollama GPU Real Workload Report",
            "",
            "Generated by unified launcher from explicit provider probe.",
            "Lane: ollama",
            "Provider: Ollama",
            "Compute lane: GPU/CUDA",
            "Intended role: primary advisory only after workload quality routing passes.",
            ("Provider execution performed: {0}" -f (Get-OptionalPropertyValue -Object $Ollama[0] -Name "provider_execution_performed" -Default $false)),
            ("Probe passed: {0}" -f (Get-OptionalPropertyValue -Object $Ollama[0] -Name "passed" -Default $false)),
            ("Selected model: {0}" -f (Get-OptionalPropertyValue -Object $Ollama[0] -Name "selected_model" -Default "")),
            "",
            "Captured text preview:",
            ("{0}" -f (Get-OptionalPropertyValue -Object $Ollama[0] -Name "text_preview" -Default "")),
            "",
            "This report wraps a real provider probe result for workload quality routing.",
            "No patches, source writes, Blender or FFmpeg execution are performed by this report."
        )
        $OllamaLines | Set-Content -LiteralPath $OllamaReport -Encoding UTF8
    } else {
        Write-Warning "Ollama probe did not pass; Ollama workload report not written."
        if (Test-Path -LiteralPath $OllamaReport -PathType Leaf) {
            Remove-Item -LiteralPath $OllamaReport -Force
        }
    }

    if ($Npu.Count -gt 0) {
        $NpuLines = @(
            "# NPU OpenVINO Real Workload Report",
            "",
            "Generated by unified launcher from explicit provider probe.",
            "Lane: npu",
            "Provider: OpenVINO NPU",
            "Compute lane: NPU",
            "Intended role: probe, guardrail, decode diagnostic or knowledge-broker support.",
            "This lane is not promoted to primary advisory by this report.",
            ("Provider execution performed: {0}" -f (Get-OptionalPropertyValue -Object $Npu[0] -Name "provider_execution_performed" -Default $false)),
            ("Probe passed: {0}" -f (Get-OptionalPropertyValue -Object $Npu[0] -Name "passed" -Default $false)),
            ("Probe error: {0}" -f (Get-OptionalPropertyValue -Object $Npu[0] -Name "error" -Default "")),
            "",
            "Captured raw preview:",
            ("{0}" -f (Get-OptionalPropertyValue -Object $Npu[0] -Name "raw_preview" -Default "")),
            "",
            "This report wraps a real NPU probe result for workload quality routing.",
            "No patches, source writes, Blender or FFmpeg execution are performed by this report."
        )
        $NpuLines | Set-Content -LiteralPath $NpuReport -Encoding UTF8
    } else {
        Write-Warning "NPU probe entry missing; NPU workload report not written."
        if (Test-Path -LiteralPath $NpuReport -PathType Leaf) {
            Remove-Item -LiteralPath $NpuReport -Force
        }
    }
}


# IA_CARMINE_EXECUTION_TAIL_PATCH_BEGIN
$Script:UnifiedLauncherTranscriptPath = $null
$Script:UnifiedLauncherTranscriptStarted = $false
$Script:UnifiedLauncherExecutionTailWritten = $false

function Start-UnifiedLauncherExecutionTranscript {
    param(
        [string]$StampValue,
        [string]$Root,
        [bool]$ProdMode
    )

    if ($ProdMode) {
        Write-Host "[INFO] Prod mode: unified launcher debug transcript/tail evidence disabled."
        return
    }

    if ($Script:UnifiedLauncherTranscriptStarted) {
        return
    }

    $safeStamp = $StampValue
    if ([string]::IsNullOrWhiteSpace($safeStamp)) {
        $safeStamp = Get-Date -Format "yyyyMMdd-HHmmss"
    }

    $transcriptOutputDir = "output"
    if (-not [string]::IsNullOrWhiteSpace($Script:UnifiedLauncherOutputDir)) {
        $transcriptOutputDir = $Script:UnifiedLauncherOutputDir
    }
    $transcriptDir = Join-Path $Root (Join-Path $transcriptOutputDir ("local_ai_runs/{0}_unified_launcher_transcript" -f $safeStamp))
    $transcriptPath = Join-Path $transcriptDir ("unified_launcher_console_{0}.log" -f $safeStamp)

    try {
        New-Item -ItemType Directory -Force -Path $transcriptDir | Out-Null
        Start-Transcript -Path $transcriptPath -Force | Out-Null
        $Script:UnifiedLauncherTranscriptPath = $transcriptPath
        $Script:UnifiedLauncherTranscriptStarted = $true
        Write-Host "[INFO] Unified launcher transcript: $transcriptPath"
    } catch {
        Write-Warning ("Could not start unified launcher transcript: {0}" -f $_.Exception.Message)
        $Script:UnifiedLauncherTranscriptPath = $null
        $Script:UnifiedLauncherTranscriptStarted = $false
    }
}

function Write-UnifiedLauncherExecutionTailEvidence {
    param(
        [string]$StampValue,
        [string]$Root,
        [string]$RunDirValue,
        [string]$ManifestPathValue,
        [string[]]$ResolvedModesValue,
        [string[]]$ReportFilesValue,
        [string[]]$ContextFilesValue,
        [bool]$ProviderExecutionRequested,
        [bool]$PatchSpecsRequested,
        [bool]$ProdMode,
        [string]$FailureMessage = ""
    )

    if ($ProdMode) {
        Write-Host "[INFO] Prod mode: unified launcher execution-tail evidence disabled."
        return
    }

    if ($Script:UnifiedLauncherExecutionTailWritten) {
        Write-Host "[INFO] Unified launcher execution-tail evidence already written."
        return
    }

    if ($Script:UnifiedLauncherTranscriptStarted) {
        try {
            Stop-Transcript | Out-Null
        } catch {
            Write-Warning ("Could not stop unified launcher transcript: {0}" -f $_.Exception.Message)
        }
        $Script:UnifiedLauncherTranscriptStarted = $false
    }

    if ([string]::IsNullOrWhiteSpace($Script:UnifiedLauncherTranscriptPath)) {
        Write-Warning "Unified launcher transcript path is empty; execution-tail evidence not written."
        return
    }

    if (-not (Test-Path -LiteralPath $Script:UnifiedLauncherTranscriptPath -PathType Leaf)) {
        Write-Warning ("Unified launcher transcript is missing; execution-tail evidence not written: {0}" -f $Script:UnifiedLauncherTranscriptPath)
        return
    }

    $safeStamp = $StampValue
    if ([string]::IsNullOrWhiteSpace($safeStamp)) {
        $safeStamp = Get-Date -Format "yyyyMMdd-HHmmss"
    }

    $allLines = @(Get-Content -LiteralPath $Script:UnifiedLauncherTranscriptPath -Encoding UTF8 -ErrorAction SilentlyContinue)
    $tailLineCount = [Math]::Min(220, $allLines.Count)
    $tailLines = @($allLines | Select-Object -Last $tailLineCount)

    $warningLines = @($allLines | Where-Object {
        $_ -match "AVVISO|WARNING|Warning|failed with exit code|Fatal|fatal|Passed: False|Patch plan count: 0|provider.*failed|did not pass"
    } | Select-Object -Last 80)

    $evidenceDirRelative = "docs/LOCAL_VALIDATION_EVIDENCE"
    if (-not [string]::IsNullOrWhiteSpace($Script:UnifiedLauncherEvidenceDir)) {
        $evidenceDirRelative = $Script:UnifiedLauncherEvidenceDir
    }
    $evidenceDir = Join-Path $Root $evidenceDirRelative
    New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null

    $jsonPath = Join-Path $evidenceDir ("unified_launcher_execution_tail_{0}.json" -f $safeStamp)
    $mdPath = Join-Path $evidenceDir ("unified_launcher_execution_tail_{0}.md" -f $safeStamp)

    $normalizedTranscriptPath = $Script:UnifiedLauncherTranscriptPath.Replace('\', '/')

    $report = [ordered]@{
        schema_version = 1
        kind = "unified_launcher_execution_tail"
        generated_at = (Get-Date).ToString("o")
        stamp = $safeStamp
        passed = [string]::IsNullOrWhiteSpace($FailureMessage)
        prod_mode = $false
        debug_tail_enabled = $true
        provider_execution_requested = $ProviderExecutionRequested
        patch_specs_requested = $PatchSpecsRequested
        patch_application_performed = $false
        source_writes_performed = $false
        blender_runtime_execution_performed = $false
        ffmpeg_execution_performed = $false
        run_dir = $RunDirValue
        manifest = $ManifestPathValue
        transcript_path = $normalizedTranscriptPath
        transcript_line_count = $allLines.Count
        tail_line_count = $tailLineCount
        anomaly_line_count = $warningLines.Count
        failure_message = $FailureMessage
        resolved_modes = @($ResolvedModesValue)
        report_files = @($ReportFilesValue)
        context_files = @($ContextFilesValue)
        anomaly_lines = @($warningLines)
        tail = @($tailLines)
        errors = @()
        warnings = @()
    }

    ($report | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $jsonPath -Encoding UTF8

    $mdLines = New-Object System.Collections.Generic.List[string]
    [void]$mdLines.Add("# Unified launcher execution tail")
    [void]$mdLines.Add("")
    [void]$mdLines.Add(('- Stamp: `{0}`' -f $safeStamp))
    [void]$mdLines.Add('- Prod mode: `False`')
    [void]$mdLines.Add('- Debug tail enabled: `True`')
    [void]$mdLines.Add(('- Provider execution requested: `{0}`' -f $ProviderExecutionRequested))
    [void]$mdLines.Add(('- Patch specs requested: `{0}`' -f $PatchSpecsRequested))
    [void]$mdLines.Add(('- Transcript: `{0}`' -f $normalizedTranscriptPath))
    [void]$mdLines.Add(('- Transcript line count: `{0}`' -f $allLines.Count))
    [void]$mdLines.Add(('- Tail line count: `{0}`' -f $tailLineCount))
    [void]$mdLines.Add(('- Anomaly line count: `{0}`' -f $warningLines.Count))
    if (-not [string]::IsNullOrWhiteSpace($FailureMessage)) { [void]$mdLines.Add(('- Failure message: `{0}`' -f $FailureMessage)) }
    [void]$mdLines.Add("")
    [void]$mdLines.Add("## Anomaly lines")
    [void]$mdLines.Add("")
    [void]$mdLines.Add('```text')
    foreach ($line in $warningLines) {
        [void]$mdLines.Add($line)
    }
    [void]$mdLines.Add('```')
    [void]$mdLines.Add("")
    [void]$mdLines.Add("## Tail")
    [void]$mdLines.Add("")
    [void]$mdLines.Add('```text')
    foreach ($line in $tailLines) {
        [void]$mdLines.Add($line)
    }
    [void]$mdLines.Add('```')
    $mdLines | Set-Content -LiteralPath $mdPath -Encoding UTF8

    $Script:UnifiedLauncherExecutionTailWritten = $true
    Write-Host "[OK] Execution tail evidence: $jsonPath"
    Write-Host "[OK] Execution tail markdown: $mdPath"
}
# IA_CARMINE_EXECUTION_TAIL_PATCH_END

Show-LauncherIntro
$RepoRoot = Resolve-RepoRoot
Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot
$ResolvedPythonExe = Resolve-PythonExe -Requested $PythonExe -Root $RepoRoot

$RepoRootCanonical = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
$ResolvedPythonCanonical = (Resolve-Path -LiteralPath $ResolvedPythonExe).Path
$RequiredRepoPy = Join-Path $RepoRootCanonical ".venv\Scripts\python.exe"
$NormalizedRepoRoot = $RepoRootCanonical.Replace("\", "/").ToLowerInvariant()
$NormalizedResolvedPython = $ResolvedPythonCanonical.Replace("\", "/").ToLowerInvariant()

Write-Host "[PYTHON-GATE] Repository root: $RepoRootCanonical"
Write-Host "[PYTHON-GATE] Resolved Python: $ResolvedPythonCanonical"
Write-Host "[PYTHON-GATE] Required RepoPy: $RequiredRepoPy"

if (-not $NormalizedResolvedPython.StartsWith($NormalizedRepoRoot + "/")) {
    [Console]::Error.WriteLine("[PYTHON-GATE] Rejected non-repository Python: $ResolvedPythonCanonical")
    [Console]::Error.WriteLine("[PYTHON-GATE] Use RepoPy only: $RequiredRepoPy")
    [Console]::Error.WriteLine("[PYTHON-GATE] Set `$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path and pass -PythonExe `$RepoPy.")
    exit 2
}

if (Test-Path -LiteralPath $RequiredRepoPy -PathType Leaf) {
    $RequiredRepoPyCanonical = (Resolve-Path -LiteralPath $RequiredRepoPy).Path
    $NormalizedRequiredRepoPy = $RequiredRepoPyCanonical.Replace("\", "/").ToLowerInvariant()
    if ($NormalizedResolvedPython -ne $NormalizedRequiredRepoPy) {
        [Console]::Error.WriteLine("[PYTHON-GATE] Rejected repository Python that is not canonical RepoPy: $ResolvedPythonCanonical")
        [Console]::Error.WriteLine("[PYTHON-GATE] Canonical RepoPy required: $RequiredRepoPyCanonical")
        exit 2
    }
}

$env:IA_CARMINE_PYTHON = $ResolvedPythonCanonical
$env:PYTHONPATH = $RepoRootCanonical
Write-Host "[PYTHON-GATE] RepoPy accepted and exported to IA_CARMINE_PYTHON."
Write-Host "[INFO] PYTHONPATH: $env:PYTHONPATH"
Write-Host "[INFO] Python: $ResolvedPythonExe"

if ($Full0To10) { $ResolvedModes = @() } elseif ($Interactive -or @($Mode).Count -eq 0) { $ResolvedModes = @(Read-InteractiveModes) } else { $ResolvedModes = @(Normalize-ModeList $Mode) }
if (@($ResolvedModes).Count -eq 0 -and -not $Full0To10) { throw "No modes selected. Use -Interactive or -Mode all." }

if ($Full0To10) {
    $UnifiedRunLegacyAliasModes = @("md", "json", "python", "chunks", "context_pack", "agent_state", "official", "provider", "patch_specs", "evidence", "contract", "full_validation")
    if ($NoPatchSpecs) { $UnifiedRunLegacyAliasModes = @($UnifiedRunLegacyAliasModes | Where-Object { $_ -ne "patch_specs" }) }
    if ($NoEvidence) { $UnifiedRunLegacyAliasModes = @($UnifiedRunLegacyAliasModes | Where-Object { $_ -ne "evidence" }) }
    $ResolvedModes = @($UnifiedRunLegacyAliasModes)

    $UseOllamaAdvisory = $true
    $UsePrimaryAdvisoryProvider = $true
    $FullContextGoldenPath = $true

    if (-not $NoWorkloadQuality) { $BuildWorkloadQualityReport = $true }
    if (-not $NoMultistepProvider) { $RunMultistepProviderWorkflow = $true }
    if (-not $NoOllamaProbe) { $RunOllamaProbe = $true }
    if (-not $NoNpuProbe) { $RunNpuProbe = $true }
    if (-not $NoNpuDecodeSmoke) { $RunNpuDecodeSmoke = $true }
    if (-not $NoMemoryWrite) { $SaveInputsToMemoryDb = $true }
    if (-not $NoEvidence) { $BuildEvidence = $true }
    if (-not $NoPatchSpecs) { $GeneratePatchSpecs = $true }
    Write-Warning "Legacy full-toolbox integrated lane is no longer auto-enabled by -Full0To10; use -RunLegacyFullToolboxIntegrated explicitly for diagnostic legacy runs."
}


if ([string]::IsNullOrWhiteSpace($Stamp)) { $Stamp = Get-Date -Format "yyyyMMdd-HHmmss" }
$DataStamp = $Stamp
if ($PrepareReviewPr) {
    if ([string]::IsNullOrWhiteSpace($ReviewPrBranch)) {
        $ReviewPrBranch = "CARMINEai/full-run-$Stamp"
    }
    if ([string]::IsNullOrWhiteSpace($ReviewPrTitle)) {
        $ReviewPrTitle = "feat(ai): full-run patch suggestion review $Stamp"
    }
    if ([string]::IsNullOrWhiteSpace($ReviewPrCommitMessage)) {
        $ReviewPrCommitMessage = "feat(ai): prepare full-run patch suggestion review"
    }
}
# IA_CARMINE_OUTPUT_DIR_EVIDENCE_DIR_FALLBACK_BEGIN
if ([string]::IsNullOrWhiteSpace($OutputDir)) { $OutputDir = "output" }
if ([string]::IsNullOrWhiteSpace($EvidenceDir)) { $EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE" }
$ValidationDir = Join-Path $OutputDir "validation"
$PipelineDir = Join-Path $OutputDir "ai_pipeline"
$AnalysisDir = Join-Path $OutputDir "analysis"
$PatchSpecsDir = Join-Path $OutputDir "patch_specs"
$LocalAiRunsDir = Join-Path $OutputDir "local_ai_runs"
$AiContextPacksDir = Join-Path $OutputDir "ai_context_packs"
if ([string]::IsNullOrWhiteSpace($AiPacketsRoot)) { $AiPacketsRoot = Join-Path $OutputDir "ai_packets" }
if ([string]::IsNullOrWhiteSpace($AiPacketsDir)) { $AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp }
$RunDir = Join-Path $LocalAiRunsDir ("{0}_unified_launcher" -f $Stamp)
$ManifestPath = Join-Path $RunDir ("unified_launcher_manifest_{0}.json" -f $Stamp)
$ReportFiles = @()
$ContextFiles = @()
$Script:UnifiedLauncherOutputDir = $OutputDir
$Script:UnifiedLauncherEvidenceDir = $EvidenceDir
# IA_CARMINE_OUTPUT_DIR_EVIDENCE_DIR_FALLBACK_END
$SmokeOnlyRun = (
    @($ResolvedModes).Count -eq 1 -and
    $ResolvedModes -contains "smoke"
)

if ($SmokeOnlyRun -and -not $Prod) {
    Write-Host "[INFO] Smoke mode: unified launcher transcript/tail evidence disabled."
    $Prod = $true
}

if ($NoExecutionTail -and -not $Prod) {
    Write-Host "[INFO] -NoExecutionTail supplied: unified launcher transcript/tail evidence disabled."
    $Prod = $true
}

Start-UnifiedLauncherExecutionTranscript -StampValue $Stamp -Root $RepoRoot -ProdMode ([bool]$Prod)

# IA-CARMINE-EARLY-OBSERVER-INIT-BEGIN
try {
    $EarlyObserverRunDir = Join-Path $RepoRoot (Join-Path $OutputDir ("local_ai_runs/{0}" -f $Stamp))
    $EarlyObserverDir = $ObserverOutputDir
    if ([string]::IsNullOrWhiteSpace($EarlyObserverDir)) {
        $EarlyObserverDir = Join-Path $RepoRoot (Join-Path $OutputDir ("local_ai_runs/{0}_observer" -f $Stamp))
    }
    if (Get-Command Initialize-UnifiedRunObserver -ErrorAction SilentlyContinue) {
        Initialize-UnifiedRunObserver `
            -StampValue $Stamp `
            -ObserverDirValue $EarlyObserverDir `
            -RepoRootValue $RepoRoot `
            -RunDirValue $EarlyObserverRunDir `
            -OpenConsoles ([bool]$OpenObserverConsoles) `
            -OpenExtendedConsoles ([bool]$OpenExtendedObserverConsoles) `
            -RefreshSeconds $ObserverRefreshSeconds
    }
} catch {
    Write-Warning ("Unified run observer early init failed: {0}" -f $_.Exception.Message)
}
# IA-CARMINE-EARLY-OBSERVER-INIT-END
if ($RunIntensity -ne "custom") {
    if ($RunIntensity -eq "quick") {
        $BudgetMinutes = 5
        $MaxRounds = 4
        $FilesPerRound = 4
        $MaxContextFiles = 80
        $MaxCharsPerFile = 4000
        $MaxNewTokens = 1600
        $KeepAlive = "8m"
        $NpuAuditorEveryRounds = 2
        $NpuAuditorTimeoutSeconds = 180
        $NpuMaxContextChars = 4000
        $NpuMaxPromptChars = 800
        $NpuMaxNewTokens = 256
        $NpuFinalWaitSeconds = 90
        $ProviderMaxContextChars = 9000
        $ContextPackMaxTotalChars = 32000
        $ContextPackMaxFileChars = 2500
        $AgentStateMaxMemoryChars = 12000
        $RepositoryConsistencyMapWorkers = 8
    } elseif ($RunIntensity -eq "balanced") {
        if ($ProviderMaxContextChars -eq 0) { $ProviderMaxContextChars = $MaxContextChars }
    } elseif ($RunIntensity -eq "deep") {
        $BudgetMinutes = 30
        $MaxRounds = 20
        $FilesPerRound = 8
        $MaxContextFiles = 220
        $MaxCharsPerFile = 6000
        $MaxNewTokens = 3600
        $KeepAlive = "35m"
        $NpuAuditorEveryRounds = 3
        $NpuAuditorTimeoutSeconds = 420
        $NpuMaxContextChars = 8000
        $NpuMaxPromptChars = 1200
        $NpuMaxNewTokens = 384
        $NpuFinalWaitSeconds = 180
        $ProviderMaxContextChars = 24000
        $ContextPackMaxTotalChars = 128000
        $ContextPackMaxFileChars = 8000
        $AgentStateMaxMemoryChars = 48000
        $RepositoryConsistencyMapWorkers = 12
    }
}
if ($ProviderMaxContextChars -eq 0) { $ProviderMaxContextChars = $MaxContextChars }
$ModeName = ((@($ResolvedModes) | Sort-Object -Unique) -join "_")
if ([string]::IsNullOrWhiteSpace($TaskBranch)) { $TaskBranch = "codex/local-ai-$ModeName-$Stamp" }

$Required = @(
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md",
    "Tools/validation/build_markdown_inventory.py",
    "Tools/validation/build_script_inventory.py",
    "Tools/validation/check_docs_links.py",
    "Tools/validation/check_validation_report_contract.py",
    "Tools/workflow/run_local_ai_task_via_pipeline.ps1",
    "Tools/workflow/run_post_validation_ai_packet.ps1",
    $TaskFile
)
foreach ($Path in $Required) { Assert-FileExists $Path }

$Warnings = @()
Add-OptionalModeWarning "validation" ".\Tools\workflow\run_local_validation_after_refactor.ps1" ([ref]$Warnings)
Add-OptionalModeWarning "smoke" ".\Tools\workflow\startup_check.py" ([ref]$Warnings)
Add-OptionalModeWarning "chunks" ".\Tools\npu\build_semantic_code_chunks.py" ([ref]$Warnings)
Add-OptionalModeWarning "context_pack" ".\Tools\ai\build_ai_context_pack.py" ([ref]$Warnings)
Add-OptionalModeWarning "agent_state" ".\Tools\ai\build_agent_state_packet.py" ([ref]$Warnings)

if ($ApplyReset -and $ConfirmResetText -ne "DELETE LOCAL AI ARTIFACTS") {
    throw "-ApplyReset requires -ConfirmResetText 'DELETE LOCAL AI ARTIFACTS'"
}

$Status = (& git status --porcelain)
if ($LASTEXITCODE -ne 0) { throw "git status failed" }
if (-not $AllowDirty -and $Status) {
    Write-Host "[ERROR] Working tree has local changes:" -ForegroundColor Red
    $Status | ForEach-Object { Write-Host $_ }
    throw "working tree is not clean; rerun with -AllowDirty only when intended"
}

if (-not $SkipGitSync) {
    Invoke-Git @("fetch", "origin")
    Invoke-Git @("switch", "master")
    Invoke-Git @("pull", "--ff-only", "origin", "master")
}

if (-not $NoBranch) {
    $ExistingBranch = (& git branch --list $TaskBranch)
    if ($LASTEXITCODE -ne 0) { throw "git branch lookup failed" }
    if ($ExistingBranch) { Invoke-Git @("switch", $TaskBranch) } else { Invoke-Git @("switch", "-c", $TaskBranch) }
}

$RunDir = "output/local_ai_runs/${Stamp}_${ModeName}_unified"
$PipelineDir = "$RunDir/pipeline"
$ValidationDir = "output/validation"
New-Item -ItemType Directory -Force -Path $PipelineDir | Out-Null
New-Item -ItemType Directory -Force -Path $ValidationDir | Out-Null
New-Item -ItemType Directory -Force -Path "output/ai_pipeline" | Out-Null
if ([string]::IsNullOrWhiteSpace($AiPacketsRoot)) { $AiPacketsRoot = "output/ai_packets" }
if ([string]::IsNullOrWhiteSpace($AiPacketsDir)) { $AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp }
$OllamaWorkloadReport = Join-Path $AiPacketsDir "ollama_gpu_real_workload_report.md"
$NpuWorkloadReport = Join-Path $AiPacketsDir "npu_real_workload_report.md"
New-Item -ItemType Directory -Force -Path $AiPacketsDir | Out-Null

trap {
    $Script:UnifiedLauncherFailureMessage = $_.Exception.Message
    if (Get-Command Write-UnifiedLauncherExecutionTailEvidence -ErrorAction SilentlyContinue) {
        try {
            Write-UnifiedLauncherExecutionTailEvidence `
                -StampValue $Stamp `
                -Root $RepoRoot `
                -RunDirValue $RunDir `
                -ManifestPathValue "$PipelineDir/unified_local_ai_refactor_manifest.json" `
                -ResolvedModesValue $ResolvedModes `
                -ReportFilesValue $ReportFiles `
                -ContextFilesValue $ContextFiles `
                -ProviderExecutionRequested ([bool]$UsePrimaryAdvisoryProvider) `
                -PatchSpecsRequested ([bool]$GeneratePatchSpecs) `
                -ProdMode ([bool]$Prod) `
                -FailureMessage $Script:UnifiedLauncherFailureMessage
        } catch {
            Write-Warning ("Could not write unified launcher failure tail evidence: {0}" -f $_.Exception.Message)
        }
    }
    Write-UnifiedLauncherStructuredError -ErrorRecord $_
    exit 2
}


$ContextFiles = @()
$ReportFiles = @()
$PhaseReports = [ordered]@{}
$PhaseStatus = [ordered]@{}


# IA_CARMINE_STRICT_REAL_RUN_ACTIVATION_BEGIN
$StrictActivationExcludedModes = @("smoke", "reset")
$StrictActivationRealModes = @($ResolvedModes | Where-Object { $StrictActivationExcludedModes -notcontains $_ })
$StrictRealRunActivationEnabled = (-not [bool]$DryRun) -and (-not [bool]$NoStrictRealRunActivation) -and ($StrictActivationRealModes.Count -gt 0)

if ($StrictRealRunActivationEnabled) {
    if (-not $NoOllamaProbe) { $RunOllamaProbe = $true }
    if (-not $NoNpuProbe) { $RunNpuProbe = $true }
    if (-not $NoNpuDecodeSmoke) { $RunNpuDecodeSmoke = $true }
    if (-not $NoMultistepProvider) { $RunMultistepProviderWorkflow = $true }
    if (-not $NoWorkloadQuality) { $BuildWorkloadQualityReport = $true }
    if (-not $NoEvidence) { $BuildEvidence = $true }
    if (-not $NoPatchSpecs) { $GeneratePatchSpecs = $true }
    if (-not $NoMemoryWrite) { $SaveInputsToMemoryDb = $true }

    $UseOllamaAdvisory = $true
    $UsePrimaryAdvisoryProvider = $true
    Write-Warning "Legacy full-toolbox integrated lane is no longer auto-enabled by -Full0To10; use -RunLegacyFullToolboxIntegrated explicitly for diagnostic legacy runs."
}
# IA_CARMINE_STRICT_REAL_RUN_ACTIVATION_END

Write-Host "[INFO] Resolved modes: $($ResolvedModes -join ',')"
Write-Host "[INFO] Stamp: $Stamp"
Write-Host "[INFO] DataStamp: $DataStamp"
Write-Host "[INFO] AI packets dir: $AiPacketsDir"
Write-Host "[INFO] Branch: $TaskBranch"
Write-Host "[INFO] TaskFile: $TaskFile"
Write-Host "[INFO] RunDir: $RunDir"
Write-Host "[INFO] Ollama advisory: $UseOllamaAdvisory"
Write-Host "[INFO] Primary advisory provider: $UsePrimaryAdvisoryProvider"
Write-Host "[INFO] Multistep provider workflow: $RunMultistepProviderWorkflow"
Write-Host "[INFO] Legacy NPU auditor provider: $RunLegacyNpuAuditorProvider"
Write-Host "[INFO] Patch specs: $GeneratePatchSpecs"
Write-Host "[INFO] Reset apply: $ApplyReset"
Write-Host "[INFO] Prepare review PR: $PrepareReviewPr"
Write-Host "[INFO] Runtime evidence correlation: $BuildRuntimeEvidenceCorrelation"
if ($PrepareReviewPr) {
    Write-Host "[INFO] Review PR branch: $ReviewPrBranch"
    Write-Host "[INFO] Review PR title: $ReviewPrTitle"
}
foreach ($warning in $Warnings) { Write-Warning $warning }

$PhaseStatus.baseline_compile = Invoke-Checked "Baseline compile validation/inventory tools" {
    Invoke-Python @("-m", "py_compile", ".\Tools\validation\build_markdown_inventory.py", ".\Tools\validation\build_script_inventory.py", ".\Tools\validation\check_validation_report_contract.py")
}

if (Test-ModeEnabled "smoke") {
    $PhaseStatus.git_diff_check_initial = Invoke-Checked "Initial git diff --check" { git diff --check } -SoftFail:$ContinueOnValidationError
    if (Test-Path .\Tools\workflow\startup_check.py) {
        $StartupCheck = "$ValidationDir/startup_check_${ModeName}_$Stamp.json"
        $PhaseStatus.startup_check = Invoke-Checked "Startup smoke check" {
            Invoke-Python @(".\Tools\workflow\startup_check.py", "--repo-root", ".", "--output", $StartupCheck)
        } -SoftFail:$ContinueOnValidationError
        if (Test-Path $StartupCheck) { $ReportFiles += $StartupCheck; $PhaseReports.startup_check = $StartupCheck }
    }
}

if (Test-ModeEnabled "reset") {
    $ResetJson = "$ValidationDir/local_ai_reset_plan_${ModeName}_$Stamp.json"
    $ResetMd = "$ValidationDir/local_ai_reset_plan_${ModeName}_$Stamp.md"
    $Candidates = @(Get-ResetCandidates -Root $RepoRoot -BeforeDate $ResetBeforeDate -IncludeMemory:$IncludeMemoryReset -IncludeGeneratedIndex:$IncludeGeneratedIndexReset)
    Write-ResetPlan -Candidates @($Candidates) -OutputJson $ResetJson -OutputMd $ResetMd -BeforeDate $ResetBeforeDate -Apply:$ApplyReset -Root $RepoRoot
    if ($ApplyReset) {
        foreach ($item in @($Candidates)) {
            $target = Join-Path $RepoRoot $item.path
            if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force }
        }
    }
    $ReportFiles += $ResetJson
    $ContextFiles = Add-ExistingContextFile $ContextFiles $ResetMd
    $PhaseReports.reset_plan = $ResetJson
    $PhaseStatus.reset_plan = $true
}

if (Test-ModeEnabled "validation") {
    if (Test-Path .\Tools\workflow\run_local_validation_after_refactor.ps1) {
        $ValidationArgs = @("-ExecutionPolicy", "Bypass", "-File", ".\Tools\workflow\run_local_validation_after_refactor.ps1", "-SkipPull", "-MatrixWorkers", "$MatrixWorkers", "-RepeatCases", "$RepeatCases")
        if ($ContinueOnValidationError) { $ValidationArgs += "-ContinueOnError" }
        $PhaseStatus.local_validation_after_refactor = Invoke-Checked "Run local validation after refactor" { powershell.exe @ValidationArgs } -SoftFail:$ContinueOnValidationError
    }
}

if (Test-ModeEnabled "md") {
    $MarkdownJson = "$ValidationDir/markdown_inventory_${ModeName}_$Stamp.json"
    $MarkdownMd = "$ValidationDir/markdown_inventory_${ModeName}_$Stamp.md"
    $DocsLinks = "$ValidationDir/docs_links_${ModeName}_$Stamp.json"
    $PhaseStatus.markdown_inventory = Invoke-Checked "Build Markdown inventory" {
        Invoke-Python @(".\Tools\validation\build_markdown_inventory.py", "--repo-root", ".", "--output", $MarkdownJson, "--markdown-output", $MarkdownMd)
    }
    $PhaseStatus.docs_links = Invoke-Checked "Check docs links" {
        Invoke-Python @(".\Tools\validation\check_docs_links.py", "--repo-root", ".", "--output", $DocsLinks)
    } -SoftFail:$ContinueOnValidationError
    $ReportFiles += @($MarkdownJson, $DocsLinks)
    $ContextFiles = Add-ExistingContextFile $ContextFiles $MarkdownMd
    $PhaseReports.markdown_inventory = $MarkdownJson
    $PhaseReports.docs_links = $DocsLinks
}

if (Test-ModeEnabled "json") {
    $JsonContract = "$ValidationDir/validation_report_contract_json_${ModeName}_$Stamp.json"
    $JsonContractArgs = @(".\Tools\validation\check_validation_report_contract.py", "--repo-root", ".", "--output", $JsonContract)
    foreach ($Report in $ReportFiles) { $JsonContractArgs += @("--report-file", $Report) }
    $PhaseStatus.json_contract = Invoke-Checked "Validate current JSON/report contracts" { Invoke-Python -PythonArgs $JsonContractArgs } -SoftFail:$ContinueOnValidationError
    $ReportFiles += $JsonContract
    $PhaseReports.json_contract = $JsonContract
}

if (Test-ModeEnabled "python") {
    $ScriptJson = "$ValidationDir/script_inventory_${ModeName}_$Stamp.json"
    $ScriptCsv = "$ValidationDir/script_inventory_${ModeName}_$Stamp.csv"
    $ScriptMd = "$ValidationDir/script_inventory_${ModeName}_$Stamp.md"
    $PhaseStatus.script_inventory = Invoke-Checked "Build script/tool inventory" {
        Invoke-Python @(".\Tools\validation\build_script_inventory.py", "--repo-root", ".", "--output", $ScriptJson, "--csv-output", $ScriptCsv, "--markdown-output", $ScriptMd)
    }
    $ReportFiles += $ScriptJson
    $ContextFiles = Add-ExistingContextFile $ContextFiles $ScriptMd
    $PhaseReports.script_inventory = $ScriptJson
    $PhaseReports.script_inventory_csv = $ScriptCsv
}

if (Test-ModeEnabled "chunks") {
    $PhaseStatus.semantic_chunks = Invoke-Checked "Build semantic code chunks" {
        Invoke-Python @(".\Tools\npu\build_semantic_code_chunks.py", "--repo-root", ".")
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "indexAI/code_chunks/semantic_code_chunks_manifest.json"
}

if (Test-ModeEnabled "context_pack") {
    $ContextPackBase = "unified_${ModeName}_context_pack_$Stamp"
    $PhaseStatus.context_pack = Invoke-Checked "Build AI context pack" {
        Invoke-Python @(".\Tools\ai\build_ai_context_pack.py", "--repo-root", ".", "--profile", "core_ai_backend", "--basename", $ContextPackBase, "--evidence-dir", $ValidationDir, "--evidence-basename", "${ContextPackBase}_evidence", "--max-total-chars", "$ContextPackMaxTotalChars", "--max-file-chars", "$ContextPackMaxFileChars")
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "output/ai_context_packs/$ContextPackBase.md"
    $ContextFiles = Add-ExistingContextFile $ContextFiles "output/ai_context_packs/$ContextPackBase.json"
}

if (Test-ModeEnabled "agent_state") {
    $AgentStateDir = "$PipelineDir/agent_state"
    New-Item -ItemType Directory -Force -Path $AgentStateDir | Out-Null
    $AgentStateBase = "unified_${ModeName}_agent_state_$Stamp"
    $AgentArgs = @(
        ".\Tools\ai\build_agent_state_packet.py",
        "--repo-root", ".",
        "--objective", "Unified local AI refactor run $ModeName",
        "--output-dir", $AgentStateDir,
        "--packet-name", $AgentStateBase,
        "--max-memory-chars", "24000",
        "--memory-note", "Unified launcher report-only run.",
        "--memory-db", $MemoryDb
    )
    if ($SaveInputsToMemoryDb) {
        $AgentArgs += "--save-inputs-to-memory-db"
    }
    $PhaseStatus.agent_state = Invoke-Checked "Build agent state packet" {
        Invoke-Python $AgentArgs
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "$AgentStateDir/$AgentStateBase.md"
    $ContextFiles = Add-ExistingContextFile $ContextFiles "$AgentStateDir/$AgentStateBase.json"
}

$FinalContract = "$ValidationDir/validation_report_contract_${ModeName}_$Stamp.json"
if ((Test-ModeEnabled "contract") -or $ReportFiles.Count -gt 0) {
    $ContractArgs = @(".\Tools\validation\check_validation_report_contract.py", "--repo-root", ".", "--output", $FinalContract)
    foreach ($Report in $ReportFiles) { $ContractArgs += @("--report-file", $Report) }
    $PhaseStatus.task_scoped_contract = Invoke-Checked "Validate task-scoped reports" { Invoke-Python $ContractArgs } -SoftFail:$ContinueOnValidationError
    $ReportFiles += $FinalContract
    $PhaseReports.task_scoped_contract = $FinalContract
}

$ContextFiles = Add-ExistingContextFile $ContextFiles $TaskFile
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md"
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md"
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/LOCAL_AI_TASKS/code-refactor-local-machine-validation-addendum.md"

$WorkloadQualityReport = "$ValidationDir/ai_workload_report_quality.json"
$WorkloadQualityRoutingOk = $false

$CanonicalOllamaWorkloadReport = $OllamaWorkloadReport
$CanonicalNpuWorkloadReport = $NpuWorkloadReport
$LocalProviderProbeReport = "output/validation/local_provider_probe.json"

if (($BuildWorkloadQualityReport -or ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality) -or $RunOllamaProbe -or $RunNpuProbe) -and -not $NoWorkloadQuality) {
    $NeedProviderWorkloadInputs = (-not (Test-Path -LiteralPath $CanonicalOllamaWorkloadReport -PathType Leaf)) -or (-not (Test-Path -LiteralPath $CanonicalNpuWorkloadReport -PathType Leaf))

    if ($NeedProviderWorkloadInputs -and ($RunOllamaProbe -or $RunNpuProbe)) {
        $ProbeArgs = @(
            ".\Tools\ai\run_local_provider_probe.py",
            "--repo-root", ".",
            "--output", $LocalProviderProbeReport
        )

        if ($RunOllamaProbe) { $ProbeArgs += "--run-ollama" }
        if ($RunNpuProbe) { $ProbeArgs += "--run-npu" }
        if (-not [string]::IsNullOrWhiteSpace($Model)) { $ProbeArgs += @("--model", $Model) }

        $PhaseStatus.provider_workload_probe = Invoke-Checked "Generate provider workload probe inputs" {
            Invoke-Python $ProbeArgs
        } -SoftFail:$true

        if (Test-Path -LiteralPath $LocalProviderProbeReport -PathType Leaf) {
            Write-ProviderWorkloadReportsFromProbe `
                -ProbeReport $LocalProviderProbeReport `
                -OllamaReport $CanonicalOllamaWorkloadReport `
                -NpuReport $CanonicalNpuWorkloadReport

            $ReportFiles += $LocalProviderProbeReport
            $PhaseReports.provider_workload_probe = $LocalProviderProbeReport

            $ContextFiles = Add-ExistingContextFile $ContextFiles $CanonicalOllamaWorkloadReport
            $ContextFiles = Add-ExistingContextFile $ContextFiles $CanonicalNpuWorkloadReport

            if (Test-Path -LiteralPath $CanonicalOllamaWorkloadReport -PathType Leaf) {
                $PhaseReports.ollama_workload_report = $CanonicalOllamaWorkloadReport
            }
            if (Test-Path -LiteralPath $CanonicalNpuWorkloadReport -PathType Leaf) {
                $PhaseReports.npu_workload_report = $CanonicalNpuWorkloadReport
            }
        }
    }
}


if ($BuildWorkloadQualityReport -or ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality)) {
    Assert-FileExists ".\Tools\validation\check_ai_workload_report_quality.py"
    $PhaseStatus.workload_quality = Invoke-Checked "Build AI workload quality routing report" {
        Invoke-Python @(".\Tools\validation\check_ai_workload_report_quality.py", "--repo-root", ".", "--report-dir", $AiPacketsDir, "--output", $WorkloadQualityReport)
    } -SoftFail:$ContinueOnValidationError

# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-BEGIN
$HeapExchangeObserverDir = $ObserverOutputDir
if ([string]::IsNullOrWhiteSpace($HeapExchangeObserverDir)) {
    $HeapExchangeObserverDir = Join-Path $OutputDir ("local_ai_runs/{0}_observer" -f $DataStamp)
}
$HeapExchangeEntryJson = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.json"
$HeapExchangeEntryMd = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.md"
$HeapExchangeRuntimeState = Join-Path $AiPacketsDir "heap_exchange_runtime_state.jsonl"
$HeapExchangeEntryArgs = @(
    "Tools/ai/build_heap_exchange_runtime_entry.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--task-file", $TaskFile,
    "--observer-dir", $HeapExchangeObserverDir,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--output", $HeapExchangeEntryJson,
    "--markdown-output", $HeapExchangeEntryMd
)
$HeapExchangeEntryOk = Invoke-Checked "Build heap/exchange runtime entry" {
    & $ResolvedPythonExe @HeapExchangeEntryArgs
}
$ReportFiles += $HeapExchangeEntryJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeEntryMd
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-END

    if (Test-Path -LiteralPath $WorkloadQualityReport -PathType Leaf) {
        $ReportFiles += $WorkloadQualityReport
        $PhaseReports.workload_quality = $WorkloadQualityReport
        $WorkloadQualityRoutingOk = $true
    }
}
if ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality -and -not (Test-Path -LiteralPath $WorkloadQualityReport -PathType Leaf)) {
    if ($DryRun -or $ContinueOnValidationError) {
        Write-Host "[DRY-RUN] Primary provider requires workload quality routing report; generation planned: output/validation/ai_workload_report_quality.json"
        if (-not $DryRun) {
            Write-Warning "Primary advisory provider workload quality report is missing; continuing because -ContinueOnValidationError is set."
            $Warnings += "primary_provider_workload_quality_missing_continued"
        }
        $WorkloadQualityRoutingOk = [bool]$DryRun
    } else {
        throw "Primary advisory provider requested but workload quality routing report is missing: output/validation/ai_workload_report_quality.json"
    }
}


# IA-CARMINE-TASK-INGRESS-CONTRACT-BEGIN
$TaskIngressContractJson = Join-Path $AiPacketsDir "task_ingress_contract.json"
$TaskIngressContractMd = Join-Path $AiPacketsDir "task_ingress_contract.md"
$TaskIngressArgs = @(
    "Tools/ai/build_task_ingress_contract.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--task-file", $TaskFile,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--observer-dir", $HeapExchangeObserverDir,
    "--output", $TaskIngressContractJson,
    "--markdown-output", $TaskIngressContractMd
)
$PhaseStatus.task_ingress_contract = Invoke-Checked "Build task ingress contract" {
    & $ResolvedPythonExe @TaskIngressArgs
}
$ReportFiles += $TaskIngressContractJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $TaskIngressContractMd
$PhaseReports.task_ingress_contract = $TaskIngressContractJson
$PhaseReports.task_ingress_contract_markdown = $TaskIngressContractMd
# IA-CARMINE-TASK-INGRESS-CONTRACT-END

# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-ENSURE-BEGIN
if (-not (Get-Variable -Name HeapExchangeObserverDir -ErrorAction SilentlyContinue)) {
    $HeapExchangeObserverDir = $ObserverOutputDir
    if ([string]::IsNullOrWhiteSpace($HeapExchangeObserverDir)) {
        $HeapExchangeObserverDir = Join-Path $OutputDir ("local_ai_runs/{0}_observer" -f $DataStamp)
    }
}
if (-not (Get-Variable -Name HeapExchangeEntryJson -ErrorAction SilentlyContinue)) {
    $HeapExchangeEntryJson = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.json"
}
if (-not (Get-Variable -Name HeapExchangeEntryMd -ErrorAction SilentlyContinue)) {
    $HeapExchangeEntryMd = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.md"
}
if (-not (Get-Variable -Name HeapExchangeRuntimeState -ErrorAction SilentlyContinue)) {
    $HeapExchangeRuntimeState = Join-Path $AiPacketsDir "heap_exchange_runtime_state.jsonl"
}

if (-not (Test-Path -LiteralPath $HeapExchangeEntryJson -PathType Leaf)) {
    $HeapExchangeEntryArgs = @(
        "Tools/ai/build_heap_exchange_runtime_entry.py",
        "--repo-root", ".",
        "--stamp", $DataStamp,
        "--task-file", $TaskFile,
        "--observer-dir", $HeapExchangeObserverDir,
        "--runtime-state", $HeapExchangeRuntimeState,
        "--output", $HeapExchangeEntryJson,
        "--markdown-output", $HeapExchangeEntryMd
    )
    $PhaseStatus.heap_exchange_runtime_entry_ensured = Invoke-Checked "Ensure heap/exchange runtime entry" {
        & $ResolvedPythonExe @HeapExchangeEntryArgs
    }
    $ReportFiles += $HeapExchangeEntryJson
    $ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeEntryMd
    $PhaseReports.heap_exchange_runtime_entry = $HeapExchangeEntryJson
}
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-ENSURE-END

# IA-CARMINE-HEAP-PEER-RUNTIME-MANIFEST-BEGIN
$HeapPeerRuntimeJson = Join-Path $AiPacketsDir "heap_peer_runtime_manifest.json"
$HeapPeerRuntimeMd = Join-Path $AiPacketsDir "heap_peer_runtime_manifest.md"
$HeapPeerRuntimeArgs = @(
    "Tools/ai/build_heap_peer_runtime_manifest.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--observer-dir", $HeapExchangeObserverDir,
    "--output", $HeapPeerRuntimeJson,
    "--markdown-output", $HeapPeerRuntimeMd
)
$PhaseStatus.heap_peer_runtime_manifest = Invoke-Checked "Build heap peer runtime manifest" {
    & $ResolvedPythonExe @HeapPeerRuntimeArgs
}
$ReportFiles += $HeapPeerRuntimeJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapPeerRuntimeMd
$PhaseReports.heap_peer_runtime_manifest = $HeapPeerRuntimeJson
$PhaseReports.heap_peer_runtime_manifest_markdown = $HeapPeerRuntimeMd
# IA-CARMINE-HEAP-PEER-RUNTIME-MANIFEST-END

# IA-CARMINE-HEAP-EXCHANGE-CLOSURE-AUDIT-BEGIN
$HeapExchangeClosureAuditJson = Join-Path $AiPacketsDir "heap_exchange_closure_audit.json"
$HeapExchangeClosureAuditMd = Join-Path $AiPacketsDir "heap_exchange_closure_audit.md"
$HeapExchangeClosureAuditArgs = @(
    "Tools/ai/build_heap_exchange_closure_audit.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--heap-peer-runtime", $HeapPeerRuntimeJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--observer-dir", $HeapExchangeObserverDir,
    "--output", $HeapExchangeClosureAuditJson,
    "--markdown-output", $HeapExchangeClosureAuditMd
)
$PhaseStatus.heap_exchange_closure_audit = Invoke-Checked "Build heap/exchange closure audit" {
    & $ResolvedPythonExe @HeapExchangeClosureAuditArgs
}
$ReportFiles += $HeapExchangeClosureAuditJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeClosureAuditMd
$PhaseReports.heap_exchange_closure_audit = $HeapExchangeClosureAuditJson
$PhaseReports.heap_exchange_closure_audit_markdown = $HeapExchangeClosureAuditMd
# IA-CARMINE-HEAP-EXCHANGE-CLOSURE-AUDIT-END

$LegacyFullToolboxReport = ""
if ($RunLegacyFullToolboxIntegrated) {
    $LegacyFullToolboxReport = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_integrated.json"
    $LegacyArgs = @{
        RepoRoot = "."
        OutputRoot = $OutputDir
        EvidenceDir = $EvidenceDir
        Stamp = $Stamp
        BudgetMinutes = $BudgetMinutes
        MaxRounds = $MaxRounds
        FilesPerRound = $FilesPerRound
        MaxContextFiles = $MaxContextFiles
        MaxCharsPerFile = $MaxCharsPerFile
        MaxNewTokens = $MaxNewTokens
        KeepAlive = $KeepAlive
        NpuAuditorEveryRounds = $NpuAuditorEveryRounds
        NpuAuditorTimeoutSeconds = $NpuAuditorTimeoutSeconds
        NpuMaxContextChars = $NpuMaxContextChars
        NpuMaxPromptChars = $NpuMaxPromptChars
        NpuMaxNewTokens = $NpuMaxNewTokens
        NpuFinalWaitSeconds = $NpuFinalWaitSeconds
        NpuMicroStartMode = $NpuMicroStartMode
        MinRecommendations = $MinRecommendations
        MinPatchPlans = $MinPatchPlans
        RepositoryConsistencyMapWorkers = $RepositoryConsistencyMapWorkers
    }
    if ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality) { $LegacyArgs.RunGpuNpuProvider = $true }
    if ($StrictRealRunActivationEnabled) { $LegacyArgs.RequireProviderArtifacts = $true }
    if ($RunLegacyNpuAuditorProvider) { $LegacyArgs.RunLegacyNpuAuditorProvider = $true }
    if ($NoMemoryWrite) { $LegacyArgs.SkipMemoryReload = $true }
    if ($NoEvidence) { $LegacyArgs.SkipSharedToolboxBundle = $true }
# IA-CARMINE-GPU0-PROVIDER-SUPPORT-BEGIN
if ($Full0To10 -or $RunOpenVinoGpu0Workload) {
    $Gpu0ProviderSupportJson = Join-Path $OutputDir ("validation/openvino_gpu0_provider_support_{0}.json" -f $DataStamp)
    $Gpu0ProviderSupportMd = Join-Path $OutputDir ("validation/openvino_gpu0_provider_support_{0}.md" -f $DataStamp)
    $Gpu0SupportOk = Invoke-Checked "Run OpenVINO GPU.0 provider support lane" {
        & $ResolvedPythonExe .\Tools\ai\build_openvino_gpu0_workload_report.py `
            --repo-root . `
            --output $Gpu0ProviderSupportJson `
            --markdown-output $Gpu0ProviderSupportMd `
            --iterations 96 `
            --min-seconds 3 `
            --role provider_support_diagnostic `
            --production-support
    } -SoftFail
    if (Get-Variable -Name ReportFiles -ErrorAction SilentlyContinue) {
        $ReportFiles += @($Gpu0ProviderSupportJson, $Gpu0ProviderSupportMd)
    }
    if (-not $Gpu0SupportOk) {
        if (Get-Variable -Name Warnings -ErrorAction SilentlyContinue) {
            $Warnings += "GPU0 provider support lane failed or degraded; see $Gpu0ProviderSupportJson"
        }
    }
}
# IA-CARMINE-GPU0-PROVIDER-SUPPORT-END

    $PhaseStatus.legacy_full_toolbox_integrated = Invoke-Checked "Run legacy full-toolbox integrated 0-to-10 lane" {
        & .\Tools\workflow\run_agent_review_full_toolbox_decision_loop_integrated.ps1 @LegacyArgs
    } -SoftFail:$ContinueOnValidationError
    if (Test-Path -LiteralPath $LegacyFullToolboxReport -PathType Leaf) {
        $ReportFiles += $LegacyFullToolboxReport
        $PhaseReports.legacy_full_toolbox_integrated = $LegacyFullToolboxReport
        foreach ($PeerReport in @(
            (Join-Path $OutputDir ("validation/gpu1_primary_advisory_{0}.json" -f $DataStamp)),
            (Join-Path $OutputDir ("validation/gpu0_peer_task_packet_{0}.json" -f $DataStamp)),
            (Join-Path $OutputDir ("validation/gpu0_peer_response_{0}.json" -f $DataStamp)),
            (Join-Path $OutputDir ("validation/gpu0_tool_requests_{0}.json" -f $DataStamp)),
            (Join-Path $OutputDir ("validation/gpu0_peer_runtime_tool_broker_{0}.json" -f $DataStamp)),
            (Join-Path $OutputDir ("validation/ai_peer_exchange_{0}.json" -f $DataStamp)),
            (Join-Path $OutputDir ("validation/ai_peer_exchange_contract_{0}.json" -f $DataStamp))
        )) {
            if (Test-Path -LiteralPath $PeerReport -PathType Leaf) {
                $ReportFiles += $PeerReport
            }
        }
        $PhaseReports.ai_peer_exchange = Join-Path $OutputDir ("validation/ai_peer_exchange_{0}.json" -f $DataStamp)
        $PhaseReports.ai_peer_exchange_contract = Join-Path $OutputDir ("validation/ai_peer_exchange_contract_{0}.json" -f $DataStamp)

# IA-CARMINE-FULL0TO10-PROVIDER-ACCEPTANCE-BEGIN
if ($Full0To10) {
    $ProviderAcceptanceJson = Join-Path $OutputDir ("validation/full0to10_provider_acceptance_{0}.json" -f $DataStamp)
    $ProviderAcceptanceMd = Join-Path $OutputDir ("validation/full0to10_provider_acceptance_{0}.md" -f $DataStamp)
    $Gpu0ProviderSupportJsonForGate = Join-Path $OutputDir ("validation/openvino_gpu0_provider_support_{0}.json" -f $DataStamp)
    $Gpu0FinalWorkloadJsonForGate = Join-Path $OutputDir ("validation/openvino_gpu0_workload_{0}.json" -f $DataStamp)
    $Gpu0CompanionJsonForGate = Join-Path $OutputDir ("validation/gpu0_companion_task_lane_{0}.json" -f $DataStamp)
    $AiPeerExchangeJsonForGate = Join-Path $OutputDir ("validation/ai_peer_exchange_{0}.json" -f $DataStamp)
    $AiPeerContractJsonForGate = Join-Path $OutputDir ("validation/ai_peer_exchange_contract_{0}.json" -f $DataStamp)
    $ProviderGateOk = Invoke-Checked "Full0To10 provider acceptance gate" {
        & $ResolvedPythonExe .\Tools\validation\check_full0to10_provider_acceptance.py `
            --repo-root . `
            --stamp $DataStamp `
            --gpu0-provider-support $Gpu0ProviderSupportJsonForGate `
            --gpu0-final-workload $Gpu0FinalWorkloadJsonForGate `
            --gpu0-companion-lane $Gpu0CompanionJsonForGate `
            --ai-peer-exchange $AiPeerExchangeJsonForGate `
            --ai-peer-contract $AiPeerContractJsonForGate `
            --output $ProviderAcceptanceJson `
            --markdown-output $ProviderAcceptanceMd
    } -SoftFail
    if (Get-Variable -Name ReportFiles -ErrorAction SilentlyContinue) {
        $ReportFiles += @($ProviderAcceptanceJson, $ProviderAcceptanceMd)
    }
    if (Get-Variable -Name PhaseReports -ErrorAction SilentlyContinue) {
        $PhaseReports.full0to10_provider_acceptance = $ProviderAcceptanceJson
    }
    if (-not $ProviderGateOk) {
        if (Get-Variable -Name Warnings -ErrorAction SilentlyContinue) {
            $Warnings += "Full0To10 provider acceptance gate failed/degraded; see $ProviderAcceptanceJson"
        }
    }
}
# IA-CARMINE-FULL0TO10-PROVIDER-ACCEPTANCE-END
    }
}


# IA-CARMINE-GPU0-WORKLOAD-BEFORE-OFFICIAL-BEGIN
if ($RunOpenVinoGpu0Workload -or $Full0To10) {
    Write-Host ""
    Write-Host "=== Run OpenVINO GPU.0 secondary workload evidence ==="
    $Gpu0Stamp = $Stamp
    if ([string]::IsNullOrWhiteSpace($Gpu0Stamp)) { $Gpu0Stamp = Get-Date -Format "yyyyMMdd-HHmmss" }

    $Gpu0Json = Join-Path $OutputDir ("validation/openvino_gpu0_workload_{0}.json" -f $Gpu0Stamp)
    $Gpu0Md = Join-Path $OutputDir ("validation/openvino_gpu0_workload_{0}.md" -f $Gpu0Stamp)
    Invoke-Python @(
        "Tools/ai/build_openvino_gpu0_workload_report.py",
        "--repo-root", ".",
        "--output", $Gpu0Json,
        "--markdown-output", $Gpu0Md
    )
    if (Get-Variable -Name ReportFiles -ErrorAction SilentlyContinue) {
        $ReportFiles += $Gpu0Json
        $ReportFiles += $Gpu0Md
    }
    if (Get-Variable -Name PhaseReports -ErrorAction SilentlyContinue) {
        $PhaseReports.openvino_gpu0_workload = $Gpu0Json.Replace("\", "/")
        $PhaseReports.openvino_gpu0_workload_markdown = $Gpu0Md.Replace("\", "/")
    }

# IA-CARMINE-FULL0TO10-PROVIDER-ACCEPTANCE-LATE-BEGIN
if ($Full0To10) {
    $ProviderAcceptanceJson = Join-Path $OutputDir ("validation/full0to10_provider_acceptance_{0}.json" -f $DataStamp)
    $ProviderAcceptanceMd = Join-Path $OutputDir ("validation/full0to10_provider_acceptance_{0}.md" -f $DataStamp)
    $Gpu0ProviderSupportJsonForGate = Join-Path $OutputDir ("validation/openvino_gpu0_provider_support_{0}.json" -f $DataStamp)
    $Gpu0FinalWorkloadJsonForGate = Join-Path $OutputDir ("validation/openvino_gpu0_workload_{0}.json" -f $DataStamp)
    $Gpu0CompanionJsonForGate = Join-Path $OutputDir ("validation/gpu0_companion_task_lane_{0}.json" -f $DataStamp)
    $AiPeerExchangeJsonForGate = Join-Path $OutputDir ("validation/ai_peer_exchange_{0}.json" -f $DataStamp)
    $AiPeerContractJsonForGate = Join-Path $OutputDir ("validation/ai_peer_exchange_contract_{0}.json" -f $DataStamp)
    $ProviderLateGateOk = Invoke-Checked "Full0To10 provider acceptance gate after final GPU0 workload" {
        & $ResolvedPythonExe .\Tools\validation\check_full0to10_provider_acceptance.py `
            --repo-root . `
            --stamp $DataStamp `
            --gpu0-provider-support $Gpu0ProviderSupportJsonForGate `
            --gpu0-final-workload $Gpu0FinalWorkloadJsonForGate `
            --gpu0-companion-lane $Gpu0CompanionJsonForGate `
            --ai-peer-exchange $AiPeerExchangeJsonForGate `
            --ai-peer-contract $AiPeerContractJsonForGate `
            --require-final-workload `
            --output $ProviderAcceptanceJson `
            --markdown-output $ProviderAcceptanceMd
    } -SoftFail
    if (Get-Variable -Name ReportFiles -ErrorAction SilentlyContinue) {
        $ReportFiles += @($ProviderAcceptanceJson, $ProviderAcceptanceMd)
    }
    if (Get-Variable -Name PhaseReports -ErrorAction SilentlyContinue) {
        $PhaseReports.full0to10_provider_acceptance_after_gpu0_workload = $ProviderAcceptanceJson
    }
    if (-not $ProviderLateGateOk) {
        if (Get-Variable -Name Warnings -ErrorAction SilentlyContinue) {
            $Warnings += "Full0To10 provider acceptance late gate failed/degraded; see $ProviderAcceptanceJson"
        }
    }
}
# IA-CARMINE-FULL0TO10-PROVIDER-ACCEPTANCE-LATE-END
}
# IA-CARMINE-GPU0-WORKLOAD-BEFORE-OFFICIAL-END
if ((Test-ModeEnabled "official") -or (Test-ModeEnabled "provider") -or (Test-ModeEnabled "patch_specs") -or (Test-ModeEnabled "evidence") -or $UseOllamaAdvisory -or $UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $GeneratePatchSpecs -or $BuildEvidence) {
    # IA-CARMINE-OFFICIAL-PHASE-VISIBILITY-BEGIN
    Write-Host ""
    Write-Host "=== Run official local AI pipeline adapter ==="
    $OfficialStamp = $Stamp
    if ([string]::IsNullOrWhiteSpace($OfficialStamp)) { $OfficialStamp = Get-Date -Format "yyyyMMdd-HHmmss" }
    $OfficialRepoRoot = $RepoRoot
    if (Get-Variable -Name ResolvedRepoRoot -ErrorAction SilentlyContinue) { $OfficialRepoRoot = $ResolvedRepoRoot }
    if ([string]::IsNullOrWhiteSpace($OfficialRepoRoot)) { $OfficialRepoRoot = (Resolve-Path ".").Path }
    $OfficialAdapterScript = Join-Path $OfficialRepoRoot "Tools/workflow/run_local_ai_task_via_pipeline.ps1"
    $OfficialRunDir = Join-Path $OutputDir ("local_ai_runs/{0}_official_adapter" -f $OfficialStamp)
    $OfficialBasename = "{0}_official_adapter" -f $OfficialStamp
    $OfficialArgs = @(
        "-PromptFile", $TaskFile,
        "-TaskFile", $TaskFile,
        "-RunDir", $OfficialRunDir,
        "-RepoRoot", $OfficialRepoRoot,
        "-Profile", $Profile,
        "-Basename", $OfficialBasename,
        "-ProposalBasename", ("{0}_proposals" -f $OfficialBasename),
        "-Model", $Model,
        "-MaxContextChars", ([string]$MaxContextChars)
    )
    if ($FullContextGoldenPath) { $OfficialArgs += "-FullContextGoldenPath" }
    if ($UsePrimaryAdvisoryProvider) { $OfficialArgs += "-UsePrimaryAdvisoryProvider" }
    if ($RunMultistepProviderWorkflow) { $OfficialArgs += "-RunMultistepProviderWorkflow" }
    if ($RunOllamaProbe) { $OfficialArgs += "-RunOllamaProbe" }
    if ($RunNpuProbe) { $OfficialArgs += "-RunNpuProbe" }
    if ($RunNpuDecodeSmoke) { $OfficialArgs += "-RunNpuDecodeSmoke" }
    if ($BuildEvidence) { $OfficialArgs += "-BuildEvidence" }
    if ($GeneratePatchSpecs) { $OfficialArgs += "-GeneratePatchSpecs" }
    if ($DryRun) { $OfficialArgs += "-DryRun" }
    if (Get-Command Invoke-UnifiedExternalPhaseCommand -ErrorAction SilentlyContinue) {
        $OfficialPhase = Invoke-UnifiedExternalPhaseCommand -RepoRoot $OfficialRepoRoot -PhaseName "official" -StampValue $OfficialStamp -OutputDir $OutputDir -FilePath $OfficialAdapterScript -Arguments $OfficialArgs -TimeoutSeconds $OfficialAdapterTimeoutSeconds -Skip:$SkipOfficialAdapter
        if (Get-Variable -Name ReportFiles -ErrorAction SilentlyContinue) {
            $ReportFiles += $OfficialPhase.json
            $ReportFiles += $OfficialPhase.markdown
        }
        if (Get-Variable -Name PhaseReports -ErrorAction SilentlyContinue) {
            $PhaseReports.official_phase_status = $OfficialPhase.json.Replace("\", "/")
            $PhaseReports.official_phase_status_markdown = $OfficialPhase.markdown.Replace("\", "/")
        }
        if (Get-Variable -Name PhaseStatus -ErrorAction SilentlyContinue) {
            $PhaseStatus["official"] = $OfficialPhase.status
        }
        if ($OfficialPhase.status -eq "timeout" -or $OfficialPhase.status -eq "skipped") {
            if (Get-Variable -Name Warnings -ErrorAction SilentlyContinue) {
                $Warnings += ("official phase {0}; report={1}" -f $OfficialPhase.status, $OfficialPhase.json)
            }
        }
        if ($OfficialPhase.status -eq "failed" -and -not $ContinueOnValidationError) {
            throw ("official phase failed; report={0}" -f $OfficialPhase.json)
        }
    } else {
        throw "unified_phase_visibility.ps1 helper was not loaded"
    }
    # IA-CARMINE-OFFICIAL-PHASE-VISIBILITY-END
}

if ($UseOllamaAdvisory -or (Test-ModeEnabled "provider")) {
    $OllamaBase = "unified_${ModeName}_ollama_$Stamp"
    $OllamaProposalBase = "unified_${ModeName}_ollama_proposals_$Stamp"
    $PostArgs = @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", ".\Tools\workflow\run_post_validation_ai_packet.ps1",
        "-Profile", $Profile,
        "-OutputDir", "output\ai_pipeline",
        "-Basename", $OllamaBase,
        "-ProposalBasename", $OllamaProposalBase,
        "-ContextFile", ($ContextFiles -join ","),
        "-ReportFile", ($ReportFiles -join ","),
        "-UseOllama",
        "-Model", $Model,
        "-MaxContextChars", "$MaxContextChars"
    )
    if ($UsePrimaryAdvisoryProvider) { $PostArgs += "-UsePrimaryAdvisoryProvider" }
    $PhaseStatus.ollama_advisory = Invoke-Checked "Run Ollama advisory packet" { powershell.exe @PostArgs } -SoftFail:$ContinueOnValidationError
    $PhaseReports.ollama_packet = "output/ai_pipeline/$OllamaBase.json"
    $PhaseReports.ollama_proposals = "output/ai_pipeline/$OllamaProposalBase.json"
}

if ($BuildTaskPatchSuggestionReport -or $ReviewPrApplyDeterministicSuggestions) {
    $TaskSuggestionJson = "$ValidationDir/task_patch_suggestions_${ModeName}_$Stamp.json"
    $TaskSuggestionMd = "$ValidationDir/task_patch_suggestions_${ModeName}_$Stamp.md"
    $PhaseStatus.task_patch_suggestion_report = Invoke-Checked "Build task Markdown patch suggestion report" {
        Invoke-Python @(
            ".\Tools\ai\build_task_patch_suggestion_report.py",
            "--repo-root", ".",
            "--task-file", $TaskFile,
            "--Stamp", $Stamp,
            "--output", $TaskSuggestionJson,
            "--markdown-output", $TaskSuggestionMd
        )
    } -SoftFail:$ContinueOnValidationError
    if (Test-Path -LiteralPath $TaskSuggestionJson -PathType Leaf) {
        $ReportFiles += $TaskSuggestionJson
        $ContextFiles = Add-ExistingContextFile $ContextFiles $TaskSuggestionMd
        $PhaseReports.task_patch_suggestions = $TaskSuggestionJson
        $PhaseReports.task_patch_suggestions_markdown = $TaskSuggestionMd
    }
}

# IA-CARMINE-HEAP-EXCHANGE-PRE-REVIEW-BRIDGE-BEGIN
if ($ReviewPrFromGeneratedPatchSpecs -or $PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) {
    Invoke-UnifiedHeapExchangePreReviewBridge `
        -StampValue $DataStamp `
        -OutputDirValue $OutputDir `
        -Root $RepoRoot `
        -RunDirValue $RunDir `
        -EvidenceDirValue $EvidenceDir
}
# IA-CARMINE-HEAP-EXCHANGE-PRE-REVIEW-BRIDGE-END
if ($ReviewPrFromGeneratedPatchSpecs) {
    $PatchSuggestionJson = "$ValidationDir/generated_patch_specs_review_pr_apply_${ModeName}_$Stamp.json"
    $EffectiveGeneratedPatchSpecsBranch = $ReviewPrBranch
    if ([string]::IsNullOrWhiteSpace($EffectiveGeneratedPatchSpecsBranch)) {
        $EffectiveGeneratedPatchSpecsBranch = "codex/generated-patch-specs-review-pr-$Stamp"
    }
    $GeneratedPatchSpecsArgs = @(
        ".\Tools\ai\apply_generated_patch_specs_for_review_pr.py",
        "--repo-root", ".",
        "--output", $PatchSuggestionJson,
        "--markdown-output", "$ValidationDir/generated_patch_specs_review_pr_apply_${ModeName}_$Stamp.md",
        "--max-applied-patches", ([string]$ReviewPrMaxAppliedPatches),
        "--create-review-branch", $EffectiveGeneratedPatchSpecsBranch
    )
    if (-not [string]::IsNullOrWhiteSpace($ReviewPrPatchSpecManifest)) {
        $GeneratedPatchSpecsArgs += "--manifest"
        $GeneratedPatchSpecsArgs += $ReviewPrPatchSpecManifest
    }
    if ($ReviewPrRequireAllValidators) { $GeneratedPatchSpecsArgs += "--require-all-validators" }
    if ($PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) { $GeneratedPatchSpecsArgs += "--apply" }
    if ($AllowDirty) { $GeneratedPatchSpecsArgs += "--allow-dirty"; $GeneratedPatchSpecsArgs += "--allow-dirty-branch" }
    $ReviewPrBranch = $EffectiveGeneratedPatchSpecsBranch
    Invoke-Checked "Apply generated patch specs for review PR" { Invoke-Python $GeneratedPatchSpecsArgs }

# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN
$HeapExchangeExitJson = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.json"
$HeapExchangeExitMd = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.md"
$HeapExchangeExitArgs = @(
    "Tools/ai/build_heap_exchange_runtime_exit.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--apply-report", $PatchSuggestionJson,
    "--observer-dir", $HeapExchangeObserverDir,
    "--output", $HeapExchangeExitJson,
    "--markdown-output", $HeapExchangeExitMd
)
if ($ReviewPrFromGeneratedPatchSpecs) { $HeapExchangeExitArgs += "--require-concrete-product" }
$HeapExchangeExitOk = Invoke-Checked "Build heap/exchange runtime exit product" {
    & $ResolvedPythonExe @HeapExchangeExitArgs
}
$ReportFiles += $HeapExchangeExitJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeExitMd
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-END

}

if (($PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) -and -not $ReviewPrFromGeneratedPatchSpecs) {
    $PatchSuggestionJson = "$ValidationDir/patch_suggestion_bundle_apply_${ModeName}_$Stamp.json"
    $PatchSuggestionArgs = @(
        ".\Tools\ai\apply_patch_suggestion_bundle.py",
        "--repo-root", ".",
        "--Stamp", $Stamp,
        "--output", $PatchSuggestionJson
    )
    if ($ReviewPrApplyDeterministicSuggestions) {
        if ($PrepareReviewPr -and -not [string]::IsNullOrWhiteSpace($ReviewPrBranch)) {
            $PatchSuggestionArgs += @("--create-review-branch", $ReviewPrBranch, "--allow-dirty-branch")
        }
        $PatchSuggestionArgs += "--apply"
        if ($AllowDirty) { $PatchSuggestionArgs += "--allow-dirty" }
    }
    $PhaseStatus.patch_suggestion_final_phase = Invoke-Checked "Patch suggestion final phase product" {
        Invoke-Python $PatchSuggestionArgs
    } -SoftFail:$ContinueOnValidationError
    if (Test-Path -LiteralPath $PatchSuggestionJson -PathType Leaf) {
        $ReportFiles += $PatchSuggestionJson
        $PhaseReports.patch_suggestion_final_phase = $PatchSuggestionJson
    }
}

if (($PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) -and (Test-Path -LiteralPath $PatchSuggestionJson -PathType Leaf)) {


# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-BEGIN
if (($PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) -and -not $ReviewPrFromGeneratedPatchSpecs) {
    $HeapExchangeExitJson = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.json"
    $HeapExchangeExitMd = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.md"

    $HeapExchangeExitArgs = @(
        "Tools/ai/build_heap_exchange_runtime_exit.py",
        "--repo-root", ".",
        "--stamp", $DataStamp,
        "--runtime-entry", $HeapExchangeEntryJson,
        "--runtime-state", $HeapExchangeRuntimeState,
        "--apply-report", $PatchSuggestionJson,
        "--observer-dir", $HeapExchangeObserverDir,
        "--output", $HeapExchangeExitJson,
        "--markdown-output", $HeapExchangeExitMd,
        "--require-concrete-product"
    )

    $PhaseStatus.heap_exchange_runtime_exit_after_patch_suggestion = Invoke-Checked "Build heap/exchange runtime exit product after patch suggestion product" {
        & $ResolvedPythonExe @HeapExchangeExitArgs
    }

    $ReportFiles += $HeapExchangeExitJson
    $ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeExitJson
    $ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeExitMd
}
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-END

# IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-BEGIN
$HeapExchangeLifecycleJson = Join-Path $OutputDir ("validation/heap_exchange_runtime_lifecycle_{0}.json" -f $DataStamp)
$HeapExchangeLifecycleMd = Join-Path $OutputDir ("validation/heap_exchange_runtime_lifecycle_{0}.md" -f $DataStamp)
$HeapExchangeLifecycleArgs = @(
    "Tools/validation/check_heap_exchange_runtime_lifecycle.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--runtime-exit", $HeapExchangeExitJson,
    "--observer-dir", $HeapExchangeObserverDir,
    "--require-public-events",
    "--require-knowledge-surface",
    "--output", $HeapExchangeLifecycleJson,
    "--markdown-output", $HeapExchangeLifecycleMd
)
if ($PrepareReviewPr -or $ReviewPrFromGeneratedPatchSpecs -or $ReviewPrApplyDeterministicSuggestions) { $HeapExchangeLifecycleArgs += "--require-concrete-exit" }
$HeapExchangeLifecycleOk = Invoke-Checked "Validate heap/exchange runtime lifecycle" {
    & $ResolvedPythonExe @HeapExchangeLifecycleArgs
}
$ReportFiles += $HeapExchangeLifecycleJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeLifecycleMd
# IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-END

# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-BEGIN
# Deferred intentionally.
# The unified chain contract is a final product gate and must run after:
# - patch suggestion product separation
# - prepare_review_pr.py
# - manifest write
# Running it here validates before the review PR product exists.
# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-END

    $PatchSuggestionProductSeparationJson = "$ValidationDir/patch_suggestion_product_separation_${ModeName}_$Stamp.json"
    $PatchSuggestionProductSeparationArgs = @(
        ".\Tools\validation\check_patch_suggestion_product_separation.py",
        "--repo-root", ".",
        "--report", $PatchSuggestionJson,
        "--output", $PatchSuggestionProductSeparationJson
    )
    if ($PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) {
        $PatchSuggestionProductSeparationArgs += "--require-product"
    }
    $PhaseStatus.patch_suggestion_product_separation = Invoke-Checked "Validate patch suggestion product separation" {
        Invoke-Python $PatchSuggestionProductSeparationArgs
    } -SoftFail:$ContinueOnValidationError
    if (Test-Path -LiteralPath $PatchSuggestionProductSeparationJson -PathType Leaf) {
        $ReportFiles += $PatchSuggestionProductSeparationJson
        $PhaseReports.patch_suggestion_product_separation = $PatchSuggestionProductSeparationJson
    }
}

if (Test-ModeEnabled "full_validation") {
    $PhaseStatus.git_diff_check_final = Invoke-Checked "Final git diff --check" { git diff --check } -SoftFail:$ContinueOnValidationError
    $PhaseStatus.git_status_final = Invoke-Checked "Final git status --short" { git status --short } -SoftFail:$ContinueOnValidationError
}

if ($PrepareReviewPr) {
    $ReviewPrJson = "$ValidationDir/review_pr_prepare_${ModeName}_$Stamp.json"
    $ReviewPrMd = "$ValidationDir/review_pr_prepare_${ModeName}_$Stamp.md"
    $ReviewEvidenceJson = Join-Path $EvidenceDir ("review_pr_prepare_{0}.json" -f $Stamp)
    $ReviewEvidenceMd = Join-Path $EvidenceDir ("review_pr_prepare_{0}.md" -f $Stamp)
        $ReviewPrArgsContextJson = "$ValidationDir/review_pr_prepare_args_context_${ModeName}_$Stamp.json"
        $ReviewPrArgsJson = "$ValidationDir/review_pr_prepare_args_${ModeName}_$Stamp.json"
    
        $ReviewPrApplyReport = ""
        if ((Get-Variable -Name PatchSuggestionJson -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $PatchSuggestionJson -PathType Leaf)) {
            $ReviewPrApplyReport = $PatchSuggestionJson
        }
    
        $ReviewPrArgsContext = [ordered]@{
            repo_root = "."
            stamp = $Stamp
            task_file = $TaskFile
            branch = $ReviewPrBranch
            base = $ReviewPrBaseBranch
            remote = $ReviewPrRemote
            title = $ReviewPrTitle
            commit_message = $ReviewPrCommitMessage
            output = $ReviewPrJson
            markdown_output = $ReviewPrMd
            evidence_output = $ReviewEvidenceJson
            evidence_markdown_output = $ReviewEvidenceMd
            include_paths = @($ReviewPrIncludePath)
            apply_report = $ReviewPrApplyReport
            auto_include_from_apply_report = [bool](-not [string]::IsNullOrWhiteSpace($ReviewPrApplyReport))
            require_product_input = $true
            allow_dirty_branch = $true
            push = [bool]$ReviewPrPush
            create_pr = [bool]$ReviewPrCreate
            draft_pr = [bool]$ReviewPrDraft
            dry_run = [bool]$DryRun
        }
        ($ReviewPrArgsContext | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ReviewPrArgsContextJson -Encoding UTF8
    
        $PhaseStatus.review_pr_prepare_args = Invoke-Checked "Build review PR prepare args" {
            & $ResolvedPythonExe "Tools/ai/build_review_pr_prepare_args.py" `
                "--context", $ReviewPrArgsContextJson `
                "--output", $ReviewPrArgsJson
        } -SoftFail:$ContinueOnValidationError
    
        $ReviewPrArgsReport = Get-Content -LiteralPath $ReviewPrArgsJson -Raw | ConvertFrom-Json
        if (-not [bool]$ReviewPrArgsReport.passed) {
            throw "Review PR prepare args builder failed: $($ReviewPrArgsReport.errors -join '; ')"
        }

        $ReviewPrReadinessJson = "$ValidationDir/review_pr_product_readiness_${ModeName}_$Stamp.json"
        $ReviewPrReadinessMd = "$ValidationDir/review_pr_product_readiness_${ModeName}_$Stamp.md"
        $PhaseStatus.review_pr_product_readiness = Invoke-Checked "Validate review PR product readiness" {
            & $ResolvedPythonExe "Tools/validation/check_review_pr_product_readiness.py" `
                "--repo-root", "." `
                "--args-report", $ReviewPrArgsJson `
                "--output", $ReviewPrReadinessJson `
                "--markdown-output", $ReviewPrReadinessMd
        } -SoftFail:$ContinueOnValidationError
        if (Test-Path -LiteralPath $ReviewPrReadinessJson -PathType Leaf) {
            $ReportFiles += $ReviewPrReadinessJson
            $PhaseReports.review_pr_product_readiness = $ReviewPrReadinessJson
        }
        $ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $ReviewPrReadinessMd
        $ReviewArgs = @($ReviewPrArgsReport.argv | ForEach-Object { [string]$_ })
    $PhaseStatus.review_pr_prepare = Invoke-Checked "Prepare review branch and PR" {
        Invoke-Python $ReviewArgs
    } -SoftFail:$ContinueOnValidationError
    if (Test-Path -LiteralPath $ReviewPrArgsJson -PathType Leaf) {
        $ReportFiles += $ReviewPrArgsJson
        $PhaseReports.review_pr_prepare_args = $ReviewPrArgsJson
    }
    if (Test-Path -LiteralPath $ReviewPrJson -PathType Leaf) {
        $ReportFiles += $ReviewPrJson
        $ContextFiles = Add-ExistingContextFile $ContextFiles $ReviewPrMd
        $PhaseReports.review_pr_prepare = $ReviewPrJson
        $PhaseReports.review_pr_prepare_markdown = $ReviewPrMd
    }
    if (Test-Path -LiteralPath $ReviewEvidenceJson -PathType Leaf) {
        $PhaseReports.review_pr_evidence = $ReviewEvidenceJson
        $PhaseReports.review_pr_evidence_markdown = $ReviewEvidenceMd
    }
}

$ManifestPath = "$PipelineDir/unified_local_ai_refactor_manifest.json"
$Manifest = [ordered]@{
    schema_version = 1
    kind = "unified_local_ai_refactor_manifest"
    generated_at = (Get-Date -Format o)
    repo_root = $RepoRoot
    mode = $ResolvedModes
    mode_name = $ModeName
    full_0_to_10_requested = [bool]$Full0To10
    full0to10_legacy_alias_requested = [bool]$Full0To10
    full0to10_standalone_pipeline = $false
    unified_run_operational_model = "single_dynamic_heap_exchange_run"
    unified_run_source_of_knowledge = "heap_exchange"
    unified_run_final_product = "reviewable_pr_with_concrete_changes"
    available_modes = @($ModeDescriptions.Keys)
    profile = $Profile
    model = $Model
    run_intensity = $RunIntensity
    budget_minutes = $BudgetMinutes
    max_rounds = $MaxRounds
    files_per_round = $FilesPerRound
    max_context_files = $MaxContextFiles
    max_chars_per_file = $MaxCharsPerFile
    max_new_tokens = $MaxNewTokens
    keep_alive = $KeepAlive
    npu_auditor_every_rounds = $NpuAuditorEveryRounds
    npu_auditor_timeout_seconds = $NpuAuditorTimeoutSeconds
    npu_max_context_chars = $NpuMaxContextChars
    npu_max_prompt_chars = $NpuMaxPromptChars
    npu_max_new_tokens = $NpuMaxNewTokens
    npu_final_wait_seconds = $NpuFinalWaitSeconds
    min_recommendations = $MinRecommendations
    min_patch_plans = $MinPatchPlans
    max_recommendations = $MaxRecommendations
    max_patch_plans = $MaxPatchPlans
    repository_consistency_map_workers = $RepositoryConsistencyMapWorkers
    provider_max_context_chars = $ProviderMaxContextChars
    context_pack_max_total_chars = $ContextPackMaxTotalChars
    context_pack_max_file_chars = $ContextPackMaxFileChars
    agent_state_max_memory_chars = $AgentStateMaxMemoryChars
    legacy_full_toolbox_integrated_requested = [bool]$RunLegacyFullToolboxIntegrated
    legacy_npu_auditor_provider_requested = [bool]$RunLegacyNpuAuditorProvider
    python_exe = $ResolvedPythonExe
    python_exe_requested = $PythonExe
    pythonpath = $env:PYTHONPATH
    ia_carmine_python_env = $env:IA_CARMINE_PYTHON
    stamp = $Stamp
    task_file = $TaskFile.Replace("\", "/")
    task_branch = $TaskBranch
    run_dir = $RunDir.Replace("\", "/")
    provider_execution_requested = [bool]($UseOllamaAdvisory -or $UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke -or (Test-ModeEnabled "provider"))
    primary_provider_requested = [bool]$UsePrimaryAdvisoryProvider
    ai_peer_exchange_required = [bool]($Full0To10 -or $StrictRealRunActivationEnabled)
    gpu1_primary_advisory_role = "mandatory_primary_advisory_planner"
    gpu0_companion_peer_role = "openvino_companion_peer_worker"
    npu_micro_lane_role = "micro_fast_task_assistant"
    deterministic_script_role = "heavy_audit_authority"
    runtime_tool_broker_role = "controlled_gpu1_gpu0_tool_execution"
    workload_quality_report = $WorkloadQualityReport
    workload_quality_routing_ok = [bool]$WorkloadQualityRoutingOk
    multistep_provider_workflow_requested = [bool]$RunMultistepProviderWorkflow
    ollama_probe_requested = [bool]$RunOllamaProbe
    npu_probe_requested = [bool]$RunNpuProbe
    npu_decode_smoke_requested = [bool]$RunNpuDecodeSmoke
    memory_in_enabled = [bool](Test-ModeEnabled "agent_state")
    memory_out_enabled = [bool]$SaveInputsToMemoryDb
    quality_gate_passed = [bool](((-not $UsePrimaryAdvisoryProvider) -or $NoWorkloadQuality) -or $WorkloadQualityRoutingOk)
    reset_apply_requested = [bool]$ApplyReset
    review_pr_prepare_requested = [bool]$PrepareReviewPr
    review_pr_branch = $ReviewPrBranch
    review_pr_base_branch = $ReviewPrBaseBranch
    review_pr_push_requested = [bool]$ReviewPrPush
    review_pr_create_requested = [bool]$ReviewPrCreate
    review_pr_apply_deterministic_suggestions = [bool]$ReviewPrApplyDeterministicSuggestions
    review_pr_from_generated_patch_specs = [bool]$ReviewPrFromGeneratedPatchSpecs
    review_pr_patch_spec_manifest = $ReviewPrPatchSpecManifest
    review_pr_max_applied_patches = $ReviewPrMaxAppliedPatches
    review_pr_require_all_validators = [bool]$ReviewPrRequireAllValidators
    review_pr_draft_requested = [bool]$ReviewPrDraft
    runtime_evidence_correlation_requested = [bool]$BuildRuntimeEvidenceCorrelation
    task_patch_suggestion_report_requested = [bool]($BuildTaskPatchSuggestionReport -or $ReviewPrApplyDeterministicSuggestions)
    patch_application_requested = [bool]($ReviewPrApplyDeterministicSuggestions -or (($PrepareReviewPr -or $ReviewPrApplyDeterministicSuggestions) -and $ReviewPrFromGeneratedPatchSpecs))
    patch_application_performed = $false
    patch_specs_requested = [bool]($GeneratePatchSpecs -or (Test-ModeEnabled "patch_specs"))
    build_evidence_requested = [bool]($BuildEvidence -or (Test-ModeEnabled "evidence"))
    memory_db = $MemoryDb
    save_inputs_to_memory_db = [bool]$SaveInputsToMemoryDb
    context_files = $ContextFiles
    report_files = $ReportFiles
    phase_status = $PhaseStatus
    phase_reports = $PhaseReports
    warnings = $Warnings
    errors = @()
}
($Manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-BEGIN
$UnifiedChainContractJson = Join-Path $OutputDir ("validation/unified_chain_contract_{0}.json" -f $DataStamp)
$UnifiedChainContractMd = Join-Path $OutputDir ("validation/unified_chain_contract_{0}.md" -f $DataStamp)
$UnifiedChainArgsContextJson = Join-Path $OutputDir ("validation/unified_chain_contract_args_context_{0}.json" -f $DataStamp)
$UnifiedChainArgsJson = Join-Path $OutputDir ("validation/unified_chain_contract_args_{0}.json" -f $DataStamp)

$UnifiedChainApplyReport = ""
if ((Get-Variable -Name PatchSuggestionJson -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $PatchSuggestionJson -PathType Leaf)) {
    $UnifiedChainApplyReport = $PatchSuggestionJson
}

$UnifiedChainProductSeparationReport = ""
if ((Get-Variable -Name PatchSuggestionProductSeparationJson -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $PatchSuggestionProductSeparationJson -PathType Leaf)) {
    $UnifiedChainProductSeparationReport = $PatchSuggestionProductSeparationJson
}

$UnifiedChainReviewPrReport = ""
if ((Get-Variable -Name ReviewPrJson -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $ReviewPrJson -PathType Leaf)) {
    $UnifiedChainReviewPrReport = $ReviewPrJson
}

$UnifiedChainArgsContext = [ordered]@{
    repo_root = "."
    stamp = $DataStamp
    mode_name = $ModeName
    manifest = $ManifestPath
    apply_report = $UnifiedChainApplyReport
    product_separation_report = $UnifiedChainProductSeparationReport
    review_pr_report = $UnifiedChainReviewPrReport
    output_report = $UnifiedChainContractJson
    markdown_report = $UnifiedChainContractMd
    use_primary_advisory_provider = [bool]$UsePrimaryAdvisoryProvider
    run_multistep_provider_workflow = [bool]$RunMultistepProviderWorkflow
    use_ollama_advisory = [bool]$UseOllamaAdvisory
    run_ollama_probe = [bool]$RunOllamaProbe
    open_extended_observer_consoles = [bool]$OpenExtendedObserverConsoles
    review_pr_from_generated_patch_specs = [bool]$ReviewPrFromGeneratedPatchSpecs
    prepare_review_pr = [bool]$PrepareReviewPr
    review_pr_apply_deterministic_suggestions = [bool]$ReviewPrApplyDeterministicSuggestions
    heap_peer_runtime = $HeapPeerRuntimeJson
    shared_memory_evidence = $HeapPeerRuntimeJson
    closure_audit_report = $HeapExchangeClosureAuditJson
}
($UnifiedChainArgsContext | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $UnifiedChainArgsContextJson -Encoding UTF8

$UnifiedChainArgsBuilderOk = Invoke-Checked "Build final unified chain contract args" {
    & $ResolvedPythonExe "Tools/ai/build_unified_chain_contract_args.py" `
        "--context", $UnifiedChainArgsContextJson `
        "--output", $UnifiedChainArgsJson
}

$UnifiedChainArgsReport = Get-Content -LiteralPath $UnifiedChainArgsJson -Raw | ConvertFrom-Json
if (-not [bool]$UnifiedChainArgsReport.passed) {
    throw "Final unified chain contract args builder failed: $($UnifiedChainArgsReport.errors -join '; ')"
}
$UnifiedChainArgs = @($UnifiedChainArgsReport.argv | ForEach-Object { [string]$_ })

$UnifiedChainContractOk = Invoke-Checked "Validate final unified heap/exchange chain contract" {
    & $ResolvedPythonExe @UnifiedChainArgs
}

$ReportFiles += $UnifiedChainArgsJson
$ReportFiles += $UnifiedChainContractJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $UnifiedChainContractMd
$PhaseStatus.unified_chain_contract_args = $UnifiedChainArgsBuilderOk
$PhaseStatus.unified_chain_contract_final = $UnifiedChainContractOk
$PhaseReports.unified_chain_contract_args = $UnifiedChainArgsJson
$PhaseReports.unified_chain_contract = $UnifiedChainContractJson
$PhaseReports.unified_chain_contract_markdown = $UnifiedChainContractMd

$Manifest.report_files = $ReportFiles
$Manifest.context_files = $ContextFiles
$Manifest.phase_status = $PhaseStatus
$Manifest.phase_reports = $PhaseReports
($Manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-END

# IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-FINAL-BEGIN
if ($BuildRuntimeEvidenceCorrelation) {
    $RuntimeEvidenceCorrelationJson = "$ValidationDir/runtime_evidence_correlation_${ModeName}_$Stamp.json"
    $RuntimeEvidenceCorrelationMd = "$ValidationDir/runtime_evidence_correlation_${ModeName}_$Stamp.md"

    function Add-ExistingRuntimeEvidencePathArg {
        param(
            [string[]]$ArgsValue,
            [string]$Flag,
            [string[]]$VariableNames
        )

        foreach ($VariableName in $VariableNames) {
            $CandidateVariable = Get-Variable -Name $VariableName -ErrorAction SilentlyContinue
            if ($null -eq $CandidateVariable) { continue }
            $CandidateValue = [string]$CandidateVariable.Value
            if ([string]::IsNullOrWhiteSpace($CandidateValue)) { continue }
            if (Test-Path -LiteralPath $CandidateValue -PathType Leaf) {
                return @($ArgsValue + $Flag + $CandidateValue)
            }
        }

        return $ArgsValue
    }

    $RuntimeEvidenceCorrelationArgs = @(
        "Tools/validation/check_runtime_evidence_correlation.py",
        "--repo-root", ".",
        "--stamp", $DataStamp,
        "--output", $RuntimeEvidenceCorrelationJson,
        "--markdown-output", $RuntimeEvidenceCorrelationMd
    )

    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--preflight-report" -VariableNames @("PreflightOutput")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--heap-entry" -VariableNames @("HeapExchangeEntryJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--heap-peer-runtime" -VariableNames @("HeapPeerRuntimeJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--gpu0-report" -VariableNames @("OpenVinoGpu0WorkloadJson", "OpenVinoGpu0Report", "Gpu0WorkloadJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--npu-report" -VariableNames @("NpuMicroCompanionJson", "NpuMicroReport", "NpuReport")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--shared-memory-evidence" -VariableNames @("SharedToolboxBundleJson", "HeapPeerRuntimeJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--tool-broker-report" -VariableNames @("RuntimeToolCapabilityManifestJson", "FullToolboxRunTelemetrySummaryJson", "FullToolboxTelemetrySummaryJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--closure-audit-report" -VariableNames @("HeapExchangeClosureAuditJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--product-readiness-report" -VariableNames @("ReviewPrProductReadinessJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--review-pr-report" -VariableNames @("ReviewPrJson")
    $RuntimeEvidenceCorrelationArgs = Add-ExistingRuntimeEvidencePathArg -ArgsValue $RuntimeEvidenceCorrelationArgs -Flag "--unified-chain-contract" -VariableNames @("UnifiedChainContractJson")

    $PhaseStatus.runtime_evidence_correlation = Invoke-Checked "Build runtime evidence correlation" {
        Invoke-Python $RuntimeEvidenceCorrelationArgs
    }

    if (Test-Path -LiteralPath $RuntimeEvidenceCorrelationJson -PathType Leaf) {
        $ReportFiles += $RuntimeEvidenceCorrelationJson
        $PhaseReports.runtime_evidence_correlation = $RuntimeEvidenceCorrelationJson
    }
    $ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $RuntimeEvidenceCorrelationMd
}
# IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-FINAL-END



Write-Host ""
Write-Host "[OK] Unified local-AI launcher complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $ManifestPath"
Write-Host "[OK] Mode: $($ResolvedModes -join ',')"
Write-Host "[OK] Provider execution requested: $($Manifest.provider_execution_requested)"
Write-Host "[OK] Reset apply requested: $($Manifest.reset_apply_requested)"
Write-Host "[OK] Patch specs requested: $($Manifest.patch_specs_requested)"
Write-Host "[OK] Review PR requested: $($Manifest.review_pr_prepare_requested)"
if ($PrepareReviewPr) { Write-Host "[OK] Review PR branch: $ReviewPrBranch" }
Write-Host "[OK] Patch application performed: False"
Write-Host "[OK] Reports: $($ReportFiles -join ', ')"
Write-Host "[OK] Context files: $($ContextFiles -join ', ')"

Write-UnifiedLauncherExecutionTailEvidence `
    -StampValue $Stamp `
    -Root $RepoRoot `
    -RunDirValue $RunDir `
    -ManifestPathValue "$PipelineDir/unified_local_ai_refactor_manifest.json" `
    -ResolvedModesValue $ResolvedModes `
    -ReportFilesValue $ReportFiles `
    -ContextFilesValue $ContextFiles `
    -ProviderExecutionRequested ([bool]$UsePrimaryAdvisoryProvider) `
    -PatchSpecsRequested ([bool]$GeneratePatchSpecs) `
    -ProdMode ([bool]$Prod) `
    -FailureMessage ""
