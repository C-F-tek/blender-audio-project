# GPU1 one-turn operator-decision/smoke map — 2026-05-25

## Purpose

This document maps the quick operator decision file and final-readable smoke tests that must be updated after the GPU1 one-turn runtime gate is implemented.

The gate must not only be enforced; it must also be immediately visible in the operator package.

## 1. OPERATOR_DECISION.txt writer

File:

```text
ia_carmine/product/code_product/final_readable_product/operator_decision.py
```

Function:

```text
write_operator_decision(...)
```

Observed behavior:

The file writes compact key/value lines:

```text
final_document_status
product_kind
product_status
gpu1_blocked_reason
resume_from_block_id
soft_lock_state
closure_quorum_status
closure_quorum_reason
gpu1_closure_decision
gpu0_closure_agreement
npu_closure_advisory
cpu_closure_validation
provider_blocked_reason
provider_replight_health_residency_only
open_pointer_count_final
decision
```

Current gap:

```text
No one-turn gate status is written to OPERATOR_DECISION.txt.
```

Patch requirement:

Extend function args or pass through a compact `gpu1_one_turn` dict.

Recommended output lines:

```text
gpu1_one_turn_runtime_gate=<passed|failed|missing>
gpu1_one_turn_runtime_gate_path=<path>
gpu1_one_turn_tool_result_consumed=<true|false>
gpu1_one_turn_final_product_delta_valid=<true|false>
gpu1_one_turn_blocker=<reason>
```

Why this matters:

`OPERATOR_DECISION.txt` is the shortest operator-facing artifact. If a run fails because GPU1 emitted a tool call but did not consume its result, the operator should see that immediately without opening the full JSON.

## 2. Final readable product smoke

File:

```text
Tools/validation/heap_runtime/run_heap_final_readable_product_smoke/cli.py
```

Observed behavior:

This smoke builds a full fixture run with:

```text
- proposal iterations;
- provider teamwork reports;
- code execution matrix;
- external pointer manifest;
- final readable product;
- Documents outputs;
- ZIP output.
```

It already checks that the final Markdown contains many important phrases, including:

```text
Decisione finale
Final document status
Piano applicabile
Laboratorio operativo
Universo pointer e memoria
Decisione operatore
Peer follow-up pending
Gerarchia GPU1/GPU0/NPU
GPU1 primary workload
GPU1 primary evidence
Generic write
GPU1/NVIDIA
GPU0/Vulkan
NPU/OpenVINO
Parallel provider overlap
Device identity map
```

Current gap:

```text
The required phrase list does not include the GPU1 one-turn gate section.
```

Patch requirement:

Update fixture proposal/gate metrics to include a passed one-turn gate:

```text
gpu1_one_turn_runtime_gate_present=true
gpu1_one_turn_runtime_gate_path=<fixture path>
gpu1_one_turn_runtime_gate_passed=true
gpu1_one_turn_native_tool_call_count=1
gpu1_one_turn_broker_result_passed_count=1
gpu1_one_turn_role_tool_reinjected=true
gpu1_one_turn_tool_result_consumed=true
gpu1_one_turn_final_product_delta_valid=true
```

Then add required Markdown phrases:

```text
GPU1 one-turn runtime gate
one-turn gate passed
Broker result consumed
role=tool reinjected
```

And add OPERATOR_DECISION.txt assertions:

```text
gpu1_one_turn_runtime_gate=passed
gpu1_one_turn_tool_result_consumed=true
```

## 3. Negative smoke needed

The current final-readable smoke is mostly a positive fixture. Add a negative fixture or extend existing assertions so that:

```text
- gate missing => final readable product is blocked;
- gate failed => OPERATOR_DECISION.txt contains gpu1_one_turn_runtime_gate=failed;
- Markdown includes the blocker reason;
- bundle/product JSON `passed` is false in complete/full provider mode.
```

Suggested blocker:

```text
gpu1_one_turn_runtime_gate_failed:gpu1_requested_tool_result_not_consumed
```

## 4. Where to inject one-turn fixture data

The smoke manually writes:

```text
heap_proposal_revision_001.json
heap_proposal_revision_002.json
provider_teamwork/*.json
heap_runtime_completeness_gate_report.json
heap_final_proposal_composer.json
```

Add one-turn fields to:

```text
heap_proposal_revision_002.json
heap_runtime_completeness_gate_report.json.metrics
```

Optionally create a fixture artifact:

```text
provider_teamwork/gpu1_one_turn_runtime_gate.json
```

with:

```json
{
  "schema_version": 1,
  "kind": "gpu1_one_turn_runtime_gate",
  "passed": true,
  "tool_result_consumed_by_gpu1": true,
  "final_product_delta_valid": true
}
```

## 5. Patch acceptance for this layer

```text
[ ] OPERATOR_DECISION.txt includes one-turn status lines.
[ ] Final-readable smoke fixture includes one-turn metrics/artifact.
[ ] Final-readable Markdown required phrase list includes one-turn section.
[ ] Smoke verifies positive one-turn status in JSON/Markdown/TXT.
[ ] Negative fixture or dedicated smoke verifies failed/missing one-turn gate blocks final product.
```

## 6. Relationship to core gate

This layer must not compute the one-turn gate. It only renders and validates the evidence already produced by:

```text
ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py
```

If the renderer has to infer the gate from generic metrics, the core patch is incomplete.
