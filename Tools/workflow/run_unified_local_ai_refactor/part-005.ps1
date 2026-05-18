# This file is dot-sourced by run_unified_local_ai_refactor.ps1.
# Source lines: 2197-2343.

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
        "Tools/validation/check_runtime_evidence_correlation/cli.py",
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


# IA-CARMINE-RUNTIME-FLOW-MAP-BEGIN
if ($BuildRuntimeEvidenceCorrelation -or $PrepareReviewPr) {
    $RuntimeFlowDir = Join-Path $ResolvedRepoRoot $EvidenceDir
    New-Item -ItemType Directory -Force -Path $RuntimeFlowDir | Out-Null

    $RuntimeFlowJson = Join-Path $RuntimeFlowDir ("runtime_flow_{0}.json" -f $DataStamp)
    $RuntimeFlowJsonl = Join-Path $RuntimeFlowDir ("runtime_flow_{0}.jsonl" -f $DataStamp)
    $RuntimeFlowMd = Join-Path $RuntimeFlowDir ("runtime_flow_{0}.md" -f $DataStamp)
    $RuntimeFlowMmd = Join-Path $RuntimeFlowDir ("runtime_flow_{0}.mmd" -f $DataStamp)

    $RuntimeFlowReportFiles = @()
    foreach ($RuntimeFlowPattern in @(
        ("output/validation/*{0}*.json" -f $DataStamp),
        ("output/analysis/*{0}*.json" -f $DataStamp),
        ("output/ai_pipeline/*{0}*.json" -f $DataStamp),
        ("output/patch_specs/*{0}*.json" -f $DataStamp),
        ("{0}/*{1}*.json" -f $EvidenceDir, $DataStamp)
    )) {
        $RuntimeFlowReportFiles += Get-ChildItem -Path (Join-Path $ResolvedRepoRoot $RuntimeFlowPattern) -File -ErrorAction SilentlyContinue
    }

    $RuntimeFlowReportFiles = @(
        $RuntimeFlowReportFiles |
            Where-Object { $_.FullName -ne $RuntimeFlowJson } |
            Sort-Object FullName -Unique
    )

    $RuntimeFlowArgs = @(
        "Tools/ai/runtime_flow_map/cli.py",
        "--repo-root", ".",
        "--stamp", $DataStamp,
        "--entrypoint", "python -m Tools.workflow run_unified_local_ai_refactor",
        "--output", $RuntimeFlowJson,
        "--jsonl-output", $RuntimeFlowJsonl,
        "--markdown-output", $RuntimeFlowMd,
        "--mermaid-output", $RuntimeFlowMmd
    )

    foreach ($RuntimeFlowReport in $RuntimeFlowReportFiles) {
        $RuntimeFlowArgs += @("--report", (Convert-ToRepoRelativePath $ResolvedRepoRoot $RuntimeFlowReport.FullName))
    }

    Invoke-Checked "Runtime flow map evidence" { Invoke-Python $RuntimeFlowArgs }

    if (-not (Test-Path -LiteralPath $RuntimeFlowJson -PathType Leaf)) {
        throw "Runtime flow map JSON missing: $RuntimeFlowJson"
    }

    $RuntimeFlowPayload = Get-Content -LiteralPath $RuntimeFlowJson -Raw | ConvertFrom-Json
    $RuntimeFlowReportCount = [int](Get-OptionalPropertyValue -Object $RuntimeFlowPayload.summary -Name "report_count" -Default 0)
    if ($RuntimeFlowReportCount -le 0) {
        throw "Runtime flow map did not ingest any current-stamp reports. This is not a complete real-product run."
    }
}
# IA-CARMINE-RUNTIME-FLOW-MAP-END



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
