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
| NPU / micro-lane | microtask auditor, diagnostic lane, small checks, support evidence | micro reports, diagnostic facts, audit notes, guardrail hints |
| CPU / validators | deterministic authority, broker, validation, file/source inspection | pass/fail reports, contracts, blocked reasons |

## Core doctrine

```text
Ollama is the main center of reasoning.
GPU0 is the coworker/reviewer department.
NPU is the micro-lane/microtask auditor.
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

NPU is the microtask lane.

It should:

```text
run small diagnostic/audit tasks
support guardrail and sanity checks
produce compact reports
stay honest about diagnostic-only status unless compute lane is validated
```

NPU should not be documented as a full compute provider until code and validation prove that role.

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
