# This file is dot-sourced by run_unified_local_ai_refactor.ps1.
# Source lines: 1677-2196.

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
    $OfficialAdapterScript = Join-Path $OfficialRepoRoot "Tools/workflow/_powershell/run_local_ai_task_via_pipeline.ps1"
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
        "-File", ".\Tools\workflow\_powershell\run_post_validation_ai_packet.ps1",
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
            "-m", "Tools.ai", "build_task_patch_suggestion_report",
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
        "-m", "Tools.ai", "generated_patch_specs_apply",
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
    "-m", "Tools.ai", "heap_exchange_runtime_exit",
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
        "-m", "Tools.ai", "apply_patch_suggestion_bundle",
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
        "-m", "Tools.ai", "heap_exchange_runtime_exit",
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
    "-m", "Tools.validation", "check_heap_exchange_runtime_lifecycle",
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
# - agent_review_prepare_pr.py
# - manifest write
# Running it here validates before the review PR product exists.
# IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-END

    $PatchSuggestionProductSeparationJson = "$ValidationDir/patch_suggestion_product_separation_${ModeName}_$Stamp.json"
    $PatchSuggestionProductSeparationArgs = @(
        "-m", "Tools.validation", "check_patch_suggestion_product_separation",
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
