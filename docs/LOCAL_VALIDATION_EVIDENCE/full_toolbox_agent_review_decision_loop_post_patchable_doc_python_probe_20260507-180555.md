# Local Validation Evidence Bundle

- Generated at: `2026-05-07T18:09:05`
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

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `collect_more_evidence`

### `output/analysis/repository_consistency_map_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `190`

### `output/validation/python_line_count_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/openvino_hardware_governance_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_hardware_governance_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['GPU.1 is visible to OpenVINO but reserved for Ollama/CUDA; do not route OpenVINO work there by default.', 'NPU startup mode may contend with GPU0/GPU1 on short live provider runs; deferred is preferred for local workstation use.', 'IA_CARMINE_GPU0_COMPANION_MODEL_DIR is not configured; GPU0 semantic peer mode will classify as unconfigured/fallback.']`

### `output/analysis/gpu_json_contract_replay_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/provider_evidence_contract_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_evidence_contract`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `["local provider probe degraded: ['ollama: probe failed']"]`

### `output/validation/gpu0_companion_task_lane_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_worker_lane`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; semantic LLM subtasks unavailable, numeric/tool companion active.']`

### `output/validation/gpu0_companion_contract_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_contract`
- Passed: `True`

### `output/ai_pipeline/gpu0_peer_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/ai_pipeline/npu_micro_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_npu_micro_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_gpu_deep_review_audit`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['TimeoutExpired: 30s', 'NPU auditor command returned 124', 'NPU provider returned an empty response']`

### `output/validation/gpu1_primary_advisory_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu1_primary_advisory`
- Passed: `True`
- Provider execution performed: `True`
- Recommendation count: `0`

### `output/validation/gpu0_peer_task_packet_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_task_packet`
- Passed: `True`

### `output/validation/gpu0_peer_response_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_response`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only.']`

### `output/validation/gpu0_tool_requests_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_tool_requests`
- Passed: `None`

### `output/validation/gpu0_peer_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/npu_micro_peer_assistant_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_micro_peer_assistant`
- Passed: `True`
- Provider execution performed: `False`
- Warnings: `['Final NPU provider pass moved off the performance path; startup NPU support and broker seed evidence are reviewed by GPU1/GPU0 plus deterministic validators.']`

### `output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['Final NPU provider pass moved off the performance path; startup NPU support and broker seed evidence are reviewed by GPU1/GPU0 plus deterministic validators.']`

### `output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.json`

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
- NPU support lane: `{'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': False, 'tool_request_count': 0, 'broker_tool_execution_count': 0, 'provider_execution_requested': False, 'provider_execution_performed': False, 'provider_slow_or_degraded': False, 'classification': 'npu_final_provider_moved_to_gpu_peer_review', 'deterministic_fallback_used': False, 'product_pass_blocker': False}`
- Peer mesh lane state: `{'schema_version': 1, 'kind': 'peer_mesh_lane_state', 'operational_lanes': ['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support'], 'support_lanes': ['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply'], 'degraded_lanes': ['gpu0_semantic_companion_model_unconfigured'], 'product_blockers': [], 'gpu0_broker_tool_execution_count': 3, 'npu_broker_tool_execution_count': 0, 'broker_runtime_tool_execution_count': 3, 'legacy_usable_lanes_are_workload_quality_only': True, 'npu_degraded_is_product_blocker': False, 'npu_heavy_audit_authority': False, 'all_required_product_lanes_present': True, 'mesh_visibility': {'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': False, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': False, 'npu_tool_requests_broker_consumed': False, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}, 'npu_support_lane': {'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': False, 'tool_request_count': 0, 'broker_tool_execution_count': 0, 'provider_execution_requested': False, 'provider_execution_performed': False, 'provider_slow_or_degraded': False, 'classification': 'npu_final_provider_moved_to_gpu_peer_review', 'deterministic_fallback_used': False, 'product_pass_blocker': False}}`

### `output/validation/ai_peer_exchange_contract_post_patchable_doc_python_probe_20260507-180555.json`

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
- Peer mesh lane state: `{'schema_version': 1, 'kind': 'peer_mesh_lane_state', 'operational_lanes': ['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support'], 'support_lanes': ['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply'], 'degraded_lanes': ['gpu0_semantic_companion_model_unconfigured'], 'product_blockers': [], 'gpu0_broker_tool_execution_count': 3, 'npu_broker_tool_execution_count': 0, 'broker_runtime_tool_execution_count': 3, 'legacy_usable_lanes_are_workload_quality_only': True, 'npu_degraded_is_product_blocker': False, 'npu_heavy_audit_authority': False, 'all_required_product_lanes_present': True, 'mesh_visibility': {'schema_version': 1, 'kind': 'ai_peer_mesh_visibility', 'all_lanes_visible': True, 'gpu1_sees_gpu0_response': True, 'gpu1_sees_gpu0_broker_results': True, 'gpu1_sees_npu_support_signal': True, 'gpu1_sees_npu_broker_results': False, 'gpu0_sees_gpu1_primary_advisory': True, 'gpu0_sees_deterministic_reports': True, 'gpu0_produces_tool_requests_for_gpu1': True, 'gpu0_tool_requests_broker_consumed': True, 'npu_sees_gpu1_gpu0_broker_context': True, 'npu_support_tool_requests_available': False, 'npu_tool_requests_broker_consumed': False, 'deterministic_scripts_visible_to_gpu0': True, 'runtime_tool_broker_visible_to_all_lanes': True, 'npu_non_blocking_support_lane': True}, 'npu_support_lane': {'role': 'npu_non_blocking_tool_support_lane', 'non_blocking': True, 'blocking': False, 'heavy_audit_authority': False, 'tool_supply_support': False, 'tool_request_count': 0, 'broker_tool_execution_count': 0, 'provider_execution_requested': False, 'provider_execution_performed': False, 'provider_slow_or_degraded': False, 'classification': 'npu_final_provider_moved_to_gpu_peer_review', 'deterministic_fallback_used': False, 'product_pass_blocker': False}}`

### `output/validation/provider_runtime_heap_live_signals_init_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_gpu1_request_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_broker_results_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_npu_support_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/validation/provider_runtime_heap_live_signals_tool_catalog_complete_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_live_signals`
- Passed: `True`

### `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/snapshot.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_snapshot`
- Passed: `None`

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_telemetry`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_post_patchable_doc_python_probe_20260507-180555_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/provider_runtime_heap_from_peer_reports_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_runtime_heap_from_peer_reports`
- Passed: `True`

### `docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `patch_plan_quality_product_gate`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `patch_notes_quality_product`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['full_toolbox_telemetry: missing (C:\\Users\\carmi\\blender\\blender-audio-project\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_run_telemetry_summary_post_patchable_doc_python_probe_20260507-180555.json)']`

### `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product_evidence_index.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_evidence_index`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product_readiness.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full0to10_final_tool_product_readiness`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `240`

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_decision_loop.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `240`
- Recommendation count: `240`
- Warnings: `['patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection']`

### `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `240`
- Warnings: `['max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection']`
- Patch plan summary count: `240`
- Fallback used: `False`
- Manual review required: `True`

## Patch plan summary

### `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.json`

- Patch plan count: `240`
- Fallback used: `False`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### consistency_001 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_review_code_patch_plan.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_agent_review_code_patch_plan.py:20` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py:20`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_002 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138` targeting `text
Tools/ai/simulate_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
Tools/ai/simulate_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_003 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT.md:60` targeting `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT.md:60`. Target `CHATGPT.md` and resolve `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_004 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/analyze_gpu_npu_run_sync.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/analyze_gpu_npu_run_sync.py` targeting `Tools/ai/analyze_gpu_npu_run_sync.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/analyze_gpu_npu_run_sync.py`. Target `Tools/ai/analyze_gpu_npu_run_sync.py` and resolve `Tools/ai/analyze_gpu_npu_run_sync.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_005 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_edit_proposal_from_plan.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_edit_proposal_from_plan.py:26` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_edit_proposal_from_plan.py:26`. Target `Tools/ai/build_code_edit_proposal_from_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_006 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139` targeting `Tools/ai/simulate_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `Tools/ai/simulate_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_007 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52` targeting `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_008 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_agnostic_tool_inventory.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_agnostic_tool_inventory.py` targeting `Tools/ai/build_agent_agnostic_tool_inventory.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_agnostic_tool_inventory.py`. Target `Tools/ai/build_agent_agnostic_tool_inventory.py` and resolve `Tools/ai/build_agent_agnostic_tool_inventory.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_009 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_patch_artifact_pack.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_artifact_pack.py:22` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_patch_artifact_pack.py:22`. Target `Tools/ai/build_code_patch_artifact_pack.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_010 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156` targeting `text
Tools/ai/run_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
Tools/ai/run_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_011 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17` targeting `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_012 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_review_code_patch_plan.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_code_patch_plan.py` targeting `Tools/ai/build_agent_review_code_patch_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools/ai/build_agent_review_code_patch_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_013 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_patch_docs_followup.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_docs_followup.py:22` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_patch_docs_followup.py:22`. Target `Tools/ai/build_code_patch_docs_followup.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_014 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157` targeting `Tools/ai/run_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `Tools/ai/run_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_015 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52` targeting `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_016 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_review_evidence_sufficiency.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_evidence_sufficiency.py` targeting `Tools/ai/build_agent_review_evidence_sufficiency.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_evidence_sufficiency.py`. Target `Tools/ai/build_agent_review_evidence_sufficiency.py` and resolve `Tools/ai/build_agent_review_evidence_sufficiency.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_017 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/enrich_github_evidence_bundle_code_plan.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23` targeting `Tools.ai.build_github_evidence_bundle`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23`. Target `Tools/ai/enrich_github_evidence_bundle_code_plan.py` and resolve `Tools.ai.build_github_evidence_bundle` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_018 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230` targeting `check_runtime_hardware_capability_manifest.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `check_runtime_hardware_capability_manifest.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_019 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:55` targeting `hardware-memory.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:55`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `hardware-memory.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_020 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_review_patch_bundle.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_patch_bundle.py` targeting `Tools/ai/build_agent_review_patch_bundle.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_patch_bundle.py`. Target `Tools/ai/build_agent_review_patch_bundle.py` and resolve `Tools/ai/build_agent_review_patch_bundle.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_025 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/enrich_github_evidence_bundle_code_plan.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/enrich_github_evidence_bundle_code_plan.py:28` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/enrich_github_evidence_bundle_code_plan.py:28`. Target `Tools/ai/enrich_github_evidence_bundle_code_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_022 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_023 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:64` targeting `text
02-sqlite-heap-memory-design.md/
  README.md
  01-schema.md
  02-chunking.md
  03-search.md
  04-cli.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:64`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
02-sqlite-heap-memory-design.md/
  README.md
  01-schema.md
  02-chunking.md
  03-search.md
  04-cli.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_024 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_review_patch_plan.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_patch_plan.py` targeting `Tools/ai/build_agent_review_patch_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_patch_plan.py`. Target `Tools/ai/build_agent_review_patch_plan.py` and resolve `Tools/ai/build_agent_review_patch_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_029 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/build_python_line_count_csv.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/validation/build_python_line_count_csv.py:24` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/validation/build_python_line_count_csv.py:24`. Target `Tools/validation/build_python_line_count_csv.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_026 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:133` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:133`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_027 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:68` targeting `02-chunking.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:68`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `02-chunking.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_028 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_agent_state_packet.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_state_packet.py` targeting `Tools/ai/build_agent_state_packet.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_state_packet.py`. Target `Tools/ai/build_agent_state_packet.py` and resolve `Tools/ai/build_agent_state_packet.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_033 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/check_artifact_domain_registry.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/validation/check_artifact_domain_registry.py:18` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/validation/check_artifact_domain_registry.py:18`. Target `Tools/validation/check_artifact_domain_registry.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_030 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/README.md:48` targeting `pipeline.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/README.md:48`. Target `Scripting/README.md` and resolve `pipeline.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_031 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:70` targeting `04-cli.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:70`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `04-cli.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_032 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_ai_context_pack.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_ai_context_pack.py` targeting `Tools/ai/build_ai_context_pack.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_ai_context_pack.py`. Target `Tools/ai/build_ai_context_pack.py` and resolve `Tools/ai/build_ai_context_pack.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_041 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/check_blender_shared_compat_smoke.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/validation/check_blender_shared_compat_smoke.py:35` targeting `Scripting.shared`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/validation/check_blender_shared_compat_smoke.py:35`. Target `Tools/validation/check_blender_shared_compat_smoke.py` and resolve `Scripting.shared` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_034 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/README.md:56` targeting `encode.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/README.md:56`. Target `Scripting/README.md` and resolve `encode.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_035 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:91` targeting `text
<topic>.md/
  README.md
  01-overview.md
  02-contract.md
  03-commands.md
  04-validation.md
  05-next-steps.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:91`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
<topic>.md/
  README.md
  01-overview.md
  02-contract.md
  03-commands.md
  04-validation.md
  05-next-steps.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_036 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_edit_proposal_from_plan.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_code_edit_proposal_from_plan.py` targeting `Tools/ai/build_code_edit_proposal_from_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_code_edit_proposal_from_plan.py`. Target `Tools/ai/build_code_edit_proposal_from_plan.py` and resolve `Tools/ai/build_code_edit_proposal_from_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_045 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/run_agent_review_code_patch_plan_smoke.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/validation/run_agent_review_code_patch_plan_smoke.py:19` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/validation/run_agent_review_code_patch_plan_smoke.py:19`. Target `Tools/validation/run_agent_review_code_patch_plan_smoke.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_038 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md:11` targeting `text
main_ready_to_jazz_wow_youtube.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md:11`. Target `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md` and resolve `text
main_ready_to_jazz_wow_youtube.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_039 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:94` targeting `01-overview.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:94`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `01-overview.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_040 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_interpreter_report.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_code_interpreter_report.py` targeting `Tools/ai/build_code_interpreter_report.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_code_interpreter_report.py`. Target `Tools/ai/build_code_interpreter_report.py` and resolve `Tools/ai/build_code_interpreter_report.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_053 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/run_code_edit_proposal_smoke.py']
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/validation/run_code_edit_proposal_smoke.py:29` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/validation/run_code_edit_proposal_smoke.py:29`. Target `Tools/validation/run_code_edit_proposal_smoke.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

#### consistency_042 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/shared/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/shared/README.md:109` targeting `text
Scripting/shared/
  README.md
  config_model.py
  panel_base.py
  scene_update.py
  diagnostics.py
  hotpatch_base.py
  scene_registry.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/shared/README.md:109`. Target `Scripting/shared/README.md` and resolve `text
Scripting/shared/
  README.md
  config_model.py
  panel_base.py
  scene_update.py
  diagnostics.py
  hotpatch_base.py
  scene_registry.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_043 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:95` targeting `02-contract.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:95`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `02-contract.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_044 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_patch_artifact_pack.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_code_patch_artifact_pack.py` targeting `Tools/ai/build_code_patch_artifact_pack.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_code_patch_artifact_pack.py`. Target `Tools/ai/build_code_patch_artifact_pack.py` and resolve `Tools/ai/build_code_patch_artifact_pack.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_046 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/shared/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/shared/README.md:112` targeting `config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/shared/README.md:112`. Target `Scripting/shared/README.md` and resolve `config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_047 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:96` targeting `03-commands.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:96`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `03-commands.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_048 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_code_patch_docs_followup.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_code_patch_docs_followup.py` targeting `Tools/ai/build_code_patch_docs_followup.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_code_patch_docs_followup.py`. Target `Tools/ai/build_code_patch_docs_followup.py` and resolve `Tools/ai/build_code_patch_docs_followup.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_050 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/shared/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/shared/README.md:113` targeting `panel_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/shared/README.md:113`. Target `Scripting/shared/README.md` and resolve `panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_051 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:97` targeting `04-validation.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:97`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `04-validation.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_052 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_dry_run_matrix_evidence_bundle.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_dry_run_matrix_evidence_bundle.py` targeting `Tools/ai/build_dry_run_matrix_evidence_bundle.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_dry_run_matrix_evidence_bundle.py`. Target `Tools/ai/build_dry_run_matrix_evidence_bundle.py` and resolve `Tools/ai/build_dry_run_matrix_evidence_bundle.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_054 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/shared/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/shared/README.md:114` targeting `scene_update.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/shared/README.md:114`. Target `Scripting/shared/README.md` and resolve `scene_update.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_055 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:98` targeting `05-next-steps.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:98`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `05-next-steps.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_056 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_full_context_golden_proposals.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_full_context_golden_proposals.py` targeting `Tools/ai/build_full_context_golden_proposals.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_full_context_golden_proposals.py`. Target `Tools/ai/build_full_context_golden_proposals.py` and resolve `Tools/ai/build_full_context_golden_proposals.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_058 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/shared/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/shared/README.md:116` targeting `hotpatch_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/shared/README.md:116`. Target `Scripting/shared/README.md` and resolve `hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_059 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:103` targeting `text
CHATGPT/<date>-<topic>/
  README.md
  01-*.md
  02-*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:103`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
