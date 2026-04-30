# AI Provider-Agnostic Pipeline Guide

## Purpose

This guide describes how AI pipeline work should remain reusable across providers, runtimes and projects.

It translates runtime-agnostic and agent-engineering references into local rules for `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, validators and future generated artifacts.

## Design goal

The project should support multiple execution targets without coupling orchestration to one provider:

```text
pipeline orchestration
  -> provider interface
  -> provider implementation
  -> validated artifact
  -> Blender/script/render workflow
```

Core pipeline code should not assume that the model is always:

- OpenVINO;
- Ollama;
- OpenAI-compatible API;
- local Python only;
- cloud-hosted only;
- NPU-only;
- GPU-only.

## Local application areas

| Area | Expected role |
|---|---|
| `Tools/ai/pipeline/` | Main modular AI artifact pipeline. |
| `Tools/npu/pipeline/` | App-agnostic NPU helper contracts and provider-free staging helpers. |
| `Tools/validation/` | Non-invasive validation layer for generated outputs and package structure. |
| `docs/AI_PIPELINE_ARCHITECTURE.md` | Current architecture map. |
| `docs/AI_PIPELINE_REFACTOR_STATUS.md` | Current status marker. |
| `docs/AI_PIPELINE_OPTIMIZATION.md` | Optimization notes and future work. |

## Required boundaries

### Orchestration layer

The orchestration layer should decide:

- which stage runs;
- which input artifact is consumed;
- which output artifact is expected;
- which validator must run;
- how failures are reported.

It should not contain provider-specific inference code.

### Provider layer

The provider layer may contain:

- OpenVINO/NPU invocation;
- Ollama invocation;
- OpenAI-compatible API invocation;
- local stub/dry-run providers;
- fixture-based test providers.

Provider results must be normalized before entering artifact validation.

### Artifact layer

The artifact layer should be provider-independent.

Expected artifact properties:

- explicit schema version;
- source input references;
- generated output path;
- validation status;
- warnings and errors;
- target files, if patch-related;
- safe write plan, if file generation is involved.

## Recommended pipeline stages

```text
1. collect source inputs
2. build compact context
3. select provider or dry-run mode
4. generate model output
5. normalize raw output
6. parse JSON or structured text
7. validate schema
8. validate repository paths
9. validate Blender compatibility when relevant
10. write artifact to safe output location
11. generate report
12. update status only after validation succeeds
```

## Provider fallback rule

Provider failure must not silently become a valid artifact.

A failed provider stage should return a structured report with:

```text
status: failed
provider: <provider-name>
stage: <stage-name>
error: <short diagnostic>
artifact_written: false
```

Fallback providers are allowed only when the report clearly states that fallback happened.

## Runtime-agnostic implementation rules

- Do not hard-code workstation paths inside reusable pipeline modules.
- Do not hard-code one model name into core orchestration.
- Keep provider configuration serializable.
- Keep dry-run and fixture modes available for tests.
- Keep JSON parsing and validation outside provider code.
- Keep generated Python policy checks separate from generation.
- Keep Blender runtime execution separate from artifact planning.
- Keep NPU helper package provider-free until a validated migration phase wires it into runtime execution.

## Good local pattern

```text
StageConfig
  -> ProviderDescriptor
  -> ProviderResult
  -> ArtifactNormalizer
  -> SchemaValidator
  -> RepositoryPathValidator
  -> ArtifactWriter
  -> ValidationReport
```

## Bad local pattern

```text
single script
  -> hard-coded model
  -> hard-coded paths
  -> model output directly written as code
  -> no schema validation
  -> no report
```

## Acceptance criteria for new pipeline modules

A new pipeline module is acceptable only if it:

- has a narrow responsibility;
- can be imported without running inference;
- can be tested with fixtures or dry-run data;
- does not mutate source files on import;
- reports errors structurally;
- integrates with existing validators where possible;
- is documented in the relevant README or docs file.

## Validation commands

Use focused validation before broad workflows:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

For NPU helper boundaries:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

## Migration strategy

When converting an existing script into reusable pipeline logic:

1. document the current behavior;
2. extract pure helpers first;
3. add fixture-based validation;
4. keep the old entrypoint stable;
5. add an adapter layer;
6. run focused validation;
7. update docs and status markers;
8. only then consider wiring the new module into runtime flow.
