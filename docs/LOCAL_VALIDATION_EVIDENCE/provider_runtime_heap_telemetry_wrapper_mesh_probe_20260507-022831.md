# Provider Runtime Heap Telemetry

- passed: `True`
- stamp: `wrapper_mesh_probe_20260507-022831`
- event_count: `37`
- parse_error_count: `0`
- tool_catalog_exchange_complete_count: `0`
- gpu1_to_gpu0_event_count: `2`
- gpu0_to_gpu1_event_count: `4`
- gpu1_gpu0_bidirectional: `True`
- gpu1_gpu0_correlated_exchange_count: `2`
- broker_request_count: `10`
- broker_result_count: `11`
- pending_broker_request_count: `0`
- validation_signal_count: `1`
- direct_execution_violation_count: `0`
- tool_catalog_tool_count: `10`

## Events by lane

- `broker`: `11`
- `deterministic`: `1`
- `gpu0`: `10`
- `gpu1`: `2`
- `npu`: `7`
- `orchestrator`: `6`

## Events by type

- `broker_request`: `10`
- `broker_result`: `11`
- `evidence_request`: `5`
- `evidence_response`: `7`
- `provider_state`: `3`
- `validation_signal`: `1`

## Interaction edges

- `broker->gpu0:broker_result`: `6`
- `broker->npu:broker_result`: `5`
- `deterministic->gpu1:validation_signal`: `1`
- `gpu0->broker:broker_request`: `6`
- `gpu0->gpu1:evidence_response`: `4`
- `gpu1->gpu0:evidence_request`: `2`
- `npu->broker:broker_request`: `4`
- `npu->gpu1:evidence_response`: `3`
- `orchestrator->gpu0:evidence_request`: `2`
- `orchestrator->none:provider_state`: `3`
- `orchestrator->npu:evidence_request`: `1`
