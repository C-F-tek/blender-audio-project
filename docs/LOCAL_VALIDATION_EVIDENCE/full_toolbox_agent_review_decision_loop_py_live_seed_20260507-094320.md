# Local Validation Evidence Bundle

- Generated at: `2026-05-07T09:37:24`
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
- `included_artifact_count`: `42`
- `patch_plan_summary_seen`: `True`

## Reports

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`
- Recommended next layer: `build_agent_review_patch_plan.py`
- Warnings: `['round 2: invalid tool requests: ["tool_requests[0].tool not allowlisted: \'build_agent_review_patch_plan.py\'"]']`

### `output/analysis/repository_consistency_map_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `184`

### `output/validation/python_line_count_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_json_contract_replay_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/provider_evidence_contract_full_toolbox_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_evidence_contract`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `["local provider probe degraded: ['ollama: probe failed']"]`

### `output/validation/gpu0_companion_task_lane_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_worker_lane`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; semantic LLM subtasks unavailable, numeric/tool companion active.']`

### `output/validation/gpu0_companion_contract_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_contract`
- Passed: `True`

### `output/ai_pipeline/gpu0_peer_support_parallel_py_live_seed_20260507-094320/round_000_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/ai_pipeline/npu_micro_support_parallel_py_live_seed_20260507-094320/round_000_npu_micro_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_gpu_deep_review_audit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['TimeoutExpired: 35s', 'NPU auditor command returned 124', 'NPU provider returned an empty response']`

### `output/validation/gpu1_primary_advisory_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu1_primary_advisory`
- Passed: `True`
- Provider execution performed: `True`
- Recommendation count: `1`

### `output/validation/gpu0_peer_task_packet_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_task_packet`
- Passed: `True`

### `output/validation/gpu0_peer_response_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_response`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only.']`

### `output/validation/gpu0_tool_requests_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_tool_requests`
- Passed: `None`

### `output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_gpu_deep_review_audit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['TimeoutExpired: 35s', 'NPU auditor command returned 124', 'NPU provider returned an empty response']`

### `output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/ai_peer_exchange_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_peer_exchange`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'npu_brokered_tool_supply', 'npu_deterministic_tool_fallback']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured', 'npu_semantic_provider_slow_or_degraded']`
- Peer mesh product blockers: `[]`
- Peer mesh visibility: `{'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': True, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': True, 'npu_tool_requests_broker_consumed': True, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}`
- NPU support lane: `{'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': True, 'tool_request_count': 4, 'broker_tool_execution_count': 4, 'provider_execution_requested': True, 'provider_execution_performed': False, 'provider_slow_or_degraded': True, 'classification': 'provider_empty_response', 'deterministic_fallback_used': True, 'product_pass_blocker': False}`
- Peer mesh lane state: `{'schema_version': 1, 'kind': 'peer_mesh_lane_state', 'operational_lanes': ['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support'], 'support_lanes': ['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'npu_brokered_tool_supply', 'npu_deterministic_tool_fallback'], 'degraded_lanes': ['gpu0_semantic_companion_model_unconfigured', 'npu_semantic_provider_slow_or_degraded'], 'product_blockers': [], 'gpu0_broker_tool_execution_count': 3, 'npu_broker_tool_execution_count': 4, 'broker_runtime_tool_execution_count': 7, 'legacy_usable_lanes_are_workload_quality_only': True, 'npu_degraded_is_product_blocker': False, 'npu_heavy_audit_authority': False, 'all_required_product_lanes_present': True, 'mesh_visibility': {'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': True, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': True, 'npu_tool_requests_broker_consumed': True, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}, 'npu_support_lane': {'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': True, 'tool_request_count': 4, 'broker_tool_execution_count': 4, 'provider_execution_requested': True, 'provider_execution_performed': False, 'provider_slow_or_degraded': True, 'classification': 'provider_empty_response', 'deterministic_fallback_used': True, 'product_pass_blocker': False}}`

### `output/validation/ai_peer_exchange_contract_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_peer_exchange_contract`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'npu_brokered_tool_supply', 'npu_deterministic_tool_fallback']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured', 'npu_semantic_provider_slow_or_degraded']`
- Peer mesh product blockers: `[]`
- Warnings: `['npu_provider_slow_or_degraded_non_blocking_support_lane', 'gpu0_peer_semantic_model_unconfigured']`
- Peer mesh lane state: `{'schema_version': 1, 'kind': 'peer_mesh_lane_state', 'operational_lanes': ['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support'], 'support_lanes': ['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'npu_brokered_tool_supply', 'npu_deterministic_tool_fallback'], 'degraded_lanes': ['gpu0_semantic_companion_model_unconfigured', 'npu_semantic_provider_slow_or_degraded'], 'product_blockers': [], 'gpu0_broker_tool_execution_count': 3, 'npu_broker_tool_execution_count': 4, 'broker_runtime_tool_execution_count': 7, 'legacy_usable_lanes_are_workload_quality_only': True, 'npu_degraded_is_product_blocker': False, 'npu_heavy_audit_authority': False, 'all_required_product_lanes_present': True, 'mesh_visibility': {'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': True, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': True, 'npu_tool_requests_broker_consumed': True, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}, 'npu_support_lane': {'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': True, 'tool_request_count': 4, 'broker_tool_execution_count': 4, 'provider_execution_requested': True, 'provider_execution_performed': False, 'provider_slow_or_degraded': True, 'classification': 'provider_empty_response', 'deterministic_fallback_used': True, 'product_pass_blocker': False}}`

### `output/validation/provider_runtime_heap_live_signals_init_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_gpu1_request_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_broker_results_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_npu_support_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/ai_runtime_heap/py_live_seed_20260507-094320/snapshot.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_snapshot`
- Passed: `None`

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_telemetry`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_py_live_seed_20260507-094320_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/provider_runtime_heap_from_peer_reports_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_from_peer_reports`
- Passed: `True`

### `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product_evidence_index.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_evidence_index`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product_readiness.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_readiness`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `20`

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_agent_review_decision_loop.json`

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

### `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.json`

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

### `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.json`

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

#### consistency_052 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_053 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_054 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_055 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_056 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:207` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:207`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_057 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:208` targeting `Tools/workflow/example_runner/phase.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:208`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner/phase.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_058 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_orchestrator.json` exists=`True` size=`136378` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.json` exists=`True` size=`15043` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`9481156` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`1213` suffix=`.json` preview_chars=`1174`
- `output/analysis/code_interpreter_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`2092196` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`3162` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`76770` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`3936` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`5691` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_evidence_contract_full_toolbox_py_live_seed_20260507-094320.json` exists=`True` size=`6784` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_task_lane_py_live_seed_20260507-094320.json` exists=`True` size=`7628` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_contract_py_live_seed_20260507-094320.json` exists=`True` size=`468` suffix=`.json` preview_chars=`456`
- `output/ai_pipeline/gpu0_peer_support_parallel_py_live_seed_20260507-094320/round_000_gpu0_peer_support.json` exists=`True` size=`1733` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/npu_micro_support_parallel_py_live_seed_20260507-094320/round_000_npu_micro_support.json` exists=`True` size=`12151` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu1_primary_advisory_py_live_seed_20260507-094320.json` exists=`True` size=`2159` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_task_packet_py_live_seed_20260507-094320.json` exists=`True` size=`5936` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_response_py_live_seed_20260507-094320.json` exists=`True` size=`4951` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_tool_requests_py_live_seed_20260507-094320.json` exists=`True` size=`3175` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.json` exists=`True` size=`29066` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.json` exists=`True` size=`11257` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.json` exists=`True` size=`27339` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_peer_exchange_py_live_seed_20260507-094320.json` exists=`True` size=`98278` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_peer_exchange_contract_py_live_seed_20260507-094320.json` exists=`True` size=`13695` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_init_py_live_seed_20260507-094320.json` exists=`True` size=`1513` suffix=`.json` preview_chars=`1464`
- `output/validation/provider_runtime_heap_live_signals_gpu1_request_py_live_seed_20260507-094320.json` exists=`True` size=`1872` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_broker_results_py_live_seed_20260507-094320.json` exists=`True` size=`4615` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_npu_support_py_live_seed_20260507-094320.json` exists=`True` size=`1855` suffix=`.json` preview_chars=`1500`
- `output/ai_runtime_heap/py_live_seed_20260507-094320/snapshot.json` exists=`True` size=`7021` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_py_live_seed_20260507-094320.json` exists=`True` size=`2397` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_py_live_seed_20260507-094320_workflow.json` exists=`True` size=`5285` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_from_peer_reports_py_live_seed_20260507-094320.json` exists=`True` size=`1499` suffix=`.json` preview_chars=`1466`
- `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320.json` exists=`True` size=`377526` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product_manifest.json` exists=`True` size=`377526` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product_evidence_index.json` exists=`True` size=`201834` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product_readiness.json` exists=`True` size=`444` suffix=`.json` preview_chars=`430`
- `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json` exists=`True` size=`361627` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_bridge_orchestrator.json` exists=`True` size=`1237` suffix=`.json` preview_chars=`1204`
- `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_agent_review_decision_loop.json` exists=`True` size=`2953` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.json` exists=`True` size=`431050` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/repository_consistency_map_full_toolbox_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `55482`
- SHA-256: `208186e1b57a6ab1a18c43e4b07cb2f72c106e100831338f696a9de0d4db45e7`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `12980`
- Markdown files: `642`
- Python files: `637`
- Markdown references: `87615`
- Markdown Python commands: `797`
- Provider execution performed: `False`
- Workers requested: `4`
- Total build seconds: `80.562`
- Markdown scan seconds: `58.892`
- Python inventory seconds: `6.164`
- Patch application performed: `False`

## Severity counts

- `high`: `4827`
- `low`: `48`
- `medium`: `8105`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `48`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `8103`
- `md_mentions_missing_powershell_path`: `740`
- `md_mentions_missing_python_path`: `4036`
- `md_python_command_script_missing`: `51`

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 294 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 295 | `patches/00_check_repo_ready.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 292 | `text
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
| `high` | `md_mentions_missing_python_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 29 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 29 | `run_patch_bundle.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 216 | `text
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 68 | `output/ai_packets/20260504-224354/npu_real_workload_report.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 142 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 231 | `shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 67 | `text
output/ai_packets/20260504-224354/npu_real_workload_report.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 141 | `powershell
python ./output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md` | 282 | `text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md` | 231 | `text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `README.md` | 42 | `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/README.md` | 48 | `pipeline.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` |
```

### `output/validation/repository_consistency_map_smoke_full_toolbox_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `381`
- SHA-256: `e9c529cbae9218bb8b141f66e911b6f53e8beea840289c32e31dbd1aed3cc83f`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Consistency Map Smoke

