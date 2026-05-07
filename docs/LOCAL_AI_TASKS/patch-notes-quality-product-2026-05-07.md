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

The product is report-only and must include request summary, normalized objective, input digest, patch plan summary, generated patch notes, telemetry quality, evidence coverage, structured success cases, structured fallback cases, fallback path notes, validation commands, stop conditions and guardrails.

Runtime tool telemetry must normalize every tool status, expose return codes when available, preserve broker-measured elapsed seconds and classify missing elapsed data instead of silently reporting an all-zero performance surface.

Provider runtime heap telemetry must include a broker-controlled tool catalog exchange event pair:

```text
tool_catalog_request
tool_catalog_response
```

This proves GPU1 can see the controlled broker capability catalog before final product telemetry without allowing provider lanes to execute tools directly.

## NPU Final Check Policy

NPU is a micro/support lane, not the final judge of its own output. Final NPU quality checks must be reviewed by GPU1, GPU0 or both, then accepted by deterministic validators.

Required classification:

```text
npu_self_check_only = not sufficient
gpu1_npu_final_review = acceptable
gpu0_npu_final_review = acceptable
gpu1_gpu0_npu_final_review = preferred when both peer reports exist
deterministic_validator_acceptance = required final authority
```

If NPU is slow, empty, timed out or degraded, the product must keep the fallback non-blocking and record which GPU lane reviewed the NPU state.

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
NPU must not be sole final reviewer of NPU lane quality
```

## Validation

```powershell
python -m py_compile .\Tools\ai\build_patch_notes_quality_product.py .\Tools\ai\build_runtime_tool_usage_telemetry.py .\Tools\ai\provider_runtime_heap_live_signals.py .\Tools\validation\run_patch_notes_quality_product_smoke.py
python .\Tools\validation\run_patch_notes_quality_product_smoke.py --repo-root .
git diff --check
```
