# Local Validation Evidence Bundle

- Generated at: `2026-05-06T00:51:19`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `True`
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

### `output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_integrated.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_full_toolbox_decision_loop_integrated`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Recommendation count: `20`

### `output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_full_toolbox_decision_loop_workflow`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Recommendation count: `20`

### `output/validation/agent_review_warning_policy_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_warning_policy`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Recommendation count: `20`

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
- Usable lanes: `['npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu']`
- Unusable lanes: `[]`
- Warnings: `['ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/validation/ai_workload_quality_lane_routing.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_workload_quality_lane_routing`
- Passed: `True`
- Provider execution performed: `False`
- Primary advisory provider: `{'provider': None, 'compute_lane': None, 'role': 'none', 'execution_mode': 'unavailable_no_usable_lane', 'enabled_by_flag': None, 'provider_execution_performed': False}`
- Routing: `{'advisory_lanes': ['npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu'], 'excluded_advisory_lanes': [], 'primary_advisory_provider': {'provider': None, 'compute_lane': None, 'role': 'none', 'execution_mode': 'unavailable_no_usable_lane', 'enabled_by_flag': None, 'provider_execution_performed': False}, 'trusted_context_files': [{'path': 'output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'indexAI/code_chunks/semantic_code_chunks_manifest.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_20260506-004242.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_context_pack_20260506-004242.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}], 'excluded_context_files': [{'path': 'output/ai_packets/20260506-004242/npu_real_workload_report.md', 'lane': 'npu', 'trusted': False, 'reason': 'usable_text', 'classification': 'usable_text'}]}`

### `output/validation/npu_decode_quality_remediation.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_decode_quality_remediation`
- Passed: `True`
- Provider execution performed: `False`

### `output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.json`

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

### `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json`

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

### `output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `20`

### `output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `collect_more_evidence`

### `output/analysis/repository_consistency_map_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `162`

### `output/validation/python_line_count_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_toolbox_run_telemetry_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_usage_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_capability_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `semantic_evidence_chunk_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `True`
- Ollama: `{'used': None, 'model': 'gpt-oss:20b', 'error': None, 'text_preview': ''}`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_final_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `True`
- Patch plan count: `20`
- Errors: `['ollama: probe failed']`
- Warnings: `['ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/validation/docs_links_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `docs_links`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_20260506-004242_memory_routing_policy.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_memory_routing_policy_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_operational_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_persistent_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_python_line_count.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_python_syntax.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_20260506-004242_runtime_tool_broker.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_runtime_tool_broker_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260506-004242_validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_20260506-004242_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_toolbox_agent_review_decision_loop_20260506-004242_bundle_validation.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `github_evidence_bundle_validation`
- Passed: `True`

### `output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `markdown_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['This inventory is evidence for review. It does not delete or rewrite Markdown files.', 'A missing index reference is not automatically obsolete; it means the file needs owner/lifecycle review.', 'GitHub templates and root community docs are repository controls, not prune candidates.']`

### `output/validation/python_syntax_full_toolbox_final_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/runtime_tool_bootstrap_requests_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_bootstrap_requests`
- Passed: `None`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/runtime_tool_broker_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `script_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/shared_toolbox_ai_to_ai_bundle_20260506-004242_validation.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `github_evidence_bundle_validation`
- Passed: `True`

### `output/validation/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242_patch_spec_drafts.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `proposal_patch_spec_draft_contract`
- Passed: `True`

### `output/validation/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242_repository_change_proposals_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposal_contract`
- Passed: `True`

### `output/validation/validation_report_contract_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/validation_report_contract_full_toolbox_final_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/validation_report_contract_full_toolbox_integrated_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/validation_report_contract_json_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/analysis/full_memory_tool_regeneration_20260506-004242_code_interpreter.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `143`

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agent_memory_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agnostic_tool_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_agnostic_tool_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_transient_request_context.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_transient_request_context`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_ollama_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': True, 'model': 'gpt-oss:20b', 'error': '', 'text_preview': '**Next Safe Milestone**  \n- **2026‑05‑01_evidence_schema_contracts.md** – review and finalize evidence schema contracts before any new runtime or provider changes.\n\n**Files to Inspect**  \n| File | Reason |\n|------|--------|\n| `output/ai_packets/20260506-004242/npu_real_workload_report.md` | Excluded from context – must be removed or replaced with a quality‑approved file. |\n| `output/validation/local_provider_probe.json` | Fails (`ollama: probe failed`). |\n| `output/validation/python_syntax.json`'}`

### `output/ai_pipeline/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_ollama_20260506-004242_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet_manifest`
- Passed: `None`

### `output/ai_pipeline/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_ollama_proposals_20260506-004242.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

## Patch plan summary

### `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json`

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
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_006 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_007 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_008 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_009 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_010 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_011 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_032 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_033 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_034 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_035 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_036 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_037 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_038 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_039 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md:13` targeting `powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./Tools/workflow
un_full0to10_manifest_contract_gate.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md:13`. Target `docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md` and resolve `powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./Tools/workflow
un_full0to10_manifest_contract_gate.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_040 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md:15` targeting `un_full0to10_manifest_contract_gate.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md:15`. Target `docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md` and resolve `un_full0to10_manifest_contract_gate.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_integrated.json` exists=`True` size=`28255` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json` exists=`True` size=`33345` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_warning_policy_20260506-004242.json` exists=`True` size=`2910` suffix=`.json` preview_chars=`1500`
- `output/validation/local_provider_probe.json` exists=`True` size=`2528` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_workload_report_quality.json` exists=`True` size=`39506` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_workload_quality_lane_routing.json` exists=`True` size=`7200` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_decode_quality_remediation.json` exists=`True` size=`2400` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.json` exists=`True` size=`2867` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json` exists=`True` size=`246253` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json` exists=`True` size=`176530` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json` exists=`True` size=`5266` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json` exists=`True` size=`14590` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.json` exists=`True` size=`27388` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_20260506-004242.json` exists=`True` size=`7416683` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.json` exists=`True` size=`1198` suffix=`.json` preview_chars=`1159`
- `output/analysis/code_interpreter_full_toolbox_20260506-004242.json` exists=`True` size=`1912750` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_20260506-004242.json` exists=`True` size=`3160` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_20260506-004242.json` exists=`True` size=`70046` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260506-004242.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260506-004242.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260506-004242.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_20260506-004242.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.json` exists=`True` size=`24408` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.json` exists=`True` size=`9882` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.json` exists=`True` size=`13988` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.json` exists=`True` size=`237529` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260506-004242.json` exists=`True` size=`1230568` suffix=`.json` preview_chars=`1500`
- `output/validation/docs_links_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json` exists=`True` size=`200035` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_memory_routing_policy.json` exists=`True` size=`8925` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_memory_routing_policy_smoke.json` exists=`True` size=`2972` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_operational_memory_status.json` exists=`True` size=`1703` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_persistent_memory_status.json` exists=`True` size=`1779` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_python_line_count.json` exists=`True` size=`3190` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_python_syntax.json` exists=`True` size=`70046` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_runtime_tool_broker.json` exists=`True` size=`95381` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_runtime_tool_broker_smoke.json` exists=`True` size=`2001` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_validation_report_contract.json` exists=`True` size=`3417` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260506-004242_workflow.json` exists=`True` size=`4921` suffix=`.json` preview_chars=`1500`
- `output/validation/full_toolbox_agent_review_decision_loop_20260506-004242_bundle_validation.json` exists=`True` size=`13636` suffix=`.json` preview_chars=`1500`
- `output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json` exists=`True` size=`476871` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_final_20260506-004242.json` exists=`True` size=`70046` suffix=`.json` preview_chars=`1500`
- `output/validation/runtime_tool_bootstrap_requests_20260506-004242.json` exists=`True` size=`2022` suffix=`.json` preview_chars=`1500`
- `output/validation/runtime_tool_broker_full_toolbox_20260506-004242.json` exists=`True` size=`26864` suffix=`.json` preview_chars=`1500`
- `output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json` exists=`True` size=`530746` suffix=`.json` preview_chars=`1500`
- `output/validation/shared_toolbox_ai_to_ai_bundle_20260506-004242_validation.json` exists=`True` size=`38929` suffix=`.json` preview_chars=`1500`
- `output/validation/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242_patch_spec_drafts.json` exists=`True` size=`2561` suffix=`.json` preview_chars=`1500`
- `output/validation/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242_repository_change_proposals_contract.json` exists=`True` size=`2483` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json` exists=`True` size=`2024` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_full_toolbox_final_20260506-004242.json` exists=`True` size=`1724` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_full_toolbox_integrated_20260506-004242.json` exists=`True` size=`1179` suffix=`.json` preview_chars=`1132`
- `output/validation/validation_report_contract_json_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260506-004242.json` exists=`True` size=`1303` suffix=`.json` preview_chars=`1256`
- `output/analysis/full_memory_tool_regeneration_20260506-004242_code_interpreter.json` exists=`True` size=`1730407` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_20260506-004242.json` exists=`True` size=`5660` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_20260506-004242.json` exists=`True` size=`5633` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agent_memory_inventory.json` exists=`True` size=`13528` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agnostic_tool_inventory.json` exists=`True` size=`823758` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_transient_request_context.json` exists=`True` size=`9186` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_ollama_20260506-004242.json` exists=`True` size=`216205` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_ollama_20260506-004242_manifest.json` exists=`True` size=`14503` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/unified_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_ollama_proposals_20260506-004242.json` exists=`True` size=`7235` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6539`
- SHA-256: `ec901354a7b372ba9effc21a683a6f5b82a4a664f8ebc275ee55312572227980`
- Content included: `True`
- Content truncated: `False`

```text
# IA-Carmine task — Full0To10 quick productization suggestions

## Repository

```text
C-F-tek/blender-audio-project
```

## Runtime base

```text
Branch locale consigliata: master aggiornato oppure branch di lavoro derivata da master
Entry point: Tools/workflow/run_unified_local_ai_refactor.ps1
```

## Stato corrente

PR #187 è stata mergiata su `master`.

Il launcher unico è l'entrypoint canonico per IA-Carmine local AI:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

La dottrina attiva resta:

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensità, non perimetro
```

La lane evidence-only `LightFull0To10` è validata come superficie compatta, ma questa task serve a una run Full0To10 quick reale per produrre suggestioni sulla qualità/prodotto della repo.

## Obiettivo immediato

Eseguire una singola run Full0To10 quick, circa 5 minuti, per generare:

```text
diagnostica
evidenze compatte
deterministic recommendations
patch plan review-only
provider/report telemetry quando disponibile
suggestioni di productization sulla repo
```

La run deve rimanere report/proposal-only.

## Non obiettivo

Non applicare patch automaticamente.

Non eseguire azioni distruttive.

Non fare commit, push, merge, deploy o modifiche a secret/permission/billing/visibility dalla run.

Non eseguire Blender runtime.

Non eseguire FFmpeg runtime.

Non committare output runtime.

## Guardrail obbligatori

```text
patch_application_performed=false
source_writes_performed=false salvo tool documentati come generatori di report/evidence
provider execution solo come advisory/report-bound
SQLite DB locale/private runtime state
output/** non committabile
docs/LOCAL_VALIDATION_EVIDENCE/** non committabile salvo selezione manuale esplicita
indexAI/code_chunks/** non committabile
indexAI/project_code_chunks/** non committabile
*.db / *.sqlite / *.sqlite3 non committabili
*.zip non committabile
renders/** non committabile
```

## Nota launcher teardown

È stato osservato che il launcher può restare appeso dopo:

```text
[OK] Unified local-AI launcher complete
```

quando transcript/execution-tail evidence è attivo.

Workaround obbligatorio per questa task:

```text
-Prod
-NoExecutionTail
```

Questi flag non riducono il perimetro Full0To10; disabilitano solo transcript/debug tail per evitare blocchi di teardown.

## Comando operativo consigliato

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$TaskFile = ".\docs\LOCAL_AI_TASKS\full-run-unica-tutto-su-tutto-patch-plan-task.md"

$OutputDir = ".\output"
$EvidenceDir = ".\docs\LOCAL_VALIDATION_EVIDENCE"
$AiPacketsRoot = Join-Path $OutputDir "ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $Stamp

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode all `
  -Full0To10 `
  -SkipGitSync `
  -NoBranch `
  -Stamp $Stamp `
  -TaskFile $TaskFile `
  -OutputDir $OutputDir `
  -EvidenceDir $EvidenceDir `
  -AiPacketsRoot $AiPacketsRoot `
  -AiPacketsDir $AiPacketsDir `
  -Profile core `
  -RunIntensity quick `
  -BudgetMinutes 5 `
  -MaxRounds 4 `
  -FilesPerRound 4 `
  -MaxContextFiles 80 `
  -MaxCharsPerFile 4000 `
  -MaxNewTokens 1600 `
  -KeepAlive 8m `
  -NpuAuditorEveryRounds 3 `
  -NpuAuditorTimeoutSeconds 180 `
  -NpuMaxContextChars 4000 `
  -NpuMaxPromptChars 800 `
  -NpuMaxNewTokens 256 `
  -NpuFinalWaitSeconds 90 `
  -MinRecommendations 1 `
  -MinPatchPlans 1 `
  -MaxRecommendations 8 `
  -MaxPatchPlans 8 `
  -RepositoryConsistencyMapWorkers 8 `
  -ContextPackMaxTotalChars 64000 `
  -ContextPackMaxFileChars 4000 `
  -AgentStateMaxMemoryChars 24000 `
  -MatrixWorkers 8 `
  -RepeatCases 1 `
  -Prod `
  -NoExecutionTail `
  -AllowDirty
```

## Interpretazione delle leve estese

Un profilo con molte voci e valori alti, per esempio:

```text
-RunIntensity custom
-BudgetMinutes 30
-MaxRounds 300
-MaxContextFiles 620
-MaxRecommendations 220
-MaxPatchPlans 220
```

è un inventario/mega profilo, non la run quick richiesta in questa task.

Per questa task usare il profilo quick sopra.

## Criteri di successo

La run è valida se il launcher ritorna al prompt e il manifest mostra:

```text
full_0_to_10_requested=true
provider_execution_requested=true
patch_specs_requested=true
patch_application_performed=false
errors vuoto oppure solo errori esplicitamente degradati/diagnosticati
```

Il log finale deve includere:

```text
[OK] Unified local-AI launcher complete
[OK] Manifest: ...
[OK] Patch application performed: False
```

## Controlli post-run

```powershell
$latest = Get-ChildItem .\output\local_ai_runs -Directory |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

$manifest = Join-Path $latest.FullName "pipeline\unified_local_ai_refactor_manifest.json"

Get-Content $manifest -Raw |
  ConvertFrom-Json |
  Select-Object `
    kind, `
    mode_name, `
    full_0_to_10_requested, `
    provider_execution_requested, `
    patch_specs_requested, `
    patch_application_performed, `
    errors, `
    warnings

git status --short
```

## Output da ispezionare dopo la run

Aprire prima il manifest:

```text
output/local_ai_runs/<stamp>_*_unified/pipeline/unified_local_ai_refactor_manifest.json
```

Poi controllare report e suggerimenti generati, preferendo superfici compatte:

```text
phase_status
phase_reports
runtime telemetry/capability reports quando presenti
recommendations
patch plan JSON/MD
compact evidence summaries
```

Non usare file existence come prova di esecuzione: verificare campi `passed`, `provider_execution_performed`, `patch_application_performed`, `errors`, `warnings`.

## Target delle suggestioni richieste

La run deve produrre suggerimenti orientati a prodotto finale del tool attuale:

```text
stabilità launcher
teardown/transcript handling
external controls ancora mancanti
manifest e quality package
release/readiness contract
documentazione stale post-merge
riduzione attrito operativo
validator smoke/acceptance
```

