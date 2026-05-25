# GPU1 one-turn final product propagation map — 2026-05-25

## Purpose

This document maps the downstream surfaces where the production GPU1 one-turn gate must appear after it is generated and validated inside the full run.

The gate cannot remain only an internal runtime metric. It must propagate into:

```text
- heap_context_closure launcher summary;
- final readable product;
- public Documents mirror;
- external heap postrun package;
- external pointer/revision artifacts;
- bundle completeness validation.
```

## 1. Launcher summary

File:

```text
ia_carmine/runtime/heap_context_closure/summary.py
```

Function:

```text
build_launcher_summary(...)
```

Observed role:

This builds `heap_runtime_context_closure_launcher.json` and determines `launcher_passed` from:

```text
state["can_continue"]
heap_result["passed"]
composer_product_ready
launcher_contract_errors
```

It also exposes heap/final/composer/external/final-readable product paths and product status.

Current gap:

```text
No GPU1 one-turn gate fields are surfaced here.
```

Patch requirement:

Read one-turn state from the heap gate report or final payload and include:

```text
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_final_product_delta_valid
gpu1_one_turn_blocker
gpu1_one_turn_errors
```

Launcher contract errors should include a typed blocker when provider generation is enabled and the gate is missing/failed:

```text
gpu1_one_turn_runtime_gate_missing
gpu1_one_turn_runtime_gate_failed
```

## 2. Final readable product

File:

```text
ia_carmine/product/code_product/final_readable_product/cli.py
```

Observed role:

The final product report already copies many GPU1 metrics from `gate.metrics`, including:

```text
gpu1_replight_valid
gpu1_boot_leader_ready
gpu1_primary_workload_valid
gpu1_primary_evidence_valid
gpu1_primary_evidence_source
leader_source
gpu1_native_tool_call_count
sidecars_start_policy
parallel_provider_overlap_seconds
gpu1_leader_valid
gpu1_consumed_gpu0_peer
gpu1_consumed_npu_peer
```

Current gap:

```text
It does not expose the one-turn production gate.
```

Patch requirement:

Add to the final readable product report and, preferably, Markdown summary:

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

Final readable product `passed` must remain false in complete/full mode when the gate fails, even if a text surface exists.

## 3. Public Documents mirror

File:

```text
ia_carmine/product/operator_product_core/public_documents.py
```

Observed role:

Copies final readable product files and selected technical artifacts into:

```text
%USERPROFILE%\Documents\aicarmine_gui_launcher_lab_<stamp>
```

Selected technical files currently include:

```text
operator_product_launcher_run.json/md
heap_runtime_context_closure_launcher.json
heap_final_readable_product.json/md/txt
external_heap_block_pointer_manifest.json/md
external_heap_revision_context.json/md
```

Current gap:

```text
It will not copy `gpu1_one_turn_runtime_gate.json` unless that file is included in the final readable product documents dir or explicitly added to selected artifacts.
```

Patch options:

Option A — Include gate report in final documents outputs.

Option B — Add gate report name/path to `_copy_selected_run_artifacts()`.

Recommended:

```text
Option A for user-facing evidence package, plus Option B for technical mirror safety.
```

## 4. External heap postrun package

File:

```text
ia_carmine/runtime/external_heap/postrun_package/cli.py
```

Observed role:

Runs postrun adapters:

```text
build_external_heap_block_pointer_manifest
normalize_heap_final_causality
compose_external_heap_block_response
build_external_heap_revision_context
```

Then aggregates `provider_execution_performed` from pointer/long response/revision reports.

Current gap:

```text
Postrun package does not know whether GPU1 one-turn gate passed.
```

Patch requirement:

Ensure pointer/long response/revision reports carry one-turn fields so postrun can expose:

```text
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_blocker
```

The postrun package should not infer the gate from provider execution alone.

## 5. External block pointer manifest

File:

```text
ia_carmine/runtime/external_heap/block_pointer_manifest/cli.py
```

Observed role:

Builds persistent external block graph from:

```text
proposal_blocks(...)
provider_blocks(...)
provider_rejections(...)
```

