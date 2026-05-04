# Workflow

## Purpose

Root operational workflow for `IA-Carmine Local AI Orchestration Workbench`.

This file defines the durable lifecycle. Scenario-specific command blocks live in task runbooks under `docs/LOCAL_AI_TASKS/`; package-specific details live next to the package/tool.

## Canonical lifecycle

```text
read contract
  -> classify task
  -> build inventories/context when useful
  -> choose one scope
  -> change minimal files
  -> validate locally
  -> build compact evidence or patch bundle
  -> open PR
  -> human review / merge
```

## Required reading

```text
AGENTS.md
README.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

For local AI runs, also read `docs/LOCAL_AI_RUN_BOOTSTRAP.md`. For code/provider/refactor work, read the nearest tool/package README and the target source file.

## Provider policy

```text
Ollama -> GPU/CUDA -> primary advisory provider only when explicitly requested and quality-gated
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
Blender runtime -> application target, frozen unless explicitly scoped
```

Provider execution must stay explicit and report-bound.

## Standard preflight

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git fetch origin
git switch <branch-or-master>
git pull --ff-only
git status --short
$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
```

Stop if unrelated local changes are present.

## Inventories before broad review/refactor

Use inventories before planning large documentation or code refactors:

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

Rules:

```text
Markdown inventory -> canonical docs, obsolete docs, generated/evidence docs, missing index review.
Script inventory -> scripts/tools, functions/classes/methods, descriptions, refactor discovery.
```

Do not commit inventory outputs from `output/**`. Commit compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` only when needed for review.

## Focused validation block

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_json_artifacts.py --repo-root . --output .\output\validation\json_artifacts.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
git status --short
```

For full workflow, provider, full-toolbox or code-refactor runs, use the dedicated task runbooks.

## Evidence and patch bundles

Preferred evidence path:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename latest_ai_workflow_evidence
```

Patch application remains manual-review-only unless the user explicitly requests apply. Use the existing full-toolbox patch bundle lane documented in:

```text
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md
```

## Index regeneration

Regenerate generated indexes after structural source/doc/workflow changes only when needed:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Generated index files are not manually maintained source.

## Guardrails

Do not do without explicit approval:

```text
delete files
force-push or rewrite history
merge to master/protected branch
change secrets, permissions, billing or visibility
deploy production
run heavy Blender/GPU workloads automatically
change provider/model execution from explicit to implicit
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
```

## PR report contract

Every PR should state:

```text
changed files
purpose
script line counts for created/modified scripts
validation run or missing
provider/runtime execution status
risk
follow-up
```
