# Tools/workflow/workflow_run context

## Role

`Tools/workflow/workflow_run` contains workflow-facing Python packages for startup checks, smart context, workflow shells, diagnostics, local artifact reset, Git helper integration and local workflow utilities.

This area supports operator workflows and local orchestration surfaces. It is separate from the core AI heap runtime implementation under `ia_carmine`.

## Responsibilities

- Run startup and environment checks.
- Provide workflow shell helpers.
- Build smart AI context reports.
- Provide workflow diagnostics.
- Support local artifact reset and cleanup flows.
- Support Git push helper surfaces where explicitly requested.
- Provide audio analysis and scene-spec workflow packages when used by application-domain tasks.

## Access

```powershell
python -m ia_carmine.cli run [explicit flags...]
python -m Tools.validation validator_unico --mode <mode> [--section <section>]
```

Direct workflow dispatcher commands are retired. These packages are implementation
modules and must not add new wrapper entrypoints.

## Workflow model

```text
operator/local request -> workflow helper -> ia_carmine or Scripting package as needed
```

Workflow helpers should coordinate existing tools rather than duplicate heap runtime logic.

## Expected artifacts

```text
startup reports
workflow diagnostics
smart context reports
local artifact reset reports
workflow shell logs when explicitly produced
```

## Boundaries

- Workflow code should remain a thin coordination layer.
- Heavy AI runtime behavior belongs under `ia_carmine`.
- Blender/media execution requires explicit application-domain task scope.
- Git operations should remain explicit and operator-driven.

## Extension notes

When adding workflow helpers, expose them through canonical run, validation or
broker mode parameters rather than a new workflow command.
