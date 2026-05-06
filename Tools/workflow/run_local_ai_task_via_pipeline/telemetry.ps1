function New-LocalAiPipelineOutputCheck {
    param(
        [string]$Name,
        [string]$PathValue,
        [string]$Kind,
        [bool]$Required = $true
    )
    $normalized = ""
    $exists = $false
    $bytes = 0
    if (-not [string]::IsNullOrWhiteSpace($PathValue)) {
        $normalized = $PathValue.Replace("\", "/")
        $full = Resolve-PlannedPath $normalized
        if (Test-Path -LiteralPath $full -PathType Leaf) {
            $exists = $true
            $bytes = (Get-Item -LiteralPath $full).Length
        }
    }
    return [ordered]@{
        name = $Name
        kind = $Kind
        path = $normalized
        required = $Required
        exists = $exists
        bytes = $bytes
    }
}

function Get-LocalAiPipelineValidationSummary {
    param(
        [string]$Name,
        [string]$PathValue
    )
    $summary = [ordered]@{
        name = $Name
        path = ($PathValue.Replace("\", "/"))
        exists = $false
        json_ok = $false
        kind = ""
        passed = $null
        error_count = 0
        warning_count = 0
    }
    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        return $summary
    }
    $full = Resolve-PlannedPath $PathValue
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        return $summary
    }
    $summary.exists = $true
    try {
        $data = Get-Content -LiteralPath $full -Raw -Encoding UTF8 | ConvertFrom-Json
        $summary.json_ok = $true
        if ($null -ne $data.kind) { $summary.kind = [string]$data.kind }
        if ($null -ne $data.passed) { $summary.passed = [bool]$data.passed }
        if ($null -ne $data.errors) { $summary.error_count = @($data.errors).Count }
        if ($null -ne $data.warnings) { $summary.warning_count = @($data.warnings).Count }
    }
    catch {
        $summary.warning_count = 1
    }
    return $summary
}

function ConvertTo-LocalAiPipelineTelemetryMarkdown {
    param([object]$Telemetry)
    $lines = @(
        "# Local AI task pipeline telemetry",
        "",
        "- Kind: ``$($Telemetry.kind)``",
        "- Basename: ``$($Telemetry.run.basename)``",
        "- Profile: ``$($Telemetry.run.profile)``",
        "- Pipeline output: ``$($Telemetry.run.pipeline_output_dir)``",
        "- Provider execution requested: ``$($Telemetry.guardrails.provider_execution_requested)``",
        "- Provider execution performed: ``$($Telemetry.guardrails.provider_execution_performed)``",
        "- Patch application performed: ``$($Telemetry.guardrails.patch_application_performed)``",
        "- Source writes performed: ``$($Telemetry.guardrails.source_writes_performed)``",
        "- Build evidence requested: ``$($Telemetry.evidence.requested)``",
        "- Output checks passed: ``$($Telemetry.output_check_summary.passed)``",
        ""
    )

    $lines += "## Output Checks"
    $lines += ""
    $lines += "| Name | Kind | Required | Exists | Bytes | Path |"
    $lines += "|---|---|---:|---:|---:|---|"
    foreach ($check in $Telemetry.output_checks) {
        $lines += "| ``$($check.name)`` | ``$($check.kind)`` | ``$($check.required)`` | ``$($check.exists)`` | ``$($check.bytes)`` | ``$($check.path)`` |"
    }

    $lines += ""
    $lines += "## Validation Summaries"
    $lines += ""
    $lines += "| Name | Exists | JSON OK | Passed | Errors | Warnings | Path |"
    $lines += "|---|---:|---:|---:|---:|---:|---|"
    foreach ($summary in $Telemetry.validation_summaries) {
        $lines += "| ``$($summary.name)`` | ``$($summary.exists)`` | ``$($summary.json_ok)`` | ``$($summary.passed)`` | ``$($summary.error_count)`` | ``$($summary.warning_count)`` | ``$($summary.path)`` |"
    }

    return ($lines -join [Environment]::NewLine) + [Environment]::NewLine
}

$TelemetryJsonPath = Resolve-PlannedPath $TelemetryJson
$TelemetryMdPath = Resolve-PlannedPath $TelemetryMd
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $TelemetryJsonPath) | Out-Null

$OutputChecks = @(
    (New-LocalAiPipelineOutputCheck -Name "adapter_manifest" -Kind "manifest" -PathValue (Get-RepoRelativePath $RepoRootPath $ManifestPath)),
    (New-LocalAiPipelineOutputCheck -Name "packet_json" -Kind "packet" -PathValue "$PipelineRel/$Basename.json"),
    (New-LocalAiPipelineOutputCheck -Name "packet_markdown" -Kind "packet" -PathValue "$PipelineRel/$Basename.md"),
    (New-LocalAiPipelineOutputCheck -Name "packet_manifest" -Kind "manifest" -PathValue "$PipelineRel/${Basename}_manifest.json"),
    (New-LocalAiPipelineOutputCheck -Name "proposals_json" -Kind "proposal" -PathValue "$PipelineRel/$ProposalBasename.json"),
    (New-LocalAiPipelineOutputCheck -Name "proposals_markdown" -Kind "proposal" -PathValue "$PipelineRel/$ProposalBasename.md"),
    (New-LocalAiPipelineOutputCheck -Name "proposal_validation" -Kind "validation" -PathValue $ProposalValidationOutput)
)

