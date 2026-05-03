# Evidence Chunk 0013/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `1805`
- line_end: `1876`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0012.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0014.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Fornire artefatti di validazione per il progetto “blender‑audio‑project”, verificando sintassi Python, contratti GPU planner e sintesi raccomandazioni.  
**Segnali principali**: tutti i file JSON indicano `passed: true`, nessun `error`

## Context before

      "preview_chars": 1500,
      "line_count": 55427
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 3151,
      "sha256": "ba015b984e9eb681aa2d9ed5ba2edad6fabf030c78d4242b154b30bdf90b264f",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"python_line_count_csv\",\n  \"generated_at\": \"2026-05-03T22:39:19\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"csv_written\": \"docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-223919.csv\",\n  \"file_count\": 320,\n  \"total_lines\": 93919,\n  \"top_files\": [\n    {\n      \"File\": \"Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py\",\n      \"Lines\": 2197\n    },\n    {\n      \"File\": \"Tools/npu/run_dual_ai_pipeline.py\",\n      \"Lines\": 1774\n    },\n    {\n      \"File\": \"old script legacy/spaziotempo_asset_visual_v61.py\",\n      \"Lines\": 1513\n    },\n    {\n      \"File\": \"Scripting/v61b/scene_tuning_panel.py\",\n      \"Lines\": 1262\n    },\n    {\n      \"File\": \"Tools/workflow/workflow_state.py\",\n      \"Lines\": 1230\n    },\n    {\n      \"File\": \"Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py\",\n      \"Lines\": 1179\n    },\n    {\n      \"File\": \"old script legacy/spaziotempo_asset_visual_v6.py\",\n      \"Lines\": 1174\n    },\n    {\n      \"File\": \"Tools/ai/run_agent_gpu_deep_planning_supervised.py\",\n      \"Lines\": 1129\n    },\n    {\n      \"File\": \"Scripting/v61b_backgood/scene_tuning_panel.py\",\n      \"Lines\": 1097\n    },\n    {\n      \"File\": \"Scripting/v61b/animation.py\",\n      \"Lines\": 1079\n    },\n    {\n      \"File\": \"Scripting/v61b_backgo",

## Chunk content

