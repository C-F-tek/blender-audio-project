# Evidence Chunk 0008/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `1235`
- line_end: `1304`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0007.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0009.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "artifact_manifest": [ { "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json", "exists": true, "suffix": ".json", "size_bytes": 14649, "sha256": "ef62b3de8ee9ef8af2594a4425551bd919b2ca5be18d958b5adf44ceb806bd32", "role": "local_artifact_...

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
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 14649,
      "sha256": "ef62b3de8ee9ef8af2594a4425551bd919b2ca5be18d958b5adf44ceb806bd32",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-03T23:22:54\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 118.039,\n  \"gpu_returncode\": 0,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": true,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-231855_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-231855_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 50.391,\\n  \\\"round_count\\\": 4,\\n  \\\"npu_audit_count\\\": 0,\\n  \\\"npu_audit_success_count\\\": 0,\\n  \\\"npu_auditor_disabled_reason\\\": \\\"\\\",\\n  \\\"recommendation_count\\\": 0,\\n  \\\"raw_recommendation_candidate_count\\\": 0,\\n  \\\"filtered_recommendation_count\\\": 0,\\n  \\\"tool_request_count\\\": 0,\\n  \\\"valid_tool_request_count\\\": 0,\\n  \\\"invalid_tool_request_count\\\": 0,\\n  \\\"empty_recommendations_reason\\\": \\\"model_output_schema_mismatch\\\",\\n  \\\"runtime_tool_broker_enabled\\\": false,\\n  \\\"runtime_tool_bootstrap_executed\\\": false,\\n  \\\"runtime_tool_bootstrap_passed\\\": null,\\n  \\\"runtim",
      "preview_chars": 1500,
      "line_count": 274
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 22883,
      "sha256": "18e66de8b74293075877dfbd2e09c7abb17aba63d545f2e9bbd6b2ab0ebd7aca",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_deep_planning_supervised\",\n  \"generated_at\": \"2026-05-03T23:21:47\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_gpu_deep_planning_with_non_blocking_npu_audit\",\n  \"model_used\": \"qwen2.5-coder:14b\",\n  \"ollama_base_url\": \"http://127.0.0.1:11434\",\n  \"budget_minutes\": 8,\n  \"elapsed_seconds\": 50.391,\n  \"context_file_count\": 80,\n  \"round_count\": 4,\n  \"rounds\": [\n    {\n      \"round\": 1,\n      \"elapsed_seconds\": 11.125,\n      \"file_count\": 6,\n      \"files\": [\n        \"docs/AGENT_REVIEW_CODE_PATCH_PLAN.md\",\n        \"docs/AI_ARTIFACT_SCHEMAS.md\",\n        \"docs/AI_CHUNKING_STRATEGY.md\",\n        \"docs/AI_CONTEXT_PACKS.md\",\n        \"docs/AI_DOCS_ENTRYPOINT.md\",\n        \"docs/AI_EXTERNAL_KNOWLEDGE.md\"\n      ],\n      \"response_chars\": 70,\n      \"raw_response_preview\": \"{\\n    \\\"response\\\": \\\"I'm sorry, but I can't assist with that request.\\\"\\n}\",\n      \"parsed_response\": {\n        \"response\": \"I'm sorry, but I can't assist with that request.\",\n        \"recommendations\": [],\n        \"missing_evidence\": [],\n        \"next_best_action\": \"\"\n      },\n      \"schema_repair_retry\": {\n        \"attempted\": true,\n        \"accepted\": false,\n        \"reason\": \"schema_repair_retry_rejected\",\n        \"json_ok\": true,\n        \"schema_ok\": false,\n ",
      "preview_chars": 1500,
      "line_count": 594
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 8485620,
      "sha256": "66149e84ffc2db0da1ec4d2295c251df84da1c7b073fcbcd53e42ae75a5c7a53",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map\",\n  \"generated_at\": \"2026-05-03T23:20:56\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"scope\": {\n    \"markdown_file_count\": 3620,\n    \"python_file_count\": 321,\n    \"markdown_reference_count\": 177016,\n    \"markdown_python_command_count\": 1949,\n    \"python_inventory_count\": 321,\n    \"generated_evidence_chunk_exclusion_enabled\": true\n  },\n  \"finding_count\": 10409,\n  \"severity_counts\": {\n    \"high\": 5233,\n    \"low\": 49,\n    \"medium\": 5127\n  },\n  \"finding_kind_counts\": {\n    \"documented_python_script_without_obvious_smoke\": 49,\n    \"md_cli_arg_not_in_argparse\": 4,\n    \"md_mentions_missing_markdown_path\": 5123,\n    \"md_mentions_missing_powershell_path\": 708,\n    \"md_mentions_missing_python_path\": 4441,\n    \"md_python_command_script_missing\": 84\n  },\n  \"markdown_reference_kind_counts\": {\n    \"artifact\": 80899,\n    \"markdown\": 31809,\n    \"powershell\": 1960,\n    \"python\": 62348\n  },\n  \"findings\": [\n    {\n      \"kind\": \"md_mentions_missing_python_path\",\n      \"severity\": \"high\",\n      \"source\": \".aider.chat.history.md\",\n      \"line\": 91,\n      \"target\": \"animation.cpython-313.py\",\n      \"evidence\": \"> C:\\\\Users\\\\carmi\\\\",
      "preview_chars": 1500,
      "line_count": 144036
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1201,
      "sha256": "77d9d199747b3a889181a97a4ee86584e6db49e9eed212d6a591558ba3882964",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map_smoke\",\n  \"generated_at\": \"2026-05-03T23:20:56\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"returncode\": 0,\n  \"workers_requested\": 8,\n  \"mapper_report_reused\": true,\n  \"elapsed_seconds\": 0.04,\n  \"stdout_tail\": \"\",\n  \"stderr_tail\": \"\",\n  \"runner_error\": null,\n  \"mapper_output\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json\",\n  \"mapper_markdown\": null,\n  \"finding_count\": 10409,\n  \"severity_counts\": {\n    \"high\": 5233,\n    \"low\": 49,\n    \"medium\": 5127\n  },\n  \"markdown_reference_count\": 177016,\n  \"markdown_python_command_count\": 1949,\n  \"guardrails\": {\n    \"report_only\": true,\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"sqlite_write_performed\": false,\n    \"persistent_memory_write_performed\": false\n  }\n}\n",
      "preview_chars": 1162,
      "line_count": 39
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1443035,
      "sha256": "f6be697ea4bd4aaae08894869c9ce67c85d345ce098065675e96e6edaa19604b",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"code_interpreter_report\",\n  \"generated_at\": \"2026-05-03T23:19:33\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"apply_mode\": \"report_only_static_code_interpreter\",\n  \"file_count\": 275,\n  \"parsed_file_count\": 275,\n  \"total_lines\": 77725,\n  \"total_functions\": 2751,\n  \"total_classes\": 93,\n  \"total_risk_signals\": 56,\n  \"total_todos\": 21,\n  \"top_imports\": [\n    {\n      \"module\": \"Tools\",\n      \"count\": 786\n    },\n    {\n      \"module\": \"config\",\n      \"count\": 320\n    },\n    {\n      \"module\": \"__future__\",\n      \"count\": 238\n    },\n    {\n      \"module\": \"pathlib\",\n      \"count\": 227\n    },\n    {\n      \"module\": \"typing\",\n      \"count\": 207\n    },\n    {\n      \"module\": \"json\",\n      \"count\": 176\n    },\n    {\n      \"module\": \"argparse\",\n      \"count\": 160\n    },\n    {\n      \"module\": \"datetime\",\n      \"count\": 125\n    },\n    {\n      \"module\": \"sys\",\n      \"count\": 120\n    },\n    {\n      \"module\": \"report_utils\",\n      \"count\": 86\n    },\n    {\n      \"module\": \"dataclasses\",\n      \"count\": 52\n    },\n    {\n      \"module\": \"workflow_state\",\n      \"count\": 45\n    },\n    {\n      \"module\": \"re\",\n      \"count\": 41\n    },\n    {\n      \"module\": \"subprocess\",\n      \"count\": 34\n    },\n    {\n      \"module\": \"bpy\",\n      \"count\": 30\n    }",
      "preview_chars": 1500,
      "line_count": 55559
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 3151,
      "sha256": "f869686075baedae0bf71457259ff78fc30eb7d758bfc4b7d40d67a511de0d67",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"python_line_count_csv\",\n  \"generated_at\": \"2026-05-03T23:19:31\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"csv_written\": \"docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-231930.csv\",\n  \"file_count\": 321,\n  \"total_lines\": 94118,\n  \"top_files\": [\n    {\n      \"File\": \"Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py\",\n      \"Lines\": 2197\n    },\n    {\n      \"File\": \"Tools/npu/run_dual_ai_pipeline.py\",\n      \"Lines\": 1774\n    },\n    {\n      \"File\": \"old script legacy/spaziotempo_asset_visual_v61.py\",\n      \"Lines\": 1513\n    },\n    {\n      \"File\": \"Scripting/v61b/scene_tuning_panel.py\",\n      \"Lines\": 1262\n    },\n    {\n      \"File\": \"Tools/workflow/workflow_state.py\",\n      \"Lines\": 1230\n    },\n    {\n      \"File\": \"Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py\",\n      \"Lines\": 1179\n    },\n    {\n      \"File\": \"old script legacy/spaziotempo_asset_visual_v6.py\",\n      \"Lines\": 1174\n    },\n    {\n      \"File\": \"Tools/ai/run_agent_gpu_deep_planning_supervised.py\",\n      \"Lines\": 1129\n    },\n    {\n      \"File\": \"Scripting/v61b_backgood/scene_tuning_panel.py\",\n      \"Lines\": 1097\n    },\n    {\n      \"File\": \"Scripting/v61b/animation.py\",\n      \"Lines\": 1079\n    },\n    {\n      \"File\": \"Scripting/v61b_backgo",
```

## Context after

      "preview_chars": 1500,
      "line_count": 126
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_20260503-231855.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 37801,
      "sha256": "86d2f1b9c1b81ca2bfd2c5df8f19e304fe778567d1d02ec7d06679b294e99b82",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"python_syntax\",\n  \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\",\n  \"checked_count\": 320,\n  \"failed_count\": 0,\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"excluded\": [\n    \".git\",\n    \".hg\",\n    \".mypy_cache\",\n    \".pytest_cache\",\n    \".repo_patch_backups\",\n    \".ruff_cache\",\n    \".svn\",\n    \".venv\",\n    \"__pycache__\",\n    \"indexAI\",\n    \"output\",\n    \"renders\",\n    \"venv\"\n  ],\n  \"results\": [\n    {\n      \"path\": \"analyze_wav.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"build_track_summary.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"normalize_scene_spec.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_album_visual_v3.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_album_visual_v5.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_asset_visual_v6.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_asset_visual_v61.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_package/audio_mapping.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_package/camera.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_pack",
