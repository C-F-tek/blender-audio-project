# AGENTS.md

This file provides operating context for AI assistants and automated code-review systems working on this repository.

## Repository identity

- Name: `blender-audio-project`
- Author: Carmine Faiola
- LinkedIn: https://it.linkedin.com/in/carmine-faiola-12471a183
- Main language: Python
- Target application: Blender
- Domain: audio-reactive visual generation and Blender scene automation
- License: MIT
- Maturity: work in progress

## Core goals

1. Preserve the Blender Python workflow.
2. Keep versioned script folders readable and traceable.
3. Avoid overwriting analysis JSON files unless explicitly requested.
4. Prefer additive documentation and modular patches.
5. Mark unverified information as `not specified`.
6. Use `Scripting/v61b/` as the quality reference for complex generated packages.
7. Keep shared utility extraction non-destructive.

## Required reading order for AI systems

Before creating or editing a package, read:

1. `README.md`
2. `docs/README.md`
3. `docs/MODULE_MAP.md`
4. `docs/DATA_FLOW.md`
5. `docs/AI_GENERATED_PACKAGE_STANDARD.md`
6. `docs/PACKAGE_CREATION_WORKFLOW.md`
7. `docs/QUALITY_GATE.md`
8. `docs/SHARED_SCRIPTING_UTILITIES.md`
9. the README of the target package under `Scripting/`
10. the target Python file before modifying it

## Expected AI workflow

When editing this repository:

1. Identify the target package or folder.
2. Read the package README and relevant docs.
3. Inspect the target Python file before modifying it.
4. Produce small, reviewable changes.
5. Keep working packages stable.
6. Document every new assumption.
7. Report changed files, purpose, risks, and tests.
8. Report line counts for scripts created or modified.

## Safe modification rules

- Do not delete generated analysis files without explicit instruction.
- Do not rewrite the whole project when a focused patch is enough.
- Do not invent Blender version compatibility.
- Do not invent external dependencies.
- Do not hardcode private local paths unless the script is explicitly workstation-specific.
- Keep audio, JSON, render-output, and script paths configurable.
- Do not destructively refactor `Scripting/v61b/`.
- Use additive extraction for shared utilities.
- Do not collapse separate generated packages into one folder.

## Known important folders

| Path | Meaning |
|---|---|
| `Scripting/` | Workspace for Blender script packages generated or refined from audio-analysis data. |
| `Scripting/v61b/` | Current quality reference for complex Blender package structure. |
| `Scripting/shared/` | Target area for reusable package-agnostic utilities. |
| `Tools/npu/` | Local AI, NPU, context-building, and review tooling. |
| `indexAI/` | AI indexes, manifests, context, and patch artifacts. |
| `docs/` | Documentation for humans and AI systems. |
| `examples/` | Future reproducible examples. |

## Output expectations

For code changes, report:

- changed files;
- purpose of each change;
- number of resulting lines for every created or modified script;
- assumptions;
- tests performed or not performed;
- risks;
- follow-up recommendations.

## Quality rule

A generated package should not be accepted as complete unless it satisfies `docs/QUALITY_GATE.md` or clearly states which checks are still missing.
