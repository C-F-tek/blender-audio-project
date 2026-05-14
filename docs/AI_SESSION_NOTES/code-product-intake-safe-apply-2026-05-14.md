# Code product intake and safe apply - 2026-05-14

## Decision

`CODE_PRODUCT_FULL_PATCH.md` is now treated as an operational artifact.

The repository has a deterministic intake tool that can:

- parse the run-produced code product by target section;
- classify each section as already integrated, integrated with context drift, forward-applicable, truncated, or review-needed;
- apply only safe forward-applicable sections when explicitly requested;
- write backups under `output/validation` before modifying existing source files;
- re-analyze after apply;
- emit JSON/Markdown evidence.

## Tools

```text
Tools/ai/analyze_code_product_artifact.py
Tools/ai/code_product_artifact_apply.py
Tools/ai/code_product_artifact_report.py
Tools/validation/run_code_product_artifact_intake_smoke.py
```

Broker tool:

```text
analyze_code_product_artifact
```

Safe apply requires:

```text
--apply-safe
confirm=safe_apply when invoked through the broker
```

## Real artifact result

Input:

```text
C:\Users\carmi\Documents\aicarmine_heap_final_proposals_20260514-195340\CODE_PRODUCT_FULL_PATCH.md
```

Intake result:

```text
target_count: 15
already_integrated_count: 15
forward_applicable_count: 0
needs_review_count: 0
all_integrated: true
safe_apply_requested: true
safe_apply_performed: false
source_writes_performed: false
```

The artifact is already represented in `master` by Day 0. No safe source write was needed.

## Validation

```text
python -m py_compile Tools/ai/agent_runtime_tool_broker.py Tools/ai/analyze_code_product_artifact.py Tools/ai/code_product_artifact_apply.py Tools/ai/code_product_artifact_report.py Tools/validation/run_code_product_artifact_intake_smoke.py
python Tools/validation/run_code_product_artifact_intake_smoke.py --repo-root . --timeout-seconds 120
python Tools/ai/analyze_code_product_artifact.py --repo-root . --code-product <CODE_PRODUCT_FULL_PATCH.md> --apply-safe --require-all-integrated
python Tools/ai/agent_runtime_tool_broker.py --repo-root . --request-file output/validation/code_product_intake_broker_request_20260514.json --timeout-seconds 180
git diff --check
```

The smoke test applies one normal patch and one new-file dump inside a temporary fixture repository under `output/validation`, then verifies both are integrated.
