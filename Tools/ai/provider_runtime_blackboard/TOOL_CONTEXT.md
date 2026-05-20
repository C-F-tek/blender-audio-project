# Tools/ai/provider_runtime_blackboard context

## Role

`Tools/ai/provider_runtime_blackboard` owns the materialized runtime blackboard used to observe provider lanes, broker requests, peer reports, live signals and validation bridge state.

This area is not the provider itself. It is the observable state layer around provider activity.

It concretizes the bridge between:

```text
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Record provider runtime heap events.
- Materialize lane state for provider/peer visibility.
- Bridge broker requests/results into runtime state.
- Bridge validation signals into the provider blackboard.
- Build peer-report derived heap artifacts.
- Provide live-signal reports that help distinguish active, stalled, degraded and diagnostic-only lanes.
- Convert provider/peer reports into heap-readable state.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai provider_runtime_blackboard ...
python -m Tools.ai provider_runtime_broker_bridge ...
python -m Tools.ai provider_runtime_live_signals ...
python -m Tools.ai provider_runtime_validation_bridge ...
python -m Tools.ai build_provider_runtime_heap_from_peer_reports ...
python -m Tools.ai run_provider_runtime_heap_gpu_peer_smoke ...
```

## Current code responsibilities

Important concepts in this package include:

```text
heap event capture
provider report materialization
pending broker request state
lane status materialization
SQLite sidecar index for provider runtime heap
full payload sidecar blobs for compact JSONL events
validation bridge signals
live signal summaries
peer report ingestion
provider runtime evidence
```

## Bridge model

```text
provider_mesh report
GPU0 peer report
NPU micro report
broker result
validator signal
-> provider_runtime_blackboard
-> materialized heap state
-> exchange evidence
-> product or blocked classification
```

The bridge makes the provider lanes observable by the rest of Universo IA.

## Boundaries

- Blackboard state is evidence, not a patch product.
- Provider visibility is not provider success by itself.
- SQLite sidecar indexes are runtime artifacts and must not be committed as databases.
- Compact JSONL events may point at the SQLite `payload_blobs` table; the full payload must remain queryable there when the event payload is compacted.
- Materialized state must distinguish diagnostic activity, semantic provider activity and operational provider output.
- Do not treat blackboard events as source-write permission.
- Do not treat live signals as proof of product success.

## Expected artifacts

```text
provider runtime heap reports
broker bridge reports
live signal reports
validation bridge reports
peer-report heap materialization
SQLite sidecar indexes under ignored runtime/output paths
```

## Validation expectations

Relevant validation areas:

```powershell
python -m Tools.validation run_provider_tool_loop_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation run_observable_peer_activity_contract_smoke ...
python -m Tools.validation run_provider_empty_response_diagnostics_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation run_provider_tool_loop_smoke ...
```

## Extension notes

When adding new blackboard tables, event kinds or materialized views, update reports and validation together. Keep runtime database writes under ignored output/runtime paths.
