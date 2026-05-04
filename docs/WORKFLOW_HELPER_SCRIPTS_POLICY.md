# Workflow Helper Scripts Policy

## Purpose

Classify workflow helper scripts that exist in the repository but must not be confused with the canonical local-AI entrypoint.

Canonical local-AI entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

This policy covers shell, GUI, debug, diagnostics, supporting workflow wrappers and push-capable helpers.

## Canonical vs supporting

| Script | Classification | Policy |
|---|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | canonical-entrypoint | Primary headless operator flow. |
| `Tools/workflow/run_local_validation_after_refactor.ps1` | supporting validation wrapper | Use directly only for focused legacy validation. Prefer launcher `validation` / `full_validation` modes for normal flow. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | launcher-internal/supporting adapter | Usually called by launcher or task wrapper; not a standalone 0-to-10 entrypoint. |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | launcher-internal/supporting advisory wrapper | Provider/advisory path; explicit use only. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | launcher-internal/supporting provider/probe wrapper | Explicit provider/probe evidence only; prefer launcher `provider` / Full0To10 paths. |
| `Tools/workflow/run_docs_md_refactor_10min.ps1` | legacy/superseded helper | Prefer unified launcher `md` mode. Do not document as active start path. |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | supporting task wrapper | Useful for task-scoped adapter runs; not a replacement for Full0To10. |
| `Tools/workflow/startup_preflight.ps1` | diagnostic-only | Startup/preflight helper. |
| `Tools/workflow/startup_check.py` | diagnostic-only | Startup check helper. |

## Promotion rule

A helper can become part of the active flow only if the unified launcher records it visibly.

Required surfaces:

```text
launcher parameter or selected mode
phase_status entry
phase_reports entry when a report is produced
manifest field for any provider/memory/patch/evidence behavior
runbook mention in unified-local-ai-refactor-launcher.md
contract mention in UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md when manifest shape changes
```

No helper may become a hidden side-channel for provider execution, SQLite writes, patch application, evidence generation or git push.

## Shell and GUI helpers

These helpers are interactive/operator-facing but are not the canonical headless flow:

```text
Tools/workflow/workflow_shell.py
Tools/workflow/workflow_debug.py
Tools/workflow/gui/workflow_gui_modern.py
```

Policy:

```text
may be used for local operator convenience
must not be documented as the default full 0-to-10 path
must not hide provider execution or patch application
must keep git status/diff visibility before write/push operations
```

## Push-capable helpers

These scripts are risky because they can push or automate git operations:

```text
Tools/workflow/workflow_shell_with_push.py
Tools/workflow/gui/workflow_gui_with_push.py
Tools/workflow/git_auto_push.py
```

Hard policy:

```text
never use as default documentation examples
never invoke from validation-only docs
require explicit user intent before push
show git status before push
show target branch and remote before push
must not merge protected branches
must not force-push or rewrite history
must not push generated DB/output/cache files
```

A push-capable helper is not allowed to bypass the normal review flow:

```text
manifest -> phase reports -> git diff/status -> explicit operator approval -> push
```

## Context/domain helpers

These scripts help build context or inspect project/domain artifacts. They are supporting tools, not entrypoints:

```text
Tools/workflow/asset_inventory.py
Tools/workflow/scene_brief.py
Tools/workflow/artifact_consult.py
Tools/workflow/project_awareness.py
Tools/workflow/smart_ai_context.py
Tools/workflow/ai_runtime_diagnostics.py
```

Initial classification:

| Script | Classification |
|---|---|
| `asset_inventory.py` | supporting-tool |
| `scene_brief.py` | supporting-tool / application-domain helper |
| `artifact_consult.py` | supporting-tool |
| `project_awareness.py` | supporting-tool |
| `smart_ai_context.py` | supporting-tool |
| `ai_runtime_diagnostics.py` | diagnostic-only |

Policy:

```text
call only when task scope requires that context
record outputs in manifest/context_files/report_files when used by launcher
keep application-domain helpers separate from AI orchestration helpers
```

## Documentation requirements

Whenever a helper script is added or promoted, update at least one of:

```text
docs/MODULE_MAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

If it becomes part of the unified launcher, also update:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

## Audit command

Use script inventory before promoting or deleting helpers:

```powershell
python .\Tools\validation\build_script_inventory.py `
  --repo-root . `
  --output .\output\validation\script_inventory_workflow_helpers.json `
  --csv-output .\output\validation\script_inventory_workflow_helpers.csv `
  --markdown-output .\output\validation\script_inventory_workflow_helpers.md
```

Review relevant rows:

```powershell
$Inv = Get-Content .\output\validation\script_inventory_workflow_helpers.json -Raw | ConvertFrom-Json
$Inv.scripts |
  Where-Object { $_.path -like 'Tools/workflow/*' } |
  Select-Object path, language, category, line_count |
  Sort-Object path |
  Format-Table -AutoSize
```

## Stop conditions

Stop if a proposed documentation/example change would:

```text
make a push-capable helper look like the default workflow
hide a provider execution path
hide patch application
hide git branch/remote target
promote a GUI/shell helper above the unified launcher
remove a script reference without confirming the script is absent or obsolete
create a new parallel active-start runbook instead of extending the unified launcher
```

## Acceptance criteria

```text
unified launcher remains canonical
supporting helpers are visible but not over-promoted
push-capable helpers have explicit risk warnings
diagnostics are separated from normal validation
script inventory is the source for broad helper audits
helpers wired into launcher are visible in manifest/status/report surfaces
no helper is deleted without explicit approval
```
