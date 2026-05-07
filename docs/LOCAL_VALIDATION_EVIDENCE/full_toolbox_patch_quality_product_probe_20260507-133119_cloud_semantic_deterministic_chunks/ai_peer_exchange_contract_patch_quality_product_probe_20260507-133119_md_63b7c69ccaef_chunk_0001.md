# Evidence Chunk 0001/0001

- source: `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `63b7c69ccaef42de46774d1ddbd222097de9403d84a93aad79f52b8c9e77c7ad`
- line_start: `1`
- line_end: `48`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: AI Peer Exchange Contract; Evidence; Peer mesh visibility; Provider-broker loop; Warnings. Preview: # AI Peer Exchange Contract - Passed: `True` - Provider execution performed: `True` - Classifications: `['peer_mesh_degraded_lanes_present_non_blocking', 'gpu0_peer_semantic_model_unconfigured']` ## Evidence - `gpu1_primary_advisory` exists=`True` passed=`True...

## Chunk content

```md
# AI Peer Exchange Contract

- Passed: `True`
- Provider execution performed: `True`
- Classifications: `['peer_mesh_degraded_lanes_present_non_blocking', 'gpu0_peer_semantic_model_unconfigured']`

## Evidence

- `gpu1_primary_advisory` exists=`True` passed=`True` path=`output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json`
- `gpu0_peer_task_packet` exists=`True` passed=`True` path=`output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json`
- `gpu0_peer_response` exists=`True` passed=`True` path=`output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json`
- `gpu0_tool_requests` exists=`True` passed=`None` path=`output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json`
- `gpu0_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- `npu_micro_response` exists=`True` passed=`True` path=`output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json`
- `npu_runtime_tool_broker` exists=`True` passed=`True` path=`output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json`
- `ai_peer_exchange` exists=`True` passed=`True` path=`output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json`

## Peer mesh visibility

- Passed: `True`
- GPU1 sees GPU0 response: `True`
- GPU1 sees NPU support signal: `True`
- GPU0 sees GPU1 primary advisory: `True`
- NPU sees GPU1/GPU0/broker context: `True`
- NPU support tool supply: `False`
- NPU slow/degraded non-blocking: `False`
- Peer mesh operational lanes: `['gpu1_ollama_primary_advisory', 'gpu0_openvino_peer_companion', 'runtime_tool_broker', 'deterministic_scripts', 'npu_nonblocking_tool_support']`
- Peer mesh support lanes: `['gpu0_openvino_numeric_tool_peer', 'gpu0_brokered_tool_supply']`
- Peer mesh degraded lanes: `['gpu0_semantic_companion_model_unconfigured']`
- Peer mesh product blockers: `[]`

## Provider-broker loop

- Passed: `True`
- Active: `True`
- Controlled executor: `runtime_tool_broker`
- Direct tool execution allowed: `False`
- Broker tool executions: `3`
- GPU0 broker executions: `3`
- NPU broker executions: `0`
- NPU non-blocking: `True`
- NPU product pass blocker: `False`
- Deterministic scripts heavy audit authority: `True`
- Product blockers: `[]`

## Warnings

- gpu0_peer_semantic_model_unconfigured
```
