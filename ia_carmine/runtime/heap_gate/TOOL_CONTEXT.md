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
- GPU1 is the primary Ollama broker/native tool-call lane and owns final synthesis. Every GPU1 provider revision must materialize a `gpu1_closure_decision_packet` with `gpu1_decision`, `gpu1_block_id`, `gpu1_revision`, `target_files`, `quality_passed`, `reject_reasons` and `evidence_refs`; `generic_write` refs are evidence only and never a GPU1 decision.
- GPU0/Ollama Vulkan is a rapid secondary congruence/veto lane. Its prompt input is only the current GPU1 decision packet plus packet evidence refs, never the full operator request or free historical context. Its output must be structured as `congruent`, `veto`, `refine_required` or `incongruent`, checked against the same GPU1 block/revision. Free text is preserved only as secondary evidence.
- GPU0 can veto/refine only an anchored current GPU1 packet. If the GPU1 packet is missing, GPU0 is `not_evaluated_waiting_for_gpu1_decision`; if GPU0 checks the wrong block/revision the result is `gpu0_checked_wrong_gpu1_packet`; unanchored historical reasons such as stale `product_readiness` are `gpu0_unanchored_reason` and cannot become final veto.
- A GPU0 `veto`, `refine_required` or `incongruent` requires the next GPU1 proposal to declare `refines_block_id=<previous_gpu1_block_id>` and `consumed_gpu0_block_id=<previous_gpu0_block_id>`. Missing linkage is `gpu1_refine_not_linked_to_gpu0_veto`.
- NPU/OpenVINO remains a bounded microtask/tool auditor lane, not primary closer. It emits `microtask_tool_calling_openvino` evidence and cannot substitute GPU1 closure or GPU0 packet review.
- In canonical provider runs, the provider boot gate first proves GPU1/Ollama, GPU0/Ollama Vulkan and NPU/OpenVINO are alive in the same provider window. GPU1 then gets the short replight check. GPU0/NPU useful workload evidence is produced in the real provider loop, not by replaying their full reports as pre-loop replight.
- GPU0 and NPU boot failures are `provider_boot_gate_failed:*` exits. GPU0 loop failures remain provider workload failures. NPU native tool-loop timeout does not erase valid `npu_peer_evidence_verified` evidence, but it is still reported as runtime/tool-loop feedback and cannot close without later GPU1 consumption.
- Time input is a shared heap counter for GPU1 cycles and coordinated soft close. GPU0/NPU sidecars use bounded watchdogs/timeouts; a selected lane that fails to start is still a hard universe block.
- GPU1 must remain resident for the whole provider production cycle, not only until its current subprocess exits. GPU0 uses the same residency rule when selected so provider lanes can call back into each other across revisions. Ollama unload happens at provider production-cycle cleanup, not as a per-lane success proof.
- Soft close enters `soft_lock_state=closing_open_pointers`: no broad new exploration, only merge/veto/refine/classify/resume work until every pointer is merged, rejected, superseded, deferred, externally blocked or requires operator input.
- Soft close exits through closure quorum, not inert repetition. GPU1 emits `soft_lock_closure_owner_decision` from its packet, GPU0 emits `gpu0_closure_agreement` only after a valid packet, CPU validates `closure_quorum_status`, and NPU remains `npu_closure_advisory=evidence_ready_non_closer` when its micro evidence is valid.
- Before provider launch, closure quorum is non-terminal. When `allow_provider_generation=true`, no GPU1/GPU0/NPU quorum may close the run while `provider_reports` are empty and no provider lane has emitted `provider_state`; missing `runtime_file_refs` remains a hard provider-start requirement that must be brokered or reported only as `runtime_file_refs_missing_before_provider_start` after real budget/no-work exhaustion.
- If GPU1 says `no_more_action` or `blocked_continuation` and GPU0 has no active veto, the arbiter closes automatically. If GPU0 vetoes, only one targeted GPU1+GPU0 refinement is allowed; NPU is not relaunched unless a new punctual risk is declared.
- `provider_revision_count` is positive evidence only. It must not be compared to an effective max to cut GPU1 recursion.
- Do not weaken gates to make a run pass.
- Do not convert all context files into patch targets.
- `generic_write` is a broker evidence tool for refined request/action-plan turns. A GPU1/GPU0/NPU no-tool capture or call forces a later GPU1 revision; after three consumed refinements it can close as `generic_write_refined_product`, including code content, but it still cannot claim patch application or source writes.

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
