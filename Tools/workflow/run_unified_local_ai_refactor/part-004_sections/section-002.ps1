
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
            & $ResolvedPythonExe -m Tools.ai build_review_pr_prepare_args `
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
            & $ResolvedPythonExe -m Tools.validation check_review_pr_product_readiness `
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
    ai_peer_exchange_required = [bool]$StrictRealRunActivationEnabled
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
    agent_review_prepare_pr = [bool]$PrepareReviewPr
    review_pr_apply_deterministic_suggestions = [bool]$ReviewPrApplyDeterministicSuggestions
    heap_peer_runtime = $HeapPeerRuntimeJson
    shared_memory_evidence = $HeapPeerRuntimeJson
    closure_audit_report = $HeapExchangeClosureAuditJson
}
($UnifiedChainArgsContext | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $UnifiedChainArgsContextJson -Encoding UTF8

$UnifiedChainArgsBuilderOk = Invoke-Checked "Build final unified chain contract args" {
    & $ResolvedPythonExe -m Tools.ai build_unified_chain_contract_args `
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
