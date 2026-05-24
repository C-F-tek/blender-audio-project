# Real product run model

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product; `PLAN_PRODUCT_FULL_PATCH.md` is the final recomposed GPU1 prompt/chat product, with pointer graph and recovery/congruence as technical attachments.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


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
continuation pointer or resume context is explicit when available
```

This is a valid safe exit. It must not pretend success.

### Blocked continuation product

```text
provider/pointer evidence exists
the universe has not reached an approved concrete product
resume_from_block_id or blocker reason is published
public Documents package is written
```

This is the canonical output when GPU1 is blocked, the budget soft-closes or
the provider graph needs another turn. It is not a code product and must not be
applied as a patch.

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
GPU0/Ollama Vulkan lane -> observable companion/review evidence
NPU/OpenVINO lane -> bounded micro-task/tool/device provider evidence, not primary semantic ownership
CPU/validator lane -> deterministic checks and contracts
```

A lane is not successful because it exists. It is useful when it produces structured evidence.

GPU1/Ollama is the closure owner. Full runs use `--provider-model auto` unless
the operator selects `--strict-provider-model`. With `--ollama-gpu-layers all`,
`ollama ps` must prove `100% GPU`; mixed `CPU/GPU`, CPU-only or unproven
residency pointer records GPU1. GPU0/Ollama Vulkan and NPU/OpenVINO are sidecar evidence lanes, but each must
produce real model/device output when selected; diagnostic tensor/preflight
evidence alone is not a real product provider lane.

Provider role truth is `provider_work_verified=true`, not device visibility,
model loading, diagnostics or short handshakes. If provider work is rejected, the
run exits as blocked with the lane reasons, for example
`gpu1_no_verified_workload`, `gpu0_ollama_vulkan_no_verified_workload` or
`npu_micro_provider_not_loaded`, instead of a generic soft-governor or
no-applicable-code-product status.

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
ia_carmine/runtime/run/TOOL_CONTEXT.md
ia_carmine/product/code_product/TOOL_CONTEXT.md
ia_carmine/product/patch_product/TOOL_CONTEXT.md
ia_carmine/product/patchkit/TOOL_CONTEXT.md
Tools/validation/real_product/TOOL_CONTEXT.md
Tools/validation/generated_patch_specs/TOOL_CONTEXT.md
Tools/validation/repository_product/TOOL_CONTEXT.md
```

## Historical source

```text
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```
