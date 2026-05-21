# Run unica real product contract — AGENTS.md

## Scope

This folder is the operational handoff for debugging the canonical IA-Carmine run unica path toward a real complex code product.

The objective is not a diagnostic-only package. The objective is a full heap/universe run where the request enters shared runtime state, providers operate with defined roles, tool evidence is absorbed, matrix/lab validation produces concrete patch candidates, and the final package contains a reviewable `CODE_PRODUCT_FULL_PATCH.md` with real non-truncated diffs when a patchable target exists.

## Canonical contract

The canonical product path is:

```text
operator request
  -> startup context/memory reload
  -> heap runtime blackboard
  -> brokered tool evidence
  -> provider universe lanes
  -> GPU1 primary planner
  -> GPU0 coworker reviewer/refiner
  -> NPU microtask auditor
  -> virtual dev / code execution matrix / runtime debug lab
  -> patch candidate synthesis
  -> pointer/revision reconstruction
  -> final readable product
  -> CODE_PRODUCT_FULL_PATCH.md
```

The run is valid only if the product path is owned by the heap/universe runtime and its artifacts prove causality.

## Required provider roles

Provider generation mode is a hard contract. If provider generation is enabled, the following lanes must be present and operational:

```text
GPU1  -> gpu1_planner              -> primary planner / cumulative responder
GPU0  -> gpu0_reviewer_refiner     -> coworker / peer reviewer / refiner
NPU   -> npu_auditor               -> controlled microtask auditor
```

Missing, failed, non-operational, unlinked, or diagnostic-only provider lanes are a run inconsistency, not a cosmetic warning.

## Entry point rule

The expected external operator command surface is:

```powershell
python -m Tools.ai run --request-file <task.md>
```

This command must resolve to the same product path as the operator launcher:

```text
Tools.ai.run
  -> operator product controller
  -> heap_context_closure
  -> run_heap_runtime_completeness_gate
  -> provider lanes
  -> matrix/lab
  -> final readable product
```

It must not silently bypass the heap/product gate through a reduced deterministic-only runtime.

## Product acceptance rule

Provider output is not a code product by itself.

A real final code product requires:

```text
- provider execution evidence
- GPU1/GPU0/NPU roles present in pointer/revision evidence
- code execution matrix passed
- concrete code proposal count > 0
- patch candidate synthesis validated when patch output is required
- CODE_PRODUCT_FULL_PATCH.md exists
- CODE_PRODUCT_FULL_PATCH.md contains at least one real `diff --git` block
- no EMPTY CODE PRODUCT marker
- no NO_APPLICABLE_CODE_PRODUCT marker when a patchable target exists
- no truncation marker
```

If targets are found but no valid diff is produced, the correct status is blocked/diagnostic, not successful product.

## Urgent debug priorities

### P0 — Align `python -m Tools.ai run`

Inspect and patch the canonical `Tools.ai.run` entrypoint so it uses the operator product controller / heap closure path, not a reduced deterministic `ContractorUniverseRuntime` path.

Expected result:

```text
python -m Tools.ai run --dry-run
```

must report a plan that routes through `heap_context_closure` / `run_heap_runtime_completeness_gate`.

### P0 — Enforce provider hard contract

When provider generation is enabled, the final launcher summary must fail if any of these is missing or non-operational:

```text
gpu1_provider_planner
gpu0_provider_peer
npu_micro_task_auditor
```

GPU1 is primary. GPU0 is coworker/reviewer/refiner. NPU is controlled microtask auditor.

### P1 — Verify startup context ingestion

Startup manifest must be the structured runtime data plane, but the request, memory, tool catalog, semantic chunks, and useful context must become active heap/GPU1 context. The readable task file may remain an artifact reference only if equivalent structured context is loaded and cited.

### P1 — Resolve NPU workload/profile mismatch

If the profile says `allow_npu_device_workload=false`, the NPU command builder must not imply uncontrolled device workload. If controlled NPU microtask is mandatory for this contract, make the profile and report explicit.

### P2 — Force GPU1 patch sketch into extractable unified diff

GPU1 must emit concrete `PATCH_SKETCH`/diff content for verified repo-relative target files when a patchable target exists. The matrix/synthesis layer should only promote it if it passes parsing and `git apply --check`.

## Preferred inspection sequence

Run the inspection in this order:

```powershell
python -m Tools.ai run --list-profiles
python -m Tools.ai run --dry-run --run-intensity quick
python -m Tools.ai run --dry-run --run-intensity deep
python -m py_compile Tools/ai/run/cli.py Tools/ai/operator_product_core/controller.py Tools/ai/operator_product_core/runner.py
```

Then inspect:

```text
Tools/ai/run/cli.py
Tools/ai/operator_product_core/controller.py
Tools/ai/operator_product_core/runner.py
Tools/ai/operator_product_core/profiles.py
Tools/ai/heap_context_closure/launcher.py
Tools/ai/heap_context_closure/commands.py
Tools/ai/heap_runtime/completeness_gate/cli.py
Tools/ai/heap_gate/provider_command_specs.py
Tools/ai/heap_gate/provider_execution.py
Tools/ai/heap_gate/provider_block_contract.py
Tools/ai/code_product/final_readable_product/product_contract.py
Tools/ai/patch_product/candidate_synthesis/evidence_diff.py
```

## Guardrails

Allowed without extra confirmation:

```text
- read source/docs
- add documentation under this folder
- patch Python entrypoint/controller code coherently with the canonical contract
- add smoke tests for dry-run routing and provider contract status
- run file-scoped py_compile/smoke commands
```

Do not perform without explicit confirmation:

```text
- destructive delete
- force push
- rewrite history
- secret/permission/billing/visibility changes
- deploy production
- merge protected branches
- apply generated patch specs automatically
- commit output/**, *.db, *.sqlite, renders/**
```

## Reporting rule

When modifying scripts or code files, report the resulting line count for every changed script/code file.

For large or delicate multi-file patches, prefer a ZIP patch bundle with an idempotent runner instead of long inline patch blocks.

## Current conclusion

The immediate inconsistency to fix is the split brain between:

```text
Tools.ai.run -> ContractorUniverseRuntime
```

and the real product path:

```text
OperatorProductController -> heap_context_closure -> completeness gate -> providers -> matrix -> final product
```

The next patch should remove that ambiguity while preserving the hard provider and final code-product contracts.
