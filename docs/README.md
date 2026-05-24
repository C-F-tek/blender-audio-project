# Documentation Index

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists. GPU1 emits causal `FINAL_PRODUCT_DELTA` records; blocked status is runtime/gate classification, not GPU1 output.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Status

Compact repository documentation index.

This file exists because repository contracts and context-pack profiles treat `docs/README.md` as a required documentation entrypoint. It is not a replacement for the root contracts.

Canonical root entrypoints:

```text
../AGENTS.md
../CHATGPT.md
../CONTEXT_INDEX.md
```

## Core-first docs-side entrypoints

```text
AI_DOCS_ENTRYPOINT.md
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
CORE_LANE_COMPLETENESS_CONTRACT.md
HEAP_EXCHANGE_USEFUL_MODEL.md
STANDALONE_HEAP_SURFACE_MODEL.md
PROVIDER_LANES_UNIFIED_MIND_MODEL.md
REAL_PRODUCT_RUN_MODEL.md
COMPACT_EVIDENCE_MODEL.md
PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
CONTEXT_INDEX.md
CONTEXT_COVERAGE_STATUS.md
DISPATCHER_CONTEXT_COVERAGE.md
```

## Current first-read path

Read these first for active IA-Carmine runtime, provider, heap/exchange, patchkit, workflow or documentation work:

```text
../AGENTS.md
../CHATGPT.md
../CONTEXT_INDEX.md
AI_DOCS_ENTRYPOINT.md
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
CORE_LANE_COMPLETENESS_CONTRACT.md
HEAP_EXCHANGE_USEFUL_MODEL.md
STANDALONE_HEAP_SURFACE_MODEL.md
PROVIDER_LANES_UNIFIED_MIND_MODEL.md
REAL_PRODUCT_RUN_MODEL.md
COMPACT_EVIDENCE_MODEL.md
PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
CONTEXT_INDEX.md
CONTEXT_COVERAGE_STATUS.md
DISPATCHER_CONTEXT_COVERAGE.md
../Tools/CONTEXT_INDEX.md
../Scripting/CONTEXT_INDEX.md
```

Older task/runbook files remain useful only after this path and only for their specific topic.

## Universo IA active models

| Area | Document |
|---|---|
| AI limitations / anti-ambiguity contract | `AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` |
| Model-to-code bridge | `IA_UNIVERSE_MODEL_TO_CODE_MAP.md` |
| Core lane completeness contract | `CORE_LANE_COMPLETENESS_CONTRACT.md` |
| Heap/exchange useful model | `HEAP_EXCHANGE_USEFUL_MODEL.md` |
| Standalone heap surface model | `STANDALONE_HEAP_SURFACE_MODEL.md` |
| Provider lanes unified mind model | `PROVIDER_LANES_UNIFIED_MIND_MODEL.md` |
| Real product run model | `REAL_PRODUCT_RUN_MODEL.md` |
| Compact evidence model | `COMPACT_EVIDENCE_MODEL.md` |
| Patch/code product boundary model | `PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md` |
| Root context navigation | `../CONTEXT_INDEX.md` |
| Docs navigation | `CONTEXT_INDEX.md` |
| Context coverage | `CONTEXT_COVERAGE_STATUS.md` |
| Dispatcher/family coverage | `DISPATCHER_CONTEXT_COVERAGE.md` |
| Tooling index | `../Tools/CONTEXT_INDEX.md` |
| Scripting index | `../Scripting/CONTEXT_INDEX.md` |

## Core-first model-to-code use

When search is noisy or inconclusive, start from the model-to-code bridge:

```text
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

It maps each current model to:

```text
code families
dispatcher commands
expected artifacts
validation/smoke commands
semantic rule
```

Before drawing conclusions, apply the anti-ambiguity contract:

```text
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
```

Then enforce lane viability with:

```text
CORE_LANE_COMPLETENESS_CONTRACT.md
```

For complete/full profiles, `degraded` and `unavailable` are `unviable`. A full smoke must not pass without valid evidence for required core lanes.

Then open the nearest family context and dispatcher:

```text
../Tools/CONTEXT_INDEX.md
../ia_carmine/CONTEXT_INDEX.md
../Tools/validation/CONTEXT_INDEX.md
../Tools/workflow/CONTEXT_INDEX.md
../Tools/npu/CONTEXT_INDEX.md
```

## Historical/task-specific runbooks

Read these only when the current task concerns that area:

```text
LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md
LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md
```

## Provider lanes as one operational mind

Provider/lane cooperation work should first read:

```text
PROVIDER_LANES_UNIFIED_MIND_MODEL.md
CORE_LANE_COMPLETENESS_CONTRACT.md
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

This is the current model for Ollama as main center, GPU0 as coworker/reviewer lane, and NPU as micro-lane/microtask auditor, with code/tool mapping in the model-to-code map.

## Standalone heap universe incubation

Standalone heap architecture work should first read:

```text
STANDALONE_HEAP_SURFACE_MODEL.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

Then, only for historical/task detail:

```text
LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md
LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md
```

## Real product run classification

Run/product classification should first read:

```text
REAL_PRODUCT_RUN_MODEL.md
CORE_LANE_COMPLETENESS_CONTRACT.md
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

Then, only for historical/task detail:

```text
LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```

## Compact evidence selection

Evidence publication decisions should first read:

```text
COMPACT_EVIDENCE_MODEL.md
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

Then inspect selected compact evidence under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Do not commit raw runtime output by default.

## Patch/code product boundary

Source-change product decisions should first read:

```text
PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

This separates provider proposal, patch plan, patch candidate, code product, PatchKit bundle, repo-patch-runner and reviewed apply.

## Other active architecture and workflow docs

| Area | Document |
|---|---|
| AI workload quality gate | `AI_WORKLOAD_REPORT_QUALITY_GATE.md` |
| Local AI core tool activation | `LOCAL_AI_CORE_TOOL_ACTIVATION.md` |
| Runtime architecture | `MAIN_RUNTIME_ARCHITECTURE.md` |
| Unified launcher contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md` |
| Local AI workflow | `LOCAL_AI_WORKFLOW.md` |
| Data flow | `DATA_FLOW.md` |
| JSON/report schemas | `JSON_SCHEMAS.md` |
| Patch-spec workflow | `PATCH_SPEC_WORKFLOW.md` |
| Project status | `PROJECT_STATUS_POINT.md` |
| AI task map | `AI_DOCS_ENTRYPOINT.md` and current files under `LOCAL_AI_TASKS/` |
| Tool package family map | `LOCAL_AI_TASKS/tool-package-family-map-2026-05-18.md` |

## Policy

Do not add competing first-read orders here. Keep this file as a compact index and route detailed instructions to active context, coverage, task or runbook documents.
