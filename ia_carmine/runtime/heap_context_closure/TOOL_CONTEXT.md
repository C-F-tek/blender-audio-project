# Heap Context Closure Runtime

The heap context closure package is the internal file-backed launcher for run-unica heap closure.

Current contract:

- The launcher materializes the augmented operator request as a run artifact and forwards that artifact with `--request-file`.
- HTTP/API and child-process arguments coordinate work; large request, context, provider prompt and report bodies live on filesystem artifacts.
- Startup context, dynamic GPU1 context pack, RAG hard surfaces and runtime refs are blockers when missing or invalid.
- Provider output JSON must carry refs, hashes and bounded tails; full text belongs in provider/composer artifacts.
- Broker tool execution evidence must pass through broker request/result artifacts, not prose or in-memory packet state.

Primary operator command:

```powershell
python -m ia_carmine.cli run ...
```

Related surfaces:

- `ia_carmine/runtime/run/TOOL_CONTEXT.md`
- `ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md`
- `ia_carmine/runtime/provider_runtime_blackboard/TOOL_CONTEXT.md`
- `ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md`
