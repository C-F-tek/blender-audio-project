# Memory tools

La memory lane SQLite è disponibile come tool invocabile via JSON.

Esempio:

```powershell
python .\Tools\ai\full0to10_runtime_tool.py memory_search `
  --args-json '{"db":"output/ai_runtime_memory/operational_context.sqlite","namespace":"repo_docs","query":"bundle telemetry"}'
```

Il DB resta runtime artifact locale e non va committato.
