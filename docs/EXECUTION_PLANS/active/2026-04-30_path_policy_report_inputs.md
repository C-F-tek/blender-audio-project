# Path Policy Report Inputs

## Status

completed

## Goal

Make generated artifact path policy usable directly on machine-readable AI pipeline reports.

The validator should remain generic:

```text
artifact/report contract validator input
  -> collected generated artifact destinations
  -> path policy result
```

It must not depend on Blender, audio/WAV, FFmpeg, GPU, NPU or a specific input data family.

## Scope

- Add `--artifact-report` to `Tools/validation/check_generated_artifact_path_policy.py`.
- Collect path-like values from known artifact destination keys.
- Ignore command argv arrays.
- Keep `--path` for explicit manual checks.
- Run the path-policy validator against `output/ai_pipeline/dry_run_matrix_report.json` in the local validation runner after the dry-run matrix exists.
- Update AI-facing documentation.

## Out of Scope

- No Blender runtime changes.
- No input-domain validator family.
- No generated Python script content policy changes.
- No heavy runtime execution.
- No prompt injection.

## Files Likely Touched

```text
Tools/validation/check_generated_artifact_path_policy.py
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/validation/README.md
docs/AI_SMART_POLICY.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/QUALITY_GATE.md
docs/EXECUTION_PLANS/active/2026-04-30_path_policy_report_inputs.md
```

## Validation Commands

```powershell
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\missing_report.json --output .\output\validation\generated_artifact_path_policy_missing_report.json
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Risk Level

low

The validator remains non-destructive and report-only. The main risk is collecting a non-path prose field. Mitigation: collect only known artifact path keys, ignore `command` arrays and require strings to look path-like.

## Progress Log

- 2026-04-30: Merged PR #31 and created branch `codex/path-policy-report-inputs`.
- 2026-04-30: Added JSON report loading and path collection for artifact destination fields.
- 2026-04-30: Moved local runner path-policy validation after dry-run matrix generation and contract validation.
- 2026-04-30: Verified the dry-run matrix report scan passes and collects 9 generated artifact destinations.
- 2026-04-30: Verified missing artifact report fails with a deterministic error.
- 2026-04-30: Ran unattended local validation runner with `-SkipPull -ContinueOnError`; all 18 steps passed.
- 2026-04-30: Regenerated AI/NPU indexes after documentation and validator changes.

## Result

Path policy report scanning is implemented and locally validated.

Validation summary:

```text
check_generated_artifact_path_policy.py --artifact-report output/ai_pipeline/dry_run_matrix_report.json: PASS, collected 9 paths
check_generated_artifact_path_policy.py --artifact-report missing_report.json: failed as expected
check_python_syntax.py: PASS, checked 167 Python files
run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError: PASS, 18 steps
```

## Follow-up

After this lands, future AI pipeline reports can be validated for generated destinations without adding Blender/audio-specific assumptions.
