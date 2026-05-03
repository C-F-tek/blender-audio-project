# Evidence Chunk 0041/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `5767`
- line_end: `5838`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0040.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0042.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: registrare i risultati di una pipeline di AI per il progetto “blender‑audio‑project”, includendo orchestratore GPU, pianificazione GPU parallela e mappa di coerenza del repository.  
**Segnali principali**: l’orchestratore non ha superato il test (`passed:false`, `gpu_returncode:2`), la pianificazione GPU parallela ha fallito per errori di parsing JSON (`json_parse_failure`), e la mappa di coerenza ha rilevato 2327 anomalie (816 high, 1465 medium, 46 low).  
**Guardrail/erori**

## Context before

        "decision": {
          "selected_chunks_built": true,
          "budget_respected": true,
          "provider_execution_seen": false,
          "source_writes_performed": false,
          "forbidden_paths_blocked": true
        },
        "errors": [],
        "warnings": []
      }
    }
  ],

## Chunk content

```json
  "artifact_manifest": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 46914,
      "sha256": "4d48c0a3aa8e35c16db123a614a511def22c3a1f63a9ebcd7427849fb5387afb",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-03T19:38:46\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": false,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 1686.543,\n  \"gpu_returncode\": 2,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": false,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-190820_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-190820_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 1679.037,\\n  \\\"round_count\\\": 50,\\n  \\\"npu_audit_count\\\": 0,\\n  \\\"npu_audit_success_count\\\": 0,\\n  \\\"npu_auditor_disabled_reason\\\": \\\"\\\",\\n  \\\"recommendation_count\\\": 0,\\n  \\\"raw_recommendation_candidate_count\\\": 0,\\n  \\\"filtered_recommendation_count\\\": 0,\\n  \\\"tool_request_count\\\": 0,\\n  \\\"valid_tool_request_count\\\": 0,\\n  \\\"invalid_tool_request_count\\\": 0,\\n  \\\"empty_recommendations_reason\\\": \\\"json_parse_failure\\\",\\n  \\\"runtime_tool_broker_enabled\\\": false,\\n  \\\"runtime_tool_bootstrap_executed\\\": false,\\n  \\\"runtime_tool_bootstrap_passed\\\": null,\\n  \\\"runtime_to",
      "preview_chars": 1500,
      "line_count": 738
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 241760,
      "sha256": "642c196f0c9e0d91757d8c155f674897336dffb9608d6c49b7e67e8341fc1fcf",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_deep_planning_supervised\",\n  \"generated_at\": \"2026-05-03T19:38:39\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": false,\n  \"errors\": [\n    \"round 1: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 2: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 3: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 4: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 5: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 6: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 7: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 8: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 9: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 10: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value\",\n    \"round 11: UnboundLocalError: cannot access local variable 'raw_response' where it is not a",
      "preview_chars": 1500,
      "line_count": 5560
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2969389,
      "sha256": "1f79291c9ad1c92bbf0f49544803baa194d85f016477dd42813a71d77348258a",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map\",\n  \"generated_at\": \"2026-05-03T19:10:40\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"scope\": {\n    \"markdown_file_count\": 1236,\n    \"python_file_count\": 316,\n    \"markdown_reference_count\": 39844,\n    \"markdown_python_command_count\": 1277,\n    \"python_inventory_count\": 316\n  },\n  \"finding_count\": 2327,\n  \"severity_counts\": {\n    \"high\": 816,\n    \"low\": 46,\n    \"medium\": 1465\n  },\n  \"finding_kind_counts\": {\n    \"documented_python_script_without_obvious_smoke\": 46,\n    \"md_cli_arg_not_in_argparse\": 2,\n    \"md_mentions_missing_markdown_path\": 1463,\n    \"md_mentions_missing_powershell_path\": 39,\n    \"md_mentions_missing_python_path\": 763,\n    \"md_python_command_script_missing\": 14\n  },\n  \"markdown_reference_kind_counts\": {\n    \"artifact\": 7558,\n    \"markdown\": 8945,\n    \"powershell\": 685,\n    \"python\": 22656\n  },\n  \"findings\": [\n    {\n      \"kind\": \"md_mentions_missing_python_path\",\n      \"severity\": \"high\",\n      \"source\": \".aider.chat.history.md\",\n      \"line\": 91,\n      \"target\": \"animation.cpython-313.py\",\n      \"evidence\": \"> C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\Scripting\\\\v61b\\\\__pycache__\\\\an",
      "preview_chars": 1500,
      "line_count": 63375
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1200,
      "sha256": "39116210e0868d9d14ec6106f1ed4ea42f5f8b395dac38485439ee2cbfad80aa",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map_smoke\",\n  \"generated_at\": \"2026-05-03T19:10:40\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"returncode\": 0,\n  \"workers_requested\": 18,\n  \"mapper_report_reused\": true,\n  \"elapsed_seconds\": 0.016,\n  \"stdout_tail\": \"\",\n  \"stderr_tail\": \"\",\n  \"runner_error\": null,\n  \"mapper_output\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json\",\n  \"mapper_markdown\": null,\n  \"finding_count\": 2327,\n  \"severity_counts\": {\n    \"high\": 816,\n    \"low\": 46,\n    \"medium\": 1465\n  },\n  \"markdown_reference_count\": 39844,\n  \"markdown_python_command_count\": 1277,\n  \"guardrails\": {\n    \"report_only\": true,\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"sqlite_write_performed\": false,\n    \"persistent_memory_write_performed\": false\n  }\n}\n",
      "preview_chars": 1161,
      "line_count": 39
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5624,
      "sha256": "5abc7edf98c7e9f046eb51b29a9f1d8f86f48db527dc99566de0c28ade11c984",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_npu_run_sync_analysis\",\n  \"generated_at\": \"2026-05-03T19:38:46\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json\"\n  },\n  \"metrics\": {\n    \"gpu_round_count\": 50,\n    \"npu_audit_count\": 9,\n    \"npu_audit_success_count\": 9,\n    \"npu_audit_round_coverage\": 0.18,\n    \"avg_gpu_round_seconds\": 33.731,\n    \"p50_gpu_round_seconds\": 33.731,\n    \"p90_gpu_round_seconds\": 33.731,\n    \"avg_npu_audit_seconds\": 105.556,\n    \"p50_npu_audit_seconds\": 106.0,\n    \"p90_npu_audit_seconds\": 108.0,\n    \"npu_to_gpu_avg_duration_ratio\": 3.129,\n    \"gpu_elapsed_seconds\": 1686.543,\n    \"provider_execution_performed\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"gpu_metrics_source\": \"gpu_elapsed_divided_by_round_count\"\n  },\n  \"performance\": {\n    \"analyzer_elapsed_seconds\": 0.001,\n    \"gpu\": {\n      \"elapsed_seconds\": 1686.543,\n      \"round_count\": 50,\n      \"round_duration_source\": \"gpu_elapsed_divided_by_round_count\",\n      \"round_duration_sample_count\": 1,\n      \"avg_round_seconds\": 33.731,\n      \"p50_round_seconds\": 3",
      "preview_chars": 1500,
      "line_count": 148
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
```

## Context after

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
