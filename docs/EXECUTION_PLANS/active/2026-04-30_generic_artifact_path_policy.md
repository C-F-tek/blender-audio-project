# Generic Artifact Path Policy

## Status

completed

## Goal

Add a deterministic, input-agnostic and output-application-agnostic guardrail for generated artifact destinations.

The policy should answer only this question:

```text
May a generated artifact be written to this repository path?
```

It must not answer:

```text
What input domain produced the artifact?
Which application will consume the artifact?
Is the generated Python compatible with Blender or another runtime?
```

## Scope

- Extend `Tools/validation/generated_file_policy.py` with reusable path-policy primitives.
- Add `Tools/validation/check_generated_artifact_path_policy.py`.
- Update local validation workflow and AI-facing docs.
- Keep sample checks deterministic and cheap.
- Keep explicit path checks opt-in through `--path`.

## Out of Scope

- No Blender runtime changes.
- No FFmpeg changes.
- No NPU/GPU execution.
- No prompt injection.
- No input-domain validator family yet.
- No migration of generated scripts into runtime packages.

## Files Likely Touched

```text
Tools/validation/generated_file_policy.py
Tools/validation/check_generated_artifact_path_policy.py
Tools/validation/README.md
Tools/workflow/run_local_validation_after_refactor.ps1
docs/QUALITY_GATE.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/MODULE_MAP.md
docs/EXECUTION_PLANS/active/2026-04-30_generic_artifact_path_policy.md
```

## Validation Commands

```powershell
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --path .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_explicit.json
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Risk Level

low

The implementation is report-only and non-destructive. The main risk is making default allowed prefixes too broad or too narrow. The first version keeps the policy configurable with `--allowed-prefix` and `--allowed-exact-path`.

## Progress Log

- 2026-04-30: Created branch `codex/generic-artifact-path-policy` from merged `master`.
- 2026-04-30: Added path-policy primitives to the generic generated-file policy engine.
- 2026-04-30: Added sample-only and explicit-path generated artifact destination validator.
- 2026-04-30: Verified allowed explicit output path passes and source doc path is blocked.
- 2026-04-30: Updated local validation runner to include AI model JSON, generated artifact path policy, generated Blender script policy and dry-run matrix contract checks.
- 2026-04-30: Ran unattended local validation runner with `-SkipPull -ContinueOnError`; all steps passed.
- 2026-04-30: Regenerated AI/NPU indexes after documentation and validator changes.

## Result

Generic generated artifact destination policy is implemented and locally validated.

Validation summary:

```text
check_generated_artifact_path_policy.py: PASS
explicit allowed path output/ai_pipeline/dry_run_matrix_report.json: PASS
explicit blocked path docs/README.md: blocked as expected
check_python_syntax.py: PASS, checked 167 Python files
run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError: PASS
```

## Follow-up

After this path policy lands, keep follow-ups separated:

```text
generated Python script adapters
input-domain validators
output-application validators
artifact/report contract validators
```
