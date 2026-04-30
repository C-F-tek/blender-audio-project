# Path Policy Report Inputs

## Status

completed

## Goal

Make generated artifact path policy usable directly on machine-readable AI pipeline reports.

The validator remains generic:

```text
artifact/report contract validator input
  -> collected generated artifact destinations
  -> path policy result
```

It does not depend on Blender, audio/WAV, FFmpeg, GPU, NPU or a specific input data family.

## Scope completed

- Added `--artifact-report` to `Tools/validation/check_generated_artifact_path_policy.py`.
- Collected path-like values from known artifact destination keys.
- Ignored command argv arrays.
- Kept `--path` for explicit manual checks.
- Moved path-policy validation in the local validation runner after the dry-run matrix report exists.
- Updated AI-facing documentation.

## Out of Scope

- No Blender runtime changes.
- No input-domain validator family.
- No generated Python script content policy changes.
- No heavy runtime execution.
- No prompt injection.

## Result

Implemented and merged through PR #32.

Validation summary from the merged PR:

```text
check_generated_artifact_path_policy.py --artifact-report output/ai_pipeline/dry_run_matrix_report.json: PASS, collected 9 paths
check_generated_artifact_path_policy.py --artifact-report missing_report.json: failed as expected
check_python_syntax.py: PASS, checked 167 Python files
run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError: PASS, 18 steps
```

## Follow-up

Future AI pipeline reports can be validated for generated destinations without adding Blender/audio-specific assumptions.

Local workstation validation remains required for runtime behavior.
