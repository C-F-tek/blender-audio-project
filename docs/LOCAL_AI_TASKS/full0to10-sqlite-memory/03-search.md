# Search

Ricerca FTS:

```powershell
python .\Tools\ai\full0to10_memory_tool.py search `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace repo_docs `
  --query "Full0To10 bundle telemetry" `
  --mode fts
```

Ricerca hybrid con provider hash offline:

```powershell
python .\Tools\ai\full0to10_memory_tool.py search `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace repo_docs `
  --query "Full0To10 bundle telemetry" `
  --mode hybrid `
  --embedding-provider hash
```
