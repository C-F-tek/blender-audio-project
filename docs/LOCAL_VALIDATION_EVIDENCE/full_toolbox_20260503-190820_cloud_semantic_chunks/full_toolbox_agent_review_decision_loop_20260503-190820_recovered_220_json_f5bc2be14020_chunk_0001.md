# Evidence Chunk 0001/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `2`
- line_end: `35`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0002.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Fornire un bundle di evidenze di validazione per il progetto “blender‑audio‑project”, includendo report di pipeline AI, analisi di coerenza del repository, sincronizzazione GPU/NPU e piani di patch.  
**Segnali principali**: risultati di orchestrazione, parallelismo GPU, raccomandazioni deterministiche, loop decisionale di revisione agente, mappature di coerenza e telemetria d’uso runtime.  
**Guardrail / errori**: eventuali incongruenze nei file JSON/MD, errori di sincronizzazione GPU/NPU, e anomalie nei piani di patch (verificati nei report di valid

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "github_validation_evidence_bundle",
  "generated_at": "2026-05-03T20:03:07",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "source_reports": [
    "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json",
    "output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json",
    "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.json",
    "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_agent_review_decision_loop_recovered_220.json",
    "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.json"
  ],
  "source_selected_chunks_evidence": [
    "docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json"
  ],
  "source_included_artifacts": [
    "output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.md",
    "output/ai_pipeline/full_toolbox_20260503-190820_agent_review_decision_loop_recovered_220.md",
    "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md",
    "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260503-190820.md",
    "output/ai_pipeline/agent_review_evidence_sufficiency.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.md",
    "output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json",
    "output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.md",
    "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.md",
    "output/analysis/repository_consistency_map_full_toolbox_20260503-190820.md",
    "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.md"
  ],
```

## Context after

  "reports": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": false,
      "summary": {
        "schema_version": 1,
        "kind": "agent_gpu_npu_parallel_orchestrator",
        "passed": false,
        "provider_execution_performed": true,
