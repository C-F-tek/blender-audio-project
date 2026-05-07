# Evidence Chunk 0014/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `1999`
- line_end: `2070`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0013.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0015.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "preview_chars": 1500, "line_count": 55 }, { "path": "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json", "exists": true, "suffix": ".json", "size_bytes": 7017, "sha256": "3e58bb12829011d743a91981c1a900e41d456a4a684177155eb5e787d...

## Context before

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

## Chunk content

```json
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
      "preview_chars": 1500,
      "line_count": 203
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 2286,
      "sha256": "ed28bc60125e4c67871907ec8c521bdf5e11d53c4ce2aa99e021a4bc8ce40bbc",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_telemetry\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"event_count\": 32,\n  \"parse_error_count\": 0,\n  \"lanes_observed\": [\n    \"broker\",\n    \"deterministic\",\n    \"gpu0\",\n    \"gpu1\",\n    \"npu\",\n    \"orchestrator\"\n  ],\n  \"events_by_lane\": {\n    \"broker\": 6,\n    \"deterministic\": 1,\n    \"gpu0\": 13,\n    \"gpu1\": 2,\n    \"npu\": 2,\n    \"orchestrator\": 8\n  },\n  \"events_by_type\": {\n    \"broker_request\": 6,\n    \"broker_result\": 6,\n    \"evidence_request\": 7,\n    \"evidence_response\": 9,\n    \"provider_state\": 3,\n    \"validation_signal\": 1\n  },\n  \"interaction_edges\": {\n    \"broker->gpu0:broker_result\": 6,\n    \"deterministic->gpu1:validation_signal\": 1,\n    \"gpu0->broker:broker_request\": 6,\n    \"gpu0->gpu1:evidence_response\": 7,\n    \"gpu1->gpu0:evidence_request\": 2,\n    \"npu->gpu1:evidence_response\": 2,\n    \"orchestrator->gpu0:evidence_request\": 5,\n    \"orchestrator->none:provider_state\": 3\n  },\n  \"tool_catalog_exchange_complete_count\": 0,\n  \"gpu1_to_gpu0_event_count\": 2,\n  \"gpu0_to_gpu1_event_count\": 7,\n  \"gpu1_gpu0_bidirectional\": true,\n  \"gpu1_gpu0_correlated_exchange_count\": 2,\n  \"gpu1_gpu0_request_event_types\": [\n    \"evidence_request\"\n  ],\n  \"gpu1_gpu0_response_event_types\": [\n    \"evidence_response\"\n  ],\n  \"broker_request_count\": 6,\n  \"broker_result_count\": 6,\n  \"pending_broker_request_count\": 0,\n  \"validation_signal_coun",
      "preview_chars": 1500,
      "line_count": 79
    },
    {
      "path": "output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5705,
      "sha256": "95f2ca23fe4dba8997ba61daf611ff0426764bc659cbda224e25d3d217b5881c",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n    \"schema_version\":  1,\n    \"kind\":  \"full_memory_tool_regeneration_workflow\",\n    \"generated_at\":  \"2026-05-07T13:31:44\",\n    \"repo_root\":  \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n    \"stamp\":  \"patch_quality_product_probe_20260507-133119\",\n    \"profile\":  \"full_refactor\",\n    \"objective\":  \"Reload IA-Carmine full toolbox context before agent review full toolbox decision-loop run.\",\n    \"passed\":  true,\n    \"errors\":  [\n\n               ],\n    \"warnings\":  [\n\n                 ],\n    \"provider_execution_performed\":  false,\n    \"patch_application_performed\":  false,\n    \"source_writes_performed\":  false,\n    \"sqlite_write_performed\":  false,\n    \"persistent_memory_write_performed\":  false,\n    \"operational_sqlite_write_allowed_under_output\":  true,\n    \"report_count\":  13,\n    \"artifact_count\":  14,\n    \"reports\":  [\n                    \".\\\\output\\\\ai_pipeline\\\\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agent_memory_inventory.json\",\n                    \".\\\\output\\\\ai_pipeline\\\\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agnostic_tool_inventory.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_persistent_memory_status.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_operational_memory_status.json\",\n                    \".\\\\output\\\\validation\\\\full_memory_t",
      "preview_chars": 1500,
      "line_count": 67
    },
    {
      "path": "output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 1649,
      "sha256": "5b219e03048da09b4da4299d4bc1183c56709bf550a133bc509a17d9f041e4b8",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"provider_runtime_heap_from_peer_reports\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"stamp\": \"patch_quality_product_probe_20260507-133119\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"event_count\": 11,\n  \"heap_snapshot\": {\n    \"event_count\": 32,\n    \"pending_broker_request_count\": 0,\n    \"event_log\": \"output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl\"\n  },\n  \"reports\": {\n    \"gpu1\": \"output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json\",\n    \"gpu0\": \"output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json\",\n    \"gpu0_tool_requests\": \"output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json\",\n    \"gpu0_broker\": \"output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json\",\n    \"npu\": \"output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json\",\n    \"npu_broker\": \"output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json\",\n    \"peer_exchange\": \"output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json\",\n    \"peer_contract\": \"output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json\"\n  },\n  \"guardrails\": {\n    \"provider_execution_performed\": false,\n    \"direct_tool_execution_allowed\": false,\n    \"broker_required_for_tool_execution\": true,\n   ",
      "preview_chars": 1500,
      "line_count": 33
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 23363,
      "sha256": "cac140fc1f09e52a24a32e30f879ff78ca40a749b05748b5a666e8c94ed2d57a",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"patch_plan_quality_product_gate\",\n  \"generated_at\": \"2026-05-07T13:33:34\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"quality_gate_passed\": true,\n  \"classification\": \"ready_for_manual_patch_review\",\n  \"non_blocking\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"quality_findings\": [],\n  \"fallback_path_notes\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"operational_sqlite_fts_write_performed\": true,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"paths\": {\n      \"patch_plan\": \"output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json\",\n      \"decision_loop\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json\",\n      \"recommendations\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json\",\n      \"runtime_usage\": \"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json\",\n      \"runtime_capability\": \"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.json\",\n      \"repository_consistency\": \"output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe",
      "preview_chars": 1500,
      "line_count": 606
    },
    {
      "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 379334,
      "sha256": "8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"kind\": \"full0to10_final_tool_product_manifest\",\n  \"passed\": true,\n  \"request\": \"Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.\",\n  \"outputs\": {\n    \"product_markdown\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product.md\",\n    \"evidence_index\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_evidence_index.json\",\n    \"readiness\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_readiness.json\",\n    \"manifest\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json\",\n    \"readme\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/README.md\",\n    \"track_input_contract\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_contract.json\",\n    \"provider_execution_bridge\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.json\"\n  },\n  \"evidence\": {\n    \"kind\": \"full0to10_final_tool_product_evidence_index\",\n    \"generated_at\": \"2026-",
```

## Context after

      "preview_chars": 1500,
      "line_count": 9371
    },
    {
      "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 379334,
      "sha256": "8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"kind\": \"full0to10_final_tool_product_manifest\",\n  \"passed\": true,\n  \"request\": \"Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.\",\n  \"outputs\": {\n    \"product_markdown\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product.md\",\n    \"evidence_index\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_evidence_index.json\",\n    \"readiness\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_readiness.json\",\n    \"manifest\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json\",\n    \"readme\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/README.md\",\n    \"track_input_contract\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_contract.json\",\n    \"provider_execution_bridge\": \"output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.json\"\n  },\n  \"evidence\": {\n    \"kind\": \"full0to10_final_tool_product_evidence_index\",\n    \"generated_at\": \"2026-",
