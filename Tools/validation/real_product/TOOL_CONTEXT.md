# Tools/validation/real_product context

## Role

`Tools/validation/real_product` contains checks for real-product run contracts, preflight gates, runtime mesh contracts, live-provider gates, bundle completeness and product boundary behavior.

Validation commands are downstream verification commands. They are not product
entrypoints. A complete provider smoke must be invoked only as downstream
verification, not as the first action of a product run.

It validates the output side of:

```text
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Validate real-product preflight reports.
- Validate runtime mesh contract reports.
- Validate live-provider gate reports.
- Validate single entry/exit behavior.
- Validate full run bundle completeness.
- Distinguish evidence-only run, blocked product run and real product run.
- Ensure provider/tool evidence does not bypass product requirements.
- Block complete-provider smoke when it is used as a standalone entry command.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_real_product_preflight_gate ...
python -m Tools.validation run_real_product_preflight_gate_smoke ...
python -m Tools.validation check_real_product_runtime_mesh_contract ...
python -m Tools.validation run_real_product_runtime_mesh_contract_smoke ...
python -m Tools.validation check_real_product_live_provider_gate ...
python -m Tools.validation run_real_product_single_entry_exit_smoke ...
python -m Tools.validation check_full_run_bundle_completeness ...
python -m Tools.validation check_real_product_intrinsic_capability_contract ...
python -m Tools.validation run_real_product_intrinsic_capability_contract_smoke ...
```

## Output role

Outputs are validation reports for real-product run readiness and contract shape.

They must help classify final state as one of:

```text
evidence-only
blocked product
real product
```

## Product gate semantics

A run is not a real product merely because it has:

```text
preflight passed
provider output
runtime report
bundle ZIP
compact evidence
readable summary
```

A real product requires:

```text
concrete operation
source target or explicit no-op/non-applicable state
code/patch product when source change is expected
validation path
reviewable artifact
blocked reason if no product exists
```

## Boundary rules

- A preflight pass is not the same as a finished product.
- A full bundle is not automatically a product.
- Runtime mesh evidence must remain explicit.
- Provider agreement does not satisfy product readiness.
- Empty/metadata-only patch specs must be classified as non-product or blocked.
- Source writes must be reported separately from generated report writes.

## Expected artifacts

```text
real product preflight report
runtime mesh contract report
live provider gate report
single entry/exit smoke report
full run bundle completeness report
intrinsic capability contract report
blocked/product classification evidence
```

## Notes

Add checks here when real-product entry/exit contracts, bundle completeness, live-provider gates or product classification rules change.
