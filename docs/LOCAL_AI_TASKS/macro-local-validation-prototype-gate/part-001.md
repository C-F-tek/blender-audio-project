<!-- IA-CARMINE-MD-SPLIT: part -->
# macro-local-validation-prototype-gate — parte 001 di 002

Sorgente indice: [`../macro-local-validation-prototype-gate.md`](../macro-local-validation-prototype-gate.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

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
PR #109 static code interpreter evidence lane
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
Tools/ai/build_code_interpreter_report.py
Tools/ai/build_code_edit_proposal_from_plan.py
Tools/validation/run_code_edit_proposal_smoke.py
Tools/validation/check_artifact_domain_registry.py
```

`check_core_activation_agnostic_contract.py` statically verifies that the local AI core activation lane still wires full-context orchestration, explicit provider flags, agnostic memory/tool/transient context artifacts, megalithic review stack and manual-review guardrails.

`run_agnostic_context_stack_smoke.py` executes the CPU-only/report-only agnostic context stack smoke: memory inventory, agnostic tool inventory, transient request context, megalithic review, signal refinement and PR draft generation. Use `--dry-run` first when testing branch integration.

`build_agent_review_evidence_sufficiency.py` and `run_agent_review_evidence_sufficiency_smoke.py` classify whether refined review findings are sufficient for manual patch candidates or still need more context. They remain provider-free and patch-free.

`build_python_line_count_csv.py` regenerates deterministic Python line-count evidence after local runs, replacing stale ad-hoc CSV snapshots with a tracked, reproducible command.

`build_code_interpreter_report.py` statically interprets Python code via AST, producing function/class/import/risk/todo/complexity evidence without executing repository code.

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
report-only static code interpretation
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

# Removed obsolete check_markdown_command_hygiene.py command; the script is not tracked in current master. Use check_docs_links.py plus check_validation_report_contract.py for this gate.

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

python .\Tools\ai\build_code_interpreter_report.py `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --output .\output\analysis\code_interpreter_report_pr109.json `
  --markdown-output .\output\analysis\code_interpreter_report_pr109.md

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
