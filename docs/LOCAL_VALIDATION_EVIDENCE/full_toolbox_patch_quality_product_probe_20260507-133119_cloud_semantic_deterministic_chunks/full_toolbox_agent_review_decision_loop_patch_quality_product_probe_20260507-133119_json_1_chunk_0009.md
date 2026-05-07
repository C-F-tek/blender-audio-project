# Evidence Chunk 0009/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `1629`
- line_end: `1698`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0008.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0010.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "artifact_manifest": [ { "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json", "exists": true, "suffix": ".json", "size_bytes": 72790, "sha256": "b652af93b70b46f7c9059d998c48b8bf641ca2617fe268c3b6b30ace0b64d52...

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
      "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 72790,
      "sha256": "b652af93b70b46f7c9059d998c48b8bf641ca2617fe268c3b6b30ace0b64d52c",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-07T13:33:23\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"gpu_provider_execution_performed\": true,\n  \"gpu0_peer_support_provider_execution_performed\": true,\n  \"npu_provider_execution_performed\": false,\n  \"legacy_npu_provider_execution_performed\": false,\n  \"npu_micro_support_provider_execution_performed\": false,\n  \"npu_micro_support_provider_requested\": false,\n  \"legacy_npu_auditor_provider_requested\": false,\n  \"npu_auditor_provider_requested\": false,\n  \"npu_auditor_provider_performed\": false,\n  \"provider_degraded_reasons\": [],\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 61.694,\n  \"gpu_returncode\": 0,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": true,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 50.767,\\n  \\\"round_count\\\": 4,\\n  \\\"npu_a",
      "preview_chars": 1500,
      "line_count": 1067
    },
    {
      "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 23981,
      "sha256": "ec608cb1c5e4c45e0b97e8fef54382afcea3497c02344be90c173e05042fe9b5",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_deep_planning_supervised\",\n  \"generated_at\": \"2026-05-07T13:33:16\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_gpu_deep_planning_with_non_blocking_npu_audit\",\n  \"model_used\": \"qwen2.5-coder:14b\",\n  \"ollama_base_url\": \"http://127.0.0.1:11434\",\n  \"budget_minutes\": 5,\n  \"elapsed_seconds\": 50.767,\n  \"context_file_count\": 80,\n  \"round_count\": 4,\n  \"rounds\": [\n    {\n      \"round\": 1,\n      \"elapsed_seconds\": 11.982,\n      \"file_count\": 4,\n      \"files\": [\n        \"docs/AGENT_REVIEW_CODE_PATCH_PLAN/_ia_carmine_md_split_manifest.json\",\n        \"docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md\",\n        \"docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-002.md\",\n        \"docs/AGENT_REVIEW_CODE_PATCH_PLAN/README.md\"\n      ],\n      \"live_context_report_count\": 1,\n      \"live_context_refresh_performed\": true,\n      \"response_chars\": 382,\n      \"raw_response_preview\": \"{\\n  \\\"schema_version\\\": 1,\\n  \\\"kind\\\": \\\"agent_review_code_patch_plan\\\",\\n  \\\"passed\\\": true,\\n  \\\"provider_execution_performed\\\": false,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"source_writes_performed\\\": false,\\n  \\\"apply_mode\\\": \\\"report_only_manual_review_code_patch_plan\\\",\\n  \\\"manual_review_required\\\": true,\\n  \\\"patch_plan_count\\\": 0,\\n  \\\"code_patch_plans\\\": ",
      "preview_chars": 1500,
      "line_count": 600
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 9571446,
      "sha256": "31785b42fc13dd2ffc9803db0a98010073c9cb6a49ba8482eff7ea447b8de8af",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map\",\n  \"generated_at\": \"2026-05-07T13:32:17\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"scope\": {\n    \"repository_file_count\": 1642,\n    \"repository_file_metadata_count\": 1642,\n    \"repository_line_count_available_count\": 1616,\n    \"repository_text_line_count_total\": 1409295,\n    \"markdown_file_count\": 635,\n    \"python_file_count\": 650,\n    \"markdown_reference_count\": 84503,\n    \"markdown_python_command_count\": 786,\n    \"python_inventory_count\": 650,\n    \"generated_evidence_chunk_exclusion_enabled\": true\n  },\n  \"finding_count\": 12321,\n  \"severity_counts\": {\n    \"high\": 3952,\n    \"low\": 48,\n    \"medium\": 8321\n  },\n  \"finding_kind_counts\": {\n    \"documented_python_script_without_obvious_smoke\": 48,\n    \"md_cli_arg_not_in_argparse\": 2,\n    \"md_mentions_missing_markdown_path\": 8319,\n    \"md_mentions_missing_powershell_path\": 524,\n    \"md_mentions_missing_python_path\": 3384,\n    \"md_python_command_script_missing\": 44\n  },\n  \"markdown_reference_kind_counts\": {\n    \"artifact\": 14609,\n    \"markdown\": 21485,\n    \"powershell\": 1566,\n    \"python\": 46843\n  },\n  \"findings\": [\n    {\n      \"kind\": \"md_mentions_missing_python_",
      "preview_chars": 1500,
      "line_count": 165785
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1228,
      "sha256": "65319c9c2c36c5074d59e32ba8300fdb26cd54b287318b7292bb3800aa39b212",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map_smoke\",\n  \"generated_at\": \"2026-05-07T13:32:17\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"returncode\": 0,\n  \"workers_requested\": 0,\n  \"mapper_report_reused\": true,\n  \"elapsed_seconds\": 0.048,\n  \"stdout_tail\": \"\",\n  \"stderr_tail\": \"\",\n  \"runner_error\": null,\n  \"mapper_output\": \"output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n  \"mapper_markdown\": null,\n  \"finding_count\": 12321,\n  \"severity_counts\": {\n    \"high\": 3952,\n    \"low\": 48,\n    \"medium\": 8321\n  },\n  \"markdown_reference_count\": 84503,\n  \"markdown_python_command_count\": 786,\n  \"guardrails\": {\n    \"report_only\": true,\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"sqlite_write_performed\": false,\n    \"persistent_memory_write_performed\": false\n  }\n}\n",
      "preview_chars": 1189,
      "line_count": 39
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2129738,
      "sha256": "ecf26290d014dec76280c0f5d26360402c8cab1be1bb9a605adcecee1e4b352c",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"code_interpreter_report\",\n  \"generated_at\": \"2026-05-07T13:31:48\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"apply_mode\": \"report_only_static_code_interpreter\",\n  \"file_count\": 601,\n  \"parsed_file_count\": 601,\n  \"total_lines\": 101948,\n  \"total_functions\": 3667,\n  \"total_classes\": 101,\n  \"total_risk_signals\": 90,\n  \"total_todos\": 21,\n  \"top_imports\": [\n    {\n      \"module\": \"Tools\",\n      \"count\": 989\n    },\n    {\n      \"module\": \"__future__\",\n      \"count\": 541\n    },\n    {\n      \"module\": \"pathlib\",\n      \"count\": 420\n    },\n    {\n      \"module\": \"typing\",\n      \"count\": 376\n    },\n    {\n      \"module\": \"config\",\n      \"count\": 320\n    },\n    {\n      \"module\": \"json\",\n      \"count\": 300\n    },\n    {\n      \"module\": \"argparse\",\n      \"count\": 257\n    },\n    {\n      \"module\": \"sys\",\n      \"count\": 195\n    },\n    {\n      \"module\": \"datetime\",\n      \"count\": 179\n    },\n    {\n      \"module\": \"constants\",\n      \"count\": 151\n    },\n    {\n      \"module\": \"report_utils\",\n      \"count\": 88\n    },\n    {\n      \"module\": \"subprocess\",\n      \"count\": 68\n    },\n    {\n      \"module\": \"dataclasses\",\n      \"count\": 61\n    },\n    {\n      \"module\": \"re\",\n      \"count\": 50\n    },\n    {\n      \"module\": \"workflow_state\",\n      \"count\":",
      "preview_chars": 1500,
      "line_count": 82992
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 3162,
      "sha256": "4d083c04175564cfb3ef6fc26e9358d8dd7752a9e19c716001b2397f26bb3070",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"python_line_count_csv\",\n  \"generated_at\": \"2026-05-07T13:31:45\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"csv_written\": \"docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv\",\n  \"file_count\": 650,\n  \"total_lines\": 119498,\n  \"top_files\": [\n    {\n      \"File\": \"Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py\",\n      \"Lines\": 2263\n    },\n    {\n      \"File\": \"Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py\",\n      \"Lines\": 2197\n    },\n    {\n      \"File\": \"Tools/npu/run_dual_ai_pipeline.py\",\n      \"Lines\": 1774\n    },\n    {\n      \"File\": \"old script legacy/spaziotempo_asset_visual_v61.py\",\n      \"Lines\": 1513\n    },\n    {\n      \"File\": \"Scripting/v61b/scene_tuning_panel.py\",\n      \"Lines\": 1262\n    },\n    {\n      \"File\": \"Tools/workflow/workflow_state.py\",\n      \"Lines\": 1230\n    },\n    {\n      \"File\": \"Tools/ai/run_agent_gpu_deep_planning_supervised.py\",\n      \"Lines\": 1180\n    },\n    {\n      \"File\": \"old script legacy/spaziotempo_asset_visual_v6.py\",\n      \"Lines\": 1174\n    },\n    {\n      \"File\": \"Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py\",\n      \"Lines\": 1100\n    },\n    {\n      \"File\": \"Scripting/v61b_backgood/scene_tuning_panel.py\",\n      \"Lines\": 1097\n    },\n    {\n      \"File\": ",
```

## Context after

      "preview_chars": 1500,
      "line_count": 126
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 78343,
      "sha256": "35727466d17cdc5e3b687e0621da07adb44acca35de85e26abe49a898f7abd95",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"python_syntax\",\n  \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\",\n  \"checked_count\": 649,\n  \"failed_count\": 0,\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"excluded\": [\n    \".git\",\n    \".hg\",\n    \".mypy_cache\",\n    \".pytest_cache\",\n    \".repo_patch_backups\",\n    \".ruff_cache\",\n    \".svn\",\n    \".venv\",\n    \"__pycache__\",\n    \"indexAI\",\n    \"output\",\n    \"renders\",\n    \"venv\"\n  ],\n  \"results\": [\n    {\n      \"path\": \"analyze_wav.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"build_track_summary.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"normalize_scene_spec.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_album_visual_v3.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_album_visual_v5.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_asset_visual_v6.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_asset_visual_v61.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_package/audio_mapping.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_package/camera.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_pack",
