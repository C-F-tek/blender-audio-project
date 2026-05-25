# GPU1 one-turn logic inside full run — 2026-05-25

## Decision

The new GPU1 validator must be used as the reference model, but the full run must not import, launch, or depend on the validator/preflight implementation.

The full run must reproduce the same runtime logic internally for one GPU1 turn.

Correct target:

```text
full run owns the GPU1 one-turn logic
validator proves the logic
preflight remains a validator/smoke reference only
```

Wrong target:

```text
full run imports Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight
full run shells out to run_gpu1_native_tool_loop_preflight
full run treats preflight output as the production GPU1 turn
```

## Reference validator

Reference only:

```text
Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py
```

Dispatcher surface:

```text
python -m Tools.validation run_gpu1_native_tool_loop_preflight ...
```

This validator demonstrates the required single GPU1 turn mechanics:

```text
GPU1 provider subturn 0
-> native tool call
-> runtime broker request
-> runtime broker executes tool
-> role=tool result is injected into the same GPU1 chat history
-> GPU1 provider subturn 1 consumes the tool result
-> GPU1 emits FINAL_PRODUCT_DELTA grounded in CONSUMED_EVIDENCE
```

## Logic that must exist in full run

For the first real GPU1 production turn, full run must implement the same five invariants:

```text
1. GPU1 must make a real native tool call.
2. The runtime broker must execute the requested tool.
3. The broker result must be reinserted as a role=tool/tool_name message in the same GPU1 conversation.
4. GPU1 must run a later subturn that consumes that tool result.
5. GPU1 must emit a valid FINAL_PRODUCT_DELTA with CONSUMED_EVIDENCE referencing the consumed broker request_id/result.
```

This is not optional for complete/full product runs. A GPU1 text response without this chain is provider prose, not a validated GPU1 runtime turn.

## One-turn production model

The full run does not need the full multi-subturn smoke loop. It needs one production turn pair:

```text
GPU1_TURN_0: ask/plan/use tool
BROKER: execute tool request
GPU1_TURN_1: consume role=tool result and emit delta
```

Allowed outcome of `GPU1_TURN_1`:

```text
FINAL_PRODUCT_KIND: text | code | text_and_code
FINAL_PRODUCT_ACTION: append | refine | replace
CURRENT_POINTER:
- previous_block_id=<consumed_request_id_or_previous_gpu1_block>
- refines_block_id=<optional>
- resume_from_block_id=<current_gpu1_block>
CONSUMED_EVIDENCE:
- <broker request_id/result id actually consumed>
NEXT_RUNTIME_INTENT:
- <next step>
FINAL_PRODUCT_DELTA:
<operator-facing grounded content>
```

Rejected outcomes:

```text
- textual JSON/fenced JSON pretending to be a tool call;
- assistant says it used a tool but no broker result exists;
- broker result exists but GPU1 never consumes it in the later subturn;
- GPU1 emits empty FINAL_PRODUCT_DELTA;
- GPU1 emits code/text+code diff without required file-window content evidence;
- GPU0/NPU sidecars start before the first GPU1 tool-result consumption is closed;
- final product is assembled from runtime fallback text instead of GPU1 delta.
```

## Where to implement

Do not implement in `Tools/validation/...`.

Implementation belongs in maintained runtime/provider code, preferably the provider/heap-gate path that already owns GPU1 provider invocation and brokered native tools.

Candidate areas to inspect and patch:

```text
ia_carmine/runtime/heap_context_closure
ia_carmine/runtime/heap_gate
ia_carmine/runtime/runtime_tool
ia_carmine/runtime/provider_runtime_blackboard
ia_carmine/product/operator_product_core/direct_command.py
ia_carmine/product/operator_product_core/runner.py
```

The operator entry remains:

```text
python -m ia_carmine.cli run ...
```

The full run may reuse runtime helpers already used by the validator, if they are production/runtime helpers, for example:

