# AI Tools

`Tools/ai/` contains report-oriented tools for IA-Carmine local AI orchestration, context building, provider diagnostics, deterministic recommendations, telemetry, evidence, final tool-product packaging and AI-to-AI handoff.

This README is a technical catalog. It is not the primary command source.

Broad local-AI execution starts from:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Current doctrine

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
provider/probe/workload-quality lanes are opt-out in Full0To10
GPU1/GPU0 peer exchange is production evidence, not smoke-only proof
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
400-line policy applies to maintained docs and source files
limitations are backlog to overcome, not reasons to skip available tools
patch application is explicit and separate
tool output should become verifiable product/evidence/readiness material, not chat-only summary
```

## Package map

| Area | Role |
|---|---|
| `pipeline/` | Modular AI artifact pipeline implementation behind `run_parallel_artifact_pipeline.py`. |
| `full0to10_final_product/` | Final tool-product package builder: product Markdown, evidence index, readiness, manifest and README. |
| `full0to10_hardware_capability/` | Full0To10 hardware/capability visibility package. |
| `full_run_bundle_zip/` | Full-run evidence ZIP support in candidate foundation work. |
| `runtime_hardware_capability/` | Runtime hardware capability support in candidate foundation work. |

## Core tool groups

| Tool family | Examples | Notes |
|---|---|---|
| Context and chunks | `build_ai_context_pack.py`, `select_semantic_code_chunks.py` | Provider-free context evidence. |
| Agent state and memory | `build_agent_state_packet.py`, `review_agent_memory.py`, `agent_runtime_sqlite_memory.py` | SQLite outputs are local/private and must not be committed. |
| Provider diagnostics | `run_local_provider_probe.py`, `check_local_resource_lanes.py`, `analyze_gpu_npu_run_sync.py` | Provider state must flow to telemetry/bundle when used in Full0To10 handoff. |
| AI peer exchange | `build_ai_peer_exchange_packet.py`, `run_gpu0_peer_companion_worker.py`, `run_npu_gpu_deep_review_auditor.py` | Wires GPU1 master advisory/worker output to GPU0 companion response, GPU0/NPU broker requests and peer contract evidence. |
| Workload routing | `build_workload_quality_lane_routing.py` | Keeps unusable provider output out of advisory context. |
| Deterministic recommendations | `build_deterministic_recommendations.py` | Supports degraded-provider recovery without hallucinated provider success. |
| Patch planning/spec support | `build_agent_review_patch_plan.py`, `build_patch_specs_from_proposals.py`, `promote_patch_spec_draft.py` | Review-only unless explicit apply is authorized separately. |
| Patch notes product | `build_patch_notes_quality_product.py`, `patch_notes_quality_product/*` | Converts a local Markdown task plus patch-plan/telemetry/evidence inputs into manual-review patch notes quality JSON/MD with structured success/fallback cases. |
| Runtime broker/telemetry | `agent_runtime_tool_broker.py`, `build_runtime_tool_usage_telemetry.py` | Records executed/failed/blocked tool calls with broker-measured elapsed time and normalized status. |
| Capability and telemetry summary | capability manifest packages/builders, `build_full_toolbox_run_telemetry_summary.py` | Handoff context for available tools/hardware lanes and run state. |
| Final tool product | `build_full0to10_final_tool_product.py`, `full0to10_final_product/*` | Aggregates contract/governor/invocation/bridge/effective-use/quality evidence into product/evidence/readiness outputs and can index current-run reports/artifacts. |
| Production bundle | `build_shared_toolbox_ai_to_ai_bundle.py` | AI-to-AI evidence/telemetry/patch-plan handoff. |
| Evidence bundles | `build_github_evidence_bundle.py`, full-run bundle ZIP tools | Compact GitHub evidence only; raw `output/**` stays ignored. |

## Final product behavior

The Full0To10 final-product builder currently composes these internal evidence families:

```text
track input contract
accelerator control
provider governor
provider invocation plan
provider execution bridge
effective-use optimization summary
quality gate
```

It writes a product Markdown, evidence index, readiness JSON, manifest and README. The builder accepts `--run-report` and `--run-artifact` inputs so production workflows can attach the current stamp's mesh, telemetry, broker and patch-plan evidence to the final product. This supports the project idea that the toolbox should produce inspectable tool products with readiness/evidence, not only advisory prose.

## Full-run handoff rule

A recommendation, patch plan or patch spec produced from run-unica evidence is incomplete unless the handoff includes:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when relevant
```

File existence alone is not proof of successful execution.

## Device strategy

```text
CPU: parsing, JSON generation, validation, orchestration.
GPU1/Ollama/RTX 5080: mandatory primary advisory planner/worker when Full0To10 provider execution is selected.
GPU0/OpenVINO: companion peer worker and controlled tool-request producer for GPU1 follow-up.
NPU/OpenVINO: orchestrator-called micro-fast task assistant, guardrail and lightweight tool-support lane.
Deterministic scripts: heavy audit and validation authority.
External GPU commands: explicit heavy generator path only, never implicit.
```

Full0To10 provider mesh runs use startup and close barriers: GPU1, GPU0, NPU and deterministic/broker bootstrap are armed at the beginning, then the orchestrator harvests or terminates active peer-support lanes before telemetry/bundle finalization. The NPU micro lane reports provider text evidence separately from brokered tool-support evidence, so a slow/empty NPU response can still be useful when it emits valid brokered tool requests. Runtime heap telemetry must close broker request/result correlation ids before the compact bundle is considered clean. The legacy NPU auditor provider is diagnostics-only behind `-RunLegacyNpuAuditorProvider`.

## Safety policy

Tools in this folder should remain report-only or explicit-run by default.

They must not silently:

```text
apply patches
queue patch specs
edit Blender runtime files
edit full analysis JSON files
commit output/**
commit SQLite DB files
execute providers outside selected provider/full-run lanes
run Blender, FFmpeg, audio playback or media generation
```

## 400-line policy

Maintained tools and docs must stay under 400 lines.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Related docs

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/DATA_FLOW.md
docs/MODULE_MAP.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```
