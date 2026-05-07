# Local Validation Evidence Bundle

- Generated at: `2026-05-07T13:33:44`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `40`
- `patch_plan_summary_seen`: `True`

## Reports

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

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `collect_more_evidence`

### `output/validation/local_provider_probe.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_provider_probe`
- Passed: `False`
- Provider execution performed: `True`
- Errors: `['ollama: probe failed']`

### `output/validation/ai_workload_report_quality.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_workload_report_quality`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Usable workload lanes: `['npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu']`
- Unusable workload lanes: `[]`
- Warnings: `['npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `185`

### `output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu1_primary_advisory`
- Passed: `True`
- Provider execution performed: `True`
- Recommendation count: `0`

### `output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_task_packet`
- Passed: `True`

### `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_response`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only.']`

### `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_tool_requests`
- Passed: `None`

### `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_micro_peer_assistant`
- Passed: `True`
- Provider execution performed: `False`
- Warnings: `['NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.']`

### `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.']`

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

### `output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_from_peer_reports`
- Passed: `True`

### `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_snapshot`
- Passed: `None`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_usage_telemetry`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_capability_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_telemetry`
- Passed: `True`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_final_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'provider_runtime_heap_blackboard', 'deterministic_scripts']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'provider_runtime_heap_broker_results']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`
- Errors: `['ollama: probe failed']`
- Warnings: `['patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection', 'max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_control.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_control`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_optimization.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_effective_use_optimization`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['NPU probe not performed or disabled']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_summary.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_effective_use_optimization_summary`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['NPU probe not performed or disabled']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_tool_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_effective_use_tool_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_provider_hardening_contracts.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_hardening_contracts`
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

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
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

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_command_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_command_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_execution_bridge`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['real_run_blocked_valid_pre_run_state']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_execution_bridge_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_real_run_gate.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_real_run_gate`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['real provider run blocked by gate']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_workload_output_paths.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_workload_output_paths`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_dry_run_steps.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_dry_run_steps`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_expected_telemetry_contract`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_invocation_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_invocation_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit_denied_valid_for_dry_run_plan']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_workload_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_workload_report_contract`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_control.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_control`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_governor`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit denied by policy; artifact generation is still valid']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_governor_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_run_permit.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_run_permit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit denied by policy; artifact generation is still valid']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_control.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_control`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_governor`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit denied by policy; artifact generation is still valid']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_governor_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_run_permit.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_run_permit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit denied by policy; artifact generation is still valid']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_dry_run_steps.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_dry_run_steps`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_expected_telemetry_contract`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_invocation_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_invocation_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit_denied_valid_for_dry_run_plan']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_workload_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_workload_report_contract`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_control.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_control`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_accelerator_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_governor`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit denied by policy; artifact generation is still valid']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_governor_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_run_permit.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_provider_run_permit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['permit denied by policy; artifact generation is still valid']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/quality_gate/full0to10_quality_gate.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_quality_gate`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['some_recent_quality_reports_not_visible', 'no_refactor_patch_specs_supplied']`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_track_input_contract`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_template.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_track_input_template`
- Passed: `None`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_operational_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_persistent_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_line_count.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_syntax.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_contract`
- Passed: `True`

### `output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_worker_lane`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; semantic LLM subtasks unavailable, numeric/tool companion active.']`

### `output/validation/gpu0_companion_tool_requests_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_tool_requests`
- Passed: `None`

### `output/validation/gpu0_companion_worker_workload_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_hardware_governance_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['GPU.1 is visible to OpenVINO but reserved for Ollama/CUDA; do not route OpenVINO work there by default.', 'IA_CARMINE_GPU0_COMPANION_MODEL_DIR is not configured; GPU0 semantic peer mode will classify as unconfigured/fallback.']`

### `output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_evidence_contract`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `["local provider probe degraded: ['ollama: probe failed']"]`

### `output/validation/runtime_tool_bootstrap_requests_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_bootstrap_requests`
- Passed: `None`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/runtime_tool_broker_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_code_interpreter.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `166`

### `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agent_memory_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agnostic_tool_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_agnostic_tool_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_transient_request_context.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_transient_request_context`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_001_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_002_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_003_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_004_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

## Patch plan summary

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
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_002 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_003 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_004 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_005 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141` targeting `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_006 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14` targeting `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md` and resolve `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_007 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_008 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_009 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_010 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_011 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_012 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_013 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_045 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_046 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_047 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_048 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_049 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_050 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_051 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json` exists=`True` size=`3058` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json` exists=`True` size=`441138` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json` exists=`True` size=`368889` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json` exists=`True` size=`1252` suffix=`.json` preview_chars=`1219`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json` exists=`True` size=`72790` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json` exists=`True` size=`23981` suffix=`.json` preview_chars=`1500`
- `output/validation/local_provider_probe.json` exists=`True` size=`2528` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_workload_report_quality.json` exists=`True` size=`24810` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`9571446` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1228` suffix=`.json` preview_chars=`1189`
- `output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`2129738` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`3162` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`78343` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1478` suffix=`.json` preview_chars=`1436`
- `output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`6134` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`5011` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`3450` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`29697` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1492` suffix=`.json` preview_chars=`1452`
- `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1010` suffix=`.json` preview_chars=`979`
- `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`61320` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`13421` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1573` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1962` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`4810` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1931` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1649` suffix=`.json` preview_chars=`1500`
- `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json` exists=`True` size=`7017` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`17990` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`15073` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`2286` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1732813` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`379334` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_control.json` exists=`True` size=`11433` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_telemetry.json` exists=`True` size=`686` suffix=`.json` preview_chars=`657`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_optimization.json` exists=`True` size=`1206` suffix=`.json` preview_chars=`1178`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_summary.json` exists=`True` size=`18342` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_tool_telemetry.json` exists=`True` size=`1379` suffix=`.json` preview_chars=`1324`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_provider_hardening_contracts.json` exists=`True` size=`7541` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_evidence_index.json` exists=`True` size=`202251` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json` exists=`True` size=`379334` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_readiness.json` exists=`True` size=`444` suffix=`.json` preview_chars=`430`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_command_plan.json` exists=`True` size=`1504` suffix=`.json` preview_chars=`1455`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.json` exists=`True` size=`45251` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge_telemetry.json` exists=`True` size=`1226` suffix=`.json` preview_chars=`1181`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_real_run_gate.json` exists=`True` size=`2029` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_workload_output_paths.json` exists=`True` size=`1751` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_dry_run_steps.json` exists=`True` size=`1736` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json` exists=`True` size=`1085` suffix=`.json` preview_chars=`1043`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_invocation_plan.json` exists=`True` size=`34138` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_workload_report_contract.json` exists=`True` size=`1198` suffix=`.json` preview_chars=`1162`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_control.json` exists=`True` size=`11433` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json` exists=`True` size=`686` suffix=`.json` preview_chars=`657`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor.json` exists=`True` size=`25367` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor_telemetry.json` exists=`True` size=`1441` suffix=`.json` preview_chars=`1384`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_run_permit.json` exists=`True` size=`2851` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_control.json` exists=`True` size=`11433` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json` exists=`True` size=`686` suffix=`.json` preview_chars=`657`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor.json` exists=`True` size=`25214` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor_telemetry.json` exists=`True` size=`1441` suffix=`.json` preview_chars=`1384`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_run_permit.json` exists=`True` size=`2851` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_dry_run_steps.json` exists=`True` size=`1736` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json` exists=`True` size=`1085` suffix=`.json` preview_chars=`1043`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_invocation_plan.json` exists=`True` size=`33956` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_workload_report_contract.json` exists=`True` size=`1198` suffix=`.json` preview_chars=`1162`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_control.json` exists=`True` size=`11433` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json` exists=`True` size=`686` suffix=`.json` preview_chars=`657`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor.json` exists=`True` size=`25289` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor_telemetry.json` exists=`True` size=`1441` suffix=`.json` preview_chars=`1384`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_run_permit.json` exists=`True` size=`2851` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/quality_gate/full0to10_quality_gate.json` exists=`True` size=`3621` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_contract.json` exists=`True` size=`7275` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/track_inputs/full0to10_track_input_template.json` exists=`True` size=`1056` suffix=`.json` preview_chars=`1024`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy.json` exists=`True` size=`8953` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy_smoke.json` exists=`True` size=`2972` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_operational_memory_status.json` exists=`True` size=`1706` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_persistent_memory_status.json` exists=`True` size=`1781` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_line_count.json` exists=`True` size=`3220` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_syntax.json` exists=`True` size=`78343` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker.json` exists=`True` size=`99586` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker_smoke.json` exists=`True` size=`2001` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_validation_report_contract.json` exists=`True` size=`3697` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.json` exists=`True` size=`5705` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`498` suffix=`.json` preview_chars=`486`
- `output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`8407` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_tool_requests_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1572` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_worker_workload_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1722` suffix=`.json` preview_chars=`1500`
- `output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`2242` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`6878` suffix=`.json` preview_chars=`1500`
- `output/validation/runtime_tool_bootstrap_requests_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1298` suffix=`.json` preview_chars=`1264`
- `output/validation/runtime_tool_broker_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`27585` suffix=`.json` preview_chars=`1500`
- `output/analysis/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_code_interpreter.json` exists=`True` size=`1947394` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`6376` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`5238` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agent_memory_inventory.json` exists=`True` size=`13556` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agnostic_tool_inventory.json` exists=`True` size=`916211` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_transient_request_context.json` exists=`True` size=`9354` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json` exists=`True` size=`1732` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_001_gpu0_peer_support.json` exists=`True` size=`1733` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_002_gpu0_peer_support.json` exists=`True` size=`1732` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_003_gpu0_peer_support.json` exists=`True` size=`1733` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_004_gpu0_peer_support.json` exists=`True` size=`1732` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `8664`
- SHA-256: `fff3f922e70a8a09b2b08df6592deb2277ef074d80a1bd26448f9fa1a6833715`
- Content included: `True`
- Content truncated: `False`

```text
# Shared Runtime Toolbox Orchestration Architecture

## Scope

This document records the IA-Carmine runtime-tool architecture after the GPU/NPU orchestration refactor.

The goal is to keep the system provider-agnostic while allowing multiple reasoning lanes to request and consume tool evidence through a single controlled execution path.

## Current target topology

```text
GPU -> tool_requests -> orchestrator -> broker -> report
NPU -> tool_requests -> orchestrator -> broker -> report

provider -> never direct executor
orchestrator -> control-plane / routing / scheduling
broker -> only controlled executor
runtime heap -> append-only blackboard / visibility mesh
report -> reinjected read-only evidence
```

## Roles

### Provider lanes

GPU and NPU lanes are requesters and consumers.

They may:

- read repository evidence and generated reports;
- produce recommendations;
- produce structured `tool_requests`;
- consume broker reports as read-only context;
- classify missing evidence and runtime failures.

They must not:

- execute shell commands directly;
- apply patches directly;
- write persistent SQLite memory without explicit controlled authorization;
- create GitHub PRs directly;
- run Blender runtime;
- bypass broker allowlists.

### Orchestrator

The orchestrator is the control-plane.

It is responsible for:

- launching GPU planning;
- launching GPU0 peer-support work at startup and from GPU checkpoints;
- launching NPU micro-support work at startup and from GPU checkpoints, with legacy NPU audits only when explicitly requested;
- collecting checkpoint reports;
- collecting GPU and NPU `tool_requests`;
- scheduling report-only tool execution;
- passing requests to the broker;
- reinjecting broker reports into later context;
- preserving non-blocking behavior for NPU support;
- surfacing guardrail counters in final reports.

The orchestrator decides when a request is executed, but it does not implement the tools themselves.

### Broker

The broker is the only executor.

It is responsible for:

- validating request packets;
- enforcing the allowlist;
- executing only known report-only tools;
- blocking or reporting disallowed requests;
- writing JSON and Markdown reports;
- exposing guardrail counters.

The broker should remain deterministic, narrow, and low-policy. High-level scheduling belongs to the orchestrator.

### Runtime heap / blackboard

The runtime heap is the shared visibility layer for provider collaboration.

It is append-only evidence, not an executor:

- GPU1 can publish a bounded evidence/tool-context request for GPU0.
- GPU0 and the broker can publish broker result visibility.
- NPU can publish a non-blocking support signal back to GPU1.
- Telemetry can summarize events, lane edges and direct-execution violations.

The heap must never execute tools, apply patches or write source. Brokered tool reports remain the execution authority; the heap only records what each lane can see.

## Supported shared toolbox capabilities

The shared toolbox currently includes report-only capabilities such as:

- agent agnostic tool inventory;
- agent memory inventory;
- transient request context;
- runtime SQLite memory status/search under controlled modes;
- Python line-count inventory;
- Python syntax validation;
- validation report contract checks;
- GPU planner JSON contract smoke;
- code-interpreter report inventory;
- provider runtime heap live signals and telemetry.

