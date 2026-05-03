# Evidence Chunk 0015/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `1949`
- line_end: `1988`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0014.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0016.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "preview_chars": 1500, "line_count": 121 }, { "path": "output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json", "exists": true, "suffix": ".json", "size_bytes": 190374, "sha256": "7a2592f10def40f97e0b5433f535ed217de72cbaaa93a040582c33a424cac6e9",...

## Context before

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

## Chunk content

```json
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
      "preview_chars": 1500,
      "line_count": 1078
    },
    {
      "path": "output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 7530,
      "sha256": "39d76f6edb1dc0f7809dde0ccf611349db58a544a1e159d23b1142a369486773",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_change_proposals\",\n  \"generated_at\": \"2026-05-01T20:50:40\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"profile\": \"core\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"apply_mode\": \"manual_review_only\",\n  \"suggestion_contract\": {\n    \"schema_version\": 1,\n    \"supported_output_kinds\": [\n      \"python_code\",\n      \"markdown\",\n      \"json\",\n      \"powershell\",\n      \"workflow_yaml\",\n      \"path_group\",\n      \"text_or_config\"\n    ],\n    \"default_operation\": \"manual_patch_suggestion\",\n    \"default_write_policy\": \"manual_review_only\",\n    \"provider_execution_performed\": false\n  },\n  \"reports_read\": [\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\python_syntax.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_modules.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_helper_tests.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_pipeline_docs.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\provider_result_parsing.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\provider_result_report.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\ai_workload_report_quality.json\",\n    \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\npu_runtime_ou",
      "preview_chars": 1500,
      "line_count": 145
    },
    {
      "path": "output/validation/full_memory_tool_regeneration_20260503-223900_workflow.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 4921,
      "sha256": "1bca61ddfe69272b954fb58dbcb5ea38ac580cf43ebcb893177f8547dbab2063",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n    \"schema_version\":  1,\n    \"kind\":  \"full_memory_tool_regeneration_workflow\",\n    \"generated_at\":  \"2026-05-03T22:39:18\",\n    \"repo_root\":  \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n    \"stamp\":  \"20260503-223900\",\n    \"profile\":  \"full_refactor\",\n    \"objective\":  \"Reload IA-Carmine full toolbox context before agent review full toolbox decision-loop run.\",\n    \"passed\":  true,\n    \"errors\":  [\n\n               ],\n    \"warnings\":  [\n\n                 ],\n    \"provider_execution_performed\":  false,\n    \"patch_application_performed\":  false,\n    \"source_writes_performed\":  false,\n    \"sqlite_write_performed\":  false,\n    \"persistent_memory_write_performed\":  false,\n    \"operational_sqlite_write_allowed_under_output\":  true,\n    \"report_count\":  13,\n    \"artifact_count\":  14,\n    \"reports\":  [\n                    \".\\\\output\\\\ai_pipeline\\\\full_memory_tool_regeneration_20260503-223900_agent_memory_inventory.json\",\n                    \".\\\\output\\\\ai_pipeline\\\\full_memory_tool_regeneration_20260503-223900_agnostic_tool_inventory.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_tool_regeneration_20260503-223900_persistent_memory_status.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_tool_regeneration_20260503-223900_operational_memory_status.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_tool_regeneration_20260503-223900_memory_routing_policy.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_tool_regeneration_2026",
      "preview_chars": 1500,
      "line_count": 67
    }
  ],
```

## Context after

  "included_artifacts": [
    {
      "path": "docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 31392,
      "sha256": "fe97cacf12f489cb2f1f65d981246dccdb35203423771c0b7c54f8ecd424b2df",
      "role": "explicit_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": true,
      "line_count": 943,
