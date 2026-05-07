# Evidence Chunk 0005/0006

- source: `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `3cce74c9364d7286ae6f1e61befb2b62211f0ab5de6182a5aaa6fe4f09a5097c`
- line_start: `602`
- line_end: `922`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/ai_peer_exchange_patch_quality_product_probe_20260507-133119_json_3cce74c9364d_chunk_0004.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/ai_peer_exchange_patch_quality_product_probe_20260507-133119_json_3cce74c9364d_chunk_0006.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: classification; provider_execution_requested; provider_execution_performed; provider_execution_succeeded; provider_empty_response. Preview: "classification": "npu_peer_provider_deferred_to_avoid_openvino_contention", "provider_execution_requested": false, "provider_execution_performed": false, "provider_execution_succeeded": false, "provider_empty_response": false, "non_blocking": true, "deferred_...

## Context before

      "operational_memory_clear_count": 0,
      "blender_runtime_touched": false,
      "git_write_performed": false,
      "manual_review_required": true
    }
  },
  "npu_micro_response": {
    "schema_version": 1,
    "kind": "npu_micro_peer_assistant",
    "generated_at": "2026-05-07T13:33:29",
    "stamp": "patch_quality_product_probe_20260507-133119",
    "passed": true,

## Chunk content

```json
    "classification": "npu_peer_provider_deferred_to_avoid_openvino_contention",
    "provider_execution_requested": false,
    "provider_execution_performed": false,
    "provider_execution_succeeded": false,
    "provider_empty_response": false,
    "non_blocking": true,
    "deferred_to_avoid_openvino_contention": true,
    "npu_micro_start_mode": "deferred",
    "reason": "NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.",
    "tool_request_count": 0,
    "tool_requests": [],
    "npu_deterministic_tool_fallback_used": false,
    "npu_deterministic_tool_fallback_count": 0,
    "runtime_tool_context_seen": true,
    "runtime_tool_context_report_count": 4,
    "warnings": [
      "NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence."
    ],
    "errors": [],
    "decision": {
      "npu_primary_advisory": false,
      "manual_review_required": true,
      "product_pass_blocker": false,
      "deferred_to_avoid_openvino_contention": true
    },
    "guardrails": {
      "report_only": true,
      "npu_micro_lane_non_blocking": true,
      "npu_primary_advisory": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    }
  },
  "npu_runtime_tool_broker": {
    "schema_version": 1,
    "kind": "agent_runtime_tool_broker",
    "generated_at": "2026-05-07T13:33:29",
    "stamp": "patch_quality_product_probe_20260507-133119",
    "passed": true,
    "executed": false,
    "classification": "npu_peer_provider_deferred_noop_broker",
    "enabled": false,
    "requested_tool_count": 0,
    "tool_request_count": 0,
    "tool_execution_count": 0,
    "failed_tool_count": 0,
    "blocked_tool_count": 0,
    "tool_results": [],
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "persistent_memory_write_performed": false,
    "warnings": [
      "NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence."
    ],
    "errors": [],
    "guardrails": {
      "report_only": true,
      "noop_broker_for_deferred_npu_peer": true,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    }
  },
  "collaboration_round": {
    "kind": "ai_peer_collaboration_round",
    "synchronized_visibility": true,
    "gpu1": {
      "role": "gpu1_master_planner_worker",
      "works_and_plans": true,
      "sees_gpu0_response": true,
      "sees_gpu0_broker_results": true,
      "sees_npu_micro_signal": true
    },
    "gpu0": {
      "role": "gpu0_companion_tool_request_producer",
      "provider_execution_performed": true,
      "produces_tool_requests": true,
      "broker_tool_executions": 3
    },
    "npu": {
      "role": "npu_support_tool_micro_lane_non_blocking",
      "non_blocking": true,
      "report_seen": true,
      "provider_execution_requested": false,
      "provider_execution_performed": false,
      "tool_request_count": 0,
      "broker_tool_executions": 0
    },
    "deterministic_scripts": {
      "role": "tool_agnostic_heavy_audit_and_validation_authority",
      "source_report_count": 5
    },
    "runtime_tool_broker": {
      "role": "controlled_tool_execution_for_gpu1_gpu0_npu_requests",
      "gpu0_tool_execution_count": 3,
      "npu_tool_execution_count": 0
    },
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
    },
    "peer_mesh_lane_state": {
      "schema_version": 1,
      "kind": "peer_mesh_lane_state",
      "operational_lanes": [
        "gpu1_ollama_primary_advisory",
        "gpu0_openvino_peer_companion",
        "runtime_tool_broker",
        "deterministic_scripts",
        "npu_nonblocking_tool_support"
      ],
      "support_lanes": [
        "gpu0_openvino_numeric_tool_peer",
        "gpu0_brokered_tool_supply"
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
    }
  },
  "peer_mesh_visibility": {
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
  },
  "peer_mesh_lane_state": {
    "schema_version": 1,
    "kind": "peer_mesh_lane_state",
    "operational_lanes": [
      "gpu1_ollama_primary_advisory",
      "gpu0_openvino_peer_companion",
      "runtime_tool_broker",
      "deterministic_scripts",
      "npu_nonblocking_tool_support"
    ],
    "support_lanes": [
      "gpu0_openvino_numeric_tool_peer",
      "gpu0_brokered_tool_supply"
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
```

## Context after

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
