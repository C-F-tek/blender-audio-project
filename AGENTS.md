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

## Required reading order

Before creating or editing a package, read:

1. `README.md`
2. `docs/README.md`
3. `docs/PROJECT_AI_CONSCIOUSNESS.md`
4. `docs/AI_EXTERNAL_KNOWLEDGE.md`
5. `docs/MODULE_MAP.md`
6. `docs/DATA_FLOW.md`
7. `docs/REFACTORING_AND_REUSE_PLAN.md`
8. `docs/QUALITY_GATE.md`
9. `docs/SHARED_SCRIPTING_UTILITIES.md`
10. `docs/PATCH_SPEC_WORKFLOW.md` when preparing mechanical edits
11. the README of the target package under `Scripting/`
12. the target Python file before modifying it

## Important folders

| Path | Meaning |
|---|---|
| `Scripting/` | Blender script packages generated or refined from audio-analysis data. |
| `Scripting/v61b/` | Current stable reference package. Do not destructively refactor. |
| `Scripting/shared/` | Reusable package-agnostic utilities. Prefer additive extraction here. |
| `Tools/ai/` | AI artifact pipeline and validation helpers. |
| `Tools/npu/` | Local AI, NPU, context-building and review tooling. |
| `Tools/validation/` | Non-invasive repository validation scripts. |
| `Tools/repo_patch_runner/` | Safe JSON patch-spec runner for small reviewable edits. |
| `patch_specs/` | Patch-spec queue and applied patch history. |
| `indexAI/` | Generated indexes, manifests, context and patch artifacts. Do not hand-refactor as source. |
| `docs/` | Stable documentation and project contracts. |

## Fast validation commands

Use focused checks before broad test runs:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

Optional report output:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output output\validation\json_artifacts.json
```

AI artifact dry run:

```powershell
python .\Tools\ai\run_parallel_artifact_pipeline.py --repo-root . --analysis-json .\output\track_analysis.json --build-chunks --build-music-summary --use-npu --validate --dry-run --write-dry-run-report
```

Regenerate indexes after structural or documentation changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
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
3. Inspect the target Python file before modifying it.
4. Produce small, reviewable changes.
5. Keep working packages stable.
6. Document every new assumption.
7. Run the smallest relevant validation.
8. Report changed files, purpose, risks, tests and line counts.

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
