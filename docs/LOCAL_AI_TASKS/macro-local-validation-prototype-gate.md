# Local AI Task — Macro local validation and prototype gate

## Purpose

Run a full local validation gate before promoting the current AI documentation/code-patch-plan work into the prototype path.

This task is intended for Carmine's local workstation, after the documentation-only PRs have been reviewed locally.

General policy reference:

```text
docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md
```

That guide defines the shared rules for GitHub Markdown startup, test runs, effective runs, `output/**` handling, compact evidence bundles and commit policy. This macro task is the concrete PR #108/#109 gate built on top of that general policy.

## Scope

Validate together:

```text
PR #108 contract-drift validation documentation
PR #109 agent-review code patch-plan design/build/smoke/docs-follow-up lane
PR #109 complete code edit proposal helper/build/smoke lane
PR #109 tool-agnostic artifact domain registry
current master local AI evidence-bundle tooling
current master selected-chunks evidence tooling
current master agnostic context stack tooling
current master evidence sufficiency tooling
current local validation/report contracts
fresh Python line-count evidence generated after local runs
```

This task does not authorize merging by itself. It produces evidence and a go/no-go decision for later manual promotion.

## Existing agnostic tools used by this gate

This macro gate intentionally reuses existing agnostic tools instead of duplicating them:

```text
Tools/validation/check_core_activation_agnostic_contract.py
Tools/validation/run_agnostic_context_stack_smoke.py
Tools/ai/build_agent_review_evidence_sufficiency.py
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py
Tools/validation/build_python_line_count_csv.py
Tools/ai/build_code_edit_proposal_from_plan.py
Tools/validation/run_code_edit_proposal_smoke.py
Tools/validation/check_artifact_domain_registry.py
```

`check_core_activation_agnostic_contract.py` statically verifies that the local AI core activation lane still wires full-context orchestration, explicit provider flags, agnostic memory/tool/transient context artifacts, megalithic review stack and manual-review guardrails.

`run_agnostic_context_stack_smoke.py` executes the CPU-only/report-only agnostic context stack smoke: memory inventory, agnostic tool inventory, transient request context, megalithic review, signal refinement and PR draft generation. Use `--dry-run` first when testing branch integration.

`build_agent_review_evidence_sufficiency.py` and `run_agent_review_evidence_sufficiency_smoke.py` classify whether refined review findings are sufficient for manual patch candidates or still need more context. They remain provider-free and patch-free.

`build_python_line_count_csv.py` regenerates deterministic Python line-count evidence after local runs, replacing stale ad-hoc CSV snapshots with a tracked, reproducible command.

`build_code_edit_proposal_from_plan.py` turns a selected `agent_review_code_patch_plan` item into complete `code_edit_proposal` metadata without applying the proposal.

`run_code_edit_proposal_smoke.py` validates complete code edit proposal artifacts without applying patches. It is the smoke gate for future coding-complete proposal lanes.

`check_artifact_domain_registry.py` validates the tool-agnostic artifact domain registry for code, docs, validation, workflow, text, audio, scene spec and provider-result lanes.

## Explicitly out of scope

PR #77 is intentionally out of scope for this macro gate.

Reason:

```text
PR #77 selected-chunks evidence wrapper was superseded by current master.
Current master already contains -BuildSelectedChunksEvidence, -SelectedChunksEvidenceBasename, selected-chunks validation/evidence outputs and adapter manifest fields.
PR #77 was diverged from master and has been closed unmerged.
```

Do not reintroduce PR #77 into the prototype stack unless a new diff proves that a useful, non-duplicated change is missing from `master`.

## Guardrails

Do not perform these actions during this macro gate:

```text
no merge to master unless explicitly commanded
no git add .
no output/** commit
no Blender runtime execution
no provider execution unless a step explicitly says provider probe
no automatic patch apply
no force-push
no SQLite/database commit
no full analysis JSON commit
no NPU advisory promotion
no OpenVINO GPU primary lane
```

Allowed:

```text
local validators
report-only drift checks
report-only evidence sufficiency classification
report-only line-count CSV generation
report-only artifact domain registry validation
report-only code patch-plan generation
report-only code edit proposal generation
report-only code edit proposal smoke validation
report-only docs follow-up generation
report-only code patch artifact packing
CPU-only/report-only agnostic context stack smoke
Git-trackable compact evidence bundle
manual review
small follow-up documentation PR if needed
```

## Phase 0 — Sync and branch state

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git status --short
git log --oneline -5
```

Check PR branches separately:

```powershell
git switch codex/doc-contract-drift-crossrefs
git pull --ff-only origin codex/doc-contract-drift-crossrefs
git status --short

git switch codex/design-code-patch-plan-lane
git pull --ff-only origin codex/design-code-patch-plan-lane
git status --short
```

Optional sanity check that PR #77 remains out of scope:

```powershell
git branch -r --contains origin/codex/wire-selected-chunks-evidence-wrapper
```

Do not switch to or merge `codex/wire-selected-chunks-evidence-wrapper` for this gate.

If either active branch has local uncommitted work, stop and inspect before continuing.

## Phase 1 — Lightweight validators per active PR

Run on PR #108 branch:

```powershell
git switch codex/doc-contract-drift-crossrefs

python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links_pr108.json

python .\Tools\validation\check_markdown_command_hygiene.py `
  --repo-root . `
  --path docs/CONTRACT_DRIFT_VALIDATION.md `
  --path docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md `
  --path docs/README.md `
  --output .\output\validation\markdown_command_hygiene_pr108.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract_pr108.json

git diff --check
```

