# Provider lanes unified mind model

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
| GPU0 / coworker lane | Ollama/Vulkan companion reviewer, discrepancy check, peer visibility | peer reports, review evidence, workload proof, contradiction notes |
| NPU / micro-lane | OpenVINO microtask/tool/device provider, small checks, support evidence | micro reports, device/tool-loop facts, audit notes, guardrail hints |
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

CPU is not a provider department. CPU may run scripts, broker/tool dispatch,
parsers, I/O, orchestration and validators, but complete provider evidence must
come from accelerator lanes only: Ollama proved GPU residency by `ollama ps`,
Ollama/Vulkan for GPU0, and OpenVINO `NPU` for NPU. OpenVINO `CPU`,
OpenVINO GPU0 fallback, heuristic fallback, CPU-only Ollama residency or unproven residency are
diagnostic evidence and must block complete run-unica provider success.

GPU1/Ollama should request full model-layer GPU offload with
`--ollama-gpu-layers all` in the canonical run. This is not a count of GPU
cards; it is the Ollama layer-offload control and maps to `options.num_gpu=-1`
only at the API edge. If `ollama ps` reports a split such as `36%/64% CPU/GPU`,
the model is partly resident in system memory. In a complete/run-unica profile,
GPU1 is viable only when the selected model is proven as `100% GPU`. A split
`CPU/GPU`, CPU-only residency or unproven residency blocks GPU1; non-strict
runtime may repair by selecting a smaller installed model that fits in VRAM.

`100% GPU` is residency evidence only. A provider role is counted only when the
lane reports `provider_work_verified=true`: device detected, model loaded,
health check passed, workload performed, useful output produced and no blocking
operator observation. For GPU1 this includes runtime GPU samples during the
inference window; for GPU0 it includes Ollama/Vulkan provider output;
for NPU it includes bounded OpenVINO `NPU` micro-provider output. Diagnostics,
tensor-only workloads, preflight checks and replight handshakes do not create
product roles.

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

Time is part of that shared operational picture. A run budget is a counter used
to choose GPU1 cycles and request a coordinated soft close near the end. GPU0
and NPU are bounded sidecars with watchdog/timeouts; a selected lane that fails
to start is a hard universe stop, but NPU must not keep the run open as primary
semantic closer.

Provider revision count is evidence, not a recursion limit. The loop may use it as evidence that revisions happened, but must not stop GPU1 because the count reached an effective maximum.

## Single Run, Not Single Direction

`Corsa unica` means one continuous heap universe, not one script line, one cycle or one-way movement.

GPU1 may move on the pointer graph:

```text
current block
-> backtrack to previous/refines block
-> propagate imports, variables, classes, schema fields, CLI flags and contracts
-> ask GPU0/NPU to re-check impacted pointer records in parallel
-> resume forward from resume_from_block_id
-> compose/refine the final code product from linked blocks
```

The final code product must be reconstructed from pointer continuity fields such as `previous_block_id`, `refines_block_id` and `resume_from_block_id`. Linked provider pointer records remain evidence until the pointer graph and deterministic product boundary can compose them.

## Department responsibilities

### Ollama / main provider

Ollama is the central planner, review opener, tool-calling coordinator and
closure/synthesis lane.

It should:

```text
read request/context/evidence
propose candidate operations
explain reasoning at product level
consume reviewer/auditor feedback
revise proposals when evidence rejects them
produce structured recommendation evidence
emit the final synthesis, blocked continuation or blocked reason
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
propose backtrack/refine/resume signals without becoming primary closer
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
finish through bounded timeout/watchdog and never become primary closer
```

NPU must not be documented or reported as the primary semantic provider. It is a
real bounded micro-provider when selected, but it remains support/micro and does
not own final product synthesis. NPU reports must use `npu_micro_provider_*`
fields, not `semantic_provider_*` or `npu_semantic_*` fields.

GPU0 native model/tool-loop timeout is provider failure in complete run-unica
provider mode. NPU has two levels: `npu_peer_evidence_verified=true` is valid
peer/audit evidence when the NPU device workload ran, the micro-audit ran and
the response schema is valid; an OpenVINO GenAI/native tool-loop timeout remains
`npu_native_tool_loop_error` runtime feedback and blocks only required native
tool-loop work. Tensor workload, device visibility or NPU preflight alone remain
diagnostic evidence.

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
provider backend
provider compute device
provider device verified
CPU fallback not used as provider
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
ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md
ia_carmine/runtime/provider_runtime_blackboard/TOOL_CONTEXT.md
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
