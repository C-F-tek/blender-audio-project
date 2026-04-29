# Generated File Policy — Blender First

## Status

active

## Goal

Introduce a reusable policy model for generated files, starting with generated Blender Python scripts.

The first concrete target is Blender because the project already encountered a real runtime failure from an obsolete Blender node:

```text
ShaderNodeTexMusgrave undefined
```

The design must remain reusable for other file and application contexts, such as:

```text
Python scripts
PowerShell scripts
JSON artifacts
YAML workflows
OpenWebUI filters
application-specific config files
```

## Design

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

This layer is domain-neutral and can be reused by future validators.

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

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Optional explicit file validation:

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
blocking all generated scripts with strict production rules
```

## Risk

low for sample-only validation.

medium when validating real generated scripts, because policy rules can become too strict. Keep warnings separate from errors.

## Follow-up

After local validation passes:

```text
1. document the validator in Tools/validation/README.md
2. add it to local validation runner only if it remains cheap and deterministic
3. extend policy adapters for other generated file types only one at a time
```

## Progress log

- 2026-04-29: Started with reusable policy engine plus Blender-specific adapter.
