# Evidence Chunk 0022/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `1894`
- line_end: `2096`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0021.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0023.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: included_artifacts. Preview: "chunk_size_lines": 200, "chunk_count": 19, "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1-L200", "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L36...

## Context before

      "exists": true,
      "suffix": ".json",
      "size_bytes": 173927,
      "sha256": "d7ee8744f7bccfd214b41c06c043668fc320019a33afcb3c4e9b61692c2ae769",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": true,
      "line_count": 3796,
      "raw_chars": 170131,
      "included_chars": 16000,
      "content": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 20,\n  \"recommendations\": [\n    {\n      \"id\": \"consistency_001\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json\",\n        \"python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json\",\n        \"git diff --check\",\n        \"git status --short\"\n      ],\n      \"stop_conditions\": [\n        \"Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.\",\n        \"Stop if the target/source evidence no longer exists after refreshing master.\",\n        \"Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.\",\n        \"Stop if resolving the finding requires inventing behavior not supported by code evidence.\"\n      ],\n      \"source\": \"repository_consistency_map\",\n      \"evidence\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163\"\n      ],\n      \"tool_evidence\": [\n        {\n          \"path\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json\",\n          \"kind\": \"repository_consistency_map\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/repository_consistency_map_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"repository_consistency_map_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/code_interpreter_full_toolbox_20260503-231855.json\",\n          \"kind\": \"code_interpreter_report\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_line_count_full_toolbox_20260503-231855.json\",\n          \"kind\": \"python_line_count_csv\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_syntax_full_toolbox_20260503-231855.json\",\n          \"kind\": \"python_syntax\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"gpu_planner_json_contract_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"deterministic_recommendation_synthesizer_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"agent_review_decision_loop_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/npu_provider_environment_full_toolbox_20260503-231855.json\",\n          \"kind\": \"npu_provider_environment\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.json\",\n          \"kind\": \"gpu_planner_json_contract_replay\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json\",\n          \"kind\": \"gpu_npu_run_sync_analysis\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/full_memory_tool_regeneration_20260503-231855_workflow.json\",\n          \"kind\": \"full_memory_tool_regeneration_workflow\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        }\n      ],\n      \"npu_audit_refs\": [\n        {\n          \"round\": 1,\n          \"status\": \"finished\",\n          \"classification\": \"usable_audit_text\",\n          \"runtime_tool_context_seen\": false,\n          \"npu_tool_request_count\": 0,\n          \"npu_runtime_tool_execution_count\": null,\n          \"npu_runtime_tool_failed_count\": null,\n          \"npu_runtime_tool_blocked_count\": null\n        }\n      ],\n      \"repository_consistency_finding\": {\n        \"kind\": \"md_python_command_script_missing\",\n        \"severity\": \"high\",\n        \"source\": \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\",\n        \"line\": 163,\n        \"target\": \"Tools/validation/check_markdown_command_hygiene.py\",\n        \"flag\": \"\",\n        \"evidence\": \"\"\n      },\n      \"guardrails\": {\n        \"patch_application_performed\": false,\n        \"manual_review_required\": true,\n        \"cosmetic_patch_allowed\": false\n      }\n    },\n    {\n      \"id\": \"consistency_002\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json\",\n        \"python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json\",\n        \"git diff --check\",\n        \"git status --short\"\n      ],\n      \"stop_conditions\": [\n        \"Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.\",\n        \"Stop if the target/source evidence no longer exists after refreshing master.\",\n        \"Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.\",\n        \"Stop if resolving the finding requires inventing behavior not supported by code evidence.\"\n      ],\n      \"source\": \"repository_consistency_map\",\n      \"evidence\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368\"\n      ],\n      \"tool_evidence\": [\n        {\n          \"path\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json\",\n          \"kind\": \"repository_consistency_map\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/repository_consistency_map_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"repository_consistency_map_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/code_interpreter_full_toolbox_20260503-231855.json\",\n          \"kind\": \"code_interpreter_report\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_line_count_full_toolbox_20260503-231855.json\",\n          \"kind\": \"python_line_count_csv\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_syntax_full_toolbox_20260503-231855.json\",\n          \"kind\": \"python_syntax\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"gpu_planner_json_contract_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"deterministic_recommendation_synthesizer_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-231855.json\",\n          \"kind\": \"agent_review_decision_loop_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/npu_provider_environment_full_toolbox_20260503-231855.json\",\n          \"kind\": \"npu_provider_environment\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.json\",\n          \"kind\": \"gpu_planner_json_contract_replay\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json\",\n          \"kind\": \"gpu_npu_run_sync_analysis\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/full_memory_tool_regeneration_20260503-231855_workflow.json\",\n          \"kind\": \"full_memory_tool_regeneration_workflow\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        }\n      ],\n      \"npu_audit_refs\": [\n        {\n          \"round\": 1,\n          \"status\": \"finished\",\n          \"classification\": \"usable_audit_text\",\n         ",

