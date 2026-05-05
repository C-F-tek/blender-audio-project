# Quality stack preflight

Lo stack preflight produce qualità utile prima della run reale.

## Produce

- hardware/tool capability;
- runtime tool registry;
- quality gate;
- stack summary.

## Non produce

- provider generation;
- patch application;
- persistent DB write;
- media/render output.

## Uso

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_full0to10_quality_stack_preflight.ps1 `
  -RepoRoot . `
  -OutputDir .\output\validation\full0to10_quality_stack_preflight `
  -PatchSpecs .\output\validation\full0to10_auto_refactor_plan\full0to10_auto_refactor_patch_specs.json `
  -NoExternalProbes
```

Il report finale decide se siamo vicini alla run reale.
