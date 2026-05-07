# InputPath normalization

## Problema

PowerShell può passare:

```powershell
-InputPath ".\README.md",".\Tools\workflow\run_unified_local_ai_refactor.ps1",".\Tools\ai\build_full_toolbox_run_telemetry_summary.py"
```

come una singola stringa comma-separated.

## Fix

Il wrapper normalizza:

- array reali;
- stringhe comma-separated;
- stringhe separate da `;`;
- newline;
- quote/spazi.

## Risultato atteso

```text
Normalized input count: 3
input: .\README.md
input: .\Tools\workflow\run_unified_local_ai_refactor.ps1
input: .\Tools\ai\build_full0to10_run_manifest.py
```
