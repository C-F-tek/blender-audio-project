# NPU/GPU Parallelism Plan

The project uses task-level parallelism, not one model split across devices.

## Current status

The AI artifact pipeline has a modular schedule layer:

```text
Tools/ai/pipeline/scheduler.py
```

Current status marker:

```text
modular_schedule_complete_pending_local_validation
```

Read:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
Tools/ai/pipeline/refactor_status.py
```

## Lanes

- CPU: file I/O, parsing, compact artifact generation, validation.
- NPU: compact artifact review, warning detection, scoring and guardrail checks.
- GPU: optional heavy generation through `--gpu-command`.

## Scheduler

The current scheduler separates ordered serial steps from independent parallel steps.

Module:

```text
Tools/ai/pipeline/scheduler.py
```

Key objects/functions:

```text
PipelineSchedule
build_schedule()
should_run_parallel()
execute_schedule()
```

The report includes a `schedule` field with:

```text
serial_count
parallel_count
total_count
serial
parallel
parallel_lanes
```

## Orchestrator

Single dry run:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --dry-run --write-dry-run-report
```

Full dry run with common stages:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run --write-dry-run-report
```

Dry-run matrix:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

## Hardware policy

For the current workstation profile:

- do not run heavy Blender rendering and large GPU LLM inference together;
- keep NPU jobs compact;
- keep NPU workers at 4 or below;
- prefer compact JSON context over full frame-level JSON;
- validate before accepting generated code;
- treat GPU generation as explicit opt-in through `--gpu-command`.

## Next scheduling improvements

After local dry-run validation passes, possible future improvements are:

```text
LaneExecutionPolicy
maximum NPU worker policy
GPU availability preflight
parallel lane grouping by resource
Markdown schedule summary
```

Do not add real hardware scheduling behavior until the current dry-run matrix passes locally.