- Passed: `True`
- Return code: `0`
- Mapper report reused: `True`
- Workers requested: `4`
- Elapsed seconds: `0.043`
- Finding count: `12980`
- Markdown reference count: `87615`
- Markdown Python command count: `797`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`

```

### `output/validation/python_line_count_all_python_files_py_live_seed_20260507-094320.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `38182`
- SHA-256: `325840df90cbedcce036311534a41ea965efe1a31185ccac874e42f1728795b9`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: py_live_seed_20260507-094320
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-093407.csv
- File count: 637
- Total Python lines: 118322
- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.

| Lines | File |
|---:|---|
| 2434 | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
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
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/build_markdown_inventory.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 331 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 327 | `Tools/ai/provider_runtime_heap_broker_bridge.py` |
| 327 | `Tools/npu/build_npu_knowledge_broker_packet.py` |
| 326 | `Tools/ai/run_gpu0_peer_companion_worker.py` |
| 326 | `Tools/npu/build_blender_manual_context.py` |
| 325 | `Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py` |
| 324 | `Tools/workflow/workflow_shell.py` |
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
| 299 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py` |
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
| 274 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py` |
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
| 203 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py` |
| 201 | `Tools/ai/code_edit_proposal_helpers.py` |
| 201 | `Tools/validation/check_validation_report_contract.py` |
| 201 | `Tools/validation/run_agent_review_code_patch_plan_smoke.py` |
| 200 | `Scripting/v61b/main_v61b.py` |
| 200 | `Tools/ai/validate_ai_artifacts.py` |
| 198 | `Scripting/v61b/world_setup.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 191 | `Tools/ai/code_interpreter_report/scanner.py` |
| 191 | `Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py` |
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
| 173 | `Tools/ai/runtime_tool_guidance.py` |
| 173 | `Tools/validation/check_generated_blender_script_policy.py` |
| 172 | `Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py` |
| 168 | `Tools/validation/run_schema_repair_context_smoke.py` |
| 167 | `Tools/ai/full_run_bundle_zip/builder.py` |
| 163 | `Tools/ai/full0to10_provider_telemetry_semantic/validator.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 161 | `Tools/validation/run_npu_runtime_tool_execution_smoke.py` |
| 160 | `Tools/npu/npu_runtime.py` |
| 159 | `Scripting/v61b/fog_filaments.py` |
| 159 | `Tools/ai/github_evidence_bundle_io.py` |
| 159 | `Tools/validation/check_npu_decode_quality_remediation.py` |
| 159 | `Tools/validation/run_provider_empty_response_diagnostics_smoke.py` |
| 157 | `Tools/npu/pipeline/__init__.py` |
| 156 | `Tools/validation/run_schema_repair_retry_bootstrap_smoke.py` |
| 154 | `Tools/validation/run_runtime_tool_feedback_loop_smoke.py` |
| 152 | `Tools/ai/pipeline/models.py` |
| 152 | `Tools/validation/run_startup_check_cli_contract_smoke.py` |
| 150 | `Scripting/v61b/hotpatch/lighting_patch.py` |
| 149 | `Tools/validation/check_refactor_status_consistency.py` |
| 148 | `Tools/npu/build_runtime_output_manifest.py` |
| 147 | `Tools/npu/build_provider_result_report.py` |
| 147 | `Tools/validation/check_blender_shared_compat_smoke.py` |
| 146 | `Tools/ai/github_evidence_bundle_decisions.py` |
| 144 | `Tools/ai/code_interpreter_report/builder.py` |
| 144 | `Tools/workflow/artifact_consult.py` |
| 143 | `Tools/validation/run_npu_runtime_tool_fallback_smoke.py` |
| 142 | `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` |
| 142 | `Tools/ai/runtime_hardware_capability/workloads.py` |
| 141 | `Tools/ai/full0to10_sqlite_memory/embedding.py` |
| 141 | `Tools/validation/check_docs_links.py` |
| 141 | `Tools/validation/check_markdown_line_limits.py` |
| 141 | `Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py` |
| 140 | `Scripting/shared/blender_compat.py` |
| 139 | `Tools/ai/runtime_hardware_capability/manifest.py` |
| 136 | `Tools/ai/full0to10_final_product/builder.py` |
| 134 | `Scripting/shared/ffmpeg_encoder.py` |
| 133 | `Scripting/shared/render_profiles.py` |
| 133 | `Scripting/v61b/hotpatch/fog_patch.py` |
| 133 | `Tools/ai/repository_consistency_map/python_inventory.py` |
| 132 | `Scripting/v61b/spaziotempo/core/collections.py` |
| 132 | `Tools/validation/check_json_artifacts.py` |
| 130 | `Tools/ai/full_run_bundle_zip/discovery.py` |
| 130 | `Tools/ai/model_json.py` |
| 130 | `Tools/validation/check_gpu0_companion_contract.py` |
| 128 | `Tools/ai/build_agent_state_packet.py` |
| 127 | `Tools/npu/pipeline/artifact_paths.py` |
| 127 | `Tools/npu/run_npu_artifact_reviewer.py` |
| 126 | `Tools/ai/repository_consistency_map/paths.py` |
| 125 | `Scripting/v61b_backgood/hotpatch/accent_patch.py` |
| 125 | `Tools/npu/pipeline/reports.py` |
| 125 | `Tools/validation/check_agent_memory_policy.py` |
| 125 | `Tools/validation/check_generated_python_policy.py` |
| 124 | `Scripting/v61b_backg
```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1344`
- SHA-256: `16010b0bbf0c46bfa7cf59d59c30a33c469d61b741c38e634a254780862a9932`
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

- `recommendations`: `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json` exists=`True` size=`361627`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.md` exists=`True` size=`28838`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_bridge_orchestrator.json` exists=`True` size=`1237`
- `patch_plan`: `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.json` exists=`True` size=`431050`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.md` exists=`True` size=`17716`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/validation/gpu1_primary_advisory_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `159`
- SHA-256: `20ea18d668309d338067fbcfa7c88c7d51bab756d0ff0e839b8854ad3c1c7a04`
- Content included: `True`
- Content truncated: `False`

```text
# GPU1 Primary Advisory

- Passed: `True`
- Provider execution performed: `True`
- Round count: `2`
- Recommendation count: `1`
- Classifications: `[]`

```

### `output/validation/gpu0_peer_response_py_live_seed_20260507-094320.md`

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

### `output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1187`
- SHA-256: `fd2054c6535607fc6d5228946956fea140ca4425d34527a9dbaad553e883941d`
- Content included: `True`
- Content truncated: `False`

```text
# NPU GPU Deep Review Audit

- Passed: `True`
- Non-blocking: `True`
- NPU Python: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- NPU Python exists: `True`
- Provider execution requested: `True`
- Provider load attempted: `False`
- Provider execution succeeded: `False`
- Provider empty response: `True`
- Dependency missing: `False`
- Patch application performed: `False`
- Classification: `provider_empty_response`
- Runtime tool context seen: `True`
- Runtime tool context report count: `4`
- Tool request count: `4`
- GPU review blocked: `False`

## Warnings
- TimeoutExpired: 35s
- NPU auditor command returned 124
- NPU provider returned an empty response

## Decision
- `gpu_review_blocked`: `False`
- `npu_primary_advisory`: `False`
- `npu_audit_usable`: `False`
- `npu_dependency_missing`: `False`
- `npu_provider_empty_response`: `True`
- `npu_python_missing`: `False`
- `runtime_tool_context_seen`: `True`
- `runtime_tool_context_report_count`: `4`
- `npu_tool_requests_available`: `True`
- `npu_tool_request_count`: `4`
- `recommendation`: `continue_manual_review; treat NPU audit as non-blocking guardrail signal only`

```

### `output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2772`
- SHA-256: `cc217587561bec9b1e7c240d21ebf5e93a2c48813a9d512150a4ace73aa375d5`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Runtime Tool Broker

- passed: `True`
- dry_run: `False`
- request_file: `output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.json`
- request_kind: `npu_gpu_deep_review_audit`
- source: `npu_deterministic_fallback`
- source_classification: `npu_deterministic_fallback`
- tool_request_count: `4`
- tool_execution_count: `4`
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

### `npu_fallback_python_syntax` — `check_python_syntax`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/npu_micro/npu_fallback_python_syntax_python_syntax.json'}`

### `npu_fallback_validation_contract` — `check_validation_report_contract`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/npu_micro/npu_fallback_validation_contract_validation_report_contract.json'}`

### `npu_fallback_transient_context` — `build_agent_transient_request_context`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/npu_micro/npu_fallback_transient_context_agent_transient_request_context.json', 'markdown_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/npu_micro/npu_fallback_transient_context_agent_transient_request_context.md'}`

### `npu_fallback_gpu_contract_smoke` — `run_gpu_planner_json_contract_smoke`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/npu_micro/npu_fallback_gpu_contract_smoke_gpu_planner_json_contract_smoke.json', 'markdown_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/npu_micro/npu_fallback_gpu_contract_smoke_gpu_planner_json_contract_smoke.md'}`

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

### `output/validation/ai_peer_exchange_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1295`
- SHA-256: `478f8140c29e85c08dcaa59d69b410389c6530fc811c7448519e54169fb5275f`
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
- NPU broker executions: `4`
- Peer mesh all lanes visible: `True`
- NPU support tool supply: `True`
- NPU slow/degraded non-blocking: `True`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'npu_brokered_tool_supply', 'npu_deterministic_tool_fallback']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured', 'npu_semantic_provider_slow_or_degraded']`
- Peer mesh product blockers: `[]`
- Provider-broker loop active: `True`
- Provider-broker controlled executor: `runtime_tool_broker`
- Provider-broker direct tool execution allowed: `False`
- Provider-broker topology: `input_md -> deterministic_baseline -> GPU1 -> GPU0 -> broker -> NPU_support -> broker -> contract -> telemetry -> bundle -> patch_plan`
- Provider-broker GPU0 executions: `3`
- Provider-broker NPU executions: `4`

