# Tools/validation context index

Use this index to find the nearest validation context before adding or changing checks.

| Family | Context file |
| --- | --- |
| Heap runtime | `Tools/validation/heap_runtime/TOOL_CONTEXT.md` |
| Provider mesh | `Tools/validation/provider_mesh/TOOL_CONTEXT.md` |
| Runtime tool | `Tools/validation/runtime_tool/TOOL_CONTEXT.md` |
| Runtime universe | `Tools/validation/runtime_universe/TOOL_CONTEXT.md` |

Canonical command surface:

```powershell
python -m Tools.validation <tool> [args...]
```

Public validation tool names are registered in `Tools/validation/dispatch.py`.

A validation report proves only the checked contract. It does not replace current source inspection.
