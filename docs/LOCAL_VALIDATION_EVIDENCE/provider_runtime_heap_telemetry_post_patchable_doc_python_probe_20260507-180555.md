# Provider Runtime Heap Telemetry

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- event_count: `62`
- parse_error_count: `0`
- tool_catalog_exchange_complete_count: `1`
- gpu1_to_gpu0_event_count: `2`
- gpu0_to_gpu1_event_count: `7`
- gpu1_gpu0_bidirectional: `True`
- gpu1_gpu0_correlated_exchange_count: `2`
- broker_request_count: `14`
- broker_result_count: `20`
- pending_broker_request_count: `0`
- validation_signal_count: `1`
- direct_execution_violation_count: `0`
- tool_catalog_tool_count: `10`

## Events by lane

- `broker`: `22`
- `deterministic`: `1`
- `gpu0`: `13`
- `gpu1`: `4`
- `npu`: `12`
- `orchestrator`: `10`

## Events by type

- `broker_request`: `14`
- `broker_result`: `20`
- `evidence_request`: `9`
- `evidence_response`: `11`
- `provider_state`: `3`
- `tool_catalog_request`: `2`
- `tool_catalog_response`: `2`
- `validation_signal`: `1`

## Interaction edges

- `broker->gpu0:broker_result`: `6`
- `broker->gpu1:tool_catalog_response`: `2`
- `broker->npu:broker_result`: `14`
- `deterministic->gpu1:validation_signal`: `1`
- `gpu0->broker:broker_request`: `6`
- `gpu0->gpu1:evidence_response`: `7`
- `gpu1->broker:tool_catalog_request`: `2`
- `gpu1->gpu0:evidence_request`: `2`
- `npu->broker:broker_request`: `8`
- `npu->gpu1:evidence_response`: `4`
- `orchestrator->gpu0:evidence_request`: `5`
- `orchestrator->none:provider_state`: `3`
- `orchestrator->npu:evidence_request`: `2`
