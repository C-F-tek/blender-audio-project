# Project Status Point

## Purpose

This document records the current technical status of `blender-audio-project` for GitHub-only AI work and local continuation.

It is a handoff checkpoint for agents that can read and edit GitHub files and for the maintainer when local workstation validation is available.

## Current baseline on `master`

The repository is now a structured audio-reactive Blender production workspace with reusable AI-pipeline and NPU/backend guardrails.

Current known baseline after PR #38 through PR #47:

| Area | Current status | Evidence / operational meaning |
|---|---|---|
| AI artifact pipeline dry-run matrix | locally validated in prior cycles | Treat the dry-run matrix as validated unless a newer local run fails. Re-run locally before validation-sensitive merges. |
| AI pipeline report contracts | merged and locally validated | PR #38 added schema-v6 report-contract work and regenerated indexes after local validation. |
| NPU helper package | merged and locally validated | PR #41 created the app-agnostic helper-contract layer under `Tools/npu/pipeline/`. |
| NPU runtime IO wiring | merged and locally validated | PR #42 wired legacy-compatible IO helper aliases into `Tools/npu/run_dual_ai_pipeline.py`. |
| NPU runtime contract/path wiring | merged and locally validated | PR #43 wired implementation draft contract validation and generated artifact path helpers. |
| NPU runtime prompt payload wiring | merged and locally validated | PR #44 wired deterministic prompt payload helpers while preserving prompt prose and provider behavior. |
| NPU runtime context/artifact helper wiring | merged and locally validated | PR #45 wired context-summary helper usage and generated support-file write planning. |
| NPU runtime output/preflight guardrails | merged and locally validated | PR #46 added exact legacy output policy, generated scene script write guards and provider-preflight normalization without provider execution changes. |
| AI reference documentation layer | merged | PR #47 added curated AI reference onboarding guides under `docs/`. |
| Generated Python policy | locally validated | Generic generated Python syntax and hazard policy exists before application adapters. |
| Generated Blender script policy | locally validated | Blender remains the first application-specific adapter, not the generic boundary. |
| Generated artifact path policy | locally validated | Generated destinations can be checked without Blender/audio assumptions. |
| SQLite local memory policy | ready with retention/promotion guardrails | Local DB is generated/untracked; GitHub-only agents must document examples but not inspect workstation DB state. |
| Blender runtime packages | frozen for current core/backend work | Do not modify runtime packages as part of NPU/backend continuation. |
| `Scripting/shared/blender_compat.py` | validated as a helper but not migrated broadly | Do not migrate runtime call sites until explicitly entering that phase. |

## Active PR / branch status

There is no active NPU helper-contract PR in this status point. PR #41 through PR #47 are merged.

Before starting the next task, inspect current GitHub PRs and local state:

```powershell
git checkout master
git pull --ff-only
git status
git log --oneline -12
```

## Recent merged PRs

| PR | Title | Scope | Runtime scope |
|---:|---|---|---|
| #38 | AI pipeline report contracts | Added/validated schema-v6 report-contract work and regenerated indexes after maintainer local run. | No Blender runtime package changes. |
| #39 | `[codex] Add NPU pipeline decomposition scaffold` | Added app-agnostic NPU helper package scaffold. | No runtime behavior changes. |
| #40 | `[codex] Add NPU pipeline IO helpers` | Added pure NPU pipeline IO helpers. | No runtime orchestrator wiring yet. |
| #41 | `[codex] Extend NPU pipeline helper contracts` | Added helper contracts, fixtures, planned-only provider descriptors, readiness gates, validators and docs. | No runtime orchestrator wiring in this PR. |
| #42 | `[codex] Wire NPU runtime IO helpers` | Replaced duplicate runtime IO helpers with imports from `Tools/npu/pipeline/io_utils.py`. | Narrow runtime wiring; no provider behavior change. |
| #43 | `[codex] Wire NPU runtime contract path helpers` | Wired implementation draft contract/path helpers and generated artifact path checks. | Narrow runtime wiring; no provider behavior change. |
| #44 | `[codex] Wire NPU runtime prompt payload helpers` | Wired deterministic prompt payload helpers. | Runtime prompt assembly helper wiring; prompt prose/provider behavior unchanged. |
| #45 | `[codex] Wire NPU runtime context and artifact helpers` | Wired context summary helper usage and generated support-file write planning. | Narrow runtime helper wiring; provider behavior unchanged. |
| #46 | `[codex] Guard NPU runtime outputs and preflight reports` | Added exact legacy output policy, scene-script write guards and provider-preflight normalization. | Runtime output/preflight guardrails; provider execution adapters unchanged. |
| #47 | `Add AI reference onboarding documentation layer` | Added curated AI reference docs under `docs/`. | Documentation-only. |

