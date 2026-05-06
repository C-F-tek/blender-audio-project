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
    [string]$TaskFile = ".\docs\LOCAL_AI_TASKS\docs-md-obsolete-pruning-next-step.md",
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
    [string]$LightFull0To10OutputDir = "output/validation/unified_light_full0to10_profile",
    [switch]$LightFull0To10NoExternalProbes
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# IA-CARMINE-LIGHTFULL0TO10-DISPATCH-BEGIN
if ($LightFull0To10) {
    $LightProfileScript = Join-Path $PSScriptRoot "run_unified_light_full0to10_profile.ps1"
    if (-not (Test-Path $LightProfileScript)) {
        throw "LightFull0To10 profile script not found: $LightProfileScript"
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

    Write-Host "[LightFull0To10] Dispatching evidence-only profile..."
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
    Write-Host "Full 0-to-10 selectable profile: use -Full0To10; disable individual steps only with explicit -No* flags."
    Write-Host "Debug tail: enabled by default; use -Prod to disable transcript and execution-tail evidence."
    Write-Host "Startup check output: Tools/workflow/startup_check.py supports --output, --text-output and --repo-root."
    Write-Host "AI packets output: use -AiPacketsRoot/-AiPacketsDir; default is output/ai_packets/<DataStamp>."
    Write-Host "Strict real-run activation: TUTTO SU TUTTO for every non-smoke/non-reset real run unless an explicit -No* flag disables one."
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
    if ($DryRun) { Write-Host "[DRY-RUN] Skipped execution."; return $true }
    & $Block
    if ($LASTEXITCODE -ne 0) {
        if ($SoftFail) { Write-Warning "$Label failed with exit code $LASTEXITCODE"; return $false }
        throw "$Label failed with exit code $LASTEXITCODE"
    }
    return $true
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

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        return "python"
    }

    throw "No usable Python interpreter found. Set -PythonExe, IA_CARMINE_PYTHON, or install py launcher with Python 3.12/3.13."
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
Write-Host "[INFO] PYTHONPATH: $env:PYTHONPATH"
Write-Host "[INFO] Python: $ResolvedPythonExe"

if ($Full0To10) { $ResolvedModes = @() } elseif ($Interactive -or @($Mode).Count -eq 0) { $ResolvedModes = @(Read-InteractiveModes) } else { $ResolvedModes = @(Normalize-ModeList $Mode) }
if (@($ResolvedModes).Count -eq 0 -and -not $Full0To10) { throw "No modes selected. Use -Interactive or -Mode all." }

if ($Full0To10) {
    $Full0To10Modes = @("md", "json", "python", "chunks", "context_pack", "agent_state", "official", "provider", "patch_specs", "evidence", "contract", "full_validation")
    if ($NoPatchSpecs) { $Full0To10Modes = @($Full0To10Modes | Where-Object { $_ -ne "patch_specs" }) }
    if ($NoEvidence) { $Full0To10Modes = @($Full0To10Modes | Where-Object { $_ -ne "evidence" }) }
    $ResolvedModes = @($Full0To10Modes)

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
    $RunLegacyFullToolboxIntegrated = $true
}


if ([string]::IsNullOrWhiteSpace($Stamp)) { $Stamp = Get-Date -Format "yyyyMMdd-HHmmss" }
$DataStamp = $Stamp
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
    throw
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
    $RunLegacyFullToolboxIntegrated = $true
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
Write-Host "[INFO] Patch specs: $GeneratePatchSpecs"
Write-Host "[INFO] Reset apply: $ApplyReset"
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
        Invoke-Python @(".\Tools\ai\build_ai_context_pack.py", "--repo-root", ".", "--profile", "core_ai_backend", "--basename", $ContextPackBase, "--evidence-basename", "${ContextPackBase}_evidence", "--max-total-chars", "64000", "--max-file-chars", "4000")
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
    if (Test-Path -LiteralPath $WorkloadQualityReport -PathType Leaf) {
        $ReportFiles += $WorkloadQualityReport
        $PhaseReports.workload_quality = $WorkloadQualityReport
        $WorkloadQualityRoutingOk = $true
    }
}
if ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality -and -not (Test-Path -LiteralPath $WorkloadQualityReport -PathType Leaf)) {
    if ($DryRun) {
        Write-Host "[DRY-RUN] Primary provider requires workload quality routing report; generation planned: output/validation/ai_workload_report_quality.json"
        $WorkloadQualityRoutingOk = $true
    } else {
        throw "Primary advisory provider requested but workload quality routing report is missing: output/validation/ai_workload_report_quality.json"
    }
}


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
        MinRecommendations = $MinRecommendations
        MinPatchPlans = $MinPatchPlans
        RepositoryConsistencyMapWorkers = $RepositoryConsistencyMapWorkers
    }
    if ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality) { $LegacyArgs.RunGpuNpuProvider = $true }
    if ($StrictRealRunActivationEnabled) { $LegacyArgs.RequireProviderArtifacts = $true }
    if ($NoMemoryWrite) { $LegacyArgs.SkipMemoryReload = $true }
    if ($NoEvidence) { $LegacyArgs.SkipSharedToolboxBundle = $true }
    $PhaseStatus.legacy_full_toolbox_integrated = Invoke-Checked "Run legacy full-toolbox integrated 0-to-10 lane" {
        & .\Tools\workflow\run_agent_review_full_toolbox_decision_loop_integrated.ps1 @LegacyArgs
    } -SoftFail:$ContinueOnValidationError
    if (Test-Path -LiteralPath $LegacyFullToolboxReport -PathType Leaf) {
        $ReportFiles += $LegacyFullToolboxReport
        $PhaseReports.legacy_full_toolbox_integrated = $LegacyFullToolboxReport
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
        $PhaseReports += $Gpu0Json
        $PhaseReports += $Gpu0Md
    }
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
            $PhaseReports += $OfficialPhase.json
            $PhaseReports += $OfficialPhase.markdown
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

if (Test-ModeEnabled "full_validation") {
    $PhaseStatus.git_diff_check_final = Invoke-Checked "Final git diff --check" { git diff --check } -SoftFail:$ContinueOnValidationError
    $PhaseStatus.git_status_final = Invoke-Checked "Final git status --short" { git status --short } -SoftFail:$ContinueOnValidationError
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

Write-Host ""
Write-Host "[OK] Unified local-AI launcher complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $ManifestPath"
Write-Host "[OK] Mode: $($ResolvedModes -join ',')"
Write-Host "[OK] Provider execution requested: $($Manifest.provider_execution_requested)"
Write-Host "[OK] Reset apply requested: $($Manifest.reset_apply_requested)"
Write-Host "[OK] Patch specs requested: $($Manifest.patch_specs_requested)"
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
