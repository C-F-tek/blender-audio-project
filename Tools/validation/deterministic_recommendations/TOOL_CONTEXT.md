# Tools/validation/deterministic_recommendations context

## Role

`Tools/validation/deterministic_recommendations` contains checks for deterministic recommendation synthesis and related recommendation evidence.

## Responsibilities

- Validate deterministic recommendation synthesizer behavior.
- Check recommendation reports for expected structure.
- Keep recommendation output separate from direct source changes.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_deterministic_recommendation_synthesizer_smoke ...
```

## Output role

Outputs are validation reports for recommendation-generation behavior.

## Notes

- Recommendations are planning/evidence artifacts.
- Source changes should still pass through code-product or patch-product paths.
- Add checks here when recommendation schema or ranking behavior changes.