## Follow-up attesi dopo lettura report

Classificare ogni raccomandazione come:

```text
SAFE_MECHANICAL
MANUAL_REVIEW
LOCAL_VALIDATION_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

Priorità suggerita:

```text
P1 fix launcher DryRun/teardown tail
P1 external controls del launcher
P2 product acceptance smoke
P2 release readiness package
P3 cleanup documentazione stale
```

## Git policy

Dopo la run non fare `git add .`.

Non committare runtime output.

Se servono evidenze compatte, selezionarle manualmente e solo dopo review.

```

### `docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6484`
- SHA-256: `da90623dc168a694fe44d738a5cdf652d2cdd9e894663d475fe461e03af25f30`
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
- launching NPU audits;
- collecting checkpoint reports;
- collecting GPU and NPU `tool_requests`;
- scheduling report-only tool execution;
- passing requests to the broker;
- reinjecting broker reports into later context;
- preserving non-blocking behavior for NPU audits;
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
- code-interpreter report inventory.

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

The NPU auditor is non-blocking and non-primary.

It may:

- read GPU checkpoints;
- read runtime toolbox context;
- classify provider states;
- produce audit reports;
- propose structured `tool_requests`.

The NPU must not execute tools directly. NPU tool requests are routed through the orchestrator and broker.

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

### `output/ai_pipeline/repository_update_suggestions.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6791`
- SHA-256: `9d46587b4cf19bcc230df1c63ae0aada2e6766f4d6f88ed238504fe58f179311`
- Content included: `True`
- Content truncated: `False`

```text
# Post-Validation AI Work Packet

- Generated at: `2026-05-06T00:46:07`
- Repo: `C:\Users\carmi\blender\blender-audio-project`
- Profile: `core`
- Ollama used: `False`
- Packet manifest: `C:\Users\carmi\blender\blender-audio-project\output\ai_pipeline\repository_update_suggestions_manifest.json`

## Advisory context routing

- Enforced: `True`
- Provider execution performed: `False`
- Advisory lanes: `npu`
- Excluded advisory lanes: `none`

## Deterministic suggestions

### P1 — Fix failing validation reports before new runtime work

- Area: `validation`
- Details: C:\Users\carmi\blender\blender-audio-project\output\validation\local_provider_probe.json: ['ollama: probe failed']

### P2 — Run or review missing validation reports before strict follow-up work

- Area: `validation`
- Details: C:\Users\carmi\blender\blender-audio-project\output\validation\python_syntax.json; C:\Users\carmi\blender\blender-audio-project\output\validation\ai_pipeline_modules.json; C:\Users\carmi\blender\blender-audio-project\output\validation\npu_pipeline_modules.json; C:\Users\carmi\blender\blender-audio-project\output\validation\npu_pipeline_helper_tests.json; C:\Users\carmi\blender\blender-audio-project\output\validation\npu_pipeline_docs.json; C:\Users\carmi\blender\blender-audio-project\output\validation\provider_result_parsing.json; C:\Users\carmi\blender\blender-audio-project\output\validation\provider_result_report.json; C:\Users\carmi\blender\blender-audio-project\output\validation\npu_runtime_output_manifest.json

### P2 — Review active execution plans before opening the next milestone

- Area: `execution_plans`
- Details: docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md; docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md; docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md; docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md; docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md; docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md; docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md

### P2 — Prefer additive observability before provider or Blender runtime changes

- Area: `agnostic_core`
- Details: Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.

## Inputs

### Trusted context files
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/AI_DOCS_ENTRYPOINT.md`
- `docs/PROJECT_STATUS_POINT.md`
- `docs/TECH_DEBT_TRACKER.md`
- `docs/REFACTORING_AND_REUSE_PLAN.md`
- `docs/JSON_SCHEMAS.md`
- `docs/AI_ARTIFACT_SCHEMAS.md`
- `Tools/npu/pipeline/README.md`
- `Tools/validation/README.md`
- `./docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md`
- `./docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md`
- `./Tools/ai/run_agent_review_decision_loop.py`
- `./Tools/ai/build_deterministic_recommendations.py`
- `./Tools/ai/build_agent_review_patch_plan.py`
- `./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`
- `./Tools/validation/run_agent_review_decision_loop_smoke.py`
- `./output/analysis/repository_consistency_map_full_toolbox_20260506-004242.md`
- `./output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.md`
- `./output/validation/python_line_count_all_python_files_20260506-004242.md`
- `./output/analysis/code_interpreter_full_toolbox_20260506-004242.md`
- `./output/analysis/gpu_json_contract_replay_full_toolbox_20260506-004242.md`
- `./output/analysis/gpu_npu_run_sync_full_toolbox_20260506-004242.md`
- `./output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.md`
- `./output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.md`

### Report files
- `output/validation/python_syntax.json`
- `output/validation/ai_pipeline_modules.json`
- `output/validation/npu_pipeline_modules.json`
- `output/validation/npu_pipeline_helper_tests.json`
- `output/validation/npu_pipeline_docs.json`
- `output/validation/provider_result_parsing.json`
- `output/validation/provider_result_report.json`
- `output/validation/ai_workload_report_quality.json`
- `output/validation/ai_workload_quality_lane_routing.json`
- `output/validation/npu_decode_quality_remediation.json`
- `output/validation/npu_decode_smoke_diagnostic.json`
- `output/validation/npu_runtime_output_manifest.json`
- `output/validation/local_ai_resource_lanes.json`
- `output/validation/local_provider_probe.json`
- `output/validation/execution_plan_status.json`
- `output/validation/validation_report_contract.json`
- `output/validation/docs_links.json`
- `./output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json`
- `./output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.json`
- `./output/analysis/repository_consistency_map_full_toolbox_20260506-004242.json`
- `./output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.json`
- `./output/analysis/code_interpreter_full_toolbox_20260506-004242.json`
- `./output/validation/python_line_count_full_toolbox_20260506-004242.json`
- `./output/validation/python_syntax_full_toolbox_20260506-004242.json`
- `./output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260506-004242.json`
- `./output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260506-004242.json`
- `./output/validation/agent_review_decision_loop_smoke_full_toolbox_20260506-004242.json`
- `./output/validation/npu_provider_environment_full_toolbox_20260506-004242.json`
- `./output/analysis/gpu_json_contract_replay_full_toolbox_20260506-004242.json`
- `./output/analysis/gpu_npu_run_sync_full_toolbox_20260506-004242.json`
- `./output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json`
- `./output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json`
- `./output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.json`
- `./output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json`
- `./output/validation/full_memory_tool_regeneration_20260506-004242_workflow.json`

## Guardrails

- Advisory only: do not auto-apply edits from this packet.
- Output/input paths are configurable; defaults are not part of the architecture boundary.
- Validate locally before committing generated indexes.
- Keep provider execution changes in a separate explicitly scoped milestone.

```

### `output/ai_pipeline/repository_change_proposals.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2344`
- SHA-256: `e172dc1118f7d4a95c07ab2b4943907b502dc14a1c92e1ab24c54315a171e9f0`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-06T00:46:07`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-NEXT-NPU-OBSERVABILITY — Add additive NPU observability before provider execution changes

- Priority: `P2`
- Area: `npu_backend`
- Change type: `observability_extension`
- Apply mode: `manual_review_only`
- Rationale: Current reports do not indicate blocking failures. The next safe app-agnostic step is deeper observability, not provider behavior changes.

### Target files
- `Tools/npu/build_runtime_output_manifest.py`
- `Tools/ai/check_local_resource_lanes.py`
- `Tools/ai/suggest_repository_updates.py`
- `docs/JSON_SCHEMAS.md`
- `Tools/validation/README.md`

### Patch sketch
- Include runtime-output manifest and resource-lane reports in the default NPU packet profile.
- Add proposal generation output next to packet JSON/Markdown.
- Keep every output advisory and generated under output/.

### Suggestion outputs
- `python_code` `Tools/npu/build_runtime_output_manifest.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/check_local_resource_lanes.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1`
- `python .\Tools\ai\check_local_resource_lanes.py --repo-root . --parallel --output .\output\validation\local_ai_resource_lanes.json --markdown-output .\output\validation\local_ai_resource_lanes.md`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_after_tests -ReportFile output/validation/local_ai_resource_lanes.json -ReportFile output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change requires modifying provider execution, prompt prose, Blender runtime or generated indexes manually.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

### `output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_integrated.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `567`
- SHA-256: `f9b874153592b65abbb063c03a401fdd6d9735dc8901bea730a93944933b527d`
- Content included: `True`
- Content truncated: `False`

```text
# Integrated Agent Review Full Toolbox Decision Loop

- Passed: `True`
- Stamp: `20260506-004242`
- Base workflow passed: `True`
- Warning policy passed: `True`
- Decision recovered: `True`
- Recommendation count: `20`
- Patch plan count: `20`
- Input-nonfatal warning count: `0`
- Fatal report failure count: `0`
- Provider execution performed: `True`
- Patch application performed: `False`
- SQLite write performed: `False`
- Persistent memory write performed: `False`

## Input-nonfatal warnings

- none

## Fatal report failures

- none

```

### `output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `22479`
- SHA-256: `3e7b512e295f9a26f7adad7880b59ce9a5ac5fe06a112d1968274bf7fb74abc4`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Full Toolbox Decision Loop Workflow

- Passed: `True`
- Stamp: `20260506-004242`
- Provider execution performed: `True`
- Patch application performed: `False`
- SQLite write performed: `False`
- Persistent memory write performed: `False`
- Recommendation count: `20`
- Patch plan count: `20`
- Max recommendations: `20`
- Max patch plans: `20`
- Provider advisory failure count: `0`
- Bundle validation passed: `True`

## Evidence to commit

- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260506-004242.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260506-004242.md`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_20260506-004242.csv`
- `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260506-004321.csv`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_20260506-004242.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_20260506-004242.md`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_20260506-004242.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_20260506-004242.md`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_20260506-004242.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_20260506-004242.md`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_20260506-004242.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_20260506-004242.md`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_capability_manifest_20260506-004242.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_capability_manifest_20260506-004242.md`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.json`
- `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0001.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0002.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0003.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0004.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0005.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0006.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0007.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0008.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0009.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0010.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0011.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0012.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0013.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0014.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0015.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0016.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0017.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0018.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0019.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0020.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0021.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0022.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0023.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0024.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0025.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0026.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0027.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0028.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0029.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0030.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0031.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0032.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0033.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0034.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0035.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0036.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0037.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0038.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0039.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0040.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0041.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0042.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0043.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0044.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0045.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0046.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0047.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0048.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0049.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0050.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0051.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0052.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0053.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0054.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0055.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0056.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0057.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0058.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0059.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0060.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0061.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0062.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0063.md`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0064.md`
- `docs/LOC
```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `380163`
- SHA-256: `d27e56d1d11b772e54789ad392636d8443b6bc80a3c914a326ad2bcd34d7c879`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: 20260506-004242
- passed: True
- provider_execution_performed: True
- patch_application_performed: False
- source_writes_performed: True
- sqlite_write_performed: False
- persistent_memory_write_performed: False
- blender_runtime_execution_performed: False

## Provider diagnostics

- Provider execution seen: `True`
- GPU primary advisory succeeded: `False`
- Provider failure detected: `True`
- Deterministic recovery used: `True`
- Provider advisory state: `recovered_degraded_provider`
- Provider failure reasons:
  - output/validation/local_provider_probe.json: ollama: probe failed
- `output/validation/local_provider_probe.json` kind=`local_provider_probe` passed=`False` provider_execution_performed=`True` errors=`['ollama: probe failed']`
- `output/validation/ai_workload_report_quality.json` kind=`ai_workload_report_quality` passed=`True` provider_execution_performed=`False` errors=`[]`
- `output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json` kind=`agent_gpu_npu_parallel_orchestrator` passed=`True` provider_execution_performed=`True` errors=`[]`

## Patch plan summary

- Seen: `True`
- Source: `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json`
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

- request_build_code_interpreter_report: build_code_interpreter_report - Build static analysis/refactor evidence.
- request_check_python_syntax: check_python_syntax - Gate Python source changes.
- request_check_validation_report_contract: check_validation_report_contract - Gate report quality before evidence bundling.

## Reports generated

- output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_integrated.json exists=True json_ok=True kind=agent_review_full_toolbox_decision_loop_integrated passed=True
- output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json exists=True json_ok=True kind=agent_review_full_toolbox_decision_loop_workflow passed=True
- output/validation/agent_review_warning_policy_20260506-004242.json exists=True json_ok=True kind=agent_review_warning_policy passed=True
- output/validation/local_provider_probe.json exists=True json_ok=True kind=local_provider_probe passed=False
- output/validation/ai_workload_report_quality.json exists=True json_ok=True kind=ai_workload_report_quality passed=True
- output/validation/ai_workload_quality_lane_routing.json exists=True json_ok=True kind=ai_workload_quality_lane_routing passed=True
- output/validation/npu_decode_quality_remediation.json exists=True json_ok=True kind=npu_decode_quality_remediation passed=True
- output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.json exists=True json_ok=True kind=agent_review_decision_loop passed=True
- output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json exists=True json_ok=True kind=agent_review_patch_plan passed=True
- output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer passed=True
- output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json exists=True json_ok=True kind=deterministic_recommendation_patch_plan_bridge_orchestrator passed=True
- output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json exists=True json_ok=True kind=agent_gpu_npu_parallel_orchestrator passed=True
- output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.json exists=True json_ok=True kind=agent_gpu_deep_planning_supervised passed=True
- output/analysis/repository_consistency_map_full_toolbox_20260506-004242.json exists=True json_ok=True kind=repository_consistency_map passed=True
- output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.json exists=True json_ok=True kind=repository_consistency_map_smoke passed=True
- output/analysis/code_interpreter_full_toolbox_20260506-004242.json exists=True json_ok=True kind=code_interpreter_report passed=True
- output/validation/python_line_count_full_toolbox_20260506-004242.json exists=True json_ok=True kind=python_line_count_csv passed=True
- output/validation/python_syntax_full_toolbox_20260506-004242.json exists=True json_ok=True kind=python_syntax passed=True
- output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260506-004242.json exists=True json_ok=True kind=gpu_planner_json_contract_smoke passed=True
- output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260506-004242.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer_smoke passed=True
- output/validation/agent_review_decision_loop_smoke_full_toolbox_20260506-004242.json exists=True json_ok=True kind=agent_review_decision_loop_smoke passed=True
- output/validation/npu_provider_environment_full_toolbox_20260506-004242.json exists=True json_ok=True kind=npu_provider_environment passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.json exists=True json_ok=True kind=full_toolbox_run_telemetry_summary passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.json exists=True json_ok=True kind=runtime_tool_usage_telemetry passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.json exists=True json_ok=True kind=runtime_tool_capability_manifest passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.json exists=True json_ok=True kind=semantic_evidence_chunk_manifest passed=True

## Remaining gaps

- output/validation/shared_toolbox_python_syntax_20260506-004242.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_20260506-004242.json: optional report missing
- output/validation/shared_toolbox_gpu_contract_smoke_20260506-004242.json: optional report missing
- output/validation/shared_toolbox_gpu_routing_20260506-004242.json: optional report missing
- output/validation/shared_toolbox_npu_execution_20260506-004242.json: optional report missing
- output/validation/shared_toolbox_npu_contract_20260506-004242.json: optional report missing
- output/validation/npu_provider_environment_shared_toolbox_20260506-004242.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260506-004242_orchestrator.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260506-004242_gpu.json: optional report missing
- output/analysis/shared_toolbox_gpu_npu_sync_20260506-004242.json: optional report missing
- output/analysis/shared_toolbox_gpu_contract_replay_20260506-004242.json: optional report missing
- docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md: optional artifact missing
- output/analysis/shared_toolbox_code_interpreter_20260506-004242.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260506-004242_orchestrator.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260506-004242_gpu.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_npu_sync_20260506-004242.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_contract_replay_20260506-004242.md: optional artifact missing
- runtime tool requests not proven in provider-backed run: No concrete tool_requests were found in the included reports.

## Recommended next task

.\docs\LOCAL_AI_TASKS\full-run-unica-tutto-su-tutto-patch-plan-task.md

## Recursive defaults

- Enabled: `True`
- Discovered reports: `51`
- Discovered artifacts: `87`

## Chunked large JSON/Markdown files

- output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json lines=227 chunks=2 chunk_size=220
  - output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json#L1-L220 -> next: output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json#L221-L227
  - output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json#L221-L227 -> next: END
- output/validation/ai_workload_report_quality.json lines=1065 chunks=5 chunk_size=220
  - output/validation/ai_workload_report_quality.json#L1-L220 -> next: output/validation/ai_workload_report_quality.json#L221-L440
  - output/validation/ai_workload_report_quality.json#L221-L440 -> next: output/validation/ai_workload_report_quality.json#L441-L660
  - output/validation/ai_workload_report_quality.json#L441-L660 -> next: output/validation/ai_workload_report_quality.json#L661-L880
  - output/validation/ai_workload_report_quality.json#L661-L880 -> next: output/validation/ai_workload_report_quality.json#L881-L1065
  - output/validation/ai_workload_report_quality.json#L881-L1065 -> next: END
- output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json lines=4896 chunks=23 chunk_size=220
  - output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json#L1-L220 -> next: output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json#L221
```

