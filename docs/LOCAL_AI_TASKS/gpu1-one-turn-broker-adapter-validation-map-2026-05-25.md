# GPU1 one-turn broker/adapter/validation map — 2026-05-25

## Purpose

This document adds the remaining implementation points for reproducing the GPU1 one-turn logic inside full run without importing the validator/preflight.

The previous maps identified the production GPU1 loop and terminal/report surfaces. This map covers:

```text
- broker bridge execution path;
- Ollama adapter/report boundary;
- existing validation smoke mismatch to fix;
- exact reason why native tool call alone is not enough.
```

## 1. Broker bridge execution path

File:

```text
ia_carmine/runtime/heap_gate/loop_steps.py
```

Function:

```text
RuntimeGateLoopStepsMixin.run_bridge()
```

Observed role:

```text
- launches `python -m ia_carmine provider_runtime_broker_bridge`;
- passes heap events/snapshot/markdown;
- records bridge JSON/MD refs;
- increments aggregate `tool_execution_count`;
- appends a generic heap-exchange broker_result event.
```

Patch implication:

```text
The one-turn gate must not trust aggregate `tool_execution_count` alone.
It must match the specific GPU1 request_id emitted in the one-turn subturn to a broker_result event.
```

Required one-turn report fields sourced here or downstream:

```text
broker_bridge_report_refs
broker_result_count_for_gpu1_request
broker_result_passed_count_for_gpu1_request
```

## 2. Provider runtime broker bridge

File:

```text
ia_carmine/runtime/provider_runtime_blackboard/broker_bridge/cli.py
```

Key functions:

```text
event_to_tool_request(...)
append_broker_results(...)
```

Observed role:

`event_to_tool_request()` hydrates heap `broker_request` events into broker tool requests and preserves:

```text
id/tool/args/requirement
lane
revision
provider_native_tool_call
provider_report
provider_block_id
proposal_block_id
native_tool_call_authority
tool_result_scope
gpu1_followup_required
cannot_close_product
peer_only
```

`append_broker_results()` writes broker results back to the heap and preserves:

```text
request_id
normalized_request_id
target_lane
tool
requirement
lane
revision
gpu1_tool_loop_subturn
tool_call_id
tool_call_index
chat_history_ref
provider_native_tool_call
provider_report
provider_block_id
proposal_block_id
native_tool_call_authority
tool_result_scope
gpu1_followup_required
cannot_close_product
peer_only
returncode
outputs
summary
errors/warnings
broker_report
```

Patch implication:

```text
The bridge already carries enough metadata for deterministic one-turn matching.
The new one-turn gate should use this bridge metadata instead of global counters.
```

Required check:

```text
Only broker_result where:
- provider_native_tool_call is true;
- lane == gpu1_planner;
- revision == target revision;
- gpu1_tool_loop_subturn < final GPU1 consumer subturn;
- request_id/normalized_request_id matches the GPU1 tool call request;
- returncode == 0 or broker_result_passed(...)
counts for the gate.
```

## 3. Ollama adapter boundary

File:

```text
ia_carmine/_shared/provider_ollama_probe.py
```

Observed role:

`run_ollama_probe()` is the real GPU1/GPU0 Ollama adapter. For chat/native tool mode it:

```text
- receives messages;
- calls `session.chat(..., tools=chat_tools)`;
- normalizes Ollama tool calls;
- stores `assistant_message`;
- sets `gpu1_tool_loop_subturn`;
- sets native tool API status fields;
- classifies textual/fenced/prose tool calls as non-executable;
- when native tool calls exist, marks provider work verified because GPU1 emitted useful pending broker work.
```

Critical detail:

```text
native_tool_calls => provider_work_verified=True
```

This is correct for provider activity, but not sufficient for complete one-turn success.

Patch implication:

```text
Do not change provider_work_verified to mean full one-turn closure.
Add a separate `gpu1_one_turn_runtime_gate` contract.
```

Reason:

```text
A GPU1 native tool call is useful provider work, but the one-turn is incomplete until:
- broker executes;
- role=tool result is injected;
- GPU1 consumes it in a later subturn;
- final delta is valid.
```

## 4. Ollama report boundary

File:

```text
ia_carmine/_shared/provider_ollama_report.py
```

Observed role:

`build_ollama_probe_report()` writes report fields including:

