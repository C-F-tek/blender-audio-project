# Evidence Chunk 0001/0001

- source: `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `5ebca2e6e783aaa9814d0a795487ebea586258ca9342c5f505c6975c93e6ebca`
- line_start: `2`
- line_end: `31`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; stamp; executed; classification. Preview: "schema_version": 1, "kind": "agent_runtime_tool_broker", "generated_at": "2026-05-07T13:33:29", "stamp": "patch_quality_product_probe_20260507-133119", "passed": true, "executed": false, "classification": "npu_peer_provider_deferred_noop_broker", "enabled": f...

## Context before

{

## Chunk content

```json
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
}
```
