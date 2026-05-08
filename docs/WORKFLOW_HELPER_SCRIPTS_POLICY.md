# Workflow Helper Scripts Policy

## Purpose

Classify workflow helper scripts that exist in the repository but must not be confused with the canonical run-unica local-AI entrypoint.

Canonical local-AI entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

This policy covers shell, GUI, debug, diagnostics, supporting workflow wrappers and push-capable helpers.

## Current references

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Current doctrine

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
```

## Canonical vs supporting

| Script | Classification | Policy |
|---|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | canonical-entrypoint | Primary headless run-unica operator flow. |
| `Tools/workflow/run_local_validation_after_refactor.ps1` | supporting validation wrapper | Use directly only for focused legacy validation. Prefer launcher modes for normal flow. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | launcher-internal/supporting adapter | Usually called by launcher or task wrapper; not a standalone run-unica or 0-to-10 entrypoint. |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | launcher-internal/supporting advisory wrapper | Provider/advisory implementation lane for `Full0To10` or explicit provider modes. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | launcher-internal/supporting provider/probe wrapper | Provider/probe implementation lane for `Full0To10` or explicit provider modes. |
| `Tools/workflow/run_docs_md_refactor_10min.ps1` | legacy/superseded helper | Prefer unified launcher `md` mode. Do not document as active start path. |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | supporting task wrapper | Useful for task-scoped adapter runs; not a replacement for the run unica. |
| `Tools/workflow/startup_preflight.ps1` | diagnostic-only | Startup/preflight helper. |
| `Tools/workflow/startup_check.py` | diagnostic-only | Startup check helper. |

Full owner boundaries live in:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
```

## Run-unica helper rule

Helpers may support the run-unica flow, but they must not redefine it.

A helper is non-compliant if it:

```text
turns quick Full0To10 into a partial run
omits a run-unica lane without an explicit No* disabler, unavailable diagnostic, dry-run planned state or visible warning
runs provider diagnostics outside Full0To10/provider-selected controls
hides runtime broker telemetry
hides runtime capability manifests
hides full toolbox telemetry summary
hides CSV/count evidence surfaces when inventory lanes run
hides discovery/index repair visibility when relevant
hides file-line-limit visibility when maintainability is in scope
bypasses the shared AI-to-AI bundle
turns a smoke helper into evidence for a run-unica Full0To10 run
```

`TUTTO SU TUTTO` remains owned by the unified launcher and its contract. Helper scripts may adjust implementation details, but they cannot narrow the run-unica semantic perimeter.

## Promotion rule

A helper can become part of the active flow only if the unified launcher records it visibly.

Required surfaces:

```text
launcher parameter or selected mode
phase_status entry
phase_reports entry when a report is produced
manifest field for any provider/memory/patch/evidence behavior
runtime telemetry or capability manifest when broker/tool execution is involved
CSV/JSON/Markdown evidence surface when inventory/discovery/count behavior is involved
file-line-limit report when maintainability is in scope
runbook mention in unified-local-ai-refactor-launcher.md
contract mention in UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md when manifest shape changes
```

No helper may become a hidden side-channel for provider execution, SQLite writes, patch application, evidence generation, index regeneration or git push.

## Telemetry and capability rule

Any helper that executes tools, probes providers, contributes evidence, builds patch specs or participates in run-unica handoff must make its output machine-readable.

Acceptable surfaces:

```text
unified manifest phase_status
unified manifest phase_reports
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
CSV/JSON/Markdown inventory or discovery reports when relevant
file-line-limit report when relevant
```

Future AI agents must be able to answer:

```text
what executed
what failed
what was blocked
what was intentionally disabled
what provider/tool capability was available
what was degraded
what discovery/index/count surface was produced or skipped
whether maintainability/file-line evidence was produced or skipped
whether source writes or patch application happened
```

File existence alone is not sufficient evidence.

## Large Markdown rule

Current policy owners:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/md-split-folder-naming-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/obsolete-monolithic-docs-review-2026-05-07.md
```

A helper policy, tool README or generated report that is too large to be reliably opened must not become a primary operational entrypoint.

Large files may remain as:

```text
catalog/reference
historical/supporting material
generated evidence with compact manifest/summary
application-domain documentation
forensic material
```

If a helper adds a large report or README, it must also add compact manifest/summary visibility.

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
must not be documented as the default run-unica path
must not hide provider execution or patch application
must not bypass telemetry/capability reporting when executing tools
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
manifest -> phase reports -> telemetry/capability surfaces when relevant -> git diff/status -> explicit operator approval -> push
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
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

If it becomes part of the unified launcher, also update:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

If it becomes part of `Full0To10` / run unica, also update the current perimeter docs:

```text
AGENTS.md
README.md
WORKFLOW.md
docs/DATA_FLOW.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Do not add new current behavior to historical/reference docs unless they are first reclassified as active.

## Audit command

Use script inventory before promoting or deleting helpers. Commands live in the unified launcher runbook and validator map.

Preferred evidence surfaces:

```text
script inventory JSON/CSV/MD
Python line-count CSV/MD
function/class/method inventory CSV
Markdown inventory JSON/MD for docs affected by helper policy
file-line-limit JSON/MD when maintainability is in scope
```

Do not commit `output/**` inventory outputs directly; promote compact evidence only when needed.

## Stop conditions

Stop if a proposed documentation/example change would:

```text
make a push-capable helper look like the default workflow
hide a provider execution path
hide patch application
hide git branch/remote target
hide telemetry or capability reporting for executed tools
hide CSV/count or discovery/index surfaces introduced by a helper
hide file-line-limit surfaces when maintainability is in scope
promote a GUI/shell helper above the unified launcher
remove a script reference without confirming the script is absent or obsolete
create a new parallel active-start runbook instead of extending the unified launcher
narrow Full0To10 coverage through a helper-specific shortcut
turn a too-large helper README/report into a primary operational entrypoint
```

## Acceptance criteria

```text
unified launcher remains canonical
supporting helpers are visible but not over-promoted
push-capable helpers have explicit risk warnings
diagnostics are separated from normal validation
script inventory is the source for broad helper audits
helpers wired into launcher are visible in manifest/status/report surfaces
helpers executing tools expose telemetry/capability surfaces when relevant
helpers producing inventory/discovery/count outputs expose CSV/JSON/Markdown summaries
helpers producing maintainability evidence expose file-line-limit summaries when relevant
no helper narrows TUTTO SU TUTTO run-unica coverage
large helper docs/reports have compact bridges or are marked catalog/evidence/supporting
no helper is deleted without explicit approval
```
