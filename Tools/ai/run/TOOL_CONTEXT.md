# Tools/ai/run context

## Role

`Tools/ai/run` is the canonical packaged entrypoint for IA-Carmine AI runs.

It is the public command surface behind:

```powershell
python -m Tools.ai run ...
```

## Responsibilities

- Accept operator run profiles and request files.
- Route execution into the maintained AI runtime packages.
- Keep the public run command stable while internal packages evolve.
- Preserve clear separation between command construction, runtime execution and final product artifacts.

## Output role

Outputs depend on the selected profile. They may include runtime reports, final readable products, code-product artifacts and validation references.

## Notes

- A command preview is not a completed run.
- A completed run requires output artifacts and return codes.
- Do not commit raw `output/**` from a run by default.
- Inspect `Tools/ai/dispatch.py` and this package before changing the public run surface.
