# Tools/workflow context index

| Family | Context file |
| --- | --- |
| Retired workflow surface | `Tools/workflow/TOOL_CONTEXT.md` |
| GUI implementation modules | `Tools/workflow/gui/TOOL_CONTEXT.md` |
| Workflow run implementation modules | `Tools/workflow/workflow_run/TOOL_CONTEXT.md` |

`Tools.workflow` has no public command surface. Use `python -m ia_carmine.cli run`
with explicit flags for runs, and use the canonical validation/broker commands
for checks and helper/tool execution.
