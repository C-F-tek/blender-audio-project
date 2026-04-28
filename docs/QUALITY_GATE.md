# Quality Gate

## Purpose

This document defines the minimum quality checks for Blender packages, AI-generated scripts, documentation updates, and shared utilities in this repository.

The goal is to keep generated work useful, testable, and maintainable without breaking existing working packages.

## Quality levels

| Level | Meaning | Expected use |
|---|---|---|
| Draft | Early idea or untested AI output | Store as notes, do not treat as production code. |
| Prototype | Runs partially or targets a single test | Acceptable for experiments. |
| Candidate | Structured package with documented inputs and tests | Acceptable for Blender validation. |
| Stable reference | Tested workflow used as a reference | Example: `Scripting/v61b/`. |

## Minimum quality gate for a new package

A new package under `Scripting/` should include:

- package `README.md`;
- clear entry point;
- configurable paths;
- documented audio input;
- documented JSON input or assumptions;
- documented render output;
- test checklist;
- known limitations;
- no destructive overwrite of existing packages;
- no hardcoded private paths unless explicitly marked as local-only.

## Minimum code quality

- Keep orchestration separate from helpers when the package is not trivial.
- Prefer `config.py` or equivalent for paths and constants.
- Keep audio mapping separate from scene object creation.
- Keep render and encoding logic explicit.
- Use `Scripting/shared/` for reusable operational logic when available.
- Do not perform broad refactoring of working packages without explicit validation.

## Minimum documentation quality

Every serious package should answer:

1. What does this package create?
2. Which file is the entry point?
3. Which audio file is expected?
4. Which JSON files are expected?
5. Which Blender version was used or is expected?
6. Where are renders written?
7. How is the final video encoded?
8. What is not specified yet?
9. What was tested?
10. What should the next AI or developer avoid changing?

## Blender validation checklist

Before calling a package candidate valid:

- Blender opens the script without syntax errors.
- The script can run from a clean scene or documents required preconditions.
- Required audio path is configurable.
- Required JSON path is configurable.
- Frame range is consistent with track duration or documented assumptions.
- Camera is created or selected.
- Lights are created or selected.
- Render settings are explicit.
- Console output is reviewed.
- A short render test is performed when practical.

## FFmpeg validation checklist

- Frame sequence path is explicit.
- Start frame number is explicit.
- Frame rate is explicit.
- Audio path is explicit.
- Output path is explicit.
- Codec is explicit.
- Pixel format is explicit.
- Color metadata is explicit when publishing to video platforms.
- CPU/GPU profile is documented.

## AI acceptance criteria

An AI-generated change is acceptable only if it includes:

- files changed;
- reason for each change;
- assumptions;
- test status;
- risks;
- follow-up recommendations;
- line counts for created or modified scripts.

## Non-destructive rule

Do not break known working scripts to improve architecture.

When extracting reusable logic:

1. create shared utility first;
2. keep original package unchanged;
3. test the shared utility;
4. use it in new packages first;
5. migrate existing packages only after validation.

## Red flags

Reject or review carefully when a generated change:

- rewrites a large working script without a clear reason;
- removes package-specific documentation;
- hardcodes paths without explanation;
- invents JSON fields;
- assumes Blender compatibility without test evidence;
- mixes audio analysis, scene creation, rendering, and encoding in one oversized function;
- deletes generated context or analysis data.

## Current reference

`Scripting/v61b/` remains the current reference for richer package structure and visual ambition.
