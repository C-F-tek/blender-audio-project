# Tools/validation/schema_repair context

## Role

`Tools/validation/schema_repair` contains smoke checks for schema repair and retry flows.

## Responsibilities

- Validate schema repair context behavior.
- Validate schema repair retry behavior.
- Validate retry bootstrap behavior.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_schema_repair_context_smoke ...
python -m Tools.validation run_schema_repair_retry_smoke ...
python -m Tools.validation run_schema_repair_retry_bootstrap_smoke ...
```

## Output role

Outputs are validation reports for schema-repair contracts.

## Notes

- Schema repair validation checks recovery behavior, not final product correctness.
- Add checks here when schema repair rules change.
