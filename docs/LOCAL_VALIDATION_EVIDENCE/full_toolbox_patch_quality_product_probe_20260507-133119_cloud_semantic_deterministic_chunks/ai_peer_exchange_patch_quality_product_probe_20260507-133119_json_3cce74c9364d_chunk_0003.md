# Evidence Chunk 0003/0006

- source: `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `3cce74c9364d7286ae6f1e61befb2b62211f0ab5de6182a5aaa6fe4f09a5097c`
- line_start: `361`
- line_end: `431`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/ai_peer_exchange_patch_quality_product_probe_20260507-133119_json_3cce74c9364d_chunk_0002.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/ai_peer_exchange_patch_quality_product_probe_20260507-133119_json_3cce74c9364d_chunk_0004.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: tool_results. Preview: "tool_results": [ { "id": "gpu0_peer_code_interpreter_context", "tool": "build_code_interpreter_report", "reason": "GPU0 peer worker needs current code-structure context through the broker allowlist.", "requested": true, "executed": true, "blocked": false, "dr...

## Context before

    "allowlisted_tools": [
      "build_agent_agnostic_tool_inventory",
      "build_agent_memory_inventory",
      "build_agent_transient_request_context",
      "build_code_interpreter_report",
      "build_python_line_count_csv",
      "build_refactor_duplication_audit",
      "check_python_syntax",
      "check_validation_report_contract",
      "run_gpu_planner_json_contract_smoke",
      "runtime_sqlite_memory"
    ],

## Chunk content

```json
    "tool_results": [
      {
        "id": "gpu0_peer_code_interpreter_context",
        "tool": "build_code_interpreter_report",
        "reason": "GPU0 peer worker needs current code-structure context through the broker allowlist.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.json",
          "markdown_report": "output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.md"
        },
        "summary": {
          "kind": "code_interpreter_report",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "report_only": true,
            "manual_review_required": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "blender_runtime_execution_performed": false,
            "sqlite_write_performed": false,
            "static_analysis_only": true,
            "project_code_executed": false,
            "providers_executed": false,
            "blender_runtime_executed": false,
            "patches_applied": false,
            "source_files_written": false
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_write_performed": false
        },
        "command": [
          "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
          "Tools/ai/build_code_interpreter_report.py",
          "--repo-root",
          ".",
          "--output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\patch_quality_product_probe_20260507-133119\\gpu0_peer\\gpu0_peer_code_interpreter_context_code_interpreter_report.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\patch_quality_product_probe_20260507-133119\\gpu0_peer\\gpu0_peer_code_interpreter_context_code_interpreter_report.md",
          "--input",
          "Tools/ai",
          "--input",
          "Tools/validation",
          "--input",
          "Tools/workflow",
          "--input",
          "Tools/npu"
        ],
        "stdout_tail": "      \"async\": false\n        },\n        {\n          \"name\": \"run_dual_ai\",\n          \"lineno\": 1053,\n          \"line_span\": 68,\n          \"arg_count\": 8,\n          \"branch_count\": 8,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"delete_target_set\",\n          \"lineno\": 582,\n          \"line_span\": 48,\n          \"arg_count\": 3,\n          \"branch_count\": 13,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"format_project_storage_stats\",\n          \"lineno\": 795,\n          \"line_span\": 44,\n          \"arg_count\": 1,\n          \"branch_count\": 9,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"scan_path_stats\",\n          \"lineno\": 641,\n          \"line_span\": 40,\n          \"arg_count\": 1,\n          \"branch_count\": 12,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"open_debug_monitor_window\",\n          \"lineno\": 1151,\n          \"line_span\": 34,\n          \"arg_count\": 2,\n          \"branch_count\": 2,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"audio_python_executable\",\n          \"lineno\": 313,\n          \"line_span\": 31,\n          \"arg_count\": 0,\n          \"branch_count\": 3,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"run_scene_director_brief\",\n          \"lineno\": 968,\n          \"line_span\": 31,\n          \"arg_count\": 1,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"load_session\",\n          \"lineno\": 159,\n          \"line_span\": 30,\n          \"arg_count\": 1,\n          \"branch_count\": 13,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"build_artifacts\",\n          \"lineno\": 93,\n          \"line_span\": 29,\n          \"arg_count\": 1,\n          \"branch_count\": 3,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"set_ai_models\",\n          \"lineno\": 266,\n          \"line_span\": 29,\n          \"arg_count\": 4,\n          \"branch_count\": 4,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"ensure_ai_prerequisites\",\n          \"lineno\": 1022,\n          \"line_span\": 29,\n          \"arg_count\": 3,\n          \"branch_count\": 10,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"set_current_wav\",\n          \"lineno\": 191,\n          \"line_span\": 25,\n          \"arg_count\": 1,\n          \"branch_count\": 2,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"mark_active_operation_interrupted\",\n          \"lineno\": 1187,\n          \"line_span\": 22,\n          \"arg_count\": 1,\n          \"branch_count\": 4,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"file_set_stats\",\n          \"lineno\": 692,\n          \"line_span\": 20,\n          \"arg_count\": 2,\n          \"branch_count\": 5,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"run_music_context\",\n          \"lineno\": 912,\n          \"line_span\": 20,\n          \"arg_count\": 3,\n          \"branch_count\": 1,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"available_operations\",\n          \"lineno\": 1211,\n          \"line_span\": 20,\n          \"arg_count\": 0,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"reset_to_default_wav\",\n          \"lineno\": 218,\n          \"line_span\": 19,\n          \"arg_count\": 0,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"available_ollama_models\",\n          \"lineno\": 248,\n          \"line_span\": 16,\n          \"arg_count\": 0,\n          \"branch_count\": 5,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"operation_status\",\n          \"lineno\": 859,\n          \"line_span\": 16,\n          \"arg_count\": 1,\n          \"branch_count\": 11,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"run_track_summary\",\n          \"lineno\": 894,\n          \"line_span\": 16,\n          \"arg_count\": 1,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"run_asset_inventory\",\n          \"lineno\": 950,\n          \"line_span\": 16,\n          \"arg_count\": 1,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"cleanup_render_frame_targets\",\n          \"lineno\": 565,\n          \"line_span\": 15,\n          \"arg_count\": 1,\n          \"branch_count\": 2,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"run_analyze_wav\",\n          \"lineno\": 877,\n          \"line_span\": 15,\n          \"arg_count\": 3,\n          \"branch_count\": 1,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"python_executable\",\n          \"lineno\": 297,\n          \"line_span\": 14,\n          \"arg_count\": 0,\n          \"branch_count\": 2,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"cleanup_intermediates\",\n          \"lineno\": 841,\n          \"line_span\": 11,\n          \"arg_count\": 3,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"default\",\n          \"lineno\": 141,\n          \"line_span\": 11,\n          \"arg_count\": 1,\n          \"branch_count\": 0,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"append_event\",\n          \"lineno\": 64,\n          \"line_span\": 10,\n          \"arg_count\": 3,\n          \"branch_count\": 1,\n          \"docstring_present\": false,\n          \"async\": false\n        }\n      ],\n      \"classes\": [\n        {\n          \"name\": \"WorkflowSession\",\n          \"lineno\": 125,\n          \"line_span\": 32,\n          \"method_count\": 2,\n          \"docstring_present\": false\n        },\n        {\n          \"name\": \"OperationResult\",\n          \"lineno\": 45,\n          \"line_span\": 12,\n          \"method_count\": 0,\n          \"docstring_present\": false\n        }\n      ],\n      \"imports\": [\n        {\n          \"type\": \"from\",\n          \"module\": \"__future__\",\n          \"name\": \"annotations\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"dataclasses\",\n          \"name\": \"dataclass\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"dataclasses\",\n          \"name\": \"asdict\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"datetime\",\n          \"name\": \"datetime\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"pathlib\",\n          \"name\": \"Path\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"json\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"os\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"re\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"shutil\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"subprocess\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"sys\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"import\",\n          \"name\": \"time\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"asset_inventory\",\n          \"name\": \"build_asset_inventory\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"scene_brief\",\n          \"name\": \"run_interactive_scene_brief\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"workflow_debug\",\n          \"name\": \"build_debug_report\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"workflow_debug\",\n          \"name\": \"format_debug_report\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"startup_check\",\n          \"name\": \"build_report\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"startup_check\",\n          \"name\": \"format_report\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"startup_check\",\n          \"name\": \"save_report\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"workflow_debug\",\n          \"name\": \"detect_active_operation\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"workflow_debug\",\n          \"name\": \"read_events\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"ollama_runtime\",\n          \"name\": \"list_models\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"ollama_runtime\",\n          \"name\": \"list_models_from_disk\",\n          \"asname\": \"\"\n        },\n        {\n          \"type\": \"from\",\n          \"module\": \"ollama_runtime\",\n          \"name\": \"DEFAULT_BASE_URL\",\n          \"asname\": \"\"\n        }\n      ],\n      \"risk_signals\": [\n        {\n          \"call\": \"subprocess.run\",\n          \"category\": \"subprocess_execution\",\n          \"lineno\": 381\n        },\n        {\n          \"call\": \"subprocess.Popen\",\n          \"category\": \"subprocess_execution\",\n          \"lineno\": 1173\n        },\n        {\n          \"call\": \"shutil.rmtree\",\n          \"category\": \"destructive_file_operation\",\n          \"lineno\": 604\n        }\n      ],\n      \"todo_signals\": [],\n      \"large_functions\": [\n        {\n          \"name\": \"cleanup_intermediate_targets\",\n          \"lineno\": 450,\n          \"line_span\": 113,\n          \"arg_count\": 3,\n          \"branch_count\": 10,\n          \"docstring_present\": false,\n          \"async\": false\n        }\n      ],\n      \"complex_functions\": [\n        {\n          \"name\": \"load_session\",\n          \"lineno\": 159,\n          \"line_span\": 30,\n          \"arg_count\": 1,\n          \"branch_count\": 13,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"run_command\",\n          \"lineno\": 346,\n          \"line_span\": 77,\n          \"arg_count\": 8,\n          \"branch_count\": 14,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"delete_target_set\",\n          \"lineno\": 582,\n          \"line_span\": 48,\n          \"arg_count\": 3,\n          \"branch_count\": 13,\n          \"docstring_present\": false,\n          \"async\": false\n        },\n        {\n          \"name\": \"scan_path_stats\",\n          \"lineno\": 641,\n          \"line_span\": 40,\n          \"arg_count\": 1,\n          \"branch_count\": 12,\n          \"docstring_present\": false,\n          \"async\": false\n        }\n      ]\n    }\n  ],\n  \"guardrails\": {\n    \"report_only\": true,\n    \"manual_review_required\": true,\n    \"provider_execution_performed\": false,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"blender_runtime_execution_performed\": false,\n    \"sqlite_write_performed\": false,\n    \"static_analysis_only\": true,\n    \"project_code_executed\": false,\n    \"providers_executed\": false,\n    \"blender_runtime_executed\": false,\n    \"patches_applied\": false,\n    \"source_files_written\": false\n  }\n}\n",
```

## Context after

        "stderr_tail": ""
      },
      {
        "id": "gpu0_peer_report_contract_context",
        "tool": "check_validation_report_contract",
        "reason": "GPU0 peer worker needs report-contract status for the evidence it received.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
