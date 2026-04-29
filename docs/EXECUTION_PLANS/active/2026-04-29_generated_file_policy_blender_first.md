# Generated Python Script Policy — Blender First Adapter

## Status

active

## Goal

Introduce a reusable policy model for generated files, starting with generated Python scripts executed by an application.

This model must remain independent from:

```text
input file type
input domain
output application
runtime renderer
media format
```

Examples of input data that must not be hardcoded into the policy model:

```text
WAV audio
JSON analysis files
images
text files
CSV/TSV datasets
application configuration
multi-file project context
```

Examples of output/runtime applications that may receive generated Python scripts in the future:

```text
Blender
other Python-scriptable creative tools
Python-scriptable data tools
Python-scriptable automation/integration tools
OpenWebUI or local AI workflow helpers
custom project applications with Python extension points
```

The first concrete adapter is Blender because the project already encountered a real runtime failure from an obsolete Blender node:

```text
ShaderNodeTexMusgrave undefined
```

Blender is therefore the first application-specific policy adapter, not the architectural boundary.

## Design principle

The intended pattern is:

```text
generic generated-file policy engine
  -> generated Python script policy concepts
  -> application-specific adapter
  -> optional input-domain checks, only when needed
```

For this first step:

```text
Tools/validation/generated_file_policy.py
  -> Tools/validation/check_generated_blender_script_policy.py
```

Future adapters should keep the same separation. A validator for another Python-scriptable app should define app-specific rules while reusing the same generic policy engine.

## Current implementation

Two layers are introduced:

```text
Tools/validation/generated_file_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

### Generic layer

```text
Tools/validation/generated_file_policy.py
```

Role:

```text
PolicyRule
PolicyFinding
PolicyResult
evaluate_text()
evaluate_paths()
```

This layer is domain-neutral. It does not know about WAV files, Blender, renderers, scenes, audio analysis, FFmpeg or any specific generated output target.

### Blender adapter

```text
Tools/validation/check_generated_blender_script_policy.py
```

Role:

```text
validate generated Blender Python scripts before execution
catch known incompatible Blender API usage
catch dangerous project/session operations
emit machine-readable JSON report
run deterministic in-memory samples even when no generated script exists
```

This adapter is intentionally Blender-specific. It is the first concrete consumer of the generic generated-file policy engine.

## Initial Blender rules

Error rules:

```text
requires_bpy_import
forbid_musgrave_node
forbid_open_mainfile
forbid_quit_blender
```

Warning rules:

```text
warn_save_as_mainfile
warn_python_eval_exec
```

## Validation command

Sample-only validation:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Explicit generated script validation:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --path .\output\some_generated_scene.py --output .\output\validation\generated_blender_script_policy.json
```

## Out of scope

```text
running Blender
rendering frames
modifying generated scripts
rewriting Scripting/v61b
changing FFmpeg behavior
assuming all generated scripts are Blender scripts
assuming all inputs are WAV/audio files
blocking all generated scripts with strict production rules
creating validators for non-Blender apps before the generic/app split is proven
```

## Risk

low for sample-only validation.

medium when validating real generated scripts, because policy rules can become too strict. Keep warnings separate from errors.

## Follow-up

After local validation passes:

```text
1. document the validator in Tools/validation/README.md
2. keep it out of the unattended runner until another stable validation cycle confirms it stays cheap and deterministic
3. define the next generated Python script adapter only after identifying a concrete target application
4. define input-domain validators separately from output-application validators
5. extend policy adapters for other file or application contexts only one at a time
```

## Progress log

- 2026-04-29: Started with reusable policy engine plus Blender-specific adapter.
- 2026-04-29: Clarified that the model is input-agnostic and output-application-agnostic. Blender is only the first Python-scriptable application adapter.
