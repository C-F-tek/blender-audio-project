# AI Tools

Additive tools for AI-assisted artifact production.

These tools do not replace Blender runtime packages and do not modify raw analysis JSON files.

## Commands

Build compact music artifacts:

```powershell
py .\Tools\ai\build_music_intermediates.py --analysis-json .\output\track_analysis.json --output-dir .\output\ai_pipeline
```

Build semantic chunks:

```powershell
py .\Tools\npu\build_semantic_code_chunks.py --repo-root .
```

Run the safe orchestrator:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate
```

## Device strategy

- CPU: parsing, JSON generation, validation, orchestration.
- NPU: short artifact review and scoring lane.
- GPU: optional external heavy generator passed through `--gpu-command`.
