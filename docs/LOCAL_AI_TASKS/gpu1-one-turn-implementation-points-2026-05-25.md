# GPU1 one-turn implementation points — 2026-05-25

## Finding

The full-run runtime already has the correct structural area for the GPU1 one-turn logic. The implementation should not import the validator/preflight path.

The validator remains the reference contract:

```text
Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py
```

But the production code path already contains:

```text
ia_carmine/runtime/heap_gate/gpu1_native_tool_chat_loop.py
```

Therefore the next patch should strengthen and report the production one-turn gate in the full run, not copy/import the validator.

## Primary implementation points

### 1. Production GPU1 chat/tool loop

File:

```text
ia_carmine/runtime/heap_gate/gpu1_native_tool_chat_loop.py
```

Role:

```text
Parent-orchestrated GPU1 native tool chat loop.
```

Observed behavior:

```text
- writes GPU1 chat history;
- runs GPU1 subturn 0;
- appends assistant message;
- publishes provider native tool calls;
- runs broker bridge;
- appends role=tool results into the same GPU1 history;
- runs later subturns;
- persists loop state with gpu1_tool_loop_closed and chat_history_ref.
```

This is the correct production implementation surface for the requested one-turn logic.

Required changes:

```text
- emit a stamp/revision scoped `gpu1_one_turn_runtime_gate` report;
- require at least one native tool call in the first GPU1 production turn when complete/full mode is active;
- distinguish closed-without-tool from valid one-turn closure;
- record role_tool_reinjected=true only after actual role=tool append;
- record tool_result_consumed_by_gpu1 from consumption state, not from broker execution alone;
- expose `gpu1_one_turn_runtime_gate_path` back to provider_execution/run summary.
```

### 2. Provider execution / sidecar start boundary

File:

```text
ia_carmine/runtime/heap_gate/provider_execution.py
```

Role:

```text
Owns provider teamwork: GPU1 primary first, then GPU0/NPU sidecars.
```

Observed behavior:

```text
- prepares selected provider lanes;
- runs replight gate;
- starts GPU1 through `run_gpu1_native_tool_chat_loop()`;
- captures GPU1 primary evidence before sidecars;
- skips sidecars if GPU1 primary evidence is invalid/pending;
- starts GPU0/NPU only after GPU1 packet is reviewable.
```

This is the correct place to enforce:

```text
gpu1_one_turn_runtime_gate.passed == true
```

before:

```text
gpu1_packet_reviewable(...)
start_provider_item(...) for GPU0/NPU sidecars
```

Required changes:

```text
- read/receive the one-turn gate result from `run_gpu1_native_tool_chat_loop()`;
- if gate fails, mark sidecars skipped with typed reason;
- block complete/full success with `gpu1_one_turn_*` blocker;
- keep diagnostic/partial behavior explicit if sidecars run without gate.
```

### 3. GPU1 primary evidence classifier

File:

```text
ia_carmine/runtime/heap_gate/provider_execution_checks.py
```

Role:

```text
Classifies GPU1 workload and primary evidence validity.
```

Observed behavior:

```text
- `gpu1_primary_workload_status()` checks non-replight useful GPU1 work;
- `gpu1_primary_evidence_status()` calls `gpu1_tool_result_consumption_state()`;
- evidence is valid if a passed tool result was consumed or a valid FINAL_PRODUCT_DELTA exists;
- if tool result consumption is still required, source is cleared and evidence blocks.
```

Required changes:

```text
- make complete/full mode require the one-turn path, not fallback to `gpu1_final_product_delta` alone;
- expose `gpu1_one_turn_native_tool_call_count`, `role_tool_reinjected`, `gpu1_one_turn_gate_passed`;
- add typed blockers for missing native tool, missing broker result, missing consumption, invalid/empty delta;
- keep `gpu1_final_product_delta` as valid only after the one-turn gate or in explicitly text-only diagnostic mode.
```

### 4. Provider-native tool call publisher

File:

```text
ia_carmine/runtime/heap_gate/tool_broker_native_calls.py
```

Role:

```text
Turns provider API-native tool_calls into broker requests.
```

Observed behavior:

```text
- only API-native calls pass `is_api_native_tool_call()`;
- textual/fenced JSON/prose tool calls publish `provider_textual_tool_call_not_executable` diagnostic;
- primary GPU1 native calls set GPU1 waiting/resume fields;
- broker_request events include `provider_native_tool_call=true`, lane, revision, subturn and chat_history_ref.
```