```

### `output/validation/ai_peer_exchange_contract_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2640`
- SHA-256: `915b7087c6e38aa56f4fb5717c0efcd564cf61548d0d20be20a3757ddf8cd61c`
- Content included: `True`
- Content truncated: `False`

```text
# AI Peer Exchange Contract

- Passed: `True`
- Provider execution performed: `True`
- Classifications: `['npu_provider_slow_or_degraded_non_blocking', 'peer_mesh_degraded_lanes_present_non_blocking', 'gpu0_peer_semantic_model_unconfigured']`

## Evidence

- `gpu1_primary_advisory` exists=`True` passed=`True` path=`output/validation/gpu1_primary_advisory_py_live_seed_20260507-094320.json`
- `gpu0_peer_task_packet` exists=`True` passed=`True` path=`output/validation/gpu0_peer_task_packet_py_live_seed_20260507-094320.json`
- `gpu0_peer_response` exists=`True` passed=`True` path=`output/validation/gpu0_peer_response_py_live_seed_20260507-094320.json`
- `gpu0_tool_requests` exists=`True` passed=`None` path=`output/validation/gpu0_tool_requests_py_live_seed_20260507-094320.json`
- `gpu0_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.json`
- `npu_micro_response` exists=`True` passed=`True` path=`output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.json`
- `npu_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.json`
- `ai_peer_exchange` exists=`True` passed=`True` path=`output/validation/ai_peer_exchange_py_live_seed_20260507-094320.json`

## Peer mesh visibility

- Passed: `True`
- GPU1 sees GPU0 response: `True`
- GPU1 sees NPU support signal: `True`
- GPU0 sees GPU1 primary advisory: `True`
- NPU sees GPU1/GPU0/broker context: `True`
- NPU support tool supply: `True`
- NPU slow/degraded non-blocking: `True`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply', 'npu_brokered_tool_supply', 'npu_deterministic_tool_fallback']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured', 'npu_semantic_provider_slow_or_degraded']`
- Peer mesh product blockers: `[]`

## Provider-broker loop

- Passed: `True`
- Active: `True`
- Controlled executor: `runtime_tool_broker`
- Direct tool execution allowed: `False`
- Broker tool executions: `7`
- GPU0 broker executions: `3`
- NPU broker executions: `4`
- NPU non-blocking: `True`
- NPU product pass blocker: `False`
- Deterministic scripts heavy audit authority: `True`
- Product blockers: `[]`

## Warnings

- npu_provider_slow_or_degraded_non_blocking_support_lane
- gpu0_peer_semantic_model_unconfigured

```

### `output/validation/provider_runtime_heap_from_peer_reports_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1037`
- SHA-256: `602bf17f5995ed49df05fdf9d6ad637f188fcfbda31b6fa853c93609326d2be1`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap From Peer Reports

- passed: `True`
- stamp: `py_live_seed_20260507-094320`
- event_count: `11`
- heap_event_count: `43`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/py_live_seed_20260507-094320/events.jsonl`

## Reports

- `gpu1`: `output/validation/gpu1_primary_advisory_py_live_seed_20260507-094320.json`
- `gpu0`: `output/validation/gpu0_peer_response_py_live_seed_20260507-094320.json`
- `gpu0_tool_requests`: `output/validation/gpu0_tool_requests_py_live_seed_20260507-094320.json`
- `gpu0_broker`: `output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.json`
- `npu`: `output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.json`
- `npu_broker`: `output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.json`
- `peer_exchange`: `output/validation/ai_peer_exchange_py_live_seed_20260507-094320.json`
- `peer_contract`: `output/validation/ai_peer_exchange_contract_py_live_seed_20260507-094320.json`

```

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1322`
- SHA-256: `76cb7bea4dbad4d1ea5667fd4e9a1cf6fcea1c0167113748af771feaa843715b`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Telemetry

- passed: `True`
- stamp: `py_live_seed_20260507-094320`
- event_count: `43`
- parse_error_count: `0`
- tool_catalog_exchange_complete_count: `0`
- gpu1_to_gpu0_event_count: `2`
- gpu0_to_gpu1_event_count: `5`
- gpu1_gpu0_bidirectional: `True`
- gpu1_gpu0_correlated_exchange_count: `2`
- broker_request_count: `10`
- broker_result_count: `15`
- pending_broker_request_count: `0`
- validation_signal_count: `1`
- direct_execution_violation_count: `0`
- tool_catalog_tool_count: `10`

## Events by lane

- `broker`: `15`
- `deterministic`: `1`
- `gpu0`: `11`
- `gpu1`: `2`
- `npu`: `7`
- `orchestrator`: `7`

## Events by type

- `broker_request`: `10`
- `broker_result`: `15`
- `evidence_request`: `6`
- `evidence_response`: `8`
- `provider_state`: `3`
- `validation_signal`: `1`

## Interaction edges

- `broker->gpu0:broker_result`: `6`
- `broker->npu:broker_result`: `9`
- `deterministic->gpu1:validation_signal`: `1`
- `gpu0->broker:broker_request`: `6`
- `gpu0->gpu1:evidence_response`: `5`
- `gpu1->gpu0:evidence_request`: `2`
- `npu->broker:broker_request`: `4`
- `npu->gpu1:evidence_response`: `3`
- `orchestrator->gpu0:evidence_request`: `3`
- `orchestrator->none:provider_state`: `3`
- `orchestrator->npu:evidence_request`: `1`

```

### `output/validation/provider_runtime_heap_live_signals_init_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `278`
- SHA-256: `9ec16a83a854f7b7182965f609011aa7683b336f253b6fa1ae5926214719a621`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `py_live_seed_20260507-094320`
- mode: `init`
- event_count: `1`
- heap_event_count: `1`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/py_live_seed_20260507-094320/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_gpu1_request_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `287`
- SHA-256: `171c65106646d2d5697816e712e05ebf2cdfac82bccc0b1852da66aad69546bc`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `py_live_seed_20260507-094320`
- mode: `gpu1-request`
- event_count: `1`
- heap_event_count: `24`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/py_live_seed_20260507-094320/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_broker_results_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `289`
- SHA-256: `51726e8ca3cc01455d39c5ab162e73fe0fb7834f3ec9eedb777361838894b6fd`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `py_live_seed_20260507-094320`
- mode: `broker-results`
- event_count: `3`
- heap_event_count: `31`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/py_live_seed_20260507-094320/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_npu_support_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `286`
- SHA-256: `3d131e498946baf6172b8f195920902815444b5859cfa1aa03c8b7ac78449e70`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `py_live_seed_20260507-094320`
- mode: `npu-support`
- event_count: `1`
- heap_event_count: `32`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/py_live_seed_20260507-094320/events.jsonl`

```

### `output/ai_runtime_heap/py_live_seed_20260507-094320/snapshot.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2486`
- SHA-256: `43f8226078d732a512f43ce31fc725539ffec85f8bfa6464f58bd01856e82c3e`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Snapshot

- Stamp: `py_live_seed_20260507-094320`
- Event count: `43`
- Parse error count: `0`
- Pending broker requests: `0`
- Event log: `output/ai_runtime_heap/py_live_seed_20260507-094320/events.jsonl`

## Runtime architecture

- `gpu1`: `primary_advisory_planner`
- `gpu0`: `coworker_helper_openvino`
- `npu`: `microtask_responder`
- `broker`: `single_controlled_executor`
- `semantic_tools_registry`: `agent_runtime_tool_broker.TOOL_SPECS`
- `deterministic_validators`: `cpu_authority_validation_lane`
- `telemetry`: `append_only_event_stream`

## Events by lane

- `orchestrator`: `{'event_count': 7, 'latest_event_at': '2026-05-07T09:37:12', 'event_types': {'provider_state': 3, 'evidence_request': 4}}`
- `broker`: `{'event_count': 15, 'latest_event_at': '2026-05-07T09:37:12', 'event_types': {'broker_result': 15}}`
- `gpu0`: `{'event_count': 11, 'latest_event_at': '2026-05-07T09:37:12', 'event_types': {'evidence_response': 5, 'broker_request': 6}}`
- `npu`: `{'event_count': 7, 'latest_event_at': '2026-05-07T09:37:12', 'event_types': {'evidence_response': 3, 'broker_request': 4}}`
- `gpu1`: `{'event_count': 2, 'latest_event_at': '2026-05-07T09:37:12', 'event_types': {'evidence_request': 2}}`
- `deterministic`: `{'event_count': 1, 'latest_event_at': '2026-05-07T09:37:12', 'event_types': {'validation_signal': 1}}`

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

### `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6335`
- SHA-256: `a3d685ca10b586e10fc570d54fafc44dd3502a701fe9b6bf4e5c55afe9e44400`
- Content included: `True`
- Content truncated: `False`

```text
# Full0To10 final tool product

## Request

Build the final local AI product for stamp py_live_seed_20260507-094320 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.

## Deliverable scope

This package is the final-tool-product staging output. It includes track input contract, SQLite FTS5 evidence, accelerator control, provider governor, invocation dry-run plan, execution bridge, command plan, telemetry contracts, and quality evidence.

## Evidence index

- `effective_use_summary` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/effective_use/full0to10_effective_use_summary.json`
- `quality_product` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/effective_use/full0to10_effective_use_quality_product.md`
- `provider_hardening` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/effective_use/full0to10_provider_hardening_contracts.json`
- `tool_telemetry` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/effective_use/full0to10_effective_use_tool_telemetry.json`
- `optimization` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/effective_use/full0to10_effective_use_optimization.json`
- `quality_gate` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/quality_gate/full0to10_quality_gate.json`
- `accelerator_control` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/accelerator_control/full0to10_accelerator_control.json`
- `provider_governor` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_governor/full0to10_provider_governor.json`
- `provider_run_permit` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_governor/full0to10_provider_run_permit.json`
- `provider_invocation_plan` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_invocation_plan/full0to10_provider_invocation_plan.json`
- `provider_workload_report_contract` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_invocation_plan/full0to10_provider_workload_report_contract.json`
- `provider_expected_telemetry_contract` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json`
- `provider_execution_bridge` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_execution_bridge/full0to10_provider_execution_bridge.json`
- `provider_real_run_gate` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_execution_bridge/full0to10_provider_real_run_gate.json`
- `provider_command_plan` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_execution_bridge/full0to10_provider_command_plan.json`
- `provider_workload_output_paths` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_execution_bridge/full0to10_provider_workload_output_paths.json`
- `track_input_contract` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/track_inputs/full0to10_track_input_contract.json`
- `track_input_template` exists=`True` path=`output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/track_inputs/full0to10_track_input_template.json`

