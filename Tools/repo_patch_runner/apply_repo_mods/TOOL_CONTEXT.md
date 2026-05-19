# Tools/repo_patch_runner/apply_repo_mods context

## Role

`Tools/repo_patch_runner/apply_repo_mods` contains the packaged repository modification runner exposed by `Tools/repo_patch_runner/dispatch.py`.

## Public command

```powershell
python -m Tools.repo_patch_runner apply_repo_mods ...
```

## Boundaries

- Use only when repository modifications are explicitly intended.
- Validate expected files and working tree state before use.
- Do not use as a general-purpose shell runner.
- Keep generated/runtime artifacts out of Git unless they are compact evidence selected for versioning.

## Notes

This package is a controlled modification runner. It must remain separate from documentation-only context passes and mapping procedures.