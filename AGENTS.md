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

## Expected AI workflow

When editing this repository:

1. Read `README.md`.
2. Read `docs/PROJECT_OVERVIEW.md`.
3. Read the README in the target folder.
4. Inspect the target Python file before modifying it.
5. Produce small, reviewable changes.
6. Document every new assumption.

## Safe modification rules

- Do not delete generated analysis files without explicit instruction.
- Do not rewrite the whole project when a focused patch is enough.
- Do not invent Blender version compatibility.
- Do not invent external dependencies.
- Do not hardcode private local paths unless the script is explicitly workstation-specific.
- Keep audio, JSON, render-output, and script paths configurable.

## Known important folders

| Path | Meaning |
|---|---|
| `Scripting/` | Main Python script workspace. |
| `Scripting/v61b/` | Current versioned workflow area. |
| `docs/` | Documentation for humans and AI systems. |
| `examples/` | Future reproducible examples. |

## Output expectations

For code changes, report:

- changed files;
- purpose of each change;
- number of resulting lines for every created or modified script;
- assumptions;
- tests performed or not performed.
