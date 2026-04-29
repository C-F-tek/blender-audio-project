# AI Core Migration Checklist

Checklist operativa per completare il refactor della pipeline AI senza rompere la pipeline Blender/NPU esistente.

## Fase 0 - Stato sicuro

- [ ] Branch attivo: `ai/generic-pipeline-core`.
- [ ] PR in draft.
- [ ] Nessuna modifica manuale non committata.
- [ ] `run_dual_ai_pipeline.py` non ancora patchato oppure patch documentata.

Comandi:

```powershell
git status
git branch --show-current
```

## Fase 1 - Smoke test non invasivi

Eseguire:

```powershell
.\Tools\smoke_tests\run_all_refactor_smoke_tests.ps1
```

File principali da controllare/condividere:

```text
output/smoke_tests/refactor_summary/refactor_smoke_summary.json
output/smoke_tests/refactor_summary/refactor_smoke_summary.md
```

Criterio di passaggio:

```json
{
  "passed": true
}
```

## Fase 2 - Patch controllata del validatore legacy

Da eseguire solo dopo Fase 1 verde:

```powershell
python Tools/npu/patch_run_dual_ai_pipeline_validation_bridge.py
```

Controllare:

```powershell
git diff -- Tools/npu/run_dual_ai_pipeline.py
python -m py_compile Tools/npu/run_dual_ai_pipeline.py
```

Criterio di passaggio:

- il diff deve mostrare solo import bridge + sostituzione di `validate_implementation_draft()`;
- `py_compile` deve terminare senza errori;
- il comando patch deve stampare il nuovo numero di righe.

## Fase 3 - Smoke test dopo patch legacy

Dopo la patch del file legacy, rieseguire:

```powershell
.\Tools\smoke_tests\run_all_refactor_smoke_tests.ps1
```

Poi aggiungere un test dedicato da creare nella fase successiva:

```powershell
.\Tools\smoke_tests\run_legacy_pipeline_bridge_smoke_tests.ps1
```

## Fase 4 - Migrazione funzioni duplicate

Migrare progressivamente da `run_dual_ai_pipeline.py` verso `Tools.ai_core`:

- [ ] `read_text()` -> `Tools.ai_core.io_utils.read_text()`.
- [ ] `read_json()` -> `Tools.ai_core.io_utils.read_json()`.
- [ ] `write_json()` -> `Tools.ai_core.io_utils.write_json()`.
- [ ] parsing JSON output modello -> `Tools.ai_core.json_utils.parse_model_json()`.
- [ ] artifact writing -> `Tools.ai_core.artifact.ArtifactStore`.
- [ ] validazione implementation draft -> `Tools.ai_adapters.blender.validators`.

Regola: una migrazione per commit, smoke test dopo ogni step.

## Fase 5 - Adapter Blender completi

Creare o completare:

```text
Tools/ai_adapters/blender/
├── generated_script_policy.py
├── validators.py
├── prompts.py
└── stages.py
```

Da spostare gradualmente:

- prompt implementation draft;
- prompt retry;
- policy sui file generati;
- validazione `scene_script`;
- regole asset/keyframes/audio.

## Fase 6 - Adapter audio

Creare:

```text
Tools/ai_adapters/audio/
├── __init__.py
├── summaries.py
└── stages.py
```

Da spostare gradualmente:

- caricamento context audio;
- normalizzazione track summary;
- segment summaries;
- bridge tra analysis JSON e prompt AI.

## Fase 7 - Pipeline a stage

Sostituire lentamente le macro-funzioni con stage:

```text
LoadContextStage
BuildPromptStage
RunModelStage
ParseJsonStage
ValidateDraftStage
WriteArtifactsStage
```

Criterio: il CLI legacy deve continuare a funzionare.

## Fase 8 - Merge PR

Prima di rendere la PR ready:

- [ ] smoke test aggregato verde;
- [ ] eventuale patch legacy compilabile;
- [ ] nessun file generato dentro `output/` committato per errore;
- [ ] documentazione aggiornata;
- [ ] PR ancora leggibile e non troppo invasiva.

## File report da condividere

Sempre preferire:

```text
output/smoke_tests/refactor_summary/refactor_smoke_summary.json
output/smoke_tests/refactor_summary/refactor_smoke_summary.md
```

Se serve dettaglio:

```text
output/smoke_tests/ai_core/ai_core_smoke_report.json
output/smoke_tests/npu_validation_bridge/npu_validation_bridge_smoke_report.json
```
