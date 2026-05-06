# GPU Peer Exchange Operational Principle

## Principle

Local AI lanes are not isolated providers.

For production IA-Carmine workflows, the canonical execution model is:

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner
GPU0 / OpenVINO = companion peer worker
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1 and GPU0 requests
```

## Primary advisory rule

GPU1/Ollama must execute the primary advisory lane for real Full0To10 runs unless explicitly disabled by an operator flag or classified as unavailable/degraded by evidence.

A Full0To10 run must not silently downgrade primary advisory to static reports, smoke-only evidence or post-run summaries.

## GPU0 companion rule

GPU0 is not complete when it only performs preflight, smoke, final workload evidence or passive support.

GPU0 must be promoted toward peer-worker behavior:

```text
GPU1 planner task packet
  -> GPU0 companion execution
  -> GPU0 response/evidence packet
  -> optional GPU0 tool requests
  -> planner/auditor consumption
  -> final telemetry, bundle and gate evidence
```

When `IA_CARMINE_GPU0_COMPANION_MODEL_DIR` is configured, GPU0 may run OpenVINO GenAI tasks on GPU.0.

When no companion model is configured, GPU0 may still produce numeric, static, tool-request or report-only evidence, but the run must classify the missing semantic companion mode explicitly.

## NPU role rule

NPU should not be the heavy audit authority when deterministic validators already cover the product.

Preferred NPU role:

```text
micro-fast task support
small checkpoint review
provider/device diagnostics
structured helper output
tool-intelligence support when cheap and available
```

Heavy audit, report validation and acceptance decisions should remain with deterministic repository scripts unless a task explicitly requests NPU semantic review.

## Runtime broker rule

The runtime tool broker may consume tool requests from both GPU1 and GPU0.

Tool execution must remain controlled, report-only by default, and visible in telemetry.

## Acceptance evidence

A production peer-exchange lane should produce or validate these surfaces:

```text
gpu1_primary_advisory_<stamp>.json/md
gpu0_peer_task_packet_<stamp>.json
gpu0_peer_response_<stamp>.json/md
gpu0_tool_requests_<stamp>.json
ai_peer_exchange_<stamp>.json/md
provider acceptance gate with peer-exchange classifications
final telemetry and bundle inclusion
```

Missing peer exchange must be classified explicitly, for example:

```text
gpu0_companion_static_report_only
gpu1_gpu0_roundtrip_missing
gpu0_tool_requests_not_broker_consumed
npu_gpu1_checkpoint_context_missing
```

## Current production chain

The maintained implementation path is not a smoke-only lane. It is wired through the Full0To10 production chain:

```text
Markdown task input
  -> unified local AI launcher
  -> full-toolbox decision loop
  -> GPU1/Ollama primary advisory report
  -> GPU0 peer task packet
  -> GPU0 OpenVINO peer response
  -> GPU0 runtime broker tool requests
  -> AI peer-exchange report
  -> peer-exchange contract
  -> Full0To10 provider acceptance gate
  -> runtime telemetry, shared AI-to-AI bundle and compact evidence
```

Current source surfaces:

```text
Tools/ai/build_ai_peer_exchange_packet.py
Tools/ai/run_gpu0_peer_companion_worker.py
Tools/validation/check_ai_peer_exchange_contract.py
Tools/validation/check_full0to10_provider_acceptance.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/agent_runtime_tool_broker.py
```

The runtime broker is the only production path for GPU1/GPU0 tool execution. GPU0 peer output may be numeric/tool evidence when `IA_CARMINE_GPU0_COMPANION_MODEL_DIR` is not configured, but that state must remain visible as `gpu0_peer_semantic_model_unconfigured`.
