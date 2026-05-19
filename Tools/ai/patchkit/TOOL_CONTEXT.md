# Tools/ai/patchkit context

## Role

`Tools/ai/patchkit` contains controlled PatchKit helpers used when a reviewed patch bundle/spec needs a deterministic application path.

## Responsibilities

- Provide the packaged PatchKit apply command surface.
- Keep patch bundle handling deterministic and reviewable.
- Keep generated patch bundles separate from raw runtime output.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai apply_patch_bundle ...
```

## Output role

Outputs are PatchKit execution reports or local apply artifacts, depending on command options and fixture/worktree scope.

## Notes

- PatchKit is not a provider proposal generator.
- Do not use PatchKit to bypass review.
- Keep generated bundle artifacts out of Git unless explicitly selected as compact evidence.
- Validate PatchKit behavior under `Tools/validation/patch_product`.
