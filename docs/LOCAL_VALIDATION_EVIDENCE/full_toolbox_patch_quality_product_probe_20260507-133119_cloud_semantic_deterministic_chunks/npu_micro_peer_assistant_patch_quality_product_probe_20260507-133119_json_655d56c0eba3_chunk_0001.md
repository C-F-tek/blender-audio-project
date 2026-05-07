# Evidence Chunk 0001/0001

- source: `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `655d56c0eba3b1eda0beedf80be9208e7db769aa4f9df71f54059fd009583c4f`
- line_start: `2`
- line_end: `40`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; stamp; classification; provider_execution_requested. Preview: "schema_version": 1, "kind": "npu_micro_peer_assistant", "generated_at": "2026-05-07T13:33:29", "stamp": "patch_quality_product_probe_20260507-133119", "passed": true, "classification": "npu_peer_provider_deferred_to_avoid_openvino_contention", "provider_execu...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "npu_micro_peer_assistant",
  "generated_at": "2026-05-07T13:33:29",
  "stamp": "patch_quality_product_probe_20260507-133119",
  "passed": true,
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
}
```
