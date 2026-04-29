# Quality Gate

## Purpose

This document defines the minimum quality checks for Blender packages, AI-generated scripts, documentation updates, shared utilities, model-output parsing and generated-file validators in this repository.

The goal is to keep generated work useful, testable, maintainable and safe to review without breaking existing working packages.

## Quality levels

| Level | Meaning | Expected use |
|---|---|---|
| Draft | Early idea or untested AI output | Store as notes, do not treat as production code. |
| Prototype | Runs partially or targets a single test | Acceptable for experiments. |
| Candidate | Structured package/script with documented inputs and validators | Acceptable for Blender validation. |
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
- Use `Tools/ai/model_json.py` for JSON-like model outputs instead of ad-hoc LLM response parsing.
- Use `Scripting/shared/json_io.py` for clean project JSON files and keep it strict.
- Use `Tools/validation/generated_file_policy.py` for reusable generated-file policy checks.
- Do not perform broad refactoring of working packages without explicit validation.

## Minimum documentation quality

Every serious package or validator should answer:

1. What does this package or validator create/check?
2. Which file is the entry point?
3. Which audio file is expected, if any?
4. Which JSON files are expected?
5. Which Blender version was used or is expected, if relevant?
6. Where are renders or reports written?
7. How is the final video encoded, if relevant?
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

## Generated Blender script policy checklist

Before running an AI-generated Blender Python script, use:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --path .\output\some_generated_scene.py --output .\output\validation\generated_blender_script_policy.json
```

Sample-only smoke:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Current blocking rules:

- generated Blender scripts must import `bpy`;
- `ShaderNodeTexMusgrave` is forbidden because it is unavailable in Blender 5.x and caused a real runtime failure;
- generated scripts must not call `bpy.ops.wm.open_mainfile()`;
- generated scripts must not call `bpy.ops.wm.quit_blender()`.

Current warning rules:

- `bpy.ops.wm.save_as_mainfile()` should be reviewed unless explicitly requested;
- dynamic `eval()` / `exec()` should be reviewed unless explicitly justified.

## Generic generated-file policy checklist

When adding policy for another file/application context:

1. keep common rule mechanics in `Tools/validation/generated_file_policy.py`;
2. create an application-specific adapter under `Tools/validation/`;
3. include deterministic in-memory samples;
4. keep warnings separate from blocking errors;
5. avoid broad, ambiguous regex rules that block legitimate generated output;
6. add explicit validation commands and report paths to documentation;
7. avoid running external tools unless the validator is explicitly a smoke test.

## AI model-output JSON checklist

Use `Tools/ai/model_json.py` for JSON-like responses from models.

Current guarantees:

- strips Markdown JSON fences;
- extracts balanced JSON object/array candidates from surrounding prose;
- removes UTF-8 BOM;
- repairs trailing commas before `}` or `]`;
- removes line-only `//` comments;
- raises `ModelJsonParseError` on parse failure;
- does not invent missing fields;
- does not return `{}` silently on failure.

Use this validator after parser or model-output caller changes:

```powershell
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
```

Do not use prompt/model-based JSON repair as the default path. It is slower, non-deterministic and can invent fields. Use deterministic local parsing first.

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

1. create shared utility or generic policy first;
2. keep original package unchanged;
3. test the shared utility/policy;
4. use it in new packages or validators first;
5. migrate existing packages only after validation.

## Red flags

Reject or review carefully when a generated change:

- rewrites a large working script without a clear reason;
- removes package-specific documentation;
- hardcodes paths without explanation;
- invents JSON fields;
- assumes Blender compatibility without test evidence;
- uses obsolete Blender APIs such as `ShaderNodeTexMusgrave`;
- opens, saves or quits Blender sessions unexpectedly;
- mixes audio analysis, scene creation, rendering and encoding in one oversized function;
- deletes generated context or analysis data;
- adds paid or external AI GitHub Actions without explicit opt-in;
- uses prompt-based repair where deterministic parsing is available.

## Current reference

`Scripting/v61b/` remains the current reference for richer package structure and visual ambition.

The current generated-file policy reference is:

```text
Tools/validation/generated_file_policy.py
Tools/validation/check_generated_blender_script_policy.py
```
