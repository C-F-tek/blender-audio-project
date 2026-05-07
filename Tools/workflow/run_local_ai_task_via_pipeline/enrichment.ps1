$ContextFiles = @($PromptRel)
if ($TaskRel -ne "") { $ContextFiles += $TaskRel }

foreach ($extra in $ExtraContextFile) {
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $extra -Root $RepoRootPath
}
$ContextFiles = @(Normalize-ContextFiles $ContextFiles)

$EnrichmentOutputs = New-EnrichmentOutputs -MemoryDb $MemoryDb

if ($BuildEnrichmentPlan) {
    $EnrichmentPlanJson = "output/ai_pipeline/${EnrichmentPlanBasename}.json"
    $EnrichmentPlanMd = "output/ai_pipeline/${EnrichmentPlanBasename}.md"
    $EnrichmentPlanValidation = "output/validation/${EnrichmentPlanBasename}_contract.json"
    Invoke-CommandChecked -Label "Build local AI enrichment plan" -Block {
        python .\Tools\ai\build_local_ai_enrichment_plan.py `
            --repo-root . `
            --objective $AgentStateObjective `
            --task-file $TaskRel `
            --profile $Profile `
            --basename $EnrichmentPlanBasename `
            --output $EnrichmentPlanJson `
            --markdown-output $EnrichmentPlanMd
    }
    Invoke-CommandChecked -Label "Validate local AI enrichment plan" -Block {
        python .\Tools\validation\check_local_ai_enrichment_plan.py `
            --repo-root . `
            --plan $EnrichmentPlanJson `
            --output $EnrichmentPlanValidation
    }
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $EnrichmentPlanMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $EnrichmentPlanJson -Root $RepoRootPath
    $ContextFiles = @(Normalize-ContextFiles $ContextFiles)
    $EnrichmentOutputs.enrichment_plan_json = $EnrichmentPlanJson
    $EnrichmentOutputs.enrichment_plan_markdown = $EnrichmentPlanMd
    $EnrichmentOutputs.enrichment_plan_validation = $EnrichmentPlanValidation
}

if ($BuildSemanticChunks) {
    Invoke-CommandChecked -Label "Build semantic code chunks" -Block {
        python .\Tools\npu\build_semantic_code_chunks.py --repo-root .
    }
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue "indexAI/code_chunks/semantic_code_chunks_manifest.json" -Root $RepoRootPath
    $ContextFiles = @(Normalize-ContextFiles $ContextFiles)
    $EnrichmentOutputs.semantic_chunks_manifest = "indexAI/code_chunks/semantic_code_chunks_manifest.json"
    $EnrichmentOutputs.semantic_chunks_json = "indexAI/code_chunks/semantic_code_chunks.json"
}

if ($SelectSemanticChunks) {
    $SelectedChunksJson = "output/ai_context_packs/$SelectedChunksBasename.json"
    $SelectedChunksMd = "output/ai_context_packs/$SelectedChunksBasename.md"
    $SelectArgs = @(
        ".\Tools\ai\select_semantic_code_chunks.py",
        "--repo-root", ".",
        "--query", $ChunkQuery,
        "--output", $SelectedChunksJson,
        "--markdown-output", $SelectedChunksMd,
        "--max-chunks", "$MaxSelectedChunks",
        "--max-total-chars", "$MaxSelectedChunkChars",
        "--max-excerpt-chars", "$MaxSelectedChunkExcerptChars"
    )
    foreach ($boost in $ChunkPathBoost) {
        $SelectArgs += @("--path-boost", $boost)
    }
    Invoke-CommandChecked -Label "Select focused semantic code chunks" -Block {
        python @SelectArgs
    }
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $SelectedChunksMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $SelectedChunksJson -Root $RepoRootPath
    $ContextFiles = @(Normalize-ContextFiles $ContextFiles)
    $EnrichmentOutputs.selected_chunks_json = $SelectedChunksJson
    $EnrichmentOutputs.selected_chunks_markdown = $SelectedChunksMd

    if ($BuildSelectedChunksEvidence) {
        $SelectedChunksValidation = "output/validation/${SelectedChunksBasename}_contract.json"
        $SelectedChunksEvidenceJson = "docs/LOCAL_VALIDATION_EVIDENCE/${SelectedChunksEvidenceBasename}.json"
        $SelectedChunksEvidenceMd = "docs/LOCAL_VALIDATION_EVIDENCE/${SelectedChunksEvidenceBasename}.md"
        Invoke-CommandChecked -Label "Validate selected semantic chunks and build compact evidence" -Block {
            python .\Tools\validation\check_selected_semantic_chunks.py `
                --repo-root . `
                --bundle $SelectedChunksJson `
                --output $SelectedChunksValidation `
                --evidence-output $SelectedChunksEvidenceJson `
                --markdown-output $SelectedChunksEvidenceMd `
                --max-total-chars $MaxSelectedChunkChars
        }
        $EnrichmentOutputs.selected_chunks_validation = $SelectedChunksValidation
        $EnrichmentOutputs.selected_chunks_evidence_json = $SelectedChunksEvidenceJson
        $EnrichmentOutputs.selected_chunks_evidence_markdown = $SelectedChunksEvidenceMd
    }
}

