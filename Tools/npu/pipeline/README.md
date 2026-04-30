# NPU Pipeline Helpers

This package contains app-agnostic helper modules for the local NPU/Ollama pipeline.

The package is intentionally additive. Existing CLI entrypoints continue to own orchestration until a later validated migration wires these helpers in one group at a time.

## Current scope

Allowed:

```text
pure configuration objects
path and generated-artifact validation
UTF-8 text and JSON-object IO helpers
prompt payload builders
context bundle helpers
planned-only provider descriptors
planned-only runner stage reports
contract validators
artifact write planning helpers
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
| `artifact_paths.py` | Generated artifact path normalization and allowed-prefix validation. |
| `io_utils.py` | UTF-8 text and JSON-object read/write helpers. |
| `prompts.py` | Deterministic prompt payload builders. |
| `context_builder.py` | Bounded context slices and compact context bundle metrics. |
| `providers.py` | Planned-only provider request/result envelopes. |
| `runner.py` | Planned-only stage-plan reports. |
| `validators.py` | Contract-level validators that preserve unknown future fields. |
| `artifact_writer.py` | Validated generated-artifact write helpers. |

## Validation

Focused smoke validation:

```powershell
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
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
2. Wire only IO helpers.
3. Wire only artifact path/contract helpers.
4. Wire only prompt/context payload helpers.
5. Move provider adapters last.
6. Compare local outputs after every wiring step.
