# IA-Carmine Local AI Orchestration Workbench

`blender-audio-project` is now primarily a local AI orchestration, validation and guardrail workbench for app-agnostic AI workflows.

The historical Blender/audio-reactive production code remains in the repository and is still valuable, but it is no longer the architectural center of gravity. The current core is the local AI backend layer that coordinates provider lanes, quality gates, advisory packets, validation reports, memory/guardrail contracts and pushable evidence bundles.

## Current project identity

Working title:

```text
IA-Carmine Local AI Orchestration Workbench
```

Repository slug:

```text
C-F-tek/blender-audio-project
```

The repository has not been renamed yet. Renaming the GitHub repository would change URLs/remotes and should be done only with explicit maintainer confirmation.

## Current primary architecture

```text
local context / reports / generated artifacts
  -> validation and quality gates
  -> provider lane classification
  -> GPU/CUDA advisory lane through Ollama
  -> NPU/OpenVINO probe, guardrail and decode diagnostics
  -> multistep workflow reports
  -> compact GitHub evidence bundles
  -> manual review / PR / merge
```

Current provider mapping:

| Lane | Provider | Role | Current status |
|---|---|---|---|
| GPU/CUDA | Ollama | Primary advisory provider | Active when quality routing confirms `ollama` as usable and workflow is run with explicit primary-advisory flag. |
| NPU/OpenVINO | OpenVINO GenAI | Probe, guardrail and decode diagnostic lane | Available for explicit smoke/probe execution. Promotion to advisory requires quality-gate evidence. |
| Blender runtime | Blender Python | Legacy application target | Frozen for the current core/backend work. Do not touch unless a task explicitly enters a Blender-runtime milestone. |

## Validated state on PR #48 branch

Local evidence pushed under `docs/LOCAL_VALIDATION_EVIDENCE/` confirms:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

The important evidence bundle is:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
```

Validated facts:

- workload quality gate still rejects the old corrupted NPU workload report;
- routing keeps Ollama/GPU as trusted advisory context;
- routing excludes the corrupted NPU workload report from advisory context;
- NPU decode smoke now runs through the dedicated NPU Python executable;
- NPU decode smoke returns readable text and passes its smoke classification;
- provider execution remains explicit and report-bound.

## Main active workflows

### Quality-based advisory routing

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json
python .\Tools\ai\build_workload_quality_lane_routing.py --repo-root . --output .\output\validation\ai_workload_quality_lane_routing.json --markdown-output .\output\validation\ai_workload_quality_lane_routing.md
```

### Parallel GPU/NPU multistep workflow

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

### Pushable evidence bundle

`output/` is intentionally ignored. Push compact evidence instead:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename latest_ai_workflow_evidence
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```

## Main repository layout

| Path | Role |
|---|---|
| `Tools/ai/` | AI orchestration entrypoints, workload quality routing, provider probes, evidence bundles and advisory packet generation. |
| `Tools/workflow/` | Local workflow runners, including post-validation packet generation and parallel GPU/NPU multistep workflows. |
| `Tools/npu/` | NPU/OpenVINO runtime checks, local AI support, context building and legacy dual-AI support. |
| `Tools/npu/pipeline/` | App-agnostic helper package for contracts, provider result envelopes, reports, paths, prompts and validation fixtures. |
| `Tools/validation/` | Non-invasive validators for syntax, docs, reports, generated policies and AI/NPU contracts. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable summaries of long local reports from `output/`. |
| `docs/EXECUTION_PLANS/` | Durable task planning and follow-up tracking. |
| `docs/` | Stable contract and orientation layer for humans and AI agents. |
| `Scripting/` | Legacy/current Blender application packages. Frozen unless explicitly targeted. |
| `indexAI/` | Generated AI indexes and patch/task materials. Do not hand-edit. |

## Guardrails

Current core/backend work must not:

- modify Blender runtime packages;
- start from Ready To Jazz;
- perform broad `blender_compat` adoption;
- modify full analysis JSON files;
- modify legacy output artifacts;
- hand-edit generated indexes;
- change prompt prose legacy, model selection, temperature or provider orchestration without a separate milestone;
- introduce OpenVINO GPU as the primary lane.

Current mapping remains:

```text
Ollama -> GPU/CUDA -> primary advisory provider
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
```

## Legacy Blender/audio role

The repository still contains mature Blender/audio-reactive assets and workflows, including `Scripting/v61b/`, `Scripting/shared/`, audio analysis scripts and FFmpeg/render documentation.

Those assets are now treated as the first application domain that benefits from the local AI orchestration layer, not as the boundary of the project.

## Recommended reading order

1. `AGENTS.md`
2. `WORKFLOW.md`
3. `docs/README.md`
4. `docs/PROJECT_STATUS_POINT.md`
5. `docs/DATA_FLOW.md`
6. `docs/LOCAL_AI_WORKFLOW.md`
7. `docs/JSON_SCHEMAS.md`
8. `Tools/npu/pipeline/README.md`
9. `Tools/validation/README.md`
10. `docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.md`

## Current operational decision

```text
Proceed with PR #48 after documentation review.
Treat Ollama/GPU as the primary advisory lane.
Treat NPU/OpenVINO as a validated smoke/probe lane, not yet a general advisory lane.
Use compact evidence bundles instead of pasting long local output reports.
Keep Blender runtime out of this milestone.
```
