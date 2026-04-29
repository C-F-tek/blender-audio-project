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

## Cosa condividere

Per una revisione rapida condividere:

```text
output/smoke_tests/ai_core/ai_core_smoke_report.json
output/smoke_tests/ai_core/ai_core_smoke_report.md
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
```

## Nota architetturale

Questi smoke test non eseguono Blender, Ollama o OpenVINO. Servono a validare il core Python generico e le regole statiche dell'adapter Blender prima del refactor completo.
