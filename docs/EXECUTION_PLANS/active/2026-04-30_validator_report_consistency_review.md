# Validator Report Consistency Review

## Status

active

## Goal

Review validator JSON reports for common root fields and implement small additive alignments where safe.

This plan started as a review-only GitHub-only task. PR #34 now includes the first low-risk implementation slice because the changes are additive, stdlib-only and do not affect Blender/runtime behavior.

## Common fields under review

```text
schema_version
kind
repo_root
passed
errors
warnings where applicable
```

## Current observations from repository source

| Validator | `schema_version` | `kind` | `repo_root` | `passed` | root `errors` | root `warnings` | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| `check_python_syntax.py` | yes | yes | yes | yes | yes | no | Failures still live in `results[].error`; root `errors` is additive. |
| `check_json_artifacts.py` | yes | yes | yes | yes | yes | no | Failures still live in `results[].error`; root `errors` is additive. |
| `check_package_structure.py` | yes | yes | yes | yes | yes | yes | Warnings remain non-blocking unless `--strict` is used. |
| `check_generated_python_policy.py` | yes | yes | yes | yes | yes | rule-level | Good reference for future generated Python adapters. |
| `check_generated_artifact_path_policy.py` | expected | expected | expected | expected | expected | expected | Confirm in local/source review before code change. |
| `check_generated_blender_script_policy.py` | expected | expected | expected | expected | expected | expected | Should remain composed over generic Python policy. |
| `python -m Tools.validation check_ai_dry_run_matrix_contract` | expected | expected | expected | expected | expected | expected | Contract validator should preserve forward compatibility. |
| `check_agent_memory/policy.py` | expected | expected | expected | expected | not confirmed | not confirmed | Requires source review before alignment. |

## Implemented in PR #34

| Item | Scope | Runtime impact | Validation required locally |
|---|---|---|---|
| `Tools/validation/_shared/report_utils.py` | Shared JSON report helpers for output resolution, JSON serialization and compact root error/warning messages. | None | Python syntax validation. |
| `check_python_syntax.py` root fields | Added `kind: python_syntax`; added root `errors`; reused shared output writer. | None | `check_python_syntax.py`. |
| `check_json_artifacts.py` root fields | Added `kind: json_artifacts`; added root `errors`; reused shared output writer. | None | `check_json_artifacts.py`. |
| `check_package_structure.py` root fields | Added `kind: package_structure`; added root `errors` and `warnings`; warnings remain non-blocking unless `--strict`. | None | `check_package_structure.py` with and without `--strict`. |

## Remaining proposed follow-up PRs

| Follow-up | Scope | Risk | Validation |
|---|---|---|---|
| Align remaining validators with a documented common report contract | Additive fields only where missing. | Low-medium | Run each validator locally. |
| Document common validator report contract in `Tools/validation/README.md` | Docs-only. | Low | Docs link check. |
| Add a deterministic report-contract validator for validation reports themselves | Optional later step; avoid over-engineering until local reports stabilize. | Medium | Full local validation runner. |

## Rules for later implementation

- Additive fields only.
- Do not remove existing report fields.
- Do not change exit codes without a dedicated plan.
- Do not make warning-only validators fail by default.
- Preserve unknown future fields in consumers.
- Keep each validator alignment in a small PR when possible.
- Keep GitHub-only changes limited to stdlib validators and docs.

## Local validation status

```text
Local workstation validation pending.
```