CHATGPT/<date>-<topic>/
  README.md
  01-*.md
  02-*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_060 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_full_run_evidence_bundle_zip.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_full_run_evidence_bundle_zip.py` targeting `Tools/ai/build_full_run_evidence_bundle_zip.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_full_run_evidence_bundle_zip.py`. Target `Tools/ai/build_full_run_evidence_bundle_zip.py` and resolve `Tools/ai/build_full_run_evidence_bundle_zip.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_061 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/shared/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/shared/README.md:117` targeting `scene_registry.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/shared/README.md:117`. Target `Scripting/shared/README.md` and resolve `scene_registry.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_062 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/README.md:21` targeting `text
01-architecture-summary.md
02-sqlite-heap-memory-design.md
03-broker-hardware-delegation-contract.md
04-implementation-plan.md
05-reset-sync-commands.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/README.md:21`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/README.md` and resolve `text
01-architecture-summary.md
02-sqlite-heap-memory-design.md
03-broker-hardware-delegation-contract.md
04-implementation-plan.md
05-reset-sync-commands.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_063 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_github_evidence_bundle.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_github_evidence_bundle.py` targeting `Tools/ai/build_github_evidence_bundle.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_github_evidence_bundle.py`. Target `Tools/ai/build_github_evidence_bundle.py` and resolve `Tools/ai/build_github_evidence_bundle.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_064 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/v61b/PROJECT_STRUCTURE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/PROJECT_STRUCTURE.md:34` targeting `spaziotempo/features/water.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/PROJECT_STRUCTURE.md:34`. Target `Scripting/v61b/PROJECT_STRUCTURE.md` and resolve `spaziotempo/features/water.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_065 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/DISCOVERY_CONTRACT.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/DISCOVERY_CONTRACT.md:13` targeting `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/DISCOVERY_CONTRACT.md:13`. Target `CHATGPT/DISCOVERY_CONTRACT.md` and resolve `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_066 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_gpu_repair_failure_recommendation.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_gpu_repair_failure_recommendation.py` targeting `Tools/ai/build_gpu_repair_failure_recommendation.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_gpu_repair_failure_recommendation.py`. Target `Tools/ai/build_gpu_repair_failure_recommendation.py` and resolve `Tools/ai/build_gpu_repair_failure_recommendation.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_067 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/v61b/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/README.md:25` targeting `text
main_v61b.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/README.md:25`. Target `Scripting/v61b/README.md` and resolve `text
main_v61b.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_068 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/README.md:25` targeting `text
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
17. CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md
18. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
19. CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
20. AI_PATCH_BUNDLE_...[truncated]
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/README.md:25`. Target `CHATGPT/README.md` and resolve `text
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
17. CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md
18. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
19. CHATGPT/chatgpt-session-problems-and-robust-fixes-...[truncated]

#### consistency_069 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_local_ai_enrichment_plan.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_local_ai_enrichment_plan.py` targeting `Tools/ai/build_local_ai_enrichment_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_local_ai_enrichment_plan.py`. Target `Tools/ai/build_local_ai_enrichment_plan.py` and resolve `Tools/ai/build_local_ai_enrichment_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_070 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/v61b/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/README.md:90` targeting `Scripting/shared/panel_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/README.md:90`. Target `Scripting/v61b/README.md` and resolve `Scripting/shared/panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_071 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:216` targeting `text
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:216`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `text
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_072 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_patch_specs_from_proposals.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_patch_specs_from_proposals.py` targeting `Tools/ai/build_patch_specs_from_proposals.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_patch_specs_from_proposals.py`. Target `Tools/ai/build_patch_specs_from_proposals.py` and resolve `Tools/ai/build_patch_specs_from_proposals.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_073 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/v61b/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/README.md:91` targeting `Scripting/shared/hotpatch_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/README.md:91`. Target `Scripting/v61b/README.md` and resolve `Scripting/shared/hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_074 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:67` targeting `text
output/ai_packets/20260504-224354/npu_real_workload_report.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:67`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `text
output/ai_packets/20260504-224354/npu_real_workload_report.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_075 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_repository_change_proposals.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_repository_change_proposals.py` targeting `Tools/ai/build_repository_change_proposals.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_repository_change_proposals.py`. Target `Tools/ai/build_repository_change_proposals.py` and resolve `Tools/ai/build_repository_change_proposals.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_076 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/README.md:18` targeting `build_*context*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/README.md:18`. Target `Tools/npu/README.md` and resolve `build_*context*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_077 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:68` targeting `output/ai_packets/20260504-224354/npu_real_workload_report.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:68`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/ai_packets/20260504-224354/npu_real_workload_report.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_078 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_runtime_hardware_capability_manifest.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_runtime_hardware_capability_manifest.py` targeting `Tools/ai/build_runtime_hardware_capability_manifest.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_runtime_hardware_capability_manifest.py`. Target `Tools/ai/build_runtime_hardware_capability_manifest.py` and resolve `Tools/ai/build_runtime_hardware_capability_manifest.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_079 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/README.md:19` targeting `run_*pipeline*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/README.md:19`. Target `Tools/npu/README.md` and resolve `run_*pipeline*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_080 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:189` targeting `shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:189`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_081 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_selective_execution_plan.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_selective_execution_plan.py` targeting `Tools/ai/build_selective_execution_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_selective_execution_plan.py`. Target `Tools/ai/build_selective_execution_plan.py` and resolve `Tools/ai/build_selective_execution_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_082 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/repo_patch_runner/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/repo_patch_runner/README.md:34` targeting `Scripting/example.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/repo_patch_runner/README.md:34`. Target `Tools/repo_patch_runner/README.md` and resolve `Scripting/example.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_083 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md:246` targeting `text
docs/TECH_DEBT_TRACKER.md
TD-025 Python string patch hygiene
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md:246`. Target `CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md` and resolve `text
docs/TECH_DEBT_TRACKER.md
TD-025 Python string patch hygiene
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_084 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/build_semantic_evidence_chunks.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_semantic_evidence_chunks.py` targeting `Tools/ai/build_semantic_evidence_chunks.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_semantic_evidence_chunks.py`. Target `Tools/ai/build_semantic_evidence_chunks.py` and resolve `Tools/ai/build_semantic_evidence_chunks.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_085 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/validation/README.md:172` targeting `un_npu_review.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/validation/README.md:172`. Target `Tools/validation/README.md` and resolve `un_npu_review.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_086 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md:282` targeting `text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md:282`. Target `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md` and resolve `text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_087 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/check_local_resource_lanes.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/check_local_resource_lanes.py` targeting `Tools/ai/check_local_resource_lanes.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/check_local_resource_lanes.py`. Target `Tools/ai/check_local_resource_lanes.py` and resolve `Tools/ai/check_local_resource_lanes.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_088 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md:127` targeting `Tools/validation/example.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md:127`. Target `docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md` and resolve `Tools/validation/example.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_089 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md:231` targeting `text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md:231`. Target `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md` and resolve `text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_090 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/check_npu_provider_environment.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/check_npu_provider_environment.py` targeting `Tools/ai/check_npu_provider_environment.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/check_npu_provider_environment.py`. Target `Tools/ai/check_npu_provider_environment.py` and resolve `Tools/ai/check_npu_provider_environment.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_091 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/CODE_CONSULTATION_REPORT/part-001.md:271` targeting `text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_paths.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/CODE_CONSULTATION_REPORT/part-001.md:271`. Target `docs/CODE_CONSULTATION_REPORT/part-001.md` and resolve `text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_paths.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_092 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `README.md:137` targeting `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/DISCOVERY_CONTRACT.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `README.md:137`. Target `README.md` and resolve `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/DISCOVERY_CONTRACT.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_093 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/enrich_github_evidence_bundle_code_plan.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/enrich_github_evidence_bundle_code_plan.py` targeting `Tools/ai/enrich_github_evidence_bundle_code_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/enrich_github_evidence_bundle_code_plan.py`. Target `Tools/ai/enrich_github_evidence_bundle_code_plan.py` and resolve `Tools/ai/enrich_github_evidence_bundle_code_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_094 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/CODE_CONSULTATION_REPORT/part-001.md:274` targeting `Tools/validation/check_docs_paths.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/CODE_CONSULTATION_REPORT/part-001.md:274`. Target `docs/CODE_CONSULTATION_REPORT/part-001.md` and resolve `Tools/validation/check_docs_paths.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_095 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Scripting/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Scripting/README.md:43` targeting `text
package_name/
  README.md
  main.py
  config.py
  pipeline.py
  audio_mapping.py
  scene_objects.py
  materials.py
  lighting.py
  camera.py
  animation.py
  render_settings.py
  encode.py
  diagnostics.py
  inputs/
    README.md
    input_schema.json
  outputs/
    README.md
  notes/
    known_issues.md
    tuning_notes.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Scripting/README.md:43`. Target `Scripting/README.md` and resolve `text
package_name/
  README.md
  main.py
  config.py
  pipeline.py
  audio_mapping.py
  scene_objects.py
  materials.py
  lighting.py
  camera.py
  animation.py
  render_settings.py
  encode.py
  diagnostics.py
  inputs/
    README.md
    input_schema.json
  outputs/
    README.md
  notes/
    known_issues.md
    tuning_notes.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_096 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/full0to10_memory_tool.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/full0to10_memory_tool.py` targeting `Tools/ai/full0to10_memory_tool.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/full0to10_memory_tool.py`. Target `Tools/ai/full0to10_memory_tool.py` and resolve `Tools/ai/full0to10_memory_tool.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_097 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/DEVELOPER_GUIDE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/DEVELOPER_GUIDE.md:176` targeting `text
analyze_wav.py
build_track_summary.py
normalize_scene_spec.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/DEVELOPER_GUIDE.md:176`. Target `docs/DEVELOPER_GUIDE.md` and resolve `text
analyze_wav.py
build_track_summary.py
normalize_scene_spec.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_098 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/git/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/git/README.md:11` targeting `Tools/npu/*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/git/README.md:11`. Target `Tools/git/README.md` and resolve `Tools/npu/*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_099 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/full0to10_runtime_tool.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/full0to10_runtime_tool.py` targeting `Tools/ai/full0to10_runtime_tool.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/full0to10_runtime_tool.py`. Target `Tools/ai/full0to10_runtime_tool.py` and resolve `Tools/ai/full0to10_runtime_tool.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_100 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:53` targeting `text
Tools/validation/check_generated_<target>_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:53`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `text
Tools/validation/check_generated_<target>_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_101 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/git/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/git/README.md:12` targeting `output/*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/git/README.md:12`. Target `Tools/git/README.md` and resolve `output/*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_102 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/promote_patch_spec_draft.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/promote_patch_spec_draft.py` targeting `Tools/ai/promote_patch_spec_draft.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/promote_patch_spec_draft.py`. Target `Tools/ai/promote_patch_spec_draft.py` and resolve `Tools/ai/promote_patch_spec_draft.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_103 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:54` targeting `_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:54`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_104 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/README.md:20` targeting `_technical_notes.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/README.md:20`. Target `Tools/npu/README.md` and resolve `_technical_notes.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_105 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/replay_gpu_planner_json_contract.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/replay_gpu_planner_json_contract.py` targeting `Tools/ai/replay_gpu_planner_json_contract.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/replay_gpu_planner_json_contract.py`. Target `Tools/ai/replay_gpu_planner_json_contract.py` and resolve `Tools/ai/replay_gpu_planner_json_contract.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_106 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:59` targeting `text
Tools/validation/check_generated_automation_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:59`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `text
Tools/validation/check_generated_automation_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_107 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/README.md:20` targeting `*_technical_notes.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/README.md:20`. Target `Tools/npu/README.md` and resolve `*_technical_notes.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_108 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/review_agent_memory.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/review_agent_memory.py` targeting `Tools/ai/review_agent_memory.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/review_agent_memory.py`. Target `Tools/ai/review_agent_memory.py` and resolve `Tools/ai/review_agent_memory.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_109 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:60` targeting `Tools/validation/check_generated_automation_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:60`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `Tools/validation/check_generated_automation_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_110 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/README.md:22` targeting `_context.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/README.md:22`. Target `Tools/npu/README.md` and resolve `_context.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_111 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` targeting `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`. Target `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` and resolve `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_112 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/carmine-like-patch-loop/01-procedure.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/carmine-like-patch-loop/01-procedure.md:7` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/carmine-like-patch-loop/01-procedure.md:7`. Target `docs/LOCAL_AI_TASKS/carmine-like-patch-loop/01-procedure.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_113 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/README.md:22` targeting `*_context.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/README.md:22`. Target `Tools/npu/README.md` and resolve `*_context.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_114 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/run_local_provider_probe.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/run_local_provider_probe.py` targeting `Tools/ai/run_local_provider_probe.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/run_local_provider_probe.py`. Target `Tools/ai/run_local_provider_probe.py` and resolve `Tools/ai/run_local_provider_probe.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_115 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md:70` targeting `powershell
Select-String -Path ./Tools/ai/*.py, ./Tools/validation/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md:70`. Target `docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md` and resolve `powershell
Select-String -Path ./Tools/ai/*.py, ./Tools/validation/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_116 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:6` targeting `npu_code_chunks/chunk_*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:6`. Target `Tools/npu/npu_code_context.md` and resolve `npu_code_chunks/chunk_*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_117 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/run_parallel_artifact_pipeline.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/run_parallel_artifact_pipeline.py` targeting `Tools/ai/run_parallel_artifact_pipeline.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/run_parallel_artifact_pipeline.py`. Target `Tools/ai/run_parallel_artifact_pipeline.py` and resolve `Tools/ai/run_parallel_artifact_pipeline.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_118 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:100` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:100`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_119 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:70` targeting `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:70`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_120 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/ai/run_pipeline_dry_run_matrix.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/run_pipeline_dry_run_matrix.py` targeting `Tools/ai/run_pipeline_dry_run_matrix.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/run_pipeline_dry_run_matrix.py`. Target `Tools/ai/run_pipeline_dry_run_matrix.py` and resolve `Tools/ai/run_pipeline_dry_run_matrix.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_121 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:318` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:318`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_122 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:71` targeting `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:71`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_123 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/docs/apply_md_code_coherence_refactor.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/docs/apply_md_code_coherence_refactor.py` targeting `Tools/docs/apply_md_code_coherence_refactor.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/docs/apply_md_code_coherence_refactor.py`. Target `Tools/docs/apply_md_code_coherence_refactor.py` and resolve `Tools/docs/apply_md_code_coherence_refactor.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_124 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:324` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:324`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_125 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:72` targeting `Tools/npu/npu_code_chunks/chunk_003_build_track_summary_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:72`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_003_build_track_summary_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_126 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/docs/build_code_aware_md_coherence.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/docs/build_code_aware_md_coherence.py` targeting `Tools/docs/build_code_aware_md_coherence.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/docs/build_code_aware_md_coherence.py`. Target `Tools/docs/build_code_aware_md_coherence.py` and resolve `Tools/docs/build_code_aware_md_coherence.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_127 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full0to10-quality-gate/10-operational-wrapper-guards.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full0to10-quality-gate/10-operational-wrapper-guards.md:14` targeting `text
run_full0to10_workflow_exit_code_guard_smoke.py
run_full0to10_markdown_shadow_guard_smoke.py
check_full0to10_generated_artifact_quarantine.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full0to10-quality-gate/10-operational-wrapper-guards.md:14`. Target `docs/LOCAL_AI_TASKS/full0to10-quality-gate/10-operational-wrapper-guards.md` and resolve `text
run_full0to10_workflow_exit_code_guard_smoke.py
run_full0to10_markdown_shadow_guard_smoke.py
check_full0to10_generated_artifact_quarantine.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_128 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:73` targeting `Tools/npu/npu_code_chunks/chunk_004_normalize_scene_spec_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:73`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_004_normalize_scene_spec_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_129 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/docs/split_large_markdown.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/docs/split_large_markdown.py` targeting `Tools/docs/split_large_markdown.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/docs/split_large_markdown.py`. Target `Tools/docs/split_large_markdown.py` and resolve `Tools/docs/split_large_markdown.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_130 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md:51` targeting `text
kind: gpu_repair_failure_recommendation
recommendation_count: 1
recommendations[0].id: gpu_repair_failure_001
recommendations[0].status: ready_for_manual_review
recommended_next_layer: build_agent_review_patch_plan.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md:51`. Target `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md` and resolve `text
kind: gpu_repair_failure_recommendation
recommendation_count: 1
recommendations[0].id: gpu_repair_failure_001
recommendations[0].status: ready_for_manual_review
recommended_next_layer: build_agent_review_patch_plan.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_131 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:74` targeting `Tools/npu/npu_code_chunks/chunk_005_normalize_scene_spec_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:74`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_005_normalize_scene_spec_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_132 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/build_npu_code_context.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/npu/build_npu_code_context.py` targeting `Tools/npu/build_npu_code_context.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/npu/build_npu_code_context.py`. Target `Tools/npu/build_npu_code_context.py` and resolve `Tools/npu/build_npu_code_context.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_133 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:174` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:174`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_134 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:75` targeting `Tools/npu/npu_code_chunks/chunk_006_Tools_npu_npu_runtime_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:75`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_006_Tools_npu_npu_runtime_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_135 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/build_npu_knowledge_broker_packet.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/npu/build_npu_knowledge_broker_packet.py` targeting `Tools/npu/build_npu_knowledge_broker_packet.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/npu/build_npu_knowledge_broker_packet.py`. Target `Tools/npu/build_npu_knowledge_broker_packet.py` and resolve `Tools/npu/build_npu_knowledge_broker_packet.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_136 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:26` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:26`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_137 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:76` targeting `Tools/npu/npu_code_chunks/chunk_007_Tools_npu_ollama_runtime_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:76`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_007_Tools_npu_ollama_runtime_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_138 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/build_project_ai_index.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/npu/build_project_ai_index.py` targeting `Tools/npu/build_project_ai_index.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/npu/build_project_ai_index.py`. Target `Tools/npu/build_project_ai_index.py` and resolve `Tools/npu/build_project_ai_index.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_139 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:100` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:100`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_140 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:77` targeting `Tools/npu/npu_code_chunks/chunk_008_Tools_npu_ollama_runtime_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:77`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_008_Tools_npu_ollama_runtime_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_141 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/build_provider_result_report.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/npu/build_provider_result_report.py` targeting `Tools/npu/build_provider_result_report.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/npu/build_provider_result_report.py`. Target `Tools/npu/build_provider_result_report.py` and resolve `Tools/npu/build_provider_result_report.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_142 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/02-zip-01-tools.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/02-zip-01-tools.md:8` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/02-zip-01-tools.md:8`. Target `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/02-zip-01-tools.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_143 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:78` targeting `Tools/npu/npu_code_chunks/chunk_009_Tools_npu_build_blender_manual_context_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:78`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_009_Tools_npu_build_blender_manual_context_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_144 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/build_semantic_code_chunks.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/npu/build_semantic_code_chunks.py` targeting `Tools/npu/build_semantic_code_chunks.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/npu/build_semantic_code_chunks.py`. Target `Tools/npu/build_semantic_code_chunks.py` and resolve `Tools/npu/build_semantic_code_chunks.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_145 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md:12` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md:12`. Target `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_146 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:79` targeting `Tools/npu/npu_code_chunks/chunk_010_Tools_npu_build_blender_manual_context_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:79`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_010_Tools_npu_build_blender_manual_context_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_147 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/repo_patch_runner/apply_repo_mods.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/repo_patch_runner/apply_repo_mods.py` targeting `Tools/repo_patch_runner/apply_repo_mods.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/repo_patch_runner/apply_repo_mods.py`. Target `Tools/repo_patch_runner/apply_repo_mods.py` and resolve `Tools/repo_patch_runner/apply_repo_mods.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_148 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md:18` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md:18`. Target `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_149 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:80` targeting `Tools/npu/npu_code_chunks/chunk_011_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:80`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_011_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_150 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/build_markdown_inventory.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/validation/build_markdown_inventory.py` targeting `Tools/validation/build_markdown_inventory.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/validation/build_markdown_inventory.py`. Target `Tools/validation/build_markdown_inventory.py` and resolve `Tools/validation/build_markdown_inventory.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_151 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md:10` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md:10`. Target `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_152 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:81` targeting `Tools/npu/npu_code_chunks/chunk_012_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:81`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_012_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_153 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/build_python_line_count_csv.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/validation/build_python_line_count_csv.py` targeting `Tools/validation/build_python_line_count_csv.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/validation/build_python_line_count_csv.py`. Target `Tools/validation/build_python_line_count_csv.py` and resolve `Tools/validation/build_python_line_count_csv.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_154 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md:12` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md:12`. Target `docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_155 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:82` targeting `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:82`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_156 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/build_script_inventory.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/validation/build_script_inventory.py` targeting `Tools/validation/build_script_inventory.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/validation/build_script_inventory.py`. Target `Tools/validation/build_script_inventory.py` and resolve `Tools/validation/build_script_inventory.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_157 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:78` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:78`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_158 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:83` targeting `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:83`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_159 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/run_agent_review_patch_plan_full_validation.py']
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/validation/run_agent_review_patch_plan_full_validation.py` targeting `Tools/validation/run_agent_review_patch_plan_full_validation.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/validation/run_agent_review_patch_plan_full_validation.py`. Target `Tools/validation/run_agent_review_patch_plan_full_validation.py` and resolve `Tools/validation/run_agent_review_patch_plan_full_validation.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

