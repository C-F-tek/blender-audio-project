# Local AI Entrypoint: Selected Multistep Review of Workflow and AI Tools for Safe Patch Specs

This is a non-interactive task file for a local AI runner.

This task is intentionally second in sequence after:

```text
docs/LOCAL_AI_TASKS/consistency-local-ai-contracts-and-powershell.md
```

The purpose is to use the local multistep pipeline to review selected workflow and AI tooling files, then propose safe patch-spec candidates. The local AI must not apply patches.

## Absolute first instruction

Before planning, editing, validating, opening a PR or generating proposals, read and obey these files in order:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

Then read this task file again and continue from the task contract below.

If the local AI cannot read `AGENTS.md` or `docs/LOCAL_AI_RUN_BOOTSTRAP.md`, it must stop and report the missing file. It must not infer their contents.

## Task classification

```text
core AI/backend review + validation/evidence + proposal-only patch-spec planning
```

Default provider execution:

```text
allowed only when explicitly requested by the wrapper flags
```

Patch application:

```text
forbidden
```

Patch-spec generation:

```text
allowed only as inert draft patch specs under output/patch_specs/ when -GeneratePatchSpecs is explicitly requested
```

## Goal

Review selected workflow and AI tool files to propose safe, small, validated patch-spec candidates that improve reliability, consistency, validation and local-AI ergonomics.

Primary target groups:

```text
Tools/workflow/*.ps1
ia_carmine/*.py
```

Priority files:

```text
Tools/workflow/run_local_ai_markdown_task.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
ia_carmine/product/repository_product/github_evidence_bundle.py
ia_carmine/context/agent_context/ai_context_pack/cli.py
ia_carmine/runtime/runtime_universe/selective_execution_plan/cli.py
ia_carmine/product/repository_product/repository_change_proposals/cli.py
ia_carmine/product/generated_patch_specs/proposal_cli.py
ia_carmine/product/generated_patch_specs/review_cli.py
ia_carmine/product/repository_product/repository_update_suggestions/cli.py
ia_carmine/_shared/workload_quality.py
```

Reference docs:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_WORKFLOW.md
docs/LOCAL_AI_TASKS/README.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

## Required review themes

The local AI must produce proposals grouped by these themes:

```text
1. PowerShell runner argument safety and placeholder ergonomics.
2. Report-only / proposal-only guardrail enforcement.
3. Explicit provider execution flags and manifest correctness.
4. Multistep heavy-work flow consistency.
5. Evidence bundle decision correctness and schema clarity.
6. Proposal contract consistency and validator coverage.
7. Patch-spec draft generation safety.
8. Dry-run and no-write semantics.
9. Error messages and stop conditions useful for local execution.
10. Documentation-to-code alignment.
```

## Required output from the local AI

The local pipeline must produce a repository proposal report with:

```text
summary
reviewed_files
findings_by_theme
safe_patch_spec_candidates
rejected_or_deferred_candidates
validator_recommendations
risk_notes
next_local_task_suggestions
```

Each patch-spec candidate must include:

```text
candidate_id
title
target_files
change_type: docs_only | script_validation | manifest_schema | runner_ergonomics | evidence_logic | validator_gap
rationale
evidence_source_files
expected_validator_commands
risk_level: low | medium | high
requires_provider_execution: true | false
requires_manual_review: true
apply_allowed_now: false
```

The local AI must explicitly distinguish:

```text
safe docs/example corrections
safe report-only script hardening
validator additions
logic changes that require separate review
changes that must be deferred
```

## Strong guidance for proposals

Prefer small proposals such as:

```text
replace copy-paste-hostile <run>/<task> examples with PowerShell variables
add manifest fields for dry_run and provider execution source
add explicit validation for generated proposal paths
add clearer stop conditions for dirty working tree / missing task files
add docs consistency validator for local task entrypoints
add evidence-builder unit-style fixture for npu_excluded_when_unusable
```

Avoid broad refactors.

Do not propose changes to Blender runtime or artistic scene generation.