```text
tool_calls
assistant_message
chat_history_ref
chat_history_message_count
gpu1_tool_loop_subturn
gpu1_native_tool_chat_loop
gpu1_waiting_for_tool_result = bool(native_tool_calls)
gpu1_tool_loop_closed = not bool(native_tool_calls)
provider_textual_tool_call_not_executable
native_tool_loop_requested
native_tool_loop_supported
native_tool_loop_performed
native_tool_call_count
```

Patch implication:

```text
`gpu1_tool_loop_closed` only means this subturn did not request another tool.
It does not prove that a previous broker result was consumed.
```

Therefore the production gate must compute:

```text
gpu1_one_turn_tool_result_consumed
```

from `gpu1_tool_result_consumption_state()`, not from `gpu1_tool_loop_closed`.

## 5. Existing validator/smoke mismatch to resolve

File:

```text
Tools/validation/heap_runtime/provider_loop_activation_smoke/cli.py
```

Observed issue:

The smoke `_probe_native_tool_routing()` expects GPU1 generic_write native request scope to be:

```text
tool_result_scope == primary_product_evidence
gpu1_followup_required == false
```

But current production `tool_broker_native_calls._lane_tool_authority()` for primary GPU1 emits the newer semantics:

```text
tool_result_scope = primary_pending_gpu1_resume_evidence
gpu1_followup_required = true
cannot_close_product = true
```

Operational interpretation:

The current one-turn design requires GPU1 follow-up after broker result. Therefore the smoke expectation appears stale for the new one-turn contract.

Patch requirement:

```text
Update `_probe_native_tool_routing()` so GPU1 native request is expected to be pending-resume evidence, not immediate product evidence.
```

Expected smoke semantics:

```text
tool_result_scope == primary_pending_gpu1_resume_evidence
gpu1_followup_required == true
cannot_close_product == true
```

This aligns the validator with the requested full-run logic.

## 6. One-turn matching algorithm

Recommended helper:

```text
ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py
```

Inputs:

```text
gate
revision
subturn_reports
final_report
events
history_path
output_path
```

Algorithm:

```text
1. Select GPU1 subturn reports for revision.
2. Identify first subturn with native API tool calls.
3. Build expected request ids using provider_native_tool_request_id or read broker_request events.
4. Find matching broker_request events: lane=gpu1_planner, provider_native_tool_call=true.
5. Find matching broker_result events written by broker bridge.
6. Check broker_result_passed for at least one result.
7. Verify chat history contains assistant tool call and role=tool result after it.
8. Run gpu1_tool_result_consumption_state(...) on final GPU1 report text.
9. Parse final_product_protocol(...).
10. Pass only if native call, broker result, role=tool reinjection, later GPU1 consumption and final delta are all valid.
```

Required output:

```json
{
  "schema_version": 1,
  "kind": "gpu1_one_turn_runtime_gate",
  "revision": 0,
  "passed": true,
  "provider_execution_performed": true,
  "gpu1_turn0_native_tool_call_count": 1,
  "broker_request_count": 1,
  "broker_result_count": 1,
  "broker_result_passed_count": 1,
  "role_tool_reinjected": true,
  "gpu1_turn1_provider_performed": true,
  "tool_result_consumed_by_gpu1": true,
  "final_product_protocol_valid": true,
  "final_product_delta_valid": true,
  "errors": [],
  "warnings": []
}
```

## 7. Practical patch implications

Patch set should include:

```text
- new runtime helper: gpu1_one_turn_gate.py;
- gpu1_native_tool_chat_loop.py: call helper and write gate report;
- provider_commands.py: preserve `gpu1_one_turn_*` summary fields;
- provider_report_absorption.py: copy fields into provider_report/event graph;
- run_loop_metrics.py: aggregate one-turn gate fields into terminal metrics;
- terminal_invariants.py: require gate in complete/full provider product runs;
- provider_loop_activation_smoke: update stale GPU1 native request expectation;
- add static check that runtime does not import validator/preflight modules.
```

## 8. New diagnosis vs previous understanding

Previous understanding:

```text
Maybe full run lacks the GPU1 native tool loop.
```

Updated code-driven understanding:

```text
Full run already has a production GPU1 native tool chat loop.
The missing part is a hard production gate artifact and success dependency.
```

The gate must prevent this false-positive chain:

```text
GPU1 emitted a native tool call
-> provider_work_verified=true
-> sidecars/product path continues
```

unless the full chain is complete:

```text
GPU1 emitted native tool call
-> broker result exists and passed
-> role=tool result reinjected
-> later GPU1 subturn consumed it
-> valid FINAL_PRODUCT_DELTA emitted
```
