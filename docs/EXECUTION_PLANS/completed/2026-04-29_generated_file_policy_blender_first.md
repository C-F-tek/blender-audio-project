# Generated Python Script Policy — Blender First Adapter

## Status

completed

## Goal

Introduce a reusable policy model for generated files, starting with generated Python scripts executed by an application.

## Architecture Boundary — Input-Agnostic / Output-Application-Agnostic

This policy family is a generic generated-artifact validation model, not a Blender-only or WAV/audio-only feature.

Fixed architectural rule:

```text
not Blender-only
not WAV/audio-only
input-agnostic
output-application-agnostic
current execution assumption: target applications accept generated Python scripts
future extension: other runtimes, other application APIs and other input data families
```

Blender is the first application-specific policy adapter because the project already encountered a real runtime failure from an obsolete Blender node:

```text
ShaderNodeTexMusgrave undefined
```

Blender is therefore the first application-specific policy adapter, not the architectural boundary.

## Completed implementation

The implemented pattern is:

```text
generic generated-file policy engine
  -> generated Python script policy concepts
  -> application-specific adapter
  -> optional input-domain checks, only when needed
```

Concrete files:

```text
Tools/validation/generated_file_policy.py
Tools/validation/generated_python_policy.py
Tools/validation/check_generated_python_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

## Initial rules

Generic Python rules:

```text
python_syntax_error              error
warn_python_eval_exec            warning
warn_os_system                   warning
warn_subprocess_shell_true       warning
```

Blender adapter rules:

```text
requires_bpy_import              error
forbid_musgrave_node             error
forbid_open_mainfile             error
forbid_quit_blender              error
warn_save_as_mainfile            warning
```

## Result

Implemented and merged through PR #33.

Validation summary from the merged PR:

```text
check_generated_python_policy.py: PASS
check_generated_blender_script_policy.py: PASS
check_docs_links.py: PASS
check_python_syntax.py: PASS
run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError: PASS
```

Known non-blocking warning from the merged PR remains unrelated:

```text
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py has an existing invalid escape sequence SyntaxWarning.
```

## Runtime scope

No Blender runtime package was modified.

`Scripting/shared/blender_compat.py` was not migrated into packages.

## Follow-up

Future adapters should compose `generated_python_policy.py` and keep app-specific rules outside the generic layer.

Input-domain validators must remain separate from output-application validators.
