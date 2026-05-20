$ManifestPath = Join-Path $PipelineDir "${Basename}_adapter_manifest.json"
$Manifest = [ordered]@{
    schema_version = 1
    kind = "local_ai_task_pipeline_adapter_manifest"
    generated_at = (Get-Date -Format o)
    repo_root = $RepoRootPath
    prompt_file = $PromptRel
    task_file = $TaskRel
    pipeline_output_dir = $PipelineRel
    profile = $Profile
    basename = $Basename
    proposal_basename = $ProposalBasename
    context_files = $ContextFiles
    context_file_count = @(As-Array $ContextFiles).Count
    full_context_golden_path_preset = [bool]$FullContextGoldenPath
    enrichment_requested = [ordered]@{
        build_enrichment_plan = [bool]$BuildEnrichmentPlan
        enrichment_plan_basename = $EnrichmentPlanBasename
        build_semantic_chunks = [bool]$BuildSemanticChunks
        select_semantic_chunks = [bool]$SelectSemanticChunks
        build_selected_chunks_evidence = [bool]$BuildSelectedChunksEvidence
        selected_chunks_evidence_basename = $SelectedChunksEvidenceBasename
        chunk_query = $ChunkQuery
        max_selected_chunks = $MaxSelectedChunks
        max_selected_chunk_chars = $MaxSelectedChunkChars
        build_context_pack = [bool]$BuildContextPack
        context_pack_profile = $ContextPackProfile
        build_agent_state_packet = [bool]$BuildAgentStatePacket
        memory_db = $MemoryDb.Replace("\", "/")
        save_inputs_to_memory_db = [bool]$SaveInputsToMemoryDb
        extra_context_file_count = @(As-Array $ExtraContextFile).Count
    }
    enrichment_outputs = $EnrichmentOutputs
    multistep_provider_workflow_requested = [bool]$RunMultistepProviderWorkflow
    multistep_basename = $MultistepBasename
    multistep_proposal_basename = $MultistepProposalBasename
    multistep_evidence_basename = $MultistepEvidenceBasename
    run_ollama_probe = [bool]$RunOllamaProbe
    run_npu_probe = [bool]$RunNpuProbe
    run_npu_decode_smoke = [bool]$RunNpuDecodeSmoke
    provider_execution_requested = [bool]($UsePrimaryAdvisoryProvider -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke)
    provider_execution_detection_report_paths = @(
        "$PipelineRel/$Basename.json",
        "$PipelineRel/$MultistepBasename.json",
        "output/validation/local_provider_probe.json",
        "output/validation/npu_decode_smoke_diagnostic.json"
    )
    patch_application_performed = $false
    provider_execution_performed_by_adapter = $false
    build_evidence_requested = [bool]$BuildEvidence
    generate_patch_specs_requested = [bool]$GeneratePatchSpecs
    outputs = [ordered]@{
        packet_json = "$PipelineRel/$Basename.json"
        packet_markdown = "$PipelineRel/$Basename.md"
        proposals_json = "$PipelineRel/$ProposalBasename.json"
        proposals_markdown = "$PipelineRel/$ProposalBasename.md"
        proposal_validation = $ProposalValidationOutput
        enrichment_plan_json = $EnrichmentOutputs.enrichment_plan_json
        enrichment_plan_markdown = $EnrichmentOutputs.enrichment_plan_markdown
        enrichment_plan_validation = $EnrichmentOutputs.enrichment_plan_validation
        selected_chunks_validation = $EnrichmentOutputs.selected_chunks_validation
        selected_chunks_evidence_json = $EnrichmentOutputs.selected_chunks_evidence_json
        selected_chunks_evidence_markdown = $EnrichmentOutputs.selected_chunks_evidence_markdown
        multistep_packet_json = "$PipelineRel/$MultistepBasename.json"
        multistep_packet_markdown = "$PipelineRel/$MultistepBasename.md"
        multistep_proposals_json = "$PipelineRel/$MultistepProposalBasename.json"
        multistep_proposals_markdown = "$PipelineRel/$MultistepProposalBasename.md"
        multistep_evidence_json = "docs/LOCAL_VALIDATION_EVIDENCE/$MultistepEvidenceBasename.json"
        patch_specs_manifest = $PatchManifest.Replace("\", "/")
        patch_specs_manifest_markdown = $PatchManifestMd.Replace("\", "/")
        evidence_json = $EvidenceJson
        evidence_markdown = $EvidenceMd
        evidence_validation = $EvidenceValidationOutput
    }
    warnings = @()
    errors = @()
}
($Manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
