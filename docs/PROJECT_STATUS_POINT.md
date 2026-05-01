# Project Status Point

## Purpose

This document records the current technical status of `IA-Carmine Local AI Orchestration Workbench` for GitHub-assisted and local continuation work.

The current GitHub repository slug is still `C-F-tek/blender-audio-project`, but the project identity has moved beyond Blender/audio. The repository is now centered on local AI orchestration, provider-lane routing, quality-gated advisory context, NPU/GPU diagnostics, validation reports and compact GitHub evidence bundles.

## Current GitHub/code baseline

Current `master` / `origin/master` state verified on 2026-05-01:

```text
ef6da71 feat(ai): add full-context golden proposal generator (#82)
```

Recent merged work after the original PR #48 provider baseline:

| PR | Status | Meaning |
|---:|---|---|
| #74 | merged | Added focused semantic chunk selection for bounded local AI context. |
| #75 | merged | Added selected-chunks real local context evidence. |
| #76 | merged | Added selected semantic chunks validator/evidence contract. |
| #78 | merged | Wired selected-chunks evidence into the local AI task adapter. |
| #79 | merged | Added the full-context AI/NPU golden path task entrypoint. |
| #80 | merged | Added compact evidence from the real full-context golden path run. |
| #81 | merged | Added the full-context golden proposal coverage validator. |
| #82 | merged | Added the deterministic full-context golden proposal generator. |

PR #77 remains open on GitHub but is superseded by merged PR #78 unless a human explicitly reopens that line of work.

## Current validated provider baseline

Validated evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
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
| Blender runtime | Blender Python | Legacy application domain | Frozen for the current core/backend milestones. |

## Current self-improvement pipeline status

The current project-owned local AI loop is now broader than the PR #48 provider baseline:

```text
Markdown task entrypoint
  -> semantic code chunk index
  -> selected semantic chunks
  -> selected-chunks evidence
  -> bounded context pack
  -> SQLite-backed agent state packet
  -> explicit multistep GPU/NPU provider workflow
  -> advisory/proposals
  -> deterministic full-context golden proposal generator
  -> manual-review-only patch-spec candidates
```

Important current source additions:

| File | Role |
|---|---|
| `Tools/ai/select_semantic_code_chunks.py` | Builds bounded selected semantic chunk bundles from the generated semantic chunk index. |
| `Tools/validation/check_selected_semantic_chunks.py` | Validates selected chunk bundles and can emit compact selected-chunks evidence. |
| `Tools/ai/build_selective_execution_plan.py` | Report-only planner that recommends validators and candidate patch specs from context/evidence. |
| `Tools/validation/check_selective_execution_plan.py` | Validates selective planner reports. |
| `Tools/ai/build_full_context_golden_proposals.py` | Deterministically emits the full-context golden proposal families P1-P6 for manual review. |
| `Tools/validation/check_full_context_golden_proposals.py` | Validates semantic coverage of full-context golden proposal reports. |

Important current evidence additions:

```text
docs/LOCAL_VALIDATION_EVIDENCE/selected_chunks_real_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/selected_chunks_real_local_ai_context_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_core_ai_backend_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
```

## Provider baseline status

PR #48 introduced the provider-lane baseline still present on `master`:

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
| GHO-002 | updated | Completed execution plans are moved out of `active/`; remaining active plans represent future work. |
| GHO-003 | in progress | Tech debt should record NPU advisory promotion and repository rename decision. |
| GHO-004 | in progress | JSON/schema docs should include new evidence/routing/smoke report contracts. |
| GHO-005 | addressed for current milestone | Compact evidence bundle now replaces pasted long local reports. |
| GHO-006 | in progress | Provider adapter work remains explicit and quality-gated through the local task adapter and multistep workflow flags. |
| GHO-007 | in progress | Memory policy is now used by the local AI task adapter through SQLite-backed agent state packets; durable promotion rules remain separate. |
| GHO-008 | in progress | NPU is validated for decode smoke, not yet for general advisory lane. |
| GHO-009 | in progress | Selected semantic chunks, context packs and full-context golden proposals now exist; next work should promote reviewed proposal families one at a time. |

## Current local owner batch

For new work, start from updated `master`:

```powershell
git fetch origin
git switch master
git pull --ff-only origin master
git status
```

Recommended full-context local run when Carmine can execute GPU/NPU workloads:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile npu -BuildSemanticChunks -SelectSemanticChunks -BuildSelectedChunksEvidence -SelectedChunksEvidenceBasename full_context_golden_selected_chunks_evidence -ChunkQuery "workflow adapter local ai full context enrichment selected chunks sqlite memory provider multistep proposals validators npu knowledge broker context oracle retrieval ranking" -ChunkPathBoost Tools/workflow,Tools/ai,Tools/validation,Tools/npu -SelectedChunksBasename full_context_golden_selected_chunks -MaxSelectedChunks 24 -MaxSelectedChunkChars 32000 -MaxSelectedChunkExcerptChars 2500 -BuildContextPack -ContextPackProfile core_ai_backend -ContextPackBasename full_context_golden_core_ai_backend -ContextPackEvidenceBasename full_context_golden_core_ai_backend_context_pack_evidence -BuildAgentStatePacket -AgentStateBasename full_context_golden_agent_state -AgentStateObjective "Run full-context local AI/NPU golden path and propose controlled complexity escalation such as core helper, validator, wrapper flag, docs contract or NPU knowledge broker." -MemoryDb .\indexAI\agent_memory\agent_memory.sqlite -SaveInputsToMemoryDb -RunMultistepProviderWorkflow -RunOllamaProbe -RunNpuProbe -RunNpuDecodeSmoke -UsePrimaryAdvisoryProvider -BuildEvidence -GeneratePatchSpecs -Basename full_context_golden_local_ai_context -ProposalBasename full_context_golden_local_ai_context_proposals -EvidenceBasename full_context_golden_local_ai_context_evidence -MultistepBasename full_context_golden_local_ai_context_multistep -MultistepProposalBasename full_context_golden_local_ai_context_multistep_proposals -MultistepEvidenceBasename full_context_golden_local_ai_context_multistep_evidence'
```

After documentation/source changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

## Recommended next technical directions

1. Promote the full-context golden proposal families P1-P6 one at a time into reviewed patch specs or focused implementation PRs.
2. Add stricter contract docs for the full-context golden proposal report and selected-chunks evidence flow where still missing.
3. Continue improving the selective planner so it can rank validators and distinguish GitHub-only from local-only next actions.
4. Open a follow-up milestone for NPU advisory promotion only if a real workload quality gate can classify NPU output as `usable_text`.
5. Decide whether to rename the GitHub repository to match the new working title.
6. Keep Blender runtime out of core provider orchestration work.

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
task-scoped AI context packs for safer continuation
selected semantic chunks for focused context
full-context golden proposal generation for controlled next steps
```

Blender/audio remains important as a legacy/current application domain, but not as the project identity or architecture boundary.
