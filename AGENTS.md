# AGENTS.md

This file provides operating context for AI assistants and automated code-review systems working on this repository.

## Repository identity

- Name: `blender-audio-project`
- Author: Carmine Faiola
- Main language: Python
- Target application: Blender
- Domain: audio-reactive visual generation and Blender scene automation
- License: MIT
- Maturity: work in progress

## Core goals

1. Preserve the Blender Python workflow.
2. Keep versioned script folders readable and traceable.
3. Avoid overwriting analysis JSON files unless explicitly requested.
4. Prefer additive documentation, shared utilities and modular patches.
5. Mark unverified information as `not specified`.
6. Use `Scripting/v61b/` as the quality reference for complex generated packages.
7. Keep shared utility extraction non-destructive.
8. Treat the modular AI artifact pipeline as validated after workstation dry-run matrix unless a newer validation fails.
9. Use `WORKFLOW.md`, execution plans and the tech debt tracker for durable task control.

## Required reading order

Before creating or editing a package or pipeline module, read:

1. `README.md`
2. `WORKFLOW.md`
3. `docs/README.md`
4. `docs/PROJECT_AI_CONSCIOUSNESS.md`
5. `docs/AI_ONBOARDING.md`
6. `docs/AI_PIPELINE_REFACTOR_STATUS.md`
7. `docs/AI_PIPELINE_ARCHITECTURE.md`
8. `docs/AI_MEMORY_POLICY.md`
9. `docs/AI_EXTERNAL_KNOWLEDGE.md`
10. `docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md`
11. `docs/EXECUTION_PLANS/README.md`
12. `docs/TECH_DEBT_TRACKER.md`
13. `docs/MODULE_MAP.md`
14. `docs/DATA_FLOW.md`
15. `docs/REFACTORING_AND_REUSE_PLAN.md`
16. `docs/QUALITY_GATE.md`
17. `docs/SHARED_SCRIPTING_UTILITIES.md`
18. `docs/PATCH_SPEC_WORKFLOW.md` when preparing mechanical edits
19. the README of the target package under `Scripting/`
20. the target Python file before modifying it

## Important folders

| Path | Meaning |
|---|---|
| `Scripting/` | Blender script packages generated or refined from audio-analysis data. |
| `Scripting/v61b/` | Current stable reference package. Do not destructively refactor. |
| `Scripting/shared/` | Reusable package-agnostic utilities. Prefer additive extraction here. |
| `Tools/ai/` | AI artifact pipeline, dry-run matrix and validation helpers. |
| `Tools/ai/pipeline/` | Modular AI artifact pipeline implementation. Read `docs/AI_PIPELINE_ARCHITECTURE.md` first. |
| `Tools/npu/` | Local AI, NPU, context-building and review tooling. |
| `Tools/validation/` | Non-invasive repository validation scripts. |
| `Tools/workflow/` | Local workflow runners and unattended validation scripts. |
| `Tools/repo_patch_runner/` | Safe JSON patch-spec runner for small reviewable edits. |
| `docs/EXECUTION_PLANS/` | Durable task records for multi-step work. |
| `patch_specs/` | Patch-spec queue and applied patch history. |
| `indexAI/` | Generated indexes, manifests, context and patch artifacts. Do not hand-refactor as source. |
| `docs/` | Stable documentation and project contracts. |

## Current AI pipeline state

The AI artifact pipeline has been modularized and locally validated.

Machine-readable status:

```text
Tools/ai/pipeline/refactor_status.py
```

Human-readable status and architecture:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
```

Operational validation now includes:

```text
AI module smoke validator: PASS
AI dry-run matrix: PASS
agent memory policy validation: PASS when no quarantined local memory exists
generated Python policy validation: PASS
generated artifact path policy validation: PASS
Blender shared compatibility smoke: PASS in Blender 5.1.1 for frame range, noise node and VSE audio strip creation
JSON artifact validation: PASS
package structure validation: PASS
index regeneration: PASS
```

## Fast validation commands

Use focused checks before broad test runs:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
```

Optional report output:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output output\validation\json_artifacts.json
```

AI pipeline module smoke validation:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
```

AI pipeline dry-run matrix:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Unattended local validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
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

## Patch-spec workflow

For small mechanical edits, prefer a JSON patch spec when it improves reviewability.

Dry-run:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --dry-run
```

Apply locally with diff:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --write --show-diff
```

Queue for GitHub Action only after human review:

```powershell
git add patch_specs/inbox/example.json
git commit -m "queue repo patch spec"
git push origin master
```

See `docs/PATCH_SPEC_WORKFLOW.md`.

## Expected AI workflow

When editing this repository:

1. Identify the target package or folder.
2. Read the nearest README and relevant docs.
3. Check active execution plans and the tech debt tracker.
4. Inspect the target Python file before modifying it.
5. Produce small, reviewable changes.
6. Keep working packages stable.
7. Document every new assumption.
8. Run the smallest relevant validation.
9. Report changed files, purpose, risks, tests and line counts.

For AI pipeline changes specifically:

1. read `docs/AI_PIPELINE_REFACTOR_STATUS.md`;
2. read `docs/AI_PIPELINE_ARCHITECTURE.md`;
3. preserve schema-v6 field meanings;
4. run `check_ai_pipeline_modules.py` and the dry-run matrix when local execution is available;
5. regenerate AI/NPU indexes after structural changes.

## Safe modification rules

Allowed without extra confirmation:

- read files and inspect repository structure;
- create additive documentation;
- create additive shared utilities;
- create non-invasive validation scripts;
- run focused validation commands when execution is available;
- create patch specs for human review.

Require explicit confirmation first:

- deleting files;
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
- Do not split monolithic generated packages before shared infrastructure exists.
- Create shared utilities first, test them, then add package adapters.
- Keep path, JSON, render, FFmpeg and Blender-compatibility logic package-agnostic when practical.
- Keep artistic scene behavior separate from infrastructure refactors.
- Keep generated indexes out of source-level refactors.
- Keep `Tools/ai/run_parallel_artifact_pipeline.py` as a thin entrypoint; add behavior to focused modules under `Tools/ai/pipeline/`.

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

A generated package should not be accepted as complete unless it satisfies `docs/QUALITY_GATE.md` or clearly states which checks are still missing.
