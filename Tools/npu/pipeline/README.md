# NPU Pipeline Helpers

This package contains app-agnostic helper modules for local NPU/OpenVINO support.

It is not the primary operator entrypoint and not the provider mesh owner.

Current command, owner and flow references:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
```

## Current doctrine

```text
quick/balanced/deep/custom = intensity, not scope
NPU helper validation != full-run proof
NPU smoke success != primary advisory promotion
NPU current role = micro/support/diagnostic/tool-support lane when selected
telemetry accompanies evidence and patch plans for completeness
```

When an NPU helper, provider descriptor, provider result report or runtime-output manifest enters production full-run handoff, the handoff must expose state through:

```text
unified launcher manifest
phase_status / phase_reports
provider diagnostics
runtime tool usage telemetry when tools execute
runtime/hardware capability manifest when capabilities matter
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
file-line-limit report when maintainability is in scope
```

## Current scope

Allowed:

```text
configuration objects
path and generated-artifact validation
legacy runtime-output policy helpers
UTF-8 text and JSON IO helpers
legacy-compatible IO aliases
legacy/new helper equivalence checks
deterministic fixtures
prompt payload builders
context bundle helpers
planned provider descriptors
provider preflight report normalizers
planned runner stage reports
contract validators
artifact write planning helpers
migration readiness reports
common validation report envelopes
runtime-output manifest helpers
```

Forbidden in this package unless explicitly scoped and validated:

```text
hidden provider calls
hidden GPU/NPU jobs
hidden NPU/Ollama provider calls
Blender runtime execution
FFmpeg jobs
Ready To Jazz migration
full analysis JSON mutation
hand-edited generated indexes
provider behavior changes
```

## Module map

| Module | Responsibility | Full-run handoff note |
|---|---|---|
| `config.py` | Repository paths, track defaults and data-only pipeline configuration. | No runtime claim by itself. |
| `artifact_paths.py` | Generated artifact path normalization, allowed-prefix validation and legacy runtime-output policy. | Path policy only; no provider execution. |
| `io_utils.py` | UTF-8 text and JSON-object read/write helpers plus legacy-compatible aliases. | Filesystem helper only. |
| `legacy_compat.py` | Equivalence helpers for comparing legacy functions with new helpers before runtime wiring. | Focused validation only. |
| `fixtures.py` | Deterministic fixture payloads for tests, dry-runs and contract examples. | Fixture evidence is not runtime proof. |
| `prompts.py` | Deterministic prompt payload builders. | Prompt payloads are not provider execution. |
| `context_builder.py` | Bounded context slices and compact context bundle metrics. | Needs manifest/bundle reference if used in full-run handoff. |
| `providers.py` | Planned provider request/result envelopes and provider preflight report normalization. | Provider state must flow to telemetry/bundle if used in full-run evidence. |
| `runner.py` | Planned stage-plan reports. | Planned-only unless an explicit runtime wrapper executes. |
| `validators.py` | Contract-level validators that preserve unknown future fields. | Validation reports do not prove provider execution. |
| `artifact_writer.py` | Validated generated-artifact write helpers. | Writes must remain scoped and report-visible. |
| `migration_readiness.py` | Deterministic gates for future runtime wiring readiness. | Gate reports are advisory until local runtime validation. |
| `reports.py` | Helper-boundary reports, validation envelopes and runtime-output manifests. | Runtime-output manifests must be bundled with telemetry when promoted. |

## Runtime-adjacent scripts outside this package

| File | Classification | Notes |
|---|---|---|
| `Tools/npu/_shared/ollama_runtime.py` | runtime-adjacent helper | Do not imply execution unless called by an explicit provider command. |
| `Tools/npu/_shared/npu_runtime.py` | runtime-adjacent helper | Keep separate from planned provider descriptors. |
| `Tools/npu/run_npu_review.py` | explicit local diagnostic/review helper | Not the unified launcher. |
| `Tools/npu/run_npu_context.ps1` | explicit local context/review wrapper | Useful local helper; not canonical full 0-to-10 path. |
| `Tools/npu/build_provider_result_report.py` | supporting report builder | Converts provider result data into report surfaces; bundle/telemetry visibility required when promoted. |
| `Tools/ai/run_npu_gpu_deep_review_auditor.py` | diagnostic/support lane | Not primary advisory proof by itself. |
| `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` | provider orchestration lane | Prefer unified launcher; verify current caller before changing behavior. |

Policy:

```text
planned helper modules may be validated without providers
runtime-adjacent helpers must not be called implicitly by validators
provider execution must be visible in launcher manifest or explicit local evidence
provider failure/degradation/exclusion must be visible in telemetry/bundle when it affects evidence or patch plans
broad validation belongs to the unified launcher
```

## File-size policy

Maintained NPU helper docs and source files follow the active file-size policy:

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split layout:

```text
name.md
name.md/part-001.md
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Validation ownership

Broad validation route:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Focused validation selection:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Focused helper validation remains allowed only for package debugging and should produce explicit reports under `output/validation/`.

Focused helper validation must not execute Blender, provider calls, GPU jobs or FFmpeg.


## Migration policy

Do not migrate `Tools/npu/run_dual_ai_pipeline.py` all at once.

Validated helper adoption so far:

```text
IO helpers
artifact path and implementation draft contract helpers
prompt payload helpers
context summary and generated support-file write-planning helpers
legacy runtime-output policy helpers
provider preflight normalization without provider execution
```

Current safe next layer:

```text
NPU validator/report contract consistency
runtime-output manifest/reporting as additive observability
provider result report cataloging without implicit provider execution
telemetry/bundle visibility for any promoted provider result report
file-line impact review before runtime wiring or large helper refactors
```

Still future work:

```text
provider execution adapters
provider result parsing/reporting
prompt prose extraction
full artifact writer runtime migration
memory/guardrail runtime integration
strict full-run telemetry completeness validation
```

Every runtime bridge phase must keep provider/model behavior stable unless a later execution plan explicitly scopes and validates that behavior change.

## Cross-reference

```text
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```