Older guardrail PRs remain part of the baseline:

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
no full analysis JSON edits
no hand-edited AI/NPU indexes
no claims of Blender/audio/GPU/NPU validation without logs
no provider/model execution behavior changes without local validation and explicit scope
```

Every GitHub-only PR must include:

```text
scope
changed files
GitHub-only validation
local validation still pending, unless local reports are supplied
runtime scope
risks
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

Current NPU/backend boundary:

```text
Tools/npu/pipeline/
  -> helper contracts, validators, fixtures, output policy and planned provider descriptors
  -> focused smoke/unit/docs validation
  -> runtime helper adoption in Tools/npu/run_dual_ai_pipeline.py for IO, paths/contracts, prompt payloads, context summary, support-file writes, output guards and preflight normalization
  -> future provider execution adapter work must remain separately scoped and locally validated
```

Blender is the first real application target. WAV/audio is the first real input family. Neither is the architectural limit.

## Active task queue status

| ID | Status | Notes |
|---|---|---|
| GHO-001 | updated | Baseline now records PR #38 through PR #47. |
| GHO-002 | in progress | Only completed execution plans should be moved from `active/` to `completed/`. |
| GHO-003 | in progress | Tech debt needs periodic refresh for generated Python policy, artifact path policy, NPU runtime wiring and GitHub-only limits. |
| GHO-004 | in progress | JSON/schema docs need report-producer-validator gap tables kept current with NPU reports. |
| GHO-005 | mostly addressed | Dry-run matrix contract checks exist; keep strictness tied to locally available report samples. |
| GHO-006 | planned | Future non-Blender Python adapter template should compose `generated_python_policy.py`. |
| GHO-007 | in progress | Memory policy examples should cover retain, quarantine, promote and drop. |
| GHO-008 | in progress | NPU pipeline decomposition has moved from helper contracts into incremental runtime helper adoption; provider execution adapters remain future work. |
| GHO-009 | in progress | PR template should expose GitHub-only and local-validation-pending checkboxes. |
| GHO-010 | in progress | Validator report consistency should be reviewed before follow-up PRs. |

## Current blockers and limits

| Blocker / limit | Impact | Correct handling |
|---|---|---|
| Local output reports are not committed | GitHub-only agents cannot inspect full local validation detail unless pasted or committed. | Use PR bodies and maintainer-provided summaries as evidence; ask for local reports when needed. |
| Runtime packages frozen | Prevents accidental breakage of known working Blender packages. | Keep current core/backend work out of Blender runtime packages. |
| Generated indexes are app-owned | Hand-editing indexes would corrupt generated context. | Regenerate with project scripts locally after structural/doc changes. |
| Schema contracts still partial | AI artifacts can drift. | Document missing checks first; add strict validators only after local report samples are available. |
| NPU runtime orchestrator still owns provider execution | Provider execution changes can affect local model behavior. | Keep provider/model execution adapter work in a separate narrow phase with local validation. |

## Next local owner batch

For the next task on `master`, start with:

```powershell
git checkout master
git pull --ff-only
git status
git log --oneline -12
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

For validation-sensitive changes, run the full local runner:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

If indexes change after local validation, commit only the intentional generated index refresh.

## Recommended next technical directions

Preferred next work should stay in core/backend/AI/NPU layers:

1. Reconcile documentation and execution-plan state after PR #41-#47.
2. Review validator/report contract consistency for the NPU helper and runtime wiring reports.
3. Consider a narrow provider-result parsing/reporting phase without changing provider execution behavior.
4. Consider a runtime-output manifest/report phase if it improves observability without changing generated artifacts.
5. Continue memory/guardrail integration only through deterministic validators and report contracts.

## Do not do yet

Do not do these without explicit scope approval:

- rewrite `Scripting/v61b/main_v61b.py`;
- split the Ready To Jazz monolith;
- migrate package imports to `Scripting/shared/blender_compat.py`;
- change NPU/Ollama provider execution behavior;
- edit full frame-level analysis JSON files;
- hand-edit generated AI/NPU indexes;
- claim Blender/audio/GPU/NPU validation without local logs;
- make dry-run matrix contract stricter before reviewing current local report samples.

## Final technical position

The correct immediate posture is stabilization and small core/backend continuation.

The repository has moved beyond helper scaffolding: NPU helper adoption has begun inside `Tools/npu/run_dual_ai_pipeline.py`, but provider execution changes remain a separate future phase. The next useful changes are state/docs reconciliation, report-contract consistency, and one narrowly scoped NPU/backend milestone at a time.
