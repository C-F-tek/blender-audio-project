# AI NPU Runtime Reference Guide

## Purpose

This guide explains how NPU, OpenVINO-style local inference and runtime fallback concepts should be applied inside this repository.

It is a project-specific guide for AI agents. It does not replace upstream OpenVINO or hardware documentation.

This document is reference guidance, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large validator/tool catalogs such as `Tools/validation/README.md` are references only and must not become primary operational entrypoints if too large or truncated.

## Current project policy

`Tools/npu/pipeline/` is currently an app-agnostic helper package under staged decomposition.

Until a later validated phase explicitly changes this, AI agents must treat it as:

```text
provider-free
runtime-free
safe to import
focused on contracts, paths, config, IO and planning helpers
```

It must not be wired into runtime orchestrators unless local validation, quality gates, telemetry/bundle visibility, file-line impact review and regenerated indexes are green.

## Hardware role separation

Current project strategy:

| Device | Preferred project role |
|---|---|
| NPU | Probe, guardrail, decode-smoke diagnostic and future promotion candidate only after quality evidence. |
| GPU | Primary advisory lane through Ollama when explicitly requested and quality-gated; also Blender/rendering domain when explicitly scoped. |
| CPU | Orchestration, validation, JSON/schema processing, fallback logic and FFmpeg CPU encoding when application-domain work is explicitly scoped. |

This separation prevents local inference experiments from blocking Blender rendering or corrupting validated pipeline behavior.

## Full-run NPU doctrine

NPU smoke success is not NPU advisory promotion.

In `Full0To10`, NPU/OpenVINO participates as:

```text
probe
guardrail
decode diagnostic
quality/remediation signal
future promotion candidate
```

It must not become a general advisory lane unless a dedicated quality-gated promotion milestone proves usable linguistic output and updates the full-run contract.

When NPU diagnostics contribute to full-run evidence, their state must be visible in:

```text
unified launcher manifest
phase_status / phase_reports
provider diagnostics
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
```

Telemetry is the completeness accessory that explains whether NPU lanes executed, failed, degraded, were excluded, were blocked, were disabled or were planned-only.

Limitations are backlog to overcome, not reasons to skip available NPU/probe/tool lanes.

## Runtime-agnostic NPU design

NPU-related helpers should not assume one fixed provider. They should describe capability and intent.

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

- config objects;
- path plans;
- compact context bundles;
- provider descriptors;
- validation contracts;
- report stubs;
- migration-readiness reports.

The helper layer should not perform actual inference unless a specific runtime module is introduced and validated.

## Safe NPU helper scope

Allowed in helper modules:

- pure path helpers;
- JSON/text IO helpers;
- artifact path planning;
- context bundle creation;
- contract validation;
- provider descriptors;
- dry-run stage reports;
- fixture-based tests;
- migration-readiness gates.

Not allowed without explicit validated phase:

- direct NPU inference calls;
- direct Ollama calls;
- direct Blender runtime modification;
- automatic provider fallback that hides failures;
- writing source files from model output;
- changing `Tools/npu/run_dual_ai_pipeline.py` behavior without local validation;
- using NPU smoke/decode success as proof of advisory readiness;
- growing maintained NPU helper/source files beyond 400 lines without split/refactor plan.

## Expected NPU workflow

```text
1. build compact project context
2. prepare input bundle
3. select planned provider descriptor
4. run provider/probe only through explicit launcher/provider diagnostic path
5. normalize provider output and diagnostics
6. validate structured artifact/report
7. write safe output report
8. carry provider quality and exclusion state into telemetry/bundle handoff when part of full-run evidence
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
quality_gate_required_before_advisory_use
```

Do not convert NPU failure into a successful creative/advisory artifact unless the fallback provider actually produced a validated artifact and the report states that fallback was used.

Full-run handoff must preserve relevant failure or exclusion state:

```text
provider_failure_detected
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
npu_excluded_from_primary_advisory
quality_gate_passed
```

## Integration with existing docs

For NPU helper work, read:

```text
AGENTS.md
WORKFLOW.md
docs/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
Tools/npu/pipeline/README.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
```

## Validation ownership

Focused NPU helper validation is described by:

```text
Tools/npu/pipeline/README.md
```

Broad local-AI validation and provider/probe execution are owned by:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

File-line validation is described by:

```text
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
Tools/validation/check_file_line_limits.py
```

Do not use focused NPU helper commands as proof that `Full0To10` passed.

## Migration readiness checklist

Before wiring NPU helpers into runtime code, require:

- helper docs updated;
- helper validators passing;
- fixture or dry-run reports available;
- provider boundary documented;
- fallback behavior documented;
- telemetry/bundle visibility documented when entering full-run evidence;
- file-line impact reviewed under the 400-line policy;
- generated indexes regenerated only when explicitly scoped;
- no Blender runtime behavior changed unintentionally;
- no source writes from raw model output;
- quality-gate evidence for advisory promotion if advisory role is proposed;
- maintainer approval for runtime wiring.

## Practical advice for AI agents

When asked to improve NPU usage:

1. inspect current helper contracts first;
2. avoid editing runtime orchestrators immediately;
3. add or refine pure helpers;
4. add validation before integration;
5. document provider boundary;
6. keep NPU as probe/guardrail/decode diagnostic unless quality evidence promotes it;
7. keep GPU advisory explicit and quality-gated;
8. state when local hardware validation is required;
9. attach telemetry/capability/bundle context when NPU results affect evidence or patch plans;
10. keep maintained NPU helper/source files under 400 lines or split by responsibility.
