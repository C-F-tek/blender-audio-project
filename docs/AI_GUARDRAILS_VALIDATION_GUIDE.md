# AI Guardrails and Validation Guide

## Purpose

This guide defines how guardrails, schema validation and evaluation-style workflows should be applied to AI-generated artifacts in this repository.

It adapts guardrails/evals concepts into local repository rules without adding mandatory external runtime dependencies.

## Core rule

AI-generated output is not accepted because it looks plausible. It is accepted only after it passes the relevant local contracts.

For this project, that means:

```text
model output
  -> parse
  -> normalize
  -> schema validation
  -> path validation
  -> Blender compatibility validation when relevant
  -> generated Python policy validation when relevant
  -> report
```

## Local validation assets

| Local asset | Role |
|---|---|
| `Tools/validation/` | Non-invasive validation scripts. |
| `docs/JSON_SCHEMAS.md` | Existing JSON schema notes and report contract map. |
| `docs/AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes. |
| `docs/QUALITY_GATE.md` | Acceptance rules for generated packages. |
| `Tools/ai/run_pipeline_dry_run_matrix.py` | Repeatable AI pipeline dry-run matrix. |
| `output/validation/` | Recommended validation report output folder. |
| `docs/EXECUTION_PLANS/` | Durable task records for complex validation/refactor work. |

## Required validation dimensions

### 1. Syntax validity

Generated JSON must parse as JSON.

Generated Python must pass syntax checks before it is considered usable.

Recommended command:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
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
```

### 3. Repository path safety

Generated artifact paths must be checked before file writes.

Rules:

- do not write outside the repository root;
- do not overwrite raw frame-by-frame analysis JSON files;
- prefer `output/`, `indexAI/patch_library/`, `Scripting/v61b/hotpatch/` or explicit safe folders;
- use patch specs for mechanical edits when reviewability matters.

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

### 5. Policy validation

Use existing policy validators for generated files:

```powershell
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
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

## Evaluation-style workflow

For repeatable AI work, prefer a small fixture/eval set:

```text
input fixture
  -> expected artifact shape
  -> validation command
  -> report path
  -> pass/fail result
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
- whether output quality degraded in obvious ways.

## Practical acceptance checklist

An AI artifact is acceptable when:

- it parses successfully;
- it matches the expected contract;
- it has explicit errors/warnings fields;
- it does not target unsafe paths;
- it does not require unapproved dependencies;
- it has a validation report;
- it states unresolved uncertainty;
- it does not bypass existing workflow docs.

## Commands

Fast general checks:

```powershell
python .\Tools\validation\check_json_artifacts.py --repo-root . --output .\output\validation\json_artifacts.json
python .\Tools\validation\check_package_structure.py --repo-root . --output .\output\validation\package_structure.json
```

AI pipeline checks:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

NPU helper checks:

```powershell
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
```

## Non-goals

This guide does not require importing Guardrails, Promptfoo, DeepEval or OpenAI Evals as project dependencies.

Those tools provide useful concepts. The repository should first enforce its own contracts with local validators and add external dependencies only after explicit review.
