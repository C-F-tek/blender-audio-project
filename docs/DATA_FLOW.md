# Data Flow

## Purpose

This document describes the current data movement across `IA-Carmine Local AI Orchestration Workbench`.

The project still contains Blender/audio-reactive workflows, but the active architectural flow is now app-agnostic local AI orchestration: launcher-selected phases, reports, provider lanes, quality gates, explicit probes, advisory packets, runtime broker telemetry, capability manifests and compact GitHub evidence.

## Current core AI orchestration flow

```text
unified launcher command
  -> selected modes / Full0To10 profile / intensity knobs
  -> unified_local_ai_refactor_manifest.json
  -> local source/docs/context
  -> Markdown and script inventories when selected
  -> semantic code chunks and selected focused chunks when useful
  -> task-scoped AI context pack when useful
  -> SQLite-backed agent state packet when requested
  -> validation reports
  -> workload report quality gate when provider routing is requested
  -> advisory lane routing
  -> trusted/excluded context selection
  -> explicit provider probes or primary advisory generation
  -> post-validation AI packet and proposals
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs
  -> explicit replacement plan and reviewed dry-run spec
  -> runtime broker report
  -> runtime tool usage telemetry
  -> runtime tool capability manifest
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

## TUTTO SU TUTTO data-flow rule

`-Full0To10` data flow is **TUTTO SU TUTTO**.

Every full-run intensity must preserve the same semantic data surfaces. `quick`, `balanced`, `deep` and `custom` may change volume, context size and runtime budget, but they must not silently remove core data flows.

The full-run perimeter can expand. When a new production-ready data surface appears, such as a registry, broker tool report, provider diagnostic, repository-consistency map, memory/context builder or telemetry summary, it must be added to this document and to the launcher contract, or explicitly excluded with rationale.

## Provider-lane flow

```text
Ollama/GPU workload report
  -> quality gate: usable_text
  -> advisory lane: ollama
  -> provider mapping: GPU/CUDA
  -> primary advisory packet generation when explicitly requested
  -> provider diagnostics and degradation state in telemetry/bundle
```

```text
NPU/OpenVINO workload report
  -> quality gate: unusable_output for old real workload report
  -> excluded from advisory context
  -> remediation report
  -> explicit NPU probe / decode smoke diagnostic
  -> possible future promotion only after quality-gated usable workload output
  -> provider diagnostics and exclusion reason in telemetry/bundle
```

Current mapping:

```text
Ollama -> GPU/CUDA
OpenVINO -> NPU
```

OpenVINO GPU is not a primary lane.

## Runtime telemetry flow

```text
runtime broker requests
  -> Tools/ai/agent_runtime_tool_broker.py
  -> runtime_tool_broker_full_toolbox_<STAMP>.json/md
  -> Tools/ai/build_runtime_tool_usage_telemetry.py
  -> runtime_tool_usage_telemetry_<STAMP>.json/md
  -> Tools/ai/build_runtime_tool_capability_manifest.py
  -> runtime_tool_capability_manifest_<STAMP>.json/md
  -> Tools/ai/build_full_toolbox_run_telemetry_summary.py
  -> full_toolbox_run_telemetry_summary_<STAMP>.json/md
  -> Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
  -> shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
  -> shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

Telemetry answers AI-critical questions:

