# PatchKit Bundle Contract Validator — 2026-05-09

## Status

Introduces a report-only validator for PatchKit bundle contracts before local dry-run/apply.

This validator strengthens the boundary:

```text
heap/exchange exit product
  -> PatchKit bundle.json
  -> bundle contract validation
  -> PatchKit dry-run
  -> PatchKit apply only by local operator / reviewed branch
```

## Tool

```text
Tools/validation/check_patchkit_bundle_contract.py
Tools/validation/run_patchkit_bundle_contract_smoke.py
```

## Purpose

The validator checks that a `patch_specs/<bundle>/bundle.json` is structurally safe before it reaches `ia_carmine/product/patchkit/apply_patch_bundle.py`.

It does not:

```text
execute providers
apply patches
write source files
delete files
run Blender
run FFmpeg
commit or push
```

It always reports:

```text
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
```

## Checks

The validator verifies:

```text
schema_version=1
kind=codemod_patch_bundle
operations is a list
operation names are supported by current PatchKit
content operations have content or content_file
content_file stays inside the bundle directory
known validators are recorded
forbidden target prefixes are blocked
DB/SQLite target suffixes are blocked
delete_file requires allow_delete=true
delete_file requires required_marker unless missing_ok=true
```

Forbidden target prefixes:

```text
output/
renders/
indexAI/code_chunks/
indexAI/project_code_chunks/
```

Forbidden target suffixes:

```text
.db
.sqlite
.sqlite3
```

## Command

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -m Tools.validation check_patchkit_bundle_contract `
  --repo-root . `
  --bundle .\patch_specs\repo_hygiene_cleanup\bundle.json `
  --output output\validation\repo_hygiene_patchkit_bundle_contract.json `
  --markdown-output output\validation\repo_hygiene_patchkit_bundle_contract.md
```

## Smoke

```powershell
& $RepoPy -m py_compile `
  .\Tools\validation\check_patchkit_bundle_contract.py `
  .\Tools\validation\run_patchkit_bundle_contract_smoke.py

& $RepoPy -m Tools.validation run_patchkit_bundle_contract_smoke --repo-root .

git diff --check
```

## Integration point

For hygiene cleanup, run the contract validator after plan generation and before PatchKit dry-run:

```text
build_repo_hygiene_plan.py
  -> check_patchkit_bundle_contract.py
  -> apply_patch_bundle.py --dry-run
  -> apply_patch_bundle.py
  -> docs/link/line validators
```

## Acceptance

A PatchKit bundle may continue to dry-run when:

```text
check_patchkit_bundle_contract.py passed=true
errors=[]
all destructive operations are explicit and guarded
```

Warnings are review signals, not automatic failure unless future policy tightens them.
