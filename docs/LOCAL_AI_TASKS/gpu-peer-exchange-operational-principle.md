# GPU Peer Exchange Operational Principle

## Principle

Local AI lanes are not isolated providers.

For production IA-Carmine workflows, the canonical execution model is:

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner/worker
GPU0 / OpenVINO = companion peer worker and tool-request producer
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1, GPU0 and NPU requests
```

## Primary advisory rule

GPU1/Ollama must execute the primary advisory lane for real Full0To10 runs unless explicitly disabled by an operator flag or classified as unavailable/degraded by evidence.

A Full0To10 run must not silently downgrade primary advisory to static reports, smoke-only evidence or post-run summaries.

## GPU0 companion rule

GPU0 is not complete when it only performs preflight, smoke, final workload evidence or passive support.

GPU0 must be promoted toward peer-worker behavior:

```text
GPU1 planner/worker task packet
  -> GPU0 companion execution
  -> GPU0 response/evidence packet
  -> optional GPU0 tool requests
  -> runtime broker execution for GPU0 requests
  -> non-blocking NPU micro/tool-support signal
  -> runtime broker execution for NPU requests when present
  -> GPU1 planner/auditor consumption
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

When provider lanes are selected, the NPU support lane should see the GPU1/GPU0 roundtrip and broker evidence as read-only context, may emit lightweight tool requests, and must remain non-blocking.

The production NPU provider path is now called by `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` itself. The orchestrator creates a `round_000` mesh bootstrap seed and starts a bounded NPU micro-support transaction alongside GPU1 and GPU0. Additional NPU micro transactions may be launched from GPU1 checkpoints and runtime-heap/toolbox context. The legacy parallel NPU auditor remains diagnostics-only and must be enabled explicitly with `-RunLegacyNpuAuditorProvider`.

## Mesh visibility and slow NPU support rule

The final product must make the GPU1/GPU0/NPU collaboration visible as a mesh, not as disconnected artifacts.

Required visibility:

```text
GPU1 sees GPU0 response and GPU0 broker results
GPU1 sees NPU support signal and NPU broker results when present
GPU0 sees GPU1 primary advisory and deterministic source reports
NPU starts from orchestrator round_000 and then sees GPU1/GPU0/broker context as read-only input
runtime broker remains visible as the only tool execution channel
NPU micro broker requests are executed during live harvest when the micro-support process finishes while GPU1 is still active
NPU launch also creates one broker-controlled live tool seed so short GPU1 runs receive NPU-lane tool evidence before the slower NPU provider returns
```

The NPU lane is allowed to be slow, empty, timed out or dependency-degraded. That state must be classified and surfaced, but it must remain non-blocking when the NPU still supplies deterministic fallback/tool-support requests or when deterministic scripts already provide heavy audit authority.

The NPU must not become the heavy audit authority and must not mark product pass/fail directly. Its production role is support intelligence and brokered tool-supply amplification.

## Runtime broker rule

The runtime tool broker may consume tool requests from GPU1, GPU0 and NPU support reports.

Tool execution must remain controlled, report-only by default, and visible in telemetry.

## Acceptance evidence

A production peer-exchange lane should produce or validate these surfaces:

```text
gpu1_primary_advisory_<stamp>.json/md
gpu0_peer_task_packet_<stamp>.json
gpu0_peer_response_<stamp>.json/md
gpu0_tool_requests_<stamp>.json
gpu0_peer_runtime_tool_broker_<stamp>.json/md
npu_micro_peer_assistant_<stamp>.json/md
npu_micro_runtime_tool_broker_<stamp>.json/md
ai_peer_exchange_<stamp>.json/md
ai_peer_exchange_contract_<stamp>.json/md
provider_runtime_heap_live_signals_init_<stamp>.json/md
provider_runtime_heap_live_signals_gpu1_request_<stamp>.json/md
provider_runtime_heap_live_signals_broker_results_<stamp>.json/md
provider_runtime_heap_live_signals_npu_support_<stamp>.json/md
provider_runtime_heap_telemetry_<stamp>.json/md
python_line_count_<timestamp>.csv
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
  -> provider-capable Python selection from IA_CARMINE_PYTHON / .venv
  -> provider runtime heap live init
  -> orchestrator startup barrier:
       GPU1/Ollama primary advisory process
       GPU0/OpenVINO peer support round_000
       NPU/OpenVINO micro support round_000
       NPU live tool-seed broker evidence
       deterministic/broker bootstrap tools
  -> GPU1 checkpoints drive additional GPU0/NPU micro-support where enabled
  -> GPU1/Ollama primary advisory report
  -> GPU0 peer task packet
  -> provider runtime heap GPU1->GPU0 evidence request
  -> GPU0 OpenVINO peer response
  -> GPU0 writes response/tool-request events into provider runtime heap
  -> GPU0 runtime broker tool requests
  -> provider runtime heap broker results
  -> NPU micro peer assistant over GPU1/GPU0/broker/runtime-heap context
  -> provider runtime heap NPU support signal
  -> NPU runtime broker tool requests during live harvest when available
  -> provider runtime heap NPU broker results before final telemetry/bundle
  -> generated artifact path policy for push-safe bundle names
  -> AI peer-exchange report
  -> peer-exchange contract
  -> Full0To10 provider acceptance gate
  -> runtime telemetry, shared AI-to-AI bundle and compact evidence
```

