---
applyTo: "**/*analysis*.py,**/*summary*.py,**/*scene_spec*.py,Tools/ai/**/*.py,Tools/npu/**/*.py"
---

# Audio and Scene-Spec Pipeline Instructions

Use these rules when editing audio-analysis, summary, scene-spec, AI artifact, or NPU pipeline code.

## Pipeline model

The expected data flow is:

```text
WAV/audio file
  -> technical analysis JSON
  -> compact summary / music context
  -> scene spec or AI implementation plan
  -> Blender package
  -> rendered image sequence
  -> encoded video
```

## Editing rules

- Preserve full frame-by-frame analysis JSON files.
- Prefer compact summaries for AI context.
- Keep CLI parsing separate from reusable logic when refactoring.
- Keep validators separate from prompt builders.
- Keep providers/runtime wrappers separate from pipeline orchestration.
- Keep generated artifacts under `output/`, `indexAI/`, or explicitly documented artifact folders.
- Do not invent JSON fields without documenting assumptions or schema updates.

## Root tools

Root scripts such as these should gradually move toward importable service logic plus CLI wrappers:

```text
analyze_wav.py
build_track_summary.py
normalize_scene_spec.py
```

Do not break their current command-line behavior during refactoring.

## AI/NPU direction

Task-level parallelism is preferred:

```text
CPU -> parsing, compact artifacts, validation
NPU -> review, scoring, warning detection
GPU -> optional heavy generation
```

Do not run heavy Blender rendering and heavy GPU model inference together unless explicitly requested.

## Validation

Use:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

For AI artifact dry runs:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run --write-dry-run-report
```