```json
      "preview_chars": 1500,
      "line_count": 126
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 37654,
      "sha256": "4ec42c05decf2357da47b1a40ecb0e31085372657dcede803bdd943bb6db9b28",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"python_syntax\",\n  \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\",\n  \"checked_count\": 319,\n  \"failed_count\": 0,\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"excluded\": [\n    \".git\",\n    \".hg\",\n    \".mypy_cache\",\n    \".pytest_cache\",\n    \".repo_patch_backups\",\n    \".ruff_cache\",\n    \".svn\",\n    \".venv\",\n    \"__pycache__\",\n    \"indexAI\",\n    \"output\",\n    \"renders\",\n    \"venv\"\n  ],\n  \"results\": [\n    {\n      \"path\": \"analyze_wav.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"build_track_summary.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"normalize_scene_spec.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_album_visual_v3.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_album_visual_v5.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_asset_visual_v6.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"old script legacy/spaziotempo_asset_visual_v61.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_package/audio_mapping.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_package/camera.py\",\n      \"ok\": true,\n      \"error\": null\n    },\n    {\n      \"path\": \"Scripting/_template_audio_reactive_pack",
      "preview_chars": 1500,
      "line_count": 1622
    },
    {
      "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 7152,
      "sha256": "f3287282ffa311b3edb7097d22def75f23b5e84c88ef2d293787deff5d86cea1",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_planner_json_contract_smoke\",\n  \"generated_at\": \"2026-05-03T22:39:22\",\n  \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"case_count\": 7,\n  \"failed_case_count\": 0,\n  \"cases\": [\n    {\n      \"name\": \"valid_recommendation\",\n      \"passed\": true,\n      \"expected_reason\": \"\",\n      \"result\": {\n        \"json_ok\": true,\n        \"schema_ok\": true,\n        \"context_echo_detected\": false,\n        \"parse_error\": \"\",\n        \"schema_errors\": [],\n        \"raw_response_sha256\": \"6a92b710401e93a30fec47fcef59b398e404b87036d01a7908fe4761b7f98319\",\n        \"raw_response_chars\": 757,\n        \"top_level_keys\": [\n          \"confidence\",\n          \"missing_evidence\",\n          \"next_best_action\",\n          \"recommendations\",\n          \"summary\"\n        ],\n        \"recommendation_count\": 1,\n        \"valid_recommendation_count\": 1,\n        \"invalid_recommendation_count\": 0,\n        \"tool_request_count\": 0,\n        \"valid_tool_request_count\": 0,\n        \"invalid_tool_request_count\": 0,\n        \"empty_recommendations_reason\": \"\"\n      }\n    },\n    {\n      \"name\": \"context_echo\",\n      \"passed\": true,\n      \"expected_reason\": \"context_echo_detected\",\n      \"result\": {",
      "preview_chars": 1500,
      "line_count": 214
    },
    {
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5378,
      "sha256": "e96a3cc002bf375883a8b8f7a679c3866dd6c4dd098c057b7d6480e6925348f9",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer_smoke\",\n  \"generated_at\": \"2026-05-03T22:39:22\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 1,\n  \"deterministic_synthesizer_used\": true,\n  \"next_best_action\": \"build_agent_review_patch_plan.py\",\n  \"synthesized_report\": {\n    \"schema_version\": 1,\n    \"kind\": \"deterministic_recommendation_synthesizer\",\n    \"generated_at\": \"2026-05-03T22:39:22\",\n    \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n    \"passed\": true,\n    \"errors\": [],\n    \"warnings\": [],\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"manual_review_required\": true,\n    \"recommendation_count\": 1,\n    \"recommendations\": [\n      {\n        \"id\": \"det_doc_code_001\",\n        \"area\": \"doc_code\",\n        \"status\": \"ready_for_patch_plan\",\n        \"target_files\": [\n          \"AGENTS.md\"\n        ],\n        \"rationale\": \"The documentation points at a recommendation lane that must be normalized before patch-plan construction.\",\n        \"proposed_strategy\": \"Create a narrow manual-review patch plan for the documentation/code r",
      "preview_chars": 1500,
      "line_count": 117
    },
    {
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1447,
      "sha256": "e0d03e157ad90c487ca1cfa2049672e1b53a83bbf5aef01777fdf309acf7f060",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_decision_loop_smoke\",\n  \"generated_at\": \"2026-05-03T22:39:22\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"returncode\": 0,\n  \"stdout_tail\": \"{\\n  \\\"passed\\\": true,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\validation\\\\\\\\agent_review_decision_loop_smoke\\\\\\\\decision_loop.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\validation\\\\\\\\agent_review_decision_loop_smoke\\\\\\\\decision_loop.md\\\",\\n  \\\"recommendation_count\\\": 1,\\n  \\\"patch_plan_count\\\": 1,\\n  \\\"deterministic_synthesizer_used\\\": true,\\n  \\\"patch_plan_fallback_used\\\": false,\\n  \\\"provider_execution_performed\\\": false,\\n  \\\"patch_application_performed\\\": false\\n}\\n\",\n  \"stderr_tail\": \"\",\n  \"decision_loop_output\": \"output/validation/agent_review_decision_loop_smoke/decision_loop.json\",\n  \"recommendation_count\": 1,\n  \"patch_plan_count\": 1,\n  \"deterministic_synthesizer_used\": true,\n  \"patch_plan_fallback_used\": false,\n  \"guardrails\": {\n    \"report_only\": true,\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"manual_review_required\": true\n  }\n}\n",
      "preview_chars": 1420,
      "line_count": 27
    },
    {
      "path": "output/validation/npu_provider_environment_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1745,
      "sha256": "c1dced0ef1faa33baeb633359b079dd26e5317f95be7fcbec5fadafcde51ac60",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"npu_provider_environment\",\n  \"generated_at\": \"2026-05-03T22:39:23\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_read_only_provider_preflight\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"returncode\": 0,\n  \"stdout_tail\": \"{\\\"python\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\venvs\\\\\\\\blender-npu-ai\\\\\\\\Scripts\\\\\\\\python.exe\\\", \\\"openvino_import\\\": true, \\\"available_devices\\\": [\\\"CPU\\\", \\\"GPU.0\\\", \\\"GPU.1\\\", \\\"NPU\\\"], \\\"npu_available\\\": true, \\\"openvino_genai_import\\\": true}\\n\",\n  \"stderr_tail\": \"\",\n  \"probe\": {\n    \"python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n    \"openvino_import\": true,\n    \"available_devices\": [\n      \"CPU\",\n      \"GPU.0\",\n      \"GPU.1\",\n      \"NPU\"\n    ],\n    \"npu_available\": true,\n    \"openvino_genai_import\": true\n  },\n  \"checks\": {\n    \"openvino_import\": true,\n    \"openvino_genai_import\": true,\n    \"openvino_genai_pip_package\": \"openvino-genai\",\n    \"npu_available\": true\n  },\n  \"decision\": {\n    \"npu_ready_for_auditor\": true,\n    \"gpu_review_should_be_blocked\": false,\n    \"npu_primary_advisory\": false\n  },\n  \"guardrails\": {\n    \"read_only\": true,\n    \"no_model_execution\": true,\n    \"provider_exe",
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
```

## Context after

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
