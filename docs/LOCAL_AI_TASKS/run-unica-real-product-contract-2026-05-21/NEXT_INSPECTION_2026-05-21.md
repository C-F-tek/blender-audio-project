# Next inspection — run unica real product

## Objective

Continue toward a real complex product with the heap universe active:

```text
request -> startup reload -> heap blackboard -> brokered tools -> GPU1/GPU0/NPU providers -> matrix/lab -> patch synthesis -> final code product
```

No relevant code surface should remain uninspected.

## Completed patches now on master

```text
157c206 fix(ai): route canonical run through operator product launcher
77fc1b7 fix(ai): respect controlled NPU device workload flag
f76c4b5 fix(ai): recognize unified patch sketch evidence keys
e83d435 fix(ai): always expose startup manifest digest to GPU1
2691595 fix(ai): restore valid final code product renderer
b22713f fix(ai): accept diff-path final code products
```

Note: commit `408b07d` introduced the intended diff-path logic but also a renderer syntax defect. It was neutralized by `2691595`, then safely reapplied as `b22713f` with only the `item_has_code_product()` logic changed.

## Current inspected surfaces

```text
Tools/ai/run/cli.py
Tools/ai/operator_product_core/controller.py
Tools/ai/operator_product_core/runner.py
Tools/ai/operator_product_core/profiles.py
Tools/ai/heap_context_closure/launcher.py
Tools/ai/heap_context_closure/commands.py
Tools/ai/heap_context_closure/summary.py
Tools/ai/heap_runtime/completeness_gate/cli.py
Tools/ai/heap_gate/loop_steps.py
Tools/ai/heap_gate/proposal_cycle_a.py
Tools/ai/heap_gate/proposal_cycle_b.py
Tools/ai/heap_gate/provider_command_specs.py
Tools/ai/heap_gate/provider_execution.py
Tools/ai/heap_gate/provider_process_collection.py
Tools/ai/heap_gate/provider_report_absorption.py
Tools/ai/heap_gate/provider_block_contract.py
Tools/ai/heap_gate/provider_prompt.py
Tools/ai/heap_gate/provider_prompt_text.py
Tools/ai/heap_gate/provider_context.py
Tools/ai/heap_gate/startup_context.py
Tools/ai/heap_gate/startup_manifest_context.py
Tools/ai/heap_gate/matrix_lab.py
Tools/ai/heap_gate/matrix_lab_evidence.py
Tools/ai/patch_product/candidate_synthesis/evidence_diff.py
Tools/ai/code_product/final_readable_product/cli.py
Tools/ai/code_product/final_readable_product/product_contract.py
Tools/ai/_shared/heap_final_code_product.py
Tools/validation/heap_runtime/run_heap_startup_context_ingestion_smoke/cli.py
```

## New finding fixed

`Tools/ai/heap_gate/matrix_lab_evidence.py` can pass synthesis candidates into the matrix as objects with:

```text
implementation_status = validated_patch_candidate
source = patch_candidate_synthesis
diff_path = <candidate diff>
```

`Tools/ai/_shared/heap_final_code_product.py` previously required `code_or_patch_sketch` even when `diff_path` existed, so a valid synthesized diff could be lost before `CODE_PRODUCT_FULL_PATCH.md`. Commit `b22713f` fixes this: validated candidates with `diff_path` now count as code product items.

## Urgent next checks

### 1. Validate locally or via CI-like smoke

Run from repo root:

```powershell
python -m py_compile `
  .\Tools\ai\run\cli.py `
  .\Tools\ai\heap_gate\provider_command_specs.py `
  .\Tools\ai\heap_gate\provider_prompt.py `
  .\Tools\ai\patch_product\candidate_synthesis\evidence_diff.py `
  .\Tools\ai\_shared\heap_final_code_product.py

python -m Tools.ai run --dry-run --run-intensity quick
python -m Tools.ai run --dry-run --run-intensity deep
python -m Tools.validation run_heap_startup_context_ingestion_smoke
python -m Tools.validation run_patch_candidate_synthesis_smoke
python -m Tools.validation run_heap_final_readable_product_smoke
```

Expected dry-run invariants:

```text
runtime == heap_context_closure
internal_runtime == Tools.ai.operator_product_core.OperatorProductController
gate_runtime == Tools.ai.heap_runtime.completeness_gate.HeapRuntimeCompletenessGate
provider_generation_requested == true
required_provider_roles includes gpu1_planner, gpu0_reviewer_refiner, npu_auditor
```

### 2. Validate GPU1 startup digest

`Tools/ai/heap_gate/provider_prompt.py` must keep these terms in the startup digest path:

```text
STARTUP_CONTEXT_DIGEST_FOR_GPU1
structured_manifest_summary
startup_manifest
request_preview
artifact_keys
context_files_sample
tool_execution_count
Use this as active heap context
```

### 3. Validate NPU command semantics

Expected behavior:

```text
NPU microtask provider lane is always part of provider generation mode.
--run-device-workload appears only when allow_npu_device_workload is true.
```

### 4. Validate patch synthesis bridge

Expected behavior:

```text
GPU1 emits PATCH_SKETCH_UNIFIED_DIFF.
Patch synthesis recognizes patch_sketch_unified_diff.
Diff target headers must be repo-relative and allowlisted.
git apply --check must pass before final product status can become real code product.
validated diff_path candidates must be rendered into CODE_PRODUCT_FULL_PATCH.md.
```

## Next surfaces to inspect

```text
Tools/ai/heap_gate/tool_broker.py
Tools/ai/runtime_tool/broker/registry.py
Tools/ai/heap_runtime/code_execution_tool/cli.py
Tools/ai/_shared/heap_code_execution_tool_core.py
Tools/ai/external_heap/postrun_package/cli.py
Tools/ai/external_heap/revision_context/*.py
Tools/ai/external_heap/block_pointer_manifest/*.py
Tools/validation/heap_runtime/run_heap_final_readable_product_smoke/cli.py
Tools/validation/patch_product/run_patch_candidate_synthesis_smoke/cli.py
```

## Hard rule

A package or readable report is not success. Success requires provider-role evidence, matrix/lab evidence, patch candidate extraction, and `CODE_PRODUCT_FULL_PATCH.md` with real non-truncated diff when a patchable target exists.
