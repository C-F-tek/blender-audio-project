# PR109 pre-local GitHub-only audit

## Scope

This note captures work that can be safely prepared while local workstation access is unavailable.

Branch:

```text
codex/design-code-patch-plan-lane
```

PR:

```text
#109 docs(ai): design manual-review code patch plan lane
```

Temporary workspace PR #110 remains scratch-only and must not be merged.

## Current confirmed constraints

```text
no provider execution
no Blender runtime
no patch auto-apply
no source writes through generated patch runners
no raw output/** commit
no full analysis JSON commit
no SQLite/database commit
no NPU advisory promotion
no OpenVINO GPU primary lane
no merge to master from GitHub-only audit
```

## GitHub-only work completed before this note

- Split GitHub evidence bundle logic into dedicated modules:
  - `Tools/ai/github_evidence_bundle_io.py`
  - `Tools/ai/github_evidence_bundle_artifacts.py`
  - `Tools/ai/github_evidence_bundle_reports.py`
  - `Tools/ai/github_evidence_bundle_decisions.py`
  - `Tools/ai/github_evidence_bundle_markdown.py`
- Added `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` as replacement-ready orchestrator.
- Refactored decision helpers and Markdown renderer into smaller functions.
- Reused promoted helpers across validation and code proposal tooling where safe.
- Left `Tools/ai/build_github_evidence_bundle.py` untouched after the API truncation/corruption risk was identified.

## Remaining hard block

The final wiring must be local:

```powershell
Copy-Item `
  .\Tools\ai\github_evidence_bundle_build_github_evidence_bundle_ready.py `
  .\Tools\ai\build_github_evidence_bundle.py `
  -Force
```

Do not perform this replacement through GitHub API unless the file can be updated from a complete verified buffer.

## Candidate local validation sequence after returning home

```powershell
git fetch origin
git switch codex/design-code-patch-plan-lane
git pull --ff-only origin codex/design-code-patch-plan-lane

git status --short
git diff --check
```

Compile the files touched by GitHub-only refactors:

```powershell
python -m py_compile `
  .\Tools\ai\github_evidence_bundle_io.py `
  .\Tools\ai\github_evidence_bundle_artifacts.py `
  .\Tools\ai\github_evidence_bundle_reports.py `
  .\Tools\ai\github_evidence_bundle_decisions.py `
  .\Tools\ai\github_evidence_bundle_markdown.py `
  .\Tools\ai\github_evidence_bundle_build_github_evidence_bundle_ready.py `
  .\Tools\ai\code_edit_proposal_helpers.py `
  .\Tools\ai\build_code_interpreter_report.py `
  .\Tools\validation\check_github_evidence_bundle.py
```

Then perform the local orchestrator replacement and compile again:

```powershell
Copy-Item `
  .\Tools\ai\github_evidence_bundle_build_github_evidence_bundle_ready.py `
  .\Tools\ai\build_github_evidence_bundle.py `
  -Force

python -m py_compile .\Tools\ai\build_github_evidence_bundle.py
```

## Focused validation after wiring

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_pr109_after_wiring.json

python .\Tools\ai\build_code_interpreter_report.py `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --output .\output\analysis\code_interpreter_report_pr109_after_wiring.json `
  --markdown-output .\output\analysis\code_interpreter_report_pr109_after_wiring.md

python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --output .\output\validation\github_evidence_bundle_pr109_after_wiring.json
```

## Bundle rebuild after wiring

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

$Reports = @(
  ".\output\validation\python_syntax_pr109_after_wiring.json",
  ".\output\analysis\code_interpreter_report_pr109_after_wiring.json",
  ".\output\validation\github_evidence_bundle_pr109_after_wiring.json"
) | Where-Object { Test-Path $_ }

python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename pr109_after_wiring_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\output\analysis\code_interpreter_report_pr109_after_wiring.md `
  --artifact .\docs\LOCAL_RUNS_TESTING_AND_EVIDENCE.md `
  --artifact .\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 80

python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\pr109_after_wiring_bundle_$Stamp.json" `
  --output ".\output\validation\pr109_after_wiring_bundle_${Stamp}_validation.json"
```

## Additional project-level findings

### 1. Validation README may need hygiene review

`Tools/validation/README.md` is very broad and contains many canonical command blocks. It should be checked locally with the Markdown command hygiene validator before more edits are made.

Recommended local command:

```powershell
python .\Tools\validation\check_markdown_command_hygiene.py `
  --repo-root . `
  --output .\output\validation\markdown_command_hygiene_pr109.json
```

### 2. Helper promotion should pause until syntax validation

The following helpers have already been promoted/reused:

```text
repo_relative
split_path_values
sha256_file
read_text
line_count
default_validation_commands_for
```

Further promotion candidates exist, but should wait for local `py_compile` and validator results:

```text
read_json_object
resolve_repo_path
compact_value
report_only_guardrails
```

### 3. Evidence bundle validator should remain backward compatible

New decision fields are intentionally optional:

```text
artifact_manifest_built
included_artifacts_built
included_artifact_count
patch_plan_summary_seen
```

They should remain warnings/check metadata only until all historical evidence bundles are regenerated.

### 4. PR #110 should be closed only after PR #109 has local evidence

The workspace PR has served its purpose as a scratch area. Do not merge it. Close it after PR #109 has:

```text
local syntax validation
fresh focused bundle
manual review of wiring commit
```

## Recommended next GitHub-only work if local access is still unavailable

Safe candidates:

```text
create or update small task/runbook notes
inspect docs for stale branch names or contradicted guardrails
review evidence bundle JSON/Markdown already committed
check PR metadata and changed file inventory
```

Avoid until local access:

```text
large file replacements
build_github_evidence_bundle.py final wiring
renaming modules
editing long README files through API
schema-breaking validator changes
```
