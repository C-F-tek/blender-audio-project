# Tools/workflow context

## Role

`Tools/workflow` owns operator workflow helpers: PowerShell wrappers, GUI/shell launchers, startup checks, local AI task execution, audio analysis and workflow observability.

Canonical invocation:

```powershell
python -m Tools.workflow <tool> [tool args...]
```

The source of truth for public workflow tools is `Tools/workflow/dispatch.py`. Some maintained workflow tools intentionally dispatch to PowerShell wrappers under `_powershell/`.

## Main families

### Operator GUI and shell surfaces

Use these when the operator needs an interactive or semi-interactive surface instead of composing long command lines manually.

Representative tools:

```text
gui
workflow_gui
workflow_shell
workflow_shell_with_push
start_workflow
```

These surfaces should remain thin. Business logic should live in reusable Python modules or existing run/AI controllers, not in the GUI layout itself.

### Local AI task launchers

Use these when starting from a Markdown task/request and producing an isolated run directory.

Representative tools:

```text
run_local_ai_markdown_task
run_local_ai_task_via_pipeline
run_local_ai_core_tool_activation
run_unified_local_ai_refactor
run_unified_real_product_pr
```

Expected flow:

```text
input MD -> prompt/task preparation -> run directory -> tool/provider execution
-> validation/evidence -> final product or blocked diagnosis
```

Do not treat a generated command as an executed run. The run is real only when artifacts and return codes exist.

### Startup and preflight

Use these to prepare or inspect runtime conditions before longer workflows.

Representative tools:

```text
startup_check
startup_check_core
startup_preflight
run_ai_cycle_startup_preflight
ai_runtime_diagnostics
```

Startup/preflight should verify environment, paths, request files, Python invocation, expected folders and safety assumptions.

### Audio, scene and Blender workflow support

Use these for project-specific creative/audio-reactive workflow preparation.

Representative tools:

```text
analyze_audio
audio_summary
scene_spec
smart_ai_context
smart_ai_context_core
```

These tools can create analysis/context artifacts for Blender/audio work. Generated runtime outputs remain local unless explicitly converted into Git-trackable docs.

### Workflow observers and visibility

Use these when a long run needs public/diagnostic visibility without mixing raw provider text into final product.

Representative tools:

```text
unified_run_observer
unified_phase_visibility
watch_unified_ai_conversation
watch_unified_ai_public_exchange
watch_unified_raw_debug_good_info
workflow_debug
workflow_debug_core
```

Observers should read/report state. They should not silently mutate source files.

### Maintenance and reset wrappers

Use these for operational maintenance tasks.

Representative tools:

```text
install_weekly_local_ai_reset_task
run_local_ai_artifact_reset
run_full_memory_tool_regeneration
repair_full_toolbox_datastamp_doc
run_local_validation_after_refactor
run_post_validation_ai_packet
```

Maintenance wrappers must keep destructive behavior explicit. Do not delete or reset artifacts without an operator-visible command path.

## Safety rules

- Prefer `python -m Tools.workflow <tool>` over direct file-path invocation.
- Keep PowerShell wrappers under `_powershell/` and registered in `dispatch.py`.
- Do not commit `output/**`, runtime logs, databases or generated local AI runs.
- Keep GUI/view code separate from core logic.
- When a workflow triggers Git actions, keep push/merge/delete operations explicit and operator-driven.
