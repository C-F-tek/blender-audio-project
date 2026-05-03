# Evidence Chunk 0014/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `1877`
- line_end: `1948`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0013.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0015.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Archiviazione e riferimenti ai risultati di analisi GPU/NPU, sintetizzatori di raccomandazioni e orchestratori di

## Context before

      "preview_chars": 1500,
      "line_count": 50
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 9487,
      "sha256": "18011b1c61c2c6471e02a43077afc5c492d6c80bebca250f736759ad6f5693d4",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_planner_json_contract_replay\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json\"\n  },\n  \"source_summary\": {\n    \"kind\": \"agent_gpu_deep_planning_supervised\",\n    \"passed\": true,\n    \"round_count\": 8,\n    \"recommendation_count\": 0,\n    \"json_parse_error_count\": 0,\n    \"repair_attempt_count\": 0,\n    \"empty_recommendations_reason\": \"context_echo_detected\",\n    \"evidence_ready_for_manual_patch_count\": 12\n  },\n  \"replayed_round_count\": 8,\n  \"contract_reason_counts\": {\n    \"json_parse_failure\": 2,\n    \"model_output_schema_mismatch\": 6\n  },\n  \"context_echo_detected_count\": 0,\n  \"json_parse_failure_count\": 2,\n  \"model_output_schema_mismatch_count\": 6,\n  \"valid_recommendation_output_count\": 0,\n  \"rounds\": [\n    {\n      \"round\": 1,\n      \"original_empty_recommendations_reason\": \"context_echo_detected\",\n      \"original_json_ok\": true,\n      \"original_parse_error\": \"\",\n      \"original_response_chars\": 4656,\n      \"contract\": {\n        \"json_ok\": false,\n        \"schema_ok\": false,\n        \"context_echo_detected\": ",

## Chunk content

