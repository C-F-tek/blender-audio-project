# AI Entry Memorandum — Heap runtime is the source of truth

## Purpose

This memorandum is mandatory context for any AI entering this project.

The project is not trying to make a single chat pretend to remember more than it can. The project exists because that model is insufficient.

A chat-only AI becomes unreliable when the project exceeds its context window, when prior decisions live in old conversations, when runtime evidence is scattered across artifacts, and when the system requires multiple agents to cooperate over time.

This project is designed to overcome that limit.

The chat is only a temporary client. The operational system is the heap runtime.

## The limit being overcome

A standalone chat has structural limits:

```text
limited context window
fragile memory across sessions
no native ownership of runtime state
weak continuity across long tasks
poor recovery of old decisions
no automatic distinction between fact, guess, decision, evidence, and product
no guaranteed awareness of repository contracts
no shared state between AI entities unless an external system enforces it
```

If an AI acts only from chat context, it will eventually become useless for this project: it will guess, duplicate layers, patch symptoms, forget constraints, confuse diagnostics with product, and lose causal continuity.

The project is explicitly trying to make that failure mode impossible or at least detectable.

## Core doctrine

```text
chat = temporary interface / client
heap = live shared operational state
artifacts = verifiable memory
pointers = decision continuity and product graph
tools = sensors and actuators
provider lanes = operational entities
composer = product/output assembler
revision context = continuity between runs
```

The AI must not treat its conversation context as project consciousness.

The AI must recover context from repository files, heap artifacts, reports, manifests, pointer graphs, revision contexts, and validation evidence.

## Non-negotiable rule

```text
The chat is not the memory of the system.
The chat is only a client.
Memory, decisions, constraints, evidence, and product state live in the heap runtime.
```

Any AI that acts only from chat history is operating with partial context.

Any AI that patches code before reconstructing the relevant runtime contracts is increasing entropy.

## What the heap universe means

The heap universe is not a static Markdown file, not a ZIP bundle, not a pointer manifest alone, and not a single JSON report.

It is the operational chain:

```text
user request
→ preflight
→ startup context/memory/tool reload
→ shared heap state
→ broker/tool evidence
→ provider lanes
→ proposal iterations
→ pointer/product graph
→ composer output
→ post-run package
→ revision context for the next run
```

The system must force AI participants to read, write, recover, validate, and cooperate through shared state instead of relying on fragile chat memory.

## Why this matters

The objective is not a nicer prompt.

The objective is to build a runtime where AI entities can continue working even when the original chat is gone, incomplete, stale, or misleading.

The heap must provide what the chat cannot reliably provide:

```text
persistent operational memory
state shared across AI entities
recoverable decisions
artifact-backed evidence
runtime-visible needs and claims
validated candidate operations
provider peer review
audit trail
product graph
resume and back-refinement points
```

Every AI entering the project must understand this: the weakness of chat context is not an incidental inconvenience. It is the technical problem the project is designed to solve.

## Correct AI behavior

An AI entering the project must:

1. identify the current branch and latest commits before reasoning about state;
2. read the relevant repository files before proposing fixes;
3. identify the entrypoint, caller, consumer, JSON contract, and side effects for each touched component;
4. reuse existing tools before creating new ones;
5. distinguish product artifacts from diagnostics;
6. distinguish provider execution evidence from pointer/product continuity;
7. preserve guardrails: no patch application, source writes, delete, force-push, rewrite history, deploy, secrets, permission, billing, visibility, or merge unless explicitly authorized;
8. produce evidence-backed findings, not architectural guesses;
9. avoid adding layers unless the existing contract has been mapped and found insufficient;
10. stop rather than patch if it cannot reconstruct the relevant contract.

## Pointer doctrine

Pointers are not merely diagnostics.

Pointers are part of the product contract.

They exist to:

```text
recover old decisions
navigate forward and backward
connect proposal chunks
mark refinement relations
support resume points
allow GPU0/NPU review of older blocks
compose a long final product beyond a single provider window
feed revision context into the next run
```

Pointer presence alone must not prove provider execution.

The correct separation is:

```text
pointer graph = product/runtime contract and decision continuity
provider_execution_performed = separate guardrail requiring explicit provider/workload evidence
```

## Provider lane doctrine

GPU1 is not a generic answer generator. It is the planner/author lane and must produce concrete, file-grounded proposal blocks.

GPU0 is not decoration. It is reviewer/refiner and may back-refine previous blocks, not only the latest output.

NPU is not decoration. It is auditor/guardrail and may verify placeholder code, invented paths, invalid claims, missing evidence, or unsafe state transitions.

The provider lanes must operate over the same heap state, artifact set, and pointer graph.

## Startup context doctrine

Startup preload is active heap input.

It must not be reduced to a path string or a post-hoc report.

Startup reload should provide the current project context through tool-owned artifacts such as context packs, memory inventories, tool catalogs, semantic chunks, validation evidence, and task files.

The gate/runner must make this context observable to provider lanes before they make decisions.

## Product doctrine

A valid product is not a generic final chat answer.

A valid product is assembled from verifiable artifacts:

```text
heap report
provider reports
proposal chunks
GPU0 reviews/refinements
NPU audits
pointer graph
composer output
post-run package
revision context
validation evidence
```

The final long response is a product view over the artifact graph, not the source of truth itself.

## Anti-patterns

Do not do these:

```text
patch from chat memory only
add a new parallel layer because one script failed
turn every failure into another wrapper
treat pointer manifests as only diagnostics
set provider_execution_performed from block presence alone
ignore existing smoke tests
ignore existing tools and create duplicates
write source without mapping caller/consumer contracts
confuse packaged output with runtime truth
confuse successful packaging with accepted product
confuse a convincing explanation with verified project knowledge
```

## Minimum file-level review before changing code

Before touching a file, record:

```text
file path
responsibility
who calls it
who consumes its output
input contract
output contract
side effects
guardrails
tests/smokes covering it
related artifacts
failure being fixed
reason the existing tool cannot already do it
```

If this cannot be answered, do not patch.

## Operational consequence

The system must be designed so that an AI does not need to "remember" the project from chat.

The AI must be able to re-enter by reading the heap universe:

```text
repository state
runtime artifacts
pointer graph
revision context
validation reports
operator policies
```

The goal is not a smarter chat.

The goal is an AI operating system for the project where chat is only one client of a persistent, inspectable, tool-grounded runtime.

## Final instruction to entering AI

If you are an AI entering this repository, do not prove that you can produce text.

Prove that you can recover state.

Prove that you can identify the correct source of truth.

Prove that you can distinguish artifact, evidence, decision, proposal, product, and guardrail.

Prove that you can operate inside the heap universe instead of replacing it with your temporary chat context.
