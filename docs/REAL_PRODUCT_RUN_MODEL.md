# Real product run model

## Status

Current compact model extracted from historical real-product/run-unica notes.

Use this document to distinguish evidence-producing runs, blocked runs and real product runs.

## One-line model

```text
task MD -> heap/exchange evidence -> candidate operations -> code/patch product -> validation -> reviewable product
```

A run is useful only if its final state is classified honestly.

## Core distinction

```text
task Markdown = input
provider answer = evidence
runtime report = evidence
recommendation = planning evidence
metadata-only patch spec = not product
candidate operation = possible product input
code/patch product = reviewable product
blocked reason = valid non-product exit
```

Do not call evidence a product.

## Valid run states

### Evidence-only run

```text
runtime executed
providers/tools/validators produced evidence
no concrete operation exists
```

This is useful diagnostics, but not a final product.

### Blocked product run

```text
heap/exchange worked
exit product was evaluated
no concrete deterministic operation candidate exists
blocked reason is explicit
```

This is a valid safe exit. It must not pretend success.

### Real product run

```text
runtime evidence exists
candidate operations exist
source targets are concrete
code/patch product exists
validators pass or report explicit failure
review artifact exists
```

This is the path that can move toward commit/PR/review.

## Product requirements

A reviewable product needs:

```text
operation_count > 0
concrete_operation_count > 0
target files identified
change strategy or diff present
validation commands present
manual review status explicit
```

When source writes are expected:

```text
changed_count > 0
```

If all outputs are metadata, the product is not real.

## Failure rules

Treat these as failures or blocked states:

```text
operation_count = 0 with apply requested
patch spec contains only metadata
provider produced prose but no target operation
review PR draft exists without concrete product
validator output missing for claimed product
source-write status unclear
```

## Lane expectations

```text
GPU/provider lane -> advisory evidence or candidate reasoning
GPU0/OpenVINO lane -> observable companion/review evidence
NPU lane -> bounded micro-task/tool/device provider evidence, not primary semantic ownership
CPU/validator lane -> deterministic checks and contracts
```

A lane is not successful because it exists. It is useful when it produces structured evidence.

## Review boundary

Review artifacts must be downstream of product evidence.

```text
evidence -> candidate operation -> code/patch product -> validation -> review artifact
```

Do not create a review product from a metadata-only draft.

## Git hygiene

Do not commit runtime-heavy artifacts by default:

```text
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
```

Commit only source, tests, documentation, selected compact evidence or reviewed product artifacts.

## Related current documents

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
Tools/ai/run/TOOL_CONTEXT.md
Tools/ai/code_product/TOOL_CONTEXT.md
Tools/ai/patch_product/TOOL_CONTEXT.md
Tools/ai/patchkit/TOOL_CONTEXT.md
Tools/validation/real_product/TOOL_CONTEXT.md
Tools/validation/generated_patch_specs/TOOL_CONTEXT.md
Tools/validation/repository_product/TOOL_CONTEXT.md
```

## Historical source

```text
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```
