# Tools/npu context index

| Family | Context file |
| --- | --- |
| PowerShell wrappers | `Tools/npu/_powershell/TOOL_CONTEXT.md` |
| Dual AI pipeline | `Tools/npu/dual_ai_pipeline/TOOL_CONTEXT.md` |
| Provider mesh | `Tools/npu/provider_mesh/TOOL_CONTEXT.md` |

Canonical command surface:

```powershell
python -m Tools.npu <tool> [args...]
```

Public NPU tool names are registered in `Tools/npu/dispatch.py`.