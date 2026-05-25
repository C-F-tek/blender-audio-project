# GPU1 one-turn deep implementation map — 2026-05-25

## Purpose

This document extends the GPU1 one-turn implementation map with the additional production files that must be patched or checked.

Constraint remains unchanged:

```text
Do not import or execute the validator/preflight from full run.
Reproduce the one-turn GPU1 logic inside production full-run runtime.
```

Reference-only validator:

```text
Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py
```

Production implementation surface:

```text
ia_carmine/runtime/heap_gate/gpu1_native_tool_chat_loop.py
```

## Additional implementation points found

### A. Provider report absorption

File:

```text
ia_carmine/runtime/heap_gate/provider_report_absorption.py
```

Why it matters:

The production provider reports are absorbed into the heap graph here. The function:

```text
absorb_completed_provider_item(...)
```

reads the provider JSON, summarizes it through `summarize_provider_report()`, enriches operational peer review, builds the provider block contract, appends the report to `gate.provider_reports`, publishes `provider_evidence`, and appends a `provider_output` heap-exchange event.

Current risk:

```text
If `gpu1_one_turn_runtime_gate` fields are written only in the raw GPU1 report but not preserved in provider_report_absorption/provider summary, later metrics and terminal invariants will not see them.
```

Patch requirement:

```text
- Preserve/copy `gpu1_one_turn_*` fields from raw provider report into provider_report.
- Include one-turn gate path/ref in provider_output heap-exchange event.
- Ensure `gate.provider_reports` contains the one-turn gate status for latest GPU1 report.
```

Candidate fields:

```text
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_native_tool_call_count
gpu1_one_turn_broker_result_count
gpu1_one_turn_broker_result_passed_count
gpu1_one_turn_role_tool_reinjected
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_final_product_delta_valid
gpu1_one_turn_blocker
gpu1_one_turn_errors
```

### B. Provider command summary

File:

```text
ia_carmine/runtime/heap_gate/provider_commands.py
```

Why it matters:

`summarize_provider_report()` is the normalization boundary for raw provider outputs. It already computes/copies:

```text
native_tool_call_count
textual_tool_call_count
native_tool_loop_requested
native_tool_loop_supported
native_tool_loop_performed
assistant_message
chat_history_ref
gpu1_tool_loop_subturn
gpu1_waiting_for_tool_result
gpu1_tool_loop_closed
provider_native_tool_call_required_unmet
provider_native_tool_api_* fields
```

Current risk:

```text
The one-turn gate may be lost or diluted unless summarize_provider_report explicitly passes it through.
```

Patch requirement:

```text
- Treat `gpu1_one_turn_*` as first-class normalized fields.
- Do not infer one-turn pass from `gpu1_tool_loop_closed` alone.
- Preserve textual/non-native tool rejection reasons as one-turn blockers.
- Keep `native_tool_call_count` as raw native call count, but add separate one-turn pass/fail semantics.
```

### C. Runtime provider metrics aggregation

File:

```text
ia_carmine/runtime/heap_gate/run_loop_metrics.py
```

Why it matters:

`build_provider_lane_metrics()` extracts latest GPU1 report and builds the final metrics consumed by terminal invariants. It already exposes:

```text
gpu1_native_tool_call_count
provider_native_tool_call_count
provider_textual_tool_call_count
provider_native_tool_loop_requested_count
provider_native_tool_loop_supported_count
gpu1_primary_workload_valid
gpu1_primary_evidence_valid
leader_source
gpu1_waiting_for_tool_result
gpu1_resume_after_tool_result_required
gpu1_consumed_tool_result_ids
gpu1_tool_result_pending_ids
gpu1_unconsumed_tool_result_ids
gpu1_tool_result_blocker
tool_result_written_count
tool_result_consumed_by_gpu1_count
latest_final_product_delta_valid
```

Current risk:

```text
The data is present in fragments, but there is no explicit aggregate that says: GPU1 one-turn production gate passed.
```

Patch requirement:

Add metrics:

```text
gpu1_one_turn_runtime_gate_present
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_native_tool_call_count
gpu1_one_turn_broker_result_count
gpu1_one_turn_broker_result_passed_count
gpu1_one_turn_role_tool_reinjected
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_final_product_delta_valid
gpu1_one_turn_blocker
gpu1_one_turn_errors
```

Do not compute pass with a weak shortcut. Production pass should require:

```text
native_tool_call_count > 0
broker_result_passed_count > 0
role_tool_reinjected == true
tool_result_consumed_by_gpu1 == true
final_product_delta_valid == true
gpu1_tool_loop_closed == true
```

### D. Terminal invariants

File:

```text
ia_carmine/runtime/heap_gate/terminal_invariants.py
```

Why it matters:

Terminal invariants decide whether complete/full product success is allowed.

Current behavior already blocks several related conditions:

```text
gpu1_primary_workload_missing
gpu1_native_tool_evidence_missing_when_required
gpu1_requested_tool_result_not_consumed
PROVIDER_TOOL_CALLS_REMAIN_TEXT
gpu1_final_product_delta_missing
gpu1_code_delta_without_file_read
ready product_status requires broker bridge reports
ready product_status requires memory/chunk/context artifacts
```

