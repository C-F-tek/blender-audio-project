# Refactor Rollback Guide

Guida rapida per annullare in sicurezza i passaggi del refactor AI core.

## Scenario A - Smoke test falliti senza modifiche legacy

Se hai eseguito solo:

```powershell
.\Tools\smoke_tests\run_all_refactor_smoke_tests.ps1
```

e non hai modificato file sorgente manualmente, non serve rollback del codice.

Condividi:

```text
output/smoke_tests/refactor_summary/refactor_smoke_summary.json
output/smoke_tests/refactor_summary/refactor_smoke_summary.md
```

## Scenario B - Hai eseguito il patch helper legacy

Il comando:

```powershell
python Tools/npu/patch_run_dual_ai_pipeline_validation_bridge.py
```

modifica:

```text
Tools/npu/run_dual_ai_pipeline.py
```

Per vedere il diff:

```powershell
git diff -- Tools/npu/run_dual_ai_pipeline.py
```

Per annullare solo quella modifica:

```powershell
git restore Tools/npu/run_dual_ai_pipeline.py
```

Per verificare:

```powershell
git status
```

## Scenario C - Vuoi annullare tutte le modifiche locali non committate

Attenzione: questo elimina tutte le modifiche locali non committate.

```powershell
git restore .
```

Se ci sono file nuovi non tracciati:

```powershell
git clean -fd
```

Prima di `git clean -fd`, controllare sempre:

```powershell
git clean -fdn
```

## Scenario D - Vuoi tornare al branch master

```powershell
git checkout master
git pull
```

## Scenario E - Vuoi eliminare il branch locale del refactor

Solo dopo essere uscito dal branch:

```powershell
git checkout master
git branch -D ai/generic-pipeline-core
```

## Scenario F - Vuoi eliminare anche il branch remoto

Da usare solo se la PR deve essere scartata:

```powershell
git push origin --delete ai/generic-pipeline-core
```

## Regola consigliata

Prima di ogni patch reale sulla pipeline legacy:

```powershell
git status
```

Dopo ogni patch reale:

```powershell
git diff --stat
python -m py_compile Tools/npu/run_dual_ai_pipeline.py
.\Tools\smoke_tests\run_all_refactor_smoke_tests.ps1
```

## File sicuri da condividere

Questi file non contengono codice sorgente completo, ma report diagnostici utili:

```text
output/smoke_tests/refactor_summary/refactor_smoke_summary.json
output/smoke_tests/refactor_summary/refactor_smoke_summary.md
output/smoke_tests/ai_core/ai_core_smoke_report.json
output/smoke_tests/npu_validation_bridge/npu_validation_bridge_smoke_report.json
```
