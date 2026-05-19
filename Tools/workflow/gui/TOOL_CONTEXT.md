# Tools/workflow/gui context

## Role

`Tools/workflow/gui` contains the workflow GUI entrypoint registered by `Tools/workflow/dispatch.py`.

The GUI is an operator-facing view/controller surface for workflow launch tasks.

## Responsibilities

- Provide visual workflow launcher access.
- Keep GUI entrypoint discoverable via `python -m Tools.workflow gui` or `python -m Tools.workflow workflow_gui`.
- Delegate workflow behavior to maintained workflow/runtime packages.

## Representative commands

```powershell
python -m Tools.workflow gui
python -m Tools.workflow workflow_gui
```

## Boundaries

- GUI code should stay thin.
- Business/runtime logic should not live only in widgets.
- Do not use GUI launch as proof that a workflow completed; verify output artifacts and return codes.

## Validation

Validate GUI-adjacent behavior through workflow smoke tests or controller-level checks where available.