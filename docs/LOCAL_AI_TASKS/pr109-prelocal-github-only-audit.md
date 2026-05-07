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
# Removed obsolete check_markdown_command_hygiene.py command; the script is not tracked in current master. Use check_docs_links.py plus check_validation_report_contract.py for this gate.
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

### 5. Documentation/task audit status

GitHub-only searches did not find tracked references to the temporary workspace branch name, PR #110 URL, or `codex/refactor-workspace-109` outside this note and PR metadata. No broad documentation rewrite is currently justified.

The broad `Tools/validation/README.md` should still be validated locally because it contains a large number of copy-paste command blocks and at least some command hygiene risk is visible from its size and scope. Do not rewrite it through API before the command hygiene validator reports concrete findings.

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

## Minimal return-home checklist

Run this short path first; fall back to the detailed sections above only if one step fails.

```powershell
# 1. Sync PR branch
git fetch origin
git switch codex/design-code-patch-plan-lane
git pull --ff-only origin codex/design-code-patch-plan-lane

# 2. Check workspace cleanliness
git status --short
git diff --check

# 3. Compile refactored entry points
python -m py_compile .\Tools\ai\github_evidence_bundle_build_github_evidence_bundle_ready.py .\Tools\ai\github_evidence_bundle_io.py .\Tools\ai\github_evidence_bundle_artifacts.py .\Tools\ai\github_evidence_bundle_reports.py .\Tools\ai\github_evidence_bundle_decisions.py .\Tools\ai\github_evidence_bundle_markdown.py .\Tools\ai\code_edit_proposal_helpers.py .\Tools\ai\build_code_interpreter_report.py .\Tools\ai\build_analysis_input_bundle.py .\Tools\validation\check_github_evidence_bundle.py

# 4. Wire replacement-ready orchestrator locally
Copy-Item .\Tools\ai\github_evidence_bundle_build_github_evidence_bundle_ready.py .\Tools\ai\build_github_evidence_bundle.py -Force

# 5. Compile wired orchestrator
python -m py_compile .\Tools\ai\build_github_evidence_bundle.py

# 6. Run focused syntax validation
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax_pr109_after_wiring.json

# 7. Rebuild focused static report
python .\Tools\ai\build_code_interpreter_report.py --repo-root . --input Tools/ai --input Tools/validation --output .\output\analysis\code_interpreter_report_pr109_after_wiring.json --markdown-output .\output\analysis\code_interpreter_report_pr109_after_wiring.md

# 8. Build and validate fresh compact bundle
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"; $Reports = @(".\output\validation\python_syntax_pr109_after_wiring.json", ".\output\analysis\code_interpreter_report_pr109_after_wiring.json") | Where-Object { Test-Path $_ }; python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename pr109_after_wiring_bundle_$Stamp --output-dir docs/LOCAL_VALIDATION_EVIDENCE --report ($Reports -join ',') --artifact .\output\analysis\code_interpreter_report_pr109_after_wiring.md --artifact .\docs\LOCAL_AI_TASKS\pr109-prelocal-github-only-audit.md --max-included-artifact-chars 12000 --max-included-artifacts 80; python .\Tools\validation\check_github_evidence_bundle.py --repo-root . --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\pr109_after_wiring_bundle_$Stamp.json" --output ".\output\validation\pr109_after_wiring_bundle_${Stamp}_validation.json"

# 9. Stage only source wiring and compact evidence
git status --short
git add .\Tools\ai\build_github_evidence_bundle.py .\docs\LOCAL_VALIDATION_EVIDENCE\pr109_after_wiring_bundle_$Stamp.json .\docs\LOCAL_VALIDATION_EVIDENCE\pr109_after_wiring_bundle_$Stamp.md

# 10. Commit and push PR branch
git diff --cached --name-only
git commit -m "refactor(ai): wire github evidence bundle orchestrator"
git push origin codex/design-code-patch-plan-lane
```

## Long touched-file inventory from GitHub metadata

Generated from the PR compare metadata only. Use it to decide what not to edit further through API.

### Do not edit further through GitHub API before local validation

```text
docs/LOCAL_VALIDATION_EVIDENCE/pr109_static_code_plan_bundle_20260502-143630.md — 2829 additions
docs/LOCAL_VALIDATION_EVIDENCE/pr109_code_interpreter_and_agnostic_bundle_20260502-141921.md — 2018 additions
docs/LOCAL_VALIDATION_EVIDENCE/pr109_static_code_plan_bundle_20260502-142630.md — 1956 additions
docs/LOCAL_VALIDATION_EVIDENCE/pr109_static_code_plan_bundle_20260502-143630.json — 1407 additions
docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md — 675 additions
docs/LOCAL_VALIDATION_EVIDENCE/pr109_code_interpreter_and_agnostic_bundle_20260502-141921.json — 530 additions
docs/LOCAL_VALIDATION_EVIDENCE/pr109_static_code_plan_bundle_20260502-142630.json — 500 additions
Tools/ai/build_agent_review_code_patch_plan.py — 499 additions
docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md — 472 additions
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md — 454 additions
docs/TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md — 452 additions
Tools/ai/build_code_interpreter_report.py — 437 additions
Tools/ai/build_github_evidence_bundle.py — 421 changed lines; local wiring pending
```

### Medium-size files: edit only for focused fixes

```text
Tools/ai/build_analysis_input_bundle.py — 304 additions
Tools/ai/build_code_patch_docs_followup.py — 266 additions
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-141635.csv — 266 additions
Tools/ai/build_code_patch_artifact_pack.py — 258 additions
Tools/ai/build_code_edit_proposal_from_plan.py — 250 additions
Tools/ai/enrich_github_evidence_bundle_code_plan.py — 231 additions
docs/LOCAL_AI_TASKS/build-analysis-input-bundle.md — 230 additions
Tools/validation/build_python_line_count_csv.py — 225 additions
docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md — growing runbook; keep edits append-only
Tools/ai/artifact_domain_registry.py — 217 additions
Tools/ai/code_patch_plan_common.py — 216 additions
Tools/ai/github_evidence_bundle_reports.py — 211 additions
Tools/ai/github_evidence_bundle_markdown.py — 209 additions
Tools/validation/run_code_edit_proposal_smoke.py — 203 additions
Tools/validation/run_agent_review_code_patch_plan_smoke.py — 201 additions
Tools/ai/code_edit_proposal_helpers.py — 201 additions
```
