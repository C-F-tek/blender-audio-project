# Tools/workflow context index

| Family | Context file |
| --- | --- |
| PowerShell wrappers | `Tools/workflow/_powershell/TOOL_CONTEXT.md` |
| GUI | `Tools/workflow/gui/TOOL_CONTEXT.md` |
| Workflow run packages | `Tools/workflow/workflow_run/TOOL_CONTEXT.md` |

Canonical command surface:

```powershell
python -m Tools.workflow <tool> [args...]
```

Public workflow tool names are registered in `Tools/workflow/dispatch.py`.