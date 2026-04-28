# AI Pipeline Optimization

## Scope

This additive layer improves AI-assisted artifact production without replacing Blender runtime workflows or editing working packages.

## Rules

- Do not rewrite raw/full analysis JSON files.
- Do not destructively refactor `Scripting/v61b/`.
- Generate context and reports under `indexAI/` or explicit output folders.
- Use CPU for deterministic parsing/validation.
- Use NPU for short review/classification/scoring tasks.
- Use GPU for optional heavy generation through explicit commands.

## Main flow

```text
analysis JSON
  -> compact music artifacts
  -> semantic code chunks
  -> task capsules
  -> optional NPU review
  -> optional GPU planner
  -> validation report
```

## Entry point

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate
```

Dry run:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run
```

## Outputs

Default generated artifacts are written under:

```text
output/ai_pipeline/
indexAI/code_chunks/
```

The pipeline is additive and can be bypassed by simply not running these tools.
