# Ingest

Comandi:

```powershell
python .\Tools\ai\full0to10_memory_tool.py init --db .\output\ai_runtime_memory\operational_context.sqlite

python .\Tools\ai\full0to10_memory_tool.py add-text `
  --db .\output\ai_runtime_memory\operational_context.sqlite `
  --namespace chatgpt_handoff `
  --text "..."
```

Per file Markdown, il chunker divide per heading.
