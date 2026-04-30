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

This list is intentionally open. Add focused app-agnostic modules or functions when implementation exposes useful reusable behavior. Examples include provider preflight helpers, JSON/model-output normalization, memory filtering, guardrail scoring, artifact manifest builders and deterministic dry-run fixtures.

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

## Phase 1 GitHub-only implementation

Branch:

```text
codex/npu-pipeline-decomposition-phase-1
```

Scope:

```text
add Tools/npu/pipeline/ package scaffold
add pure config/path/prompt payload helpers
do not wire helpers into Tools/npu/run_dual_ai_pipeline.py yet
do not change provider/runtime behavior
do not edit generated indexes
```

Validation required locally before merge:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

## Phase 2 GitHub-only implementation

Branch:

```text
codex/npu-pipeline-decomposition-phase-2
```

Scope:

```text
add Tools/npu/pipeline/io_utils.py
export pure IO helpers from Tools/npu/pipeline/__init__.py
do not wire helpers into Tools/npu/run_dual_ai_pipeline.py yet
do not change provider/runtime behavior
do not edit generated indexes until maintainer local regeneration
```

Rationale:

```text
IO helpers are app-agnostic, deterministic and easy to validate by syntax/import checks.
Keeping the existing orchestrator untouched in this phase avoids partial runtime migration while the maintainer is away from the workstation.
```

Validation required locally before merge:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

## Away batch implementation

Branch:

```text
codex/npu-pipeline-decomposition-away-batch
```

Scope:

```text
add pure artifact writer helpers
add pure contract validators
add NPU pipeline module smoke validator
wire that smoke validator into the local PowerShell validation runner
do not modify Tools/npu/run_dual_ai_pipeline.py
do not modify provider/runtime behavior
do not edit generated indexes until maintainer local regeneration
```

Batch rationale:

```text
The maintainer is away from the workstation, so this batch intentionally stops before runtime wiring.
It prepares multiple pure-helper improvements plus one focused validator, then waits for one final local validation cycle.
```

Validation required before merge:

```powershell
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
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
| `io_utils.py` | UTF-8 text and JSON-object read/write helpers | Pure helpers; no provider, Blender or model loading. |

## Core function policy

Reusable functions are part of the core when they satisfy all of these:

```text
app-agnostic
deterministic where practical
owned by a focused module
validated by syntax checks, dry-runs or a dedicated validator
free of Ready To Jazz or Blender package assumptions
```

Do not wait for a large split to add a useful core helper. Add it when it reduces duplication or improves validation, then keep the existing CLI behavior stable.

## Migration strategy later

1. Read `Tools/npu/run_dual_ai_pipeline.py` and current NPU docs locally.
2. Add package folder with `__init__.py` and no behavior change.
3. Move pure config constants first.
4. Move prompt strings second.
5. Extract small reusable functions when they are app-agnostic and covered by focused validation.
6. Move context assembly only after tests or deterministic dry-runs exist.
7. Move provider calls last.
8. Keep old CLI command behavior stable until local validation passes.
9. Regenerate AI/NPU indexes locally after the split.

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
| Catch-all core utility drift | Add focused helper modules with clear ownership instead of broad utility dumps. |
| GitHub-only overclaiming | Mark local validation pending until workstation logs are available. |

## Local validation status

```text
Local workstation validation pending.
```
