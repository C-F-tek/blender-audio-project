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
GPU0/OpenVINO -> coworker reviewer/refiner lane, not primary closer
NPU/OpenVINO -> bounded microtask/tool auditor lane, not primary closer
CPU/helper -> broker, validator, lab, composer
```

## Boundaries

- Provider text is evidence, not product.
- Pointer/proposal blocks do not prove provider workload by themselves.
- `provider_execution_performed` must be backed by explicit workload/provider evidence.
- GPU1 owns closure and may drive broker/native tool calls. GPU0 can review/refine and use tools as evidence. NPU can run only bounded micro audit/tool work and must not hold the run open as semantic closer.
- In canonical provider runs, GPU1 is launched first for a live replight gate, not merely a surface `ollama ps` check. GPU1 must answer with model/backend/device, generated phrase, token metrics, tool/function surface and `replight_passed=true` before GPU0/NPU sidecars or labs can start. CPU-only, unproven, missing or incomplete provider replight blocks immediately before sidecars/labs.
- GPU0 and NPU also have hard replight requirements when selected. A sidecar that cannot produce live provider evidence is a `blocked_with_reason` exit, not a degraded provider success and not a CPU fallback.
- Time input is a shared heap counter for GPU1 cycles and coordinated soft close. GPU0/NPU sidecars use bounded watchdogs/timeouts; a selected lane that fails to start is still a hard universe block.
- Soft close enters `soft_lock_state=closing_open_pointers`: no broad new exploration, only merge/veto/refine/classify/resume work until every pointer is merged, rejected, superseded, deferred, externally blocked or requires operator input.
- Soft close exits through closure quorum, not inert repetition. GPU1 emits `soft_lock_closure_owner_decision`, GPU0 emits `gpu0_closure_agreement`, CPU validates `closure_quorum_status`, and NPU remains `npu_closure_advisory=evidence_ready_non_closer` when its micro evidence is valid.
- If GPU1 says `no_more_action` or `blocked_continuation` and GPU0 has no active veto, the arbiter closes automatically. If GPU0 vetoes, only one targeted GPU1+GPU0 refinement is allowed; NPU is not relaunched unless a new punctual risk is declared.
- `provider_revision_count` is positive evidence only. It must not be compared to an effective max to cut GPU1 recursion.
- Do not weaken gates to make a run pass.
- Do not convert all context files into patch targets.

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
