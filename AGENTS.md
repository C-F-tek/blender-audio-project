# AGENTS.md

This file provides operating context for AI assistants and automated code-review systems working on this repository.

## Repository identity

- Working title: `IA-Carmine Local AI Orchestration Workbench`
- Current GitHub repository slug: `C-F-tek/blender-audio-project`
- Author: Carmine Faiola
- Main language: Python
- Primary architecture: local AI orchestration, validation, provider-lane routing and guardrail/evidence workflows
- Primary provider lane: `Ollama -> GPU/CUDA -> primary advisory`
- Secondary provider lane: `OpenVINO -> NPU -> probe / guardrail / decode diagnostic`
- Legacy application domain: Blender audio-reactive scene automation
- License: MIT
- Maturity: active work in progress

The repository name is historical. Do not infer that Blender/audio is still the architectural boundary. The current core work is app-agnostic AI/backend orchestration; Blender remains the first application domain and is frozen for this milestone unless explicitly targeted.

## Core goals

1. Preserve the local AI orchestration workflow and provider-lane contracts.
2. Use Ollama/GPU as the primary advisory lane only when the quality-routing gate confirms it.
3. Keep NPU/OpenVINO available for preflight, probe, guardrail and decode-smoke diagnostics.
4. Exclude unusable workload outputs from advisory context before content is read.
5. Use compact Git-trackable evidence bundles instead of pasting large `output/` reports.
6. Preserve historical Blender Python workflows unless a task explicitly enters a Blender-runtime milestone.
7. Avoid overwriting analysis JSON files unless explicitly requested.
8. Prefer additive documentation, validators, workflow runners and modular patches.
9. Mark unverified information as `not specified`.
10. Use `WORKFLOW.md`, execution plans and the tech debt tracker for durable task control.

## Required reading order

Before creating or editing a package or pipeline module, read:

1. `README.md`
2. `WORKFLOW.md`
3. `docs/README.md`
4. `docs/PROJECT_STATUS_POINT.md`
5. `docs/DATA_FLOW.md`
6. `docs/LOCAL_AI_WORKFLOW.md`
7. `docs/JSON_SCHEMAS.md`
8. `docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.md` when reviewing PR #48 or later evidence bundles
9. `Tools/npu/pipeline/README.md`
10. `Tools/validation/README.md`
11. `docs/EXECUTION_PLANS/README.md`
12. `docs/TECH_DEBT_TRACKER.md`
13. the target source file before modifying it

## Important folders

| Path | Meaning |
|---|---|
| `Tools/ai/` | AI orchestration entrypoints, workload quality routing, provider probes, evidence bundles and advisory packet generation. |
| `Tools/workflow/` | Local workflow runners, including post-validation packet generation and parallel GPU/NPU multistep workflows. |
| `Tools/npu/` | Local AI, OpenVINO/NPU runtime checks, context-building and review tooling. |
| `Tools/npu/pipeline/` | App-agnostic helper package for contracts, provider envelopes, reports, paths, prompts and validation fixtures. |
| `Tools/validation/` | Non-invasive repository validation scripts. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable summaries of long generated reports from ignored `output/`. |
| `docs/EXECUTION_PLANS/` | Durable task records for multi-step work. |
| `docs/` | Stable documentation and project contracts. |
| `Scripting/` | Legacy/current Blender script packages generated or refined from audio-analysis data. Frozen for core/backend work. |
| `Scripting/v61b/` | Historical stable Blender reference package. Do not destructively refactor. |
| `Scripting/shared/` | Reusable package-agnostic Blender helpers. Do not broadly adopt in this milestone. |
| `indexAI/` | Generated indexes, manifests, context and patch artifacts. Do not hand-refactor as source. |

## Current validated AI/provider state

Evidence pushed under `docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json` confirms:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

Operational interpretation:

```text
Ollama/GPU is the primary advisory lane.
NPU/OpenVINO is validated for explicit smoke/probe execution.
The old NPU workload report remains unusable and must stay excluded from advisory context.
NPU promotion to general advisory requires a future quality-gated milestone.
```

## Current NPU/helper package state

`Tools/npu/pipeline/` is an app-agnostic helper package.

Current intended scope:

```text
pure config/path/context helpers
JSON/text IO helpers and legacy-compatible aliases
artifact path and write planning helpers
contract validators
provider result parsing and envelopes
planned-only and explicit provider diagnostics
fixtures, helper-boundary reports and migration-readiness gates
```

Current exclusion:

```text
no Blender runtime changes
no implicit provider execution
no OpenVINO GPU as primary lane
no broad migration of legacy Blender packages
```

## Fast validation commands

Focused core/provider workflow:

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

Core validation:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename latest_ai_workflow_evidence
```

NPU helper validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
```

Regenerate indexes after structural or documentation changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Execution plan workflow

For multi-step work, create a plan under:

```text
docs/EXECUTION_PLANS/active/
```

Move it to:

```text
docs/EXECUTION_PLANS/completed/
docs/EXECUTION_PLANS/abandoned/
```

when the task is finished or intentionally stopped.

See:

```text
docs/EXECUTION_PLANS/README.md
```

## Expected AI workflow

When editing this repository:

1. Identify whether the task is core AI/backend, validation/evidence, NPU/provider diagnostic or legacy Blender runtime.
2. Read the nearest README and relevant docs.
3. Check active execution plans and the tech debt tracker.
4. Inspect the target Python/PowerShell file before modifying it.
5. Produce small, reviewable changes.
6. Keep working packages stable.
7. Document every new assumption.
8. Run the smallest relevant validation.
9. Prefer compact evidence bundles under `docs/LOCAL_VALIDATION_EVIDENCE/` for long local outputs.
10. Report changed files, purpose, risks, tests and line counts.

## Safe modification rules

Allowed without extra confirmation:

- read files and inspect repository structure;
- create additive documentation;
- create additive validators and evidence tooling;
- create report-only or explicit-run workflow scripts;
- run focused validation commands when execution is available;
- create patch specs for human review.

Require explicit confirmation first:

- deleting files;
- renaming the GitHub repository;
- rewriting large working Blender scripts;
- moving package entry points;
- changing full frame-by-frame analysis JSON files;
- adding external dependencies;
- running destructive git operations;
- running long Blender renders;
- changing CI/CD workflows in a way that affects repository automation;
- pushing queued patch specs to trigger GitHub Actions.

## Refactoring rules

- Do not destructively refactor `Scripting/v61b/`.
- Do not split monolithic generated Blender packages in this core/backend milestone.
- Do not migrate package imports to `Scripting/shared/blender_compat.py` unless explicitly scoped.
- Keep path, JSON, provider, evidence and validation logic app-agnostic when practical.
- Keep artistic scene behavior separate from infrastructure refactors.
- Keep generated indexes out of source-level refactors.
- Keep provider execution explicit and report-bound.

## Output expectations

For code changes, report:

- changed files;
- purpose of each change;
- resulting line count for every created or modified script;
- assumptions;
- tests performed or not performed;
- risks;
- follow-up recommendations.

## Quality rule

A local AI workflow change should not be accepted as complete unless it produces a compact evidence bundle or clearly states which checks are still missing.
