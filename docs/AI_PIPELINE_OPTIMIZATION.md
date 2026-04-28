# AI Pipeline Optimization

## Scope

This document defines the additive AI-assistance layer for the project.

It does not replace the Blender runtime workflow, render workflow, audio analysis scripts, or any working package under `Scripting/`.

The objective is to improve the quality and throughput of AI-produced artifacts by using better intermediate data, semantic code chunks, task capsules, validation reports, and optional CPU/NPU/GPU task separation.

## Non-destructive rules

- Keep full audio-analysis JSON files as read-only data inputs.
- Do not rewrite frame-by-frame keyframe JSON files.
- Do not refactor `Scripting/v61b/` from this pipeline.
- Generate new context, review, and planning artifacts under `indexAI/` or an explicit output folder.
- Use feature flags for optional NPU/GPU work.
- Treat every AI-generated plan or script as a draft until validated.
- Prefer small package-specific patches over monolithic replacement scripts.

## Device roles

| Device | Role | Typical tasks |
|---|---|---|
| CPU | Deterministic orchestration | file I/O, parsing, AST extraction, JSON validation, report generation |
| NPU | Lightweight AI review lane | short summaries, checklist review, candidate scoring, assumption detection |
| GPU | Heavy generation lane | main LLM generation, creative merge, Blender code generation, larger reranking jobs |

The pipeline should not try to split one model across NPU and GPU. It should run different tasks on different devices.

## Artifact model

The recommended artifact flow is:

```text
analysis JSON
  -> compact music summary
  -> music segments
  -> audio event map
  -> scene brief
  -> mapping candidates
  -> selected mapping
  -> scene spec / patch plan
  -> validation report
```

The full analysis JSON remains the canonical low-level data source. The AI should usually consume compact artifacts rather than raw frame-level data.

## New artifact names

| Artifact | Purpose |
|---|---|
| `track_summary.json` | Compact global track facts. |
| `music_segments.json` | Intro/build/climax/release/outro style sections. |
| `audio_event_map.json` | Peaks, beats, onsets, and silence markers when available. |
| `ai_scene_brief.json` | Creative and technical brief for the next AI stage. |
| `ai_resource_budget.json` | Practical resource limits for object count, frames, memory, render profile. |
| `ai_mapping_candidates.json` | Candidate audio-to-visual mappings. |
| `ai_selected_mapping.json` | Merged or selected mapping for implementation. |
| `ai_validation_report.json` | Validation result and risk report. |
| `ai_pipeline_run_report.json` | Execution report for the orchestrator. |

## Semantic chunking

Code chunks should be grouped by responsibility and symbol, not by arbitrary text length.

A semantic chunk should include:

```json
{
  "chunk_id": "Scripting/v61b/materials.py::make_material",
  "path": "Scripting/v61b/materials.py",
  "symbol": "make_material",
  "kind": "function",
  "line_start": 10,
  "line_end": 50,
  "domain": ["materials", "shader", "blender_compat"],
  "blender_api": ["bpy.data.materials", "nodes.new"],
  "risk": "medium",
  "compatibility_notes": [],
  "dependencies": ["config.py"],
  "sha256": "..."
}
```

The generator in `Tools/npu/build_semantic_code_chunks.py` creates this layer without modifying source files.

## Task capsules

Task capsules are small JSON files under `indexAI/task_capsules/`.

They contain stable operational memory for the AI, such as Blender compatibility rules, known risky APIs, audio mapping strategy, and package-generation expectations.

Capsules are not source code. They are AI context artifacts.

## Validation

`Tools/ai/validate_ai_artifacts.py` performs a conservative validation pass:

- checks JSON syntax;
- checks required sections for known AI artifacts;
- applies guardrails from task capsules;
- scans optional package folders against the project quality gate;
- emits an explicit score and blocking errors.

The validator must be run before treating a generated package or patch plan as candidate-quality.

## Parallel execution

`Tools/ai/run_parallel_artifact_pipeline.py` coordinates local steps.

Default behavior is safe and local:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --dry-run
```

Example with an analysis JSON:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py `
  --repo-root . `
  --analysis-json .\output\Feel_The_Light_analysis.json `
  --build-chunks `
  --build-music-summary `
  --validate
```

Optional NPU lane:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py `
  --repo-root . `
  --analysis-json .\output\Feel_The_Light_analysis.json `
  --build-chunks `
  --build-music-summary `
  --use-npu `
  --validate
```

Optional external GPU command:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py `
  --repo-root . `
  --analysis-json .\output\Feel_The_Light_analysis.json `
  --gpu-command "py .\Tools\ai\your_gpu_generator.py --input {brief} --output {output}" `
  --validate
```

The placeholders `{brief}` and `{output}` are replaced by the orchestrator.

## Acceptance criteria

A produced artifact set is acceptable only when:

- raw analysis files were not modified;
- generated files are isolated;
- validation report has no blocking errors;
- assumptions are explicit;
- generated code avoids blocked Blender API patterns;
- package output follows the quality gate before being promoted from draft to candidate.

## Rollback

Because this implementation is additive, rollback is simple:

```powershell
git switch master
git branch -D ai-pipeline-optimization-safe
```

or revert the specific commits/files added by this feature branch.
