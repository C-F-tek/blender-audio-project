# AI Pipeline Report Contracts

## Status

active

## Goal

Add deterministic, local validation for AI pipeline report contracts so `dry_run_matrix_report.json` and per-case `ai_pipeline_dry_run_report.json` files enforce the existing schema-v6 field meanings without changing runtime behavior.

## Scope

```text
Tools/validation/
Tools/workflow/run_local_validation_after_refactor.ps1
docs/
```

## Out of scope

```text
Ready To Jazz runtime migration
Blender runtime package changes
Scripting/shared/blender_compat.py adoption
full frame-level analysis JSON edits
third-party schema dependencies
changing existing schema-v6 field meanings
```

## Files likely touched

```text
Tools/validation/ai_pipeline_report_contracts.py
Tools/validation/check_ai_pipeline_report_contract.py
Tools/validation/check_ai_dry_run_matrix_contract.py
Tools/validation/check_ai_pipeline_modules.py
Tools/validation/README.md
Tools/workflow/run_local_validation_after_refactor.ps1
docs/AI_ARTIFACT_SCHEMAS.md
docs/JSON_SCHEMAS.md
docs/QUALITY_GATE.md
```

## Validation commands

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 12 --repeat-cases 1
python .\Tools\validation\check_ai_pipeline_report_contract.py --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_outputs.py --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output .\output\validation\json_artifacts.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
```

## Risk level

medium

The risk is schema over-tightening. Mitigation: preserve unknown future fields, keep optional extension checks warning-friendly where practical, and validate only already generated reports.

## Progress log

- 2026-04-30: Started after PR #37 merged; scope limited to core validation/report contracts.
- 2026-04-30: Added reusable schema-v6 report contract helper and a direct `check_ai_pipeline_report_contract.py` validator.
- 2026-04-30: Wired matrix contract validation to validate referenced per-case dry-run reports.
- 2026-04-30: Local runner passed with `-MatrixWorkers 12 -RepeatCases 2`; 23 validation steps passed and 80 dry-run cases were checked.

## Result

implemented and locally validated

## Follow-up

After this contract layer is stable, continue with NPU pipeline decomposition before any Ready To Jazz or `blender_compat.py` adoption work.
