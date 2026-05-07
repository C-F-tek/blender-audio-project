# Evidence Chunk 0020/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `2391`
- line_end: `2510`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0019.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0021.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: included_artifacts. Preview: }, { "path": "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.md", "exists": true, "suffix": ".md", "size_bytes": 2552, "sha256": "63b7c69ccaef42de46774d1ddbd222097de9403d84a93aad79f52b8c9e77c7ad", "role": "auto_related_...

## Context before

      "exists": true,
      "suffix": ".md",
      "size_bytes": 1192,
      "sha256": "11242ce1279e1995b4c882843d56f94a56525ff99581c8b89c58e50f6ab198da",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 23,
      "raw_chars": 1169,
      "included_chars": 1169,
      "content": "# AI Peer Exchange\n\n- Passed: `True`\n- Provider execution performed: `True`\n- Classifications: `['gpu0_peer_semantic_model_unconfigured']`\n- Task count: `4`\n- GPU0 response passed: `True`\n- Broker executions: `3`\n- NPU micro lane seen: `True`\n- NPU broker executions: `0`\n- Peer mesh all lanes visible: `True`\n- NPU support tool supply: `False`\n- NPU slow/degraded non-blocking: `False`\n- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`\n- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`\n- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`\n- Peer mesh product blockers: `[]`\n- Provider-broker loop active: `True`\n- Provider-broker controlled executor: `runtime_tool_broker`\n- Provider-broker direct tool execution allowed: `False`\n- Provider-broker topology: `input_md -> deterministic_baseline -> GPU1 -> GPU0 -> broker -> NPU_support -> broker -> contract -> telemetry -> bundle -> patch_plan`\n- Provider-broker GPU0 executions: `3`\n- Provider-broker NPU executions: `0`\n"

## Chunk content

```json
    },
    {
      "path": "output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 2552,
      "sha256": "63b7c69ccaef42de46774d1ddbd222097de9403d84a93aad79f52b8c9e77c7ad",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 48,
      "raw_chars": 2504,
      "included_chars": 2504,
      "content": "# AI Peer Exchange Contract\n\n- Passed: `True`\n- Provider execution performed: `True`\n- Classifications: `['peer_mesh_degraded_lanes_present_non_blocking', 'gpu0_peer_semantic_model_unconfigured']`\n\n## Evidence\n\n- `gpu1_primary_advisory` exists=`True` passed=`True` path=`output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`\n- `gpu0_peer_task_packet` exists=`True` passed=`True` path=`output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json`\n- `gpu0_peer_response` exists=`True` passed=`True` path=`output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`\n- `gpu0_tool_requests` exists=`True` passed=`None` path=`output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`\n- `gpu0_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`\n- `npu_micro_response` exists=`True` passed=`True` path=`output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`\n- `npu_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`\n- `ai_peer_exchange` exists=`True` passed=`True` path=`output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`\n\n## Peer mesh visibility\n\n- Passed: `True`\n- GPU1 sees GPU0 response: `True`\n- GPU1 sees NPU support signal: `True`\n- GPU0 sees GPU1 primary advisory: `True`\n- NPU sees GPU1/GPU0/broker context: `True`\n- NPU support tool supply: `False`\n- NPU slow/degraded non-blocking: `False`\n- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`\n- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`\n- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`\n- Peer mesh product blockers: `[]`\n\n## Provider-broker loop\n\n- Passed: `True`\n- Active: `True`\n- Controlled executor: `runtime_tool_broker`\n- Direct tool execution allowed: `False`\n- Broker tool executions: `3`\n- GPU0 broker executions: `3`\n- NPU broker executions: `0`\n- NPU non-blocking: `True`\n- NPU product pass blocker: `False`\n- Deterministic scripts heavy audit authority: `True`\n- Product blockers: `[]`\n\n## Warnings\n\n- gpu0_peer_semantic_model_unconfigured\n"
    },
    {
      "path": "output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 1187,
      "sha256": "98fb493f0c05adc084c975124172ae3d88e32f65394f601a53a140e3a91ec40c",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 19,
      "raw_chars": 1168,
      "included_chars": 1168,
      "content": "# Provider Runtime Heap From Peer Reports\n\n- passed: `True`\n- stamp: `patch_quality_product_probe_20260507-133119`\n- event_count: `11`\n- heap_event_count: `32`\n- pending_broker_request_count: `0`\n- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`\n\n## Reports\n\n- `gpu1`: `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`\n- `gpu0`: `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`\n- `gpu0_tool_requests`: `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`\n- `gpu0_broker`: `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`\n- `npu`: `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`\n- `npu_broker`: `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`\n- `peer_exchange`: `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`\n- `peer_contract`: `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json`\n"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 1214,
      "sha256": "3de77760ff64f3a96e057f16c2b5e517907dae356cac04014a521c37ed562b33",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 46,
      "raw_chars": 1168,
      "included_chars": 1168,
      "content": "# Provider Runtime Heap Telemetry\n\n- passed: `True`\n- stamp: `patch_quality_product_probe_20260507-133119`\n- event_count: `32`\n- parse_error_count: `0`\n- tool_catalog_exchange_complete_count: `0`\n- gpu1_to_gpu0_event_count: `2`\n- gpu0_to_gpu1_event_count: `7`\n- gpu1_gpu0_bidirectional: `True`\n- gpu1_gpu0_correlated_exchange_count: `2`\n- broker_request_count: `6`\n- broker_result_count: `6`\n- pending_broker_request_count: `0`\n- validation_signal_count: `1`\n- direct_execution_violation_count: `0`\n- tool_catalog_tool_count: `10`\n\n## Events by lane\n\n- `broker`: `6`\n- `deterministic`: `1`\n- `gpu0`: `13`\n- `gpu1`: `2`\n- `npu`: `2`\n- `orchestrator`: `8`\n\n## Events by type\n\n- `broker_request`: `6`\n- `broker_result`: `6`\n- `evidence_request`: `7`\n- `evidence_response`: `9`\n- `provider_state`: `3`\n- `validation_signal`: `1`\n\n## Interaction edges\n\n- `broker->gpu0:broker_result`: `6`\n- `deterministic->gpu1:validation_signal`: `1`\n- `gpu0->broker:broker_request`: `6`\n- `gpu0->gpu1:evidence_response`: `7`\n- `gpu1->gpu0:evidence_request`: `2`\n- `npu->gpu1:evidence_response`: `2`\n- `orchestrator->gpu0:evidence_request`: `5`\n- `orchestrator->none:provider_state`: `3`\n"
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 308,
      "sha256": "2143ea48a3ec3e60f825e53c855ad2763749797241b0bcece0b6de9cf9129b7e",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 9,
      "raw_chars": 299,
      "included_chars": 299,
      "content": "# Provider Runtime Heap Live Signals\n\n- passed: `True`\n- stamp: `patch_quality_product_probe_20260507-133119`\n- mode: `init`\n- event_count: `1`\n- heap_event_count: `1`\n- pending_broker_request_count: `0`\n- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`\n"
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 317,
      "sha256": "39505d921f837340642180397a0f97e5c20337a0b09b53879219b5f63995865d",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 9,
      "raw_chars": 308,
      "included_chars": 308,
      "content": "# Provider Runtime Heap Live Signals\n\n- passed: `True`\n- stamp: `patch_quality_product_probe_20260507-133119`\n- mode: `gpu1-request`\n- event_count: `1`\n- heap_event_count: `13`\n- pending_broker_request_count: `0`\n- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`\n"
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 319,
      "sha256": "cb612b56344462950625629ede0810436bd01eaf5d7e3a16bcca2df89d5eeb59",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 9,
      "raw_chars": 310,
      "included_chars": 310,
      "content": "# Provider Runtime Heap Live Signals\n\n- passed: `True`\n- stamp: `patch_quality_product_probe_20260507-133119`\n- mode: `broker-results`\n- event_count: `3`\n- heap_event_count: `20`\n- pending_broker_request_count: `0`\n- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`\n"
    },
    {
      "path": "output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 316,
      "sha256": "d1f4af305b48b9e8a7d9c22947ac2fbe72647def537c6cfc32f20bbdf512bb0d",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 9,
      "raw_chars": 307,
      "included_chars": 307,
      "content": "# Provider Runtime Heap Live Signals\n\n- passed: `True`\n- stamp: `patch_quality_product_probe_20260507-133119`\n- mode: `npu-support`\n- event_count: `1`\n- heap_event_count: `21`\n- pending_broker_request_count: `0`\n- event_log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`\n"
    },
    {
      "path": "output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 2493,
      "sha256": "92257aa5a2499b1abd1daf4f8b15356114edd356126c514e3c8697c14ec6188d",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 40,
      "raw_chars": 2453,
      "included_chars": 2453,
      "content": "# Provider Runtime Heap Snapshot\n\n- Stamp: `patch_quality_product_probe_20260507-133119`\n- Event count: `32`\n- Parse error count: `0`\n- Pending broker requests: `0`\n- Event log: `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/events.jsonl`\n\n## Runtime architecture\n\n- `gpu1`: `primary_advisory_planner`\n- `gpu0`: `coworker_helper_openvino`\n- `npu`: `microtask_responder`\n- `broker`: `single_controlled_executor`\n- `semantic_tools_registry`: `agent_runtime_tool_broker.TOOL_SPECS`\n- `deterministic_validators`: `cpu_authority_validation_lane`\n- `telemetry`: `append_only_event_stream`\n\n## Events by lane\n\n- `orchestrator`: `{'event_count': 8, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'provider_state': 3, 'evidence_request': 5}}`\n- `gpu0`: `{'event_count': 13, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'evidence_response': 7, 'broker_request': 6}}`\n- `gpu1`: `{'event_count': 2, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'evidence_request': 2}}`\n- `broker`: `{'event_count': 6, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'broker_result': 6}}`\n- `npu`: `{'event_count': 2, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'evidence_response': 2}}`\n- `deterministic`: `{'event_count': 1, 'latest_event_at': '2026-05-07T13:33:30', 'event_types': {'validation_signal': 1}}`\n\n## Semantic tools registry\n\n- Tool count: `10`\n- `build_agent_agnostic_tool_inventory`: Inventory existing reusable IA-Carmine tools and guardrails.\n- `build_agent_memory_inventory`: Read-only SQLite/JSONL agent memory inventory.\n- `build_agent_transient_request_context`: Build request-scoped context from memory notes, raw files and reports.\n- `build_code_interpreter_report`: Build static code-interpreter style report over selected roots.\n- `build_python_line_count_csv`: Build full Python line-count CSV/JSON/MD evidence.\n- `build_refactor_duplication_audit`: Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.\n- `check_python_syntax`: Validate Python syntax across repository.\n- `check_validation_report_contract`: Validate validation report contract for a scoped report-dir or explicit report files.\n- `run_gpu_planner_json_contract_smoke`: Run GPU planner JSON contract smoke tests without provider.\n- `runtime_sqlite_memory`: Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.\n"
```

## Context after

    },
    {
      "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 7008,
      "sha256": "5de59cd339a0b56850f03005bab50888d9ae7f3584bb97ad9025909c0bd426df",
      "role": "explicit_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 78,
