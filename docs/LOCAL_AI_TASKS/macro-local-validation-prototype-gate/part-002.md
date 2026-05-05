<!-- IA-CARMINE-MD-SPLIT: part -->
# macro-local-validation-prototype-gate — parte 002 di 002

Sorgente indice: [`../macro-local-validation-prototype-gate.md`](../macro-local-validation-prototype-gate.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Phase 5 — Contract drift reports

On the branch that contains the contract-drift guide or after locally stacking both active PRs for test only, run:

```powershell
python .\Tools\validation\check_code_contract_drift.py `
  --repo-root . `
  --output .\output\validation\code_contract_drift.json `
  --markdown-output .\output\validation\code_contract_drift.md

python .\Tools\validation\check_docs_contract_drift.py `
  --repo-root . `
  --output .\output\validation\docs_contract_drift.json `
  --markdown-output .\output\validation\docs_contract_drift.md

python .\Tools\validation\check_markdown_command_hygiene.py `
  --repo-root . `
  --output .\output\validation\markdown_command_hygiene.json
```

Expected semantics:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

A failed drift or hygiene report means review is needed. It does not mean apply patches automatically.

## Phase 6 — Optional stacked integration test

Only for local testing, create a temporary branch that stacks PR #108 and PR #109. Do not push unless you explicitly want an integration branch.

```powershell
git switch master
git pull --ff-only origin master
git switch -c local/macro-pr108-pr109-integration

git merge --no-ff --no-commit origin/codex/doc-contract-drift-crossrefs
git merge --no-ff --no-commit origin/codex/design-code-patch-plan-lane
```

If there are conflicts, stop and resolve manually or abort:

```powershell
git merge --abort
```

If clean, inspect staged/working changes:

```powershell
git status --short
git diff --stat
git diff --check
```

Do not merge or test PR #77 here.

Do not commit this local integration branch unless explicitly needed.

## Phase 7 — Macro validator and generator block

Run the non-provider macro block on the stacked local branch or on the active branch you are validating:

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_macro.json

python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output .\output\validation\python_line_count_macro.json `
  --markdown-output .\output\validation\python_line_count_macro.md

python .\Tools\ai\build_code_interpreter_report.py `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --output .\output\analysis\code_interpreter_report_macro.json `
  --markdown-output .\output\analysis\code_interpreter_report_macro.md

python .\Tools\validation\check_artifact_domain_registry.py `
  --repo-root . `
  --output .\output\validation\artifact_domain_registry_macro.json

python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links_macro.json

python .\Tools\validation\check_markdown_command_hygiene.py `
  --repo-root . `
  --output .\output\validation\markdown_command_hygiene_macro.json

python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\Tools\ai\fixtures\agent_review_code_patch_plan_fixture.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_macro.json

python .\Tools\validation\run_code_edit_proposal_smoke.py `
  --repo-root . `
  --proposal .\Tools\ai\fixtures\code_edit_proposal_fixture.json `
  --output .\output\validation\code_edit_proposal_smoke_macro.json

python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\output\validation\code_contract_drift.json `
  --output .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --markdown-output .\output\patch_specs\agent_review_code_patch_plan_macro.md

python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_macro_built.json

python .\Tools\ai\build_code_edit_proposal_from_plan.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --output .\output\patch_specs\code_edit_proposal_from_plan_macro.json `
  --markdown-output .\output\patch_specs\code_edit_proposal_from_plan_macro.md

python .\Tools\validation\run_code_edit_proposal_smoke.py `
  --repo-root . `
  --proposal .\output\patch_specs\code_edit_proposal_from_plan_macro.json `
  --output .\output\validation\code_edit_proposal_from_plan_smoke_macro.json

python .\Tools\ai\build_code_patch_docs_followup.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --output .\output\patch_specs\agent_review_code_docs_followup_macro.json `
  --markdown-output .\output\patch_specs\agent_review_code_docs_followup_macro.md

python .\Tools\ai\build_code_patch_artifact_pack.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --docs-followup .\output\patch_specs\agent_review_code_docs_followup_macro.json `
  --output .\output\validation\code_patch_artifact_pack_macro.json `
  --markdown-output .\output\validation\code_patch_artifact_pack_macro.md

python .\Tools\validation\check_json_artifacts.py `
  --repo-root . `
  --output .\output\validation\json_artifacts_macro.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract_macro.json

python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --output .\output\validation\github_evidence_bundle_macro.json

git diff --check
```

Provider-free expectation:

```text
no Ollama execution
no OpenVINO/NPU execution
no Blender execution
no patch application
no source writes outside report outputs and timestamped compact evidence
```

## Phase 8 — Build compact macro evidence bundle

Use a timestamped basename:

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
  ".\output\validation\agnostic_context_stack_smoke.json",
  ".\output\validation\agent_review_evidence_sufficiency_smoke_macro.json",
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

python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename macro_pr108_pr109_validation_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact .\output\analysis\code_interpreter_report_macro.md `
  --artifact .\output\patch_specs\agent_review_code_patch_plan_macro.md `
  --artifact .\output\patch_specs\code_edit_proposal_from_plan_macro.md `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 80
```

Validate the new bundle:

```powershell
python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_pr108_pr109_validation_$Stamp.json" `
  --output ".\output\validation\macro_pr108_pr109_validation_${Stamp}_bundle_validation.json"
```

## Phase 9 — Prototype gate decision

The prototype gate is green only if:

```text
all required validators passed
fresh python line-count CSV/report generated
static code interpreter report generated
artifact domain registry validation passes
agnostic core activation contract passes
agnostic context stack dry-run passes
agnostic context stack full smoke passes or is explicitly deferred with reason
evidence sufficiency smoke passes or is explicitly skipped because refined-review artifacts are absent
new evidence bundle validates
code patch-plan smoke passes
code edit proposal smoke passes
code edit proposal from plan smoke passes
code docs-follow-up report is generated or explicitly reports no ready follow-up
code patch artifact pack is generated and validates guardrails
no output/** is staged
no DB/SQLite/full analysis JSON is staged
no provider execution was implied by provider-free reports
no Blender runtime was required
manual review found no architectural conflict between #108 and #109
PR #77 remains closed/superseded and no selected-chunks baseline gap was found
```

Inspect before any commit:

```powershell
git status --short
git diff --cached --name-only
```

Only compact evidence may be versioned, and only intentionally:

```powershell
git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_pr108_pr109_validation_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_pr108_pr109_validation_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\python_line_count_$Stamp.csv"
```

Do not use `git add .`.

## Phase 10 — If everything passes

If the macro gate is green, the recommended order is:

```text
1. merge or approve PR #108 first, because it adds contract-drift documentation and index links;
2. rebase/update PR #109 on top of the new master;
3. merge or approve PR #109;
4. only then start a separate prototype implementation branch.
```

Prototype implementation should be separate and may target:

```text
schema docs and validator docs
optional reviewed code/docs patch generated from the report-only queues
```

The following are already part of PR #109:

```text
Tools/ai/build_agent_review_code_patch_plan.py
Tools/ai/build_code_interpreter_report.py
Tools/ai/build_code_edit_proposal_from_plan.py
Tools/ai/build_code_patch_docs_followup.py
Tools/ai/build_code_patch_artifact_pack.py
Tools/ai/code_edit_proposal_helpers.py
Tools/ai/artifact_domain_registry.py
Tools/validation/check_artifact_domain_registry.py
Tools/validation/run_agent_review_code_patch_plan_smoke.py
Tools/validation/run_code_edit_proposal_smoke.py
Tools/validation/build_python_line_count_csv.py
```

Any created or modified Python/PowerShell file must report resulting line count.

## Stop conditions

Stop immediately if:

```text
validator output is not JSON-parseable
python line-count CSV/report generation fails
static code interpreter report fails
artifact domain registry validation fails
contract drift reports show source_writes_performed=true
agnostic core activation contract fails
agent_review_evidence_sufficiency_smoke fails when refined-review inputs are present
agent_review_code_patch_plan smoke report fails
code_edit_proposal_smoke fails
code_edit_proposal_from_plan_smoke fails
agent_review_code_docs_followup reports source_writes_performed=true
code_patch_artifact_pack reports source_writes_performed=true
markdown command hygiene report fails
any output/** file is staged
any generated full analysis JSON is staged
Blender runtime is required
provider execution happened in a provider-free phase
merge conflict appears during stacked local test
PR #77 changes appear in the integration diff
```