Required changes:

```text
- no major rewrite needed;
- ensure one-turn report counts only calls that became broker_request events;
- surface textual/non-native tool-call diagnostics into the one-turn gate errors;
- keep sidecar tool calls non-closing and GPU1-followup-required.
```

### 5. GPU1 tool-result consumption logic

File:

```text
ia_carmine/runtime/heap_gate/gpu1_tool_result_consumption.py
```

Role:

```text
Determines whether GPU1 consumed broker results in CONSUMED_EVIDENCE.
```

Observed behavior:

```text
- finds GPU1 native broker requests;
- finds matching GPU1 native broker results;
- checks CONSUMED_EVIDENCE / refs in later GPU1 response;
- prevents same-subturn result consumption;
- reports pending, unconsumed, consumed-passed and consumed-failed ids.
```

Required changes:

```text
- likely no core parser rewrite needed;
- use this directly from the production one-turn gate report;
- persist its result into `gpu1_one_turn_runtime_gate`;
- promote `gpu1_requested_tool_result_not_consumed` to complete/full blocker.
```

### 6. Proposal/final delta validation

File:

```text
ia_carmine/runtime/heap_gate/proposal_cycle_a.py
```

Role:

```text
Persists heap proposal iteration and validates FINAL_PRODUCT_DELTA.
```

Observed behavior:

```text
- builds final_product_protocol;
- checks code_file_read_contract;
- calls gpu1_tool_result_consumption_state;
- rejects proposal when GPU1 resume after tool result is still required;
- writes proposal iteration artifact with final_product_delta_valid and consumption fields.
```

Required changes:

```text
- consume the production `gpu1_one_turn_runtime_gate` result as a hard complete/full precondition;
- make `quality_passed` require one-turn gate when provider generation is enabled;
- record one-turn gate refs in proposal iteration artifact;
- reject final product when one-turn gate failed even if delta protocol alone appears valid.
```

### 7. Main run loop / final metrics / terminal invariants

File:

```text
ia_carmine/runtime/heap_gate/run_loop.py
```

Role:

```text
Coordinates lifecycle and builds final heap_runtime_completeness_gate metrics.
```

Observed behavior:

```text
- after provider teamwork, publishes native tool calls and bridge results;
- drains provider-consumable evidence;
- persists proposal iteration artifacts;
- builds final metrics for terminal invariant evaluation;
- emits final report `kind=heap_runtime_completeness_gate`.
```

Required changes:

```text
- add metrics from production one-turn gate:
  - gpu1_one_turn_runtime_gate_passed
  - gpu1_one_turn_native_tool_call_count
  - gpu1_one_turn_broker_result_passed_count
  - gpu1_one_turn_role_tool_reinjected
  - gpu1_one_turn_tool_result_consumed
  - gpu1_one_turn_final_product_delta_valid
  - gpu1_one_turn_runtime_gate_path
- terminal invariants must reject complete/full product success if one-turn gate is false/missing.
```

## Patch order recommended

```text
1. Add production one-turn gate report builder inside runtime/heap_gate, preferably near gpu1_native_tool_chat_loop.py.
2. Make gpu1_native_tool_chat_loop.py populate that report for revision 0.
3. Make provider_execution.py require that report before GPU0/NPU sidecars start.
4. Make provider_execution_checks.py classify GPU1 primary evidence using that gate in complete/full mode.
5. Make proposal_cycle_a.py and run_loop.py expose/require the gate in final metrics.
6. Add validator checks that full run does not import the preflight validator and that one-turn fields exist.
```

## Minimal blocker names

```text
gpu1_one_turn_native_tool_call_missing
gpu1_one_turn_textual_tool_call_not_executable
gpu1_one_turn_broker_result_missing
gpu1_one_turn_role_tool_reinjection_missing
gpu1_one_turn_tool_result_not_consumed
gpu1_one_turn_final_product_protocol_invalid
gpu1_one_turn_operator_delta_invalid
gpu1_one_turn_final_product_delta_empty
gpu0_npu_started_before_gpu1_one_turn_closed
```

## Do not do

```text
- Do not import `Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.*` from runtime code.
- Do not shell out to `python -m Tools.validation run_gpu1_native_tool_loop_preflight` from full run.
- Do not accept broker execution as product evidence until GPU1 consumes it in a later subturn.
- Do not let GPU0/NPU sidecars close or bypass the one-turn gate.
- Do not treat provider free text as one-turn success.
```