## Recommended execution command: multistep provider review

Run through the project-owned local wrapper and adapter:

```powershell
python -m Tools.workflow run_local_ai_markdown_task `
  -TaskFile .\docs\LOCAL_AI_TASKS\selected-review-workflow-ai-tools-patch-specs.md `
  -TaskBranch codex/selected-review-workflow-ai-tools `
  -RunnerCommand 'python -m Tools.workflow run_local_ai_task_via_pipeline -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile npu -RunMultistepProviderWorkflow -RunOllamaProbe -RunNpuProbe -UsePrimaryAdvisoryProvider -BuildEvidence -GeneratePatchSpecs -Basename selected_review_workflow_ai_tools -ProposalBasename selected_review_workflow_ai_tools_proposals -EvidenceBasename selected_review_workflow_ai_tools_evidence -MultistepBasename selected_review_workflow_ai_tools_multistep -MultistepProposalBasename selected_review_workflow_ai_tools_multistep_proposals -MultistepEvidenceBasename selected_review_workflow_ai_tools_multistep_evidence'
```

## Optional proposal-only first pass

For a first pass without provider execution:

```powershell
python -m Tools.workflow run_local_ai_markdown_task `
  -TaskFile .\docs\LOCAL_AI_TASKS\selected-review-workflow-ai-tools-patch-specs.md `
  -TaskBranch codex/selected-review-workflow-ai-tools `
  -RunnerCommand 'python -m Tools.workflow run_local_ai_task_via_pipeline -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}" -Profile docs -Basename selected_review_workflow_ai_tools_report_only -ProposalBasename selected_review_workflow_ai_tools_report_only_proposals'
```

## Required validation after run

Run:

```powershell
python -m Tools.validation check_repository_change_proposals `
  --repo-root . `
  --proposal .\output\local_ai_runs\<actual-run-dir>\pipeline\selected_review_workflow_ai_tools_proposals.json `
  --output .\output\validation\selected_review_workflow_ai_tools_proposals_contract.json

python -m Tools.validation check_patch_spec_drafts `
  --repo-root . `
  --manifest .\output\patch_specs\selected_review_workflow_ai_tools_patch_specs_manifest.json `
  --output .\output\validation\selected_review_workflow_ai_tools_patch_spec_drafts.json

python -m Tools.validation check_github_evidence_bundle `
  --repo-root . `
  --output .\output\validation\github_evidence_bundle.json

python -m Tools.validation check_validation_report_contract `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
```

Replace `<actual-run-dir>` manually with the generated run directory name. Do not paste `<actual-run-dir>` literally into PowerShell.

## Allowed outputs

Allowed tracked outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/selected_review_workflow_ai_tools_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/selected_review_workflow_ai_tools_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/selected_review_workflow_ai_tools_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/selected_review_workflow_ai_tools_multistep_evidence.md
```

Allowed ignored outputs:

```text
output/local_ai_runs/**
output/validation/**
output/ai_packets/**
output/patch_specs/**
```

## Forbidden changes

Do not touch:

```text
Blender runtime
Ready To Jazz
Scripting/shared/blender_compat.py
full analysis JSON
generated indexes manually
provider behavior without explicit scope
prompt prose legacy
models
temperatures
automatic source patch application
automatic merge
```

Do not promote NPU to advisory.

Do not introduce OpenVINO GPU as primary lane.

Do not write source patches from this task unless the user explicitly starts a separate apply/reviewed patch-spec milestone.

## Stop conditions

Stop and report if:

```text
AGENTS.md is missing
LOCAL_AI_RUN_BOOTSTRAP.md is missing
primary target files are missing
draft patch specs request concrete source replacement without reviewed promotion
a generated patch spec attempts to touch forbidden files
a proposal requires provider promotion or implicit provider execution
```

## Final local report

At the end, report:

```text
branch name
run directory
proposal JSON path
proposal Markdown path
patch spec manifest path, if generated
evidence paths
validator results
provider execution statement
patch application statement
top 5 safe patch-spec candidates
recommended next task
```
