# Tools/validation/heap_provider context

## Role

`Tools/validation/heap_provider` contains checks for heap-provider behavior such as provider budget governance and provider-related runtime contracts.

## Responsibilities

- Validate provider budget governor behavior.
- Check provider/runtime readiness contracts when scoped to heap execution.
- Keep provider checks separate from final product applicability.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_provider_budget_governor_smoke ...
```

Known package examples include:

```text
Tools/validation/heap_provider/budget_governor_smoke
```

## Output role

Outputs are validation reports for heap-provider contract behavior.

## Notes

- Provider readiness is evidence, not final product success.
- Add checks here when heap-provider budget or lifecycle rules change.
- Inspect `Tools/validation/dispatch.py` before assuming public command names.
