# Recent telemetry state — 2026-05-05

## Status

Doc-only historical-recent telemetry summary for PR #187 and branch `codex/unified-local-ai-refactor-launcher`.

This file summarizes recent committed compact telemetry/evidence. It does not replace the runtime bundle for run `20260505-143844`.

## Current phase relationship

The current active phase remains:

```text
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

This note provides recent baseline context from earlier same-day runs so future agents do not reopen already-validated issues.

## Recent telemetry baseline

### Run 20260505-073332

Committed telemetry summary:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260505-073332.md
```

Observed state:

```text
passed=true
recommendation_count=5
patch_plan_count=5
provider_execution_performed=true
patch_application_performed=false
source_writes_performed=false
```

Runtime tool usage:

```text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-073332.md
```

Observed broker/bootstrap state:

```text
tool_call_entries=3
executed_count=3
failed_count=0
blocked_count=0
caller=orchestrator
phase=explicit_runtime_tool_broker_bootstrap
executed tools:
  - check_python_syntax
  - build_python_line_count_csv
  - check_validation_report_contract
declared_runtime_tool_requests=136
declared_not_executed_count=136
```

Operational interpretation:

```text
The broker telemetry preservation fix is validated for bootstrap broker evidence.
The declared provider/runtime tool request count is advisory/declarative and not equal to broker executions.
Use executed_count/failed_count/blocked_count and broker_reports to reason about actual tool execution.
```

### Run 20260505-081141

Committed telemetry summary:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260505-081141.md
```

Observed state:

```text
passed=true
recommendation_count=3
patch_plan_count=3
provider_execution_performed=true
patch_application_performed=false
source_writes_performed=false
```

Top patch targets were documentation-only:

```text
docs/AI_ONBOARDING.md
docs/AI_REFERENCE_ONBOARDING.md
docs/AI_REFERENCE_SOURCE_MAP.md
```

Runtime tool usage:

```text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-081141.md
```

Observed broker/bootstrap state:

```text
tool_call_entries=3
executed_count=3
failed_count=0
blocked_count=0
caller=orchestrator
phase=explicit_runtime_tool_broker_bootstrap
executed tools:
  - check_python_syntax
  - build_python_line_count_csv
  - check_validation_report_contract
declared_runtime_tool_requests=72
declared_not_executed_count=72
```

Shared bundle evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_20260505-081141.md
```

Observed bundle state:

```text
patch_plan_summary_seen=true
provider_execution_seen=true
local_provider_probe passed=false
local_provider_probe error=ollama: probe failed
ai_workload_report_quality passed=true
usable_lanes=['npu']
agent_review_patch_plan passed=true
patch_plan_count=3
fallback_used=false
manual_review_required=true
provider_execution_performed=false for patch plan itself
patch_application_performed=false
source_writes_performed=false
runtime_tool_usage_telemetry present and passed
runtime_tool_capability_manifest present and passed
repository_consistency_map present and passed
repository_consistency_map_smoke present and passed
```

Operational interpretation:

```text
Provider degradation is visible and recovered/quality-gated; it is not a reason by itself to rerun.
Patch planning stayed review-only.
The 081141 patch recommendations were documentation/reference hygiene, not runtime refactor.
The current 143844 refactor/reuse runtime bundle must be inspected separately before selecting code/helper refactor patches.
```

## GPU/NPU timing interpretation

Both 073332 and 081141 telemetry summaries include the operational opinion that NPU should remain sampled/advisory and that GPU timing was inferred.

A later smoke validation in PR #187 established that `Tools/ai/gpu_npu_run_sync_analysis/cli.py` now prefers real `rounds[*].elapsed_seconds` samples when present.

Documentation implication:

```text
Do not treat old inferred GPU timing as current analyzer behavior for newly generated reports.
For new reports, inspect round_duration_source and round_duration_sample_count before making timing claims.
```

## What is closed

```text
Broker telemetry loss from run 20260505-002508 is closed unless a new regression appears.
Provider diagnostic degradation is expected to be visible and quality-gated, not hidden.
Patch application remains false across these recent evidence surfaces.
Source writes remain false across these recent evidence surfaces.
```

## What remains active

```text
Read the 20260505-143844 refactor/reuse runtime bundle.
Inspect manifest, decision loop, recommendations, patch plan, telemetry, capability manifest, full toolbox telemetry summary, shared AI-to-AI bundle, provider diagnostics and workload quality.
Classify patch plans into SAFE_MECHANICAL, MANUAL_REVIEW, LOCAL_VALIDATION_REQUIRED, BLENDER_RUNTIME_REQUIRED, PROVIDER_VALIDATION_REQUIRED, DEFER or DO_NOT_PROMOTE.
Select only review-first source/docs changes after evidence review.
```

## Guardrails for future agents

```text
Do not infer success from file existence alone.
Do not rerun providers only because Ollama probe degraded in a past bundle.
Do not apply patch specs automatically.
Do not commit output/**, indexAI/code_chunks/**, *.db, *.sqlite or renders/**.
Do not run Blender or FFmpeg during documentation/refactor planning.
Do not promote Blender/FFmpeg/Git-write/provider-execution tools to broker defaults.
```
