# Tools/validation/generated_artifacts context

## Role

`Tools/validation/generated_artifacts` contains checks for generated Python, generated Blender scripts and generated artifact path policy.

## Responsibilities

- Check generated artifact paths.
- Check generated Python policy.
- Check generated Blender script policy.
- Keep generated source/material separate from maintained source.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_generated_artifact_path_policy ...
python -m Tools.validation check_generated_python_policy ...
python -m Tools.validation check_generated_blender_script_policy ...
```

## Output role

Outputs are validation reports for generated artifact policy.

## Notes

- Generated artifacts are not automatically maintained source.
- Keep media/render outputs outside Git by default.
- Add checks here when generated artifact policy changes.
