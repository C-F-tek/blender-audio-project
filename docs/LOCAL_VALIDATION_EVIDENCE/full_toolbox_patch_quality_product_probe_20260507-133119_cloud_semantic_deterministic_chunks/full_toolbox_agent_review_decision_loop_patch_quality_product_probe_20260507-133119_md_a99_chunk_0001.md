# Evidence Chunk 0001/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `1`
- line_end: `264`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Local Validation Evidence Bundle; Decision summary; Reports; `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json`; `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json`. Preview: # Local Validation Evidence Bundle - Generated at: `2026-05-07T13:33:44` - Kind: `github_validation_evidence_bundle` ## Decision summary - `ollama_gpu_primary_advisory`: `False` - `npu_excluded_when_unusable`: `False` - `provider_execution_seen`: `True` - `npu...

## Chunk content

```md
# Local Validation Evidence Bundle

- Generated at: `2026-05-07T13:33:44`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `42`
- `patch_plan_summary_seen`: `True`

## Reports

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `collect_more_evidence`

### `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_consistency_map_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `185`

### `output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_hardware_governance_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['GPU.1 is visible to OpenVINO but reserved for Ollama/CUDA; do not route OpenVINO work there by default.', 'IA_CARMINE_GPU0_COMPANION_MODEL_DIR is not configured; GPU0 semantic peer mode will classify as unconfigured/fallback.']`

### `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_evidence_contract`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `["local provider probe degraded: ['ollama: probe failed']"]`

### `output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_worker_lane`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; semantic LLM subtasks unavailable, numeric/tool companion active.']`

### `output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_companion_contract`
- Passed: `True`

### `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `openvino_gpu0_secondary_workload`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['OpenVINO GPU.1 is visible but reserved; no workload was executed on GPU.1.']`

### `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu1_primary_advisory`
- Passed: `True`
- Provider execution performed: `True`
- Recommendation count: `0`

### `output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_task_packet`
- Passed: `True`

### `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_response`
- Passed: `True`
- Provider execution performed: `True`
- Warnings: `['IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only.']`

### `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu0_peer_tool_requests`
- Passed: `None`

### `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_micro_peer_assistant`
- Passed: `True`
- Provider execution performed: `False`
- Warnings: `['NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.']`

### `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_runtime_tool_broker`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Warnings: `['NPU peer provider deferred to avoid OpenVINO/NPU contention while GPU1/GPU0 produce the product evidence.']`

```

## Context after

### `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_peer_exchange`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