foreach ($entry in $EnrichmentOutputs.GetEnumerator()) {
    $value = [string]$entry.Value
    if ([string]::IsNullOrWhiteSpace($value) -or $entry.Key -eq "memory_db") {
        continue
    }
    $OutputChecks += New-LocalAiPipelineOutputCheck -Name "enrichment_$($entry.Key)" -Kind "enrichment" -PathValue $value -Required $false
}

if ($GeneratePatchSpecs) {
    $OutputChecks += New-LocalAiPipelineOutputCheck -Name "patch_specs_manifest" -Kind "patch-spec" -PathValue $PatchManifest
    $OutputChecks += New-LocalAiPipelineOutputCheck -Name "patch_specs_markdown" -Kind "patch-spec" -PathValue $PatchManifestMd
}

$RequiredChecks = @($OutputChecks | Where-Object { $_.required })
$MissingRequired = @($RequiredChecks | Where-Object { -not $_.exists })

$Telemetry = [ordered]@{
    schema_version = 1
    kind = "local_ai_task_pipeline_telemetry"
    generated_at = (Get-Date -Format o)
    repo_root = $RepoRootPath
    run = [ordered]@{
        basename = $Basename
        proposal_basename = $ProposalBasename
        profile = $Profile
        prompt_file = $PromptRel
        task_file = $TaskRel
        pipeline_output_dir = $PipelineRel
        full_context_golden_path_preset = [bool]$FullContextGoldenPath
        dry_run = [bool]$DryRun
    }
    scenario_flags = [ordered]@{
        build_enrichment_plan = [bool]$BuildEnrichmentPlan
        build_semantic_chunks = [bool]$BuildSemanticChunks
        select_semantic_chunks = [bool]$SelectSemanticChunks
        build_selected_chunks_evidence = [bool]$BuildSelectedChunksEvidence
        build_context_pack = [bool]$BuildContextPack
        build_agent_state_packet = [bool]$BuildAgentStatePacket
        build_evidence = [bool]$BuildEvidence
        generate_patch_specs = [bool]$GeneratePatchSpecs
        run_multistep_provider_workflow = [bool]$RunMultistepProviderWorkflow
        run_ollama_probe = [bool]$RunOllamaProbe
        run_npu_probe = [bool]$RunNpuProbe
        run_npu_decode_smoke = [bool]$RunNpuDecodeSmoke
    }
    guardrails = [ordered]@{
        provider_execution_requested = [bool]($UsePrimaryAdvisoryProvider -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke)
        provider_execution_performed = $false
        provider_execution_performed_by_adapter = $false
        patch_application_performed = $false
        source_writes_performed = $false
        blender_runtime_execution_performed = $false
        ffmpeg_runtime_execution_performed = $false
        sqlite_write_performed = [bool]$SaveInputsToMemoryDb
        persistent_memory_write_performed = [bool]$SaveInputsToMemoryDb
        writes_forbidden_output_paths = $false
    }
    evidence = [ordered]@{
        requested = [bool]$BuildEvidence
        basename = $EvidenceBasename
        evidence_json = $EvidenceJson
        evidence_markdown = $EvidenceMd
        evidence_validation = $EvidenceValidationOutput
        telemetry_included_as_report = [bool]$BuildEvidence
        telemetry_included_as_artifact = [bool]$BuildEvidence
    }
    output_check_summary = [ordered]@{
        checked_count = @($OutputChecks).Count
        required_count = @($RequiredChecks).Count
        missing_required_count = @($MissingRequired).Count
        passed = (@($MissingRequired).Count -eq 0)
    }
    output_checks = $OutputChecks
    validation_summaries = @(
        (Get-LocalAiPipelineValidationSummary -Name "proposal_validation" -PathValue $ProposalValidationOutput)
    )
    warnings = @()
    errors = @()
}

if ($MissingRequired.Count -gt 0) {
    $Telemetry["errors"] = @($MissingRequired | ForEach-Object { "missing required output: $($_.name) -> $($_.path)" })
}

($Telemetry | ConvertTo-Json -Depth 12) | Set-Content -LiteralPath $TelemetryJsonPath -Encoding UTF8
ConvertTo-LocalAiPipelineTelemetryMarkdown -Telemetry $Telemetry | Set-Content -LiteralPath $TelemetryMdPath -Encoding UTF8
