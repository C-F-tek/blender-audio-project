# Evidence Chunk 0001/0004

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `cf4364b662a4a63fc507c4039335852a4f76f55ebf6e95c2f55e0b56fa0bc9ae`
- line_start: `2`
- line_end: `99`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_patch_quality_product_probe_20260507-133119_json_cf4364_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; stamp; provider_execution_performed. Preview: "schema_version": 1, "kind": "full_toolbox_run_telemetry_summary", "generated_at": "2026-05-07T13:33:46", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "stamp": "patch_quality_product_probe_20260507-133119", "passed": true, "errors": [], "wa...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "full_toolbox_run_telemetry_summary",
  "generated_at": "2026-05-07T13:33:46",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "stamp": "patch_quality_product_probe_20260507-133119",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "provider_evidence": {
    "provider_execution_requested": true,
    "provider_execution_performed": true,
    "gpu_provider_execution_performed": true,
    "gpu0_peer_support_provider_execution_performed": true,
    "gpu0_peer_support_count": 5,
    "gpu0_peer_support_success_count": 5,
    "gpu0_peer_support_overlap_count": 4,
    "gpu_round_count": 4,
    "gpu_returncode": 0,
    "gpu_classification": null,
    "gpu_provider_empty_response": false,
    "legacy_npu_auditor_provider_requested": false,
    "npu_provider_execution_performed": false,
    "legacy_npu_provider_execution_performed": false,
    "npu_micro_provider_execution_performed": false,
    "npu_micro_tool_lane_performed": false,
    "npu_micro_support_count": 0,
    "npu_micro_support_success_count": 0,
    "npu_micro_support_provider_success_count": 0,
    "npu_micro_support_tool_success_count": 0,
    "npu_micro_support_overlap_count": 0,
    "npu_micro_support_tool_request_count": 0,
    "npu_micro_runtime_tool_execution_count": 0,
    "npu_audit_count": 0,
    "npu_audit_success_count": 0,
    "npu_lane_mode": "metadata_only",
    "provider_degraded_reasons": []
  },
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "decision_loop": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json",
    "recommendations": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
    "patch_plan": "output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json",
    "repository_consistency": "output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "repository_consistency_smoke": "output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "gpu_npu_sync": "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "orchestrator": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
    "gpu_report": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json",
    "peer_exchange": "output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json",
    "peer_contract": "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json",
    "provider_runtime_heap_telemetry": "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json",
    "provider_runtime_heap_snapshot": "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json",
    "provider_runtime_heap_live_signals": [
      "output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json",
      "output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json",
      "output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json",
      "output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json"
    ],
    "line_count_csv": "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv"
  },
  "run_parameters": {
    "budget_minutes": 5,
    "max_rounds": 4,
    "files_per_round": 4,
    "max_context_files": 80,
    "max_chars_per_file": 4000,
    "max_new_tokens": 1600,
    "npu_auditor_every_rounds": 3,
    "repository_consistency_map_workers": 0
  },
  "workflow_summary": {
    "passed": true,
    "recommendation_count": 20,
    "patch_plan_count": 20,
    "deterministic_synthesizer_used": true,
    "patch_plan_fallback_used": null,
    "bundle_validation_passed": true,
    "evidence_to_commit": [
      "docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_patch_quality_product_probe_20260507-133119.json",
      "docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_patch_quality_product_probe_20260507-133119.md",
      "docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_patch_quality_product_probe_20260507-133119.csv",
      "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json",
      "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md",
      "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json",
      "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.md",
      "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.json",
      "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.md",
      "docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.json",
      "docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.md",
      "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json",
      "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.md",
      "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv"
    ]
  },
```

## Context after

  "recommendations_first20": [
    {
      "id": "consistency_001",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
