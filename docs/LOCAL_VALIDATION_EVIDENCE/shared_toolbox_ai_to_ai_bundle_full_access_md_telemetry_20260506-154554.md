# Local Validation Evidence Bundle

- Generated at: `2026-05-06T15:47:25`
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

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.json`

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

### `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json`

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

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `20`

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `False`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Errors: `['GPU output missing: output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json']`

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_parallel_report`
- Passed: `False`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Errors: `['required GPU provider artifact missing before fallback generation']`

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
- Usable lanes: `['npu']`
- Unusable lanes: `[]`
- Warnings: `['ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `162`

### `output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_usage_telemetry`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_capability_manifest`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `shared_toolbox_ai_to_ai_final_summary`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `20`
- Errors: `['GPU output missing: output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json', 'required GPU provider artifact missing before fallback generation', 'ollama: probe failed']`
- Warnings: `['patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection', 'max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/validation/docs_links_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `docs_links`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_memory_routing_policy.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_memory_routing_policy_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_routing_policy_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_operational_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_persistent_memory_status.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_sqlite_memory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_python_line_count.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_python_syntax.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_runtime_tool_broker.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_runtime_tool_broker_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `markdown_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['This inventory is evidence for review. It does not delete or rewrite Markdown files.', 'A missing index reference is not automatically obsolete; it means the file needs owner/lifecycle review.', 'GitHub templates and root community docs are repository controls, not prune candidates.']`

### `output/validation/runtime_tool_bootstrap_requests_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `runtime_tool_bootstrap_requests`
- Passed: `None`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/runtime_tool_broker_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `script_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/validation_report_contract_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/validation/validation_report_contract_json_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/analysis/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_code_interpreter.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `143`

### `output/analysis/gpu_json_contract_replay_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agent_memory_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_memory_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agnostic_tool_inventory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_agnostic_tool_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_transient_request_context.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_transient_request_context`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Patch plan summary

### `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json`

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

#### consistency_042 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_043 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_044 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_045 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_046 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_047 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:184` targeting `Tools/workflow/example_runner/phase.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:184`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner/phase.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_048 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.json` exists=`True` size=`3042` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json` exists=`True` size=`232936` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json` exists=`True` size=`177388` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json` exists=`True` size=`1249` suffix=`.json` preview_chars=`1216`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json` exists=`True` size=`10095` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json` exists=`True` size=`1280` suffix=`.json` preview_chars=`1245`
- `output/validation/local_provider_probe.json` exists=`True` size=`2528` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_workload_report_quality.json` exists=`True` size=`2951` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`7625018` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1225` suffix=`.json` preview_chars=`1186`
- `output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1916927` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`3160` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`70162` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`10055` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`14008` suffix=`.json` preview_chars=`1500`
- `output/analysis/shared_toolbox_ai_to_ai_final_summary_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1462468` suffix=`.json` preview_chars=`1500`
- `output/validation/docs_links_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`200544` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_memory_routing_policy.json` exists=`True` size=`8950` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_memory_routing_policy_smoke.json` exists=`True` size=`2972` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_operational_memory_status.json` exists=`True` size=`1703` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_persistent_memory_status.json` exists=`True` size=`1779` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_python_line_count.json` exists=`True` size=`3215` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_python_syntax.json` exists=`True` size=`70162` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_runtime_tool_broker.json` exists=`True` size=`98206` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_runtime_tool_broker_smoke.json` exists=`True` size=`2001` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_validation_report_contract.json` exists=`True` size=`3667` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_workflow.json` exists=`True` size=`5621` suffix=`.json` preview_chars=`1500`
- `output/validation/markdown_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`481630` suffix=`.json` preview_chars=`1500`
- `output/validation/runtime_tool_bootstrap_requests_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`2097` suffix=`.json` preview_chars=`1500`
- `output/validation/runtime_tool_broker_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`27339` suffix=`.json` preview_chars=`1500`
- `output/validation/script_inventory_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`531699` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`2124` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_json_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1353` suffix=`.json` preview_chars=`1306`
- `output/analysis/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_code_interpreter.json` exists=`True` size=`1734584` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1710` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`4805` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agent_memory_inventory.json` exists=`True` size=`13528` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agnostic_tool_inventory.json` exists=`True` size=`825181` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_transient_request_context.json` exists=`True` size=`9336` suffix=`.json` preview_chars=`1500`

## Included artifact contents

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

### `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `17740`
- SHA-256: `be05a3090e22534418bc6eb0f3f9fdbd7a76f0c81bccd77c1833181dddd08db7`
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

- `orchestrator`: `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json`
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

### consistency_042 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_043 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_044 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without for
```

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1404`
- SHA-256: `91c98cad59b93499962a254a2fc3de8252983c4b5c5d2614efaebf4030821619`
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

- `recommendations`: `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json` exists=`True` size=`177388`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.md` exists=`True` size=`25608`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json` exists=`True` size=`1249`
- `patch_plan`: `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json` exists=`True` size=`232936`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.md` exists=`True` size=`17740`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `25608`
- SHA-256: `1e72c7ce08f0d14f979e143fee7b7ad04ff16cd8ecd492dd837cc1717ed1ee67`
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

### consistency_042 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_043 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_044 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATG
```

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2177`
- SHA-256: `e9c3555eeadaae61d1bd6f739b9732ee18267d3167be0cd1f9d76fff7f46755b`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `False`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `1`
- `elapsed_seconds`: `2.01`
- `npu_audit_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `None`
- `gpu_empty_recommendations_reason`: ``
- `gpu_evidence_ready_for_manual_patch_count`: `0`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `0`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `0`
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
- `recommended_next_layer`: `None`
- `gpu_empty_recommendations_reason`: ``
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
- `npu_lane_mode`: `skipped`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `3`

