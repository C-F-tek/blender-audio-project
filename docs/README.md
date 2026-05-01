# Documentation

This folder contains the stable technical documentation for `IA-Carmine Local AI Orchestration Workbench`.

The GitHub repository slug is still `C-F-tek/blender-audio-project`, but the current project identity is broader than Blender/audio. The active architecture centers on local AI orchestration, provider-lane routing, quality gates, NPU/GPU diagnostics, validation reports, memory/guardrail contracts and compact GitHub evidence bundles.

Blender/audio-reactive generation remains the first application domain and legacy production target. It is not the current architectural boundary.

## Recommended reading order

1. `../AGENTS.md`
2. `../WORKFLOW.md`
3. `PROJECT_STATUS_POINT.md`
4. `DATA_FLOW.md`
5. `LOCAL_AI_WORKFLOW.md`
6. `JSON_SCHEMAS.md`
7. `../Tools/npu/pipeline/README.md`
8. `../Tools/validation/README.md`
9. `LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.md` when reviewing the validated GPU/NPU workflow
10. `EXECUTION_PLANS/README.md`
11. `TECH_DEBT_TRACKER.md`
12. `MODULE_MAP.md`
13. `REFACTORING_AND_REUSE_PLAN.md`
14. `GITHUB_LOCAL_VALIDATION_WORKFLOW.md`
15. `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`
16. `AI_CONTEXT_PACKS.md`
17. `AI_SELECTIVE_PLANNER.md`
18. `LOCAL_AI_CORE_TOOL_ACTIVATION.md`
19. `LOCAL_AI_TASKS/README.md`
20. `AI_WORKLOAD_REPORT_QUALITY_GATE.md`
21. `AI_REFERENCE_ONBOARDING.md`
22. `AI_REFERENCE_SOURCE_MAP.md`
23. `AI_MEMORY_POLICY.md`
24. `AI_PIPELINE_ARCHITECTURE.md`
25. `AI_PIPELINE_REFACTOR_STATUS.md`
26. `LOCAL_WORKSTATION_TARGET.md`
27. Blender/audio docs only when entering that application domain.

## Current validated provider posture

```text
Ollama -> GPU/CUDA -> primary advisory provider
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
```

Validated evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_master_final_smoke_20260501-232755.json
```

Confirmed decisions:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

## Documentation groups

### Core AI orchestration and validation

| File | Purpose |
|---|---|
| `../README.md` | Current project identity, provider-lane architecture and main workflows. |
| `../AGENTS.md` | Operating contract for AI agents and automated reviewers. |
| `../WORKFLOW.md` | Root operational workflow from task selection to evidence bundle. |
| `PROJECT_STATUS_POINT.md` | Current status checkpoint and next recommended tasks. |
| `DATA_FLOW.md` | Current app-agnostic data/report/provider flow. |
| `LOCAL_AI_WORKFLOW.md` | Local AI provider workflow, GPU/NPU parallelism and evidence handling. |
| `JSON_SCHEMAS.md` | JSON/report contract notes and current schema gap index. |
| `AI_SELECTIVE_PLANNER.md` | Report-only selective planner that recommends validators and candidate patch specs from context/evidence. |
| `LOCAL_AI_CORE_TOOL_ACTIVATION.md` | App-agnostic activation lane for selected chunks, context packs, enrichment plans, knowledge broker packets, proposals and evidence. |
| `LOCAL_AI_TASKS/README.md` | Non-interactive Markdown task entrypoints for local AI runs. |
| `LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable local validation evidence. |
| `../Tools/validation/README.md` | Local validation commands and report contracts. |
| `../Tools/npu/pipeline/README.md` | App-agnostic NPU/provider helper package. |

### Provider, guardrail and memory workflow