```text
which tools were available
which tools executed
which tools failed
which tools were blocked
which provider lanes degraded
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
| Unified manifest | `Tools/workflow/run_unified_local_ai_refactor.ps1` | human/AI review | First review object for selected modes, phase status, reports, context, providers and guardrails. |
| Source/docs context | repository files | inventories, context packs, advisory packet builder | Non-workload files are trusted unless normal file read fails. |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | docs cleanup, pruning, link review | Generated under `output/**`; do not commit unless compact evidence is intentionally built. |
| Script inventory | `Tools/validation/build_script_inventory.py` | tool/function visibility, refactor review | JSON/CSV/Markdown inventory under `output/**`. |
| Semantic code chunks | `Tools/npu/build_semantic_code_chunks.py` | selected chunk builder, local AI task adapter | Generated context under index/output paths; do not hand-edit. |
| Selected semantic chunks | `Tools/ai/select_semantic_code_chunks.py` | context pack builder, local AI task adapter, provider packets | Bounded focused context under ignored `output/ai_context_packs/`; validator can emit compact tracked evidence. |
| AI context pack | `Tools/ai/build_ai_context_pack.py` | human/AI task planning, proposal builders | Bounded task-scoped context under ignored `output/ai_context_packs/` plus compact tracked evidence. |
| Agent state packet | `Tools/ai/build_agent_state_packet.py` | local AI task adapter, advisory packet builder | Can use SQLite memory locally; generated SQLite DB files stay untracked. |
| Workload reports | local provider workload scripts | quality gate | Generated text reports from provider lanes. |
| Workload quality report | `Tools/validation/check_ai_workload_report_quality.py` | lane routing, remediation, packet builder | Determines `usable_lanes` and `unusable_lanes`. |
| Lane routing report | `Tools/ai/build_workload_quality_lane_routing.py` | packet builder, evidence bundle | Declares trusted/excluded context and primary advisory provider. |
| Provider diagnostics | provider/probe tools and sync analyzers | telemetry summary, bundle, AI agents | Must expose advisory state, failure reasons, degraded components and GPU/NPU timing source. |
| NPU remediation report | `Tools/validation/check_npu_decode_quality_remediation.py` | maintainer, proposals, evidence | Explains why NPU is excluded and what must happen before promotion. |
| NPU decode smoke report | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | evidence bundle and future promotion gates | Explicit-run diagnostic; does not imply NPU general advisory quality. |
| Local provider probe report | `Tools/ai/run_local_provider_probe.py` | evidence bundle | Explicit GPU/Ollama and NPU/OpenVINO probe evidence. |
| Runtime broker report | `Tools/ai/agent_runtime_tool_broker.py` | runtime telemetry, full toolbox bundle | Shows broker-requested tool calls and guardrail outcomes. |
| Runtime tool usage telemetry | `Tools/ai/build_runtime_tool_usage_telemetry.py` | AI agents, telemetry summary, bundle | Counts executed/failed/blocked broker calls and carries broker report inputs. |
| Runtime tool capability manifest | `Tools/ai/build_runtime_tool_capability_manifest.py` | AI agents, bundle, cloud handoff | Describes available tools, allowed args and execution guardrails. |
| Full toolbox run telemetry summary | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | AI agents, bundle, PR review | Cross-run summary of provider, GPU/NPU, broker, patch-plan and guardrail state. |
| Shared AI-to-AI bundle | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | next local/cloud AI, PR review | Production handoff surface; must carry diagnostics, telemetry, capability and patch-plan summary. |
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

- Start full local AI flows from the unified launcher manifest path.
- Preserve TUTTO SU TUTTO coverage for all full-run intensities.
- Add new stable data surfaces to this flow when the full-run perimeter expands.
- Read telemetry/capability surfaces before declaring run success or failure.
- Exclude unusable workload reports from advisory context before reading their content.
- Treat NPU short smoke success as diagnostic evidence, not as general advisory promotion.
- Keep provider execution explicit and report-bound.
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
- runtime tool usage telemetry;
- runtime tool capability manifest;
- full toolbox run telemetry summary;
- shared AI-to-AI bundle final summary;
- selected semantic chunks report/evidence beyond the focused contract already present;
- full-context golden proposal report beyond the focused validator already present;
- legacy audio analysis JSON;
- music context JSON;
- generated artifact plan/manifest schema;
- promotion from reviewed dry-run patch spec to approved local apply or GitHub Action queue;
- richer context-pack profiles and selective execution plans for changed-file workflows.

## Recommended next improvement

Keep the unified launcher contract and docs indexes aligned with the actual runner, finish external-control pass-through for subordinate launcher calls, and keep telemetry/capability manifests as first-class AI handoff inputs. Promote full-context golden proposal families P1-P6 one at a time only after the relevant telemetry, provider diagnostics and guardrails are visible in compact evidence.
