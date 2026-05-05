<!-- IA-CARMINE-MD-SPLIT: part -->
# PROJECT_AI_CONSCIOUSNESS — parte 002 di 002

Sorgente indice: [`../PROJECT_AI_CONSCIOUSNESS.md`](../PROJECT_AI_CONSCIOUSNESS.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Implemented validation foundation

Current validators:

| Tool | Role |
|---|---|
| `Tools/validation/check_python_syntax.py` | Compiles Python files without importing them. |
| `Tools/validation/check_package_structure.py` | Inspects Blender package folders under `Scripting/`. |
| `Tools/validation/check_json_artifacts.py` | Checks JSON parseability without rewriting artifacts; accepts UTF-8 with or without BOM. |
| `Tools/validation/check_ai_pipeline_modules.py` | Smoke-checks modular AI pipeline imports, step builders, preflight and report generation without heavy workloads. |
| `Tools/validation/check_ai_model_json.py` | Validates reusable model-output JSON parser and Ollama legacy wrapper behavior. |
| `Tools/validation/check_ai_dry_run_matrix_contract.py` | Validates the AI dry-run matrix report contract without running the matrix. |
| `Tools/validation/check_refactor_status_consistency.py` | Checks that duplicated AI pipeline refactor status remains consistent across docs and code. |
| `Tools/validation/check_docs_links.py` | Checks internal documentation links after doc changes. |
| `Tools/validation/check_agent_memory_policy.py` | Checks local agent memory policy and optional generated memory DB state. |
| `Tools/validation/check_blender_shared_compat_smoke.py` | Runs a Blender no-render compatibility smoke when Blender is available. |
| `Tools/validation/check_generated_python_policy.py` | Validates generic generated Python syntax and warning policy without application assumptions. |
| `Tools/validation/check_generated_blender_script_policy.py` | Validates the first generated Python script policy adapter for Blender by composing generic Python rules with Blender rules. |
| `Tools/validation/check_npu_pipeline_modules.py` | Checks app-agnostic NPU helper imports, contracts, compatibility aliases and readiness gates. |
| `Tools/validation/check_npu_pipeline_helper_tests.py` | Runs deterministic unit tests for NPU helper modules and emits a JSON validation report. |
| `Tools/validation/check_npu_pipeline_docs.py` | Checks NPU helper README/module alignment. |

Preferred local validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

Generic agent state packet smoke:

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan generic generated Python validation" --include-file .\docs\QUALITY_GATE.md --include-file .\Tools\validation\README.md
```

Optional persistent memory can use SQLite without external dependencies:

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan generic generated Python validation" --memory-db .\indexAI\agent_memory\agent_memory.sqlite --save-inputs-to-memory-db --memory-note "Keep input-domain policy separate from output-application policy."
```

Memory retention and promotion review:

```powershell
python .\Tools\ai\review_agent_memory.py --repo-root .
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
```

Blender shared compatibility smoke:

```powershell
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
```

Generated Blender script policy smoke:

```powershell
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
```

```powershell
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
```

Unattended validation runner:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

Add new validators to the unattended runner only after focused smoke validation shows they are cheap, deterministic and non-rendering.

## Generated index policy

After documentation or structural changes, regenerate:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Expected generated files:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

If only these files changed after regeneration, that is expected.

## Patch-spec capability

The repository contains an advanced patch runner:

```text
Tools/repo_patch_runner/apply_repo_mods.py
patch_specs/inbox/
patch_specs/applied/
.github/workflows/apply_repo_mods.yml
```

Use it for small, mechanical, reviewable edits.

Capabilities:

- dry-run;
- exact replacement;
- regex replacement;
- insert before/after anchor;
- path safety checks;
- before/after content validation;
- optional backup;
- line count summary;
- optional git diff display;
- GitHub Action queue through `patch_specs/inbox/*.json`.

## High-priority next tasks

1. Validate the active NPU helper batch locally using the focused helper runner and the full local validation runner.
2. Regenerate AI/NPU indexes after the NPU helper batch validation.
3. If the batch is green, merge it and start a narrow runtime-wiring phase for IO helpers only.
4. Keep generated Python script policy input-agnostic and application-agnostic; Blender remains only the first adapter.
5. Continue formal JSON/report contracts without changing existing schema-v6 field meanings.
6. Continue `TD-010` only after schema/report contracts remain stable; do not inject agent packets into prompts yet.
7. Select one non-critical `Scripting/shared/blender_compat.py` call-site pilot only after confirming the no-render smoke result on the workstation.
8. Keep `TD-001` PowerShell runner compatibility under review when changing validation commands.
9. Evaluate CI/GitHub Actions only after the local runner remains stable and the intended checks are cheap, deterministic and non-rendering.

## Avoid now

Do not do these without explicit instruction:

```text
rewrite Scripting/v61b/main_v61b.py
split Ready To Jazz monolithic script
remove v61b_backgood before checking if it contains unique fixes
change Blender render behavior
change final FFmpeg output behavior
add dependencies without validation
modify generated full analysis JSON files
run long Blender renders or GPU generation automatically
change AI pipeline schema-v6 field meanings without local dry-run matrix validation
mass-migrate runtime packages to Scripting/shared/blender_compat.py
wire Tools/npu/pipeline/ helpers into Tools/npu/run_dual_ai_pipeline.py before focused validation, full validation and index regeneration
add AI GitHub Actions that call paid or external model APIs automatically
use prompt-based repair for JSON parsing as a default path
turn generic generated-file policy into Blender-only or WAV-only logic
mix input-domain validators with output-application validators without a clear adapter boundary
```

## Reporting format for AI agents

Every implementation response should include:

```text
changed files
purpose
resulting line count for every created or modified script
validation commands run
validation result
risks
next recommended action
```

## Mental model

The project should be treated as a production pipeline, not a demo.

Correct posture:

```text
stability first
small patches
generic utility before adapter
input-domain logic separate from output-application logic
shared utilities before migration
validation before commit
indexes regenerated after structure changes
proof-of-work reports for agentic work
execution plans for multi-step work
technical debt tracked instead of rediscovered
```
