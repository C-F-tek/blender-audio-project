# Patch suggestion bundle final phase

Status: active implementation note for the unified launcher product loop  
Scope: IA-Carmine Full0To10, AI-to-AI bundle/evidence/telemetry, deterministic patch suggestions, draft review PR.

## Canonical product interface

The operator-facing product interface is the unified launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

This document describes the internal patch-suggestion family used by that launcher. It is not a second operator runbook and it must not override:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
AGENTS.md
```

## Product loop

The complete product loop is:

```text
Task Markdown input
-> unified launcher Full0To10 run
-> context/chunks/agent-state preparation
-> GPU1 primary advisory/planner
-> GPU0 OpenVINO companion peer worker
-> NPU non-blocking micro/tool-support lane
-> runtime broker tool execution
-> runtime heap / blackboard evidence
-> deterministic repository validators
-> raw reports under output/**
-> compact AI-to-AI bundle, telemetry and evidence
-> deterministic patch suggestion extraction
-> safe patch application on CARMINEai/* review branch
-> product-vs-supplemental separation validation
-> automatic source/doc path discovery from apply report
-> draft GitHub PR for human review
```

The raw `output/**` reports are official process inputs. They feed bundle, evidence, telemetry, final summaries and patch-suggestion reports. They are not committed directly.

## Stamp ownership

`$Stamp` is a launcher-owned run variable. It is created or accepted by `run_unified_local_ai_refactor.ps1` and propagated to internal tools.

Internal tools must consume the launcher-propagated stamp. They must not introduce a separate unrelated stamp convention for the same product run.

Manual helper invocations may pass `--Stamp` only for diagnostics, replay or focused validation against a known launcher run.

## Internal tool family

The existing reuse-first family is:

```text
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/prepare_review_pr.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Expected responsibilities:

| Tool | Role |
|---|---|
| `build_task_patch_suggestion_report.py` | Extract task Markdown patch suggestions into a JSON/MD report. |
| `apply_patch_suggestion_bundle.py` | Discover stamped/current suggestion reports and apply only deterministic safe operations when explicitly requested by the launcher. |
| `check_patch_suggestion_product_separation.py` | Validate that essential patch suggestions remain separate from telemetry/debug/supporting evidence. |
| `prepare_review_pr.py` | Stage reviewed source/doc paths, commit, push and create a draft PR; production path derives paths from `patch_suggestion_bundle_apply` results. |

## Product versus supplemental output

The patch product is the applied source/doc diff in a draft review PR.

Supporting surfaces are still required, but they are not the product by themselves:

```text
provider telemetry
GPU0/NPU diagnostics
runtime heap/broker data
workload quality reports
validation reports
AI-to-AI bundle/final summary
compact evidence under docs/LOCAL_VALIDATION_EVIDENCE
```

The apply report separates:

```text
essential_patch_suggestion_items
supplemental_telemetry_debug_items
```

Essential/product-facing suggestions require:

```text
safe concrete source/doc target files
title or rationale
patch sketch or deterministic operation
validation commands or stop conditions
```

Telemetry, evidence, debug and validation-status-only findings remain supplemental.

## Deterministic operations

Supported deterministic operations are:

```text
replace_once
append_once
insert_after_once
insert_before_once
write_file
```

Accepted target path keys include:

```text
path
target
target_file
file
file_path
```

Proposal-only operations are preserved for manual review:

```text
manual_patch_suggestion
proposal_only
manual_review_only
```

## Path and PR policy

The production path for the review PR is automatic path discovery from `patch_suggestion_bundle_apply`:

```text
results[].path where applied=true or changed=true
```

Explicit include paths are allowed only as additive/manual overrides for reviewed source/doc/evidence paths. They are not the primary product mechanism.

The review PR must:

```text
use a CARMINEai/* branch
be draft by default
stage only safe source/doc or compact evidence paths
never stage output/**
never stage indexAI/code_chunks/** or indexAI/project_code_chunks/**
never stage *.db, *.sqlite, *.sqlite3
never stage renders/**
never merge itself to master
never force-push
```

## Provider-capable Python rule

Every phase must use the same provider-capable repository Python selected by the launcher:

```text
IA_CARMINE_PYTHON
PYTHONPATH=<repo root>
```

The expected OpenVINO device visibility on the IA-Carmine workstation is:

```text
CPU, GPU.0, GPU.1, NPU
```

A missing provider dependency is an environment failure, not a GPU0/NPU semantic failure.

## Manual diagnostics only

Direct calls to the internal tools are valid for diagnostics and focused replay only. They are not the canonical product flow.

Examples of diagnostic use:

```text
compile a touched helper
inspect a known patch_suggestion_bundle_apply report
run the product separation validator against a known report
perform a dry-run of prepare_review_pr without committing or pushing
```

For production, call the unified launcher with the relevant Full0To10/product flags so one run owns the stamp, provider loop, bundle/evidence/telemetry, patch application and draft PR creation.

## Guardrails

```text
No merge to master without explicit human command.
No delete, force-push or history rewrite.
No deploy.
No secret/permission/billing/visibility changes.
No Blender runtime.
No FFmpeg runtime.
No raw output/** commit.
No generated chunk commit.
No DB/SQLite/render commit.
Provider lanes advise or support; deterministic validators decide pass/fail.
Broker remains the controlled execution surface for tool requests.
```