## Chunk content

```json
      "chunk_size_lines": 200,
      "chunk_count": 19,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3601-L3796",
      "chunk_pointers": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L201-L400",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1-L200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L401-L600",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L201-L400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L601-L800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L601-L800",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L401-L600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L801-L1000",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 801,
          "line_end": 1000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L601-L800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1001-L1200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1001-L1200",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 1001,
          "line_end": 1200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L801-L1000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1201-L1400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1201-L1400",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 1201,
          "line_end": 1400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1001-L1200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1401-L1600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1401-L1600",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 1401,
          "line_end": 1600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1201-L1400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1601-L1800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1601-L1800",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 1601,
          "line_end": 1800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1401-L1600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1801-L2000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1801-L2000",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 1801,
          "line_end": 2000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1601-L1800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2001-L2200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2001-L2200",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 2001,
          "line_end": 2200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L1801-L2000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2201-L2400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2201-L2400",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 2201,
          "line_end": 2400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2001-L2200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2401-L2600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2401-L2600",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 2401,
          "line_end": 2600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2201-L2400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2601-L2800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2601-L2800",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 2601,
          "line_end": 2800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2401-L2600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2801-L3000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2801-L3000",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 2801,
          "line_end": 3000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2601-L2800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3001-L3200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3001-L3200",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 3001,
          "line_end": 3200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L2801-L3000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3201-L3400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3201-L3400",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 3201,
          "line_end": 3400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3001-L3200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3401-L3600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3401-L3600",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 3401,
          "line_end": 3600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3201-L3400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3601-L3796",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3601-L3796",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
          "line_start": 3601,
          "line_end": 3796,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json#L3401-L3600",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 19814,
      "sha256": "c8106161ae149539300413af4c741d4ea73950af0fa9a72588d982fe5ff4ff22",
```

## Context after

      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": false,
      "line_count": 175,
      "raw_chars": 19599,
      "included_chars": 16000,
      "content": "# Deterministic Recommendation Synthesizer\n\n- Passed: `True`\n- Recommendation count: `20`\n- Deterministic synthesizer used: `True`\n- GPU empty recommendations reason: `model_output_schema_mismatch`\n- Evidence ready for manual patch count: `12`\n- Next best action: `build_agent_review_patch_plan.py`\n- Patch application performed: `False`\n\n## Recommendations\n\n### consistency_001 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_002 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_003 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_004 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_005 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_006 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_007 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `Tools/init_db.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_008 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `app.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_009 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_010 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_011 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_012 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_013 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_014 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_015 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_016 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235` targeting `Tools/validation/check_markdown_command_hygiene.py`.\n- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\n\n### consistency_017 — md_python\n- Source: `repository_consistency_map`\n- Status: `ready_for_patch_plan`\n- Risk: `medium`\n- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`\n- Rationale: Repository consistency mapper reported high `md_python_"
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
      "exists": true,
