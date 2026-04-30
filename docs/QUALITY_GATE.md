# Quality Gate

## Purpose

This document defines the minimum quality checks for Blender packages, AI-generated scripts, documentation updates, shared utilities, model-output parsing and generated-file validators in this repository.

The goal is to keep generated work useful, testable, maintainable and safe to review without breaking existing working packages.

## Quality levels

| Level | Meaning | Expected use |
|---|---|---|
| Draft | Early idea or untested AI output | Store as notes, do not treat as production code. |
| Prototype | Runs partially or targets a single test | Acceptable for experiments. |
| Candidate | Structured package/script with documented inputs and validators | Acceptable for application-level validation. |
| Stable reference | Tested workflow used as a reference | Example: `Scripting/v61b/`. |

## Architecture Boundary — Input-Agnostic / Output-Application-Agnostic

Reusable generated-artifact policy must not be tied to the current concrete Blender/audio workflow.

Fixed architectural rule:

```text
not Blender-only
not WAV/audio-only
input-agnostic
output-application-agnostic
current execution assumption: target applications accept generated Python scripts
future extension: other runtimes, other application APIs and other input data families
```

Reason:

```text
Blender is the current real application target, but it is not the architectural limit.
WAV/audio is the current real input family, but it is not the architectural limit.
```

Quality gates must keep these layers separate:

```text
input-domain validation
output-application validation
generated Python script policy
artifact/report contract validation
```

## Minimum quality gate for a new package

A new package under `Scripting/` should include:

- package `README.md`;
- clear entry point;
- configurable paths;
- documented input assumptions;
- documented JSON input or schema assumptions when relevant;
- documented output target;
- test checklist;
- known limitations;
- no destructive overwrite of existing packages;
- no hardcoded private paths unless explicitly marked as local-only.

For Blender/audio packages, additionally document:

- expected audio input when relevant;
- expected analysis JSON when relevant;
- render output path;
- FFmpeg/video encoding path when relevant.

## Minimum code quality

- Keep orchestration separate from helpers when the package is not trivial.
- Prefer `config.py` or equivalent for paths and constants.
- Keep input-domain logic separate from output-application logic.
- For audio/Blender workflows, keep audio mapping separate from scene object creation.
- Keep render and encoding logic explicit when the target app renders media.
- Use `Scripting/shared/` for reusable operational logic when available.
- Use `Tools/ai/model_json.py` for JSON-like model outputs instead of ad-hoc LLM response parsing.
- Use `Scripting/shared/json_io.py` for clean project JSON files and keep it strict.
- Use `Tools/validation/generated_file_policy.py` for reusable generated-file policy checks.
- Use `Tools/validation/check_generated_artifact_path_policy.py` before accepting proposed generated artifact destinations outside the current safe prefixes.
- Do not perform broad refactoring of working packages without explicit validation.

## Minimum documentation quality

Every serious package or validator should answer:

1. What does this package or validator create/check?
2. Which file is the entry point?
3. Which input file types are expected, if any?
4. Which JSON files or schemas are expected, if any?
5. Which application/runtime executes the generated output?
6. Which application/runtime version was used or is expected, if relevant?
7. Where are reports, generated files, renders or other outputs written?
8. How is the final artifact encoded or exported, if relevant?
9. What is not specified yet?
10. What was tested?
11. What should the next AI or developer avoid changing?

## Blender validation checklist

Before calling a Blender package candidate valid:

- Blender opens the script without syntax errors.
- The script can run from a clean scene or documents required preconditions.
- Required audio path is configurable when the workflow is audio-driven.
- Required JSON path is configurable when the workflow is data-driven.
- Frame range is consistent with track duration or documented assumptions when audio/video is involved.
- Camera is created or selected when rendering visuals.
- Lights are created or selected when rendering visuals.
- Render settings are explicit.
- Console output is reviewed.
- A short render test is performed when practical.

## Generated Python script policy checklist

Generated Python script validators should be separated into:

```text
generic generated-file policy engine
  -> generated Python script policy concepts
  -> application-specific adapter
  -> optional input-domain checks only when needed
```

