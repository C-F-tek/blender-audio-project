# Evidence Chunk 0042/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `5839`
- line_end: `5876`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0041.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0043.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Archiviazione e verifica dei risultati di un ciclo di raccomandazioni e patching automatizzato per un progetto AI.  
**Segnali principali**: 220 raccomandazioni GPU generate, 220 patch plan, tutti i file esistenti e senza errori, ma richiedono revisione manuale.  
**Guardrail / errori**: Nessun errore riportato; avvisi vuoti; `provider_execution_performed` e `patch_application_performed` sono false, indicando che l’esecuzione è stata simulata.  
**Perché serve a una AI cloud**: Fornisce un bundle

## Context before

    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1563444,
      "sha256": "5e47daa32352033f202ac54e5c6a798dac09a8689cceb30fd033108e1e72f821",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer\",\n  \"generated_at\": \"2026-05-03T19:54:03\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 220,\n  \"recommendations\": [\n    {\n      \"id\": \"consistency_001\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax",
      "preview_chars": 1500,
      "line_count": 35445

## Chunk content

```json
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 37585,
      "sha256": "d429fafb0d267182b0db2cbe4c2ba6364219d2fc7a82d14d53bfe752926112e7",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n  \"generated_at\": \"2026-05-03T19:54:03\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"gpu_output\": \"output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json\",\n  \"gpu_recommendation_count\": 220,\n  \"gpu_empty_recommendations_reason\": \"\",\n  \"gpu_recommended_next_layer\": \"build_agent_review_patch_plan.py\",\n  \"npu_audits\": [\n    {\n      \"round\": 1,\n      \"checkpoint\": \"output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_001.json\",\n      \"audit_output\": \"output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_001_npu_async_audit.json\",\n      \"started_at\": \"2026-05-03T19:10:46\",\n      \"status\": \"finished\",\n      \"command\": [\n        \"C:\\\\Python314\\\\python.exe\",\n        \"Tools/ai/run_npu_gpu_deep_review_auditor.py\",\n        \"--repo-root\",\n        \".\",\n        \"--gpu-review\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_001.json\",\n        \"--output\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_001_npu_async_audit.json\",\n        \"--markdown-output\",\n        \"C:\\\\Users\\\\car",
      "preview_chars": 1500,
      "line_count": 556
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_agent_review_decision_loop_recovered_220.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2734,
      "sha256": "8104c45a3dc4b98293ace5d847297c838fe15e5570380a1340db16906efc562c",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_decision_loop\",\n  \"generated_at\": \"2026-05-03T19:54:03\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 220,\n  \"patch_plan_count\": 220,\n  \"deterministic_synthesizer_used\": true,\n  \"patch_plan_fallback_used\": false,\n  \"next_best_action\": \"manual_review_patch_plan\",\n  \"outputs\": {\n    \"recommendations\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json\",\n      \"exists\": true,\n      \"size_bytes\": 1563444\n    },\n    \"recommendations_markdown\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.md\",\n      \"exists\": true,\n      \"size_bytes\": 213245\n    },\n    \"bridge_orchestrator\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json\",\n      \"exists\": true,\n      \"size_bytes\": 37585\n    },\n    \"patch_plan\": {\n      \"path\": \"output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.json\",\n      \"exists\": true,\n      \"size_bytes\": 3342261\n    },\n    \"patch_plan_markdown\": {\n      \"path\": \"output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md\",\n      \"exists\": ",
      "preview_chars": 1500,
      "line_count": 74
    },
    {
      "path": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 3342261,
      "sha256": "8b5c9c7341fe5070a26ec252e4b5de092b18a5b6b640f068de359d9c5c6339c4",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_patch_plan\",\n  \"generated_at\": \"2026-05-03T19:54:03\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_manual_review_patch_plan\",\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json\",\n    \"evidence\": \"output/ai_pipeline/agent_review_evidence_sufficiency.json\",\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json\",\n    \"orchestrator_kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n    \"evidence_kind\": \"agent_review_evidence_sufficiency\",\n    \"gpu_kind\": \"deterministic_recommendation_synthesizer\"\n  },\n  \"decision\": {\n    \"ready_for_manual_review\": true,\n    \"patch_plan_count\": 220,\n    \"skipped_candidate_count\": 0,\n    \"gpu_recommendation_count\": 220,\n    \"gpu_ready_count\": 0,\n    \"fallback_used\": false,\n    \"evidence_ready_for_manual_patch_count\": 12,\n    \"evidence_sufficient_for_real_pr\": true,\n    \"recommended_next_layer\": \"manual_review_then_targeted_patch\",\n    \"manual_review_required\": true,\n    \"cosmetic_patch_suppression_enabled\": true\n  },\n  \"patch_plan_count\": 220,\n  \"available_patch_plan_count\": 220,\n  \"max_patch_plans\": 0,\n  \"patch_plans\": [\n    {\n      \"",
      "preview_chars": 1500,
      "line_count": 68033
    }
  ],
```

## Context after

  "included_artifacts": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 213245,
      "sha256": "224474a615b5dde74727028341451ed70c6e7a6891a136d9940a1bf6e6765fdd",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": true,
      "line_count": 2063,
