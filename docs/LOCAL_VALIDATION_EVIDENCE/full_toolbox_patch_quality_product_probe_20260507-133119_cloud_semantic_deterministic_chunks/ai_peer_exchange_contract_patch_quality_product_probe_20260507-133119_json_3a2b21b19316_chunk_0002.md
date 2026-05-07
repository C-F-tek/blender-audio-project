# Evidence Chunk 0002/0002

- source: `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `3a2b21b1931640a86731d9b66e4dfb3990f336f7c129b64ee4c2aa12745c380c`
- line_start: `276`
- line_end: `388`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119_json_3a2b21b19316_chunk_0001.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: evidence; guardrails; report_only; gpu1_primary_advisory_required; gpu0_peer_response_required. Preview: "evidence": [ { "name": "gpu1_primary_advisory", "path": "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json", "exists": true, "error": "", "kind": "gpu1_primary_advisory", "passed": true, "provider_execution_performed": t...

## Context before

      },
      {
        "id": "contract_telemetry_bundle",
        "from": "deterministic validators",
        "to": "patch bundle/evidence handoff",
        "performed": true
      }
    ]
  },
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,

## Chunk content

```json
  "evidence": [
    {
      "name": "gpu1_primary_advisory",
      "path": "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "gpu1_primary_advisory",
      "passed": true,
      "provider_execution_performed": true,
      "classifications": [],
      "runtime_tool_execution_count": 0
    },
    {
      "name": "gpu0_peer_task_packet",
      "path": "output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "gpu0_peer_task_packet",
      "passed": true,
      "provider_execution_performed": null,
      "classifications": [],
      "task_count": 4
    },
    {
      "name": "gpu0_peer_response",
      "path": "output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "gpu0_peer_response",
      "passed": true,
      "provider_execution_performed": true,
      "classifications": [
        "gpu0_peer_semantic_model_unconfigured"
      ],
      "task_count": 4,
      "response_count": 4,
      "tool_request_count": 3
    },
    {
      "name": "gpu0_tool_requests",
      "path": "output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "gpu0_peer_tool_requests",
      "passed": null,
      "provider_execution_performed": null,
      "classifications": []
    },
    {
      "name": "gpu0_runtime_tool_broker",
      "path": "output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "agent_runtime_tool_broker",
      "passed": true,
      "provider_execution_performed": false,
      "classifications": [],
      "tool_request_count": 3,
      "tool_execution_count": 3
    },
    {
      "name": "npu_micro_response",
      "path": "output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "npu_micro_peer_assistant",
      "passed": true,
      "provider_execution_performed": false,
      "classifications": [],
      "tool_request_count": 0
    },
    {
      "name": "npu_runtime_tool_broker",
      "path": "output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "agent_runtime_tool_broker",
      "passed": true,
      "provider_execution_performed": false,
      "classifications": [],
      "tool_request_count": 0,
      "tool_execution_count": 0
    },
    {
      "name": "ai_peer_exchange",
      "path": "output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "error": "",
      "kind": "ai_peer_exchange",
      "passed": true,
      "provider_execution_performed": true,
      "classifications": [
        "gpu0_peer_semantic_model_unconfigured"
      ]
    }
  ],
  "guardrails": {
    "report_only": true,
    "gpu1_primary_advisory_required": true,
    "gpu0_peer_response_required": true,
    "gpu0_broker_execution_required": true,
    "npu_micro_lane_non_blocking": true,
    "npu_micro_lane_not_heavy_authority": true,
    "npu_support_tool_supply_non_blocking": true,
    "npu_slow_or_degraded_not_product_blocker": true,
    "peer_mesh_visibility_required": true,
    "deterministic_scripts_heavy_audit_authority": true,
    "provider_broker_loop_required": true,
    "provider_broker_loop_controlled_executor_required": "runtime_tool_broker",
    "patch_application_performed": false,
    "source_writes_performed": false
  }
}
```
