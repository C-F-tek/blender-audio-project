# Provider departments model

## Status

Current compact model for the IA-Carmine multi-provider runtime.

## One-line model

```text
one shared heap -> multiple provider departments -> shared evidence -> one classified outcome
```

## Department roles

| Department | Role |
| --- | --- |
| Ollama | Main semantic center. Interprets request/context/evidence and proposes recommendations or candidate operations. |
| GPU1 | Coworker/provider peer. Supports planning, comparison and proposal refinement inside the same heap. |
| GPU0 | Companion/review department. Produces observable peer workload, review evidence and runtime diagnostics. |
| NPU | Micro-lane for microtasks. Produces narrow diagnostic/audit evidence and reports degraded/unavailable states explicitly. |
| Operator | External authority. Provides intent, repository authority, review authority and final judgment. |

## Shared-mind rule

No department owns a separate truth.

A department is useful only when it contributes structured evidence to the same heap/exchange state:

```text
input refs
execution status
output refs
warnings/errors
recommendations
candidate operations
blocked reasons
validation links
```

## Decision rule

```text
Ollama semantic evidence
+ GPU1 coworker evidence
+ GPU0 companion evidence
+ NPU micro-lane evidence
+ broker/tool reports
+ validators
+ source inspection
= classified outcome
```

Possible outcomes:

```text
evidence-only
blocked
candidate operation
code product
patch product
review product
```

## Product rule

```text
provider text != product
provider agreement != product
product requires concrete targets, operations and validation path
```

## Related files

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
Tools/ai/provider_mesh/TOOL_CONTEXT.md
Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md
Tools/validation/provider_mesh/TOOL_CONTEXT.md
Tools/npu/provider_mesh/TOOL_CONTEXT.md
```
