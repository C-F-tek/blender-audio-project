# NPU/GPU Parallelism Plan

## Objective

Use the local machine as a heterogeneous AI workstation without forcing one model to span multiple devices.

The design uses task-level parallelism:

- CPU for deterministic preparation and validation;
- NPU for compact review/classification tasks;
- GPU for heavy generation.

## Execution lanes

```text
CPU lane:
  parse -> summarize -> validate -> write reports

NPU lane:
  compact artifact review -> warning detection -> candidate scoring

GPU lane:
  optional external planner/generator -> scene spec/code/patch plan
```

## Orchestrator

The entry point is:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --dry-run
```

The NPU lane is enabled only with:

```powershell
--use-npu
```

The GPU lane is enabled only by passing an explicit command:

```powershell
--gpu-command "py .\Tools\ai\your_gpu_generator.py --input {brief} --output {output}"
```

## Hardware policy for current workstation

For the current 32 GB RAM / 16 GB VRAM workstation profile:

- do not run heavy Blender rendering and large GPU LLM inference together;
- keep NPU jobs compact;
- keep NPU workers at 4 or below;
- prefer compact JSON context over full frame-level analysis files;
- run validation before accepting generated code.
