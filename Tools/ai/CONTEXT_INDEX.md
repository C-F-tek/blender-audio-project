# Tools/ai context index

Use this index to find the nearest `TOOL_CONTEXT.md` before working on a package family.

| Family | Context file |
| --- | --- |
| Agent context | `Tools/ai/agent_context/TOOL_CONTEXT.md` |
| Agent memory | `Tools/ai/agent_memory/TOOL_CONTEXT.md` |
| Agent review | `Tools/ai/agent_review/TOOL_CONTEXT.md` |
| Code product | `Tools/ai/code_product/TOOL_CONTEXT.md` |
| External heap | `Tools/ai/external_heap/TOOL_CONTEXT.md` |
| Generated patch specs | `Tools/ai/generated_patch_specs/TOOL_CONTEXT.md` |
| Heap context memory reload | `Tools/ai/heap_context_memory_reload/TOOL_CONTEXT.md` |
| Heap gate | `Tools/ai/heap_gate/TOOL_CONTEXT.md` |
| Heap runtime | `Tools/ai/heap_runtime/TOOL_CONTEXT.md` |
| Operator product core | `Tools/ai/operator_product_core/TOOL_CONTEXT.md` |
| Patch product | `Tools/ai/patch_product/TOOL_CONTEXT.md` |
| Provider mesh | `Tools/ai/provider_mesh/TOOL_CONTEXT.md` |
| Provider runtime blackboard | `Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md` |
| Repository product | `Tools/ai/repository_product/TOOL_CONTEXT.md` |
| Runtime tool | `Tools/ai/runtime_tool/TOOL_CONTEXT.md` |
| Runtime universe | `Tools/ai/runtime_universe/TOOL_CONTEXT.md` |

Canonical command surface:

```powershell
python -m Tools.ai <tool> [args...]
```

Public tool names are registered in `Tools/ai/dispatch.py`.