Tool execution is always mediated by `Tools/ai/agent_runtime_tool_broker.py`.

## GPU path

### Standalone mode

The GPU supervised runner remains able to execute runtime tools directly through the broker for standalone workflows.

This compatibility mode is intentionally preserved because the supervised runner is still useful outside the full GPU/NPU orchestrator.

### Orchestrated mode

In orchestrated mode, the GPU runner should behave as a provider/requester:

1. The GPU planner receives evidence and toolbox context.
2. The GPU planner emits structured `tool_requests`.
3. The orchestrator collects the requests from GPU reports/checkpoints.
4. The orchestrator passes valid requests to the broker.
5. The broker executes allowlisted tools and writes reports.
6. The orchestrator reinjects the broker reports as read-only context.

The architectural preference is to keep this path symmetrical with the NPU path.

## NPU path

The production NPU lane is a bounded micro-support lane. The legacy NPU auditor remains available for diagnostics, but it is not enabled by default in Full0To10.

It may:

- start from the orchestrator `round_000` bootstrap seed so NPU readiness is visible at the beginning of the run;
- read GPU checkpoints;
- read runtime toolbox context;
- classify provider states;
- produce audit reports;
- propose structured `tool_requests`.

The NPU must not execute tools directly. NPU tool requests are routed through the orchestrator and broker.

NPU provider text evidence and NPU micro tool-support evidence are separate success surfaces. A timed-out or empty NPU provider response is recorded as provider degradation, but the micro lane can still be operationally successful when it emits valid brokered tool requests and the runtime heap closes the matching broker results with zero pending requests.

In full-toolbox peer exchange, NPU micro support sees GPU1/GPU0/broker/runtime-heap context, may emit brokered tool requests, and remains non-blocking. Heavy NPU audit waits require an explicit legacy-auditor flag and must not be confused with product NPU support.

The orchestrator owns both synchronization points:

```text
startup barrier: GPU1 primary process + GPU0 peer support + NPU micro support + deterministic/broker bootstrap
close barrier: harvest or terminate active GPU0/NPU/legacy support subprocesses before final telemetry and bundle reports
```

## Memory model

The memory model is split by scope:

- persistent memory: durable project rules, decisions and long-lived facts;
- operational memory: scratch/runtime context that can be regenerated or cleared;
- report artifacts: JSON/Markdown evidence under `output/**` or compact committed evidence under `docs/LOCAL_VALIDATION_EVIDENCE` when explicitly needed.

Persistent writes require explicit controlled authorization. Report-only reads/status checks are safe default operations.

## Guardrails

Permanent guardrails:

- no provider direct execution;
- no free shell from provider output;
- no patch application from provider output;
- no production deploy path;
- no Blender runtime in these validation lanes;
- no implicit persistent SQLite writes;
- no SQLite/database artifacts committed;
- no `output/**` artifacts committed except selected compact evidence when explicitly intended;
- line-count CSV evidence under `docs/LOCAL_VALIDATION_EVIDENCE` is a first-class compact evidence artifact when listed by workflow `evidence_to_commit`;
- NPU remains non-blocking and non-primary;
- broker remains the only executor.

## Smoke coverage

Key smoke coverage after the orchestration work:

```text
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py
Tools/validation/run_npu_runtime_tool_execution_smoke.py
Tools/validation/run_npu_tool_request_contract_smoke.py
Tools/validation/run_npu_runtime_tool_context_smoke.py
Tools/validation/run_provider_empty_response_diagnostics_smoke.py
Tools/validation/run_agent_runtime_tool_broker_smoke.py
```

Expected no-provider/report-only invariants:

```text
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
*_runtime_tool_request_count >= 1 when testing request routing
*_runtime_tool_execution_count >= 1 when testing broker execution
*_runtime_tool_failed_count=0 for positive smoke cases
*_runtime_tool_blocked_count=0 for positive smoke cases
```

## Operational workflow

Recommended local sequence after major toolbox/orchestrator changes:

1. Run targeted smoke for the changed lane.
2. Run GPU runtime routing smoke.
3. Run NPU runtime execution smoke.
4. Run syntax validation.
5. Run full memory/tool regeneration workflow when the architecture changes materially.
6. Commit only code/docs and selected compact validation evidence when needed.
7. Do not commit `output/**`, SQLite files, or generated runtime databases.

## Design rule

The high-level design rule is:

```text
Providers ask.
Orchestrator decides.
Broker executes.
Reports become evidence.
```

This preserves agnosticism: new providers or future local AI workers can join the same loop by producing structured requests and consuming reports, without receiving direct execution authority.

```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `33442`
- SHA-256: `195b6ec96dec9c0ced9ae32b75e1bf6189122539614a681d18650b05904d86c6`
- Content included: `True`
- Content truncated: `True`

```text
File,Lines
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,2263
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1774
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
Tools/ai/run_agent_gpu_deep_planning_supervised.py,1180
old script legacy/spaziotempo_asset_visual_v6.py,1174
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,1100
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/ai/build_deterministic_recommendations.py,909
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/ai/build_runtime_tool_usage_telemetry.py,823
Tools/ai/agent_runtime_tool_broker.py,759
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Tools/ai/build_refactor_duplication_audit.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Tools/ai/run_npu_gpu_deep_review_auditor.py,694
Scripting/v61b/materials.py,657
Tools/ai/build_ai_peer_exchange_packet.py,642
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_agent_review_patch_plan.py,626
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/analyze_gpu_npu_run_sync.py,587
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,579
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/build_full_toolbox_run_telemetry_summary.py,567
Tools/ai/build_semantic_evidence_chunks.py,562
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/agent_runtime_sqlite_memory.py,527
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/docs/build_code_aware_md_coherence.py,498
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/validation/check_provider_evidence_contract.py,478
Tools/ai/agent_memory_routing_policy.py,471
normalize_scene_spec.py,469
Tools/ai/build_agent_review_evidence_sufficiency.py,454
Tools/validation/check_reviewed_patch_specs.py,446
Tools/workflow/startup_check.py,444
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/docs/split_large_markdown.py,438
Tools/npu/ollama_runtime.py,438
Tools/validation/build_script_inventory.py,437
Tools/ai/provider_runtime_heap.py,436
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/validation/check_ai_peer_exchange_contract.py,412
Tools/ai/schema_repair_context.py,411
Tools/ai/agent_review_warning_policy.py,408
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
Tools/validation/check_full0to10_provider_acceptance.py,397
Scripting/v61b/encode_image_sequence_v61b.py,395
Scripting/v61b/hotpatch/hero_material_patch.py,395
Scripting/v61b_backgood/hotpatch/hero_material_patch.py,395
Scripting/v61b/fog_dynamics.py,392
Tools/ai/build_full_context_golden_proposals.py,392
Tools/validation/check_code_contract_drift.py,392
Tools/workflow/gui/components/artifact_browser.py,390
Tools/ai/gpu_planner_json_contract.py,380
Scripting/v61b_backgood/encode_image_sequence_v61b.py,376
indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py,369
Tools/npu/generated_blender_script_candidate.py,369
Tools/npu/generated_blender_script_candidate_FristNear.py,369
Tools/validation/check_repository_change_proposals.py,366
Tools/validation/test_npu_pipeline_helpers.py,359
Scripting/v61b_backgood/config.py,358
Tools/ai/build_local_ai_enrichment_plan.py,357
Tools/ai/build_provider_runtime_heap_from_peer_reports.py,357
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,354
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py,344
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/build_markdown_inventory.py,339
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py,333
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/validation/check_local_ai_adapter_manifest.py,331
Tools/ai/provider_runtime_heap_broker_bridge.py,327
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/ai/run_gpu0_peer_companion_worker.py,326
Tools/npu/build_blender_manual_context.py,326
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py,325
Tools/workflow/workflow_shell.py,324
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py,322
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/ai/build_music_intermediates.py,319
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/ai/github_evidence_bundle_artifacts.py,317
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/run_agent_review_decision_loop.py,311
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/validation/run_agent_review_decision_loop_smoke.py,307
Tools/ai/build_analysis_input_bundle.py,304
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/build_agent_transient_request_context.py,291
Tools/ai/select_semantic_code_chunks.py,291
Tools/validation/check_ai_pipeline_modules.py,290
Tools/validation/run_gpu_planner_json_contract_smoke.py,290
Tools/ai/build_runtime_tool_capability_manifest.py,289
Scripting/v61b/hotpatch/diagnostics.py,286
Tools/ai/build_gpu_repair_failure_recommendation.py,286
Tools/validation/run_agent_review_patch_plan_smoke.py,283
Tools/validation/run_substantive_planning_smoke.py,280
Tools/workflow/gui/components/session_overview.py,278
Tools/validation/check_generated_artifact_path_policy.py,272
Scripting/v61b/render_setup.py,270
Tools/validation/check_full_context_golden_docs_contract.py,270
Scripting/v61b_backgood/render_setup.py,267
Tools/workflow/ai_runtime_diagnostics.py,267
Tools/ai/build_code_patch_docs_followup.py,266
Tools/ai/provider_runtime_heap_live_signals.py,262
Tools/ai/build_megalithic_review_pr_draft.py,259
Tools/validation/check_docs_contract_drift.py,259
Tools/ai/build_code_patch_artifact_pack.py,258
Tools/validation/run_refactor_duplication_audit_smoke.py,258
analyze_wav.py,257
Tools/ai/github_evidence_bundle_reports.py,257
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py,247
Tools/validation/run_agent_review_patch_bundle_builder_smoke.py,244
Tools/validation/run_agent_runtime_tool_broker_smoke.py,244
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/ai/build_github_evidence_bundle.py,239
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/validation/run_agent_review_warning_policy_smoke.py,237
Tools/validation/generated_file_policy.py,235
Tools/validation/run_agent_memory_routing_policy_smoke.py,234
Tools/ai/workload_quality.py,233
Tools/ai/replay_gpu_planner_json_contract.py,232
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/ai/github_evidence_bundle_markdown.py,228
Tools/ai/build_gpu0_companion_task_lane.py,227
Tools/ai/build_provider_runtime_heap_telemetry.py,223
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/docs/apply_md_code_coherence_refactor.py,221
Tools/validation/check_file_line_limits.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/build_python_line_count_csv.py,212
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/run_repository_consistency_map_smoke.py,209
Tools/ai/repository_consistency_map/paths.py,208
Tools/validation/check_docs_links.py,208
Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py,208
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/ai/code_patch_plan_common.py,205
Tools/ai/patch_unified_launcher_light_full0to10.py,204
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
Tools/validation/runtime_hardware_delegation_checks.py,204
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py,203
Tools/validation/run_code_edit_proposal_smoke.py,203
Tools/ai/code_edit_proposal_helpers.py,201
Tools/validation/check_validation_report_contract.py,201
Tools/validation/run_agent_review_code_patch_plan_smoke.py,201
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py,196
Tools/ai/code_interpreter_report/scanner.py,191
Tools/validation/full_run_bundle_completeness.py,190
Tools/validation/report_utils.py,190
Tools/validation/run_runtime_tool_guidance_fallback_smoke.py,190
Tools/ai/check_npu_provider_environment.py,189
Tools/ai/build_workload_quality_lane_routing.py,186
Tools/validation/run_npu_runtime_tool_context_smoke.py,186
Tools/workflow/git_auto_push.py,186
Tools/ai/pipeline/remediation.py,185
Tools/validation/run_gpu_runner_provider_error_smoke.py,185
Tools/validation/check_ai_dry_run_matrix_cases.py,183
Tools/validation/run_schema_repair_retry_smoke.py,183
Tools/workflow/gui/components/action_panel.py,183
Tools/ai/run_local_provider_probe.py,182
Tools/workflow/gui/components/live_output_panel.py,182
Scripting/v61b_backgood/main_v61b.py,181
Tools/workflow/gui/workflow_gui_with_push.py,181
Tools/ai/provider_runtime_heap_validation_bridge.py,175
Scripting/v61b_backgood/world_setup.py,174
Tools/ai/build_openvino_hardware_governance_report.py,174
Tools/ai/runtime_tool_guidance.py,173
Tools/validation/check_generated_blender_script_policy.py,173
Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py,172
Tools/validation/run_schema_repair_context_smoke.py,168
Tools/ai/full_run_bundle_zip/builder.py,167
Tools/ai/repository_consistency_map/python_inventory.py,166
Tools/ai/full0to10_provider_telemetry_semantic/validator.py,163
Scripting/shared/image_sequence.py,161
Tools/ai/repository_consistency_map/builder.py,161
Tools/validation/run_npu_runtime_tool_execution_smoke.py,161
Tools/npu/npu_runtime.py,160
Scripting/v61b/fog_filaments.py,159
Tools/ai/github_evidence_bundle_io.py,159
Tools/validation/check_npu_decode_quality_remediation.py,159
Tools/validation/run_provider_empty_response_diagnostics_smoke.py,159
Tools/npu/pipeline/__init__.py,157
Tools/validation/run_schema_repair_retry_bootstrap_smoke.py,156
Tools/validation/run_runtime_tool_feedback_loop_smoke.py,154
Tools/ai/pipeline/models.py,152
Tools/validation/run_startup_check_cli_contract_smoke.py,152
Scripting/v61b/hotpatch/lighting_patch.py,150
Tools/validation/check_refactor_status_consistency.py,149
Tools/npu/build_runtime_output_manifest.py,148
Tools/npu/build_provider_result_report.py,147
Tools/validation/check_blender_shared_compat_smoke.py,147
Tools/ai/github_evidence_bundle_decisions.py,146
Tools/ai/repository_consistency_map/markdown.py,146
Tools/ai/code_interpreter_report/builder.py,144
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/ai/runtime_hardware_capability/workloads.py,142
Tools/ai/full0to10_sqlite_memory/embedding.py,141
Tools/validation/check_markdown_line_limits.py,141
Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py,141
Scripting/shared/blender_compat.py,140
Tools/ai/runtime_hardware_capability/manifest.py,139
Tools/ai/full0to10_final_product/builder.py,136
Scripting/shared/ffmpeg_encoder.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/full_run_bundle_zip/discovery.py,130
Tools/ai/model_json.py,130
Tools/validation/check_gpu0_companion_contract.py,130
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/ai/full0to10_effective_use/memory_product.py,123
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/ai/
```

### `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `17842`
- SHA-256: `8e3a2fc0d5ac59e8f9c680d5d365a7f84f6ee131ecc3a8eb36fbe081b81a7b08`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_patch_plan`
- Provider execution performed: `False`
- Patch application performed: `False`
- Patch plan count: `20`
- Fallback used: `False`
- Manual review required: `True`

## Inputs

- `orchestrator`: `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json`
- `orchestrator_kind`: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- `evidence_kind`: `agent_review_evidence_sufficiency`
- `gpu_kind`: `deterministic_recommendation_synthesizer`

## Patch plans

### consistency_001 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_003 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_005 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141` targeting `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14` targeting `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md` and resolve `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_013 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_045 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_046 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_047 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` witho
```

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1419`
- SHA-256: `52593dd72bbe946c7642dcaa457f61f7b4492208f2d76196e2de322fe7f2e4ad`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop

