# Tools/validation

This folder contains lightweight repository validation helpers.

The tools are intentionally non-invasive: they inspect files and write optional reports, but they do not rewrite source code, generated scripts, generated JSON artifacts, Blender packages, render outputs or FFmpeg outputs.

## Validation model

Validation is split into small deterministic checks:

```text
source/code syntax checks
repository/package structure checks
JSON artifact checks
documentation link checks
AI pipeline smoke checks
agent memory policy checks
Blender compatibility smokes
generated-file policy checks
```

Validators should remain cheap, reviewable and safe to run locally. They must not launch long Blender renders, GPU generation, NPU model execution or FFmpeg encodes.

## Available checks

Core repository checks:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
```

AI pipeline, model-output and memory checks:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
```

Blender and generated-file checks:

```powershell
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

## What each check does

| Tool | Role | Heavy workloads |
|---|---|---|
| `check_python_syntax.py` | Compiles Python files without importing project modules. | No |
| `check_package_structure.py` | Reports package-level structure and warnings under `Scripting/`. | No |
| `check_json_artifacts.py` | Checks JSON parseability; accepts UTF-8 with or without BOM and skips very large files by default. | No |
| `check_docs_links.py` | Validates repository-local Markdown links and ignores external URLs. | No |
| `check_ai_pipeline_modules.py` | Imports modular AI pipeline code, builds representative steps, checks preflight/report helpers and verifies the thin entrypoint. | No |
| `check_ai_model_json.py` | Validates deterministic parsing of JSON-like model output and the legacy Ollama parser wrapper. | No |
| `check_refactor_status_consistency.py` | Checks that AI pipeline status markers and main docs agree on pipeline state and expected modules. | No |
| `check_agent_memory_policy.py` | Checks generic memory retention, quarantine and promotion guardrails; also inspects local SQLite memory DB when present. | No |
| `check_blender_shared_compat_smoke.py` | Imports `Scripting/shared/blender_compat.py`; outside Blender it marks runtime checks skipped, inside Blender it performs no-render compatibility smoke. | No render |
| `check_generated_blender_script_policy.py` | Applies reusable generated-file policy rules to generated Blender Python scripts and deterministic in-memory samples. | No |

## Generated-file policy

The generated-file policy has two layers:

```text
Tools/validation/generated_file_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

`generated_file_policy.py` is input-agnostic and application-agnostic. It does not know whether the source data is WAV, JSON, text, image, CSV, project context or another file type. It also does not know whether the output application is Blender, another Python-scriptable tool, an automation runtime or a custom application.

It provides reusable primitives:

```text
PolicyRule
PolicyFinding
PolicyResult
evaluate_text()
evaluate_paths()
```

The current policy pattern is:

```text
generic generated-file policy engine
  -> generated Python script policy concepts
  -> application-specific adapter
  -> optional input-domain checks only when needed
```

`check_generated_blender_script_policy.py` is the first adapter. It validates generated Blender Python scripts before execution. Blender is not the architectural boundary; it is the first concrete Python-scriptable application target.

Current Blender policy rules:

```text
requires_bpy_import              error
forbid_musgrave_node             error
forbid_open_mainfile             error
forbid_quit_blender              error
warn_save_as_mainfile            warning
warn_python_eval_exec            warning
```

The `forbid_musgrave_node` rule protects against the known Blender 5.x failure:

```text
ShaderNodeTexMusgrave undefined
```

Default sample-only validation:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Explicit generated script validation:

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --path .\output\some_generated_scene.py --output .\output\validation\generated_blender_script_policy.json
```

Future generated Python script adapters should use a new application-specific validator and reuse `generated_file_policy.py`, instead of adding Blender-specific assumptions to the generic layer.

## AI model JSON parser validation

The reusable model-output parser lives at:

```text
Tools/ai/model_json.py
```

The validator checks:

```text
plain JSON object
Markdown fenced JSON object
JSON surrounded by prose
trailing comma repair
line-only // comment repair
JSON array parsing
object-only parser rejection for arrays
invalid text failure
legacy Tools/npu/ollama_runtime.py::parse_json_response() wrapper behavior
```

Command:

```powershell
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
```

## AI pipeline dry-run matrix

The dry-run matrix is located outside this folder because it invokes the pipeline entrypoint multiple times:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Expected matrix output:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

Important fields to inspect:

```text
passed
results[].name
results[].returncode
results[].report_passed
results[].step_count
results[].lanes
results[].agent_state_packet
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
agent_state_packet
guardrail_remediation_loop
steps
```

## Standard local validation block

Use this block after structural refactors, documentation changes, AI pipeline changes, model-output parser changes or generated-file policy changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
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
- `check_json_artifacts.py` checks JSON parseability, accepts UTF-8 with or without BOM and skips very large files by default.
- `check_docs_links.py` checks repository-local Markdown links.
- `check_ai_pipeline_modules.py` is a smoke validator for the modular AI artifact pipeline and schema-v6 report metadata.
- `check_ai_model_json.py` checks reusable model-output JSON parsing and the Ollama parser compatibility wrapper.
- `check_refactor_status_consistency.py` checks status marker and documentation consistency.
- `check_agent_memory_policy.py` checks generic memory retention and promotion guardrails.
- `check_blender_shared_compat_smoke.py` verifies shared Blender compatibility helpers without requiring a render.
- `check_generated_blender_script_policy.py` validates the first generated Python script policy adapter for Blender using the reusable generated-file policy engine.
- Validation helpers should not launch Blender renders, GPU generation, NPU model execution or FFmpeg encodes.
