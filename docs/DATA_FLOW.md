# Data Flow

## Purpose

This document describes the current data movement across `IA-Carmine Local AI Orchestration Workbench`.

The project still contains Blender/audio-reactive workflows, but the active architectural flow is now app-agnostic local AI orchestration: run-unica parameters, reports, provider lanes, quality gates, probes, advisory packets, runtime broker telemetry, capability manifests, discovery/index/CSV/file-line-limit evidence and compact GitHub evidence.

## Current core AI orchestration flow

```text
unified launcher command
  -> run unica parameters / Full0To10 perimeter / explicit -No* opt-outs
  -> unified_local_ai_refactor_manifest.json
  -> local source/docs/context
  -> Markdown and script inventories
  -> CSV/count evidence surfaces
  -> file-line-limit evidence surface
  -> auto-discovery and index-drift reports when relevant
  -> semantic code chunks and selected focused chunks when useful
  -> task-scoped AI context pack when useful
  -> SQLite-backed agent state packet when enabled
  -> validation reports
  -> workload report quality gate for Full0To10/provider lanes
  -> advisory lane routing
  -> trusted/excluded context selection
  -> provider probes and primary advisory generation unless disabled or diagnosed unavailable
  -> provider bridge/gate/readiness planning when selected
  -> effective-use local memory/product surfaces when selected
  -> post-validation AI packet and proposals
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs
  -> explicit replacement plan and reviewed dry-run spec
  -> runtime broker report
  -> runtime tool usage telemetry
  -> runtime/hardware capability manifest
  -> final tool-product evidence/readiness package when selected
  -> full toolbox run telemetry summary
  -> compact evidence bundle under docs/LOCAL_VALIDATION_EVIDENCE/
  -> shared production AI-to-AI bundle
  -> manual review / PR / merge
```

Primary operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

The manifest is the first review object. Telemetry and capability manifests are the next AI reasoning surfaces. Detailed reports are opened only after manifest and telemetry show which phases produced them.

## Run unica / TUTTO SU TUTTO data-flow rule

The primary model is one parameterized run:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
LightFull0To10 = evidence-only profile, not provider/runtime proof
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
400-line policy applies to maintained docs and source files
limitations are backlog to overcome, not reasons to skip available tools
```

`-Full0To10` data flow is **TUTTO SU TUTTO**.

Every intensity preset must preserve the same semantic data surfaces. `quick`, `balanced`, `deep` and `custom` may change volume, context size, token limits and runtime budget, but they must not silently remove core data flows.

The full-run perimeter can expand. When a new production-ready data surface appears, such as a registry, broker tool report, provider diagnostic, repository-consistency map, memory/context builder, discovery/index report, CSV/count surface, file-line-limit report or telemetry summary, it must be added to this document and to the launcher contract, or explicitly excluded with rationale.

## Discovery, index and CSV/count flow

Discovery and count surfaces are data-flow evidence, not source authority.

```text
Markdown inventory
  -> docs lifecycle, obsolete/redundant docs, missing index review

script inventory
  -> tool/function/class/method visibility
  -> JSON/CSV/MD outputs

Python line-count CSV/MD
  -> sizing evidence
  -> refactor planning
  -> PR/report line-count support

file-line-limit JSON/MD
  -> 400-line policy evidence
  -> docs/source maintainability debt
  -> split/refactor planning

function/class/method CSV
  -> duplication and helper-reuse triage
  -> superclass/base-class opportunity review

auto-discovery/index repair report
  -> scanner/index visibility drift detection
  -> repair plan/report before any regeneration
```

Policy:

```text
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Do not hand-edit generated indexes or chunks as source.
Index repair is plan/report-first unless explicitly requested.
CSV/count/file-line-limit surfaces support review and sizing; they do not override source code or canonical docs.
```

## Provider-lane flow

```text
Ollama/GPU workload report
  -> quality gate: usable_text
  -> advisory lane: ollama
  -> provider mapping: GPU/CUDA
  -> primary advisory packet generation for Full0To10 unless disabled/unavailable
  -> provider diagnostics and degradation state in telemetry/bundle
```

```text
NPU/OpenVINO workload report
  -> quality gate: unusable_output for old real workload report
  -> excluded from advisory context
  -> remediation report
  -> NPU probe / decode smoke diagnostic for Full0To10 unless disabled/unavailable
  -> possible future promotion only after quality-gated usable workload output
  -> provider diagnostics and exclusion reason in telemetry/bundle