The generic engine must stay independent from:

```text
input file type
input domain
output application
runtime renderer
media format
```

The current generic reference is:

```text
Tools/validation/generated_file_policy.py
```

The first application-specific adapter is Blender:

```text
Tools/validation/check_generated_blender_script_policy.py
```

Before running an AI-generated Blender Python script, use:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --path .\output\some_generated_scene.py --output .\output\validation\generated_blender_script_policy.json
```

Sample-only smoke:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Current Blender blocking rules:

- generated Blender scripts must import `bpy`;
- `ShaderNodeTexMusgrave` is forbidden because it is unavailable in Blender 5.x and caused a real runtime failure;
- generated scripts must not call `bpy.ops.wm.open_mainfile()`;
- generated scripts must not call `bpy.ops.wm.quit_blender()`.

Current Blender warning rules:

- `bpy.ops.wm.save_as_mainfile()` should be reviewed unless explicitly requested;
- dynamic `eval()` / `exec()` should be reviewed unless explicitly justified.

## Generic generated-file policy checklist

When adding policy for another file/application context:

1. keep common rule mechanics in `Tools/validation/generated_file_policy.py`;
2. create an application-specific adapter under `Tools/validation/`;
3. keep input-domain checks separate from output-application checks;
4. include deterministic in-memory samples;
5. keep warnings separate from blocking errors;
6. avoid broad, ambiguous regex rules that block legitimate generated output;
7. add explicit validation commands and report paths to documentation;
8. avoid running external tools unless the validator is explicitly a smoke test.

## Generic generated artifact path policy checklist

Generated artifact path policy is not an input-domain validator and not an output-application adapter. It validates only whether a generated file destination is allowed.

Current validator:

```text
Tools/validation/check_generated_artifact_path_policy.py
```

Default command:

```powershell
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
```

Explicit destination check:

```powershell
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --path .\output\some_generated_artifact.json --output .\output\validation\generated_artifact_path_policy.json
```

Default allowed destinations:

```text
output/
indexAI/
patch_specs/inbox/
patch_specs/applied/
Scripting/v61b/hotpatch/
Tools/npu/npu_code_chunks/
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

Do not broaden these defaults casually. Use `--allowed-prefix` or `--allowed-exact-path` for deliberate workflow-specific extensions, then document why the destination is safe.

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

## AI dry-run matrix report contract checklist

The dry-run matrix report is a report contract, not an output-application adapter and not an input-domain validator.

Current generated report:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

Validate the JSON contract after running the matrix:

```powershell
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
```

Explicit report validation:

```powershell
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --matrix-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\ai_dry_run_matrix_contract.json
```

Minimum root fields:

```text
schema_version
repo_root
output_dir
case_count
passed
results
```

Minimum per-case fields:

```text
name
purpose
command
returncode
duration_sec
report_path
report_exists
report_passed
step_count
lanes
summary
schedule
agent_state_packet
```

Quality rules:

- accept unknown future fields;
- keep warnings separate from blocking errors;
- do not run the dry-run matrix from the contract validator;
- do not rewrite generated artifacts from the contract validator;
- validate `agent_state_packet` metadata only when present.

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
- assumes application/runtime compatibility without test evidence;
- assumes all generated Python scripts are Blender scripts;
- assumes all input data is WAV/audio;
- uses obsolete Blender APIs such as `ShaderNodeTexMusgrave`;
- opens, saves or quits Blender sessions unexpectedly;
- mixes input analysis, output application control, rendering and encoding in one oversized function;
- deletes generated context or analysis data;
- adds paid or external AI GitHub Actions without explicit opt-in;
- uses prompt-based repair where deterministic parsing is available;
- hardens report schemas so much that additive future fields fail validation.

## Current reference

`Scripting/v61b/` remains the current reference for richer Blender package structure and visual ambition.

The current generated-file policy reference is:

```text
Tools/validation/generated_file_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

The current report-contract validator reference is:

```text
Tools/validation/check_ai_dry_run_matrix_contract.py
```

The generated-file policy architecture is intended to outgrow Blender and audio/WAV inputs through small, validated adapters.
