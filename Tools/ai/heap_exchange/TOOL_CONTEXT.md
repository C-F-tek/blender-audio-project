# Tools/ai/heap_exchange context

## Role

`Tools/ai/heap_exchange` contains helpers around heap exchange lifecycle, wiring patches and runtime exchange artifacts.

## Responsibilities

- Support heap exchange lifecycle wiring.
- Build or patch exchange-related reports where explicitly scoped.
- Keep exchange output linked to runtime state and validation artifacts.

## Representative commands

Use through the AI dispatcher when registered:

```powershell
python -m Tools.ai <tool> [args...]
```

Known package examples include:

```text
Tools/ai/heap_exchange/unified_lifecycle_wiring_patch
```

## Output role

Outputs from this area are exchange/lifecycle support artifacts. They help the runtime universe describe what happened across a run.

## Notes

- Heap exchange support is not a substitute for heap runtime state.
- Keep generated exchange artifacts out of Git unless selected as compact evidence.
- Inspect `Tools/ai/dispatch.py` before assuming a package is public CLI surface.
