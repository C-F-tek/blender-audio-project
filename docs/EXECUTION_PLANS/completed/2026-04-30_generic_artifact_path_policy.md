# Generic Artifact Path Policy

## Status

completed

## Goal

Add a deterministic, input-agnostic and output-application-agnostic guardrail for generated artifact destinations.

The policy answers only this question:

```text
May a generated artifact be written to this repository path?
```

It does not answer:

```text
What input domain produced the artifact?
Which application will consume the artifact?
Is the generated Python compatible with Blender or another runtime?
```

## Scope completed

- Extended `Tools/validation/generated_file_policy.py` with reusable path-policy primitives.
- Added `Tools/validation/check_generated_artifact_path_policy.py`.
- Updated local validation workflow and AI-facing docs.
- Kept sample checks deterministic and cheap.
- Kept explicit path checks opt-in through `--path`.

## Out of Scope

- No Blender runtime changes.
- No FFmpeg changes.
- No NPU/GPU execution.
- No prompt injection.
- No input-domain validator family.
- No migration of generated scripts into runtime packages.

## Result

Implemented and merged through PR #31.

Validation summary from the merged PR:

```text
check_generated_artifact_path_policy.py: PASS
explicit allowed path output/ai_pipeline/dry_run_matrix_report.json: PASS
explicit blocked path docs/README.md: blocked as expected
check_python_syntax.py: PASS, checked 167 Python files
run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError: PASS
```

## Follow-up

Keep follow-ups separated:

```text
generated Python script adapters
input-domain validators
output-application validators
artifact/report contract validators
```

Local workstation validation remains the source of truth for runtime behavior.
