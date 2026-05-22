# ia_carmine/runtime/heap_gate context

## Role

`ia_carmine/runtime/heap_gate` contains the runtime gate/loop logic that turns startup context and brokered evidence into provider work, proposal iterations, decisions and product signals.

It is the control plane for the shared heap universe. It must not be reduced to a linear script chain.

## Responsibilities

- Initialize runtime state for a request.
- Consume startup context and startup manifests.
- Build provider prompts from verified context.
- Coordinate provider lanes and brokered tool requests.
- Record facts, claims, decisions, tool evidence and proposal chunks.
- Enforce terminal invariants and source-write guardrails.
- Select target candidates without treating the whole context as patchable.

## Key concepts

```text
heap state -> shared runtime blackboard
broker -> required tool execution control plane
provider lanes -> GPU1/GPU0/NPU roles
proposal chunks -> evidence blocks, not final product
matrix/lab -> deterministic code-product evidence
terminal invariants -> final status contract
```

## Provider roles

```text
GPU1/Ollama -> planner, review opener, closure owner and final synthesis lane
GPU0/Ollama Vulkan -> coworker reviewer/refiner lane, not primary closer
NPU/OpenVINO -> bounded microtask/tool auditor lane, not primary closer
CPU/helper -> broker, validator, lab, composer
```

## Boundaries

- Provider text is evidence, not product.
- Pointer/proposal blocks do not prove provider workload by themselves.
- `provider_execution_performed` must be backed by explicit workload/provider evidence.
- GPU1 and GPU0 are Ollama operative lanes and may drive broker/native tool calls. NPU can emit bounded micro audit/veto/tool evidence only as diagnostic support and must not drive broker execution or hold closure as semantic closer.
- In canonical provider runs, the provider boot gate first proves GPU1/Ollama, GPU0/Ollama Vulkan and NPU/OpenVINO are alive in the same provider window. GPU1 then gets the short replight check. GPU0/NPU useful workload evidence is produced in the real provider loop, not by replaying their full reports as pre-loop replight.
- GPU0 and NPU boot failures are `provider_boot_gate_failed:*` exits. GPU0/NPU loop failures remain provider workload failures, not degraded provider success and not CPU fallback.
- Time input is a shared heap counter for GPU1 cycles and coordinated soft close. GPU0/NPU sidecars use bounded watchdogs/timeouts; a selected lane that fails to start is still a hard universe block.
- GPU1 must remain resident for the whole provider production cycle, not only until its current subprocess exits. GPU0 uses the same residency rule when selected so provider lanes can call back into each other across revisions. Ollama unload happens at provider production-cycle cleanup, not as a per-lane success proof.
- Soft close enters `soft_lock_state=closing_open_pointers`: no broad new exploration, only merge/veto/refine/classify/resume work until every pointer is merged, rejected, superseded, deferred, externally blocked or requires operator input.
- Soft close exits through closure quorum, not inert repetition. GPU1 emits `soft_lock_closure_owner_decision`, GPU0 emits `gpu0_closure_agreement`, CPU validates `closure_quorum_status`, and NPU remains `npu_closure_advisory=evidence_ready_non_closer` when its micro evidence is valid.
- If GPU1 says `no_more_action` or `blocked_continuation` and GPU0 has no active veto, the arbiter closes automatically. If GPU0 vetoes, only one targeted GPU1+GPU0 refinement is allowed; NPU is not relaunched unless a new punctual risk is declared.
- `provider_revision_count` is positive evidence only. It must not be compared to an effective max to cut GPU1 recursion.
- Do not weaken gates to make a run pass.
- Do not convert all context files into patch targets.
- `generic_write` is a broker evidence tool for refined request/action-plan turns. A GPU1/GPU0 call forces a later GPU1 revision; after three consumed refinements it can close as `generic_write_refined_product`, including code content, but it still cannot claim patch application or source writes.

## Expected downstream outputs

Heap gate output should support downstream assembly of:

```text
heap runtime report
broker tool outputs
provider teamwork reports
proposal iterations
pointer manifest
revision context
final readable product
CODE_PRODUCT_FULL_PATCH.md or explicit blocked/non-applicable result
```

## Extension notes

When extending this area, add validation in `Tools/validation/heap_runtime`, `Tools/validation/heap_provider` or `Tools/validation/runtime_universe` as appropriate. Runtime behavior changes without contract tests are high risk.
