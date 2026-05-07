# Evidence Chunk 0002/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `99`
- line_end: `454`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0001.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0003.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports. Preview: "reports": [ { "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json", "exists": true, "json_ok": true, "kind": "agent_gpu_npu_parallel_orchestrator", "passed": true, "summary": { "schema_version": 1, "kind": "a...

## Context before

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

## Chunk content

```json
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
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_deep_planning_supervised",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_supervised",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "recommendation_count": 0,
        "round_count": 4,
        "empty_recommendations_reason": "model_output_schema_mismatch",
        "evidence_ready_for_manual_patch_count": 0,
        "recommended_next_layer": "collect_more_evidence"
      }
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "repository_consistency_map",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "repository_consistency_map_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "code_interpreter_report",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "code_interpreter_report",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true,
        "recommendation_count": 185
      }
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_line_count_csv",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "python_line_count_csv",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_syntax",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "python_syntax",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_planner_json_contract_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu_planner_json_contract_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "deterministic_recommendation_synthesizer_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true,
        "recommendation_count": 1
      }
    },
    {
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_review_decision_loop_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "patch_plan_count": 1,
        "manual_review_required": true,
        "recommendation_count": 1
      }
    },
    {
      "path": "output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_provider_environment",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "npu_provider_environment",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "checks": {}
      }
    },
    {
      "path": "output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "openvino_hardware_governance_report",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "openvino_hardware_governance_report",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [
          "GPU.1 is visible to OpenVINO but reserved for Ollama/CUDA; do not route OpenVINO work there by default.",
          "IA_CARMINE_GPU0_COMPANION_MODEL_DIR is not configured; GPU0 semantic peer mode will classify as unconfigured/fallback."
        ]
      }
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_planner_json_contract_replay",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu_planner_json_contract_replay",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_npu_run_sync_analysis",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu_npu_run_sync_analysis",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "provider_evidence_contract",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "provider_evidence_contract",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [
          "local provider probe degraded: ['ollama: probe failed']"
        ],
        "manual_review_required": true
      }
    },
    {
      "path": "output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu0_companion_worker_lane",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu0_companion_worker_lane",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": [
          "IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; semantic LLM subtasks unavailable, numeric/tool companion active."
        ]
      }
    },
    {
      "path": "output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu0_companion_contract",
      "passed": true,
      "summary": {
        "schema_version": 3,
        "kind": "gpu0_companion_contract",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json",
      "exists": true,
      "json_ok": true,
      "kind": "openvino_gpu0_secondary_workload",
      "passed": true,
      "summary": {
        "schema_version": 2,
        "kind": "openvino_gpu0_secondary_workload",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [
          "OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1."
        ]
      }
    },
    {
      "path": "output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu1_primary_advisory",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu1_primary_advisory",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": [],
        "recommendation_count": 0,
        "round_count": 4
      }
    },
    {
      "path": "output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json",
```

## Context after

      "exists": true,
      "json_ok": true,
      "kind": "gpu0_peer_task_packet",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu0_peer_task_packet",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