- Passed: `True`
- Recommendation count: `20`
- Patch plan count: `20`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `False`
- Provider execution performed: `False`
- Patch application performed: `False`

## Outputs

- `recommendations`: `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json` exists=`True` size=`368889`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.md` exists=`True` size=`26611`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json` exists=`True` size=`1252`
- `patch_plan`: `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json` exists=`True` size=`441138`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.md` exists=`True` size=`17842`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `26611`
- SHA-256: `a6191cd7e58559744e2a93d500d28f8a0a26b6aa25ebbde581d14b78edbfc422`
- Content included: `True`
- Content truncated: `True`

```text
# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `20`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `model_output_schema_mismatch`
- Evidence ready for manual patch count: `0`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### consistency_001 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_003 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_005 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141` targeting `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14` targeting `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md` and resolve `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_013 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_045 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_046 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_047 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` 
```

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3989`
- SHA-256: `3750ace6cb43a4fe63444f62993e00d0b7bf87020ce7a9a9edc9f0184f1697ea`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `61.694`
- `gpu0_peer_support_count`: `5`
- `gpu0_peer_support_success_count`: `5`
- `gpu0_peer_support_overlap_count`: `4`
- `gpu0_peer_support_provider_execution_performed`: `True`
- `npu_micro_support_count`: `0`
- `npu_micro_support_success_count`: `0`
- `npu_micro_support_overlap_count`: `0`
- `npu_micro_support_provider_execution_performed`: `False`
- `npu_micro_support_tool_request_count`: `0`
- `npu_micro_runtime_tool_execution_count`: `0`
- `npu_audit_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `model_output_schema_mismatch`
- `gpu_evidence_ready_for_manual_patch_count`: `0`
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_request_count`: `15`
- `runtime_tool_execution_count`: `7`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `7`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `provider_mesh_mode`: `startup_barrier_parallel_peer_support`
- `all_lanes_ready_at_start`: `True`
- `gpu0_peer_support_started_with_gpu1`: `True`
- `npu_micro_support_started_with_gpu1`: `False`
- `npu_auditor_mode`: `legacy_disabled`
- `npu_audit_success_count`: `0`
- `npu_micro_support_success_count`: `0`
- `npu_micro_support_provider_success_count`: `0`
- `npu_micro_support_tool_success_count`: `0`
- `npu_micro_support_tool_request_count`: `0`
- `npu_micro_live_tool_seed_count`: `0`
- `npu_micro_runtime_tool_execution_count`: `0`
- `npu_micro_runtime_tool_live_execution_count`: `0`
- `npu_micro_support_tool_lane_performed`: `False`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_deterministic_tool_fallback_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `False`
- `recommended_next_layer`: `collect_more_evidence`
- `gpu_empty_recommendations_reason`: `model_output_schema_mismatch`
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_bootstrap_executed`: `True`
- `runtime_tool_bootstrap_execution_count`: `7`
- `runtime_tool_provider_request_count`: `0`
- `runtime_tool_provider_request_execution_count`: `0`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `7`
- `runtime_tool_result_count`: `7`
- `manual_review_required`: `True`
- `provider_execution_performed`: `True`
- `gpu_provider_execution_performed`: `True`
- `gpu0_peer_support_provider_execution_performed`: `True`
- `npu_provider_execution_performed`: `False`
- `npu_micro_support_provider_execution_performed`: `False`
- `legacy_npu_auditor_provider_requested`: `False`
- `provider_degraded_reasons`: `[]`
- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `metadata_only`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `4`

## NPU Audits

## GPU0 Peer Support
- round `0` status=`finished` provider=`True` overlap=`True`
- round `1` status=`finished` provider=`True` overlap=`True`
- round `2` status=`finished` provider=`True` overlap=`True`
- round `3` status=`finished` provider=`True` overlap=`True`
- round `4` status=`finished` provider=`True` overlap=`False`

## NPU Micro Support

```

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1049`
- SHA-256: `1747c07b5ac4bd38f4d5a37f565bcc6a3781485457639817de10869fb33a0a66`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `50.767`
- Round count: `4`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `0`
- Context echo detected count: `0`
- Model output schema mismatch count: `4`
- Empty recommendations reason: `model_output_schema_mismatch`
- Evidence ready for manual patch count: `0`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `False`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `collect_more_evidence`
- `manual_review_required`: `True`

## Recommendations


```

### `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `56878`
- SHA-256: `b8dc343722aa7723ab004fa279ffba3f19553d509c8404a2e97a2fa027ae62a2`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `12321`
- Repository files: `1642`
- File metadata records: `1642`
- Counted text-like files: `1616`
- Total counted text lines: `1409295`
- Markdown files: `635`
- Python files: `650`
- Markdown references: `84503`
- Markdown Python commands: `786`
- Provider execution performed: `False`
- Workers requested: `0`
- Adaptive worker mode: `True`
- Single file manifest: `True`
- File metadata enabled: `True`
- Total build seconds: `25.864`
- Markdown scan seconds: `18.523`
- Python inventory seconds: `0.407`
- Patch application performed: `False`

## Severity counts

- `high`: `3952`
- `low`: `48`
- `medium`: `8321`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `48`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `8319`
- `md_mentions_missing_powershell_path`: `524`
- `md_mentions_missing_python_path`: `3384`
- `md_python_command_script_missing`: `44`

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 374 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 375 | `patches/00_check_repo_ready.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 372 | `text
README.md
run_patch_bundle.py
patches/00_check_repo_ready.py
patches/01_*.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 237 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 292 | `some_script.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 302 | `changed.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 323 | `some_tool.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 324 | `some_smoke.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 325 | `some_runner.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 323 | `Tools/validation/some_smoke.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT.md` | 60 | `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 22 | `agent_memory_schema.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 23 | `agent_memory_chunker.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 24 | `agent_memory_embeddings.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 25 | `agent_memory_search.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 26 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 325 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 328 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 334 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` | 339 | `agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 74 | `Tools/validation/check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 98 | `Tools/ai/agent_memory_schema.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 99 | `Tools/ai/agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 139 | `Tools/ai/simulate_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 157 | `Tools/ai/run_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 230 | `check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 52 | `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 73 | `text
Tools/validation/check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 97 | `text
Tools/ai/agent_memory_schema.py
Tools/ai/agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 138 | `text
Tools/ai/simulate_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 156 | `text
Tools/ai/run_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 55 | `hardware-memory.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 68 | `02-chunking.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 70 | `04-cli.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 94 | `01-overview.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 95 | `02-contract.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 96 | `03-commands.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 97 | `04-validation.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 98 | `05-next-steps.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 17 | `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 52 | `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 64 | `text
02-sqlite-heap-memory-design.md/
  README.md
  01-schema.md
  02-chunking.md
  03-search.md
  04-cli.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 91 | `text
<topic>.md/
  README.md
  01-overview.md
  02-contract.md
  03-commands.md
  04-validation.md
  05-next-steps.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` | 103 | `text
CHATGPT/<date>-<topic>/
  README.md
  01-*.md
  02-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/README.md` | 21 | `text
01-architecture-summary.md
02-sqlite-heap-memory-design.md
03-broker-hardware-delegation-contract.md
04-implementation-plan.md
05-reset-sync-commands.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/DISCOVERY_CONTRACT.md` | 13 | `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/README.md` | 25 | `text
1. AGENTS.md
2. CHATGPT.md
3. docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
4. docs/MAIN_RUNTIME_ARCHITECTURE.md
5. docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
6. docs/AI_PIPELINE_ARCHITECTURE.md
7. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
8. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
9. docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
10. docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
11. docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
12. docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
13. docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
14. docs/LOCAL_AI_TASKS/project-tool-registry.md
15. docs/TECH_DEBT_TRACKER.md
16. CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
17. CH
```

### `output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `381`
- SHA-256: `fbca8ef9cc4cb934e1df6e2a75ab7b56eecbc52deb3b4a086187114ff8bc9322`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Consistency Map Smoke

- Passed: `True`
- Return code: `0`
- Mapper report reused: `True`
- Workers requested: `0`
- Elapsed seconds: `0.048`
- Finding count: `12321`
- Markdown reference count: `84503`
- Markdown Python command count: `786`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`

```

### `output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7129`
- SHA-256: `5963bc8bf594dd3adf40c00079a3ec9d0179e69152e68522dc0cfe9da633db2e`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `601`
- Parsed files: `601`
- Total lines: `101948`
- Total functions: `3667`
- Total classes: `101`
- Risk signals: `90`
- TODO/FIXME markers: `21`
- Recommendation count: `185`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` - `2263` lines, risk `high`
- `Tools/npu/run_dual_ai_pipeline.py` - `1774` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` - `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` - `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` - `1180` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` - `1100` lines, risk `high`
- `Scripting/v61b/animation.py` - `1079` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` - `909` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` - `902` lines, risk `high`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` - `823` lines, risk `high`
- `Tools/ai/agent_runtime_tool_broker.py` - `759` lines, risk `medium`
- `Tools/workflow/gui/workflow_gui.py` - `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` - `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` - `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` - `725` lines, risk `medium`
- `Tools/npu/build_music_context.py` - `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` - `694` lines, risk `medium`
- `Scripting/v61b/materials.py` - `657` lines, risk `medium`
- `Tools/ai/build_ai_peer_exchange_packet.py` - `642` lines, risk `medium`
- `Tools/npu/run_npu_review.py` - `631` lines, risk `medium`

## Recommendations

- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected
- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected
- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_021` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_022` `Tools/ai/agent_review_warning_policy.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_023` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_025` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module
- `code_static_027` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_028` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_029` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_034` `Tools/ai/build_ai_peer_exchange_packet.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_038` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_039` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_040` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1762`
- SHA-256: `568d6c51a0fa10a05f52a4b87bd440a9058c697b5413dfc7f1843ad63414bb5e`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv`
- File count: `650`
- Total lines: `119498`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest Python files

- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `2263` lines
- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines
- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines
- `old script legacy/spaziotempo_asset_visual_v61.py` — `1513` lines
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines
- `Tools/workflow/workflow_state.py` — `1230` lines
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1180` lines
- `old script legacy/spaziotempo_asset_visual_v6.py` — `1174` lines
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `1100` lines
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines
- `Scripting/v61b/animation.py` — `1079` lines
- `Scripting/v61b_backgood/animation.py` — `1019` lines
- `old script legacy/spaziotempo_album_visual_v5.py` — `969` lines
- `Tools/ai/build_deterministic_recommendations.py` — `909` lines
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines
- `Tools/ai/build_runtime_tool_usage_telemetry.py` — `823` lines
- `Tools/ai/agent_runtime_tool_broker.py` — `759` lines
- `Tools/workflow/gui/workflow_gui.py` — `738` lines
- `Scripting/v61b/physics_setup.py` — `737` lines
- `Scripting/v61b/asset_setup.py` — `725` lines

## Guardrail

This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.

```

