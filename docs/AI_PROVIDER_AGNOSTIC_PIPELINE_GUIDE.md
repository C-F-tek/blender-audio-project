# AI Provider-Agnostic Pipeline Guide

## Purpose

This guide describes how AI pipeline work should remain reusable across providers, runtimes and projects.

It is architectural guidance, not a command catalog. Current operator commands and flow ownership live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Design goal

The project should support multiple execution targets without coupling orchestration to one provider:

```text
run-unica launcher
  -> pipeline orchestration
  -> provider interface or provider execution plan
  -> provider implementation when selected and permitted
  -> normalized diagnostics
  -> validation report
  -> runtime telemetry and capability context
  -> discovery/index/CSV-count/file-line context when relevant
  -> shared AI-to-AI bundle / patch-plan handoff
  -> downstream application workflow only when explicitly scoped
```

Core pipeline code should not assume a single model runtime such as OpenVINO, Ollama, an OpenAI-compatible API, local Python, cloud-only runtime, NPU-only runtime or GPU-only runtime.

## Run-unica provider doctrine

Provider-agnostic does not mean provider-invisible.

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
LightFull0To10 = evidence-only profile, not provider/runtime proof
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
CSV/index/discovery/file-line-limit surfaces = evidence lanes when relevant
```

When provider output influences evidence, recommendations, patch plans or patch specs, the handoff must preserve provider state through telemetry/capability/bundle surfaces.

Required state signals include:

```text
provider_advisory_state
provider_failure_detected
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
workload_quality_routing_ok
quality_gate_passed
runtime tool usage telemetry when tools execute
runtime/hardware capability manifest when capability matters
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/count summaries when inventory lanes ran
file-line-limit report when maintainability is in scope
discovery/index repair reports when relevant
```

Telemetry is the completeness accessory. It does not replace provider artifacts or validation reports.

## Local application areas

| Area | Expected role |
|---|---|
| `Tools/ai/pipeline/` | Modular AI artifact pipeline. |
| `Tools/npu/pipeline/` | App-agnostic NPU helper contracts and provider-free staging helpers. |
| `Tools/ai/full0to10_provider_execution_bridge/*` | Provider execution bridge planning/gating/readiness artifacts. |
| `Tools/ai/full0to10_final_product/*` | Final tool-product package: product Markdown, evidence index, readiness, manifest and README. |
| `Tools/ai/build_workload_quality_lane_routing.py` | Quality-based advisory routing. |
| `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | Provider/broker/GPU/NPU/patch-plan telemetry summary. |
| `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | Production AI-to-AI handoff bundle. |
| `Tools/validation/check_file_line_limits.py` | Report-only line-budget evidence for maintained docs/source files. |
| `Tools/validation/` | Non-invasive validation layer for generated outputs and package structure. |

Use the owner map before adding or bypassing scripts.

## Required boundaries

### Orchestration layer

The orchestration layer decides:

```text
which stage runs
which input artifact is consumed
which output artifact is expected
which validator must run
how failures are reported
how provider/telemetry state is surfaced
how discovery/index/CSV-count/file-line state is surfaced when relevant
```

It should not contain provider-specific inference code.

### Provider layer

The provider layer may contain:

```text
OpenVINO/NPU invocation
Ollama invocation
OpenAI-compatible API invocation
local stub or fixture providers
dry-run providers
```

Provider results must be normalized before entering artifact validation, telemetry summary or bundle handoff.

### Provider bridge layer

Provider bridge/gate/readiness evidence is not proof of model execution by itself. A real provider run must set explicit execution state and must not reuse non-executing bridge evidence as runtime proof.

### Artifact layer

Artifacts should be provider-independent and include:

```text
schema version
source input references
generated output path
validation status
warnings and errors
target files if patch-related
safe write plan if file generation is involved
provider/telemetry companion references when run-derived
discovery/index/CSV-count/file-line companion references when repository-wide evidence is involved
```

## Recommended pipeline stages

```text
1. collect source inputs
2. build compact context
3. select provider, provider plan or dry-run mode
4. generate model output only when explicitly selected and permitted
5. normalize raw output and diagnostics
6. parse structured output
7. validate schema
8. validate repository paths
9. validate file-line impact when maintainability is in scope
10. validate Blender compatibility only when explicitly scoped
11. write artifact to safe output location
12. generate report
13. attach telemetry/capability context for run-unica handoff
14. attach discovery/CSV/index/file-line context when relevant
15. update status only after validation succeeds
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

Fallback providers are allowed only when the report clearly states that fallback happened. Run-unica handoff must expose fallback/degradation in telemetry and AI-to-AI bundle state.

## Runtime-agnostic implementation rules

- Do not hard-code workstation paths inside reusable pipeline modules.
- Do not hard-code one model name into core orchestration.
- Keep provider configuration serializable.
- Keep dry-run and fixture modes available for tests.
- Keep JSON parsing and validation outside provider code.
- Keep generated Python policy checks separate from generation.
- Keep Blender runtime execution separate from artifact planning.
- Keep provider bridge/gate/readiness evidence separate from real provider execution proof.
- Keep reusable `Tools/npu/pipeline/` helper contracts provider-free.
- Keep telemetry/capability context separate from provider implementation but attached to run-unica handoff.
- Keep discovery/index/CSV-count/file-line context separate from provider implementation but attached when repository visibility or maintainability matters.
- Keep maintained source files compact through responsibility-based modules.

## Good local pattern

```text
StageConfig
  -> ProviderDescriptor or ProviderExecutionPlan
  -> ProviderResult when real execution is explicitly permitted
  -> ArtifactNormalizer
  -> SchemaValidator
  -> RepositoryPathValidator
  -> FileLineImpactReport when relevant
  -> ArtifactWriter
  -> ValidationReport
  -> Telemetry/Capability companion when used in run-unica evidence
  -> Discovery/CSV/Index/File-line companion when repository visibility or maintainability is part of the evidence
```

## Bad local pattern

```text
single script
  -> hard-coded model
  -> hard-coded paths
  -> model output directly written as code
  -> no schema validation
  -> no report
  -> no telemetry/capability context
  -> no discovery/index/CSV/file-line context
  -> treats bridge/readiness output as real provider execution
  -> grows beyond line-budget policy without split/refactor plan
```

## Acceptance criteria for new pipeline modules

A new pipeline module is acceptable only if it:

```text
has a narrow responsibility
can be imported without running inference
can be tested with fixtures or dry-run data
does not mutate source files on import
reports errors structurally
integrates with existing validators where possible
is documented in the relevant README or docs file
stays within line-budget policy or is split by responsibility
exposes manifest/report/telemetry/bundle visibility when promoted into run-unica
clearly distinguishes plan/gate/readiness evidence from actual provider execution
```

## Validation ownership

Focused direct validation is appropriate only when changing provider-agnostic modules or validators themselves. Broad local-AI validation should route through the unified launcher.

Validation cycle selector:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Migration strategy

When converting an existing script into reusable pipeline logic:

```text
1. read source and current owner maps
2. document current behavior
3. extract pure helpers first
4. add fixture-based validation
5. keep the old entrypoint stable
6. add an adapter layer
7. run focused validation
8. update docs and status markers
9. add telemetry/capability/bundle references if entering run-unica
10. only then consider runtime wiring
```

Do not claim Full0To10 success from provider-agnostic dry-runs alone.
