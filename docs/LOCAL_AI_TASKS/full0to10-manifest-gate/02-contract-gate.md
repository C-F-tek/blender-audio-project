# Contract gate

Il gate post-bundle esegue due step:

1. `build_full0to10_run_manifest.py`
2. `check_full0to10_bundle_contracts.py`

Il primo produce la mappa della run. Il secondo verifica che bundle, memory lane e
hardware delegation siano visibili.

## Uso

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflowun_full0to10_manifest_contract_gate.ps1 `
  -RepoRoot . `
  -Bundle .\docs\LOCAL_VALIDATION_EVIDENCE\<bundle>.json `
  -EvidenceDir .\docs\LOCAL_VALIDATION_EVIDENCE
```