Run on PR #109 branch:

```powershell
git switch codex/design-code-patch-plan-lane

python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_pr109.json

python .\Tools\validation\check_artifact_domain_registry.py `
  --repo-root . `
  --output .\output\validation\artifact_domain_registry_pr109.json

python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links_pr109.json

python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\Tools\ai\fixtures\agent_review_code_patch_plan_fixture.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_pr109.json

python .\Tools\validation\run_code_edit_proposal_smoke.py `
  --repo-root . `
  --proposal .\Tools\ai\fixtures\code_edit_proposal_fixture.json `
  --output .\output\validation\code_edit_proposal_smoke_pr109.json

python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\Tools\ai\fixtures\code_contract_drift_fixture.json `
  --output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --markdown-output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.md

python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_built_pr109.json

python .\Tools\ai\build_code_edit_proposal_from_plan.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\patch_specs\code_edit_proposal_from_plan_pr109.json `
  --markdown-output .\output\patch_specs\code_edit_proposal_from_plan_pr109.md

python .\Tools\validation\run_code_edit_proposal_smoke.py `
  --repo-root . `
  --proposal .\output\patch_specs\code_edit_proposal_from_plan_pr109.json `
  --output .\output\validation\code_edit_proposal_from_plan_smoke_pr109.json

python .\Tools\ai\build_code_patch_docs_followup.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\patch_specs\agent_review_code_docs_followup_pr109.json `
  --markdown-output .\output\patch_specs\agent_review_code_docs_followup_pr109.md

python .\Tools\ai\build_code_patch_artifact_pack.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --docs-followup .\output\patch_specs\agent_review_code_docs_followup_pr109.json `
  --output .\output\validation\code_patch_artifact_pack_pr109.json `
  --markdown-output .\output\validation\code_patch_artifact_pack_pr109.md

python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --csv-output .\docs\LOCAL_VALIDATION_EVIDENCE\python_line_count_latest.csv `
  --report-output .\output\validation\python_line_count_latest_pr109.json `
  --markdown-output .\output\validation\python_line_count_latest_pr109.md

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract_pr109.json

git diff --check
```

## Phase 2 — Master baseline selected-chunks smoke

Selected-chunks evidence is now treated as current `master` baseline, not as PR #77 content.

Run only if you want to verify that the baseline still works before prototype promotion:

```powershell
git switch master
git pull --ff-only origin master

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
  -PromptFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -RunDir .\output\local_ai_runs\selected_chunks_baseline_smoke `
  -BuildSemanticChunks `
  -SelectSemanticChunks `
  -BuildSelectedChunksEvidence `
  -SelectedChunksBasename selected_chunks_baseline_smoke_focus `
  -SelectedChunksEvidenceBasename selected_chunks_baseline_smoke_evidence `
  -ChunkQuery "contract drift code patch plan selected chunks validation evidence" `
  -ChunkPathBoost Tools/ai,Tools/validation,Tools/workflow,docs `
  -DryRun
```

This command is a dry-run wrapper smoke. It should not execute providers, apply patches, run Blender or commit evidence.

## Phase 3 — Agnostic core/context prechecks

Run the static agnostic core activation contract check:

```powershell
python .\Tools\validation\check_core_activation_agnostic_contract.py `
  --repo-root . `
  --output .\output\validation\core_activation_agnostic_contract.json `
  --markdown-output .\output\validation\core_activation_agnostic_contract.md
```

Then run the agnostic context stack smoke in dry-run mode first:

```powershell
python .\Tools\validation\run_agnostic_context_stack_smoke.py `
  --repo-root . `
  --dry-run `
  --output .\output\validation\agnostic_context_stack_smoke_dryrun.json `
  --markdown-output .\output\validation\agnostic_context_stack_smoke_dryrun.md
```

If the dry-run command shape is correct and you want the full CPU-only/report-only stack smoke, run:

```powershell
python .\Tools\validation\run_agnostic_context_stack_smoke.py `
  --repo-root . `
  --output .\output\validation\agnostic_context_stack_smoke.json `
  --markdown-output .\output\validation\agnostic_context_stack_smoke.md
```

Expected semantics:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
real_github_pr_created = false
sqlite_read_only = true
```

## Phase 4 — Evidence sufficiency classification

If refined megalithic review/proposal files exist from a prior local run, classify whether the evidence is sufficient before generating or promoting patch plans:

```powershell
python .\Tools\validation\run_agent_review_evidence_sufficiency_smoke.py `
  --repo-root . `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review.json `
  --refined-proposals .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_proposals.json `
  --report-file .\output\validation\core_activation_agnostic_contract.json `
  --report-file .\output\validation\agnostic_context_stack_smoke.json `
  --tool-output .\output\ai_pipeline\agent_review_evidence_sufficiency_macro.json `
  --tool-markdown-output .\output\ai_pipeline\agent_review_evidence_sufficiency_macro.md `
  --output .\output\validation\agent_review_evidence_sufficiency_smoke_macro.json `
  --markdown-output .\output\validation\agent_review_evidence_sufficiency_smoke_macro.md
```

If the refined review files are not present, skip this phase and record the skip reason in the final manual notes. Do not synthesize fake refined-review evidence.

Expected semantics:

```text
kind = agent_review_evidence_sufficiency_smoke
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

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
  --report ($Reports -join ',')
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