### `output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `38977`
- SHA-256: `16687cfda6d239f7e67bbebe0995316df8f7245b5de6ba45977c40ee87005e70`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: patch_quality_product_probe_20260507-133119
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv
- File count: 650
- Total Python lines: 119498
- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.

| Lines | File |
|---:|---|
| 2263 | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
| 2197 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` |
| 1774 | `Tools/npu/run_dual_ai_pipeline.py` |
| 1513 | `old script legacy/spaziotempo_asset_visual_v61.py` |
| 1262 | `Scripting/v61b/scene_tuning_panel.py` |
| 1230 | `Tools/workflow/workflow_state.py` |
| 1180 | `Tools/ai/run_agent_gpu_deep_planning_supervised.py` |
| 1174 | `old script legacy/spaziotempo_asset_visual_v6.py` |
| 1100 | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| 1097 | `Scripting/v61b_backgood/scene_tuning_panel.py` |
| 1079 | `Scripting/v61b/animation.py` |
| 1019 | `Scripting/v61b_backgood/animation.py` |
| 969 | `old script legacy/spaziotempo_album_visual_v5.py` |
| 909 | `Tools/ai/build_deterministic_recommendations.py` |
| 902 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
| 823 | `Tools/ai/build_runtime_tool_usage_telemetry.py` |
| 759 | `Tools/ai/agent_runtime_tool_broker.py` |
| 738 | `Tools/workflow/gui/workflow_gui.py` |
| 737 | `Scripting/v61b/physics_setup.py` |
| 725 | `Scripting/v61b/asset_setup.py` |
| 725 | `Scripting/v61b_backgood/asset_setup.py` |
| 725 | `Tools/ai/build_refactor_duplication_audit.py` |
| 720 | `Scripting/v61b_backgood/physics_setup.py` |
| 711 | `Tools/npu/build_music_context.py` |
| 710 | `old script legacy/spaziotempo_album_visual_v3.py` |
| 694 | `Tools/ai/run_npu_gpu_deep_review_auditor.py` |
| 657 | `Scripting/v61b/materials.py` |
| 642 | `Tools/ai/build_ai_peer_exchange_packet.py` |
| 631 | `Tools/npu/run_npu_review.py` |
| 627 | `Tools/validation/check_npu_pipeline_modules.py` |
| 626 | `Tools/ai/build_agent_review_patch_plan.py` |
| 618 | `Tools/ai/build_selective_execution_plan.py` |
| 608 | `Tools/ai/build_agent_review_patch_bundle.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 587 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 579 | `Tools/ai/build_ai_context_pack.py` |
| 573 | `Tools/ai/run_pipeline_dry_run_matrix.py` |
| 567 | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` |
| 562 | `Tools/ai/build_semantic_evidence_chunks.py` |
| 554 | `Scripting/v61b/atmosphere_setup.py` |
| 551 | `Tools/ai/suggest_repository_updates.py` |
| 544 | `Tools/ai/agent_state.py` |
| 543 | `Scripting/v61b_backgood/atmosphere_setup.py` |
| 527 | `Tools/ai/agent_runtime_sqlite_memory.py` |
| 519 | `Tools/ai/run_megalithic_repo_review.py` |
| 513 | `Scripting/v61b_backgood/materials.py` |
| 499 | `Tools/ai/build_agent_review_code_patch_plan.py` |
| 498 | `Tools/docs/build_code_aware_md_coherence.py` |
| 497 | `Tools/validation/ai_pipeline_report_contracts.py` |
| 490 | `Tools/npu/npu_guardrail_service.py` |
| 489 | `Tools/ai/refine_megalithic_review_signals.py` |
| 487 | `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| 483 | `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` |
| 478 | `Tools/validation/check_provider_evidence_contract.py` |
| 471 | `Tools/ai/agent_memory_routing_policy.py` |
| 469 | `normalize_scene_spec.py` |
| 454 | `Tools/ai/build_agent_review_evidence_sufficiency.py` |
| 446 | `Tools/validation/check_reviewed_patch_specs.py` |
| 444 | `Tools/workflow/startup_check.py` |
| 443 | `Tools/repo_patch_runner/apply_repo_mods.py` |
| 442 | `Tools/ai/promote_patch_spec_draft.py` |
| 439 | `Scripting/v61b/config.py` |
| 438 | `Tools/docs/split_large_markdown.py` |
| 438 | `Tools/npu/ollama_runtime.py` |
| 437 | `Tools/validation/build_script_inventory.py` |
| 436 | `Tools/ai/provider_runtime_heap.py` |
| 436 | `Tools/npu/build_project_ai_index.py` |
| 425 | `Tools/validation/check_ai_context_pack_contract.py` |
| 422 | `Tools/workflow/gui/components/storage_dashboard.py` |
| 419 | `Tools/workflow/scene_brief.py` |
| 414 | `Tools/ai/build_patch_specs_from_proposals.py` |
| 412 | `Tools/validation/check_ai_peer_exchange_contract.py` |
| 411 | `Tools/ai/schema_repair_context.py` |
| 408 | `Tools/ai/agent_review_warning_policy.py` |
| 408 | `Tools/ai/build_agent_agnostic_tool_inventory.py` |
| 402 | `Tools/npu/build_npu_code_context.py` |
| 401 | `Tools/validation/check_github_evidence_bundle.py` |
| 400 | `Tools/validation/check_patch_spec_drafts.py` |
| 399 | `Scripting/v61b/encode_ffmpeg_v61b.py` |
| 398 | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` |
| 397 | `Tools/ai/build_agent_memory_inventory.py` |
| 397 | `Tools/validation/check_full0to10_provider_acceptance.py` |
| 395 | `Scripting/v61b/encode_image_sequence_v61b.py` |
| 395 | `Scripting/v61b/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b_backgood/hotpatch/hero_material_patch.py` |
| 392 | `Scripting/v61b/fog_dynamics.py` |
| 392 | `Tools/ai/build_full_context_golden_proposals.py` |
| 392 | `Tools/validation/check_code_contract_drift.py` |
| 390 | `Tools/workflow/gui/components/artifact_browser.py` |
| 380 | `Tools/ai/gpu_planner_json_contract.py` |
| 376 | `Scripting/v61b_backgood/encode_image_sequence_v61b.py` |
| 369 | `indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py` |
| 369 | `Tools/npu/generated_blender_script_candidate.py` |
| 369 | `Tools/npu/generated_blender_script_candidate_FristNear.py` |
| 366 | `Tools/validation/check_repository_change_proposals.py` |
| 359 | `Tools/validation/test_npu_pipeline_helpers.py` |
| 358 | `Scripting/v61b_backgood/config.py` |
| 357 | `Tools/ai/build_local_ai_enrichment_plan.py` |
| 357 | `Tools/ai/build_provider_runtime_heap_from_peer_reports.py` |
| 355 | `Tools/npu/build_ai_service_packet.py` |
| 354 | `Tools/workflow/project_awareness.py` |
| 344 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py` |
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/build_markdown_inventory.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 333 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 331 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 327 | `Tools/ai/provider_runtime_heap_broker_bridge.py` |
| 327 | `Tools/npu/build_npu_knowledge_broker_packet.py` |
| 326 | `Tools/ai/run_gpu0_peer_companion_worker.py` |
| 326 | `Tools/npu/build_blender_manual_context.py` |
| 325 | `Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py` |
| 324 | `Tools/workflow/workflow_shell.py` |
| 322 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py` |
| 321 | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` |
| 319 | `Tools/ai/build_music_intermediates.py` |
| 319 | `Tools/workflow/gui/workflow_gui_modern.py` |
| 317 | `Tools/ai/github_evidence_bundle_artifacts.py` |
| 314 | `Tools/ai/run_npu_decode_smoke_diagnostic.py` |
| 311 | `Tools/ai/run_agent_review_decision_loop.py` |
| 307 | `Tools/ai/agent_memory_policy.py` |
| 307 | `Tools/validation/check_full_context_golden_proposals.py` |
| 307 | `Tools/validation/run_agent_review_decision_loop_smoke.py` |
| 304 | `Tools/ai/build_analysis_input_bundle.py` |
| 301 | `Scripting/v61b/hotpatch/accent_patch.py` |
| 297 | `Tools/npu/pipeline/providers.py` |
| 291 | `Tools/ai/build_agent_transient_request_context.py` |
| 291 | `Tools/ai/select_semantic_code_chunks.py` |
| 290 | `Tools/validation/check_ai_pipeline_modules.py` |
| 290 | `Tools/validation/run_gpu_planner_json_contract_smoke.py` |
| 289 | `Tools/ai/build_runtime_tool_capability_manifest.py` |
| 286 | `Scripting/v61b/hotpatch/diagnostics.py` |
| 286 | `Tools/ai/build_gpu_repair_failure_recommendation.py` |
| 283 | `Tools/validation/run_agent_review_patch_plan_smoke.py` |
| 280 | `Tools/validation/run_substantive_planning_smoke.py` |
| 278 | `Tools/workflow/gui/components/session_overview.py` |
| 272 | `Tools/validation/check_generated_artifact_path_policy.py` |
| 270 | `Scripting/v61b/render_setup.py` |
| 270 | `Tools/validation/check_full_context_golden_docs_contract.py` |
| 267 | `Scripting/v61b_backgood/render_setup.py` |
| 267 | `Tools/workflow/ai_runtime_diagnostics.py` |
| 266 | `Tools/ai/build_code_patch_docs_followup.py` |
| 262 | `Tools/ai/provider_runtime_heap_live_signals.py` |
| 259 | `Tools/ai/build_megalithic_review_pr_draft.py` |
| 259 | `Tools/validation/check_docs_contract_drift.py` |
| 258 | `Tools/ai/build_code_patch_artifact_pack.py` |
| 258 | `Tools/validation/run_refactor_duplication_audit_smoke.py` |
| 257 | `analyze_wav.py` |
| 257 | `Tools/ai/github_evidence_bundle_reports.py` |
| 256 | `Tools/validation/run_agnostic_context_stack_smoke.py` |
| 250 | `Tools/ai/build_code_edit_proposal_from_plan.py` |
| 247 | `Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py` |
| 244 | `Tools/validation/run_agent_review_patch_bundle_builder_smoke.py` |
| 244 | `Tools/validation/run_agent_runtime_tool_broker_smoke.py` |
| 240 | `Scripting/v61b_backgood/fog_dynamics.py` |
| 240 | `Tools/ai/review_wave_entrypoints.py` |
| 239 | `Tools/ai/build_github_evidence_bundle.py` |
| 238 | `Tools/npu/run_ollama_music_agent.py` |
| 238 | `Tools/validation/check_selective_execution_plan.py` |
| 237 | `Tools/validation/run_agent_review_warning_policy_smoke.py` |
| 235 | `Tools/validation/generated_file_policy.py` |
| 234 | `Tools/validation/run_agent_memory_routing_policy_smoke.py` |
| 233 | `Tools/ai/workload_quality.py` |
| 232 | `Tools/ai/replay_gpu_planner_json_contract.py` |
| 232 | `Tools/ai/smart_ai_gatekeeper.py` |
| 231 | `Tools/ai/enrich_github_evidence_bundle_code_plan.py` |
| 230 | `Tools/validation/check_ai_dry_run_matrix_outputs.py` |
| 229 | `Tools/validation/check_npu_knowledge_broker_packet.py` |
| 228 | `Tools/ai/github_evidence_bundle_markdown.py` |
| 227 | `Tools/ai/build_gpu0_companion_task_lane.py` |
| 223 | `Tools/ai/build_provider_runtime_heap_telemetry.py` |
| 221 | `Scripting/v61b/spaziotempo/core/registry.py` |
| 221 | `Tools/docs/apply_md_code_coherence_refactor.py` |
| 221 | `Tools/validation/check_file_line_limits.py` |
| 219 | `Tools/workflow/smart_ai_context.py` |
| 217 | `Tools/ai/artifact_domain_registry.py` |
| 212 | `Tools/validation/build_python_line_count_csv.py` |
| 209 | `Tools/validation/check_local_ai_enrichment_plan.py` |
| 209 | `Tools/validation/run_repository_consistency_map_smoke.py` |
| 208 | `Tools/ai/repository_consistency_map/paths.py` |
| 208 | `Tools/validation/check_docs_links.py` |
| 208 | `Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py` |
| 207 | `Tools/validation/check_core_activation_agnostic_contract.py` |
| 206 | `Scripting/v61b/hotpatch/render_patch.py` |
| 206 | `Scripting/v61b_backgood/hotpatch/render_patch.py` |
| 205 | `Tools/ai/code_patch_plan_common.py` |
| 204 | `Tools/ai/patch_unified_launcher_light_full0to10.py` |
| 204 | `Tools/validation/run_agent_review_evidence_sufficiency_smoke.py` |
| 204 | `Tools/validation/runtime_hardware_delegation_checks.py` |
| 203 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` |
| 203 | `Tools/validation/run_code_edit_proposal_smoke.py` |
| 201 | `Tools/ai/code_edit_proposal_helpers.py` |
| 201 | `Tools/validation/check_validation_report_contract.py` |
| 201 | `Tools/validation/run_agent_review_code_patch_plan_smoke.py` |
| 200 | `Scripting/v61b/main_v61b.py` |
| 200 | `Tools/ai/validate_ai_artifacts.py` |
| 198 | `Scripting/v61b/world_setup.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 196 | `Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py` |
| 191 | `Tools/ai/code_interpreter_report/scanner.py` |
| 190 | `Tools/validation/full_run_bundle_completeness.py` |
| 190 | `Tools/validation/report_utils.py` |
| 190 | `Tools/validation/run_runtime_tool_guidance_fallback_smoke.py` |
| 189 | `Tools/ai/check_npu_provider_environment.py` |
| 186 | `Tools/ai/build_workload_quality_lane_routing.py` |
| 186 | `Tools/validation/run_npu_runtime_tool_context_smoke.py` |
| 186 | `Tools/workflow/git_auto_push.py` |
| 185 | `Tools/ai/pipeline/remediation.py` |
| 185 | `Tools/validation/run_gpu_runner_provider_error_smoke.py` |
| 183 | `Tools/validation/check_ai_dry_run_matrix_cases.py` |
| 183 | `Tools/validation/run_schema_repair_retry_smoke.py` |
| 183 | `Tools/workflow/gui/components/action_panel.py` |
| 182 | `Tools/ai/run_local_provider_probe.py` |
| 182 | `Tools/workflow/gui/components/live_output_panel.py` |
| 181 | `Scripting/v61b_backgood/main_v61b.py` |
| 181 | `Tools/workflow/gui/workflow_gui_with_push.py` |
| 175 | `Tools/ai/provider_runtime_heap_validation_bridge.py` |
| 174 | `Scripting/v61b_backgood/world_setup.py` |
| 174 | `Tools/ai/build_openvino_hardware_governance_report.py` |
| 173 | `Tools/ai/runtime_tool_guidance.py` |
| 173 | `Tools/validation/check_generated_blender_script_policy.py` |
| 172 | `Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py` |
| 168 | `Tools/validation/run_schema_repair_context_smoke.py` |
| 167 | `Tools/ai/full_run_bundle_zip/builder.py` |
| 166 | `Tools/ai/repository_consistency_map/python_inventory.py` |
| 163 | `Tools/ai/full0to10_provider_telemetry_semantic/validator.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 161 | `Tools/ai/repository_consistency_map/builder.py` |
| 161 | `Tools/validation/run_npu_runtime_tool_execution_smoke.py` |
| 160 | `Tools/npu/npu_runtime.py` |
| 159 | `Scripting/v61b/fog_filaments.py` |
| 159 | `Tools/ai/github_evidence_bundle_io.py` |
| 159 | `Tools/validation/check_npu_decode_quality_remediation.py` |
| 159 | `Tools/validation/run_provider_empty_response_diagnostics_smo
```

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1585`
- SHA-256: `76dd638fee0692e6dd33f6f1e939f55c30942291b9aabbed865675f425bfc8b1`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Smoke