### `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `17628`
- SHA-256: `fe227f96380e4f5074727e15c63a7e1f89ed8fae40593ff19eb487648999fe32`
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

- `orchestrator`: `output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json`
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
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_032 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_033 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_034 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_035 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_036 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_037 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_pow
```

### `output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1279`
- SHA-256: `b612edcb5b034c3555104abb75741e09b54e608db5271a94dec0ea2f8729fa3b`
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

- `recommendations`: `output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json` exists=`True` size=`176530`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.md` exists=`True` size=`23606`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json` exists=`True` size=`5266`
- `patch_plan`: `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json` exists=`True` size=`246253`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.md` exists=`True` size=`17628`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `23606`
- SHA-256: `ca67118e2ee808e10aca3527c63688b67f20dfa3ff93121a7841e99533361ce8`
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
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_032 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_033 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_034 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_035 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_036 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### 
```

### `output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2319`
- SHA-256: `911d289313aa34ec1a8773526cb5fe98b605820b491a3e9af0d6ad8b7ce50c89`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `108.061`
- `npu_audit_count`: `1`
- `npu_audit_success_count`: `1`
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
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `16`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `1`
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
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_bootstrap_executed`: `False`
- `runtime_tool_bootstrap_execution_count`: `0`
- `runtime_tool_provider_request_count`: `0`
- `runtime_tool_provider_request_execution_count`: `0`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_result_count`: `0`
- `manual_review_required`: `True`
- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `slow`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `4`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1049`
- SHA-256: `6c4a286aeb3bbc5c86b96f5918194786f802c8a483ed24f9d56b7f733b50a1a9`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `83.907`
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

### `output/analysis/repository_consistency_map_full_toolbox_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `55937`
- SHA-256: `756120c413b80b0a697fcbf86dd826ab53da0e8554c42fa706b2c9231e914ee3`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `9721`
- Markdown files: `568`
- Python files: `582`
- Markdown references: `61224`
- Markdown Python commands: `835`
- Provider execution performed: `False`
- Workers requested: `8`
- Total build seconds: `51.357`
- Markdown scan seconds: `38.351`
- Python inventory seconds: `4.403`
- Patch application performed: `False`

## Severity counts

- `high`: `2500`
- `low`: `48`
- `medium`: `7173`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `48`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `7171`
- `md_mentions_missing_powershell_path`: `222`
- `md_mentions_missing_python_path`: `2247`
- `md_python_command_script_missing`: `31`

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 248 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 249 | `patches/00_check_repo_ready.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `AGENTS.md` | 105 | `text
CHATGPT.md                         # root pointer
CHATGPT/README.md                  # index and reading order
CHATGPT/next-chat-handoff-*.md     # current handoff state
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 246 | `text
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
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 47 | `Tools/ai/build_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 74 | `Tools/validation/check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 98 | `Tools/ai/agent_memory_schema.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 99 | `Tools/ai/agent_memory_tools.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 139 | `Tools/ai/simulate_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 157 | `Tools/ai/run_npu_tool_proxy.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 229 | `build_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 230 | `check_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md` | 46 | `text
Tools/ai/build_runtime_hardware_capability_manifest.py` | Correct the documentation reference or restore the missing target if it is still required. |
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
| `high` | `md_mentions_missing_python_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 29 | `run_patch_bundle.py` | Correct the documentation reference or restore th
```

### `output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `379`
- SHA-256: `51fb8f2284cebc58452b6f5ba8414ac3096f07a82a05121df44f50a0f35efeaf`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Consistency Map Smoke

- Passed: `True`
- Return code: `0`
- Mapper report reused: `True`
- Workers requested: `8`
- Elapsed seconds: `0.04`
- Finding count: `9721`
- Markdown reference count: `61224`
- Markdown Python command count: `835`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`

```

### `output/analysis/code_interpreter_full_toolbox_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7065`
- SHA-256: `1401c7d5675cee79463a04aba885cf50ebf494362054ce6e1255a99dadd5939b`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `533`
- Parsed files: `533`
- Total lines: `90862`
- Total functions: `3294`
- Total classes: `97`
- Risk signals: `84`
- TODO/FIXME markers: `21`
- Recommendation count: `162`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1129` lines, risk `high`
- `Scripting/v61b/animation.py` — `1079` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` — `909` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `850` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` — `675` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`

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
- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module
- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_034` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_038` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: large functions detected
- `code_static_039` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_040` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/validation/python_line_count_full_toolbox_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1760`
- SHA-256: `57070d0ae904e9af42e78fe5462ce30abc5688424bf2799e1eb93d8bb8b62bc7`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260506-004321.csv`
- File count: `582`
- Total lines: `108393`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest Python files

- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines
- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines
- `old script legacy/spaziotempo_asset_visual_v61.py` — `1513` lines
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines
- `Tools/workflow/workflow_state.py` — `1230` lines
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines
- `old script legacy/spaziotempo_asset_visual_v6.py` — `1174` lines
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1129` lines
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines
- `Scripting/v61b/animation.py` — `1079` lines
- `Scripting/v61b_backgood/animation.py` — `1019` lines
- `old script legacy/spaziotempo_album_visual_v5.py` — `969` lines
- `Tools/ai/build_deterministic_recommendations.py` — `909` lines
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `850` lines
- `Tools/workflow/gui/workflow_gui.py` — `738` lines
- `Scripting/v61b/physics_setup.py` — `737` lines
- `Scripting/v61b/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/asset_setup.py` — `725` lines
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines

## Guardrail

This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.

```

### `output/validation/python_line_count_all_python_files_20260506-004242.md`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `34774`
- SHA-256: `6730557ca41d40cc142d1c019d772475c688e880076bff51dbf65e93f07b5f64`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: 20260506-004242
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260506-004321.csv
- File count: 582
- Total Python lines: 108393
- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.

| Lines | File |
|---:|---|
| 2197 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` |
| 1774 | `Tools/npu/run_dual_ai_pipeline.py` |
| 1513 | `old script legacy/spaziotempo_asset_visual_v61.py` |
| 1262 | `Scripting/v61b/scene_tuning_panel.py` |
| 1230 | `Tools/workflow/workflow_state.py` |
| 1179 | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
| 1174 | `old script legacy/spaziotempo_asset_visual_v6.py` |
| 1129 | `Tools/ai/run_agent_gpu_deep_planning_supervised.py` |
| 1097 | `Scripting/v61b_backgood/scene_tuning_panel.py` |
| 1079 | `Scripting/v61b/animation.py` |
| 1019 | `Scripting/v61b_backgood/animation.py` |
| 969 | `old script legacy/spaziotempo_album_visual_v5.py` |
| 909 | `Tools/ai/build_deterministic_recommendations.py` |
| 902 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
| 850 | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| 738 | `Tools/workflow/gui/workflow_gui.py` |
| 737 | `Scripting/v61b/physics_setup.py` |
| 725 | `Tools/ai/build_refactor_duplication_audit.py` |
| 725 | `Scripting/v61b_backgood/asset_setup.py` |
| 725 | `Scripting/v61b/asset_setup.py` |
| 720 | `Scripting/v61b_backgood/physics_setup.py` |
| 715 | `Tools/ai/agent_runtime_tool_broker.py` |
| 711 | `Tools/npu/build_music_context.py` |
| 710 | `old script legacy/spaziotempo_album_visual_v3.py` |
| 694 | `Tools/ai/run_npu_gpu_deep_review_auditor.py` |
| 687 | `Tools/ai/build_repository_consistency_map.py` |
| 675 | `Tools/ai/build_runtime_tool_usage_telemetry.py` |
| 657 | `Scripting/v61b/materials.py` |
| 631 | `Tools/npu/run_npu_review.py` |
| 627 | `Tools/validation/check_npu_pipeline_modules.py` |
| 626 | `Tools/ai/build_agent_review_patch_plan.py` |
| 618 | `Tools/ai/build_selective_execution_plan.py` |
| 608 | `Tools/ai/build_agent_review_patch_bundle.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 580 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
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
| 497 | `Tools/validation/ai_pipeline_report_contracts.py` |
| 490 | `Tools/npu/npu_guardrail_service.py` |
| 489 | `Tools/ai/refine_megalithic_review_signals.py` |
| 487 | `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| 483 | `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` |
| 479 | `Tools/docs/build_code_aware_md_coherence.py` |
| 471 | `Tools/ai/agent_memory_routing_policy.py` |
| 469 | `normalize_scene_spec.py` |
| 446 | `Tools/validation/check_reviewed_patch_specs.py` |
| 444 | `Tools/workflow/startup_check.py` |
| 443 | `Tools/repo_patch_runner/apply_repo_mods.py` |
| 442 | `Tools/ai/promote_patch_spec_draft.py` |
| 439 | `Scripting/v61b/config.py` |
| 438 | `Tools/npu/ollama_runtime.py` |
| 438 | `Tools/docs/split_large_markdown.py` |
| 437 | `Tools/validation/build_script_inventory.py` |
| 437 | `Tools/ai/build_code_interpreter_report.py` |
| 436 | `Tools/npu/build_project_ai_index.py` |
| 425 | `Tools/validation/check_ai_context_pack_contract.py` |
| 422 | `Tools/workflow/gui/components/storage_dashboard.py` |
| 419 | `Tools/workflow/scene_brief.py` |
| 414 | `Tools/ai/build_patch_specs_from_proposals.py` |
| 411 | `Tools/ai/schema_repair_context.py` |
| 408 | `Tools/ai/build_agent_agnostic_tool_inventory.py` |
| 408 | `Tools/ai/agent_review_warning_policy.py` |
| 407 | `Tools/ai/build_agent_review_evidence_sufficiency.py` |
| 402 | `Tools/npu/build_npu_code_context.py` |
| 401 | `Tools/validation/check_github_evidence_bundle.py` |
| 400 | `Tools/validation/check_patch_spec_drafts.py` |
| 399 | `Scripting/v61b/encode_ffmpeg_v61b.py` |
| 398 | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` |
| 397 | `Tools/ai/build_agent_memory_inventory.py` |
| 395 | `Scripting/v61b_backgood/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/encode_image_sequence_v61b.py` |
| 392 | `Tools/validation/check_code_contract_drift.py` |
| 392 | `Tools/ai/build_full_context_golden_proposals.py` |
| 392 | `Scripting/v61b/fog_dynamics.py` |
| 390 | `Tools/workflow/gui/components/artifact_browser.py` |
| 380 | `Tools/ai/gpu_planner_json_contract.py` |
| 376 | `Scripting/v61b_backgood/encode_image_sequence_v61b.py` |
| 369 | `Tools/npu/generated_blender_script_candidate_FristNear.py` |
| 369 | `Tools/npu/generated_blender_script_candidate.py` |
| 369 | `indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py` |
| 366 | `Tools/validation/check_repository_change_proposals.py` |
| 359 | `Tools/validation/test_npu_pipeline_helpers.py` |
| 358 | `Scripting/v61b_backgood/config.py` |
| 357 | `Tools/ai/build_local_ai_enrichment_plan.py` |
| 355 | `Tools/npu/build_ai_service_packet.py` |
| 354 | `Tools/workflow/project_awareness.py` |
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 339 | `Tools/validation/build_markdown_inventory.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 327 | `Tools/npu/build_npu_knowledge_broker_packet.py` |
| 326 | `Tools/npu/build_blender_manual_context.py` |
| 325 | `Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py` |
| 324 | `Tools/workflow/workflow_shell.py` |
| 321 | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` |
| 319 | `Tools/workflow/gui/workflow_gui_modern.py` |
| 319 | `Tools/ai/build_music_intermediates.py` |
| 317 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 315 | `Tools/ai/github_evidence_bundle_artifacts.py` |
| 314 | `Tools/ai/run_npu_decode_smoke_diagnostic.py` |
| 311 | `Tools/ai/run_agent_review_decision_loop.py` |
| 307 | `Tools/validation/run_agent_review_decision_loop_smoke.py` |
| 307 | `Tools/validation/check_full_context_golden_proposals.py` |
| 307 | `Tools/ai/agent_memory_policy.py` |
| 304 | `Tools/ai/build_analysis_input_bundle.py` |
| 301 | `Scripting/v61b/hotpatch/accent_patch.py` |
| 297 | `Tools/npu/pipeline/providers.py` |
| 294 | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` |
| 291 | `Tools/ai/select_semantic_code_chunks.py` |
| 291 | `Tools/ai/build_agent_transient_request_context.py` |
| 290 | `Tools/validation/run_gpu_planner_json_contract_smoke.py` |
| 290 | `Tools/validation/check_ai_pipeline_modules.py` |
| 289 | `Tools/ai/build_runtime_tool_capability_manifest.py` |
| 286 | `Tools/ai/build_gpu_repair_failure_recommendation.py` |
| 286 | `Scripting/v61b/hotpatch/diagnostics.py` |
| 283 | `Tools/validation/run_agent_review_patch_plan_smoke.py` |
| 280 | `Tools/validation/run_substantive_planning_smoke.py` |
| 278 | `Tools/workflow/gui/components/session_overview.py` |
| 270 | `Tools/validation/check_full_context_golden_docs_contract.py` |
| 270 | `Scripting/v61b/render_setup.py` |
| 267 | `Tools/workflow/ai_runtime_diagnostics.py` |
| 267 | `Scripting/v61b_backgood/render_setup.py` |
| 266 | `Tools/ai/build_code_patch_docs_followup.py` |
| 259 | `Tools/validation/check_docs_contract_drift.py` |
| 259 | `Tools/ai/build_megalithic_review_pr_draft.py` |
| 258 | `Tools/validation/run_refactor_duplication_audit_smoke.py` |
| 258 | `Tools/ai/build_code_patch_artifact_pack.py` |
| 257 | `analyze_wav.py` |
| 256 | `Tools/validation/run_agnostic_context_stack_smoke.py` |
| 250 | `Tools/ai/build_code_edit_proposal_from_plan.py` |
| 247 | `Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py` |
| 244 | `Tools/validation/run_agent_runtime_tool_broker_smoke.py` |
| 244 | `Tools/validation/run_agent_review_patch_bundle_builder_smoke.py` |
| 240 | `Tools/ai/review_wave_entrypoints.py` |
| 240 | `Scripting/v61b_backgood/fog_dynamics.py` |
| 238 | `Tools/validation/check_selective_execution_plan.py` |
| 238 | `Tools/npu/run_ollama_music_agent.py` |
| 237 | `Tools/validation/run_agent_review_warning_policy_smoke.py` |
| 234 | `Tools/validation/run_agent_memory_routing_policy_smoke.py` |
| 232 | `Tools/ai/smart_ai_gatekeeper.py` |
| 232 | `Tools/ai/replay_gpu_planner_json_contract.py` |
| 231 | `Tools/ai/enrich_github_evidence_bundle_code_plan.py` |
| 230 | `Tools/validation/check_ai_dry_run_matrix_outputs.py` |
| 229 | `Tools/validation/check_npu_knowledge_broker_packet.py` |
| 228 | `Tools/ai/build_github_evidence_bundle.py` |
| 222 | `Tools/validation/check_generated_artifact_path_policy.py` |
| 222 | `Tools/ai/workload_quality.py` |
| 221 | `Tools/docs/apply_md_code_coherence_refactor.py` |
| 221 | `Scripting/v61b/spaziotempo/core/registry.py` |
| 219 | `Tools/workflow/smart_ai_context.py` |
| 217 | `Tools/validation/generated_file_policy.py` |
| 217 | `Tools/ai/artifact_domain_registry.py` |
| 212 | `Tools/validation/build_python_line_count_csv.py` |
| 211 | `Tools/ai/github_evidence_bundle_reports.py` |
| 209 | `Tools/validation/run_repository_consistency_map_smoke.py` |
| 209 | `Tools/validation/check_local_ai_enrichment_plan.py` |
| 209 | `Tools/ai/github_evidence_bundle_markdown.py` |
| 208 | `Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py` |
| 207 | `Tools/validation/check_core_activation_agnostic_contract.py` |
| 206 | `Scripting/v61b_backgood/hotpatch/render_patch.py` |
| 206 | `Scripting/v61b/hotpatch/render_patch.py` |
| 205 | `Tools/ai/code_patch_plan_common.py` |
| 204 | `Tools/validation/run_agent_review_evidence_sufficiency_smoke.py` |
| 204 | `Tools/ai/patch_unified_launcher_light_full0to10.py` |
| 203 | `Tools/validation/run_code_edit_proposal_smoke.py` |
| 203 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` |
| 201 | `Tools/validation/run_agent_review_code_patch_plan_smoke.py` |
| 201 | `Tools/validation/check_validation_report_contract.py` |
| 201 | `Tools/ai/code_edit_proposal_helpers.py` |
| 200 | `Tools/ai/validate_ai_artifacts.py` |
| 200 | `Scripting/v61b/main_v61b.py` |
| 198 | `Scripting/v61b/world_setup.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 190 | `Tools/validation/run_runtime_tool_guidance_fallback_smoke.py` |
| 190 | `Tools/validation/report_utils.py` |
| 189 | `Tools/ai/check_npu_provider_environment.py` |
| 186 | `Tools/workflow/git_auto_push.py` |
| 186 | `Tools/validation/run_npu_runtime_tool_context_smoke.py` |
| 186 | `Tools/ai/build_workload_quality_lane_routing.py` |
| 185 | `Tools/validation/run_gpu_runner_provider_error_smoke.py` |
| 185 | `Tools/ai/pipeline/remediation.py` |
| 183 | `Tools/workflow/gui/components/action_panel.py` |
| 183 | `Tools/validation/run_schema_repair_retry_smoke.py` |
| 183 | `Tools/validation/check_ai_dry_run_matrix_cases.py` |
| 182 | `Tools/workflow/gui/components/live_output_panel.py` |
| 182 | `Tools/ai/run_local_provider_probe.py` |
| 181 | `Tools/workflow/gui/workflow_gui_with_push.py` |
| 181 | `Scripting/v61b_backgood/main_v61b.py` |
| 174 | `Scripting/v61b_backgood/world_setup.py` |
| 173 | `Tools/validation/check_generated_blender_script_policy.py` |
| 173 | `Tools/ai/runtime_tool_guidance.py` |
| 172 | `Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py` |
| 168 | `Tools/validation/run_schema_repair_context_smoke.py` |
| 167 | `Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py` |
| 163 | `Tools/ai/full0to10_provider_telemetry_semantic/validator.py` |
| 161 | `Tools/validation/run_npu_runtime_tool_execution_smoke.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 160 | `Tools/npu/npu_runtime.py` |
| 159 | `Tools/validation/check_npu_decode_quality_remediation.py` |
| 159 | `Tools/validation/run_provider_empty_response_diagnostics_smoke.py` |
| 159 | `Scripting/v61b/fog_filaments.py` |
| 159 | `Tools/ai/github_evidence_bundle_io.py` |
| 157 | `Tools/npu/pipeline/__init__.py` |
| 156 | `Tools/validation/run_schema_repair_retry_bootstrap_smoke.py` |
| 154 | `Tools/validation/run_runtime_tool_feedback_loop_smoke.py` |
| 152 | `Tools/validation/run_startup_check_cli_contract_smoke.py` |
| 152 | `Tools/ai/pipeline/models.py` |
| 150 | `Scripting/v61b/hotpatch/lighting_patch.py` |
| 149 | `Tools/validation/check_refactor_status_consistency.py` |
| 148 | `Tools/npu/build_runtime_output_manifest.py` |
| 147 | `Tools/validation/check_blender_shared_compat_smoke.py` |
| 147 | `Tools/npu/build_provider_result_report.py` |
| 146 | `Tools/ai/github_evidence_bundle_decisions.py` |
| 144 | `Tools/workflow/artifact_consult.py` |
| 143 | `Tools/validation/run_npu_runtime_tool_fallback_smoke.py` |
| 142 | `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` |
| 141 | `Tools/validation/check_markdown_line_limits.py` |
| 141 | `Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py` |
| 141 | `Tools/ai/full0to10_sqlite_memory/embedding.py` |
| 141 | `Tools/validation/check_docs_links.py` |
| 140 | `Scripting/shared/blender_compat.py` |
| 134 | `Scripting/shared/ffmpeg_encoder.py` |
| 133 | `Scripting/v61b/hotpatch/fog_patch.py` |
| 133 | `Scripting/shared/render_profiles.py` |
| 132 | `Tools/validation/check_json_artifacts.py` |
| 132 | `Scripting/v61b/spaziotempo/core/collections.py` |
| 130 | `Tools/ai/model_json.py` |
| 128 | `Tools/ai/build_agent_state_packet.py
```

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260506-004242.md`

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

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260506-004242.md`

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

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260506-004242.md`

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

