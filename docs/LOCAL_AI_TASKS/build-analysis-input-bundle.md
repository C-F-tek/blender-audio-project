# Local AI Task — Build enriched analysis/evidence bundle

## Purpose

Build a Git-trackable evidence bundle that can include the contents the tool considers necessary for review.

The operational input model remains unchanged:

```text
start from Markdown task/runbook
read the current repository state
consume selected local reports/evidence files
```

This task extends the final output bundle. The bundle may include bounded content from Python, Markdown, JSON, TXT, YAML, CSV and other text-like artifacts when the tool or user marks them useful for review.

## Key distinction

Do not change the run input philosophy:

```text
Markdown task -> current repo -> local reports -> evidence bundle
```

Do extend the final bundle output:

```text
summary reports
artifact manifest
selected artifact contents
related Markdown/CSV/JSON outputs
auto-discovered sibling artifacts
explicit artifacts selected by the user
native code patch-plan summaries
```

## Tools

Primary bundle builder:

```text
Tools/ai/repository_product/github_evidence_bundle.py
```

Code patch-plan enrichment post-processor:

```text
Tools/ai/repository_product/github_evidence_bundle_code_plan_enrichment.py
```

Relevant bundle options:

```text
--report                         validation/report JSON input, repeatable or comma-separated
--artifact                       extra file to include with bounded content, repeatable or comma-separated
--no-auto-include-related-artifacts
--max-included-artifact-chars
--max-included-artifacts
--selected-chunks-evidence
```

By default, the bundle may auto-include related sibling/declared artifacts such as matching `.md` files or paths referenced in report `inputs` metadata.

## Build enriched bundle from macro reports

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

$Reports = @(
  ".\output\validation\python_syntax_macro.json",
  ".\output\validation\python_line_count_macro.json",
  ".\output\analysis\code_interpreter_report_macro.json",
  ".\output\validation\artifact_domain_registry_macro.json",
  ".\output\validation\docs_links_macro.json",
  ".\output\validation\markdown_command_hygiene_macro.json",
  ".\output\validation\core_activation_agnostic_contract.json",
  ".\output\validation\agnostic_context_stack_smoke_dryrun.json",
  ".\output\validation\agent_review_code_patch_plan_smoke_macro.json",
  ".\output\validation\code_edit_proposal_smoke_macro.json",
  ".\output\validation\agent_review_code_patch_plan_smoke_macro_built.json",
  ".\output\validation\code_edit_proposal_from_plan_smoke_macro.json",
  ".\output\validation\code_patch_artifact_pack_macro.json",
  ".\output\validation\json_artifacts_macro.json",
  ".\output\validation\validation_report_contract_macro.json",
  ".\output\validation\github_evidence_bundle_macro.json",
  ".\output\validation\code_contract_drift.json",
  ".\output\validation\docs_contract_drift.json"
) | Where-Object { Test-Path $_ }

python -m Tools.ai build_github_evidence_bundle `
  --repo-root . `
  --basename macro_pr108_pr109_validation_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\docs\TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md `
  --artifact .\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md `
  --artifact .\docs\LOCAL_RUNS_TESTING_AND_EVIDENCE.md `
  --max-included-artifact-chars 9000 `
  --max-included-artifacts 60
```

## Add explicit output artifacts when useful

`output/**` files should not be committed directly, but selected contents can be included inside the compact evidence bundle when needed for review.

Example:

```powershell
python -m Tools.ai build_github_evidence_bundle `
  --repo-root . `
  --basename enriched_analysis_review_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\output\patch_specs\agent_review_code_patch_plan_macro.md `
  --artifact .\output\patch_specs\code_edit_proposal_from_plan_macro.md `
  --artifact .\output\validation\artifact_domain_registry_macro.json `
  --artifact .\output\analysis_input\agnostic_code_lane_bundle.md `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 80
```

This keeps raw output files local while preserving review-critical content in a bounded Git-trackable bundle.

## Enrich a bundle with native code patch-plan summary

Use this after generating a bundle that references an `agent_review_code_patch_plan` report, especially the static code plan report.

```powershell
python -m Tools.ai enrich_github_evidence_bundle_code_plan `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\pr109_static_code_plan_bundle_$Stamp.json"
```

Expected decision fields after enrichment:

```text
patch_plan_summary_seen = true
code_patch_plan_summary_enriched_count >= 1
```

The Markdown bundle should also include a native `Patch plan summary` section for the `agent_review_code_patch_plan` report.

## Static code plan bundle example

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

$Reports = @(
  ".\output\validation\python_syntax_pr109.json",
  ".\output\analysis\code_interpreter_report_pr109.json",
  ".\output\validation\artifact_domain_registry_pr109.json",
  ".\output\validation\agent_review_code_patch_plan_with_static_smoke_pr109.json",
  ".\output\validation\code_edit_proposal_from_plan_smoke_pr109.json",
  ".\output\validation\code_patch_artifact_pack_static_pr109.json",
  ".\output\validation\python_line_count_pr109.json",
  ".\output\patch_specs\agent_review_code_patch_plan_with_static_pr109.json"
) | Where-Object { Test-Path $_ }

python -m Tools.ai build_github_evidence_bundle `
  --repo-root . `
  --basename pr109_static_code_plan_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\output\analysis\code_interpreter_report_pr109.md `
  --artifact .\output\patch_specs\agent_review_code_patch_plan_with_static_pr109.md `
  --artifact .\output\patch_specs\code_edit_proposal_from_plan_pr109.md `
  --artifact .\docs\TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md `
  --artifact .\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 80

python -m Tools.ai enrich_github_evidence_bundle_code_plan `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\pr109_static_code_plan_bundle_$Stamp.json"
```

## Disable auto-related inclusion

Use this when you want only explicitly selected artifacts:

```powershell
python -m Tools.ai build_github_evidence_bundle `
  --repo-root . `
  --basename explicit_only_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\docs\TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md `
  --no-auto-include-related-artifacts
```

## Validate bundle

```powershell
python -m Tools.validation check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_pr108_pr109_validation_$Stamp.json" `
  --output ".\output\validation\macro_pr108_pr109_validation_${Stamp}_bundle_validation.json"
```

## Commit policy

Only commit the compact bundle artifacts:

```powershell
git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_pr108_pr109_validation_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_pr108_pr109_validation_$Stamp.md"
```

Do not commit raw `output/**` files.

Do not use:

```powershell
git add .
```

## Stop conditions

Stop if:

```text
bundle validation fails
code patch-plan enrichment fails
bundle includes blocked full_analysis / analysis_full / SQLite / DB content
raw output/** files are staged directly
the included artifact payload becomes too large for review
provider execution is implied by a provider-free run
patch application happened unexpectedly
```
