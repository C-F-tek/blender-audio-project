# Patch Spec Workflow

## Status

Current reference document for patch specs and patchkit-related patch product boundaries.

This file is not the primary Markdown-to-review-PR command catalog. Current operating/product docs are:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
docs/LOCAL_AI_TASKS/repository-hygiene-cleanup-and-refactor-procedure-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Purpose

Patch specs describe small, reviewable file modifications as deterministic specs.

PatchKit bundles describe controlled file modifications that can be authored by an AI without local access, committed to a PR or pasted/transferred to the user, then applied from the user's terminal with dry-run, backups and validators.

The current source-write direction is:

```text
heap/exchange exit product
  -> concrete deterministic operation candidates
  -> patchkit bundle or deterministic patch suggestion bridge
  -> validation/report
  -> prepare_review_pr.py or user terminal apply
  -> manual-review PR
```

Patch specs remain useful, but they must not bypass heap/exchange lifecycle validation, patchkit, product separation or human review.

## Current product boundaries

There are three related but separate lanes:

```text
legacy patch spec runner
  -> Tools/repo_patch_runner/apply_repo_mods.py
  -> patch_specs/inbox or local explicit apply
  -> high-risk explicit action only

patch suggestion bridge
  -> build_task_patch_suggestion_report.py / generated patch specs
  -> apply_patch_suggestion_bundle.py or apply_generated_patch_specs_for_review_pr.py
  -> check_patch_suggestion_product_separation.py
  -> prepare_review_pr.py

patchkit bundle lane
  -> patch_specs/<bundle>/bundle.json
  -> fragments
  -> Tools/ai/patchkit/apply_patch_bundle.py
  -> run_patchkit_smoke.py / validators
```

Preferred future bundle lane:

```text
patchkit bundle lane
```

## Remote-AI PatchKit handoff mode

PatchKit must stay usable when an AI has GitHub/API access but no local terminal.

In that mode, the AI must not pretend to have applied local changes. It should produce only:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*
procedure/update docs when useful
PowerShell commands for the user
validation commands for the user
expected touched files and line-count reporting policy
```

The user applies locally:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run `
  --output output\validation\<bundle>_patchkit_dry_run.json `
  --markdown-output output\validation\<bundle>_patchkit_dry_run.md

& $RepoPy .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --output output\validation\<bundle>_patchkit_apply.json `
  --markdown-output output\validation\<bundle>_patchkit_apply.md

git diff --check
git status --short
```

This is the preferred route for large patches when local command execution is required but the AI session cannot access the workstation. The AI focuses on the modification core; PatchKit handles safe local application.

Remote-AI handoff requirements:

```text
bundle must be idempotent where practical
bundle must use explicit stable anchors or guarded delete markers
bundle must keep destructive operations explicit
bundle must include validators in bundle.json when possible
AI must list exact local commands
AI must state that local apply/validation is pending until user output is provided
```

## Current review PR behavior

Code-driven facts from `Tools/ai/prepare_review_pr.py`:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with --auto-include-from-apply-report plus --apply-report.
prepare_review_pr.py supports --draft-pr.
--draft-pr requires --create-pr.
create_github_pr() appends --draft to gh pr create when requested.
metadata-only patch drafts are not enough for a successful review PR product.
```

Do not infer branch, commit, push or PR success from flags alone. Use the prepare-review report fields.

## Run-unica patch-plan doctrine

Patch specs and patch plans are incomplete by themselves when they originate from run-unica evidence.

