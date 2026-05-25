# GPU1 one-turn rendering/package map — 2026-05-25

## Purpose

This document maps the final renderer and product-package implementation points for the GPU1 one-turn runtime gate.

The goal is to make the gate visible to the operator, not only enforced internally.

## 1. Final readable Markdown synthesis

File:

```text
ia_carmine/_shared/heap_final_readable_synthesis.py
```

Function:

```text
render_markdown(...)
```

Observed behavior:

The final readable product Markdown already contains operator-facing sections for:

```text
- final decision;
- provider proposal status;
- product status;
- resume_from_block_id;
- soft lock / closure quorum;
- GPU1/GPU0/NPU hierarchy;
- provider replight table;
- generic_write evidence;
- peer follow-up pending;
- pointer graph chain;
- validation summary;
- code product sections.
```

It reads many metrics from `gate.metrics`, including:

```text
gpu1_primary_workload_valid
gpu1_primary_evidence_valid
gpu1_native_tool_call_count
sidecars_start_policy
parallel_provider_overlap_seconds
gpu1_leader_valid
gpu1_consumed_gpu0_peer
gpu1_consumed_npu_peer
```

Current gap:

```text
There is no explicit operator-facing section for `GPU1 one-turn gate`.
```

Patch requirement:

Add a section near `Gerarchia GPU1/GPU0/NPU` or before `Peer follow-up pending`:

```text
## GPU1 one-turn runtime gate

- Gate passed: `<bool>`
- Gate report: `<path>`
- Native tool calls: `<count>`
- Broker results passed: `<count>`
- role=tool reinjected: `<bool>`
- Tool result consumed by GPU1: `<bool>`
- Final product delta valid: `<bool>`
- Blocker: `<reason>`
```

Recommended helper:

```python
def gpu1_one_turn_gate_summary(metrics: dict[str, Any]) -> list[str]:
    ...
```

This keeps renderer readable and testable.

## 2. Final readable product JSON

File:

```text
ia_carmine/product/code_product/final_readable_product/cli.py
```

Already mapped as product report builder.

Additional renderer-specific requirement:

The report JSON should expose the same fields rendered in Markdown:

```text
gpu1_one_turn_runtime_gate_present
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

If the gate failed, `blocking_reasons` must include:

```text
gpu1_one_turn_runtime_gate_failed:<blocker>
```

## 3. Heap runtime product package

File:

```text
ia_carmine/runtime/heap_runtime/product_package/cli.py
```

Observed behavior:

Builds deterministic package reports:

```text
heap_runtime_product_manifest.json
heap_runtime_product_evidence_index.json
heap_runtime_product_readiness.json
heap_runtime_product.md
README.md
```

It compacts supplied `--run-report` and `--run-artifact` paths but does not know specific gate semantics.

Current gap:

```text
If the caller does not pass the GPU1 one-turn gate report as `--run-report` or `--run-artifact`, the package will not include it.
```

Patch requirement options:

Option A — caller-side inclusion:

```text
Ensure launcher/final package builder passes `gpu1_one_turn_runtime_gate.json` to product_package as a run report/artifact.
```

Option B — package-level validation:

```text
If any supplied report has allow_provider_generation/complete provider mode, require a report/artifact with kind `gpu1_one_turn_runtime_gate`.
```

Recommended:

```text
Do both. Caller includes it; package validates presence.
```

Suggested package fields:

```text
gpu1_one_turn_runtime_gate_present
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
```

## 4. Causality renderer

File:

```text
ia_carmine/product/heap_final_proposals/normalize_final_causality/cli.py
```

Additional rendering requirement:

`render_markdown()` should show one-turn gate status under product acceptance reasons when failed/missing.

Suggested line:

```text
- GPU1 one-turn runtime gate: `<passed/failed/missing>` (`<blocker>`)
```

## 5. Operator decision text

File:

```text
ia_carmine/product/code_product/final_readable_product/operator_decision.py
```

Not inspected in this pass, but likely should include one-turn gate status because `OPERATOR_DECISION.txt` is the quick decision surface copied into Documents.

Search/patch target after core gate:

```text
write_operator_decision(...)
```

Expected addition:

```text
gpu1_one_turn_runtime_gate=<passed|failed|missing>
gpu1_one_turn_blocker=<reason>
```

## 6. Product-package validation rule

The renderer/package chain should follow this rule:

```text
A product may be readable even when blocked, but it must not hide the GPU1 one-turn gate status.
```

So:

```text
- blocked product: include gate failure reason;
- ready product: include gate passed evidence path;
- bundle/package validation: require gate artifact when provider generation was enabled.
```

## 7. Patch acceptance for rendering/package layer

```text
[ ] Final readable Markdown has a GPU1 one-turn gate section.
[ ] Final readable JSON exposes one-turn fields.
[ ] OPERATOR_DECISION.txt includes one-turn status.
[ ] Product package includes one-turn gate report as evidence.
[ ] Product package/readiness marks missing/failed one-turn gate as blocked in complete provider mode.
[ ] Bundle completeness can find the gate artifact.
```

## 8. Implementation note

Do not render the full GPU1 chat history in final Markdown. Only render compact refs/paths and counts:

```text
chat_history_ref path
broker_report_refs
consumed request ids
blocker/errors
```

The full chat history should remain a technical artifact, not inline final output.
