# Local Validation Evidence Bundle

- Generated at: `2026-05-02T14:36:30`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `12`
- `patch_plan_summary_seen`: `True`
- `code_patch_plan_summary_enriched_count`: `2`

## Reports

### `output/validation/python_syntax_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/analysis/code_interpreter_report_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `67`

### `output/validation/artifact_domain_registry_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `artifact_domain_registry_validation`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/agent_review_code_patch_plan_with_static_smoke_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_code_patch_plan_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/code_edit_proposal_from_plan_smoke_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_edit_proposal_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/code_patch_artifact_pack_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_patch_artifact_pack`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_line_count_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/patch_specs/agent_review_code_patch_plan_with_static_pr109.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_code_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `31`
- Recommended next layer: `manual_review_then_targeted_code_pr`
- Warnings: `['static recommendations capped at 30 of 67']`
- Patch plan summary count: `31`
- Fallback used: `None`
- Manual review required: `True`

### `output/patch_specs/agent_review_code_patch_plan_fixture_built.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_code_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommended next layer: `manual_review_then_targeted_code_pr`
- Patch plan summary count: `1`
- Fallback used: `None`
- Manual review required: `True`

## Patch plan summary

### `output/patch_specs/agent_review_code_patch_plan_with_static_pr109.json`

- Patch plan count: `31`
- Fallback used: `None`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### code_contract_001 — cpu_validation
- Source: `None`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: `['Tools/validation/check_validation_report_contract.py']`
- Rationale: Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.
- Strategy: Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation. Current CSV sizing hint: 187 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_001 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/agent_memory_policy.py']`
- Rationale: Static code interpreter recommendation `code_static_001` flagged `Tools/ai/agent_memory_policy.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 307 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_002 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/agent_state.py']`
- Rationale: Static code interpreter recommendation `code_static_002` flagged `Tools/ai/agent_state.py` for manual review: medium-size Python module.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 533 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_003 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/artifact_domain_registry.py']`
- Rationale: Static code interpreter recommendation `code_static_003` flagged `Tools/ai/artifact_domain_registry.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 202 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_004 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_agent_agnostic_tool_inventory.py']`
- Rationale: Static code interpreter recommendation `code_static_004` flagged `Tools/ai/build_agent_agnostic_tool_inventory.py` for manual review: medium-size Python module, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 408 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_005 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_agent_memory_inventory.py']`
- Rationale: Static code interpreter recommendation `code_static_005` flagged `Tools/ai/build_agent_memory_inventory.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 397 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_006 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_agent_review_code_patch_plan.py']`
- Rationale: Static code interpreter recommendation `code_static_006` flagged `Tools/ai/build_agent_review_code_patch_plan.py` for manual review: medium-size Python module.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 351 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_007 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_agent_review_patch_plan.py']`
- Rationale: Static code interpreter recommendation `code_static_007` flagged `Tools/ai/build_agent_review_patch_plan.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 562 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_008 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_ai_context_pack.py']`
- Rationale: Static code interpreter recommendation `code_static_008` flagged `Tools/ai/build_ai_context_pack.py` for manual review: medium-size Python module, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 558 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_009 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_code_interpreter_report.py']`
- Rationale: Static code interpreter recommendation `code_static_009` flagged `Tools/ai/build_code_interpreter_report.py` for manual review: medium-size Python module, TODO/FIXME markers detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 415 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_010 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_dry_run_matrix_evidence_bundle.py']`
- Rationale: Static code interpreter recommendation `code_static_010` flagged `Tools/ai/build_dry_run_matrix_evidence_bundle.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 398 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_011 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_full_context_golden_proposals.py']`
- Rationale: Static code interpreter recommendation `code_static_011` flagged `Tools/ai/build_full_context_golden_proposals.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 392 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_012 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_github_evidence_bundle.py']`
- Rationale: Static code interpreter recommendation `code_static_012` flagged `Tools/ai/build_github_evidence_bundle.py` for manual review: medium-size Python module, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 688 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_013 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_local_ai_enrichment_plan.py']`
- Rationale: Static code interpreter recommendation `code_static_013` flagged `Tools/ai/build_local_ai_enrichment_plan.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 357 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_014 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_music_intermediates.py']`
- Rationale: Static code interpreter recommendation `code_static_014` flagged `Tools/ai/build_music_intermediates.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 314 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_015 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_patch_specs_from_proposals.py']`
- Rationale: Static code interpreter recommendation `code_static_015` flagged `Tools/ai/build_patch_specs_from_proposals.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 414 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_016 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_repository_change_proposals.py']`
- Rationale: Static code interpreter recommendation `code_static_016` flagged `Tools/ai/build_repository_change_proposals.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 582 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_017 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_selective_execution_plan.py']`
- Rationale: Static code interpreter recommendation `code_static_017` flagged `Tools/ai/build_selective_execution_plan.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 618 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_018 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/build_workload_quality_lane_routing.py']`
- Rationale: Static code interpreter recommendation `code_static_018` flagged `Tools/ai/build_workload_quality_lane_routing.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 186 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_019 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/check_local_resource_lanes.py']`
- Rationale: Static code interpreter recommendation `code_static_019` flagged `Tools/ai/check_local_resource_lanes.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 335 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_020 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/check_npu_provider_environment.py']`
- Rationale: Static code interpreter recommendation `code_static_020` flagged `Tools/ai/check_npu_provider_environment.py` for manual review: large functions detected, complex functions detected, static risk calls detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 189 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_021 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/code_patch_plan_common.py']`
- Rationale: Static code interpreter recommendation `code_static_021` flagged `Tools/ai/code_patch_plan_common.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 199 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_022 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/model_json.py']`
- Rationale: Static code interpreter recommendation `code_static_022` flagged `Tools/ai/model_json.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 130 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_023 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/pipeline/preflight.py']`
- Rationale: Static code interpreter recommendation `code_static_023` flagged `Tools/ai/pipeline/preflight.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 104 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_024 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/pipeline/remediation.py']`
- Rationale: Static code interpreter recommendation `code_static_024` flagged `Tools/ai/pipeline/remediation.py` for manual review: large functions detected, complex functions detected, TODO/FIXME markers detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 185 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_025 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/pipeline/steps.py']`
- Rationale: Static code interpreter recommendation `code_static_025` flagged `Tools/ai/pipeline/steps.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 197 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_026 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/promote_patch_spec_draft.py']`
- Rationale: Static code interpreter recommendation `code_static_026` flagged `Tools/ai/promote_patch_spec_draft.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 442 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_027 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/refine_megalithic_review_signals.py']`
- Rationale: Static code interpreter recommendation `code_static_027` flagged `Tools/ai/refine_megalithic_review_signals.py` for manual review: medium-size Python module.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 489 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_028 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/review_wave_entrypoints.py']`
- Rationale: Static code interpreter recommendation `code_static_028` flagged `Tools/ai/review_wave_entrypoints.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 240 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_029 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/run_agent_gpu_deep_planning_review.py']`
- Rationale: Static code interpreter recommendation `code_static_029` flagged `Tools/ai/run_agent_gpu_deep_planning_review.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 714 lines; verify current count locally before editing. Do not apply this plan automatically.

#### code_static_030 — static_code_interpreter
- Source: `None`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/ai/run_agent_gpu_deep_planning_supervised.py']`
- Rationale: Static code interpreter recommendation `code_static_030` flagged `Tools/ai/run_agent_gpu_deep_planning_supervised.py` for manual review: medium-size Python module, large functions detected, complex functions detected, static risk calls detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 478 lines; verify current count locally before editing. Do not apply this plan automatically.


