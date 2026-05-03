# Evidence Chunk 0027/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `2420`
- line_end: `2616`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0026.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0028.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Definire la struttura di suddivisione di un file JSON di grandi dimensioni in blocchi di 200 righe per l’elaborazione distribuita.  
**Segnali principali**: `chunk_size_lines`, `chunk_count`, ID del primo e ultimo blocco, e un array di `chunk_pointers` con ID, percorso, intervallo di righe, riferimenti

## Context before

      "exists": true,
      "suffix": ".json",
      "size_bytes": 370564,
      "sha256": "3ded3a5338a007113d8cbdc04ef23ecd8dc138e67d66fe2ce70b619831279d36",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": true,
      "line_count": 7936,
      "raw_chars": 362628,
      "included_chars": 16000,
      "content": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 40,\n  \"recommendations\": [\n    {\n      \"id\": \"consistency_001\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json\",\n        \"python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json\",\n        \"git diff --check\",\n        \"git status --short\"\n      ],\n      \"stop_conditions\": [\n        \"Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.\",\n        \"Stop if the target/source evidence no longer exists after refreshing master.\",\n        \"Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.\",\n        \"Stop if resolving the finding requires inventing behavior not supported by code evidence.\"\n      ],\n      \"source\": \"repository_consistency_map\",\n      \"evidence\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163\"\n      ],\n      \"tool_evidence\": [\n        {\n          \"path\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json\",\n          \"kind\": \"repository_consistency_map\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/repository_consistency_map_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"repository_consistency_map_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/code_interpreter_full_toolbox_20260503-223900.json\",\n          \"kind\": \"code_interpreter_report\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_line_count_full_toolbox_20260503-223900.json\",\n          \"kind\": \"python_line_count_csv\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_syntax_full_toolbox_20260503-223900.json\",\n          \"kind\": \"python_syntax\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"gpu_planner_json_contract_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"deterministic_recommendation_synthesizer_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"agent_review_decision_loop_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/npu_provider_environment_full_toolbox_20260503-223900.json\",\n          \"kind\": \"npu_provider_environment\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_json_contract_replay_full_toolbox_20260503-223900.json\",\n          \"kind\": \"gpu_planner_json_contract_replay\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_npu_run_sync_full_toolbox_20260503-223900.json\",\n          \"kind\": \"gpu_npu_run_sync_analysis\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/full_memory_tool_regeneration_20260503-223900_workflow.json\",\n          \"kind\": \"full_memory_tool_regeneration_workflow\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        }\n      ],\n      \"npu_audit_refs\": [\n        {\n          \"round\": 1,\n          \"status\": \"finished\",\n          \"classification\": \"usable_audit_text\",\n          \"runtime_tool_context_seen\": false,\n          \"npu_tool_request_count\": 0,\n          \"npu_runtime_tool_execution_count\": null,\n          \"npu_runtime_tool_failed_count\": null,\n          \"npu_runtime_tool_blocked_count\": null\n        },\n        {\n          \"round\": 6,\n          \"status\": \"finished\",\n          \"classification\": \"usable_audit_text\",\n          \"runtime_tool_context_seen\": false,\n          \"npu_tool_request_count\": 0,\n          \"npu_runtime_tool_execution_count\": null,\n          \"npu_runtime_tool_failed_count\": null,\n          \"npu_runtime_tool_blocked_count\": null\n        }\n      ],\n      \"repository_consistency_finding\": {\n        \"kind\": \"md_python_command_script_missing\",\n        \"severity\": \"high\",\n        \"source\": \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\",\n        \"line\": 163,\n        \"target\": \"Tools/validation/check_markdown_command_hygiene.py\",\n        \"flag\": \"\",\n        \"evidence\": \"\"\n      },\n      \"guardrails\": {\n        \"patch_application_performed\": false,\n        \"manual_review_required\": true,\n        \"cosmetic_patch_allowed\": false\n      }\n    },\n    {\n      \"id\": \"consistency_002\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json\",\n        \"python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json\",\n        \"git diff --check\",\n        \"git status --short\"\n      ],\n      \"stop_conditions\": [\n        \"Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.\",\n        \"Stop if the target/source evidence no longer exists after refreshing master.\",\n        \"Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.\",\n        \"Stop if resolving the finding requires inventing behavior not supported by code evidence.\"\n      ],\n      \"source\": \"repository_consistency_map\",\n      \"evidence\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368\"\n      ],\n      \"tool_evidence\": [\n        {\n          \"path\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json\",\n          \"kind\": \"repository_consistency_map\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/repository_consistency_map_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"repository_consistency_map_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/code_interpreter_full_toolbox_20260503-223900.json\",\n          \"kind\": \"code_interpreter_report\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_line_count_full_toolbox_20260503-223900.json\",\n          \"kind\": \"python_line_count_csv\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_syntax_full_toolbox_20260503-223900.json\",\n          \"kind\": \"python_syntax\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"gpu_planner_json_contract_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"deterministic_recommendation_synthesizer_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-223900.json\",\n          \"kind\": \"agent_review_decision_loop_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/npu_provider_environment_full_toolbox_20260503-223900.json\",\n          \"kind\": \"npu_provider_environment\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_json_contract_replay_full_toolbox_20260503-223900.json\",\n          \"kind\": \"gpu_planner_json_contract_replay\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_npu_run_sync_full_toolbox_20260503-223900.json\",\n          \"kind\": \"gpu_npu_run_sync_analysis\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/full_memory_tool_regeneration_20260503-223900_workflow.json\",\n          \"kind\": \"full_memory_tool_regeneration_workflow\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_exe",

## Chunk content

```json
      "chunk_size_lines": 200,
      "chunk_count": 40,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L7801-L7936",
      "chunk_pointers": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L201-L400",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1-L200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L401-L600",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L201-L400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L601-L800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L601-L800",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L401-L600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L801-L1000",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 801,
          "line_end": 1000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L601-L800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1001-L1200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1001-L1200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 1001,
          "line_end": 1200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L801-L1000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1201-L1400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1201-L1400",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 1201,
          "line_end": 1400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1001-L1200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1401-L1600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1401-L1600",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 1401,
          "line_end": 1600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1201-L1400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1601-L1800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1601-L1800",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 1601,
          "line_end": 1800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1401-L1600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1801-L2000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1801-L2000",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 1801,
          "line_end": 2000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1601-L1800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2001-L2200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2001-L2200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 2001,
          "line_end": 2200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L1801-L2000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2201-L2400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2201-L2400",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 2201,
          "line_end": 2400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2001-L2200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2401-L2600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2401-L2600",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 2401,
          "line_end": 2600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2201-L2400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2601-L2800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2601-L2800",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 2601,
          "line_end": 2800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2401-L2600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2801-L3000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2801-L3000",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 2801,
          "line_end": 3000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2601-L2800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3001-L3200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3001-L3200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 3001,
          "line_end": 3200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L2801-L3000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3201-L3400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3201-L3400",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 3201,
          "line_end": 3400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3001-L3200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3401-L3600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3401-L3600",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 3401,
          "line_end": 3600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3201-L3400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3601-L3800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3601-L3800",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 3601,
          "line_end": 3800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3401-L3600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3801-L4000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3801-L4000",
```

## Context after

          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 3801,
          "line_end": 4000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L3601-L3800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L4001-L4200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json#L4001-L4200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
          "line_start": 4001,
