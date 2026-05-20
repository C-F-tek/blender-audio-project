# Tools/workflow/workflow_run context

## Role

`Tools/workflow/workflow_run` contains workflow-facing Python packages for startup checks, smart context, workflow shells, diagnostics, local artifact reset, Git helper integration and local workflow utilities.

This area supports operator workflows and local orchestration surfaces. It is separate from the core AI heap runtime implementation under `Tools/ai`.

## Responsibilities

- Run startup and environment checks.
- Provide workflow shell helpers.
- Build smart AI context reports.
- Provide workflow diagnostics.
- Support local artifact reset and cleanup flows.
- Support Git push helper surfaces where explicitly requested.
- Provide audio analysis and scene-spec workflow packages when used by application-domain tasks.

## Representative command surface

Use through the workflow dispatcher:

```powershell
python -m Tools.workflow startup_check ...
python -m Tools.workflow workflow_debug ...
python -m Tools.workflow smart_ai_context ...
python -m Tools.workflow workflow_shell ...
python -m Tools.workflow workflow_shell_with_push ...
python -m Tools.workflow git_auto_push ...
python -m Tools.workflow run_local_ai_artifact_reset ...
python -m Tools.workflow analyze_audio ...
python -m Tools.workflow scene_spec ...
```

## Workflow model

```text
operator/local request -> workflow helper -> Tools.ai or Scripting package as needed
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
- Heavy AI runtime behavior belongs under `Tools/ai`.
- Blender/media execution requires explicit application-domain task scope.
- Git operations should remain explicit and operator-driven.

## Extension notes

When adding workflow helpers, keep them small and register them through `Tools/workflow/dispatch.py`.
