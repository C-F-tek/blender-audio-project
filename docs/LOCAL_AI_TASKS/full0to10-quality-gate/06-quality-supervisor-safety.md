# Quality supervisor safety

Il quality supervisor è quality-only di default.

## Regola

```text
default = no launcher
-RunLauncher = launcher esplicito
-AllowGitSyncBranching = consente git sync/branching nel launcher
```

Senza `-RunLauncher`, il supervisor produce solo:

- preflight quality stack;
- final quality stack.

## Compatibilità report-dir

`Tools/validation/check_ai_workload_report_quality.py` accetta ora:

```text
--report
--report-dir
```

Questo evita crash quando il launcher ufficiale passa una directory di report.

## Uso sicuro

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_full0to10_quality_supervisor.ps1 `
  -RepoRoot . `
  -NoExternalProbes `
  -OutputDir .\output\validation\full0to10_quality_supervisor_safe_only
```
