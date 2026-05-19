# Tools/ai/heap_provider context

## Role

`Tools/ai/heap_provider` contains provider-side heap execution helpers such as budget governance and invocation contracts.

## Responsibilities

- Build provider budget-governor reports.
- Build provider invocation contract reports.
- Keep provider lifecycle evidence separate from final product assembly.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai heap_provider_budget_governor ...
python -m Tools.ai heap_provider_invocation_contract ...
```

## Output role

Outputs are heap-provider governance and contract artifacts.

## Notes

- Provider governance does not prove product success.
- Validation belongs under `Tools/validation/heap_provider` when behavior changes.
- Inspect dispatcher/source before changing provider lifecycle behavior.
