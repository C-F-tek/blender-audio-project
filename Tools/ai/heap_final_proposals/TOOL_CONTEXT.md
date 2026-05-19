# Tools/ai/heap_final_proposals context

## Role

`Tools/ai/heap_final_proposals` contains helpers for final heap proposal artifacts and final-causality normalization.

## Responsibilities

- Build final heap proposal reports.
- Normalize final proposal causality where required.
- Keep final proposal artifacts linked to prior heap/runtime evidence.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai heap_final_proposals ...
python -m Tools.ai normalize_heap_final_causality ...
```

## Output role

Outputs are proposal/finality artifacts. They help downstream product assembly and review.

## Notes

- Final proposal artifacts are not source changes by themselves.
- Keep causality links explicit and traceable.
- Inspect heap/runtime artifacts before relying on a final proposal report.
