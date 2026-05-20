# Tools/validation/code_product context

## Role

`Tools/validation/code_product` contains checks for code-product intake and related product-artifact behavior.

It validates code-product state classification described by:

```text
Tools/ai/code_product/TOOL_CONTEXT.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Validate code-product artifact intake reports.
- Check section classification behavior.
- Check real diff/code detection.
- Check no-op, already-integrated and manual-review states.
- Check empty product and non-applicable states.
- Keep code-product validation separate from runtime/provider reports.
- Keep full-run bundle ZIP classification separate from apply-ready code-product classification.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_code_product_artifact_intake_smoke ...
python -m Tools.validation run_generated_patch_specs_empty_product_smoke ...
```

Related product-readiness checks:

```powershell
python -m Tools.validation check_review_pr_final_product_contract ...
python -m Tools.validation check_review_pr_product_readiness ...
```

## Output role

Outputs are validation reports. They prove only the code-product intake/classification behavior under test.

They should help classify code-product sections as:

```text
real diff/code present
already integrated
verified target with no diff / evidence-only
empty no-op / non-applicable
missing or truncated payload
manual-review
blocked
```

## Boundary checks

Code-product validation should block or flag:

```text
provider prose treated as code product
bundle ZIP treated as apply-ready product by itself
metadata-only section treated as patch
empty product without explicit no-op/non-applicable state
truncated payload treated as safe-applicable
source writes not reported accurately
```

## Notes

- Keep fixture inputs small and explicit.
- Do not treat provider prose as code-product evidence.
- Do not treat full-run bundle ZIP existence as product success.
- Add new checks here when code-product parser or classifier behavior changes.
- Update `Tools/ai/code_product/TOOL_CONTEXT.md` and `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` when semantic meaning changes.