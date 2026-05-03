# Shared Toolbox Refactor Duplication Audit Next Task — 2026-05-03

## Purpose

Use this Markdown as the next concrete AI-to-AI task for the local IA-Carmine pipeline after PR #142.

The goal is to return to the main shared-toolbox implementation work and verify whether the current tooling code contains repeated logic that should be reused, promoted, or refactored before adding more runtime tools.

This is a task request, not a patch instruction. The local IA must produce evidence, recommendations and optional manual-review patch-plan targets only.

## Repository baseline

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
current reference commit: 4cfabf0 feat(ai): add shared toolbox AI-to-AI bundle builder
project: IA-Carmine
workflow: ChatGPT -> MD task -> local IA -> reports/bundle -> ChatGPT review -> manual PR only if approved
```

Required sync before running:

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

Expected:

```text
git status --short is empty
HEAD is master/origin/master at or after 4cfabf0
```

## Read first

Read these files before planning:

```text
docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
docs/LOCAL_AI_TASKS/full-memory-tool-regeneration-procedure.md
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_agent_agnostic_tool_inventory.py
Tools/ai/build_github_evidence_bundle.py
Tools/ai/github_evidence_bundle_artifacts.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py
```

## Architectural rule

Preserve this design rule:

```text
Providers ask.
Orchestrator decides.
Broker executes.
Reports become evidence.
```

The AI must not turn providers into executors and must not put orchestration or broker execution policy inside summary/bundle builders.

## Main objective

Audit the shared-toolbox implementation after PR #142 and answer:

```text
1. Are there duplicated helper functions or repeated logic across Tools/ai and Tools/validation?
2. Which repeated logic should reuse existing helpers?
3. Which local functions should be promoted to existing shared modules?
4. Which repeated logic is intentionally local and should not be refactored?
5. Did PR #142 keep chunking/artifact policy in the shared evidence-bundle layer rather than duplicating it in the shared-toolbox builder?
6. What is the next safe manual-review refactor target, if any?
```

## Mandatory duplication/refactor audit

The local IA must explicitly inspect repeated code, not only file size.

Check for repeated implementations of:

```text
repo-relative path helpers
path resolving helpers
JSON read/write helpers
Markdown rendering helpers
line-count helpers
artifact discovery helpers
chunk/pointer generation helpers
report-only guardrail blocks
CLI argument patterns
validation command generation
runtime tool request packet construction
broker output summarization
```

For every duplication candidate, return:

```text
candidate_id
repeated_logic
files_involved
existing_helper_available
preferred_existing_helper_or_module
recommendation_type
risk
schema_or_cli_impact
validation_required
manual_review_required
```

Allowed `recommendation_type` values:

```text
reuse_existing_helper
promote_existing_function
extract_new_shared_helper
keep_local_by_design
advisory_only
needs_more_context
```

Do not classify anything as ready for implementation unless the target seam is small, the helper destination is clear, and CLI/report schemas can be preserved.

## Refactor verification requirements

Verify the current refactor state using evidence, not intuition:

```text
- compare current touched files from PR #142 against the intended layering
- confirm build_shared_toolbox_ai_to_ai_bundle.py delegates bundle assembly to build_github_evidence_bundle.py
- confirm recursive discovery/chunking belongs to github_evidence_bundle_artifacts.py and/or shared evidence-bundle helpers
- confirm check_github_evidence_bundle remains the validation layer
- confirm run_shared_toolbox_ai_to_ai_bundle_smoke.py covers final summary, bundle validation, recursive discovery and chunk pointers
- identify any remaining large or repeated helpers that should move to report_utils.py, github_evidence_bundle_io.py, github_evidence_bundle_artifacts.py, or an existing local helper module
```

## Guardrails

This task is report-only unless the user explicitly asks for a later implementation PR.

Do not:

```text
execute providers
apply patches automatically
run Blender runtime
write persistent SQLite memory
commit output/**
commit *.db or *.sqlite
change provider/model settings
rewrite prompts broadly
merge to master
```

Allowed outputs are JSON/Markdown/CSV reports under `output/**` and compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/**` only when explicitly selected for review.

## Required tool/evidence run

Start with agnostic and static evidence:

```powershell
python .\Tools\ai\build_agent_agnostic_tool_inventory.py `
  --repo-root . `
  --output ".\output\ai_pipeline\shared_toolbox_refactor_agnostic_tool_inventory_$Stamp.json" `
  --markdown-output ".\output\ai_pipeline\shared_toolbox_refactor_agnostic_tool_inventory_$Stamp.md"

python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\shared_toolbox_refactor_python_line_count_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_refactor_python_line_count_$Stamp.md"

python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/workflow `
  --input Tools/npu `
  --output ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.json" `
  --markdown-output ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.md"

python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_refactor_python_syntax_$Stamp.json"
```

Validate PR #142 smoke coverage still passes on master:

```powershell
python .\Tools\validation\run_shared_toolbox_ai_to_ai_bundle_smoke.py `
  --repo-root . `
  --output ".\output\validation\shared_toolbox_refactor_bundle_smoke_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_refactor_bundle_smoke_$Stamp.md"
```

Optional, use the memory routing policy as request planning evidence only:

```powershell
python .\Tools\ai\agent_memory_routing_policy.py `
  --repo-root . `
  --objective "Audit shared toolbox duplicated code and verify refactoring after PR142." `
  --profile full_refactor `
  --output ".\output\validation\shared_toolbox_refactor_memory_routing_$Stamp.json" `
  --markdown-output ".\output\validation\shared_toolbox_refactor_memory_routing_$Stamp.md"
```

## Required final AI report

The local IA must produce a final report with this structure:

```text
output/analysis/shared_toolbox_refactor_duplication_audit_<STAMP>.json
output/analysis/shared_toolbox_refactor_duplication_audit_<STAMP>.md
```

Required JSON fields:

```text
schema_version
kind = shared_toolbox_refactor_duplication_audit
passed
provider_execution_performed
patch_application_performed
sqlite_write_performed
persistent_memory_write_performed
refactor_verification
duplication_candidates
helper_reuse_recommendations
manual_review_patch_plan_candidates
advisory_only_findings
validation_commands
stop_conditions
errors
warnings
```

`refactor_verification` must include:

```text
layering_preserved
builder_delegates_to_common_bundle
chunking_in_common_evidence_layer
validator_reused
smoke_coverage_present
cli_schema_preserved
report_schema_preserved
```

`duplication_candidates` must not be empty unless the report explains why no duplicated or repeated logic was found.

## Evidence bundle command

Use the post-PR142 builder instead of manual final-summary PowerShell:

```powershell
python -m Tools.ai.build_shared_toolbox_ai_to_ai_bundle `
  --repo-root . `
  --stamp $Stamp `
  --basename "shared_toolbox_refactor_duplication_audit_bundle_$Stamp" `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ".\output\ai_pipeline\shared_toolbox_refactor_agnostic_tool_inventory_$Stamp.json" `
  --report ".\output\validation\shared_toolbox_refactor_python_line_count_$Stamp.json" `
  --report ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.json" `
  --report ".\output\validation\shared_toolbox_refactor_python_syntax_$Stamp.json" `
  --report ".\output\validation\shared_toolbox_refactor_bundle_smoke_$Stamp.json" `
  --report ".\output\analysis\shared_toolbox_refactor_duplication_audit_$Stamp.json" `
  --artifact ".\docs\LOCAL_AI_TASKS\shared-toolbox-refactor-duplication-audit-next-task-2026-05-03.md" `
  --artifact ".\output\analysis\shared_toolbox_refactor_code_interpreter_$Stamp.md" `
  --artifact ".\output\analysis\shared_toolbox_refactor_duplication_audit_$Stamp.md" `
  --validate-bundle
```

The builder may recursively include stamped `.json`/`.md` evidence and should expose chunk pointers for large files. Do not commit raw `output/**` artifacts.

## Stop conditions

Stop and report if any occur:

```text
python syntax validation fails
shared toolbox bundle smoke fails
provider_execution_performed=True during no-provider validation reports
patch_application_performed=True
sqlite_write_performed=True outside explicitly authorized operational scratch semantics
persistent_memory_write_performed=True
refactor recommendation requires CLI/report schema break without migration plan
bundle cannot be built or validated
```

## Commit policy

For this task, the default result is evidence only.

Allowed commit candidates, only if explicitly preparing an evidence PR:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_refactor_duplication_audit_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_refactor_duplication_audit_bundle_<STAMP>.md
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
```

## Expected final answer back to ChatGPT

Return:

```text
1. whether duplicated/repeated code exists
2. top duplication/refactor candidates
3. whether PR #142 layering remains correct
4. recommended next manual-review patch target or advisory_only
5. compact bundle paths
6. exact validation commands executed
7. guardrail booleans
```