### `output/validation/npu_provider_environment_full_toolbox_20260506-004242.md`

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

### `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `5761`
- SHA-256: `dc072de951745595428a47028c511ae224db1253e57027f9387b9c89a4f8afc9`
- Content included: `True`
- Content truncated: `False`

```text
# Full Toolbox Run Telemetry Summary

- Passed: `True`
- Stamp: `20260506-004242`
- Recommendation count: `20`
- Patch plan count: `20`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `None`
- Provider execution performed: `True`

## Repository consistency performance

- `total_build_report_seconds`: `51.357`
- `markdown_scan_seconds`: `38.351`
- `file_discovery_seconds`: `5.198`
- `python_inventory_seconds`: `4.403`
- `path_index_seconds`: `3.349`
- `findings_build_seconds`: `0.056`

## Top recommendations

- `consistency_001` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_002` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_003` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_004` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_005` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- `consistency_006` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_007` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_008` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- `consistency_009` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- `consistency_010` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_011` `md_python` `medium` -> `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- `consistency_032` `md_powershell` `medium` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_033` `md_powershell` `medium` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_034` `md_powershell` `medium` -> `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_035` `md_powershell` `medium` -> `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- `consistency_036` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`
- `consistency_037` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']`
- `consistency_038` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']`
- `consistency_039` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md']`
- `consistency_040` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md']`

## Top patch plans

- `consistency_001` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_002` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_003` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_004` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_005` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- `consistency_006` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_007` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_008` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- `consistency_009` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- `consistency_010` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_011` `md_python` review=`True` -> `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- `consistency_032` `md_powershell` review=`True` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_033` `md_powershell` review=`True` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_034` `md_powershell` review=`True` -> `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_035` `md_powershell` review=`True` -> `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- `consistency_036` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`
- `consistency_037` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md']`
- `consistency_038` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']`
- `consistency_039` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md']`
- `consistency_040` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/full0to10-manifest-gate/02-contract-gate.md']`

## GPU/NPU operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.


```

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1218`
- SHA-256: `5a4e21b2f4ec273408ab2c9d23420592dee73afe3fc61fe35ae281074f5c6ce3`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `20260506-004242`
- Tool call entries: `3`
- Executed count: `3`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `0.0`
- Declared runtime tool requests: `16`
- Broker runtime tool executions: `0`
- Declared not executed count: `16`

## By caller AI

- `orchestrator`: count=`3` executed=`3` failed=`0` elapsed=`0.0`

## By phase

- `explicit_runtime_tool_broker_bootstrap`: count=`3` executed=`3` failed=`0` elapsed=`0.0`

## By tool

- `check_python_syntax`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `build_python_line_count_csv`: count=`1` executed=`1` failed=`0` elapsed=`0.0`
- `check_validation_report_contract`: count=`1` executed=`1` failed=`0` elapsed=`0.0`

## First tool call entries

- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_python_syntax` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`build_python_line_count_csv` status=`None` elapsed=`0.0`
- `orchestrator` `explicit_runtime_tool_broker_bootstrap` round=`1` tool=`check_validation_report_contract` status=`None` elapsed=`0.0`


```

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7655`
- SHA-256: `2ecdec169282347ca5453b469da929137990fb33537d276cf68238df4eb3099c`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Capability Manifest

- Passed: `True`
- Tool count: `10`
- Declared runtime tool requests: `16`
- Broker runtime tool executions: `0`
- Declared not executed count: `16`
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
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
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
- Usage observed: `{'count': 0, 'executed': 0, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
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
- Usage observed: `{'count': 2, 'executed': 2, 'failed': 0, 'blocked': 0, 'elapsed_seconds': 0.0}`
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

- `Tools/ai/agent_runtime_tool_broker.py` role=`runtime_tool_broker_allowlist_source` exists=`True` sha256=`f948a459a39709877fac86cf098601b01f9560628644ec87d080c11f6fe3f449`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` role=`runtime_tool_usage_telemetry_builder` exists=`True` sha256=`250ed48a4c518b1c27ac28459a9e73513aefed454f0a9a966ddc96cee8e6cad7`
- `Tools/ai/build_semantic_evidence_chunks.py` role=`semantic_cloud_handoff_chunker` exists=`True` sha256=`5fdcbc74f6eb931f3b95c6b54b1eb1071e57f8f41a34c694864b3ac8cdab80f7`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` role=`shared_toolbox_bundle_builder` exists=`True` sha256=`6a1f5c3e6303cfa040fe9c1f30342dada4231deb8f6a06ea058be4cd99dfb18e`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.json` role=`observed_runtime_tool_usage_report` exists=`True` sha256=`0b25a0f08fa57f340edd73088522ae5af02737e3fa37ea3494522eac9e42fe05`

```

### `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `13328`
- SHA-256: `5026892135c8c968b9b77a7a092c7ac4c5607522dce961134cbc27983492db8f`
- Content included: `True`
- Content truncated: `False`

```text
# Semantic Evidence Chunk Manifest

- Passed: `True`
- Generated at: `2026-05-06T00:46:14`
- Ollama enabled: `False`
- Ollama model: `gpt-oss:20b`
- Chunk files: `109`

## Sources

- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260506-004242.json` chunks=`77` lines=`12879` sha256=`c864da5fd516aa685489f057d8a0ae3e0c08d6dc98e285cc80d1506f4ac69c9c`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0001.md` lines `2-55` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0002.md` lines `56-393` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0003.md` lines `394-542` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0004.md` lines `543-698` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0005.md` lines `699-843` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0006.md` lines `844-949` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0007.md` lines `950-1019` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0008.md` lines `1020-1091` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0009.md` lines `1092-1163` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0010.md` lines `1164-1179` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0011.md` lines `1180-1220` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0012.md` lines `1221-1235` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0013.md` lines `1236-1250` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0014.md` lines `1251-1306` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0015.md` lines `1307-1357` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0016.md` lines `1358-1387` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0017.md` lines `1388-1432` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0018.md` lines `1433-1629` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0019.md` lines `1630-1653` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_json_c864da5fd516_chunk_0020.md` lines `1654-1694` summary_source=`deterministic`
  - ... 57 more chunks
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260506-004242.md` chunks=`23` lines=`4033` sha256=`1c6ca878108bf258e2ebc1cd48150d2c84e572c408d6569c20d633ae72ea7ef3`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0001.md` lines `1-270` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0002.md` lines `271-388` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0003.md` lines `389-462` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0004.md` lines `463-724` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0005.md` lines `725-787` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0006.md` lines `788-1099` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0007.md` lines `1100-1149` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0008.md` lines `1150-1237` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0009.md` lines `1238-1310` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0010.md` lines `1311-1527` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0011.md` lines `1528-1600` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0012.md` lines `1601-1851` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0013.md` lines `1852-2049` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0014.md` lines `2050-2152` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0015.md` lines `2153-2304` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0016.md` lines `2305-2570` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0017.md` lines `2571-2760` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0018.md` lines `2761-2857` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0019.md` lines `2858-3075` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260506-004242_md_1c6ca878108b_chunk_0020.md` lines `3076-3218` summary_source=`deterministic`
  - ... 3 more chunks
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.json` chunks=`3` lines=`659` sha256=`3defd2230b538951148f7590f61fbfea8084f997eafcc5001ecac118b97bbc4c`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_20260506-004242_json_3defd2230b53_chunk_0001.md` lines `2-295` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_20260506-004242_json_3defd2230b53_chunk_0002.md` lines `296-631` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_20260506-004242_json_3defd2230b53_chunk_0003.md` lines `632-659` summary_source=`deterministic`
- `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.md` chunks=`1` lines=`71` sha256=`dc072de951745595428a47028c511ae224db1253e57027f9387b9c89a4f8afc9`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_20260506-004242_md_dc072de95174_chunk_0001.md` lines `1-71` summary_source=`deterministic`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.json` chunks=`1` lines=`216` sha256=`0b25a0f08fa57f340edd73088522ae5af02737e3fa37ea3494522eac9e42fe05`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/runtime_tool_usage_telemetry_20260506-004242_json_0b25a0f08fa5_chunk_0001.md` lines `2-216` summary_source=`deterministic`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.md` chunks=`1` lines=`33` sha256=`5a4e21b2f4ec273408ab2c9d23420592dee73afe3fc61fe35ae281074f5c6ce3`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/runtime_tool_usage_telemetry_20260506-004242_md_5a4e21b2f4ec_chunk_0001.md` lines `1-33` summary_source=`deterministic`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.json` chunks=`2` lines=`447` sha256=`4a4c7cfa43c8f3d698f5631355afc3f92ecc521a52a88df06a3da1325f35292f`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/runtime_tool_capability_manifest_20260506-004242_json_4a4c7cfa43c8_chunk_0001.md` lines `2-392` summary_source=`deterministic`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/runtime_tool_capability_manifest_20260506-004242_json_4a4c7cfa43c8_chunk_0002.md` lines `393-447` summary_source=`deterministic`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.md` chunks=`1` lines=`194` sha256=`2ecdec169282347ca5453b469da929137990fb33537d276cf68238df4eb3099c`
  - `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunks/runtime_tool_capability_manifest_20260506-004242_md_2ecdec169282_chunk_0001.md` lines `1-194` summary_source=`deterministic`

```

### `output/analysis/code_interpreter_full_toolbox_20260506-004242.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1912750`
- SHA-256: `89992c2d0af77a2cc2fcf2236ec7c857a037fd424d002aa2ae6abb967210ae83`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-06T00:43:24",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 533,
  "parsed_file_count": 533,
  "total_lines": 90862,
  "total_functions": 3294,
  "total_classes": 97,
  "total_risk_signals": 84,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 786
    },
    {
      "module": "__future__",
      "count": 476
    },
    {
      "module": "pathlib",
      "count": 367
    },
    {
      "module": "typing",
      "count": 335
    },
    {
      "module": "config",
      "count": 320
    },
    {
      "module": "json",
      "count": 275
    },
    {
      "module": "argparse",
      "count": 231
    },
    {
      "module": "sys",
      "count": 175
    },
    {
      "module": "datetime",
      "count": 160
    },
    {
      "module": "constants",
      "count": 151
    },
    {
      "module": "report_utils",
      "count": 84
    },
    {
      "module": "subprocess",
      "count": 62
    },
    {
      "module": "dataclasses",
      "count": 57
    },
    {
      "module": "re",
      "count": 48
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
      "module": "os",
      "count": 24
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
      "count": 21
    },
    {
      "module": "full0to10_sqlite_memory",
      "count": 19
    },
    {
      "module": "time",
      "count": 16
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
      "module": "components",
      "count": 15
    },
    {
      "module": "math",
      "count": 14
    },
    {
      "module": "materials",
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
      "module": "ast",
      "count": 12
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "sqlite3",
      "count": 11
    },
    {
      "module": "concurrent",
      "count": 11
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
      "module": "spaziotempo",
      "count": 9
    }
  ],
  "largest_files": [
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
      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
      "line_count": 1179,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
      "line_count": 1129,
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
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 850,
      "risk": "high"
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
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "line_count": 715,
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
      "path": "Tools/ai/build_repository_consistency_map.py",
      "line_count": 687,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "line_count": 675,
      "risk": "medium"
    },
    {
      "path": "Scripting/v61b/materials.py",
      "line_count": 657,
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
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "line_count": 580,
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
      "path": "Tools/ai/build_semantic_evidence_chunks.py",
      "line_count": 562,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "low": 371,
    "medium": 153,
    "high": 9
  },
  "recommendation_count": 162,
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
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output
```

### `output/analysis/full_memory_tool_regeneration_20260506-004242_code_interpreter.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1730407`
- SHA-256: `0d7b442f693e6a9d6d754c337c21009c51884e1dd8b2ad645aa8a25c37085138`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-06T00:43:10",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 491,
  "parsed_file_count": 491,
  "total_lines": 80257,
  "total_functions": 3013,
  "total_classes": 75,
  "total_risk_signals": 72,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 786
    },
    {
      "module": "__future__",
      "count": 469
    },
    {
      "module": "pathlib",
      "count": 351
    },
    {
      "module": "typing",
      "count": 329
    },
    {
      "module": "json",
      "count": 269
    },
    {
      "module": "argparse",
      "count": 231
    },
    {
      "module": "sys",
      "count": 169
    },
    {
      "module": "datetime",
      "count": 160
    },
    {
      "module": "constants",
      "count": 151
    },
    {
      "module": "report_utils",
      "count": 84
    },
    {
      "module": "subprocess",
      "count": 60
    },
    {
      "module": "dataclasses",
      "count": 53
    },
    {
      "module": "re",
      "count": 45
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
      "module": "os",
      "count": 22
    },
    {
      "module": "hashlib",
      "count": 21
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
      "module": "models",
      "count": 16
    },
    {
      "module": "ollama_runtime",
      "count": 16
    },
    {
      "module": "time",
      "count": 15
    },
    {
      "module": "components",
      "count": 15
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
      "module": "ast",
      "count": 12
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "sqlite3",
      "count": 11
    },
    {
      "module": "concurrent",
      "count": 11
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
      "module": "collections",
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
    },
    {
      "module": "agent_memory_policy",
      "count": 7
    },
    {
      "module": "full0to10_provider_feedback_loop",
      "count": 7
    }
  ],
  "largest_files": [
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
      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
      "line_count": 1179,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
      "line_count": 1129,
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
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 850,
      "risk": "high"
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
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "line_count": 715,
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
      "path": "Tools/ai/build_repository_consistency_map.py",
      "line_count": 687,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "line_count": 675,
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
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "line_count": 580,
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
    },
    {
      "path": "Tools/ai/build_agent_review_code_patch_plan.py",
      "line_count": 499,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "medium": 136,
    "low": 348,
    "high": 7
  },
  "recommendation_count": 143,
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
        "python -m py_compil
