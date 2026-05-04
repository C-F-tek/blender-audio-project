# NPU Pipeline Helpers

This package contains app-agnostic helper modules for the local NPU/Ollama pipeline.

The package is intentionally additive. Existing CLI entrypoints own orchestration while validated migration phases wire selected helpers in one group at a time.

For full local AI orchestration, start from the unified launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

This package is not the primary operator entrypoint.

## Current scope

Allowed:

```text
pure configuration objects
path and generated-artifact validation
legacy dual-AI runtime output policy helpers
UTF-8 text and JSON-object IO helpers
legacy-compatible IO aliases
legacy/new helper equivalence checks
deterministic fixtures for tests and dry-runs
prompt payload builders
context bundle helpers
planned-only provider descriptors
provider preflight report normalizers
planned-only runner stage reports
contract validators
artifact write planning helpers
migration readiness reports
common validation report envelopes
runtime-output manifest helpers for additive observability
```

Forbidden in this package unless explicitly validated:

```text
Blender runtime execution
NPU/Ollama provider calls
GPU jobs
FFmpeg jobs
Ready To Jazz migration
full analysis JSON mutation
hand-edited generated indexes
provider execution behavior changes
```

## Module map

| Module | Responsibility |
|---|---|
| `config.py` | Repository paths, track defaults and data-only pipeline configuration. |
| `artifact_paths.py` | Generated artifact path normalization, allowed-prefix validation and exact legacy runtime output policy. |
| `io_utils.py` | UTF-8 text and JSON-object read/write helpers plus legacy-compatible aliases. |
| `legacy_compat.py` | Equivalence helpers for comparing legacy functions with new helpers before runtime wiring. |
| `fixtures.py` | Deterministic fixture payloads for tests, dry-runs and contract examples. |
| `prompts.py` | Deterministic prompt payload builders. |
| `context_builder.py` | Bounded context slices and compact context bundle metrics. |
| `providers.py` | Planned-only provider request/result envelopes and provider preflight report normalization. |
| `runner.py` | Planned-only stage-plan reports. |
| `validators.py` | Contract-level validators that preserve unknown future fields. |
| `artifact_writer.py` | Validated generated-artifact write helpers. |
| `migration_readiness.py` | Deterministic gates for future runtime wiring readiness. |
| `reports.py` | Helper-boundary reports, common validation report envelopes and runtime-output manifests. |

## Runtime-adjacent scripts outside this package

These scripts are related to NPU/Ollama/provider behavior but are not automatically part of this helper package's runtime-free contract.

| File | Classification | Notes |
|---|---|---|
| `Tools/npu/ollama_runtime.py` | runtime-adjacent helper | Ollama runtime/session helper. Do not imply execution unless called by an explicit provider command. |
| `Tools/npu/npu_runtime.py` | runtime-adjacent helper | NPU preflight/runtime helper. Keep separate from planned-only provider descriptors. |
| `Tools/npu/run_npu_review.py` | explicit local diagnostic/review entrypoint | Provider/model behavior must remain explicit. Not the unified launcher. |
| `Tools/npu/run_npu_context.ps1` | explicit local context/review wrapper | Useful local helper; not the canonical full 0-to-10 path. |
| `Tools/npu/build_provider_result_report.py` | supporting report builder | Converts provider result data into report surfaces. Do not treat as provider execution by itself. |
| `Tools/ai/run_npu_gpu_deep_review_auditor.py` | diagnostic-only | Explicit heavy local diagnostic. |
| `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` | legacy/integrated orchestration lane | Prefer unified launcher; verify current caller before changing runtime behavior. |

Policy:

```text
planned-only helper modules may be validated without providers
runtime-adjacent helpers must not be called implicitly by validators
provider execution must be visible in the unified launcher manifest or explicit local evidence
```

## Validation

Focused helper validation workflow:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

Focused smoke validation:

```powershell
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
```

Focused unit-test validation:

```powershell
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
```

Documentation/module alignment validation:

```powershell
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
```

Direct unittest mode:

```powershell
python .\Tools\validation\test_npu_pipeline_helpers.py
```

Full local validation should normally be routed through the unified launcher:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode validation,contract,full_validation `
  -RunIntensity quick
```

Legacy direct full-validation wrapper remains available as supporting detail:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
```

Regenerate indexes after accepted structural changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Do not hand-edit generated indexes.

## Migration policy

Do not migrate `Tools/npu/run_dual_ai_pipeline.py` all at once.

Completed validated runtime-helper adoption:

1. IO helpers.
2. Artifact path and implementation draft contract helpers.
3. Prompt payload helpers.
4. Context summary and generated support-file write-planning helpers.
5. Exact legacy runtime output policy helpers.
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

Every runtime bridge phase must keep provider/model execution behavior stable unless a later execution plan explicitly scopes and validates that behavior change.

## Cross-reference

Forgotten-script visibility and classification audit:

```text
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
```
