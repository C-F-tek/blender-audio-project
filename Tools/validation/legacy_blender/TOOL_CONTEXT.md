# Tools/validation/legacy_blender context

## Role

`Tools/validation/legacy_blender` contains compatibility checks for legacy Blender/shared scripting surfaces.

## Responsibilities

- Validate Blender shared compatibility smoke behavior.
- Keep legacy Blender compatibility checks separate from runtime Blender execution.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_blender_shared_compat_smoke ...
```

## Output role

Outputs are compatibility validation reports.

## Notes

- This package validates compatibility; it does not run production rendering.
- Blender runtime should only be executed when explicitly requested by the operator.
