<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 001 di 004

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

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
AI dry-run matrix evidence bundle checks
AI pipeline schema-v6 report contract checks
GitHub evidence bundle contract checks
selective execution plan contract checks
selected semantic chunks contract checks
repository change proposal contract checks
full-context golden proposal contract checks
proposal patch-spec draft contract checks
reviewed patch-spec dry-run contract checks
AI context pack contract checks
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
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
```

Optional stricter mode after more reports are aligned:

```powershell
python -m Tools.validation check_validation_report_contract --repo-root . --require-recommended --output .\output\validation\validation_report_contract.json
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
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json
python -m Tools.validation check_package_structure --repo-root . --output .\output\validation\package_structure.json
python -m Tools.validation check_json_artifacts --repo-root . --output .\output\validation\json_artifacts.json
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.validation check_execution_plan_status --repo-root . --output .\output\validation\execution_plan_status.json
```

AI pipeline, NPU helper, report-contract and memory checks:

```powershell
python -m Tools.validation check_ai_pipeline_modules --repo-root . --output .\output\validation\ai_pipeline_modules.json
python -m Tools.validation check_npu_pipeline_modules --repo-root . --output .\output\validation\npu_pipeline_modules.json
python -m Tools.validation check_npu_pipeline_helper_tests --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python -m Tools.validation check_ai_model_json --repo-root . --output .\output\validation\ai_model_json.json
python -m Tools.validation check_ai_dry_run_matrix_cases --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
python -m Tools.validation check_ai_pipeline_report_contract --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python -m Tools.validation check_ai_dry_run_matrix_contract --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python -m Tools.validation check_ai_dry_run_matrix_outputs --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python -m Tools.validation check_dry_run_matrix_evidence_bundle --repo-root . --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\ai_pipeline_dry_run_matrix_evidence.json --output .\output\validation\dry_run_matrix_evidence_bundle.json
python -m Tools.validation check_github_evidence_bundle --repo-root . --output .\output\validation\github_evidence_bundle.json
python -m Tools.validation check_selective_execution_plan --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
python -m Tools.validation check_selected_semantic_chunks --repo-root . --bundle .\output\ai_context_packs\full_context_golden_selected_chunks.json --output .\output\validation\full_context_golden_selected_chunks_contract.json --evidence-output .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.json --markdown-output .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.md
python -m Tools.validation check_repository_change_proposals --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals.json --output .\output\validation\repository_change_proposals_contract.json
python -m Tools.validation check_full_context_golden_proposals --repo-root . --proposal .\output\ai_pipeline\full_context_golden_proposals.json --output .\output\validation\full_context_golden_proposals_contract.json --min-proposals 6
python -m Tools.validation check_patch_spec_drafts --repo-root . --manifest .\output\patch_specs\proposal_patch_specs_manifest.json --output .\output\validation\patch_spec_drafts.json
python -m Tools.validation check_reviewed_patch_specs --repo-root . --manifest .\output\patch_specs\reviewed_patch_spec_manifest.json --output .\output\validation\reviewed_patch_specs.json
python -m Tools.validation check_ai_context_pack_contract --repo-root . --pack .\output\ai_context_packs\project_self_improvement.json --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\project_self_improvement_context_pack_evidence.json --output .\output\validation\ai_context_pack_contract.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
python -m Tools.validation check_refactor_status_consistency --repo-root . --output .\output\validation\refactor_status_consistency.json
python -m Tools.validation policy --repo-root . --output .\output\validation\agent_memory_policy.json
```

Blender and generated-file checks:

```powershell
python -m Tools.validation check_blender_shared_compat_smoke --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python -m Tools.validation check_generated_python_policy --repo-root . --output .\output\validation\generated_python_policy.json
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --output .\output\validation\generated_artifact_path_policy.json
python -m Tools.validation check_generated_blender_script_policy --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

## AI workload report quality gate

The AI workload report quality gate validates already-generated AI workload
reports before packet/proposal builders use them as advisory context.

Canonical contract:

```text
docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md
```

Validator:

```powershell
python .\Tools
alidation\check_ai_workload_report_quality.py --repo-root . --output .\output
alidationi_workload_report_quality.json
```

Core report kind and policy:

```text
ai_workload_report_quality
usable_text_lanes_only_for_advisory_context
```

The validator is report-only and must keep:

```text
provider_execution_performed=false
source_writes_performed=false
```

NPU review metadata can be emitted without provider loading:

```powershell
python .\Tools
pu
un_npu_review.py --metadata-only --metadata-out .\output
alidation
pu_review_metadata.json
```

The `npu_review_metadata` sidecar records advisory role and quality-gate status.
Metadata-only mode must keep provider execution disabled.

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
| `check_dry_run_matrix_evidence_bundle.py` | Validates compact Git-trackable dry-run matrix evidence bundles. | No |
| `check_ai_pipeline_report_contract.py` | Validates one schema-v6 AI pipeline report, including dry-run-only semantics when requested. | No |
| `check_github_evidence_bundle.py` | Validates Git-trackable AI/provider evidence bundle shape and decision fields without reading ignored `output/` contents. | No |
| `check_selective_execution_plan.py` | Validates report-only selective execution plan recommendations, local-only command sets and patch-spec candidate boundaries. | No |
| `check_selected_semantic_chunks.py` | Validates selected semantic chunk bundles and can emit compact selected-chunks evidence. | No |
| `check_repository_change_proposals.py` | Validates manual-review repository proposal reports and their code/Markdown/JSON suggestion descriptors. | No |
| `check_full_context_golden_proposals.py` | Validates semantic coverage of full-context golden proposal families beyond the generic repository proposal schema. | No |
| `check_patch_spec_drafts.py` | Validates proposal-derived draft patch specs under `output/patch_specs/` and rejects queued or concrete replacements. | No |
| `check_reviewed_patch_specs.py` | Validates reviewed patch specs and reruns dry-run without writing source files. | No |
| `check_ai_context_pack_contract.py` | Validates AI context packs and compact context-pack evidence without executing providers. | No |
| `check_validation_report_contract.py` | Validates generated reports in `output/validation/` for common root fields. | No |
| `check_refactor_status_consistency.py` | Checks that AI pipeline status markers and docs agree. | No |
| `check_agent_memory/policy.py` | Checks generic memory retention and promotion guardrails. | No |
| `check_blender_shared_compat_smoke.py` | Imports shared Blender compatibility helpers; performs no render. | No render |
| `check_generated_python_policy.py` | Validates generic generated Python syntax and hazard policy. | No |
| `check_generated_artifact_path_policy.py` | Validates generated artifact destination paths. | No |
| `check_generated_blender_script_policy.py` | Validates generated Blender Python scripts before execution. | No |
