# Tools/validation/code_product context

## Role

`Tools/validation/code_product` contains checks for code-product intake and related product-artifact behavior.

## Responsibilities

- Validate code-product artifact intake reports.
- Check section classification behavior.
- Check no-op, already-integrated and manual-review states.
- Keep code-product validation separate from runtime/provider reports.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_code_product_artifact_intake_smoke ...
```

## Output role

Outputs are validation reports. They prove only the code-product intake behavior under test.

## Notes

- Keep fixture inputs small and explicit.
- Do not treat provider prose as code-product evidence.
- Add new checks here when code-product parser or classifier behavior changes.
