# NPU Pipeline Decomposition Plan

## Status

active

## Goal

Plan a later non-destructive split of `Tools/npu/run_dual_ai_pipeline.py` into focused modules.

This plan does not perform the split.

## Current target

Current large orchestration file:

```text
Tools/npu/run_dual_ai_pipeline.py
```

Future module family:

```text
Tools/npu/pipeline/config.py
Tools/npu/pipeline/context_builder.py
Tools/npu/pipeline/prompts.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/validators.py
Tools/npu/pipeline/artifact_writer.py
Tools/npu/pipeline/runner.py
```

## GitHub-only scope

Allowed now:

```text
create this execution plan
record target module boundaries
record validation requirements
record migration constraints
```

Forbidden now:

```text
no code split
no provider behavior changes
no NPU/GPU execution claims
no hand-edited generated indexes
no local output report claims
```

## Proposed module responsibilities

| Future module | Responsibility | Notes |
|---|---|---|
| `config.py` | CLI/config dataclasses, path defaults, environment-independent options | Must not load models. |
| `context_builder.py` | Build compact project/music/context inputs | Should reuse existing context builders where possible. |
| `prompts.py` | Prompt templates and prompt assembly helpers | Keep prompts versioned and testable as strings. |
| `providers.py` | Ollama/NPU/provider adapters | Keep provider-specific failures isolated. |
| `validators.py` | Validate model outputs, required JSON keys and generated artifact destinations | Reuse `Tools/ai/model_json.py` and generated artifact path policy. |
| `artifact_writer.py` | Write generated JSON/Markdown/script artifacts | Keep writes inside allowed generated destinations. |
| `runner.py` | Orchestrate the staged flow and preserve CLI behavior | Should remain thin after split. |

## Migration strategy later

1. Read `Tools/npu/run_dual_ai_pipeline.py` and current NPU docs locally.
2. Add package folder with `__init__.py` and no behavior change.
3. Move pure config constants first.
4. Move prompt strings second.
5. Move context assembly only after tests or deterministic dry-runs exist.
6. Move provider calls last.
7. Keep old CLI command behavior stable until local validation passes.
8. Regenerate AI/NPU indexes locally after the split.

## Validation required later

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

If deterministic NPU pipeline dry-runs exist by then, add them to the local validation block.

## Risks

| Risk | Mitigation |
|---|---|
| Provider behavior changes during split | Move provider adapters last and compare local outputs. |
| Prompt drift | Move prompts without rewriting content first. |
| Path policy bypass | Route artifact writes through allowed destinations and validate generated paths. |
| Overfitting to Blender/audio | Keep config/context/provider boundaries generic where practical. |
| GitHub-only overclaiming | Mark local validation pending until workstation logs are available. |

## Local validation status

```text
Local workstation validation pending.
```