## Current run product evidence

- Passed: `True`
- Report count: `17`
- Artifact count: `10`
- Missing count: `0`

- report `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_orchestrator.json` exists=`True`
- report `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.json` exists=`True`
- report `output/analysis/gpu_npu_run_sync_full_toolbox_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/provider_evidence_contract_full_toolbox_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/ai_peer_exchange_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/ai_peer_exchange_contract_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/provider_runtime_heap_from_peer_reports_py_live_seed_20260507-094320.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_py_live_seed_20260507-094320.json` exists=`True`
- report `output/ai_runtime_heap/py_live_seed_20260507-094320/snapshot.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_py_live_seed_20260507-094320.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/runtime_tool_broker_full_toolbox_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.json` exists=`True`
- report `output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.json` exists=`True`
- report `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json` exists=`True`
- report `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_agent_review_decision_loop.json` exists=`True`
- report `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.json` exists=`True`

## Track inputs

The track input contract resolves analysis_json, music_context_json and blender_keyframes_json. Missing inputs are warnings by default and can be promoted to blockers by startup guard strict mode.

## Provider execution bridge

The execution bridge is the final non-executing gate before a future real provider run.

## Readiness

- Ready for product review: `True`
- Ready for real provider run: `False`
- Score: `100`

## Blockers

- None

## Warnings

- None

```

### `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/README.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `585`
- SHA-256: `a83ddd96ba8c9ab5fe9ba580dd137500ae860ddd6e2db6e367d9acc2a2f573f0`
- Content included: `True`
- Content truncated: `False`

```text
# Full0To10 final tool product package

- Passed: `True`
- Product markdown: `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/full0to10_final_tool_product.md`
- Track input contract: `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/track_inputs/full0to10_track_input_contract.json`
- Provider execution bridge: `output/validation/full0to10_final_tool_product_py_live_seed_20260507-094320/provider_execution_bridge/full0to10_provider_execution_bridge.json`

This directory is generated output and should not be committed.

```

### `output/patch_specs/full_toolbox_py_live_seed_20260507-094320_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `17716`
- SHA-256: `929bec675252ecd546de0dbd93acced9cc54c7944b3a439223132edae538f437`
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

- `orchestrator`: `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json`
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

