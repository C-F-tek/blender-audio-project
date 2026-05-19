# Mapping tool evidence publishing — 2026-05-19

## Scope

This task defines how to run repository mapping tools locally and register useful results on GitHub as compact evidence.

Raw tool outputs stay local under `output/validation/`. GitHub should receive only curated summaries under `docs/LOCAL_VALIDATION_EVIDENCE/` plus task/status Markdown under `docs/LOCAL_AI_TASKS/`.

## Why

The repository contains many script surfaces. The first exhaustive inventory reported:

```text
script_count: 1479
syntax_warning_count: 0
ai_tool: 652
validator: 450
workflow_runner: 148
npu_or_provider_tool: 96
blender_application_script: 78
script: 50
git_helper: 5
```

A manual documentation pass cannot safely cover everything. Mapping must be driven by tool output.

## Mapping tools to run

Run these in local checkout:

```powershell
python -m Tools.validation build_script_inventory
python -m Tools.docs tool_root_inventory
python -m Tools.docs repo_tool_surface_audit
python -m Tools.docs tool_package_family_audit
python -m Tools.docs module_duplication_audit
python -m Tools.validation build_markdown_inventory
python -m Tools.validation check_package_structure
python -m Tools.validation check_python_syntax
```

Use the current repository Python, with fallback to global Python only when `.venv` is absent.

## Output policy

Raw outputs:

```text
output/validation/mapping/*.json
output/validation/mapping/*.csv
output/validation/mapping/*.md
```

Git-trackable compact evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_<stamp>.md
docs/LOCAL_VALIDATION_EVIDENCE/mapping_tool_results_<stamp>.json
```

Do not commit raw `output/**` files by default.

## Required summary fields

The compact GitHub evidence should include:

```text
stamp
repo root
git branch
git head
script inventory counts
tool root inventory summary
repo tool surface audit summary
package family audit summary
module duplication audit summary
markdown inventory summary
package structure result
python syntax result
raw output paths
next documentation targets
```

## Follow-up rule

After publishing the compact evidence, return to Markdown documentation updates:

1. inspect the largest uncovered families from script inventory;
2. add or update `TOOL_CONTEXT.md` files only where the family is meaningful;
3. update `docs/SCRIPT_SURFACE_CONTEXT.md`, `Tools/TOOL_CONTEXT.md`, or area docs as needed;
4. keep raw inventory local unless explicitly promoted to compact evidence.

## Guardrails

This procedure is mapping/documentation only. It must not run Blender, FFmpeg, providers, patch apply, deploy, force-push, merge or destructive cleanup.

Do not commit:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```
