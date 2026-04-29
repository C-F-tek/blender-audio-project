# AI Pipeline Optimization

## Scope

This additive layer improves AI-assisted artifact production without replacing Blender runtime workflows or editing working packages.

The current AI artifact pipeline is modularized under:

```text
Tools/ai/pipeline/
```

Status marker:

```text
modular_schedule_complete_pending_local_validation
```

Read before modifying pipeline behavior:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
Tools/ai/pipeline/refactor_status.py
```

## Rules

- Do not rewrite raw/full analysis JSON files.
- Do not destructively refactor `Scripting/v61b/`.
- Generate context and reports under `indexAI/` or explicit output folders.
- Use CPU for deterministic parsing/validation.
- Use NPU for short review/classification/scoring tasks.
- Use GPU for optional heavy generation through explicit commands.
- Keep the public CLI and schema-v6 report fields compatible unless local dry-run matrix validation confirms a safe change.

## Main flow

```text
analysis JSON
  -> preflight awareness report
  -> compact music artifacts
  -> semantic code chunks
  -> task capsules or smart context
  -> optional NPU review/guardrail
  -> optional GPU planner
  -> semantic validation report
  -> dry-run/run report with summary and schedule
```

## Modular pipeline structure

| Module | Optimization role |
|---|---|
| `defaults.py` | Centralizes tunable defaults. |
| `artifact_contracts.py` | Keeps expected artifacts explicit. |
| `preflight.py` | Detects missing inputs and workstation constraints early. |
| `steps.py` | Builds command steps consistently. |
| `scheduler.py` | Encapsulates serial/parallel policy. |
| `orchestrator.py` | Runs serial/parallel steps. |
| `schema_report.py` | Emits `summary` and `schedule` fields. |
| `guardrail_models.py` | Normalizes remediation queue data. |
| `remediation.py` | Executes auto-safe guardrail passes. |

## Current report fields

The pipeline report uses schema version `6`.

Important fields:

```text
passed
preflight
summary
schedule
lanes
guardrail_remediation_loop
steps
post_run_expected_outputs
```

The `summary` field provides:

```text
ok_count
failed_count
planned_only_count
total_duration_sec
failed_steps
lane_counts
```

The `schedule` field provides:

```text
serial_count
parallel_count
total_count
serial
parallel
parallel_lanes
```

## Entry point

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate
```

Dry run:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run
```

Dry run with report file:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run --write-dry-run-report
```

Dry-run matrix:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

## Outputs

Default generated artifacts are written under:

```text
output/ai_pipeline/
indexAI/code_chunks/
```

Dry-run matrix report:

```text
output/ai_pipeline/dry_run_matrix_report.json
```

Individual matrix reports:

```text
output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json
```

## Optimization priorities

Current priority order:

```text
1. local validation of modular split
2. index regeneration
3. report readability
4. lane policy refinement
5. Markdown report generation
6. deeper NPU pipeline split
```

## Validation

After pipeline changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

The pipeline is additive and can be bypassed by simply not running these tools.
