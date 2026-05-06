if ($BuildEvidence) {
    $ManifestRel = Get-RepoRelativePath $RepoRootPath $ManifestPath
    $EvidenceArgs = @(
        "-m", "Tools.ai.build_github_evidence_bundle",
        "--repo-root", ".",
        "--basename", $EvidenceBasename,
        "--no-auto-discover-selected-chunks-evidence"
    )

    foreach ($path in @(
        $ManifestRel,
        $TelemetryJson,
        "$PipelineRel/$Basename.json",
        "$PipelineRel/${Basename}_manifest.json",
        "$PipelineRel/$ProposalBasename.json",
        $ProposalValidationOutput,
        $PatchManifest,
        $EnrichmentOutputs.enrichment_plan_validation,
        $EnrichmentOutputs.selected_chunks_validation,
        $EnrichmentOutputs.agent_state_memory_manifest
    )) {
        $EvidenceArgs = Add-ExistingBundlePathArg -ArgsList $EvidenceArgs -Kind "report" -PathValue $path -Root $RepoRootPath
    }

    foreach ($path in @($ReportFiles)) {
        $EvidenceArgs = Add-ExistingBundlePathArg -ArgsList $EvidenceArgs -Kind "report" -PathValue $path -Root $RepoRootPath -WarnIfMissing $false
    }

    foreach ($path in @(
        $PromptRel,
        $TaskRel,
        $TelemetryMd,
        "$PipelineRel/$Basename.md",
        "$PipelineRel/$ProposalBasename.md",
        $PatchManifestMd,
        $EnrichmentOutputs.enrichment_plan_markdown,
        $EnrichmentOutputs.selected_chunks_markdown,
        $EnrichmentOutputs.context_pack_markdown,
        $EnrichmentOutputs.agent_state_markdown
    )) {
        $EvidenceArgs = Add-ExistingBundlePathArg -ArgsList $EvidenceArgs -Kind "artifact" -PathValue $path -Root $RepoRootPath
    }

    foreach ($path in @($EnrichmentOutputs.selected_chunks_evidence_json)) {
        $EvidenceArgs = Add-ExistingBundlePathArg -ArgsList $EvidenceArgs -Kind "selected-chunks-evidence" -PathValue $path -Root $RepoRootPath
    }

    Invoke-CommandChecked -Label "Build task-scoped compact GitHub evidence bundle" -Block {
        python @EvidenceArgs
    }
    Invoke-CommandChecked -Label "Validate task-scoped compact GitHub evidence bundle" -Block {
        python -m Tools.validation.check_github_evidence_bundle `
            --repo-root . `
            --bundle $EvidenceJson `
            --output $EvidenceValidationOutput
    }
}
