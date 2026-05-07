# Evidence Chunk 0003/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `455`
- line_end: `773`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0002.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0004.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports. Preview: "exists": true, "json_ok": true, "kind": "gpu0_peer_task_packet", "passed": true, "summary": { "schema_version": 1, "kind": "gpu0_peer_task_packet", "passed": true, "provider_execution_performed": null, "patch_application_performed": null, "source_writes_perfo...

## Context before

        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": [],
        "recommendation_count": 0,
        "round_count": 4
      }
    },
    {
      "path": "output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json",

## Chunk content

```json
      "exists": true,
      "json_ok": true,
      "kind": "gpu0_peer_task_packet",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu0_peer_task_packet",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu0_peer_response",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu0_peer_response",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": [
          "IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only."
        ]
      }
    },
    {
      "path": "output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu0_peer_tool_requests",
      "passed": null,
      "summary": {
        "schema_version": 1,
        "kind": "gpu0_peer_tool_requests",
        "passed": null,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_runtime_tool_broker",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_runtime_tool_broker",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_micro_peer_assistant",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "npu_micro_peer_assistant",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": [
          "NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence."
        ]
      }
    },
    {
      "path": "output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_runtime_tool_broker",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_runtime_tool_broker",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [
          "NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence."
        ]
      }
    },
    {
      "path": "output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "ai_peer_exchange",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "ai_peer_exchange",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
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
        "provider_broker_loop_active": true,
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
        }
      }
    },
    {
      "path": "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "ai_peer_exchange_contract",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "ai_peer_exchange_contract",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [
          "gpu0_peer_semantic_model_unconfigured"
        ],
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
```

## Context after

            "provider_slow_or_degraded": false,
            "classification": "npu_peer_provider_deferred_to_avoid_openvino_contention",
            "deterministic_fallback_used": false,
            "product_pass_blocker": false
          }
        }
      }
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