#### consistency_160 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap/part-001.md:95` targeting `text
empty_recommendations_reason: context_echo_detected
schema_status: wrong_json_shape
recommended_next_layer: compact_prompt_retry or build_agent_review_patch_plan.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap/part-001.md:95`. Target `docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap/part-001.md` and resolve `text
empty_recommendations_reason: context_echo_detected
schema_status: wrong_json_shape
recommended_next_layer: compact_prompt_retry or build_agent_review_patch_plan.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_161 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:84` targeting `Tools/npu/npu_code_chunks/chunk_015_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:84`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_015_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_162 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:155` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:155`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_163 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:85` targeting `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:85`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_164 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:25` targeting `_smoke.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:25`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `_smoke.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_165 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:86` targeting `Tools/npu/npu_code_chunks/chunk_017_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:86`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_017_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_166 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:271` targeting `_smoke.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:271`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `_smoke.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_167 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:87` targeting `Tools/npu/npu_code_chunks/chunk_018_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:87`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_018_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_168 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md:43` targeting `text
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/README.md
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/validation/**
Tools/workflow/**
Tools/npu/**
Scripting/v61b/**
analyze_wav.py
build_track_summary.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md:43`. Target `docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md` and resolve `text
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/README.md
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/validation/**
Tools/workflow/**
Tools/npu/**
Scripting/v61b/**
analyze_wav.py
build_track_summary.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_169 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:88` targeting `Tools/npu/npu_code_chunks/chunk_019_Tools_npu_run_dual_ai_pipeline_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:88`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_019_Tools_npu_run_dual_ai_pipeline_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_170 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md:56` targeting `text
Tools/workflow/*.ps1
Tools/ai/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md:56`. Target `docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md` and resolve `text
Tools/workflow/*.ps1
Tools/ai/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_171 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:89` targeting `Tools/npu/npu_code_chunks/chunk_020_Scripting_v61b_config_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:89`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_020_Scripting_v61b_config_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_172 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md:245` targeting `_smoke.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md:245`. Target `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` and resolve `_smoke.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_173 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:90` targeting `Tools/npu/npu_code_chunks/chunk_021_Scripting_v61b_config_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:90`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_021_Scripting_v61b_config_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_174 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:257` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:257`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_175 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:91` targeting `Tools/npu/npu_code_chunks/chunk_022_Scripting_v61b_main_v61b_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:91`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_022_Scripting_v61b_main_v61b_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_176 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/MODULE_MAP.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/MODULE_MAP.md:89` targeting `Tools/lib/scene_spec.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/MODULE_MAP.md:89`. Target `docs/MODULE_MAP.md` and resolve `Tools/lib/scene_spec.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_177 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:92` targeting `Tools/npu/npu_code_chunks/chunk_023_Scripting_v61b_animation_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:92`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_023_Scripting_v61b_animation_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_178 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/MODULE_MAP.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/MODULE_MAP.md:102` targeting `Scripting/shared/panel_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/MODULE_MAP.md:102`. Target `docs/MODULE_MAP.md` and resolve `Scripting/shared/panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_179 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:93` targeting `Tools/npu/npu_code_chunks/chunk_024_Scripting_v61b_animation_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:93`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_024_Scripting_v61b_animation_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_180 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/MODULE_MAP.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/MODULE_MAP.md:104` targeting `hotpatch_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/MODULE_MAP.md:104`. Target `docs/MODULE_MAP.md` and resolve `hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_181 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:94` targeting `Tools/npu/npu_code_chunks/chunk_025_Scripting_v61b_animation_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:94`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_025_Scripting_v61b_animation_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_182 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/MODULE_MAP.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/MODULE_MAP.md:265` targeting `pipeline.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/MODULE_MAP.md:265`. Target `docs/MODULE_MAP.md` and resolve `pipeline.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_183 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:95` targeting `Tools/npu/npu_code_chunks/chunk_026_Scripting_v61b_animation_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:95`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_026_Scripting_v61b_animation_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_184 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/MODULE_MAP.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/MODULE_MAP.md:273` targeting `encode.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/MODULE_MAP.md:273`. Target `docs/MODULE_MAP.md` and resolve `encode.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_185 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:96` targeting `Tools/npu/npu_code_chunks/chunk_027_Scripting_v61b_animation_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:96`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_027_Scripting_v61b_animation_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_186 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY/part-002.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY/part-002.md:78` targeting `text
check_docs_links.py
check_refactor_status_consistency.py
check_ai_pipeline_modules.py
check_npu_pipeline_modules.py
check_npu_pipeline_helper_tests.py
check_npu_pipeline_docs.py
build_runtime_tool_usage_telemetry.py
build_runtime_tool_capability_manifest.py
build_full_toolbox_run_telemetry_summary.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY/part-002.md:78`. Target `docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY/part-002.md` and resolve `text
check_docs_links.py
check_refactor_status_consistency.py
check_ai_pipeline_modules.py
check_npu_pipeline_modules.py
check_npu_pipeline_helper_tests.py
check_npu_pipeline_docs.py
build_runtime_tool_usage_telemetry.py
build_runtime_tool_capability_manifest.py
build_full_toolbox_run_telemetry_summary.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_187 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:97` targeting `Tools/npu/npu_code_chunks/chunk_028_Scripting_v61b_animation_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:97`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_028_Scripting_v61b_animation_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_188 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/PACKAGE_CREATION_WORKFLOW.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/PACKAGE_CREATION_WORKFLOW.md:106` targeting `text
main.py
config.py
audio_mapping.py
scene_objects.py
materials.py
camera.py
lighting.py
render_settings.py
encode_ffmpeg.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/PACKAGE_CREATION_WORKFLOW.md:106`. Target `docs/PACKAGE_CREATION_WORKFLOW.md` and resolve `text
main.py
config.py
audio_mapping.py
scene_objects.py
materials.py
camera.py
lighting.py
render_settings.py
encode_ffmpeg.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_189 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:98` targeting `Tools/npu/npu_code_chunks/chunk_029_Scripting_v61b_materials_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:98`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_029_Scripting_v61b_materials_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_190 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/PROJECT_AI_CONSCIOUSNESS/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/PROJECT_AI_CONSCIOUSNESS/part-001.md:355` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/PROJECT_AI_CONSCIOUSNESS/part-001.md:355`. Target `docs/PROJECT_AI_CONSCIOUSNESS/part-001.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_191 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:99` targeting `Tools/npu/npu_code_chunks/chunk_030_Scripting_v61b_materials_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:99`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_030_Scripting_v61b_materials_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_192 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/REFACTORING_AND_REUSE_PLAN.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/REFACTORING_AND_REUSE_PLAN.md:192` targeting `text
Tools/npu/pipeline/
  config.py
  artifact_paths.py
  io_utils.py
  legacy_compat.py
  fixtures.py
  prompts.py
  context_builder.py
  providers.py
  runner.py
  validators.py
  artifact_writer.py
  migration_readiness.py
  reports.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/REFACTORING_AND_REUSE_PLAN.md:192`. Target `docs/REFACTORING_AND_REUSE_PLAN.md` and resolve `text
Tools/npu/pipeline/
  config.py
  artifact_paths.py
  io_utils.py
  legacy_compat.py
  fixtures.py
  prompts.py
  context_builder.py
  providers.py
  runner.py
  validators.py
  artifact_writer.py
  migration_readiness.py
  reports.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_193 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:100` targeting `Tools/npu/npu_code_chunks/chunk_031_Scripting_v61b_materials_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:100`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_031_Scripting_v61b_materials_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_194 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/REFACTORING_AND_REUSE_PLAN.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/REFACTORING_AND_REUSE_PLAN.md:282` targeting `src/spaziotempo_audio/scene_spec.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/REFACTORING_AND_REUSE_PLAN.md:282`. Target `docs/REFACTORING_AND_REUSE_PLAN.md` and resolve `src/spaziotempo_audio/scene_spec.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_195 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:101` targeting `Tools/npu/npu_code_chunks/chunk_032_Scripting_v61b_physics_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:101`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_032_Scripting_v61b_physics_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_196 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/REFACTORING_AND_REUSE_PLAN.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/REFACTORING_AND_REUSE_PLAN.md:282` targeting `Tools/lib/scene_spec.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/REFACTORING_AND_REUSE_PLAN.md:282`. Target `docs/REFACTORING_AND_REUSE_PLAN.md` and resolve `Tools/lib/scene_spec.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_197 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:102` targeting `Tools/npu/npu_code_chunks/chunk_033_Scripting_v61b_physics_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:102`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_033_Scripting_v61b_physics_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_198 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/SHARED_SCRIPTING_UTILITIES.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/SHARED_SCRIPTING_UTILITIES.md:39` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/SHARED_SCRIPTING_UTILITIES.md:39`. Target `docs/SHARED_SCRIPTING_UTILITIES.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_199 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:103` targeting `Tools/npu/npu_code_chunks/chunk_034_Scripting_v61b_physics_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:103`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_034_Scripting_v61b_physics_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_200 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/SHARED_SCRIPTING_UTILITIES.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/SHARED_SCRIPTING_UTILITIES.md:41` targeting `Scripting/shared/hotpatch_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/SHARED_SCRIPTING_UTILITIES.md:41`. Target `docs/SHARED_SCRIPTING_UTILITIES.md` and resolve `Scripting/shared/hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_201 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:104` targeting `Tools/npu/npu_code_chunks/chunk_035_Scripting_v61b_fog_dynamics_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:104`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_035_Scripting_v61b_fog_dynamics_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_202 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/SHARED_SCRIPTING_UTILITIES.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/SHARED_SCRIPTING_UTILITIES.md:42` targeting `Scripting/shared/panel_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/SHARED_SCRIPTING_UTILITIES.md:42`. Target `docs/SHARED_SCRIPTING_UTILITIES.md` and resolve `Scripting/shared/panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_203 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:105` targeting `Tools/npu/npu_code_chunks/chunk_036_Scripting_v61b_fog_dynamics_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:105`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_036_Scripting_v61b_fog_dynamics_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_204 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/SHARED_SCRIPTING_UTILITIES.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/SHARED_SCRIPTING_UTILITIES.md:43` targeting `Scripting/shared/scene_registry.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/SHARED_SCRIPTING_UTILITIES.md:43`. Target `docs/SHARED_SCRIPTING_UTILITIES.md` and resolve `Scripting/shared/scene_registry.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_205 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:106` targeting `Tools/npu/npu_code_chunks/chunk_037_Scripting_v61b_fog_filaments_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:106`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_037_Scripting_v61b_fog_filaments_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_206 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/SHARED_SCRIPTING_UTILITIES.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/SHARED_SCRIPTING_UTILITIES.md:143` targeting `panel_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/SHARED_SCRIPTING_UTILITIES.md:143`. Target `docs/SHARED_SCRIPTING_UTILITIES.md` and resolve `panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_207 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:107` targeting `Tools/npu/npu_code_chunks/chunk_038_Scripting_v61b_atmosphere_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:107`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_038_Scripting_v61b_atmosphere_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_208 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/SHARED_SCRIPTING_UTILITIES.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/SHARED_SCRIPTING_UTILITIES.md:144` targeting `hotpatch_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/SHARED_SCRIPTING_UTILITIES.md:144`. Target `docs/SHARED_SCRIPTING_UTILITIES.md` and resolve `hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_209 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:108` targeting `Tools/npu/npu_code_chunks/chunk_039_Scripting_v61b_atmosphere_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:108`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_039_Scripting_v61b_atmosphere_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_210 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['guida_git_github_blender_audio_project.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `guida_git_github_blender_audio_project.md:91` targeting `gitignore
.aider*
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.tmp
.DS_Store

output/
renders/

Scripting/v61b_backgood/
old script legacy/

# NPU generated cache/chunks
Tools/npu/.npucache/
Tools/npu/__pycache__/
Tools/npu/npu_blender_manual_chunks/
Tools/npu/npu_code_chunks/
Tools/npu/npu_music_chunks/

# AI generated indexes/chunks
indexAI/project_code_chunks/
indexAI/project_code_index.md
indexAI/project_code_manifest.json

# Generated scene bundles / AI packets
indexAI/scene_scripts/*_scene_bundle/
indexAI/patch_library/*_gpu_task_packet.json
indexAI/patch_library/*_npu_service_capsule.json
indexAI/patch_library/*_npu_service_capsule.md

# Backups / archives
*.bak
*.bak2
*.zip
*_backup_*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `guida_git_github_blender_audio_project.md:91`. Target `guida_git_github_blender_audio_project.md` and resolve `gitignore
.aider*
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.tmp
.DS_Store

output/
renders/

Scripting/v61b_backgood/
old script legacy/

# NPU generated cache/chunks
Tools/npu/.npucache/
Tools/npu/__pycache__/
Tools/npu/npu_blender_manual_chunks/
Tools/npu/npu_code_chunks/
Tools/npu/npu_music_chunks/

# AI generated indexes/chunks
indexAI/project_code_chunks/
indexAI/project_code_index.md
indexAI/project_code_manifest.json

# Generated scene bundles / AI packets
indexAI/scene_scripts/*_scene_bundle/
indexAI/patch_library/*_gpu_task_packet.json
indexAI/patch_library/*_npu_service_capsule.json
indexAI/patch_library/*_npu_service_capsule.md

# Backups / archives
*.bak
*.bak2
*.zip
*_backup_*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_211 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:109` targeting `Tools/npu/npu_code_chunks/chunk_040_Scripting_v61b_world_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:109`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_040_Scripting_v61b_world_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_212 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['guida_git_github_blender_audio_project.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `guida_git_github_blender_audio_project.md:212` targeting `powershell
git restore --staged Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `guida_git_github_blender_audio_project.md:212`. Target `guida_git_github_blender_audio_project.md` and resolve `powershell
git restore --staged Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_213 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:110` targeting `Tools/npu/npu_code_chunks/chunk_041_Scripting_v61b_render_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:110`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_041_Scripting_v61b_render_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_214 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['guida_git_github_blender_audio_project.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `guida_git_github_blender_audio_project.md:213` targeting `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `guida_git_github_blender_audio_project.md:213`. Target `guida_git_github_blender_audio_project.md` and resolve `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_215 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:111` targeting `Tools/npu/npu_code_chunks/chunk_042_Scripting_v61b_scene_tuning_panel_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:111`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_042_Scripting_v61b_scene_tuning_panel_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_216 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['guida_git_github_blender_audio_project.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `guida_git_github_blender_audio_project.md:486` targeting `powershell
git restore --staged Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `guida_git_github_blender_audio_project.md:486`. Target `guida_git_github_blender_audio_project.md` and resolve `powershell
git restore --staged Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_217 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:112` targeting `Tools/npu/npu_code_chunks/chunk_043_Scripting_v61b_scene_tuning_panel_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:112`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_043_Scripting_v61b_scene_tuning_panel_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_218 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['guida_git_github_blender_audio_project.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `guida_git_github_blender_audio_project.md:487` targeting `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `guida_git_github_blender_audio_project.md:487`. Target `guida_git_github_blender_audio_project.md` and resolve `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/_backup_previous_elastic_touch_fix.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_219 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:113` targeting `Tools/npu/npu_code_chunks/chunk_044_Scripting_v61b_scene_tuning_panel_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:113`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_044_Scripting_v61b_scene_tuning_panel_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_220 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['indexAI/scene_scripts/new_plan_luca_vera_master_scene_bundle/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `indexAI/scene_scripts/new_plan_luca_vera_master_scene_bundle/README.md:5` targeting `new_plan_luca_vera_master_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `indexAI/scene_scripts/new_plan_luca_vera_master_scene_bundle/README.md:5`. Target `indexAI/scene_scripts/new_plan_luca_vera_master_scene_bundle/README.md` and resolve `new_plan_luca_vera_master_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_221 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:114` targeting `Tools/npu/npu_code_chunks/chunk_045_Scripting_v61b_scene_tuning_panel_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:114`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_045_Scripting_v61b_scene_tuning_panel_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_222 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['indexAI/scene_scripts/parameters_luca_vera_premaster_master_scene_bundle/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `indexAI/scene_scripts/parameters_luca_vera_premaster_master_scene_bundle/README.md:5` targeting `parameters_luca_vera_premaster_master_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `indexAI/scene_scripts/parameters_luca_vera_premaster_master_scene_bundle/README.md:5`. Target `indexAI/scene_scripts/parameters_luca_vera_premaster_master_scene_bundle/README.md` and resolve `parameters_luca_vera_premaster_master_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_223 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:115` targeting `Tools/npu/npu_code_chunks/chunk_046_Scripting_v61b_scene_tuning_panel_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:115`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_046_Scripting_v61b_scene_tuning_panel_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_224 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['indexAI/scene_scripts/phazzah_luca_vera_master_scene_bundle/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `indexAI/scene_scripts/phazzah_luca_vera_master_scene_bundle/README.md:5` targeting `phazzah_luca_vera_master_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `indexAI/scene_scripts/phazzah_luca_vera_master_scene_bundle/README.md:5`. Target `indexAI/scene_scripts/phazzah_luca_vera_master_scene_bundle/README.md` and resolve `phazzah_luca_vera_master_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_225 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:116` targeting `Tools/npu/npu_code_chunks/chunk_047_Scripting_v61b_scene_tuning_panel_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:116`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_047_Scripting_v61b_scene_tuning_panel_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_226 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['indexAI/scene_scripts/ready_to_jazz_luca_vera_master_scene_bundle/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `indexAI/scene_scripts/ready_to_jazz_luca_vera_master_scene_bundle/README.md:5` targeting `ready_to_jazz_luca_vera_master_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `indexAI/scene_scripts/ready_to_jazz_luca_vera_master_scene_bundle/README.md:5`. Target `indexAI/scene_scripts/ready_to_jazz_luca_vera_master_scene_bundle/README.md` and resolve `ready_to_jazz_luca_vera_master_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_227 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:117` targeting `Tools/npu/npu_code_chunks/chunk_048_Scripting_v61b_hot_update_scene_v61b_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:117`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_048_Scripting_v61b_hot_update_scene_v61b_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_228 — doc_python
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported medium `md_cli_arg_not_in_argparse` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:260` targeting `--bundle`.
- Strategy: Build a focused patch plan for `md_cli_arg_not_in_argparse` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:260`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `--bundle` without formatting-only edits. Mapper recommendation: Correct the documented CLI flag or update the script argparse contract in a focused PR.

#### consistency_229 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:118` targeting `Tools/npu/npu_code_chunks/chunk_049_Scripting_v61b_encode_image_sequence_v61b_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:118`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_049_Scripting_v61b_encode_image_sequence_v61b_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_230 — doc_python
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported medium `md_cli_arg_not_in_argparse` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:260` targeting `--output`.
- Strategy: Build a focused patch plan for `md_cli_arg_not_in_argparse` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:260`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `--output` without formatting-only edits. Mapper recommendation: Correct the documented CLI flag or update the script argparse contract in a focused PR.

#### consistency_231 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:119` targeting `Tools/npu/npu_code_chunks/chunk_050_Scripting_v61b_encode_image_sequence_v61b_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:119`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_050_Scripting_v61b_encode_image_sequence_v61b_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_232 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:120` targeting `Tools/npu/npu_code_chunks/chunk_051_Scripting_v61b_encode_ffmpeg_v61b_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:120`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_051_Scripting_v61b_encode_ffmpeg_v61b_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_233 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:121` targeting `Tools/npu/npu_code_chunks/chunk_052_Scripting_v61b_encode_ffmpeg_v61b_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:121`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_052_Scripting_v61b_encode_ffmpeg_v61b_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_234 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:122` targeting `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:122`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_235 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:123` targeting `Tools/npu/npu_code_chunks/chunk_054_Scripting_v61b_SCENE_TUNING_GUIDE_md.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:123`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_054_Scripting_v61b_SCENE_TUNING_GUIDE_md.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_236 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:124` targeting `Tools/npu/npu_code_chunks/chunk_055_Scripting_v61b_SCENE_TUNING_GUIDE_md.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:124`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_055_Scripting_v61b_SCENE_TUNING_GUIDE_md.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_237 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:125` targeting `Tools/npu/npu_code_chunks/chunk_056_Scripting_v61b_init_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:125`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_056_Scripting_v61b_init_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_238 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:126` targeting `Tools/npu/npu_code_chunks/chunk_057_Scripting_v61b_asset_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:126`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_057_Scripting_v61b_asset_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_239 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:127` targeting `Tools/npu/npu_code_chunks/chunk_058_Scripting_v61b_asset_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:127`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_058_Scripting_v61b_asset_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_240 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:128` targeting `Tools/npu/npu_code_chunks/chunk_059_Scripting_v61b_asset_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:128`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_059_Scripting_v61b_asset_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_241 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:129` targeting `Tools/npu/npu_code_chunks/chunk_060_Scripting_v61b_camera_setup_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:129`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_060_Scripting_v61b_camera_setup_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_242 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:130` targeting `Tools/npu/npu_code_chunks/chunk_061_Scripting_v61b_io_utils_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:130`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_061_Scripting_v61b_io_utils_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_243 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:131` targeting `Tools/npu/npu_code_chunks/chunk_062_Scripting_v61b_reload_utils_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:131`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_062_Scripting_v61b_reload_utils_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_244 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_context.md']
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `Tools/npu/npu_code_context.md:132` targeting `Tools/npu/npu_code_chunks/chunk_063_Scripting_v61b_scene_utils_py.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `Tools/npu/npu_code_context.md:132`. Target `Tools/npu/npu_code_context.md` and resolve `Tools/npu/npu_code_chunks/chunk_063_Scripting_v61b_scene_utils_py.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_orchestrator.json` exists=`True` size=`180957` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.json` exists=`True` size=`28401` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`12538946` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1235` suffix=`.json` preview_chars=`1196`
- `output/analysis/code_interpreter_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`2169900` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`3163` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`79725` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/openvino_hardware_governance_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`2370` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`5694` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`5297` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_evidence_contract_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`6912` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_task_lane_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`8601` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_contract_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`506` suffix=`.json` preview_chars=`494`
- `output/ai_pipeline/gpu0_peer_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_gpu0_peer_support.json` exists=`True` size=`1732` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/npu_micro_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_npu_micro_support.json` exists=`True` size=`12550` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu1_primary_advisory_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1491` suffix=`.json` preview_chars=`1449`
- `output/validation/gpu0_peer_task_packet_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`6242` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_response_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`5026` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_tool_requests_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`3514` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`30311` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_micro_peer_assistant_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1587` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1066` suffix=`.json` preview_chars=`1035`
- `output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`62225` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_peer_exchange_contract_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`13433` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_init_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1589` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_gpu1_request_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1986` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_broker_results_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`4862` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_npu_support_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1951` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_tool_catalog_complete_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`3158` suffix=`.json` preview_chars=`1500`
- `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/snapshot.json` exists=`True` size=`7200` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`2576` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_post_patchable_doc_python_probe_20260507-180555_workflow.json` exists=`True` size=`5817` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_from_peer_reports_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`1689` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`141071` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`5417659` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555.json` exists=`True` size=`381087` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product_manifest.json` exists=`True` size=`381087` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product_evidence_index.json` exists=`True` size=`202573` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product_readiness.json` exists=`True` size=`444` suffix=`.json` preview_chars=`430`
- `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json` exists=`True` size=`4434640` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_bridge_orchestrator.json` exists=`True` size=`1257` suffix=`.json` preview_chars=`1224`
- `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_decision_loop.json` exists=`True` size=`3094` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.json` exists=`True` size=`5435491` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/repository_consistency_map_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `57400`
- SHA-256: `cc3fbdac0413ca3fc6d607f9eb1aca71b34d2326b3da14ac428e883ca9f73a2f`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `16703`
- Repository files: `1747`
- File metadata records: `1747`
- Counted text-like files: `1721`
- Total counted text lines: `2055298`
- Markdown files: `679`
- Python files: `661`
- Markdown references: `109153`
- Markdown Python commands: `793`
- Provider execution performed: `False`
- Workers requested: `12`
- Adaptive worker mode: `False`
- Single file manifest: `True`
- File metadata enabled: `True`
- Total build seconds: `32.449`
- Markdown scan seconds: `21.912`
- Python inventory seconds: `0.756`
- Patch application performed: `False`

## Severity counts

- `high`: `5164`
- `low`: `48`
- `medium`: `11491`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `48`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `11489`
- `md_mentions_missing_powershell_path`: `511`
- `md_mentions_missing_python_path`: `4607`
- `md_python_command_script_missing`: `31`
- `python_import_symbol_missing`: `15`

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT.md` | 60 | `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 139 | `Tools/ai/simulate_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 157 | `Tools/ai/run_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 230 | `check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 52 | `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md` | Correct the documentation reference or restore the missing target if it is still required. |
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
17. CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md
18. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
19. CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
20. AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 29 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 216 | `text
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 68 | `output/ai_packets/20260504-224354/npu_real_workload_report.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 133 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 189 | `shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 67 | `text
output/ai_packets/20260504-224354/npu_real_workload_report.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md` | 246 | `text
docs/TECH_DEBT_TRACKER.md
TD-025 Python string patch hygiene
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md` | 282 | `text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md` | 231 | `text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `README.md` | 137 | `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/DISCOVERY_CONTRACT.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/README.md` | 48 | `pipeline.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/README.md` | 56 | `encode.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Scripting/README.md` | 43 | `text
package_name/
  README.md
  main.py
  config.py
  pipeline.py
  audio_mapping.py
  scene_objects.py
  materials.py
  lighting.py
  camera.py
  animation.py
  render_settings.py
  encode.py
  diagnostics.py
  inputs/
    README.md
    input_schema.json
  outputs/
    README.md
  notes/
    known_issues.md
    tuning_notes.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md` | 11 | `text
main_ready_to_jazz_wow_youtube.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 112 | `config_model.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 113 | `panel_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 114 | `scene_update.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 116 | `hotpatch_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 117 | `scene_registry.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 109 | `text
Scripting/shared/
  README.md
  config_model.py
  panel_base.py
  scene_update.py
  diagnostics.py
  hotpatch_base.py
  scene_registry.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/PROJECT_STRUCTURE.md` | 34 | `spaziotempo/features/water.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/README.md` | 90 | `Scripting/shared/panel_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/README.md` | 91 | `Scripting/shared/hotpatch_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/README.md` | 25 | `text
main_v61b.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/git/README.md` | 11 | `Tools/npu/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/git/README.md` | 12 | `output/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/README.md` | 20 | `_technical_notes.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/README.md` | 22 | `_context.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Tools/npu/README.md` | 18 | `build_*context*.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Tools/npu/README.md` | 19 | `run_*pipeline*.py` | Correct the documentation reference or restore the missing target if it
```

### `output/validation/repository_consistency_map_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `383`
- SHA-256: `a448d07f00493a20d455699856d1393eafd34b4a65d3ef8168636f2c8eba5c57`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Consistency Map Smoke

- Passed: `True`
- Return code: `0`
- Mapper report reused: `True`
- Workers requested: `12`
- Elapsed seconds: `0.058`
- Finding count: `16703`
- Markdown reference count: `109153`
- Markdown Python command count: `793`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`

```

### `output/validation/python_line_count_all_python_files_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `39696`
- SHA-256: `0760ccd459dcd4cbbbb5fe93dc9d7c0bf3ec94718e98613bf31e647d6270e5fe`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: post_patchable_doc_python_probe_20260507-180555
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-180624.csv
- File count: 661
- Total Python lines: 121515
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
| 1015 | `Tools/ai/build_deterministic_recommendations.py` |
| 969 | `old script legacy/spaziotempo_album_visual_v5.py` |
| 902 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
| 836 | `Tools/ai/build_runtime_tool_usage_telemetry.py` |
| 751 | `Tools/ai/agent_runtime_tool_broker.py` |
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
| 613 | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` |
| 608 | `Tools/ai/build_agent_review_patch_bundle.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 587 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 579 | `Tools/ai/build_ai_context_pack.py` |
| 573 | `Tools/ai/run_pipeline_dry_run_matrix.py` |
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
| 465 | `Tools/ai/patch_notes_quality_product/scoring.py` |
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
| 399 | `Tools/validation/run_patch_notes_quality_product_smoke.py` |
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
| 348 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py` |
| 345 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py` |
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/build_markdown_inventory.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 331 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 328 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py` |
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
| 306 | `Tools/ai/provider_runtime_heap_live_signals.py` |
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
| 225 | `Tools/ai/repository_consistency_map/python_inventory.py` |
| 223 | `Tools/ai/build_provider_runtime_heap_telemetry.py` |
| 221 | `Scripting/v61b/spaziotempo/core/registry.py` |
| 221 | `Tools/docs/apply_md_code_coherence_refactor.py` |
| 221 | `Tools/validation/check_file_line_limits.py` |
| 219 | `Tools/workflow/smart_ai_context.py` |
| 217 | `Tools/ai/artifact_domain_registry.py` |
| 212 | `Tools/validation/build_python_line_count_csv.py` |
| 210 | `Tools/ai/patch_notes_quality_product/telemetry_quality.py` |
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
| 198 | `Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 191 | `Tools/ai/code_interpreter_report/scanner.py` |
| 190 | `Tools/validation/full_run_bundle_completeness.py` |
| 190 | `Tools/validation/report_utils.py` |
| 190 | `Tools/validation/run_runtime_tool_guidance_fallback_smoke.py` |
| 189 | `Tools/ai/check_npu_provider_environment.py` |
| 188 | `Tools/ai/patch_notes_quality_product/builder.py` |
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
| 163 | `Tools/ai/full0to10_provider_telemetry_semantic/validator.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 161 | `Tools/ai/repository_consistency_map/builder.py` |
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
| 146 | `Tools/ai/repository_consistency_map/markdown.py` |
| 144 | `Tools/ai/code_interpreter_report/builder.py` |
| 144 | `Tools/workflow/artifact_consult.py` |
| 143 | `Tools/validation/run_npu_runtime_tool_fallback_smoke.py` |
| 142 | `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` |
| 142 | `Tools/ai/runtime_hardware_capability/workloads.py` |
| 141 | `Tools/ai/full0to10_sqlite_memory/embedding.py` |
| 141 | `Tools/validation/check_markdown_line_limits.py` |
| 141 | `Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py` |
| 140 | `Scripting/shared/blender_compat.py` |
| 139 | `Tools/ai/runtime_hardware_capability/manifest.py` |
| 136 | `Tools/ai/full0to10_final_product/builder.py` |
| 134 | `Scripting/shared/ffmpeg_encoder.py` |
| 133 | `Scripting/shared/render_profiles.py` |
| 133 | `Scripting/v61b/hotpatch/fog_patch.py` |
| 132 | `Scripting/v61b/spaziotempo/core/collections.py` |
| 132 | `Tools/validation/check_json_artifacts.py` |
| 132 | `Tools/workflow/run_agent_review_full_toolbox_decision_loop.py` |
| 130 | `Tool
```

### `output/validation/openvino_hardware_governance_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1413`
- SHA-256: `0eaf614429ff54a3351966777a348694480fe9357a3b41836b507fec719c9f2b`
- Content included: `True`
- Content truncated: `False`

```text
# OpenVINO Hardware Governance Report

- Passed: `True`
- Classification: `openvino_probe_available`
- Available devices: `['CPU', 'GPU.0', 'GPU.1', 'NPU']`
- GPU0 visible: `True`
- GPU1 visible: `True`
- NPU visible: `True`
- Requested NPU micro start mode: `startup`
- Recommended NPU micro start mode: `deferred`

## Routing policy

### `gpu1_primary_advisory`
- Owner: `Ollama/CUDA`
- Preferred device: `RTX 5080 / CUDA / GPU1`
- Policy: reserved_for_primary_advisory_not_openvino_workload

### `gpu0_companion_peer`
- Owner: `OpenVINO companion worker`
- Preferred device: `GPU.0`
- Policy: use GPU.0 when visible; never steal GPU.1 from Ollama

### `npu_micro_support`
- Owner: `OpenVINO NPU micro support`
- Preferred device: `NPU`
- Policy: live seed through broker while GPU mesh is active; provider execution may be deferred to avoid contention

### `deterministic_validators`
- Owner: `Python validators`
- Preferred device: `CPU`
- Policy: heavy audit authority stays deterministic and report-only

## Warnings

- GPU.1 is visible to OpenVINO but reserved for Ollama/CUDA; do not route OpenVINO work there by default.
- NPU startup mode may contend with GPU0/GPU1 on short live provider runs; deferred is preferred for local workstation use.
- IA_CARMINE_GPU0_COMPANION_MODEL_DIR is not configured; GPU0 semantic peer mode will classify as unconfigured/fallback.

```

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1445`
- SHA-256: `e8ca310c01ea1d331d15b4055546e666ea2c4ac9fec603a8888b88557675f7b5`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop

- Passed: `True`
- Recommendation count: `240`
- Patch plan count: `240`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `False`
- Provider execution performed: `False`
- Patch application performed: `False`

## Outputs

- `recommendations`: `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json` exists=`True` size=`4434640`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.md` exists=`True` size=`202826`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_bridge_orchestrator.json` exists=`True` size=`1257`
- `patch_plan`: `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.json` exists=`True` size=`5435491`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.md` exists=`True` size=`193076`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/validation/gpu1_primary_advisory_post_patchable_doc_python_probe_20260507-180555.md`

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

### `output/validation/gpu0_peer_response_post_patchable_doc_python_probe_20260507-180555.md`

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

### `output/validation/npu_micro_peer_assistant_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `407`
- SHA-256: `9ef381113dbf2e4b01253b2838c42e1b7b9ba6d0c36eef07b1a3cf3f353d6f01`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Micro Peer Assistant

- Passed: `True`
- Provider execution requested: `False`
- Provider execution performed: `False`
- Non-blocking: `True`
- Mode: `startup`
- Classification: `npu_final_provider_moved_to_gpu_peer_review`
- Reason: Final NPU provider pass moved off the performance path; startup NPU support and broker seed evidence are reviewed by GPU1/GPU0 plus deterministic validators.

```

### `output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `332`
- SHA-256: `f0421bb4082d1e596222dbc5b3529e087daa8f3a1151f2b3b8c850b9f9311c96`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Micro Runtime Tool Broker

- Passed: `True`
- Executed: `False`
- Tool execution count: `0`
- Classification: `npu_peer_provider_deferred_noop_broker`
- Reason: Final NPU provider pass moved off the performance path; startup NPU support and broker seed evidence are reviewed by GPU1/GPU0 plus deterministic validators.

```

### `output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.md`

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

### `output/validation/ai_peer_exchange_contract_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2584`
- SHA-256: `7dd21988266b0c12a3e6935be89427b48a439b74c9d3c4095eb1f434b5fbd3d0`
- Content included: `True`
- Content truncated: `False`

```text
# AI Peer Exchange Contract

- Passed: `True`
- Provider execution performed: `True`
- Classifications: `['peer_mesh_degraded_lanes_present_non_blocking', 'gpu0_peer_semantic_model_unconfigured']`

## Evidence

- `gpu1_primary_advisory` exists=`True` passed=`True` path=`output/validation/gpu1_primary_advisory_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0_peer_task_packet` exists=`True` passed=`True` path=`output/validation/gpu0_peer_task_packet_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0_peer_response` exists=`True` passed=`True` path=`output/validation/gpu0_peer_response_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0_tool_requests` exists=`True` passed=`None` path=`output/validation/gpu0_tool_requests_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/gpu0_peer_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json`
- `npu_micro_response` exists=`True` passed=`True` path=`output/validation/npu_micro_peer_assistant_post_patchable_doc_python_probe_20260507-180555.json`
- `npu_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json`
- `ai_peer_exchange` exists=`True` passed=`True` path=`output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.json`

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

### `output/validation/provider_runtime_heap_from_peer_reports_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1227`
- SHA-256: `325e5a7520b49af6727a56d6fecec7cbb2aa63582b4d914d52bf788fadf12451`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap From Peer Reports

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- event_count: `11`
- heap_event_count: `58`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

## Reports

- `gpu1`: `output/validation/gpu1_primary_advisory_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0`: `output/validation/gpu0_peer_response_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0_tool_requests`: `output/validation/gpu0_tool_requests_post_patchable_doc_python_probe_20260507-180555.json`
- `gpu0_broker`: `output/validation/gpu0_peer_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json`
- `npu`: `output/validation/npu_micro_peer_assistant_post_patchable_doc_python_probe_20260507-180555.json`
- `npu_broker`: `output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json`
- `peer_exchange`: `output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.json`
- `peer_contract`: `output/validation/ai_peer_exchange_contract_post_patchable_doc_python_probe_20260507-180555.json`

```

### `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1497`
- SHA-256: `770034c7a34ec0f326c297a1f6a893d13e9427961d3d994dbeff8438e0218e21`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Telemetry

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- event_count: `60`
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

- `broker`: `21`
- `deterministic`: `1`
- `gpu0`: `13`
- `gpu1`: `3`
- `npu`: `12`
- `orchestrator`: `10`

## Events by type

- `broker_request`: `14`
- `broker_result`: `20`
- `evidence_request`: `9`
- `evidence_response`: `11`
- `provider_state`: `3`
- `tool_catalog_request`: `1`
- `tool_catalog_response`: `1`
- `validation_signal`: `1`

## Interaction edges

- `broker->gpu0:broker_result`: `6`
- `broker->gpu1:tool_catalog_response`: `1`
- `broker->npu:broker_result`: `14`
- `deterministic->gpu1:validation_signal`: `1`
- `gpu0->broker:broker_request`: `6`
- `gpu0->gpu1:evidence_response`: `7`
- `gpu1->broker:tool_catalog_request`: `1`
- `gpu1->gpu0:evidence_request`: `2`
- `npu->broker:broker_request`: `8`
- `npu->gpu1:evidence_response`: `4`
- `orchestrator->gpu0:evidence_request`: `5`
- `orchestrator->none:provider_state`: `3`
- `orchestrator->npu:evidence_request`: `2`

```

### `output/validation/provider_runtime_heap_live_signals_init_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `316`
- SHA-256: `6599171bf6071f05936277eb6415cc0c6fc42bd3418da5601f2c36895448a1aa`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- mode: `init`
- event_count: `1`
- heap_event_count: `1`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_gpu1_request_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `325`
- SHA-256: `dd268ce82819d1807e14175086c697b16f424a8b089d7d9906c29e99d0446041`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- mode: `gpu1-request`
- event_count: `1`
- heap_event_count: `39`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_broker_results_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `327`
- SHA-256: `ca051739b8fb51340c2ca9b5d0b6d5bfb4ba93318bf5ed949a05a6a4a1663475`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- mode: `broker-results`
- event_count: `3`
- heap_event_count: `46`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_npu_support_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `324`
- SHA-256: `0c08daca66512157bba79a7ed9251d76353e04e69e1f10c0a8adec52227b058d`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- mode: `npu-support`
- event_count: `1`
- heap_event_count: `47`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

```

### `output/validation/provider_runtime_heap_live_signals_tool_catalog_complete_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `334`
- SHA-256: `03e0d53505f56f0554e0a88ca8c78f07aee6edceef5f906a10b54178138af739`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Live Signals

- passed: `True`
- stamp: `post_patchable_doc_python_probe_20260507-180555`
- mode: `tool-catalog-complete`
- event_count: `2`
- heap_event_count: `60`
- pending_broker_request_count: `0`
- event_log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

```

### `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/snapshot.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2581`
- SHA-256: `d29f11985bea3899ce48793495e370234332b6a3e7c996ab6984f28bf9883be8`
- Content included: `True`
- Content truncated: `False`

```text
# Provider Runtime Heap Snapshot

- Stamp: `post_patchable_doc_python_probe_20260507-180555`
- Event count: `60`
- Parse error count: `0`
- Pending broker requests: `0`
- Event log: `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/events.jsonl`

## Runtime architecture

- `gpu1`: `primary_advisory_planner`
- `gpu0`: `coworker_helper_openvino`
- `npu`: `microtask_responder`
- `broker`: `single_controlled_executor`
- `semantic_tools_registry`: `agent_runtime_tool_broker.TOOL_SPECS`
- `deterministic_validators`: `cpu_authority_validation_lane`
- `telemetry`: `append_only_event_stream`

## Events by lane

- `orchestrator`: `{'event_count': 10, 'latest_event_at': '2026-05-07T18:08:37', 'event_types': {'provider_state': 3, 'evidence_request': 7}}`
- `broker`: `{'event_count': 21, 'latest_event_at': '2026-05-07T18:08:45', 'event_types': {'broker_result': 20, 'tool_catalog_response': 1}}`
- `gpu0`: `{'event_count': 13, 'latest_event_at': '2026-05-07T18:08:37', 'event_types': {'evidence_response': 7, 'broker_request': 6}}`
- `npu`: `{'event_count': 12, 'latest_event_at': '2026-05-07T18:08:37', 'event_types': {'evidence_response': 4, 'broker_request': 8}}`
- `gpu1`: `{'event_count': 3, 'latest_event_at': '2026-05-07T18:08:45', 'event_types': {'evidence_request': 2, 'tool_catalog_request': 1}}`
- `deterministic`: `{'event_count': 1, 'latest_event_at': '2026-05-07T18:08:37', 'event_types': {'validation_signal': 1}}`

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

### `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7448`
- SHA-256: `2005bb9dba85c03302d493e8e9449ee295499e44804ae5549004bd92a6e68e13`
- Content included: `True`
- Content truncated: `False`

```text
# Full0To10 final tool product

## Request

Build the final local AI product for stamp post_patchable_doc_python_probe_20260507-180555 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.

## Deliverable scope

This package is the final-tool-product staging output. It includes track input contract, SQLite FTS5 evidence, accelerator control, provider governor, invocation dry-run plan, execution bridge, command plan, telemetry contracts, and quality evidence.

## Evidence index

- `effective_use_summary` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/effective_use/full0to10_effective_use_summary.json`
- `quality_product` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/effective_use/full0to10_effective_use_quality_product.md`
- `provider_hardening` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/effective_use/full0to10_provider_hardening_contracts.json`
- `tool_telemetry` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/effective_use/full0to10_effective_use_tool_telemetry.json`
- `optimization` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/effective_use/full0to10_effective_use_optimization.json`
- `quality_gate` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/quality_gate/full0to10_quality_gate.json`
- `accelerator_control` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/accelerator_control/full0to10_accelerator_control.json`
- `provider_governor` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_governor/full0to10_provider_governor.json`
- `provider_run_permit` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_governor/full0to10_provider_run_permit.json`
- `provider_invocation_plan` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_invocation_plan/full0to10_provider_invocation_plan.json`
- `provider_workload_report_contract` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_invocation_plan/full0to10_provider_workload_report_contract.json`
- `provider_expected_telemetry_contract` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json`
- `provider_execution_bridge` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_execution_bridge/full0to10_provider_execution_bridge.json`
- `provider_real_run_gate` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_execution_bridge/full0to10_provider_real_run_gate.json`
- `provider_command_plan` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_execution_bridge/full0to10_provider_command_plan.json`
- `provider_workload_output_paths` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_execution_bridge/full0to10_provider_workload_output_paths.json`
- `track_input_contract` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/track_inputs/full0to10_track_input_contract.json`
- `track_input_template` exists=`True` path=`output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/track_inputs/full0to10_track_input_template.json`

## Current run product evidence

- Passed: `True`
- Report count: `20`
- Artifact count: `13`
- Missing count: `0`

- report `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_orchestrator.json` exists=`True`
- report `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.json` exists=`True`
- report `output/analysis/gpu_npu_run_sync_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/provider_evidence_contract_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/ai_peer_exchange_contract_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/provider_runtime_heap_from_peer_reports_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/provider_runtime_heap_live_signals_tool_catalog_complete_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/ai_runtime_heap/post_patchable_doc_python_probe_20260507-180555/snapshot.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/runtime_tool_broker_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/gpu0_peer_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json` exists=`True`
- report `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_decision_loop.json` exists=`True`
- report `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`
- report `docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.json` exists=`True`

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

### `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/README.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `642`
- SHA-256: `6c98c9dad2e3ee158c857cd3af21d9e563d5b5be566a95b946cfd557775bb9cc`
- Content included: `True`
- Content truncated: `False`

```text
# Full0To10 final tool product package

- Passed: `True`
- Product markdown: `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/full0to10_final_tool_product.md`
- Track input contract: `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/track_inputs/full0to10_track_input_contract.json`
- Provider execution bridge: `output/validation/full0to10_final_tool_product_post_patchable_doc_python_probe_20260507-180555/provider_execution_bridge/full0to10_provider_execution_bridge.json`

This directory is generated output and should not be committed.

```

### `output/patch_specs/full_toolbox_post_patchable_doc_python_probe_20260507-180555_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `193076`
- SHA-256: `4a603cac04f3a78ca3a9e328a409bc9c603e46ef0ed03712dd1a407d37d4b7a6`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_patch_plan`
- Provider execution performed: `False`
- Patch application performed: `False`
- Patch plan count: `240`
- Fallback used: `False`
- Manual review required: `True`

## Inputs

- `orchestrator`: `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json`
- `orchestrator_kind`: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- `evidence_kind`: `agent_review_evidence_sufficiency`
- `gpu_kind`: `deterministic_recommendation_synthesizer`

## Patch plans

### consistency_001 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['Tools/ai/build_agent_review_code_patch_plan.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_agent_review_code_patch_plan.py:20` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py:20`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_002 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138` targeting `text
Tools/ai/simulate_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
Tools/ai/simulate_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_003 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['CHATGPT.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT.md:60` targeting `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT.md:60`. Target `CHATGPT.md` and resolve `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_004 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['Tools/ai/analyze_gpu_npu_run_sync.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/analyze_gpu_npu_run_sync.py` targeting `Tools/ai/analyze_gpu_npu_run_sync.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/analyze_gpu_npu_run_sync.py`. Target `Tools/ai/analyze_gpu_npu_run_sync.py` and resolve `Tools/ai/analyze_gpu_npu_run_sync.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_005 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['Tools/ai/build_code_edit_proposal_from_plan.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_edit_proposal_from_plan.py:26` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_edit_proposal_from_plan.py:26`. Target `Tools/ai/build_code_edit_proposal_from_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_006 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139` targeting `Tools/ai/simulate_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `Tools/ai/simulate_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_007 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52` targeting `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_008 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['Tools/ai/build_agent_agnostic_tool_inventory.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_agnostic_tool_inventory.py` targeting `Tools/ai/build_agent_agnostic_tool_inventory.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_agnostic_tool_inventory.py`. Target `Tools/ai/build_agent_agnostic_tool_inventory.py` and resolve `Tools/ai/build_agent_agnostic_tool_inventory.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_009 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['Tools/ai/build_code_patch_artifact_pack.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_artifact_pack.py:22` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_patch_artifact_pack.py:22`. Target `Tools/ai/build_code_patch_artifact_pack.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_010 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156` targeting `text
Tools/ai/run_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
Tools/ai/run_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_011 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17` targeting `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_012 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['Tools/ai/build_agent_review_code_patch_plan.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_code_patch_plan.py` targeting `Tools/ai/build_agent_review_code_patch_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools/ai/build_agent_review_code_patch_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_013 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['Tools/ai/build_code_patch_docs_followup.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_docs_followup.py:22` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_patch_docs_followup.py:22`. Target `Tools/ai/build_code_patch_docs_followup.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_014 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157` targeting `Tools/ai/run_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `Tools/ai/run_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_015 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52` targeting `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_016 — python_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['Tools/ai/build_agent_review_evidence_sufficiency.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_evidence_sufficiency.py` targeting `Tools/ai/build_agent_review_evidence_sufficiency.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_evidence_sufficiency.py`. Target `Tools/ai/build_agent_review_evidence_sufficiency.py` and resolve `Tools/ai/build_agent_review_evidence_sufficiency.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_017 — python_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23` targeting `Tools.ai.build_github_evidence_bundle`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23`. Target `Tools/ai/enrich_github_evidence_bundle_code_plan.py` and resolve `Tools.ai.build_github_evidence_bundle` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_018 — doc_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230` targeting `check_runtime_hardware_capability_manifest.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `check_runtime_hardware_capability_manifest.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_019 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:55` targeting `hardware-memory.md`.
- Strategy: Build a focused patch plan for `md_ment
```

### `docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `22380`
- SHA-256: `aeed43b7e7386e64e444aae72aba35cdefbe00c054878cc3c7c56f7750a4f51e`
- Content included: `True`
- Content truncated: `True`

```text
# Patch Plan Quality Product Gate

- passed: `True`
- quality_gate_passed: `True`
- classification: `ready_for_manual_patch_review`
- non_blocking: `True`
- Patch plans: `240`
- Average plan score: `100.0`
- SQLite FTS5 enabled: `True`
- FTS total hits: `40`

## Fallback path notes

- None.

## Plan scores

- `consistency_001` score=`100` targets=`['Tools/ai/build_agent_review_code_patch_plan.py']`
- `consistency_002` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_003` score=`100` targets=`['CHATGPT.md']`
- `consistency_004` score=`100` targets=`['Tools/ai/analyze_gpu_npu_run_sync.py']`
- `consistency_005` score=`100` targets=`['Tools/ai/build_code_edit_proposal_from_plan.py']`
- `consistency_006` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_007` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_008` score=`100` targets=`['Tools/ai/build_agent_agnostic_tool_inventory.py']`
- `consistency_009` score=`100` targets=`['Tools/ai/build_code_patch_artifact_pack.py']`
- `consistency_010` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_011` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_012` score=`100` targets=`['Tools/ai/build_agent_review_code_patch_plan.py']`
- `consistency_013` score=`100` targets=`['Tools/ai/build_code_patch_docs_followup.py']`
- `consistency_014` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_015` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_016` score=`100` targets=`['Tools/ai/build_agent_review_evidence_sufficiency.py']`
- `consistency_017` score=`100` targets=`['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- `consistency_018` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_019` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_020` score=`100` targets=`['Tools/ai/build_agent_review_patch_bundle.py']`
- `consistency_025` score=`100` targets=`['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- `consistency_022` score=`100` targets=`['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_023` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_024` score=`100` targets=`['Tools/ai/build_agent_review_patch_plan.py']`
- `consistency_029` score=`100` targets=`['Tools/validation/build_python_line_count_csv.py']`
- `consistency_026` score=`100` targets=`['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_027` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_028` score=`100` targets=`['Tools/ai/build_agent_state_packet.py']`
- `consistency_033` score=`100` targets=`['Tools/validation/check_artifact_domain_registry.py']`
- `consistency_030` score=`100` targets=`['Scripting/README.md']`
- `consistency_031` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_032` score=`100` targets=`['Tools/ai/build_ai_context_pack.py']`
- `consistency_041` score=`100` targets=`['Tools/validation/check_blender_shared_compat_smoke.py']`
- `consistency_034` score=`100` targets=`['Scripting/README.md']`
- `consistency_035` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_036` score=`100` targets=`['Tools/ai/build_code_edit_proposal_from_plan.py']`
- `consistency_045` score=`100` targets=`['Tools/validation/run_agent_review_code_patch_plan_smoke.py']`
- `consistency_038` score=`100` targets=`['Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md']`
- `consistency_039` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_040` score=`100` targets=`['Tools/ai/build_code_interpreter_report.py']`
- `consistency_053` score=`100` targets=`['Tools/validation/run_code_edit_proposal_smoke.py']`
- `consistency_042` score=`100` targets=`['Scripting/shared/README.md']`
- `consistency_043` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_044` score=`100` targets=`['Tools/ai/build_code_patch_artifact_pack.py']`
- `consistency_046` score=`100` targets=`['Scripting/shared/README.md']`
- `consistency_047` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_048` score=`100` targets=`['Tools/ai/build_code_patch_docs_followup.py']`
- `consistency_050` score=`100` targets=`['Scripting/shared/README.md']`
- `consistency_051` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_052` score=`100` targets=`['Tools/ai/build_dry_run_matrix_evidence_bundle.py']`
- `consistency_054` score=`100` targets=`['Scripting/shared/README.md']`
- `consistency_055` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_056` score=`100` targets=`['Tools/ai/build_full_context_golden_proposals.py']`
- `consistency_058` score=`100` targets=`['Scripting/shared/README.md']`
- `consistency_059` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_060` score=`100` targets=`['Tools/ai/build_full_run_evidence_bundle_zip.py']`
- `consistency_061` score=`100` targets=`['Scripting/shared/README.md']`
- `consistency_062` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/README.md']`
- `consistency_063` score=`100` targets=`['Tools/ai/build_github_evidence_bundle.py']`
- `consistency_064` score=`100` targets=`['Scripting/v61b/PROJECT_STRUCTURE.md']`
- `consistency_065` score=`100` targets=`['CHATGPT/DISCOVERY_CONTRACT.md']`
- `consistency_066` score=`100` targets=`['Tools/ai/build_gpu_repair_failure_recommendation.py']`
- `consistency_067` score=`100` targets=`['Scripting/v61b/README.md']`
- `consistency_068` score=`100` targets=`['CHATGPT/README.md']`
- `consistency_069` score=`100` targets=`['Tools/ai/build_local_ai_enrichment_plan.py']`
- `consistency_070` score=`100` targets=`['Scripting/v61b/README.md']`
- `consistency_071` score=`100` targets=`['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_072` score=`100` targets=`['Tools/ai/build_patch_specs_from_proposals.py']`
- `consistency_073` score=`100` targets=`['Scripting/v61b/README.md']`
- `consistency_074` score=`100` targets=`['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_075` score=`100` targets=`['Tools/ai/build_repository_change_proposals.py']`
- `consistency_076` score=`100` targets=`['Tools/npu/README.md']`
- `consistency_077` score=`100` targets=`['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_078` score=`100` targets=`['Tools/ai/build_runtime_hardware_capability_manifest.py']`
- `consistency_079` score=`100` targets=`['Tools/npu/README.md']`
- `consistency_080` score=`100` targets=`['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_081` score=`100` targets=`['Tools/ai/build_selective_execution_plan.py']`
- `consistency_082` score=`100` targets=`['Tools/repo_patch_runner/README.md']`
- `consistency_083` score=`100` targets=`['CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md']`
- `consistency_084` score=`100` targets=`['Tools/ai/build_semantic_evidence_chunks.py']`
- `consistency_085` score=`100` targets=`['Tools/validation/README.md']`
- `consistency_086` score=`100` targets=`['FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-001.md']`
- `consistency_087` score=`100` targets=`['Tools/ai/check_local_resource_lanes.py']`
- `consistency_088` score=`100` targets=`['docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md']`
- `consistency_089` score=`100` targets=`['FULL_RUN_UNICA_TUTTO_SU_TUTTO/part-002.md']`
- `consistency_090` score=`100` targets=`['Tools/ai/check_npu_provider_environment.py']`
- `consistency_091` score=`100` targets=`['docs/CODE_CONSULTATION_REPORT/part-001.md']`
- `consistency_092` score=`100` targets=`['README.md']`
- `consistency_093` score=`100` targets=`['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- `consistency_094` score=`100` targets=`['docs/CODE_CONSULTATION_REPORT/part-001.md']`
- `consistency_095` score=`100` targets=`['Scripting/README.md']`
- `consistency_096` score=`100` targets=`['Tools/ai/full0to10_memory_tool.py']`
- `consistency_097` score=`100` targets=`['docs/DEVELOPER_GUIDE.md']`
- `consistency_098` score=`100` targets=`['Tools/git/README.md']`
- `consistency_099` score=`100` targets=`['Tools/ai/full0to10_runtime_tool.py']`
- `consistency_100` score=`100` targets=`['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']`
- `consistency_101` score=`100` targets=`['Tools/git/README.md']`
- `consistency_102` score=`100` targets=`['Tools/ai/promote_patch_spec_draft.py']`
- `consistency_103` score=`100` targets=`['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']`
- `consistency_104` score=`100` targets=`['Tools/npu/README.md']`
- `consistency_105` score=`100` targets=`['Tools/ai/replay_gpu_planner_json_contract.py']`
- `consistency_106` score=`100` targets=`['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']`
- `consistency_107` score=`100` targets=`['Tools/npu/README.md']`
- `consistency_108` score=`100` targets=`['Tools/ai/review_agent_memory.py']`
- `consistency_109` score=`100` targets=`['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']`
- `consistency_110` score=`100` targets=`['Tools/npu/README.md']`
- `consistency_111` score=`100` targets=`['Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py']`
- `consistency_112` score=`100` targets=`['docs/LOCAL_AI_TASKS/carmine-like-patch-loop/01-procedure.md']`
- `consistency_113` score=`100` targets=`['Tools/npu/README.md']`
- `consistency_114` score=`100` targets=`['Tools/ai/run_local_provider_probe.py']`
- `consistency_115` score=`100` targets=`['docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md']`
- `consistency_116` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_117` score=`100` targets=`['Tools/ai/run_parallel_artifact_pipeline.py']`
- `consistency_118` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']`
- `consistency_119` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_120` score=`100` targets=`['Tools/ai/run_pipeline_dry_run_matrix.py']`
- `consistency_121` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']`
- `consistency_122` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_123` score=`100` targets=`['Tools/docs/apply_md_code_coherence_refactor.py']`
- `consistency_124` score=`100` targets=`['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']`
- `consistency_125` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_126` score=`100` targets=`['Tools/docs/build_code_aware_md_coherence.py']`
- `consistency_127` score=`100` targets=`['docs/LOCAL_AI_TASKS/full0to10-quality-gate/10-operational-wrapper-guards.md']`
- `consistency_128` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_129` score=`100` targets=`['Tools/docs/split_large_markdown.py']`
- `consistency_130` score=`100` targets=`['docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md']`
- `consistency_131` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_132` score=`100` targets=`['Tools/npu/build_npu_code_context.py']`
- `consistency_133` score=`100` targets=`['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- `consistency_134` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_135` score=`100` targets=`['Tools/npu/build_npu_knowledge_broker_packet.py']`
- `consistency_136` score=`100` targets=`['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_137` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_138` score=`100` targets=`['Tools/npu/build_project_ai_index.py']`
- `consistency_139` score=`100` targets=`['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_140` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_141` score=`100` targets=`['Tools/npu/build_provider_result_report.py']`
- `consistency_142` score=`100` targets=`['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/02-zip-01-tools.md']`
- `consistency_143` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_144` score=`100` targets=`['Tools/npu/build_semantic_code_chunks.py']`
- `consistency_145` score=`100` targets=`['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md']`
- `consistency_146` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_147` score=`100` targets=`['Tools/repo_patch_runner/apply_repo_mods.py']`
- `consistency_148` score=`100` targets=`['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/03-zip-02-apply.md']`
- `consistency_149` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_150` score=`100` targets=`['Tools/validation/build_markdown_inventory.py']`
- `consistency_151` score=`100` targets=`['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md']`
- `consistency_152` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_153` score=`100` targets=`['Tools/validation/build_python_line_count_csv.py']`
- `consistency_154` score=`100` targets=`['docs/LOCAL_AI_TASKS/markdown-line-budget-download-procedure/04-zip-03-all-in-one.md']`
- `consistency_155` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_156` score=`100` targets=`['Tools/validation/build_script_inventory.py']`
- `consistency_157` score=`100` targets=`['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- `consistency_158` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_159` score=`100` targets=`['Tools/validation/run_agent_review_patch_plan_full_validation.py']`
- `consistency_160` score=`100` targets=`['docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap/part-001.md']`
- `consistency_161` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_162` score=`100` targets=`['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- `consistency_163` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_164` score=`100` targets=`['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_165` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_166` score=`100` targets=`['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_167` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_168` score=`100` targets=`['docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md']`
- `consistency_169` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_170` score=`100` targets=`['docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md']`
- `consistency_171` score=`100` targets=`['Tools/npu/npu_code_context.md']`
- `consistency_172` score=`100` targets=`['docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md']`
- `consistency_173` score=`100` targets=`['Tools/npu/npu_code_context.md
```

### `docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `11565`
- SHA-256: `a4339ee8a38ff9ba22619de7cb22bf92972c1afd177da216ed1b5df7f0a63211`
- Content included: `True`
- Content truncated: `False`

```text
# Patch Notes Quality Product

- passed: `True`
- quality_gate_passed: `True`
- classification: `ready_for_patch_notes_review`
- non_blocking: `True`
- quality_score: `100.0`
- Input task MD: `docs/LOCAL_AI_TASKS/all-all-project-progression-python-first-patch-notes-2026-05-07.md`
- Task digest: `70644ce8329993bde699a25a53596889b906eea5afc4a1d92d77b2a2e88502dc`
- Manual review required: `True`
- Telemetry quality score: `87.5`
- Evidence coverage score: `75.0`
- Patch notes applicable: `True`
- Patch notes invalid count: `0`

## Request

Scope: whole repository Mode: ALL_ALL / Python-first / policy-aware / refactor-proposal ## Objective Produce a larger and more useful patch-notes product for progressing the project itself.

## Patch Plan Summary

- patch_plan_count: `240`
- patch_quality_gate_passed: `True`
- patch_quality_classification: `ready_for_manual_patch_review`
- average_plan_score: `100.0`

## Patch Notes Applicability

- note_count: `240`
- applicable_count: `240`
- invalid_note_count: `0`
- all_applicable: `True`

## Product Sufficiency

- mode: `ALL_ALL`
- requested_min_patch_notes: `40`
- actual_patch_note_count: `240`
- sufficient: `True`
- requested_areas: `['doc_doc', 'doc_python', 'python_doc', 'python_python', 'policy_violation', 'refactor_candidate', 'telemetry_gap', 'evidence_gap']`
- available_requested_areas: `['doc_doc', 'doc_python', 'python_doc', 'python_python']`
- unavailable_requested_areas: `['policy_violation', 'refactor_candidate', 'telemetry_gap', 'evidence_gap']`
- actual_areas: `['doc_doc', 'doc_python', 'python_doc', 'python_python']`
- missing_available_areas: `[]`
- insufficiency_reasons: `[]`

## Generated Patch Notes

- `consistency_001` `python_python` score=`100` targets=`['Tools/ai/build_agent_review_code_patch_plan.py']`
  - Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_agent_review_code_patch_plan.py:20` targeting `Tools.ai.code_patch_plan_common`.
- `consistency_002` `doc_python` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
  - Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138` targeting `text
Tools/ai/simulate_npu_tool_proxy.py`.
- `consistency_003` `doc_doc` score=`100` targets=`['CHATGPT.md']`
  - Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT.md:60` targeting `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md`.
- `consistency_004` `python_doc` score=`100` targets=`['Tools/ai/analyze_gpu_npu_run_sync.py']`
  - Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/analyze_gpu_npu_run_sync.py` targeting `Tools/ai/analyze_gpu_npu_run_sync.py`.
- `consistency_005` `python_python` score=`100` targets=`['Tools/ai/build_code_edit_proposal_from_plan.py']`
  - Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_edit_proposal_from_plan.py:26` targeting `Tools.ai.code_patch_plan_common`.
- `consistency_006` `doc_python` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
  - Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139` targeting `Tools/ai/simulate_npu_tool_proxy.py`.
- `consistency_007` `doc_doc` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
  - Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52` targeting `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md`.
- `consistency_008` `python_doc` score=`100` targets=`['Tools/ai/build_agent_agnostic_tool_inventory.py']`
  - Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_agnostic_tool_inventory.py` targeting `Tools/ai/build_agent_agnostic_tool_inventory.py`.
- `consistency_009` `python_python` score=`100` targets=`['Tools/ai/build_code_patch_artifact_pack.py']`
  - Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_artifact_pack.py:22` targeting `Tools.ai.code_patch_plan_common`.
- `consistency_010` `doc_python` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
  - Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156` targeting `text
Tools/ai/run_npu_tool_proxy.py`.
- `consistency_011` `doc_doc` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
  - Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17` targeting `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md`.
- `consistency_012` `python_doc` score=`100` targets=`['Tools/ai/build_agent_review_code_patch_plan.py']`
  - Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_code_patch_plan.py` targeting `Tools/ai/build_agent_review_code_patch_plan.py`.
- `consistency_013` `python_python` score=`100` targets=`['Tools/ai/build_code_patch_docs_followup.py']`
  - Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_docs_followup.py:22` targeting `Tools.ai.code_patch_plan_common`.
- `consistency_014` `doc_python` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
  - Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157` targeting `Tools/ai/run_npu_tool_proxy.py`.
- `consistency_015` `doc_doc` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
  - Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52` targeting `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md`.
- `consistency_016` `python_doc` score=`100` targets=`['Tools/ai/build_agent_review_evidence_sufficiency.py']`
  - Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_evidence_sufficiency.py` targeting `Tools/ai/build_agent_review_evidence_sufficiency.py`.
- `consistency_017` `python_python` score=`100` targets=`['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
  - Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23` targeting `Tools.ai.build_github_evidence_bundle`.
- `consistency_018` `doc_python` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
  - Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230` targeting `check_runtime_hardware_capability_manifest.py`.
- `consistency_019` `doc_doc` score=`100` targets=`['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
  - Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:55` targeting `hardware-memory.md`.
- `consistency_020` `python_doc` score=`100` targets=`['Tools/ai/build_agent_review_patch_bundle.py']`
  - Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_patch_bundle.py` targeting `Tools/ai/build_agent_review_patch_bundle.py`.

## Telemetry Quality

- runtime_usage_seen: `True`
- runtime_capability_seen: `True`
- tool_call_entries_seen: `True`
- provider_execution_observed: `True`
- gpu1_primary_observed: `True`
- gpu0_companion_observed: `True`
- npu_micro_or_tool_observed: `True`
- npu_final_review_observed: `False`
- Missing signals: `['npu_final_review_observed']`

## Evidence Coverage

- patch_quality: `True`
- decision_loop: `True`
- runtime_usage: `True`
- runtime_capability: `True`
- repository_consistency: `True`
- memory_bundle: `True`
- full_toolbox_telemetry: `False`
- github_evidence_bundle: `False`

## Success Cases

- `patch_notes_quality_product` score=`100.0` gate=`True`
- `patch_plan_quality_product` score=`100.0` gate=`True`
- `runtime_tool_broker` score=`None` gate=`None`
- `npu_final_review` score=`None` gate=`None`

## Structured Fallback Cases

- `npu_provider_empty_or_timeout` primary=`npu_semantic_provider` fallback=`npu_brokered_tool_support` recovered=`True`

## Validation Commands

- `python -m py_compile Tools/ai/build_agent_review_code_patch_plan.py`
- `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
- `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
- `git diff --check`
- `git status --short`
- `python -m py_compile Tools/ai/analyze_gpu_npu_run_sync.py`
- `python -m py_compile Tools/ai/build_code_edit_proposal_from_plan.py`
- `python -m py_compile Tools/ai/build_agent_agnostic_tool_inventory.py`
- `python -m py_compile Tools/ai/build_code_patch_artifact_pack.py`
- `python -m py_compile Tools/ai/build_code_patch_docs_followup.py`
- `python -m py_compile Tools/ai/build_agent_review_evidence_sufficiency.py`
- `python -m py_compile Tools/ai/enrich_github_evidence_bundle_code_plan.py`
- `python -m py_compile Tools/ai/build_agent_review_patch_bundle.py`
- `python -m py_compile Tools/ai/build_agent_review_patch_plan.py`
- `python -m py_compile Tools/validation/build_python_line_count_csv.py`
- `python -m py_compile Tools/ai/build_agent_state_packet.py`
- `python -m py_compile Tools/validation/check_artifact_domain_registry.py`
- `python -m py_compile Tools/ai/build_ai_context_pack.py`
- `python -m py_compile Tools/validation/check_blender_shared_compat_smoke.py`
- `python -m py_compile Tools/validation/run_agent_review_code_patch_plan_smoke.py`

## Stop Conditions

- Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.
- Stop if the target/source evidence no longer exists after refreshing master.
- Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.
- Stop if resolving the finding requires inventing behavior not supported by code evidence.

## Warnings

- full_toolbox_telemetry: missing (C:\Users\carmi\blender\blender-audio-project\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_post_patchable_doc_python_probe_20260507-180555.json)

```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-180624.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `34069`
- SHA-256: `9633e3484dbb14090599994d98bbb5d9e6aa0ccee06aee351641625b127ac687`
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
Tools/ai/build_deterministic_recommendations.py,1015
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/ai/build_runtime_tool_usage_telemetry.py,836
Tools/ai/agent_runtime_tool_broker.py,751
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
Tools/ai/build_full_toolbox_run_telemetry_summary.py,613
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/analyze_gpu_npu_run_sync.py,587
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,579
Tools/ai/run_pipeline_dry_run_matrix.py,573
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
Tools/ai/patch_notes_quality_product/scoring.py,465
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
Tools/validation/run_patch_notes_quality_product_smoke.py,399
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
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py,348
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py,345
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/build_markdown_inventory.py,339
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/validation/check_local_ai_adapter_manifest.py,331
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py,328
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
Tools/ai/provider_runtime_heap_live_signals.py,306
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
Tools/ai/repository_consistency_map/python_inventory.py,225
Tools/ai/build_provider_runtime_heap_telemetry.py,223
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/docs/apply_md_code_coherence_refactor.py,221
Tools/validation/check_file_line_limits.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/build_python_line_count_csv.py,212
Tools/ai/patch_notes_quality_product/telemetry_quality.py,210
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
Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/ai/code_interpreter_report/scanner.py,191
Tools/validation/full_run_bundle_completeness.py,190
Tools/validation/report_utils.py,190
Tools/validation/run_runtime_tool_guidance_fallback_smoke.py,190
Tools/ai/check_npu_provider_environment.py,189
Tools/ai/patch_notes_quality_product/builder.py,188
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
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py,132
Tools/ai/full_run_bundle_zip/discovery.py,130
Tools/ai/model_json.py,130
Tools/validation/check_gpu0_companion_contract.py,130
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
Tools/ai/runtime_hardware_capability/policy.py,118
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
Tools/ai/repository_consistency_map/findings.py,114
build_track_summary.py,113
Tools/ai/run_provider_runtime_heap_gpu_peer_smoke.py,112
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_engine.py,112
Tools/npu/ai_memory_context.py,111
Tools/ai/provider_mesh_runtime/npu_micro.py,110
Tools/workflow/asset_inventory.py,110
Tools/ai/full0to10_final_product_quality/builder.py,108
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/ai/full0to10_provider_feedback_loop/builder.py,106
Tools/validation/check_python_syntax.py,105
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
Tools/ai/build_repository_consistency_map.py,96
Tools/ai/full0to10_effective_use/builder.py,96
Tools/validation/check_npu_pipeline_docs.py,96
Tools/ai/full0to10_hardware_capability/openvino_devices.py,95
Tools/ai/full0to10_provider_invocation_plan/builder.py,94
Tools/ai/full0to10_auto_refactor_apply/applier.py,
```

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `3949`
- SHA-256: `1e85bb1b1370ed8eeef4e7c4a0b6410dd1f8231c1144f2c3aea2899402ad8cdc`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_review_evidence_sufficiency",
  "generated_at": "2026-05-07T18:07:04",
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
        "path": "output/analysis/repository_consistency_map_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
        "exists": true,
        "kind": "repository_consistency_map",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/repository_consistency_map_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
        "exists": true,
        "kind": "repository_consistency_map_smoke",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/analysis/code_interpreter_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
        "exists": true,
        "kind": "code_interpreter_report",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/python_line_count_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
        "exists": true,
        "kind": "python_line_count_csv",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/python_syntax_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
        "exists": true,
        "kind": "python_syntax",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/validation/openvino_hardware_governance_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
        "exists": true,
        "kind": "openvino_hardware_governance_report",
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

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1257`
- SHA-256: `5ed2fa18be53e633e45e46ca5582d546a91ae0317eb6fac7aba8992eae5ff58c`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-07T18:08:41",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json",
  "gpu_recommendation_count": 240,
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

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `4434640`
- SHA-256: `f575b47873848dae884b1c739c3d37f89ae7b815a9a3ab13e4e6facc3af642e3`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_synthesizer",
  "generated_at": "2026-05-07T18:08:41",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "recommendation_count": 240,
  "recommendations": [
    {
      "id": "consistency_001",
      "area": "python_python",
      "status": "ready_for_patch_plan",
      "target_files": [
        "Tools/ai/build_agent_review_code_patch_plan.py"
      ],
      "rationale": "Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_agent_review_code_patch_plan.py:20` targeting `Tools.ai.code_patch_plan_common`.",
      "proposed_strategy": "Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py:20`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.",
      "risk": "medium",
      "validation_commands": [
        "python -m py_compile Tools/ai/build_agent_review_code_patch_plan.py",
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
        "Tools/ai/build_agent_review_code_patch_plan.py:20"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/python_line_count_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/python_syntax_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/npu_provider_environment_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/openvino_hardware_governance_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
          "kind": "openvino_hardware_governance_report",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_json_contract_replay_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/provider_evidence_contract_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu0_companion_task_lane_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu0_companion_contract_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/ai_pipeline/gpu0_peer_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_gpu0_peer_support.json",
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
          "path": "output/ai_pipeline/npu_micro_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_npu_micro_support.json",
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
          "path": "output/validation/gpu1_primary_advisory_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu0_peer_task_packet_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu0_peer_response_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu0_tool_requests_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/gpu0_peer_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/npu_micro_peer_assistant_post_patchable_doc_python_probe_20260507-180555.json",
          "kind": "npu_micro_peer_assistant",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/npu_micro_runtime_tool_broker_post_patchable_doc_python_probe_20260507-180555.json",
          "kind": "agent_runtime_tool_broker",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/ai_peer_exchange_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/ai_peer_exchange_contract_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/provider_runtime_heap_live_signals_init_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/provider_runtime_heap_live_signals_gpu1_request_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/provider_runtime_heap_live_signals_broker_results_post_patchable_doc_python_probe_20260507-180555.json",
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
          "path": "output/validation/provider_runti
```

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `202826`
- SHA-256: `be374d49f1bef5bc25f574534fa1f5ba9159e40bf5cdb1b818b8f211f25be498`
- Content included: `True`
- Content truncated: `True`

```text
# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `240`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `model_output_schema_mismatch`
- Evidence ready for manual patch count: `0`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### consistency_001 — python_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['Tools/ai/build_agent_review_code_patch_plan.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_agent_review_code_patch_plan.py:20` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py:20`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_002 — doc_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138` targeting `text
Tools/ai/simulate_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:138`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
Tools/ai/simulate_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_003 — doc_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['CHATGPT.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT.md:60` targeting `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT.md:60`. Target `CHATGPT.md` and resolve `text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_004 — python_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['Tools/ai/analyze_gpu_npu_run_sync.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/analyze_gpu_npu_run_sync.py` targeting `Tools/ai/analyze_gpu_npu_run_sync.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/analyze_gpu_npu_run_sync.py`. Target `Tools/ai/analyze_gpu_npu_run_sync.py` and resolve `Tools/ai/analyze_gpu_npu_run_sync.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_005 — python_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['Tools/ai/build_code_edit_proposal_from_plan.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_edit_proposal_from_plan.py:26` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_edit_proposal_from_plan.py:26`. Target `Tools/ai/build_code_edit_proposal_from_plan.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_006 — doc_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139` targeting `Tools/ai/simulate_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:139`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `Tools/ai/simulate_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_007 — doc_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52` targeting `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:52`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_008 — python_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['Tools/ai/build_agent_agnostic_tool_inventory.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_agnostic_tool_inventory.py` targeting `Tools/ai/build_agent_agnostic_tool_inventory.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_agnostic_tool_inventory.py`. Target `Tools/ai/build_agent_agnostic_tool_inventory.py` and resolve `Tools/ai/build_agent_agnostic_tool_inventory.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_009 — python_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['Tools/ai/build_code_patch_artifact_pack.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_artifact_pack.py:22` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_patch_artifact_pack.py:22`. Target `Tools/ai/build_code_patch_artifact_pack.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_010 — doc_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156` targeting `text
Tools/ai/run_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:156`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `text
Tools/ai/run_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_011 — doc_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17` targeting `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:17`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_012 — python_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['Tools/ai/build_agent_review_code_patch_plan.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_code_patch_plan.py` targeting `Tools/ai/build_agent_review_code_patch_plan.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_code_patch_plan.py`. Target `Tools/ai/build_agent_review_code_patch_plan.py` and resolve `Tools/ai/build_agent_review_code_patch_plan.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_013 — python_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['Tools/ai/build_code_patch_docs_followup.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/build_code_patch_docs_followup.py:22` targeting `Tools.ai.code_patch_plan_common`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/build_code_patch_docs_followup.py:22`. Target `Tools/ai/build_code_patch_docs_followup.py` and resolve `Tools.ai.code_patch_plan_common` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_014 — doc_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157` targeting `Tools/ai/run_npu_tool_proxy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:157`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `Tools/ai/run_npu_tool_proxy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_015 — doc_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- Rationale: Repository consistency mapper reported medium `md_mentions_missing_markdown_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52` targeting `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md`.
- Strategy: Build a focused patch plan for `md_mentions_missing_markdown_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md:52`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md` and resolve `text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_016 — python_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['Tools/ai/build_agent_review_evidence_sufficiency.py']`
- Rationale: Repository consistency mapper reported low `documented_python_script_without_obvious_smoke` at `Tools/ai/build_agent_review_evidence_sufficiency.py` targeting `Tools/ai/build_agent_review_evidence_sufficiency.py`.
- Strategy: Build a focused patch plan for `documented_python_script_without_obvious_smoke` using mapper evidence `Tools/ai/build_agent_review_evidence_sufficiency.py`. Target `Tools/ai/build_agent_review_evidence_sufficiency.py` and resolve `Tools/ai/build_agent_review_evidence_sufficiency.py` without formatting-only edits. Mapper recommendation: Consider adding a smoke validator or documenting why none is needed.

### consistency_017 — python_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- Rationale: Repository consistency mapper reported high `python_import_symbol_missing` at `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23` targeting `Tools.ai.build_github_evidence_bundle`.
- Strategy: Build a focused patch plan for `python_import_symbol_missing` using mapper evidence `Tools/ai/enrich_github_evidence_bundle_code_plan.py:23`. Target `Tools/ai/enrich_github_evidence_bundle_code_plan.py` and resolve `Tools.ai.build_github_evidence_bundle` without formatting-only edits. Mapper recommendation: Fix the import or add the missing module in a focused code PR.

### consistency_018 — doc_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230` targeting `check_runtime_hardware_capability_manifest.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md:230`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` and resolve `check_runtime_hardware_capability_manifest.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_019 — doc_doc
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['CHATGPT/2026-
```

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `180957`
- SHA-256: `2af993ec62a006c6e654e59e2daa0460a80a56d06a71df99bd07861d24689adc`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-07T18:08:30",
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
  "elapsed_seconds": 81.698,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 69.994,\n  \"round_count\": 4,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"empty_recommendations_reason\": \"model_output_schema_mismatch\",\n  \"runtime_tool_broker_enabled\": false,\n  \"runtime_tool_bootstrap_executed\": false,\n  \"runtime_tool_bootstrap_passed\": null,\n  \"runtime_tool_bootstrap_request_count\": 0,\n  \"runtime_tool_bootstrap_execution_count\": 0,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 16,\n  \"runtime_tool_execution_count\": 0,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 0,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 0,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"collect_more_evidence\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "model_output_schema_mismatch",
  "gpu_evidence_ready_for_manual_patch_count": 0,
  "gpu_recommended_next_layer": "collect_more_evidence",
  "gpu_live_context_refresh_count": 4,
  "runtime_tool_broker_enabled": true,
  "runtime_tool_bootstrap_executed": true,
  "runtime_tool_bootstrap_passed": true,
  "runtime_tool_bootstrap_request_count": 7,
  "runtime_tool_bootstrap_execution_count": 7,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 34,
  "runtime_tool_execution_count": 18,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 18,
  "gpu_runtime_tool_broker_enabled": false,
  "gpu_runtime_tool_request_count": 16,
  "gpu_runtime_tool_execution_count": 0,
  "gpu_runtime_tool_failed_count": 0,
  "gpu_runtime_tool_blocked_count": 0,
  "gpu_runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 16,
  "runtime_tool_provider_request_execution_count": 11,
  "runtime_tool_provider_request_failed_count": 0,
  "runtime_tool_provider_request_blocked_count": 0,
  "runtime_tool_provider_request_result_count": 11,
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
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\round_000_tool_requests.json",
      "--tool-output-dir",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000",
      "--timeout-seconds",
      "300",
      "--output",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\round_000_runtime_tool_broker.json",
      "--markdown-output",
      "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\round_000_runtime_tool_broker.md"
    ],
    "returncode": 0,
    "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\post_patchable_doc_python_probe_20260507-180555\\\\round_000\\\\round_000_runtime_tool_broker.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\post_patchable_doc_python_probe_20260507-180555\\\\round_000\\\\round_000_runtime_tool_broker.md\",\n  \"tool_request_count\": 7,\n  \"tool_execution_count\": 7,\n  \"blocked_tool_count\": 0,\n  \"failed_tool_count\": 0,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"persistent_memory_write_performed\": false,\n  \"persistent_memory_write_count\": 0,\n  \"operational_sqlite_write_performed\": false,\n  \"operational_sqlite_write_count\": 0,\n  \"operational_memory_clear_count\": 0\n}\n",
    "stderr_tail": "",
    "error": "",
    "request_file": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/round_000_tool_requests.json",
    "broker_output": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/round_000_runtime_tool_broker.json",
    "broker_markdown": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/round_000_runtime_tool_broker.md",
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
        "status": "executed_ok",
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json",
          "markdown_report": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md"
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
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md"
        ],
        "started_at": "2026-05-07T18:07:08",
        "finished_at": "2026-05-07T18:07:09",
        "elapsed_seconds": 1.022,
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\post_patchable_doc_python_probe_20260507-180555\\\\round_000\\\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\post_patchable_doc_python_probe_20260507-180555\\\\round_000\\\\orchestrator_bootstrap_tool_inventory_agent_agnostic_tool_inventory.md\",\n  \"tool_count\": 621,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
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
        "status": "executed_ok",
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "markdown_report": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
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
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\post_patchable_doc_python_probe_20260507-180555\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        ],
        "started_at": "2026-05-07T18:07:09",
        "finished_at": "2026-05-07T18:07:09",
        "elapsed_seconds": 0.141,
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\post_patchable_doc_python_probe_20260507-180555\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\post_patchable_doc_python_probe_20260507-180555\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md\",\n  \"record_count\": 101,\n  \"memory_db_exists\": true,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
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
        "status": "executed_ok",
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.json",
          "markdown_report": "output/ai_runtime_tools/post_patchable_doc_python_probe_20260507-180555/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.md"
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
            "operational_memory_clear_per
```

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `4204`
- SHA-256: `4df07932069fac17a94560cd6d7154341bfcfb4768cdf81cf0d17d3830a6e45a`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `81.698`
- `gpu0_peer_support_count`: `5`
- `gpu0_peer_support_success_count`: `5`
- `gpu0_peer_support_overlap_count`: `5`
- `gpu0_peer_support_provider_execution_performed`: `True`
- `npu_micro_support_count`: `2`
- `npu_micro_support_success_count`: `2`
- `npu_micro_support_overlap_count`: `2`
- `npu_micro_support_provider_execution_performed`: `False`
- `npu_micro_support_tool_request_count`: `8`
- `npu_micro_runtime_tool_execution_count`: `11`
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
- `runtime_tool_request_count`: `34`
- `runtime_tool_execution_count`: `18`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `18`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `provider_mesh_mode`: `startup_barrier_parallel_peer_support`
- `all_lanes_ready_at_start`: `True`
- `gpu0_peer_support_started_with_gpu1`: `True`
- `npu_micro_support_started_with_gpu1`: `True`
- `npu_auditor_mode`: `legacy_disabled`
- `npu_audit_success_count`: `0`
- `npu_micro_support_success_count`: `2`
- `npu_micro_support_provider_success_count`: `0`
- `npu_micro_support_tool_success_count`: `2`
- `npu_micro_support_tool_request_count`: `8`
- `npu_micro_live_tool_seed_count`: `1`
- `npu_micro_runtime_tool_execution_count`: `11`
- `npu_micro_runtime_tool_live_execution_count`: `7`
- `npu_micro_support_tool_lane_performed`: `True`
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
- `runtime_tool_provider_request_count`: `11`
- `runtime_tool_provider_request_execution_count`: `11`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `18`
- `runtime_tool_result_count`: `18`
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
- round `4` status=`finished` provider=`True` overlap=`True`

## NPU Micro Support
- round `0` status=`finished` class=`provider_empty_response` provider=`False` overlap=`True` tools=`4`
- round `1` status=`finished` class=`provider_empty_response` provider=`False` overlap=`True` tools=`4`

```

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `28401`
- SHA-256: `60894d733f54632fa1df3ccbb56a965c1f1a4dc5532217c428efbc2ef9bc4e51`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-07T18:08:22",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 10,
  "elapsed_seconds": 69.994,
  "context_file_count": 20,
  "round_count": 4,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 31.24,
      "file_count": 6,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/_ia_carmine_md_split_manifest.json",
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-001.md",
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-002.md",
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN/README.md",
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md"
      ],
      "live_context_report_count": 1,
      "live_context_refresh_performed": true,
      "response_chars": 2518,
      "raw_response_preview": "{\n  \"response\": \"I have reviewed the provided document structure and content. Here are some key points and observations:\\n\\n1. **Document Structure**: The documents are organized into multiple parts, with an index file (`README.md`) that links to individual sections. This is useful for maintaining navigability, especially in longer documents.\\n\\n2. **Content Overview**:\\n   - `AGENT_REVIEW_CODE_PATCH_PLAN.md` and its parts (`part-001.md`, `part-002.md`) discuss the process of reviewing code patches generated by AI tools. It outlines steps for validation, review, and potential implementation.\\n   - `AI_ARTIFACT_SCHEMAS.md` provides guidelines on the schema requirements for various AI artifacts produced in a pipeline. This includes required keys, producers, validators, and missing checks.\\n\\n3. **Key Sections**:\\n   - **AGENT_REVIEW_CODE_PATCH_PLAN**: Focuses on the review process of code patches generated by AI tools. It emphasizes manual review and adherence to specific guidelines to ensure quality and safety.\\n   - **AI_ARTIFACT_SCHEMAS**: Details the schema requirements for different AI artifacts, ensuring consistency and compatibility across the pipeline.\\n\\n4. **Schema Requirements**:\\n   - The `AI_ARTIFACT_SCHEMAS.md` document lists required keys for various artifacts such as `track_summary.json`, `music_segments.json`, etc., along with producers, validators, and missing checks.\\n   - It also mentions related report contracts and their typical producers, validators, and required fields.\\n\\n5. **Validation and Compliance**:\\n   - Both documents emphasize the importance of validation and compliance with specific schemas and contracts to ensure that AI-generated artifacts are accurate, reliable, and safe for use.\\n\\n6. **Implementation Sequence**:\\n   - The `AGENT_REVIEW_CODE_PATCH_PLAN` document provides a recommended sequence for implementing code patch reviews, from running drift reports to building documentation follow-ups and reviewing queues together.\\n\\n7. **Navigation and References**:\\n   - Each part of the documents includes references back to the main index (`README.md`) and other relevant sections, ensuring that users can easily navigate through the content.\\n\\nOverall, these documents provide a comprehensive guide for managing AI-generated code patches and artifacts, emphasizing validation, review, and compliance with specific schemas and contracts. This ensures that the tools and processes are robust, reliable, and safe for use in production environments.\"\n}",
      "parsed_response": {
        "response": "I have reviewed the provided document structure and content. Here are some key points and observations:\n\n1. **Document Structure**: The documents are organized into multiple parts, with an index file (`README.md`) that links to individual sections. This is useful for maintaining navigability, especially in longer documents.\n\n2. **Content Overview**:\n   - `AGENT_REVIEW_CODE_PATCH_PLAN.md` and its parts (`part-001.md`, `part-002.md`) discuss the process of reviewing code patches generated by AI tools. It outlines steps for validation, review, and potential implementation.\n   - `AI_ARTIFACT_SCHEMAS.md` provides guidelines on the schema requirements for various AI artifacts produced in a pipeline. This includes required keys, producers, validators, and missing checks.\n\n3. **Key Sections**:\n   - **AGENT_REVIEW_CODE_PATCH_PLAN**: Focuses on the review process of code patches generated by AI tools. It emphasizes manual review and adherence to specific guidelines to ensure quality and safety.\n   - **AI_ARTIFACT_SCHEMAS**: Details the schema requirements for different AI artifacts, ensuring consistency and compatibility across the pipeline.\n\n4. **Schema Requirements**:\n   - The `AI_ARTIFACT_SCHEMAS.md` document lists required keys for various artifacts such as `track_summary.json`, `music_segments.json`, etc., along with producers, validators, and missing checks.\n   - It also mentions related report contracts and their typical producers, validators, and required fields.\n\n5. **Validation and Compliance**:\n   - Both documents emphasize the importance of validation and compliance with specific schemas and contracts to ensure that AI-generated artifacts are accurate, reliable, and safe for use.\n\n6. **Implementation Sequence**:\n   - The `AGENT_REVIEW_CODE_PATCH_PLAN` document provides a recommended sequence for implementing code patch reviews, from running drift reports to building documentation follow-ups and reviewing queues together.\n\n7. **Navigation and References**:\n   - Each part of the documents includes references back to the main index (`README.md`) and other relevant sections, ensuring that users can easily navigate through the content.\n\nOverall, these documents provide a comprehensive guide for managing AI-generated code patches and artifacts, emphasizing validation, review, and compliance with specific schemas and contracts. This ensures that the tools and processes are robust, reliable, and safe for use in production environments.",
        "recommendations": [],
        "missing_evidence": [],
        "next_best_action": ""
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
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        },
        "source": "provider_tool_requests",
        "provider_generated_tool_requests": true
      },
      "provider_tool_request_count": 4,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "missing top-level keys: recommendations"
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
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "a96ee8cbce42f15f3b2ebac1290659610016cc75790ec8ef877196d8c23f7dd3",
        "raw_response_chars": 2518,
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
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "model_output_schema_mismatch",
      "evidence_ready_for_manual_patch_count": 0,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 11.771,
      "file_count": 6,
      "files": [
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md"
      ],
      "live_context_report_count": 1,
      "live_context_refresh_performed": true,
      "response_chars": 70,
      "raw_response_preview": "{\n    \"response\": \"I'm sorry, but I can't assist with that request.\"\n}",
      "parsed_response": {
        "response": "I'm sorry, but I can't assist with that request.",
        "recommendations": [],
        "missing_evidence": [],
        "next_best_action": ""
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
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        },
        "source": "provider_tool_requests",
        "provider_generated_tool_requests": true
      },
      "provider_tool_request_count": 4,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "missing top-level keys: recommendations"
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
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "model_output_schema_mismatch",
      "evidence_ready_for_manual_patch_count": 0,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 3,
      "elapsed_seconds": 12.928,
      "file_count": 6,
      "files": [
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md",
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md"
      ],
      "live_context_report_count": 1,
      "live_context_refresh_performed": true,
      "response_chars": 70,
      "raw_response_preview": "{\n    \"response\": \"I'm sorry, but I can't assist with that request.\"\n}",
      "parsed_response": {
        "response": "I'm sorry, but I can't assist with that request.",
        "recommendations": [],
        "missing_evidence": [],
        "next_best_action": ""
      },
      "schema_repair_retry": {
        "attempted": true,
        "accepted": false,
        "reason": "schema_repair_retry_rejected",
        "json_ok": true,
        "schema_ok": false,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,

```

### `output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1049`
- SHA-256: `df33d406dcbc63e8a87485cfd0b029f1d2d7c9118c1912e1c0a127d5e8f76fb6`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `69.994`
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

### `output/ai_pipeline/gpu0_peer_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_gpu0_peer_support.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1732`
- SHA-256: `6788021accdc9166b7a6a4c4ac01db627f986c6d891acb151b8571b92cabae38`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 2,
  "kind": "openvino_gpu0_secondary_workload",
  "generated_at": "2026-05-07T18:07:12",
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
  "openvino_gpu0_sustained_iterations_performed": 7042,
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
  "elapsed_seconds": 2.142612,
  "compile_seconds": 0.04104,
  "inference_seconds": 1.000094,
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

### `output/ai_pipeline/gpu0_peer_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_gpu0_peer_support.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1009`
- SHA-256: `ba4b18b29dfcb06d43e84d9b007f608cd11a5abf6d843cedb7d7a22bb702ad6d`
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
- GPU.0 iterations performed: `7042`
- GPU.0 min seconds requested: `1.0`
- GPU.1 reserved visible: `True`
- GPU.1 workload performed: `False`
- Selected device: `GPU.0`
- Available devices: `['CPU', 'GPU.0', 'GPU.1', 'NPU']`
- Elapsed seconds: `2.142612`
- Compile seconds: `0.04104`
- Inference seconds: `1.000094`

## Output preview

[1.0, 1.0, 1.0, 1.0]

## Errors
- none

## Warnings
- OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.

```

### `output/ai_pipeline/npu_micro_support_parallel_post_patchable_doc_python_probe_20260507-180555/round_000_npu_micro_support.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1187`
- SHA-256: `d1c052cba32660229ed870b94182b661147dfb3939a9286aaddd6fc7cdfca93b`
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
- TimeoutExpired: 30s
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

### `output/ai_runtime_memory/patch_plan_quality_product_post_patchable_doc_python_probe_20260507-180555.sqlite`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.sqlite`
- Size bytes: `1732608`
- SHA-256: `4e264ab7ea84a6e54c0b46b926b0f7e2ad1c1b212aefe39a12d193dae0f7bf36`
- Content included: `False`
- Content truncated: `False`
- Skip reason: `suffix_not_text_allowlisted`

### `output/analysis/code_interpreter_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7102`
- SHA-256: `ca6213d2a6418bc20b85bc5d5a1f8346d448de433063f291d6758547749d2b27`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `612`
- Parsed files: `612`
- Total lines: `103965`
- Total functions: `3740`
- Total classes: `102`
- Risk signals: `90`
- TODO/FIXME markers: `21`
- Recommendation count: `190`
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
- `Tools/ai/build_deterministic_recommendations.py` - `1015` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` - `902` lines, risk `high`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` - `836` lines, risk `high`
- `Tools/ai/agent_runtime_tool_broker.py` - `751` lines, risk `medium`
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
- `code_static_024` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
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

### `output/analysis/gpu_json_contract_replay_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

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

### `output/analysis/gpu_npu_run_sync_full_toolbox_post_patchable_doc_python_probe_20260507-180555.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5297`
- SHA-256: `f0be2d5c902f598d21056434cc00167323b6f6642720b92a779ef1d3f62ed595`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-07T18:08:30",
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
    "orchestrator": "output/ai_pipeline/full_toolbox_post_patchable_doc_python_probe_20260507-180555_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 4,
    "npu_audit_count": 2,
    "legacy_npu_audit_count": 0,
    "npu_micro_support_count": 2,
    "npu_micro_support_overlap_count": 2,
    "gpu0_peer_support_count": 5,
    "gpu0_peer_support_overlap_count": 5,
    "npu_audit_success_count": 2,
    "npu_audit_round_coverage": 0.5,
    "avg_gpu_round_seconds": 20.424,
    "p50_gpu_round_seconds": 20.424,
    "p90_gpu_round_seconds": 20.424,
    "avg_npu_audit_seconds": 34.0,
    "p50_npu_audit_seconds": 34.0,
    "p90_npu_audit_seconds": 34.0,
    "npu_to_gpu_avg_duration_ratio": 1.665,
    "gpu_elapsed_seconds": 81.698,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.001,
    "gpu": {
      "elapsed_seconds": 81.698,
      "round_count": 4,
      "round_duration_source": "gpu_elapsed_divided_by_round_count",
      "round_duration_sample_count": 1,
      "avg_round_seconds": 20.424,
      "p50_round_seconds": 20.424,
      "p90_round_seconds": 20.424,
      "max_round_seconds": 20.424,
      "round_durations_total_seconds": 20.424,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 34,
        "runtime_tool_execution_count": 18,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 16,
        "runtime_tool_provider_request_execution_count": 11,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0
      },
      "embedded_performance": {}
    },
    "npu": {
      "audit_count": 2,
      "audit_requested_count": 2,
      "audit_success_count": 2,
      "duration_sample_count": 2,
      "avg_audit_seconds": 34.0,
      "p50_audit_seconds": 34.0,
      "p90_audit_seconds": 34.0,
      "max_audit_seconds": 34.0,
      "audit_durations_total_seconds": 68.0,
      "status_counts": {
        "finished": 2
      },
      "classification_counts": {
        "provider_empty_response": 2
      },
      "lane_diagnostics": {}
    },
    "sync": {
      "npu_to_gpu_avg_duration_ratio": 1.665,
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
    "npu_too_slow_for_per_round_lockstep": true,
    "recommended_next_layer": "feed timing-backed GPU/NPU suggestions into decision-loop patch planning",
    "manual_review_required": true
  }
}

```

### `output/analysis/gpu_npu_run_sync_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2337`
- SHA-256: `6611c2f678e3125517f5e24ba41202a7d7f5b9a1217bbd12db5bcd00b720aa15`
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
- `npu_audit_count`: `2`
- `legacy_npu_audit_count`: `0`
- `npu_micro_support_count`: `2`
- `npu_micro_support_overlap_count`: `2`
- `gpu0_peer_support_count`: `5`
- `gpu0_peer_support_overlap_count`: `5`
- `npu_audit_success_count`: `2`
- `npu_audit_round_coverage`: `0.5`
- `avg_gpu_round_seconds`: `20.424`
- `p50_gpu_round_seconds`: `20.424`
- `p90_gpu_round_seconds`: `20.424`
- `avg_npu_audit_seconds`: `34.0`
- `p50_npu_audit_seconds`: `34.0`
- `p90_npu_audit_seconds`: `34.0`
- `npu_to_gpu_avg_duration_ratio`: `1.665`
- `gpu_elapsed_seconds`: `81.698`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `81.698`
- GPU average round seconds: `20.424`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- GPU timing sample count: `1`
- GPU round durations total seconds: `20.424`
- NPU average audit seconds: `34.0`
- NPU duration sample count: `2`

## Operational opinions

- GPU/NPU cadence is measurable; tune audit frequency from timing evidence rather than intuition.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count

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

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_post_patchable_doc_python_probe_20260507-180555.md`

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
