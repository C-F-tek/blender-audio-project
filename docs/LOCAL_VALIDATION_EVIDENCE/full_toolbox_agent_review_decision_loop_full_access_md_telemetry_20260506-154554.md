# Local Validation Evidence Bundle

- Generated at: `2026-05-06T15:47:26`
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
- `included_artifact_count`: `24`
- `patch_plan_summary_seen`: `True`

## Reports

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

### `output/ai_pipeline/repository_change_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
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

#### consistency_001 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_002 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_003 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_004 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_005 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141` targeting `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_006 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14` targeting `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md` and resolve `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_007 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_008 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_009 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_010 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_011 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_012 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_013 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

#### consistency_042 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_043 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_044 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_045 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_046 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_047 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:184` targeting `Tools/workflow/example_runner/phase.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:184`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner/phase.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_048 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text
run_unified_full0to10_quality_supervisor.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text
run_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_orchestrator.json` exists=`True` size=`10095` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_parallel_gpu.json` exists=`True` size=`1280` suffix=`.json` preview_chars=`1245`
- `output/analysis/repository_consistency_map_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`7625018` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1225` suffix=`.json` preview_chars=`1186`
- `output/analysis/code_interpreter_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1916927` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`3160` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`70162` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`1710` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_full_access_md_telemetry_20260506-154554.json` exists=`True` size=`4805` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_deterministic_recommendations.json` exists=`True` size=`177388` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_bridge_orchestrator.json` exists=`True` size=`1249` suffix=`.json` preview_chars=`1216`
- `output/ai_pipeline/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_decision_loop.json` exists=`True` size=`3042` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_full_access_md_telemetry_20260506-154554_agent_review_patch_plan.json` exists=`True` size=`232936` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/repository_change_proposals.json` exists=`True` size=`8723` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_full_access_md_telemetry_20260506-154554_workflow.json` exists=`True` size=`5621` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md`

- Role: `explicit_artifact`
- Exists: `False`
- Suffix: `.md`
- Size bytes: `None`
- SHA-256: `None`
- Content included: `False`
- Content truncated: `False`

### `docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `714`
- SHA-256: `bc278e114d5b0b6c51c2be9d8761627e4f91dad9eda5f614b67cbf1f9c481333`
- Content included: `True`
- Content truncated: `False`

```text
<!-- IA-CARMINE-MD-SPLIT: index -->
# gpu-npu-parallel-evidence-runbook

Questo documento Ã¨ stato diviso automaticamente per rispettare il budget di righe Markdown.

- File originale: `docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md`
- Limite massimo configurato: `400` righe
- Indice completo: `gpu-npu-parallel-evidence-runbook/README.md` (`gpu-npu-parallel-evidence-runbook/README.md`, generated evidence path not committed)

## Parti

- `gpu-npu-parallel-evidence-runbook/part-001.md` (`gpu-npu-parallel-evidence-runbook/part-001.md`, generated evidence path not committed)
- `gpu-npu-parallel-evidence-runbook/part-002.md` (`gpu-npu-parallel-evidence-runbook/part-002.md`, generated evidence path not committed)

## Nota operativa

Mantenere questo file come entrypoint stabile per non rompere i riferimenti esistenti.

```

### `Tools/ai/run_agent_review_decision_loop.py`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.py`
- Size bytes: `14608`
- SHA-256: `e996e04b636a7aea8076d9115c2ee12424bb8f5bbb2cb59bb0e67322b80e914c`
- Content included: `True`
- Content truncated: `False`

