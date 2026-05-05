# LightFull0To10 launcher flag

## Scopo

Il launcher unico espone il profilo leggero evidence-only tramite:

```powershell
-LightFull0To10
```

## Comando

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . `
  -LightFull0To10 `
  -LightFull0To10OutputDir .\output\validation\launcher_light_full0to10 `
  -LightFull0To10NoExternalProbes
```

## Guardrail

Il profilo light resta evidence-only:

- provider generation non eseguita;
- patch apply non eseguito;
- Blender non eseguito;
- FFmpeg non eseguito.

## Nota

Non cancellare Markdown in lavorazione durante questa fase.