Current source surfaces:

```text
Tools/ai/build_ai_peer_exchange_packet.py
Tools/ai/run_gpu0_peer_companion_worker.py
Tools/ai/run_npu_gpu_deep_review_auditor.py
Tools/ai/provider_runtime_heap.py
Tools/ai/provider_runtime_heap_live_signals.py
Tools/ai/build_provider_runtime_heap_telemetry.py
Tools/validation/check_ai_peer_exchange_contract.py
Tools/validation/check_full0to10_provider_acceptance.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop/main.ps1
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/agent_runtime_tool_broker.py
```

The runtime broker is the only production path for GPU1/GPU0/NPU tool execution. GPU0 peer output may be numeric/tool evidence when `IA_CARMINE_GPU0_COMPANION_MODEL_DIR` is not configured, but that state must remain visible as `gpu0_peer_semantic_model_unconfigured`. NPU output remains non-blocking support evidence and must not replace deterministic validators as heavy audit authority.

The production mesh has two synchronization barriers:

```text
startup barrier: GPU1 process, GPU0 support, NPU micro support and deterministic/broker bootstrap are all armed at the beginning
close barrier: GPU0/NPU/legacy-auditor subprocesses are harvested or terminated within the final wait budget before telemetry/bundle finalization
```

`-Full0To10` does not enable the legacy NPU auditor provider by default. Use `-RunLegacyNpuAuditorProvider` only when comparing the old auditor path against the production micro-support lane.

## Peer mesh operational lanes rule

`usable_lanes` remains a workload-quality/advisory-routing signal and must not be used as the product-level proof that GPU0/GPU1/NPU/broker participated in the run.

The product-facing peer mesh must expose separate lane surfaces:

```text
peer_mesh_operational_lanes
peer_mesh_support_lanes
peer_mesh_degraded_lanes
peer_mesh_product_blockers
```

GPU0 numeric/OpenVINO/tool evidence is a valid operational/support lane even when the semantic companion model is not configured. NPU slow, empty or degraded output is a support-lane degradation, not a product blocker, as long as brokered fallback/tool-support evidence and deterministic validators remain available.

## Provider-broker loop product contract

The production peer architecture is a provider-broker loop, not independent provider reports followed by a late broker pass.

Required loop:

```text
input_md -> deterministic_baseline
deterministic_baseline -> GPU1/Ollama primary advisory
GPU1 -> GPU0/OpenVINO peer task packet
GPU0 -> runtime broker -> GPU1/GPU0 read-only context
GPU1/GPU0/broker context -> NPU/OpenVINO micro support
NPU -> runtime broker -> live heap context -> final context
provider_broker_loop -> peer_exchange_contract -> telemetry -> shared AI-to-AI bundle -> review-only patch bundle
```

Contract rules:

- `runtime_tool_broker` is the only controlled executor.
- Provider lanes may request tools but must not bypass broker allowlists.
- GPU1 remains the primary advisory/planner/worker lane.
- GPU0 is a peer companion and tool-request producer.
- NPU is a slow/degraded-tolerant support/tool-intelligence lane.
- NPU degradation is telemetry, not a product pass blocker.
- Deterministic scripts remain the heavy audit authority.
- Patch application remains manual/review-only.