```

### `output/analysis/full_memory_tool_regeneration_20260506-004242_code_interpreter.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7338`
- SHA-256: `7d7612d11ff58973f455e5727f473d3d5b92ae034245cfd5bf1a3737f6d8ecad`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `491`
- Parsed files: `491`
- Total lines: `80257`
- Total functions: `3013`
- Total classes: `75`
- Risk signals: `72`
- TODO/FIXME markers: `21`
- Recommendation count: `143`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1129` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` — `909` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `850` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` — `675` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `626` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_bundle.py` — `608` lines, risk `medium`
- `Tools/workflow/workflow_debug.py` — `607` lines, risk `medium`

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
- `code_static_011` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module
- `code_static_012` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_013` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_014` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_015` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_016` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_017` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_018` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_019` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: large functions detected
- `code_static_020` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_021` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_022` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_023` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Tools/ai/build_refactor_duplication_audit.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_025` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_026` `Tools/ai/build_repository_consistency_map.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_027` `Tools/ai/build_runtime_tool_capability_manifest.py` risk `medium`: complex functions detected
- `code_static_028` `Tools/ai/build_runtime_tool_usage_telemetry.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_029` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_030` `Tools/ai/build_semantic_evidence_chunks.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_031` `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_033` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_034` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_035` `Tools/ai/full0to10_accelerator_control/device_visibility.py` risk `medium`: complex functions detected
- `code_static_036` `Tools/ai/full0to10_final_product/readiness.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/full0to10_hardware_capability/openvino_devices.py` risk `medium`: complex functions detected
- `code_static_038` `Tools/ai/full0to10_runtime_tools/memory_adapter.py` risk `medium`: complex functions detected
- `code_static_039` `Tools/ai/github_evidence_bundle_artifacts.py` risk `medium`: complex functions detected
- `code_static_040` `Tools/ai/gpu_planner_json_contract.py` risk `medium`: complex functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260506-004242.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5660`
- SHA-256: `ff1183df2cb22414b9cecd05dbf868802c18f3596f0ada876c4a54c750f37ebb`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_planner_json_contract_replay",
  "generated_at": "2026-05-06T00:46:06",
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
    "gpu_report": "output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.json"
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
      "original_response_chars": 66,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "468d9d717e60e6ddfb2f4ab943c8b9f737ce7e42a80a7c5d19f1b658de933a43",
        "raw_response_chars": 66,
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
      "round": 2,
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
      "original_response_chars": 2487,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "4c787c969f5e63136802ab80680a91c253c55282e93a71dfcab86b624b39ec8f",
        "raw_response_chars": 2487,
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

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260506-004242.md`

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

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260506-004242.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5633`
- SHA-256: `3947c140a15ddf5b66f1bd29240d5ec434909025f8c417cd954f23258b6e702e`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-06T00:46:06",
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
    "orchestrator": "output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 4,
    "npu_audit_count": 1,
    "npu_audit_success_count": 1,
    "npu_audit_round_coverage": 0.25,
    "avg_gpu_round_seconds": 27.015,
    "p50_gpu_round_seconds": 27.015,
    "p90_gpu_round_seconds": 27.015,
    "avg_npu_audit_seconds": 92.0,
    "p50_npu_audit_seconds": 92.0,
    "p90_npu_audit_seconds": 92.0,
    "npu_to_gpu_avg_duration_ratio": 3.405,
    "gpu_elapsed_seconds": 108.061,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.001,
    "gpu": {
      "elapsed_seconds": 108.061,
      "round_count": 4,
      "round_duration_source": "gpu_elapsed_divided_by_round_count",
      "round_duration_sample_count": 1,
      "avg_round_seconds": 27.015,
      "p50_round_seconds": 27.015,
      "p90_round_seconds": 27.015,
      "max_round_seconds": 27.015,
      "round_durations_total_seconds": 27.015,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 16,
        "runtime_tool_execution_count": 0,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 16,
        "runtime_tool_provider_request_execution_count": 0,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0
      },
      "embedded_performance": {}
    },
    "npu": {
      "audit_count": 1,
      "audit_requested_count": 0,
      "audit_success_count": 1,
      "duration_sample_count": 1,
      "avg_audit_seconds": 92.0,
      "p50_audit_seconds": 92.0,
      "p90_audit_seconds": 92.0,
      "max_audit_seconds": 92.0,
      "audit_durations_total_seconds": 92.0,
      "status_counts": {
        "finished": 1
      },
      "classification_counts": {
        "usable_audit_text": 1
      },
      "lane_diagnostics": {}
    },
    "sync": {
      "npu_to_gpu_avg_duration_ratio": 3.405,
      "npu_audit_round_coverage": 0.25,
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
      "Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.",
      "NPU audits are usable; tune cadence rather than disabling the lane."
    ],
    "parameters": {
      "npu_auditor_every_rounds": 3,
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
    "NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.",
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
    },
    {
      "priority": "medium",
      "area": "npu_cadence",
      "recommendation": "Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget.",
      "evidence": "npu_to_gpu_avg_duration_ratio=3.405",
      "guardrail": "keep_max_concurrent_npu_audits_1"
    }
  ],
  "decision": {
    "npu_too_slow_for_per_round_lockstep": true,
    "recommended_next_layer": "feed timing-backed GPU/NPU suggestions into decision-loop patch planning",
    "manual_review_required": true
  }
}

```

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260506-004242.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2563`
- SHA-256: `3617832003dde354315ea136739e49f59b9054677007b2603e61c5d75556ce7e`
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
- `npu_audit_count`: `1`
- `npu_audit_success_count`: `1`
- `npu_audit_round_coverage`: `0.25`
- `avg_gpu_round_seconds`: `27.015`
- `p50_gpu_round_seconds`: `27.015`
- `p90_gpu_round_seconds`: `27.015`
- `avg_npu_audit_seconds`: `92.0`
- `p50_npu_audit_seconds`: `92.0`
- `p90_npu_audit_seconds`: `92.0`
- `npu_to_gpu_avg_duration_ratio`: `3.405`
- `gpu_elapsed_seconds`: `108.061`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `108.061`
- GPU average round seconds: `27.015`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- GPU timing sample count: `1`
- GPU round durations total seconds: `27.015`
- NPU average audit seconds: `92.0`
- NPU duration sample count: `1`

## Operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count
- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=3.405

## Suggested balanced profile

- `npu_auditor_every_rounds`: `3`
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
- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.
- NPU audits are usable; tune cadence rather than disabling the lane.


```

