# Project Status Point

## Purpose

This document records the current technical status of `blender-audio-project` for GitHub-only AI work.

It is a handoff checkpoint for agents that can read and edit GitHub files but cannot access the local workstation, Blender runtime, audio files, GPU/NPU lanes or local `output/` reports.

## Current baseline on `master`

The repository is now a structured audio-reactive Blender production workspace with reusable AI-pipeline guardrails.

Current known baseline after PR #38, PR #39 and PR #40:

| Area | Current status | Evidence / operational meaning |
|---|---|---|
| AI artifact pipeline dry-run matrix | locally validated before this GitHub-only handoff | Treat the dry-run matrix as validated unless a newer local run fails. Do not rerun or claim runtime validation from GitHub-only access. |
| AI pipeline report contracts | locally validated and merged | PR #38 added report-contract work and regenerated indexes after local validation. |
| NPU pipeline scaffold | merged | PR #39 added the app-agnostic NPU helper package scaffold without runtime wiring. |
| NPU IO helpers | merged | PR #40 added pure IO helpers without runtime wiring. |
| Generated Python policy | locally validated | Generic generated Python syntax and hazard policy exists before application adapters. |
| Generated Blender script policy | locally validated | Blender remains the first application-specific adapter, not the generic boundary. |
| Generated artifact path policy | locally validated | Generated destinations can be checked without Blender/audio assumptions. |
| Artifact report path scanning | locally validated | Path policy can scan AI pipeline JSON reports for generated destinations. |
| SQLite local memory policy | ready with retention/promotion guardrails | Local DB is generated/untracked; GitHub-only agents must document examples but not inspect workstation DB state. |
| Blender runtime packages | frozen for GitHub-only work | Do not modify runtime packages from GitHub-only context. |
| `Scripting/shared/blender_compat.py` | validated as a helper but not migrated | Do not migrate runtime call sites yet. |

## Active PR / branch status

| PR / branch | Status | Scope | Runtime scope |
|---|---|---|---|
| PR #41 / `codex/npu-pipeline-decomposition-away-batch` | draft, pending local validation | Extends `Tools/npu/pipeline/` with helper contracts, fixtures, planned-only provider descriptors, readiness gates, focused validators and documentation alignment. | No `Tools/npu/run_dual_ai_pipeline.py` runtime wiring. |

## Recent merged PRs

| PR | Title | Scope | Runtime scope |
|---:|---|---|---|
| #38 | AI pipeline report contracts | Added/validated schema-v6 report-contract work and regenerated indexes after maintainer local run. | No Blender runtime package changes. |
| #39 | `[codex] Add NPU pipeline decomposition scaffold` | Added app-agnostic NPU helper package scaffold and regenerated indexes after maintainer local run. | No NPU/Ollama/Blender runtime behavior changes. |
| #40 | `[codex] Add NPU pipeline IO helpers` | Added pure NPU pipeline IO helpers and regenerated indexes after maintainer local run. | No runtime orchestrator wiring. |

Older GitHub-only guardrail PRs remain part of the baseline:

| PR | Scope |
|---:|---|
| #31 | Generic artifact destination policy and validator. |
| #32 | `--artifact-report` scanning for AI pipeline machine-readable reports. |
| #33 | Generic generated Python policy and Blender adapter over it. |

## Fixed guardrails for GitHub-only work

Allowed from GitHub-only access:

```text
docs updates
execution plans
tech-debt tracker updates
static validators using Python stdlib only
deterministic in-memory samples
schema/report contract planning
small PRs marked local validation pending
```

Forbidden from GitHub-only access:

```text
no Blender runtime package edits
no Ready To Jazz split
no Scripting/shared/blender_compat.py migration
no Tools/npu/run_dual_ai_pipeline.py runtime wiring before local validation/index regeneration
no full analysis JSON edits
no hand-edited AI/NPU indexes
no claims of Blender/audio/GPU/NPU validation without logs
```

