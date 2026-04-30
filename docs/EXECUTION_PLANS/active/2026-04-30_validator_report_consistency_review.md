# Validator Report Consistency Review

## Status

active

## Goal

Review validator JSON reports for common root fields and propose small follow-up PRs.

This plan records the review scope. It does not change validator code.

## Common fields under review

```text
schema_version
repo_root
passed
errors
```

## Current observations from repository source

| Validator | `schema_version` | `repo_root` | `passed` | root `errors` | Notes |
|---|---:|---:|---:|---:|---|
| `check_python_syntax.py` | yes | yes | yes | no | Failures live in `results[].error`; root has `failed_count`. |
| `check_json_artifacts.py` | yes | yes | yes | no | Failures live in `results[].error`; root has `failed_count`. |
| `check_package_structure.py` | yes | yes | yes | no | Warnings live in package entries; strict mode can fail. |
| `check_generated_python_policy.py` | yes | yes | yes | yes | Good reference for future generated Python adapters. |
| `check_generated_artifact_path_policy.py` | expected | expected | expected | expected | Confirm in local/source review before code change. |
| `check_generated_blender_script_policy.py` | expected | expected | expected | expected | Should remain composed over generic Python policy. |
| `check_ai_dry_run_matrix_contract.py` | expected | expected | expected | expected | Contract validator should preserve forward compatibility. |
| `check_agent_memory_policy.py` | expected | expected | expected | not confirmed | Requires source review before alignment. |

## Proposed follow-up PRs

| Follow-up | Scope | Risk | Validation |
|---|---|---|---|
| Add root `errors` to `check_python_syntax.py` reports | Non-breaking additive report field derived from failed results. | Low | Python syntax check plus JSON artifacts check. |
| Add root `errors` to `check_json_artifacts.py` reports | Non-breaking additive report field derived from failed JSON results. | Low | JSON artifacts check with a deterministic bad sample if added. |
| Add root `errors` to `check_package_structure.py` reports | Non-breaking additive field; warnings may remain warnings. | Low-medium | Package structure check with and without `--strict`. |
| Document common validator report contract in `Tools/validation/README.md` | Docs-only. | Low | Docs link check. |

## Rules for later implementation

- Additive fields only.
- Do not remove existing report fields.
- Do not change exit codes without a dedicated plan.
- Do not make warning-only validators fail by default.
- Preserve unknown future fields in consumers.
- Keep each validator alignment in a small PR.

## Local validation status

```text
Local workstation validation pending.
```