### `output/patch_specs/agent_review_code_patch_plan_fixture_built.json`

- Patch plan count: `1`
- Fallback used: `None`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### code_contract_001 — cpu_validation
- Source: `None`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: `['Tools/validation/check_validation_report_contract.py']`
- Rationale: Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.
- Strategy: Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation. Current CSV sizing hint: 152 lines; verify current count locally before editing. Do not apply this plan automatically.


## Artifact manifest

- `output/validation/python_syntax_pr109.json` exists=`True` size=`30785` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_report_pr109.json` exists=`True` size=`623938` suffix=`.json` preview_chars=`1500`
- `output/validation/artifact_domain_registry_pr109.json` exists=`True` size=`11762` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_code_patch_plan_with_static_smoke_pr109.json` exists=`True` size=`7644` suffix=`.json` preview_chars=`1500`
- `output/validation/code_edit_proposal_from_plan_smoke_pr109.json` exists=`True` size=`2652` suffix=`.json` preview_chars=`1500`
- `output/validation/code_patch_artifact_pack_pr109.json` exists=`True` size=`4947` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_pr109.json` exists=`True` size=`3104` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/agent_review_code_patch_plan_with_static_pr109.json` exists=`True` size=`66137` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/code_interpreter_report_pr109.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7365`
- SHA-256: `aab021c1054fca1dc80c7607fa31c5ecb02f1b65c02974998c368a12d15cdc47`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `123`
- Parsed files: `123`
- Total lines: `32676`
- Total functions: `1140`
- Total classes: `29`
- Risk signals: `12`
- TODO/FIXME markers: `17`
- Recommendation count: `67`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `714` lines, risk `medium`
- `Tools/ai/build_github_evidence_bundle.py` — `688` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/ai/build_repository_change_proposals.py` — `582` lines, risk `medium`
- `Tools/ai/run_pipeline_dry_run_matrix.py` — `573` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `562` lines, risk `medium`
- `Tools/ai/build_ai_context_pack.py` — `558` lines, risk `medium`
- `Tools/ai/suggest_repository_updates.py` — `551` lines, risk `medium`
- `Tools/ai/agent_state.py` — `533` lines, risk `medium`
- `Tools/ai/run_megalithic_repo_review.py` — `519` lines, risk `medium`
- `Tools/validation/ai_pipeline_report_contracts.py` — `497` lines, risk `medium`
- `Tools/ai/build_agent_review_code_patch_plan.py` — `494` lines, risk `medium`
- `Tools/ai/refine_megalithic_review_signals.py` — `489` lines, risk `medium`
- `Tools/validation/run_agent_review_patch_plan_full_validation.py` — `487` lines, risk `medium`
- `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` — `483` lines, risk `medium`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `478` lines, risk `medium`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `471` lines, risk `medium`
- `Tools/validation/check_reviewed_patch_specs.py` — `446` lines, risk `medium`
- `Tools/ai/promote_patch_spec_draft.py` — `442` lines, risk `medium`

## Recommendations

- `code_static_001` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_002` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_003` `Tools/ai/artifact_domain_registry.py` risk `medium`: complex functions detected
- `code_static_004` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_005` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_006` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_007` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_008` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_009` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_010` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_011` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_012` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_013` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_014` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_015` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_017` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_018` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_019` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_021` `Tools/ai/code_patch_plan_common.py` risk `medium`: complex functions detected
- `code_static_022` `Tools/ai/model_json.py` risk `medium`: complex functions detected
- `code_static_023` `Tools/ai/pipeline/preflight.py` risk `medium`: complex functions detected
- `code_static_024` `Tools/ai/pipeline/remediation.py` risk `medium`: large functions detected, complex functions detected, TODO/FIXME markers detected
- `code_static_025` `Tools/ai/pipeline/steps.py` risk `medium`: large functions detected
- `code_static_026` `Tools/ai/promote_patch_spec_draft.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_027` `Tools/ai/refine_megalithic_review_signals.py` risk `medium`: medium-size Python module
- `code_static_028` `Tools/ai/review_wave_entrypoints.py` risk `medium`: large functions detected, complex functions detected
- `code_static_029` `Tools/ai/run_agent_gpu_deep_planning_review.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_030` `Tools/ai/run_agent_gpu_deep_planning_supervised.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_031` `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_032` `Tools/ai/run_local_provider_probe.py` risk `medium`: complex functions detected
- `code_static_033` `Tools/ai/run_megalithic_repo_review.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_034` `Tools/ai/run_npu_decode_smoke_diagnostic.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_035` `Tools/ai/run_npu_gpu_deep_review_auditor.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_036` `Tools/ai/run_pipeline_dry_run_matrix.py` risk `medium`: medium-size Python module, large functions detected, static risk calls detected
- `code_static_037` `Tools/ai/select_semantic_code_chunks.py` risk `medium`: large functions detected, complex functions detected
- `code_static_038` `Tools/ai/smart_ai_gatekeeper.py` risk `medium`: complex functions detected, TODO/FIXME markers detected
- `code_static_039` `Tools/ai/suggest_repository_updates.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_040` `Tools/ai/validate_ai_artifacts.py` risk `medium`: complex functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/patch_specs/agent_review_code_patch_plan_with_static_pr109.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `23352`
- SHA-256: `c2c50e9369d592eb03137e7f214a9510d9d56f1c39f5cbab65e85a7c92ed87b0`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Code Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_code_patch_plan`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `31`
- Contract-drift plan count: `1`
- Static-code plan count: `30`

## Inputs

