# Evidence Chunk 0001/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `2`
- line_end: `98`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; source_reports; source_selected_chunks_evidence. Preview: "schema_version": 1, "kind": "github_validation_evidence_bundle", "generated_at": "2026-05-07T13:33:44", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "source_reports": [ "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "github_validation_evidence_bundle",
  "generated_at": "2026-05-07T13:33:44",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "source_reports": [
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json",
    "output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json",
    "output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json",
    "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json",
    "output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
    "output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json",
    "output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
    "output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json",
    "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json",
    "output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json",
    "output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json",
    "output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json",
    "output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json",
    "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json",
    "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json",
    "output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.json",
    "output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.json",
    "docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.json",
    "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json",
    "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json",
    "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_evidence_index.json",
    "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_readiness.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json",
    "output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json"
  ],
  "source_selected_chunks_evidence": [
    "docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json"
  ],
  "source_included_artifacts": [
    "output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md",
    "output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.md",
    "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.md",
    "output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.md",
    "output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.md",
    "output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.md",
    "output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.md",
    "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.md",
    "output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.md",
    "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.md",
    "output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.md",
    "output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.md",
    "output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.md",
    "output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.md",
    "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.md",
    "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product.md",
    "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/README.md",
    "output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.md",
    "docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.md",
    "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv",
    "output/ai_pipeline/agent_review_evidence_sufficiency.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.md",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.md",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json",
    "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.md",
    "output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json",
    "output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.md",
    "output/ai_runtime_memory/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.sqlite",
    "output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md",
    "output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.md",
    "output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.md"
  ],
```

## Context after

  "reports": [
    {
      "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_gpu_npu_parallel_orchestrator",
        "passed": true,
        "provider_execution_performed": true,
