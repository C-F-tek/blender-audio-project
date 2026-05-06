# AI Guardrails and Validation Guide

## Purpose

This guide defines how guardrails, schema validation and evaluation-style workflows should be applied to AI-generated artifacts in this repository.

It adapts guardrails/evals concepts into local repository rules without adding mandatory external runtime dependencies.

This document is guidance, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

`Tools/validation/README.md` is a validator catalog/reference. Do not treat it as the primary operational entrypoint if it is oversized or truncated.

## Core rule

AI-generated output is not accepted because it looks plausible. It is accepted only after it passes the relevant local contracts and its execution context is visible.

For this project, that means:

```text
model/tool output
  -> parse
  -> normalize
  -> schema validation
  -> path validation
  -> file-line-limit visibility when maintainability is in scope
  -> Blender compatibility validation when relevant
  -> generated Python policy validation when relevant
  -> report
  -> manifest/phase visibility when part of launcher flow
  -> telemetry/capability companion when tools/providers/patch plans are involved
  -> shared AI-to-AI bundle when part of production handoff
```

## Full-run guardrail doctrine

`Full0To10` is **TUTTO SU TUTTO**.

A full-run artifact, recommendation, evidence bundle, patch plan or patch spec is not complete unless the handoff also carries the telemetry/capability context needed to interpret it.

Telemetry is a guardrail accessory. It does not replace schema validation, evidence or patch plans; it explains whether the relevant lanes executed, failed, were blocked, degraded, disabled or planned-only.

Limitations are backlog to overcome, not reasons to skip available tools. A lane/tool is unavailable only when current code, telemetry, capability manifest, provider diagnostic or validator evidence says so.

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

## Local validation assets

| Local asset | Role |
|---|---|
| `Tools/validation/` | Non-invasive validation scripts. |
| `Tools/validation/check_file_line_limits.py` | Report-only 400-line policy validator for maintained docs and source files. |
| `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md` | Compact contract note for the line-limit validator. |
| `docs/JSON_SCHEMAS.md` | Existing JSON schema notes and report contract map; broad catalog only. |
| `docs/AI_ARTIFACT_SCHEMAS.md` | AI artifact, telemetry and bundle schema notes. |
| `docs/QUALITY_GATE.md` | Acceptance rules for generated packages. |
| `Tools/ai/run_pipeline_dry_run_matrix.py` | Repeatable AI pipeline dry-run matrix. Planned-only proof, not full-run proof. |
| `Tools/ai/build_runtime_tool_usage_telemetry.py` | Runtime tool usage telemetry. |
| Runtime/hardware capability manifest builders | Runtime or hardware lane capability and guardrail manifests from current code/evidence. |
| `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | Full-run telemetry summary. |
| `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | Production AI-to-AI bundle. |
| `output/validation/` | Recommended local validation report output folder. Ignored unless compact evidence is promoted. |
| `docs/EXECUTION_PLANS/` | Durable task records for complex validation/refactor work. |

## Required validation dimensions

### 1. Syntax validity

Generated JSON must parse as JSON.

Generated Python must pass syntax checks before it is considered usable.

Command ownership:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

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

Full-run-derived artifacts should also reference the companion handoff surfaces:

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

- do not write outside the repository root;
- do not overwrite raw frame-by-frame analysis JSON files;
- prefer `output/`, `indexAI/patch_library/`, `Scripting/v61b/hotpatch/` or explicit safe folders;
- use patch specs for mechanical edits when reviewability matters;
- never treat `output/**` or SQLite DB files as Git-tracked handoff artifacts.

### 4. Blender compatibility

Generated Blender Python must avoid known incompatible APIs and deprecated node types.

Current hard rule:

```text
Do not use ShaderNodeTexMusgrave for Blender 5.x.
```

Generated scene scripts should preserve:

- audio loading;
- frame range setup;
- FPS setup;
- camera;
- lighting;
- render configuration;
- output path configuration.

Blender/audio/media runtime remains application-domain work and must not be triggered by normal AI/tooling full-run validation.

### 5. Policy validation

Use existing policy validators for generated files. Commands are owned by the unified launcher runbook and compact task docs.

### 6. Telemetry and capability validation

When tools, broker calls, provider lanes or patch plans participate in a production handoff, validate or inspect the companion surfaces:

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
which docs/source files exceed 400 lines when maintainability is in scope
```

## Guardrail failure behavior

A failed validation must produce a structured failure, not a silent fallback.

Recommended report shape:

```json
{
  "status": "failed",
  "stage": "schema_validation",
  "errors": [
    {
      "code": "missing_required_field",
      "field": "target_files",
      "message": "Patch artifact does not declare target files."
    }
  ],
  "warnings": [],
  "artifact_written": false
}
```

Provider fallback or deterministic recovery must also be visible in telemetry/bundle summaries when relevant.

## Evaluation-style workflow

For repeatable AI work, prefer a small fixture/eval set:

```text
input fixture
  -> expected artifact shape
  -> validation command owner
  -> report path
  -> pass/fail result
  -> telemetry/capability companion when the artifact joins full-run handoff
```

Good future locations:

```text
Tools/ai/fixtures/
Tools/validation/fixtures/
output/validation/
docs/EXECUTION_PLANS/
```

## Prompt and artifact regression policy

When a prompt or provider changes, the agent should check:

- whether artifact structure changed;
- whether schema fields are still present;
- whether validation reports still pass;
- whether generated code policy still passes;
- whether paths remain safe;
- whether output quality degraded in obvious ways;
- whether telemetry reports provider degradation or deterministic recovery;
- whether the shared AI-to-AI bundle still carries evidence, patch-plan and telemetry references together;
- whether file-line-limit evidence changed when maintainability is in scope.

## Practical acceptance checklist

An AI artifact is acceptable when:

- it parses successfully;
- it matches the expected contract;
- it has explicit errors/warnings fields;
- it does not target unsafe paths;
- it does not require unapproved dependencies;
- it has a validation report;
- it states unresolved uncertainty;
- it does not bypass existing workflow docs;
- it has telemetry/capability companion context when it comes from or feeds a full-run evidence/patch-plan lane.

## Non-goals

This guide does not require importing Guardrails, Promptfoo, DeepEval or OpenAI Evals as project dependencies.

Those tools provide useful concepts. The repository should first enforce its own contracts with local validators and add external dependencies only after explicit review.