- `code_contract_drift_report`: `Tools/ai/fixtures/code_contract_drift_fixture.json`
- `line_count_csv`: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-141635.csv`
- `line_count_csv_loaded`: `True`
- `code_interpreter_report`: `output/analysis/code_interpreter_report_pr109.json`
- `code_interpreter_report_loaded`: `True`

## Plans

### `code_contract_001`

- Area: `cpu_validation`
- Source kind: `code_contract_drift`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: `Tools/validation/check_validation_report_contract.py`
- Rationale: Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.
- Strategy: Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation. Current CSV sizing hint: 187 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_001`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/agent_memory_policy.py`
- Rationale: Static code interpreter recommendation `code_static_001` flagged `Tools/ai/agent_memory_policy.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 307 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_002`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/agent_state.py`
- Rationale: Static code interpreter recommendation `code_static_002` flagged `Tools/ai/agent_state.py` for manual review: medium-size Python module.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 533 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_003`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/artifact_domain_registry.py`
- Rationale: Static code interpreter recommendation `code_static_003` flagged `Tools/ai/artifact_domain_registry.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 202 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_004`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_agent_agnostic_tool_inventory.py`
- Rationale: Static code interpreter recommendation `code_static_004` flagged `Tools/ai/build_agent_agnostic_tool_inventory.py` for manual review: medium-size Python module, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 408 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_005`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_agent_memory_inventory.py`
- Rationale: Static code interpreter recommendation `code_static_005` flagged `Tools/ai/build_agent_memory_inventory.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 397 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_006`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_agent_review_code_patch_plan.py`
- Rationale: Static code interpreter recommendation `code_static_006` flagged `Tools/ai/build_agent_review_code_patch_plan.py` for manual review: medium-size Python module.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 351 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_007`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_agent_review_patch_plan.py`
- Rationale: Static code interpreter recommendation `code_static_007` flagged `Tools/ai/build_agent_review_patch_plan.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 562 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_008`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_ai_context_pack.py`
- Rationale: Static code interpreter recommendation `code_static_008` flagged `Tools/ai/build_ai_context_pack.py` for manual review: medium-size Python module, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 558 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_009`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_code_interpreter_report.py`
- Rationale: Static code interpreter recommendation `code_static_009` flagged `Tools/ai/build_code_interpreter_report.py` for manual review: medium-size Python module, TODO/FIXME markers detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 415 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_010`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_dry_run_matrix_evidence_bundle.py`
- Rationale: Static code interpreter recommendation `code_static_010` flagged `Tools/ai/build_dry_run_matrix_evidence_bundle.py` for manual review: complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 398 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_011`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_full_context_golden_proposals.py`
- Rationale: Static code interpreter recommendation `code_static_011` flagged `Tools/ai/build_full_context_golden_proposals.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 392 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_012`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_github_evidence_bundle.py`
- Rationale: Static code interpreter recommendation `code_static_012` flagged `Tools/ai/build_github_evidence_bundle.py` for manual review: medium-size Python module, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 688 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_013`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_local_ai_enrichment_plan.py`
- Rationale: Static code interpreter recommendation `code_static_013` flagged `Tools/ai/build_local_ai_enrichment_plan.py` for manual review: large functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 357 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_014`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_music_intermediates.py`
- Rationale: Static code interpreter recommendation `code_static_014` flagged `Tools/ai/build_music_intermediates.py` for manual review: large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 314 lines; verify current count locally before editing. Do not apply this plan automatically.

### `code_static_015`

- Area: `static_code_interpreter`
- Source kind: `code_interpreter_report`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `Tools/ai/build_patch_specs_from_proposals.py`
- Rationale: Static code interpreter recommendation `code_static_015` flagged `Tools/ai/build_patch_specs_from_proposals.py` for manual review: medium-size Python module, large functions detected, complex functions detected.
- Strategy: Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `agent_review_code_patch_plan`. Current CSV sizing hint: 414 lines; verify current count local
```

### `output/patch_specs/code_edit_proposal_from_plan_pr109.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1104`
- SHA-256: `a4d2c8d7779b339f60d30e59ea0d9dc07a099147b7a22a54aec0dd6bc0eb55ae`
- Content included: `True`
- Content truncated: `False`

```text
# Code Edit Proposal Build

- Passed: `True`
- Apply mode: `report_only_code_edit_proposal_build`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Selected plan: `code_contract_001`

## Proposal summary

- Target file: `Tools/validation/check_validation_report_contract.py`
- Edit kind: `no_op`
- Ready for manual review: `True`
- Target line count: `187`
- Target SHA-256: `fbdf0101c508fd1d12ed285b7cb180658bb243cc46b8f69b57634ad7bc0497d0`
- Rationale: Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.
- Strategy: Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation. Current CSV sizing hint: 152 lines; verify current count locally before editing. Do not apply this plan automatically.

## Guardrail

This build creates proposal metadata only. It does not apply the proposal.

```

### `docs/TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `8579`
- SHA-256: `d0a5be72375cbd31aec7347b1fef2f3ebab74f7114fdcfa29c56e788d4f5bdde`
- Content included: `True`
- Content truncated: `False`

