# Dry-Run Matrix Evidence Bundle

## Status

completed

## Goal

Make the AI pipeline dry-run matrix reviewable from GitHub by producing a compact, Git-trackable evidence bundle and a focused validator for that evidence.

## Scope

- Add a report-only evidence builder for `output/ai_pipeline/dry_run_matrix_report.json`.
- Add a validator for the compact dry-run matrix evidence bundle.
- Run the dry-run matrix locally with parallel workers and repeated cases if the runner remains stable.
- Document the new evidence contract and validation commands.
- Close the pending local-validation note in the dry-run matrix execution plan if validation passes.

## Out of scope

- No Blender runtime changes.
- No Ready To Jazz edits.
- No `Scripting/shared/blender_compat.py` adoption.
- No provider execution.
- No GPU/NPU workloads beyond dry-run planning metadata.
- No prompt prose, model, temperature or provider policy changes.
- No generated index hand-edits.

## Files likely touched

```text
ia_carmine/product/pipeline/dry_run_matrix/evidence_cli.py
Tools/validation/pipeline/dry_run_matrix_evidence_bundle/cli.py
Tools/validation/README.md
docs/AI_ARTIFACT_SCHEMAS.md
docs/JSON_SCHEMAS.md
docs/LOCAL_AI_WORKFLOW.md
docs/LOCAL_VALIDATION_EVIDENCE/
docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md
```

## Validation commands

```powershell
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json
python -m Tools.validation check_ai_dry_run_matrix_cases --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
python -m ia_carmine.cli pipeline_dry_run_matrix --repo-root . --continue-on-error --matrix-workers 12 --repeat-cases 2
python -m Tools.validation check_ai_dry_run_matrix_contract --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python -m Tools.validation check_ai_dry_run_matrix_outputs --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
python -m ia_carmine.cli build_dry_run_matrix_evidence_bundle --repo-root . --basename ai_pipeline_dry_run_matrix_evidence
python -m Tools.validation check_dry_run_matrix_evidence_bundle --repo-root . --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\ai_pipeline_dry_run_matrix_evidence.json --output .\output\validation\dry_run_matrix_evidence_bundle.json
python -m Tools.validation check_json_artifacts --repo-root . --output .\output\validation\json_artifacts.json
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.validation check_execution_plan_status --repo-root . --output .\output\validation\execution_plan_status.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
```

## Risk level

medium

## Progress log

- 2026-05-01: Started from the external technical assessment recommendation to add dry-run matrix evidence.
- 2026-05-01: Added the dry-run matrix evidence builder, focused evidence validator, schema documentation and tracked evidence bundle.
- 2026-05-01: Ran the dry-run matrix locally with 12 workers and 2 repeats. The matrix produced 80 dry-run cases, all planned-only and passing.

## Future task notes

- Selective execution planning from context packs can later consume this evidence to choose safer next validation commands.
- Provider execution evidence remains separate and must keep using explicit GPU/NPU workflows.

## Result

Completed. The dry-run matrix is now reviewable from GitHub through:

```text
docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.md
```

The evidence confirms:

```text
case_count: 80
matrix_workers: 12
repeat_cases: 2
provider_execution_performed: false
gpu_npu_workloads_executed: false
all_cases_dry_run: true
all_steps_planned_only: true
```

The new validator report path is:

```text
output/validation/dry_run_matrix_evidence_bundle.json
```

## Follow-up

If this passes, use the evidence pattern for selective execution planner reports.
