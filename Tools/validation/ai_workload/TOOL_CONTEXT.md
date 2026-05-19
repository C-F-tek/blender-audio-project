# Tools/validation/ai_workload context

## Role

`Tools/validation/ai_workload` contains checks for AI workload quality reports and lane-routing quality artifacts.

## Responsibilities

- Validate workload quality report shape.
- Validate stamp-scoped workload reports.
- Validate workload report directories.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_ai_workload_report_quality ...
python -m Tools.validation run_ai_workload_quality_report_dir_smoke ...
python -m Tools.validation run_ai_workload_report_quality_stamp_scoped_smoke ...
```

## Output role

Outputs are validation reports for workload-quality artifacts.

## Notes

- Workload quality is routing/planning evidence, not provider execution.
- Add checks here when workload quality schema changes.
