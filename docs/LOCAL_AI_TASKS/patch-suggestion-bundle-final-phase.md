# Patch suggestion bundle final phase

Status: current reference for the deterministic patch suggestion bridge.  
Scope: IA-Carmine full toolbox flow, deterministic patch suggestion application, review PR preparation.

## Current position

This document describes one bridge lane inside the current product path. It is not the whole product path.

Current product path:

```text
task Markdown
  -> unified launcher
  -> context/agent-state/workload evidence
  -> heap/exchange runtime entry
  -> dynamic provider/tool/broker/validator exchange
  -> generated patch specs or patch suggestion bridge
  -> heap/exchange runtime exit product
  -> heap/exchange lifecycle validation
  -> patchkit or deterministic patch suggestion application
  -> prepare_review_pr.py
  -> GitHub PR for human review
```

Canonical operating model:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/PATCH_SPEC_WORKFLOW.md
```

## Code-verified current state

Current script family:

```text
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/apply_generated_patch_specs_for_review_pr.py
Tools/ai/patch_suggestion_bundle/cli.py
Tools/ai/prepare_review_pr.py
Tools/validation/run_patch_suggestion_bundle_apply_smoke.py
Tools/validation/check_patch_suggestion_product_separation.py
Tools/validation/run_full0to10_product_pr_chain_smoke.py
```

Code-driven behavior:

```text
apply_patch_suggestion_bundle.py discovers stamped/current suggestion JSON reports.
apply_patch_suggestion_bundle.py dedupes explicit --suggestion-report paths against Stamp discovery.
apply_patch_suggestion_bundle.py can apply only deterministic operations when --apply is supplied.
apply_patch_suggestion_bundle.py creates/switches a review branch when requested, but does not commit.
apply_patch_suggestion_bundle.py may push the review branch when --push-review-branch is supplied, but does not force-push.
prepare_review_pr.py stages only explicit --include-path values or safe auto-discovered paths from apply reports.
prepare_review_pr.py rejects output/**, generated chunks, renders and DB/SQLite paths.
prepare_review_pr.py can commit, push and call gh pr create when requested.
prepare_review_pr.py supports --draft-pr; it requires --create-pr and appends --draft to gh pr create.
check_patch_suggestion_product_separation.py is report-only and validates apply reports or smoke wrapper reports.
```

Do not infer success from flags alone. Use generated reports for branch, commit, push, PR and draft status.

## Product target versus current bridge

The bridge is valid only when it produces concrete deterministic operations or product-facing manual review items.

Metadata-only drafts are not enough.

Current accepted product statuses:

```text
deterministic_patch_operations_ready
manual_review_product_suggestions_ready
```

Failure/non-product status:

```text
no_applicable_patch_product
metadata-only draft operation has no concrete replacements
```

## Safety contract

The final apply phase is conservative by design:

```text
No provider execution.
No Blender execution.
No FFmpeg execution.
No SQLite writes.
No Git commit in apply_patch_suggestion_bundle.py.
No merge.
No force-push.
No delete.
No output/** target edits.
No renders/** target edits.
No indexAI/code_chunks/** or indexAI/project_code_chunks/** target edits.
```

Apply policy:

```text
apply is allowed only on a dedicated review branch
branch name must match an allowed prefix
current default allowed prefixes are CARMINEai/ and codex/
master/main apply is refused by branch policy
```

Natural-language suggestions and proposal-only `manual_patch_suggestion` items are preserved for manual review.

## Product vs supplemental output

The final phase separates review output into:

```text
essential_patch_suggestion_items
supplemental_telemetry_debug_items
```

Essential/product-facing suggestions must have:

```text
safe concrete source/doc target files
title or rationale
patch sketch or deterministic operation
validation commands or stop conditions
```

Telemetry, evidence, debug and validation-status-only items remain supplemental. They are useful for diagnosis, but they are not enough to close the product loop as an applicable patch suggestion.

Readiness fields:

```text
patch_product_status
ready_for_patch_suggestion_review
manual_review_product.product_facing_manual_review_count
manual_review_product.supplemental_manual_review_count
manual_review_product.deterministic_operation_count
manual_review_product.deterministic_apply_ready
```

## Supported deterministic operations

Suggestion/proposal JSON may contain explicit operations:

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

Accepted operation keys include:

```text
operation
op
action
patch_operation
edit_operation
```

Proposal-only operations are preserved for manual review:

```text
manual_patch_suggestion
proposal_only
manual_review_only
```

## Validation and product gates

Focused validation:

```powershell
& $ProjectPython .\Tools\validation\run_patch_suggestion_bundle_apply_smoke.py `
  --repo-root . `
  --output .\output\validation\patch_suggestion_bundle_apply_smoke.json

& $ProjectPython .\Tools\validation\run_full0to10_product_pr_chain_smoke.py `
  --repo-root . `
  --output .\output\validation\full0to10_product_pr_chain_smoke.json `
  --markdown-output .\output\validation\full0to10_product_pr_chain_smoke.md
```

Heap/exchange product validation:

```text
Tools/ai/build_heap_exchange_runtime_entry.py
Tools/ai/build_heap_exchange_runtime_exit.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
```

Patchkit validation when patchkit is selected:

```text
Tools/ai/patchkit/apply_patch_bundle.py
Tools/validation/run_patchkit_smoke.py
```

## Unified launcher review PR phase

The unified launcher can call `prepare_review_pr.py` through:

```text
-PrepareReviewPr
-ReviewPrBranch
-ReviewPrBaseBranch
-ReviewPrRemote
-ReviewPrTitle
-ReviewPrCommitMessage
-ReviewPrIncludePath
-ReviewPrPush
-ReviewPrCreate
-ReviewPrDraft
```

Current behavior:

```text
explicit -ReviewPrIncludePath remains supported
apply-report auto discovery is supported by prepare_review_pr.py with --auto-include-from-apply-report and --apply-report
-ReviewPrDraft maps to prepare_review_pr.py --draft-pr when wired by the launcher path
```

Use the prepare-review report fields, not assumptions, to confirm:

```text
git_branch_created
git_commit_performed
git_push_performed
github_pr_created
github_pr_draft_requested
github_pr_url
product_commit
```

## Evidence bundle after local apply

After local apply and validation, build compact Git-trackable evidence if needed:

```powershell
$EvidenceStamp = Get-Date -Format "yyyyMMdd-HHmmss"

& $ProjectPython .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename patch_suggestion_bundle_final_phase_$EvidenceStamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --report .\output\validation\patch_suggestion_bundle_apply_smoke.json `
  --report .\output\validation\patch_suggestion_product_separation.json
```

Commit only generated compact evidence JSON/MD if it is useful for PR review.

## Current recommendation

For current Markdown-to-review-PR product flow, prefer:

```text
heap/exchange runtime entry
provider/official/patch-spec lanes
heap/exchange runtime exit product
heap/exchange lifecycle validation
patchkit or deterministic patch suggestion bridge
prepare_review_pr.py
```

Use this patch suggestion bridge when existing reports already contain concrete deterministic operations. For future repeated source edits, prefer patchkit bundles because the modification core is compact and reusable.
