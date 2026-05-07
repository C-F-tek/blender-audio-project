# Patch Notes Quality Product Task

Status: active local AI task
Date: 2026-05-07
Branch: `codex/provider-mesh-runtime-extract-p1`

## Objective

Produce a manual-review patch notes quality product from a local Markdown task, patch plan, patch quality gate, runtime telemetry, capability manifest, repository consistency, memory bundle and compact evidence bundle.

## Required Product

The run must produce:

```text
docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_<stamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_<stamp>.md
```

The product is report-only and must include request summary, normalized objective, input digest, patch plan summary, generated patch notes, telemetry quality, evidence coverage, fallback path notes, validation commands, stop conditions and guardrails.

## Runtime Posture

For focused builder tests, do not execute providers. For the final Full0To10 validation, providers are expected because the operator explicitly requested TUTTO SU TUTTO.

## Guardrails

```text
no patch apply
no source writes by generated patch specs
no Blender runtime
no FFmpeg runtime
no output/** commit
no SQLite commit
manual review required
```

## Validation

```powershell
python -m py_compile .\Tools\ai\build_patch_notes_quality_product.py .\Tools\validation\run_patch_notes_quality_product_smoke.py
python .\Tools\validation\run_patch_notes_quality_product_smoke.py --repo-root .
git diff --check
```