## NPU Audits

```

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `305`
- SHA-256: `22b682c90704a13c5ce182baad618a26f0a02731988efd44a7febed25f171acf`
- Content included: `True`
- Content truncated: `False`

```text
# Required GPU provider fallback

- Passed: `False`
- Provider execution requested: `True`
- Provider execution performed: `False`
- Classification: `required_provider_artifact_missing`

Strict real-run activation required GPU primary advisory output, but the provider lane did not produce it.

```

### `output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `55673`
- SHA-256: `e515d482bb82a724ae50d45c7ff189ff1ac6bd4f295a82fd206ae258f1de0e77`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `10107`
- Markdown files: `571`
- Python files: `583`
- Markdown references: `61370`
- Markdown Python commands: `812`
- Provider execution performed: `False`
- Workers requested: `8`
- Total build seconds: `46.573`
- Markdown scan seconds: `40.907`
- Python inventory seconds: `2.511`
- Patch application performed: `False`

## Severity counts

- `high`: `2566`
- `low`: `46`
- `medium`: `7495`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `46`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `7493`
- `md_mentions_missing_powershell_path`: `226`
- `md_mentions_missing_python_path`: `2299`
- `md_python_command_script_missing`: `41`

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 280 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 281 | `patches/00_check_repo_ready.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `AGENTS.md` | 137 | `text
CHATGPT.md                         # root pointer
CHATGPT/README.md                  # index and reading order
CHATGPT/next-chat-handoff-*.md     # current handoff state
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 278 | `text
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
| `high` | `md_mentions_missing_python_path` | `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` | 29 | `run_patch_bundle.py` | Correct the documentation reference or restore t
```

### `output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `381`
- SHA-256: `f24177b9be31b7fd9553a7c1f1dbd37d27ae183a96a5cb54cc089311eca92ea1`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Consistency Map Smoke

- Passed: `True`
- Return code: `0`
- Mapper report reused: `True`
- Workers requested: `8`
- Elapsed seconds: `0.034`
- Finding count: `10107`
- Markdown reference count: `61370`
- Markdown Python command count: `812`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`

```

### `output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7065`
- SHA-256: `7a30e1fdc69fd6fa626a838104948e722bc38ebf9a77508666542246fe56c729`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `534`
- Parsed files: `534`
- Total lines: `91083`
- Total functions: `3306`
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

### `output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1760`
- SHA-256: `0b3f1d858ce20a8f4098fc3b4a03fa87cbec90cf41443f95c5dadf34ea00eafd`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260506-154628.csv`
- File count: `583`
- Total lines: `108633`
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

### `output/validation/python_line_count_all_python_files_full_access_md_telemetry_20260506-154554.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `34855`
- SHA-256: `3a8bfd2a70819dc1db0f81068d42aae085d4732814627b39f8696bdb8eb5955d`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: full_access_md_telemetry_20260506-154554
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260506-154628.csv
- File count: 583
- Total Python lines: 108633
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
| 498 | `Tools/docs/build_code_aware_md_coherence.py` |
| 497 | `Tools/validation/ai_pipeline_report_contracts.py` |
| 490 | `Tools/npu/npu_guardrail_service.py` |
| 489 | `Tools/ai/refine_megalithic_review_signals.py` |
| 487 | `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| 483 | `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` |
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
| 221 | `Tools/validation/check_file_line_limits.py` |
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

```

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.md`

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

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.md`

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

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.md`

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

### `output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.md`

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

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1241`
- SHA-256: `5ec0e5c6c9dd57778ef72ba2469ce4cb32c19f6924e0bc348b9214a65b6ee954`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Usage Telemetry

- Passed: `True`
- Stamp: `full_access_md_telemetry_20260506-154554`
- Tool call entries: `3`
- Executed count: `3`
- Failed count: `0`
- Blocked count: `0`
- Total reported tool elapsed seconds: `0.0`
- Declared runtime tool requests: `0`
- Broker runtime tool executions: `0`
- Declared not executed count: `0`

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

### `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7678`
- SHA-256: `0bc387fc9546a50e15361ce4d14e96c1748a9ed0fadf0c54d4b93c96807c400e`
- Content included: `True`
- Content truncated: `False`

```text
# Runtime Tool Capability Manifest

- Passed: `True`
- Tool count: `10`
- Declared runtime tool requests: `0`
- Broker runtime tool executions: `0`
- Declared not executed count: `0`
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
- `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_full_access_md_telemetry_20260506-154554.json` role=`observed_runtime_tool_usage_report` exists=`True` sha256=`0197fdfd7a8f75bc7a5aadfba8961b9d081c025c131631c74da72ceb3759235b`

```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `497044`
- SHA-256: `0256e6f618bff8d023047ba07946fd4eb578a0e43eda1c3f90eaf66bc2896dad`
- Content included: `True`
- Content truncated: `True`

