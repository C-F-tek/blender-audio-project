# Evidence Chunk 0012/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `1735`
- line_end: `1804`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0011.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0013.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Registrare i risultati di una pipeline di orchestrazione GPU/NPU per un progetto audio‑AI, includendo output di pianificazione, audit e mappatura di coerenza del repository.  
**Segnali principali**:  
- *Orchestrator* (full_toolbox_20260503-223900_orchestrator.json): esecuzione parallela GPU con audit NPU, 278 s, nessun errore, output riferito a file paralleli.  
- *Parallel GPU* (full_toolbox_20260503-223900_parallel_gpu.json): pianificazione profonda con modello Qwen2.5

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
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 18643,
      "sha256": "85f4066c552fe98d814965569c406169603100d024e7926a6436100d7cd3c44f",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-03T22:45:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 278.09,\n  \"gpu_returncode\": 0,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": true,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-223900_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-223900_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 203.44,\\n  \\\"round_count\\\": 8,\\n  \\\"npu_audit_count\\\": 0,\\n  \\\"npu_audit_success_count\\\": 0,\\n  \\\"npu_auditor_disabled_reason\\\": \\\"\\\",\\n  \\\"recommendation_count\\\": 0,\\n  \\\"raw_recommendation_candidate_count\\\": 0,\\n  \\\"filtered_recommendation_count\\\": 0,\\n  \\\"tool_request_count\\\": 0,\\n  \\\"valid_tool_request_count\\\": 0,\\n  \\\"invalid_tool_request_count\\\": 0,\\n  \\\"empty_recommendations_reason\\\": \\\"context_echo_detected\\\",\\n  \\\"runtime_tool_broker_enabled\\\": false,\\n  \\\"runtime_tool_bootstrap_executed\\\": false,\\n  \\\"runtime_tool_bootstrap_passed\\\": null,\\n  \\\"runtime_tool_b",
      "preview_chars": 1500,
      "line_count": 332
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 68132,
      "sha256": "c62431d23c5e6894a6e5413eff1074d8fdf62669d2b9a43563bae9bbc3bfbcbb",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_deep_planning_supervised\",\n  \"generated_at\": \"2026-05-03T22:44:16\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_gpu_deep_planning_with_non_blocking_npu_audit\",\n  \"model_used\": \"qwen2.5-coder:14b\",\n  \"ollama_base_url\": \"http://127.0.0.1:11434\",\n  \"budget_minutes\": 12,\n  \"elapsed_seconds\": 203.44,\n  \"context_file_count\": 120,\n  \"round_count\": 8,\n  \"rounds\": [\n    {\n      \"round\": 1,\n      \"elapsed_seconds\": 43.381,\n      \"file_count\": 8,\n      \"files\": [\n        \"docs/AGENT_REVIEW_CODE_PATCH_PLAN.md\",\n        \"docs/AI_ARTIFACT_SCHEMAS.md\",\n        \"docs/AI_CHUNKING_STRATEGY.md\",\n        \"docs/AI_CONTEXT_PACKS.md\",\n        \"docs/AI_DOCS_ENTRYPOINT.md\",\n        \"docs/AI_EXTERNAL_KNOWLEDGE.md\",\n        \"docs/AI_GENERATED_PACKAGE_STANDARD.md\",\n        \"docs/AI_GUARDRAILS_VALIDATION_GUIDE.md\"\n      ],\n      \"response_chars\": 4656,\n      \"raw_response_preview\": \"{\\n    \\\"path\\\": \\\"docs/AI_GUARDRAILS_VALIDATION_GUIDE.md\\\",\\n    \\\"exists\\\": true,\\n    \\\"lines\\\": 212,\\n    \\\"chars\\\": 5842,\\n    \\\"content_preview\\\": \\\"# AI Guardrails and Validation Guide\\\\n\\\\n## Purpose\\\\n\\\\nThis guide defines how guardrails, schema validation and evaluation-style workflows should be applied to AI-generated artifacts in this repository.\\\\n\\\\nI",
      "preview_chars": 1500,
      "line_count": 1071
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 9334924,
      "sha256": "27dd1b4ce90ebffeb622b405cb3cd2a6183e1dd0682d69d3cbc0dc1c6a5a0903",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map\",\n  \"generated_at\": \"2026-05-03T22:40:52\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"scope\": {\n    \"markdown_file_count\": 3769,\n    \"python_file_count\": 320,\n    \"markdown_reference_count\": 183678,\n    \"markdown_python_command_count\": 1948,\n    \"python_inventory_count\": 320\n  },\n  \"finding_count\": 11488,\n  \"severity_counts\": {\n    \"high\": 6265,\n    \"low\": 49,\n    \"medium\": 5174\n  },\n  \"finding_kind_counts\": {\n    \"documented_python_script_without_obvious_smoke\": 49,\n    \"md_cli_arg_not_in_argparse\": 4,\n    \"md_mentions_missing_markdown_path\": 5170,\n    \"md_mentions_missing_powershell_path\": 972,\n    \"md_mentions_missing_python_path\": 5191,\n    \"md_python_command_script_missing\": 102\n  },\n  \"markdown_reference_kind_counts\": {\n    \"artifact\": 86178,\n    \"markdown\": 33873,\n    \"powershell\": 2200,\n    \"python\": 61427\n  },\n  \"findings\": [\n    {\n      \"kind\": \"md_mentions_missing_python_path\",\n      \"severity\": \"high\",\n      \"source\": \".aider.chat.history.md\",\n      \"line\": 91,\n      \"target\": \"animation.cpython-313.py\",\n      \"evidence\": \"> C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\Scripting\\\\v61b\\\\__pyca",
      "preview_chars": 1500,
      "line_count": 153712
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1202,
      "sha256": "35667dd4533e55cef69d7a12ec0cdd4d26aaa4c9abbfd11842449bbd394683a4",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"repository_consistency_map_smoke\",\n  \"generated_at\": \"2026-05-03T22:40:52\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"manual_review_required\": true,\n  \"returncode\": 0,\n  \"workers_requested\": 8,\n  \"mapper_report_reused\": true,\n  \"elapsed_seconds\": 0.044,\n  \"stdout_tail\": \"\",\n  \"stderr_tail\": \"\",\n  \"runner_error\": null,\n  \"mapper_output\": \"output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json\",\n  \"mapper_markdown\": null,\n  \"finding_count\": 11488,\n  \"severity_counts\": {\n    \"high\": 6265,\n    \"low\": 49,\n    \"medium\": 5174\n  },\n  \"markdown_reference_count\": 183678,\n  \"markdown_python_command_count\": 1948,\n  \"guardrails\": {\n    \"report_only\": true,\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"sqlite_write_performed\": false,\n    \"persistent_memory_write_performed\": false\n  }\n}\n",
      "preview_chars": 1163,
      "line_count": 39
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_20260503-223900.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1439710,
      "sha256": "8885c1a2d3991995d0c3f2143637910dbf67fb23d17399483b696cf3b0e904d5",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"code_interpreter_report\",\n  \"generated_at\": \"2026-05-03T22:39:21\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"apply_mode\": \"report_only_static_code_interpreter\",\n  \"file_count\": 274,\n  \"parsed_file_count\": 274,\n  \"total_lines\": 77526,\n  \"total_functions\": 2745,\n  \"total_classes\": 93,\n  \"total_risk_signals\": 56,\n  \"total_todos\": 21,\n  \"top_imports\": [\n    {\n      \"module\": \"Tools\",\n      \"count\": 786\n    },\n    {\n      \"module\": \"config\",\n      \"count\": 320\n    },\n    {\n      \"module\": \"__future__\",\n      \"count\": 237\n    },\n    {\n      \"module\": \"pathlib\",\n      \"count\": 226\n    },\n    {\n      \"module\": \"typing\",\n      \"count\": 207\n    },\n    {\n      \"module\": \"json\",\n      \"count\": 175\n    },\n    {\n      \"module\": \"argparse\",\n      \"count\": 159\n    },\n    {\n      \"module\": \"datetime\",\n      \"count\": 124\n    },\n    {\n      \"module\": \"sys\",\n      \"count\": 120\n    },\n    {\n      \"module\": \"report_utils\",\n      \"count\": 86\n    },\n    {\n      \"module\": \"dataclasses\",\n      \"count\": 52\n    },\n    {\n      \"module\": \"workflow_state\",\n      \"count\": 45\n    },\n    {\n      \"module\": \"re\",\n      \"count\": 41\n    },\n    {\n      \"module\": \"subprocess\",\n      \"count\": 34\n    },\n    {\n      \"module\": \"bpy\",\n      \"count\": 30\n    }",
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
```

## Context after

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
