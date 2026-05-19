# Tools/validation/real_product context

## Role

`Tools/validation/real_product` contains checks for real-product run contracts, preflight gates, runtime mesh contracts and product boundary behavior.

## Responsibilities

- Validate real-product preflight reports.
- Validate runtime mesh contract reports.
- Validate live-provider gate reports.
- Validate single entry/exit behavior.
- Validate full run bundle completeness.

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
```

## Output role

Outputs are validation reports for real-product run readiness and contract shape.

## Notes

- A preflight pass is not the same as a finished product.
- Keep runtime mesh evidence explicit.
- Add checks here when real-product entry/exit contracts change.
