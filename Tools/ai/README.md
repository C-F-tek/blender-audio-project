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

Select focused semantic chunks for a task:

```powershell
py .\Tools\ai\select_semantic_code_chunks.py `
  --repo-root . `
  --query "workflow adapter local ai full context enrichment selected chunks sqlite memory provider multistep proposals validators" `
  --path-boost Tools/workflow `
  --path-boost Tools/ai `
  --path-boost Tools/validation `
  --output .\output\ai_context_packs\selected_chunks_focus.json `
  --markdown-output .\output\ai_context_packs\selected_chunks_focus.md
```

Build a bounded context pack:

```powershell
py .\Tools\ai\build_ai_context_pack.py `
  --repo-root . `
  --profile core_ai_backend `
  --basename project_self_improvement_context_pack `
  --evidence-basename project_self_improvement_context_pack_evidence
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

Build a report-only selective execution plan:

```powershell
py .\Tools\ai\build_selective_execution_plan.py `
  --repo-root . `
  --output .\output\ai_pipeline\selective_execution_plan.json `
  --markdown-output .\output\ai_pipeline\selective_execution_plan.md
```

Build deterministic full-context golden proposal families:

```powershell
py .\Tools\ai\build_full_context_golden_proposals.py `
  --repo-root . `
  --source-report .\output\local_ai_runs\<run>\pipeline\full_context_golden_local_ai_context_proposals.json `
  --output .\output\ai_pipeline\full_context_golden_proposals.json `
  --markdown-output .\output\ai_pipeline\full_context_golden_proposals.md
```

Run the safe orchestrator:

```powershell
py .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate
```

## Device strategy

- CPU: parsing, JSON generation, validation, orchestration.
- GPU/Ollama: primary advisory lane only when explicitly requested and quality-gated.
- NPU/OpenVINO: probe, guardrail, decode diagnostic and possible future lightweight context-preparation helper.
- External GPU commands: optional explicit heavy generator path, never implicit.

## Current self-improvement loop

The current local AI workbench can now build a bounded, reviewable loop:

```text
Markdown task
  -> semantic chunks
  -> selected semantic chunks
  -> context pack
  -> agent state packet
  -> explicit multistep GPU/NPU evidence
  -> repository proposals
  -> full-context golden proposal families
  -> manual-review-only patch-spec candidates
```

All tools in this folder are expected to remain report-only or explicit-run. They must not apply patches, edit Blender runtime files, edit full analysis JSON files or execute providers implicitly.

## Agent state packets

`build_agent_state_packet.py` creates a generic JSON/Markdown packet for app or agent use. It combines included files, persistent JSONL or SQLite memory records and recent CLI notes, then emits planned microtasks for CPU, NPU, GPU and validation lanes.

The tool is non-invasive: it does not run Blender, model inference, FFmpeg, GPU work or NPU work. It only writes packet artifacts under the selected output folder.

`review_agent_memory.py` applies retention, quarantine and promotion-candidate policy. It never deletes memory and never promotes records into documentation automatically.
