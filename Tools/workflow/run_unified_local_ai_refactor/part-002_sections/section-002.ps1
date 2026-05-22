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
    "Tools/validation/docs_hygiene/markdown_inventory/cli.py",
    "Tools/validation/docs_hygiene/build_script_inventory/cli.py",
    "Tools/validation/docs_hygiene/check_docs_links/cli.py",
    "Tools/validation/pipeline/check_validation_report_contract/cli.py",
    "Tools/workflow/_powershell/run_local_ai_task_via_pipeline.ps1",
    "Tools/workflow/_powershell/run_post_validation_ai_packet.ps1",
    $TaskFile
)
foreach ($Path in $Required) { Assert-FileExists $Path }

$Warnings = @()
Add-OptionalModeWarning "validation" ".\Tools\workflow\_powershell\run_local_validation_after_refactor.ps1" ([ref]$Warnings)
Add-OptionalModeWarning "smoke" ".\Tools\workflow\workflow_run\startup_check_core\cli.py" ([ref]$Warnings)
Add-OptionalModeWarning "chunks" ".\Tools\npu\provider_mesh\semantic_code_chunks\cli.py" ([ref]$Warnings)
Add-OptionalModeWarning "context_pack" ".\ia_carmine\context\agent_context\ai_context_pack\cli.py" ([ref]$Warnings)
Add-OptionalModeWarning "agent_state" ".\ia_carmine\context\agent_context\state_packet\cli.py" ([ref]$Warnings)

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
