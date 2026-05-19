# Tools/validation/pipeline context

## Role

`Tools/validation/pipeline` contains checks for AI pipeline modules, dry-run matrix contracts, output contracts, report schemas and local adapter manifests.

## Responsibilities

- Validate AI pipeline module presence and contracts.
- Validate dry-run matrix cases, outputs and evidence bundles.
- Validate pipeline report contracts.
- Validate local AI adapter manifests.
- Validate NPU pipeline helper modules and docs.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_ai_pipeline_modules ...
python -m Tools.validation check_ai_pipeline_report_contract ...
python -m Tools.validation check_ai_dry_run_matrix_cases ...
python -m Tools.validation check_ai_dry_run_matrix_contract ...
python -m Tools.validation check_ai_dry_run_matrix_outputs ...
python -m Tools.validation check_dry_run_matrix_evidence_bundle ...
python -m Tools.validation check_local_ai_adapter_manifest ...
python -m Tools.validation npu_pipeline_modules_check ...
```

## Output role

Outputs are validation reports for pipeline contracts and dry-run matrix behavior.

## Notes

- Pipeline validation should be deterministic.
- Dry-run matrix reports are evidence, not final product by themselves.
- Add checks here when pipeline schemas or matrix behavior changes.
