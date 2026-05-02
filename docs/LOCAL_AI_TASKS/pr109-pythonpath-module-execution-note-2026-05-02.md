# PR109 Python module execution note — 2026-05-02

## Purpose

Document the required Python import context for the modularized PR #109 tools.

After the GitHub evidence bundle split, some entry points import repository modules with package-style imports such as:

```python
from Tools.ai.github_evidence_bundle_artifacts import build_included_artifacts
```

When those tools are executed as direct script paths, Python may not include the repository root in `sys.path` and can fail with:

```text
ModuleNotFoundError: No module named 'Tools'
```

## Required PowerShell setup

Before running modular PR #109 tools from the repository root, set `PYTHONPATH` for the current shell:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONPATH
```

Expected value:

```text
C:\Users\carmi\blender\blender-audio-project
```

## Preferred execution style

Prefer module execution for package-style tools:

```powershell
python -m Tools.ai.build_github_evidence_bundle --help
python -m Tools.validation.check_github_evidence_bundle --help
```

Use this instead of direct script execution when a tool imports `Tools.*` modules:

```powershell
# Preferred
python -m Tools.ai.build_github_evidence_bundle ...

# Avoid for modularized Tools.* imports unless PYTHONPATH/import fallback is known good
python .\Tools\ai\build_github_evidence_bundle.py ...
```

## PR109 bundle rebuild example

```powershell
$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

$Reports = @(
  ".\output\validation\python_syntax_pr109_after_wiring.json",
  ".\output\analysis\code_interpreter_report_pr109_after_wiring.json"
) | Where-Object { Test-Path $_ }

python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename pr109_after_wiring_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\output\analysis\code_interpreter_report_pr109_after_wiring.md `
  --artifact .\docs\LOCAL_AI_TASKS\pr109-meta-doc-index-2026-05-02.md `
  --artifact .\docs\LOCAL_AI_TASKS\pr109-pre-return-status-2026-05-02.md `
  --artifact .\docs\LOCAL_AI_TASKS\pr109-evidence-flow.md `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 80

python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\pr109_after_wiring_bundle_$Stamp.json" `
  --output ".\output\validation\pr109_after_wiring_bundle_${Stamp}_validation.json"
```

## Scope

This note is documentation-only. It does not change provider execution, Blender runtime, patch application, evidence policy or merge policy.