`proposal_blocks()` already carries several proposal-level fields:

```text
final_product_delta_valid
final_product_protocol
final_product_file_read_verified
final_product_file_read_refs
gpu1_code_delta_without_file_read
gpu1_closure_decision_packet
quality_passed
accepted
consumed_gpu0_block_ids
consumed_npu_block_ids
consumed_provider_block_ids
```

Current gap:

```text
Proposal blocks do not carry GPU1 one-turn gate data.
```

Patch requirement:

Add to each proposal block from the proposal iteration report:

```text
gpu1_one_turn_runtime_gate_path
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_final_product_delta_valid
gpu1_one_turn_blocker
gpu1_one_turn_errors
```

Manifest top-level should also aggregate:

```text
gpu1_one_turn_runtime_gate_passed
source_gpu1_one_turn_gate_count
gpu1_one_turn_gate_failed_count
gpu1_one_turn_gate_blockers
```

## 6. Proposal iteration artifact

File already identified:

```text
ia_carmine/runtime/heap_gate/proposal_cycle_a.py
```

Why it matters downstream:

`external_heap/block_pointer_manifest/cli.py::proposal_blocks()` reads proposal iteration JSON files. Therefore, if `proposal_cycle_a.py` does not write one-turn fields into proposal iterations, external heap cannot expose them.

Patch requirement:

Add one-turn fields to `data = { ... }` in `write_proposal_iteration_artifact(...)`.

## 7. Bundle completeness validation

Files:

```text
Tools/validation/_shared/full_run_bundle_completeness.py
Tools/validation/real_product/check_full_run_bundle_completeness/cli.py
```

Observed role:

Validates ZIP contents against artifact list and required recursive roots.

Patch requirement:

Once final documents or technical artifacts include the gate report, bundle validation should assert:

```text
- at least one artifact/member has kind/path matching `gpu1_one_turn_runtime_gate`;
- it is required in complete/full provider runs;
- bundle validation fails if the gate is missing.
```

## 8. Final product pass/fail propagation rule

Production rule:

```text
If allow_provider_generation is true and complete/full mode is expected,
then final readable product, launcher summary, external postrun package and bundle completeness cannot pass without the one-turn gate.
```

Required pass chain:

```text
gpu1_one_turn_runtime_gate.passed == true
-> heap_runtime_completeness_gate.passed may be true
-> heap_context_closure_launcher.launcher_passed may be true
-> heap_final_readable_product.passed may be true
-> public documents package may be accepted
-> full-run bundle completeness may be true
```

Missing/failing gate should produce:

```text
product_status=blocked_with_reason or blocked_continuation_product
product_blocked_reason=gpu1_one_turn_runtime_gate_failed:<reason>
```

## 9. Updated implementation chain

Add/patch in this downstream order after core gate exists:

```text
1. proposal_cycle_a.py: write one-turn fields into proposal iteration.
2. external_heap/block_pointer_manifest/cli.py: copy/aggregate one-turn fields.
3. external_heap/postrun_package/cli.py: expose one-turn summary from generated reports.
4. final_readable_product/cli.py: include one-turn fields and blockers in final product report/Markdown.
5. heap_context_closure/summary.py: add launcher one-turn fields and launcher contract blocker.
6. public_documents.py: copy gate report into technical/public output package.
7. full_run_bundle_completeness.py: require gate artifact in complete/full provider run bundles.
```

## 10. Final note

At this point the implementation search shows two layers:

Core production enforcement:

```text
gpu1_native_tool_chat_loop.py
provider_execution.py
provider_commands.py
provider_report_absorption.py
run_loop_metrics.py
terminal_invariants.py
```

Downstream propagation:

```text
proposal_cycle_a.py
external_heap/block_pointer_manifest/cli.py
external_heap/postrun_package/cli.py
final_readable_product/cli.py
heap_context_closure/summary.py
public_documents.py
full_run_bundle_completeness.py
```

Both layers are required. Core enforcement alone is not enough if the final package hides the gate evidence.