### `output/analysis/repository_consistency_map_full_toolbox_20260506-004242.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `7416683`
- SHA-256: `bf1cfd1e61fea4a88b690d2ae4354a31edda8c9384d30b4e75a50d1b8cffa670`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "repository_consistency_map",
  "generated_at": "2026-05-06T00:44:17",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "manual_review_required": true,
  "scope": {
    "markdown_file_count": 568,
    "python_file_count": 582,
    "markdown_reference_count": 61224,
    "markdown_python_command_count": 835,
    "python_inventory_count": 582,
    "generated_evidence_chunk_exclusion_enabled": true
  },
  "finding_count": 9721,
  "severity_counts": {
    "high": 2500,
    "low": 48,
    "medium": 7173
  },
  "finding_kind_counts": {
    "documented_python_script_without_obvious_smoke": 48,
    "md_cli_arg_not_in_argparse": 2,
    "md_mentions_missing_markdown_path": 7171,
    "md_mentions_missing_powershell_path": 222,
    "md_mentions_missing_python_path": 2247,
    "md_python_command_script_missing": 31
  },
  "markdown_reference_kind_counts": {
    "artifact": 10856,
    "markdown": 16662,
    "powershell": 1061,
    "python": 32645
  },
  "findings": [
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AGENTS.md",
      "line": 248,
      "target": "run_patch_bundle.py",
      "evidence": "run_patch_bundle.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AGENTS.md",
      "line": 249,
      "target": "patches/00_check_repo_ready.py",
      "evidence": "patches/00_check_repo_ready.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "AGENTS.md",
      "line": 105,
      "target": "text\nCHATGPT.md                         # root pointer\nCHATGPT/README.md                  # index and reading order\nCHATGPT/next-chat-handoff-*.md     # current handoff state\nCHATGPT/chatgpt-session-problems-and-robust-fixes-*.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AGENTS.md",
      "line": 246,
      "target": "text\nREADME.md\nrun_patch_bundle.py\npatches/00_check_repo_ready.py\npatches/01_*.py",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 237,
      "target": "run_patch_bundle.py",
      "evidence": "run_patch_bundle.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_powershell_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 292,
      "target": "some_script.ps1",
      "evidence": "[System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path \".\\Tools\\workflow\\some_script.ps1\"), [ref]$Tokens, [ref]$ParseErrors) | Out-Null",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 302,
      "target": "changed.py",
      "evidence": "- run `python -m py_compile <changed.py>`",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 323,
      "target": "some_tool.py",
      "evidence": ".\\Tools\\ai\\some_tool.py `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 324,
      "target": "some_smoke.py",
      "evidence": ".\\Tools\\validation\\some_smoke.py `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_powershell_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 325,
      "target": "some_runner.ps1",
      "evidence": ".\\Tools\\workflow\\some_runner.ps1",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
      "line": 323,
      "target": "Tools/validation/some_smoke.py",
      "evidence": ".\\Tools\\ai\\some_tool.py `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 22,
      "target": "agent_memory_schema.py",
      "evidence": "agent_memory_schema.py                  # DB schema + migrations",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 23,
      "target": "agent_memory_chunker.py",
      "evidence": "agent_memory_chunker.py                 # Markdown/text chunking",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 24,
      "target": "agent_memory_embeddings.py",
      "evidence": "agent_memory_embeddings.py              # embedding cache",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 25,
      "target": "agent_memory_search.py",
      "evidence": "agent_memory_search.py                  # FTS5 + vector/hybrid search",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 26,
      "target": "agent_memory_tools.py",
      "evidence": "agent_memory_tools.py                   # memory_add_text / memory_add_file / memory_search CLI",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 325,
      "target": "agent_memory_tools.py",
      "evidence": "python .\\Tools\\ai\\agent_memory_tools.py init `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 328,
      "target": "agent_memory_tools.py",
      "evidence": "python .\\Tools\\ai\\agent_memory_tools.py memory_add_text `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 334,
      "target": "agent_memory_tools.py",
      "evidence": "python .\\Tools\\ai\\agent_memory_tools.py memory_add_file `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
      "line": 339,
      "target": "agent_memory_tools.py",
      "evidence": "python .\\Tools\\ai\\agent_memory_tools.py memory_search `",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 47,
      "target": "Tools/ai/build_runtime_hardware_capability_manifest.py",
      "evidence": "Tools/ai/build_runtime_hardware_capability_manifest.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 74,
      "target": "Tools/validation/check_runtime_hardware_capability_manifest.py",
      "evidence": "Tools/validation/check_runtime_hardware_capability_manifest.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 98,
      "target": "Tools/ai/agent_memory_schema.py",
      "evidence": "Tools/ai/agent_memory_schema.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 99,
      "target": "Tools/ai/agent_memory_tools.py",
      "evidence": "Tools/ai/agent_memory_tools.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 139,
      "target": "Tools/ai/simulate_npu_tool_proxy.py",
      "evidence": "Tools/ai/simulate_npu_tool_proxy.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 157,
      "target": "Tools/ai/run_npu_tool_proxy.py",
      "evidence": "Tools/ai/run_npu_tool_proxy.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 229,
      "target": "build_runtime_hardware_capability_manifest.py",
      "evidence": "build_runtime_hardware_capability_manifest.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 230,
      "target": "check_runtime_hardware_capability_manifest.py",
      "evidence": "check_runtime_hardware_capability_manifest.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 46,
      "target": "text\nTools/ai/build_runtime_hardware_capability_manifest.py",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md",
      "line": 52,
      "target": "text\ndocs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json\ndocs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md",
      "evidence": "```text",
      "re
```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260506-004242.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1230568`
- SHA-256: `88a7500e572d44aee37381bdde9bbe39a414c110590f278abeb50dbcd83a1c8f`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "shared_toolbox_ai_to_ai_final_summary",
  "stamp": "20260506-004242",
  "passed": true,
  "tools_available": [
    "build_agent_agnostic_tool_inventory",
    "build_agent_memory_inventory",
    "build_agent_transient_request_context",
    "build_code_interpreter_report",
    "build_python_line_count_csv",
    "build_refactor_duplication_audit",
    "check_python_syntax",
    "check_validation_report_contract",
    "run_gpu_planner_json_contract_smoke",
    "runtime_sqlite_memory"
  ],
  "tool_capabilities": [
    {
      "tool_name": "build_agent_agnostic_tool_inventory",
      "category": "inventory",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Inventory existing reusable IA-Carmine tools and guardrails."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Discover reusable tooling before adding new scripts.",
      "allowed_args": [
        "root"
      ]
    },
    {
      "tool_name": "build_agent_memory_inventory",
      "category": "inventory",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Read-only SQLite/JSONL agent memory inventory."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Summarize durable project memory as read-only context.",
      "allowed_args": [
        "objective",
        "memory_db"
      ]
    },
    {
      "tool_name": "build_agent_transient_request_context",
      "category": "context",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build request-scoped context from memory notes, raw files and reports."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Assemble request-scoped context for local AI planning.",
      "allowed_args": [
        "objective",
        "memory_note",
        "raw_file",
        "report_file"
      ]
    },
    {
      "tool_name": "build_code_interpreter_report",
      "category": "static_analysis",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build static code-interpreter style report over selected roots."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Build static analysis/refactor evidence.",
      "allowed_args": [
        "input"
      ]
    },
    {
      "tool_name": "build_python_line_count_csv",
      "category": "inventory",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build full Python line-count CSV/JSON/MD evidence."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Refresh complete Python inventory before refactor planning.",
      "allowed_args": [
        "exclude_dir"
      ]
    },
    {
      "tool_name": "build_refactor_duplication_audit",
      "category": "support_tool",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Use through the runtime tool broker when a report-only request requires it.",
      "allowed_args": [
        "root",
        "report",
        "input_audit_report",
        "line_count_report",
        "code_interpreter_report",
        "python_syntax_report",
        "bundle_smoke_report",
        "memory_routing_report"
      ]
    },
    {
      "tool_name": "check_python_syntax",
      "category": "validation",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Validate Python syntax across repository."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Gate Python source changes.",
      "allowed_args": []
    },
    {
      "tool_name": "check_validation_report_contract",
      "category": "validation",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Validate validation report contract for a scoped report-dir or explicit report files."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Gate report quality before evidence bundling.",
      "allowed_args": [
        "report_file"
      ]
    },
    {
      "tool_name": "run_gpu_planner_json_contract_smoke",
      "category": "validation",
      "safe_default_mode": "report-only",
      "what_it_can_do": [
        "Run GPU planner JSON contract smoke tests without provider."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write SQLite or persistent memory"
      ],
      "recommended_next_use": "Validate planner JSON contract without providers.",
      "allowed_args": []
    },
    {
      "tool_name": "runtime_sqlite_memory",
      "category": "memory_status",
      "safe_default_mode": "controlled read-only/status by default",
      "what_it_can_do": [
        "Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**."
      ],
      "what_it_must_not_do": [
        "execute arbitrary shell commands",
        "apply patches",
        "run Blender runtime",
        "commit output artifacts",
        "write persistent memory without explicit confirmation and authorization"
      ],
      "recommended_next_use": "Read memory status/search through broker-controlled actions.",
      "allowed_args": [
        "action",
        "scope",
        "database",
        "persistent_database",
        "summary",
        "content",
        "role",
        "tag",
        "query",
        "limit",
        "confirm",
        "allow_persistent_write"
      ]
    }
  ],
  "tool_requests_executed_or_proposed": [
    {
      "id": "request_build_code_interpreter_report",
      "tool": "build_code_interpreter_report",
      "reason": "Build static analysis/refactor evidence.",
      "args": {},
      "status": "proposed_or_reported"
    },
    {
      "id": "request_check_python_syntax",
      "tool": "check_python_syntax",
      "reason": "Gate Python source changes.",
      "args": {},
      "status": "proposed_or_reported"
    },
    {
      "id": "request_check_validation_report_contract",
      "tool": "check_validation_report_contract",
      "reason": "Gate report quality before evidence bundling.",
      "args": {},
      "status": "proposed_or_reported"
    }
  ],
  "reports_generated": [
    {
      "path": "output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_integrated.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_full_toolbox_decision_loop_integrated",
      "passed": true
    },
    {
      "path": "output/validation/agent_review_full_toolbox_decision_loop_20260506-004242_workflow.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_full_toolbox_decision_loop_workflow",
      "passed": true
    },
    {
      "path": "output/validation/agent_review_warning_policy_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_warning_policy",
      "passed": true
    },
    {
      "path": "output/validation/local_provider_probe.json",
      "exists": true,
      "json_ok": true,
      "kind": "local_provider_probe",
      "passed": false
    },
    {
      "path": "output/validation/ai_workload_report_quality.json",
      "exists": true,
      "json_ok": true,
      "kind": "ai_workload_report_quality",
      "passed": true
    },
    {
      "path": "output/validation/ai_workload_quality_lane_routing.json",
      "exists": true,
      "json_ok": true,
      "kind": "ai_workload_quality_lane_routing",
      "passed": true
    },
    {
      "path": "output/validation/npu_decode_quality_remediation.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_decode_quality_remediation",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260506-004242_agent_review_decision_loop.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop",
      "passed": true
    },
    {
      "path": "output/patch_specs/full_toolbox_20260506-004242_agent_review_patch_plan.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_patch_plan",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260506-004242_deterministic_recommendations.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260506-004242_bridge_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260506-004242_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260506-004242_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_deep_planning_supervised",
      "passed": true
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map",
      "passed": true
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map_smoke",
      "passed": true
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "code_interpreter_report",
      "passed": true
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_line_count_csv",
      "passed": true
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_syntax",
      "passed": true
    },
    {
      "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_planner_json_contract_smoke",
      "passed": true
    },
    {
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer_smoke",
      "passed": true
    },
    {
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop_smoke",
      "passed": true
    },
    {
      "path": "output/validation/npu_provider_environment_full_toolbox_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_provider_environment",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "full_toolbox_run_telemetry_summary",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "runtime_tool_usage_telemetry",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260506-004242.json",
      "exists": true,
      "json_ok": true,
      "kind": "runtime_tool_capability_manifest",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260506-004242_cloud_semantic_deterministic_chunk_manifest.json",
      "exists": true,
      "json_ok": true,
      "kind": "semantic_evidence_chunk_manifest",
      "passed": true
    }
  ],
  "remaining_gaps": [
    {
      "path": "output/validation/shared_toolbox_python_syntax_20260506-004242.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_20260506-004242.json",
      "reason": "optional report missing"
    },
    {
      "path": "outpu
```

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agent_memory_inventory.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `13528`
- SHA-256: `0915f944304d964fda03c0e3ccb1841ac7622de243ac8b0079064ed52925661c`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_memory_inventory",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_read_only_inventory",
  "objective": "Reload IA-Carmine full toolbox context before agent review full toolbox decision-loop run.",
  "objective_keywords": [
    "full",
    "toolbox",
    "agent",
    "before",
    "carmine",
    "context",
    "decision",
    "loop",
    "reload",
    "review",
    "run"
  ],
  "inputs": {
    "memory_db": "indexAI/agent_memory/agent_memory.sqlite",
    "memory_db_exists": true,
    "memory_jsonl": [],
    "memory_db_limit": 1000,
    "max_memory_chars": 24000
  },
  "sqlite": {
    "path": "indexAI/agent_memory/agent_memory.sqlite",
    "exists": true,
    "read_only": true,
    "opened": true,
    "schema_version": "1",
    "tables": [
      {
        "name": "memory_meta",
        "row_count": 1,
        "columns": [
          {
            "name": "key",
            "type": "TEXT",
            "notnull": false,
            "pk": true
          },
          {
            "name": "value",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          }
        ]
      },
      {
        "name": "memory_records",
        "row_count": 86,
        "columns": [
          {
            "name": "record_id",
            "type": "TEXT",
            "notnull": false,
            "pk": true
          },
          {
            "name": "kind",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "scope",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "source",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "summary",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "content",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "tags_json",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "confidence",
            "type": "REAL",
            "notnull": true,
            "pk": false
          },
          {
            "name": "created_at",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          },
          {
            "name": "updated_at",
            "type": "TEXT",
            "notnull": false,
            "pk": false
          },
          {
            "name": "expires_at",
            "type": "TEXT",
            "notnull": false,
            "pk": false
          },
          {
            "name": "metadata_json",
            "type": "TEXT",
            "notnull": true,
            "pk": false
          }
        ]
      }
    ],
    "indexes": [
      {
        "name": "idx_memory_kind",
        "table": "memory_records"
      },
      {
        "name": "idx_memory_scope",
        "table": "memory_records"
      },
      {
        "name": "idx_memory_source",
        "table": "memory_records"
      },
      {
        "name": "sqlite_autoindex_memory_meta_1",
        "table": "memory_meta"
      },
      {
        "name": "sqlite_autoindex_memory_records_1",
        "table": "memory_records"
      }
    ],
    "errors": []
  },
  "records": {
    "record_count": 86,
    "total_content_chars": 348469,
    "kind_counts": {
      "source_file": 84,
      "operator_note": 2
    },
    "scope_counts": {
      "project": 84,
      "task": 2
    },
    "top_sources": {
      "output/ai_context_packs/full_context_golden_core_ai_backend.json": 12,
      "output/ai_context_packs/full_context_golden_core_ai_backend.md": 12,
      "output/ai_context_packs/full_context_golden_selected_chunks.json": 12,
      "output/ai_context_packs/full_context_golden_selected_chunks.md": 12,
      "indexAI/code_chunks/semantic_code_chunks_manifest.json": 12,
      "output/ai_pipeline/full_context_golden_enrichment_plan.json": 12,
      "output/ai_pipeline/full_context_golden_enrichment_plan.md": 5,
      "cli_note_1": 2,
      "docs/LOCAL_AI_TASKS/refactor-unused-useful-code-tool-class-promotion-2026-05-05.md": 1,
      "docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md": 1,
      "docs/LOCAL_AI_TASKS/docs-md-obsolete-pruning-next-step.md": 1,
      "docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md": 1,
      "docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md": 1,
      "docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md": 1,
      "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md": 1
    },
    "tag_counts": {
      "source_file": 84,
      "json": 48,
      "md": 36,
      "recent": 2,
      "operator_note": 2
    },
    "confidence_buckets": {
      "0.90-1.00": 86
    }
  },
  "policy_report": {
    "kind": "agent_memory_policy_report",
    "passed": true,
    "record_count": 86,
    "promotion_candidate_count": 0,
    "review_count": 0,
    "risk_count": 0,
    "duplicate_group_count": 0,
    "action_counts": {
      "keep": 86
    },
    "promotion_candidates": [],
    "risks": []
  },
  "selected_memory_preview": [
    {
      "record_id": "434e2dcb7cc913e15205",
      "kind": "source_file",
      "scope": "project",
      "source": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md",
      "tags": [
        "source_file",
        "md"
      ],
      "confidence": 1.0,
      "rank_score": 26.0,
      "summary": "# Shared Runtime Toolbox AI-to-AI Next Task — 2026-05-03 ## Purpose Use this Markdown as the next official task request for the local IA-Carmine pipeline. This is not a generic procedure. It is a concrete AI-to-AI handoff request from ChatGPT to the local IA. The local IA should read this file as the task input, use the committed evidence bundle as context, run only safe/report-only tooling unless explicitly configured otherwise, and produce a compact evidence bundle for review. ## Repository baseline ```text repository: C-F-tek/blender-audio-project branch to sync: master current reference commit: eb5ec1d test(ai): add shared runtime toolbox evidence bundle project: IA-Carmine workflow: ChatGPT -> MD task -> local IA -> reports/bundle -> GitHub evidence -> ChatGPT review ``` Required sync before running: ```powershell cd C:\\Users\\carmi\\blender\\blender-audio-project git fetch origin g..."
    },
    {
      "record_id": "f72277896ae11782f051",
      "kind": "source_file",
      "scope": "project",
      "source": "docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md",
      "tags": [
        "source_file",
        "md"
      ],
      "confidence": 1.0,
      "rank_score": 22.0,
      "summary": "# IA-Carmine task — patch plan for FULL RUN UNICA / TUTTO SU TUTTO ## Repository ```text C-F-tek/blender-audio-project ``` ## Branch ```text codex/unified-local-ai-refactor-launcher ``` ## Objective Generate a review-only patch plan for aligning the canonical IA-Carmine full run to the current policy: ```text FULL RUN UNICA = TUTTO SU TUTTO ``` The output must be recommendations and patch-plan artifacts only. Do not apply source patches automatically. ## Current user decision The previous conservative policy is no longer valid for canonical full runs. Canonical full run policy: ```text TUTTO SU TUTTO all declared runtime/tool/provider/advisory/evidence/patch-spec/memory lanes active ``` Do not use a reduced/minimal command as the canonical full run. The canonical procedure must provide a long single PowerShell script with variables for input/output/runtime knobs. ## Required scope to..."
    },
    {
      "record_id": "2b456a3f9d873a6f7c44",
      "kind": "source_file",
      "scope": "project",
      "source": "docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md",
      "tags": [
        "source_file",
        "md"
      ],
      "confidence": 1.0,
      "rank_score": 18.0,
      "summary": "﻿# Refactor/reuse methods, classes and tools planning task ## Status Stable local-AI planning task for IA-Carmine refactor/reuse work. This task is intended for a full-run planning pass, not for automatic patch application. ## Objective Analyze the repository code and produce a manual-review refactor/reuse plan for: ```text duplicate methods/classes reusable helper functions base-class/superclass opportunities project-tool promotion candidates support-library extraction candidates workflow/provider/telemetry utility centralization code that should remain app-specific and not be promoted The goal is a controlled mega patch plan, not a blind rewrite. Current doctrine Full0To10 = TUTTO SU TUTTO quick/balanced/deep/custom = intensity, not scope telemetry accompanies evidence and patch plans for completeness For this task, tutto includes code, docs, workflow scripts, validation tools, prov..."
    },
    {
      "record_id": "5459d392df91cf0be01f",
      "kind": "source_file",
      "scope": "project",
      "source": "output/ai_pipeline/full_context_golden_enrichment_plan.json",
      "tags": [
        "source_file",
        "json"
      ],
      "confidence": 1.0,
      "rank_score": 18.0,
      "summary": "{ \"schema_version\": 1, \"kind\": \"local_ai_enrichment_plan\", \"generated_at\": \"2026-05-04T20:45:15.029513+00:00\", \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\", \"objective\": \"Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker.\", \"task_file\": \"docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md\", \"profile\": \"npu\", \"basename\": \"full_context_golden_enrichment_plan\", \"apply_mode\": \"report_only\", \"provider_execution_performed\": false, \"source_writes_performed\": false, \"patch_application_performed\": false, \"complexity\": { \"level\": \"high\", \"score\": 16, \"matched_terms\": [ \"architecture\", \"broker\", \"context\", \"full-context\", \"gpu\", \"knowledge\", \"npu\", \"ollama\", \"patch\", \"provider\" ], \"task_text_chars_sampled\": 8000 }, \"lane_policy\": { \"primary_advisory..."
    },
    {
      "record_id": "2ceb4033da1ff042e86f",
      "kind": "source_file",
      "scope": "project",
      "source": "output/ai_pipeline/full_context_golden_enrichment_plan.json",
      "tags": [
        "source_file",
        "json"
      ],
      "confidence": 1.0,
      "rank_score": 18.0,
      "summary": "{ \"schema_version\": 1, \"kind\": \"local_ai_enrichment_plan\", \"generated_at\": \"2026-05-04T20:32:37.994981+00:00\", \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\", \"objective\": \"Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker.\", \"task_file\": \"docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md\", \"profile\": \"npu\", \"basename\": \"full_context_golden_enrichment_plan\", \"apply_mode\": \"report_only\", \"provider_execution_performed\": false, \"source_writes_performed\": false, \"patch_application_performed\": false, \"complexity\": { \"level\": \"high\", \"score\": 16, \"matched_terms\": [ \"architecture\", \"broker\", \"context\", \"full-context\", \"gpu\", \"knowledge\", \"npu\", \"ollama\", \"patch\", \"provider\" ], \"task_text_chars_sampled\": 8000 }, \"lane_policy\": { \"primary_advisory..."
    },
    {
      "record_id": "286c46e67169094fd008",
      "kind": "operator_note",
      "scope": "task",
      "source": "cli_note_1",
      "tags": [
        "recent",
        "operator_note"
      ],
      "confidence": 1.0,
      "rank_score": 6.0,
      "summary": "Unified launcher report-only run."
    },
    {
      "record_id": "8afcda325efa964d05c6",
      "kind": "operator_note",
      "scope": "task",
      "source": "cli_note_1",
      "tags": [
        "recent",
        "operator_note"
      ],
      "confidence": 1.0,
      "rank_score": 6.0,
      "summary": "Local AI enrichment run. Preserve report-only defaults, explicit providers, NPU guardrail role and no patch apply."
    }
  ],
  "integration": {
    "compatible_with_agent_state_packet": true,
    "compatible_with_megalithic_review": true,
    "recommended_consumer_artifacts": [
      "run_megalithic_repo_review.py",
      "refine_megalithic_review_signals.py",
      "build_megalithic_review_pr_draft.py",
      "run_local_ai_core_tool_activation.ps1"
    ]
  },
  "guardrails": {
    "sqlite_read_only": true,
    "sqlite_db_committed": false,
    "memory_promotion_performed": false,
    "memory_delete_performed": false,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "blender_runtime_touched": false
  }
}

