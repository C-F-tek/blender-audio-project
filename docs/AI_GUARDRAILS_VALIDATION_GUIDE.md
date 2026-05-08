# AI Guardrails and Validation Guide

## Purpose

Policy guide for guardrails, schema validation and evaluation-style workflows applied to AI-generated artifacts in this repository.

This is guidance, not a command catalog. Current validation routing lives in:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
Tools/validation/README.md
```

## Core rule

AI-generated output is not accepted because it looks plausible. It is accepted only after it passes relevant local contracts and its execution context is visible.

For this project:

```text
model/tool output
  -> parse
  -> normalize
  -> schema validation
  -> path validation
  -> file-line-limit visibility when maintainability is in scope
  -> generated Python / Blender compatibility validation when relevant
  -> report
  -> manifest/phase visibility when part of launcher flow
  -> telemetry/capability companion when tools/providers/patch plans are involved
  -> shared AI-to-AI bundle when part of production handoff
```

## Full-run guardrail doctrine

`Full0To10` is **TUTTO SU TUTTO**.

A full-run artifact, recommendation, evidence bundle, patch plan or patch spec is incomplete unless the handoff carries telemetry/capability context needed to interpret it.

Guardrails must prevent these false positives:

```text
artifact exists -> therefore success
patch plan exists -> therefore safe to apply
provider report exists -> therefore provider succeeded
NPU smoke passed -> therefore NPU is advisory-ready
dry-run matrix passed -> therefore Full0To10 passed
reviewed patch spec exists -> therefore queued/apply is authorized
historical limitation note exists -> therefore skip current tool lane
```

## Validation owner map

Do not create duplicate validators when an owner exists.

```text
Python syntax -> Tools/validation/check_python_syntax.py
report contracts -> Tools/validation/check_validation_report_contract.py
docs links -> Tools/validation/check_docs_links.py
file line limits -> Tools/validation/check_file_line_limits.py
patch suggestion product separation -> Tools/validation/check_patch_suggestion_product_separation.py
patch suggestion smoke -> Tools/validation/run_patch_suggestion_bundle_apply_smoke.py
runtime broker smoke -> Tools/validation/run_agent_runtime_tool_broker_smoke.py
peer exchange contract -> Tools/validation/check_ai_peer_exchange_contract.py
provider evidence contract -> Tools/validation/check_provider_evidence_contract.py
```

Current focused cycles live in:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Required validation dimensions

### 1. Syntax validity

Generated JSON must parse as JSON. Generated Python must pass syntax checks before it is considered usable.

### 2. Schema conformance

Generated artifacts should declare or imply a schema version and satisfy required fields.

Minimum expected fields for AI artifacts usually include:

```text
schema_version
source_inputs
stage
status
output_path or planned_output_path
validation
errors
warnings
```

Patch-related artifacts should also include:

```text
target_files
safe_write_plan
review_notes
manual_review_only
patch_application_performed
source_writes_performed
```

Full-run-derived artifacts should reference companion handoff surfaces:

```text
runtime_tool_usage_telemetry
runtime_or_hardware_capability_manifest
full_toolbox_run_telemetry_summary
shared_ai_to_ai_bundle_or_final_summary
file_line_limit_report when maintainability is in scope
```

### 3. Repository path safety

Generated artifact paths must be checked before file writes.

Rules:

```text
do not write outside the repository root
do not overwrite raw frame-by-frame analysis JSON files
prefer output/, indexAI/patch_library/, Scripting/v61b/hotpatch/ or explicit safe folders
use patch specs for mechanical edits when reviewability matters
never treat output/** or SQLite DB files as Git-tracked handoff artifacts
```

### 4. Blender compatibility

Blender/audio/media runtime is application-domain work and must not be triggered by normal AI/tooling validation.

Hard known Blender rule:

```text
Do not use ShaderNodeTexMusgrave for Blender 5.x.
```

### 5. Telemetry and capability validation

When tools, broker calls, provider lanes or patch plans participate in a production handoff, inspect companion surfaces:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md or runtime_hardware_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
file_line_limit_report.json/md when maintainability is in scope
```

Required questions:

```text
which tools executed
which failed
which were blocked
which capabilities were available
which provider lanes degraded
whether deterministic recovery was used
whether source writes happened
whether patch application happened
which docs/source files exceed policy when maintainability is in scope
```

## Guardrail failure behavior

A failed validation must produce a structured failure, not a silent fallback.

Provider fallback or deterministic recovery must also be visible in telemetry/bundle summaries when relevant.

## Evaluation-style workflow

For repeatable AI work, prefer a small fixture/eval set:

```text
input fixture
  -> expected artifact shape
  -> validation command owner
  -> report path
  -> pass/fail result
  -> telemetry/capability companion when artifact joins full-run handoff
```

Good future locations:

```text
Tools/ai/fixtures/
Tools/validation/fixtures/
output/validation/
docs/EXECUTION_PLANS/
```

## Acceptance checklist

An AI artifact is acceptable when:

```text
it parses successfully
it matches the expected contract
it has explicit errors/warnings fields
it does not target unsafe paths
it does not require unapproved dependencies
it has a validation report
it states unresolved uncertainty
it does not bypass existing owners/workflows
it has telemetry/capability companion context when it feeds full-run evidence or patch-plan lanes
```

## Non-goals

This guide does not require importing Guardrails, Promptfoo, DeepEval or OpenAI Evals as project dependencies.

Those tools provide useful concepts. The repository should first enforce its own contracts with local validators and add external dependencies only after explicit review.
