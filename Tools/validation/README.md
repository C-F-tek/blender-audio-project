# Tools/validation

This folder contains lightweight repository validation helpers.

The tools are intentionally non-invasive: they inspect files and write optional reports, but they do not rewrite source code or generated artifacts.

## Available checks

Core repository checks:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

AI artifact pipeline smoke check:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
```

The AI pipeline smoke check imports the modular pipeline, builds representative steps, checks preflight/report helpers and verifies the thin entrypoint is importable. It does not execute NPU, GPU, Blender or FFmpeg workloads.

## Optional reports

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output output\validation\python_syntax.json
python .\Tools\validation\check_package_structure.py --repo-root . --output output\validation\package_structure.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output output\validation\json_artifacts.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output output\validation\ai_pipeline_modules.json
```

## AI pipeline dry-run matrix

The dry-run matrix is located outside this folder because it invokes the pipeline entrypoint multiple times:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Expected matrix output:

```text
output/ai_pipeline/dry_run_matrix_report.json
```

Important fields to inspect:

```text
passed
results[].name
results[].returncode
results[].report_passed
results[].step_count
results[].lanes
```

Each matrix case also writes an individual dry-run report under:

```text
output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json
```

Important fields in individual reports:

```text
passed
summary
schedule
lanes
guardrail_remediation_loop
steps
```

## Standard local validation block

Use this block after structural refactors, documentation changes, or AI pipeline changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
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

## Notes

- `check_python_syntax.py` compiles Python files without importing project modules.
- `check_package_structure.py` reports package-level warnings under `Scripting/`.
- `check_json_artifacts.py` checks JSON parseability and skips very large files by default.
- `check_ai_pipeline_modules.py` is a smoke validator for the modular AI artifact pipeline.
- Validation helpers should not launch Blender renders, GPU generation, NPU model execution or FFmpeg encodes.
