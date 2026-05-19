# Tools/validation/generated_patch_specs context

## Role

`Tools/validation/generated_patch_specs` contains checks for generated patch spec drafts, reviewed specs, empty products and review-lane behavior.

## Responsibilities

- Validate generated patch spec drafts.
- Validate reviewed patch spec reports.
- Check empty generated-product behavior.
- Check current-stamp discovery for generated specs.
- Check review-lane behavior for generated specs.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_patch_spec_drafts ...
python -m Tools.validation reviewed_patch_specs_check ...
python -m Tools.validation run_generated_patch_specs_empty_product_smoke ...
python -m Tools.validation run_generated_patch_specs_current_stamp_discovery_smoke ...
python -m Tools.validation run_generated_patch_specs_review_pr_lane_smoke ...
```

## Output role

Outputs are validation reports for generated spec shape, status and review readiness.

## Notes

- Keep spec validation deterministic.
- Empty/non-applicable products must be explicit.
- Add checks here when generated spec fields or lifecycle rules change.
