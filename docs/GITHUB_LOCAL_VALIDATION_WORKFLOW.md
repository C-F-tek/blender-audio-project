# GitHub Local Validation Workflow

## Purpose

Local Git/GitHub review lifecycle after AI-assisted refactoring, documentation updates or pipeline changes.

This is policy and review guidance, not a command catalog. Current commands and flow ownership live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Primary rule

Use the unified launcher as the primary local validation and local-AI orchestration entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Supporting wrappers are implementation lanes or focused debugging targets, not first entrypoints.

## Run-unica validation doctrine

```text
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = phase diagnostic only
```

A broad validation proof is incomplete if it only says files exist or that a focused dry-run passed. Review manifest, phase reports, telemetry, capability, evidence and bundle surfaces together.

## Recommended lifecycle

```text
pull latest
confirm branch and dirty state
choose unified launcher mode or focused validator cycle
run focused validation or Full0To10 through the owning entrypoint
inspect manifest-first outputs
inspect telemetry/capability/final-summary when relevant
inspect CSV/count, file-line-limit and discovery/index summaries when relevant
promote only compact evidence when needed
commit intended docs/source changes
push results
share manifest/reports/telemetry for review
```

## Manifest-first inspection

Primary run artifact:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

Review order:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
runtime tool usage telemetry when tools/broker lanes ran
runtime/hardware capability manifest when capabilities matter
full toolbox telemetry summary for run-unica handoff
shared AI-to-AI bundle/final summary for production handoff
compact Markdown, CSV/count or file-line-limit summaries
discovery/index repair reports when relevant
detailed evidence only when needed
```

Do not begin review from a long evidence bundle, oversized Markdown catalog or historical handoff.

## Validation routing

| Need | Preferred route |
|---|---|
| Docs-only change | `validator-smoke-cycle-map` Cycle A. |
| Python/script change | `validator-smoke-cycle-map` Cycle B. |
| Launcher/workflow change | `validator-smoke-cycle-map` Cycle C plus manifest inspection. |
| Provider mesh change | `validator-smoke-cycle-map` Cycle D. |
| Patch suggestion/review PR change | `validator-smoke-cycle-map` Cycle E. |
| Context/memory/index change | `validator-smoke-cycle-map` Cycle F. |
| Real full product run | unified launcher `-Full0To10`. |
| Single phase diagnostic | unified launcher with `-NoStrictRealRunActivation`. |

Focused validation is not proof that `Full0To10` passed.

## Supporting wrappers

These scripts remain available only as implementation lanes or focused debugging targets:

```text
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/workflow/run_npu_pipeline_helper_validation.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
```

Policy:

```text
Do not document them as primary local validation commands.
Do not use them as run-unica substitutes.
If launcher delegates to them, their outputs must be visible in the launcher manifest.
```

## Report review

Primary fields to check in the unified manifest:

```text
mode
mode_name
full_0_to_10_requested
run_intensity
provider_execution_requested
primary_provider_requested
workload_quality_routing_ok
quality_gate_passed
memory_in_enabled
memory_out_enabled
patch_specs_requested
patch_application_performed
phase_status
phase_reports
context_files
report_files
errors
warnings
```

Companion telemetry/final-summary fields to check when available:

```text
tool_call_entry_count
executed_count
failed_count
blocked_count
broker_reports
runtime/hardware capability manifest path
provider_advisory_state
provider_failure_detected
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
gpu_metrics_source
round_duration_source
source_writes_performed
patch_application_performed
```

## Evidence policy

Because `output/` is ignored, promote only compact evidence files under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Do not bulk-add the whole evidence directory. Add only reviewed evidence files that directly support the PR.

Do not commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw provider outputs
unreviewed generated indexes
indexAI/code_chunks/**
```

## Index and generated-output policy

Generated indexes are not source-of-truth docs. Do not hand-edit generated chunks or manifests.

`indexAI/code_chunks/**` and `indexAI/project_code_chunks/**` must not be committed as ordinary source.

Index repair is plan/report-first unless explicitly requested.

## File-size policy

Maintained files must remain compact:

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split layout is exact:

```text
path/name.md
path/name.md/part-001.md
```

Policies:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/md-split-folder-naming-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

## Git change inspection

Before committing, inspect:

```text
git status
git diff --stat
git diff --check
```

If validation produced only local output reports, they should normally remain uncommitted.

If source files changed unexpectedly, stop and review before committing.

## PR report contract

A PR should state:

```text
summary
scope
changed files
launcher mode/parameters/flags or focused validator used
manifest path when available
phase reports/evidence paths when available
runtime telemetry/capability/final-summary paths when relevant
discovery/index/CSV/file-line evidence when relevant
provider execution statement
patch application statement
source writes statement
risk notes
follow-up
```

For docs/workflow-state cleanup PRs, explicitly state:

```text
No runtime files, provider behavior, generated indexes, full analysis JSON, Blender scripts or audio/media outputs touched.
```

## Troubleshooting policy

When a focused validator, NPU helper or provider lane fails:

```text
first inspect launcher manifest if the run used the launcher
then inspect telemetry/capability/final-summary surfaces if involved
then inspect discovery/index/CSV/file-line surfaces if relevant
then inspect the focused JSON report
then inspect stderr/logs
then rerun only the failing focused validator/lane if needed
```

Do not jump directly to legacy full wrappers as a workaround.

## Guardrails

Do not push generated indexes before checking validation results.

Do not commit output validation reports unless explicitly needed as compact evidence.

Do not modify Blender runtime packages while validating AI pipeline or NPU helper refactors.

Do not treat push-capable workflow helpers as default validation commands. Push-capable helpers require explicit user intent and visible git status review.

Do not claim a run-unica Full0To10 run passed from dry-run, focused validator, oversized Markdown or file existence alone.

Do not treat historical limitation notes as reasons to skip available tools.
