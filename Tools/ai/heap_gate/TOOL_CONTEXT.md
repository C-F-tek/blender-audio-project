# Tools/ai/heap_gate context

## Role

`Tools/ai/heap_gate` contains the runtime gate/loop logic that turns startup context and brokered evidence into provider work, proposal iterations, decisions and product signals.

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
GPU1/Ollama -> planner and proposal lane
GPU0/OpenVINO -> reviewer/refiner lane
NPU/OpenVINO -> sampled auditor/guardrail lane
CPU/helper -> broker, validator, lab, composer
```

## Boundaries

- Provider text is evidence, not product.
- Pointer/proposal blocks do not prove provider workload by themselves.
- `provider_execution_performed` must be backed by explicit workload/provider evidence.
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
