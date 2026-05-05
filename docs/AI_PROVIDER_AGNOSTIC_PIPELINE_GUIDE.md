# AI Provider-Agnostic Pipeline Guide

## Purpose

This guide describes how AI pipeline work should remain reusable across providers, runtimes and projects.

It translates runtime-agnostic and agent-engineering references into local rules for `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, validators and future generated artifacts.

This document is architectural guidance, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large validator/tool catalogs such as `Tools/validation/README.md` are references only and must not become primary operational entrypoints if too large or truncated.

## Design goal

The project should support multiple execution targets without coupling orchestration to one provider:

```text
run-unica launcher
  -> pipeline orchestration
  -> provider interface
  -> provider implementation
  -> normalized provider diagnostics
  -> validated artifact/evidence
  -> runtime telemetry and capability context
  -> discovery/index/CSV-count context when repository visibility is involved
  -> shared AI-to-AI bundle / patch-plan handoff
  -> downstream application workflow when explicitly scoped
```

Core pipeline code should not assume that the model is always:

- OpenVINO;
- Ollama;
- OpenAI-compatible API;
- local Python only;
- cloud-hosted only;
- NPU-only;
- GPU-only.

## Run-unica provider doctrine

Provider-agnostic does not mean provider-invisible.

Current doctrine:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
```

When provider output influences run-unica evidence, recommendations, patch plans or patch specs, the handoff must preserve provider state through telemetry/capability/bundle surfaces:

```text
provider_advisory_state
provider_failure_detected
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
workload_quality_routing_ok
quality_gate_passed
runtime tool usage telemetry when tools execute
runtime capability manifest when tool capability matters
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
```

Telemetry is the completeness accessory. It does not replace provider artifacts or validation reports; it explains whether provider lanes executed, failed, degraded, were blocked, were disabled, unavailable or planned-only.

`Full0To10` remains **TUTTO SU TUTTO**. A provider-specific wrapper or dry-run cannot narrow run-unica scope or serve as proof that the full run passed.

## Local application areas

| Area | Expected role |
|---|---|
| `Tools/ai/pipeline/` | Main modular AI artifact pipeline. |
| `Tools/npu/pipeline/` | App-agnostic NPU helper contracts and provider-free staging helpers. |
| `Tools/ai/build_workload_quality_lane_routing.py` | Quality-based advisory routing. |
| `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | Provider/broker/GPU/NPU/patch-plan telemetry summary. |
| `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | Production AI-to-AI handoff bundle. |
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
- how failures are reported;
- how provider/telemetry state is surfaced into the launcher manifest and bundle;
- how discovery/index/CSV-count state is surfaced when repository visibility is involved.

It should not contain provider-specific inference code.

### Provider layer

The provider layer may contain:

- OpenVINO/NPU invocation;
- Ollama invocation;
- OpenAI-compatible API invocation;
- local stub/dry-run providers;
- fixture-based test providers.

Provider results must be normalized before entering artifact validation, telemetry summary or bundle handoff.

### Artifact layer

The artifact layer should be provider-independent.

Expected artifact properties:

- explicit schema version;
- source input references;
- generated output path;
- validation status;
- warnings and errors;
- target files, if patch-related;
- safe write plan, if file generation is involved;
- provider/telemetry companion references when derived from a run-unica execution;
- discovery/index/CSV-count companion references when derived from repository-wide evidence.

## Recommended pipeline stages

```text
1. collect source inputs
2. build compact context
3. select provider or dry-run mode
4. generate model output when explicitly requested or selected by Full0To10/provider lanes
5. normalize raw output and diagnostics
6. parse JSON or structured text
7. validate schema
8. validate repository paths
9. validate Blender compatibility when explicitly scoped
10. write artifact to safe output location
11. generate report
12. attach telemetry/capability context when part of run-unica handoff
13. attach CSV/index/discovery context when repository visibility is part of the evidence
14. update status only after validation succeeds
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

Fallback providers are allowed only when the report clearly states that fallback happened. Run-unica handoff must also expose fallback/degradation in telemetry and AI-to-AI bundle state.

## Runtime-agnostic implementation rules

- Do not hard-code workstation paths inside reusable pipeline modules.
- Do not hard-code one model name into core orchestration.
- Keep provider configuration serializable.
- Keep dry-run and fixture modes available for tests.
- Keep JSON parsing and validation outside provider code.
- Keep generated Python policy checks separate from generation.
- Keep Blender runtime execution separate from artifact planning.
- Keep NPU helper package provider-free until a validated migration phase wires it into runtime execution.
- Keep telemetry and capability context separate from provider implementation but attached to run-unica handoff.
- Keep discovery/index/CSV-count context separate from provider implementation but attached when repository visibility affects recommendations or patch plans.

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
  -> Telemetry/Capability companion when used in run-unica evidence
  -> Discovery/CSV/Index companion when repository visibility is part of the evidence
```

## Bad local pattern

```text
single script
  -> hard-coded model
  -> hard-coded paths
  -> model output directly written as code
  -> no schema validation
  -> no report
  -> no telemetry/capability context for downstream patch plan
  -> no discovery/index/CSV context for repository-wide recommendations
```

## Acceptance criteria for new pipeline modules

A new pipeline module is acceptable only if it:

- has a narrow responsibility;
- can be imported without running inference;
- can be tested with fixtures or dry-run data;
- does not mutate source files on import;
- reports errors structurally;
- integrates with existing validators where possible;
- is documented in the relevant README or docs file;
- exposes manifest/report/telemetry/bundle visibility when promoted into the run-unica perimeter;
- exposes discovery/index/CSV-count visibility when it affects repository-wide inventory or refactor/reuse planning.

## Validation ownership

Use focused validation before broad workflows, but keep command ownership in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Focused direct validation is appropriate only when changing provider-agnostic pipeline modules or validators themselves. Broad local-AI validation should route through the unified launcher.

## Migration strategy

When converting an existing script into reusable pipeline logic:

1. document the current behavior;
2. extract pure helpers first;
3. add fixture-based validation;
4. keep the old entrypoint stable;
5. add an adapter layer;
6. run focused validation;
7. update docs and status markers;
8. add telemetry/capability/bundle references if the module enters run-unica evidence;
9. add discovery/index/CSV references if the module affects repository-wide visibility;
10. only then consider wiring the new module into runtime flow.

Do not claim run-unica Full0To10 success from provider-agnostic dry-runs alone.
