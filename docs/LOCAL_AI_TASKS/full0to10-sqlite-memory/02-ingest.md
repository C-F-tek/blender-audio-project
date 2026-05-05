# Ingest

Comandi:

```powershell
python .\Toolsiull0to10_memory_tool.py init --db .\outputi_runtime_memory\operational_context.sqlite

python .\Toolsiull0to10_memory_tool.py add-text `
  --db .\outputi_runtime_memory\operational_context.sqlite `
  --namespace chatgpt_handoff `
  --text "..."
```

Per file Markdown, il chunker divide per heading.
