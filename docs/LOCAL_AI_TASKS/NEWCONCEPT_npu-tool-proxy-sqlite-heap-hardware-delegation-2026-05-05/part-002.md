<!-- IA-CARMINE-MD-SPLIT: part -->
# NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05 — parte 002 di 002

Sorgente indice: [`../NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05.md`](../NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Evidence push policy

Compact evidence should be pushed after every serious run, but raw generated output must not be pushed.

Always promote/push, when produced and reviewed:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json/md
compact inventory/discovery/index/CSV evidence selected for review
```

Never push as ordinary source:

```text
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
*.sqlite3
renders/**
raw audio/video/media output
```

The complete ZIP bundle should be uploaded or attached for chat/master-AI review. The ZIP is a runtime artifact, not normal source.

## Required new contracts before implementation

Before moving NPU/GPU0 into tool-proxy or coworker operation, add or validate these contracts:

```text
NPU tool-proxy request schema
NPU tool-proxy response schema
NPU helper timeout/degradation policy
GPU0 worker request schema
GPU0 worker response schema
GPU0 task allowlist
SQLite heap memory read/write policy for lane outputs
runtime broker delegation policy
runtime capability manifest extension for local hardware lanes
telemetry fields for delegated hardware tasks
full toolbox telemetry summary fields for NPU/GPU0 helper calls
shared AI-to-AI bundle fields for delegated task summaries
validator for NPU tool-proxy reports
validator for GPU0 worker reports
```

## Recommended implementation sequence

1. Keep current NPU diagnostic posture during the active run.
2. Add report-only schema docs and validators for NPU tool-proxy requests/responses.
3. Add report-only schema docs and validators for GPU0 worker requests/responses.
4. Extend capability manifest to describe NPU helper and GPU0 coworker as callable bounded tools, not advisory providers.
5. Extend runtime telemetry to count delegated helper/coworker calls.
6. Extend SQLite memory policy for multi-lane heap entries.
7. Add one safe simulated helper task: lightweight classification or calculation.
8. Validate with CPU-only simulated proxy first.
9. Add real NPU helper for one task family only.
10. Add GPU0 report-only probe/capability lane.
11. Only then allow primary AI lanes to delegate bounded helper tasks.

## Non-goals for the first implementation

```text
no autonomous NPU agent
no autonomous GPU0 agent
no unbounded repository review by helper lanes
no source writes
no patch application
no Git operations
no secret/network access
no Blender/FFmpeg/media runtime
no automatic generated-index mutation
```

## Success criteria

A successful future implementation proves:

```text
NPU helper call appears in runtime telemetry
NPU helper capability appears in runtime capability manifest
GPU0 availability/capability appears in runtime capability manifest
GPU0 worker call appears in telemetry only after worker schema exists
helper output is bounded and schema-valid
SQLite heap memory write, if enabled, is typed and policy-validated
provider/tool degradation is visible
source_writes_performed=false
patch_application_performed=false
raw SQLite DB is not committed
compact evidence is available for review
bundle ZIP contains helper/delegation summary
```

## Decision summary

The architecture direction is accepted as a future staged evolution with this interpretation:

```text
NPU = bounded delegated tool worker, not primary advisory
GPU0 = possible OpenVINO coworker after capability/report contracts
SQLite = shared heap memory with typed facts and strict policy
CSV/index/discovery = start-of-run factual base and compact evidence
runtime broker = required control plane for all delegated hardware calls
```
