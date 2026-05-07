# 04 — Implementation plan

## Target patch family

The next architecture patch family can combine these report-only foundations:

```text
GPU0/NPU hardware capability manifest report-only
+ SQLite heap memory schema/policy
+ NPU tool-proxy schema docs + validator
+ broker delegation contract
```

This is one coherent foundation because all four parts define how local hardware and memory become controlled tools instead of hidden side channels.

## Phase 1 — Documentation and schemas only

Add or update:

```text
docs/LOCAL_AI_TASKS/NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05.md
docs/AI_ARTIFACT_SCHEMAS.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-registry.md
docs/TECH_DEBT_TRACKER.md
```

Define:

```text
NPU tool-proxy request schema
NPU tool-proxy response schema
GPU0 worker request/response schema
hardware capability manifest fields
broker delegated-call telemetry fields
SQLite heap memory schema and persistence policy
```

No runtime behavior yet.

## Phase 2 — Report-only hardware capability manifest

Add a tool that detects and reports local hardware capability without running heavy inference:

```text
Tools/ai/build_runtime_hardware_capability_manifest.py
```

Expected output:

```text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_hardware_capability_manifest_<STAMP>.md
```

Required behavior:

```text
query OpenVINO devices when available
record CPU/GPU.0/NPU visibility
record Ollama/NVIDIA GPU advisory lane separately
no source writes
no patch application
no persistent memory writes
no Blender/FFmpeg/media runtime
```

## Phase 3 — Validator for hardware manifest

Add:

```text
future runtime hardware capability manifest validator
```

Validate:

```text
schema_version
kind
repo_root
generated_at
devices
resource ids
role labels
source_writes_performed=false
patch_application_performed=false
persistent_memory_write_performed=false
errors/warnings shape
```

## Phase 4 — SQLite heap schema/policy module

Add or extend:

```text
future memory schema module after smoke-backed implementation
future memory tool CLI module after smoke-backed implementation
```

First scope:

```text
init scratch DB
create tables
memory_add_text scratch only
memory_search fts_only
memory_export_manifest
```

Defer embeddings until schema and FTS are stable.

## Phase 5 — Broker allowlist and telemetry extension

Extend broker/capability docs first, then code:

```text
memory_search
memory_add_text scratch
memory_add_file scratch with denylist
hardware_capability_manifest
```

Add telemetry counters:

```text
memory_tool_call_count
hardware_capability_report_seen
delegated_call_count
blocked_delegated_call_count
```

## Phase 6 — Simulated NPU proxy

Before real NPU execution, add CPU-only simulated NPU proxy report:

```text
Tools/ai/simulate_npu_tool_proxy.py
```

Use same request/response schemas as future NPU proxy.

Allowed task:

```text
classify_finding
```

No provider execution.

## Phase 7 — Real NPU proxy one-task pilot

Only after phases 1-6 validate locally:

```text
Tools/ai/run_npu_tool_proxy.py
```

First real task:

```text
classify_finding
```

Hard limits:

```text
small prompt
small output
strict JSON
short timeout
no source write
no patch apply
no persistent memory unless explicitly enabled
```

## Phase 8 — GPU0 coworker probe

Start with report-only detection/probe:

```text
GPU0 availability
OpenVINO compatibility
small model availability if already present
no inference unless explicitly scoped
```

Then later:

```text
small embedding probe
small classification probe
batch similarity probe
```

## Phase 9 — Run-unica integration

Only after focused validators pass:

```text
add hardware capability manifest to Full0To10 perimeter
add memory tools to capability manifest
add NPU proxy/GPU0 coworker as disabled-by-default or report-only lanes
add telemetry summary fields
add shared AI-to-AI bundle fields
```

## Phase 10 — Evidence and bundle policy

Every serious run should carry:

```text
runtime_hardware_capability_manifest_<STAMP>.json/md
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
memory manifest summary when memory tools run
hardware delegation summary when helper/coworker calls run
```

## First safe patch recommendation

The safest first implementation patch is:

```text
build_runtime_hardware_capability_manifest.py
check_runtime_hardware_capability_manifest.py
docs updates to reference report-only GPU0/NPU hardware capability
no real NPU/GPU0 delegated work yet
```

This lets the project observe hardware safely before routing tasks to it.
