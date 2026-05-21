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
Tools/ai/run/cli.py
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
python -m Tools.ai run
  -> OperatorProductController
  -> heap_context_closure
  -> run_heap_runtime_completeness_gate
```

This removes the previous split-brain behavior where the canonical command routed directly into `ContractorUniverseRuntime`, a reduced deterministic runtime that could not prove real GPU1/GPU0/NPU provider operation.

### 3. Dry-run contract enriched

Expected dry-run report now declares:

```text
runtime = heap_context_closure
internal_runtime = Tools.ai.operator_product_core.OperatorProductController
heap_runtime = Tools.ai.heap_context_closure
gate_runtime = Tools.ai.heap_runtime.completeness_gate.HeapRuntimeCompletenessGate
provider_generation_requested = true when profile forwards --allow-provider-generation
required_provider_roles = gpu1_planner, gpu0_reviewer_refiner, npu_auditor
```

## Inspection findings still open

### P1 — NPU workload/profile mismatch

Observation:

`Tools/ai/heap_gate/provider_command_specs.py` always adds:

```text
--run-device-workload
```

for `build_npu_micro_task_companion_report`, while profiles such as `deep_external_heap` and `day0_full_code_product` currently set:

```json
"allow_npu_device_workload": false
```

The shared NPU CLI then treats requested-but-not-performed device workload as a hard failure.

Decision required in code:

```text
A) Make NPU device workload mandatory and update profiles/report wording accordingly.
B) Or make provider_command_specs respect allow_npu_device_workload and keep semantic NPU audit mandatory.
```

Given the run-unica contract, the preferred direction is:

```text
NPU microtask provider is mandatory.
NPU physical device workload is controlled/explicit.
The report must distinguish semantic/micro provider activity from device workload activity.
```

### P1 — Verify startup digest is active context

The startup manifest is correctly treated as structured runtime data plane, but next validation must prove that GPU1 actually receives useful request/memory/tool/chunk context via `STARTUP_CONTEXT_DIGEST_FOR_GPU1`.

Relevant files:

```text
Tools/ai/heap_gate/startup_manifest_context.py
Tools/ai/heap_gate/startup_context.py
Tools/ai/heap_gate/provider_prompt.py
```

### P2 — Force GPU1 patch output into extractable unified diff

Current product contract is correct: no real `diff --git`, no real code product.

Next inspection must verify whether the GPU1 prompt and provider feedback force this shape strongly enough:

```text
PATCH_SKETCH
unified diff
repo-relative verified target paths
git apply --check compatible
validation commands
```

Relevant files:

```text
Tools/ai/heap_gate/provider_prompt.py
Tools/ai/heap_gate/provider_commands.py
Tools/ai/patch_product/candidate_synthesis/evidence_diff.py
Tools/ai/_shared/heap_final_code_product.py
```

## Required local validation commands

Run from repository root:

```powershell
python -m py_compile .\Tools\ai\run\cli.py
python -m Tools.ai run --dry-run --run-intensity quick
python -m Tools.ai run --dry-run --run-intensity deep
```

Expected dry-run checks:

```text
runtime == heap_context_closure
internal_runtime == Tools.ai.operator_product_core.OperatorProductController
command contains heap_context_closure
command contains --allow-provider-generation for quick/deep profiles
required_provider_roles contains gpu1_planner/gpu0_reviewer_refiner/npu_auditor
```

## Do not lose context

Next task should continue from here:

```text
Inspect and patch P1 NPU workload/profile mismatch, then inspect GPU1 PATCH_SKETCH/diff extraction pressure.
```
