# Evidence Chunk 0002/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `265`
- line_end: `457`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0001.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0003.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`; `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json`; `output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json`; `output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json`; `output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json`. Preview: ### `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json` - Exists: `True` - JSON OK: `True` - Kind: `ai_peer_exchange` - Passed: `True` - Provider execution performed: `True` - Patch application performed: `False` - Source writ...

## Context before


### `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.']`


## Chunk content

```md
### `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_peer_exchange`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`
- Peer mesh visibility: `{'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': False, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': False, 'npu_tool_requests_broker_consumed': False, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}`
- NPU support lane: `{'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': False, 'tool_request_count': 0, 'broker_tool_execution_count': 0, 'provider_execution_requested': False, 'provider_execution_performed': False, 'provider_slow_or_degraded': False, 'classification': 'npu_peer_provider_deferred_to_avoid_openvino_contention', 'deterministic_fallback_used': False, 'product_pass_blocker': False}`
- Peer mesh lane state: `{'schema_version': 1, 'kind': 'peer_mesh_lane_state', 'operational_lanes': ['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support'], 'support_lanes': ['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply'], 'degraded_lanes': ['gpu0_semantic_companion_model_unconfigured'], 'product_blockers': [], 'gpu0_broker_tool_execution_count': 3, 'npu_broker_tool_execution_count': 0, 'broker_runtime_tool_execution_count': 3, 'legacy_usable_lanes_are_workload_quality_only': True, 'npu_degraded_is_product_blocker': False, 'npu_heavy_audit_authority': False, 'all_required_product_lanes_present': True, 'mesh_visibility': {'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': False, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': False, 'npu_tool_requests_broker_consumed': False, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}, 'npu_support_lane': {'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': False, 'tool_request_count': 0, 'broker_tool_execution_count': 0, 'provider_execution_requested': False, 'provider_execution_performed': False, 'provider_slow_or_degraded': False, 'classification': 'npu_peer_provider_deferred_to_avoid_openvino_contention', 'deterministic_fallback_used': False, 'product_pass_blocker': False}}`

### `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_peer_exchange_contract`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`
- Warnings: `['gpu0_peer_semantic_model_unconfigured']`
- Peer mesh lane state: `{'schema_version': 1, 'kind': 'peer_mesh_lane_state', 'operational_lanes': ['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support'], 'support_lanes': ['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply'], 'degraded_lanes': ['gpu0_semantic_companion_model_unconfigured'], 'product_blockers': [], 'gpu0_broker_tool_execution_count': 3, 'npu_broker_tool_execution_count': 0, 'broker_runtime_tool_execution_count': 3, 'legacy_usable_lanes_are_workload_quality_only': True, 'npu_degraded_is_product_blocker': False, 'npu_heavy_audit_authority': False, 'all_required_product_lanes_present': True, 'mesh_visibility': {'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': False, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': False, 'npu_tool_requests_broker_consumed': False, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}, 'npu_support_lane': {'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': False, 'tool_request_count': 0, 'broker_tool_execution_count': 0, 'provider_execution_requested': False, 'provider_execution_performed': False, 'provider_slow_or_degraded': False, 'classification': 'npu_peer_provider_deferred_to_avoid_openvino_contention', 'deterministic_fallback_used': False, 'product_pass_blocker': False}}`

### `output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_snapshot`
- Passed: `None`

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_telemetry`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_from_peer_reports`
- Passed: `True`

### `docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `patch_plan_quality_product_gate`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_evidence_index.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_evidence_index`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_readiness.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_readiness`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `20`

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Recommendation count: `20`
- Warnings: `['patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection']`

### `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Warnings: `['max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection']`
- Patch plan summary count: `20`
- Fallback used: `False`
- Manual review required: `True`

## Patch plan summary

```

## Context after

### `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json`

- Patch plan count: `20`
- Fallback used: `False`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### consistency_001 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