```

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agent_memory_inventory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6728`
- SHA-256: `6fa44501e293b3c446df33b2d2d6b4664b1fef08be5667ce4d1954b8626ddfb0`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Memory Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Memory DB: `indexAI/agent_memory/agent_memory.sqlite`
- Memory DB exists: `True`
- Record count: `86`
- SQLite opened read-only: `True`

## SQLite

- Schema version: `1`

- `memory_meta` rows=`1` columns=`2`
- `memory_records` rows=`86` columns=`12`

## Record distributions

### kind_counts

- `source_file`: 84
- `operator_note`: 2

### scope_counts

- `project`: 84
- `task`: 2

### confidence_buckets

- `0.90-1.00`: 86

## Policy summary

- `passed`: `True`
- `promotion_candidate_count`: `0`
- `review_count`: `0`
- `risk_count`: `0`
- `duplicate_group_count`: `0`

## Selected memory preview

### 434e2dcb7cc913e15205 - docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md

- Kind: `source_file`
- Scope: `project`
- Score: `26.0`

# Shared Runtime Toolbox AI-to-AI Next Task — 2026-05-03 ## Purpose Use this Markdown as the next official task request for the local IA-Carmine pipeline. This is not a generic procedure. It is a concrete AI-to-AI handoff request from ChatGPT to the local IA. The local IA should read this file as the task input, use the committed evidence bundle as context, run only safe/report-only tooling unless explicitly configured otherwise, and produce a compact evidence bundle for review. ## Repository baseline ```text repository: C-F-tek/blender-audio-project branch to sync: master current reference commit: eb5ec1d test(ai): add shared runtime toolbox evidence bundle project: IA-Carmine workflow: ChatGPT -> MD task -> local IA -> reports/bundle -> GitHub evidence -> ChatGPT review ``` Required sync before running: ```powershell cd C:\Users\carmi\blender\blender-audio-project git fetch origin g...

### f72277896ae11782f051 - docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md

- Kind: `source_file`
- Scope: `project`
- Score: `22.0`

# IA-Carmine task — patch plan for FULL RUN UNICA / TUTTO SU TUTTO ## Repository ```text C-F-tek/blender-audio-project ``` ## Branch ```text codex/unified-local-ai-refactor-launcher ``` ## Objective Generate a review-only patch plan for aligning the canonical IA-Carmine full run to the current policy: ```text FULL RUN UNICA = TUTTO SU TUTTO ``` The output must be recommendations and patch-plan artifacts only. Do not apply source patches automatically. ## Current user decision The previous conservative policy is no longer valid for canonical full runs. Canonical full run policy: ```text TUTTO SU TUTTO all declared runtime/tool/provider/advisory/evidence/patch-spec/memory lanes active ``` Do not use a reduced/minimal command as the canonical full run. The canonical procedure must provide a long single PowerShell script with variables for input/output/runtime knobs. ## Required scope to...

### 2b456a3f9d873a6f7c44 - docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md

- Kind: `source_file`
- Scope: `project`
- Score: `18.0`

﻿# Refactor/reuse methods, classes and tools planning task ## Status Stable local-AI planning task for IA-Carmine refactor/reuse work. This task is intended for a full-run planning pass, not for automatic patch application. ## Objective Analyze the repository code and produce a manual-review refactor/reuse plan for: ```text duplicate methods/classes reusable helper functions base-class/superclass opportunities project-tool promotion candidates support-library extraction candidates workflow/provider/telemetry utility centralization code that should remain app-specific and not be promoted The goal is a controlled mega patch plan, not a blind rewrite. Current doctrine Full0To10 = TUTTO SU TUTTO quick/balanced/deep/custom = intensity, not scope telemetry accompanies evidence and patch plans for completeness For this task, tutto includes code, docs, workflow scripts, validation tools, prov...

### 5459d392df91cf0be01f - output/ai_pipeline/full_context_golden_enrichment_plan.json

- Kind: `source_file`
- Scope: `project`
- Score: `18.0`

