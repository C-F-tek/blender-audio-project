# Data Flow

## Purpose

This document describes the current data movement across `IA-Carmine Local AI Orchestration Workbench`.

The project still contains Blender/audio-reactive workflows, but the active architectural flow is now app-agnostic local AI orchestration: reports, provider lanes, quality gates, explicit probes, advisory packets and compact GitHub evidence.

## Current core AI orchestration flow

```text
local source/docs/context
  -> semantic code chunks and selected focused chunks when useful
  -> task-scoped AI context pack when useful
  -> SQLite-backed agent state packet when requested
  -> validation reports
  -> workload report quality gate
  -> advisory lane routing
  -> trusted/excluded context selection
  -> explicit provider probes or primary advisory generation
  -> post-validation AI packet and proposals
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs
  -> explicit replacement plan and reviewed dry-run spec
  -> compact evidence bundle under docs/LOCAL_VALIDATION_EVIDENCE/
  -> manual review / PR / merge
```

## Provider-lane flow

```text
Ollama/GPU workload report
  -> quality gate: usable_text
  -> advisory lane: ollama
  -> provider mapping: GPU/CUDA
  -> primary advisory packet generation when explicitly requested
```

```text
NPU/OpenVINO workload report
  -> quality gate: unusable_output for old real workload report
  -> excluded from advisory context
  -> remediation report
  -> explicit NPU probe / decode smoke diagnostic
  -> possible future promotion only after quality-gated usable workload output
```

Current mapping:

```text
Ollama -> GPU/CUDA
OpenVINO -> NPU
```

OpenVINO GPU is not a primary lane.

## Parallel multistep workflow flow

`Tools/workflow/run_parallel_ai_provider_multistep.ps1` coordinates:

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
| Source/docs context | repository files | advisory packet builder | Non-workload files are trusted unless normal file read fails. |
| Semantic code chunks | `Tools/npu/build_semantic_code_chunks.py` | selected chunk builder, local AI task adapter | Generated context under index/output paths; do not hand-edit. |
| Selected semantic chunks | `Tools/ai/select_semantic_code_chunks.py` | context pack builder, local AI task adapter, provider packets | Bounded focused context under ignored `output/ai_context_packs/`; validator can emit compact tracked evidence. |
| AI context pack | `Tools/ai/build_ai_context_pack.py` | human/AI task planning, proposal builders | Bounded task-scoped context under ignored `output/ai_context_packs/` plus compact tracked evidence. |
| Agent state packet | `Tools/ai/build_agent_state_packet.py` | local AI task adapter, advisory packet builder | Can use SQLite memory locally; generated SQLite DB files stay untracked. |
| Workload reports | local provider workload scripts | quality gate | Generated text reports from provider lanes. |
| Workload quality report | `Tools/validation/check_ai_workload_report_quality.py` | lane routing, remediation, packet builder | Determines `usable_lanes` and `unusable_lanes`. |
| Lane routing report | `Tools/ai/build_workload_quality_lane_routing.py` | packet builder, evidence bundle | Declares trusted/excluded context and primary advisory provider. |
| NPU remediation report | `Tools/validation/check_npu_decode_quality_remediation.py` | maintainer, proposals, evidence | Explains why NPU is excluded and what must happen before promotion. |
| NPU decode smoke report | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | evidence bundle and future promotion gates | Explicit-run diagnostic; does not imply NPU general advisory quality. |
| Local provider probe report | `Tools/ai/run_local_provider_probe.py` | evidence bundle | Explicit GPU/Ollama and NPU/OpenVINO probe evidence. |
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

- provider probe report;
- selected semantic chunks report/evidence beyond the focused contract already present;
- full-context golden proposal report beyond the focused validator already present;
- legacy audio analysis JSON;
- music context JSON;
- generated artifact plan/manifest schema.
- promotion from reviewed dry-run patch spec to approved local apply or GitHub Action queue;
- richer context-pack profiles and selective execution plans for changed-file workflows.

## Recommended next improvement

Promote the full-context golden proposal families P1-P6 one at a time, then add direct raw-output validators for provider probe reports and continue shaping the suggestion/proposal loop from context packs through reviewed dry-run specs toward approved local apply or queue workflows.