Current risk:

```text
The invariants are distributed. A run can be hard to diagnose because there is no single one-turn gate code/path and no one-turn-specific blocker family.
```

Patch requirement:

Add complete/full blocker:

```text
if allow_provider_generation and not pre_provider and detailed_output_expected:
    require gpu1_one_turn_runtime_gate_passed is True
```

Typed errors:

```text
gpu1_one_turn_runtime_gate_missing
gpu1_one_turn_native_tool_call_missing
gpu1_one_turn_broker_result_missing
gpu1_one_turn_role_tool_reinjection_missing
gpu1_one_turn_tool_result_not_consumed
gpu1_one_turn_final_product_delta_invalid
gpu1_one_turn_textual_tool_call_not_executable
```

Suggested category:

```text
PRODUCT_ACCEPTANCE_BLOCKER
```

For `gpu1_one_turn_tool_result_not_consumed`, category may remain `RECOVERY_BLOCKER` if recovery turn is still allowed.

### E. GPU1 provider prompt and command preparation

File:

```text
ia_carmine/runtime/heap_gate/provider_prompt.py
```

Why it matters:

`gpu1_provider_prompt()` builds the prompt used by GPU1. `startup_context_digest()` already tells GPU1 that tool execution must use native API tool calls and that Markdown/fenced JSON/prose tool-call text is not executable evidence.

Current risk:

```text
If the prompt allows GPU1 to answer directly without a tool in the first production turn, the one-turn gate must still block success, but the model may waste the first run.
```

Patch requirement:

```text
- Ensure the first production GPU1 prompt explicitly requires one native tool call before first reviewable packet in complete/full mode.
- Keep the instruction in runtime prompt, not only validator prompt.
- Prompt should tell GPU1 that GPU0/NPU sidecars wait until the first consumed tool result.
```

This is prompt pressure only. The hard guarantee belongs to the gate/report/invariants, not the prompt.

### F. Production GPU1 loop report builder

Recommended new helper file:

```text
ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py
```

Purpose:

```text
Build the production `gpu1_one_turn_runtime_gate` report from:
- GPU1 subturn reports;
- broker_request/broker_result events;
- chat_history_ref;
- gpu1_tool_result_consumption_state;
- final_product_protocol;
- textual/non-native diagnostics.
```

Why new helper:

```text
Keeps gpu1_native_tool_chat_loop.py from becoming too large and makes terminal/validator tests easier.
```

Suggested API:

```python
def build_gpu1_one_turn_runtime_gate(
    gate,
    *,
    revision: int,
    final_report: dict,
    subturn_reports: list[dict],
    events: list[dict],
    history_path: Path,
    output_path: Path,
) -> dict:
    ...
```

### G. Validator additions after production patch

Do not make full run depend on the validator. Instead, add validators/smokes that inspect production behavior.

Candidate validators:

```text
Tools/validation/heap_runtime/provider_loop_activation_smoke/cli.py
Tools/validation/heap_runtime/run_heap_gate_terminal_invariants_smoke/cli.py
Tools/validation/real_product/runtime_mesh_contract/cli.py
Tools/validation/real_product/live_provider_gate/cli.py
```

Required checks:

```text
- runtime code does not import `Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight`;
- production reports expose `kind=gpu1_one_turn_runtime_gate` or equivalent;
- negative fixture: no native tool call => full run cannot pass complete mode;
- negative fixture: broker result exists but not consumed => full run cannot pass;
- negative fixture: textual/fenced tool call => one-turn gate fails;
- positive fixture: native call + broker result + role=tool + consumed evidence + delta => gate passes.
```

## Updated patch order

```text
1. Add `gpu1_one_turn_gate.py` production helper.
2. Patch `gpu1_native_tool_chat_loop.py` to build/write the report for revision 0 and later revisions as needed.
3. Patch `provider_commands.py` to preserve one-turn fields in provider summary.
4. Patch `provider_report_absorption.py` to carry one-turn fields into `gate.provider_reports`, provider_evidence and heap_exchange provider_output.
5. Patch `provider_execution.py` to require the one-turn gate before GPU0/NPU sidecars can start in complete/full mode.
6. Patch `run_loop_metrics.py` to expose aggregate one-turn metrics.
7. Patch `terminal_invariants.py` to require one-turn gate pass for complete/full product success.
8. Patch proposal/final product validation only where needed to include gate refs and blockers.
9. Add smokes/validators proving no dependency on preflight and positive/negative one-turn behavior.
```

## Quick implementation diagnosis

The project is closer than it looked: most primitives already exist in production runtime.

Existing production primitives:

```text
- GPU1 chat history loop: gpu1_native_tool_chat_loop.py
- API-native tool publication: tool_broker_native_calls.py
- broker execution path: runtime_tool broker / run_bridge
- role=tool reinjection: gpu1_native_tool_chat_loop.py
- consumption validator: gpu1_tool_result_consumption.py
- final product protocol parser: final_product_delta_protocol.py
- terminal blocker framework: terminal_invariants.py
```

Missing production contract:

```text
A single explicit `gpu1_one_turn_runtime_gate` artifact and hard complete/full dependency on it.
```
