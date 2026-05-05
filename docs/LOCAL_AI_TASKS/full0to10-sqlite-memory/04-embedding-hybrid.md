# Embedding hybrid

La memoria SQLite include cache embedding locale.

## Provider

- `none`: FTS only;
- `hash`: embedding deterministico offline per smoke e test;
- `ollama`: embedding via API locale Ollama, da usare solo quando il servizio è pronto.

## Pre-cache

```powershell
python .\Tools\ai\full0to10_memory_tool.py embed-missing `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace repo_docs `
  --embedding-provider hash `
  --limit 1000
```

## Guardrail

La patch non genera testo, non applica patch, non scrive DB persistente versionato.
I database restano sotto `output/**` o path locali ignorati.