```

Current mapping:

```text
Ollama -> GPU/CUDA
OpenVINO -> NPU
OpenVINO GPU.0/GPU.1 -> visibility/diagnostic lanes, not primary advisory lanes
```

Provider execution is explicit when the operator selects `-Full0To10` or provider/probe modes. It is not an extra per-lane opt-in after `-Full0To10` is selected.

## Provider bridge and capability flow

Current provider bridge/capability outputs distinguish availability, planning and real execution.

```text
Full0To10 hardware/tool capability manifest
  -> required tool inventory
  -> Python environment visibility
  -> GPU/Ollama/NPU/OpenVINO device visibility/probes
  -> provider_execution_performed=false
  -> patch_application_performed=false
  -> source_writes_performed=false
```

```text
Full0To10 provider execution bridge
  -> provider invocation plan
  -> real-run gate
  -> command plan
  -> workload output paths
  -> bridge telemetry
  -> readiness report
  -> provider_execution_performed=false
  -> patch_application_performed=false
  -> source_writes_performed=false
```

These surfaces are critical because they let later agents see whether a tool/provider was available, planned, gated, skipped or actually executed. Do not treat bridge/readiness/capability evidence as provider runtime proof unless the artifact itself records provider execution.

## Effective-use memory/product flow

Current code includes an effective-use lane:

```text
Tools/ai/full0to10_effective_use/*
Tools/ai/full0to10_sqlite_memory/*
```

It builds:

```text
provider hardening contracts
effective-use optimization JSON
tool telemetry JSON
quality product Markdown
SQLite FTS5 memory DB under output/ai_runtime_memory/
```

The SQLite memory code creates the DB directory, opens SQLite, enables WAL/foreign keys, initializes schema, inserts memory items/chunks/FTS rows and commits. This is a real local output DB write, but it is not a source write and must not be committed.

Current semantic caveat:

```text
summary safety flags may still say persistent_memory_write_performed=false
```

Treat that flag as incomplete for local output DB writes until TD-029 is resolved. Preserve the stronger operational rule:

```text
output/** SQLite artifacts are local/private and non-commit-ready.
source_writes_performed=false means source files were not modified.
```

## Runtime telemetry flow

```text
runtime broker requests
  -> Tools/ai/agent_runtime_tool_broker.py
  -> runtime_tool_broker_full_toolbox_<STAMP>.json/md
  -> Tools/ai/build_runtime_tool_usage_telemetry.py
  -> runtime_tool_usage_telemetry_<STAMP>.json/md
  -> runtime/hardware capability manifest builder for the active lane
  -> runtime_tool_capability_manifest_<STAMP>.json/md or runtime_hardware_capability_manifest_<STAMP>.json/md
  -> Tools/ai/build_full_toolbox_run_telemetry_summary.py
  -> full_toolbox_run_telemetry_summary_<STAMP>.json/md
  -> Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
  -> shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
  -> shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

Current code note:

```text
Older docs may mention Tools/ai/build_runtime_tool_capability_manifest.py.
Current code includes the Full0To10 hardware/capability package and PR #192 adds Tools/ai/build_runtime_hardware_capability_manifest.py.
Treat capability-manifest names through current code/evidence, not historical filename assumptions.
```

Telemetry answers AI-critical questions:

```text
which tools were available
which tools executed
which tools failed
which tools were blocked
which provider lanes degraded
which discovery/index/count/file-line-limit surfaces were present, skipped or degraded
which reports were absorbed into the bundle
which source writes or patch applications did not happen
```

Important fields:

```text
tool_call_entry_count
executed_count
failed_count
blocked_count
broker_reports
provider_advisory_state
provider_failure_reasons
degraded_provider_components
gpu_metrics_source
round_duration_source
patch_application_performed
source_writes_performed
```

AI agents must not infer run success from output file presence alone.

## Final tool-product flow

Current code includes a Full0To10 final-product builder:

```text
Tools/ai/build_full0to10_final_tool_product.py
Tools/ai/full0to10_final_product/*
```

It composes track input contract, accelerator control, provider governor, provider invocation plan, provider execution bridge, effective-use optimization summary and quality gate.

It writes:

```text
product Markdown
evidence index
readiness JSON
manifest JSON
README
```

This is the intended direction of the project: tools should produce verifiable product/evidence/readiness packages, not only chat summaries.

## Parallel multistep workflow flow

`Tools/workflow/run_parallel_ai_provider_multistep.ps1` is a supporting provider lane. It is normally selected through the unified launcher or called directly only for explicit provider diagnostics.

It coordinates:

```text
Step 1: workload quality gate
Step 2: parallel provider probes / NPU decode smoke
Step 3: quality-based routing and NPU remediation
Step 4: primary advisory packet/proposals
Step 5: GitHub evidence bundle
```

Primary evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
```

Validated decisions from that evidence:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

## Main data categories

| Data | Producer | Consumer | Notes |
|---|---|---|---|
| Unified manifest | `Tools/workflow/run_unified_local_ai_refactor.ps1` | human/AI review | First review object for run-unica parameters, phase status, reports, context, providers and guardrails. |
| Source/docs context | repository files | inventories, context packs, advisory packet builder | Non-workload files are trusted unless normal file read fails. |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | docs cleanup, pruning, link review | Generated under `output/**`; do not commit unless compact evidence is intentionally built. |
| Script inventory | `Tools/validation/build_script_inventory.py` | tool/function visibility, refactor review | JSON/CSV/Markdown inventory under `output/**`. |
| Python line-count CSV/MD | validation/broker inventory lanes | PR review, refactor sizing, line-count reporting | Evidence surface; not source authority. |
| File line-limit JSON/MD | `Tools/validation/check_file_line_limits.py` | docs/code maintainability review, split/refactor planning | Report-only 400-line policy evidence; no rewrite or delete. |
| Function/class/method CSV | script inventory lanes | duplication, helper reuse and base-class opportunity review | Evidence surface for refactor/reuse planning. |
| Auto-discovery/index repair report | scanner/index validators and repair planners | local AI agents, maintainers | Plan/report-first when index drift is suspected; generated indexes remain non-source. |
| Semantic code chunks | `Tools/npu/build_semantic_code_chunks.py` | selected chunk builder, local AI task adapter | Generated context under index/output paths; do not hand-edit. |
| Selected semantic chunks | `Tools/ai/select_semantic_code_chunks.py` | context pack builder, local AI task adapter, provider packets | Bounded focused context under ignored `output/ai_context_packs/`; validator can emit compact tracked evidence. |
| AI context pack | `Tools/ai/build_ai_context_pack.py` | human/AI task planning, proposal builders | Bounded task-scoped context under ignored `output/ai_context_packs/` plus compact tracked evidence. |
| Agent state packet | `Tools/ai/build_agent_state_packet.py` | local AI task adapter, advisory packet builder | Can use SQLite memory locally; generated SQLite DB files stay untracked. |
| Effective-use SQLite memory | `Tools/ai/full0to10_effective_use/*`, `Tools/ai/full0to10_sqlite_memory/*` | effective-use quality product, local memory/search evidence | Writes SQLite FTS5 DB under `output/ai_runtime_memory/`; local/private output artifact, not source and not commit-ready. |
| Workload reports | local provider workload scripts | quality gate | Generated text reports from provider lanes. |
| Workload quality report | `Tools/validation/check_ai_workload_report_quality.py` | lane routing, remediation, packet builder | Determines `usable_lanes` and `unusable_lanes`. |
| Lane routing report | `Tools/ai/build_workload_quality_lane_routing.py` | packet builder, evidence bundle | Declares trusted/excluded context and primary advisory provider. |
| Provider diagnostics | provider/probe tools and sync analyzers | telemetry summary, bundle, AI agents | Must expose advisory state, failure reasons, degraded components and GPU/NPU timing source. |
| Provider bridge/readiness report | `Tools/ai/full0to10_provider_execution_bridge/*` | maintainers, telemetry, bundle, future provider runners | Builds invocation/gate/command/workload/telemetry/readiness surfaces; not real provider execution proof by itself. |
| Hardware/tool capability manifest | `Tools/ai/full0to10_hardware_capability/*` or current runtime hardware capability builder | AI agents, bundle, cloud handoff | Captures tool inventory and CPU/GPU/Ollama/OpenVINO/NPU visibility; not source writes or patch application. |
| Final tool-product package | `Tools/ai/build_full0to10_final_tool_product.py` | maintainers, AI agents, readiness review | Product/evidence/readiness package that composes Full0To10 contract/governor/bridge/effective-use/quality surfaces. |
| NPU remediation report | `Tools/validation/check_npu_decode_quality_remediation.py` | maintainer, proposals, evidence | Explains why NPU is excluded and what must happen before promotion. |
| NPU decode smoke report | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | evidence bundle and future promotion gates | Full0To10 diagnostic unless disabled/unavailable; does not imply NPU general advisory quality. |
| Local provider probe report | `Tools/ai/run_local_provider_probe.py` | evidence bundle | Full0To10/provider probe evidence unless disabled/unavailable. |
| Runtime broker report | `Tools/ai/agent_runtime_tool_broker.py` | runtime telemetry, full toolbox bundle | Shows broker-requested tool calls and guardrail outcomes. |
| Runtime tool usage telemetry | `Tools/ai/build_runtime_tool_usage_telemetry.py` | AI agents, telemetry summary, bundle | Counts executed/failed/blocked broker calls and carries broker report inputs. |
| Runtime/hardware capability manifest | current capability manifest builder for active lane | AI agents, bundle, cloud handoff | Describes available tools/hardware lanes, allowed args and execution guardrails. |
| Full toolbox run telemetry summary | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | AI agents, bundle, PR review | Cross-run summary of provider, GPU/NPU, broker, patch-plan and guardrail state. |
| Shared AI-to-AI bundle | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | next local/cloud AI, PR review | Production handoff surface; must carry diagnostics, telemetry, capability, discovery/count and patch-plan summary. |
| Post-validation AI packet | `Tools/ai/suggest_repository_updates.py` | maintainer / proposal builder | Uses quality-approved advisory context only. |
| Repository change proposals | `Tools/ai/build_repository_change_proposals.py` | maintainer, future trusted patch builders | Advisory only; no auto-apply. Includes `suggestion_outputs` descriptors for code/MD/JSON/PowerShell targets. |
| Full-context golden proposals | `Tools/ai/build_full_context_golden_proposals.py` | maintainer, validators, future patch-spec promotion | Deterministic P1-P6 proposal families; manual-review-only and no source mutation. |
| Proposal patch-spec drafts | `Tools/ai/build_patch_specs_from_proposals.py` | maintainer, trusted patch builders | Inert draft specs under `output/patch_specs/`; no replacements, no queue writes, no auto-apply. |
| Reviewed patch specs | `Tools/ai/promote_patch_spec_draft.py` | maintainer, trusted patch builders | Concrete replacements plus mandatory dry-run under `output/patch_specs/`; no source writes and no queue writes. |
| Dry-run matrix evidence bundle | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` | GitHub review, validation handoffs, future selective execution planners | Compact tracked summary of ignored dry-run matrix reports; proves dry-run/planned-only coverage, not provider execution. |
| Evidence bundle | `Tools/ai/build_github_evidence_bundle.py` | GitHub review and future AI agents | Compact tracked summary of ignored `output/` reports. |
| NPU runtime output manifest | `Tools/npu/build_runtime_output_manifest.py` | validation/evidence | Observability only. |
| Provider result envelope | `Tools/npu/pipeline/providers.py` | result reports, diagnostics and evidence | Normalizes provider output and metadata. |
| AI/NPU indexes | `Tools/npu/build_project_ai_index.py`, `Tools/npu/build_npu_code_context.py` | AI agents and future sessions | Generated context; do not hand-edit. |

## Legacy Blender/audio flow

The historical Blender application flow remains:

```text
Audio file
  -> audio analysis process
  -> JSON analysis data
  -> music context / scene specification
  -> Blender Python script or package
  -> generated or tuned Blender scene
  -> render frames
  -> encoded video
```

This is now one application domain over the local AI orchestration workbench, not the project boundary.

## Rules for AI systems

- Start local AI flows from the unified launcher manifest path.
- Preserve run unica semantics: parameters change capacity, not scope.
- Preserve TUTTO SU TUTTO coverage for `Full0To10` unless a lane is explicitly disabled, unavailable or excluded with rationale.
- Add new stable data surfaces to this flow when the full-run perimeter expands.
- Read telemetry/capability surfaces before declaring run success or failure.
- Treat limitations as backlog to overcome, not as reasons to skip available tools.
- Exclude unusable workload reports from advisory context before reading their content.
- Treat NPU short smoke success as diagnostic evidence, not as general advisory promotion.
- Keep provider execution report-bound and opt-out inside Full0To10, not implicit outside selected workflows.
- Do not treat LightFull0To10, provider bridge/readiness or capability manifests as real provider execution proof unless the artifact itself records provider execution.
- Do not treat local output SQLite memory writes as source writes, and do not commit generated DB files.
- Do not overwrite large analysis JSON files unless explicitly requested.
- Treat `indexAI/` and generated manifests as generated context.
- Preserve local path configurability.
- Keep input-domain validators separate from output-application adapters.
- Keep Blender runtime out of core provider orchestration work unless explicitly scoped.
- Document every new expected input and output.

## Missing formal schemas

`docs/JSON_SCHEMAS.md` exists as a schema-notes file, but the following contracts still need more formal treatment:

- unified launcher manifest/phase contract beyond the compact contract doc;
- provider probe report;
- provider bridge/readiness report;
- effective-use SQLite memory/product report;
- runtime tool usage telemetry;
- runtime/hardware capability manifest;
- full toolbox run telemetry summary;
- shared AI-to-AI bundle final summary;
- discovery/index repair reports;
- Python line-count and function/class/method CSV surfaces;
- file-line-limit report;
- selected semantic chunks report/evidence beyond the focused contract already present;
- full-context golden proposal report beyond the focused validator already present;
- legacy audio analysis JSON;
- music context JSON;
- generated artifact plan/manifest schema;
- final tool-product manifest/evidence/readiness package;
- promotion from reviewed dry-run patch spec to approved local apply or GitHub Action queue;
- richer context-pack profiles and selective execution plans for changed-file workflows.

## Recommended next improvement

Inspect the current Full0To10 evidence branches and compact runtime bundles, classify recommendations and patch plans, then select review-first refactor/reuse patch families only after telemetry, provider diagnostics, workload quality, discovery/index, CSV/count and file-line-limit evidence have been reviewed.
