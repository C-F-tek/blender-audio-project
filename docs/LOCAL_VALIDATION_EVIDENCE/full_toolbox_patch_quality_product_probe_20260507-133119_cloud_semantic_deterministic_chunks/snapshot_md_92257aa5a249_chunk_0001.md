# Evidence Chunk 0001/0001

- source: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.md`
- source_sha256: `92257aa5a2499b1abd1daf4f8b15356114edd356126c514e3c8697c14ec6188d`
- line_start: `1`
- line_end: `40`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Provider Runtime Heap Snapshot; Runtime architecture; Events by lane; Semantic tools registry. Preview: # Provider Runtime Heap Snapshot - Stamp: `patch_quality_product_probe_20260507-133119` - Event count: `32` - Parse error count: `0` - Pending broker requests: `0` - Event log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl` #...

## Chunk content

```md
# Provider Runtime Heap Snapshot

- Stamp: `patch_quality_product_probe_20260507-133119`
- Event count: `32`
- Parse error count: `0`
- Pending broker requests: `0`
- Event log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`

## Runtime architecture

- `gpu1`: `primary_advisory_planner`
- `gpu0`: `coworker_helper_openvino`
- `npu`: `microtask_responder`
- `broker`: `single_controlled_executor`
- `semantic_tools_registry`: `agent_runtime_tool_broker.TOOL_SPECS`
- `deterministic_validators`: `cpu_authority_validation_lane`
- `telemetry`: `append_only_event_stream`

## Events by lane

- `orchestrator`: `{'event_count': 8, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'provider_state': 3, 'evidence_request': 5}}`
- `gpu0`: `{'event_count': 13, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'evidence_response': 7, 'broker_request': 6}}`
- `gpu1`: `{'event_count': 2, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'evidence_request': 2}}`
- `broker`: `{'event_count': 6, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'broker_result': 6}}`
- `npu`: `{'event_count': 2, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'evidence_response': 2}}`
- `deterministic`: `{'event_count': 1, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'validation_signal': 1}}`

## Semantic tools registry

- Tool count: `10`
- `build_agent_agnostic_tool_inventory`: Inventory existing reusable IA-Carmine tools and guardrails.
- `build_agent_memory_inventory`: Read-only SQLite/JSONL agent memory inventory.
- `build_agent_transient_request_context`: Build request-scoped context from memory notes, raw files and reports.
- `build_code_interpreter_report`: Build static code-interpreter style report over selected roots.
- `build_python_line_count_csv`: Build full Python line-count CSV/JSON/MD evidence.
- `build_refactor_duplication_audit`: Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.
- `check_python_syntax`: Validate Python syntax across repository.
- `check_validation_report_contract`: Validate validation report contract for a scoped report-dir or explicit report files.
- `run_gpu_planner_json_contract_smoke`: Run GPU planner JSON contract smoke tests without provider.
- `runtime_sqlite_memory`: Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.
```
