# Tools/validation/repository_product context

## Role

`Tools/validation/repository_product` contains checks for repository product reports, review preparation artifacts and GitHub evidence bundles.

## Responsibilities

- Validate repository consistency reports.
- Validate repository change proposal reports.
- Validate review preparation and readiness reports.
- Validate GitHub evidence bundle reports.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_github_evidence_bundle ...
python -m Tools.validation check_repository_change_proposals ...
python -m Tools.validation check_review_pr_product_readiness ...
python -m Tools.validation run_repository_consistency_map_smoke ...
python -m Tools.validation run_review_pr_prepare_args_smoke ...
```

## Output role

Outputs are validation reports for repository-product artifacts.

## Notes

- Repository product validation is evidence validation, not final source modification.
- Add checks here when repository-product schemas change.
