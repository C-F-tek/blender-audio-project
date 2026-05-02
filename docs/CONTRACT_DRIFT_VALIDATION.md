# Contract Drift Validation

## Purpose

This document defines how IA-Carmine tracks drift between documented AI workflow contracts and the code that implements or validates those contracts.

The contract-drift lane is evidence-first and report-only. It helps local and GitHub-only agents decide whether documentation, validators or orchestration code have moved out of sync, without executing providers or applying patches automatically.

## Current validators

| Validator | Kind | Role |
|---|---|---|
| `Tools/validation/check_code_contract_drift.py` | `code_contract_drift` | Checks that important Python and PowerShell tools still expose the guardrail strings, symbols and lane contracts required by the local AI core/tool workflow. |
| `Tools/validation/check_docs_contract_drift.py` | `docs_contract_drift` | Checks that central Markdown documents mention required workflow, provider and report-contract terms. |
| `Tools/validation/apply_docs_contract_drift_fixes.py` | explicit docs fixer | Applies only narrow documentation fixes when explicitly run with its apply flag; it is not a generic patch runner. |

All of these tools must remain:

```text
provider-free
Blender-runtime-free
output/**-free for committed artifacts
manual-review-only for promotion
non-destructive by default
```

## Code contract drift

`code_contract_drift` is a static report over source files. It is useful after local AI/core tooling changes, provider-lane routing changes or patch-plan workflow changes.

Recommended command:

```powershell
python .\Tools\validation\check_code_contract_drift.py `
  --repo-root . `
  --output .\output\validation\code_contract_drift.json `
  --markdown-output .\output\validation\code_contract_drift.md
```

Expected report semantics:

```text
kind = code_contract_drift
apply_mode = report_only_manual_review_only
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

A failed report is not an instruction to patch automatically. It is a queue of manual-review suggestions.

## Documentation contract drift

`docs_contract_drift` checks whether central documents still advertise the current local AI workflow, workload quality gate and manual-review evidence route.

Recommended command:

```powershell
python .\Tools\validation\check_docs_contract_drift.py `
  --repo-root . `
  --output .\output\validation\docs_contract_drift.json `
  --markdown-output .\output\validation\docs_contract_drift.md
```

Expected report semantics:

```text
kind = docs_contract_drift
apply_mode = report_only
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

If a documentation fix is needed, prefer a small PR that updates the affected Markdown and includes the validator output in the local evidence bundle.

## Relationship with patch plans

Contract-drift reports are upstream signals for patch-plan work. They are not patch plans by themselves.

Safe sequence:

```text
contract drift report
  -> human/AI review
  -> manual-review patch plan
  -> small documentation or code PR
  -> validators
  -> compact evidence bundle
```

For documentation patch plans, use the existing agent-review lane:

```text
docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md
Tools/validation/run_agent_review_patch_plan_full_validation.py
```

For future code patch plans, keep the default design stricter:

```text
agent_review_code_patch_plan
report_only_manual_review_code_patch_plan
manual_review_required = true
patch_application_performed = false
source_writes_performed = false by default
```

## Line-count evidence

The repository currently includes this line-count evidence file:

```text
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv
```

It is useful for prioritizing review effort and spotting large/high-risk files. It is not necessarily current after later commits, so treat it as a sizing hint, not as authoritative state.

Observed examples from that CSV:

| File | Lines | Meaning |
|---|---:|---|
| `Tools/npu/run_dual_ai_pipeline.py` | 1577 | Large NPU/AI orchestrator; avoid broad edits without local validation. |
| `Tools/workflow/workflow_state.py` | 1071 | Large workflow state module; prefer targeted patches. |
| `Tools/validation/check_code_contract_drift.py` | 360 | Existing code-contract drift validator. |
| `Tools/validation/check_docs_contract_drift.py` | 232 | Existing documentation-contract drift validator. |
| `Tools/validation/apply_docs_contract_drift_fixes.py` | 269 | Explicit docs fixer; do not treat as generic patch apply. |

When using the CSV:

```text
use it to choose review order
verify current file content before patching
regenerate it locally after structural code changes
commit only compact evidence, not output/** raw reports
```

## Evidence bundle usage

After running drift validators and any related patch-plan validators, build a compact bundle with the updated evidence bundle builder:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename contract_drift_validation_evidence_<stamp> `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\validation\code_contract_drift.json `
  --report .\output\validation\docs_contract_drift.json `
  --report .\output\validation\validation_report_contract.json `
  --report .\output\validation\python_syntax.json
```

Commit only the generated compact evidence files under `docs/LOCAL_VALIDATION_EVIDENCE/` when they are part of a reviewed task.

## Guardrails

Do not use contract drift reports to justify:

```text
implicit provider execution
automatic patch application
Blender runtime execution
OpenVINO GPU as primary lane
NPU advisory promotion
creation of runtime files only because a stale document mentions them
committing output/**
```

The correct promotion model is small, reviewed, validator-backed PRs.
