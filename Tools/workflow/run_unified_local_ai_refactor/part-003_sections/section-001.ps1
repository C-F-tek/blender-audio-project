# This file is dot-sourced by run_unified_local_ai_refactor.ps1.
# Source lines: 1163-1676.


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
    Invoke-Python @("-m", "py_compile", ".\Tools\validation\build_markdown_inventory\cli.py", ".\Tools\validation\build_script_inventory\cli.py", ".\Tools\validation\check_validation_report_contract\cli.py")
}

if (Test-ModeEnabled "smoke") {
    $PhaseStatus.git_diff_check_initial = Invoke-Checked "Initial git diff --check" { git diff --check } -SoftFail:$ContinueOnValidationError
    if (Test-Path .\Tools\workflow\startup_check_core\cli.py) {
        $StartupCheck = "$ValidationDir/startup_check_${ModeName}_$Stamp.json"
        $PhaseStatus.startup_check = Invoke-Checked "Startup smoke check" {
            Invoke-Python @("-m", "Tools.workflow", "startup_check", "--repo-root", ".", "--output", $StartupCheck)
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
    if (Test-Path .\Tools\workflow\_powershell\run_local_validation_after_refactor.ps1) {
        $ValidationArgs = @("-m", "Tools.workflow", "run_local_validation_after_refactor", "-SkipPull", "-MatrixWorkers", "$MatrixWorkers", "-RepeatCases", "$RepeatCases")
        if ($ContinueOnValidationError) { $ValidationArgs += "-ContinueOnError" }
        $PhaseStatus.local_validation_after_refactor = Invoke-Checked "Run local validation after refactor" { Invoke-Python $ValidationArgs } -SoftFail:$ContinueOnValidationError
    }
}

if (Test-ModeEnabled "md") {
    $MarkdownJson = "$ValidationDir/markdown_inventory_${ModeName}_$Stamp.json"
    $MarkdownMd = "$ValidationDir/markdown_inventory_${ModeName}_$Stamp.md"
    $DocsLinks = "$ValidationDir/docs_links_${ModeName}_$Stamp.json"
    $PhaseStatus.markdown_inventory = Invoke-Checked "Build Markdown inventory" {
        Invoke-Python @("-m", "Tools.validation", "build_markdown_inventory", "--repo-root", ".", "--output", $MarkdownJson, "--markdown-output", $MarkdownMd)
    }
    $PhaseStatus.docs_links = Invoke-Checked "Check docs links" {
        Invoke-Python @("-m", "Tools.validation", "check_docs_links", "--repo-root", ".", "--output", $DocsLinks)
    } -SoftFail:$ContinueOnValidationError
    $ReportFiles += @($MarkdownJson, $DocsLinks)
    $ContextFiles = Add-ExistingContextFile $ContextFiles $MarkdownMd
    $PhaseReports.markdown_inventory = $MarkdownJson
    $PhaseReports.docs_links = $DocsLinks
}

if (Test-ModeEnabled "json") {
    $JsonContract = "$ValidationDir/validation_report_contract_json_${ModeName}_$Stamp.json"
    $JsonContractArgs = @("-m", "Tools.validation", "check_validation_report_contract", "--repo-root", ".", "--output", $JsonContract)
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
        Invoke-Python @("-m", "Tools.validation", "build_script_inventory", "--repo-root", ".", "--output", $ScriptJson, "--csv-output", $ScriptCsv, "--markdown-output", $ScriptMd)
    }
    $ReportFiles += $ScriptJson
    $ContextFiles = Add-ExistingContextFile $ContextFiles $ScriptMd
    $PhaseReports.script_inventory = $ScriptJson
    $PhaseReports.script_inventory_csv = $ScriptCsv
}

if (Test-ModeEnabled "chunks") {
    $PhaseStatus.semantic_chunks = Invoke-Checked "Build semantic code chunks" {
        Invoke-Python @("-m", "Tools.npu", "build_semantic_code_chunks", "--repo-root", ".")
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "indexAI/code_chunks/semantic_code_chunks_manifest.json"
}

if (Test-ModeEnabled "context_pack") {
    $ContextPackBase = "unified_${ModeName}_context_pack_$Stamp"
    $PhaseStatus.context_pack = Invoke-Checked "Build AI context pack" {
        Invoke-Python @("-m", "Tools.ai", "build_ai_context_pack", "--repo-root", ".", "--profile", "core_ai_backend", "--basename", $ContextPackBase, "--evidence-dir", $ValidationDir, "--evidence-basename", "${ContextPackBase}_evidence", "--max-total-chars", "$ContextPackMaxTotalChars", "--max-file-chars", "$ContextPackMaxFileChars")
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "output/ai_context_packs/$ContextPackBase.md"
    $ContextFiles = Add-ExistingContextFile $ContextFiles "output/ai_context_packs/$ContextPackBase.json"
}

if (Test-ModeEnabled "agent_state") {
    $AgentStateDir = "$PipelineDir/agent_state"
    New-Item -ItemType Directory -Force -Path $AgentStateDir | Out-Null
    $AgentStateBase = "unified_${ModeName}_agent_state_$Stamp"
    $AgentArgs = @(
        "-m", "Tools.ai", "build_agent_state_packet",
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
    $ContractArgs = @("-m", "Tools.validation", "check_validation_report_contract", "--repo-root", ".", "--output", $FinalContract)
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
$LocalProviderProbeReport = Join-Path $OutputDir ("validation/local_provider_probe_{0}.json" -f $DataStamp)

if (($BuildWorkloadQualityReport -or ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality) -or $RunOllamaProbe -or $RunNpuProbe) -and -not $NoWorkloadQuality) {
    $NeedProviderWorkloadInputs = (-not (Test-Path -LiteralPath $CanonicalOllamaWorkloadReport -PathType Leaf)) -or (-not (Test-Path -LiteralPath $CanonicalNpuWorkloadReport -PathType Leaf))

    if ($NeedProviderWorkloadInputs -and ($RunOllamaProbe -or $RunNpuProbe)) {
        $ProbeArgs = @(
            "-m", "Tools.ai", "run_local_provider_probe",
            "--repo-root", ".",
            "--output", $LocalProviderProbeReport
        )

        if ($RunOllamaProbe) { $ProbeArgs += "--run-ollama" }
        if ($RunNpuProbe) { $ProbeArgs += "--run-npu" }
        if (-not [string]::IsNullOrWhiteSpace($Model)) { $ProbeArgs += @("--model", $Model) }

        # IA-CARMINE-PROVIDER-PROBE-NO-FALLBACK-BEGIN
        $ProviderProbeSoftFail = -not ($UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow)
        if (-not $ProviderProbeSoftFail) {
            Write-Host "[INFO] Provider probe hard gate enabled: no provider fallback for real-product advisory run."
        }
        $PhaseStatus.provider_workload_probe = Invoke-Checked "Generate provider workload probe inputs" {
            Invoke-Python $ProbeArgs
        } -SoftFail:$ProviderProbeSoftFail
        # IA-CARMINE-PROVIDER-PROBE-NO-FALLBACK-END

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

# IA-CARMINE-OLLAMA-WORKLOAD-NO-FALLBACK-BEGIN
if (($UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow) -and $RunOllamaProbe -and -not (Test-Path -LiteralPath $CanonicalOllamaWorkloadReport -PathType Leaf)) {
    throw "Provider/Ollama advisory path requested but no canonical Ollama workload report was produced. No fallback to metadata-only proposals is allowed."
}
# IA-CARMINE-OLLAMA-WORKLOAD-NO-FALLBACK-END

# IA-CARMINE-REAL-PRODUCT-LIVE-PROVIDER-GATE-BEGIN
if (($UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow) -and ($RunOllamaProbe -or $RunNpuProbe)) {
    $LiveProviderGateJson = Join-Path $OutputDir ("validation/real_product_live_provider_gate_{0}.json" -f $DataStamp)
    $LiveProviderGateMd = Join-Path $OutputDir ("validation/real_product_live_provider_gate_{0}.md" -f $DataStamp)
    $LiveProviderGateArgs = @(
        "-m", "Tools.validation", "check_real_product_live_provider_gate",
        "--repo-root", ".",
        "--provider-probe", $LocalProviderProbeReport,
        "--output", $LiveProviderGateJson,
        "--markdown-output", $LiveProviderGateMd
    )
    if ($RunOllamaProbe) { $LiveProviderGateArgs += "--require-ollama" }
    if ($RunNpuProbe) { $LiveProviderGateArgs += "--require-npu" }
    if (-not [string]::IsNullOrWhiteSpace($Model)) { $LiveProviderGateArgs += @("--model", $Model) }

    $PhaseStatus.real_product_live_provider_gate = Invoke-Checked "Validate real-product live provider gate" {
        & $ResolvedPythonExe @LiveProviderGateArgs
    }
    $ReportFiles += $LiveProviderGateJson
    $ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $LiveProviderGateMd
    $PhaseReports.real_product_live_provider_gate = $LiveProviderGateJson
    $PhaseReports.real_product_live_provider_gate_markdown = $LiveProviderGateMd
}
# IA-CARMINE-REAL-PRODUCT-LIVE-PROVIDER-GATE-END

if ($BuildWorkloadQualityReport -or ($UsePrimaryAdvisoryProvider -and -not $NoWorkloadQuality)) {
    Assert-FileExists ".\Tools\validation\check_ai_workload_report_quality\cli.py"
    $PhaseStatus.workload_quality = Invoke-Checked "Build AI workload quality routing report" {
        Invoke-Python @("-m", "Tools.validation", "check_ai_workload_report_quality", "--repo-root", ".", "--report-dir", $AiPacketsDir, "--output", $WorkloadQualityReport)
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
    "-m", "Tools.ai", "build_heap_exchange_runtime_entry",
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
    "-m", "Tools.ai", "build_task_ingress_contract",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--task-file", $TaskFile,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--observer-dir", $HeapExchangeObserverDir,
    "--output", $TaskIngressContractJson,
    "--markdown-output", $TaskIngressContractMd
)
