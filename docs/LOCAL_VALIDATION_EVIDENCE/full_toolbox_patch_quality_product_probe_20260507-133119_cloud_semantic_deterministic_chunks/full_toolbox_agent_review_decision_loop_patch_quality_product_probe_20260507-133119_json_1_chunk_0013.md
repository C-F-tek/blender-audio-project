# Evidence Chunk 0013/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `1936`
- line_end: `1998`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0012.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0014.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "role": "local_artifact_reference", "content_included": true, "preview": "{\n \"schema_version\": 1,\n \"kind\": \"ai_peer_exchange\",\n \"generated_at\": \"2026-05-07T13:33:30\",\n \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n \"passed\": true...

## Context before

      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_runtime_tool_broker\",\n  \"generated_at\": \"2026-05-07T13:33:29\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"passed\": true,\n  \"executed\": false,\n  \"classification\": \"npu_peer_provider_deferred_noop_broker\",\n  \"enabled\": false,\n  \"requested_tool_count\": 0,\n  \"tool_request_count\": 0,\n  \"tool_execution_count\": 0,\n  \"failed_tool_count\": 0,\n  \"blocked_tool_count\": 0,\n  \"tool_results\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"warnings\": [\n    \"NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.\"\n  ],\n  \"errors\": [],\n  \"guardrails\": {\n    \"report_only\": true,\n    \"noop_broker_for_deferred_npu_peer\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"persistent_memory_write_performed\": false\n  }\n}\n",
      "preview_chars": 979,
      "line_count": 31
    },
    {
      "path": "output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 61320,
      "sha256": "3cce74c9364d7286ae6f1e61befb2b62211f0ab5de6182a5aaa6fe4f09a5097c",

## Chunk content

```json
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"ai_peer_exchange\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"passed\": true,\n  \"primary_advisory\": {\n    \"schema_version\": 1,\n    \"kind\": \"gpu1_primary_advisory\",\n    \"generated_at\": \"2026-05-07T13:33:30\",\n    \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n    \"role\": \"gpu1_master_planner_worker\",\n    \"lane\": \"GPU1/Ollama/RTX5080\",\n    \"passed\": true,\n    \"provider_execution_performed\": true,\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json\",\n    \"gpu_markdown\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.md\",\n    \"gpu_report_exists\": true,\n    \"round_count\": 4,\n    \"recommendation_count\": 0,\n    \"runtime_tool_request_count\": 8,\n    \"runtime_tool_execution_count\": 0,\n    \"provider_empty_response\": false,\n    \"classification\": \"\",\n    \"classifications\": [],\n    \"errors\": [],\n    \"warnings\": [],\n    \"recommendations_preview\": [],\n    \"decision\": {\n      \"ready_for_patch_plan\": false,\n      \"ready_count\": 0,\n      \"needs_more_context_count\": 0,\n      \"fallback_patch_plan_recommended\": false,\n      \"npu_auditor_non_blocking\": true,\n      \"npu_unusable_or_failed_count\": 0,\n      \"npu_audit_success_count\": 0,\n      \"npu_auditor_disabled_reason\": \"\",\n      \"recommended_next_layer\": \"collect_more_evidence\",\n      \"manual_review_required\": true\n    },\n    \"guardrails\": {\n   ",
      "preview_chars": 1500,
      "line_count": 1067
    },
    {
      "path": "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 13421,
      "sha256": "3a2b21b1931640a86731d9b66e4dfb3990f336f7c129b64ee4c2aa12745c380c",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"ai_peer_exchange_contract\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"classifications\": [\n    \"peer_mesh_degraded_lanes_present_non_blocking\",\n    \"gpu0_peer_semantic_model_unconfigured\"\n  ],\n  \"errors\": [],\n  \"warnings\": [\n    \"gpu0_peer_semantic_model_unconfigured\"\n  ],\n  \"peer_mesh_visibility_contract\": {\n    \"passed\": true,\n    \"mesh_visibility\": {\n      \"schema_version\": 1,\n      \"kind\": \"ai_peer_mesh_visibility\",\n      \"all_lanes_visible\": true,\n      \"gpu1_sees_gpu0_response\": true,\n      \"gpu1_sees_gpu0_broker_results\": true,\n      \"gpu1_sees_npu_support_signal\": true,\n      \"gpu1_sees_npu_broker_results\": false,\n      \"gpu0_sees_gpu1_primary_advisory\": true,\n      \"gpu0_sees_deterministic_reports\": true,\n      \"gpu0_produces_tool_requests_for_gpu1\": true,\n      \"gpu0_tool_requests_broker_consumed\": true,\n      \"npu_sees_gpu1_gpu0_broker_context\": true,\n      \"npu_support_tool_requests_available\": false,\n      \"npu_tool_requests_broker_consumed\": false,\n      \"deterministic_scripts_visible_to_gpu0\": true,\n      \"runtime_tool_broker_visible_to_all_lanes\": true,\n      \"npu_non_blocking_support_lane\": true\n    },\n    \"npu_support_lane\": {\n      \"role\": \"npu_non_blocking_tool_support_lane\",\n      \"non_blocking\": true,\n      \"blocking\": false,\n      \"heavy_audit_authority\": false,\n      \"tool_su",
      "preview_chars": 1500,
      "line_count": 388
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1573,
      "sha256": "1840556765c20798786d42e18a8a54fb008db352e19fb3576a0cc1f855ec4053",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_live_signals\",\n  \"generated_at\": \"2026-05-07T13:31:19\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"mode\": \"init\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"event_count\": 1,\n  \"events\": [\n    {\n      \"schema_version\": 1,\n      \"kind\": \"provider_runtime_event\",\n      \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n      \"created_at\": \"2026-05-07T13:31:19\",\n      \"source\": \"orchestrator\",\n      \"target\": null,\n      \"round\": null,\n      \"event_type\": \"provider_state\",\n      \"correlation_id\": \"patch_quality_product_probe_20260507-133119:live-runtime-heap\",\n      \"payload\": {\n        \"state\": \"live_runtime_heap_initialized\",\n        \"mode\": \"init\",\n        \"direct_execution\": false,\n        \"broker_required\": true\n      },\n      \"guardrails\": {\n        \"provider_execution_performed\": false,\n        \"direct_tool_execution_allowed\": false,\n        \"broker_required_for_tool_execution\": true,\n        \"patch_application_performed\": false,\n        \"source_writes_performed\": false\n      }\n    }\n  ],\n  \"heap_snapshot\": {\n    \"event_count\": 1,\n    \"pending_broker_request_count\": 0,\n    \"event_log\": \"output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl\"\n  },\n  \"guardrails\": {\n    \"provider_execution_performed\": false,\n    \"direct_tool_execution_allowed\": false,\n    \"broker_required_for_tool_execution\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_",
      "preview_chars": 1500,
      "line_count": 49
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1962,
      "sha256": "6061e3c5388342478f4a2873b6ea004da9ade66122453887442d021ba9286ba2",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_live_signals\",\n  \"generated_at\": \"2026-05-07T13:33:23\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"mode\": \"gpu1-request\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"event_count\": 1,\n  \"events\": [\n    {\n      \"schema_version\": 1,\n      \"kind\": \"provider_runtime_event\",\n      \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n      \"created_at\": \"2026-05-07T13:33:23\",\n      \"source\": \"gpu1\",\n      \"target\": \"gpu0\",\n      \"round\": 1,\n      \"event_type\": \"evidence_request\",\n      \"correlation_id\": \"patch_quality_product_probe_20260507-133119:gpu1-gpu0-live-evidence\",\n      \"payload\": {\n        \"objective\": \"GPU1 primary advisory requests live coworker evidence from GPU0 before GPU0 execution.\",\n        \"gpu1_report\": \"output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json\",\n        \"gpu0_task_packet\": \"output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json\",\n        \"gpu1_passed\": true,\n        \"gpu1_provider_execution_performed\": true,\n        \"task_count\": 4,\n        \"direct_execution\": false,\n        \"broker_required\": true\n      },\n      \"guardrails\": {\n        \"provider_execution_performed\": false,\n        \"direct_tool_execution_allowed\": false,\n        \"broker_required_for_tool_execution\": true,\n        \"patch_application_performed\": false,\n        \"source_writes_performed\": false\n      }\n    }\n  ],\n  \"heap_snapshot",
      "preview_chars": 1500,
      "line_count": 53
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 4810,
      "sha256": "bca07ed298311198245f37602e34fc904c0d54818833cc1828d94a079fa6e486",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_live_signals\",\n  \"generated_at\": \"2026-05-07T13:33:29\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"mode\": \"broker-results\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"event_count\": 3,\n  \"events\": [\n    {\n      \"schema_version\": 1,\n      \"kind\": \"provider_runtime_event\",\n      \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n      \"created_at\": \"2026-05-07T13:33:29\",\n      \"source\": \"broker\",\n      \"target\": \"gpu0\",\n      \"round\": 1,\n      \"event_type\": \"broker_result\",\n      \"correlation_id\": \"gpu0_peer_code_interpreter_context\",\n      \"payload\": {\n        \"request_id\": \"gpu0_peer_code_interpreter_context\",\n        \"tool\": \"build_code_interpreter_report\",\n        \"executed\": true,\n        \"blocked\": false,\n        \"returncode\": 0,\n        \"outputs\": {\n          \"json_report\": \"output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.json\",\n          \"markdown_report\": \"output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.md\"\n        },\n        \"errors\": [],\n        \"warnings\": [],\n        \"broker_report\": \"output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json\"\n      },\n      \"guardrails\": {\n        \"provider_execution_performed\": false,\n        \"direct_tool_execution_allowed\": fa",
      "preview_chars": 1500,
      "line_count": 120
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1931,
      "sha256": "6292db52e34610b1d59d3b9b25e21e1e285b73655091926e91022f4953013adb",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_live_signals\",\n  \"generated_at\": \"2026-05-07T13:33:29\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"mode\": \"npu-support\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"event_count\": 1,\n  \"events\": [\n    {\n      \"schema_version\": 1,\n      \"kind\": \"provider_runtime_event\",\n      \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n      \"created_at\": \"2026-05-07T13:33:29\",\n      \"source\": \"npu\",\n      \"target\": \"gpu1\",\n      \"round\": 1,\n      \"event_type\": \"evidence_response\",\n      \"correlation_id\": \"patch_quality_product_probe_20260507-133119:npu-live-support\",\n      \"payload\": {\n        \"summary\": \"NPU micro/support lane published live support evidence to GPU1.\",\n        \"npu_report\": \"output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json\",\n        \"npu_passed\": true,\n        \"provider_execution_requested\": false,\n        \"provider_execution_performed\": false,\n        \"non_blocking\": true,\n        \"tool_request_count\": 0,\n        \"product_pass_blocker\": null,\n        \"direct_execution\": false,\n        \"broker_required\": true\n      },\n      \"guardrails\": {\n        \"provider_execution_performed\": false,\n        \"direct_tool_execution_allowed\": false,\n        \"broker_required_for_tool_execution\": true,\n        \"patch_application_performed\": false,\n        \"source_writes_performed\": false\n      }\n    }\n  ],\n  \"heap_snapshot\": {\n    \"event_count\": 21,\n    \"",
```

## Context after

      "preview_chars": 1500,
      "line_count": 55
    },
    {
      "path": "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 7017,
      "sha256": "3e58bb12829011d743a91981c1a900e41d456a4a684177155eb5e787d142888a",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_snapshot\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"event_log\": \"output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl\",\n  \"event_count\": 32,\n  \"parse_error_count\": 0,\n  \"by_lane\": {\n    \"orchestrator\": {\n      \"event_count\": 8,\n      \"latest_event_at\": \"2026-05-07T13:33:30\",\n      \"event_types\": {\n        \"provider_state\": 3,\n        \"evidence_request\": 5\n      }\n    },\n    \"gpu0\": {\n      \"event_count\": 13,\n      \"latest_event_at\": \"2026-05-07T13:33:30\",\n      \"event_types\": {\n        \"evidence_response\": 7,\n        \"broker_request\": 6\n      }\n    },\n    \"gpu1\": {\n      \"event_count\": 2,\n      \"latest_event_at\": \"2026-05-07T13:33:30\",\n      \"event_types\": {\n        \"evidence_request\": 2\n      }\n    },\n    \"broker\": {\n      \"event_count\": 6,\n      \"latest_event_at\": \"2026-05-07T13:33:30\",\n      \"event_types\": {\n        \"broker_result\": 6\n      }\n    },\n    \"npu\": {\n      \"event_count\": 2,\n      \"latest_event_at\": \"2026-05-07T13:33:30\",\n      \"event_types\": {\n        \"evidence_response\": 2\n      }\n    },\n    \"deterministic\": {\n      \"event_count\": 1,\n      \"latest_event_at\": \"2026-05-07T13:33:30\",\n      \"event_types\": {\n        \"validation_signal\": 1\n      }\n    }\n  },\n  \"by_event_type\": {\n    \"provider_state\": 3,\n    \"evidence_request\": 7,\n    \"evidence_response\": 9,\n    \"broker_request\": 6,\n    \"broker_result\": 6,\n    \"validation_s",