Every GitHub-only PR must include:

```text
scope
changed files
GitHub-only validation
local validation still pending
runtime scope
risks
```

Required marker:

```text
Local workstation validation pending.
```

## Current architectural boundary

The generated-artifact policy family remains:

```text
input-agnostic
output-application-agnostic
not Blender-only
not WAV/audio-only
```

Current concrete layers:

```text
Tools/validation/generated_file_policy.py
  -> Tools/validation/generated_python_policy.py
  -> Tools/validation/check_generated_python_policy.py
  -> Tools/validation/check_generated_artifact_path_policy.py
  -> Tools/validation/check_generated_blender_script_policy.py
```

Current NPU helper boundary:

```text
Tools/npu/pipeline/
  -> pure helper contracts
  -> focused smoke/unit/docs validation
  -> migration-readiness gates
  -> future runtime wiring only after local validation and index regeneration
```

Blender is the first real application target. WAV/audio is the first real input family. Neither is the architectural limit.

## Active GitHub-only task queue status

| ID | Status | Notes |
|---|---|---|
| GHO-001 | updated | This file records current baseline through PR #40 plus active PR #41. |
| GHO-002 | in progress | Only completed execution plans should be moved from `active/` to `completed/`. |
| GHO-003 | in progress | Tech debt needs periodic refresh for generated Python policy, artifact path policy, NPU helper contracts and GitHub-only limits. |
| GHO-004 | in progress | JSON/schema docs need report-producer-validator gap tables. |
| GHO-005 | mostly addressed | Dry-run matrix contract checks exist; keep strictness tied to locally available report samples. |
| GHO-006 | planned | Future non-Blender Python adapter template should compose `generated_python_policy.py`. |
| GHO-007 | in progress | Memory policy examples should cover retain, quarantine, promote and drop. |
| GHO-008 | active | NPU pipeline decomposition is underway through helper package PR #41; runtime wiring is not started. |
| GHO-009 | in progress | PR template should expose GitHub-only and local-validation-pending checkboxes. |
| GHO-010 | in progress | Validator report consistency should be reviewed before follow-up PRs. |

## Current blockers and limits

| Blocker / limit | Impact | Correct handling |
|---|---|---|
| No workstation access | Cannot run Blender, audio, GPU/NPU, local dry-run matrix or inspect local `output/`. | Mark local validation pending. |
| Runtime packages frozen | Prevents accidental breakage of known working Blender packages. | Keep changes in docs/plans/static validators. |
| Generated indexes unavailable for regeneration | Hand-editing indexes would corrupt generated context. | Leave AI/NPU index regeneration to the local owner batch. |
| Schema contracts still partial | AI artifacts can drift. | Document missing checks first; add strict validators only after local report samples are available. |
| NPU runtime orchestrator still large | Harder to test and evolve. | Validate helper package first; wire one helper group at a time later. |

## Next local owner batch

When workstation access returns, run:

```powershell
git fetch origin
git checkout codex/npu-pipeline-decomposition-away-batch
git pull --ff-only
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

If indexes change after local validation, commit only the intentional generated index refresh.

## Do not do yet

Do not do these from GitHub-only context:

- rewrite `Scripting/v61b/main_v61b.py`;
- split the Ready To Jazz monolith;
- migrate package imports to `Scripting/shared/blender_compat.py`;
- wire `Tools/npu/pipeline/` helpers into `Tools/npu/run_dual_ai_pipeline.py` before PR #41 local validation and index regeneration are green;
- edit full frame-level analysis JSON files;
- hand-edit generated AI/NPU indexes;
- claim Blender/audio/GPU/NPU validation without local logs;
- make dry-run matrix contract stricter before reviewing current local report samples.

## Final technical position

The correct GitHub-only posture is maintenance, planning and pure helper/validator work, not runtime refactoring.

The next useful changes are small documentation, contract and helper updates that reduce ambiguity for the next local workstation validation cycle.
