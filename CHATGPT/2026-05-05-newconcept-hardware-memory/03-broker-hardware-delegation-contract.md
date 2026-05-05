# 03 — Broker hardware delegation contract sketch

## Purpose

Define the intended control-plane contract for delegated local hardware work.

No delegated NPU/GPU0 coworker behavior should be enabled until the broker can describe, route, time out, report and guard the call.

## Delegation principle

Primary AI lanes may delegate bounded work only through broker-managed contracts.

No lane may call hardware workers directly as an uncontrolled side channel.

## Candidate lanes

```text
NVIDIA GPU / Ollama
  role: primary advisory / planner / patch-plan reasoning

NPU / OpenVINO GenAI
  role: bounded tool-proxy helper

Intel GPU0 / OpenVINO
  role: candidate coworker for compatible report-only workloads

CPU deterministic
  role: validators, inventories, parsers, report builders

SQLite memory
  role: shared heap memory and checkpoint/observation store
```

## Required broker fields

Each delegated hardware/tool call must report:

```text
call_id
run_stamp
requested_by_lane
target_resource
requested_tool
input_schema_version
output_schema_version
timeout_seconds
side_effect_class
source_writes_allowed
patch_application_allowed
persistent_memory_write_allowed
provider_execution_performed
started_at
finished_at
duration_seconds
passed
errors
warnings
degraded_state
```

## Side-effect classes

```text
read_only
report_only
scratch_memory_write
persistent_memory_write
source_write
patch_apply
media_runtime
network_or_secret_access
```

Default allowed class for NPU/GPU0 helpers:

```text
read_only or report_only
```

Anything above that requires explicit approval and a validator/report contract.

## Capability manifest extension

Future capability manifest entry shape:

```json
{
  "name": "npu_tool_proxy.classify_finding",
  "resource": "NPU",
  "role": "bounded_tool_proxy",
  "provider": "openvino_genai",
  "input_schema": "npu_tool_proxy_request.v1",
  "output_schema": "npu_tool_proxy_response.v1",
  "allowed_side_effects": ["read_only", "report_only"],
  "source_writes_allowed": false,
  "patch_application_allowed": false,
  "persistent_memory_write_allowed": false,
  "timeout_seconds_default": 120
}
```

GPU0 example:

```json
{
  "name": "gpu0_worker.embedding_or_classification_probe",
  "resource": "GPU.0",
  "role": "openvino_coworker_report_only",
  "provider": "openvino",
  "input_schema": "gpu0_worker_request.v1",
  "output_schema": "gpu0_worker_response.v1",
  "allowed_side_effects": ["read_only", "report_only"],
  "source_writes_allowed": false,
  "patch_application_allowed": false,
  "persistent_memory_write_allowed": false,
  "timeout_seconds_default": 120
}
```

## NPU tool-proxy request schema sketch

```json
{
  "schema_version": "npu_tool_proxy_request.v1",
  "task_type": "classify_finding",
  "run_stamp": "20260505-HHMMSS",
  "requested_by": "gpu_primary_lane",
  "input_text": "compact finding text",
  "candidate_labels": [
    "PROMOTE_TO_PROJECT_TOOL",
    "UNUSED_BUT_USEFUL",
    "DO_NOT_PROMOTE"
  ],
  "constraints": {
    "max_response_tokens": 256,
    "source_writes_allowed": false,
    "patch_application_allowed": false
  },
  "metadata": {}
}
```

## NPU tool-proxy response schema sketch

```json
{
  "schema_version": "npu_tool_proxy_response.v1",
  "kind": "npu_tool_proxy_response",
  "passed": true,
  "task_type": "classify_finding",
  "selected_label": "UNUSED_BUT_USEFUL",
  "confidence": 0.72,
  "rationale": "Short bounded explanation.",
  "requires_human_review": true,
  "provider_execution_performed": true,
  "source_writes_performed": false,
  "patch_application_performed": false,
  "persistent_memory_write_performed": false,
  "errors": [],
  "warnings": []
}
```

## GPU0 worker schema sketch

GPU0 starts report-only.

Allowed first tasks:

```text
detect_available_device
small_embedding_probe
small_classification_probe
batch_similarity_probe
```

No source writes, patch application or persistent memory writes in v1.

## Validator requirements

Before enabling real delegated calls, add validators for:

```text
NPU tool-proxy request
NPU tool-proxy response
GPU0 worker request
GPU0 worker response
broker delegated-call telemetry
hardware capability manifest
SQLite heap memory event reports
```

Validators must accept unknown future fields but reject unsafe side effects unless explicitly allowed.

## Telemetry requirements

Runtime telemetry must count:

```text
delegated_call_count
npu_helper_call_count
gpu0_worker_call_count
cpu_deterministic_call_count
memory_tool_call_count
failed_delegated_call_count
blocked_delegated_call_count
degraded_delegated_call_count
```

Full toolbox telemetry summary must expose:

```text
hardware_lanes_seen
hardware_lanes_degraded
hardware_delegation_performed
source_writes_performed
patch_application_performed
persistent_memory_write_performed
```

## First safe implementation

First implementation should be:

```text
report-only hardware capability manifest for CPU/GPU.0/NPU
no delegated worker execution
no source writes
no persistent memory writes
no patch application
validator for manifest shape
bundle summary includes hardware capability section
```
