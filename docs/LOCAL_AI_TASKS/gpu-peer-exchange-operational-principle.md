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
