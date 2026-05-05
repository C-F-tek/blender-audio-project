# Quality supervisor integration

Il quality supervisor collega lo stack qualità al flusso Full0To10.

## Sequenza

```text
preflight quality stack
-> optional unified Full0To10 supervisor
-> final quality stack
```

## Entry point

```text
Tools/workflow/run_unified_full0to10_quality_supervisor.ps1
```

## Modalità sicura

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_full0to10_quality_supervisor.ps1 `
  -RepoRoot . `
  -SkipLauncher `
  -NoExternalProbes
```

## Regola

Finché il quality stack non è pulito, la run reale resta separata. La qualità
deve precedere la generazione provider.
