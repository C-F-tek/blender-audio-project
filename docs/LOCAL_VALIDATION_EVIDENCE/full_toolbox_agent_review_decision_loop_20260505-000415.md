# Local Validation Evidence Bundle

- Generated at: `2026-05-05T00:05:21`
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

### `output/ai_pipeline/full_toolbox_20260505-000415_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `False`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Errors: `['GPU output missing: output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.json']`

### `output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_parallel_report`
- Passed: `False`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Errors: `['required GPU provider artifact missing before fallback generation']`

### `output/analysis/repository_consistency_map_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `159`

### `output/validation/python_line_count_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-000415.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `20`

### `output/ai_pipeline/full_toolbox_20260505-000415_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_20260505-000415_agent_review_decision_loop.json`

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

### `output/patch_specs/full_toolbox_20260505-000415_agent_review_patch_plan.json`

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

### `output/validation/full_memory_tool_regeneration_20260505-000415_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Patch plan summary

### `output/patch_specs/full_toolbox_20260505-000415_agent_review_patch_plan.json`

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

- `output/ai_pipeline/full_toolbox_20260505-000415_orchestrator.json` exists=`True` size=`9996` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.json` exists=`True` size=`1255` suffix=`.json` preview_chars=`1220`
- `output/analysis/repository_consistency_map_full_toolbox_20260505-000415.json` exists=`True` size=`6267594` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_20260505-000415.json` exists=`True` size=`1198` suffix=`.json` preview_chars=`1159`
- `output/analysis/code_interpreter_full_toolbox_20260505-000415.json` exists=`True` size=`1462969` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_20260505-000415.json` exists=`True` size=`3151` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_20260505-000415.json` exists=`True` size=`38308` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-000415.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-000415.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-000415.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_20260505-000415.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-000415.json` exists=`True` size=`1685` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-000415.json` exists=`True` size=`4756` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.json` exists=`True` size=`166369` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260505-000415_bridge_orchestrator.json` exists=`True` size=`1224` suffix=`.json` preview_chars=`1191`
- `output/ai_pipeline/full_toolbox_20260505-000415_agent_review_decision_loop.json` exists=`True` size=`2867` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_20260505-000415_agent_review_patch_plan.json` exists=`True` size=`233904` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/repository_change_proposals.json` exists=`True` size=`8384` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260505-000415_workflow.json` exists=`True` size=`4921` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `31392`
- SHA-256: `fe97cacf12f489cb2f1f65d981246dccdb35203423771c0b7c54f8ecd424b2df`
- Content included: `True`
- Content truncated: `True`

```text
# Code Refactor 0 -> 10 Procedure — IA-Carmine

## Purpose

Use this guide when the user asks to start a code refactor cycle.

This is the canonical 0 -> 10 operating procedure for report-only code refactoring in `C-F-tek/blender-audio-project` after PR #116.

It combines:

```text
- current post-PR116 repository state
- full Python line-count inventory
- repository/tool discovery before planning
- helper/function reuse and promotion review
- balanced GPU/NPU AI-to-AI run
- manual-review code patch-plan lane
- compact evidence bundle policy
```

Default mode:

```text
report-only
manual-review-only
no automatic patch application
no Blender runtime
no raw output/** commit
```

## Current context baseline

