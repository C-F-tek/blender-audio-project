# Tools/workflow/gui context

## Role

`Tools/workflow/gui` contains retired GUI implementation modules.

The GUI is an operator-facing view/controller surface for workflow launch tasks.

## Responsibilities

- Provide visual workflow launcher access.
- Do not expose GUI modules as standalone workflow dispatcher commands.
- Delegate workflow behavior to maintained workflow/runtime packages.

## Representative commands

The public runtime entrypoint remains `python -m ia_carmine.cli run`.

## Boundaries

- GUI code should stay thin.
- Business/runtime logic should not live only in widgets.
- Do not use GUI launch as proof that a workflow completed; verify output artifacts and return codes.

## Validation

Validate GUI-adjacent behavior through workflow smoke tests or controller-level checks where available.