```text
ia_carmine._shared.provider_ollama_probe.run_ollama_probe
ia_carmine.runtime.runtime_tool.broker.executor.build_report
ia_carmine.runtime.heap_gate.final_product_delta_protocol.final_product_protocol
ia_carmine.runtime.heap_gate.gpu1_tool_result_messages.gpu1_tool_result_payload
a_carmine.runtime.heap_gate.gpu1_tool_result_messages.gpu1_tool_result_text
ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption.gpu1_tool_result_consumption_state
```

But the full run must not import validator modules such as:

```text
Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.cli
Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.context
Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.review
```

## Required production artifacts

The full run should write its own production report, not a preflight report:

```text
kind = gpu1_one_turn_runtime_gate
```

Minimum fields:

```json
{
  "schema_version": 1,
  "kind": "gpu1_one_turn_runtime_gate",
  "provider_execution_performed": true,
  "gpu1_turn0_provider_performed": true,
  "gpu1_turn0_native_tool_call_count": 1,
  "broker_request_count": 1,
  "broker_result_count": 1,
  "broker_result_passed_count": 1,
  "role_tool_reinjected": true,
  "gpu1_turn1_provider_performed": true,
  "tool_result_consumed_by_gpu1": true,
  "final_product_protocol_valid": true,
  "operator_delta_valid": true,
  "final_product_delta_valid": true,
  "gpu0_npu_started_before_gpu1_one_turn_closed": false,
  "passed": true,
  "errors": [],
  "warnings": []
}
```

The final launcher/run summary must reference this report:

```text
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_delta_valid
```

## Full-run blocking rules

Complete/full run must block product success when any required one-turn invariant fails.

Typed blockers:

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

## Sidecar ordering rule

GPU0/NPU sidecars may start only after this gate is true:

```text
gpu1_one_turn_runtime_gate.passed == true
```

Equivalent expanded condition:

```text
gpu1_turn0_native_tool_call_count > 0
broker_result_passed_count > 0
role_tool_reinjected == true
gpu1_turn1_provider_performed == true
tool_result_consumed_by_gpu1 == true
final_product_delta_valid == true
```

Diagnostic/partial modes may collect degraded evidence, but complete/full mode must not pass product success when this gate fails.

## Validator relationship after implementation

After implementation, the validator should validate that production code contains and reports equivalent semantics.

The validator may remain a live smoke fixture, but its job is to prove the contract, not to be used by the full run as an implementation dependency.

Desired validation additions:

```text
- static check: full-run production code does not import gpu1_native_tool_loop_preflight modules;
- contract check: full-run report exposes gpu1_one_turn_runtime_gate fields;
- negative fixture: tool prose without native tool call fails;
- negative fixture: broker result not consumed fails;
- positive fixture: native tool call + broker result + role=tool + consumed delta passes.
```

## Acceptance criteria

```text
[ ] Full run implements one GPU1 tool-call/consume/delta turn internally.
[ ] Full run does not import or shell out to `run_gpu1_native_tool_loop_preflight`.
[ ] Full run writes `gpu1_one_turn_runtime_gate` or equivalent production report.
[ ] Full run blocks complete product success if GPU1 one-turn gate fails.
[ ] GPU0/NPU sidecars cannot satisfy or bypass the GPU1 one-turn gate.
[ ] GPU0/NPU sidecars start only after the first GPU1 one-turn gate is closed.
[ ] Validator remains a smoke/contract reference and can validate equivalent behavior.
[ ] Final public product package references the production GPU1 one-turn gate evidence.
```

## Suggested patch title

```text
fix(ai): reproduce GPU1 one-turn tool loop inside full run
```

## Suggested first implementation task for Codex

```text
Study `Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py` only as a reference. Do not import it.
Implement the same one-turn GPU1 production gate inside the maintained full-run heap/provider path.
The production path must perform: GPU1 native tool call -> broker execution -> role=tool reinjection -> GPU1 consumption subturn -> valid FINAL_PRODUCT_DELTA.
Write stamp-scoped `gpu1_one_turn_runtime_gate` evidence and make complete/full product success depend on it.
Add validation that full run does not import the preflight validator and that missing native tool call / missing consumption block product success.
```