```text
# Shared Toolbox AI-to-AI Final Summary

- stamp: full_access_md_telemetry_20260506-154554
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
- Provider advisory state: `recovered_degraded_provider`
- Provider failure reasons:
  - output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json: GPU output missing: output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json
  - output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json: GPU primary advisory output was required by strict real-run activation but was not produced.
  - output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json: required GPU provider artifact missing before fallback generation
  - output/validation/local_provider_probe.json: ollama: probe failed
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json` kind=`agent_gpu_npu_parallel_orchestrator` passed=`False` provider_execution_performed=`True` errors=`['GPU output missing: output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json']`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json` kind=`agent_gpu_parallel_report` passed=`False` provider_execution_performed=`False` errors=`['required GPU provider artifact missing before fallback generation']`
- `output/validation/local_provider_probe.json` kind=`local_provider_probe` passed=`False` provider_execution_performed=`True` errors=`['ollama: probe failed']`
- `output/validation/ai_workload_report_quality.json` kind=`ai_workload_report_quality` passed=`True` provider_execution_performed=`False` errors=`[]`

## Patch plan summary

- Seen: `True`
- Source: `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json`
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

- output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.json exists=True json_ok=True kind=agent_review_decision_loop passed=True
- output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json exists=True json_ok=True kind=agent_review_patch_plan passed=True
- output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer passed=True
- output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json exists=True json_ok=True kind=deterministic_recommendation_patch_plan_bridge_orchestrator passed=True
- output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json exists=True json_ok=True kind=agent_gpu_npu_parallel_orchestrator passed=False
- output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json exists=True json_ok=True kind=agent_gpu_parallel_report passed=False
- output/validation/local_provider_probe.json exists=True json_ok=True kind=local_provider_probe passed=False
- output/validation/ai_workload_report_quality.json exists=True json_ok=True kind=ai_workload_report_quality passed=True
- output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=repository_consistency_map passed=True
- output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=repository_consistency_map_smoke passed=True
- output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=code_interpreter_report passed=True
- output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=python_line_count_csv passed=True
- output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=python_syntax passed=True
- output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=gpu_planner_json_contract_smoke passed=True
- output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=deterministic_recommendation_synthesizer_smoke passed=True
- output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=agent_review_decision_loop_smoke passed=True
- output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=npu_provider_environment passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=runtime_tool_usage_telemetry passed=True
- docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_full_access_md_telemetry_20260506-154554.json exists=True json_ok=True kind=runtime_tool_capability_manifest passed=True

## Remaining gaps

- output/validation/shared_toolbox_python_syntax_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/analysis/shared_toolbox_code_interpreter_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/validation/shared_toolbox_gpu_contract_smoke_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/validation/shared_toolbox_gpu_routing_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/validation/shared_toolbox_npu_execution_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/validation/shared_toolbox_npu_contract_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/validation/npu_provider_environment_shared_toolbox_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_full_access_md_telemetry_20260506-154554_orchestrator.json: optional report missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_full_access_md_telemetry_20260506-154554_gpu.json: optional report missing
- output/analysis/shared_toolbox_gpu_npu_sync_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/analysis/shared_toolbox_gpu_contract_replay_full_access_md_telemetry_20260506-154554.json: optional report missing
- output/validation/agent_review_full_toolbox_decision_loop_full_access_md_telemetry_20260506-154554_integrated.json: optional report missing
- output/validation/agent_review_full_toolbox_decision_loop_full_access_md_telemetry_20260506-154554_workflow.json: optional report missing
- output/validation/agent_review_warning_policy_full_access_md_telemetry_20260506-154554.json: optional report missing
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_full_access_md_telemetry_20260506-154554.json: optional report missing
- docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_full_access_md_telemetry_20260506-154554_cloud_semantic_deterministic_chunk_manifest.json: optional report missing
- docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md: optional artifact missing
- output/analysis/shared_toolbox_code_interpreter_full_access_md_telemetry_20260506-154554.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_full_access_md_telemetry_20260506-154554_orchestrator.md: optional artifact missing
- output/ai_pipeline/shared_toolbox_ai_to_ai_full_access_md_telemetry_20260506-154554_gpu.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_npu_sync_full_access_md_telemetry_20260506-154554.md: optional artifact missing
- output/analysis/shared_toolbox_gpu_contract_replay_full_access_md_telemetry_20260506-154554.md: optional artifact missing
- output/analysis/shared_toolbox_ai_to_ai_final_summary_full_access_md_telemetry_20260506-154554.md: optional artifact missing
- output/validation/agent_review_full_toolbox_decision_loop_full_access_md_telemetry_20260506-154554_integrated.md: optional artifact missing
- output/validation/agent_review_full_toolbox_decision_loop_full_access_md_telemetry_20260506-154554_workflow.md: opt
```