Repository:

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
project: IA-Carmine
workflow: local validation + GitHub/API PRs
```

Merged baseline at the time this guide was written:

```text
PR #109: docs(ai): design manual-review code patch plan lane
PR #111: feat(ai): surface GPU repair-failure recommendations
PR #112: feat(ai): harden GPU planner JSON contract
PR #113: feat(ai): analyze GPU/NPU run sync and balanced profile
PR #114: feat(ai): replay GPU planner JSON contract on real outputs
PR #115: feat(ai): wire GPU planner JSON contract into runner diagnostics
PR #116: docs(ai): add post-PR115 full Python refactor handoff
```

Relevant current master commits:

```text
56bb6b0 feat(ai): wire GPU planner JSON contract into runner diagnostics
5dfd127 docs(ai): add post-PR115 full Python refactor handoff
```

Primary post-PR116 entry handoff:

```text
docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md
```

## Core rule

A code refactor cycle must not start from intuition only.

It must start from:

```text
1. current repo state
2. current docs/runbooks
3. full Python line-count CSV
4. complete Python inventory Markdown, not top-N only
5. existing reusable tools/helpers
6. report-only validation evidence
```

Line count is a signal, not a filter. The planner must see all counted Python files and decide candidates.

## Refactor-specific guardrails

Never do these without explicit command:

```text
delete
force-push
rewrite history
merge to master/protected branch
change secrets/permissions/billing/visibility
deploy production
```

Project guardrails:

```text
no automatic patch application
no Blender runtime execution
no SQLite/database commit
no raw output/** commit
no full analysis JSON commit outside compact evidence bundle
no NPU advisory promotion
no OpenVINO GPU primary lane
manual review required for patch plans
```

Code refactor guardrails:

```text
no broad rewrite of large files in one PR
no provider/model setting changes unless explicitly requested
no prompt rewriting unless explicitly requested
preserve CLI arguments and report schemas unless a migration plan is explicit
prefer reuse/promotion of existing helpers over new duplication
always include validation commands and stop conditions
```

Legacy/refactor exclusion:

```text
Do not create ready-for-patch refactor plans for paths containing:
legacy
archive
old
backup
bak
```

Exception:

```text
Scripting/v61b/** is the current template lane and may be reviewed/refactored only when the path is not a backup path.
```

Allowed examples:

```text
Scripting/v61b/*.py
Scripting/v61b/**/*.py
```

Disallowed examples:

```text
Scripting/v61b/**/backup*/**
Scripting/v61b/**/*backup*.py
Scripting/v61b/**/*bak*.py
any path outside Scripting/v61b containing legacy/archive/old/backup/bak
```

If a legacy/archive/backup issue is valuable but outside scope, classify it as:

```text
advisory_only
needs_more_context
```

not:

```text
ready_for_patch_plan
```

---

# 0 -> 10 Procedure

## 0. Sync repository and shell setup

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short
git log --oneline -10

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

Expected:

```text
git status --short is empty
HEAD is master/origin/master
```

Do not continue if local source files are dirty unless the user explicitly says those changes are intentional input.

## 1. Read repository instructions and reference docs

Read these before planning or running a refactor cycle:

```powershell
Get-Content .\AGENTS.md -TotalCount 260
Get-Content .\docs\LOCAL_AI_RUN_BOOTSTRAP.md -TotalCount 260
Get-Content .\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md -TotalCount 420
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md -TotalCount 300
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md -TotalCount 420
Get-Content .\docs\LOCAL_AI_TASKS\gpu-npu-balanced-run-profile.md -TotalCount 280
Get-Content .\docs\LOCAL_AI_TASKS\post-pr114-next-task-handoff.md -TotalCount 340
Get-Content .\docs\LOCAL_AI_TASKS\next-chat-handoff-after-balanced-full-run-2026-05-02.md -TotalCount 380
Get-Content .\docs\LOCAL_AI_TASKS\next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md -TotalCount 520
Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\README.md -TotalCount 240
```

Purpose:

```text
avoid reinventing architecture
reuse existing project rules
respect evidence/bundle policy
stay aligned with current post-PR115 diagnostics
```

## 2. Discover existing tools/helpers before proposing refactor

Inspect existing reusable primitives before inventing new modules:

```powershell
Get-Content .\Tools\ai\code_patch_plan_common.py -TotalCount 360
Get-Content .\Tools\ai\code_edit_proposal_helpers.py -TotalCount 420
Get-Content .\Tools\ai\build_agent_review_code_patch_plan.py -TotalCount 420
Get-Content .\Tools\ai\build_code_edit_proposal_from_plan.py -TotalCount 420
Get-Content .\Tools\ai\build_code_interpreter_report.py -TotalCount 360
Get-Content .\Tools\ai\build_github_evidence_bundle.py -TotalCount 420
Get-Content .\Tools\validation\build_python_line_count_csv.py -TotalCount 320
Get-Content .\Tools\validation\run_agent_review_code_patch_plan_smoke.py -TotalCount 360
Get-Content .\Tools\validation\check_python_syntax.py -TotalCount 260
Get-Content .\Tools\validation\check_validation_report_contract.py -TotalCount 300
```

Search for already-factored utilities:

```powershell
Get-ChildItem .\Tools -Recurse -File -Filter *.py |
  Select-String -Pattern "def repo_rel|def resolve_path|def write_json|def render_markdown|report_only_guardrails|write_json_and_markdown|normalize_repo_path|load_line_counts" |
  Select-Object Path, LineNumber, Line |
  Format-Table -AutoSize
