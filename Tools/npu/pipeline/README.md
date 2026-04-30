# NPU Pipeline Helpers

This package contains app-agnostic helper modules for the local NPU/Ollama pipeline.

The package is intentionally additive. Existing CLI entrypoints continue to own orchestration until a later validated migration wires these helpers in one group at a time.

## Current scope

Allowed:

```text
pure configuration objects
path and generated-artifact validation
legacy dual-AI runtime output policy helpers
UTF-8 text and JSON-object IO helpers
legacy-compatible IO aliases for later wiring
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
```

Forbidden in this package until explicitly validated:

```text
Blender runtime execution
NPU/Ollama provider calls
GPU jobs
FFmpeg jobs
Ready To Jazz migration
full analysis JSON mutation
hand-edited generated indexes
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
| `reports.py` | Helper-boundary report utilities. |

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

Full local validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
```

Regenerate indexes after accepted structural changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Migration policy

Do not migrate `Tools/npu/run_dual_ai_pipeline.py` all at once.

Recommended order:

1. Validate this helper package.
2. Regenerate AI/NPU indexes.
3. Use `default_runtime_wiring_readiness()` as a conservative runtime-wiring gate.
4. Wire only IO helpers.
5. Wire only artifact path/contract helpers.
6. Wire only prompt/context payload helpers.
7. Wire only context summary and generated-artifact write-planning helpers.
8. Wire exact legacy runtime output policy helpers.
9. Wire provider preflight normalization without provider execution.
10. Move provider execution adapters last.
11. Compare local outputs after every wiring step.
