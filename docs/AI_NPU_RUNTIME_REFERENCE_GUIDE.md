# AI NPU Runtime Reference Guide

## Purpose

Project-specific guide for NPU, OpenVINO-style local inference and fallback concepts in IA-Carmine.

This is reference guidance, not a command catalog. Current command, owner and flow maps:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Current project policy

NPU participates in the current architecture as a constrained support lane:

```text
probe/diagnostic lane
non-blocking micro task lane
decode/quality signal lane
lightweight tool-support lane when selected by provider mesh
not heavy audit authority
not primary advisory lane
```

Current source owners:

```text
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/run_npu_gpu_deep_review_auditor.py
Tools/ai/agent_runtime_tool_broker.py
```

`Tools/npu/pipeline/` remains app-agnostic helper/support code unless a validated owner wires it into runtime.

## Hardware role separation

| Device | Preferred project role |
|---|---|
| GPU1 / Ollama / RTX 5080 | Primary advisory planner/worker when provider execution is selected and quality-gated. |
| GPU0 / OpenVINO | Companion peer worker and broker-visible tool-request producer. |
| NPU / OpenVINO | Non-blocking micro/task support, diagnostics, decode-quality and lightweight tool-support lane. |
| CPU | Orchestration, validation, JSON/schema processing, fallback logic and deterministic authority. |

This separation prevents local inference experiments from blocking provider mesh or Blender/application runtime work.

## Full-run NPU doctrine

NPU smoke success is not NPU primary advisory promotion.

In `Full0To10`, NPU state must be visible when selected or available:

```text
unified launcher manifest
phase_status / phase_reports
provider diagnostics
peer exchange / NPU support report when produced
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
```

Telemetry explains whether NPU lanes executed, failed, degraded, were excluded, blocked, disabled or planned-only.

## Runtime-agnostic NPU design

Preferred abstraction:

```text
NpuCapability
  -> ProviderDescriptor
  -> StagePlan
  -> InputBundle
  -> ProviderResult
  -> ValidationReport
  -> Telemetry/Bundle companion when used in full-run evidence
  -> FileLineImpactReport when maintainability is in scope
```

The helper layer may prepare:

```text
config objects
path plans
compact context bundles
provider descriptors
validation contracts
report stubs
migration-readiness reports
```

The helper layer should not perform actual inference unless a specific runtime module is introduced and validated.

## Safe NPU helper scope

Allowed in helper modules:

```text
pure path helpers
JSON/text IO helpers
artifact path planning
context bundle creation
contract validation
provider descriptors
dry-run stage reports
fixture-based tests
migration-readiness gates
```

Not allowed without explicit validated phase:

```text
direct NPU inference calls hidden inside helper code
direct Ollama calls hidden inside helper code
direct Blender runtime modification
automatic provider fallback that hides failures
writing source files from model output
using NPU smoke/decode success as proof of primary advisory readiness
growing maintained NPU helper/source files beyond file-size policy without split/refactor plan
```

## Expected NPU workflow

```text
1. build compact project context
2. prepare input bundle
3. select provider descriptor or planned support lane
4. run provider/probe only through explicit launcher/provider diagnostic path
5. normalize provider output and diagnostics
6. validate structured artifact/report
7. write safe output report
8. carry provider quality and exclusion state into telemetry/bundle handoff
9. include file-line-limit evidence when maintainability is in scope
10. regenerate indexes only after accepted structural changes and explicit local task scope
```

## Failure handling

NPU failures must be explicit.

Recommended report fields:

```text
status
stage
provider
device
error
fallback_used
artifact_written
validation_status
advisory_role
quality_gate_required_before_primary_use
```

Do not convert NPU failure into a successful advisory artifact unless a fallback provider actually produced a validated artifact and the report states fallback was used.

Full-run handoff must preserve relevant failure or exclusion state:

```text
provider_failure_detected
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
npu_excluded_from_primary_advisory
quality_gate_passed
```

## Validation ownership

Focused NPU/helper validation is reference-level. Broad local-AI validation and provider/probe execution are owned by the unified launcher.

Validation selector:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Provider mesh owner map:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
```

Do not use focused NPU helper commands as proof that `Full0To10` passed.

## Migration readiness checklist

Before wiring NPU helpers into runtime code, require:

```text
helper docs updated
helper validators passing
fixture or dry-run reports available
provider boundary documented
fallback behavior documented
telemetry/bundle visibility documented when entering full-run evidence
file-line impact reviewed under active file-size policy
generated indexes regenerated only when explicitly scoped
no Blender runtime behavior changed unintentionally
no source writes from raw model output
quality-gate evidence for any primary advisory promotion
maintainer approval for runtime wiring
```

## Practical advice for AI agents

When asked to improve NPU usage:

```text
inspect current helper contracts first
inspect py_mesh/provider owners before adding scripts
avoid editing runtime orchestrators immediately
add or refine pure helpers first
add validation before integration
document provider boundary
keep NPU as micro/support/diagnostic unless quality evidence promotes it
keep GPU1 advisory explicit and quality-gated
state when local hardware validation is required
attach telemetry/capability/bundle context when NPU affects evidence or patch plans
stay within file-size policy or split by responsibility
```
