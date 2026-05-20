# Tools/validation/patch_product context

## Role

`Tools/validation/patch_product` contains checks for patch-product reports, PatchKit bundle contracts, patch suggestion products, patch candidate synthesis and code edit proposal behavior.

It validates the patch/source-write boundary described by:

```text
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
Tools/ai/patch_product/TOOL_CONTEXT.md
Tools/ai/patchkit/TOOL_CONTEXT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Validate PatchKit bundle shape.
- Validate PatchKit dry-run/apply fixture behavior.
- Validate patch suggestion product separation.
- Validate patch candidate synthesis reports.
- Validate code edit proposal smokes.
- Validate patch suggestion bundle apply fixtures.
- Ensure provider prose and patch plans do not become apply-ready products.
- Preserve blocked/manual-review state when payloads are missing, truncated, ambiguous or path-invalid.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_patch_candidate_synthesis_smoke ...
python -m Tools.validation run_patchkit_smoke ...
python -m Tools.validation run_patchkit_bundle_contract_smoke ...
python -m Tools.validation check_patchkit_bundle_contract ...
python -m Tools.validation check_patch_suggestion_product_separation ...
python -m Tools.validation run_patch_suggestion_bundle_apply_smoke ...
python -m Tools.validation run_task_patch_suggestion_markdown_authoring_smoke ...
python -m Tools.validation run_task_patch_suggestion_runtime_deferral_smoke ...
python -m Tools.validation run_code_edit_proposal_smoke ...
```

## Output role

Outputs are validation reports for patch-product contracts and fixture behavior.

They should classify artifacts as:

```text
evidence-only
patch plan
patch candidate
PatchKit bundle
fixture apply result
blocked/manual-review
```

## Boundary checks

Patch-product validation should block or flag:

```text
provider prose treated as patch
metadata-only patch spec treated as product
patch plan without concrete diff/code treated as apply-ready
unknown or invented target path
truncated payload
manual-review item with no payload
source write without explicit apply boundary
```

## Notes

- Keep patch-product validation separate from source editing.
- Prefer fixture-based checks.
- A passing fixture smoke proves only the checked contract, not real repo applicability.
- Add checks here when patch-product schema, PatchKit bundle contract or classification changes.
- Update `docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md` and `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` when semantic meaning changes.