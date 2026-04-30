# Project Status Point

## Purpose

This document records the current technical status of `IA-Carmine Local AI Orchestration Workbench` for GitHub-assisted and local continuation work.

The current GitHub repository slug is still `C-F-tek/blender-audio-project`, but the project identity has moved beyond Blender/audio. The repository is now centered on local AI orchestration, provider-lane routing, quality-gated advisory context, NPU/GPU diagnostics, validation reports and compact GitHub evidence bundles.

## Current validated baseline on PR #48 branch

Validated evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
```

Evidence decision summary:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

## Current provider-lane status

| Lane | Provider | Role | Evidence / meaning |
|---|---|---|---|
| GPU/CUDA | Ollama | Primary advisory provider | Quality routing declares `ollama` usable and primary; advisory packet execution used Ollama when explicitly requested. |
| NPU/OpenVINO | OpenVINO GenAI | Probe / guardrail / decode diagnostic | Real NPU decode smoke passed through dedicated NPU Python and produced readable text. |
| Historical NPU workload report | OpenVINO/NPU generated report | Excluded advisory input | The old `npu_real_workload_report.md` remains numeric/hex-like and is correctly excluded from advisory context. |
| Blender runtime | Blender Python | Legacy application domain | Frozen for this milestone. No runtime package work belongs to PR #48. |

## PR #48 status

PR #48 implements the current local AI orchestration milestone:

```text
P-AI-WORKLOAD-QUALITY-BASED-LANE-ROUTING
P-NPU-DECODE-QUALITY-REMEDIATION
P-NPU-DECODE-SMOKE-DIAGNOSTIC
P-ADVISORY-CONTEXT-FILTER-ENFORCEMENT
parallel GPU/NPU multistep workflow
github evidence bundle generation
```

Important source additions:

| File | Role |
|---|---|
| `Tools/ai/workload_quality.py` | Shared helper for quality-based advisory context routing. |
| `Tools/ai/build_workload_quality_lane_routing.py` | Builds lane routing report and declares Ollama/GPU primary advisory provider. |
| `Tools/ai/run_npu_decode_smoke_diagnostic.py` | Explicit NPU/OpenVINO decode smoke diagnostic through dedicated NPU Python. |
| `Tools/ai/build_github_evidence_bundle.py` | Builds compact Git-trackable evidence from ignored `output/` reports. |
| `Tools/validation/check_npu_decode_quality_remediation.py` | Builds NPU decode remediation plan from quality metrics. |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | Supports primary advisory provider mode. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | Coordinates workload quality gate, parallel probes, routing, packet/proposals and evidence. |

Important local evidence additions:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
```

## Current architectural boundary

The current app-agnostic boundary is:

```text
local context and validation reports
  -> workload quality analysis
  -> advisory context routing
  -> provider lane selection
  -> explicit provider probes or advisory generation
  -> compact evidence bundle
  -> manual review and PR merge
```

The correct provider mapping is:

```text
Ollama -> GPU/CUDA
OpenVINO -> NPU
```

Do not introduce OpenVINO GPU as the primary lane.

## Fixed guardrails

Allowed from GitHub-assisted work:

```text
docs updates
execution plans
tech-debt tracker updates
static validators using Python stdlib only
report/evidence summarizers
explicit-run provider diagnostic scripts
workflow runners that keep provider execution explicit
small PRs with local evidence bundles
```

Forbidden without explicit scope approval:

```text
no Blender runtime package edits
no Ready To Jazz split
no Scripting/shared/blender_compat.py broad migration
no full analysis JSON edits
no hand-edited AI/NPU indexes
no implicit provider execution
no provider/model/temperature/prompt prose changes outside a dedicated milestone
no OpenVINO GPU primary lane
no repository rename without explicit maintainer confirmation
```

Every GitHub-assisted PR should include:

```text
scope
changed files
provider execution mode
local evidence bundle path if available
runtime scope
risks
```

## Current blockers and limits

| Blocker / limit | Impact | Correct handling |
|---|---|---|
| Repository slug still says `blender-audio-project` | Name no longer reflects the active architecture. | Documentation now uses `IA-Carmine Local AI Orchestration Workbench`; repository rename requires explicit confirmation. |
| Historical NPU workload output is corrupt/non-linguistic | Cannot use that report as advisory context. | Keep excluded until a future quality-gated workload proves NPU advisory quality. |
| NPU smoke passes only for short diagnostic | Does not yet prove NPU is a general advisory model lane. | Keep NPU as probe/guardrail/diagnostic until broader quality gates pass. |
| `output/` is ignored | Long local reports cannot be reviewed directly on GitHub. | Use `docs/LOCAL_VALIDATION_EVIDENCE/` bundles. |
| Blender runtime packages are frozen | Prevents accidental breakage of known working scene packages. | Keep current work in core AI/backend layers. |

## Active task queue status

| ID | Status | Notes |
|---|---|---|
| GHO-001 | updated | Project identity updated to local AI orchestration workbench. |
| GHO-002 | in progress | Active execution plans should be reconciled after PR #48 merge. |
| GHO-003 | in progress | Tech debt should record NPU advisory promotion and repository rename decision. |
| GHO-004 | in progress | JSON/schema docs should include new evidence/routing/smoke report contracts. |
| GHO-005 | addressed for current milestone | Compact evidence bundle now replaces pasted long local reports. |
| GHO-006 | planned | Future provider adapter work should remain explicit and quality-gated. |
| GHO-007 | in progress | Memory policy remains separate but should use the same evidence/report pattern. |
| GHO-008 | in progress | NPU is validated for decode smoke, not yet for general advisory lane. |

## Next local owner batch

For the next task on this branch:

```powershell
git fetch origin
git checkout ai/workload-quality-routing-npu-remediation
git pull --ff-only
git status
```

Recommended verification:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename parallel_gpu_npu_multistep_real_npu_v2 `
  -ProposalBasename parallel_gpu_npu_multistep_real_npu_v2_proposals `
  -EvidenceBasename parallel_gpu_npu_multistep_real_npu_v2_evidence
```

After documentation/source changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

## Recommended next technical directions

1. Merge PR #48 after documentation and evidence review.
2. Open a follow-up milestone for NPU advisory promotion only if a real workload quality gate can classify NPU output as `usable_text`.
3. Add formal schema notes for:
   - `ai_workload_quality_lane_routing`;
   - `npu_decode_quality_remediation`;
   - `npu_decode_smoke_diagnostic`;
   - `github_validation_evidence_bundle`.
4. Decide whether to rename the GitHub repository to match the new working title.
5. Keep Blender runtime out of core provider orchestration work.

## Do not do yet

Do not do these without explicit scope approval:

- rewrite `Scripting/v61b/main_v61b.py`;
- split the Ready To Jazz monolith;
- migrate package imports to `Scripting/shared/blender_compat.py`;
- change provider execution from explicit to implicit;
- edit full frame-level analysis JSON files;
- hand-edit generated AI/NPU indexes;
- claim NPU is a general advisory lane based only on short smoke success;
- rename the GitHub repository.

## Final technical position

The repository has crossed from Blender/audio project into a local AI orchestration workbench.

The active architecture is now validated around:

```text
Ollama/GPU primary advisory
NPU/OpenVINO explicit probe and decode-smoke diagnostics
quality-based advisory context filtering
parallel provider workflow
compact GitHub evidence bundles
```

Blender/audio remains important as a legacy/current application domain, but not as the project identity or architecture boundary.