### consistency_052 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_053 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_054 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_055 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_056 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:207` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:207`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_057 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:208` targeting `Tools/workflow/examp
```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-093407.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `32766`
- SHA-256: `60280decb304fb340da85654b674bdbee14e99717aac9467f42c145853082954`
- Content included: `True`
- Content truncated: `True`

```text
File,Lines
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,2434
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
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/build_markdown_inventory.py,339
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/validation/check_local_ai_adapter_manifest.py,331
Tools/ai/provider_runtime_heap_broker_bridge.py,327
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/ai/run_gpu0_peer_companion_worker.py,326
Tools/npu/build_blender_manual_context.py,326
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py,325
Tools/workflow/workflow_shell.py,324
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
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py,299
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
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py,274
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
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py,203
Tools/ai/code_edit_proposal_helpers.py,201
Tools/validation/check_validation_report_contract.py,201
Tools/validation/run_agent_review_code_patch_plan_smoke.py,201
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/ai/code_interpreter_report/scanner.py,191
Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py,191
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
Tools/ai/runtime_tool_guidance.py,173
Tools/validation/check_generated_blender_script_policy.py,173
Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py,172
Tools/validation/run_schema_repair_context_smoke.py,168
Tools/ai/full_run_bundle_zip/builder.py,167
Tools/ai/full0to10_provider_telemetry_semantic/validator.py,163
Scripting/shared/image_sequence.py,161
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
Tools/ai/code_interpreter_report/builder.py,144
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/ai/runtime_hardware_capability/workloads.py,142
Tools/ai/full0to10_sqlite_memory/embedding.py,141
Tools/validation/check_docs_links.py,141
Tools/validation/check_markdown_line_limits.py,141
Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py,141
Scripting/shared/blender_compat.py,140
Tools/ai/runtime_hardware_capability/manifest.py,139
Tools/ai/full0to10_final_product/builder.py,136
Scripting/shared/ffmpeg_encoder.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Tools/ai/repository_consistency_map/python_inventory.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/full_run_bundle_zip/discovery.py,130
Tools/ai/model_json.py,130
Tools/validation/check_gpu0_companion_contract.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Tools/ai/repository_consistency_map/paths.py,126
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/ai/full0to10_effective_use/memory_product.py,123
Tools/validation/check_execution_plan_status.py,123
Tools/ai/repository_consistency_map/builder.py,122
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py,120
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/ai/runtime_hardware_capability/policy.py,118
Tools/ai/repository_consistency_map/markdown.py,117
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
Tools/ai/repository_consistency_map/findings.py,114
build_track_summary.py,113
Tools/ai/run_provider_runtime_heap_gpu_peer_smoke.py,112
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/full0to10_final_product_quality/builder.py,108
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/ai/full0to10_provider_feedback_loop/builder.py,106
Tools/validation/check_python_syntax.py,105
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_engine.py,105
Tools/ai/full0to10_sqlite_memory/search.py,104
Tools/ai/pipeline/preflight.py,104
Tools/ai/summarize_full0to10_light_evidence.py,104
Tools/validation/run_full0to10_bundle_contracts_smoke.py,104
Tools/validation/run_unified_full0to10_supervisor_gate_smoke.py,104
Scripting/v61b/hotpatch/runner.py,103
Tools/validation/run_full_toolbox_deterministic_chunks_telemetry_smoke.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/ai/full0to10_memory_tool.py,101
Tools/ai/build_openvino_gpu0_workload_report.py,99
Tools/npu/pipeline/prompts.py,99
Tools/validation/run_full0to10_manifest_gate_smoke.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/ai/full0to10_effective_use/builder.py,96
Tools/validation/check_npu_pipeline_docs.py,96
Tools/ai/full0to10_hardware_capability/openvino_devices.py,95
Tools/ai/full0to10_provider_invocation_plan/builder.py,94
Tools/ai/full0to10_auto_refactor_apply/applier.py,93
Tools/ai/full0to10_provider_execution_bridge/builder.py,92
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Tools/ai/full0to10_markdown_split/applier.py,90
Tools/validation/run_npu_tool_request_contract_smoke.py,90
Scripting/shared/json_io.py,88
Tools/ai/ful
```

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `3551`
- SHA-256: `26d727f7550eabc56a557c9a2d79b530e3719ee6dfc2fadc1f9f11510730c46b`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_review_evidence_sufficiency",
  "generated_at": "2026-05-07T09:35:35",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": false,
  "errors": [
    "blocked_missing_refined_review_input: output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json"
  ],
  "warnings": [
    "Evidence sufficiency input is missing; Full0To10 must classify this instead of raising a traceback."
  ],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_evidence_sufficiency",
  "inputs": {
    "refined_review": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
    "refined_review_exists": false,
    "refined_proposals": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals.json",
    "refined_proposals_exists": false,
    "refined_proposal_count": null,
    "context_reports": [
      {
        "path": "output/analysis/repository_consistency_map_full_toolbox_py_live_seed_20260507-094320.json",
        "exists": true,
        "kind": "repository_consistency_map",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/repository_consistency_map_smoke_full_toolbox_py_live_seed_20260507-094320.json",
        "exists": true,
        "kind": "repository_consistency_map_smoke",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/analysis/code_interpreter_full_toolbox_py_live_seed_20260507-094320.json",
        "exists": true,
        "kind": "code_interpreter_report",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/python_line_count_full_toolbox_py_live_seed_20260507-094320.json",
        "exists": true,
        "kind": "python_line_count_csv",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/python_syntax_full_toolbox_py_live_seed_20260507-094320.json",
        "exists": true,
        "kind": "python_syntax",
        "passed": true,
        "error": "",
        "summary": {}
      }
    ]
  },
  "areas": {
    "doc_code": {
      "area": "doc_code",
      "item_count": 0,
      "ready_for_manual_patch_count": 0,
      "needs_more_context_count": 0,
      "items": []
    },
    "doc_doc": {
      "area": "doc_doc",
      "item_count": 0,
      "ready_for_manual_patch_count": 0,
      "needs_more_context_count": 0,
      "items": []
    },
    "code_code": {
      "area": "code_code",
      "item_count": 0,
      "ready_for_manual_patch_count": 0,
      "needs_more_context_count": 0,
      "items": []
    }
  },
  "decision": {
    "ready_for_manual_patch_count": 0,
    "needs_more_context_count": 0,
    "recommended_mode": "blocked_missing_refined_review_input",
    "sufficient_for_real_pr": false,
    "next_steps": [
      "Generate refined review/proposals or rewire this lane to current-run reports before acceptance."
    ]
  },
  "guardrails": {
    "report_only": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "real_github_pr_created": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "manual_review_required": true
  }
}

```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1237`
- SHA-256: `e0bce8346e0e4d8d589bdf1a135306c0ee8387e73355783f23790955cd374581`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-07T09:37:13",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json",
  "gpu_recommendation_count": 20,
  "gpu_empty_recommendations_reason": "",
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "npu_audits": [],
  "decision": {
    "deterministic_recommendation_bridge": true,
    "manual_review_required": true,
    "recommended_next_layer": "build_agent_review_patch_plan.py"
  },
  "guardrails": {
    "report_only": true,
    "manual_review_required": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "blender_runtime_execution_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "real_github_pr_created": false
  }
}

```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `361627`
- SHA-256: `6e21d86868067df40469e8c2c5f2fdc90449afc5704a958fde756674447f8542`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_synthesizer",
  "generated_at": "2026-05-07T09:37:13",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "recommendation_count": 20,
  "recommendations": [
    {
      "id": "consistency_001",
      "area": "md_python",
      "status": "ready_for_patch_plan",
      "target_files": [
        "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md"
      ],
      "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.",
      "proposed_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
      "risk": "medium",
      "validation_commands": [
        "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
        "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
        "git diff --check",
        "git status --short"
      ],
      "stop_conditions": [
        "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
        "Stop if the target/source evidence no longer exists after refreshing master.",
        "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
        "Stop if resolving the finding requires inventing behavior not supported by code evidence."
      ],
      "source": "repository_consistency_map",
      "evidence": [
        "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "repository_consistency_map",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "repository_consistency_map_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/code_interpreter_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "code_interpreter_report",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/python_line_count_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "python_line_count_csv",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/python_syntax_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "python_syntax",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "gpu_planner_json_contract_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "deterministic_recommendation_synthesizer_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "agent_review_decision_loop_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/npu_provider_environment_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "npu_provider_environment",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_json_contract_replay_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "gpu_planner_json_contract_replay",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "gpu_npu_run_sync_analysis",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/provider_evidence_contract_full_toolbox_py_live_seed_20260507-094320.json",
          "kind": "provider_evidence_contract",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/gpu0_companion_task_lane_py_live_seed_20260507-094320.json",
          "kind": "gpu0_companion_worker_lane",
          "passed": true,
          "tool_request_count": 4,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu0_companion_contract_py_live_seed_20260507-094320.json",
          "kind": "gpu0_companion_contract",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/ai_pipeline/gpu0_peer_support_parallel_py_live_seed_20260507-094320/round_000_gpu0_peer_support.json",
          "kind": "openvino_gpu0_secondary_workload",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": false
        },
        {
          "path": "output/ai_pipeline/npu_micro_support_parallel_py_live_seed_20260507-094320/round_000_npu_micro_support.json",
          "kind": "npu_gpu_deep_review_audit",
          "passed": true,
          "tool_request_count": 4,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/gpu1_primary_advisory_py_live_seed_20260507-094320.json",
          "kind": "gpu1_primary_advisory",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu0_peer_task_packet_py_live_seed_20260507-094320.json",
          "kind": "gpu0_peer_task_packet",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu0_peer_response_py_live_seed_20260507-094320.json",
          "kind": "gpu0_peer_response",
          "passed": true,
          "tool_request_count": 3,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu0_tool_requests_py_live_seed_20260507-094320.json",
          "kind": "gpu0_peer_tool_requests",
          "passed": null,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.json",
          "kind": "agent_runtime_tool_broker",
          "passed": true,
          "tool_request_count": 3,
          "tool_execution_count": 3,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/npu_micro_peer_assistant_py_live_seed_20260507-094320.json",
          "kind": "npu_gpu_deep_review_audit",
          "passed": true,
          "tool_request_count": 4,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/npu_micro_runtime_tool_broker_py_live_seed_20260507-094320.json",
          "kind": "agent_runtime_tool_broker",
          "passed": true,
          "tool_request_count": 4,
          "tool_execution_count": 4,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/ai_peer_exchange_py_live_seed_20260507-094320.json",
          "kind": "ai_peer_exchange",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/ai_peer_exchange_contract_py_live_seed_20260507-094320.json",
          "kind": "ai_peer_exchange_contract",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": true,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/provider_runtime_heap_live_signals_init_py_live_seed_20260507-094320.json",
          "kind": "provider_runtime_heap_live_signals",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/provider_runtime_heap_live_signals_gpu1_request_py_live_seed_20260507-094320.json",
          "kind": "provider_runtime_heap_live_signals",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/provider_runtime_heap_live_signals_broker_results_py_live_seed_20260507-094320.json",
          "kind": "provider_runtime_heap_live_signals",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/provider_runtime_heap_live_signals_npu_support_py_live_seed_20260507-094320.json",
          "kind": "provider_runtime_heap_live_signals",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/ai_runtime_heap/py_live_seed_20260507-094320/snapshot.json",
          "kind": "provider_runtime_heap_snapshot",
          "passed": null,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_py
```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `28838`
- SHA-256: `53734fcd4ae11ee2b0bc0ef983122f4900ab96680f742268a0dd172476256ce9`
- Content included: `True`
- Content truncated: `True`

```text
# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `20`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: ``
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

### consistency_052 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_053 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_054 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_055 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_056 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:207` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:207`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_057 — md_powershell
- Source: `repository_consistency_ma
```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `136378`
- SHA-256: `7cde42cff9d56ba8d30a3203ec306ef40440da050dc0f5a563c568225a5ad888`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-07T09:36:26",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "gpu_provider_execution_performed": true,
  "gpu0_peer_support_provider_execution_performed": true,
  "npu_provider_execution_performed": false,
  "legacy_npu_provider_execution_performed": false,
  "npu_micro_support_provider_execution_performed": false,
  "npu_micro_support_provider_requested": true,
  "legacy_npu_auditor_provider_requested": false,
  "npu_auditor_provider_requested": false,
  "npu_auditor_provider_performed": false,
  "provider_degraded_reasons": [],
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 46.976,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_py_live_seed_20260507-094320_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_py_live_seed_20260507-094320_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 34.586,\n  \"round_count\": 2,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 1,\n  \"raw_recommendation_candidate_count\": 1,\n  \"filtered_recommendation_count\": 1,\n  \"tool_request_count\": 1,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 1,\n  \"empty_recommendations_reason\": \"\",\n  \"runtime_tool_broker_enabled\": false,\n  \"runtime_tool_bootstrap_executed\": false,\n  \"runtime_tool_bootstrap_passed\": null,\n  \"runtime_tool_bootstrap_request_count\": 0,\n  \"runtime_tool_bootstrap_execution_count\": 0,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 0,\n  \"runtime_tool_execution_count\": 0,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 0,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 0,\n  \"ready_for_patch_plan\": true,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.md",
  "gpu_recommendation_count": 1,
  "gpu_empty_recommendations_reason": "",
  "gpu_evidence_ready_for_manual_patch_count": 0,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "gpu_live_context_refresh_count": 2,
  "runtime_tool_broker_enabled": true,
  "runtime_tool_bootstrap_executed": true,
  "runtime_tool_bootstrap_passed": true,
  "runtime_tool_bootstrap_request_count": 7,
  "runtime_tool_bootstrap_execution_count": 7,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 15,
  "runtime_tool_execution_count": 14,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 1,
  "runtime_tool_result_count": 15,
  "gpu_runtime_tool_broker_enabled": false,
  "gpu_runtime_tool_request_count": 0,
  "gpu_runtime_tool_execution_count": 0,
  "gpu_runtime_tool_failed_count": 0,
  "gpu_runtime_tool_blocked_count": 0,
  "gpu_runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 8,
  "runtime_tool_provider_request_execution_count": 7,
  "runtime_tool_provider_request_failed_count": 0,
  "runtime_tool_provider_request_blocked_count": 1,
  "runtime_tool_provider_request_result_count": 8,
  "deterministic_runtime_tool_fallback_request_count": 0,
  "deterministic_runtime_tool_fallback_execution_count": 0,
  "deterministic_runtime_tool_fallback_failed_count": 0,
  "deterministic_runtime_tool_fallback_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap": {
    "enabled": true,
    "executed": true,
    "source": "orchestrator_bootstrap",
    "requested_tool_count": 7,
    "command": [
      "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
      "Tools/ai/agent_runtime_tool_broker.py",
      "--repo-root",
      ".",
      "--request-file",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\round_000_tool_requests.json",
      "--tool-output-dir",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000",
      "--timeout-seconds",
      "300",
      "--output",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\round_000_runtime_tool_broker.json",
      "--markdown-output",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\round_000_runtime_tool_broker.md"
    ],
    "returncode": 0,
    "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\py_live_seed_20260507-094320\\\\round_000\\\\round_000_runtime_tool_broker.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\py_live_seed_20260507-094320\\\\round_000\\\\round_000_runtime_tool_broker.md\",\n  \"tool_request_count\": 7,\n  \"tool_execution_count\": 7,\n  \"blocked_tool_count\": 0,\n  \"failed_tool_count\": 0,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"persistent_memory_write_count\": 0,\n  \"operational_sqlite_write_performed\": false,\n  \"operational_sqlite_write_count\": 0,\n  \"operational_memory_clear_count\": 0\n}\n",
    "stderr_tail": "",
    "error": "",
    "request_file": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/round_000_tool_requests.json",
    "broker_output": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/round_000_runtime_tool_broker.json",
    "broker_markdown": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/round_000_runtime_tool_broker.md",
    "broker_output_exists": true,
    "passed": true,
    "tool_request_count": 7,
    "tool_execution_count": 7,
    "blocked_tool_count": 0,
    "failed_tool_count": 0,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "operational_sqlite_write_performed": false,
    "tool_results": [
      {
        "id": "orchestrator_bootstrap_tool_inventory",
        "tool": "build_agent_agnostic_tool_inventory",
        "reason": "Bootstrap shared runtime tool inventory before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json",
          "markdown_report": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md"
        },
        "summary": {
          "kind": "agent_agnostic_tool_inventory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "report_only": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "sqlite_db_touched": false,
            "blender_runtime_touched": false,
            "real_github_pr_created": false,
            "output_artifacts_should_not_be_committed": true
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_write_performed": false
        },
        "command": [
          "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
          "Tools/ai/build_agent_agnostic_tool_inventory.py",
          "--repo-root",
          ".",
          "--output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md"
        ],
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\py_live_seed_20260507-094320\\\\round_000\\\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\py_live_seed_20260507-094320\\\\round_000\\\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md\",\n  \"tool_count\": 597,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
        "stderr_tail": ""
      },
      {
        "id": "orchestrator_bootstrap_memory_inventory",
        "tool": "build_agent_memory_inventory",
        "reason": "Bootstrap durable project memory inventory before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "markdown_report": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        },
        "summary": {
          "kind": "agent_memory_inventory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "sqlite_read_only": true,
            "sqlite_db_committed": false,
            "memory_promotion_performed": false,
            "memory_delete_performed": false,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_write_performed": false
        },
        "command": [
          "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
          "Tools/ai/build_agent_memory_inventory.py",
          "--repo-root",
          ".",
          "--objective",
          "Runtime read-only memory inventory for IA-Carmine planner.",
          "--memory-db",
          "indexAI/agent_memory/agent_memory.sqlite",
          "--output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\py_live_seed_20260507-094320\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        ],
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\py_live_seed_20260507-094320\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\py_live_seed_20260507-094320\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md\",\n  \"record_count\": 94,\n  \"memory_db_exists\": true,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
        "stderr_tail": ""
      },
      {
        "id": "orchestrator_bootstrap_persistent_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap persistent memory status in read-only mode before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.json",
          "markdown_report": "output/ai_runtime_tools/py_live_seed_20260507-094320/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.md"
        },
        "summary": {
          "kind": "agent_runtime_sqlite_memory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "persistent_memory_read_only": true,
            "persistent_memory_write_performed": false,
            "persistent_memory_promotion_performed": false,
            "persistent_memory_write_authorized": false,
            "sqlite_write_performed": false,
            "operational_sqlite_write_performed": false,
            "operational_memory_clear_performed": false,
            "operational_database_must_be_under_output": true,
            "operational_database_under_output": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false,
            "git_write_performed": false
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_w
```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3926`
- SHA-256: `9f7026fccaf451e56425e2cf188fccef0f0c6fa694a440d173b588611a0ee94b`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `46.976`
- `gpu0_peer_support_count`: `3`
- `gpu0_peer_support_success_count`: `3`
- `gpu0_peer_support_overlap_count`: `2`
- `gpu0_peer_support_provider_execution_performed`: `True`
- `npu_micro_support_count`: `1`
- `npu_micro_support_success_count`: `1`
- `npu_micro_support_overlap_count`: `1`
- `npu_micro_support_provider_execution_performed`: `False`
- `npu_micro_support_tool_request_count`: `4`
- `npu_micro_runtime_tool_execution_count`: `7`
- `npu_audit_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `1`
- `gpu_empty_recommendations_reason`: ``
- `gpu_evidence_ready_for_manual_patch_count`: `0`
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_request_count`: `15`
- `runtime_tool_execution_count`: `14`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `1`
- `runtime_tool_result_count`: `15`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `provider_mesh_mode`: `startup_barrier_parallel_peer_support`
- `all_lanes_ready_at_start`: `True`
- `gpu0_peer_support_started_with_gpu1`: `True`
- `npu_micro_support_started_with_gpu1`: `True`
- `npu_auditor_mode`: `legacy_disabled`
- `npu_audit_success_count`: `0`
- `npu_micro_support_success_count`: `1`
- `npu_micro_support_provider_success_count`: `0`
- `npu_micro_support_tool_success_count`: `1`
- `npu_micro_support_tool_request_count`: `4`
- `npu_micro_live_tool_seed_count`: `1`
- `npu_micro_runtime_tool_execution_count`: `7`
- `npu_micro_runtime_tool_live_execution_count`: `3`
- `npu_micro_support_tool_lane_performed`: `True`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_deterministic_tool_fallback_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `True`
- `fallback_patch_plan_recommended`: `False`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: ``
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_bootstrap_executed`: `True`
- `runtime_tool_bootstrap_execution_count`: `7`
- `runtime_tool_provider_request_count`: `8`
- `runtime_tool_provider_request_execution_count`: `7`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `14`
- `runtime_tool_result_count`: `15`
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
- round `2` status=`finished` provider=`True` overlap=`False`

## NPU Micro Support
- round `0` status=`finished` class=`provider_empty_response` provider=`False` overlap=`True` tools=`4`

```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `15043`
- SHA-256: `39238e050caac6801e32c1f2c493c686ad936128de7b8131b0bedc02fd8fe3a0`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-07T09:36:17",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [
    "round 2: invalid tool requests: [\"tool_requests[0].tool not allowlisted: 'build_agent_review_patch_plan.py'\"]"
  ],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 2,
  "elapsed_seconds": 34.586,
  "context_file_count": 24,
  "round_count": 2,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 14.106,
      "file_count": 2,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/_ia_carmine_md_split_manifest.json",
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md"
      ],
      "live_context_report_count": 1,
      "live_context_refresh_performed": true,
      "response_chars": 964,
      "raw_response_preview": "{\n  \"summary\": \"The repository review evidence is ready for conversion into schema-valid recommendations.\",\n  \"confidence\": \"medium\",\n  \"recommendations\": [\n    {\n      \"id\": \"rec_convert_evidence_to_recommendations\",\n      \"area\": \"workflow\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"output/patch_specs/agent_review_code_patch_plan.json\"\n      ],\n      \"rationale\": \"The repository evidence is available and ready for conversion into schema-valid recommendations.\",\n      \"proposed_strategy\": \"Run the script `Tools/ai/build_agent_review_code_patch_plan.py` to generate the patch plan.\",\n      \"risk\": \"low\",\n      \"validation_commands\": [\n        \"python Tools/validation/run_agent_review_code_patch_plan_smoke.py\"\n      ],\n      \"stop_conditions\": [\n        \"Manual review of the generated patch plan.\"\n      ]\n    }\n  ],\n  \"tool_requests\": [],\n  \"missing_evidence\": [],\n  \"next_best_action\": \"build_agent_review_patch_plan.py\"\n}",
      "parsed_response": {
        "summary": "The repository review evidence is ready for conversion into schema-valid recommendations.",
        "confidence": "medium",
        "recommendations": [
          {
            "id": "rec_convert_evidence_to_recommendations",
            "area": "workflow",
            "status": "ready_for_patch_plan",
            "target_files": [
              "output/patch_specs/agent_review_code_patch_plan.json"
            ],
            "rationale": "The repository evidence is available and ready for conversion into schema-valid recommendations.",
            "proposed_strategy": "Run the script `Tools/ai/build_agent_review_code_patch_plan.py` to generate the patch plan.",
            "risk": "low",
            "validation_commands": [
              "python Tools/validation/run_agent_review_code_patch_plan_smoke.py"
            ],
            "stop_conditions": [
              "Manual review of the generated patch plan."
            ]
          }
        ],
        "tool_requests": [],
        "missing_evidence": [],
        "next_best_action": "build_agent_review_patch_plan.py"
      },
      "schema_repair_retry": {
        "attempted": false,
        "accepted": false,
        "reason": "not_needed",
        "json_ok": null,
        "schema_ok": null,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": ""
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "provider_tool_request_count": 0,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": true,
      "parse_error": "",
      "schema_ok": true,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "",
      "contract": {
        "json_ok": true,
        "schema_ok": true,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [],
        "raw_response_sha256": "75555688a58af3e14e23ff597d50d876e7ae68bc0e0630c43f3af83bd25cd477",
        "raw_response_chars": 964,
        "top_level_keys": [
          "confidence",
          "missing_evidence",
          "next_best_action",
          "recommendations",
          "summary",
          "tool_requests"
        ],
        "recommendation_count": 1,
        "valid_recommendation_count": 1,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": ""
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 1,
      "filtered_recommendation_count": 1,
      "recommendation_count": 1,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "",
      "evidence_ready_for_manual_patch_count": 0,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 19.843,
      "file_count": 2,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-002.md",
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/README.md"
      ],
      "live_context_report_count": 1,
      "live_context_refresh_performed": true,
      "response_chars": 691,
      "raw_response_preview": "{\n  \"summary\": \"The repository contains documentation for code patch plans, but no schema-valid recommendations or tool requests have been generated.\",\n  \"confidence\": \"low\",\n  \"recommendations\": [],\n  \"tool_requests\": [\n    {\n      \"id\": \"need_schema_valid_recommendations\",\n      \"tool\": \"build_agent_review_patch_plan.py\",\n      \"reason\": \"No schema-valid recommendations or broker-compatible tool_requests have been generated from the available evidence.\",\n      \"args\": {}\n    }\n  ],\n  \"missing_evidence\": [\n    \"schema-valid recommendations or broker-compatible tool_requests\"\n  ],\n  \"next_best_action\": \"run requested broker tools, then retry schema-valid recommendation generation\"\n}",
      "parsed_response": {
        "summary": "The repository contains documentation for code patch plans, but no schema-valid recommendations or tool requests have been generated.",
        "confidence": "low",
        "recommendations": [],
        "tool_requests": [
          {
            "id": "need_schema_valid_recommendations",
            "tool": "build_agent_review_patch_plan.py",
            "reason": "No schema-valid recommendations or broker-compatible tool_requests have been generated from the available evidence.",
            "args": {}
          }
        ],
        "missing_evidence": [
          "schema-valid recommendations or broker-compatible tool_requests"
        ],
        "next_best_action": "run requested broker tools, then retry schema-valid recommendation generation"
      },
      "schema_repair_retry": {
        "attempted": true,
        "accepted": false,
        "reason": "schema_repair_retry_rejected",
        "json_ok": true,
        "schema_ok": false,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [
        "tool_requests[0].tool not allowlisted: 'build_agent_review_patch_plan.py'"
      ],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "provider_tool_request_count": 0,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "tool_requests[0].tool not allowlisted: 'build_agent_review_patch_plan.py'"
      ],
      "context_echo_detected": false,
      "model_output_schema_mismatch": true,
      "contract_empty_recommendations_reason": "model_output_schema_mismatch",
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "tool_requests[0].tool not allowlisted: 'build_agent_review_patch_plan.py'"
        ],
        "raw_response_sha256": "dba417626f601d75cd6809f3ea06e199781d97f597b929124e44cea631e7c43d",
        "raw_response_chars": 691,
        "top_level_keys": [
          "confidence",
          "missing_evidence",
          "next_best_action",
          "recommendations",
          "summary",
          "tool_requests"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 1,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 1,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 1,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 1,
      "empty_recommendations_reason": "model_output_schema_mismatch",
      "evidence_ready_for_manual_patch_count": 0,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    }
  ],
  "npu_audit_count": 0,
  "npu_audit_requested_count": 0,
  "npu_audit_success_count": 0,
  "npu_auditor_disabled_reason": "",
  "npu_audits": [],
  "runtime_tool_broker_enabled": false,
  "runtime_tool_bootstrap_enabled": false,
  "runtime_tool_bootstrap_executed": false,
  "runtime_tool_bootstrap_passed": null,
  "runtime_tool_bootstrap_request_count": 0,
  "runtime_tool_bootstrap_execution_count": 0,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_bootstrap_result_count": 0,
  "runtime_tool_bootstrap_output": "",
  "runtime_tool_bootstrap": {
    "enabled": false,
    "executed": false,
    "bootstrap": true,
    "requested_tool_count": 0,
    "tool_results": [],
    "guardrails": {
      "bootstrap_requires_enable_runtime_tool_broker": true,
      "patch_application_performed": false,
      "persistent_memory_write_performed": false
    }
  },
  "runtime_tool_request_count": 0,
  "runtime_tool_execution_count": 0,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 0,
  "runtime_tool_provider_request_execution_count": 0,
  "runtime_tool_feedback_context_report_count": 0,
  "live_context_refresh_enabled": true,
  "live_context_report_paths": [
    "output/ai_runtime_heap/py_live_seed_20260507-094320/snapshot.json"
  ],
  "live_context_refresh_count": 2,
  "deterministic_runtime_tool_fallback_request_count": 0,
  "deterministic_runtime_tool_fallback_execution_count": 0,
  "deterministic_runtime_tool_fallback_failed_count": 0,
  "deterministic_runtime_tool_fallback_blocked_count": 0,
  "provider_empty_response_count": 0,
  "provider_error_count": 0,
  "schema_repair_retry_attempt_count": 1,
  "schema_repair_retry_accept_count": 0,
  "recommendation_count": 1,
  "recommendations": [
    {
      "id": "rec_convert_evidence_to_recommendations",
      "area": "workflow",
      "status": "ready_for_patch_plan",
      "target_files": [
        "output/patch_specs/agent_review_code_patch_plan.json"
      ],
      "rationale": "The repository evidence is available and ready for conversion into schema-valid recommendations.",
      "proposed_strategy": "Run the script `Tools/ai/build_agent_review_code_patch_plan.py` to generate the patch plan.",
      "risk": "low",
      "validation_commands": [
        "python Tools/validation/run_agent_review_code_patch_plan_smoke.py"
      ],
      "stop_conditions": [
        "Manual review of the generated patch plan."
      ]
    }
  ],
  "json_parse_error_count": 0,
  "context_echo_detected_count": 0,
  "model_output_schema_mismatch_count": 1,
  "parse_error": "",
  "repair_attempt_count": 0,
  "raw_recommendation_candidate_count": 1,
  "filtered_recommendation_count": 1,
  "tool_request_count": 1,
  "valid_tool_request_count": 0,
  "invalid_tool_request_count": 1,
  "empty_recommendations_reason": "",
  "evidence_ready_for_manual_patch_count": 0,
  "provider_tool_request_absence_reason": "",
  "recommended_next_layer": "build_agent_review_patch_plan.py",
  "decision": {
    "ready_for_patch_plan": true,
    "ready_count": 1,
    "needs_more_context_count": 0,
    "fallback_patch_plan_recommended": false,
    "npu_auditor_non_blocking": true,
    "npu_unusable_or_failed_count": 0,
    "npu_audit_success_count": 0,
    "npu_auditor_disabled_reason": "",
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "manual_review_required": true
  },
  "inputs": {
    "evidence_kind": "agent_review_evidence_sufficiency",
    "refined_kind": null,
    "context_report_count": 15
  },
  "guardrails": {
    "provider_execution_requires_use_ollama": true,
    "npu_auditor_requires_include_npu_auditor": true,
    "npu_auditor_non_blocking": true,
    "npu_primary_advisory": false,
    "patch_application_performed": false,
    "real_github_pr_created": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "runtime_tool_broker_report_only": true,
    "runtime_tool_broker_requires_enable_runtime_tool_broker": true,
    "manual_review_required": true
  }
}

```

### `output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1432`
- SHA-256: `dd6591d54beb3da5af78901afc3c1c70203f5925af0d9f433144a330180b5788`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `34.586`
- Round count: `2`
- Recommendation count: `1`
- Raw recommendation candidates: `1`
- Filtered recommendation count: `1`
- Tool request count: `1`
- Valid tool request count: `0`
- Invalid tool request count: `1`
- JSON parse error count: `0`
- Context echo detected count: `0`
- Model output schema mismatch count: `1`
- Empty recommendations reason: ``
- Evidence ready for manual patch count: `0`

## Decision

- `ready_for_patch_plan`: `True`
- `ready_count`: `1`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `False`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations

### rec_convert_evidence_to_recommendations — workflow
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['output/patch_specs/agent_review_code_patch_plan.json']`
- Rationale: The repository evidence is available and ready for conversion into schema-valid recommendations.
- Strategy: Run the script `Tools/ai/build_agent_review_code_patch_plan.py` to generate the patch plan.


```

### `output/ai_pipeline/gpu0_peer_support_parallel_py_live_seed_20260507-094320/round_000_gpu0_peer_support.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1733`
- SHA-256: `c6a5254ba6e65c26d51871b8cbeb2d55fab2a617c40705bc2d27e7b06a96078b`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 2,
  "kind": "openvino_gpu0_secondary_workload",
  "generated_at": "2026-05-07T09:35:42",
  "provider_execution_requested": true,
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "media_runtime_performed": false,
  "openvino_gpu0_visible": true,
  "openvino_gpu0_probe_performed": true,
  "openvino_gpu0_workload_performed": true,
  "openvino_gpu0_workload_passed": true,
  "openvino_gpu0_provider_execution_performed": true,
  "openvino_gpu0_role": "peer_support_round_000",
  "openvino_gpu0_not_primary_advisory": false,
  "openvino_gpu0_support_lane": true,
  "openvino_gpu0_sustained_workload_requested": true,
  "openvino_gpu0_sustained_workload_performed": true,
  "openvino_gpu0_sustained_iterations_requested": 24,
  "openvino_gpu0_sustained_iterations_performed": 7425,
  "openvino_gpu0_sustained_min_seconds_requested": 1.0,
  "openvino_gpu1_reserved_visible": true,
  "openvino_gpu1_workload_performed": false,
  "openvino_gpu1_openvino_workload_allowed": false,
  "openvino_gpu1_role": "reserved_for_cuda_ollama",
  "selected_device": "GPU.0",
  "available_devices": [
    "CPU",
    "GPU.0",
    "GPU.1",
    "NPU"
  ],
  "elapsed_seconds": 1.917144,
  "compile_seconds": 0.036489,
  "inference_seconds": 1.000024,
  "output_preview": "[1.0, 1.0, 1.0, 1.0]",
  "errors": [],
  "warnings": [
    "OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1."
  ],
  "passed": true,
  "production_support": true,
  "iterations": 24,
  "min_seconds": 1.0,
  "requested_role": "peer_support_round_000",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project"
}

```

### `output/ai_pipeline/gpu0_peer_support_parallel_py_live_seed_20260507-094320/round_000_gpu0_peer_support.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1010`
- SHA-256: `d9ce330cda28f7580d700120a884c4bfe37d6d1328363524143b4c1f3d34e25e`
- Content included: `True`
- Content truncated: `False`

```text
# OpenVINO GPU.0 secondary workload

- Passed: `True`
- Provider execution performed: `True`
- Production support: `True`
- Iterations: `24`
- Minimum seconds: `1.0`
- Requested role: `peer_support_round_000`
- GPU.0 visible: `True`
- GPU.0 probe performed: `True`
- GPU.0 workload performed: `True`
- GPU.0 workload passed: `True`
- GPU.0 role: `peer_support_round_000`
- GPU.0 support lane: `True`
- GPU.0 sustained requested: `True`
- GPU.0 sustained performed: `True`
- GPU.0 iterations requested: `24`
- GPU.0 iterations performed: `7425`
- GPU.0 min seconds requested: `1.0`
- GPU.1 reserved visible: `True`
- GPU.1 workload performed: `False`
- Selected device: `GPU.0`
- Available devices: `['CPU', 'GPU.0', 'GPU.1', 'NPU']`
- Elapsed seconds: `1.917144`
- Compile seconds: `0.036489`
- Inference seconds: `1.000024`

## Output preview

[1.0, 1.0, 1.0, 1.0]

## Errors
- none

## Warnings
- OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.

```

### `output/ai_pipeline/npu_micro_support_parallel_py_live_seed_20260507-094320/round_000_npu_micro_support.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1187`
- SHA-256: `5abfbc46840176f3a6b58661f84ec8cbade617bc3646a43dfac9bce198162284`
- Content included: `True`
- Content truncated: `False`

```text
# NPU GPU Deep Review Audit

- Passed: `True`
- Non-blocking: `True`
- NPU Python: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- NPU Python exists: `True`
- Provider execution requested: `True`
- Provider load attempted: `False`
- Provider execution succeeded: `False`
- Provider empty response: `True`
- Dependency missing: `False`
- Patch application performed: `False`
- Classification: `provider_empty_response`
- Runtime tool context seen: `True`
- Runtime tool context report count: `2`
- Tool request count: `4`
- GPU review blocked: `False`

## Warnings
- TimeoutExpired: 35s
- NPU auditor command returned 124
- NPU provider returned an empty response

## Decision
- `gpu_review_blocked`: `False`
- `npu_primary_advisory`: `False`
- `npu_audit_usable`: `False`
- `npu_dependency_missing`: `False`
- `npu_provider_empty_response`: `True`
- `npu_python_missing`: `False`
- `runtime_tool_context_seen`: `True`
- `runtime_tool_context_report_count`: `2`
- `npu_tool_requests_available`: `True`
- `npu_tool_request_count`: `4`
- `recommendation`: `continue_manual_review; treat NPU audit as non-blocking guardrail signal only`

```

### `output/analysis/code_interpreter_full_toolbox_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7129`
- SHA-256: `b35cb243feeb72ce7136ddec9be3681e27c59623b613d928a90fd228a7b16636`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `588`
- Parsed files: `588`
- Total lines: `100772`
- Total functions: `3612`
- Total classes: `101`
- Risk signals: `90`
- TODO/FIXME markers: `21`
- Recommendation count: `184`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` - `2434` lines, risk `high`
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

### `output/analysis/gpu_json_contract_replay_full_toolbox_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `644`
- SHA-256: `6bf838c5fb4bbea4eba84e3f82df39f549d234c575812a59a0af8dd7b39b0560`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `2`
- Context echo detected: `0`
- JSON parse failures: `0`
- Schema mismatches: `1`
- Valid recommendation outputs: `1`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `model_output_schema_mismatch`: `1`
- `valid_recommendation_output`: `1`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_full_toolbox_py_live_seed_20260507-094320.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5691`
- SHA-256: `f925ab35719d741591dc8244157004ff18abbb3086c75a755b99a3aa39580a77`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-07T09:36:26",
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
    "orchestrator": "output/ai_pipeline/full_toolbox_py_live_seed_20260507-094320_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 2,
    "npu_audit_count": 1,
    "legacy_npu_audit_count": 0,
    "npu_micro_support_count": 1,
    "npu_micro_support_overlap_count": 1,
    "gpu0_peer_support_count": 3,
    "gpu0_peer_support_overlap_count": 2,
    "npu_audit_success_count": 1,
    "npu_audit_round_coverage": 0.5,
    "avg_gpu_round_seconds": 23.488,
    "p50_gpu_round_seconds": 23.488,
    "p90_gpu_round_seconds": 23.488,
    "avg_npu_audit_seconds": 40.0,
    "p50_npu_audit_seconds": 40.0,
    "p90_npu_audit_seconds": 40.0,
    "npu_to_gpu_avg_duration_ratio": 1.703,
    "gpu_elapsed_seconds": 46.976,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.001,
    "gpu": {
      "elapsed_seconds": 46.976,
      "round_count": 2,
      "round_duration_source": "gpu_elapsed_divided_by_round_count",
      "round_duration_sample_count": 1,
      "avg_round_seconds": 23.488,
      "p50_round_seconds": 23.488,
      "p90_round_seconds": 23.488,
      "max_round_seconds": 23.488,
      "round_durations_total_seconds": 23.488,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 15,
        "runtime_tool_execution_count": 14,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 1,
        "runtime_tool_provider_request_count": 8,
        "runtime_tool_provider_request_execution_count": 7,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0
      },
      "embedded_performance": {}
    },
    "npu": {
      "audit_count": 1,
      "audit_requested_count": 1,
      "audit_success_count": 1,
      "duration_sample_count": 1,
      "avg_audit_seconds": 40.0,
      "p50_audit_seconds": 40.0,
      "p90_audit_seconds": 40.0,
      "max_audit_seconds": 40.0,
      "audit_durations_total_seconds": 40.0,
      "status_counts": {
        "finished": 1
      },
      "classification_counts": {
        "provider_empty_response": 1
      },
      "lane_diagnostics": {}
    },
    "sync": {
      "npu_to_gpu_avg_duration_ratio": 1.703,
      "npu_audit_round_coverage": 0.5,
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
      "GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate.",
      "NPU audits are usable; tune cadence rather than disabling the lane."
    ],
    "parameters": {
      "npu_auditor_every_rounds": 2,
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
    "GPU/NPU cadence is measurable; tune audit frequency from timing evidence rather than intuition.",
    "GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.",
    "Runtime tool execution had failed or blocked requests; recommendations should reference broker evidence before proposing patches."
  ],
  "refactoring_suggestions": [
    {
      "priority": "high",
      "area": "gpu_runner_timing",
      "recommendation": "Use rounds[*].elapsed_seconds as the primary GPU round timing source.",
      "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count",
      "guardrail": "report_only_no_provider_setting_change"
    },
    {
      "priority": "medium",
      "area": "runtime_tool_broker",
      "recommendation": "Surface failed/blocked runtime tool IDs in the next decision-loop patch plan input.",
      "evidence": "failed=0, blocked=1",
      "guardrail": "broker_report_only"
    }
  ],
  "decision": {
    "npu_too_slow_for_per_round_lockstep": true,
    "recommended_next_layer": "feed timing-backed GPU/NPU suggestions into decision-loop patch planning",
    "manual_review_required": true
  }
}

```

### `output/analysis/gpu_npu_run_sync_full_toolbox_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2619`
- SHA-256: `3390ff3d508893a9d660d3622a042b869137f329081661e0746b81bd45aebc07`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `2`
- `npu_audit_count`: `1`
- `legacy_npu_audit_count`: `0`
- `npu_micro_support_count`: `1`
- `npu_micro_support_overlap_count`: `1`
- `gpu0_peer_support_count`: `3`
- `gpu0_peer_support_overlap_count`: `2`
- `npu_audit_success_count`: `1`
- `npu_audit_round_coverage`: `0.5`
- `avg_gpu_round_seconds`: `23.488`
- `p50_gpu_round_seconds`: `23.488`
- `p90_gpu_round_seconds`: `23.488`
- `avg_npu_audit_seconds`: `40.0`
- `p50_npu_audit_seconds`: `40.0`
- `p90_npu_audit_seconds`: `40.0`
- `npu_to_gpu_avg_duration_ratio`: `1.703`
- `gpu_elapsed_seconds`: `46.976`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `46.976`
- GPU average round seconds: `23.488`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- GPU timing sample count: `1`
- GPU round durations total seconds: `23.488`
- NPU average audit seconds: `40.0`
- NPU duration sample count: `1`

## Operational opinions

- GPU/NPU cadence is measurable; tune audit frequency from timing evidence rather than intuition.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.
- Runtime tool execution had failed or blocked requests; recommendations should reference broker evidence before proposing patches.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count
- `medium` `runtime_tool_broker`: Surface failed/blocked runtime tool IDs in the next decision-loop patch plan input. Evidence: failed=0, blocked=1

## Suggested balanced profile

- `npu_auditor_every_rounds`: `2`
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

- GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate.
- NPU audits are usable; tune cadence rather than disabling the lane.


```

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_py_live_seed_20260507-094320.md`

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

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_py_live_seed_20260507-094320.md`

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

### `output/validation/full_memory_tool_regeneration_py_live_seed_20260507-094320_workflow.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3294`
- SHA-256: `aee5796c3fa3e778a929196201a0b92230bd91bc4357c8bc81503d123d3a06ba`
- Content included: `True`
- Content truncated: `False`

```text
# Full Memory / Tool Regeneration Workflow

- Passed: `True`
- Stamp: `py_live_seed_20260507-094320`
- Profile: `full_refactor`
- Report count: `13`
- Artifact count: `14`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`
- Persistent memory write performed: `False`

## Reports

- `.\output\ai_pipeline\full_memory_tool_regeneration_py_live_seed_20260507-094320_agent_memory_inventory.json`
- `.\output\ai_pipeline\full_memory_tool_regeneration_py_live_seed_20260507-094320_agnostic_tool_inventory.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_persistent_memory_status.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_operational_memory_status.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_memory_routing_policy.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_runtime_tool_broker.json`
- `.\output\ai_pipeline\full_memory_tool_regeneration_py_live_seed_20260507-094320_transient_request_context.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_python_line_count.json`
- `.\output\analysis\full_memory_tool_regeneration_py_live_seed_20260507-094320_code_interpreter.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_python_syntax.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_validation_report_contract.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_runtime_tool_broker_smoke.json`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_memory_routing_policy_smoke.json`

## Artifacts

- `.\docs\LOCAL_AI_TASKS\full-memory-tool-regeneration-procedure.md`
- `.\Tools\workflow\run_full_memory_tool_regeneration.ps1`
- `.\output\ai_pipeline\full_memory_tool_regeneration_py_live_seed_20260507-094320_agent_memory_inventory.md`
- `.\output\ai_pipeline\full_memory_tool_regeneration_py_live_seed_20260507-094320_agnostic_tool_inventory.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_persistent_memory_status.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_operational_memory_status.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_memory_routing_policy.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_runtime_tool_broker.md`
- `.\output\ai_pipeline\full_memory_tool_regeneration_py_live_seed_20260507-094320_transient_request_context.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_python_line_count.md`
- `.\docs/LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_py_live_seed_20260507-094320.csv`
- `.\output\analysis\full_memory_tool_regeneration_py_live_seed_20260507-094320_code_interpreter.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_runtime_tool_broker_smoke.md`
- `.\output\validation\full_memory_tool_regeneration_py_live_seed_20260507-094320_memory_routing_policy_smoke.md`

```

### `output/validation/gpu0_companion_contract_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `216`
- SHA-256: `060bb07dfafe4a1954edd7a1be66023a935e5170b8c3a132f23ce6aa6022bb40`
- Content included: `True`
- Content truncated: `False`

```text
# GPU0 Companion Contract

- Passed: `True`
- Selected report: `C:\Users\carmi\blender\blender-audio-project\output\validation\gpu0_companion_task_lane_py_live_seed_20260507-094320.json`
- Classifications: `[]`

```

### `output/validation/gpu0_companion_task_lane_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `757`
- SHA-256: `9dbe33a412929e913f914778d679696cdfef6866f67a17f36f8e7bf041681c2c`
- Content included: `True`
- Content truncated: `False`

```text
# GPU0 Companion Worker Lane

- Passed: `True`
- Production role: `companion_worker`
- Companion task count: `4`
- Tool request count: `4`
- GPU0 workload passed: `True`
- Semantic execution mode: `model_unconfigured_numeric_tool_companion`

## Tasks
- `gpu0_companion_provider_warning_triage`: Classify provider/Ollama warnings before the primary planner treats the run as green.
- `gpu0_companion_npu_audit_precompute`: Precompute compact evidence signals that can be attached to NPU audit checkpoints.
- `gpu0_companion_patch_plan_evidence_check`: Score whether recommendations and patch plans reference available evidence.
- `gpu0_companion_failed_report_root_cause_scan`: Scan failed reports and produce root-cause hints for GPU1/Ollama.

```

### `output/validation/gpu0_peer_runtime_tool_broker_py_live_seed_20260507-094320.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2482`
- SHA-256: `1ee3ed1762f6c381d8bc9b0fc5616c221151bee7aa0b99a11da4ce578dcfe6ab`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Runtime Tool Broker

- passed: `True`
- dry_run: `False`
- request_file: `output/validation/gpu0_tool_requests_py_live_seed_20260507-094320.json`
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
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.json', 'markdown_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/gpu0_peer/gpu0_peer_code_interpreter_context_code_interpreter_report.md'}`

### `gpu0_peer_report_contract_context` — `check_validation_report_contract`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/gpu0_peer/gpu0_peer_report_contract_context_validation_report_contract.json'}`

### `gpu0_peer_refactor_duplication_context` — `build_refactor_duplication_audit`

- Executed: `True`
- Blocked: `False`
- Return code: `0`
- Outputs: `{'json_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/gpu0_peer/gpu0_peer_refactor_duplication_context_refactor_duplication_audit.json', 'markdown_report': 'output/ai_runtime_tools/py_live_seed_20260507-094320/gpu0_peer/gpu0_peer_refactor_duplication_context_refactor_duplication_audit.md'}`

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
