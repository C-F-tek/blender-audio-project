# Tools/ai/deterministic_recommendations context

## Role

`Tools/ai/deterministic_recommendations` contains deterministic recommendation builders that turn evidence into structured recommendation reports.

## Responsibilities

- Build deterministic recommendation reports.
- Convert evidence into recommendation candidates.
- Keep recommendation output separate from source edits and final products.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai deterministic_recommendations ...
python -m Tools.ai evidence_to_recommendation ...
```

## Output role

Outputs are deterministic recommendation artifacts. They can guide later review and product steps, but do not apply changes by themselves.

## Notes

- Recommendations are evidence/planning artifacts.
- Validate recommendation behavior under `Tools/validation/deterministic_recommendations` when schema or ranking changes.
- Inspect current source and dispatcher before using old recommendation reports.
