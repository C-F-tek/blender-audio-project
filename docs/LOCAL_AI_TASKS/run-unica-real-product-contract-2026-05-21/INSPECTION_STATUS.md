# Run unica real product contract — inspection status

## Timestamp

2026-05-21

## Current objective

Continue debugging the IA-Carmine canonical run unica so the system produces a real complex code product with the universe active:

```text
request -> startup reload -> heap blackboard -> brokered tools -> GPU1/GPU0/NPU providers -> matrix/lab -> patch synthesis -> final code product
```

## Completed in this inspection

### 1. Contract folder created

Added:

```text
docs/LOCAL_AI_TASKS/run-unica-real-product-contract-2026-05-21/AGENTS.md
```

Purpose: local/agent handoff for the run unica real-product contract.

### 2. Canonical entrypoint aligned

Patched:

```text
ia_carmine/runtime/run/cli.py
```

Commit:

```text
157c206fdcc8eecc4c327d81880f3898ebbcfb8e
```

Resulting line count:

```text
391
```

Behavioral intent:

```text
python -m ia_carmine.cli run
  -> OperatorProductController
  -> heap_context_closure
  -> run_heap_runtime_completeness_gate
```

This removes the previous split-brain behavior where the canonical command routed directly into `ContractorUniverseRuntime`, a reduced deterministic runtime that could not prove real GPU1/GPU0/NPU provider operation.

### 3. Dry-run contract enriched

Expected dry-run report now declares:

```text
runtime = heap_context_closure
internal_runtime = ia_carmine.product.operator_product_core.OperatorProductController
heap_runtime = ia_carmine.runtime.heap_context_closure
gate_runtime = ia_carmine.runtime.heap_runtime.completeness_gate.HeapRuntimeCompletenessGate
provider_generation_requested = true when the direct CLI forwards --allow-provider-generation
required_provider_roles = gpu1_planner, gpu0_reviewer_refiner, npu_auditor
```

### 4. P1 NPU workload/direct-parameter mismatch patched

Patched:

```text
ia_carmine/runtime/heap_gate/provider_command_specs.py
```

Commit:

```text
77fc1b7a03c0e34c773a39d3dd9385718d24746c
```

Resulting line count:

```text
154
```

Behavioral intent:

```text
NPU microtask provider lane remains mandatory in provider generation mode.
Physical OpenVINO/NPU device workload is controlled by allow_npu_device_workload.
```

Before this patch, `provider_command_specs.py` always forwarded `--run-device-workload` to the NPU report tool even when selected runtime parameters declared `allow_npu_device_workload=false`. That made parameter semantics inconsistent with runtime behavior.

### 5. P2 provider diff extraction key patched

Patched:

```text
ia_carmine/product/patch_product/candidate_synthesis/evidence_diff.py
```

Commit:

```text
f76c4b521fff26f71284eae25e8d1dcc618526fa
```

Resulting line count:

```text
193
```

Behavioral intent:

```text
GPU1 prompt requires PATCH_SKETCH_UNIFIED_DIFF.
Patch candidate synthesis now recognizes patch_sketch_unified_diff as an evidence diff key.
```

The extractor also now recognizes `diff_text` and `full_patch`, reducing the risk that valid provider-generated unified diffs are ignored because of field-name mismatch.

## Still open

### P1 — Verify startup digest is active context

The startup manifest is correctly treated as structured runtime data plane, but next validation must prove that GPU1 actually receives useful request/memory/tool/chunk context via `STARTUP_CONTEXT_DIGEST_FOR_GPU1`.

Relevant files:

```text
ia_carmine/runtime/heap_gate/startup_manifest_context.py
ia_carmine/runtime/heap_gate/startup_context.py
ia_carmine/runtime/heap_gate/provider_prompt.py
```

### P2 — Verify GPU1 diff pressure end to end

The prompt now demands `PATCH_SKETCH_UNIFIED_DIFF`, and synthesis recognizes that key, but the end-to-end path must still be validated:

```text
GPU1 provider output -> evidence report -> _json_text_sources -> _diff_blocks -> diff_targets -> git apply --check -> code matrix -> CODE_PRODUCT_FULL_PATCH.md
```

Relevant files:

```text
ia_carmine/runtime/heap_gate/provider_prompt_text.py
ia_carmine/runtime/heap_gate/provider_prompt.py
ia_carmine/runtime/heap_gate/provider_commands.py
ia_carmine/product/patch_product/candidate_synthesis/evidence_diff.py
ia_carmine/_shared/heap_final_code_product.py
ia_carmine/product/code_product/final_readable_product/product_contract.py
```

### P2 — Add focused smoke tests

Recommended smoke coverage:

```text
1. dry-run route asserts ia_carmine.runtime.run -> heap_context_closure.
2. provider_command_specs asserts --run-device-workload appears only when allow_npu_device_workload=true.
3. evidence_diff asserts patch_sketch_unified_diff JSON field containing a diff --git block is extracted.
```

## Required local validation commands

Run from repository root:

```powershell
python -m py_compile `
  .\ia_carmine\runtime\run\cli.py `
  .\ia_carmine\runtime\heap_gate\provider_command_specs.py `
  .\ia_carmine\product\patch_product\candidate_synthesis\evidence_diff.py

python -m ia_carmine.cli run --dry-run
python -m ia_carmine.cli run --dry-run --allow-provider-generation --max-iterations 2 --max-rounds 8
```

Expected dry-run checks:

```text
runtime == heap_context_closure
internal_runtime == ia_carmine.product.operator_product_core.OperatorProductController
command contains heap_context_closure
command contains --allow-provider-generation only when explicitly requested
required_provider_roles contains gpu1_planner/gpu0_reviewer_refiner/npu_auditor
```

Recommended focused NPU command-spec check:

```text
Without --allow-npu-device-workload, NPU command must not contain --run-device-workload.
With --allow-npu-device-workload, NPU command must contain --run-device-workload.
```

## Do not lose context

Next task should continue from here:

```text
Inspect startup digest active context, then add focused smoke tests for dry-run routing, controlled NPU workload flag, and patch_sketch_unified_diff extraction.
```
