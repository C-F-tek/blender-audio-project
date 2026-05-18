# Documentation Index

## Status

Compact repository documentation index.

This file exists because repository contracts and context-pack profiles treat
`docs/README.md` as a required documentation entrypoint. It is not a replacement
for the root contract.

Canonical root contract:

```text
../AGENTS.md
```

Current docs-side entrypoint:

```text
AI_DOCS_ENTRYPOINT.md
```

## Current first-read path

Read these first for active IA-Carmine runtime, provider, heap/exchange and
patchkit work:

```text
../AGENTS.md
../CHATGPT.md
../CHATGPT/README.md
README.md
AI_DOCS_ENTRYPOINT.md
LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Active architecture and workflow docs

| Area | Document |
|---|---|
| Runtime architecture | `MAIN_RUNTIME_ARCHITECTURE.md` |
| Unified launcher contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md` |
| Local AI workflow | `LOCAL_AI_WORKFLOW.md` |
| Data flow | `DATA_FLOW.md` |
| JSON/report schemas | `JSON_SCHEMAS.md` |
| Patch-spec workflow | `PATCH_SPEC_WORKFLOW.md` |
| Project status | `PROJECT_STATUS_POINT.md` |
| AI task map | `LOCAL_AI_TASKS/README.md` |
| Tooling index | `../Tools/ai/README.md`, `../Tools/workflow/README.md`, `../Tools/validation/README.md` |
| Tool package family map | `LOCAL_AI_TASKS/tool-package-family-map-2026-05-18.md` |

## Policy

Do not add competing first-read orders here. Keep this file as a compact index
and route detailed instructions to the active task/runbook documents.

## Standalone heap universe incubation

New local-AI architecture work should also read:

```text
LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md
```

This document describes the standalone heap function that is currently separate from the full run-unica path. It is used to harden strict input, context/memory preload, SQLite/FTS5/chunk memory surfaces, GPU1/GPU0/NPU same-heap cooperation, in-heap refinement and composed output before promotion into the full product run.

## Standalone heap tool surface

For the new standalone heap function, read both:

```text
LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md
LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md
```

The second document maps SQLite/FTS5, chunk memory, context namespace, tool catalog, broker outputs, provider lanes and validator evidence as heap-owned surfaces.