- Passed: `True`
- Case count: `7`
- Failed case count: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## `valid_recommendation`

- Passed: `True`
- Expected reason: ``
- Reason: ``
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`

## `tool_requests_pending`

- Passed: `True`
- Expected reason: `tool_requests_pending`
- Reason: `tool_requests_pending`
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `invalid_tool_request`

- Passed: `True`
- Expected reason: `model_output_schema_mismatch`
- Reason: `model_output_schema_mismatch`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `False`

## `evidence_ready_no_tool_request`

- Passed: `True`
- Expected reason: `evidence_ready_but_no_tool_requests`
- Reason: `evidence_ready_but_no_tool_requests`
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `malformed_json`

- Passed: `True`
- Expected reason: `json_parse_failure`
- Reason: `json_parse_failure`
- JSON OK: `False`
- Schema OK: `False`
- Context echo detected: `False`

## `schema_context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`


```

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1487`
- SHA-256: `d0f044b80c6e1d6797bf9c34875a8ef1b4045cc6392587ff084a34a99d942566`
- Content included: `True`
- Content truncated: `False`

```text
# Deterministic Recommendation Synthesizer Smoke

- Passed: `True`
- Recommendation count: `1`
- Deterministic synthesizer used: `True`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Synthesized report preview

# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `1`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `1`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### det_doc_code_001 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['AGENTS.md']`
- Rationale: The documentation points at a recommendation lane that must be normalized before patch-plan construction.
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Tools/ai/build_deterministic_recommendations.py` and update `AGENTS.md` only if the reference is stale or should point at an existing artifact. Prefer existing candidate `Tools/ai/build_agent_review_patch_plan.py` over inventing a new runtime artifact. Candidate references observed: `Tools/ai/build_agent_review_patch_plan.py`, `Tools/ai/gpu_planner_json_contract.py`.

## Guardrails

This report is deterministic and report-only. It is not a patch queue.

```

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `212`
- SHA-256: `ab8c829b5f099b245a1f6048441784a3a280a173d7787782e1288efabc3bec5e`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop Smoke

- Passed: `True`
- Return code: `0`
- Recommendation count: `1`
- Patch plan count: `1`
- Deterministic synthesizer used: `True`
- Patch application performed: `False`

```

### `output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `304`
- SHA-256: `ebcef793de1795cfc3f55063d9a02cad3467d28b6cee31e068b8067e70e75ded`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Provider Environment

- `passed`: `True`
- `npu_python`: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- `npu_python_exists`: `True`
- `openvino_import`: `True`
- `openvino_genai_import`: `True`
- `openvino_genai_pip_package`: `openvino-genai`
- `npu_available`: `True`

```

### `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `159`
- SHA-256: `8455a7e281c3444ba41667d4e2605150d6da8d2c304a1956e960597500296110`
- Content included: `True`
- Content truncated: `False`

```text
# GPU1 Primary Advisory

- Passed: `True`
- Provider execution performed: `True`
- Round count: `4`
- Recommendation count: `0`
- Classifications: `[]`

```

### `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `986`
- SHA-256: `d6d6d190549b30695038e7cadbadb482ee79ca49e9580a4d416482f42565a2db`
- Content included: `True`
- Content truncated: `False`

```text
# GPU0 Peer Companion Response

- Passed: `True`
- Provider execution performed: `True`
- Semantic mode: `semantic_model_unconfigured_numeric_tool_peer`
- Task count: `4`
- Response count: `4`
- Tool request count: `3`
- Classifications: `['gpu0_peer_semantic_model_unconfigured']`

## Responses

- `gpu0_peer_primary_advisory_quality` status=`ready` findings=`['Task can be handled with deterministic/broker evidence in this peer cycle.']`
- `gpu0_peer_runtime_tool_context` status=`ready` findings=`['Task can be handled with deterministic/broker evidence in this peer cycle.']`
- `gpu0_peer_patch_spec_readiness` status=`ready` findings=`['Task can be handled with deterministic/broker evidence in this peer cycle.']`
- `gpu0_peer_failed_report_triage` status=`ready` findings=`['Task can be handled with deterministic/broker evidence in this peer cycle.']`

## Warnings

- IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only.

```

### `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2572`
- SHA-256: `2042f8e0bd32362f575811a74b30f04bfbdd5766af22bca8f90233fc2c3d3000`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Runtime Tool Broker

- passed: `True`
- dry_run: `False`
- request_file: `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`
- request_kind: `gpu0_peer_tool_requests`
- source: `gpu0_peer_companion`
- source_classification: `gpu0_peer_companion`
- tool_request_count: `3`
- tool_execution_count: `3`
- blocked_tool_count: `0`
- failed_tool_count: `0`
- provider_execution_performed: `False`
- patch_application_performed: `False`
- sqlite_write_performed: `False`
- persistent_memory_write_performed: `False`
- operational_sqlite_write_performed: `False`
- operational_sqlite_write_count: `0`
- operational_memory_clear_count: `0`
- blender_runtime_execution_performed: `False`

## Tool results

### `gpu0_peer_code_interpreter_context` — `build_code_interpreter_report`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.json', 'markdown_report': 'output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.md'}`

### `gpu0_peer_report_contract_context` — `check_validation_report_contract`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_report_contract_context_validation_report_contract.json'}`

### `gpu0_peer_refactor_duplication_context` — `build_refactor_duplication_audit`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_refactor_duplication_context_refactor_duplication_audit.json', 'markdown_report': 'output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/gpu0_peer/gpu0_peer_refactor_duplication_context_refactor_duplication_audit.md'}`

## Guardrails

- `free_shell_exposed`: `False`
- `allowlist_enforced`: `True`
- `provider_execution_performed`: `False`
- `patch_application_performed`: `False`
- `sqlite_write_performed`: `False`
- `persistent_memory_write_performed`: `False`
- `operational_sqlite_write_allowed_under_output`: `True`
- `operational_sqlite_write_performed`: `False`
- `operational_memory_clear_count`: `0`
- `blender_runtime_touched`: `False`
- `git_write_performed`: `False`
- `manual_review_required`: `True`

```

### `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `368`
- SHA-256: `833452c6ebaca9f56b3382a3da41d7d40d9ae98947606d4b0fbe5a736e2d11f5`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Micro Peer Assistant

- Passed: `True`
- Provider execution requested: `False`
- Provider execution performed: `False`
- Non-blocking: `True`
- Mode: `deferred`
- Classification: `npu_peer_provider_deferred_to_avoid_openvino_contention`
- Reason: NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.

```

### `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `280`
- SHA-256: `4add8370766a66f6ad234c0777ee6316e238ab2af77a83d0bdd6c5c592d724d1`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Micro Runtime Tool Broker

- Passed: `True`
- Executed: `False`
- Tool execution count: `0`
- Classification: `npu_peer_provider_deferred_noop_broker`
- Reason: NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.

```

### `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1192`
- SHA-256: `11242ce1279e1995b4c882843d56f94a56525ff99581c8b89c58e50f6ab198da`
- Content included: `True`
- Content truncated: `False`

```text
# AI Peer Exchange

- Passed: `True`
- Provider execution performed: `True`
- Classifications: `['gpu0_peer_semantic_model_unconfigured']`
- Task count: `4`
- GPU0 response passed: `True`
- Broker executions: `3`
- NPU micro lane seen: `True`
- NPU broker executions: `0`
- Peer mesh all lanes visible: `True`
- NPU support tool supply: `False`
- NPU slow/degraded non-blocking: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`
- Provider-broker loop active: `True`
- Provider-broker controlled executor: `runtime_tool_broker`
- Provider-broker direct tool execution allowed: `False`
- Provider-broker topology: `input_md -> deterministic_baseline -> GPU1 -> GPU0 -> broker -> NPU_support -> broker -> contract -> telemetry -> bundle -> patch_plan`
- Provider-broker GPU0 executions: `3`
- Provider-broker NPU executions: `0`

```

### `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2552`
- SHA-256: `63b7c69ccaef42de46774d1ddbd222097de9403d84a93aad79f52b8c9e77c7ad`
- Content included: `True`
- Content truncated: `False`

```text
# AI Peer Exchange Contract

- Passed: `True`
- Provider execution performed: `True`
- Classifications: `['peer_mesh_degraded_lanes_present_non_blocking', 'gpu0_peer_semantic_model_unconfigured']`

## Evidence

- `gpu1_primary_advisory` exists=`True` passed=`True` path=`output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`
- `gpu0_peer_task_packet` exists=`True` passed=`True` path=`output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json`
- `gpu0_peer_response` exists=`True` passed=`True` path=`output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`
- `gpu0_tool_requests` exists=`True` passed=`None` path=`output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`
- `gpu0_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- `npu_micro_response` exists=`True` passed=`True` path=`output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`
- `npu_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- `ai_peer_exchange` exists=`True` passed=`True` path=`output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`

## Peer mesh visibility

- Passed: `True`
- GPU1 sees GPU0 response: `True`
- GPU1 sees NPU support signal: `True`
- GPU0 sees GPU1 primary advisory: `True`
- NPU sees GPU1/GPU0/broker context: `True`
- NPU support tool supply: `False`
- NPU slow/degraded non-blocking: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`

## Provider-broker loop

- Passed: `True`
- Active: `True`
- Controlled executor: `runtime_tool_broker`
- Direct tool execution allowed: `False`
- Broker tool executions: `3`
- GPU0 broker executions: `3`
- NPU broker executions: `0`
- NPU non-blocking: `True`
- NPU product pass blocker: `False`
- Deterministic scripts heavy audit authority: `True`
- Product blockers: `[]`

## Warnings

