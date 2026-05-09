# Patch Notes Quality Product Task

Status: historical/reference local AI task.  
Date: 2026-05-07  
Original branch: `codex/provider-mesh-runtime-extract-p1`

## Current position

This file describes a historical patch-notes quality product task and proposal-ledger workflow.

It is not the current Markdown-to-review-PR product path.

Current product path:

```text
task Markdown
  -> unified launcher
  -> heap/exchange runtime entry
  -> dynamic provider/tool/broker/validator exchange
  -> heap/exchange runtime exit product
  -> heap/exchange lifecycle validation
  -> patchkit or deterministic patch suggestion bridge
  -> prepare_review_pr.py
  -> manual-review PR
```

Current operating docs:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/PATCH_SPEC_WORKFLOW.md
docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
```

## Objective

Produce a manual-review patch notes quality product from a local Markdown task, patch plan, patch quality gate, runtime telemetry, capability manifest, repository consistency, memory bundle and compact evidence bundle.

## Required Product

The run produced or expected:

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

## Proposal Core Handoff

The patch-notes product is a suggestion ledger, not a patch bundle. A `ready_for_patch_notes_review` product may be pushed as durable evidence, but its `patch_notes[]` entries must not be applied blindly.

When the product is included in a GitHub evidence bundle, the bundle must expose the compact ledger under:

```text
summary.proposal_core
summary.proposal_core.notes[]
```

The proposal core is the source for follow-up patch waves. Each note must retain enough data for another AI/session or human operator to decide whether the suggestion is still valid:

```text
id
area
severity
status
target_files
summary
edit_strategy
validation_commands
stop_conditions
manual_review_required
```

## Patch Suggestion Review Order

For historical ledgers, review suggestion lanes in this order:

```text
1. python_python
2. python_doc
3. doc_doc
4. doc_python
```

Before creating any source patch from a suggestion:

```text
refresh against current master
verify the reported source/target still exists
reject stale findings whose missing module/path now exists
reject generated-evidence noise and placeholder fenced-code paths
prefer small patch waves with explicit validation commands
record skipped stale suggestions as evidence when useful
route current product work through heap/exchange exit and lifecycle validation
prefer patchkit for reviewed reusable bundle application
```

`python_python` can justify code changes only when the import/module/symbol is still missing on the current branch. `python_doc` usually means a documented script lacks an obvious smoke/check/test; prefer report-only smoke wrappers over invasive refactors. `doc_doc` and `doc_python` must be filtered for template/path-placeholder noise before editing Markdown.

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

For focused builder tests, do not execute providers. For Full0To10 validation, providers may be expected when the operator explicitly requested TUTTO SU TUTTO and did not disable those lanes.

## Guardrails

```text
no patch apply unless explicitly requested
no source writes by generated patch specs
no Blender runtime
no FFmpeg runtime
no output/** commit
no SQLite commit
manual review required
NPU must not be sole final reviewer of NPU lane quality
patch notes are proposals until converted into a reviewed patchkit bundle, deterministic patch suggestion bridge or branch diff
```

## Validation

Historical validation for this task:

```powershell
python -m py_compile .\Tools\ai\build_patch_notes_quality_product.py .\Tools\ai\build_runtime_tool_usage_telemetry.py .\Tools\ai\provider_runtime_heap_live_signals.py .\Tools\validation\run_patch_notes_quality_product_smoke.py
python .\Tools\validation\run_patch_notes_quality_product_smoke.py --repo-root .
git diff --check
```

For current product-path work, also consider:

```powershell
python .\Tools\validation\run_heap_exchange_runtime_lifecycle_smoke.py --repo-root .
python .\Tools\validation\run_patchkit_smoke.py --repo-root .
```
