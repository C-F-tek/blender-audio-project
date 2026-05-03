# AI Patch Bundle Technical Gotchas

## Purpose

This root-level note is for AI assistants and local operators that generate or apply patch bundles in this repository.

Read this before producing ZIP patch bundles, PowerShell workflow patches, Git status parsers or generated patch runners.

The file is intentionally placed at repository root so it is visible early, not buried in `docs/`.

## Current incident log

### 2026-05-03 — triple quote / macro-patch generation failure

A Python script generated a ZIP patch bundle using nested triple-quoted strings that themselves contained Python and PowerShell multiline blocks.

Observed failure:

```text
SyntaxError: invalid syntax
```

Root cause:

```text
outer Python triple quote
  -> embedded Python triple quote
  -> embedded PowerShell / Markdown multiline block
  -> parser boundary collision
```

Operational rule:

```text
Do not generate large patch runners with nested triple-quoted Python strings.
```

Preferred patterns:

```text
1. build file content from explicit list[str] lines and "\n".join(lines)
2. store large replacement templates as separate files inside the ZIP
3. use json.dumps/string escaping for generated Python literals
4. keep PowerShell here-strings out of generated Python source when possible
5. if triple quotes are unavoidable, use a different delimiter level and run py_compile before sharing
```

Bad pattern:

```python
runner = '''
old_block = '''if ($Something) {
    ...
}'''
'''
```

Safer pattern:

```python
lines = [
    "old_block = (",
    "    'if ($Something) {'",
    "    '    ...'",
    "    '}'",
    ")",
]
content = "\n".join(lines) + "\n"
```

### 2026-05-03 — `git status --short` parser failed on `M Tools/...`

A patch-bundle runner attempted to allow an incremental dirty working tree but parsed `git status --short` incorrectly.

Observed input examples:

```text
M Tools/ai/build_repository_consistency_map.py
 M Tools/validation/run_repository_consistency_map_smoke.py
```

The runner used a fixed slice and turned one path into:

```text
ools/ai/build_repository_consistency_map.py
```

Operational rule:

```text
Do not parse short Git status with fragile fixed slicing.
```

Preferred robust options:

```text
1. use `git status --porcelain=v1 -z` and split on NUL
2. support both `XY path` and compact/pasted `X path`
3. handle rename format `old -> new`
4. normalize backslashes to forward slashes
5. print normalized paths before enforcing allowlists
```

Safer regex for non-NUL fallback:

```python
raw = re.sub(r"^[ MADRCU?!]{1,2}\s+", "", line.strip())
raw = raw.strip().strip('"').replace("\\", "/")
if " -> " in raw:
    raw = raw.split(" -> ", 1)[1]
```

### 2026-05-03 — partial patch bundle application

A bundle patched two files successfully, then failed on a later anchor.

Observed result:

```text
M Tools/ai/build_repository_consistency_map.py
M Tools/validation/run_repository_consistency_map_smoke.py
```

Then the incremental fix initially refused to run because it expected a clean tree.

Operational rule:

```text
A recovery bundle must explicitly declare whether it accepts a partially dirty tree.
```

Recovery-bundle policy:

```text
- normal patch bundle: require clean working tree
- incremental recovery bundle: allow dirty tree only for declared target files
- print the current branch
- print the normalized dirty file list
- fail on any dirty file outside the declared target set
- never auto-commit
```

### 2026-05-03 — LF/CRLF warning on PowerShell workflow files

Git reported:

```text
warning: in the working copy of 'Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1', LF will be replaced by CRLF the next time Git touches it
```

Interpretation:

```text
This is a line-ending normalization warning, not automatically a semantic failure.
```

Operational rule:

```text
Do not rewrite whole PowerShell files unnecessarily. Preserve line endings when practical.
```

Suggested follow-up:

```text
Add or review `.gitattributes` for PowerShell files if line-ending churn becomes noisy.
Possible policy:
*.ps1 text eol=crlf
*.py  text eol=lf
*.md  text eol=lf
```

Do not add this policy casually inside unrelated PRs.

### 2026-05-03 — mapper CPU usage around 10 percent

The repository consistency mapper showed low total CPU usage on an Intel Ultra system.

Interpretation:

```text
Low total CPU does not necessarily mean the mapper is broken.
```

Reasons:

