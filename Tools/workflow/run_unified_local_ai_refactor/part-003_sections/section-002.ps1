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
        "-m", "ia_carmine.cli", "heap_exchange_runtime_entry",
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
    "-m", "ia_carmine.cli", "heap_exchange_peer_runtime_manifest",
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
    "-m", "ia_carmine.cli", "heap_exchange_closure_audit",
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
if ($RunOpenVinoGpu0Workload) {
    $Gpu0ProviderSupportJson = Join-Path $OutputDir ("validation/openvino_gpu0_provider_support_{0}.json" -f $DataStamp)
    $Gpu0ProviderSupportMd = Join-Path $OutputDir ("validation/openvino_gpu0_provider_support_{0}.md" -f $DataStamp)
    $Gpu0SupportOk = Invoke-Checked "Run OpenVINO GPU.0 provider support lane" {
        & $ResolvedPythonExe -m ia_carmine build_openvino_gpu0_workload_report `
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
        Invoke-Python (@("-m", "Tools.workflow", "run_agent_review_full_toolbox_decision_loop_integrated") + $LegacyArgs)
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

    }
}


# IA-CARMINE-GPU0-WORKLOAD-BEFORE-OFFICIAL-BEGIN
if ($RunOpenVinoGpu0Workload) {
    Write-Host ""
    Write-Host "=== Run OpenVINO GPU.0 secondary workload evidence ==="
    $Gpu0Stamp = $Stamp
    if ([string]::IsNullOrWhiteSpace($Gpu0Stamp)) { $Gpu0Stamp = Get-Date -Format "yyyyMMdd-HHmmss" }

    $Gpu0Json = Join-Path $OutputDir ("validation/openvino_gpu0_workload_{0}.json" -f $Gpu0Stamp)
    $Gpu0Md = Join-Path $OutputDir ("validation/openvino_gpu0_workload_{0}.md" -f $Gpu0Stamp)
    Invoke-Python @(
        "-m", "ia_carmine.cli", "build_openvino_gpu0_workload_report",
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

}
