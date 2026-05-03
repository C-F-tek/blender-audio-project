# Evidence Chunk 0010/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `1377`
- line_end: `1448`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0009.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0011.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "preview_chars": 1500, "line_count": 164 }, { "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json", "exists": true, "suffix": ".json", "size_bytes": 5488, "sha256": "5bbf86d1908f977edf7d9a9cf0824d2eac9407686b3c23a480c9173a5ac96965", "ro...

## Context before

      "preview_chars": 1500,
      "line_count": 50
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5657,
      "sha256": "0d0d1fde554b1dee4509eec6904877282f1468860576cca9693170f77d860cce",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_planner_json_contract_replay\",\n  \"generated_at\": \"2026-05-03T23:22:54\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json\"\n  },\n  \"source_summary\": {\n    \"kind\": \"agent_gpu_deep_planning_supervised\",\n    \"passed\": true,\n    \"round_count\": 4,\n    \"recommendation_count\": 0,\n    \"json_parse_error_count\": 0,\n    \"repair_attempt_count\": 0,\n    \"empty_recommendations_reason\": \"model_output_schema_mismatch\",\n    \"evidence_ready_for_manual_patch_count\": 12\n  },\n  \"replayed_round_count\": 4,\n  \"contract_reason_counts\": {\n    \"model_output_schema_mismatch\": 4\n  },\n  \"context_echo_detected_count\": 0,\n  \"json_parse_failure_count\": 0,\n  \"model_output_schema_mismatch_count\": 4,\n  \"valid_recommendation_output_count\": 0,\n  \"rounds\": [\n    {\n      \"round\": 1,\n      \"original_empty_recommendations_reason\": \"model_output_schema_mismatch\",\n      \"original_json_ok\": true,\n      \"original_parse_error\": \"\",\n      \"original_response_chars\": 70,\n      \"contract\": {\n        \"json_ok\": true,\n        \"schema_ok\": false,\n        \"context_echo_detected\": false,\n        \"pa",

## Chunk content

```json
      "preview_chars": 1500,
      "line_count": 164
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5488,
      "sha256": "5bbf86d1908f977edf7d9a9cf0824d2eac9407686b3c23a480c9173a5ac96965",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_npu_run_sync_analysis\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json\"\n  },\n  \"metrics\": {\n    \"gpu_round_count\": 4,\n    \"npu_audit_count\": 1,\n    \"npu_audit_success_count\": 1,\n    \"npu_audit_round_coverage\": 0.25,\n    \"avg_gpu_round_seconds\": 29.51,\n    \"p50_gpu_round_seconds\": 29.51,\n    \"p90_gpu_round_seconds\": 29.51,\n    \"avg_npu_audit_seconds\": 104.0,\n    \"p50_npu_audit_seconds\": 104.0,\n    \"p90_npu_audit_seconds\": 104.0,\n    \"npu_to_gpu_avg_duration_ratio\": 3.524,\n    \"gpu_elapsed_seconds\": 118.039,\n    \"provider_execution_performed\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"gpu_metrics_source\": \"gpu_elapsed_divided_by_round_count\"\n  },\n  \"performance\": {\n    \"analyzer_elapsed_seconds\": 0.0,\n    \"gpu\": {\n      \"elapsed_seconds\": 118.039,\n      \"round_count\": 4,\n      \"round_duration_source\": \"gpu_elapsed_divided_by_round_count\",\n      \"round_duration_sample_count\": 1,\n      \"avg_round_seconds\": 29.51,\n      \"p50_round_seconds\": 29.51,\n      ",
      "preview_chars": 1500,
      "line_count": 147
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 173927,
      "sha256": "d7ee8744f7bccfd214b41c06c043668fc320019a33afcb3c4e9b61692c2ae769",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 20,\n  \"recommendations\": [\n    {\n      \"id\": \"consistency_001\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.",
      "preview_chars": 1500,
      "line_count": 3796
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5267,
      "sha256": "da76d67b8b48c27aa042047e263d140063df659cd111e54daf8bb03153ce4584",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"gpu_output\": \"output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json\",\n  \"gpu_recommendation_count\": 20,\n  \"gpu_empty_recommendations_reason\": \"\",\n  \"gpu_recommended_next_layer\": \"build_agent_review_patch_plan.py\",\n  \"npu_audits\": [\n    {\n      \"round\": 1,\n      \"checkpoint\": \"output/ai_pipeline/full_toolbox_20260503-231855_checkpoints/round_001.json\",\n      \"audit_output\": \"output/ai_pipeline/full_toolbox_20260503-231855_checkpoints/round_001_npu_async_audit.json\",\n      \"started_at\": \"2026-05-03T23:21:08\",\n      \"status\": \"finished\",\n      \"command\": [\n        \"C:\\\\Python314\\\\python.exe\",\n        \"Tools/ai/run_npu_gpu_deep_review_auditor.py\",\n        \"--repo-root\",\n        \".\",\n        \"--gpu-review\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_checkpoints\\\\round_001.json\",\n        \"--output\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_checkpoints\\\\round_001_npu_async_audit.json\",\n        \"--markdown-output\",\n        \"C:\\\\Users\\\\carmi\\\\blender\\\\bl",
      "preview_chars": 1500,
      "line_count": 92
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_agent_review_decision_loop.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2657,
      "sha256": "acddc346a5c5cb3328b37b663778e6c72d310976d5a9a045b01acace01cc26ac",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_decision_loop\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 20,\n  \"patch_plan_count\": 20,\n  \"deterministic_synthesizer_used\": true,\n  \"patch_plan_fallback_used\": false,\n  \"next_best_action\": \"manual_review_patch_plan\",\n  \"outputs\": {\n    \"recommendations\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json\",\n      \"exists\": true,\n      \"size_bytes\": 173927\n    },\n    \"recommendations_markdown\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.md\",\n      \"exists\": true,\n      \"size_bytes\": 19814\n    },\n    \"bridge_orchestrator\": {\n      \"path\": \"output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json\",\n      \"exists\": true,\n      \"size_bytes\": 5267\n    },\n    \"patch_plan\": {\n      \"path\": \"output/patch_specs/full_toolbox_20260503-231855_agent_review_patch_plan.json\",\n      \"exists\": true,\n      \"size_bytes\": 253164\n    },\n    \"patch_plan_markdown\": {\n      \"path\": \"output/patch_specs/full_toolbox_20260503-231855_agent_review_patch_plan.md\",\n      \"exists\": true,\n      \"size_bytes\": 19406\n    }\n  },\n  \"inputs\": {\n    \"evidence\": \"ou",
      "preview_chars": 1500,
      "line_count": 74
    },
    {
      "path": "output/patch_specs/full_toolbox_20260503-231855_agent_review_patch_plan.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 253164,
      "sha256": "95332bdc38ae1524888353162fb719b3581a1aa685141da8afc04d69630aee81",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_patch_plan\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_manual_review_patch_plan\",\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json\",\n    \"evidence\": \"output/ai_pipeline/agent_review_evidence_sufficiency.json\",\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json\",\n    \"orchestrator_kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n    \"evidence_kind\": \"agent_review_evidence_sufficiency\",\n    \"gpu_kind\": \"deterministic_recommendation_synthesizer\"\n  },\n  \"decision\": {\n    \"ready_for_manual_review\": true,\n    \"patch_plan_count\": 20,\n    \"skipped_candidate_count\": 0,\n    \"gpu_recommendation_count\": 20,\n    \"gpu_ready_count\": 0,\n    \"fallback_used\": false,\n    \"evidence_ready_for_manual_patch_count\": 12,\n    \"evidence_sufficient_for_real_pr\": true,\n    \"recommended_next_layer\": \"manual_review_then_targeted_patch\",\n    \"manual_review_required\": true,\n    \"cosmetic_patch_suppression_enabled\": true\n  },\n  \"patch_plan_count\": 20,\n  \"available_patch_plan_count\": 20,\n  \"max_patch_plans\": 0,\n  \"requested_max_patch_plans\": 0,\n  \"patch_plans\": [\n    {\n     ",
      "preview_chars": 1500,
      "line_count": 4894
    },
    {
      "path": "output/ai_pipeline/repository_change_proposals.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 7325,
      "sha256": "9d8109da2aaf830ffd7a9eef81027433515e09bb398ff80530157af986b52950",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_change_proposals\",\n  \"generated_at\": \"2026-05-03T23:22:55\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"profile\": \"core\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"apply_mode\": \"manual_review_only\",\n  \"suggestion_contract\": {\n    \"schema_version\": 1,\n    \"supported_output_kinds\": [\n      \"python_code\",\n      \"markdown\",\n      \"json\",\n      \"powershell\",\n      \"workflow_yaml\",\n      \"path_group\",\n      \"text_or_config\"\n    ],\n    \"default_operation\": \"manual_patch_suggestion\",\n    \"default_write_policy\": \"manual_review_only\",\n    \"provider_execution_performed\": false\n  },\n  \"reports_read\": [\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\python_syntax.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_modules.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_helper_tests.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_docs.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\provider_result_parsing.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\provider_result_report.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\ai_workload_report_quality.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_runtime_ou",
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
