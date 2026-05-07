# Evidence Chunk 0006/0006

- source: `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `3cce74c9364d7286ae6f1e61befb2b62211f0ab5de6182a5aaa6fe4f09a5097c`
- line_start: `923`
- line_end: `1067`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/ai_peer_exchange_patch_quality_product_probe_20260507-133119_json_3cce74c9364d_chunk_0005.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: mesh_visibility; npu_support_lane; provider_broker_loop; schema_version; active. Preview: "mesh_visibility": { "schema_version": 1, "kind": "ai_peer_mesh_visibility", "all_lanes_visible": true, "gpu1_sees_gpu0_response": true, "gpu1_sees_gpu0_broker_results": true, "gpu1_sees_npu_support_signal": true, "gpu1_sees_npu_broker_results": false, "gpu0_s...

## Context before

    ],
    "degraded_lanes": [
      "gpu0_semantic_companion_model_unconfigured"
    ],
    "product_blockers": [],
    "gpu0_broker_tool_execution_count": 3,
    "npu_broker_tool_execution_count": 0,
    "broker_runtime_tool_execution_count": 3,
    "legacy_usable_lanes_are_workload_quality_only": true,
    "npu_degraded_is_product_blocker": false,
    "npu_heavy_audit_authority": false,
    "all_required_product_lanes_present": true,

## Chunk content

```json
    "mesh_visibility": {
      "schema_version": 1,
      "kind": "ai_peer_mesh_visibility",
      "all_lanes_visible": true,
      "gpu1_sees_gpu0_response": true,
      "gpu1_sees_gpu0_broker_results": true,
      "gpu1_sees_npu_support_signal": true,
      "gpu1_sees_npu_broker_results": false,
      "gpu0_sees_gpu1_primary_advisory": true,
      "gpu0_sees_deterministic_reports": true,
      "gpu0_produces_tool_requests_for_gpu1": true,
      "gpu0_tool_requests_broker_consumed": true,
      "npu_sees_gpu1_gpu0_broker_context": true,
      "npu_support_tool_requests_available": false,
      "npu_tool_requests_broker_consumed": false,
      "deterministic_scripts_visible_to_gpu0": true,
      "runtime_tool_broker_visible_to_all_lanes": true,
      "npu_non_blocking_support_lane": true
    },
    "npu_support_lane": {
      "role": "npu_non_blocking_tool_support_lane",
      "non_blocking": true,
      "blocking": false,
      "heavy_audit_authority": false,
      "tool_supply_support": false,
      "tool_request_count": 0,
      "broker_tool_execution_count": 0,
      "provider_execution_requested": false,
      "provider_execution_performed": false,
      "provider_slow_or_degraded": false,
      "classification": "npu_peer_provider_deferred_to_avoid_openvino_contention",
      "deterministic_fallback_used": false,
      "product_pass_blocker": false
    }
  },
  "provider_broker_loop": {
    "schema_version": 1,
    "kind": "provider_broker_loop",
    "active": true,
    "topology": "input_md -> deterministic_baseline -> GPU1 -> GPU0 -> broker -> NPU_support -> broker -> contract -> telemetry -> bundle -> patch_plan",
    "controlled_executor": "runtime_tool_broker",
    "direct_tool_execution_allowed": false,
    "provider_lanes": {
      "gpu1": "primary_advisory_planner_worker",
      "gpu0": "openvino_peer_companion_tool_request_producer",
      "npu": "nonblocking_micro_tool_support_lane"
    },
    "broker_tool_execution_count": 3,
    "gpu0_broker_tool_execution_count": 3,
    "npu_broker_tool_execution_count": 0,
    "gpu0_tool_request_count": 3,
    "npu_tool_request_count": 0,
    "npu_non_blocking": true,
    "npu_product_pass_blocker": false,
    "deterministic_scripts_heavy_audit_authority": true,
    "product_pass_blockers": [],
    "loop_steps": [
      {
        "id": "deterministic_baseline",
        "from": "input_md_and_static_scripts",
        "to": "gpu1_primary_advisory",
        "performed": true
      },
      {
        "id": "gpu1_primary_advisory",
        "from": "GPU1/Ollama/RTX5080",
        "to": "GPU0/OpenVINO peer task packet",
        "performed": true
      },
      {
        "id": "gpu0_peer_response",
        "from": "GPU0/OpenVINO",
        "to": "runtime broker",
        "performed": true
      },
      {
        "id": "gpu0_broker_execution",
        "from": "runtime broker",
        "to": "GPU1/GPU0 read-only context",
        "performed": true
      },
      {
        "id": "npu_nonblocking_support",
        "from": "NPU/OpenVINO micro support lane",
        "to": "runtime broker",
        "performed": false,
        "blocking": false
      },
      {
        "id": "npu_broker_execution",
        "from": "runtime broker",
        "to": "final peer exchange context",
        "performed": false,
        "blocking": false
      },
      {
        "id": "contract_telemetry_bundle",
        "from": "deterministic validators",
        "to": "patch bundle/evidence handoff",
        "performed": true
      }
    ]
  },
  "provider_broker_loop_active": true,
  "peer_mesh_operational_lanes": [
    "gpu1_ollama_primary_advisory",
    "gpu0_openvino_peer_companion",
    "runtime_tool_broker",
    "deterministic_scripts",
    "npu_nonblocking_tool_support"
  ],
  "peer_mesh_support_lanes": [
    "gpu0_openvino_numeric_tool_peer",
    "gpu0_brokered_tool_supply"
  ],
  "peer_mesh_degraded_lanes": [
    "gpu0_semantic_companion_model_unconfigured"
  ],
  "peer_mesh_product_blockers": [],
  "contract": {},
  "classifications": [
    "gpu0_peer_semantic_model_unconfigured"
  ],
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "paths": {
    "primary_advisory": "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json",
    "task_packet": "output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json",
    "gpu0_response": "output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json",
    "gpu0_runtime_tool_broker": "output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
    "npu_micro_response": "output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json",
    "npu_runtime_tool_broker": "output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
    "contract": ""
  },
  "guardrails": {
    "report_only": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "openvino_gpu1_workload_allowed": false,
    "npu_micro_lane_non_blocking": true
  }
}
```