```json
      "preview_chars": 1500,
      "line_count": 269
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5494,
      "sha256": "7933edd214b3248457c69b956c620ae7f04a73afdca4f88335ccbe33202474ab",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_npu_run_sync_analysis\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json\"\n  },\n  \"metrics\": {\n    \"gpu_round_count\": 8,\n    \"npu_audit_count\": 2,\n    \"npu_audit_success_count\": 2,\n    \"npu_audit_round_coverage\": 0.25,\n    \"avg_gpu_round_seconds\": 34.761,\n    \"p50_gpu_round_seconds\": 34.761,\n    \"p90_gpu_round_seconds\": 34.761,\n    \"avg_npu_audit_seconds\": 100.0,\n    \"p50_npu_audit_seconds\": 98.0,\n    \"p90_npu_audit_seconds\": 102.0,\n    \"npu_to_gpu_avg_duration_ratio\": 2.877,\n    \"gpu_elapsed_seconds\": 278.09,\n    \"provider_execution_performed\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"gpu_metrics_source\": \"gpu_elapsed_divided_by_round_count\"\n  },\n  \"performance\": {\n    \"analyzer_elapsed_seconds\": 0.001,\n    \"gpu\": {\n      \"elapsed_seconds\": 278.09,\n      \"round_count\": 8,\n      \"round_duration_source\": \"gpu_elapsed_divided_by_round_count\",\n      \"round_duration_sample_count\": 1,\n      \"avg_round_seconds\": 34.761,\n      \"p50_round_seconds\": 34.761,\n  ",
      "preview_chars": 1500,
      "line_count": 147
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 370564,
      "sha256": "3ded3a5338a007113d8cbdc04ef23ecd8dc138e67d66fe2ce70b619831279d36",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 40,\n  \"recommendations\": [\n    {\n      \"id\": \"consistency_001\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.",
      "preview_chars": 1500,
      "line_count": 7936
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_bridge_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 9304,
      "sha256": "2eb4a13386435fea871d21b0513c299363fea0f93f956e730cf9bda10b205cc1",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"gpu_output\": \"output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json\",\n  \"gpu_recommendation_count\": 40,\n  \"gpu_empty_recommendations_reason\": \"\",\n  \"gpu_recommended_next_layer\": \"build_agent_review_patch_plan.py\",\n  \"npu_audits\": [\n    {\n      \"round\": 1,\n      \"checkpoint\": \"output/ai_pipeline/full_toolbox_20260503-223900_checkpoints/round_001.json\",\n      \"audit_output\": \"output/ai_pipeline/full_toolbox_20260503-223900_checkpoints/round_001_npu_async_audit.json\",\n      \"started_at\": \"2026-05-03T22:41:36\",\n      \"status\": \"finished\",\n      \"command\": [\n        \"C:\\\\Python314\\\\python.exe\",\n        \"Tools/ai/run_npu_gpu_deep_review_auditor.py\",\n        \"--repo-root\",\n        \".\",\n        \"--gpu-review\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-223900_checkpoints\\\\round_001.json\",\n        \"--output\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-223900_checkpoints\\\\round_001_npu_async_audit.json\",\n        \"--markdown-output\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\bl",
      "preview_chars": 1500,
      "line_count": 150
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_agent_review_decision_loop.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2657,
      "sha256": "ce1beaf984e8a78c5093a9766d35621232360ffb614f5d59409771ed9736a647",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_decision_loop\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 40,\n  \"patch_plan_count\": 40,\n  \"deterministic_synthesizer_used\": true,\n  \"patch_plan_fallback_used\": false,\n  \"next_best_action\": \"manual_review_patch_plan\",\n  \"outputs\": {\n    \"recommendations\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json\",\n      \"exists\": true,\n      \"size_bytes\": 370564\n    },\n    \"recommendations_markdown\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.md\",\n      \"exists\": true,\n      \"size_bytes\": 45467\n    },\n    \"bridge_orchestrator\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-223900_bridge_orchestrator.json\",\n      \"exists\": true,\n      \"size_bytes\": 9304\n    },\n    \"patch_plan\": {\n      \"path\": \"output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.json\",\n      \"exists\": true,\n      \"size_bytes\": 561222\n    },\n    \"patch_plan_markdown\": {\n      \"path\": \"output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md\",\n      \"exists\": true,\n      \"size_bytes\": 44226\n    }\n  },\n  \"inputs\": {\n    \"evidence\": \"ou",
      "preview_chars": 1500,
      "line_count": 74
    },
    {
      "path": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 561222,
      "sha256": "11993742268448ef4dc6ac30d2949b54a6dd575ff57334a2ca41c1ac24ee288a",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_patch_plan\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_manual_review_patch_plan\",\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_20260503-223900_bridge_orchestrator.json\",\n    \"evidence\": \"output/ai_pipeline/agent_review_evidence_sufficiency.json\",\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json\",\n    \"orchestrator_kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n    \"evidence_kind\": \"agent_review_evidence_sufficiency\",\n    \"gpu_kind\": \"deterministic_recommendation_synthesizer\"\n  },\n  \"decision\": {\n    \"ready_for_manual_review\": true,\n    \"patch_plan_count\": 40,\n    \"skipped_candidate_count\": 0,\n    \"gpu_recommendation_count\": 40,\n    \"gpu_ready_count\": 0,\n    \"fallback_used\": false,\n    \"evidence_ready_for_manual_patch_count\": 12,\n    \"evidence_sufficient_for_real_pr\": true,\n    \"recommended_next_layer\": \"manual_review_then_targeted_patch\",\n    \"manual_review_required\": true,\n    \"cosmetic_patch_suppression_enabled\": true\n  },\n  \"patch_plan_count\": 40,\n  \"available_patch_plan_count\": 40,\n  \"max_patch_plans\": 0,\n  \"requested_max_patch_plans\": 0,\n  \"patch_plans\": [\n    {\n     ",
      "preview_chars": 1500,
      "line_count": 10614
    },
    {
      "path": "output/ai_pipeline/repository_change_proposals.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 7325,
      "sha256": "2c5ac9ea19a60347cabec901ee9825af87a637e51c691a4ce55e2fe8a4259089",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_change_proposals\",\n  \"generated_at\": \"2026-05-03T22:45:31\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"profile\": \"core\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"apply_mode\": \"manual_review_only\",\n  \"suggestion_contract\": {\n    \"schema_version\": 1,\n    \"supported_output_kinds\": [\n      \"python_code\",\n      \"markdown\",\n      \"json\",\n      \"powershell\",\n      \"workflow_yaml\",\n      \"path_group\",\n      \"text_or_config\"\n    ],\n    \"default_operation\": \"manual_patch_suggestion\",\n    \"default_write_policy\": \"manual_review_only\",\n    \"provider_execution_performed\": false\n  },\n  \"reports_read\": [\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\python_syntax.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_modules.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_helper_tests.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_docs.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\provider_result_parsing.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\provider_result_report.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\ai_workload_report_quality.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_runtime_ou",
```

## Context after

      "preview_chars": 1500,
      "line_count": 121
    },
    {
      "path": "output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 190374,
      "sha256": "7a2592f10def40f97e0b5433f535ed217de72cbaaa93a040582c33a424cac6e9",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"post_validation_ai_work_packet\",\n  \"generated_at\": \"2026-05-01T20:50:40\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"profile\": \"core\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"packet_manifest\": {\n    \"schema_version\": 1,\n    \"kind\": \"post_validation_ai_work_packet_manifest\",\n    \"path\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_packets\\\\gpu_planner_nonempty_recommendations_advisory_manifest.json\",\n    \"outputs\": {\n      \"json\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_packets\\\\gpu_planner_nonempty_recommendations_advisory.json\",\n      \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_packets\\\\gpu_planner_nonempty_recommendations_advisory.md\"\n    },\n    \"profile\": \"core\",\n    \"input_count\": 34,\n    \"requested_context_files\": [\n      \"AGENTS.md\",\n      \"WORKFLOW.md\",\n      \"docs/AI_DOCS_ENTRYPOINT.md\",\n      \"docs/PROJECT_STATUS_POINT.md\",\n      \"docs/TECH_DEBT_TRACKER.md\",\n      \"docs/REFACTORING_AND_REUSE_PLAN.md\",\n      \"docs/JSON_SCHEMAS.md\",\n      \"docs/AI_ARTIFACT_SCHEMAS.md\",\n      \"Tools/npu/pipeline/README.md\",\n      \"Tools/validation/README.md\",\n      \"./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md\",\n      \"./Tools/ai/run_agent_gpu_deep_planning_review.py\",\n      \"./Tools/ai/run_agent_gpu_deep_planning_supervised.py\",\n      \"./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py\",\n      \"./Tools/ai/build_ag",
