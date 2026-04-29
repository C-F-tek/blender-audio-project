# AI Pipeline Refactor Plan

## Stato rilevato

Il progetto contiene gia una pipeline AI avanzata, ma la logica e ancora concentrata in script operativi specifici, soprattutto `Tools/npu/run_dual_ai_pipeline.py` e `Tools/ai/run_parallel_artifact_pipeline.py`.

Sono gia presenti elementi maturi:

- context packet per AI;
- review first-wave WAV entrypoints;
- guardrail NPU;
- remediation loop;
- generazione artifact;
- validazioni per script Blender generati;
- separazione CPU/NPU/GPU a livello operativo.

Il limite principale e che queste capacita non sono ancora estratte in un core riutilizzabile da altri progetti.

## Intervento introdotto

E stato aggiunto il package `Tools/ai_core/`, volutamente indipendente da Blender, audio, Ollama, OpenVINO e layout specifico del repository.

Moduli introdotti:

```text
Tools/ai_core/
├── __init__.py
├── artifact.py
├── io_utils.py
├── json_utils.py
├── models.py
├── pipeline.py
└── validators.py
```

## Responsabilita dei moduli

### `io_utils.py`

Funzioni riutilizzabili per lettura/scrittura file e JSON:

- `read_text()`
- `write_text()`
- `read_json()`
- `write_json()`
- `ensure_dir()`
- `file_meta()`

Da usare al posto di funzioni duplicate sparse negli script.

### `json_utils.py`

Parser JSON per output LLM:

- rimuove fence Markdown;
- estrae il blocco JSON principale;
- ripara trailing comma e commenti riga semplici;
- espone `parse_model_json()` e `parse_model_json_object()`.

Questo deve diventare il punto unico per parsing di output Ollama/NPU/OpenAI-compatible.

### `models.py`

Interfaccia generica modello:

- `ModelClient`;
- `ModelResponse`;
- `StaticModelClient` per test deterministici.

Gli adapter futuri saranno:

- `OllamaModelClient`;
- `OpenVINOModelClient`;
- `OpenAICompatibleModelClient`.

### `validators.py`

Primitive comuni di validazione:

- `ValidationIssue`;
- `ValidationReport`;
- `Validator`;
- `RequiredKeysValidator`.

I validatori Blender-specific dovrebbero stare in `Tools/ai_adapters/blender/` o in un modulo dedicato.

### `artifact.py`

Gestione artifact per run:

- directory per run;
- scrittura JSON/testi;
- manifest finale.

Serve a standardizzare output come prompt, raw response, parsed JSON, validation report, final artifact.

### `pipeline.py`

Runner generico a stage:

- `PipelineContext`;
- `PipelineStage`;
- `SequentialPipeline`;
- `PipelineResult`.

Ogni stage muta il contesto e produce log/artifact.

## Migrazione consigliata

### Fase 1 - Migrazione funzioni duplicate

Sostituire progressivamente in `Tools/npu/run_dual_ai_pipeline.py`:

```python
read_text()
read_json()
write_json()
```

con:

```python
from Tools.ai_core import read_text, read_json, write_json
```

Questa fase e a basso rischio.

### Fase 2 - Parser JSON unico

Sostituire wrapper locali come `safe_parse_json()` dove possibile con:

```python
from Tools.ai_core import parse_model_json
```

Per non rompere compatibilita, mantenere fallback specifici solo dove servono per output storici.

### Fase 3 - Artifact store per ogni run

Ogni run AI dovrebbe scrivere:

```text
output/ai_runs/<run_id>/
├── job.json
├── prompt_primary.txt
├── raw_primary.txt
├── parsed_primary.json
├── validation_report.json
├── final_result.json
└── manifest.json
```

Usare `ArtifactStore`.

### Fase 4 - Stage generici

Estrarre da `run_dual_ai_pipeline.py` stage come:

- `LoadMusicContextStage`;
- `BuildPromptStage`;
- `RunModelStage`;
- `ParseJsonStage`;
- `ValidateImplementationDraftStage`;
- `WriteGeneratedScriptStage`.

Gli stage generici restano in `Tools/ai_core`; quelli Blender/audio vanno in adapter.

### Fase 5 - Adapter Blender/audio

Creare in seguito:

```text
Tools/ai_adapters/
├── blender/
│   ├── __init__.py
│   ├── validators.py
│   ├── prompts.py
│   └── stages.py
└── audio/
    ├── __init__.py
    ├── summaries.py
    └── stages.py
```

## Architettura target

```text
WAV / codice / log / documenti
        ↓
input loader adapter
        ↓
AI core pipeline
        ↓
prompt builder adapter
        ↓
model client
        ↓
JSON parser core
        ↓
validator adapter
        ↓
artifact store core
        ↓
output specifico progetto
```

## Valutazione tecnica dei cambi recenti

Il commit recente `ai: integrate first wave review into smart pipeline` ha portato la pipeline artifact allo schema v6 aggiungendo review degli entrypoint WAV. Questo e coerente con la direzione generale: spostare il controllo qualità sempre piu a monte, prima che i JSON tecnici alimentino Blender.

La prossima ottimizzazione e ridurre la duplicazione tra:

- `Tools/ai/run_parallel_artifact_pipeline.py`;
- `Tools/npu/run_dual_ai_pipeline.py`;
- script di review e context building.

Il core introdotto serve esattamente a questo.

## Regola pratica

Ogni nuova funzione va classificata cosi:

| Tipo | Dove deve stare |
| --- | --- |
| lettura/scrittura file | `Tools/ai_core/io_utils.py` |
| parsing output modello | `Tools/ai_core/json_utils.py` |
| chiamata modello | `Tools/ai_core/models.py` o adapter client |
| validazione generica | `Tools/ai_core/validators.py` |
| validazione Blender | `Tools/ai_adapters/blender/validators.py` |
| prompt Blender | `Tools/ai_adapters/blender/prompts.py` |
| pipeline orchestration | `Tools/ai_core/pipeline.py` |
| script CLI specifico | `Tools/ai/` o `Tools/npu/` |

## Prossimo intervento consigliato

1. Creare `Tools/ai_adapters/blender/validators.py`.
2. Spostare dentro quel modulo la logica di `validate_implementation_draft()`.
3. Creare `Tools/ai_adapters/blender/generated_script_policy.py` per regole come:
   - prefissi ammessi;
   - file sorgente read-only;
   - controllo `import bpy`;
   - divieto di modificare JSON full-frame.
4. Collegare `run_dual_ai_pipeline.py` al nuovo validator mantenendo il vecchio comportamento.

## Comando test minimo

Dopo checkout del branch:

```powershell
python - <<'PY'
from Tools.ai_core import parse_model_json, StaticModelClient, ArtifactStore

print(parse_model_json('```json\n{"ok": true,}\n```'))
client = StaticModelClient('{"result": "ok"}')
print(client.generate('test').text)
store = ArtifactStore('output/ai_runs', run_id='core_smoke_test')
store.write_json('result.json', {'ok': True})
store.write_manifest()
print('core smoke test ok')
PY
```

Risultato atteso:

```text
{'ok': True}
{"result": "ok"}
core smoke test ok
```
