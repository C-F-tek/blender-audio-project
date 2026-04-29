# Local AI Workflow

## Purpose

This document records the intended direction for moving parts of the Blender script-generation workflow toward a local AI-assisted pipeline.

The local workflow should be deterministic where possible, explicit about generated artifacts, and safe for repeated dry-runs.

## Current workflow

At the current stage, the workflow is generally:

```text
Audio input
  -> technical analysis
  -> JSON files and compact context
  -> modular AI artifact pipeline
  -> local or external model-assisted planning/review
  -> generated Blender script package or patch plan
  -> stored under Scripting/ or indexAI/patch_library/
  -> manual or assisted refinement
```

## Current AI artifact pipeline status

Status marker:

```text
modular_schedule_complete_pending_local_validation
```

Key files:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/ai/pipeline/
Tools/validation/check_ai_pipeline_modules.py
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
```

The current entrypoint is intentionally thin. Implementation belongs under `Tools/ai/pipeline/`.

## Target direction

The objective is to perform more of the script-generation and review loop locally, when hardware and model quality allow it.

Candidate local components:

- local project indexing;
- local compact context generation;
- generic agent state packet generation;
- local JSON summarization;
- local Blender-aware code planning;
- local patch planning;
- local patch validation;
- NPU-assisted review where useful;
- GPU-assisted model execution where required.

## Repository areas involved

| Area | Role |
|---|---|
| `Scripting/` | Destination for generated Blender script packages. |
| `Scripting/shared/` | Shared reusable helpers used before package migration. |
| `Tools/ai/` | Modular artifact pipeline entrypoints and dry-run matrix. |
| `Tools/ai/pipeline/` | Modular AI artifact pipeline implementation. |
| `Tools/npu/` | Local AI, NPU, context-building, and review tooling. |
| `indexAI/` | Project index, manifests, compact context, and patch materials. |
| `indexAI/patch_library/` | Generated plans, service capsules, and task packets. |
| `docs/` | Stable documentation for human and AI orientation. |

## Desired local pipeline

```text
WAV/audio data
  -> analysis JSON
  -> compact music and technical context
  -> agent state packet with memory, constraints and lane microtasks
  -> modular AI artifact pipeline
  -> local AI planner/reviewer
  -> implementation plan
  -> patch generator or package generator
  -> validation against repo index
  -> generated Blender package under Scripting/
  -> Blender test run
  -> render and FFmpeg workflow
```

## Required validation after pipeline changes

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

After validation:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Requirements for safe local generation

- A reliable project index.
- Clear target files.
- Clear JSON schema or documented assumptions.
- Patch validation before writing files.
- No destructive overwrite of source or analysis data.
- Explicit logging of generated files.
- Explicit memory packet or state packet when a task spans multiple steps.
- Optional persistent memory through JSONL or SQLite, with SQLite preferred before external database dependencies.
- Manual review for major scene-generation changes.
- Dry-run reports for pipeline or patch generation.

## AI rules

- Treat local AI output as draft material until validated.
- Keep generated packages separated by track, concept, or version.
- Do not merge unrelated generated packages automatically.
- Preserve full analysis JSON files.
- Prefer compact summaries for model input.
- Record assumptions in generated implementation notes.
- Do not interpret the modular pipeline split as incomplete unless local validation fails.

## Not specified

- Final local model choice.
- Final NPU or GPU runtime.
- Final prompt format.
- Final patch schema.
- Final validation command for Blender runtime.
