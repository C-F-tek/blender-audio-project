# Tools/validation/patch_product context

## Role

`Tools/validation/patch_product` contains checks for patch-product reports, PatchKit bundle contracts, patch suggestion products and code edit proposal behavior.

## Responsibilities

- Validate PatchKit bundle shape.
- Validate patch suggestion product separation.
- Validate patch candidate synthesis reports.
- Validate code edit proposal smokes.
- Validate patch suggestion bundle apply fixtures.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_patch_candidate_synthesis_smoke ...
python -m Tools.validation run_patchkit_smoke ...
python -m Tools.validation run_patchkit_bundle_contract_smoke ...
python -m Tools.validation check_patchkit_bundle_contract ...
python -m Tools.validation check_patch_suggestion_product_separation ...
python -m Tools.validation run_code_edit_proposal_smoke ...
```

## Output role

Outputs are validation reports for patch-product contracts and fixture behavior.

## Notes

- Keep patch-product validation separate from source editing.
- Prefer fixture-based checks.
- Add checks here when patch-product schema or classification changes.
