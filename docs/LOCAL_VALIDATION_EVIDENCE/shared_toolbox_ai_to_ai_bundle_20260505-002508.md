# Local Validation Evidence Bundle

- Generated at: `2026-05-05T00:32:05`
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

### `output/ai_pipeline/full_toolbox_20260505-002508_agent_review_decision_loop.json`

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

### `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json`

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

### `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `20`

### `output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json`

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
- Source writes performed: `False`
- Usable lanes: `['npu']`
- Unusable lanes: `[]`
- Warnings: `['ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_usage_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_capability_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_final_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Errors: `['ollama: probe failed']`
- Warnings: `['patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection', 'max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/docs_links_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `docs_links`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_operational_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_persistent_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_python_line_count.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_python_syntax.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_20260505-002508_runtime_tool_broker.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_runtime_tool_broker_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260505-002508_validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_20260505-002508_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `markdown_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['This inventory is evidence for review. It does not delete or rewrite Markdown files.', 'A missing index reference is not automatically obsolete; it means the file needs owner/lifecycle review.', 'GitHub templates and root community docs are repository controls, not prune candidates.']`

### `output/validation/npu_provider_environment_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_line_count_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/repository_consistency_map_smoke_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/runtime_tool_bootstrap_requests_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_bootstrap_requests`
- Passed: `None`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/runtime_tool_broker_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `script_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/validation_report_contract_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/validation_report_contract_json_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/analysis/code_interpreter_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `159`

### `output/analysis/full_memory_tool_regeneration_20260505-002508_code_interpreter.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `140`

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/repository_consistency_map_full_toolbox_20260505-002508.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agent_memory_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agnostic_tool_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_agnostic_tool_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_transient_request_context.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_transient_request_context`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Patch plan summary

### `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json`

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
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_002 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_003 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_004 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_005 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_006 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_007 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_008 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `app.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_009 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_010 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_011 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_012 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_013 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_014 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_015 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_016 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_017 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1325` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1325`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_018 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1326` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1326`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_019 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1333` targeting `app.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1333`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_020 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1334` targeting `app.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1334`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_20260505-002508_agent_review_decision_loop.json` exists=`True` size=`2868` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json` exists=`True` size=`291484` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json` exists=`True` size=`188679` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json` exists=`True` size=`13341` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json` exists=`True` size=`22632` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json` exists=`True` size=`95305` suffix=`.json` preview_chars=`1500`
- `output/validation/local_provider_probe.json` exists=`True` size=`2528` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_workload_report_quality.json` exists=`True` size=`2743` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json` exists=`True` size=`10546` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260505-002508.json` exists=`True` size=`13989` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260505-002508.json` exists=`True` size=`1028707` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-002508.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-002508.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/docs_links_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json` exists=`True` size=`154286` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy.json` exists=`True` size=`8925` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy_smoke.json` exists=`True` size=`2972` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_operational_memory_status.json` exists=`True` size=`1702` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_persistent_memory_status.json` exists=`True` size=`1779` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_python_line_count.json` exists=`True` size=`3189` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_python_syntax.json` exists=`True` size=`38308` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_runtime_tool_broker.json` exists=`True` size=`98114` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_runtime_tool_broker_smoke.json` exists=`True` size=`2001` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_validation_report_contract.json` exists=`True` size=`3417` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-002508_workflow.json` exists=`True` size=`4921` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-002508.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json` exists=`True` size=`315785` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_provider_environment_full_toolbox_20260505-002508.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_20260505-002508.json` exists=`True` size=`3159` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_20260505-002508.json` exists=`True` size=`38308` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_20260505-002508.json` exists=`True` size=`1199` suffix=`.json` preview_chars=`1160`
- `output/validation/runtime_tool_bootstrap_requests_20260505-002508.json` exists=`True` size=`2022` suffix=`.json` preview_chars=`1500`
- `output/validation/runtime_tool_broker_full_toolbox_20260505-002508.json` exists=`True` size=`28063` suffix=`.json` preview_chars=`1500`
- `output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json` exists=`True` size=`341305` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json` exists=`True` size=`2024` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_json_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_20260505-002508.json` exists=`True` size=`1303` suffix=`.json` preview_chars=`1256`
- `output/analysis/code_interpreter_full_toolbox_20260505-002508.json` exists=`True` size=`1464242` suffix=`.json` preview_chars=`1500`
- `output/analysis/full_memory_tool_regeneration_20260505-002508_code_interpreter.json` exists=`True` size=`1281883` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-002508.json` exists=`True` size=`14368` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-002508.json` exists=`True` size=`5622` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_20260505-002508.json` exists=`True` size=`6540351` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agent_memory_inventory.json` exists=`True` size=`13178` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agnostic_tool_inventory.json` exists=`True` size=`560563` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_transient_request_context.json` exists=`True` size=`9178` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15584`
- SHA-256: `302c2f4ff41c5fc4b144ac175a9d40383b992aebad14c1cd722bd71c1a3a1fe3`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Runtime Toolbox AI-to-AI Next Task — 2026-05-03

## Purpose

Use this Markdown as the next official task request for the local IA-Carmine pipeline.

This is not a generic procedure. It is a concrete AI-to-AI handoff request from ChatGPT to the local IA. The local IA should read this file as the task input, use the committed evidence bundle as context, run only safe/report-only tooling unless explicitly configured otherwise, and produce a compact evidence bundle for review.

## Repository baseline

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
current reference commit: eb5ec1d test(ai): add shared runtime toolbox evidence bundle
project: IA-Carmine
workflow: ChatGPT -> MD task -> local IA -> reports/bundle -> GitHub evidence -> ChatGPT review
```

Required sync before running:

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

Expected:

```text
git status --short is empty
HEAD is master/origin/master
```

## Evidence to read first

Read these committed files before planning:

```text
docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md
docs/LOCAL_AI_TASKS/full-memory-tool-regeneration-procedure.md
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_20260503-011858.json
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_20260503-011858.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_20260503-011858.csv
```

The evidence bundle indicates a successful full-refactor regeneration after the shared runtime toolbox work:

```text
passed=True
profile=full_refactor
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
report_count=13
artifact_count=14
errors={}
```

## Architecture to validate

The target architecture is:

```text
GPU -> tool_requests -> orchestrator -> broker -> report
NPU -> tool_requests -> orchestrator -> broker -> report

provider -> never direct executor
orchestrator -> control-plane / routing / scheduling
broker -> only controlled executor
report -> reinjected read-only evidence
```

Design rule:

```text
Providers ask.
Orchestrator decides.
Broker executes.
Reports become evidence.
```

## Available runtime tools

The current runtime tool contract allowlist contains these tool names:

```text
build_python_line_count_csv
build_agent_memory_inventory
build_agent_agnostic_tool_inventory
build_agent_transient_request_context
check_python_syntax
check_validation_report_contract
run_gpu_planner_json_contract_smoke
build_code_interpreter_report
runtime_sqlite_memory
```

All requests for these tools must use structured `tool_requests` and must be executed only through the orchestrator/broker path in orchestrated runs.

### Tool capabilities in this context

#### `build_python_line_count_csv`

Use to build deterministic Python inventory.

Possible uses:

```text
- detect largest Python modules after recent orchestration refactors
- compare line-count drift across Tools/ai, Tools/validation, Tools/workflow, Tools/npu
- prepare compact CSV evidence for ChatGPT review
```

Example tool request:

```json
{
  "id": "request_python_line_count_shared_toolbox",
  "tool": "build_python_line_count_csv",
  "reason": "Build a fresh Python line-count inventory to identify large files after shared toolbox orchestration changes.",
  "args": {}
}
```

#### `build_agent_memory_inventory`

Use to summarize durable project memory state.

Possible uses:

```text
- verify persistent memory contains the new shared-toolbox architecture state
- detect stale memory assumptions about GPU direct broker execution
- prepare a memory state summary for handoff bundles
```

Example tool request:

```json
{
  "id": "request_memory_inventory_shared_toolbox",
  "tool": "build_agent_memory_inventory",
  "reason": "Check durable project memory for shared runtime toolbox architecture alignment.",
  "args": {}
}
```

#### `build_agent_agnostic_tool_inventory`

Use to inventory local IA tools without making provider-specific assumptions.

Possible uses:

```text
- list report-only tools available to the local IA
- confirm broker/orchestrator validation tools are discoverable
- detect missing or duplicated tool capabilities
```

Example tool request:

```json
{
  "id": "request_agnostic_tool_inventory_shared_toolbox",
  "tool": "build_agent_agnostic_tool_inventory",
  "reason": "Inventory available report-only tools for the shared toolbox control-plane.",
  "args": {}
}
```

#### `build_agent_transient_request_context`

Use to assemble a request-scoped context packet.

Possible uses:

```text
- combine this MD, architecture docs and compact evidence into a local IA context packet
- provide a smaller context surface for GPU/NPU runs
- preserve task intent without relying on chat history
```

Example tool request:

```json
{
  "id": "request_transient_context_shared_toolbox",
  "tool": "build_agent_transient_request_context",
  "reason": "Build a transient request context from the shared toolbox handoff and evidence bundle.",
  "args": {
    "objective": "Validate the shared runtime toolbox architecture and produce next-step evidence."
  }
}
```

#### `check_python_syntax`

Use as source safety gate.

Possible uses:

```text
- verify all Python files still compile after recent orchestrator/broker work
- gate any future patch plan before commit
- catch accidental syntax regressions in Tools/ai and Tools/validation
```

Example tool request:

```json
{
  "id": "request_python_syntax_shared_toolbox",
  "tool": "check_python_syntax",
  "reason": "Validate Python syntax before recommending any shared toolbox follow-up.",
  "args": {}
}
```

#### `check_validation_report_contract`

Use to validate generated JSON report contracts.

Possible uses:

```text
- check reports generated by GPU/NPU orchestration and broker smoke tools
- catch missing guardrail fields or malformed report metadata
- validate compact evidence inputs before bundling
```

Example tool request:

```json
{
  "id": "request_validation_contract_shared_toolbox",
  "tool": "check_validation_report_contract",
  "reason": "Validate generated report contracts for the shared toolbox AI-to-AI run.",
  "args": {}
}
```

#### `run_gpu_planner_json_contract_smoke`

Use to validate provider output contract handling without running a real provider.

Possible uses:

```text
- confirm GPU/NPU tool_requests schema remains valid
- verify empty/invalid model output classifications
- ensure tool request allowlist enforcement remains stable
```

Example tool request:

```json
{
  "id": "request_gpu_contract_smoke_shared_toolbox",
  "tool": "run_gpu_planner_json_contract_smoke",
  "reason": "Verify the GPU planner JSON/tool request contract before any provider run.",
  "args": {}
}
```

#### `build_code_interpreter_report`

Use for static/code-structure report generation.

Possible uses:

```text
- identify refactor opportunities in orchestration/broker code
- detect duplicated helpers between Tools/ai and Tools/validation
- produce recommendations without applying patches
```

Example tool request:

```json
{
  "id": "request_code_interpreter_shared_toolbox",
  "tool": "build_code_interpreter_report",
  "reason": "Analyze AI tooling code for next shared-toolbox refactor opportunities without applying patches.",
  "args": {
    "inputs": ["Tools/ai", "Tools/validation", "Tools/workflow", "Tools/npu"]
  }
}
```

#### `runtime_sqlite_memory`

Use only through controlled actions and scopes.

Possible uses:

```text
- read persistent memory status
- read/search operational scratch state
- confirm no unauthorized persistent writes occurred
- prepare memory-routing evidence
```

Allowed safe request patterns:

```json
{
  "id": "request_persistent_memory_status_shared_toolbox",
  "tool": "runtime_sqlite_memory",
  "reason": "Check persistent memory status in read-only mode.",
  "args": {
    "action": "status",
    "scope": "persistent"
  }
}
```

```json
{
  "id": "request_operational_memory_status_shared_toolbox",
  "tool": "runtime_sqlite_memory",
  "reason": "Check operational scratch memory status for current run context.",
  "args": {
    "action": "status",
    "scope": "operational"
  }
}
```

Do not write persistent memory unless the user explicitly authorizes a controlled persistent-memory write task.

## Requests to execute in this AI-to-AI cycle

The local IA should answer these requests using evidence, reports and brokered tool execution. It should not guess from model memory alone.

### Request 1 — Toolbox availability summary

Produce a technical summary of available runtime tools and explain what each tool can do in the shared toolbox architecture.

Required output fields:

```text
tool_name
category
safe_default_mode
what_it_can_do
what_it_must_not_do
recommended_next_use
```

### Request 2 — Architecture conformance audit

Audit whether the current repository matches the target model:

```text
GPU -> tool_requests -> orchestrator -> broker -> report
NPU -> tool_requests -> orchestrator -> broker -> report
```

Use current code and smoke reports. Identify any remaining asymmetry between GPU and NPU lanes.

### Request 3 — Tool request examples

Generate at least 10 valid tool request examples relevant to this project.

The examples must include:

```text
- 2 inventory requests
- 2 validation requests
- 2 memory/status requests
- 2 context/evidence requests
- 2 code/refactor analysis requests
```

Each example must include:

```text
id
tool
reason
args
expected_report
risk
stop_condition
```

### Request 4 — Next safe automation candidate

Recommend the next safe automation/refactor step after the shared toolbox architecture.

Allowed recommendation types:

```text
ready_for_patch_plan
needs_more_context
advisory_only
```

Do not recommend automatic patch application. If code changes are recommended, produce a manual-review patch-plan target only.

### Request 5 — Evidence bundle plan

Propose the exact compact evidence bundle to return to ChatGPT.

The plan must list:

```text
reports to include
artifacts to include
bundle basename
validation command
commit policy
```

## Recommended local commands

Start with no-provider/report-only validation:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

python .\Tools\validation\run_orchestrator_gpu_runtime_tool_routing_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_gpu_routing_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_ai_to_ai_gpu_routing_$Stamp.md"

python .\Tools\validation\run_npu_runtime_tool_execution_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_npu_execution_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_ai_to_ai_npu_execution_$Stamp.md"

python .\Tools\validation\run_npu_tool_request_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_npu_contract_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_ai_to_ai_npu_contract_$Stamp.md"
```

Then run static evidence:

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_ai_to_ai_python_syntax_$Stamp.json"

python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/workflow `
  --input Tools/npu `
  --output ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.json" `
  --markdown-output ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.md"
```

Optional provider run may be executed only if explicitly requested by the user.

## Expected final local outputs

The local IA should produce these runtime outputs:

```text
output/validation/shared_toolbox_ai_to_ai_gpu_routing_<STAMP>.json
output/validation/shared_toolbox_ai_to_ai_npu_execution_<STAMP>.json
output/validation/shared_toolbox_ai_to_ai_npu_contract_<STAMP>.json
output/validation/shared_toolbox_ai_to_ai_python_syntax_<STAMP>.json
output/analysis/shared_toolbox_ai_to_ai_code_interpreter_<STAMP>.json
output/analysis/shared_toolbox_ai_to_ai_code_interpreter_<STAMP>.md
```

Then it should build compact evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md
```

Do not commit raw `output/**` artifacts.

## Compact bundle command template

```powershell
$Reports = @(
  ".\output\validation\shared_toolbox_ai_to_ai_gpu_routing_$Stamp.json",
  ".\output\validation\shared_toolbox_ai_to_ai_npu_execution_$Stamp.json",
  ".\output\validation\shared_toolbox_ai_to_ai_npu_contract_$Stamp.json",
  ".\output\validation\shared_toolbox_ai_to_ai_python_syntax_$Stamp.json",
  ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.json"
) | Where-Object { Test-Path $_ }

python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename "shared_toolbox_ai_to_ai_bundle_$Stamp" `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact ".\docs\LOCAL_AI_TASKS\shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\shared-runtime-toolbox-orchestration-architecture.md" `
  --artifact ".\output\analysis\shared_toolbox_ai_to_ai_code_interpreter_$Stamp.md" `
  --max-included-artifact-chars 14000 `
  --max-included-artifacts 40
```

## Bundle validation

If bundle validation tooling is available, validate the compact bundle before commit:

```powershell
python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL
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

### `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `19406`
- SHA-256: `9feb9a1aa3f8781195c6b8e3ff99a8d7d01bfdc20b19c5a1167a6f144ab5f562`
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

- `orchestrator`: `output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json`
- `orchestrator_kind`: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- `evidence_kind`: `agent_review_evidence_sufficiency`
- `gpu_kind`: `deterministic_recommendation_synthesizer`

## Patch plans

### consistency_001 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_003 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_005 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `app.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_013 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_014 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_015 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mappe
```

### `output/ai_pipeline/full_toolbox_20260505-002508_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1280`
- SHA-256: `29563ca1c4c067c84eff6325fced960f3a0bc6657b10fd781ae2963c36fb426f`
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

- `recommendations`: `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json` exists=`True` size=`188679`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.md` exists=`True` size=`19806`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json` exists=`True` size=`13341`
- `patch_plan`: `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json` exists=`True` size=`291484`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.md` exists=`True` size=`19406`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `19806`
- SHA-256: `afcc266515a83be4083c71b5e13f9a856433f249850de458431611296146f176`
- Content included: `True`
- Content truncated: `True`

```text
# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `20`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `context_echo_detected`
- Evidence ready for manual patch count: `0`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### consistency_001 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_003 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_005 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:246`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `app.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1120`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1123`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1140`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1143`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_013 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1201`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_014 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1203`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_015 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_
```

### `output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2449`
- SHA-256: `10bc025f7c6b2fa85ef4bec4cb0c137c8015a5a68c283f7715c79caf3676306f`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `342.107`
- `npu_audit_count`: `3`
- `npu_audit_success_count`: `3`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `gpu_evidence_ready_for_manual_patch_count`: `0`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `44`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `3`
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
- `gpu_empty_recommendations_reason`: `context_echo_detected`
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
- round `4` status=`finished` class=`usable_audit_text` success=`True`
- round `8` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1045`
- SHA-256: `731e6808d28c16347337af52455747f072d3657933d59bbc6d1765c19d0e24d5`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `323.984`
- Round count: `13`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `0`
- Context echo detected count: `2`
- Model output schema mismatch count: `13`
- Empty recommendations reason: `context_echo_detected`
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

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1218`
- SHA-256: `8b18da054a9558435b43bbd2657641995d1984914032c6b8daee40b05ad36423`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `20260505-002508`
- Tool call entries: `3`
- Executed count: `3`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `0.0`
- Declared runtime tool requests: `44`
- Broker runtime tool executions: `0`
- Declared not executed count: `44`

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

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7655`
- SHA-256: `0836a414dbba45b531d4624ecef0ff652bc11fc1b13184a263a95dfb76d8624f`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Capability Manifest

- Passed: `True`
- Tool count: `10`
- Declared runtime tool requests: `44`
- Broker runtime tool executions: `0`
- Declared not executed count: `44`
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
- `Tools/ai/build_runtime_tool_usage_telemetry.py` role=`runtime_tool_usage_telemetry_builder` exists=`True` sha256=`94af9f4e8331609fcb6fc568f5ca19d2eca13262c7909044e6b8df5ae2f873be`
- `Tools/ai/build_semantic_evidence_chunks.py` role=`semantic_cloud_handoff_chunker` exists=`True` sha256=`5fdcbc74f6eb931f3b95c6b54b1eb1071e57f8f41a34c694864b3ac8cdab80f7`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` role=`shared_toolbox_bundle_builder` exists=`True` sha256=`402d10af697ed9b9b19e1a44aabaee9a3c9eff5763995088327f6b2e3dbc0ab8`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json` role=`observed_runtime_tool_usage_report` exists=`True` sha256=`716a43051b087034263821a001144ec2a356c32d595c6d3bba9dd7ad3943e9d2`

```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `314843`
- SHA-256: `6e292147bc1172828d5c705c93a08a6b9e7ce470b2dc115ef20822aa2475d5fd`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: 20260505-002508
- passed: True
- provider_execution_performed: True
- patch_application_performed: False
- source_writes_performed: False
- sqlite_write_performed: False
- persistent_memory_write_performed: False
- blender_runtime_execution_performed: False

## Provider diagnostics

- Provider execution seen: `True`
- GPU primary advisory succeeded: `False`
- Provider failure detected: `True`
- Deterministic recovery used: `True`
- `output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json` kind=`agent_gpu_npu_parallel_orchestrator` passed=`True` provider_execution_performed=`True` errors=`[]`
- `output/validation/local_provider_probe.json` kind=`local_provider_probe` passed=`False` provider_execution_performed=`True` errors=`['ollama: probe failed']`
- `output/validation/ai_workload_report_quality.json` kind=`ai_workload_report_quality` passed=`True` provider_execution_performed=`False` errors=`[]`

## Patch plan summary

- Seen: `True`
- Source: `output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json`
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

- output/ai_pipeline/full_toolbox_20260505-002508_agent_review_decision_loop.json exists=True json_ok=True kind=agent_review_decision_loop passed=True
- output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json exists=True json_ok=True kind=agent_review_patch_plan passed=True
- output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer passed=True
- output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json exists=True json_ok=True kind=deterministic_recommendation_patch_plan_bridge_orchestrator passed=True
- output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json exists=True json_ok=True kind=agent_gpu_npu_parallel_orchestrator passed=True
- output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json exists=True json_ok=True kind=agent_gpu_deep_planning_supervised passed=True
- output/validation/local_provider_probe.json exists=True json_ok=True kind=local_provider_probe passed=False
- output/validation/ai_workload_report_quality.json exists=True json_ok=True kind=ai_workload_report_quality passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json exists=True json_ok=True kind=runtime_tool_usage_telemetry passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260505-002508.json exists=True json_ok=True kind=runtime_tool_capability_manifest passed=True

## Remaining gaps

- output/validation/shared_toolbox_python_syntax_20260505-002508.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_20260505-002508.json: optional report missing
- output/validation/shared_toolbox_gpu_contract_smoke_20260505-002508.json: optional report missing
- output/validation/shared_toolbox_gpu_routing_20260505-002508.json: optional report missing
- output/validation/shared_toolbox_npu_execution_20260505-002508.json: optional report missing
- output/validation/shared_toolbox_npu_contract_20260505-002508.json: optional report missing
- output/validation/npu_provider_environment_shared_toolbox_20260505-002508.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_orchestrator.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_gpu.json: optional report missing
- output/analysis/shared_toolbox_gpu_npu_sync_20260505-002508.json: optional report missing
- output/analysis/shared_toolbox_gpu_contract_replay_20260505-002508.json: optional report missing
- output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_integrated.json: optional report missing
- output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_workflow.json: optional report missing
- output/validation/agent_review_warning_policy_20260505-002508.json: optional report missing
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260505-002508.json: optional report missing
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260505-002508_cloud_semantic_deterministic_chunk_manifest.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_20260505-002508.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_orchestrator.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_gpu.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_npu_sync_20260505-002508.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_contract_replay_20260505-002508.md: optional artifact missing
- output/analysis/shared_toolbox_ai_to_ai_final_summary_20260505-002508.md: optional artifact missing
- output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_integrated.md: optional artifact missing
- output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_workflow.md: optional artifact missing
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260505-002508.md: optional artifact missing
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260505-002508_cloud_semantic_deterministic_chunk_manifest.md: optional artifact missing
- runtime tool requests not proven in provider-backed run: No concrete tool_requests were found in the included reports.

## Recommended next task

docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md

## Recursive defaults

- Enabled: `True`
- Discovered reports: `38`
- Discovered artifacts: `27`

## Chunked large JSON/Markdown files

- output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json lines=5776 chunks=29 chunk_size=200
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1-L200 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L201-L400
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L201-L400 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L401-L600
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L401-L600 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L601-L800
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L601-L800 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L801-L1000
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L801-L1000 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1001-L1200
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1001-L1200 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1201-L1400
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1201-L1400 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1401-L1600
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1401-L1600 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1601-L1800
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1601-L1800 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1801-L2000
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L1801-L2000 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2001-L2200
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2001-L2200 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2201-L2400
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2201-L2400 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2401-L2600
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2401-L2600 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2601-L2800
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2601-L2800 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2801-L3000
  - output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L2801-L3000 -> next: output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json#L3001-L3200
  - output/patch_specs/full_toolbox_20260505-00250
```

### `output/analysis/code_interpreter_full_toolbox_20260505-002508.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1464242`
- SHA-256: `54412573960ac2393b52b00541ed8e4effd6477f2b75de82ed2ace2db6ce6338`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-05T00:25:44",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 279,
  "parsed_file_count": 279,
  "total_lines": 79196,
  "total_functions": 2806,
  "total_classes": 94,
  "total_risk_signals": 58,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 786
    },
    {
      "module": "config",
      "count": 320
    },
    {
      "module": "__future__",
      "count": 242
    },
    {
      "module": "pathlib",
      "count": 231
    },
    {
      "module": "typing",
      "count": 210
    },
    {
      "module": "json",
      "count": 179
    },
    {
      "module": "argparse",
      "count": 164
    },
    {
      "module": "datetime",
      "count": 127
    },
    {
      "module": "sys",
      "count": 122
    },
    {
      "module": "report_utils",
      "count": 86
    },
    {
      "module": "dataclasses",
      "count": 54
    },
    {
      "module": "workflow_state",
      "count": 45
    },
    {
      "module": "re",
      "count": 42
    },
    {
      "module": "subprocess",
      "count": 36
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
      "module": "tkinter",
      "count": 23
    },
    {
      "module": "time",
      "count": 17
    },
    {
      "module": "hashlib",
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
      "module": "components",
      "count": 15
    },
    {
      "module": "math",
      "count": 13
    },
    {
      "module": "materials",
      "count": 13
    },
    {
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "io_utils",
      "count": 11
    },
    {
      "module": "ast",
      "count": 11
    },
    {
      "module": "defaults",
      "count": 11
    },
    {
      "module": "spaziotempo",
      "count": 9
    },
    {
      "module": "concurrent",
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
      "module": "path_utils",
      "count": 8
    },
    {
      "module": "runner",
      "count": 8
    },
    {
      "module": "types",
      "count": 8
    },
    {
      "module": "registry",
      "count": 8
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
      "line_count": 908,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 902,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 769,
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
      "path": "Scripting/v61b/materials.py",
      "line_count": 657,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "line_count": 653,
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
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "line_count": 569,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_semantic_evidence_chunks.py",
      "line_count": 562,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "low": 120,
    "medium": 151,
    "high": 8
  },
  "recommendation_count": 159,
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
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\outpu
```

### `output/analysis/code_interpreter_full_toolbox_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7095`
- SHA-256: `ab02d3aaad46fbc3f8ce30ce031c0521818fd70d82fc9c3f7dd6e71280f16343`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `279`
- Parsed files: `279`
- Total lines: `79196`
- Total functions: `2806`
- Total classes: `94`
- Risk signals: `58`
- TODO/FIXME markers: `21`
- Recommendation count: `159`
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
- `Tools/ai/build_deterministic_recommendations.py` — `908` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `769` lines, risk `medium`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` — `653` lines, risk `medium`
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
- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module, complex functions detected
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

### `output/analysis/full_memory_tool_regeneration_20260505-002508_code_interpreter.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1281883`
- SHA-256: `8c47f71caec18818cc20c6058a1257220a46bf33e83700890ef34786355a5a8d`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-05T00:25:34",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 237,
  "parsed_file_count": 237,
  "total_lines": 68591,
  "total_functions": 2525,
  "total_classes": 72,
  "total_risk_signals": 46,
  "total_todos": 21,
  "top_imports": [
    {
      "module": "Tools",
      "count": 786
    },
    {
      "module": "__future__",
      "count": 235
    },
    {
      "module": "pathlib",
      "count": 215
    },
    {
      "module": "typing",
      "count": 204
    },
    {
      "module": "json",
      "count": 173
    },
    {
      "module": "argparse",
      "count": 164
    },
    {
      "module": "datetime",
      "count": 127
    },
    {
      "module": "sys",
      "count": 116
    },
    {
      "module": "report_utils",
      "count": 86
    },
    {
      "module": "dataclasses",
      "count": 50
    },
    {
      "module": "workflow_state",
      "count": 45
    },
    {
      "module": "re",
      "count": 39
    },
    {
      "module": "subprocess",
      "count": 34
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
      "count": 17
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
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "reports",
      "count": 12
    },
    {
      "module": "ast",
      "count": 11
    },
    {
      "module": "defaults",
      "count": 11
    },
    {
      "module": "concurrent",
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
      "module": "io_utils",
      "count": 8
    },
    {
      "module": "providers",
      "count": 8
    },
    {
      "module": "collections",
      "count": 7
    },
    {
      "module": "agent_memory_policy",
      "count": 7
    },
    {
      "module": "runner",
      "count": 7
    },
    {
      "module": "types",
      "count": 7
    },
    {
      "module": "config",
      "count": 6
    },
    {
      "module": "urllib",
      "count": 5
    },
    {
      "module": "csv",
      "count": 5
    },
    {
      "module": "scene_brief",
      "count": 5
    },
    {
      "module": "sqlite3",
      "count": 4
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
      "line_count": 908,
      "risk": "high"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 902,
      "risk": "high"
    },
    {
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "line_count": 769,
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
      "line_count": 653,
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
      "path": "Tools/ai/analyze_gpu_npu_run_sync.py",
      "line_count": 569,
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
    "medium": 134,
    "low": 97,
    "high": 6
  },
  "recommendation_count": 140,
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
        "medium-size Python module",
        "complex functions detected"
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
        "python -m py_compile .\\Tools\\ai\
```

### `output/analysis/full_memory_tool_regeneration_20260505-002508_code_interpreter.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7327`
- SHA-256: `3f3ab006d384b571449133751dd2eab0aa234f17a17a9d80a5b41ce764f25abc`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `237`
- Parsed files: `237`
- Total lines: `68591`
- Total functions: `2525`
- Total classes: `72`
- Risk signals: `46`
- TODO/FIXME markers: `21`
- Recommendation count: `140`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1129` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` — `908` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` — `769` lines, risk `medium`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` — `653` lines, risk `medium`
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
- `code_static_007` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module, complex functions detected
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
- `code_static_031` `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_033` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_034` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_035` `Tools/ai/github_evidence_bundle_artifacts.py` risk `medium`: complex functions detected
- `code_static_036` `Tools/ai/gpu_planner_json_contract.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/model_json.py` risk `medium`: complex functions detected
- `code_static_038` `Tools/ai/pipeline/preflight.py` risk `medium`: complex functions detected
- `code_static_039` `Tools/ai/pipeline/remediation.py` risk `medium`: large functions detected, complex functions detected, TODO/FIXME markers detected
- `code_static_040` `Tools/ai/pipeline/steps.py` risk `medium`: large functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-002508.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `14368`
- SHA-256: `a68ffb2f1bdb2418acfcbf0bddbe6241e3f48ab060019fe418b44e73d9465405`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_planner_json_contract_replay",
  "generated_at": "2026-05-05T00:32:02",
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
    "gpu_report": "output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json"
  },
  "source_summary": {
    "kind": "agent_gpu_deep_planning_supervised",
    "passed": true,
    "round_count": 13,
    "recommendation_count": 0,
    "json_parse_error_count": 0,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "context_echo_detected",
    "evidence_ready_for_manual_patch_count": 0
  },
  "replayed_round_count": 13,
  "contract_reason_counts": {
    "model_output_schema_mismatch": 11,
    "json_parse_failure": 2
  },
  "context_echo_detected_count": 0,
  "json_parse_failure_count": 2,
  "model_output_schema_mismatch_count": 11,
  "valid_recommendation_output_count": 0,
  "rounds": [
    {
      "round": 1,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 68,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "original_response_chars": 68,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "original_response_chars": 200,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "58262d0291a1609162fedeea6108c7d3cd6fe5c6969ff12964f47fe24d300b78",
        "raw_response_chars": 200,
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
      "original_response_chars": 68,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "round": 5,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 635,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "89809978510335e36184cfef4c58b38b89c696191e0833d76aa0a7adc151eb85",
        "raw_response_chars": 635,
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
      "round": 6,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 1891,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "3203bd7a35099f975ee8dd588cc555b5bbe98ea48d59c9757e3e7ac21c2db5b4",
        "raw_response_chars": 1891,
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
      "round": 7,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 1297,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "7dfc732384552093e9fcffda354f7a7ef7269aff665cdb2326978f36f52263e7",
        "raw_response_chars": 1297,
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
      "round": 8,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 392,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "bf8937f124ead5695d349723122f52ab6f8eaabfd2ec918daf6e58847614ce61",
        "raw_response_chars": 392,
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
      "round": 9,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 2310,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "93ce335573f43d48aeb7e5f431d4e33588e2c1d514c64f394be62d18e902f028",
        "raw_response_chars": 2310,
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
      "round": 10,
      "original_empty_recommendations_reason": "context_echo_detected",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 4177,
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "outer JSON document appears truncated or unbalanced",
        "schema_errors": [],
        "raw_response_sha256": "732e373938d17358250ae15d6ae70af01d12e01b5ba0b646907e5707b4d45333",
        "raw_response_chars": 3000,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
      }
    },
    {
      "round": 11,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 68,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "round": 12,
      "original_empty_recommendations_reason": "model_output_schema_mismatch",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 68,
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "round": 13,
      "original_empty_recommendations_reason": "context_echo_detected",
      "original_json_ok": true,
      "original_parse_error": "",
      "original_response_chars": 6637,
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "outer JSON document appears truncated or unbalanced",
        "schema_errors": [],
        "raw_response_sha256": "73a93d7ca8c60983c6e435f32f9f0100a1b14ac161c278e5f0eebb89aaf05698",
        "raw_response_chars": 3000,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
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

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `638`
- SHA-256: `fa73b6a25671475220af1d54c6e584031de35879612f961928072fedc3ed276e`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `13`
- Context echo detected: `0`
- JSON parse failures: `2`
- Schema mismatches: `11`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `json_parse_failure`: `2`
- `model_output_schema_mismatch`: `11`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-002508.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5622`
- SHA-256: `e5464b8fb4b3c6fd881c3065deaafcd547ba5c0edcba74dbeb002db3446d65ed`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-05T00:32:02",
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
    "orchestrator": "output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 13,
    "npu_audit_count": 3,
    "npu_audit_success_count": 3,
    "npu_audit_round_coverage": 0.231,
    "avg_gpu_round_seconds": 26.316,
    "p50_gpu_round_seconds": 26.316,
    "p90_gpu_round_seconds": 26.316,
    "avg_npu_audit_seconds": 107.333,
    "p50_npu_audit_seconds": 104.0,
    "p90_npu_audit_seconds": 116.0,
    "npu_to_gpu_avg_duration_ratio": 4.079,
    "gpu_elapsed_seconds": 342.107,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.001,
    "gpu": {
      "elapsed_seconds": 342.107,
      "round_count": 13,
      "round_duration_source": "gpu_elapsed_divided_by_round_count",
      "round_duration_sample_count": 1,
      "avg_round_seconds": 26.316,
      "p50_round_seconds": 26.316,
      "p90_round_seconds": 26.316,
      "max_round_seconds": 26.316,
      "round_durations_total_seconds": 26.316,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 44,
        "runtime_tool_execution_count": 0,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 44,
        "runtime_tool_provider_request_execution_count": 0,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0
      },
      "embedded_performance": {}
    },
    "npu": {
      "audit_count": 3,
      "audit_requested_count": 0,
      "audit_success_count": 3,
      "duration_sample_count": 3,
      "avg_audit_seconds": 107.333,
      "p50_audit_seconds": 104.0,
      "p90_audit_seconds": 116.0,
      "max_audit_seconds": 116.0,
      "audit_durations_total_seconds": 322.0,
      "status_counts": {
        "finished": 3
      },
      "classification_counts": {
        "usable_audit_text": 3
      },
      "lane_diagnostics": {}
    },
    "sync": {
      "npu_to_gpu_avg_duration_ratio": 4.079,
      "npu_audit_round_coverage": 0.231,
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
      "NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round.",
      "Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.",
      "NPU audits are usable; tune cadence rather than disabling the lane."
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
    "NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.",
    "Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.",
    "GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics."
  ],
  "refactoring_suggestions": [
    {
      "priority": "high",
      "area": "gpu_runner_timing",
      "recommendation": "Add per-round elapsed_seconds to each GPU planner round record.",
      "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count",
      "guardrail": "report_only_no_provider_setting_change"
    },
    {
      "priority": "medium",
      "area": "npu_cadence",
      "recommendation": "Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget.",
      "evidence": "npu_to_gpu_avg_duration_ratio=4.079",
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

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2467`
- SHA-256: `904ca255f9d66143996f657ad3a31fc82522d21d2b4501769b48712b8d06eabc`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `13`
- `npu_audit_count`: `3`
- `npu_audit_success_count`: `3`
- `npu_audit_round_coverage`: `0.231`
- `avg_gpu_round_seconds`: `26.316`
- `p50_gpu_round_seconds`: `26.316`
- `p90_gpu_round_seconds`: `26.316`
- `avg_npu_audit_seconds`: `107.333`
- `p50_npu_audit_seconds`: `104.0`
- `p90_npu_audit_seconds`: `116.0`
- `npu_to_gpu_avg_duration_ratio`: `4.079`
- `gpu_elapsed_seconds`: `342.107`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `342.107`
- GPU average round seconds: `26.316`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- NPU average audit seconds: `107.333`
- NPU duration sample count: `3`

## Operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count
- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=4.079

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

- NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round.
- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.
- NPU audits are usable; tune cadence rather than disabling the lane.


```

### `output/analysis/repository_consistency_map_full_toolbox_20260505-002508.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `6540351`
- SHA-256: `000916c715045c2bf36949b3a9a2baa60fbf91b14d10e8e8523c5950fcf9a464`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "repository_consistency_map",
  "generated_at": "2026-05-05T00:26:20",
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
    "markdown_file_count": 338,
    "python_file_count": 325,
    "markdown_reference_count": 50375,
    "markdown_python_command_count": 888,
    "python_inventory_count": 325,
    "generated_evidence_chunk_exclusion_enabled": true
  },
  "finding_count": 8349,
  "severity_counts": {
    "high": 1913,
    "low": 44,
    "medium": 6392
  },
  "finding_kind_counts": {
    "documented_python_script_without_obvious_smoke": 44,
    "md_cli_arg_not_in_argparse": 2,
    "md_mentions_missing_markdown_path": 6390,
    "md_mentions_missing_powershell_path": 179,
    "md_mentions_missing_python_path": 1708,
    "md_python_command_script_missing": 26
  },
  "markdown_reference_kind_counts": {
    "artifact": 9530,
    "markdown": 13790,
    "powershell": 843,
    "python": 26212
  },
  "findings": [
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "AGENTS.md",
      "line": 69,
      "target": "text\nCHATGPT.md                         # root pointer\nCHATGPT/README.md                  # index and reading order\nCHATGPT/next-chat-handoff-*.md     # current handoff state\nCHATGPT/chatgpt-session-problems-and-robust-fixes-*.md",
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
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "CHATGPT/DISCOVERY_CONTRACT.md",
      "line": 13,
      "target": "text\nCHATGPT.md\nCHATGPT/README.md\nCHATGPT/*.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md",
      "line": 29,
      "target": "run_patch_bundle.py",
      "evidence": "- run_patch_bundle.py or run_patch_bundle.ps1;",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_powershell_path",
      "severity": "high",
      "source": "CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md",
      "line": 29,
      "target": "run_patch_bundle.ps1",
      "evidence": "- run_patch_bundle.py or run_patch_bundle.ps1;",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md",
      "line": 216,
      "target": "text\nCHATGPT/README.md\nCHATGPT/next-chat-handoff-*.md\nCHATGPT/chatgpt-session-problems-and-robust-fixes-*.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md",
      "line": 142,
      "target": "run_patch_bundle.py",
      "evidence": "python .\\output\\validation\\patch_bundles\\ia_carmine_real_run_strict_tool_activation_bundle\\run_patch_bundle.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md",
      "line": 67,
      "target": "text\noutput/ai_packets/20260504-224354/npu_real_workload_report.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md",
      "line": 141,
      "target": "powershell\npython ./output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py",
      "evidence": "```powershell",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "FULL_RUN_UNICA_TUTTO_SU_TUTTO.md",
      "line": 470,
      "target": "_cloud_semantic_deterministic_chunk_manifest.md",
      "evidence": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.md",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "README.md",
      "line": 28,
      "target": "text\nCHATGPT.md\nCHATGPT/README.md\nCHATGPT/next-chat-handoff-*.md\nCHATGPT/chatgpt-session-problems-and-robust-fixes-*.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/README.md",
      "line": 47,
      "target": "pipeline.py",
      "evidence": "pipeline.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/README.md",
      "line": 55,
      "target": "encode.py",
      "evidence": "encode.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "Scripting/README.md",
      "line": 42,
      "target": "text\npackage_name/\n  README.md\n  main.py\n  config.py\n  pipeline.py\n  audio_mapping.py\n  scene_objects.py\n  materials.py\n  lighting.py\n  camera.py\n  animation.py\n  render_settings.py\n  encode.py\n  diagnostics.py\n  inputs/\n    README.md\n    input_schema.json\n  outputs/\n    README.md\n  notes/\n    known_issues.md\n    tuning_notes.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/README.md",
      "line": 11,
      "target": "text\nmain_ready_to_jazz_wow_youtube.py",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/shared/README.md",
      "line": 100,
      "target": "config_model.py",
      "evidence": "config_model.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/shared/README.md",
      "line": 101,
      "target": "panel_base.py",
      "evidence": "panel_base.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/shared/README.md",
      "line": 102,
      "target": "scene_update.py",
      "evidence": "scene_update.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/shared/README.md",
      "line": 104,
      "target": "hotpatch_base.py",
      "evidence": "hotpatch_base.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/shared/README.md",
      "line": 105,
      "target": "scene_registry.py",
      "evidence": "scene_registry.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/shared/README.md",
      "line": 97,
      "target": "text\nScripting/shared/\n  README.md\n  config_model.py\n  panel_base.py\n  scene_update.py\n  diagnostics.py\n  hotpatch_base.py\n  scene_registry.py",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/v61b/PROJECT_STRUCTURE.md",
      "line": 34,
      "target": "spaziotempo/features/water.py",
      "evidence": "L'acqua non e stata aggiunta. Il layer `ST_60_Water` serve solo come spazio pronto: in futuro potra avere un modulo dedicato, ad esempio `spaziotempo/features/water.py`, con build/update/check separati e senza toccare...",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/v61b/README.md",
      "line": 88,
      "target": "Scripting/shared/panel_base.py",
      "evidence": "| `scene_tuning_panel.py` | `Scripting/shared/panel_base.py`, `render_profiles.py` |",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/v61b/README.md",
      "line": 89,
      "target": "Scripting/shared/hotpatch_base.py",
      "evidence": "| `hotpatch/common.py` | `Scripting/shared/hotpatch_base.py`, `diagnostics.py` |",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "Scripting/v61b/README.md",
      "line": 23,
      "target": "text\nmain_v61b.py
```

### `output/analysis/repository_consistency_map_full_toolbox_20260505-002508.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `54850`
- SHA-256: `9a8f52f5f43e9d4ca443050b8bf309942346a66034a2450760d33232b292e7b5`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `8349`
- Markdown files: `338`
- Python files: `325`
- Markdown references: `50375`
- Markdown Python commands: `888`
- Provider execution performed: `False`
- Workers requested: `8`
- Total build seconds: `33.749`
- Markdown scan seconds: `29.247`
- Python inventory seconds: `1.931`
- Patch application performed: `False`

## Severity counts

- `high`: `1913`
- `low`: `44`
- `medium`: `6392`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `44`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `6390`
- `md_mentions_missing_powershell_path`: `179`
- `md_mentions_missing_python_path`: `1708`
- `md_python_command_script_missing`: `26`

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `medium` | `md_mentions_missing_markdown_path` | `AGENTS.md` | 69 | `text
CHATGPT.md                         # root pointer
CHATGPT/README.md                  # index and reading order
CHATGPT/next-chat-handoff-*.md     # current handoff state
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 237 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 292 | `some_script.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 302 | `changed.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 323 | `some_tool.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 324 | `some_smoke.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_powershell_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 325 | `some_runner.ps1` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 323 | `Tools/validation/some_smoke.py` | Correct the documentation reference or restore the missing target if it is still required. |
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
| `high` | `md_mentions_missing_python_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 142 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 67 | `text
output/ai_packets/20260504-224354/npu_real_workload_report.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` | 141 | `powershell
python ./output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `FULL_RUN_UNICA_TUTTO_SU_TUTTO.md` | 470 | `_cloud_semantic_deterministic_chunk_manifest.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `README.md` | 28 | `text
CHATGPT.md
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/README.md` | 47 | `pipeline.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/README.md` | 55 | `encode.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Scripting/README.md` | 42 | `text
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
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 100 | `config_model.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 101 | `panel_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 102 | `scene_update.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 104 | `hotpatch_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 105 | `scene_registry.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/shared/README.md` | 97 | `text
Scripting/shared/
  README.md
  config_model.py
  panel_base.py
  scene_update.py
  diagnostics.py
  hotpatch_base.py
  scene_registry.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/PROJECT_STRUCTURE.md` | 34 | `spaziotempo/features/water.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/README.md` | 88 | `Scripting/shared/panel_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/README.md` | 89 | `Scripting/shared/hotpatch_base.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Scripting/v61b/README.md` | 23 | `text
main_v61b.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 31 | `selected_chunks_focus.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 68 | `selective_execution_plan.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 78 | `full_context_golden_proposals.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 84 | `local_ai_enrichment_plan.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 90 | `npu_knowledge_broker_packet.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 96 | `agent_review_evidence_sufficiency.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 97 | `agent_review_patch_plan.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 77 | `--markdown-output ./output/ai_pipeline/full_context_golden_proposals.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 83 | `powershell
py ./Tools/ai/build_local_ai_enrichment_plan.py --repo-root . --output ./output/ai_pipeline/local_ai_enrichment_plan.json --markdown-output ./output/ai_pipeline/local_ai_enrichment_plan.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 89 | `powershell
py ./Tools/npu/build_npu_knowledge_broker_packet.py --repo-root . --output ./output/ai_pipeline/npu_knowledge_broker_packet.json --markdown-output ./output/ai_pipeline/npu_knowledge_broker_packet.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/ai/README.md` | 95 | `powershell
py ./Tools/ai/build_agent_review_evidence_sufficiency.py --repo-root . --output ./output/ai_pipeline/agent_review_evidence_sufficiency.json --markdown-output ./output/ai_pipeline/agent_review_evidence_sufficiency.md
py ./Tools/ai/build_agent_review_patch_plan.py --repo-root . --output ./output/patch_specs/agent_review_patch_plan.json --markdown-output ./output/patch_specs/agent_review_patch_plan.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/git/README.md` | 11 | `Tools/npu/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/git/README.md` | 12 | `output/*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/README.md` | 20 | `_technical_notes.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/README.md` | 22 | `_context.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Tools/npu/README.md` | 18 | `build_*context*.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `Tools/npu/README.md` | 19 | `run_*pipeline*.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/README.md` | 20 | `*_technical_notes.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/README.md` | 22 | `*_context.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 70 | `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 71 | `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 72 | `Tools/npu/npu_code_chunks/chunk_003_build_track_summary_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 73 | `Tools/npu/npu_code_chunks/chunk_004_normalize_scene_spec_py.md` | Correct the documentation reference or restore the missing target if it 
```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_20260505-002508.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1028707`
- SHA-256: `052285f3a23b85e5dba81b288d561bd0122f805e1c4f9615424df71d8d5c0f89`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "shared_toolbox_ai_to_ai_final_summary",
  "stamp": "20260505-002508",
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
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_agent_review_decision_loop.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop",
      "passed": true
    },
    {
      "path": "output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_patch_plan",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_deep_planning_supervised",
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
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json",
      "exists": true,
      "json_ok": true,
      "kind": "runtime_tool_usage_telemetry",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260505-002508.json",
      "exists": true,
      "json_ok": true,
      "kind": "runtime_tool_capability_manifest",
      "passed": true
    }
  ],
  "remaining_gaps": [
    {
      "path": "output/validation/shared_toolbox_python_syntax_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_contract_smoke_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_routing_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_execution_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_contract_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/npu_provider_environment_shared_toolbox_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_orchestrator.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_gpu.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_integrated.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_workflow.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/agent_review_warning_policy_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260505-002508.json",
      "reason": "optional report missing"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260505-002508_cloud_semantic_deterministic_chunk_manifest.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_20260505-002508.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_orchestrator.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_20260505-002508_gpu.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_npu_sync_20260505-002508.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_gpu_contract_replay_20260505-002508.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/analysis/shared_toolbox_ai_to_ai_final_summary_20260505-002508.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_integrated.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "output/validation/agent_review_full_toolbox_decision_loop_20260505-002508_workflow.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260505-002508.md",
      "reason": "optional artifact missing"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260505-002508_cloud_semantic_deterministic_chunk_manifest.md",
      "reason": "optional artifact missing"
    },
    {
  
```

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agent_memory_inventory.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `13178`
- SHA-256: `ed80e6b74ec28de6d71cba84087b198ced63f948d0ad93aa2e4e0a96cbf26eb0`
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
        "row_count": 36,
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
    "record_count": 36,
    "total_content_chars": 142080,
    "kind_counts": {
      "source_file": 34,
      "operator_note": 2
    },
    "scope_counts": {
      "project": 34,
      "task": 2
    },
    "top_sources": {
      "output/ai_context_packs/full_context_golden_core_ai_backend.json": 5,
      "output/ai_context_packs/full_context_golden_core_ai_backend.md": 5,
      "output/ai_context_packs/full_context_golden_selected_chunks.json": 5,
      "output/ai_context_packs/full_context_golden_selected_chunks.md": 5,
      "indexAI/code_chunks/semantic_code_chunks_manifest.json": 5,
      "output/ai_pipeline/full_context_golden_enrichment_plan.json": 5,
      "cli_note_1": 2,
      "output/ai_pipeline/full_context_golden_enrichment_plan.md": 2,
      "docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md": 1,
      "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md": 1
    },
    "tag_counts": {
      "source_file": 34,
      "json": 20,
      "md": 14,
      "recent": 2,
      "operator_note": 2
    },
    "confidence_buckets": {
      "0.90-1.00": 36
    }
  },
  "policy_report": {
    "kind": "agent_memory_policy_report",
    "passed": true,
    "record_count": 36,
    "promotion_candidate_count": 0,
    "review_count": 0,
    "risk_count": 0,
    "duplicate_group_count": 0,
    "action_counts": {
      "keep": 36
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
      "record_id": "dc8f442d4388ebb634a3",
      "kind": "source_file",
      "scope": "project",
      "source": "output/ai_pipeline/full_context_golden_enrichment_plan.json",
      "tags": [
        "source_file",
        "json"
      ],
      "confidence": 1.0,
      "rank_score": 18.0,
      "summary": "{ \"schema_version\": 1, \"kind\": \"local_ai_enrichment_plan\", \"generated_at\": \"2026-05-04T20:13:47.382294+00:00\", \"repo_root\": \"C:/Users/carmi/blender/blender-audio-project\", \"objective\": \"Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker.\", \"task_file\": \"docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md\", \"profile\": \"npu\", \"basename\": \"full_context_golden_enrichment_plan\", \"apply_mode\": \"report_only\", \"provider_execution_performed\": false, \"source_writes_performed\": false, \"patch_application_performed\": false, \"complexity\": { \"level\": \"high\", \"score\": 16, \"matched_terms\": [ \"architecture\", \"broker\", \"context\", \"full-context\", \"gpu\", \"knowledge\", \"npu\", \"ollama\", \"patch\", \"provider\" ], \"task_text_chars_sampled\": 8000 }, \"lane_policy\": { \"primary_advisory..."
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

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agent_memory_inventory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6717`
- SHA-256: `b047bf3d4bed81ee570c4184e2f915bbc46ecc481ffd35143cb02879195d7bea`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Memory Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Memory DB: `indexAI/agent_memory/agent_memory.sqlite`
- Memory DB exists: `True`
- Record count: `36`
- SQLite opened read-only: `True`

## SQLite

- Schema version: `1`

- `memory_meta` rows=`1` columns=`2`
- `memory_records` rows=`36` columns=`12`

## Record distributions

### kind_counts

- `source_file`: 34
- `operator_note`: 2

### scope_counts

- `project`: 34
- `task`: 2

### confidence_buckets

- `0.90-1.00`: 36

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

### dc8f442d4388ebb634a3 - output/ai_pipeline/full_context_golden_enrichment_plan.json

- Kind: `source_file`
- Scope: `project`
- Score: `18.0`

{ "schema_version": 1, "kind": "local_ai_enrichment_plan", "generated_at": "2026-05-04T20:13:47.382294+00:00", "repo_root": "C:/Users/carmi/blender/blender-audio-project", "objective": "Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker.", "task_file": "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md", "profile": "npu", "basename": "full_context_golden_enrichment_plan", "apply_mode": "report_only", "provider_execution_performed": false, "source_writes_performed": false, "patch_application_performed": false, "complexity": { "level": "high", "score": 16, "matched_terms": [ "architecture", "broker", "context", "full-context", "gpu", "knowledge", "npu", "ollama", "patch", "provider" ], "task_text_chars_sampled": 8000 }, "lane_policy": { "primary_advisory...

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

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agnostic_tool_inventory.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `560563`
- SHA-256: `976bd24a2451484e1f5308ca7e3e2adfcff476bfc8106b0f15207b738c50483d`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_agnostic_tool_inventory",
  "generated_at": "2026-05-05T00:25:27",
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
    "tool_count": 257,
    "category_counts": {
      "validator": 93,
      "provider_probe_or_adapter": 49,
      "support_tool": 45,
      "orchestrator_pipeline": 38,
      "agent_context_builder": 10,
      "git_helper": 10,
      "proposal_or_review_builder": 7,
      "review_helper": 5
    },
    "owner_lane_counts": {
      "npu_explicit_provider_tool": 85,
      "gpu_cuda_explicit_provider_tool": 64,
      "cpu_validation": 44,
      "cpu_support": 34,
      "cpu_orchestration": 21,
      "cpu_context_builder": 5,
      "cpu_proposal_builder": 4
    },
    "consumed_lane_counts": {
      "cpu": 257,
      "npu": 189,
      "gpu_cuda": 148
    },
    "apply_mode_counts": {
      "not_declared": 128,
      "report_only": 98,
      "manual_review_only": 21,
      "explicit_git_operation": 10
    },
    "provider_execution_default_counts": {
      "none_or_reported": 234,
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
      "lines": 569,
      "symbols": [
        "analyze",
        "audit_duration_seconds",
        "build_operational_opinions",
        "build_performance_summary",
        "build_refactoring_suggestions",
        "build_suggestions",
        "compact_performance_source",
        "duration_from_timestamps",
        "elapsed_seconds",
        "extract_gpu_round_durations",
        "extract_round_duration",
        "first_int",
        "list_of_dicts",
        "main",
        "nested_dict",
        "now_iso",
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
        "build_records",
        "classify_category",
        "classify_owner_lane",
        "consumed_lanes",
        "extract_flags",
        "extract_guardrails",
        "extract_symbols",
        "iter_tool_files",
        "main",
        "now_iso",
        "provider_execution_default",
        "python_symbols",
        "read_text",
        "record_to_dict",
        "render_markdown",
        "repo_rel",
        "resolve_path",
        "summarize"
      ],
      "flags": [
        "--markdown-output",
        "--max-items-per-category",
        "--max-tools",
        "--output",
        "--repo-root",
        "--root",
        "--use-ollama"
      ],
      "guardrails": [
        "blender_runtime_guardrail",
        "manual_review_only",
        "no_blender_runtime",
        "npu_advisory_guardrail",
        "openvino_gpu_primary_guardrail",
        "output_artifacts_guardrail",
        "patch_application_reported",
        "provider_execution_reported",
        "read_only",
        "sqlite_awareness"
      ]
    },
    {
      "path": "Tools/ai/build_agent_memory_inventory.py",
      "extension": ".py",
      "category": "agent_context_builder",
      "owner_lane": "cpu_context_builder",
      "consumed_by_lanes": [
        "cpu",
        "npu"
      ],
      "provider_execution_default": "none_or_reported",
      "apply_mode": "report_only",
      "lines": 397,
      "symbols": [
```

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agnostic_tool_inventory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15853`
- SHA-256: `860b2d6a7fdba9378f6f9fefeeee6b0f3fa89685eec0d547452f6be459d89d64`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Agnostic Tool Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Tool count: `257`

## category_counts

- `validator`: 93
- `provider_probe_or_adapter`: 49
- `support_tool`: 45
- `orchestrator_pipeline`: 38
- `agent_context_builder`: 10
- `git_helper`: 10
- `proposal_or_review_builder`: 7
- `review_helper`: 5

## owner_lane_counts

- `npu_explicit_provider_tool`: 85
- `gpu_cuda_explicit_provider_tool`: 64
- `cpu_validation`: 44
- `cpu_support`: 34
- `cpu_orchestration`: 21
- `cpu_context_builder`: 5
- `cpu_proposal_builder`: 4

## consumed_lane_counts

- `cpu`: 257
- `npu`: 189
- `gpu_cuda`: 148

## apply_mode_counts

- `not_declared`: 128
- `report_only`: 98
- `manual_review_only`: 21
- `explicit_git_operation`: 10

## provider_execution_default_counts

- `none_or_reported`: 234
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
- `Tools/ai/build_full_toolbox_run_telemetry_summary.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_gpu_repair_failure_recommendation.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_music_intermediates.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/build_refactor_duplication_audit.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_repository_consistency_map.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_runtime_tool_capability_manifest.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_semantic_evidence_chunks.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/code_patch_plan_common.py` lane=`cpu_support` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/merge_ai_candidates.py` lane=`cpu_support` apply=`not_declared` provider=`none_or_reported`

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
- `Tools/ai/build_local_ai_enrichment_plan.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_selective_execution_plan.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_workload_quality_lane_routing.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/run_agent_review_decision_loop.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/run_local_provider_probe.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`explicit_only`
- `Tools/ai/run_megalithic_repo_review.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/run_npu_decode_smoke_diagnostic.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`explicit_only`
- `Tools/ai/runtime_tool_guidance.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/workload_quality.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/ai_memory_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_ai_service_packet.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_blender_manual_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/npu/build_music_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`explicit_only`
- `Tools/npu/build_npu_code_context.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`

### proposal_or_review_builder

- `Tools/ai/build_code_edit_proposal_from_plan.py` lane=`cpu_proposal_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/build_full_context_golden_proposals.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_megalithic_review_pr_draft.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_patch_specs_from_proposals.py` lane=`cpu_proposal_builder` apply=`manual_review_only` provider=`none_or_reported`
- `Tools/ai/build_repository_change_proposals.py` lane=`npu_explicit_provider_tool` apply=`manual_review_only` provider=`explicit_only`
- `Tools/ai/code_edit_proposal_helpers.py` lane=`cpu_proposal_builder` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/promote_patch_spec_draft.py` lane=`cpu_proposal_builder` apply=`manual_review_only` provider=`none_or_reported`

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

### validator

- `Tools/ai/check_local_resource_lanes.py` lane=`npu_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/check_npu_provider_environment.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/ai/gpu_planner_json_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/pipeline/artifact_contracts.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/ai/replay_gpu_planner_json_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/ai_pipeline_report_contracts.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/apply_docs_contract_drift_fixes.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/build_full_python_line_count_markdown.py` lane=`cpu_validation` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/build_markdown_inventory.py` lane=`gpu_cuda_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/build_python_line_count_csv.py` lane=`cpu_validation` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/build_script_inventory.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`
- `Tools/validation/check_agent_memory_policy.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_context_pack_contract.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_dry_run_matrix_cases.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_dry_run_matrix_contract.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_dry_run_matrix_outputs.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_model_json.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_pipeline_modules.py` lane=`gpu_cuda_explicit_provider_tool` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_pipeline_report_contract.py` lane=`cpu_validation` apply=`not_declared` provider=`none_or_reported`
- `Tools/validation/check_ai_workload_report_quality.py` lane=`npu_explicit_provider_tool` apply=`report_only` provider=`none_or_reported`

### orchestrator_pipeline

- `Tools/workflow/ai_runtime_diagnostics.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/artifact_consult.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/asset_inventory.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/git_auto_push.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/__init__.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/action_panel.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/artifact_browser.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/live_output_panel.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/session_overview.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_reported`
- `Tools/workflow/gui/components/st_theme.py` lane=`cpu_orchestration` apply=`not_declared` provider=`none_or_r
```

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_transient_request_context.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `9178`
- SHA-256: `dd70e5a2f54e81707b0734d49f86437f2d479e1d6a84602bb9a0bf89f2d4236f`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_transient_request_context",
  "generated_at": "2026-05-05T00:25:32",
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
        "path": "output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agent_memory_inventory.json",
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
        "path": "output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "summary": {
            "tool_count": 257,
            "category_counts": {
              "validator": 93,
              "provider_probe_or_adapter": 49,
              "support_tool": 45,
              "orchestrator_pipeline": 38,
              "agent_context_builder": 10,
              "git_helper": 10,
              "proposal_or_review_builder": 7,
              "review_helper": 5
            },
            "owner_lane_counts": {
              "npu_explicit_provider_tool": 85,
              "gpu_cuda_explicit_provider_tool": 64,
              "cpu_validation": 44,
              "cpu_support": 34,
              "cpu_orchestration": 21,
              "cpu_context_builder": 5,
              "cpu_proposal_builder": 4
            },
            "consumed_lane_counts": {
              "cpu": 257,
              "npu": 189,
              "gpu_cuda": 148
            },
            "apply_mode_counts": {
              "not_declared": 128,
              "report_only": 98,
              "manual_review_only": 21,
              "explicit_git_operation": 10
            },
            "provider_execution_default_counts": {
              "none_or_reported": 234,
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
        "path": "output/validation/full_memory_tool_regeneration_20260505-002508_persistent_memory_status.json",
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
        "path": "output/validation/full_memory_tool_regeneration_20260505-002508_operational_memory_status.json",
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
        "path": "output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy.json",
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
        "path": "output/validation/full_memory_tool_regeneration_20260505-002508_runtime_tool_broker.json",
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

### `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_transient_request_context.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1754`
- SHA-256: `c9389e64514d6e4ff9f5f773d375d075139f54776c9f48a5dcd856ba89bc38f7`
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

- `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agent_memory_inventory.json` kind=`agent_memory_inventory` passed=`True` error=``
- `output/ai_pipeline/full_memory_tool_regeneration_20260505-002508_agnostic_tool_inventory.json` kind=`agent_agnostic_tool_inventory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260505-002508_persistent_memory_status.json` kind=`agent_runtime_sqlite_memory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260505-002508_operational_memory_status.json` kind=`agent_runtime_sqlite_memory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy.json` kind=`agent_memory_routing_policy` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_20260505-002508_runtime_tool_broker.json` kind=`agent_runtime_tool_broker` passed=`True` error=``

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

### `output/ai_pipeline/full_toolbox_20260505-002508_agent_review_decision_loop.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `2868`
- SHA-256: `dcaa5a74b0966bc72a18c1bf44b00e7d69633a04730b2855c78810112159075b`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_review_decision_loop",
  "generated_at": "2026-05-05T00:32:02",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [
    "patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection"
  ],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "recommendation_count": 20,
  "patch_plan_count": 20,
  "deterministic_synthesizer_used": true,
  "patch_plan_fallback_used": false,
  "next_best_action": "manual_review_patch_plan",
  "outputs": {
    "recommendations": {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json",
      "exists": true,
      "size_bytes": 188679
    },
    "recommendations_markdown": {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.md",
      "exists": true,
      "size_bytes": 19806
    },
    "bridge_orchestrator": {
      "path": "output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json",
      "exists": true,
      "size_bytes": 13341
    },
    "patch_plan": {
      "path": "output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.json",
      "exists": true,
      "size_bytes": 291484
    },
    "patch_plan_markdown": {
      "path": "output/patch_specs/full_toolbox_20260505-002508_agent_review_patch_plan.md",
      "exists": true,
      "size_bytes": 19406
    }
  },
  "inputs": {
    "evidence": "output/ai_pipeline/agent_review_evidence_sufficiency.json",
    "orchestrator": "output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json",
    "gpu_report": ".\\output\\ai_pipeline\\full_toolbox_20260505-002508_parallel_gpu.json",
    "tool_report_count": 12,
    "max_recommendations": 20,
    "max_patch_plans": 20,
    "recommendation_kind": "deterministic_recommendation_synthesizer",
    "patch_plan_kind": "agent_review_patch_plan"
  },
  "decision": {
    "recommendations_ready": true,
    "patch_plan_ready": true,
    "manual_review_required": true,
    "recommended_next_layer": "manual_review_patch_plan"
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
    "real_github_pr_created": false,
    "npu_primary_advisory": false,
    "openvino_gpu_primary_lane": false
  }
}

```

### `output/ai_pipeline/full_toolbox_20260505-002508_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `13341`
- SHA-256: `f0ca18afd84be7813bc4b819f00a528545e470ad45ce8ef6cf13bed860cc6936`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-05T00:32:02",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json",
  "gpu_recommendation_count": 20,
  "gpu_empty_recommendations_reason": "",
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-05T00:26:34",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "skipped",
      "npu_effective_auditor_every_rounds_at_launch": 3,
      "finished_at": "2026-05-05T00:28:30",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-05T00:28:32",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-05T00:30:16",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 8,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_008.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_008_npu_async_audit.json",
      "started_at": "2026-05-05T00:30:18",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_008_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-05T00:32:00",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_008_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_008_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    }
  ],
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

### `output/ai_pipeline/full_toolbox_20260505-002508_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `188679`
- SHA-256: `60dcef3b828968f5b954b01c28088b185ed8cce92efcda854b323af64f4409c3`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_synthesizer",
  "generated_at": "2026-05-05T00:32:02",
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
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.",
      "proposed_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
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
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260505-002508.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/python_line_count_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/python_syntax_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/npu_provider_environment_full_toolbox_20260505-002508.json",
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
          "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260505-002508.json",
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
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/full_memory_tool_regeneration_20260505-002508_workflow.json",
          "kind": "full_memory_tool_regeneration_workflow",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        }
      ],
      "npu_audit_refs": [
        {
          "round": 1,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 4,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 8,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        }
      ],
      "repository_consistency_finding": {
        "kind": "md_python_command_script_missing",
        "severity": "high",
        "source": "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md",
        "line": 163,
        "target": "Tools/validation/check_markdown_command_hygiene.py",
        "flag": "",
        "evidence": ""
      },
      "guardrails": {
        "patch_application_performed": false,
        "manual_review_required": true,
        "cosmetic_patch_allowed": false
      }
    },
    {
      "id": "consistency_002",
      "area": "md_python",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.",
      "proposed_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
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
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260505-002508.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/python_line_count_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/python_syntax_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-002508.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-002508.json",
          "kind": "d
```

### `output/ai_pipeline/full_toolbox_20260505-002508_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `22632`
- SHA-256: `b6b7272db3dee1cee2af0943f8f1afca8d0346f39cfc073515650453eb28492a`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-05T00:32:02",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 342.107,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 323.984,\n  \"round_count\": 13,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"empty_recommendations_reason\": \"context_echo_detected\",\n  \"runtime_tool_broker_enabled\": false,\n  \"runtime_tool_bootstrap_executed\": false,\n  \"runtime_tool_bootstrap_passed\": null,\n  \"runtime_tool_bootstrap_request_count\": 0,\n  \"runtime_tool_bootstrap_execution_count\": 0,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 44,\n  \"runtime_tool_execution_count\": 0,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 0,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 0,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"collect_more_evidence\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "context_echo_detected",
  "gpu_evidence_ready_for_manual_patch_count": 0,
  "gpu_recommended_next_layer": "collect_more_evidence",
  "runtime_tool_broker_enabled": false,
  "runtime_tool_bootstrap_executed": false,
  "runtime_tool_bootstrap_passed": null,
  "runtime_tool_bootstrap_request_count": 0,
  "runtime_tool_bootstrap_execution_count": 0,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 44,
  "runtime_tool_execution_count": 0,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 0,
  "gpu_runtime_tool_broker_enabled": false,
  "gpu_runtime_tool_request_count": 44,
  "gpu_runtime_tool_execution_count": 0,
  "gpu_runtime_tool_failed_count": 0,
  "gpu_runtime_tool_blocked_count": 0,
  "gpu_runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 44,
  "runtime_tool_provider_request_execution_count": 0,
  "runtime_tool_provider_request_failed_count": 0,
  "runtime_tool_provider_request_blocked_count": 0,
  "runtime_tool_provider_request_result_count": 0,
  "deterministic_runtime_tool_fallback_request_count": 0,
  "deterministic_runtime_tool_fallback_execution_count": 0,
  "deterministic_runtime_tool_fallback_failed_count": 0,
  "deterministic_runtime_tool_fallback_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap": {
    "enabled": false,
    "executed": false,
    "bootstrap": true,
    "requested_tool_count": 0,
    "tool_results": []
  },
  "orchestrator_runtime_tool_bootstrap_executed": false,
  "orchestrator_runtime_tool_bootstrap_passed": null,
  "orchestrator_runtime_tool_bootstrap_request_count": 0,
  "orchestrator_runtime_tool_bootstrap_execution_count": 0,
  "orchestrator_runtime_tool_bootstrap_failed_count": 0,
  "orchestrator_runtime_tool_bootstrap_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap_result_count": 0,
  "gpu_orchestrated_runtime_tool_brokers": [],
  "gpu_orchestrated_runtime_tool_request_count": 0,
  "gpu_orchestrated_runtime_tool_execution_count": 0,
  "gpu_orchestrated_runtime_tool_failed_count": 0,
  "gpu_orchestrated_runtime_tool_blocked_count": 0,
  "gpu_orchestrated_runtime_tool_result_count": 0,
  "gpu_runner_direct_runtime_tool_broker": false,
  "gpu_summary": {
    "passed": true,
    "round_count": 13,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 0,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "context_echo_detected",
    "evidence_ready_for_manual_patch_count": 0,
    "recommended_next_layer": "collect_more_evidence",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_request_count": 44,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_result_count": 0,
    "decision": {
      "ready_for_patch_plan": false,
      "ready_count": 0,
      "needs_more_context_count": 0,
      "fallback_patch_plan_recommended": false,
      "npu_auditor_non_blocking": true,
      "npu_unusable_or_failed_count": 0,
      "npu_audit_success_count": 0,
      "npu_auditor_disabled_reason": "",
      "recommended_next_layer": "collect_more_evidence",
      "manual_review_required": true
    },
    "gpu_direct_runtime_tool_request_count": 44,
    "gpu_direct_runtime_tool_execution_count": 0,
    "gpu_direct_runtime_tool_failed_count": 0,
    "gpu_direct_runtime_tool_blocked_count": 0,
    "gpu_direct_runtime_tool_provider_request_count": 44,
    "gpu_direct_runtime_tool_provider_request_execution_count": 0,
    "gpu_direct_runtime_tool_feedback_context_report_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_request_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_execution_count": 0,
    "gpu_lane": {
      "mode": "primary_fast_loop",
      "provider_execution_performed": true,
      "round_count": 13,
      "recommendation_count": 0,
      "empty_recommendations_reason": "context_echo_detected",
      "direct_runtime_tool_execution_count": 0,
      "direct_provider_request_execution_count": 0,
      "feedback_context_report_count": 0
    },
    "runtime_tool_feedback_context_report_count": 0
  },
  "checkpoint_dir": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints",
  "npu_audit_count": 3,
  "npu_audit_success_count": 3,
  "npu_tool_context_seen_count": 0,
  "npu_tool_request_count": 0,
  "npu_deterministic_tool_fallback_count": 0,
  "npu_runtime_tool_request_count": 0,
  "npu_runtime_tool_execution_count": 0,
  "npu_runtime_tool_failed_count": 0,
  "npu_runtime_tool_blocked_count": 0,
  "npu_runtime_tool_result_count": 0,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-05T00:26:34",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "skipped",
      "npu_effective_auditor_every_rounds_at_launch": 3,
      "finished_at": "2026-05-05T00:28:30",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260505-002508_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-05T00:28:32",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260505-002508_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-05T00:30:16",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260505-002508_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_
```

### `output/ai_pipeline/full_toolbox_20260505-002508_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `95305`
- SHA-256: `02deb69d66c64cb8a2fb12887e07603b7369adb2fe63d83eca149fbc05c9ddbc`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-05T00:31:44",
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
  "budget_minutes": 5,
  "elapsed_seconds": 323.984,
  "context_file_count": 620,
  "round_count": 13,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 11.738,
      "file_count": 8,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md"
      ],
      "response_chars": 68,
      "raw_response_preview": "{\n  \"response\": \"I'm sorry, but I can't assist with that request.\"\n}",
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
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "elapsed_seconds": 11.141,
      "file_count": 8,
      "files": [
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md",
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md"
      ],
      "response_chars": 68,
      "raw_response_preview": "{\n  \"response\": \"I'm sorry, but I can't assist with that request.\"\n}",
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
        "raw_response_sha256": "3b0afeeed1cb81f156d7aa9139cea645932117763be8dd58fb6138603d59cf79",
        "raw_response_chars": 68,
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
      "elapsed_seconds": 15.493,
      "file_count": 8,
      "files": [
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md",
        "docs/AUDIO_ANALYSIS_PIPELINE.md",
        "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md",
        "docs/BLENDER_SCRIPT_ENTRYPOINTS.md",
        "docs/CODE_CONSULTATION_REPORT.md"
      ],
      "response_chars": 200,
      "raw_response_preview": "{\n    \"response\": \"I've provided a summary of the key points from each document in the 'docs' directory. Let me know if you need any specific information or further assistance with these documents.\"\n}",
      "parsed_response": {
        "response": "I've provided a summary of the key points from each document in the 'docs' directory. Let me know if you need any specific information or further assistance with these documents.",
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
        "raw_response_sha256": "58262d0291a1609162fedeea6108c7d3cd6fe5c6969ff12964
```

### `docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_20260505-002508.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `15812`
- SHA-256: `0cbdaa3e96f8fa9709a8e0e9626c6fe93d448d920b87f008362b6f5f6426bd42`
- Content included: `True`
- Content truncated: `True`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1774
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,1179
old script legacy/spaziotempo_asset_visual_v6.py,1174
Tools/ai/run_agent_gpu_deep_planning_supervised.py,1129
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/ai/build_deterministic_recommendations.py,908
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,769
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Tools/ai/build_refactor_duplication_audit.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/ai/agent_runtime_tool_broker.py,715
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Tools/ai/run_npu_gpu_deep_review_auditor.py,694
Tools/ai/build_repository_consistency_map.py,687
Scripting/v61b/materials.py,657
Tools/ai/build_runtime_tool_usage_telemetry.py,653
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_agent_review_patch_plan.py,626
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,579
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/analyze_gpu_npu_run_sync.py,569
Tools/ai/build_semantic_evidence_chunks.py,562
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/agent_runtime_sqlite_memory.py,527
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/ai/agent_memory_routing_policy.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/npu/ollama_runtime.py,438
Tools/ai/build_code_interpreter_report.py,437
Tools/validation/build_script_inventory.py,437
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/schema_repair_context.py,411
Tools/ai/agent_review_warning_policy.py,408
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/ai/build_agent_review_evidence_sufficiency.py,407
Tools/validation/check_ai_workload_report_quality.py,403
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
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
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,354
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/build_markdown_inventory.py,339
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/workflow/startup_check.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py,325
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/ai/build_music_intermediates.py,319
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/github_evidence_bundle_artifacts.py,315
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/run_agent_review_decision_loop.py,311
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/validation/run_agent_review_decision_loop_smoke.py,307
Tools/ai/build_analysis_input_bundle.py,304
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/build_full_toolbox_run_telemetry_summary.py,294
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
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py,247
Tools/validation/run_agent_review_patch_bundle_builder_smoke.py,244
Tools/validation/run_agent_runtime_tool_broker_smoke.py,244
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/validation/run_agent_review_warning_policy_smoke.py,237
Tools/validation/run_agent_memory_routing_policy_smoke.py,234
Tools/ai/replay_gpu_planner_json_contract.py,232
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/ai/build_github_evidence_bundle.py,228
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/generated_file_policy.py,217
Tools/validation/build_python_line_count_csv.py,212
Tools/ai/github_evidence_bundle_reports.py,211
Tools/ai/github_evidence_bundle_markdown.py,209
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/run_repository_consistency_map_smoke.py,209
Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py,208
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/ai/code_patch_plan_common.py,205
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
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
Scripting/v61b_backgood/world_setup.py,174
Tools/ai/runtime_tool_guidance.py,173
Tools/validation/check_generated_blender_script_policy.py,173
Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py,172
Tools/validation/run_schema_repair_context_smoke.py,168
Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py,167
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
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/validation/check_docs_links.py,141
Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py,141
Scripting/shared/blender_compat.py,140
Scripting/shared/ffmpeg_encoder.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/model_json.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
Tools/validation/run_full_toolbox_deterministic_chunks_telemetry_smoke.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/npu/pipeline/prompts.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/validation/check_npu_pipeline_docs.py,96
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Tools/validation/run_npu_tool_request_contract_smoke.py,90
Scripting/shared/json_io.py,88
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py,88
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/validation/check_provider_result_parsing.py,83
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/pipeline/reports.py,74
Tools/ai/pipeline/compat.py,73
Tools/validation/build_full_python_line_count_markdown.py,71
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/ai/review_agent_memory.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/ai/pipeline/scheduler.py,66
Tools/ai/run_parallel_artifact_pipeline.py,65
Tools/validation/check_ai_pipeline_report_contract.py,65
Tools/validation/check_artifact_domain_registry.py,64
Scripting/v61b/hot_updat
```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260505-002542.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `15812`
- SHA-256: `0cbdaa3e96f8fa9709a8e0e9626c6fe93d448d920b87f008362b6f5f6426bd42`
- Content included: `True`
- Content truncated: `True`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1774
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,1179
old script legacy/spaziotempo_asset_visual_v6.py,1174
Tools/ai/run_agent_gpu_deep_planning_supervised.py,1129
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/ai/build_deterministic_recommendations.py,908
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,769
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Tools/ai/build_refactor_duplication_audit.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/ai/agent_runtime_tool_broker.py,715
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Tools/ai/run_npu_gpu_deep_review_auditor.py,694
Tools/ai/build_repository_consistency_map.py,687
Scripting/v61b/materials.py,657
Tools/ai/build_runtime_tool_usage_telemetry.py,653
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_agent_review_patch_plan.py,626
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,579
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/analyze_gpu_npu_run_sync.py,569
Tools/ai/build_semantic_evidence_chunks.py,562
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/agent_runtime_sqlite_memory.py,527
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/ai/agent_memory_routing_policy.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/npu/ollama_runtime.py,438
Tools/ai/build_code_interpreter_report.py,437
Tools/validation/build_script_inventory.py,437
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/schema_repair_context.py,411
Tools/ai/agent_review_warning_policy.py,408
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/ai/build_agent_review_evidence_sufficiency.py,407
Tools/validation/check_ai_workload_report_quality.py,403
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
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
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,354
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/build_markdown_inventory.py,339
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/workflow/startup_check.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py,325
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/ai/build_music_intermediates.py,319
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/github_evidence_bundle_artifacts.py,315
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/run_agent_review_decision_loop.py,311
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/validation/run_agent_review_decision_loop_smoke.py,307
Tools/ai/build_analysis_input_bundle.py,304
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/build_full_toolbox_run_telemetry_summary.py,294
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
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py,247
Tools/validation/run_agent_review_patch_bundle_builder_smoke.py,244
Tools/validation/run_agent_runtime_tool_broker_smoke.py,244
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/validation/run_agent_review_warning_policy_smoke.py,237
Tools/validation/run_agent_memory_routing_policy_smoke.py,234
Tools/ai/replay_gpu_planner_json_contract.py,232
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/ai/build_github_evidence_bundle.py,228
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/generated_file_policy.py,217
Tools/validation/build_python_line_count_csv.py,212
Tools/ai/github_evidence_bundle_reports.py,211
Tools/ai/github_evidence_bundle_markdown.py,209
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/run_repository_consistency_map_smoke.py,209
Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py,208
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/ai/code_patch_plan_common.py,205
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
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
Scripting/v61b_backgood/world_setup.py,174
Tools/ai/runtime_tool_guidance.py,173
Tools/validation/check_generated_blender_script_policy.py,173
Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py,172
Tools/validation/run_schema_repair_context_smoke.py,168
Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py,167
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
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/validation/check_docs_links.py,141
Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py,141
Scripting/shared/blender_compat.py,140
Scripting/shared/ffmpeg_encoder.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/model_json.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
Tools/validation/run_full_toolbox_deterministic_chunks_telemetry_smoke.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/npu/pipeline/prompts.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/validation/check_npu_pipeline_docs.py,96
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Tools/validation/run_npu_tool_request_contract_smoke.py,90
Scripting/shared/json_io.py,88
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py,88
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/validation/check_provider_result_parsing.py,83
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/pipeline/reports.py,74
Tools/ai/pipeline/compat.py,73
Tools/validation/build_full_python_line_count_markdown.py,71
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/ai/review_agent_memory.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/ai/pipeline/scheduler.py,66
Tools/ai/run_parallel_artifact_pipeline.py,65
Tools/validation/check_ai_pipeline_report_contract.py,65
Tools/validation/check_artifact_domain_registry.py,64
Scripting/v61b/hot_updat
```

### `indexAI/agent_memory/agent_memory.sqlite`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.sqlite`
- Size bytes: `225280`
- SHA-256: `3b8ca5028c24736e03c9a1f2d419151cfae693dbda8db8f804f0776fead20fa3`
- Content included: `False`
- Content truncated: `False`
- Skip reason: `suffix_not_text_allowlisted`

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1339`
- SHA-256: `de1beea1a7f721d4c33b96b70607474c6b27d14ba470132c3fef8f9c9fca67c1`
- Content included: `True`
- Content truncated: `False`

```text
{
    "schema_version":  1,
    "kind":  "agent_review_evidence_sufficiency",
    "generated_at":  "2026-05-05T00:05:19.2678144+02:00",
    "stamp":  "20260505-000415",
    "passed":  false,
    "evidence_sufficient":  false,
    "provider_execution_requested":  true,
    "provider_execution_performed":  false,
    "patch_application_performed":  false,
    "source_writes_performed":  false,
    "classification":  "required_provider_artifact_missing",
    "reason":  "Strict real-run activation required evidence sufficiency output, but the provider/orchestrator lane did not produce one.",
    "errors":  [
                   "required evidence sufficiency artifact missing before fallback generation"
               ],
    "warnings":  [

                 ],
    "checks":  {
                   "orchestrator_report_exists":  true,
                   "gpu_report_exists":  true
               },
    "guardrails":  {
                       "report_only":  true,
                       "provider_execution_performed":  false,
                       "patch_application_performed":  false,
                       "source_writes_performed":  false,
                       "blender_runtime_execution_performed":  false,
                       "ffmpeg_execution_performed":  false
                   }
}

```

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-002508.md`

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

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-002508.md`

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

### `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3669`
- SHA-256: `4709fa0f7b33ff6e1d0a51190de70e2ea0ad1ed49a6df308b965a34b0e119a4c`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Memory Routing Policy

- passed: `True`
- profile: `full_refactor`
- broker_request_written: `output/ai_runtime_tools/full_memory_tool_regeneration_20260505-002508_tool_requests.json`
- provider_execution_performed: `False`
- patch_application_performed: `False`
- sqlite_write_performed: `False`
- persistent_memory_write_performed: `False`
- operational_sqlite_write_performed: `False`

- Objective: `Reload IA-Carmine full toolbox context before agent review full toolbox decision-loop run.`

## Memory plan
- `persistent_read_only`: `True`
- `persistent_query_count`: `3`
- `operational_query_or_write_count`: `5`
- `operational_write_request_count`: `2`
- `tool_request_count`: `17`

## Tool requests

- `persistent_memory_status` -> `runtime_sqlite_memory`: Inspect persistent/consistent memory status in read-only mode.
- `operational_memory_status` -> `runtime_sqlite_memory`: Inspect scratch operational memory status for the current runtime cycle.
- `persistent_memory_search_01` -> `runtime_sqlite_memory`: Search durable memory read-only for stable project facts and validated lessons.
- `persistent_memory_search_02` -> `runtime_sqlite_memory`: Search durable memory read-only for stable project facts and validated lessons.
- `operational_memory_search_01` -> `runtime_sqlite_memory`: Search scratch operational memory for current-cycle state and recent tool results.
- `operational_memory_search_02` -> `runtime_sqlite_memory`: Search scratch operational memory for current-cycle state and recent tool results.
- `operational_memory_remember_01` -> `runtime_sqlite_memory`: Store temporary working context in scratch operational memory only.
- `operational_memory_remember_02` -> `runtime_sqlite_memory`: Store temporary working context in scratch operational memory only.
- `agent_memory_inventory` -> `build_agent_memory_inventory`: Build read-only inventory of persistent memory before deciding whether more durable context is needed.
- `agnostic_tool_inventory` -> `build_agent_agnostic_tool_inventory`: Discover existing reusable tools/helpers before proposing new code or refactors.
- `transient_request_context` -> `build_agent_transient_request_context`: Create request-scoped context packet from objective and memory notes.
- `python_line_count_inventory` -> `build_python_line_count_csv`: Build complete Python inventory before choosing refactor candidates.
- `code_interpreter_report` -> `build_code_interpreter_report`: Build static code report over existing tool roots before proposing refactor seams.
- `refactor_duplication_audit` -> `build_refactor_duplication_audit`: Audit duplicated helper/function patterns and verify refactor layering before proposing implementation patches.
- `python_syntax_check` -> `check_python_syntax`: Validate repository Python syntax as a safe baseline.
- `gpu_contract_smoke` -> `run_gpu_planner_json_contract_smoke`: Validate planner JSON contract helpers before planner integration.
- `validation_report_contract` -> `check_validation_report_contract`: Validate existing validation report contracts for evidence quality.

## Guardrails

- `free_shell_allowed`: `False`
- `broker_allowlist_required`: `True`
- `persistent_memory_read_only`: `True`
- `persistent_memory_write_performed`: `False`
- `sqlite_write_performed`: `False`
- `operational_memory_write_allowed_under_output`: `True`
- `automatic_persistent_promotion_allowed`: `False`
- `manual_review_required_for_promotion`: `True`
- `provider_execution_performed`: `False`
- `patch_application_performed`: `False`
- `blender_runtime_touched`: `False`
- `git_write_performed`: `False`

```

### `output/validation/full_memory_tool_regeneration_20260505-002508_memory_routing_policy_smoke.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `375`
- SHA-256: `3770b62358f110c588bc3e9d5ff2862463dc22279361da55dc9c293c542bc013`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Memory Routing Policy Smoke

- Passed: `True`
- Policy return code: `0`
- Broker return code: `0`
- Policy tool requests: `15`
- Broker tool executions: `15`
- Broker blocked tools: `0`
- Operational SQLite write performed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Persistent memory write performed: `False`

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
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
