<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 003 di 004

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-002.md)
- [Parte successiva](part-004.md)

## NPU pipeline helper validation

Focused import/contract smoke:

```powershell
python -m Tools.validation npu_pipeline_modules_check --repo-root . --output .\output\validation\npu_pipeline_modules.json
```

Focused unit-test report:

```powershell
python -m Tools.validation check_npu_pipeline_helper_tests --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
```

Direct unittest mode, useful while debugging locally:

```powershell
python -m Tools.validation test_npu_pipeline_helpers
```

These tests must remain provider-free and runtime-free. They may use temporary directories, but they must not invoke Blender, NPU, GPU, Ollama, FFmpeg or modify project source files.

## Post-validation AI work packet

After local validation and index regeneration, a local advisory work packet can be generated for ChatGPT/Codex:

```powershell
python -m Tools.workflow run_post_validation_ai_packet
```

The default output path is only a convenience, not an architectural binding:

```text
output/ai_pipeline/repository_update_suggestions.json
output/ai_pipeline/repository_update_suggestions.md
output/ai_pipeline/repository_update_suggestions_manifest.json
```

Profiles:

```powershell
python -m Tools.workflow run_post_validation_ai_packet -Profile core
python -m Tools.workflow run_post_validation_ai_packet -Profile npu
python -m Tools.workflow run_post_validation_ai_packet -Profile docs
```

Custom output name/location:

```powershell
python -m Tools.workflow run_post_validation_ai_packet -Profile npu -OutputDir output/ai_packets -Basename npu_after_tests
```

Extra context and report inputs:

```powershell
python -m Tools.workflow run_post_validation_ai_packet `
  -ContextFile docs/PROJECT_STATUS_POINT.md `
  -ContextFile Tools/npu/run_dual_ai_pipeline.py `
  -ReportFile output/validation/npu_pipeline_modules.json
```

Optional local Ollama drafting:

```powershell
python -m Tools.workflow run_post_validation_ai_packet -UseOllama
```

The packet is advisory only. It must not auto-apply edits. Use it as broader local context for the next AI task after tests.

## Generated Python and Blender script policy

The generated-file policy has layered components:

```text
Tools/validation/_shared/generated_file_policy.py
Tools/validation/_shared/generated_python_policy.py
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
Tools/npu/context_artifacts/npu_code_context.md
Tools/npu/context_artifacts/npu_code_index.md
Tools/npu/context_artifacts/npu_code_manifest.json
```

Explicit generated artifact destination validation:

```powershell
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --path .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
```

Artifact report validation:

```powershell
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
```

## AI pipeline dry-run matrix

Static case-definition validator:

```powershell
python -m Tools.validation check_ai_dry_run_matrix_cases --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
```

Dry-run matrix:

```powershell
python -m Tools.ai pipeline_dry_run_matrix --repo-root . --continue-on-error --matrix-workers 8 --repeat-cases 1
```

Stress mode for the workstation:

```powershell
python -m Tools.ai pipeline_dry_run_matrix --repo-root . --continue-on-error --matrix-workers 12 --repeat-cases 2
```

Expected matrix output:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

Post-run validators:

```powershell
python -m Tools.validation check_ai_pipeline_report_contract --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python -m Tools.validation check_ai_dry_run_matrix_contract --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python -m Tools.validation check_ai_dry_run_matrix_outputs --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
```

Compact evidence bundle for GitHub review:

```powershell
python -m Tools.ai build_dry_run_matrix_evidence_bundle --repo-root . --basename ai_pipeline_dry_run_matrix_evidence
python -m Tools.validation check_dry_run_matrix_evidence_bundle --repo-root . --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\ai_pipeline_dry_run_matrix_evidence.json --output .\output\validation\dry_run_matrix_evidence_bundle.json
```

The evidence bundle verifies that the generated matrix was dry-run-only, every per-case report was present, all steps were planned-only, matrix-level parallelism was used when reported, and no provider execution proof is implied.

## Standard local validation block

Use the PowerShell runner for the full local batch:

```powershell
python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
```

Manual core block:

```powershell
python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json
python -m Tools.validation check_ai_model_json --repo-root . --output .\output\validation\ai_model_json.json
python -m Tools.validation check_ai_pipeline_modules --repo-root . --output .\output\validation\ai_pipeline_modules.json
python -m Tools.validation npu_pipeline_modules_check --repo-root . --output .\output\validation\npu_pipeline_modules.json
python -m Tools.validation check_npu_pipeline_helper_tests --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python -m Tools.validation check_execution_plan_status --repo-root . --output .\output\validation\execution_plan_status.json
python -m Tools.validation check_ai_dry_run_matrix_cases --repo-root . --output .\output\validation\ai_dry_run_matrix_cases.json
python -m Tools.validation check_generated_python_policy --repo-root . --output .\output\validation\generated_python_policy.json
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --output .\output\validation\generated_artifact_path_policy.json
python -m Tools.validation check_generated_blender_script_policy --repo-root . --output .\output\validation\generated_blender_script_policy.json
python -m Tools.validation check_refactor_status_consistency --repo-root . --output .\output\validation\refactor_status_consistency.json
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.validation policy --repo-root . --output .\output\validation\agent_memory_policy.json
python -m Tools.validation check_blender_shared_compat_smoke --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python -m Tools.ai pipeline_dry_run_matrix --repo-root . --continue-on-error --matrix-workers 8 --repeat-cases 1
python -m Tools.validation check_ai_pipeline_report_contract --repo-root . --report .\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json --require-dry-run --output .\output\validation\ai_pipeline_report_contract.json
python -m Tools.validation check_ai_dry_run_matrix_contract --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python -m Tools.validation check_ai_dry_run_matrix_outputs --repo-root . --output .\output\validation\ai_dry_run_matrix_outputs.json
python -m Tools.validation check_generated_artifact_path_policy --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
python -m Tools.ai build_dry_run_matrix_evidence_bundle --repo-root . --basename ai_pipeline_dry_run_matrix_evidence
python -m Tools.validation check_dry_run_matrix_evidence_bundle --repo-root . --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\ai_pipeline_dry_run_matrix_evidence.json --output .\output\validation\dry_run_matrix_evidence_bundle.json
python -m Tools.ai build_selective_execution_plan --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md
python -m Tools.validation check_selective_execution_plan --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
python -m Tools.validation check_package_structure --repo-root . --output .\output\validation\package_structure.json
python -m Tools.validation check_json_artifacts --repo-root . --output .\output\validation\json_artifacts.json
python -m Tools.validation check_github_evidence_bundle --repo-root . --output .\output\validation\github_evidence_bundle.json
python -m Tools.validation check_repository_change_proposals --repo-root . --proposal .\output\ai_pipeline\repository_change_proposals.json --output .\output\validation\repository_change_proposals_contract.json
python -m Tools.validation check_patch_spec_drafts --repo-root . --manifest .\output\patch_specs\proposal_patch_specs_manifest.json --output .\output\validation\patch_spec_drafts.json
python -m Tools.validation reviewed_patch_specs_check --repo-root . --manifest .\output\patch_specs\reviewed_patch_spec_manifest.json --output .\output\validation\reviewed_patch_specs.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
python -m Tools.npu build_project_ai_index
python -m Tools.npu build_npu_code_context
```

If only generated index files changed after this block, commit them as:

```powershell
git add Tools/npu/context_artifacts/npu_code_context.md `
        Tools/npu/context_artifacts/npu_code_index.md `
        Tools/npu/context_artifacts/npu_code_manifest.json `
        indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
git push origin master
```
