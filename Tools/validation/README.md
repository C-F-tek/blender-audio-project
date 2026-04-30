# Tools/validation

This folder contains lightweight repository validation helpers.

The tools are intentionally non-invasive: they inspect files and write optional reports. They must not rewrite source code, generated scripts, generated JSON artifacts, Blender packages, render outputs or FFmpeg outputs.

## Validation model

Validation is split into deterministic checks:

```text
source/code syntax checks
repository/package structure checks
JSON artifact checks
documentation link checks
execution-plan folder/status checks
AI pipeline smoke checks
NPU pipeline helper smoke and unit tests
AI dry-run matrix case-definition checks
AI dry-run matrix output consistency checks
AI dry-run matrix report contract checks
AI pipeline schema-v6 report contract checks
validation report contract checks
agent memory policy checks
Blender compatibility smokes
generated-file policy checks
generated Python policy checks
generated artifact path policy checks
```

Validators should remain cheap, reviewable and safe to run locally.

## Common validation report contract

Validation reports should converge toward these root fields:

```text
schema_version
kind
repo_root
passed
errors
warnings, when applicable
```

Rules:

- `schema_version` should be an integer.
- `kind` should identify the validator/report family.
- `repo_root` should be a string.
- `passed` should be a boolean.
- `errors` should be a list.
- `warnings` should be a list when present.
- Adding these fields must be additive and should not remove validator-specific fields.

Meta-validator:

```powershell
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
```

Optional stricter mode after more reports are aligned:

```powershell
python .\Tools\validation\check_validation_report_contract.py --repo-root . --require-recommended --output .\output\validation\validation_report_contract.json
```

## Architecture boundary

Generated-file validation is not Blender-only and not WAV/audio-only.

Keep these validation layers separate:

```text
input-domain validators
output-application validators
generated Python script policy adapters
artifact/report contract validators
```

## Available checks

Core repository checks:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output .\output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output .\output\validation\json_artifacts.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

AI pipeline, NPU helper, report-contract and memory checks:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_dry_run_matrix_cases.py --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
python .\Tools\validation\check_ai_pipeline_report_contract.py --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_outputs.py --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
```

Blender and generated-file checks:

```powershell
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

## Tool map

| Tool | Role | Heavy workloads |
|---|---|---|
| `check_python_syntax.py` | Compiles Python files without importing project modules. | No |
| `check_package_structure.py` | Reports package-level structure and warnings under `Scripting/`. | No |
| `check_json_artifacts.py` | Checks JSON parseability; accepts UTF-8 with or without BOM and skips very large files by default. | No |
| `check_docs_links.py` | Validates repository-local Markdown links and ignores external URLs. | No |
| `check_execution_plan_status.py` | Ensures terminal execution plans are not left under `docs/EXECUTION_PLANS/active/`. | No |
| `check_ai_pipeline_modules.py` | Imports modular AI pipeline code and validates representative planning/report helpers. | No |
| `check_npu_pipeline_modules.py` | Imports app-agnostic NPU pipeline helpers and validates representative contract, provider-planning and boundary helpers. | No |
| `check_npu_pipeline_helper_tests.py` | Runs deterministic `unittest` coverage for app-agnostic NPU helper modules and emits a JSON validation report. | No |
| `test_npu_pipeline_helpers.py` | Unit test module used by `check_npu_pipeline_helper_tests.py`. | No |
| `check_ai_model_json.py` | Validates deterministic parsing of JSON-like model output and legacy wrapper behavior. | No |
| `check_ai_dry_run_matrix_cases.py` | Validates dry-run matrix case definitions without executing the matrix. | No |
| `check_ai_dry_run_matrix_outputs.py` | Validates generated dry-run matrix outputs against per-case reports. | No |
| `check_ai_dry_run_matrix_contract.py` | Validates the machine-readable dry-run matrix report contract. | No |
| `check_ai_pipeline_report_contract.py` | Validates one schema-v6 AI pipeline report, including dry-run-only semantics when requested. | No |
| `check_validation_report_contract.py` | Validates generated reports in `output/validation/` for common root fields. | No |
| `check_refactor_status_consistency.py` | Checks that AI pipeline status markers and docs agree. | No |
| `check_agent_memory_policy.py` | Checks generic memory retention and promotion guardrails. | No |
| `check_blender_shared_compat_smoke.py` | Imports shared Blender compatibility helpers; performs no render. | No render |
| `check_generated_python_policy.py` | Validates generic generated Python syntax and hazard policy. | No |
| `check_generated_artifact_path_policy.py` | Validates generated artifact destination paths. | No |
| `check_generated_blender_script_policy.py` | Validates generated Blender Python scripts before execution. | No |

## Execution plan status validation

Completed plans must live under:

```text
docs/EXECUTION_PLANS/completed/
```

Active plans must not have top-level status `completed`, `abandoned` or `wont_fix`.

Run:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

This check exists because completed plans left under `active/` confuse future AI task selection.

## NPU pipeline helper validation

Focused import/contract smoke:

```powershell
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
```

Focused unit-test report:

```powershell
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
```

Direct unittest mode, useful while debugging locally:

```powershell
python .\Tools\validation\test_npu_pipeline_helpers.py
```

These tests must remain provider-free and runtime-free. They may use temporary directories, but they must not invoke Blender, NPU, GPU, Ollama, FFmpeg or modify project source files.

## Post-validation AI work packet

After local validation and index regeneration, a local advisory work packet can be generated for ChatGPT/Codex:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1
```

Optional local Ollama drafting:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -UseOllama
```

Generated reports:

```text
output/ai_pipeline/repository_update_suggestions.json
output/ai_pipeline/repository_update_suggestions.md
```

The packet is advisory only. It must not auto-apply edits. Use it as broader local context for the next AI task after tests.

## Generated Python and Blender script policy

The generated-file policy has layered components:

```text
Tools/validation/generated_file_policy.py
Tools/validation/generated_python_policy.py
Tools/validation/check_generated_python_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

Generic Python policy rules:

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

The Blender adapter protects against the known Blender 5.x failure:

```text
ShaderNodeTexMusgrave undefined
```

## Generated artifact path policy

Generated artifact destination validation answers only:

```text
May a generated artifact be written to this repository path?
```

Default safe destinations are intentionally narrow and reviewable:

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

Explicit generated artifact destination validation:

```powershell
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --path .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
```

Artifact report validation:

```powershell
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
```

## AI pipeline dry-run matrix

Static case-definition validator:

```powershell
python .\Tools\validation\check_ai_dry_run_matrix_cases.py --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
```

Dry-run matrix:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 8 --repeat-cases 1
```

Stress mode for the workstation:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 12 --repeat-cases 2
```

Expected matrix output:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

Post-run validators:

```powershell
python .\Tools\validation\check_ai_pipeline_report_contract.py --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_outputs.py --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
```

## Standard local validation block

Use the PowerShell runner for the full local batch:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
```

Manual core block:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\validation\check_ai_dry_run_matrix_cases.py --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 8 --repeat-cases 1
python .\Tools\validation\check_ai_pipeline_report_contract.py --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_dry_run_matrix_outputs.py --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
python .\Tools\validation\check_package_structure.py --repo-root . --output .\output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output .\output\validation\json_artifacts.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

If only generated index files changed after this block, commit them as:

```powershell
git add Tools/npu/npu_code_context.md `
        Tools/npu/npu_code_index.md `
        Tools/npu/npu_code_manifest.json `
        indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
git push origin master
```
