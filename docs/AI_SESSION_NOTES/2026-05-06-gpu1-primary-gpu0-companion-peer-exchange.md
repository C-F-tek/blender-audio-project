# 2026-05-06 GPU peer-exchange session note

## Decision

Local AI lanes are not isolated providers. They must cooperate through a peer-exchange contract.

Canonical roles:

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner
GPU0 / OpenVINO = companion peer worker
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1 and GPU0 requests
```

## Required flow

```text
GPU1 primary advisory
  -> emits bounded task packets for GPU0
GPU0 companion worker
  -> reads tasks
  -> runs OpenVINO GenAI on GPU.0 when configured
  -> falls back to numeric/tool/report-only evidence when not configured
  -> emits response/evidence/tool requests
runtime tool broker
  -> may consume tool requests from GPU1 and GPU0
NPU
  -> receives GPU1 context for checkpoint or micro-task support
orchestrator
  -> records roundtrips, timing, classifications, telemetry and bundle evidence
```

## Run observation

Run `gpu0_companion_full0to10_quick_20260506-191903` showed GPU0 as support/companion evidence, but not yet as live peer exchange.

Observed classification:

```text
gpu0_companion_static_report_only
gpu1_gpu0_roundtrip_missing
gpu0_tool_requests_not_broker_consumed
npu_gpu1_checkpoint_context_missing
```

## Next implementation target

Add an AI peer-exchange lane so GPU1/Ollama can always run primary advisory and delegate bounded tasks to GPU0, while deterministic validators remain responsible for heavy audit.