```text
#!/usr/bin/env python3
"""Run the report-only agent review decision loop.

This wrapper closes the local AI review loop without reimplementing either
decision layer:

1. build deterministic schema-valid recommendations from evidence/GPU/tool reports;
2. write a bridge orchestrator for the existing patch-plan builder;
3. build the existing manual-review patch plan.

It is report-only: no providers, no patch application, no SQLite writes, no
Blender runtime and no GitHub actions are executed.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.build_agent_review_patch_plan import build_patch_plan, render_markdown as render_patch_plan_markdown
    from Tools.ai.build_deterministic_recommendations import (
        build_patch_plan_bridge_orchestrator,
        build_recommendation_report,
        load_report_at,
        render_markdown as render_recommendations_markdown,
        resolve_path,
    )
    from Tools.validation.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.build_agent_review_patch_plan import build_patch_plan, render_markdown as render_patch_plan_markdown  # type: ignore
    from Tools.ai.build_deterministic_recommendations import (  # type: ignore
        build_patch_plan_bridge_orchestrator,
        build_recommendation_report,
        load_report_at,
        render_markdown as render_recommendations_markdown,
        resolve_path,
    )
    from Tools.validation.report_utils import write_json_report, write_text_report  # type: ignore

DEFAULT_EVIDENCE = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_ORCHESTRATOR = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json"
DEFAULT_RECOMMENDATIONS_OUTPUT = "output/ai_pipeline/agent_review_decision_loop_deterministic_recommendations.json"
DEFAULT_RECOMMENDATIONS_MARKDOWN = "output/ai_pipeline/agent_review_decision_loop_deterministic_recommendations.md"
DEFAULT_BRIDGE_ORCHESTRATOR = "output/ai_pipeline/agent_review_decision_loop_bridge_orchestrator.json"
DEFAULT_PATCH_PLAN_OUTPUT = "output/patch_specs/agent_review_patch_plan.json"
DEFAULT_PATCH_PLAN_MARKDOWN = "output/patch_specs/agent_review_patch_plan.md"
DEFAULT_OUTPUT = "output/ai_pipeline/agent_review_decision_loop.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_review_decision_loop.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def compact_output_result(path: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "path": repo_rel(path, repo_root),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
    }


def build_patch_plan_from_bridge_args(
    *,
    repo_root: Path,
    bridge_orchestrator: Path,
    evidence_path: Path,
    patch_plan_output: Path,
    patch_plan_markdown: Path,
    max_patch_plans: int = 0,
) -> dict[str, Any]:
    args = argparse.Namespace(
        repo_root=str(repo_root),
        orchestrator=str(bridge_orchestrator),
        evidence=str(evidence_path),
        output=str(patch_plan_output),
        markdown_output=str(patch_plan_markdown),
        max_patch_plans=max_patch_plans,
    )
    return build_patch_plan(args)


def build_decision_loop_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    evidence_path = resolve_path(repo_root, args.evidence)
    source_orchestrator_path = resolve_path(repo_root, args.orchestrator)
    recommendations_output = resolve_path(repo_root, args.recommendations_output)
    recommendations_markdown = resolve_path(repo_root, args.recommendations_markdown)
    bridge_orchestrator_output = resolve_path(repo_root, args.bridge_orchestrator_output)
    patch_plan_output = resolve_path(repo_root, args.patch_plan_output)
    patch_plan_markdown = resolve_path(repo_root, args.patch_plan_markdown)

    recommendation_args = argparse.Namespace(
        repo_root=str(repo_root),
        evidence=str(evidence_path),
        orchestrator=str(source_orchestrator_path),
        gpu_report=args.gpu_report,
        tool_report=list(args.tool_report or []),
        max_recommendations=args.max_recommendations,
    )
    recommendation_report = build_recommendation_report(recommendation_args)
    if recommendation_report.get("errors"):
        errors.extend(f"recommendations: {error}" for error in recommendation_report["errors"])
    warnings.extend(f"recommendations: {warning}" for warning in recommendation_report.get("warnings", []))

    write_json_report(recommendation_report, recommendations_output)
    write_text_report(render_recommendations_markdown(recommendation_report), recommendations_markdown)

    source_orchestrator, source_orchestrator_warnings = load_report_at(
        repo_root,
        source_orchestrator_path,
        missing_is_error=False,
    )
    warnings.extend(f"source_orchestrator: {warning}" for warning in source_orchestrator_warnings)

    bridge_report = build_patch_plan_bridge_orchestrator(
        repo_root=repo_root,
        recommendation_report=recommendation_report,
        recommendation_output=recommendations_output,
        source_orchestrator=source_orchestrator,
    )
    write_json_report(bridge_report, bridge_orchestrator_output)

    patch_plan_report: dict[str, Any] = {}
    if recommendation_report.get("passed") is True and recommendation_report.get("recommendation_count", 0) > 0:
        patch_plan_report = build_patch_plan_from_bridge_args(
            repo_root=repo_root,
            bridge_orchestrator=bridge_orchestrator_output,
            evidence_path=evidence_path,
            patch_plan_output=patch_plan_output,
            patch_plan_markdown=patch_plan_markdown,
            max_patch_plans=int(args.max_patch_plans),
        )
        if patch_plan_report.get("errors"):
            errors.extend(f"patch_plan: {error}" for error in patch_plan_report["errors"])
        warnings.extend(f"patch_plan: {warning}" for warning in patch_plan_report.get("warnings", []))
        write_json_report(patch_plan_report, patch_plan_output)
        write_text_report(render_patch_plan_markdown(patch_plan_report), patch_plan_markdown)
    else:
        errors.append("recommendation stage did not produce schema-valid recommendations for patch-plan build")

    recommendation_count = int(recommendation_report.get("recommendation_count") or 0)
    patch_plan_count = int(patch_plan_report.get("patch_plan_count") or 0) if patch_plan_report else 0
    if recommendation_count < int(args.min_recommendations):
        errors.append(
            f"recommendation_count below minimum: expected >= {args.min_recommendations}, got {recommendation_count}"
        )
    if patch_plan_count < int(args.min_patch_plans):
        errors.append(f"patch_plan_count below minimum: expected >= {args.min_patch_plans}, got {patch_plan_count}")

    if patch_plan_report and patch_plan_report.get("decision", {}).get("fallback_used") is True:
        warnings.append("patch_plan fallback_used=true; deterministic bridge was bypassed or produced no usable GPU recommendations")

    return {
        "schema_version": 1,
        "kind": "agent_review_decision_loop",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "recommendation_count": recommendation_count,
        "patch_plan_count": patch_plan_count,
        "deterministic_synthesizer_used": recommendation_report.get("decision", {}).get(
            "deterministic_synthesizer_used"
        ),
        "patch_plan_fallback_used": patch_plan_report.get("decision", {}).get("fallback_used") if patch_plan_report else None,
        "next_best_action": "manual_review_patch_plan" if patch_plan_count else "collect_more_evidence",
        "outputs": {
            "recommendations": compact_output_result(recommendations_output, repo_root),
            "recommendations_markdown": compact_output_result(recommendations_markdown, repo_root),
            "bridge_orchestrator": compact_output_result(bridge_orchestrator_output, repo_root),
            "patch_plan": compact_output_result(patch_plan_output, repo_root),
            "patch_plan_markdown": compact_output_result(patch_plan_markdown, repo_root),
        },
        "inputs": {
            "evidence": repo_rel(evidence_path, repo_root),
            "orchestrator": repo_rel(source_orchestrator_path, repo_root),
            "gpu_report": args.gpu_report,
            "tool_report_count": len(args.tool_report or []),
            "max_recommendations": args.max_recommendations,
            "max_patch_plans": args.max_patch_plans,
            "recommendation_kind": recommendation_report.get("kind"),
            "patch_plan_kind": patch_plan_report.get("kind") if patch_plan_report else None,
        },
        "decision": {
            "recommendations_ready": recommendation_count >= int(args.min_recommendations),
            "patch_plan_ready": patch_plan_count >= int(args.min_patch_plans),
            "manual_review_required": True,
            "recommended_next_layer": "manual_review_patch_plan" if patch_plan_count else "collect_more_evidence",
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "real_github_pr_created": False,
            "npu_primary_advisory": False,
            "openvino_gpu_primary_lane": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Decision Loop", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Recommendation count: `{report['recommendation_count']}`")
    lines.append(f"- Patch plan count: `{report['patch_plan_count']}`")
    lines.append(f"- Deterministic synthesizer used: `{report.get('deterministic_synthesizer_used')}`")
    lines.append(f"- Patch plan fallback used: `{report.get('patch_plan_fallback_used')}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    for key, value in report.get("outputs", {}).items():
        lines.append(
            f"- `{key}`: `{value.get('path')}` exists=`{value.get('exists')}` size=`{value.get('size_bytes')}`"
        )
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        for error in report["errors"]:
            lines.append(f"- {error}")
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.append("Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--orchestrator", default=DEFAULT_ORCHESTRATOR)
    parser.add_argument("--gpu-report", default="")
    parser.add_argument("--tool-report", action="append", default=[])
    parser.add_argument("--max-recommendations", type=int, default=20)
    parser.add_argument("--max-patch-plans", type=int, default=0, help="Maximum patch plans to keep; 0 means no additional cap.")
    parser.add_argument("--min-recommendations", type=int, default=1)
    parser.add_argument("--min-patch-plans", type=int, default=1)
    parser.add_argument("--recommendations-output", default=DEFAULT_RECOMMENDATIONS_OUTPUT)
    parser.add_argument("--recommendations-markdown", default=DEFAULT_RECOMMENDATIONS_MARKDOWN)
    parser.add_argument("--bridge-orchestrator-output", default=DEFAULT_BRIDGE_ORCHESTRATOR)
    parser.add_argument("--patch-plan-output", default=DEFAULT_PATCH_PLAN_OUTPUT)
    parser.add_argument("--patch-plan-markdown", default=DEFAULT_PATCH_PLAN_MARKDOWN)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_decision_loop_report(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "recommendation_count": report["recommendation_count"],
                "patch_plan_count": report["patch_plan_count"],
                "deterministic_synthesizer_used": report["deterministic_synthesizer_used"],
                "patch_plan_fallback_used": report["patch_plan_fallback_used"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

```

### `Tools/validation/run_agent_review_decision_loop_smoke.py`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.py`
- Size bytes: `11896`
- SHA-256: `91be3dd92478bee3cb4eb1b85d481c93502860677b12a0f34167cd519e13cdcc`
- Content included: `True`
- Content truncated: `False`

```text
#!/usr/bin/env python3
"""Smoke-test the agent review decision loop wrapper."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

DEFAULT_OUTPUT = "output/validation/agent_review_decision_loop_smoke.json"
DEFAULT_MARKDOWN = "output/validation/agent_review_decision_loop_smoke.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def write_fixture(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_command(command: list[str], repo_root: Path, timeout_seconds: int) -> tuple[int, str, str, str | None]:
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return completed.returncode, completed.stdout[-12000:], completed.stderr[-12000:], None
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "", f"TimeoutExpired: {timeout_seconds}s"
    except Exception as exc:  # noqa: BLE001 - smoke report should capture unexpected failures.
        return 1, "", "", f"{type(exc).__name__}: {exc}"


def load_json(path: Path) -> tuple[dict[str, Any], str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return {}, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return {}, "JSON root is not an object"
    return data, None


def build_fixtures(repo_root: Path, work_dir: Path) -> tuple[Path, Path, Path]:
    gpu_path = work_dir / "gpu.json"
    evidence_path = work_dir / "evidence.json"
    orchestrator_path = work_dir / "orchestrator.json"

    evidence = {
        "schema_version": 1,
        "kind": "agent_review_evidence_sufficiency",
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": [],
        "decision": {
            "ready_for_manual_patch_count": 1,
            "sufficient_for_real_pr": True,
        },
        "areas": {
            "doc_code": {
                "items": [
                    {
                        "doc": "AGENTS.md",
                        "reference": "Tools/ai/run_agent_review_decision_loop.py",
                        "existing_candidate": "Tools/ai/build_agent_review_patch_plan.py",
                        "candidate_references": [
                            "Tools/ai/build_deterministic_recommendations.py",
                            "Tools/ai/build_agent_review_patch_plan.py",
                        ],
                        "reason": "Decision loop should turn evidence-ready output into a manual review patch plan.",
                        "confidence": "high",
                        "evidence_sufficient": True,
                        "evidence_files": [
                            {
                                "path": "AGENTS.md",
                                "exists": True,
                                "kind": "markdown",
                                "matched_terms": ["manual review", "evidence"],
                            }
                        ],
                    }
                ]
            }
        },
    }
    gpu = {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_supervised",
        "repo_root": str(repo_root),
        "passed": False,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "recommendation_count": 0,
        "recommendations": [],
        "empty_recommendations_reason": "json_parse_failure",
        "evidence_ready_for_manual_patch_count": 1,
    }
    orchestrator = {
        "schema_version": 1,
        "kind": "agent_gpu_npu_parallel_orchestrator",
        "repo_root": str(repo_root),
        "passed": False,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "gpu_output": rel(gpu_path, repo_root),
        "gpu_empty_recommendations_reason": "json_parse_failure",
        "npu_audits": [
            {
                "round": 1,
                "status": "success",
                "classification": "usable_audit_text",
                "runtime_tool_context_seen": True,
                "npu_tool_request_count": 1,
                "npu_runtime_tool_execution_count": 1,
                "npu_runtime_tool_failed_count": 0,
                "npu_runtime_tool_blocked_count": 0,
            }
        ],
    }
    write_fixture(evidence_path, evidence)
    write_fixture(gpu_path, gpu)
    write_fixture(orchestrator_path, orchestrator)
    return evidence_path, orchestrator_path, gpu_path


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Decision Loop Smoke", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Return code: `{report['returncode']}`")
    lines.append(f"- Recommendation count: `{report.get('recommendation_count')}`")
    lines.append(f"- Patch plan count: `{report.get('patch_plan_count')}`")
    lines.append(f"- Deterministic synthesizer used: `{report.get('deterministic_synthesizer_used')}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        for error in report["errors"]:
            lines.append(f"- {error}")
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def run_smoke(repo_root: Path, timeout_seconds: int) -> dict[str, Any]:
    work_dir = repo_root / "output" / "validation" / "agent_review_decision_loop_smoke"
    evidence_path, orchestrator_path, gpu_path = build_fixtures(repo_root, work_dir)

    loop_output = work_dir / "decision_loop.json"
    loop_markdown = work_dir / "decision_loop.md"
    recommendation_output = work_dir / "deterministic_recommendations.json"
    recommendation_markdown = work_dir / "deterministic_recommendations.md"
    bridge_output = work_dir / "bridge_orchestrator.json"
    patch_plan_output = work_dir / "agent_review_patch_plan.json"
    patch_plan_markdown = work_dir / "agent_review_patch_plan.md"

    command = [
        sys.executable,
        "Tools/ai/run_agent_review_decision_loop.py",
        "--repo-root",
        ".",
        "--evidence",
        str(evidence_path),
        "--orchestrator",
        str(orchestrator_path),
        "--gpu-report",
        str(gpu_path),
        "--recommendations-output",
        str(recommendation_output),
        "--recommendations-markdown",
        str(recommendation_markdown),
        "--bridge-orchestrator-output",
        str(bridge_output),
        "--patch-plan-output",
        str(patch_plan_output),
        "--patch-plan-markdown",
        str(patch_plan_markdown),
        "--output",
        str(loop_output),
        "--markdown-output",
        str(loop_markdown),
        "--min-recommendations",
        "1",
        "--min-patch-plans",
        "1",
    ]
    returncode, stdout, stderr, runner_error = run_command(command, repo_root, timeout_seconds)
    errors: list[str] = []
    warnings: list[str] = []
    if runner_error:
        errors.append(runner_error)
    if returncode != 0:
        errors.append(f"decision loop returned {returncode}")

    decision_loop_report, read_error = load_json(loop_output)
    if read_error:
        errors.append(f"unable to read decision loop output: {read_error}")

    recommendation_count = decision_loop_report.get("recommendation_count")
    patch_plan_count = decision_loop_report.get("patch_plan_count")
    deterministic_used = decision_loop_report.get("deterministic_synthesizer_used")
    fallback_used = decision_loop_report.get("patch_plan_fallback_used")

    if decision_loop_report:
        if decision_loop_report.get("passed") is not True:
            errors.append("decision loop report did not pass")
        if recommendation_count != 1:
            errors.append(f"expected recommendation_count=1, got {recommendation_count!r}")
        if patch_plan_count != 1:
            errors.append(f"expected patch_plan_count=1, got {patch_plan_count!r}")
        if deterministic_used is not True:
            errors.append(f"expected deterministic_synthesizer_used=true, got {deterministic_used!r}")
        if fallback_used is not False:
            errors.append(f"expected patch_plan_fallback_used=false, got {fallback_used!r}")
        if decision_loop_report.get("provider_execution_performed") is not False:
            errors.append("decision loop must not perform provider execution")
        if decision_loop_report.get("patch_application_performed") is not False:
            errors.append("decision loop must not perform patch application")
        warnings.extend(decision_loop_report.get("warnings", []))

    return {
        "schema_version": 1,
        "kind": "agent_review_decision_loop_smoke",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "returncode": returncode,
        "stdout_tail": stdout,
        "stderr_tail": stderr,
        "decision_loop_output": rel(loop_output, repo_root),
        "recommendation_count": recommendation_count,
        "patch_plan_count": patch_plan_count,
        "deterministic_synthesizer_used": deterministic_used,
        "patch_plan_fallback_used": fallback_used,
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "manual_review_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root, args.timeout_seconds)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown_output)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

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
python ./output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` | Correct 
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
| 130 | `Tools/ai/model_json.py` |
| 128 | `Tools/ai/build_agent_state_packet.py` |
| 127 | `Tools/npu/run_npu_artifact_reviewer.py` |
| 127 | `Tools/npu/pipeline/artifact_paths.py` |
| 125 | `Tools/validation/check_agent_memory_policy.py` |
| 125 | `Tools/validation/check_generated_python_policy.py` |
| 125 | `Scripting/v61b_backgood/hotpatch/accent_patch.py` |
| 125 | `Tools/npu/pipeline/reports.py` |
| 124 | `Scripting/v61b_backgood/hotpatch/fog_patch.py` |
| 123 | `Tools/validation/check_execution_plan_status.py` |
| 123 | `Tools/ai/full0to10_effective_use/memory_product.py` |
| 119 | `Tools/validation/check_package_structure.py` |
| 119 | `Tools/validation/check_ai_model_json.py` |
| 118 | `Tools/ai/pipeline/schema_report.py` |
| 117 | `Tools/workflow/workflow_shell_with_push.py` |
| 116 | `Tools/validation/run_runtime_sqlite_persistent_write_smoke.py` |
| 113 | `build_track_summary.py` |
| 111 | `Tools/npu/ai_memory_context.py` |
| 110 | `Tools/workflow/asset_inventory.py` |
| 108 | `Tools/ai/full0to10_final_product_quality/builder.py` |
| 107 | `Tools/npu/pipeline/config.py` |
| 107 | `Tools/ai/pipeline/markdown_report.py` |
| 106 | `Tools/ai/full0to10_provider_feedback_loop/builder.py` |
| 105 | `Tools/validation/check_python_syntax.py` |
| 105 | `Tools/ai/full0to10_final_product/builder.py` |
| 104 | `Tools/validation/run_full0to10_bundle_contracts_smoke.py` |
| 104 | `Tools/validation/run_unified_full0to10_supervisor_gate_smoke.py` |
| 104 | `Tools/ai/summarize_full0to10_light_evidence.py` |
| 104 | `Tools/ai/full0to10_sqlite_memory/search.py` |
| 104 | `Tools/ai/pipeline/preflight.py` |
| 103 | `Tools/validation/run_full_toolbox_deterministic_chunks_telemetry_smoke.py` |
| 103 | `Scripting/v61b/hotpatch/runner.py` |
| 102 | `Tools/ai/pipeline/runner.py` |
| 102 | `Scripting/shared/path_utils.py` |
| 101 | `Tools/ai/full0to10_memory_tool.py` |
| 99 | `Tools/validation/run_full0to10_manifest_gate_smoke.py` |
| 99 | `Tools/npu/pipeline/prompts.py` |
| 97 | `
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
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Tools/ai/full0to10_markdown_split/applier.py,90
Tools/validation/run_npu_tool_request_contract_smoke.py,90
Scripting/shared/json_io.py,88
Tools/ai/full0to10_provider_governor/builder.py,88
Tools/ai/full0to10_repo_quality/builder.py,88
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py,88
Tools/validation/ai_workload_quality/reporter.py,87
Tools/ai/full0to10_accelerator_control/device_visibility.py,86
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/ai/full0to10_runtime_tools/memory_adapter.py,83
Tools/validation/check_provider_result_parsing.py,83
Tools/validation/check_full0to10_generated_artifact_quarantine.py,82
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Tools/validation/check_md_code_coherence.py,77
Tools/ai/full0to10_accelerator_control/builder.py,76
Tools/ai/full0to10_repo_quality/inventory.py,76
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/full0to10_final_product/readiness.py,74
Tools/ai/pipeline/reports.py,74
Tools/validation/run_full0to10_quality_supervisor_safety_smoke.py,74
Tools/ai/full0to10_final_product_quality/constants.py,73
Tools/ai/full0to10_sqlite_memory/ingest.py,73
Tools/ai/pipeline/compat.py,73
Tools/ai/full0to10_markdown_split/shadow.py,72
Tools/validation/build_full_python_line_count_markdown.py,71
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/validation/run_full0to10_provider_governor_smoke.py,70
Tools/ai/review_agent_memory.py,69
Tools/validation/run_full0to10_openvino_device_visibility_smoke.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/validation/full0to10_contracts/memory_contract.py,68
Tools/validation/run_full0to10_controlled_refactor_applier_sm
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

### consistency_001 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_003 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_005 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141` targeting `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14` targeting `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md` and resolve `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_013 â€” md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_042 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_043 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_044 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_045 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_046 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_047 â€” md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:184` targeti
```

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1364`
- SHA-256: `ca70b760f7c4599e1e62f49aee22962b1f922b56e6b5e4ac3eef33507bc8e1fc`
- Content included: `True`
- Content truncated: `False`

```text
{
    "schema_version":  1,
    "kind":  "agent_review_evidence_sufficiency",
    "generated_at":  "2026-05-06T15:47:22.5570133+02:00",
    "stamp":  "full_access_md_telemetry_20260506-154554",
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

### consistency_001 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:327`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_003 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:333`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338` targeting `Tools/ai/agent_memory_tools.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:338`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_005 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141` targeting `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md:141`. Target `CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md` and resolve `output/validation/patch_bundles/ia_carmine_real_run_strict_tool_activation_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_006 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14` targeting `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md:14`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md` and resolve `output/validation/patch_bundles/full0to10_chained_md_budget_repo_quality_patch_bundle/run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_007 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md:173`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_008 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:25`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_009 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md:101`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_010 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_011 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311` targeting `Tools/validation/check_example_contract.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md:311`. Target `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` and resolve `Tools/validation/check_example_contract.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_013 â€” md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_042 â€” md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_043 â€” md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_044 â€” md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_045 â€” md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_046 â€” md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183` targeting `Tools/workflow/example_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md:183`. Target `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` and resolve `Tools/workflow/example_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_047 â€” md_powershell
- Source: `repository_consistency_ma
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

### `output/ai_pipeline/repository_change_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2344`
- SHA-256: `5df7140635e353c08534efdcd123ce572530948b8e345c71237e7bf6e8238138`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-06T15:47:23`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-NEXT-NPU-OBSERVABILITY â€” Add additive NPU observability before provider execution changes

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

- `Tools/npu/run_dual_ai_pipeline.py` â€” `1774` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` â€” `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` â€” `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` â€” `1179` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` â€” `1129` lines, risk `high`
- `Scripting/v61b/animation.py` â€” `1079` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` â€” `909` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` â€” `902` lines, risk `high`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` â€” `850` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` â€” `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` â€” `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` â€” `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` â€” `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` â€” `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` â€” `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` â€” `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` â€” `687` lines, risk `medium`
- `Tools/ai/build_runtime_tool_usage_telemetry.py` â€” `675` lines, risk `medium`
- `Scripting/v61b/materials.py` â€” `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` â€” `631` lines, risk `medium`

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

### det_doc_code_001 â€” doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['AGENTS.md']`
- Rationale: The documentation points at a recommendation lane that must be normalized before patch-plan construction.
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Tools/ai/build_deterministic_recommendations.py` and update `AGENTS.md` only if the reference is stale or should point at an existing artifact. Prefer existing candidate `Tools/ai/build_agent_review_patch_plan.py` over inventing a new runtime artifact. Candidate references observed: `Tools/ai/build_agent_review_patch_plan.py`, `Tools/ai/gpu_planner_json_contract.py`.

## Guardrails

This report is deterministic and report-only. It is not a patch queue.

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