- gpu0_peer_semantic_model_unconfigured

```

### `output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `308`
- SHA-256: `2143ea48a3ec3e60f825e53c855ad2763749797241b0bcece0b6de9cf9129b7e`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `patch_quality_product_probe_20260507-133119`
- mode: `init`
- event_count: `1`
- heap_event_count: `1`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `317`
- SHA-256: `39505d921f837340642180397a0f97e5c20337a0b09b53879219b5f63995865d`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `patch_quality_product_probe_20260507-133119`
- mode: `gpu1-request`
- event_count: `1`
- heap_event_count: `13`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `319`
- SHA-256: `cb612b56344462950625629ede0810436bd01eaf5d7e3a16bcca2df89d5eeb59`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `patch_quality_product_probe_20260507-133119`
- mode: `broker-results`
- event_count: `3`
- heap_event_count: `20`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `316`
- SHA-256: `d1f4af305b48b9e8a7d9c22947ac2fbe72647def537c6cfc32f20bbdf512bb0d`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `patch_quality_product_probe_20260507-133119`
- mode: `npu-support`
- event_count: `1`
- heap_event_count: `21`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`

```

### `output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1187`
- SHA-256: `98fb493f0c05adc084c975124172ae3d88e32f65394f601a53a140e3a91ec40c`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap From Peer Reports

- passed: `True`
- stamp: `patch_quality_product_probe_20260507-133119`
- event_count: `11`
- heap_event_count: `32`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`

## Reports

- `gpu1`: `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`
- `gpu0`: `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`
- `gpu0_tool_requests`: `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`
- `gpu0_broker`: `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- `npu`: `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`
- `npu_broker`: `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- `peer_exchange`: `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`
- `peer_contract`: `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json`

```

### `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2493`
- SHA-256: `92257aa5a2499b1abd1daf4f8b15356114edd356126c514e3c8697c14ec6188d`
- Content included: `True`
- Content truncated: `False`

```text
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

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2202`
- SHA-256: `fd4e97b659b885dd70f80c9ceaf9e8f8109cc1c6ff0548e8a0c1e22785a683af`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `patch_quality_product_probe_20260507-133119`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- NPU provider execution performed: `False`
- Provider degraded reasons: `['npu_auditor_not_confirmed:audit_count=0;success_count=0;lane_mode=metadata_only']`
- Tool call entries: `6`
- Executed count: `6`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `0.0`
- Declared runtime tool requests: `15`
- Declared runtime tool executions: `7`
- Broker runtime tool executions: `6`
- Declared not executed count: `8`

## By caller AI

