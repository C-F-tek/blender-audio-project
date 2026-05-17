# This file is dot-sourced by run_unified_local_ai_refactor.ps1.
# Source lines: 133-651.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Script:UnifiedLauncherCurrentPhase = "startup"
$Script:UnifiedLauncherFailureMessage = ""

if ($ContinueOnValidationError) {
    [Console]::Error.WriteLine("-ContinueOnValidationError is forbidden for unified launcher runs. Fix the failing phase instead of allowing a soft-failed run to complete.")
    exit 2
}

# IA-CARMINE-UNIFIED-PHASE-VISIBILITY-IMPORT-BEGIN
$UnifiedPhaseVisibilityScript = Join-Path $UnifiedLauncherScriptRoot "_powershell/unified_phase_visibility.ps1"
if (Test-Path -LiteralPath $UnifiedPhaseVisibilityScript -PathType Leaf) {
    . $UnifiedPhaseVisibilityScript
} else {
    Write-Warning "Unified phase visibility helper not found: $UnifiedPhaseVisibilityScript"
}
# IA-CARMINE-UNIFIED-PHASE-VISIBILITY-IMPORT-END

# IA-CARMINE-UNIFIED-RUN-OBSERVER-IMPORT-BEGIN
$UnifiedRunObserverScript = Join-Path $UnifiedLauncherScriptRoot "_powershell/unified_run_observer.ps1"
if (Test-Path -LiteralPath $UnifiedRunObserverScript -PathType Leaf) {
    . $UnifiedRunObserverScript
} else {
    Write-Warning "Unified run observer helper not found: $UnifiedRunObserverScript"
}
# IA-CARMINE-UNIFIED-RUN-OBSERVER-IMPORT-END
# IA-CARMINE-HEAP-EXCHANGE-REVIEW-BRIDGE-IMPORT-BEGIN
$UnifiedHeapExchangeReviewBridgeScript = Join-Path $UnifiedLauncherScriptRoot "_powershell/heap_exchange_review_bridge.ps1"
if (Test-Path -LiteralPath $UnifiedHeapExchangeReviewBridgeScript -PathType Leaf) {
    . $UnifiedHeapExchangeReviewBridgeScript
} else {
    Write-Warning "Heap exchange review bridge helper not found: $UnifiedHeapExchangeReviewBridgeScript"
}
# IA-CARMINE-HEAP-EXCHANGE-REVIEW-BRIDGE-IMPORT-END

$ModeOrder = @(
    "smoke", "reset", "validation", "md", "json", "python", "chunks", "context_pack",
    "agent_state", "official", "provider", "patch_specs", "evidence", "contract", "full_validation"
)

$ModeDescriptions = [ordered]@{
    smoke = "Fast smoke checks: git diff --check and python -m Tools.workflow startup_check when available."
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
    Write-Host "Debug tail: enabled by default; use -Prod to disable transcript and execution-tail evidence."
    Write-Host "Startup check output: python -m Tools.workflow startup_check supports --output, --text-output and --repo-root."
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
