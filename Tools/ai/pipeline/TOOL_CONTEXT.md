# Tools/ai/pipeline context

## Role

`Tools/ai/pipeline` contains AI pipeline helpers and package material used by local AI workflows.

## Responsibilities

- Keep pipeline-specific helpers and documentation near the package.
- Support local AI pipeline stages when invoked through registered tools.
- Keep pipeline artifacts separate from final code-product artifacts.

## Representative source

```text
Tools/ai/pipeline/README.md
```

Use public tools only through the dispatcher:

```powershell
python -m Tools.ai <tool> [args...]
```

## Output role

Outputs from this area are pipeline evidence or intermediate pipeline artifacts. They are not source patches by themselves.

## Notes

- Inspect `Tools/ai/dispatch.py` before assuming a package is public surface.
- Keep raw output under ignored runtime folders unless selected as compact evidence.
- Add validation under `Tools/validation/pipeline` when pipeline contracts change.
