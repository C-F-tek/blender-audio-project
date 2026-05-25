# GPU1 one-turn composer/causality propagation map — 2026-05-25

## Purpose

This document maps the product-composer and external-causality points where the GPU1 one-turn production gate must be propagated after it is written into proposal iterations.

Core rule:

```text
A native GPU1 tool call is useful provider activity, but it is not final product causality until the one-turn gate proves:
GPU1 native call -> broker result -> role=tool reinjection -> later GPU1 consumption -> valid FINAL_PRODUCT_DELTA.
```

## 1. Heap final proposal composer

File:

```text
ia_carmine/product/heap_final_proposals/cli.py
```

Observed role:

This CLI builds:

```text
heap_final_proposal_composer.json
heap_final_proposal_composer.md
```

It loads:

```text
- heap_runtime_completeness_gate_report.json
- startup manifest/reconciliation
- proposal iteration JSONs
- provider reports
```

Then builds:

```text
proposal_count
accepted_proposal_count
rejected_proposal_count
provider_report_count
gpu0_review_count
npu_audit_count
blocking_issues
product_causality
operator_decision
proposals summaries
provider_reports summaries
```

Current gap:

`_proposal_summary()` does not include GPU1 one-turn fields.

Patch requirement:

Add to `_proposal_summary()`:

```text
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_native_tool_call_count
gpu1_one_turn_broker_result_passed_count
gpu1_one_turn_role_tool_reinjected
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_final_product_delta_valid
gpu1_one_turn_blocker
gpu1_one_turn_errors
```

Add to `_build_result()` top-level summary:

```text
gpu1_one_turn_gate_passed_count
gpu1_one_turn_gate_failed_count
gpu1_one_turn_gate_blockers
gpu1_one_turn_runtime_gate_paths
```

## 2. Composer artifact discovery

File:

```text
ia_carmine/product/heap_final_proposals/artifacts.py
```

Observed role:

`list_proposals()` reads proposal iteration JSON files under:

```text
team_context/proposal_iterations/heap_proposal_revision_*.json
```

It extracts proposal metadata used by composer and later external causality.

Current gap:

`list_proposals()` does not copy one-turn fields from proposal iteration JSON.

Patch requirement:

Add the same one-turn fields to each proposal dictionary returned by `list_proposals()`.

`flatten_quality_blockers()` should add a clear blocker when a proposal indicates:

```text
gpu1_one_turn_runtime_gate_passed is false
```

Suggested blocker string:

```text
gpu1_one_turn_runtime_gate_failed:<blocker>
```

This makes failures visible in `blocking_issues` and downstream product acceptance.

## 3. Product causality computation

File:

```text
ia_carmine/product/heap_final_proposals/artifacts.py
```

Function:

```text
compute_product_causality(...)
```

Observed behavior:

It checks:

```text
startup input_ready_before_heap
artifact refs
provider execution
proposal count
startup reconciliation
product_status=ready without provider/proposals
```

Current gap:

It does not check whether accepted proposals are backed by a passed GPU1 one-turn gate.

Patch requirement:

When provider execution is active and proposals exist, causal product readiness should require at least one accepted proposal with:

```text
gpu1_one_turn_runtime_gate_passed == true
```

If no proposal has passed one-turn gate:

```text
failed_reasons.append("GPU1 one-turn runtime gate missing or failed")
```

## 4. External final causality normalization

File:

```text
ia_carmine/product/heap_final_proposals/normalize_final_causality/cli.py
```

Observed role:

Distinguishes:

```text
causal_chain_passed
product_acceptance_passed
```

`compute_product_acceptance()` currently checks:

```text
product_status == ready
quality_output_passed == true
accepted proposals / accepted deltas > 0
blocking issues empty
```

Current gap:

It does not check one-turn gate status.

Patch requirement:

Read one-turn fields from composer JSON and/or pointer manifest. Product acceptance should fail when:

```text
gpu1_one_turn_gate_failed_count > 0
or gpu1_one_turn_gate_passed_count <= 0
```

Suggested product acceptance reason:

```text
gpu1_one_turn_runtime_gate_failed_or_missing
```

## 5. External pointer manifest

File already mapped:

```text
ia_carmine/runtime/external_heap/block_pointer_manifest/cli.py
```

Connection to composer/causality:

`normalize_final_causality` can read pointer manifest counts only if the pointer manifest aggregated the one-turn gate fields.

Therefore:

```text
proposal_cycle_a.py -> proposal JSON one-turn fields
artifacts.py/list_proposals -> composer proposal one-turn fields
heap_final_proposals/cli.py -> composer top-level one-turn summary
block_pointer_manifest/cli.py -> external pointer one-turn summary
normalize_final_causality/cli.py -> product acceptance check
```

## 6. Rendering / operator-facing markdown

Files:

```text
ia_carmine/product/heap_final_proposals/rendering.py
ia_carmine/_shared/heap_final_readable_synthesis.py
```

Not inspected in this pass, but likely targets after code patch.

Expected UI/Markdown content:

```text
GPU1 one-turn gate: passed/failed
Native tool call count
Broker result consumed: yes/no
Final product delta valid: yes/no
Blocker/reason when failed
```

## 7. Patch acceptance for composer/causality layer

After core gate is implemented, composer/causality is aligned when:

```text
[ ] proposal iteration JSON includes one-turn fields.
[ ] list_proposals() carries one-turn fields.
[ ] flatten_quality_blockers() exposes failed one-turn gate.
[ ] composer JSON includes one-turn counts/paths/blockers.
[ ] normalize_final_causality rejects product acceptance without passed one-turn gate.
[ ] final readable product and external pointer manifest expose the same one-turn status.
```

## 8. Why this matters

Without this layer, the runtime could correctly block internally, but the external package could still say only:

```text
product_status=blocked_with_reason
quality_output_passed=false
```

instead of the useful operator diagnosis:

```text
gpu1_one_turn_runtime_gate_failed: tool result was not consumed by later GPU1 turn
```

The latter is the actionable failure mode needed to fix run-unica behavior.
