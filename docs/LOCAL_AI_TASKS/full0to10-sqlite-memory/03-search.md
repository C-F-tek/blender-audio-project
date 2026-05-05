# Search

Ricerca FTS/hybrid-ready:

```powershell
python .\Toolsiull0to10_memory_tool.py search `
  --db .\outputi_runtime_memory\operational_context.sqlite `
  --namespace repo_docs `
  --query "Full0To10 bundle telemetry"
```

In questa patch `hybrid_score` coincide con FTS score. La cache embedding è nello
schema per la patch provider successiva.
