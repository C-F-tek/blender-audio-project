# Evidence Chunk 0011/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `1771`
- line_end: `1854`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0010.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0012.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "preview_chars": 1500, "line_count": 63 }, { "path": "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json", "exists": true, "suffix": ".json", "size_bytes": 6376, "sha256": "e3745d67a12053f5438d9605ab6e5740e96...

## Context before

      "preview_chars": 1500,
      "line_count": 50
    },
    {
      "path": "output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2242,
      "sha256": "a816f6425456f472ad117d324a31055d6eb73951ee073629beca835376a016d4",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"openvino_hardware_governance_report\",\n  \"generated_at\": \"2026-05-07T13:31:51\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"classification\": \"openvino_probe_available\",\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"available_devices\": [\n    \"CPU\",\n    \"GPU.0\",\n    \"GPU.1\",\n    \"NPU\"\n  ],\n  \"probe_error\": \"\",\n  \"gpu0_visible\": true,\n  \"gpu1_visible\": true,\n  \"npu_visible\": true,\n  \"gpu0_companion_model_dir_configured\": false,\n  \"requested_npu_micro_start_mode\": \"deferred\",\n  \"recommended_npu_micro_start_mode\": \"deferred\",\n  \"routing_policy\": {\n    \"gpu1_primary_advisory\": {\n      \"owner\": \"Ollama/CUDA\",\n      \"preferred_device\": \"RTX 5080 / CUDA / GPU1\",\n      \"openvino_device\": null,\n      \"policy\": \"reserved_for_primary_advisory_not_openvino_workload\"\n    },\n    \"gpu0_companion_peer\": {\n      \"owner\": \"OpenVINO companion worker\",\n      \"preferred_device\": \"GPU.0\",\n      \"semantic_model_configured\": false,\n      \"policy\": \"use GPU.0 when visible; never steal GPU.1 from Ollama\"\n    },\n    \"npu_micro_support\": {\n      \"owner\": \"OpenVINO NPU micro support\",\n      \"preferred_device\": \"NPU\",\n      \"start_mode\": \"deferred\",\n      \"policy\": \"live seed through broker while GPU mesh is active; provider execution may be deferred to avoid contention\"\n    },\n    \"deterministic_validators\": {\n      \"owne",

## Chunk content

```json
      "preview_chars": 1500,
      "line_count": 63
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 6376,
      "sha256": "e3745d67a12053f5438d9605ab6e5740e96ae01d91fd8cd72c03fe1990edd8b9",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_planner_json_contract_replay\",\n  \"generated_at\": \"2026-05-07T13:33:23\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json\"\n  },\n  \"source_summary\": {\n    \"kind\": \"agent_gpu_deep_planning_supervised\",\n    \"passed\": true,\n    \"round_count\": 4,\n    \"recommendation_count\": 0,\n    \"json_parse_error_count\": 0,\n    \"repair_attempt_count\": 0,\n    \"empty_recommendations_reason\": \"model_output_schema_mismatch\",\n    \"evidence_ready_for_manual_patch_count\": 0\n  },\n  \"replayed_round_count\": 4,\n  \"contract_reason_counts\": {\n    \"model_output_schema_mismatch\": 4\n  },\n  \"context_echo_detected_count\": 0,\n  \"json_parse_failure_count\": 0,\n  \"model_output_schema_mismatch_count\": 4,\n  \"valid_recommendation_output_count\": 0,\n  \"rounds\": [\n    {\n      \"round\": 1,\n      \"original_empty_recommendations_reason\": \"model_output_schema_mismatch\",\n      \"original_json_ok\": true,\n      \"original_parse_error\": \"\",\n      \"original_response_chars\": 382,\n      \"contract\": {\n        \"json_ok\": true,\n        \"schema_ok\": false,\n        \"context_echo_d",
      "preview_chars": 1500,
      "line_count": 187
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5238,
      "sha256": "60600cb5f05992f6f5bbb6b700a0312dd025899f469e59d7663ddb828c2c16c9",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_npu_run_sync_analysis\",\n  \"generated_at\": \"2026-05-07T13:33:23\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json\"\n  },\n  \"metrics\": {\n    \"gpu_round_count\": 4,\n    \"npu_audit_count\": 0,\n    \"legacy_npu_audit_count\": 0,\n    \"npu_micro_support_count\": 0,\n    \"npu_micro_support_overlap_count\": 0,\n    \"gpu0_peer_support_count\": 5,\n    \"gpu0_peer_support_overlap_count\": 4,\n    \"npu_audit_success_count\": 0,\n    \"npu_audit_round_coverage\": 0.0,\n    \"avg_gpu_round_seconds\": 15.424,\n    \"p50_gpu_round_seconds\": 15.424,\n    \"p90_gpu_round_seconds\": 15.424,\n    \"avg_npu_audit_seconds\": 0.0,\n    \"p50_npu_audit_seconds\": 0.0,\n    \"p90_npu_audit_seconds\": 0.0,\n    \"npu_to_gpu_avg_duration_ratio\": 0.0,\n    \"gpu_elapsed_seconds\": 61.694,\n    \"provider_execution_performed\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"gpu_metrics_source\": \"gpu_elapsed_divided_by_round_count\"\n  },\n  \"performance\": {\n    \"analyzer_elapsed_seconds\": 0.001,\n    \"gpu\": {\n      \"elapsed_seconds\": 61.694,\n",
      "preview_chars": 1500,
      "line_count": 140
    },
    {
      "path": "output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 6878,
      "sha256": "d687632bd553c518af22079a3c443eec227f335b58818e5aa1e9bf673d1ac5b2",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_evidence_contract\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [\n    \"local provider probe degraded: ['ollama: probe failed']\"\n  ],\n  \"provider_execution_requested\": true,\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json\",\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json\",\n    \"gpu_npu_sync\": \"output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n    \"local_provider_probe\": \"output/validation/local_provider_probe.json\",\n    \"hardware_manifest\": \"output/validation/runtime_hardware_capability_manifest.json\",\n    \"openvino_gpu0_workload\": \"output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json\"\n  },\n  \"cuda_gpu_primary_real\": true,\n  \"openvino_gpu0_secondary_real\": true,\n  \"openvino_gpu0_secondary_file_real\": true,\n  \"gpu0_peer_support_real\": true,\n  \"npu_auditor_real\": false,\n  \"npu_micro_support_real\": false,\n  \"openvino_gpu1_reserved_visible\": true,\n  \"gpu\": {\n    \"r",
      "preview_chars": 1500,
      "line_count": 213
    },
    {
      "path": "output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 8407,
      "sha256": "5e258f7d0dc0eca023e438f6fed4ad2f0b8483424d48c941bb2bf12188c85816",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu0_companion_worker_lane\",\n  \"generated_at\": \"2026-05-07T13:32:21\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"production_role\": \"companion_worker\",\n  \"production_support\": true,\n  \"provider_execution_performed\": true,\n  \"semantic_execution_mode\": \"model_unconfigured_numeric_tool_companion\",\n  \"gpu0_model_dir_configured\": false,\n  \"gpu0_model_dir\": \"\",\n  \"companion_task_count\": 4,\n  \"tool_request_count\": 4,\n  \"companion_tasks\": [\n    {\n      \"id\": \"gpu0_companion_provider_warning_triage\",\n      \"role\": \"companion_worker\",\n      \"objective\": \"Classify provider/Ollama warnings before the primary planner treats the run as green.\",\n      \"requires_semantic_model\": false\n    },\n    {\n      \"id\": \"gpu0_companion_npu_audit_precompute\",\n      \"role\": \"companion_worker\",\n      \"objective\": \"Precompute compact evidence signals that can be attached to NPU audit checkpoints.\",\n      \"requires_semantic_model\": false\n    },\n    {\n      \"id\": \"gpu0_companion_patch_plan_evidence_check\",\n      \"role\": \"companion_worker\",\n      \"objective\": \"Score whether recommendations and patch plans reference available evidence.\",\n      \"requires_semantic_model\": false\n    },\n    {\n      \"id\": \"gpu0_companion_failed_report_root_cause_scan\",\n      \"role\": \"companion_worker\",\n      \"objective\": \"Scan failed reports and produce root-cause hints for GPU1/Ollama.\",\n      \"",
      "preview_chars": 1500,
      "line_count": 210
    },
    {
      "path": "output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 498,
      "sha256": "10051f6682d6faaefcd0caa7091aad6bddd0a60bb8f41bb182f1741203fcfb87",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 3,\n  \"kind\": \"gpu0_companion_contract\",\n  \"passed\": true,\n  \"classifications\": [],\n  \"errors\": [],\n  \"requested_report\": \"output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json\",\n  \"selected_report\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json\",\n  \"selected_report_exists\": true,\n  \"candidate_count\": 1,\n  \"diagnostics\": []\n}\n",
      "preview_chars": 486,
      "line_count": 12
    },
    {
      "path": "output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1732,
      "sha256": "4a3190c637722fb097134af2c4c412a8a3795fa238810eefa1f9f2460e3afd09",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 2,\n  \"kind\": \"openvino_gpu0_secondary_workload\",\n  \"generated_at\": \"2026-05-07T13:32:25\",\n  \"provider_execution_requested\": true,\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"media_runtime_performed\": false,\n  \"openvino_gpu0_visible\": true,\n  \"openvino_gpu0_probe_performed\": true,\n  \"openvino_gpu0_workload_performed\": true,\n  \"openvino_gpu0_workload_passed\": true,\n  \"openvino_gpu0_provider_execution_performed\": true,\n  \"openvino_gpu0_role\": \"peer_support_round_000\",\n  \"openvino_gpu0_not_primary_advisory\": false,\n  \"openvino_gpu0_support_lane\": true,\n  \"openvino_gpu0_sustained_workload_requested\": true,\n  \"openvino_gpu0_sustained_workload_performed\": true,\n  \"openvino_gpu0_sustained_iterations_requested\": 24,\n  \"openvino_gpu0_sustained_iterations_performed\": 8012,\n  \"openvino_gpu0_sustained_min_seconds_requested\": 1.0,\n  \"openvino_gpu1_reserved_visible\": true,\n  \"openvino_gpu1_workload_performed\": false,\n  \"openvino_gpu1_openvino_workload_allowed\": false,\n  \"openvino_gpu1_role\": \"reserved_for_cuda_ollama\",\n  \"selected_device\": \"GPU.0\",\n  \"available_devices\": [\n    \"CPU\",\n    \"GPU.0\",\n    \"GPU.1\",\n    \"NPU\"\n  ],\n  \"elapsed_seconds\": 1.918213,\n  \"compile_seconds\": 0.034811,\n  \"inference_seconds\": 1.00004,\n  \"output_preview\": \"[1.0, 1.0, 1.0, 1.0]\",\n  \"errors\": [],\n  \"warnings\": [\n    \"OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.\"\n  ],\n  \"passed\": true,\n  ",
      "preview_chars": 1500,
      "line_count": 48
    },
    {
      "path": "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1478,
      "sha256": "91fb22ea23f2aa504ce5cb2b0b779f9cd1ef0d9739962a5ab96eac537128caff",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu1_primary_advisory\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"role\": \"gpu1_master_planner_worker\",\n  \"lane\": \"GPU1/Ollama/RTX5080\",\n  \"passed\": true,\n  \"provider_execution_performed\": true,\n  \"gpu_report\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json\",\n  \"gpu_markdown\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.md\",\n  \"gpu_report_exists\": true,\n  \"round_count\": 4,\n  \"recommendation_count\": 0,\n  \"runtime_tool_request_count\": 8,\n  \"runtime_tool_execution_count\": 0,\n  \"provider_empty_response\": false,\n  \"classification\": \"\",\n  \"classifications\": [],\n  \"errors\": [],\n  \"warnings\": [],\n  \"recommendations_preview\": [],\n  \"decision\": {\n    \"ready_for_patch_plan\": false,\n    \"ready_count\": 0,\n    \"needs_more_context_count\": 0,\n    \"fallback_patch_plan_recommended\": false,\n    \"npu_auditor_non_blocking\": true,\n    \"npu_unusable_or_failed_count\": 0,\n    \"npu_audit_success_count\": 0,\n    \"npu_auditor_disabled_reason\": \"\",\n    \"recommended_next_layer\": \"collect_more_evidence\",\n    \"manual_review_required\": true\n  },\n  \"guardrails\": {\n    \"report_only\": true,\n    \"gpu1_reserved_for_primary_ollama\": true,\n    \"openvino_gpu1_workload_allowed\": false,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false\n  }\n}\n",
```

## Context after

      "preview_chars": 1436,
      "line_count": 42
    },
    {
      "path": "output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 6134,
      "sha256": "4d8ea71966046beef522765af9fb07c4280ecf9b80397075fd32e72771adefe8",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu0_peer_task_packet\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"source_lane\": \"gpu1_master_primary_advisory_worker\",\n  \"target_lane\": \"gpu0_openvino_peer_worker\",\n  \"passed\": true,\n  \"primary_advisory_report\": \"output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json\",\n  \"task_count\": 4,\n  \"tasks\": [\n    {\n      \"id\": \"gpu0_peer_primary_advisory_quality\",\n      \"role\": \"companion_peer_worker\",\n      \"objective\": \"Verify whether GPU1/Ollama planned and worked on usable primary advisory evidence.\",\n      \"requires_semantic_model\": false\n    },\n    {\n      \"id\": \"gpu0_peer_runtime_tool_context\",\n      \"role\": \"companion_peer_worker\",\n      \"objective\": \"Request broker-controlled deterministic tool evidence for GPU1 planner follow-up.\",\n      \"requires_semantic_model\": false\n    },\n    {\n      \"id\": \"gpu0_peer_patch_spec_readiness\",\n      \"role\": \"companion_peer_worker\",\n      \"objective\": \"Check whether recommendations, patch specs and validation evidence can support a review-only patch proposal.\",\n      \"requires_semantic_model\": false\n    },\n    {\n      \"id\": \"gpu0_peer_failed_report_triage\",\n      \"role\": \"companion_peer_worker\",\n      \"objective\": \"Triage failed deterministic reports and return compact blockers for GPU1.\",\n      \"requires_semantic_model\": false\n    }\n  ],\n  \"tool_request_templates\": [\n    {\n      \"id\": \"gpu0_peer_code_interpreter_",
