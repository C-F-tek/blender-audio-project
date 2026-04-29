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

Build a generic agent state packet:

```powershell
py .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan Blender/audio app smoke tests" --include-file .\docs\AI_SMART_POLICY.md --include-file .\docs\LOCAL_AI_WORKFLOW.md
```

Use optional SQLite persistent memory:

```powershell
py .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan Blender/audio app smoke tests" --memory-db .\indexAI\agent_memory\agent_memory.sqlite --save-inputs-to-memory-db --memory-note "Keep NPU guardrails non-blocking."
```

Review memory retention and promotion candidates:

```powershell
py .\Tools\ai\review_agent_memory.py --repo-root .
```

Run the safe orchestrator:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate
```

## Device strategy

- CPU: parsing, JSON generation, validation, orchestration.
- NPU: short artifact review and scoring lane.
- GPU: optional external heavy generator passed through `--gpu-command`.

## Agent state packets

`build_agent_state_packet.py` creates a generic JSON/Markdown packet for app or agent use. It combines included files, persistent JSONL or SQLite memory records and recent CLI notes, then emits planned microtasks for CPU, NPU, GPU and validation lanes.

The tool is non-invasive: it does not run Blender, model inference, FFmpeg, GPU work or NPU work. It only writes packet artifacts under the selected output folder.

`review_agent_memory.py` applies retention, quarantine and promotion-candidate policy. It never deletes memory and never promotes records into documentation automatically.
