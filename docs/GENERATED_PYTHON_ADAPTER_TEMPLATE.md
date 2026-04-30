# Generated Python Adapter Template

## Purpose

This document defines how future non-Blender generated Python adapters should compose the generic generated Python policy.

It is a planning/template document. It does not introduce a new runtime validator by itself.

## Boundary

Future adapters must preserve the existing separation:

```text
generic generated-file policy engine
  -> generic generated Python policy
  -> application-specific adapter
  -> optional input-domain checks only when needed
```

Do not move application-specific rules into:

```text
Tools/validation/generated_file_policy.py
Tools/validation/generated_python_policy.py
```

## Current generic layer

Use this layer first for every generated Python target:

```text
Tools/validation/generated_python_policy.py
Tools/validation/check_generated_python_policy.py
```

Current generic responsibilities:

```text
parse generated Python with ast
block syntax errors
warn on eval/exec
warn on os.system
warn on subprocess shell=True
return a machine-readable report
```

## Adapter structure

A future adapter should be named for the target application or runtime, not for the input domain.

Recommended shape:

```text
Tools/validation/check_generated_<target>_script_policy.py
```

Example for a hypothetical Python-scriptable tool:

```text
Tools/validation/check_generated_automation_script_policy.py
```

The adapter should:

1. import `evaluate_python_text()` or `evaluate_python_paths()` from `generated_python_policy.py`;
2. run generic Python checks first;
3. append target-specific rules;
4. keep warnings separate from blocking errors;
5. include deterministic in-memory samples;
6. accept optional `--path` inputs;
7. write an optional JSON report with a stable contract;
8. avoid launching the target application unless the validator is explicitly a smoke test.

## Report contract recommendation

Use these common root fields when practical:

```text
schema_version
kind
repo_root
passed
errors
warnings or warning_count
rules
sample_results
path_results
```

If the adapter has no root `warnings` list, expose warning counts and rule-level findings in `sample_results` or `path_results`.

## Minimal pseudo-flow

```text
parse CLI args
resolve repo_root
run deterministic samples
for each path:
  run generic generated Python policy
  run target-specific rules
merge errors and warnings
write JSON report when --output is set
exit 0 when passed else 2
```

## Target-specific rules

Rules should be concrete and evidence-backed.

Good examples:

```text
forbid an API known to be removed in the target application version
require an import that is necessary for target execution
warn on save/overwrite operations unless explicitly requested
forbid application quit/session destructive calls
```

Bad examples:

```text
assume every generated Python script is for Blender
assume every generated Python script consumes WAV/audio data
block broad strings that may appear in comments or docs without context
reject unknown future fields in reports
```

## Input-domain checks

Input-domain checks should be separate.

Examples:

```text
WAV/audio analysis contract
CSV input contract
image metadata contract
project-context packet contract
```

These should not be embedded into application adapters unless the adapter explicitly validates a target-specific generated artifact that requires those inputs.

## GitHub-only rule

GitHub-only agents may add this kind of adapter plan or deterministic stdlib-only validator skeleton, but must not claim runtime execution against the target application without local logs.

Required PR marker:

```text
Local workstation validation pending.
```

## First candidate follow-up

The next adapter should only be created after a concrete non-Blender Python-scriptable target is identified.

Until then, keep the work at the template/planning level.
