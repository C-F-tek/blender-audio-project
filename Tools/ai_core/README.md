# Tools.ai_core

Core riutilizzabile per pipeline AI locali o ibride.

Questo package non dipende da Blender, Ollama, OpenVINO, file audio o layout specifici del progetto. Deve contenere solo primitive riusabili.

## Obiettivo

Standardizzare il flusso:

```text
input tecnico
  -> prompt/model execution
  -> parsing JSON robusto
  -> validazione
  -> artifact per run
  -> output finale
```

## Moduli

- `io_utils.py`: lettura/scrittura file e JSON.
- `json_utils.py`: parsing output LLM.
- `models.py`: interfaccia modello.
- `validators.py`: validazione generica.
- `artifact.py`: artifact store per run.
- `pipeline.py`: pipeline sequenziale a stage.

## Regola architetturale

Se una funzione nomina direttamente `bpy`, WAV, Blender, NPU, Ollama o un file specifico del progetto, non deve stare qui: deve stare in un adapter o in uno script CLI.

## Esempio minimo

```python
from Tools.ai_core import ArtifactStore, PipelineContext, SequentialPipeline

store = ArtifactStore("output/ai_runs", run_id="demo")
context = PipelineContext(job={"name": "demo"}, artifacts=store)
result = SequentialPipeline([]).run(context)
print(result.to_dict())
```
