# GitHub Local Validation Workflow

## Purpose

This document defines the local Git/GitHub review lifecycle after AI-assisted refactoring, documentation updates or pipeline changes.

It is policy and review guidance, not a command catalog. Current executable commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large tool catalogs such as `Tools/validation/README.md` and `Tools/npu/pipeline/README.md` are references only and must not become primary operational entrypoints if too large or truncated.

## Primary rule

Use the unified launcher as the primary local validation and local-AI orchestration entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

The primary model is one parameterized run:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
```

Supporting wrappers may exist, but they are not first entrypoints.

## Run-unica validation doctrine

`Full0To10` means **TUTTO SU TUTTO**.

`quick`, `balanced`, `deep` and `custom` are parameter presets or operator values only. They must not silently narrow scope.

A broad validation proof is incomplete if it only says that files exist or that a focused dry-run passed. When a PR is derived from a run-unica execution, provider lane, broker/tool lane, evidence bundle, recommendation or patch plan, the review must include companion telemetry/capability surfaces and, when relevant, discovery/index/CSV-count surfaces.

Telemetry is a completeness accessory for evidence and patch plans. It does not replace validation reports; it explains whether lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

## Recommended lifecycle

```text
pull latest
choose unified launcher mode/parameters/presets
run focused validation or run-unica Full0To10 flow through launcher
inspect manifest-first outputs
inspect telemetry/capability/final-summary surfaces when relevant
inspect CSV/count and discovery/index summaries when relevant
promote only compact evidence when needed
commit intended docs/source/index changes
push results
share manifest/reports/telemetry for review
```

## Manifest-first inspection

The primary run artifact is:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

Read this before opening long reports.

Review order:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
runtime tool usage telemetry when tools/broker lanes ran
runtime tool capability manifest when capabilities matter
full toolbox telemetry summary for run-unica/production handoff
shared AI-to-AI bundle/final summary for production handoff
compact Markdown or CSV/count summaries
discovery/index repair reports when relevant
detailed evidence only when needed
```

Do not begin review from a long evidence bundle or oversized Markdown catalog.

## Validation routing

| Need | Preferred route |
|---|---|
| Quick docs/source validation | unified launcher quick parameter preset with relevant validation phases |
| Run-unica Full0To10 review | unified launcher Full0To10 with selected presets/parameters |
| Deep provider/repo review | unified launcher Full0To10 with deep/custom parameters; provider/probe lanes included unless disabled/unavailable |
| NPU helper-only work | focused NPU helper validation, then unified launcher full validation if broader scope changed |
| Validator debugging | direct focused validator command from validator catalog/reference |
| GitHub evidence handoff | compact evidence builder through launcher/tool README, never bulk-add raw output |
| Discovery/index/CSV-count review | inventory/chunks/repository-consistency phases through launcher; index repair remains plan/report-first |

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
If their output feeds evidence/patch plans, companion telemetry/capability state must be visible in the handoff.
If they produce inventory/discovery/count artifacts, compact CSV/JSON/Markdown references must be visible in the handoff.
```

## Repository sync preflight

Before local validation, confirm:

```text
current branch
remote sync state
working tree status
whether dirty changes are intentional
Python/venv selected by launcher
ignored output/cache/state files are not staged
```

For PR work, validate on the PR branch unless the task explicitly says to start a new branch from `master`.

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
runtime capability manifest path
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

Discovery/index/CSV-count surfaces to check when relevant:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
Python line-count CSV/MD
function/class/method inventory CSV
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report
index repair plan/report
```

A broad validation run is not acceptable if these surfaces are missing or if selected phases vanish silently.

## Evidence policy

Because `output/` is ignored, promote only compact evidence files under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Do not bulk-add the whole evidence directory. Add only reviewed evidence files that directly support the PR.

When adding run-unica evidence or patch-plan evidence, also include or reference:

```text
runtime telemetry
runtime capability manifest
full toolbox telemetry summary
shared AI-to-AI final summary
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
```

Do not commit:

```text
output/**
renders/**
*.db
*.sqlite
raw provider outputs
unreviewed generated indexes
indexAI/code_chunks/**
```

## Index regeneration

Regenerate generated indexes only when structural source/doc/workflow changes require it and the task explicitly scopes regeneration.

Generated indexes are not source-of-truth docs. Do not hand-edit generated chunks or manifests.

`indexAI/code_chunks/**` must not be committed as ordinary source.

Index repair is plan/report-first unless explicitly requested.

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
discovery/index/CSV-count evidence when relevant
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

## Optional Blender compatibility smoke

Blender-facing validation is application-domain work and must not be silently included in core local-AI validation.

Outside Blender, import/syntax smokes may be run as focused validators. Real Blender runtime validation requires explicit Blender scope.

## Troubleshooting policy

When a focused validator, NPU helper or provider lane fails:

```text
first inspect the launcher manifest if the run used the launcher
then inspect telemetry/capability/final-summary surfaces if involved
then inspect discovery/index/CSV-count surfaces if relevant
then inspect the focused JSON report
then inspect stderr/logs
then rerun only the failing focused validator/lane if needed
```

Do not jump directly to legacy full wrappers as a workaround.

## Guardrails

Do not push generated indexes before checking validation results.

Do not commit output validation reports unless explicitly needed as compact evidence.

Do not modify Blender runtime packages while validating AI pipeline or NPU helper refactors.

Do not wire `Tools/npu/pipeline/` helpers into runtime orchestration until focused NPU helper validation, broad launcher validation, quality gates, telemetry/bundle visibility and index review pass.

Do not treat push-capable workflow helpers as default validation commands. Any push-capable helper must require explicit user intent and visible git status review.

Do not claim a run-unica Full0To10 run passed from dry-run, focused validator, oversized Markdown or file existence alone.
