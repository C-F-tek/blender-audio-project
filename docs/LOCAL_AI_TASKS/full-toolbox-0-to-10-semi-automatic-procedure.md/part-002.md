<!-- IA-CARMINE-MD-SPLIT: part -->
# full-toolbox-0-to-10-semi-automatic-procedure — parte 002 di 004

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)
- [Parte successiva](part-003.md)

```powershell
# Replace the provider-run knobs above with:
--budget-minutes 40 `
--max-rounds 28 `
--files-per-round 12 `
--max-context-files 280 `
--max-chars-per-file 9000 `
--max-new-tokens 5200 `
--npu-auditor-every-rounds 4 `
--npu-auditor-timeout-seconds 360 `
--npu-max-context-chars 6000 `
--npu-max-prompt-chars 900 `
--npu-max-new-tokens 256 `
--npu-final-wait-seconds 120
```