Current doctrine:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
heap/exchange center is dynamic; entry and exit are controlled
patchkit is deterministic application infrastructure for reviewed bundles
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
limitations are backlog to overcome, not reasons to skip available tools
```

A complete run-derived product review requires the relevant group:

```text
launcher manifest
phase_status / phase_reports
evidence artifacts
heap/exchange runtime entry
heap/exchange runtime state
heap/exchange runtime exit product
heap/exchange lifecycle report
patchkit report when the source-write boundary was selected
patch-plan artifacts
patch-spec artifacts when produced
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/count summaries when inventory lanes ran
file-line-limit report when maintainability is in scope
discovery/index repair reports when relevant
patch suggestion product/separation reports when the review-PR path is selected
```

Telemetry is an obligatory completeness accessory. It does not replace evidence, patch plans or patch specs; it explains whether producing lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

File existence alone is not proof that a patch plan/spec is valid.

## Main files

| Path | Role |
|---|---|
| `Tools/ai/build_heap_exchange_runtime_entry.py` | Deterministic entry boundary for dynamic heap/exchange. |
| `Tools/ai/build_heap_exchange_runtime_exit.py` | Deterministic exit-product boundary. |
| `Tools/validation/check_heap_exchange_runtime_lifecycle.py` | Lifecycle gate. |
| `Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py` | Lifecycle smoke. |
| `Tools/ai/patchkit/apply_patch_bundle.py` | Preferred reusable controlled patch bundle applicator and remote-AI handoff apply target. |
| `Tools/validation/run_patchkit_smoke.py` | Patchkit dry/apply/idempotency smoke. |
| `Tools/repo_patch_runner/apply_repo_mods.py` | Legacy low-level patch runner; explicit apply only. |
| `Tools/ai/build_patch_specs_from_proposals.py` | Builds inert proposal-derived draft specs under ignored output. |
| `Tools/validation/check_patch_spec_drafts.py` | Validates draft specs before review-to-concrete promotion. |
| `Tools/ai/promote_patch_spec_draft.py` | Promotes a draft plus explicit replacement plan into reviewed spec. |
| `Tools/validation/check_reviewed_patch_specs.py` | Revalidates reviewed specs and reruns dry-run without apply. |
| `Tools/ai/build_task_patch_suggestion_report.py` | Task Markdown to patch suggestion report. |
| `Tools/ai/apply_patch_suggestion_bundle.py` | Deterministic patch suggestion dry/apply owner. |
| `Tools/ai/apply_generated_patch_specs_for_review_pr.py` | Generated patch-spec review bridge. |
| `Tools/validation/check_patch_suggestion_product_separation.py` | Product-vs-supplemental validator. |
| `Tools/ai/prepare_review_pr.py` | Review branch/commit/push/PR preparation owner. |
| `output/patch_specs/` | Ignored local workspace for generated draft/reviewed patch specs. |
| `patch_specs/inbox/` | Explicit high-risk queue; not default run-unica path. |
| `.github/workflows/apply_repo_mods.yml` | High-risk GitHub Action queue; not default run-unica path. |

## Patchkit bundle procedure

Future long or repeated patch work should centralize only the modification core:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Standard application:

```powershell
python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit must provide:

```text
idempotency markers
stable anchors
backup report
changed_count
line_counts
validator results
provider_execution_performed=false unless explicitly selected elsewhere
patch_application_performed/source_writes_performed truth fields
```

## Legacy patch spec runner policy

`Tools/repo_patch_runner/apply_repo_mods.py` can still apply reviewed specs, but it is not the preferred future patch-bundle abstraction.

It is explicit-apply only:

```text
patch_application_performed=false by default
source_writes_performed=false by default
manual_review_only=true by default
```

Do not queue or push `patch_specs/inbox/*.json` as part of normal Full0To10. Use the Action queue only after explicit approval for a reviewed spec.

## Draft spec rule

Proposal-derived drafts are intentionally inert:

```text
they live under ignored output/patch_specs/
they contain target operations and review metadata
they contain empty replacements lists
they use draft_status=needs_concrete_replacements
they must not be copied into patch_specs/inbox/ without separate review
```

Metadata-only drafts are manual-review items, not product patches.

## Review-to-concrete promotion

Promotion from draft to concrete spec requires explicit replacement operations.

The promoted spec must:

```text
target files already listed in the draft
run dry-run cleanly
change at least one target
stay out of generated/runtime/evidence denied paths
remain manual-review until explicitly applied
```

## Guardrails

Do not use any patch lane to bypass:

```text
no merge to master without explicit command
no delete without explicit scope
no force-push or rewrite history
no secrets/permissions/billing/visibility changes
no Blender runtime
no FFmpeg runtime
no output/** commit
no indexAI/code_chunks/** commit
no database/runtime artifact commit
```

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

For remote-AI-to-user-terminal workflows, prefer:

```text
patchkit bundle authored/reviewed in GitHub
  -> user dry-run locally
  -> user apply locally
  -> user returns validation output
  -> AI continues from actual logs/diff
```

For code refactors, prefer normal reviewed commits unless the edit is small, exact, anchorable and easy to validate.

For run-unica-derived patch plans/specs, require evidence plus telemetry/capability/discovery/file-line bundle context before treating the recommendation as complete.