```text
# Tool-Agnostic Artifact Expansion Roadmap

## Purpose

This document reframes the current local AI work as a tool-agnostic artifact engine rather than a Blender-only prototype.

The immediate implementation is code-focused because code is the safest and most testable base layer. The same philosophy should generalize to audio, text, documentation, scene descriptions, validation reports, prompts and future domain-specific artifacts.

## Core shift

Previous framing:

```text
Blender prototype support
```

Current framing:

```text
tool-agnostic artifact production and validation framework
```

The framework should be able to ingest evidence, generate proposals, validate contracts, produce compact bundles and keep every high-risk action manual-review-first.

## Stable primitives already emerging

The current PR introduces or connects these primitives:

```text
contract drift report
agent review patch plan
code patch plan
complete code edit proposal
docs follow-up suggestion
artifact pack
evidence bundle
line-count evidence
agnostic context stack smoke
manual review gate
```

These are not code-only concepts. They can be generalized as:

```text
domain evidence
artifact proposal
artifact validator
artifact follow-up
artifact pack
artifact evidence bundle
manual promotion gate
```

## Domains

The framework should treat domains as lanes, not as hard-coded project identities.

Initial domains:

```text
code
docs
validation
workflow
local_ai_context
```

Planned domains:

```text
audio
text
prompt
scene_spec
render_plan
asset_manifest
model_context
provider_result
```

Each domain should declare:

```text
input evidence types
allowed output artifact types
validators
blocked targets
manual review rules
promotion rules
bundle summary shape
```

## Artifact lifecycle

Every artifact should pass through the same lifecycle:

```text
collect evidence
normalize evidence
produce proposal
validate proposal
pack compact evidence
manual review
promote or reject
```

No artifact should jump directly from AI generation to source/runtime mutation.

## Universal guardrails

All lanes inherit these default guardrails:

```text
provider_execution_performed = false unless explicitly requested
patch_application_performed = false unless explicitly requested
source_writes_performed = false unless explicitly requested
manual_review_required = true
output/** is local only
raw runtime artifacts are not versioned
compact evidence is preferred
full analysis JSON is not committed
SQLite/database artifacts are not committed
Blender runtime is not executed unless the task is explicitly runtime-scoped
```

## Artifact categories

### Evidence artifact

Evidence artifacts describe what was observed.

Examples:

```text
code_contract_drift
docs_contract_drift
python_line_count_csv
agnostic_context_stack_smoke
provider_result_report
audio_analysis_summary
text_corpus_summary
```

Requirements:

```text
schema_version
kind
passed
errors
warnings
provider_execution_performed
patch_application_performed
source_writes_performed
source references
compact summary
```

### Proposal artifact

Proposal artifacts describe what could be changed or generated.

Examples:

```text
agent_review_code_patch_plan
code_edit_proposal
agent_review_code_docs_followup
scene_patch_plan
audio_feature_mapping_plan
text_rewrite_plan
prompt_refinement_plan
```

Requirements:

```text
kind
apply_mode
manual_review_required
targets
rationale
strategy
validation_commands
stop_conditions
risk
status
```

### Pack artifact

Pack artifacts summarize large proposal/evidence sets for GitHub review.

Examples:

```text
code_patch_artifact_pack
github_evidence_bundle
future audio_artifact_pack
future text_artifact_pack
future scene_spec_artifact_pack
```

Requirements:

```text
raw content minimized
large payloads omitted or bounded
reviewable summaries only
links/paths to source local artifacts
manual decision section
```

## Limits to actively test

The next phase should intentionally find limits in these areas.

### 1. Schema pressure

Question:

```text
Can one schema family describe code, docs, audio, text and scene artifacts without becoming vague?
```

Test strategy:

```text
create one minimal proposal fixture per domain
run common smoke validator concepts
compare required fields
split only when field semantics truly diverge
```

### 2. Evidence size pressure

Question:

```text
How much raw evidence can be summarized before decisions lose traceability?
```

Test strategy:

```text
large code file summary
large audio analysis summary
large text corpus summary
large provider result summary
compact pack output
manual review check
```

### 3. Target safety pressure

Question:

```text
Can target path policies stay generic while still blocking dangerous domain-specific outputs?
```

Test strategy:

```text
code target policy
docs target policy
audio output target policy
scene spec target policy
runtime artifact target policy
```

### 4. Validator portability

Question:

```text
Can validators be declared as metadata and executed separately from artifact generation?
```

Test strategy:

```text
proposal declares validators
smoke validates validators exist as strings
runner remains separate
no automatic execution in proposal generation
```

### 5. Provider boundary

Question:

```text
Can provider outputs be consumed as evidence without turning provider execution into a hidden dependency?
```

Test strategy:

```text
provider_result_report fixture
provider_execution_performed flag
source prompt hash
output summary only
manual review gate
```

### 6. Domain handoff quality

Question:

```text
Can one artifact from a domain notify another domain safely?
```

Examples:

```text
code patch plan -> docs follow-up
audio analysis -> scene spec proposal
text analysis -> prompt refinement plan
provider result -> validation follow-up
```

Test strategy:

```text
build bridge artifacts
validate no writes
validate compact summary
require manual review
```

## New horizon: artifact domain registry

The framework should eventually define a domain registry.

Potential file:

```text
Tools/ai/artifact_domain_registry.py
```

Initial registry record:

```json
{
  "domain": "code",
  "proposal_kinds": ["agent_review_code_patch_plan", "code_edit_proposal"],
  "evidence_kinds": ["code_contract_drift", "python_line_count_csv"],
  "pack_kinds": ["code_patch_artifact_pack"],
  "blocked_target_prefixes": ["output/", "renders/"],
  "blocked_target_suffixes": [".db", ".sqlite", ".sqlite3"],
  "requires_manual_review": true
}
```

This would let future domains plug into the same lifecycle without copying logic.

## New horizon: universal artifact proposal

The code edit proposal can evolve into a universal proposal shape.

Generic shape:

```json
{
  "kind": "artifact_proposal",
  "domain": "code|docs|audio|text|scene_spec|prompt",
  "target": {},
  "rationale": "why",
  "strategy": "how",
  "payload": {},
  "validation_commands": [],
  "stop_conditions": [],
  "manual_review_required": true,
  "provider_execution_performed": false,
  "artifact_write_performed": false
}
```

Do not replace domain-specific proposals too early. First collect fixtures and real examples.

## Recommended next implementation sequence

### Phase A — complete code lane base

```text
code_edit_proposal_smoke
code patch artifact pack includes code edit proposal summaries
macro evidence bundle includes code edit proposal smoke
local validation proves contract
```

### Phase B — introduce artifact domain registry

```text
create registry module
add code/docs domains
add smoke validator for registry
consume registry in proposal validators where useful
```

### Phase C — add non-code fixture lane

Choose one low-risk domain first:

```text
text artifact proposal
```

Reason:

```text
text has low runtime risk
text is easy to validate structurally
text can reuse docs/prompt workflows
```

Then add:

```text
audio summary proposal
scene spec proposal
provider result proposal
```

### Phase D — measure limits

For each domain, measure:

```text
artifact size
summary quality
validator strictness
manual review burden
cross-domain follow-up quality
```

## Decision rule

A new capability is acceptable only when it preserves:

```text
explicit evidence
bounded artifact size
manual review
validated report contract
no implicit runtime side effects
compact GitHub evidence
```

If a capability requires hidden execution, raw output commits or automatic mutation, it belongs in a separate explicit implementation branch, not in the agnostic base layer.

```

### `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `12430`
- SHA-256: `761012517b6af20afb6bb9d65fceaeeacbffe4895b459bd4d0bdba9168653678`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Code Patch Plan

## Purpose

This document defines the report-only lane for turning repository review evidence into safe, manual-review code patch plans.

The goal is to extend the current documentation patch-plan workflow toward code editing without enabling automatic source mutation.

This lane may describe code edits and related documentation follow-up work. It must not apply either code or documentation patches automatically.

## Relationship to existing lanes

Existing documentation patch-plan lane:

```text
local evidence / review reports
  -> Tools/ai/build_agent_review_patch_plan.py
  -> output/patch_specs/agent_review_patch_plan.json
  -> Tools/validation/run_agent_review_patch_plan_smoke.py
  -> manual-review documentation edits
  -> Git-trackable evidence bundle
```

Code patch-plan lane:

```text
code_contract_drift report
  -> Tools/ai/build_agent_review_code_patch_plan.py
  -> output/patch_specs/agent_review_code_patch_plan.json
  -> Tools/validation/run_agent_review_code_patch_plan_smoke.py
  -> manual review
  -> optional small hand-applied code PR
```

Complete code edit proposal helper:

```text
manual-review code patch plan item
  -> Tools/ai/code_edit_proposal_helpers.py
  -> code_edit_proposal metadata
  -> validators + stop conditions
  -> human applies or rejects the edit in a separate implementation step
```

Documentation follow-up bridge:

```text
agent_review_code_patch_plan report
  -> Tools/ai/build_code_patch_docs_followup.py
  -> output/patch_specs/agent_review_code_docs_followup.json
  -> manual-review documentation queue
```

The bridge lets code-plan output notify the documentation lane. It is not an apply queue.

## Required default behavior

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
apply_mode = report_only_manual_review_code_patch_plan
```

For complete code edit proposals:

```text
kind = code_edit_proposal
apply_mode = report_only_manual_review_code_edit_proposal
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

For docs follow-up reports:

```text
kind = agent_review_code_docs_followup
apply_mode = report_only_manual_review_docs_followup
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

A report that violates these defaults should fail validation unless the task explicitly authorizes a later, separate reviewed implementation phase.

## JSON report shape

```json
{
  "schema_version": 1,
  "kind": "agent_review_code_patch_plan",
  "passed": true,
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_manual_review_code_patch_plan",
  "manual_review_required": true,
  "patch_plan_count": 0,
  "code_patch_plans": [],
  "errors": [],
  "warnings": []
}
```

Each `code_patch_plans[]` item should be small and reviewable:

```json
{
  "id": "code_patch_001",
  "area": "validation",
  "risk": "low",
  "status": "ready_for_manual_review",
  "target_files": ["Tools/validation/example.py"],
  "rationale": "Why the edit is needed.",
  "edit_strategy": "How the edit should be made.",
  "proposed_patch": "optional bounded preview only",
  "validation_commands": [
    "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
    "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
    "git diff --check"
  ],
  "stop_conditions": [
    "Stop if the target file does not exist unless the task explicitly authorizes a new source file.",
    "Stop if the patch touches output/**.",
    "Stop if validation fails.",
    "Stop if Blender runtime execution is required."
  ],
  "manual_review_required": true
}
```

## Complete code edit proposal helper

Helper:

```text
Tools/ai/code_edit_proposal_helpers.py
```

This helper is the first coding-complete primitive for the code-editor lane. It does not apply edits. It builds a complete proposal object containing:

```text
target path
target metadata: exists, suffix, line_count, sha256
edit kind: no_op, structured_edit, unified_diff
bounded unified diff preview
structured operations
rationale
edit strategy
validation commands
stop conditions
manual review status
```

Supported edit kinds:

```text
no_op
structured_edit
unified_diff
```

Supported structured operations:

```text
replace
insert_after
insert_before
delete
append
```

A complete proposal must remain metadata-only:

```text
source_writes_performed = false
patch_application_performed = false
provider_execution_performed = false
```

The helper validates that target files do not escape the repository, do not target blocked artifacts, and include validators. For Python targets it automatically adds:

```powershell
python -m py_compile .\<target-file>
```

alongside repository validators:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

A unified-diff proposal must reference the normalized target file and include standard diff markers:

```text
---
+++
@@
```

The helper rejects or flags proposals that mention blocked fragments such as:

```text
output/
renders/
.sqlite
.db
full_analysis
analysis_full
```

## Builder, fixtures and smoke validator

Builder:

```text
Tools/ai/build_agent_review_code_patch_plan.py
```

Fixture inputs:

```text
Tools/ai/fixtures/code_contract_drift_fixture.json
Tools/ai/fixtures/agent_review_code_patch_plan_fixture.json
```

Smoke validator:

```text
Tools/validation/run_agent_review_code_patch_plan_smoke.py
```

Build from fixture:

```powershell
python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\Tools\ai\fixtures\code_contract_drift_fixture.json `
  --output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --markdown-output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.md
```

Validate fixture report:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\Tools\ai\fixtures\agent_review_code_patch_plan_fixture.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke.json
```

Validate generated report:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_built.json
```

The builder and smoke validator preserve:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

They do not apply patches, run providers, run Blender or write source files.

## Documentation follow-up bridge

When a code patch plan proposes code changes, the docs follow-up bridge emits a related documentation review queue.

Bridge:

```text
Tools/ai/build_code_patch_docs_followup.py
```

Run:

```powershell
python .\Tools\ai\build_code_patch_docs_followup.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\patch_specs\agent_review_code_docs_followup.json `
  --markdown-output .\output\patch_specs\agent_review_code_docs_followup.md
```

The bridge maps code target areas to likely documentation surfaces, for example:

| Code area/path | Candidate docs |
|---|---|
| `Tools/validation/**` | `Tools/validation/README.md`, `docs/JSON_SCHEMAS.md`, `docs/CONTRACT_DRIFT_VALIDATION.md` |
| `Tools/workflow/**` | `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md`, `docs/LOCAL_AI_TASKS/README.md`, `WORKFLOW.md` |
| `Tools/ai/**` | `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md`, `docs/JSON_SCHEMAS.md`, `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` |
| `Tools/npu/**` | `docs/LOCAL_AI_WORKFLOW.md`, `docs/LOCAL_WORKSTATION_TARGET.md`, `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` |

Docs follow-up suggestions remain manual-review-only. They should be reviewed after the related code patch plan is accepted or materially changed.

## Allowed targets

A code patch plan may target source files only when all conditions hold:

```text
file exists, unless the task explicitly authorizes a new source file
file is not under output/**
file is not generated index content
file is not full analysis JSON
file is not a SQLite/database artifact
edit is small and target-specific
validation commands are listed
stop conditions are explicit
```

## Blocked targets

The code patch-plan lane must reject or mark blocked any plan touching:

```text
output/**
*.db
*.sqlite
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
full_analysis*.json
*analysis_full*.json
Blender runtime execution paths without explicit runtime task scope
provider credentials, secrets, billing, permissions or repository visibility
```

## Smoke validator expectations

The smoke validator checks:

```text
kind == agent_review_code_patch_plan
apply_mode == report_only_manual_review_code_patch_plan
manual_review_required == true
provider_execution_performed == false
patch_application_performed == false
source_writes_performed == false
patch_plan_count == len(code_patch_plans)
all target files are allowed or explicitly declared future/new-file candidates
all plans include validation_commands and stop_conditions
no forbidden path appears in target_files or proposed_patch metadata
```

The smoke validator must not:

```text
apply patches
run providers
run Blender
write source files
read ignored output/** reports unless explicitly supplied as input evidence
```

## Evidence bundle integration

The existing evidence bundle builder should summarize code patch-plan and docs follow-up reports in the same compact style used for documentation patch plans.

Recommended code-plan summary fields:

```text
patch_plan_count
manual_review_required
provider_execution_performed
patch_application_performed
source_writes_performed
plans[].id
plans[].area
plans[].risk
plans[].status
plans[].target_files
plans[].rationale
plans[].edit_strategy
plans[].validation_commands
plans[].stop_conditions
```

Recommended code edit proposal summary fields:

```text
id
target_file
edit_kind
manual_review_required
ready_for_manual_review
target_sha256
target_line_count
rationale
edit_strategy
validation_commands
stop_conditions
```

Recommended docs-follow-up summary fields:

```text
docs_followup_count
manual_review_required
provider_execution_performed
patch_application_performed
source_writes_performed
suggestions[].id
suggestions[].source_code_patch_plan_id
suggestions[].target_files
suggestions[].rationale
suggestions[].edit_strategy
```

The bundle may include `proposed_patch` only as a bounded preview. Full raw artifacts should remain local unless they are deliberately small, reviewed and Git-trackable.

## Line-count evidence usage

Use `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv` as a sizing hint before prioritizing code patch plans.

Large files require narrower patch scope. The CSV is useful but may be stale, so always inspect current file content before generating or applying any code patch.

## Guardrails

This lane must remain:

```text
report-only by default
manual-review-only
provider-free unless a separate explicit evidence step already ran
patch-application-free
source-write-free until a human-approved implementation phase
Blender-runtime-free
NPU advisory promotion-free
OpenVINO GPU primary-lane-free
```

## Recommended next implementation sequence

```text
1. Run code_contract_dr
```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-141635.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `12369`
- SHA-256: `507d76d8c92296fbbce768e5624713f191279d8401d805d169584fa4c5c1d286`
- Content included: `True`
- Content truncated: `True`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1773
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
old script legacy/spaziotempo_asset_visual_v6.py,1174
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/ai/run_agent_gpu_deep_planning_review.py,714
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Tools/ai/build_github_evidence_bundle.py,688
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,628
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_selective_execution_plan.py,618
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/build_agent_review_patch_plan.py,562
Tools/ai/build_ai_context_pack.py,558
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/agent_state.py,533
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/ai/run_agent_gpu_deep_planning_supervised.py,478
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/npu/ollama_runtime.py,422
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_code_interpreter_report.py,415
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/run_npu_gpu_deep_review_auditor.py,411
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
Scripting/v61b/encode_image_sequence_v61b.py,395
Scripting/v61b/hotpatch/hero_material_patch.py,395
Scripting/v61b_backgood/hotpatch/hero_material_patch.py,395
Tools/ai/build_agent_review_evidence_sufficiency.py,394
Scripting/v61b/fog_dynamics.py,392
Tools/ai/build_full_context_golden_proposals.py,392
Tools/validation/check_code_contract_drift.py,392
Tools/workflow/gui/components/artifact_browser.py,390
Scripting/v61b_backgood/encode_image_sequence_v61b.py,376
Tools/validation/check_github_evidence_bundle.py,376
indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py,369
Tools/npu/generated_blender_script_candidate.py,369
Tools/npu/generated_blender_script_candidate_FristNear.py,369
Tools/validation/check_repository_change_proposals.py,366
Tools/validation/test_npu_pipeline_helpers.py,359
Scripting/v61b_backgood/config.py,358
Tools/ai/build_local_ai_enrichment_plan.py,357
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,353
Tools/ai/build_agent_review_code_patch_plan.py,351
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/build_music_intermediates.py,314
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/ai/build_analysis_input_bundle.py,305
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/select_semantic_code_chunks.py,291
Tools/validation/check_ai_pipeline_modules.py,290
Scripting/v61b/hotpatch/diagnostics.py,286
Tools/workflow/startup_check.py,284
Tools/ai/build_agent_transient_request_context.py,283
Tools/validation/run_agent_review_patch_plan_smoke.py,283
Tools/workflow/gui/components/session_overview.py,278
Scripting/v61b/render_setup.py,270
Tools/validation/check_full_context_golden_docs_contract.py,270
Scripting/v61b_backgood/render_setup.py,267
Tools/workflow/ai_runtime_diagnostics.py,267
Tools/validation/check_ai_workload_report_quality.py,260
Tools/validation/check_docs_contract_drift.py,259
analyze_wav.py,257
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_patch_docs_followup.py,251
Tools/ai/build_megalithic_review_pr_draft.py,245
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/build_code_edit_proposal_from_plan.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/ai/build_code_patch_artifact_pack.py,239
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/ai/smart_ai_gatekeeper.py,232
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/validation/build_python_line_count_csv.py,221
Tools/workflow/smart_ai_context.py,219
Tools/validation/generated_file_policy.py,217
Tools/ai/code_edit_proposal_helpers.py,215
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py,203
Tools/ai/artifact_domain_registry.py,202
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Tools/ai/code_patch_plan_common.py,199
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/validation/run_agent_review_code_patch_plan_smoke.py,191
Tools/ai/check_npu_provider_environment.py,189
Tools/validation/check_validation_report_contract.py,187
Tools/ai/build_workload_quality_lane_routing.py,186
Tools/workflow/git_auto_push.py,186
Tools/ai/pipeline/remediation.py,185
Tools/validation/check_ai_dry_run_matrix_cases.py,183
Tools/workflow/gui/components/action_panel.py,183
Tools/ai/run_local_provider_probe.py,182
Tools/workflow/gui/components/live_output_panel.py,182
Scripting/v61b_backgood/main_v61b.py,181
Tools/workflow/gui/workflow_gui_with_push.py,181
Scripting/v61b_backgood/world_setup.py,174
Tools/validation/check_generated_blender_script_policy.py,173
Tools/validation/run_code_edit_proposal_smoke.py,164
Scripting/shared/image_sequence.py,161
Tools/npu/npu_runtime.py,160
Scripting/v61b/fog_filaments.py,159
Tools/validation/check_npu_decode_quality_remediation.py,159
Tools/npu/pipeline/__init__.py,157
Tools/ai/pipeline/models.py,152
Scripting/v61b/hotpatch/lighting_patch.py,150
Tools/validation/check_refactor_status_consistency.py,149
Tools/npu/build_runtime_output_manifest.py,148
Tools/npu/build_provider_result_report.py,147
Tools/validation/check_blender_shared_compat_smoke.py,147
Tools/workflow/artifact_consult.py,144
Tools/validation/check_docs_links.py,141
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
Tools/ai/pipeline/schema_report.py,118
Tools/validation/check_package_structure.py,117
Tools/workflow/workflow_shell_with_push.py,117
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
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
Scripting/shared/json_io.py,88
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
Tools/validation/report_utils.py,50
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
Scripting/v61b/spaziotempo/fe
```

### `output/analysis/code_interpreter_report_pr109.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `623938`
- SHA-256: `4e5e0706fb8023bef7e12a84805b836b3cb0248715b8056bf5cfe5379b2abbcb`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "code_interpreter_report",
  "generated_at": "2026-05-02T14:36:25",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_static_code_interpreter",
  "file_count": 123,
  "parsed_file_count": 123,
  "total_lines": 32676,
  "total_functions": 1140,
  "total_classes": 29,
  "total_risk_signals": 12,
  "total_todos": 17,
  "top_imports": [
    {
      "module": "Tools",
      "count": 391
    },
    {
      "module": "__future__",
      "count": 123
    },
    {
      "module": "pathlib",
      "count": 116
    },
    {
      "module": "typing",
      "count": 116
    },
    {
      "module": "argparse",
      "count": 95
    },
    {
      "module": "json",
      "count": 91
    },
    {
      "module": "report_utils",
      "count": 68
    },
    {
      "module": "datetime",
      "count": 54
    },
    {
      "module": "sys",
      "count": 50
    },
    {
      "module": "dataclasses",
      "count": 28
    },
    {
      "module": "agent_state",
      "count": 26
    },
    {
      "module": "re",
      "count": 20
    },
    {
      "module": "models",
      "count": 16
    },
    {
      "module": "artifact_contracts",
      "count": 13
    },
    {
      "module": "pipeline",
      "count": 13
    },
    {
      "module": "subprocess",
      "count": 12
    },
    {
      "module": "os",
      "count": 11
    },
    {
      "module": "defaults",
      "count": 11
    },
    {
      "module": "hashlib",
      "count": 7
    },
    {
      "module": "agent_memory_policy",
      "count": 7
    },
    {
      "module": "concurrent",
      "count": 7
    },
    {
      "module": "time",
      "count": 7
    },
    {
      "module": "ast",
      "count": 5
    },
    {
      "module": "reports",
      "count": 4
    },
    {
      "module": "runner",
      "count": 4
    },
    {
      "module": "compat",
      "count": 4
    },
    {
      "module": "sqlite3",
      "count": 3
    },
    {
      "module": "collections",
      "count": 3
    },
    {
      "module": "importlib",
      "count": 3
    },
    {
      "module": "warnings",
      "count": 2
    },
    {
      "module": "csv",
      "count": 2
    },
    {
      "module": "guardrail_models",
      "count": 2
    },
    {
      "module": "orchestrator",
      "count": 2
    },
    {
      "module": "copy",
      "count": 2
    },
    {
      "module": "string",
      "count": 2
    },
    {
      "module": "ai_pipeline_report_contracts",
      "count": 2
    },
    {
      "module": "unittest",
      "count": 2
    },
    {
      "module": "tempfile",
      "count": 2
    },
    {
      "module": "mimetypes",
      "count": 1
    },
    {
      "module": "math",
      "count": 1
    }
  ],
  "largest_files": [
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_review.py",
      "line_count": 714,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_github_evidence_bundle.py",
      "line_count": 688,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_npu_pipeline_modules.py",
      "line_count": 627,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_selective_execution_plan.py",
      "line_count": 618,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_repository_change_proposals.py",
      "line_count": 582,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_pipeline_dry_run_matrix.py",
      "line_count": 573,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_patch_plan.py",
      "line_count": 562,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_ai_context_pack.py",
      "line_count": 558,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/suggest_repository_updates.py",
      "line_count": 551,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/agent_state.py",
      "line_count": 533,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_megalithic_repo_review.py",
      "line_count": 519,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/ai_pipeline_report_contracts.py",
      "line_count": 497,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_code_patch_plan.py",
      "line_count": 494,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/refine_megalithic_review_signals.py",
      "line_count": 489,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/run_agent_review_patch_plan_full_validation.py",
      "line_count": 487,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/run_agnostic_ai_tools_smoke_matrix.py",
      "line_count": 483,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
      "line_count": 478,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
      "line_count": 471,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_reviewed_patch_specs.py",
      "line_count": 446,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/promote_patch_spec_draft.py",
      "line_count": 442,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_code_interpreter_report.py",
      "line_count": 427,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_ai_context_pack_contract.py",
      "line_count": 425,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_patch_specs_from_proposals.py",
      "line_count": 414,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/run_npu_gpu_deep_review_auditor.py",
      "line_count": 411,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_agnostic_tool_inventory.py",
      "line_count": 408,
      "risk": "medium"
    },
    {
      "path": "Tools/validation/check_patch_spec_drafts.py",
      "line_count": 400,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_dry_run_matrix_evidence_bundle.py",
      "line_count": 398,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_memory_inventory.py",
      "line_count": 397,
      "risk": "medium"
    },
    {
      "path": "Tools/ai/build_agent_review_evidence_sufficiency.py",
      "line_count": 394,
      "risk": "low"
    },
    {
      "path": "Tools/ai/build_full_context_golden_proposals.py",
      "line_count": 392,
      "risk": "medium"
    }
  ],
  "risk_summary": {
    "medium": 67,
    "low": 56
  },
  "recommendation_count": 67,
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
        "git diff --check"
      ]
    },
    {
      "id": "code_static_002",
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
        "git diff --check"
      ]
    },
    {
      "id": "code_static_003",
      "target_file": "Tools/ai/artifact_domain_registry.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\artifact_domain_registry.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_004",
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
        "git diff --check"
      ]
    },
    {
      "id": "code_static_005",
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
        "git diff --check"
      ]
    },
    {
      "id": "code_static_006",
      "target_file": "Tools/ai/build_agent_review_code_patch_plan.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_review_code_patch_plan.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_007",
      "target_file": "Tools/ai/build_agent_review_patch_plan.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "large functions detected",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_agent_review_patch_plan.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_008",
      "target_file": "Tools/ai/build_ai_context_pack.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "complex functions detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_ai_context_pack.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "git diff --check"
      ]
    },
    {
      "id": "code_static_009",
      "target_file": "Tools/ai/build_code_interpreter_report.py",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "reasons": [
        "medium-size Python module",
        "TODO/FIXME markers detected"
      ],
      "recommended_next_layer": "agent_review_code_patch_plan",
      "validation_commands": [
        "python -m py_compile .\\Tools\\ai\\build_code_interpreter_report.py",

```

### `output/patch_specs/agent_review_code_docs_followup_pr109.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `3653`
- SHA-256: `ea916ce3f0893e2f03a67bd7d62849a68cc02202fb281b2086d2e162d59b2f64`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_review_code_docs_followup",
  "generated_at": "2026-05-02T14:16:30",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_manual_review_docs_followup",
  "inputs": {
    "code_patch_plan": "output/patch_specs/agent_review_code_patch_plan_fixture_built.json",
    "code_patch_plan_kind": "agent_review_code_patch_plan",
    "code_patch_plan_count": 1
  },
  "docs_followup_count": 1,
  "docs_followup_suggestions": [
    {
      "id": "docs_followup_001",
      "source_code_patch_plan_id": "code_contract_001",
      "area": "cpu_validation",
      "risk": "medium",
      "status": "candidate_for_manual_review",
      "target_files": [
        "Tools/validation/README.md",
        "docs/JSON_SCHEMAS.md"
      ],
      "missing_candidate_docs": [
        "docs/CONTRACT_DRIFT_VALIDATION.md"
      ],
      "rationale": "Code patch plan `code_contract_001` may change `Tools/validation/check_validation_report_contract.py`; documentation should be reviewed for matching contract, workflow or schema updates.",
      "edit_strategy": "After the code patch is reviewed, update only the affected docs with a narrow cross-reference, schema note, validator command or workflow note. Do not duplicate full contracts and do not apply documentation edits automatically.",
      "validation_commands": [
        "python .\\Tools\\validation\\check_docs_links.py --repo-root . --output .\\output\\validation\\docs_links.json",
        "python .\\Tools\\validation\\check_markdown_command_hygiene.py --repo-root . --output .\\output\\validation\\markdown_command_hygiene.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ],
      "stop_conditions": [
        "Stop if the related code patch is rejected or substantially changed.",
        "Stop if the docs update would touch output/**, generated indexes, full analysis JSON or runtime artifacts.",
        "Stop if documentation validation fails."
      ],
      "manual_review_required": true,
      "source_evidence": {
        "code_patch_plan_id": "code_contract_001",
        "code_target_files": [
          "Tools/validation/check_validation_report_contract.py"
        ],
        "code_rationale": "Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.",
        "code_edit_strategy": "Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation. Current CSV sizing hint: 152 lines; verify current count locally before editing. Do not apply this plan automatically."
      }
    }
  ],
  "decision": {
    "ready_for_manual_docs_review": true,
    "docs_followup_count": 1,
    "manual_review_required": true,
    "recommended_next_layer": "review_docs_followups_after_code_plan"
  },
  "guardrails": {
    "report_only": true,
    "manual_review_required": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "blender_runtime_execution_performed": false,
    "sqlite_write_performed": false,
    "docs_written": false
  }
}

```

### `output/patch_specs/agent_review_code_patch_plan_fixture_built.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `3669`
- SHA-256: `21992b62fce4f830962c7735692b942c1bc370fd11ab4e695ff6c14079d2a78c`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_review_code_patch_plan",
  "generated_at": "2026-05-02T14:16:25",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "apply_mode": "report_only_manual_review_code_patch_plan",
  "inputs": {
    "code_contract_drift_report": "Tools/ai/fixtures/code_contract_drift_fixture.json",
    "line_count_csv": "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv",
    "line_count_csv_loaded": true
  },
  "patch_plan_count": 1,
  "code_patch_plans": [
    {
      "id": "code_contract_001",
      "area": "cpu_validation",
      "risk": "medium",
      "status": "ready_for_manual_review",
      "target_files": [
        "Tools/validation/check_validation_report_contract.py"
      ],
      "rationale": "Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.",
      "edit_strategy": "Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation. Current CSV sizing hint: 152 lines; verify current count locally before editing. Do not apply this plan automatically.",
      "proposed_patch": "",
      "validation_commands": [
        "python -m py_compile .\\Tools\\validation\\check_validation_report_contract.py",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
        "git diff --check"
      ],
      "stop_conditions": [
        "Stop if the target file changed since the drift report was generated.",
        "Stop if the edit requires provider execution, Blender runtime execution, or patch auto-apply.",
        "Stop if the patch touches output/**, generated indexes, full analysis JSON, SQLite, secrets, permissions, billing, or repository visibility.",
        "Stop if local validation fails."
      ],
      "manual_review_required": true,
      "source_evidence": {
        "contract": "fixture_validation_report_contract_manual_review_gate",
        "owner_lane": "cpu_validation",
        "consumed_by_lanes": [
          "cpu"
        ],
        "missing_required_terms": [
          "fixture_manual_review_gate"
        ],
        "missing_recommended_terms": [
          "manual_review_required"
        ],
        "errors": [
          "missing required term: fixture_manual_review_gate"
        ],
        "warnings": [
          "missing recommended term: manual_review_required"
        ],
        "line_count_csv_hint": 152
      }
    }
  ],
  "skipped_candidate_count": 0,
  "skipped_candidates": [],
  "decision": {
    "ready_for_manual_review": true,
    "patch_plan_count": 1,
    "manual_review_required": true,
    "recommended_next_layer": "manual_review_then_targeted_code_pr"
  },
  "guardrails": {
    "report_only": true,
    "manual_review_required": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "blender_runtime_execution_performed": false,
    "sqlite_write_performed": false,
    "npu_primary_advisory": false,
    "openvino_gpu_primary_lane": false
  }
}

```

### `output/validation/code_patch_artifact_pack_pr109.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1306`
- SHA-256: `2fbe5bdada8605b5fac3a1d9be86cbdf763adbdeccb429c321f0bc8798d3af09`
- Content included: `True`
- Content truncated: `False`

```text
# Code Patch Artifact Pack

- Passed: `True`
- Apply mode: `report_only_compact_code_patch_artifact_pack`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Code patch plan count: `1`
- Docs follow-up count: `1`

## Code patch plans

### `code_contract_001`
- Area: `cpu_validation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: `['Tools/validation/check_validation_report_contract.py']`
- Rationale: Contract drift check `fixture_validation_report_contract_manual_review_gate` reported a code-review candidate. Missing required terms: `fixture_manual_review_gate`. Missing recommended terms: `manual_review_required`.

## Docs follow-up suggestions

### `docs_followup_001`
- Source code plan: `code_contract_001`
- Area: `cpu_validation`
- Risk: `medium`
- Status: `candidate_for_manual_review`
- Target files: `['Tools/validation/README.md', 'docs/JSON_SCHEMAS.md']`
- Rationale: Code patch plan `code_contract_001` may change `Tools/validation/check_validation_report_contract.py`; documentation should be reviewed for matching contract, workflow or schema updates.

## Guardrail

This pack is compact evidence only. It is not a patch apply queue.

```

### `output/validation/python_line_count_pr109.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1704`
- SHA-256: `d03cefe79424175b45e05f6724a6f9b713d15b652a4bd572066391b1ea23fd5b`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-141635.csv`
- File count: `265`
- Total lines: `75396`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest Python files

- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines
- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines
- `old script legacy/spaziotempo_asset_visual_v61.py` — `1513` lines
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines
- `Tools/workflow/workflow_state.py` — `1230` lines
- `old script legacy/spaziotempo_asset_visual_v6.py` — `1174` lines
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines
- `Scripting/v61b/animation.py` — `1079` lines
- `Scripting/v61b_backgood/animation.py` — `1019` lines
- `old script legacy/spaziotempo_album_visual_v5.py` — `969` lines
- `Tools/workflow/gui/workflow_gui.py` — `738` lines
- `Scripting/v61b/physics_setup.py` — `737` lines
- `Scripting/v61b/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/physics_setup.py` — `720` lines
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `714` lines
- `Tools/npu/build_music_context.py` — `711` lines
- `old script legacy/spaziotempo_album_visual_v3.py` — `710` lines
- `Tools/ai/build_github_evidence_bundle.py` — `688` lines
- `Scripting/v61b/materials.py` — `657` lines

## Guardrail

This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.

```

### `Tools/ai/fixtures/code_contract_drift_fixture.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `2410`
- SHA-256: `499dbe08231e1622a709a52a9d8db33d117cbe1041fdc8650f32e242a6a4ebb6`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "code_contract_drift",
  "repo_root": ".",
  "passed": false,
  "errors": [
    "Tools/validation/check_validation_report_contract.py: missing required term: fixture_manual_review_gate"
  ],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_manual_review_only",
  "drift_count": 1,
  "lane_policy": {
    "cpu": "validators and contract analyzers run here by default"
  },
  "checks": [
    {
      "path": "Tools/validation/check_validation_report_contract.py",
      "contract": "fixture_validation_report_contract_manual_review_gate",
      "owner_lane": "cpu_validation",
      "consumed_by_lanes": [
        "cpu"
      ],
      "exists": true,
      "ok": false,
      "required_term_count": 1,
      "recommended_term_count": 1,
      "missing_required_terms": [
        "fixture_manual_review_gate"
      ],
      "missing_recommended_terms": [
        "manual_review_required"
      ],
      "forbidden_terms_present": [],
      "forbidden_global_terms_present": [],
      "allowed_global_forbidden_terms_present": [],
      "errors": [
        "missing required term: fixture_manual_review_gate"
      ],
      "warnings": [
        "missing recommended term: manual_review_required"
      ],
      "safe_actions": [
        {
          "path": "Tools/validation/check_validation_report_contract.py",
          "operation": "manual_code_patch_suggestion",
          "apply_mode": "manual_review_only",
          "owner_lane": "cpu_validation",
          "hint": "Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation."
        }
      ]
    }
  ],
  "safe_actions": [
    {
      "path": "Tools/validation/check_validation_report_contract.py",
      "operation": "manual_code_patch_suggestion",
      "apply_mode": "manual_review_only",
      "owner_lane": "cpu_validation",
      "hint": "Fixture-only suggestion. Do not apply; validate report-only code patch-plan generation."
    }
  ],
  "guardrails": {
    "code_report_only": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "blender_runtime_touched": false,
    "full_analysis_json_touched": false,
    "sqlite_db_touched": false,
    "npu_promoted_to_advisory": false,
    "openvino_gpu_primary_lane": false
  }
}

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
