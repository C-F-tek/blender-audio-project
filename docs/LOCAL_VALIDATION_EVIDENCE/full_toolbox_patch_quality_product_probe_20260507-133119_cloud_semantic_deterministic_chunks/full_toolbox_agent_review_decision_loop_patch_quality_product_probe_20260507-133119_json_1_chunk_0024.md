# Evidence Chunk 0024/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `2631`
- line_end: `2797`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0023.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0025.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: included_artifacts. Preview: "chunk_size_lines": 200, "chunk_count": 41, "first_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1-L200", "last_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_prob...

## Context before

      "exists": true,
      "suffix": ".json",
      "size_bytes": 368889,
      "sha256": "b1598bb0f81214786c9d9072a5fcd6462442c54aab95a533bc00612e7cb03eb1",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": true,
      "line_count": 8101,
      "raw_chars": 360788,
      "included_chars": 16000,
      "content": "{\n  \"schema_version\": 1,\n  \"kind\": \"deterministic_recommendation_synthesizer\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"manual_review_required\": true,\n  \"recommendation_count\": 20,\n  \"recommendations\": [\n    {\n      \"id\": \"consistency_001\",\n      \"area\": \"md_python\",\n      \"status\": \"ready_for_patch_plan\",\n      \"target_files\": [\n        \"CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md\"\n      ],\n      \"rationale\": \"Repository consistency mapper reported high `md_python_command_script_missing` at `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324` targeting `Tools/ai/agent_memory_tools.py`.\",\n      \"proposed_strategy\": \"Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324`. Target `CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md` and resolve `Tools/ai/agent_memory_tools.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.\",\n      \"risk\": \"medium\",\n      \"validation_commands\": [\n        \"python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json\",\n        \"python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json\",\n        \"git diff --check\",\n        \"git status --short\"\n      ],\n      \"stop_conditions\": [\n        \"Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.\",\n        \"Stop if the target/source evidence no longer exists after refreshing master.\",\n        \"Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.\",\n        \"Stop if resolving the finding requires inventing behavior not supported by code evidence.\"\n      ],\n      \"source\": \"repository_consistency_map\",\n      \"evidence\": [\n        \"CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md:324\"\n      ],\n      \"tool_evidence\": [\n        {\n          \"path\": \"output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"repository_consistency_map\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"repository_consistency_map_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"code_interpreter_report\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"python_line_count_csv\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"python_syntax\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu_planner_json_contract_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"deterministic_recommendation_synthesizer_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"agent_review_decision_loop_smoke\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"npu_provider_environment\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"openvino_hardware_governance_report\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu_planner_json_contract_replay\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu_npu_run_sync_analysis\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"provider_evidence_contract\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu0_companion_worker_lane\",\n          \"passed\": true,\n          \"tool_request_count\": 4,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu0_companion_contract\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json\",\n          \"kind\": \"openvino_gpu0_secondary_workload\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu1_primary_advisory\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu0_peer_task_packet\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu0_peer_response\",\n          \"passed\": true,\n          \"tool_request_count\": 3,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"gpu0_peer_tool_requests\",\n          \"passed\": null,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"agent_runtime_tool_broker\",\n          \"passed\": true,\n          \"tool_request_count\": 3,\n          \"tool_execution_count\": 3,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"npu_micro_peer_assistant\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"agent_runtime_tool_broker\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": false,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"ai_peer_exchange\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"ai_peer_exchange_contract\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": true,\n          \"patch_application_performed\": false\n        },\n        {\n          \"path\": \"output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"provider_runtime_heap_live_signals\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"provider_runtime_heap_live_signals\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"provider_runtime_heap_live_signals\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json\",\n          \"kind\": \"provider_runtime_heap_live_signals\",\n          \"passed\": true,\n          \"tool_request_count\": null,\n          \"tool_execution_count\": null,\n          \"failed_tool_count\": null,\n          \"blocked_tool_count\": null,\n          \"provider_execution_performed\": null,\n          \"patch_application_performed\": null\n        },\n        {\n          \"path\": \"output/ai_runtime_heap/patch_quality_product_probe_202605",

## Chunk content

```json
      "chunk_size_lines": 200,
      "chunk_count": 41,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L8001-L8101",
      "chunk_pointers": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L201-L400",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1-L200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L401-L600",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L201-L400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L601-L800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L601-L800",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L401-L600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L801-L1000",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 801,
          "line_end": 1000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L601-L800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1001-L1200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1001-L1200",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 1001,
          "line_end": 1200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L801-L1000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1201-L1400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1201-L1400",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 1201,
          "line_end": 1400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1001-L1200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1401-L1600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1401-L1600",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 1401,
          "line_end": 1600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1201-L1400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1601-L1800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1601-L1800",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 1601,
          "line_end": 1800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1401-L1600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1801-L2000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1801-L2000",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 1801,
          "line_end": 2000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1601-L1800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2001-L2200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2001-L2200",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 2001,
          "line_end": 2200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L1801-L2000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2201-L2400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2201-L2400",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 2201,
          "line_end": 2400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2001-L2200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2401-L2600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2401-L2600",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 2401,
          "line_end": 2600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2201-L2400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2601-L2800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2601-L2800",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 2601,
          "line_end": 2800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2401-L2600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2801-L3000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2801-L3000",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 2801,
          "line_end": 3000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2601-L2800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3001-L3200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3001-L3200",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 3001,
          "line_end": 3200,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L2801-L3000",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3201-L3400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3201-L3400",
```

## Context after

          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 3201,
          "line_end": 3400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3001-L3200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3401-L3600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json#L3401-L3600",
          "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json",
          "line_start": 3401,