| File | Purpose |
|---|---|
| `AI_MEMORY_POLICY.md` | Retention, promotion and quarantine policy for generic agent memory. |
| `AI_WORKLOAD_REPORT_QUALITY_GATE.md` | Documentation and validator workflow for workload quality-gate drift. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local Git/GitHub validation, evidence, index regeneration, commit and push workflow. |
| `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` | GitHub-only continuation mode and local-validation handoff. |
| `AI_CONTEXT_PACKS.md` | Task-scoped AI context pack profiles, builder contract and compact evidence workflow. |
| `EXECUTION_PLANS/README.md` | Durable task-plan workflow for larger or staged work. |
| `TECH_DEBT_TRACKER.md` | Known debt and remediation queue. |
| `MODULE_MAP.md` | Repository areas and navigation map. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | External agent-first engineering patterns mapped into project actions. |
| `AI_EXTERNAL_KNOWLEDGE.md` | External AI-coding knowledge adapted to this project. |
| `AI_REFERENCE_ONBOARDING.md` | AI-to-AI reference onboarding for current local AI/evidence lanes. |
| `AI_REFERENCE_SOURCE_MAP.md` | Source map for AI reference docs and local evidence workflows. |

### AI artifact pipeline and generated policy

| File | Purpose |
|---|---|
| `AI_PIPELINE_ARCHITECTURE.md` | Modular AI artifact pipeline map. |
| `AI_PIPELINE_REFACTOR_STATUS.md` | Stable refactor status marker. |
| `AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes and validation report contracts. |
| `GENERATED_PYTHON_ADAPTER_TEMPLATE.md` | Template for future generated Python application adapters. |
| `PATCH_SPEC_WORKFLOW.md` | Safe JSON patch-spec workflow and dry-run/apply commands. |

### Legacy Blender/audio application domain

These docs remain relevant when working on Blender/audio outputs, but are not the current core architecture:

| File | Purpose |
|---|---|
| `PROJECT_OVERVIEW.md` | Historical/high-level project overview. |
| `BLENDER_SCRIPT_ENTRYPOINTS.md` | Known Blender script entry points and execution notes. |
| `AUDIO_ANALYSIS_PIPELINE.md` | Audio analysis workflow and generated data. |
| `AI_GENERATED_PACKAGE_STANDARD.md` | Expected structure of generated Blender packages. |
| `PACKAGE_CREATION_WORKFLOW.md` | Operational workflow for creating future Blender packages. |
| `QUALITY_GATE.md` | Acceptance checks for generated packages. |
| `RENDER_WORKFLOW.md` | Blender rendering workflow. |
| `FFMPEG_WORKFLOW.md` | Final video encoding workflow. |
| `COMPATIBILITY.md` | Blender/version compatibility notes. |
| `SHARED_SCRIPTING_UTILITIES.md` | Shared Blender utility policy and modules. |

### Setup and operations

| File | Purpose |
|---|---|
| `INSTALLATION.md` | Environment setup notes. |
| `USAGE.md` | Common usage notes. |
| `KNOWN_LIMITATIONS.md` | Known gaps and incomplete areas. |
| `LOCAL_WORKSTATION_TARGET.md` | Local workstation target notes. |
| `DEVELOPER_GUIDE.md` | Practical workflow for development and review. |
| `PROJECT_AUDIT.md` | Technical assessment, risks and next actions. |

## Current workflow summary

Provider baseline validation workflow:

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

Evidence push workflow:

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```

Preferred current local AI core/tool activation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_core_tool_activation.ps1
```

The full-context golden path remains available as a heavier task-specific run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
```

## Documentation style

Use direct, explicit documentation.

Rules:

- Mark unverified information as `not specified`.
- Prefer tables for file maps and contracts.
- Keep provider execution modes explicit.
- Keep package-specific Blender instructions near the package.
- Keep global AI/provider/validation rules in `docs/`, `README.md`, `AGENTS.md` and `WORKFLOW.md`.
- Do not document generated artifacts as manually maintained source.
- Update this index when adding a new stable documentation file.

## AI usage

AI systems should treat this folder as the contract layer for the repository.

Before editing code, an AI system should:

1. read `../AGENTS.md`;
2. read `../WORKFLOW.md`;
3. read this documentation index;
4. read `PROJECT_STATUS_POINT.md`;
5. read `DATA_FLOW.md`;
6. read `LOCAL_AI_WORKFLOW.md`;
7. read `JSON_SCHEMAS.md`;
8. read `../Tools/npu/pipeline/README.md` for NPU/provider work;
9. read `../Tools/validation/README.md` for validation/report work;
10. inspect the target source file before producing a patch.

## Refactoring note

The repository should move toward reusable AI/backend modules first. Legacy Blender package reuse remains valuable, but shared utility extraction must not break working packages and must stay outside the current GPU/NPU orchestration milestone unless explicitly scoped.