```text
- repository scan is partly I/O-bound
- Python regex/text parsing is partly GIL-bound
- AST parsing may not scale with ThreadPoolExecutor
- Windows filesystem/cache behavior can dominate short scans
- 8 workers improves overlap but should not be expected to saturate 24 threads
```

Operational rule:

```text
Use bounded workers by default, not full saturation.
```

Current target policy:

```text
--workers 8
```

If more performance is needed, measure first:

```text
- elapsed_seconds total
- markdown_scan_seconds
- python_inventory_seconds
- markdown_scan_workers
- python_scan_workers
- files scanned per phase
```

Only after measurement consider:

```text
- ProcessPoolExecutor for CPU-heavy Python AST inventory
- separate I/O read phase from AST parse phase
- cache/index reuse
- avoiding duplicate full mapper runs during smoke
```

## Patch-bundle construction rules

### Runner structure

Every patch ZIP should contain:

```text
README.md
manifest.json
run_patch_bundle.py
patches/
```

The runner must:

```text
- find repository root by walking up to `.git`
- print branch name
- validate expected branch when branch-specific
- check working tree policy
- patch only declared target files
- be idempotent or clearly fail before writing
- print resulting line counts for modified scripts
- not commit
- not stage files
- not write generated artifacts intended for commit under `output/**`
```

### Anchor policy

Use exact anchors only when they are stable.

Fragile pattern:

```text
replace one huge multiline block that may already have changed
```

Preferred pattern:

```text
- patch one parameter line
- patch one command argument list
- patch one function with clear start/end markers
- after every transform, assert the intended symbol/argument exists
```

### PowerShell-specific rules

For PowerShell files:

```text
- parse with System.Management.Automation.Language.Parser after patch
- avoid broad format rewrites
- avoid changing BOM/line endings unless intended
- keep backticks only in user-facing commands, not generated patch internals where possible
- validate argument-list commas carefully
```

PowerShell parser validation:

```powershell
$ParseErrors = $null
$Tokens = $null
[System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path ".\Tools\workflow\some_script.ps1"), [ref]$Tokens, [ref]$ParseErrors) | Out-Null
$ParseErrors | Format-List
if ($ParseErrors.Count) { exit 1 }
```

### Python-specific rules

For Python files:

```text
- run `python -m py_compile <changed.py>`
- avoid nested triple quote generation
- prefer list[str] line assembly for generated patch files
- keep large templates as external files when possible
- if modifying AST/regex-heavy tools, add smoke tests and timing fields
```

### Git staging rules

Never use:

```powershell
git add .
git add output
git add .\output
```

Use explicit add lists:

```powershell
git add `
  .\Tools\ai\some_tool.py `
  .\Tools\validation\some_smoke.py `
  .\Tools\workflow\some_runner.ps1
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
*.sqlite-wal
*.sqlite-shm
output/validation/patch_bundles/**
```

## Full-toolbox mapper performance policy

The mapper is now part of the full-toolbox workflow.

Expected behavior:

```text
CPU deterministic scan
  -> repository_consistency_map.json
  -> repository_consistency_map_smoke.json
  -> provider report-file input
  -> decision-loop tool-report input
  -> evidence bundle input
```

Performance rules:

```text
- default to 8 workers on Carmine's Intel Ultra workstation
- do not assume 100 percent CPU utilization is required
- do not rerun expensive scans unnecessarily if a validated map report can be reused
- expose worker/timing metadata in reports
- keep provider execution separate and explicit
```

## Checklist for future AI assistants

Before giving Carmine a patch bundle:

```text
[ ] Did I avoid nested triple-quoted generated source?
[ ] Did I include README.md and manifest.json?
[ ] Does the runner find repo root from `.git`?
[ ] Does it enforce or explicitly relax clean-tree policy?
[ ] If relaxed, does it allow only declared dirty files?
[ ] Does Git status parsing handle `M path`, ` M path`, renames and quoted paths?
[ ] Does it print line counts for modified scripts?
[ ] Does it avoid Blender/Scripting unless explicitly scoped?
[ ] Does it avoid `output/**`, DB and SQLite commits?
[ ] Did I provide PowerShell parse validation for `.ps1` files?
[ ] Did I provide `py_compile` for changed Python files?
[ ] Did I include `git diff --check` and explicit `git add` commands?
```

## Living notes

Append new incidents here when they happen.

Keep entries concrete:

```text
symptom
root cause
safe rule
validation command
```
