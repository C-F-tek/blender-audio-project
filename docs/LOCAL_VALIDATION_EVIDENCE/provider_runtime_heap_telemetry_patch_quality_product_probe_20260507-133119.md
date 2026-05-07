# Provider Runtime Heap Telemetry

- passed: `True`
- stamp: `patch_quality_product_probe_20260507-133119`
- event_count: `32`
- parse_error_count: `0`
- tool_catalog_exchange_complete_count: `0`
- gpu1_to_gpu0_event_count: `2`
- gpu0_to_gpu1_event_count: `7`
- gpu1_gpu0_bidirectional: `True`
- gpu1_gpu0_correlated_exchange_count: `2`
- broker_request_count: `6`
- broker_result_count: `6`
- pending_broker_request_count: `0`
- validation_signal_count: `1`
- direct_execution_violation_count: `0`
- tool_catalog_tool_count: `10`

## Events by lane

- `broker`: `6`
- `deterministic`: `1`
- `gpu0`: `13`
- `gpu1`: `2`
- `npu`: `2`
- `orchestrator`: `8`

## Events by type

- `broker_request`: `6`
- `broker_result`: `6`
- `evidence_request`: `7`
- `evidence_response`: `9`
- `provider_state`: `3`
- `validation_signal`: `1`

## Interaction edges

- `broker->gpu0:broker_result`: `6`
- `deterministic->gpu1:validation_signal`: `1`
- `gpu0->broker:broker_request`: `6`
- `gpu0->gpu1:evidence_response`: `7`
- `gpu1->gpu0:evidence_request`: `2`
- `npu->gpu1:evidence_response`: `2`
- `orchestrator->gpu0:evidence_request`: `5`
- `orchestrator->none:provider_state`: `3`
