# GitHub Local Validation Workflow

## Purpose

This document defines the local Git/GitHub review lifecycle after AI-assisted refactoring, documentation updates or pipeline changes.

It is policy and review guidance, not a command catalog. Current executable commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

## Primary rule

Use the unified launcher as the primary local validation and local-AI orchestration entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

All broad validation profiles must be launcher modes/profiles:

```text
quick validation
balanced full run
deep full run
provider/probe run
patch-spec validation
reset planning/full cleanup
full_validation
```

Supporting wrappers may exist, but they are not first entrypoints.

## Recommended lifecycle

```text
pull latest
choose unified launcher mode/profile/intensity
run focused validation or full 0-to-10 flow through launcher
inspect manifest-first outputs
promote only compact evidence when needed
commit intended docs/source/index changes
push results
share manifest/reports for review
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
compact Markdown or CSV summaries
detailed evidence only when needed
```

Do not begin review from a long evidence bundle.

## Validation routing

| Need | Preferred route |
|---|---|
| Quick docs/source validation | unified launcher quick mode/profile with validation phases |
| Full repository 0-to-10 run | unified launcher Full0To10 profile |
| Deep provider/repo review | unified launcher deep profile with explicit provider/probe flags |
| NPU helper-only work | focused NPU helper validation, then unified launcher full validation if broader scope changed |
| Validator debugging | direct focused validator command from `Tools/validation/README.md` |
| GitHub evidence handoff | compact evidence builder through launcher/tool README, never bulk-add raw output |

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
Do not use them as full-run substitutes.
If launcher delegates to them, their outputs must be visible in the launcher manifest.
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

A broad validation run is not acceptable if these surfaces are missing or if selected phases vanish silently.

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
raw provider outputs
unreviewed generated indexes
```

## Index regeneration

Regenerate generated indexes only when structural source/doc/workflow changes require it.

Generated indexes are not source-of-truth docs. Do not hand-edit generated chunks or manifests.

Commit generated indexes only when intentional and useful for review.

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
launcher mode/profile/flags or focused validator used
manifest path when available
phase reports/evidence paths when available
provider execution statement
patch application statement
risk notes
follow-up
```

For docs/workflow-state cleanup PRs, explicitly state:

```text
No runtime files, provider behavior, generated indexes, full analysis JSON or Blender scripts touched.
```

## Optional Blender compatibility smoke

Blender-facing validation is application-domain work and must not be silently included in core local-AI validation.

Outside Blender, import/syntax smokes may be run as focused validators. Real Blender runtime validation requires explicit Blender scope.

## Troubleshooting policy

When a focused validator, NPU helper or provider lane fails:

```text
first inspect the launcher manifest if the run used the launcher
then inspect the focused JSON report
then inspect stderr/logs
then rerun only the failing focused validator/lane if needed
```

Do not jump directly to legacy full wrappers as a workaround.

## Guardrails

Do not push generated indexes before checking validation results.

Do not commit output validation reports unless explicitly needed as compact evidence.

Do not modify Blender runtime packages while validating AI pipeline or NPU helper refactors.

Do not wire `Tools/npu/pipeline/` helpers into runtime orchestration until focused NPU helper validation, broad launcher validation and index review pass.

Do not treat push-capable workflow helpers as default validation commands. Any push-capable helper must require explicit user intent and visible git status review.
