# Quality Gate

## Purpose

This document defines the minimum quality checks for Blender packages, AI-generated scripts, documentation updates, shared utilities, model-output parsing, generated-file validators and local-AI run-unica handoffs in this repository.

The goal is to keep generated work useful, testable, maintainable and safe to review without breaking existing working packages.

This document is a policy guide, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large validator/tool catalogs such as `Tools/validation/README.md` are references only and must not become primary operational entrypoints if too large or truncated.

## Run-unica quality gate

Current doctrine:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
```

A run-unica quality gate passes only when the handoff can show what happened across active lanes. Evidence, recommendations, patch plans and patch specs are incomplete without companion telemetry/capability context and relevant discovery/count context.

Required run-unica handoff group:

```text
launcher manifest
phase_status / phase_reports
evidence artifacts
patch-plan artifacts when produced
runtime tool usage telemetry when tools/broker lanes ran
runtime tool capability manifest when capabilities matter
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
```

Telemetry is a completeness accessory. It does not replace validators, evidence or patch plans; it explains whether the producing lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

Never accept these as proof by themselves:

```text
file exists
patch plan exists
dry-run matrix passed
provider report exists
NPU smoke passed
reviewed patch spec exists
large Markdown mentions it
```

## Quality levels

| Level | Meaning | Expected use |
|---|---|---|
| Draft | Early idea or untested AI output | Store as notes, do not treat as production code. |
| Prototype | Runs partially or targets a single test | Acceptable for experiments. |
| Candidate | Structured package/script with documented inputs and validators | Acceptable for application-level validation. |
| Stable reference | Tested workflow used as a reference | Example: `Scripting/v61b/`. |
| Run-unica handoff | Evidence + patch plan + telemetry/capability/final summary + relevant CSV/index/discovery context | Required for production local-AI handoff. |

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
runtime telemetry and capability interpretation
CSV/index/discovery evidence interpretation
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
- Use `Tools/validation/generated_python_policy.py` for reusable generated Python syntax and hazard checks before application-specific adapters.
- Use `Tools/validation/check_generated_artifact_path_policy.py` before accepting proposed generated artifact destinations outside the current safe prefixes.
- Do not perform broad refactoring of working packages without explicit validation.

## Minimum documentation quality

Every serious package, validator or run-unica lane should answer:

1. What does this package, validator or lane create/check?
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
12. Which telemetry/capability/final-summary surfaces accompany this lane when it enters run-unica handoff?
13. Which CSV/count or discovery/index surfaces accompany this lane when it affects repository-wide visibility or refactor/reuse work?

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

Blender runtime validation is application-domain work. It must not be silently included in core local-AI tooling runs.

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

The current generic Python blocking rules:

- generated Python must parse successfully before adapter validation.

Current generic Python warning rules:

- dynamic `eval()` / `exec()` should be reviewed unless explicitly justified;
- `os.system()` should be reviewed unless explicitly justified;
- `subprocess` calls with `shell=True` should be reviewed unless explicitly justified.

Current Blender blocking rules:

- generated Blender scripts must import `bpy`;
- `ShaderNodeTexMusgrave` is forbidden because it is unavailable in Blender 5.x and caused a real runtime failure;
- generated scripts must not call `bpy.ops.wm.open_mainfile()`;
- generated scripts must not call `bpy.ops.wm.quit_blender()`.

Current Blender warning rules:

- `bpy.ops.wm.save_as_mainfile()` should be reviewed unless explicitly requested;
- generic Python warning rules also apply through the Blender adapter.

Command ownership:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Use validator/tool catalogs only as secondary references.

## Generic generated-file policy checklist

When adding policy for another file/application context:

1. keep common rule mechanics in `Tools/validation/generated_file_policy.py`;
2. create an application-specific adapter under `Tools/validation/`;
3. keep input-domain checks separate from output-application checks;
4. include deterministic in-memory samples;
5. keep warnings separate from blocking errors;
6. avoid broad, ambiguous regex rules that block legitimate generated output;
7. add explicit validation ownership and report paths to documentation;
8. avoid running external tools unless the validator is explicitly a smoke test.

## Generic generated artifact path policy checklist

Generated artifact path policy is not an input-domain validator and not an output-application adapter. It validates only whether a generated file destination is allowed.

Current validator:

```text
Tools/validation/check_generated_artifact_path_policy.py
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

Do not broaden these defaults casually. Use workflow-specific allowed prefixes only when deliberately scoped, then document why the destination is safe.

Do not use `patch_specs/inbox/` as a normal run-unica output. Queueing/applying patch specs remains an explicit reviewed action.

Do not treat `indexAI/code_chunks/**` as commit-ready source. Generated indexes/chunks are regenerated or repaired through explicit plan/report-first flows.

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

Do not use prompt/model-based JSON repair as the default path. It is slower, non-deterministic and can invent fields. Use deterministic local parsing first.

## AI dry-run matrix report contract checklist

The dry-run matrix report is a report contract, not an output-application adapter, not an input-domain validator and not proof of `Full0To10`.

Current generated report:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
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
- validate `agent_state_packet` metadata only when present;
- validate referenced per-case schema-v6 reports without changing their field meanings;
- never report dry-run matrix success as run-unica Full0To10 success.

For dry-run reports, every step must keep:

```text
dry_run=true
planned_only=true
```

## Runtime telemetry/capability checklist

For run-unica, provider, broker, recommendation or patch-plan handoff, inspect or provide:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

Minimum semantics to verify:

```text
tool_call_entry_count
executed_count
failed_count
blocked_count
broker_reports
provider_advisory_state
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
gpu_metrics_source
round_duration_source
patch_application_performed
source_writes_performed
```

## Discovery/index/CSV-count checklist

For refactor/reuse, repository-wide visibility, documentation cleanup or run-unica handoff, inspect or provide relevant surfaces:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
Python line-count CSV/MD
function/class/method inventory CSV
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report
index repair plan/report
```

Minimum semantics to verify:

```text
provider_execution_performed=false for pure inventory/count/report lanes
source_writes_performed=false unless explicit apply/regeneration is selected
patch_application_performed=false unless explicit patch apply is selected
output paths stay under ignored output/** unless compact evidence is intentionally promoted
indexAI/code_chunks/** is not commit-ready source
index repair is plan/report-first unless explicitly requested
```

## FFmpeg validation checklist

FFmpeg validation is application-domain work and must be explicitly scoped.

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
- line counts for created or modified scripts;
- telemetry/capability/final-summary context when it derives from run-unica evidence or patch plans;
- discovery/index/CSV-count context when it derives from refactor/reuse, inventory or repository-wide evidence.

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
- hardens report schemas so much that additive future fields fail validation;
- claims run-unica Full0To10 success from dry-run, focused validator, provider report, NPU smoke, oversized Markdown or file existence alone;
- presents evidence or patch plans without telemetry/capability/final-summary context when the output derives from run-unica evidence;
- presents refactor/reuse or repository-wide plans without relevant discovery/index/CSV-count context.

## Current reference

`Scripting/v61b/` remains the current reference for richer Blender package structure and visual ambition.

The current generated-file policy reference is:

```text
Tools/validation/generated_file_policy.py
Tools/validation/generated_python_policy.py
Tools/validation/check_generated_python_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

The current report-contract validator reference is:

```text
Tools/validation/check_ai_dry_run_matrix_contract.py
```

The current run-unica telemetry/handoff reference is:

```text
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_runtime_tool_capability_manifest.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
```

The generated-file policy architecture is intended to outgrow Blender and audio/WAV inputs through small, validated adapters.
