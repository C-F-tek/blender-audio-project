# NPU Pipeline Helpers

This package contains app-agnostic helper modules for the local NPU/Ollama pipeline.

For broad local AI orchestration and full validation, start from the unified launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

This package is not the primary operator entrypoint.

## Command ownership

This README is a package catalog and migration policy. Current executable commands for broad validation, full runs, quick tests, provider probes and full validation live in the unified launcher runbook.

Focused NPU helper commands may be used only when debugging this package or validating one helper contract directly. They must not be presented as replacements for the unified launcher.

## Current scope

Allowed:

```text
configuration objects
path and generated-artifact validation
legacy runtime-output policy helpers
UTF-8 text and JSON IO helpers
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
common validation envelopes
runtime-output manifest helpers
```

Forbidden in this package unless explicitly scoped and validated:

```text
Blender runtime execution
provider calls
GPU jobs
FFmpeg jobs
Ready To Jazz migration
full analysis JSON mutation
hand-edited generated indexes
provider behavior changes
```

## Module map

| Module | Responsibility |
|---|---|
| `config.py` | Repository paths, track defaults and data-only pipeline configuration. |
| `artifact_paths.py` | Generated artifact path normalization, allowed-prefix validation and legacy runtime-output policy. |
| `io_utils.py` | UTF-8 text and JSON-object read/write helpers plus legacy-compatible aliases. |
| `legacy_compat.py` | Equivalence helpers for comparing legacy functions with new helpers before runtime wiring. |
| `fixtures.py` | Deterministic fixture payloads for tests, dry-runs and contract examples. |
| `prompts.py` | Deterministic prompt payload builders. |
| `context_builder.py` | Bounded context slices and compact context bundle metrics. |
| `providers.py` | Planned provider request/result envelopes and provider preflight report normalization. |
| `runner.py` | Planned stage-plan reports. |
| `validators.py` | Contract-level validators that preserve unknown future fields. |
| `artifact_writer.py` | Validated generated-artifact write helpers. |
| `migration_readiness.py` | Deterministic gates for future runtime wiring readiness. |
| `reports.py` | Helper-boundary reports, validation envelopes and runtime-output manifests. |

## Runtime-adjacent scripts outside this package

| File | Classification | Notes |
|---|---|---|
| `Tools/npu/ollama_runtime.py` | runtime-adjacent helper | Do not imply execution unless called by an explicit provider command. |
| `Tools/npu/npu_runtime.py` | runtime-adjacent helper | Keep separate from planned provider descriptors. |
| `Tools/npu/run_npu_review.py` | explicit local diagnostic/review helper | Not the unified launcher. |
| `Tools/npu/run_npu_context.ps1` | explicit local context/review wrapper | Useful local helper; not the canonical full 0-to-10 path. |
| `Tools/npu/build_provider_result_report.py` | supporting report builder | Converts provider result data into report surfaces. |
| `Tools/ai/run_npu_gpu_deep_review_auditor.py` | diagnostic-only | Explicit heavy local diagnostic. |
| `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` | legacy/integrated orchestration lane | Prefer unified launcher; verify current caller before changing behavior. |

Policy:

```text
planned helper modules may be validated without providers
runtime-adjacent helpers must not be called implicitly by validators
provider execution must be visible in launcher manifest or explicit local evidence
broad validation belongs to the unified launcher
```

## Validation ownership

Broad validation route:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Focused helper validation remains allowed only for package debugging and should produce explicit reports under `output/validation/`.

Focused package validation must not execute Blender, provider calls, GPU jobs or FFmpeg.

Full local validation should normally be routed through the unified launcher. Legacy direct full-validation wrappers are supporting detail only.

## Migration policy

Do not migrate `Tools/npu/run_dual_ai_pipeline.py` all at once.

Completed validated runtime-helper adoption:

1. IO helpers.
2. Artifact path and implementation draft contract helpers.
3. Prompt payload helpers.
4. Context summary and generated support-file write-planning helpers.
5. Legacy runtime-output policy helpers.
6. Provider preflight normalization without provider execution.

Current safe next layer:

```text
NPU validator/report contract consistency
runtime-output manifest/reporting as additive observability
provider result report cataloging without implicit provider execution
```

Still future work:

```text
provider execution adapters
provider result parsing/reporting
prompt prose extraction
full artifact writer runtime migration
memory/guardrail runtime integration
```

Every runtime bridge phase must keep provider/model behavior stable unless a later execution plan explicitly scopes and validates that behavior change.

## Cross-reference

```text
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```