### `output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1916927`
- SHA-256: `0c80f71aa4f71e6103934c7d4e7432e8a14df35d96fdbc0ed939ab402ff93b30`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-06T15:46:32",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 534,
  "parsed_file_count": 534,
  "total_lines": 91083,
  "total_functions": 3306,
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
      "count": 477
    },
    {
      "module": "pathlib",
      "count": 368
    },
    {
      "module": "typing",
      "count": 336
    },
    {
      "module": "config",
      "count": 320
    },
    {
      "module": "json",
      "count": 276
    },
    {
      "module": "argparse",
      "count": 232
    },
    {
      "module": "sys",
      "count": 175
    },
    {
      "module": "datetime",
      "count": 161
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
    "low": 372,
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

### `output/analysis/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_code_interpreter.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1734584`
- SHA-256: `0fdb42e33f73cec4f986d486c1033f046138692e724755ea9ff5aa42e8d5c303`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-06T15:46:19",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 492,
  "parsed_file_count": 492,
  "total_lines": 80478,
  "total_functions": 3025,
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
      "count": 470
    },
    {
      "module": "pathlib",
      "count": 352
    },
    {
      "module": "typing",
      "count": 330
    },
    {
      "module": "json",
      "count": 270
    },
    {
      "module": "argparse",
      "count": 232
    },
    {
      "module": "sys",
      "count": 169
    },
    {
      "module": "datetime",
      "count": 161
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
    "low": 349,
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

### `output/analysis/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_code_interpreter.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7338`
- SHA-256: `ec6bf4cbc43daa957e75eb7df7f625886382dacfd6fc8d32943518c866d4b195`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `492`
- Parsed files: `492`
- Total lines: `80478`
- Total functions: `3025`
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

### `output/analysis/gpu_json_contract_replay_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1710`
- SHA-256: `fe0b74fa75cc0f8466a79fdccd85b90ceb1385304607c9058151751df0055efb`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_planner_json_contract_replay",
  "generated_at": "2026-05-06T15:47:22",
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
    "gpu_report": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json"
  },
  "source_summary": {
    "kind": "agent_gpu_parallel_report",
    "passed": false,
    "round_count": null,
    "recommendation_count": 0,
    "json_parse_error_count": null,
    "repair_attempt_count": null,
    "empty_recommendations_reason": null,
    "evidence_ready_for_manual_patch_count": 0
  },
  "replayed_round_count": 0,
  "contract_reason_counts": {},
  "context_echo_detected_count": 0,
  "json_parse_failure_count": 0,
  "model_output_schema_mismatch_count": 0,
  "valid_recommendation_output_count": 0,
  "rounds": [],
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

### `output/analysis/gpu_json_contract_replay_full_toolbox_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `567`
- SHA-256: `3f81984f70c09bb0856919dfcf7026e22231b54b617603673abe5e4d88b2c20a`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `0`
- Context echo detected: `0`
- JSON parse failures: `0`
- Schema mismatches: `0`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts


## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `4805`
- SHA-256: `795381a201d910c11be866aee04775bde0e9e2b4c918d3ccaf738227a31b45da`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-06T15:47:22",
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
    "orchestrator": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 0,
    "npu_audit_count": 0,
    "npu_audit_success_count": 0,
    "npu_audit_round_coverage": 0.0,
    "avg_gpu_round_seconds": 0.0,
    "p50_gpu_round_seconds": 0.0,
    "p90_gpu_round_seconds": 0.0,
    "avg_npu_audit_seconds": 0.0,
    "p50_npu_audit_seconds": 0.0,
    "p90_npu_audit_seconds": 0.0,
    "npu_to_gpu_avg_duration_ratio": 0.0,
    "gpu_elapsed_seconds": 2.01,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "unavailable"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.0,
    "gpu": {
      "elapsed_seconds": 2.01,
      "round_count": 0,
      "round_duration_source": "unavailable",
      "round_duration_sample_count": 0,
      "avg_round_seconds": 0.0,
      "p50_round_seconds": 0.0,
      "p90_round_seconds": 0.0,
      "max_round_seconds": 0.0,
      "round_durations_total_seconds": 0.0,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 0,
        "runtime_tool_execution_count": 0,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 0,
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
      "gpu_metrics_source": "unavailable"
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
      "No NPU audits were observed; first verify provider availability before tuning cadence."
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
      "evidence": "gpu_metrics_source=unavailable",
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

### `output/analysis/gpu_npu_run_sync_full_toolbox_full_access_md_telemetry_20260506-154554.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1982`
- SHA-256: `49c39b163ae903ec4370c66a94f1ab3375c5dbf4b5936af0e459cc2aa315cacb`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `0`
- `npu_audit_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_audit_round_coverage`: `0.0`
- `avg_gpu_round_seconds`: `0.0`
- `p50_gpu_round_seconds`: `0.0`
- `p90_gpu_round_seconds`: `0.0`
- `avg_npu_audit_seconds`: `0.0`
- `p50_npu_audit_seconds`: `0.0`
- `p90_npu_audit_seconds`: `0.0`
- `npu_to_gpu_avg_duration_ratio`: `0.0`
- `gpu_elapsed_seconds`: `2.01`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `unavailable`

## Performance

- Analyzer elapsed seconds: `0.0`
- GPU elapsed seconds: `2.01`
- GPU average round seconds: `0.0`
- GPU timing source: `unavailable`
- GPU timing sample count: `0`
- GPU round durations total seconds: `0.0`
- NPU average audit seconds: `0.0`
- NPU duration sample count: `0`

## Operational opinions

- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=unavailable

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


```

### `output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `7625018`
- SHA-256: `04ae76554eca613860b6e84a6878bf3f7abca23ed51da2b598fb58001264eac3`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "repository_consistency_map",
  "generated_at": "2026-05-06T15:47:20",
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
    "markdown_file_count": 571,
    "python_file_count": 583,
    "markdown_reference_count": 61370,
    "markdown_python_command_count": 812,
    "python_inventory_count": 583,
    "generated_evidence_chunk_exclusion_enabled": true
  },
  "finding_count": 10107,
  "severity_counts": {
    "high": 2566,
    "low": 46,
    "medium": 7495
  },
  "finding_kind_counts": {
    "documented_python_script_without_obvious_smoke": 46,
    "md_cli_arg_not_in_argparse": 2,
    "md_mentions_missing_markdown_path": 7493,
    "md_mentions_missing_powershell_path": 226,
    "md_mentions_missing_python_path": 2299,
    "md_python_command_script_missing": 41
  },
  "markdown_reference_kind_counts": {
    "artifact": 10853,
    "markdown": 16745,
    "powershell": 1102,
    "python": 32670
  },
  "findings": [
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AGENTS.md",
      "line": 280,
      "target": "run_patch_bundle.py",
      "evidence": "run_patch_bundle.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AGENTS.md",
      "line": 281,
      "target": "patches/00_check_repo_ready.py",
      "evidence": "patches/00_check_repo_ready.py",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_markdown_path",
      "severity": "medium",
      "source": "AGENTS.md",
      "line": 137,
      "target": "text\nCHATGPT.md                         # root pointer\nCHATGPT/README.md                  # index and reading order\nCHATGPT/next-chat-handoff-*.md     # current handoff state\nCHATGPT/chatgpt-session-problems-and-robust-fixes-*.md",
      "evidence": "```text",
      "recommendation": "Correct the documentation reference or restore the missing target if it is still required."
    },
    {
      "kind": "md_mentions_missing_python_path",
      "severity": "high",
      "source": "AGENTS.md",
      "line": 278,
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
      "r
```

### `output/analysis/shared_toolbox_ai_to_ai_final_summary_full_access_md_telemetry_20260506-154554.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1462468`
- SHA-256: `d028eeb63b65d241243e3ad2ee06834fee412b21e3abbb466f19a08325f9b31d`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "shared_toolbox_ai_to_ai_final_summary",
  "stamp": "full_access_md_telemetry_20260506-154554",
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
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop",
      "passed": true
    },
    {
      "path": "output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_patch_plan",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
      "passed": true
    },
    {
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": false
    },
    {
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_parallel_report",
      "passed": false
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
      "path": "output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map",
      "passed": true
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map_smoke",
      "passed": true
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "code_interpreter_report",
      "passed": true
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_line_count_csv",
      "passed": true
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_syntax",
      "passed": true
    },
    {
      "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_planner_json_contract_smoke",
      "passed": true
    },
    {
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer_smoke",
      "passed": true
    },
    {
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop_smoke",
      "passed": true
    },
    {
      "path": "output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_provider_environment",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "runtime_tool_usage_telemetry",
      "passed": true
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_full_access_md_telemetry_20260506-154554.json",
      "exists": true,
      "json_ok": true,
      "kind": "runtime_tool_capability_manifest",
      "passed": true
    }
  ],
  "remaining_gaps": [
    {
      "path": "output/validation/shared_toolbox_python_syntax_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/analysis/shared_toolbox_code_interpreter_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_contract_smoke_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_gpu_routing_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_execution_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/shared_toolbox_npu_contract_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/validation/npu_provider_environment_shared_toolbox_full_access_md_telemetry_20260506-154554.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_full_access_md_telemetry_20260506-154554_orchestrator.json",
      "reason": "optional report missing"
    },
    {
      "path": "output/ai_pipeline/shared_toolbox_ai_to_ai_full_access_md_telemetry_20260506-154554_gpu.json",
      "
```

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agent_memory_inventory.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `13528`
- SHA-256: `f57701496579fa833a2474dc4635a125af0055697a984558bc06f038d3666e1a`
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
        "row_count": 94,
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
    "record_count": 94,
    "total_content_chars": 381637,
    "kind_counts": {
      "source_file": 92,
      "operator_note": 2
    },
    "scope_counts": {
      "project": 92,
      "task": 2
    },
    "top_sources": {
      "output/ai_context_packs/full_context_golden_core_ai_backend.json": 13,
      "output/ai_context_packs/full_context_golden_core_ai_backend.md": 13,
      "output/ai_context_packs/full_context_golden_selected_chunks.json": 13,
      "output/ai_context_packs/full_context_golden_selected_chunks.md": 13,
      "indexAI/code_chunks/semantic_code_chunks_manifest.json": 13,
      "output/ai_pipeline/full_context_golden_enrichment_plan.json": 13,
      "output/ai_pipeline/full_context_golden_enrichment_plan.md": 6,
      "cli_note_1": 2,
      "docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md": 2,
      "docs/LOCAL_AI_TASKS/refactor-unused-useful-code-tool-class-promotion-2026-05-05.md": 1,
      "docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md": 1,
      "docs/LOCAL_AI_TASKS/docs-md-obsolete-pruning-next-step.md": 1,
      "docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md": 1,
      "docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md": 1,
      "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md": 1
    },
    "tag_counts": {
      "source_file": 92,
      "json": 52,
      "md": 40,
      "recent": 2,
      "operator_note": 2
    },
    "confidence_buckets": {
      "0.90-1.00": 94
    }
  },
  "policy_report": {
    "kind": "agent_memory_policy_report",
    "passed": true,
    "record_count": 94,
    "promotion_candidate_count": 0,
    "review_count": 0,
    "risk_count": 0,
    "duplicate_group_count": 0,
    "action_counts": {
      "keep": 94
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

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agent_memory_inventory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6728`
- SHA-256: `71bd840a0ee7801e819f25a3e599268df9320ebd3248ebb00f5aabd83c646086`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Memory Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Memory DB: `indexAI/agent_memory/agent_memory.sqlite`
- Memory DB exists: `True`
- Record count: `94`
- SQLite opened read-only: `True`

## SQLite

- Schema version: `1`

- `memory_meta` rows=`1` columns=`2`
- `memory_records` rows=`94` columns=`12`

## Record distributions

### kind_counts

- `source_file`: 92
- `operator_note`: 2

### scope_counts

- `project`: 92
- `task`: 2

### confidence_buckets

- `0.90-1.00`: 94

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

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agnostic_tool_inventory.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `825181`
- SHA-256: `bba0c4a6ff32315b086d6030e691a6b98abf6bc7051068369405d9c093fab409`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_agnostic_tool_inventory",
  "generated_at": "2026-05-06T15:46:11",
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
    "tool_count": 534,
    "category_counts": {
      "support_tool": 164,
      "validator": 162,
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
      "cpu_validation": 83,
      "cpu_orchestration": 34,
      "cpu_proposal_builder": 6,
      "cpu_context_builder": 5
    },
    "consumed_lane_counts": {
      "cpu": 534,
      "npu": 297,
      "gpu_cuda": 226
    },
    "apply_mode_counts": {
      "not_declared": 354,
      "report_only": 143,
      "manual_review_only": 21,
      "explicit_git_operation": 16
    },
    "provider_execution_default_counts": {
      "none_or_reported": 511,
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

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agnostic_tool_inventory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `16334`
- SHA-256: `1fe0e5693e7bf0971f52ac151d403091369daf08e28356bacfcdd182fbb75aa9`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Agnostic Tool Inventory

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Tool count: `534`

## category_counts

- `support_tool`: 164
- `validator`: 162
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
- `cpu_validation`: 83
- `cpu_orchestration`: 34
- `cpu_proposal_builder`: 6
- `cpu_context_builder`: 5

## consumed_lane_counts

- `cpu`: 534
- `npu`: 297
- `gpu_cuda`: 226

## apply_mode_counts

- `not_declared`: 354
- `report_only`: 143
- `manual_review_only`: 21
- `explicit_git_operation`: 16

## provider_execution_default_counts

- `none_or_reported`: 511
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

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_transient_request_context.json`

- Role: `recursive_default_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `9336`
- SHA-256: `cf994f10522dcfddfc38ea248eac18b7d0c77650f82eef910c3fe5ff54a9bf14`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_transient_request_context",
  "generated_at": "2026-05-06T15:46:17",
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
        "path": "output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agent_memory_inventory.json",
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
        "path": "output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "summary": {
            "tool_count": 534,
            "category_counts": {
              "support_tool": 164,
              "validator": 162,
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
              "cpu_validation": 83,
              "cpu_orchestration": 34,
              "cpu_proposal_builder": 6,
              "cpu_context_builder": 5
            },
            "consumed_lane_counts": {
              "cpu": 534,
              "npu": 297,
              "gpu_cuda": 226
            },
            "apply_mode_counts": {
              "not_declared": 354,
              "report_only": 143,
              "manual_review_only": 21,
              "explicit_git_operation": 16
            },
            "provider_execution_default_counts": {
              "none_or_reported": 511,
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
        "path": "output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_persistent_memory_status.json",
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
        "path": "output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_operational_memory_status.json",
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
        "path": "output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_memory_routing_policy.json",
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
        "path": "output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_runtime_tool_broker.json",
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

### `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_transient_request_context.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1904`
- SHA-256: `6cc1c538862ef65241a2961cae4843bc685e65acd5f0756b578f65188c9e6f6b`
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

- `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agent_memory_inventory.json` kind=`agent_memory_inventory` passed=`True` error=``
- `output/ai_pipeline/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_agnostic_tool_inventory.json` kind=`agent_agnostic_tool_inventory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_persistent_memory_status.json` kind=`agent_runtime_sqlite_memory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_operational_memory_status.json` kind=`agent_runtime_sqlite_memory` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_memory_routing_policy.json` kind=`agent_memory_routing_policy` passed=`True` error=``
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_runtime_tool_broker.json` kind=`agent_runtime_tool_broker` passed=`True` error=``

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

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `3042`
- SHA-256: `4b95b0cfeccf330a9b96696d66a2686f57b0e1fdc084134650d9f7d4a6d62ceb`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_review_decision_loop",
  "generated_at": "2026-05-06T15:47:22",
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
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json",
      "exists": true,
      "size_bytes": 177388
    },
    "recommendations_markdown": {
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.md",
      "exists": true,
      "size_bytes": 25608
    },
    "bridge_orchestrator": {
      "path": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json",
      "exists": true,
      "size_bytes": 1249
    },
    "patch_plan": {
      "path": "output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json",
      "exists": true,
      "size_bytes": 232936
    },
    "patch_plan_markdown": {
      "path": "output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.md",
      "exists": true,
      "size_bytes": 17740
    }
  },
  "inputs": {
    "evidence": "output/ai_pipeline/agent_review_evidence_sufficiency.json",
    "orchestrator": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json",
    "gpu_report": ".\\output\\ai_pipeline\\full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json",
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

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1249`
- SHA-256: `bd9d06494ad3c565042258e33b0bf1a48ed76e83daa2787883fbb90a2a89ae8c`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-06T15:47:22",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json",
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

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `177388`
- SHA-256: `67461642bc2601b913c98484ee5d103f28db88054e8c74b29218fe22f414a20e`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_synthesizer",
  "generated_at": "2026-05-06T15:47:22",
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
          "path": "output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/analysis/gpu_json_contract_replay_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_workflow.json",
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
      "npu_audit_refs": [],
      "repository_consistency_finding": {
        "kind": "md_python_command_script_missing",
        "severity": "high",
        "source": "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md",
        "line": 324,
        "target": "Tools/ai/agent_memory_tools.py",
        "flag": "",
        "evidence": "```powershell"
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
        "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md"
      ],
      "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.",
      "proposed_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
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
        "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
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
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json",
          "kind": "agent_review_d
```

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `10095`
- SHA-256: `bab56606d35d80a121494bb6e0eadd99ba64994a8021489bcc14c3f853d1477c`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-06T15:47:22",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": false,
  "errors": [
    "GPU output missing: output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json"
  ],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 2.01,
  "gpu_returncode": 1,
  "gpu_stdout_tail": "",
  "gpu_stderr_tail": "Traceback (most recent call last):\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_supervised.py\", line 1129, in <module>\n    raise SystemExit(main())\n                     ~~~~^^\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_supervised.py\", line 1078, in main\n    report = run_supervised(args)\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_supervised.py\", line 730, in run_supervised\n    evidence = read_json(resolve_path(repo_root, args.evidence))\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_review.py\", line 122, in read_json\n    return json.loads(path.read_text(encoding=\"utf-8-sig\"))\n                      ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Python314\\Lib\\pathlib\\__init__.py\", line 787, in read_text\n    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:\n         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Python314\\Lib\\pathlib\\__init__.py\", line 771, in open\n    return io.open(self, mode, buffering, encoding, errors, newline)\n           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nFileNotFoundError: [Errno 2] No such file or directory: 'C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\agent_review_evidence_sufficiency.json'\n",
  "gpu_output": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.md",
  "gpu_recommendation_count": null,
  "gpu_empty_recommendations_reason": "",
  "gpu_evidence_ready_for_manual_patch_count": 0,
  "gpu_recommended_next_layer": null,
  "runtime_tool_broker_enabled": false,
  "runtime_tool_bootstrap_executed": false,
  "runtime_tool_bootstrap_passed": null,
  "runtime_tool_bootstrap_request_count": 0,
  "runtime_tool_bootstrap_execution_count": 0,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 0,
  "runtime_tool_execution_count": 0,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 0,
  "gpu_runtime_tool_broker_enabled": false,
  "gpu_runtime_tool_request_count": 0,
  "gpu_runtime_tool_execution_count": 0,
  "gpu_runtime_tool_failed_count": 0,
  "gpu_runtime_tool_blocked_count": 0,
  "gpu_runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 0,
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
    "passed": null,
    "round_count": null,
    "recommendation_count": null,
    "raw_recommendation_candidate_count": null,
    "filtered_recommendation_count": null,
    "json_parse_error_count": null,
    "repair_attempt_count": null,
    "empty_recommendations_reason": "",
    "evidence_ready_for_manual_patch_count": 0,
    "recommended_next_layer": null,
    "runtime_tool_broker_enabled": false,
    "runtime_tool_request_count": 0,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_result_count": 0,
    "decision": {},
    "gpu_direct_runtime_tool_request_count": 0,
    "gpu_direct_runtime_tool_execution_count": 0,
    "gpu_direct_runtime_tool_failed_count": 0,
    "gpu_direct_runtime_tool_blocked_count": 0,
    "gpu_direct_runtime_tool_provider_request_count": 0,
    "gpu_direct_runtime_tool_provider_request_execution_count": 0,
    "gpu_direct_runtime_tool_feedback_context_report_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_request_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_execution_count": 0,
    "gpu_lane": {
      "mode": "primary_fast_loop",
      "provider_execution_performed": false,
      "round_count": 0,
      "recommendation_count": 0,
      "empty_recommendations_reason": "",
      "direct_runtime_tool_execution_count": 0,
      "direct_provider_request_execution_count": 0,
      "feedback_context_report_count": 0
    },
    "runtime_tool_feedback_context_report_count": 0
  },
  "checkpoint_dir": "output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_checkpoints",
  "npu_audit_count": 0,
  "npu_audit_success_count": 0,
  "npu_tool_context_seen_count": 0,
  "npu_tool_request_count": 0,
  "npu_deterministic_tool_fallback_count": 0,
  "npu_runtime_tool_request_count": 0,
  "npu_runtime_tool_execution_count": 0,
  "npu_runtime_tool_failed_count": 0,
  "npu_runtime_tool_blocked_count": 0,
  "npu_runtime_tool_result_count": 0,
  "npu_audits": [],
  "decision": {
    "gpu_review_blocked_by_npu": false,
    "npu_auditor_mode": "parallel_best_effort",
    "npu_audit_success_count": 0,
    "npu_tool_context_seen_count": 0,
    "npu_tool_request_count": 0,
    "npu_deterministic_tool_fallback_count": 0,
    "npu_runtime_tool_request_count": 0,
    "npu_runtime_tool_execution_count": 0,
    "npu_runtime_tool_failed_count": 0,
    "npu_runtime_tool_blocked_count": 0,
    "npu_runtime_tool_result_count": 0,
    "ready_for_patch_plan": false,
    "fallback_patch_plan_recommended": false,
    "recommended_next_layer": null,
    "gpu_empty_recommendations_reason": "",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_bootstrap_executed": false,
    "runtime_tool_bootstrap_execution_count": 0,
    "runtime_tool_provider_request_count": 0,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "runtime_tool_execution_count": 0,
    "runtime_tool_result_count": 0,
    "manual_review_required": true,
    "gpu_lane_mode": "primary_fast_loop",
    "npu_lane_mode": "skipped",
    "gpu_direct_runtime_tool_provider_request_execution_count": 0,
    "runtime_tool_feedback_context_report_count": 0,
    "npu_effective_auditor_every_rounds": 3
  },
  "guardrails": {
    "gpu_continues_without_waiting_for_npu": true,
    "npu_auditor_non_blocking": true,
    "npu_primary_advisory": false,
    "patch_application_performed": false,
    "real_github_pr_created": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "runtime_tool_broker_report_only": true,
    "orchestrator_controls_gpu_runtime_tools": true,
    "gpu_runner_direct_runtime_tool_broker": false,
    "npu_runtime_tools_execute_via_broker": true
  },
  "gpu_direct_runtime_tool_request_count": 0,
  "gpu_direct_runtime_tool_execution_count": 0,
  "gpu_direct_runtime_tool_failed_count": 0,
  "gpu_direct_runtime_tool_blocked_count": 0,
  "gpu_direct_runtime_tool_provider_request_count": 0,
  "gpu_direct_runtime_tool_provider_request_execution_count": 0,
  "gpu_direct_runtime_tool_feedback_context_report_count": 0,
  "gpu_direct_deterministic_runtime_tool_fallback_request_count": 0,
  "gpu_direct_deterministic_runtime_tool_fallback_execution_count": 0,
  "gpu_lane_mode": "primary_fast_loop",
  "gpu_lane": {
    "mode": "primary_fast_loop",
    "provider_execution_performed": false,
    "round_count": 0,
    "recommendation_count": 0,
    "empty_recommendations_reason": "",
    "direct_runtime_tool_execution_count": 0,
    "direct_provider_request_execution_count": 0,
    "feedback_context_report_count": 0
  },
  "npu_lane_mode": "skipped",
  "npu_lane": {
    "mode": "skipped",
    "provider_requested": true,
    "audit_count": 0,
    "finished_count": 0,
    "running_count": 0,
    "success_count": 0,
    "failed_count": 0,
    "avg_elapsed_seconds": 0.0,
    "max_elapsed_seconds": 0.0,
    "slow_threshold_seconds": 60.0,
    "base_auditor_every_rounds": 3,
    "slow_auditor_every_rounds": 4,
    "effective_auditor_every_rounds": 3,
    "non_blocking": true
  },
  "runtime_tool_feedback_context_report_count": 0
}

```

### `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1280`
- SHA-256: `01db911751463881c0e7abf34287796a630e51d7bdc36767c5fcf0d89fb101c9`
- Content included: `True`
- Content truncated: `False`

```text
{
    "schema_version":  1,
    "kind":  "agent_gpu_parallel_report",
    "generated_at":  "2026-05-06T15:47:22.5570133+02:00",
    "stamp":  "full_access_md_telemetry_20260506-154554",
    "passed":  false,
    "provider_execution_requested":  true,
    "provider_execution_performed":  false,
    "patch_application_performed":  false,
    "source_writes_performed":  false,
    "classification":  "required_provider_artifact_missing",
    "provider_error":  "GPU primary advisory output was required by strict real-run activation but was not produced.",
    "provider_empty_response":  true,
    "recommendation_count":  0,
    "recommendations":  [

                        ],
    "errors":  [
                   "required GPU provider artifact missing before fallback generation"
               ],
    "warnings":  [

                 ],
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

### `docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_full_access_md_telemetry_20260506-154554.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `29856`
- SHA-256: `8b4b1c67164cc4ccbc6d18d7b4381b124e7b2ef1545d37f3c1a07d31189fd460`
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
Tools/ai/build_deterministic_recommendations.py,909
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,850
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
Tools/ai/build_runtime_tool_usage_telemetry.py,675
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_agent_review_patch_plan.py,626
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/analyze_gpu_npu_run_sync.py,580
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
Tools/ai/agent_memory_routing_policy.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/workflow/startup_check.py,444
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/docs/split_large_markdown.py,438
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
Tools/docs/apply_md_code_coherence_refactor.py,221
Tools/validation/check_file_line_limits.py,221
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
Tools/ai/patch_unified_launcher_light_full0to10.py,204
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
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/ai/full0to10_sqlite_memory/embedding.py,141
Tools/validation/check_docs_links.py,141
Tools/validation/check_markdown_line_limits.py,141
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
Tools/ai/full0to10_effective_use/memory_product.py,123
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/full0to10_final_product_quality/builder.py,108
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/ai/full0to10_provider_feedback_loop/builder.py,106
Tools/ai/full0to10_final_product/builder.py,105
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
Scripting/v61b_backgood
```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260506-154628.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `29856`
- SHA-256: `8b4b1c67164cc4ccbc6d18d7b4381b124e7b2ef1545d37f3c1a07d31189fd460`
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
Tools/ai/build_deterministic_recommendations.py,909
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,850
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
Tools/ai/build_runtime_tool_usage_telemetry.py,675
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_agent_review_patch_plan.py,626
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/analyze_gpu_npu_run_sync.py,580
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
Tools/ai/agent_memory_routing_policy.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/workflow/startup_check.py,444
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/docs/split_large_markdown.py,438
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
Tools/docs/apply_md_code_coherence_refactor.py,221
Tools/validation/check_file_line_limits.py,221
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
Tools/ai/patch_unified_launcher_light_full0to10.py,204
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
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/ai/full0to10_sqlite_memory/embedding.py,141
Tools/validation/check_docs_links.py,141
Tools/validation/check_markdown_line_limits.py,141
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
Tools/ai/full0to10_effective_use/memory_product.py,123
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/full0to10_final_product_quality/builder.py,108
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/ai/full0to10_provider_feedback_loop/builder.py,106
Tools/ai/full0to10_final_product/builder.py,105
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
Scripting/v61b_backgood
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
