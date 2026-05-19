# Tools/workflow/_powershell context

## Role

`Tools/workflow/_powershell` contains maintained PowerShell wrappers registered by `Tools/workflow/dispatch.py`.

These wrappers are workflow entrypoints or operator helpers, not ad-hoc scripts.

## Responsibilities

- Provide Windows/operator-friendly workflow launch surfaces.
- Wrap local AI task, startup, observer, reset and validation flows.
- Keep long command sequences discoverable through the workflow dispatcher.

## Representative invocation

Prefer the dispatcher form:

```powershell
python -m Tools.workflow <tool> [args...]
```

Do not call `_powershell/*.ps1` directly unless the dispatcher path is not suitable for the specific operator task.

## Boundaries

- PowerShell wrappers should stay thin.
- Core logic should live in Python packages or existing runtime tools when possible.
- Do not commit `output/**` produced by wrapper runs.
- Git/push-related wrappers must remain explicit operator actions.

## Validation

Validate wrapper behavior through the related workflow or validation smoke where available.