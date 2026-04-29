# Smoke Tests - file da condividere

Questa guida elenca i file prodotti dagli smoke test che possono essere condivisi per analisi successiva.

## AI core smoke test

Esecuzione PowerShell:

```powershell
.\Tools\smoke_tests\run_ai_core_smoke_tests.ps1
```

Esecuzione Python diretta:

```powershell
python Tools/smoke_tests/run_ai_core_smoke_tests.py --output-dir output/smoke_tests/ai_core
```

Output generati:

```text
output/smoke_tests/ai_core/ai_core_smoke_report.json
output/smoke_tests/ai_core/ai_core_smoke_report.md
output/smoke_tests/ai_core/core_pipeline_smoke/
├── value.json
├── pipeline_result.json
└── manifest.json
```

## NPU validation bridge smoke test

Questo test verifica il bridge tra la vecchia pipeline NPU e il nuovo adapter Blender.

Esecuzione PowerShell:

```powershell
.\Tools\smoke_tests\run_npu_validation_bridge_smoke_tests.ps1
```

Esecuzione Python diretta:

```powershell
python Tools/smoke_tests/run_npu_validation_bridge_smoke_tests.py --output-dir output/smoke_tests/npu_validation_bridge --manifest Tools/npu/npu_code_manifest.json
```

Output generati:

```text
output/smoke_tests/npu_validation_bridge/npu_validation_bridge_smoke_report.json
output/smoke_tests/npu_validation_bridge/npu_validation_bridge_smoke_report.md
```

## Cosa condividere

Per una revisione rapida condividere:

```text
output/smoke_tests/ai_core/ai_core_smoke_report.json
output/smoke_tests/ai_core/ai_core_smoke_report.md
output/smoke_tests/npu_validation_bridge/npu_validation_bridge_smoke_report.json
output/smoke_tests/npu_validation_bridge/npu_validation_bridge_smoke_report.md
```

Per una revisione piu dettagliata condividere anche:

```text
output/smoke_tests/ai_core/core_pipeline_smoke/manifest.json
output/smoke_tests/ai_core/core_pipeline_smoke/pipeline_result.json
```

## Cosa verificano

Gli smoke test verificano:

- parsing JSON da output LLM con Markdown fence e trailing comma;
- model client statico;
- pipeline sequenziale generica;
- artifact store;
- validatore Blender per script generati;
- bridge legacy-compatible per `run_dual_ai_pipeline.py`;
- blocco di proposed file che tentano di sovrascrivere sorgenti esistenti;
- blocco di script Blender troppo piccoli o placeholder.

## Interpretazione rapida

Nel file JSON cercare:

```json
{
  "passed": true
}
```

Se `passed` e `false`, condividere il JSON completo per analisi. Il dettaglio degli errori si trova in:

```text
checks.blender_validator.invalid_report.issues
checks.sequential_pipeline.result.errors
checks.invalid_draft_rejection.report.issues
```

## Patch helper per collegare il bridge alla pipeline legacy

Il file seguente prepara la migrazione controllata di `run_dual_ai_pipeline.py`:

```text
Tools/npu/patch_run_dual_ai_pipeline_validation_bridge.py
```

Esecuzione:

```powershell
python Tools/npu/patch_run_dual_ai_pipeline_validation_bridge.py
```

Il comando:

- aggiunge l'import del bridge;
- sostituisce solo il blocco `validate_implementation_draft()`;
- mantiene la shape legacy `{ "passed": bool, "issues": list[str] }`;
- stampa il nuovo numero di righe del file patchato.

## Nota architetturale

Questi smoke test non eseguono Blender, Ollama o OpenVINO. Servono a validare il core Python generico, le regole statiche dell'adapter Blender e il bridge NPU prima del refactor completo.