- `orchestrator`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu0`: count=`3` executed=`3` failed=`0` elapsed=`0.0`

## By phase

- `explicit_runtime_tool_broker_bootstrap`: count=`3` executed=`3` failed=`0` elapsed=`0.0`
- `gpu0_peer_runtime_tool_broker`: count=`3` executed=`3` failed=`0` elapsed=`0.0`

## By tool

- `check_python_syntax`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_python_line_count_csv`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `check_validation_report_contract`: count=`2` executed=`2` failed=`0` elapsed=`0.0`
- `build_code_interpreter_report`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_refactor_duplication_audit`: count=`1` executed=`1` failed=`0` elapsed=`0.0`

## First tool call entries

- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`build_python_line_count_csv` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_code_interpreter_report` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`
- `gpu0` `gpu0_peer_runtime_tool_broker` round=`2` tool=`build_refactor_duplication_audit` status=`None` elapsed=`0.0`


```

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7682`
- SHA-256: `c1650f156ec709d94b2e36aaadf73c03871c590b008e91e78593e537750790c8`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Capability Manifest

- Passed: `True`
- Tool count: `10`
- Declared runtime tool requests: `15`
- Broker runtime tool executions: `7`
- Declared not executed count: `8`
- Provider execution performed: `False`
- Patch application performed: `False`

## Cloud handoff policy

- `include_with_evidence_chunks`: `True`
- `include_runtime_usage_telemetry`: `True`
- `include_patch_plan_and_recommendations`: `True`
- `no_free_shell`: `True`
- `tool_execution_requires_local_broker`: `True`
- `cloud_model_may_reason_about_tools_but_must_not_execute_them`: `True`

## Caller modes

- Supported callers: `['gpu', 'npu', 'orchestrator', 'ollama-local', 'deterministic']`
- Rule: cloud receives capability manifest plus runtime usage telemetry; local execution remains broker-controlled

## Tools

### `build_agent_agnostic_tool_inventory`

- Category: `inventory`
- Safe mode: `report-only`
- Description: Inventory existing reusable IA-Carmine tools and guardrails.
- Allowed args: `['root']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_agent_memory_inventory`

- Category: `inventory`
- Safe mode: `report-only`
- Description: Read-only SQLite/JSONL agent memory inventory.
- Allowed args: `['objective', 'memory_db']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_agent_transient_request_context`

- Category: `context`
- Safe mode: `report-only`
- Description: Build request-scoped context from memory notes, raw files and reports.
- Allowed args: `['objective', 'memory_note', 'raw_file', 'report_file']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_code_interpreter_report`

- Category: `static_analysis`
- Safe mode: `report-only`
- Description: Build static code-interpreter style report over selected roots.
- Allowed args: `['input']`
- Usage observed: `{'count': 2, 'executed': 2, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_python_line_count_csv`

- Category: `inventory`
- Safe mode: `report-only`
- Description: Build full Python line-count CSV/JSON/MD evidence.
- Allowed args: `['exclude_dir']`
- Usage observed: `{'count': 2, 'executed': 2, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `build_refactor_duplication_audit`

- Category: `refactor_analysis`
- Safe mode: `report-only`
- Description: Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.
- Allowed args: `['root', 'report', 'input_audit_report', 'line_count_report', 'code_interpreter_report', 'python_syntax_report', 'bundle_smoke_report', 'memory_routing_report']`
- Usage observed: `{'count': 2, 'executed': 2, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `check_python_syntax`

- Category: `validation`
- Safe mode: `report-only`
- Description: Validate Python syntax across repository.
- Allowed args: `[]`
- Usage observed: `{'count': 2, 'executed': 2, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `check_validation_report_contract`

- Category: `validation`
- Safe mode: `report-only`
- Description: Validate validation report contract for a scoped report-dir or explicit report files.
- Allowed args: `['report_file']`
- Usage observed: `{'count': 4, 'executed': 4, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `run_gpu_planner_json_contract_smoke`

- Category: `validation`
- Safe mode: `report-only`
- Description: Run GPU planner JSON contract smoke tests without provider.
- Allowed args: `[]`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - no SQLite or persistent memory write

### `runtime_sqlite_memory`

- Category: `memory_status`
- Safe mode: `controlled read-only/status by default; persistent write requires explicit confirm`
- Description: Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.
- Allowed args: `['action', 'scope', 'database', 'persistent_database', 'summary', 'content', 'role', 'tag', 'query', 'limit', 'confirm', 'allow_persistent_write']`
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
- Guardrails:
  - no free shell exposure
  - broker allowlist required
  - no provider execution
  - no patch application
  - no Blender runtime execution
  - no Git writes
  - persistent memory write requires allow_persistent_write=true and confirm=persistent_write
  - operational scratch writes allowed only under output/** when broker-controlled

## Source files

- `Tools/ai/agent_runtime_tool_broker.py` role=`runtime_tool_broker_allowlist_source` exists=`True` sha256=`9dd4d5307a1bb63ef5da341d0ac7bf44df1c7270018a011f9f6e8a30e153eca8`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` role=`runtime_tool_usage_telemetry_builder` exists=`True` sha256=`3be03865ef3b906dd9587b0a4cbe4348217000e1083464929a5e5a2048a2fa3b`
- `Tools/ai/build_semantic_evidence_chunks.py` role=`semantic_cloud_handoff_chunker` exists=`True` sha256=`5fdcbc74f6eb931f3b95c6b54b1eb1071e57f8f41a34c694864b3ac8cdab80f7`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` role=`shared_toolbox_bundle_builder` exists=`True` sha256=`346f8bef6e54135ce297b99dd84a983268bea703a38bab373f51d8eb4634652a`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json` role=`observed_runtime_tool_usage_report` exists=`True` sha256=`d15007219a343a237392b38f72315144bdf5bdf1902e038d75d09c0eca0c61fd`

```

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1214`
- SHA-256: `3de77760ff64f3a96e057f16c2b5e517907dae356cac04014a521c37ed562b33`
- Content included: `True`
- Content truncated: `False`

```text
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

```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `570779`
- SHA-256: `629f30bb8a690f6bdaf6f0e67e7453223be126bfe30934f308571c2b9a30bc0d`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: patch_quality_product_probe_20260507-133119
- passed: True
- provider_execution_performed: True
- patch_application_performed: False
- source_writes_performed: False
- sqlite_write_performed: False
- persistent_memory_write_performed: False
- blender_runtime_execution_performed: False

## Provider diagnostics

- Provider execution seen: `True`
- GPU primary advisory succeeded: `True`
- Provider failure detected: `True`
- Deterministic recovery used: `True`
- Provider advisory state: `primary_gpu_advisory_succeeded`
- Provider failure reasons:
  - output/validation/local_provider_probe.json: ollama: probe failed

## Peer mesh product state

- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'provider_runtime_heap_blackboard', 'deterministic_scripts']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'provider_runtime_heap_broker_results']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`
- Legacy usable lanes are workload quality only: `True`
- NPU degraded is product blocker: `False`
- NPU heavy audit authority: `False`

- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json` kind=`agent_gpu_npu_parallel_orchestrator` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`True` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/local_provider_probe.json` kind=`local_provider_probe` passed=`False` source=`None` source_classification=`None` provider_execution_performed=`True` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`['ollama: probe failed']`
- `output/validation/ai_workload_report_quality.json` kind=`ai_workload_report_quality` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`False` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json` kind=`gpu1_primary_advisory` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`True` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json` kind=`gpu0_peer_response` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`True` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json` kind=`agent_runtime_tool_broker` passed=`True` source=`gpu0_peer_companion` source_classification=`gpu0_peer_companion` provider_execution_performed=`False` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json` kind=`agent_runtime_tool_broker` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`False` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json` kind=`ai_peer_exchange` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`True` collaboration_visibility=`True` peer_mesh=`True` npu_support=`True` errors=`[]`
- `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json` kind=`ai_peer_exchange_contract` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`True` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json` kind=`provider_runtime_heap_live_signals` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`None` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json` kind=`provider_runtime_heap_live_signals` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`None` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`
- `output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json` kind=`provider_runtime_heap_live_signals` passed=`True` source=`None` source_classification=`None` provider_execution_performed=`None` collaboration_visibility=`None` peer_mesh=`False` npu_support=`False` errors=`[]`

## Patch plan summary

- Seen: `True`
- Source: `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json`
- Patch plan count: `20`
- Manual review required: `None`
- Patch application performed: `False`

## Tools available

### build_agent_agnostic_tool_inventory

- Category: inventory
- Safe default mode: report-only
- Recommended next use: Discover reusable tooling before adding new scripts.
- Allowed args: `['root']`
- Can do:
  - Inventory existing reusable IA-Carmine tools and guardrails.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_agent_memory_inventory

- Category: inventory
- Safe default mode: report-only
- Recommended next use: Summarize durable project memory as read-only context.
- Allowed args: `['objective', 'memory_db']`
- Can do:
  - Read-only SQLite/JSONL agent memory inventory.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_agent_transient_request_context

- Category: context
- Safe default mode: report-only
- Recommended next use: Assemble request-scoped context for local AI planning.
- Allowed args: `['objective', 'memory_note', 'raw_file', 'report_file']`
- Can do:
  - Build request-scoped context from memory notes, raw files and reports.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_code_interpreter_report

- Category: static_analysis
- Safe default mode: report-only
- Recommended next use: Build static analysis/refactor evidence.
- Allowed args: `['input']`
- Can do:
  - Build static code-interpreter style report over selected roots.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_python_line_count_csv

- Category: inventory
- Safe default mode: report-only
- Recommended next use: Refresh complete Python inventory before refactor planning.
- Allowed args: `['exclude_dir']`
- Can do:
  - Build full Python line-count CSV/JSON/MD evidence.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### build_refactor_duplication_audit

- Category: support_tool
- Safe default mode: report-only
- Recommended next use: Use through the runtime tool broker when a report-only request requires it.
- Allowed args: `['root', 'report', 'input_audit_report', 'line_count_report', 'code_interpreter_report', 'python_syntax_report', 'bundle_smoke_report', 'memory_routing_report']`
- Can do:
  - Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### check_python_syntax

- Category: validation
- Safe default mode: report-only
- Recommended next use: Gate Python source changes.
- Allowed args: `[]`
- Can do:
  - Validate Python syntax across repository.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### check_validation_report_contract

- Category: validation
- Safe default mode: report-only
- Recommended next use: Gate report quality before evidence bundling.
- Allowed args: `['report_file']`
- Can do:
  - Validate validation report contract for a scoped report-dir or explicit report files.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### run_gpu_planner_json_contract_smoke

- Category: validation
- Safe default mode: report-only
- Recommended next use: Validate planner JSON contract without providers.
- Allowed args: `[]`
- Can do:
  - Run GPU planner JSON contract smoke tests without provider.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write SQLite or persistent memory

### runtime_sqlite_memory

- Category: memory_status
- Safe default mode: controlled read-only/status by default
- Recommended next use: Read memory status/search through broker-controlled actions.
- Allowed args: `['action', 'scope', 'database', 'persistent_database', 'summary', 'content', 'role', 'tag', 'query', 'limit', 'confirm', 'allow_persistent_write']`
- Can do:
  - Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.
- Must not do:
  - execute arbitrary shell commands
  - apply patches
  - run Blender runtime
  - commit output artifacts
  - write persistent memory without explicit confirmation and authorization

## Tool requests executed or proposed

- gpu0_peer_code_interpreter_context: build_code_interpreter_report - GPU0 peer worker needs current code-structure context through the broker allowlist.
- gpu0_peer_report_contract_context: check_validation_report_contract - GPU0 peer worker needs report-contract status for the evidence it received.
- gpu0_peer_refactor_duplication_context: build_refactor_duplication_audit - GPU0 peer worker needs deterministic reuse/refactor overlap evidence.

## Reports generated

- output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json exists=True json_ok=True kind=agent_review_decision_loop passed=True
- output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json exists=True json_ok=True kind=agent_review_patch_plan passed=True
- output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer passed=True
- output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json exists=True json_ok=True kind=deterministic_recommendation_patch_plan_bridge_orchestrator passed=True
- output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json exists=True json_ok=True kind=agent_gpu_npu_parallel_orchestrator passed=True
- output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json exists=True json_ok=True kind=agent_gpu_deep_planning_supervised passed=True
- output/validation/local_provider_probe.json exists=True json_ok=True kind=local_provider_probe passed=False
- output/validation/ai_workload_report_quality.json exists=True json_ok=True kind=ai_workload_report_quality passed=True
- output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=repository_consistency_map passed=True
- output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=repository_consistency_map_smoke passed=True
- output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=code_interpreter_report passed=True
- output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=python_line_count_csv passed=True
- output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=python_syntax passed=True
- output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=gpu_planner_json_contract_smoke passed=True
- output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer_smoke passed=True
- output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=agent_review_decision_loop_smoke passed=True
- output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=npu_provider_environment passed=True
- output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=gpu1_primary_advisory passed=True
- output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=gpu0_peer_task_packet passed=True
- output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json exists=True json_ok=True kind=gpu0_peer_response passed=True
- output/validation/gpu0_tool_requests_patch_qual
```

### `output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `2129738`
- SHA-256: `ecf26290d014dec76280c0f5d26360402c8cab1be1bb9a605adcecee1e4b352c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-07T13:31:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 601,
  "parsed_file_count": 601,
  "total_lines": 101948,
  "total_functions": 3667,
  "total_classes": 101,
  "total_risk_signals": 90,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 989
    },
    {
      "module": "__future__",
      "count": 541
    },
    {
      "module": "pathlib",
      "count": 420
    },
    {
      "module": "typing",
      "count": 376
    },
    {
      "module": "config",
      "count": 320
    },
    {
      "module": "json",
      "count": 300
    },
    {
      "module": "argparse",
      "count": 257
    },
    {
      "module": "sys",
      "count": 195
    },
    {
      "module": "datetime",
      "count": 179
    },
    {
      "module": "constants",
      "count": 151
    },
    {
      "module": "report_utils",
      "count": 88
    },
    {
      "module": "subprocess",
      "count": 68
    },
    {
      "module": "dataclasses",
      "count": 61
    },
    {
      "module": "re",
      "count": 50
    },
    {
      "module": "workflow_state",
      "count": 45
    },
    {
      "module": "paths",
      "count": 42
    },
    {
      "module": "os",
      "count": 32
    },
    {
      "module": "bpy",
      "count": 30
    },
    {
      "module": "pipeline",
      "count": 28
    },
    {
      "module": "common",
      "count": 26
    },
    {
      "module": "agent_state",
      "count": 26
    },
    {
      "module": "io_utils",
      "count": 23
    },
    {
      "module": "tkinter",
      "count": 23
    },
    {
      "module": "hashlib",
      "count": 22
    },
    {
      "module": "full0to10_sqlite_memory",
      "count": 19
    },
    {
      "module": "time",
      "count": 18
    },
    {
      "module": "models",
      "count": 16
    },
    {
      "module": "ollama_runtime",
      "count": 16
    },
    {
      "module": "py_support",
      "count": 16
    },
    {
      "module": "components",
      "count": 15
    },
    {
      "module": "math",
      "count": 14
    },
    {
      "module": "concurrent",
      "count": 14
    },
    {
      "module": "materials",
      "count": 13
    },
    {
      "module": "sqlite3",
      "count": 13
    },
    {
      "module": "ast",
      "count": 13
    },
    {
      "module": "builder",
      "count": 13
    },
    {
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "collections",
      "count": 12
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "render",
      "count": 11
    }
  ],
  "largest_files": [
    {
      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
      "line_count": 2263,
      "risk": "high"
    },
    {
      "path": "Tools/npu/run_dual_ai_pipeline.py",
      "line_count": 1774,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b/scene_tuning_panel.py",
      "line_count": 1262,
      "risk": "high"
    },
    {
      "path": "Tools/workflow/workflow_state.py",
      "line_count": 1230,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
      "line_count": 1180,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 1100,
      "risk": "high"
    },
    {
      "path": "Scripting/v61b/animation.py",
      "line_count": 1079,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_deterministic_recommendations.py",
      "line_count": 909,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 902,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "line_count": 823,
      "risk": "high"
    },
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "line_count": 759,
      "risk": "medium"
    },
    {
      "path": "Tools/workflow/gui/workflow_gui.py",
      "line_count": 738,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/physics_setup.py",
      "line_count": 737,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/asset_setup.py",
      "line_count": 725,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_refactor_duplication_audit.py",
      "line_count": 725,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/build_music_context.py",
      "line_count": 711,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_npu_gpu_deep_review_auditor.py",
      "line_count": 694,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/materials.py",
      "line_count": 657,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_peer_exchange_packet.py",
      "line_count": 642,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/run_npu_review.py",
      "line_count": 631,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_npu_pipeline_modules.py",
      "line_count": 627,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_plan.py",
      "line_count": 626,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_selective_execution_plan.py",
      "line_count": 618,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_bundle.py",
      "line_count": 608,
      "risk": "medium"
    },
    {
      "path": "Tools/workflow/workflow_debug.py",
      "line_count": 607,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "line_count": 587,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_context_pack.py",
      "line_count": 579,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_pipeline_dry_run_matrix.py",
      "line_count": 573,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_full_toolbox_run_telemetry_summary.py",
      "line_count": 567,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "low": 420,
    "medium": 171,
    "high": 10
  },
  "recommendation_count": 185,
  "recommendations": [
    {
      "id": "code_static_001",
      "target_file": "Scripting/shared/image_sequence.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\shared\\image_sequence.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_002",
      "target_file": "Scripting/v61b/animation.py",
      "risk": "high",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\animation.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_003",
      "target_file": "Scripting/v61b/asset_setup.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\asset_setup.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_004",
      "target_file": "Scripting/v61b/atmosphere_setup.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\atmosphere_setup.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_005",
      "target_file": "Scripting/v61b/config.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\config.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_006",
      "target_file": "Scripting/v61b/encode_ffmpeg_v61b.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected",
        "static risk calls detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\encode_ffmpeg_v61b.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_007",
      "target_file": "Scripting/v61b/encode_image_sequence_v61b.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\encode_image_sequence_v61b.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_008",
      "target_file": "Scripting/v61b/fog_dynamics.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\fog_dynamics.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_009",
      "target_file": "Scripting/v61b/hotpatch/accent_patch.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\hotpatch\\accent_patch.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_010",
      "target_file": "Scripting/v61b/hotpatch/diagnostics.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Scripting\\v61b\\hotpatch\\diagnostics.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-roo
```

### `output/analysis/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_code_interpreter.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1947394`
- SHA-256: `63cad0ede1a6e843a4411b805522427ca7e326bb3c212a334031a5778c36acb4`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-07T13:31:32",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 559,
  "parsed_file_count": 559,
  "total_lines": 91343,
  "total_functions": 3386,
  "total_classes": 79,
  "total_risk_signals": 78,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 989
    },
    {
      "module": "__future__",
      "count": 534
    },
    {
      "module": "pathlib",
      "count": 404
    },
    {
      "module": "typing",
      "count": 370
    },
    {
      "module": "json",
      "count": 294
    },
    {
      "module": "argparse",
      "count": 257
    },
    {
      "module": "sys",
      "count": 189
    },
    {
      "module": "datetime",
      "count": 179
    },
    {
      "module": "constants",
      "count": 151
    },
    {
      "module": "report_utils",
      "count": 88
    },
    {
      "module": "subprocess",
      "count": 66
    },
    {
      "module": "dataclasses",
      "count": 57
    },
    {
      "module": "re",
      "count": 47
    },
    {
      "module": "workflow_state",
      "count": 45
    },
    {
      "module": "paths",
      "count": 42
    },
    {
      "module": "os",
      "count": 30
    },
    {
      "module": "pipeline",
      "count": 28
    },
    {
      "module": "agent_state",
      "count": 26
    },
    {
      "module": "tkinter",
      "count": 23
    },
    {
      "module": "hashlib",
      "count": 22
    },
    {
      "module": "io_utils",
      "count": 20
    },
    {
      "module": "full0to10_sqlite_memory",
      "count": 19
    },
    {
      "module": "time",
      "count": 17
    },
    {
      "module": "models",
      "count": 16
    },
    {
      "module": "ollama_runtime",
      "count": 16
    },
    {
      "module": "py_support",
      "count": 16
    },
    {
      "module": "components",
      "count": 15
    },
    {
      "module": "concurrent",
      "count": 14
    },
    {
      "module": "sqlite3",
      "count": 13
    },
    {
      "module": "ast",
      "count": 13
    },
    {
      "module": "builder",
      "count": 13
    },
    {
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "collections",
      "count": 12
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "render",
      "count": 11
    },
    {
      "module": "defaults",
      "count": 11
    },
    {
      "module": "openvino",
      "count": 9
    },
    {
      "module": "npu_runtime",
      "count": 9
    },
    {
      "module": "artifact_paths",
      "count": 9
    },
    {
      "module": "providers",
      "count": 8
    }
  ],
  "largest_files": [
    {
      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
      "line_count": 2263,
      "risk": "high"
    },
    {
      "path": "Tools/npu/run_dual_ai_pipeline.py",
      "line_count": 1774,
      "risk": "high"
    },
    {
      "path": "Tools/workflow/workflow_state.py",
      "line_count": 1230,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
      "line_count": 1180,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 1100,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_deterministic_recommendations.py",
      "line_count": 909,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 902,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "line_count": 823,
      "risk": "high"
    },
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "line_count": 759,
      "risk": "medium"
    },
    {
      "path": "Tools/workflow/gui/workflow_gui.py",
      "line_count": 738,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_refactor_duplication_audit.py",
      "line_count": 725,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/build_music_context.py",
      "line_count": 711,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_npu_gpu_deep_review_auditor.py",
      "line_count": 694,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_peer_exchange_packet.py",
      "line_count": 642,
      "risk": "medium"
    },
    {
      "path": "Tools/npu/run_npu_review.py",
      "line_count": 631,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_npu_pipeline_modules.py",
      "line_count": 627,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_plan.py",
      "line_count": 626,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_selective_execution_plan.py",
      "line_count": 618,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_bundle.py",
      "line_count": 608,
      "risk": "medium"
    },
    {
      "path": "Tools/workflow/workflow_debug.py",
      "line_count": 607,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "line_count": 587,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_context_pack.py",
      "line_count": 579,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_pipeline_dry_run_matrix.py",
      "line_count": 573,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_full_toolbox_run_telemetry_summary.py",
      "line_count": 567,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_semantic_evidence_chunks.py",
      "line_count": 562,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/suggest_repository_updates.py",
      "line_count": 551,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_state.py",
      "line_count": 544,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_runtime_sqlite_memory.py",
      "line_count": 527,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_megalithic_repo_review.py",
      "line_count": 519,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "medium": 154,
    "low": 397,
    "high": 8
  },
  "recommendation_count": 166,
  "recommendations": [
    {
      "id": "code_static_001",
      "target_file": "Tools/ai/agent_memory_policy.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_memory_policy.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_002",
      "target_file": "Tools/ai/agent_memory_routing_policy.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_memory_routing_policy.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_003",
      "target_file": "Tools/ai/agent_review_warning_policy.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_review_warning_policy.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_004",
      "target_file": "Tools/ai/agent_runtime_sqlite_memory.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_runtime_sqlite_memory.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_005",
      "target_file": "Tools/ai/agent_runtime_tool_broker.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected",
        "static risk calls detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_runtime_tool_broker.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_006",
      "target_file": "Tools/ai/agent_state.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\agent_state.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_007",
      "target_file": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\analyze_gpu_npu_run_sync.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_008",
      "target_file": "Tools/ai/build_agent_agnostic_tool_inventory.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_agnostic_tool_inventory.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_009",
      "target_file": "Tools/ai/build_agent_memory_inventory.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "large functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_memory_inventory.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_010",
      "target_file": "Tools/ai/build_agent_review_code_patch_plan.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_r
```

### `output/analysis/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_code_interpreter.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7350`
- SHA-256: `3fbb1bdcef3e16612aee1ffcad01edc8454e05b6b06b5339da902478464be654`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `559`
- Parsed files: `559`
- Total lines: `91343`
- Total functions: `3386`
- Total classes: `79`
- Risk signals: `78`
- TODO/FIXME markers: `21`
- Recommendation count: `166`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` - `2263` lines, risk `high`
- `Tools/npu/run_dual_ai_pipeline.py` - `1774` lines, risk `high`
- `Tools/workflow/workflow_state.py` - `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` - `1180` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` - `1100` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` - `909` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` - `902` lines, risk `high`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` - `823` lines, risk `high`
- `Tools/ai/agent_runtime_tool_broker.py` - `759` lines, risk `medium`
- `Tools/workflow/gui/workflow_gui.py` - `738` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` - `725` lines, risk `medium`
- `Tools/npu/build_music_context.py` - `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` - `694` lines, risk `medium`
- `Tools/ai/build_ai_peer_exchange_packet.py` - `642` lines, risk `medium`
- `Tools/npu/run_npu_review.py` - `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` - `627` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` - `626` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` - `618` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_bundle.py` - `608` lines, risk `medium`
- `Tools/workflow/workflow_debug.py` - `607` lines, risk `medium`

## Recommendations

- `code_static_001` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_002` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_003` `Tools/ai/agent_review_warning_policy.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_006` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_007` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module
- `code_static_008` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_009` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_010` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_011` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_012` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_013` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_014` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_015` `Tools/ai/build_ai_peer_exchange_packet.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_017` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_018` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_019` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_020` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_021` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_022` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_023` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Tools/ai/build_provider_runtime_heap_from_peer_reports.py` risk `medium`: large functions detected, complex functions detected
- `code_static_025` `Tools/ai/build_refactor_duplication_audit.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_026` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_027` `Tools/ai/build_runtime_tool_capability_manifest.py` risk `medium`: complex functions detected
- `code_static_028` `Tools/ai/build_runtime_tool_usage_telemetry.py` risk `high`: large Python module, complex functions detected
- `code_static_029` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_030` `Tools/ai/build_semantic_evidence_chunks.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_031` `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_033` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_034` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_035` `Tools/ai/code_interpreter_report/builder.py` risk `low`: TODO/FIXME markers detected
- `code_static_036` `Tools/ai/code_interpreter_report/constants.py` risk `low`: TODO/FIXME markers detected
- `code_static_037` `Tools/ai/code_interpreter_report/render.py` risk `low`: TODO/FIXME markers detected
- `code_static_038` `Tools/ai/code_interpreter_report/scanner.py` risk `low`: TODO/FIXME markers detected
- `code_static_039` `Tools/ai/full0to10_accelerator_control/device_visibility.py` risk `medium`: complex functions detected
- `code_static_040` `Tools/ai/full0to10_final_product/builder.py` risk `medium`: large functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `6376`
- SHA-256: `e3745d67a12053f5438d9605ab6e5740e96ae01d91fd8cd72c03fe1990edd8b9`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_planner_json_contract_replay",
  "generated_at": "2026-05-07T13:33:23",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "blender_runtime_execution_performed": false,
  "sqlite_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "gpu_report": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json"
  },
  "source_summary": {
    "kind": "agent_gpu_deep_planning_supervised",
    "passed": true,
    "round_count": 4,
    "recommendation_count": 0,
    "json_parse_error_count": 0,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "model_output_schema_mismatch",
    "evidence_ready_for_manual_patch_count": 0
  },
  "replayed_round_count": 4,
  "contract_reason_counts": {
    "model_output_schema_mismatch": 4
  },
  "context_echo_detected_count": 0,
  "json_parse_failure_count": 0,
  "model_output_schema_mismatch_count": 4,
  "valid_recommendation_output_count": 0,
  "rounds": [
    {
      "round": 1,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 382,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "91d5d16c83cf950eeabab1c1c5958e519bdc625156d61b7c3c244e7e7f6b3f86",
        "raw_response_chars": 382,
        "top_level_keys": [
          "apply_mode",
          "code_patch_plans",
          "errors",
          "kind",
          "manual_review_required",
          "passed",
          "patch_application_performed",
          "patch_plan_count",
          "provider_execution_performed",
          "schema_version",
          "source_writes_performed",
          "warnings"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      }
    },
    {
      "round": 2,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 1014,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "53f83791776a33e0408f8c2f2cf959ebc4120d876c2812f39288b9571c69c282",
        "raw_response_chars": 1014,
        "top_level_keys": [
          "decision",
          "file_count",
          "forbidden_path_count",
          "included_file_count",
          "included_paths",
          "kind",
          "passed",
          "profile",
          "provider_execution_performed",
          "required_missing",
          "schema_version",
          "source_pack",
          "truncated_file_count"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      }
    },
    {
      "round": 3,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 70,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "50a2eed61fec792f17f6fa74a4e3ebd3efec834b87a7281f59dfe110c161f763",
        "raw_response_chars": 70,
        "top_level_keys": [
          "response"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      }
    },
    {
      "round": 4,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 70,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "50a2eed61fec792f17f6fa74a4e3ebd3efec834b87a7281f59dfe110c161f763",
        "raw_response_chars": 70,
        "top_level_keys": [
          "response"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      }
    }
  ],
  "decision": {
    "contract_helper_replay_available": true,
    "safe_to_wire_runner_after_replay": true,
    "recommended_next_layer": "wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py",
    "manual_review_required": true
  },
  "guardrails": {
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "blender_runtime_execution_performed": false,
    "sqlite_write_performed": false,
    "manual_review_required": true
  }
}

```

### `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `606`
- SHA-256: `ade444a4d7002868f8529cb9b2c5e7a8ebf09a6b78014fc2b3c7286211cd8b8e`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `4`
- Context echo detected: `0`
- JSON parse failures: `0`
- Schema mismatches: `4`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `model_output_schema_mismatch`: `4`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5238`
- SHA-256: `60600cb5f05992f6f5bbb6b700a0312dd025899f469e59d7663ddb828c2c16c9`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-07T13:33:23",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "blender_runtime_execution_performed": false,
  "sqlite_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "orchestrator": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 4,
    "npu_audit_count": 0,
    "legacy_npu_audit_count": 0,
    "npu_micro_support_count": 0,
    "npu_micro_support_overlap_count": 0,
    "gpu0_peer_support_count": 5,
    "gpu0_peer_support_overlap_count": 4,
    "npu_audit_success_count": 0,
    "npu_audit_round_coverage": 0.0,
    "avg_gpu_round_seconds": 15.424,
    "p50_gpu_round_seconds": 15.424,
    "p90_gpu_round_seconds": 15.424,
    "avg_npu_audit_seconds": 0.0,
    "p50_npu_audit_seconds": 0.0,
    "p90_npu_audit_seconds": 0.0,
    "npu_to_gpu_avg_duration_ratio": 0.0,
    "gpu_elapsed_seconds": 61.694,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.001,
    "gpu": {
      "elapsed_seconds": 61.694,
      "round_count": 4,
      "round_duration_source": "gpu_elapsed_divided_by_round_count",
      "round_duration_sample_count": 1,
      "avg_round_seconds": 15.424,
      "p50_round_seconds": 15.424,
      "p90_round_seconds": 15.424,
      "max_round_seconds": 15.424,
      "round_durations_total_seconds": 15.424,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 15,
        "runtime_tool_execution_count": 7,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 8,
        "runtime_tool_provider_request_execution_count": 0,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0
      },
      "embedded_performance": {}
    },
    "npu": {
      "audit_count": 0,
      "audit_requested_count": 0,
      "audit_success_count": 0,
      "duration_sample_count": 0,
      "avg_audit_seconds": 0.0,
      "p50_audit_seconds": 0.0,
      "p90_audit_seconds": 0.0,
      "max_audit_seconds": 0.0,
      "audit_durations_total_seconds": 0.0,
      "status_counts": {},
      "classification_counts": {},
      "lane_diagnostics": {}
    },
    "sync": {
      "npu_to_gpu_avg_duration_ratio": 0.0,
      "npu_audit_round_coverage": 0.0,
      "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
    },
    "guardrails": {
      "report_only": true,
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "blender_runtime_execution_performed": false,
      "sqlite_write_performed": false
    }
  },
  "suggestions": {
    "recommended_profile": "gpu_npu_balanced_advisory",
    "reasoning": [
      "No NPU audits were observed; first verify provider availability before tuning cadence.",
      "GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate."
    ],
    "parameters": {
      "npu_auditor_every_rounds": 4,
      "max_concurrent_npu_audits": 1,
      "npu_auditor_timeout_seconds": 420,
      "npu_max_context_chars": 8000,
      "npu_max_prompt_chars": 1200,
      "npu_max_new_tokens": 384,
      "npu_final_wait_seconds": 180,
      "gpu_max_new_tokens": 3600,
      "gpu_files_per_round": 8,
      "gpu_max_chars_per_file": 6000
    },
    "guardrails": {
      "do_not_change_provider_model_settings_first": true,
      "keep_npu_auditor_non_blocking": true,
      "keep_max_concurrent_npu_audits": 1,
      "do_not_promote_npu_advisory": true,
      "do_not_make_openvino_gpu_primary": true
    }
  },
  "operational_opinions": [
    "Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.",
    "GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present."
  ],
  "refactoring_suggestions": [
    {
      "priority": "high",
      "area": "gpu_runner_timing",
      "recommendation": "Use rounds[*].elapsed_seconds as the primary GPU round timing source.",
      "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count",
      "guardrail": "report_only_no_provider_setting_change"
    }
  ],
  "decision": {
    "npu_too_slow_for_per_round_lockstep": false,
    "recommended_next_layer": "feed timing-backed GPU/NPU suggestions into decision-loop patch planning",
    "manual_review_required": true
  }
}

```

### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2367`
- SHA-256: `11aef7aeee95ee274bd5f397bde63f698d765de29985a4b1d40911f2e4fb6e89`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `4`
- `npu_audit_count`: `0`
- `legacy_npu_audit_count`: `0`
- `npu_micro_support_count`: `0`
- `npu_micro_support_overlap_count`: `0`
- `gpu0_peer_support_count`: `5`
- `gpu0_peer_support_overlap_count`: `4`
- `npu_audit_success_count`: `0`
- `npu_audit_round_coverage`: `0.0`
- `avg_gpu_round_seconds`: `15.424`
- `p50_gpu_round_seconds`: `15.424`
- `p90_gpu_round_seconds`: `15.424`
- `avg_npu_audit_seconds`: `0.0`
- `p50_npu_audit_seconds`: `0.0`
- `p90_npu_audit_seconds`: `0.0`
- `npu_to_gpu_avg_duration_ratio`: `0.0`
- `gpu_elapsed_seconds`: `61.694`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `61.694`
- GPU average round seconds: `15.424`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- GPU timing sample count: `1`
- GPU round durations total seconds: `15.424`
- NPU average audit seconds: `0.0`
- NPU duration sample count: `0`

## Operational opinions

- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count

## Suggested balanced profile

- `npu_auditor_every_rounds`: `4`
- `max_concurrent_npu_audits`: `1`
- `npu_auditor_timeout_seconds`: `420`
- `npu_max_context_chars`: `8000`
- `npu_max_prompt_chars`: `1200`
- `npu_max_new_tokens`: `384`
- `npu_final_wait_seconds`: `180`
- `gpu_max_new_tokens`: `3600`
- `gpu_files_per_round`: `8`
- `gpu_max_chars_per_file`: `6000`

## Reasoning

- No NPU audits were observed; first verify provider availability before tuning cadence.
- GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate.


```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git status --short
# Replace <bundle_basename> with the generated evidence bundle basename.
git add -- `
  .\docs\LOCAL_VALIDATION_EVIDENCE\<bundle_basename>.json `
  .\docs\LOCAL_VALIDATION_EVIDENCE\<bundle_basename>.md
git commit -m "test: add local ai workflow evidence bundle"
git push
# Never use: git add docs/LOCAL_VALIDATION_EVIDENCE/
```
