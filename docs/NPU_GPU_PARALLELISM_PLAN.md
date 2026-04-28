# NPU/GPU Parallelism Plan

The project uses task-level parallelism, not one model split across devices.

## Lanes

- CPU: file I/O, parsing, compact artifact generation, validation.
- NPU: compact artifact review, warning detection, scoring.
- GPU: optional heavy generation through `--gpu-command`.

## Orchestrator

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate
```

## Hardware policy

For the current 32 GB RAM / 16 GB VRAM workstation profile:

- do not run heavy Blender rendering and large GPU LLM inference together;
- keep NPU jobs compact;
- keep NPU workers at 4 or below;
- prefer compact JSON context over full frame-level JSON;
- validate before accepting generated code.
