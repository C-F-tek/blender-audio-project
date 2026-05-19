# Exhaustive script surface inventory — 2026-05-19

## Scope

The previous context pass mapped important script areas, but it was not an exhaustive file-by-file script inventory. The repository contains more scripts than the documented area examples.

This task defines the correct next step: generate a complete script inventory from the repository itself, then update context documents from that inventory.

## Source of truth

Use the existing report-only inventory tool:

```powershell
python -m Tools.validation build_script_inventory `
  --repo-root . `
  --output output/validation/script_inventory.json `
  --csv-output output/validation/script_inventory.csv `
  --markdown-output output/validation/script_inventory.md `
  --markdown-max-rows 500
```

The tool scans source scripts with suffixes:

```text
.py
.ps1
.sh
.bat
.cmd
```

and categorizes paths such as:

```text
Tools/validation/** -> validator
Tools/workflow/**   -> workflow_runner
Tools/ai/**         -> ai_tool
Tools/npu/**        -> npu_or_provider_tool
Tools/git/**        -> git_helper
Scripting/**        -> blender_application_script
examples/**         -> example
test* or */test*    -> test_or_fixture
other               -> script
```

## Why this is required

Manual GitHub search and area-level documentation are not enough. They miss:

- nested package CLIs;
- PowerShell wrappers;
- split workflow script parts;
- Blender scripts outside `Tools`;
- generated or template package scripts;
- root-level or examples scripts;
- shell/batch helpers;
- validators and fixtures that are not exposed as top-level dispatch names.

## Required local run

Run from the working checkout. This command is degradable: it uses `.venv` when present, then `py -3`, then `python` from PATH.

```powershell
cd "C:\Users\carmi\ProjectsDir\blender-audio-project"

git switch master
git pull --ff-only origin master

$RepoRoot = (Resolve-Path .).Path
$VenvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (Test-Path $VenvPy) {
  $RepoPy = $VenvPy
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $RepoPy = (py -3 -c "import sys; print(sys.executable)").Trim()
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $RepoPy = (Get-Command python).Source
} else {
  throw "Python non trovato: crea .venv oppure installa Python 3."
}

$env:PYTHONPATH = $RepoRoot
Write-Host "RepoPy=$RepoPy" -ForegroundColor Cyan
& $RepoPy --version

& $RepoPy -m Tools.validation build_script_inventory `
  --repo-root . `
  --output output/validation/script_inventory.json `
  --csv-output output/validation/script_inventory.csv `
  --markdown-output output/validation/script_inventory.md `
  --markdown-max-rows 500
```

Optional quick summary:

```powershell
$inv = Get-Content output/validation/script_inventory.json -Raw | ConvertFrom-Json
$inv | Select-Object kind, passed, script_count, syntax_warning_count
$inv.category_counts
```

## Do not commit raw inventory output by default

The generated files under `output/validation/` are runtime/validation artifacts and should normally remain local:

```text
output/validation/script_inventory.json
output/validation/script_inventory.csv
output/validation/script_inventory.md
```

If a compact evidence artifact is needed later, build or copy a curated summary under `docs/LOCAL_VALIDATION_EVIDENCE/` instead of committing raw output.

## Documentation update rule

After the generated inventory exists:

1. group by category;
2. identify scripts not covered by existing `TOOL_CONTEXT.md` files;
3. add missing context files only for meaningful families;
4. update `docs/SCRIPT_SURFACE_CONTEXT.md` with discovered non-Tools families;
5. update `Tools/TOOL_CONTEXT.md` or area docs only when dispatcher/package roles changed;
6. keep raw inventory local unless explicitly promoted to compact evidence.

## Expected next candidates from inventory

Likely groups to inspect after running the inventory:

```text
Tools/workflow/run_unified_local_ai_refactor/** split ps1 parts
Tools/workflow/_powershell/** wrappers
Tools/validation/** nested validators not yet described
Tools/ai/provider_runtime_blackboard/**
Tools/ai/external_heap/**
Tools/ai/repository_product/**
Tools/ai/agent_review/**
Tools/ai/generated_patch_specs/**
Scripting/** package-local scripts
examples/** or root-level scripts, if present
```

## Guardrails

This task is inventory/documentation only.

Do not run Blender, FFmpeg, providers, patch apply, Git push automation or destructive cleanup as part of the inventory.