{ "schema_version": 1, "kind": "local_ai_enrichment_plan", "generated_at": "2026-05-04T20:45:15.029513+00:00", "repo_root": "C:/Users/carmi/blender/blender-audio-project", "objective": "Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker.", "task_file": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md", "profile": "npu", "basename": "full_context_golden_enrichment_plan", "apply_mode": "report_only", "provider_execution_performed": false, "source_writes_performed": false, "patch_application_performed": false, "complexity": { "level": "high", "score": 16, "matched_terms": [ "architecture", "broker", "context", "full-context", "gpu", "knowledge", "npu", "ollama", "patch", "provider" ], "task_text_chars_sampled": 8000 }, "lane_policy": { "primary_advisory...

### 2ceb4033da1ff042e86f - output/ai_pipeline/full_context_golden_enrichment_plan.json

- Kind: `source_file`
- Scope: `project`
- Score: `18.0`

{ "schema_version": 1, "kind": "local_ai_enrichment_plan", "generated_at": "2026-05-04T20:32:37.994981+00:00", "repo_root": "C:/Users/carmi/blender/blender-audio-project", "objective": "Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker.", "task_file": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md", "profile": "npu", "basename": "full_context_golden_enrichment_plan", "apply_mode": "report_only", "provider_execution_performed": false, "source_writes_performed": false, "patch_application_performed": false, "complexity": { "level": "high", "score": 16, "matched_terms": [ "architecture", "broker", "context", "full-context", "gpu", "knowledge", "npu", "ollama", "patch", "provider" ], "task_text_chars_sampled": 8000 }, "lane_policy": { "primary_advisory...

### 286c46e67169094fd008 - cli_note_1

- Kind: `operator_note`
- Scope: `task`
- Score: `6.0`

Unified launcher report-only run.

### 8afcda325efa964d05c6 - cli_note_1

- Kind: `operator_note`
- Scope: `task`
- Score: `6.0`

Local AI enrichment run. Preserve report-only defaults, explicit providers, NPU guardrail role and no patch apply.


## Guardrails

- `sqlite_read_only`: `True`
- `sqlite_db_committed`: `False`
- `memory_promotion_performed`: `False`
- `memory_delete_performed`: `False`
- `provider_execution_performed`: `False`
- `patch_application_performed`: `False`
- `blender_runtime_touched`: `False`

```

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agnostic_tool_inventory.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `823758`
- SHA-256: `797676999106037ed204637414dd5273e2aff9627c66137cadea3612b0104d29`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_agnostic_tool_inventory",
  "generated_at": "2026-05-06T00:43:01",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_read_only_inventory",
  "roots": [
    "Tools/ai",
    "Tools/validation",
    "Tools/workflow",
    "Tools/npu",
    "Tools/git",
    "Tools/repo_patch_runner"
  ],
  "summary": {
    "tool_count": 533,
    "category_counts": {
      "support_tool": 164,
      "validator": 161,
      "provider_probe_or_adapter": 116,
      "orchestrator_pipeline": 57,
      "agent_context_builder": 10,
      "proposal_or_review_builder": 10,
      "git_helper": 10,
      "review_helper": 5
    },
    "owner_lane_counts": {
      "cpu_support": 170,
      "npu_explicit_provider_tool": 134,
      "gpu_cuda_explicit_provider_tool": 102,
      "cpu_validation": 82,
      "cpu_orchestration": 34,
      "cpu_proposal_builder": 6,
      "cpu_context_builder": 5
    },
    "consumed_lane_counts": {
      "cpu": 533,
      "npu": 297,
      "gpu_cuda": 226
    },
    "apply_mode_counts": {
      "not_declared": 354,
      "report_only": 142,
      "manual_review_only": 21,
      "explicit_git_operation": 16
    },
    "provider_execution_default_counts": {
      "none_or_reported": 510,
      "explicit_only": 23
    }
  },
  "tools": [
    {
      "path": "Tools/ai/agent_memory_policy.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "cpu_support",
      "consumed_by_lanes": [
        "cpu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "not_declared",
      "lines": 307,
      "symbols": [
        "MemoryReview",
        "days_since",
        "detect_secret_patterns",
        "evaluate_memory_records",
        "kind_threshold",
        "load_records",
        "parse_datetime",
        "promotion_reason",
        "review_record",
        "to_dict",
        "write_memory_policy_markdown"
      ],
      "flags": [],
      "guardrails": [
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_memory_routing_policy.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 471,
      "symbols": [
        "build_discovery_tool_requests",
        "build_memory_tool_requests",
        "build_policy",
        "build_promotion_candidates",
        "default_operational_queries",
        "default_persistent_queries",
        "main",
        "now_iso",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "safe_id",
        "split_values",
        "tool_request"
      ],
      "flags": [
        "--broker-request-output",
        "--clear-operational",
        "--markdown-output",
        "--memory-search-limit",
        "--objective",
        "--operational-query",
        "--output",
        "--persistent-query",
        "--profile",
        "--promotion-candidate",
        "--remember-note",
        "--repo-root"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_review_warning_policy.py",
      "extension": ".py",
      "category": "review_helper",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 408,
      "symbols": [
        "as_int",
        "build_policy_report",
        "extract_existing_warnings",
        "extract_next_layer",
        "extract_reason",
        "final_decision_recovered",
        "infer_level",
        "is_final_authoritative",
        "load_report",
        "main",
        "now_iso",
        "render_markdown",
        "repo_rel",
        "resolve_path"
      ],
      "flags": [
        "--decision-report",
        "--final-report",
        "--markdown-output",
        "--min-patch-plans",
        "--min-recommendations",
        "--output",
        "--repo-root",
        "--report-file"
      ],
      "guardrails": [
        "patch_application_reported",
        "provider_execution_reported",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_runtime_sqlite_memory.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "cpu_support",
      "consumed_by_lanes": [
        "cpu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 527,
      "symbols": [
        "build_report",
        "clear_operational",
        "ensure_operational_db",
        "ensure_persistent_db",
        "is_under",
        "main",
        "now_iso",
        "operational_status",
        "parse_tags",
        "persistent_row_to_dict",
        "persistent_status",
        "remember_operational",
        "remember_persistent",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "row_to_dict",
        "safe_id",
        "search_operational",
        "search_persistent"
      ],
      "flags": [
        "--action",
        "--allow-persistent-write",
        "--confirm",
        "--content",
        "--database",
        "--limit",
        "--markdown-output",
        "--output",
        "--persistent-database",
        "--query",
        "--repo-root",
        "--request-id",
        "--role",
        "--scope",
        "--summary",
        "--tag"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 715,
      "symbols": [
        "ToolSpec",
        "base_outputs",
        "build_agent_agnostic_tool_inventory",
        "build_agent_memory_inventory",
        "build_agent_transient_request_context",
        "build_code_interpreter_report",
        "build_python_line_count_csv",
        "build_refactor_duplication_audit",
        "build_report",
        "check_python_syntax",
        "check_validation_report_contract",
        "compact_value",
        "execute_command",
        "execute_tool_request",
        "extract_tool_requests",
        "main",
        "now_iso",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "run_gpu_planner_json_contract_smoke",
        "runtime_sqlite_memory",
        "safe_id",
        "split_values",
        "truthy",
        "validate_request_args"
      ],
      "flags": [
        "--action",
        "--allow-persistent-write",
        "--bundle-smoke-report",
        "--code-interpreter-report",
        "--confirm",
        "--content",
        "--csv-output",
        "--database",
        "--dry-run",
        "--exclude-dir",
        "--input",
        "--input-audit-report",
        "--limit",
        "--line-count-report",
        "--markdown-output",
        "--memory-db",
        "--memory-note",
        "--memory-routing-report",
        "--objective",
        "--output",
        "--persistent-database",
        "--python-syntax-report",
        "--query",
        "--raw-file",
        "--repo-root",
        "--report",
        "--report-dir",
        "--report-file",
        "--report-output",
        "--request-file",
        "--request-id",
        "--role",
        "--root",
        "--scope",
        "--stamp",
        "--summary",
        "--tag",
        "--timeout-seconds",
        "--tool-output-dir"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "no_blender_runtime",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/agent_state.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "gpu_cuda_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "not_declared",
      "lines": 544,
      "symbols": [
        "AgentMicroTask",
        "MemoryRecord",
        "append_memory_jsonl",
        "build_agent_state_packet",
        "clamp_confidence",
        "compact_text",
        "default_microtasks",
        "ensure_memory_db",
        "from_mapping",
        "from_text",
        "json_or_default",
        "keywords",
        "load_memory_db",
        "load_memory_jsonl",
        "read_text",
        "records_from_files",
        "relative_path",
        "score_record",
        "select_memory",
        "sha256_text",
        "slugify",
        "stable_tag_tuple",
        "to_dict",
        "upsert_memory_db",
        "utc_now_iso",
        "write_agent_state_markdown"
      ],
      "flags": [],
      "guardrails": [
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "extension": ".py",
      "category": "provider_probe_or_adapter",
      "owner_lane": "npu_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 580,
      "symbols": [
        "analyze",
        "audit_duration_seconds",
        "build_operational_opinions",
        "build_performance_summary",
        "build_refactoring_suggestions",
        "build_suggestions",
        "collect_round_field_durations",
        "compact_performance_source",
        "duration_from_timestamps",
        "elapsed_seconds",
        "extract_gpu_round_durations",
        "extract_round_duration_alias",
        "first_int",
        "has_real_gpu_round_timing",
        "list_of_dicts",
        "main",
        "nested_dict",
        "now_iso",
        "numeric_round_field",
        "parse_iso_seconds",
        "percentile",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "rounded_sum",
        "runtime_tool_counters",
        "safe_float",
        "safe_int",
        "summarize_gpu_timing",
        "summarize_npu_timing"
      ],
      "flags": [
        "--markdown-output",
        "--orchestrator",
        "--output",
        "--repo-root"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/apply_full0to10_auto_refactor_patch_specs.py",
      "extension": ".py",
      "category": "proposal_or_review_builder",
      "owner_lane": "cpu_proposal_builder",
      "consumed_by_lanes": [
        "cpu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "not_declared",
      "lines": 49,
      "symbols": [
        "main",
        "parse_args"
      ],
      "flags": [
        "--apply",
        "--markdown-output",
        "--max-specs",
        "--output",
        "--patch-specs",
        "--repo-root"
      ],
      "guardrails": []
    },
    {
      "path": "Tools/ai/apply_full0to10_markdown_split_patch_specs.py",
      "extension": ".py",
      "category": "proposal_or_review_builder",
      "owner_lane": "cpu_proposal_builder",
      "consumed_by_lanes": [
        "cpu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "not_declared",
      "lines": 53,
      "symbols": [
        "main",
        "parse_args"
      ],
      "flags": [
        "--apply-shadow",
        "--markdown-output",
        "--max-specs",
        "--output",
        "--patch-specs",
        "--repo-root",
        "--shadow-root"
      ],
      "guardrails": []
    },
    {
      "path": "Tools/ai/artifact_domain_registry.py",
      "extension": ".py",
      "category": "support_tool",
      "owner_lane": "cpu_support",
      "consumed_by_lanes": [
        "cpu",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 217,
      "symbols": [
        "ArtifactDomain",
        "get_domain",
        "list_domains",
        "registry_guardrails",
        "registry_report",
        "to_report_dict",
        "validate_domain",
        "validate_registry"
      ],
      "flags": [],
      "guardrails": [
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/build_agent_agnostic_tool_inventory.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "npu_explicit_provider_tool",
      "consumed_by_lanes": [
        "cpu",
        "gpu_cuda",
        "npu"
      ],
      "provider_execution_default": "explicit_only",
      "apply_mode": "manual_review_only",
      "lines": 408,
      "symbols": [
        "ToolRecord",
        "apply_mode",
        "build_inventory",
        "build_reco
```

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agnostic_tool_inventory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `16334`
- SHA-256: `d9aba39a90b66356926f8625a3f696ca3197f0dff63197e86cc59f374c57ae38`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Agnostic Tool Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Tool count: `533`

## category_counts

- `support_tool`: 164
- `validator`: 161
- `provider_probe_or_adapter`: 116
- `orchestrator_pipeline`: 57
- `agent_context_builder`: 10
- `proposal_or_review_builder`: 10
- `git_helper`: 10
- `review_helper`: 5

## owner_lane_counts

- `cpu_support`: 170
- `npu_explicit_provider_tool`: 134
- `gpu_cuda_explicit_provider_tool`: 102
- `cpu_validation`: 82
- `cpu_orchestration`: 34
- `cpu_proposal_builder`: 6
- `cpu_context_builder`: 5

## consumed_lane_counts

- `cpu`: 533
- `npu`: 297
- `gpu_cuda`: 226

## apply_mode_counts

- `not_declared`: 354
- `report_only`: 142
- `manual_review_only`: 21
- `explicit_git_operation`: 16

## provider_execution_default_counts

- `none_or_reported`: 510
- `explicit_only`: 23

## Categories

### support_tool

- `Tools/ai/agent_memory_policy.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/agent_memory_routing_policy.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/agent_runtime_sqlite_memory.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/agent_runtime_tool_broker.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/artifact_domain_registry.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_code_interpreter_report.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_code_patch_artifact_pack.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_code_patch_docs_followup.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_dry_run_matrix_evidence_bundle.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_accelerator_control.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_auto_refactor_plan.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_effective_use_optimization.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_final_product_quality_package.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_final_tool_product.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_hardware_tool_capability.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_light_profile_promotion.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_memory_visibility_assertion.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_quality_gate.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_quality_stack_summary.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_repo_quality_packet.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`

### review_helper

- `Tools/ai/agent_review_warning_policy.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/refine_megalithic_review_signals.py` lane=`gpu_cuda_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/review_agent_memory.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/review_wave_entrypoints.py` lane=`cpu_support` apply=`not_declared` provider=`explicit_only`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`explicit_only`

### agent_context_builder

- `Tools/ai/agent_state.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_agent_agnostic_tool_inventory.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/build_agent_memory_inventory.py` lane=`cpu_context_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_code_patch_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_evidence_sufficiency.py` lane=`cpu_context_builder` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_patch_bundle.py` lane=`cpu_context_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_review_patch_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_agent_state_packet.py` lane=`cpu_context_builder` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_agent_transient_request_context.py` lane=`cpu_context_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_ai_context_pack.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`

### provider_probe_or_adapter

- `Tools/ai/analyze_gpu_npu_run_sync.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_analysis_input_bundle.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_deterministic_recommendations.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_full0to10_provider_execution_bridge.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_provider_governor.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_provider_invocation_plan.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_provider_telemetry_semantic_validation.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_full0to10_provider_tool_feedback_loop.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_local_ai_enrichment_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_selective_execution_plan.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_workload_quality_lane_routing.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/builder.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/constants.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/device_visibility.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/gpu_body.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/npu_auditor.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/render.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/scheduler.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_auto_refactor/constants.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_auto_refactor/hardware.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`

### proposal_or_review_builder

- `Tools/ai/apply_full0to10_auto_refactor_patch_specs.py` lane=`cpu_proposal_builder` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/apply_full0to10_markdown_split_patch_specs.py` lane=`cpu_proposal_builder` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_code_edit_proposal_from_plan.py` lane=`cpu_proposal_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_full_context_golden_proposals.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_megalithic_review_pr_draft.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_patch_specs_from_proposals.py` lane=`cpu_proposal_builder` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_repository_change_proposals.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/code_edit_proposal_helpers.py` lane=`cpu_proposal_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/full0to10_auto_refactor/patch_specs.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/promote_patch_spec_draft.py` lane=`cpu_proposal_builder` apply=`manual_review_only` provider=`none_or_reported`

### validator

- `Tools/ai/build_full0to10_track_input_contract.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/check_local_resource_lanes.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/check_npu_provider_environment.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/full0to10_accelerator_control/gpu0_contract.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_effective_use/provider_contracts.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_provider_invocation_plan/telemetry_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/full0to10_provider_invocation_plan/workload_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/full0to10_track_inputs/contract.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/gpu_planner_json_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/artifact_contracts.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/replay_gpu_planner_json_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/ai_pipeline_report_contracts.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/__init__.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/classifier.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/constants.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/metrics.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/paths.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/reporter.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/roles.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/ai_workload_quality/selector.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`

### git_helper

- `Tools/ai/build_github_evidence_bundle.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/enrich_github_evidence_bundle_code_plan.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_artifacts.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_decisions.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_io.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_markdown.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/github_evidence_bundle_reports.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/git/auto_push_generated_artifacts.ps1` lane=`cpu_support` apply=`explicit_git_operation` provider=`none_or_reported`
- `Tools/git/auto_push_generated_data.ps1` lane=`cpu_support` apply=`explicit_git_operation` provider=`none_or_reported`

### orchestrator_pipeline

- `Tools/workflow/ai_runtime_diagnostics.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/artifact_consult.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/asset_inventory.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/git_auto_push.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/__init__.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/action_panel.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/
```

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_transient_request_context.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `9186`
- SHA-256: `f0ae0042e9f36109add4b4cf30063c06e4d48fa5d28a802562a0f64802a134b9`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_transient_request_context",
  "generated_at": "2026-05-06T00:43:08",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_request_scoped_context",
  "objective": "Full memory/tool regeneration context for IA-Carmine.",
  "scope": "current_request_only",
  "persistence": {
    "persistent_memory_write_performed": false,
    "sqlite_write_performed": false,
    "promotion_performed": false,
    "delete_performed": false,
    "commit_allowed": false
  },
  "memory_notes": [
    {
      "id": "note-001",
      "chars": 103,
      "sha256": "e3cdb479d3d06dee65b82388340a38bd07df73f9e1ffdffedcb5a04e764f9a6a",
      "content": "Persistent memory is read-only. Operational memory is scratch. Runtime tools are brokered by allowlist."
    }
  ],
  "raw_context": {
    "file_count": 0,
    "total_chars": 0,
    "max_files": 80,
    "max_chars_per_file": 12000,
    "files": []
  },
  "report_context": {
    "file_count": 6,
    "reports": [
      {
        "path": "output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agent_memory_inventory.json",
        "exists": true,
        "kind": "agent_memory_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "guardrails": {
            "sqlite_read_only": true,
            "sqlite_db_committed": false,
            "memory_promotion_performed": false,
            "memory_delete_performed": false,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false
          },
          "inputs": {
            "memory_db": "indexAI/agent_memory/agent_memory.sqlite",
            "memory_db_exists": true,
            "memory_jsonl": [],
            "memory_db_limit": 1000,
            "max_memory_chars": 24000
          }
        }
      },
      {
        "path": "output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "summary": {
            "tool_count": 533,
            "category_counts": {
              "support_tool": 164,
              "validator": 161,
              "provider_probe_or_adapter": 116,
              "orchestrator_pipeline": 57,
              "agent_context_builder": 10,
              "proposal_or_review_builder": 10,
              "git_helper": 10,
              "review_helper": 5
            },
            "owner_lane_counts": {
              "cpu_support": 170,
              "npu_explicit_provider_tool": 134,
              "gpu_cuda_explicit_provider_tool": 102,
              "cpu_validation": 82,
              "cpu_orchestration": 34,
              "cpu_proposal_builder": 6,
              "cpu_context_builder": 5
            },
            "consumed_lane_counts": {
              "cpu": 533,
              "npu": 297,
              "gpu_cuda": 226
            },
            "apply_mode_counts": {
              "not_declared": 354,
              "report_only": 142,
              "manual_review_only": 21,
              "explicit_git_operation": 16
            },
            "provider_execution_default_counts": {
              "none_or_reported": 510,
              "explicit_only": 23
            }
          },
          "guardrails": {
            "report_only": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "sqlite_db_touched": false,
            "blender_runtime_touched": false,
            "real_github_pr_created": false,
            "output_artifacts_should_not_be_committed": true
          }
        }
      },
      {
        "path": "output/validation/full_memory_tool_regeneration_20260506-004242_persistent_memory_status.json",
        "exists": true,
        "kind": "agent_runtime_sqlite_memory",
        "passed": true,
        "error": "",
        "summary": {
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
        }
      },
      {
        "path": "output/validation/full_memory_tool_regeneration_20260506-004242_operational_memory_status.json",
        "exists": true,
        "kind": "agent_runtime_sqlite_memory",
        "passed": true,
        "error": "",
        "summary": {
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
        }
      },
      {
        "path": "output/validation/full_memory_tool_regeneration_20260506-004242_memory_routing_policy.json",
        "exists": true,
        "kind": "agent_memory_routing_policy",
        "passed": true,
        "error": "",
        "summary": {
          "decision": {
            "use_persistent_memory_for": [
              "validated durable project facts",
              "guardrails",
              "historical lessons",
              "stable architecture state"
            ],
            "use_operational_memory_for": [
              "current run state",
              "temporary planner notes",
              "tool results",
              "hypotheses not yet validated"
            ],
            "promotion_policy": "manual_review_after_evidence_only",
            "next_layer": "agent_runtime_tool_broker"
          },
          "guardrails": {
            "free_shell_allowed": false,
            "broker_allowlist_required": true,
            "persistent_memory_read_only": true,
            "persistent_memory_write_performed": false,
            "sqlite_write_performed": false,
            "operational_memory_write_allowed_under_output": true,
            "automatic_persistent_promotion_allowed": false,
            "manual_review_required_for_promotion": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false,
            "git_write_performed": false
          }
        }
      },
      {
        "path": "output/validation/full_memory_tool_regeneration_20260506-004242_runtime_tool_broker.json",
        "exists": true,
        "kind": "agent_runtime_tool_broker",
        "passed": true,
        "error": "",
        "summary": {
          "guardrails": {
            "free_shell_exposed": false,
            "allowlist_enforced": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "sqlite_write_performed": false,
            "persistent_memory_write_performed": false,
            "operational_sqlite_write_allowed_under_output": true,
            "operational_sqlite_write_performed": true,
            "operational_memory_clear_count": 0,
            "blender_runtime_touched": false,
            "git_write_performed": false,
            "manual_review_required": true
          }
        }
      }
    ]
  },
  "integration": {
    "compatible_with_megalithic_review": true,
    "compatible_with_core_activation": true,
    "recommended_as_report_file": true,
    "request_scoped": true
  },
  "guardrails": {
    "report_only": true,
    "request_scoped": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "persistent_memory_write_performed": false,
    "sqlite_write_performed": false,
    "blender_runtime_touched": false,
    "real_github_pr_created": false,
    "output_artifacts_should_not_be_committed": true
  }
}

```

### `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_transient_request_context.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1754`
- SHA-256: `1ba714409870e0156a21f2cf634d0138237ba82a9300eb7aefed4a98ba925461`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Transient Request Context

- Scope: `current_request_only`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Persistent memory write: `False`
- SQLite write: `False`
- Memory notes: `1`
- Raw files: `0`
- Report refs: `6`

## Memory notes

### note-001

Persistent memory is read-only. Operational memory is scratch. Runtime tools are brokered by allowlist.

## Report context

- `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agent_memory_inventory.json` kind=`agent_memory_inventory` passed=`True` error=``
- `output/ai_pipeline/full_memory_tool_regeneration_20260506-004242_agnostic_tool_inventory.json` kind=`agent_agnostic_tool_inventory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260506-004242_persistent_memory_status.json` kind=`agent_runtime_sqlite_memory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260506-004242_operational_memory_status.json` kind=`agent_runtime_sqlite_memory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260506-004242_memory_routing_policy.json` kind=`agent_memory_routing_policy` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260506-004242_runtime_tool_broker.json` kind=`agent_runtime_tool_broker` passed=`True` error=``

## Guardrails

- `report_only`: `True`
- `request_scoped`: `True`
- `provider_execution_performed`: `False`
- `patch_application_performed`: `False`
- `persistent_memory_write_performed`: `False`
- `sqlite_write_performed`: `False`
- `blender_runtime_touched`: `False`
- `real_github_pr_created`: `False`
- `output_artifacts_should_not_be_committed`: `True`

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
- Total selected chars: `24080`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
