# Tools/git/_powershell context

## Role

`Tools/git/_powershell` contains Git-related PowerShell wrappers exposed through `python -m Tools.git`.

## Public commands

Registered by `Tools/git/dispatch.py`:

```powershell
python -m Tools.git auto_push_generated_artifacts ...
python -m Tools.git auto_push_generated_data ...
```

## Boundaries

- Treat these as explicit operator Git helpers.
- Do not use them as default commit/push behavior.
- Prefer manual `git add <specific files>` for normal repository work.
- Never use `git add .` for IA-Carmine generated artifacts.

## Notes

Generated/runtime outputs should remain out of Git unless a compact evidence artifact is explicitly selected.