```

Helper decision taxonomy for every proposed refactor:

```text
reuse_existing_helper
promote_existing_function
extract_new_shared_helper
keep_local_by_design
```

Promotion candidates:

```text
path normalization
JSON read/write
Markdown report rendering
guardrail blocks
compact value/list helpers
validation command generation
line-count loading/parsing
report-only schema fields
forbidden target checks
```

Preferred promotion targets:

```text
Tools/ai/code_patch_plan_common.py
Tools/validation/report_utils.py
existing local helper modules in Tools/ai or Tools/validation
```

Do not create a new shared helper module if an existing one is a better fit.

## 2.1 Optional memory/tool reload after code or knowledge changes

Use this optional step only when the repository knowledge surface changed materially before a 0 -> 10 run.

Typical triggers:

```text
- new or modified AI tooling under Tools/ai, Tools/validation, Tools/workflow or Tools/npu
- new or modified docs/runbooks under docs/LOCAL_AI_TASKS or docs/LOCAL_VALIDATION_EVIDENCE
- merged PRs that change runtime toolbox, broker, orchestrator, memory routing or provider diagnostics
- stale evidence bundle after code/doc changes
- ChatGPT/local IA handoff says the memory/tool context may be outdated
```

Default behavior:

```text
optional
report-only
no provider execution
no patch application
no Blender runtime
no persistent memory write
no raw output/** commit
```

Recommended safe reload command:

```powershell
$MemoryReloadStamp = Get-Date -Format "yyyyMMdd-HHmmss"

.\Tools\workflow\run_full_memory_tool_regeneration.ps1 `
  -RepoRoot . `
  -Stamp $MemoryReloadStamp `
  -Profile full_refactor `
  -Objective "Reload IA-Carmine memory/tool context after code or knowledge changes before a 0 -> 10 run." `
  -WriteCompactBundle
```

Inspect the workflow report:

```powershell
Get-Content ".\output\validation\full_memory_tool_regeneration_${MemoryReloadStamp}_workflow.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, profile, provider_execution_performed, patch_application_performed, sqlite_write_performed, persistent_memory_write_performed, report_count, artifact_count, errors, bundle_json, bundle_markdown
```

Required guardrail result:

```text
passed=True
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
```

Evidence policy:

```text
Commit compact evidence only if it is needed for the review:
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_<STAMP>.csv
```

Never commit:

```text
output/**
*.db
*.sqlite
renders/**
```

If this optional reload is run, add the generated compact bundle as a `--report-file` or committed evidence reference in the later GPU/NPU/refactor run so the local IA sees the refreshed state.

## 3. Build full Python line-count evidence

Run the deterministic line-count tool:

```powershell
python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --markdown-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.md"
```

Inspect report summary:

```powershell
$LineCountReport = Get-Content ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" -Raw | ConvertFrom-Json
$LineCountCsv = $LineCountReport.csv_written

$LineCountReport |
  Select-Object passed, file_count, total_lines, csv_written, errors, warnings

"LINE_COUNT_CSV=$LineCountCsv"
```

Create a full untruncated Markdown inventory from the CSV:

```powershell
$LineCountAllMd = ".\output\validation\python_line_count_all_python_files_$Stamp.md"
$Rows = Import-Csv $LineCountCsv | Sort-Object {[int]$_.Lines} -Descending
$TotalLines = ($Rows | Measure-Object -Property Lines -Sum).Sum
$FileCount = ($Rows | Measure-Object).Count

$Lines = @()
$Lines += "# Full Python Line Count Inventory"
$Lines += ""
$Lines += "- Stamp: `$Stamp`"
$Lines += "- CSV: `$LineCountCsv`"
$Lines += "- File count: `$FileCount`"
$Lines += "- Total Python lines: `$TotalLines`"
$Lines += "- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20."
$Lines += ""
$Lines += "| Lines | File |"
$Lines += "|---:|---|"
foreach ($Row in $Rows) {
  $Lines += "| $($Row.Lines) | `$($Row.File)` |"
}
$Lines | Set-Content -Path $LineCountAllMd -Encoding UTF8

Get-Content $LineCountAllMd -Raw
```

Rule:

```text
The complete inventory is the input. Do not reduce the planner view to only top 10/top 20 files.
```

## 4. Static validation and code interpreter report

Run baseline syntax validation:

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_code_refactor_$Stamp.json"
```

Run static/code interpreter style report with current tool roots and template roots:

```powershell
python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/npu `
  --input Tools/workflow `
  --input Scripting/v61b `
  --input Scripting/shared `
  --output ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" `
  --markdown-output ".\output\analysis\code_interpreter_code_refactor_$Stamp.md"
```

Inspect summary:

```powershell
Get-Content ".\output\validation\python_syntax_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, checked_count, failed_count, errors, warnings

Get-Content ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, errors, warnings
```

Stop if syntax validation fails unexpectedly.

## 5. Contract/tool smoke before provider run

Post-PR115 diagnostics depend on the GPU JSON contract helpers. Validate them before a long run:

```powershell
python -m py_compile `
  .\Tools\ai\gpu_planner_json_contract.py `
  .\Tools\ai\replay_gpu_planner_json_contract.py `
  .\Tools\ai\analyze_gpu_npu_run_sync.py `
  .\Tools\ai\build_gpu_repair_failure_recommendation.py `
  .\Tools\ai\run_agent_gpu_deep_planning_review.py `
  .\Tools\ai\run_agent_gpu_deep_planning_supervised.py `
  .\Tools\validation\run_gpu_planner_json_contract_smoke.py

python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, case_count, failed_case_count, patch_application_performed, source_writes_performed
```

## 6. NPU/provider preflight

Run NPU provider environment check:

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, patch_application_performed, errors, warnings
```

## 7. Run balanced GPU/NPU complete review

Use the balanced profile. Do not increase token budget before evaluating post-PR115 diagnostics.

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 30 `
  --max-rounds 20 `
  --files-per-round 8 `
  --max-context-files 220 `
  --max-chars-per-file 6000 `
  --max-new-tokens 3600 `
  --keep-alive 35m `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --report-file ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" `
  --report-file ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --context-root Tools\npu `
  --context-root Scripting\v61b `
  --context-root Scripting\shared `
  --context-root $LineCountAllMd `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 3 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 420 `
  --npu-max-context-chars 8000 `
  --npu-max-prompt-chars 1200 `
  --npu-max-new-tokens 384 `
  --npu-final-wait-seconds 180 `
  --checkpoint-dir ".\output\ai_pipeline\cod
```

### `docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15694`
- SHA-256: `084bfbae973243cd05aca6a0e5497d8ddf29e469d6156335f2ffbaca54ae8053`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Parallel Evidence Runbook

This task/runbook explains how a local AI agent should run the full GPU/NPU parallel diagnostic workflow, collect compact Git-trackable evidence, and interpret the initial `gpu_recommendation_count == 0` problem.

It is intended for non-interactive local AI runs and master-AI handoff review.

## Required reading order

A local AI agent must read these files first, before running commands or proposing edits:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md
```

If any instruction in this runbook conflicts with `AGENTS.md`, preserve `AGENTS.md` and stop with a conflict report.

## Purpose

Use the local machine as a controlled multi-lane AI system:

```text
CPU orchestration
GPU/Ollama planner
NPU/OpenVINO checkpoint auditor
Git-trackable evidence bundle
master-AI review before any patch
```

The current diagnostic focus is:

```text
GPU/Ollama can complete many planning rounds but produce zero recommendations.
NPU/OpenVINO audits selected checkpoints successfully.
The fallback patch-plan layer can still produce manual-review patch candidates from evidence sufficiency.
```

## Guardrails

```text
Do not apply patches automatically.
Do not commit output/**.
Do not commit SQLite databases.
Do not run Blender.
Do not promote NPU output to primary advisory.
Do not make OpenVINO GPU a primary advisory lane.
Do not change provider/model settings unless explicitly requested.
Do not create or merge a real PR unless explicitly requested by the human/master AI.
```

Provider execution must be explicit. Report-only tools should keep:

```text
patch_application_performed: false
source_writes_performed: false
manual_review_required: true
```

## Required input artifacts

Before running the full GPU/NPU parallel workflow, these local reports should exist:

```text
output/ai_pipeline/agent_review_evidence_sufficiency.json
output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json
output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json
output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json
output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json
output/ai_packets/gpu_planner_nonempty_recommendations_advisory_manifest.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json
```

The first two are the core planning inputs:

```text
agent_review_evidence_sufficiency.json
  tells whether there is enough evidence for manual-review patch candidates.

local_ai_core_tool_activation_megalithic_refined_review_v3.json
  contains refined doc/code/doc-doc/code-code findings after noise reduction.
```

The `report-file` inputs enrich the planner context with memory/tool/transient/advisory state.

## Optional NPU provider preflight

Before a live NPU run, check the dedicated NPU Python environment:

```powershell
$NpuPy = "$HOME\blender\venvs\blender-npu-ai\Scripts\python.exe"

& $NpuPy -c "import sys; print(sys.executable); import openvino; print('openvino OK'); import openvino_genai; print('openvino_genai OK')"
& $NpuPy -c "import openvino as ov; print(ov.Core().available_devices)"
```

Expected output pattern:

```text
openvino OK
openvino_genai OK
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

Naming rule:

```text
Python import module: openvino_genai
PyPI package name: openvino-genai
```

The project-owned preflight is preferred when available:

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output .\output\validation\npu_provider_environment.json `
  --markdown-output .\output\validation\npu_provider_environment.md
```

Expected report fields:

```text
passed: true
checks.openvino_import: true
checks.openvino_genai_import: true
checks.npu_available: true
decision.npu_ready_for_auditor: true
provider_execution_performed: false
patch_application_performed: false
```

## Full GPU/NPU parallel run

Use this command for the diagnostic run used by the current evidence bundle:

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 30 `
  --max-rounds 24 `
  --files-per-round 10 `
  --max-context-files 240 `
  --max-chars-per-file 8000 `
  --max-new-tokens 4800 `
  --keep-alive 35m `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 4 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 600 `
  --npu-max-context-chars 12000 `
  --npu-max-prompt-chars 1500 `
  --npu-max-new-tokens 512 `
  --npu-final-wait-seconds 120 `
  --checkpoint-dir .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_checkpoints `
  --gpu-output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.json `
  --gpu-markdown-output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.md `
  --output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --markdown-output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.md
```

### Expected behavior

The orchestrator should behave as follows:

```text
GPU/Ollama process runs continuously and writes round checkpoints.
NPU/OpenVINO audits selected checkpoints in parallel.
GPU review must not be blocked by NPU audit latency.
CPU joins the final report.
```

Healthy output should include:

```text
passed: true
gpu_returncode: 0
gpu_round_count > 0
npu_audit_count >= 1
npu_audit_success_count >= 1
gpu_review_blocked_by_npu: false
patch_application_performed: false
```

For this specific diagnostic family, it is acceptable and expected that the GPU report may still show:

```text
gpu_recommendation_count: 0
```

That is the problem under investigation, not proof that the full run failed.

## Inspect the full run output

After the run, inspect the orchestrator report:

```powershell
$orch = Get-Content .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json -Raw | ConvertFrom-Json

$orch |
  Select-Object kind, passed, provider_execution_performed, patch_application_performed, elapsed_seconds, gpu_returncode, npu_audit_count, npu_audit_success_count

$orch.gpu_summary
$orch.decision

$orch.npu_audits |
  Select-Object round, status, classification, provider_execution_requested, provider_load_attempted, provider_execution_succeeded, provider_execution_performed, dependency_missing, gpu_review_blocked, warnings |
  Format-List
```

Inspect the GPU report selected by the orchestrator:

```powershell
$GpuReport = $orch.gpu_output
$gpu = Get-Content $GpuReport -Raw | ConvertFrom-Json

$gpu |
  Select-Object kind, passed, round_count, recommendation_count

$gpu.decision
$gpu.rounds |
  Select-Object round, status, json_ok, recommendation_count, parse_error, empty_recommendations_reason |
  Format-Table -AutoSize
```

## Post-validation AI packet

Use the project-owned post-validation AI packet, not a manual ZIP, to produce advisory/proposal files from selected context and report files.

First resolve the GPU report path:

```powershell
$par = Get-Content .\output\ai_pipeline\agent_gpu_npu_parallel_orchestrator_live.json -Raw | ConvertFrom-Json
$GpuReport = $par.gpu_output
$GpuReport
```

If using the diagnostic orchestrator output from this runbook, use:

```powershell
$par = Get-Content .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json -Raw | ConvertFrom-Json
$GpuReport = $par.gpu_output
$GpuReport
```

Then pass arrays, not repeated PowerShell parameters:

```powershell
$ContextFiles = @(
  ".\docs\LOCAL_AI_TASKS\improve-gpu-planner-nonempty-recommendations.md",
  ".\Tools\ai\run_agent_gpu_deep_planning_review.py",
  ".\Tools\ai\run_agent_gpu_deep_planning_supervised.py",
  ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
  ".\Tools\ai\build_agent_review_patch_plan.py"
)

$ReportFiles = @(
  ".\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json",
  $GpuReport
)

$params = @{
  Profile     = "core"
  ContextFile = $ContextFiles
  ReportFile  = $ReportFiles
}

& .\Tools\workflow\run_post_validation_ai_packet.ps1 @params
```

Expected output files include:

```text
output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json
output/ai_packets/gpu_planner_nonempty_recommendations_advisory.md
output/ai_packets/gpu_planner_nonempty_recommendations_advisory_manifest.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.md
output/ai_pipeline/repository_change_proposals.json
output/ai_pipeline/repository_change_proposals.md
```

## Patch-plan fallback layer

When the GPU planner returns zero recommendations but evidence sufficiency says candidates are ready, use the patch-plan builder as the deterministic/manual-review fallback layer.

Typical command:

```powershell
python .\Tools\ai\build_agent_review_patch_plan.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output .\output\patch_specs\agent_review_patch_plan.json `
  --markdown-output .\output\patch_specs\agent_review_patch_plan.md
```

Expected behavior:

```text
manual_review_only
patch_application_performed: false
fallback_used: true when GPU recommendations are empty and evidence candidates exist
```

Validate it:

```powershell
python .\Tools\validation\run_agent_review_patch_plan_smoke.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output .\output\validation\agent_review_patch_plan_smoke.json `
  --markdown-output .\output\validation\agent_review_patch_plan_smoke.md
```

## Git-trackable evidence bundle procedure

Do not upload or commit raw `output/**` reports directly.

The project-owned evidence flow is:

```text
build_github_evidence_bundle.py
→ docs/LOCAL_VALIDATION_EVIDENCE/*.json/*.md
→ check_github_evidence_bundle.py
→ git add only compact evidence docs
→ commit/push
```

Build the compact evidence bundle:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename gpu_planner_nonempty_recommendations_evidence `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json `
  --report .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --report .\output\patch_specs\agent_review_patch_plan.json `
  --report .\output\validation\agent_review_patch_plan_full_validation.json `
  --report .\output\validation\agent_review_patch_plan_smoke.json `
  --report .\output\validation\validation_report_contract.json `
  --report .\output\ai_pipeline\repository_change_proposals.json `
  --report .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --report .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.json
```

Expected Git-trackable outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Validate the evidence bundle:

```powershell
python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  --output .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json
```

Inspect validation:

```powershell
Get-Content .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

## Final validation before push

Run standard validation:

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
git status --short
```

Only Git-trackable compact evidence should be staged for an evidence-only update:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Commit and push:

```powershell
git add `
  .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.md

git commit -m "test(ai): add gpu planner nonempty recommendations evidence bundle"

git push -u origin codex/improve-gpu-planner-nonempty-recommendations
```

## Review of the initial problem

The initial problem is not that the GPU/NPU full run fails. The full run can be healthy while still exposing a planning-quality issue.

Observed state:

```text
orchestrator passed
GPU/Ollama completed many rounds
NPU/OpenVINO audits were usable and non-blocking
patch_application_performed was false
GPU recommendation_count was 0
agent_review_evidence_sufficiency had ready manual-review candidates
patch-plan fallback generated candidates
```

Interpretation:

```text
The infrastructure works.
The GPU planner needs better diagnostics and/or stricter output contract enforcement.
The fallback patch-plan layer is currently required to convert evidence sufficiency into actionable manual-review plans.
```

Recommended fix direction:

```text
1. Add explicit diagnostics to GPU planner round reports:
   - json_ok
   - parse_error
   - repair_attempt_count
   - raw_recommendation_candidate_count
   - filtered_recommendation_count
   - recommendation_count
   - empty_recommendations_reason
   - evidence_ready_for_manual_patch_count

2. If evidence_sufficiency.ready_for_manual_patch_count > 0 and GPU recommendations remain empty, report:
   - empty_recommendations_reason: evidence_ready_but_no_gpu_plan
   - recommended_next_layer: build_agent_review_patch_plan.py

3. Keep fallback patch-plan generation deterministic and manual-review-only.

4. Do not force the GPU planner to invent recommendations. Prefer explicit empty-state diagnostics over hallucinated patch plans.
```

Acceptable end state:

```text
GPU recommendations may still be 0.
But the report must explain why and point to the fallback/manual-review patch-plan layer.
```

## What to send to a master AI after push

After pushing the evidence bundle, send either the branch/PR or these two files:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Do not send raw `output/**` unless explicitly requested for local-only debugging.

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

### `output/analysis/repository_consistency_map_full_toolbox_20260505-000415.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `53763`
- SHA-256: `1d6a7971b8a66450fab43ada1d04f67162dbc5a440e07c11eaf1495b612157b8`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `7926`
- Markdown files: `328`
- Python files: `325`
- Markdown references: `46318`
- Markdown Python commands: `862`
- Provider execution performed: `False`
- Workers requested: `8`
- Total build seconds: `31.796`
- Markdown scan seconds: `26.877`
- Python inventory seconds: `2.419`
- Patch application performed: `False`

## Severity counts

- `high`: `1661`
- `low`: `43`
- `medium`: `6222`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `43`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `6220`
- `md_mentions_missing_powershell_path`: `166`
- `md_mentions_missing_python_path`: `1469`
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
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 73 | `Tools/npu/npu_code_chunks/chunk_004_normalize_scene_spec_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 74 | `Tools/npu/npu_code_chunks/chunk_005_normalize_scene_spec_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 75 | `Tools/npu/npu_code_chunks/chunk_006_Tools_npu_npu_runtime_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 76 | `Tools/npu/npu_code_chunks/chunk_007_Tools_npu_ollama_runtime_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 77 | `Tools/npu/npu_code_chunks/chunk_008_Tools_npu_ollama_runtime_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 78 | `Tools/npu/npu_code_chunks/chunk_009_Tools_npu_build_blender_manual_context_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 79 | `Tools/npu/npu_code_chunks/chunk_010_Tools_npu_build_blender_manual_context_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 80 | `Tools/npu/npu_code_chunks/chunk_011_Tools_npu_run_dual_ai_pipeline_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 81 | `Tools/npu/npu_code_chunks/chunk_012_Tools_npu_run_dual_ai_pipeline_py.md` | Correct the documentation reference or restore the missing target if it is still required. |
| `medium` | `md_mentions_missing_markdown_path` | `Tools/npu/npu_code_context.md` | 82 | `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipe
```

### `output/validation/repository_consistency_map_smoke_full_toolbox_20260505-000415.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `379`
- SHA-256: `b2d06444ade6f64e09f1eb69030d3758202c80156e281893e3e9cf12c96f1ece`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Consistency Map Smoke

- Passed: `True`
- Return code: `0`
- Mapper report reused: `True`
- Workers requested: `8`
- Elapsed seconds: `0.03`
- Finding count: `7926`
- Markdown reference count: `46318`
- Markdown Python command count: `862`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`

```

### `output/validation/python_line_count_all_python_files_20260505-000415.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `18721`
- SHA-256: `170fad87a562f12edbe76adea7801669444ac91d098733f52843dae81a3a3c7f`
- Content included: `True`
- Content truncated: `True`

```text
# Full Python Line Count Inventory

- Stamp: 20260505-000415
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260505-000440.csv
- File count: 325
- Total Python lines: 95377
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
| 908 | `Tools/ai/build_deterministic_recommendations.py` |
| 902 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
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
| 657 | `Scripting/v61b/materials.py` |
| 631 | `Tools/npu/run_npu_review.py` |
| 627 | `Tools/validation/check_npu_pipeline_modules.py` |
| 626 | `Tools/ai/build_agent_review_patch_plan.py` |
| 618 | `Tools/ai/build_selective_execution_plan.py` |
| 608 | `Tools/ai/build_agent_review_patch_bundle.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 606 | `Tools/ai/build_runtime_tool_usage_telemetry.py` |
| 604 | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 579 | `Tools/ai/build_ai_context_pack.py` |
| 573 | `Tools/ai/run_pipeline_dry_run_matrix.py` |
| 569 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
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
| 471 | `Tools/ai/agent_memory_routing_policy.py` |
| 469 | `normalize_scene_spec.py` |
| 446 | `Tools/validation/check_reviewed_patch_specs.py` |
| 443 | `Tools/repo_patch_runner/apply_repo_mods.py` |
| 442 | `Tools/ai/promote_patch_spec_draft.py` |
| 439 | `Scripting/v61b/config.py` |
| 438 | `Tools/npu/ollama_runtime.py` |
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
| 403 | `Tools/validation/check_ai_workload_report_quality.py` |
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
| 331 | `Tools/workflow/startup_check.py` |
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
| 141 | `Tools/validation/run_ai_workload_report_quality_stamp_scoped_smoke.py` |
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
| 119 | `Tools/validation/check_package_structure.py` |
| 119 | `Tools/validation/check_ai_model_json.py` |
| 118 | `Tools/ai/pipeline/schema_report.py` |
| 117 | `Tools/workflow/workflow_shell_with_push.py` |
| 116 | `Tools/validation/run_runtime_sqlite_persistent_write_smoke.py` |
| 113 | `build_track_summary.py` |
| 111 | `Tools/npu/ai_memory_context.py` |
| 110 | `Tools/workflow/asset_inventory.py` |
| 107 | `Tools/npu/pipeline/config.py` |
| 107 | `Tools/ai/pipeline/markdown_report.py` |
| 105 | `Tools/validation/check_python_syntax.py` |
| 104 | `Tools/ai/pipeline/preflight.py` |
| 103 | `Tools/validation/run_full_toolbox_deterministic_chunks_telemetry_smoke.py` |
| 103 | `Scripting/v61b/hotpatch/runner.py` |
| 102 | `Tools/ai/pipeline/runner.py` |
| 102 | `Scripting/shared/path_utils.py` |
| 99 | `Tools/npu/pipeline/prompts.py` |
| 97 | `Tools/ai/pipeline/guardrail_models.py` |
| 97 | `Scripting/v61b_backgood/scene_utils.py` |
| 97 | `Scripting/v61b/scene_utils.py` |
| 96 | `Tools/validation/check_npu_pipeline_docs.py` |
| 92 | `Tools/workflow/gui/components/st_theme.py` |
| 91 | `Tools/npu/build_semantic_code_chunks.py` |
| 91 | `Scripting/v61b_backgood/hotpatch/common.py` |
| 91 | `Scripting/v61b/hotpatch/common.py` |
| 90 | `Tools/validation/run_npu_tool_request_contract_smoke.py` |
| 88 | `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` |
| 88 | `Scripting/shared/json_io.py` |
| 86 | `Tools/ai/pipeline/artifact_contracts.py` |
| 85 | `Scripting/v61b_backgood/hotpatch/lighting_patch.py` |
| 84 | `Tools/npu/pipeline/validators.py` |
| 83 | `Tools/validation/check_provider_result_parsing.py` |
| 81 | `Scripting/v61b_backgood/io_utils.py` |
| 81 | `Scripting/v61b/io_utils.py` |
| 80 | `Tools/npu/pipeline/fixtures.py` |
| 79 | `Scripting/_template_audio_reactive_package/main.py` |
| 75 | `Tools/npu/pipeline/context_builder.py` |
| 75 | `Scripting
```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260505-000440.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `15812`
- SHA-256: `44d67346aed16a1cad7309d5424c0a305d21fa521ebe799d2b94352d881fd4bd`
- Content included: `True`
- Content truncated: `False`

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
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_agent_review_patch_plan.py,626
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/build_runtime_tool_usage_telemetry.py,606
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,604
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
Scripting/v61b/hot_update_scene_v61b.py,63
Scripting/v61b_backgood/hot_update_scene_v61b.py,61
Tools/npu/pipeline/io_utils.py,61
Scripting/v61b_backgood/hotpatch/runner.py,60
Tools/validation/check_npu_pipeline_helper_tests.py,59
Tools/npu/pipeline/artifact_writer.py,56
Tools/ai/merge_ai_candidates.py,53
Tools/npu/pipeline/legacy_compat.py,52
Scripting/_template_audio_reactive_package/audio_mapping.py,51
Scripting/v61b/reload_utils.py,51
Tools/ai/pipeline/cli.py,50
Scripting/_template_audio_reactive_package/config.py,49
Scripting/_template_audio_reactive_package/materials.py,35
Tools/ai/pipeline/orchestrator.py,31
Scripting/v61b/camera_setup.py,29
Scripting/v61b_backgood/camera_setup.py,29
Scripting/_template_audio_reactive_package/camera.py,26
Scripting/_template_audio_reactive_package/render_settings.py,26
Scripting/_template_audio_reactive_package/lighting.py,23
Tools/ai/pipeline/__init__.py,23
Scripting/_template_audio_reactive_package/scene_objects.py,21
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profiles_reference.py,20
Scripting/v61b/spaziotempo/features/catalog.py,19
Tools/ai/pipeline/defaults.py,15
Scripting/shared/__init__.py,13
Scripting/v61b/spaziotempo/__init__.py,4
Scripting/v61b/hotpatch/__init__.py,3
Scripting/v61b_backgood/hotpatch/__init__.py,3
Scripting/v61b/__init__.py,1
Scripting/v61b/spaziotempo/core/__init__.py,1
Scripting/v61b/spaziotempo/features/__init__.py,1
Scripting/v61b_backgood/__init__.py,1
Tools/workflow/gui/components/__init__.py,1

```

### `output/ai_pipeline/full_toolbox_20260505-000415_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1279`
- SHA-256: `548e931d689f61ab24f80e2f76760c896afba92192fc42c2aabaa1731d0a75aa`
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

- `recommendations`: `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.json` exists=`True` size=`166369`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.md` exists=`True` size=`19785`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_20260505-000415_bridge_orchestrator.json` exists=`True` size=`1224`
- `patch_plan`: `output/patch_specs/full_toolbox_20260505-000415_agent_review_patch_plan.json` exists=`True` size=`233904`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_20260505-000415_agent_review_patch_plan.md` exists=`True` size=`19406`

## Warnings

- patch_plan: max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/patch_specs/full_toolbox_20260505-000415_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `19406`
- SHA-256: `6f1b478df4f923501b0d7bac6aa7c0b30f473e9ed1dcc345bedffa535a04f001`
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

- `orchestrator`: `output/ai_pipeline/full_toolbox_20260505-000415_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.json`
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
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_016 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_017 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1325` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/ful
```

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

### `output/ai_pipeline/full_toolbox_20260505-000415_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1224`
- SHA-256: `74188ef58231759c038c776ae681b67fd572852a800435b3b8f04b6768169210`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-05T00:05:19",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.json",
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

### `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `166369`
- SHA-256: `0ecfeb4ea5a35bcaa8b41fc2d7d34290ac800e84c954383cef5c27881b453e77`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_synthesizer",
  "generated_at": "2026-05-05T00:05:19",
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
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/python_line_count_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/python_syntax_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/npu_provider_environment_full_toolbox_20260505-000415.json",
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
          "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260505-000415.json",
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
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/full_memory_tool_regeneration_20260505-000415_workflow.json",
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
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/analysis/code_interpreter_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/python_line_count_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/python_syntax_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/npu_provider_environment_full_toolbox_20260505-000415.json",
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
          "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260505-000415.json",
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
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260505-000415.json",
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
          "path": "output/validation/full_memory_tool_regeneration_20260505-000415_workflow.json",
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
        "source": "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md",
        "line": 368,
        "target": "Tools/validation/check_markdown_command_hygiene.py",
        "flag": "",
        "evidence": ""
      },
      "guardrails": {
        "patch_application_performed": false,
        "manual_review_required": true,
        "cosmetic_patch_allo
```

### `output/ai_pipeline/full_toolbox_20260505-000415_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `19785`
- SHA-256: `ee298ab78d2df6e71a0de27648f892c21782bbd7f1eb1e1c9b51c3ee72a02e50`
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
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1232`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_016 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_017 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `d
```

### `output/ai_pipeline/full_toolbox_20260505-000415_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `9996`
- SHA-256: `234a42c9d6a018b5d38dd36ee21960457c7ad6ef5bbbcf271f2b1871728efbc0`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-05T00:05:19",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": false,
  "errors": [
    "GPU output missing: output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.json"
  ],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 2.008,
  "gpu_returncode": 1,
  "gpu_stdout_tail": "",
  "gpu_stderr_tail": "Traceback (most recent call last):\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_supervised.py\", line 1129, in <module>\n    raise SystemExit(main())\n                     ~~~~^^\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_supervised.py\", line 1078, in main\n    report = run_supervised(args)\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_supervised.py\", line 730, in run_supervised\n    evidence = read_json(resolve_path(repo_root, args.evidence))\n  File \"C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\ai\\run_agent_gpu_deep_planning_review.py\", line 122, in read_json\n    return json.loads(path.read_text(encoding=\"utf-8-sig\"))\n                      ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Python314\\Lib\\pathlib\\__init__.py\", line 787, in read_text\n    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:\n         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Python314\\Lib\\pathlib\\__init__.py\", line 771, in open\n    return io.open(self, mode, buffering, encoding, errors, newline)\n           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nFileNotFoundError: [Errno 2] No such file or directory: 'C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\agent_review_evidence_sufficiency.json'\n",
  "gpu_output": "output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.md",
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
  "checkpoint_dir": "output/ai_pipeline/full_toolbox_20260505-000415_checkpoints",
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

### `output/ai_pipeline/full_toolbox_20260505-000415_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2178`
- SHA-256: `86a6daad905c8773c4f43b4657971bcc04a417d3bc1b0e49035b1975e1417650`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `False`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `1`
- `elapsed_seconds`: `2.008`
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

### `output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1255`
- SHA-256: `054285827650641ded86c2ea0ca869edd73a0457aa5f268b92807c8ded851f36`
- Content included: `True`
- Content truncated: `False`

```text
{
    "schema_version":  1,
    "kind":  "agent_gpu_parallel_report",
    "generated_at":  "2026-05-05T00:05:19.2678144+02:00",
    "stamp":  "20260505-000415",
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

### `output/ai_pipeline/full_toolbox_20260505-000415_parallel_gpu.md`

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
- SHA-256: `0d3deca6c419e58fdbd8f2f3ee20a322e21f503d4256139e2936fbc55246ac82`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-05T00:05:19`
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

### `output/analysis/code_interpreter_full_toolbox_20260505-000415.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7088`
- SHA-256: `a2f6197f97261f02abae9b618ca361432ac5e885e626c323cf99b054355ca827`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `279`
- Parsed files: `279`
- Total lines: `78984`
- Total functions: `2802`
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
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `626` lines, risk `medium`

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

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260505-000415.md`

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

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260505-000415.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1882`
- SHA-256: `9f14a9107694b5ca865d5b118cebbf7f4513bba188080eca8e750cb6b3099d94`
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
- `gpu_elapsed_seconds`: `2.008`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `unavailable`

## Performance

- Analyzer elapsed seconds: `0.0`
- GPU elapsed seconds: `2.008`
- GPU average round seconds: `0.0`
- GPU timing source: `unavailable`
- NPU average audit seconds: `0.0`
- NPU duration sample count: `0`

## Operational opinions

- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=unavailable

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

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_20260505-000415.md`

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

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260505-000415.md`

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