if ($BuildContextPack) {
    Invoke-CommandChecked -Label "Build bounded AI context pack" -Block {
        python .\Tools\ai\build_ai_context_pack.py `
            --repo-root . `
            --profile $ContextPackProfile `
            --basename $ContextPackBasename `
            --evidence-basename $ContextPackEvidenceBasename `
            --max-total-chars $ContextPackMaxTotalChars `
            --max-file-chars $ContextPackMaxFileChars
    }
    $ContextPackJson = "output/ai_context_packs/$ContextPackBasename.json"
    $ContextPackMd = "output/ai_context_packs/$ContextPackBasename.md"
    $ContextPackEvidenceJson = "docs/LOCAL_VALIDATION_EVIDENCE/$ContextPackEvidenceBasename.json"
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $ContextPackMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $ContextPackJson -Root $RepoRootPath
    $ContextFiles = @(Normalize-ContextFiles $ContextFiles)
    $EnrichmentOutputs.context_pack_json = $ContextPackJson
    $EnrichmentOutputs.context_pack_markdown = $ContextPackMd
    $EnrichmentOutputs.context_pack_evidence_json = $ContextPackEvidenceJson
}

if ($BuildAgentStatePacket) {
    $ContextFiles = @(Normalize-ContextFiles $ContextFiles)
    $AgentArgs = @(
        ".\Tools\ai\build_agent_state_packet.py",
        "--repo-root", ".",
        "--objective", $AgentStateObjective,
        "--output-dir", $AgentStateRel,
        "--packet-name", $AgentStateBasename,
        "--max-memory-chars", "$AgentStateMaxMemoryChars",
        "--memory-db", $MemoryDb
    )
    if ($SaveInputsToMemoryDb) { $AgentArgs += "--save-inputs-to-memory-db" }
    $AgentArgs += @("--memory-note", "Local AI enrichment run. Preserve report-only defaults, explicit providers, NPU guardrail role and no patch apply.")
    foreach ($context in $ContextFiles) {
        $AgentArgs += @("--include-file", $context)
    }
    Invoke-CommandChecked -Label "Build agent state packet with SQLite memory" -Block {
        python @AgentArgs
    }
    $AgentStateJson = "$AgentStateRel/$AgentStateBasename.json"
    $AgentStateMd = "$AgentStateRel/$AgentStateBasename.md"
    $AgentStateManifest = "$AgentStateRel/${AgentStateBasename}_memory_manifest.json"
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $AgentStateMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $AgentStateJson -Root $RepoRootPath
    $ContextFiles = @(Normalize-ContextFiles $ContextFiles)
    $EnrichmentOutputs.agent_state_json = $AgentStateJson
    $EnrichmentOutputs.agent_state_markdown = $AgentStateMd
    $EnrichmentOutputs.agent_state_memory_manifest = $AgentStateManifest
}

$ContextFiles = @(Normalize-ContextFiles $ContextFiles)
