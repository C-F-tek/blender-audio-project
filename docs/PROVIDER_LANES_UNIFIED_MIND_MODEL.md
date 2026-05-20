# Provider lanes unified mind model

## Status

Current compact model for the IA-Carmine multi-provider runtime idea.

Use this document to understand the intended role split between Ollama/provider, GPU0 and NPU without treating them as isolated agents.

## One-line model

```text
one operational mind -> multiple specialized departments -> shared heap evidence -> deterministic product decision
```

The system should not behave as three unrelated assistants. It should behave as one runtime mind with distinct operational departments.

## Provider departments

| Department | Main role | Expected output |
| --- | --- | --- |
| Ollama / main provider | central reasoning, planning, synthesis, candidate generation | advisory evidence, proposed operations, final reasoning inputs |
| GPU0 / coworker lane | companion reviewer, OpenVINO/helper workload, discrepancy check, peer visibility | peer reports, review evidence, workload proof, contradiction notes |
| NPU / micro-lane | microtask/tool/device provider, small checks, support evidence | micro reports, device/tool-loop facts, audit notes, guardrail hints |
| CPU / validators | deterministic authority, broker, validation, file/source inspection | pass/fail reports, contracts, blocked reasons |

## Core doctrine

```text
Ollama is the main center of reasoning.
GPU0 is the coworker/reviewer department.
NPU is the micro-lane/microtask tool provider.
CPU validators are deterministic authority.
The heap is the shared memory and evidence surface.
```

Ollama may be the main creative/planning center, but it is not allowed to become an unchecked source-writing authority.

## Unified mind rule

The providers must share the same operational picture:

```text
same request
same context refs
same heap state
same product rules
same blocked/success criteria
same evidence ledger
```

If lanes operate on different context, the result is not a unified mind. It is only parallel prompting.

Time is part of that shared operational picture. A run budget is a counter used to choose cycles and request a coordinated soft close near the end; it is not a hard lane cutoff. A provider lane that fails to start is a hard universe block, while a started lane must close through heap state, chunks and pointers.

Provider revision count is evidence, not a recursion limit. The loop may use it as evidence that revisions happened, but must not stop GPU1 because the count reached an effective maximum.

## Single Run, Not Single Direction

`Corsa unica` means one continuous heap universe, not one script line, one cycle or one-way movement.

GPU1 may move on the pointer graph:

```text
current block
-> backtrack to previous/refines block
-> propagate imports, variables, classes, schema fields, CLI flags and contracts
-> ask GPU0/NPU to re-check impacted blocks in parallel
-> resume forward from resume_from_block_id
-> compose/refine the final code product from linked blocks
```

The final code product must be reconstructed from `previous_block_id`, `refines_block_id`, `resume_from_block_id` and linked GPU1/GPU0/NPU blocks. A long provider answer is still only evidence until the pointer graph and deterministic product boundary can compose it.

## Department responsibilities

### Ollama / main provider

Ollama is the central planner and synthesis lane.

It should:

```text
read request/context/evidence
propose candidate operations
explain reasoning at product level
consume reviewer/auditor feedback
revise proposals when evidence rejects them
produce structured recommendation evidence
```

It must not:

```text
claim tool execution without broker evidence
claim validation without validator reports
claim product success without concrete operations
write source directly outside controlled product paths
```

### GPU0 / coworker lane

GPU0 is the coworker/reviewer lane. It is not the main brain, but it should not be decorative.

It should:

```text
prove observable workload when enabled
review or refine provider claims
check discrepancy and feasibility
produce peer evidence
support hardware/runtime visibility
```

Useful GPU0 output is structured evidence, not just device presence.

### NPU / micro-lane

NPU is the microtask/tool/device lane.

It should:

```text
run small diagnostic/audit tasks
run bounded OpenVINO device/tool-loop work when selected
support guardrail and sanity checks
produce compact reports
publish `npu_micro_provider_*` evidence when the micro provider runs
```

NPU must not be documented or reported as the primary semantic provider. It is a
real bounded micro-provider when selected, but it remains support/micro and does
not own final product synthesis. NPU reports must use `npu_micro_provider_*`
fields, not `semantic_provider_*` or `npu_semantic_*` fields.

### CPU / validators

CPU validators and deterministic tools are the final factual authority.

They should:

```text
inspect files
run parsers/compilers/smokes
validate report contracts
classify pass/fail/blocked
prevent provider prose from becoming product
```

## Collaboration loop

```text
request enters heap
preload provides context and tool catalog
Ollama proposes
GPU0 reviews/checks
NPU audits micro-facts
broker/tools produce evidence
validators classify
Ollama revises or finalizes
composer assembles product or blocked reason
```

This is a loop, not a one-shot chain.

## Evidence requirements

Each provider department must leave evidence:

```text
lane name
execution requested/performed
input refs
output refs
warnings/errors
recommendations/rejections
product impact
```

A lane that does not leave evidence is not part of the operational mind.

## Product rule

Provider agreement is not product success.

```text
Ollama says yes + GPU0 says ok + NPU says ok != product
```

A real product still requires:

```text
concrete operation
source target
code/patch product
validation result
reviewable artifact
```

For this classification, read:

```text
docs/REAL_PRODUCT_RUN_MODEL.md
```

## Related current files

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

## Naming note

User shorthand:

```text
Ollama = main center / creator / planner
GPU0 = coworker / reviewer lane
NPU = micro-lane / microtask auditor
```

Use precise role names in code and docs, but preserve this mental model for orientation.
