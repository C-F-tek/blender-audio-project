# Validator and smoke cycle map — 2026-05-07

Status: active code-driven validation map  
Scope: validator families, smoke strategy and validation cycles.

This document is the compact navigation layer for `Tools/validation/`. The long `Tools/validation/README.md` remains a catalog; this file tells operators which validation cycle to run.

## Validation owner rule

Do not replace validators with ad-hoc checks when an owner already exists.

```text
Python syntax -> check_python_syntax.py
report contracts -> check_validation_report_contract.py
docs links -> check_docs_links.py
file line limits -> check_file_line_limits.py
patch suggestion product separation -> check_patch_suggestion_product_separation.py
patch suggestion dry/apply smoke -> run_patch_suggestion_bundle_apply_smoke.py
Full0To10 product PR chain smoke -> run_full0to10_product_pr_chain_smoke.py
runtime broker smoke -> run_agent_runtime_tool_broker_smoke.py
peer exchange contract -> check_ai_peer_exchange_contract.py
provider evidence contract -> check_provider_evidence_contract.py
repository consistency smoke -> run_repository_consistency_map_smoke.py
```

## Cycle A: docs-only change

Use for Markdown-only changes.

```text
check_docs_links.py
check_file_line_limits.py when touching line policy or large Markdown
git diff --check
```

No provider execution is required.

## Cycle B: Python/script change

Use for code changes that do not alter provider runtime semantics.

```text
python -m py_compile for touched files
check_python_syntax.py
focused smoke for the modified family
check_validation_report_contract.py
git diff --check
line count for touched scripts
```

## Cycle C: launcher/workflow change

Use for `Tools/workflow` changes.

```text
PowerShell parser check for touched .ps1 files
no-strict launcher smoke for the touched mode
manifest inspection
check_validation_report_contract.py
Full0To10 or LightFull0To10 only when validating real full behavior
```

Single-mode diagnostics must include:

```text
-NoStrictRealRunActivation
```

## Cycle D: provider mesh change

Use for GPU1/GPU0/NPU/broker/provider changes.

```text
provider-capable Python preflight
check_local_resource_lanes.py or run_local_provider_probe.py
run_gpu_planner_json_contract_smoke.py
run_agent_runtime_tool_broker_smoke.py
check_ai_peer_exchange_contract.py
check_provider_evidence_contract.py
runtime heap / telemetry report inspection
```

Provider-capable Python preflight:

```powershell
$env:IA_CARMINE_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path
& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; print(Core().available_devices)"
```

Expected IA-Carmine workstation device visibility:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

## Cycle E: patch suggestion / review PR change

Use for patch suggestion, deterministic apply and review PR flow.

```text
run_patch_suggestion_bundle_apply_smoke.py
run_full0to10_product_pr_chain_smoke.py
check_patch_suggestion_product_separation.py
apply_patch_suggestion_bundle.py dry-run by Stamp
prepare_review_pr.py report inspection when used
check_python_syntax.py for touched Python files
git diff --check
```

Current code requires explicit include paths for review PR staging:

```text
ReviewPrIncludePath / prepare_review_pr.py --include-path
```

`run_full0to10_product_pr_chain_smoke.py` is the focused "all together" smoke
for the product path. It runs in a temporary git repo and verifies:

```text
task Markdown patch_suggestion extraction
deduped deterministic apply by Stamp plus explicit suggestion report
product separation validation with --require-product
canonical launcher workflow trace for the same product phases
review branch preparation and product commit
no push and no real GitHub PR from the smoke
```

## Cycle F: context/memory/index change

Use for context packs, semantic chunks, agent state and memory.

```text
check_selected_semantic_chunks.py
check_ai_context_pack_contract.py
check_agent_memory_policy.py
check_validation_report_contract.py
```

SQLite DB outputs are local/private and must not be committed.

## Cycle G: generated artifact policy change

Use for generated path, generated Python or Blender-script policy changes.

```text
check_generated_python_policy.py
check_generated_blender_script_policy.py
check_generated_artifact_path_policy.py
check_validation_report_contract.py
```

No Blender runtime or FFmpeg runtime is allowed unless explicitly scoped.

## Common report contract

Validators should write reports with these root fields:

```text
schema_version
kind
repo_root
passed
errors
warnings
```

Meta-validator:

```powershell
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
```

## Output policy

```text
output/** = generated reports, do not commit
*.db / *.sqlite / *.sqlite3 = local/private, do not commit
docs/LOCAL_VALIDATION_EVIDENCE/** = compact evidence, commit only when useful
```

## When uncertain

Read in this order:

```text
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
this document
Tools/validation/README.md
source validator
```
