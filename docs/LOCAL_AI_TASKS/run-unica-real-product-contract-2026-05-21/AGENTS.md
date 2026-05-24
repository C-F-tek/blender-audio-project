# Run unica real product contract — AGENTS.md

## Scope

This folder is the operational handoff for debugging the canonical IA-Carmine run unica path toward a real complex code product.

The objective is not a diagnostic-only package. The objective is a full heap/universe run where the request enters shared runtime state, providers operate with defined roles, tool evidence is absorbed, matrix/lab validation produces concrete patch candidates, and the final package contains a reviewable `CODE_PRODUCT_FULL_PATCH.md` with real non-truncated diffs when a patchable target exists.

The run must stay one integrated recursive flow. The final product bundle must be reconstructed from heap memory, pointer links and GPU1/GPU0/NPU pointer records produced at each round, so the system does not depend on chat context or a single provider token window.

GPU0 may enrich the pointer graph with coherent propagation information, including text/script/change refs, then return control to the main GPU1 pointer record. When a partial response is rejected, the wrong response becomes explicit evidence and the next cycle must ask GPU1 to change response typology. A first-turn GPU1 plan is allowed only as `PLAN_THEN_PROPOSAL` evidence, not as product.

`contractor_universe` is not to be excluded. Treat its priority heap and logical
soft-time clock as the compact model to integrate into the same canonical run,
not as a standalone route and not as product proof without provider evidence.

Every useful surface for the task must remain visible in that one flow:
startup manifest, memory reload, tool catalog, semantic chunks, provider
teamwork packet, contractor scheduler surface, broker/tool evidence,
matrix/lab, pointer/revision context and code-product bundle. One surface must
not exclude another unless a validator proves it is irrelevant for the selected
task.

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
python -m ia_carmine.cli run --request-file <task.md>
```

This command must resolve to the same product path as the operator launcher:

```text
ia_carmine.runtime.run
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

### P0 — Align `python -m ia_carmine.cli run`

Inspect and patch the canonical `ia_carmine.runtime.run` entrypoint so it uses the operator product controller / heap closure path, not a reduced deterministic `ContractorUniverseRuntime` path.

Expected result:

```text
python -m ia_carmine.cli run --dry-run
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

### P1 — Resolve NPU workload/direct-parameter mismatch

If `allow_npu_device_workload=false`, the NPU command builder must not imply uncontrolled device workload. If controlled NPU microtask is mandatory for this contract, make the direct parameter and report explicit.

### P2 — Force GPU1 patch sketch into extractable unified diff

GPU1 must emit concrete `PATCH_SKETCH`/diff content for verified repo-relative target files when a patchable target exists. The matrix/synthesis layer should only promote it if it passes parsing and `git apply --check`.

## Preferred inspection sequence

Run the inspection in this order:

```powershell
python -m ia_carmine.cli run --dry-run
python -m ia_carmine.cli run --dry-run --allow-provider-generation --max-iterations 2 --max-rounds 8
python -m py_compile ia_carmine/runtime/run/cli.py ia_carmine/product/operator_product_core/controller.py ia_carmine/product/operator_product_core/runner.py
```

Then inspect:

```text
ia_carmine/runtime/run/cli.py
ia_carmine/product/operator_product_core/controller.py
ia_carmine/product/operator_product_core/runner.py
ia_carmine/product/operator_product_core/direct_command.py
ia_carmine/runtime/heap_context_closure/launcher.py
ia_carmine/runtime/heap_context_closure/commands.py
ia_carmine/runtime/heap_runtime/completeness_gate/cli.py
ia_carmine/runtime/heap_gate/provider_command_specs.py
ia_carmine/runtime/heap_gate/provider_execution.py
ia_carmine/runtime/heap_gate/provider_block_contract.py
ia_carmine/product/code_product/final_readable_product/product_contract.py
ia_carmine/product/patch_product/candidate_synthesis/evidence_diff.py
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

The historical split-brain entrypoint was fixed by commit `157c206`, and the real product path is now the expected route:

```text
OperatorProductController -> heap_context_closure -> completeness gate -> providers -> matrix -> final product
```

The current urgent risk is subtler: a recoverable GPU1/GPU0/NPU provider graph without a proposal chunk must resume inside the same run universe. It must not be reported as a final product and must not create an out-of-band product flow.
