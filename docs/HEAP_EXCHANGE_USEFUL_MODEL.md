# Heap/Exchange useful model

## Status

Current compact model for understanding the IA-Carmine heap/exchange idea.

This document surfaces the useful architecture without requiring a reader to reconstruct it from older task handoffs.

## One-line model

```text
controlled input -> shared heap/exchange -> cooperating lanes -> evidence -> deterministic exit product
```

The heap/exchange is not a fixed script chain. It is a shared runtime knowledge surface where lanes publish and consume evidence.

## Why it exists

A linear pipeline tends to create isolated reports:

```text
script A output
script B output
script C output
no shared state
no real cross-check
no accountable final product
```

The heap/exchange model exists to turn that into:

```text
common runtime state
provider/lane observations
tool evidence
validation signals
proposal candidates
explicit blocked/success exit state
```

## Core boundaries

### IN: controlled entry

A run enters the heap with explicit material:

```text
task/request Markdown
run identity/stamp
repository root and Python path gate
context pack
agent memory/context state
tool inventory
capability evidence
workload/routing evidence
```

The input side must be repeatable and inspectable.

### LOOP: shared heap/exchange

Inside the heap, lanes cooperate through evidence rather than private assumptions.

Typical lanes:

```text
provider planner lane
GPU/OpenVINO companion lane
NPU diagnostic lane
context/memory lane
runtime tool broker lane
validation/CPU authority lane
public exchange event stream
```

The exact lane names can change. The rule does not: a lane is useful only if it is observable and writes structured evidence.

### OUT: deterministic exit

The exit side must not be vague. It should produce one of two states:

```text
success: concrete deterministic product exists
blocked: evidence exists, but no concrete deterministic product exists
```

A blocked state is valid. It is better than pretending that provider prose or metadata-only drafts are a product.

## What the heap is

The heap is the current shared state of the run:

```text
facts
constraints
lane status
provider claims
tool results
validation findings
candidate operations
blocked reasons
final product decision
```

It can be represented through JSON, JSONL, SQLite, reports, manifests or event streams. The storage format is less important than the contract: evidence must be readable by other stages.

## What the exchange is

The exchange is the communication layer around the heap:

```text
runtime entry event
lane registration
provider/tool events
public event stream
runtime state updates
exit product event
validation bridge event
```

The exchange makes the system observable. Without observable exchange events, the system becomes a set of disconnected scripts again.

## What counts as useful output

Useful output is not just text. It must be classified.

```text
diagnostic evidence
recommendation evidence
candidate operation
code product
patch product
review product
blocked reason
```

Only a code/patch product with concrete target operations can move toward source modification.

## Product rule

Provider text is evidence, not product.

```text
provider answer != patch
recommendation != patch
metadata-only draft != patch
candidate without target/diff != patch
```

A source-change product must contain concrete operations, target files and validation path, or explicitly declare non-applicable/blocked status.

## Minimal useful run evidence

A useful heap/exchange run should be able to answer:

```text
What entered the heap?
Which lanes registered?
Which lanes produced evidence?
Which tools were requested?
Which reports were accepted/rejected?
Which validators ran?
What final decision was made?
Was a product produced or explicitly blocked?
```

## Relationship with patch/code products

Heap/exchange decides and explains. Patch/code product applies the deterministic boundary.

```text
heap/exchange evidence
-> candidate product
-> code product or patchkit/repo-patch-runner path
-> validation
-> review/commit path
```

Do not let heap/exchange write source directly unless the operation passes through a controlled product path.

## Related current navigation

```text
CONTEXT_INDEX.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
Tools/ai/heap_exchange/TOOL_CONTEXT.md
Tools/validation/heap_exchange/TOOL_CONTEXT.md
Tools/ai/heap_runtime/TOOL_CONTEXT.md
Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md
Tools/ai/runtime_tool/TOOL_CONTEXT.md
Tools/ai/code_product/TOOL_CONTEXT.md
Tools/ai/patch_product/TOOL_CONTEXT.md
Tools/ai/patchkit/TOOL_CONTEXT.md
```

## Historical source

The older detailed operating note remains useful background:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
```

Use this current document as the compact model and the older file as historical detail.
