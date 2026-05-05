# Controlled applier

L'applier Full0To10 accetta patch-spec JSON e applica solo kind allowlistati.

## Default

Dry-run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_full0to10_auto_refactor_apply.ps1 `
  -RepoRoot . `
  -PatchSpecs .\output\validation\full0to10_auto_refactor_plan\full0to10_auto_refactor_patch_specs.json
```

## Apply

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_full0to10_auto_refactor_apply.ps1 `
  -RepoRoot . `
  -PatchSpecs .\output\validation\full0to10_auto_refactor_plan\full0to10_auto_refactor_patch_specs.json `
  -Apply
```

## Non supportato automaticamente

- delete;
- rename;
- Markdown split;
- code split;
- GPU/NPU runtime mutation.
