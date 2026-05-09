# Patch Spec Workflow

## Purpose

This document explains the repository patch-spec workflow used by `IA-Carmine Local AI Orchestration Workbench`.

Patch specs are one safe way to describe small, reviewable file modifications as JSON specs, dry-run them, review them as Git diffs and apply them only after explicit approval.

This file is a contract/policy document, not the primary command catalog and not the primary Markdown-to-review-PR product path.

Current command and flow owners:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Patch spec vs patch suggestion product

There are two separate lanes:

```text
patch spec workflow
  -> JSON patch spec
  -> dry run
  -> explicit local apply or explicit GitHub Action queue

patch suggestion product workflow
  -> task Markdown
  -> build_task_patch_suggestion_report.py
  -> apply_patch_suggestion_bundle.py
  -> check_patch_suggestion_product_separation.py
  -> prepare_review_pr.py
```

The patch suggestion product workflow is the current Markdown-to-review-PR product path. Patch specs remain available for deterministic mechanical patches, but they are not the default review-PR product lane.

Current patch suggestion product status:

```text
ReviewPrIncludePath is explicit.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py does not create draft PRs yet.
```

## Run-unica patch-plan doctrine

Patch specs and patch plans are not complete by themselves when they originate from run-unica evidence.

Current doctrine:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
```

For `Full0To10`, patch-plan and patch-spec artifacts must travel with telemetry, capability and relevant discovery/count context:

```text
launcher manifest
phase_status / phase_reports
evidence artifacts
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

Telemetry is an obligatory completeness accessory. It does not replace evidence, patch plans or patch specs; it explains whether the producing lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

File existence alone is not proof that a patch plan/spec is valid.

## Main files

| Path | Role |
|---|---|
| `Tools/repo_patch_runner/apply_repo_mods.py` | Safe repository patch runner. Explicit apply tool, not automatic run-unica behavior. |
| `Tools/ai/build_patch_specs_from_proposals.py` | Builds inert proposal-derived draft specs under `output/patch_specs/`. |
| `Tools/validation/check_patch_spec_drafts.py` | Validates draft specs before review-to-concrete promotion. |
| `Tools/ai/promote_patch_spec_draft.py` | Promotes one draft plus an explicit replacement plan into a reviewed dry-run-passing spec. |
| `Tools/validation/check_reviewed_patch_specs.py` | Revalidates reviewed specs and reruns dry-run without applying patches. |
| `Tools/validation/check_file_line_limits.py` | Report-only line-budget validator. Does not rewrite, split, delete or apply patches. |
| `Tools/ai/build_task_patch_suggestion_report.py` | Task Markdown to patch suggestion report for the current product path. |
| `Tools/ai/apply_patch_suggestion_bundle.py` | Deterministic patch suggestion dry/apply owner for the current product path. |
| `Tools/validation/check_patch_suggestion_product_separation.py` | Product-vs-supplemental validator for the current product path. |
| `Tools/ai/prepare_review_pr.py` | Review branch/PR preparation owner for the current product path. |
| `output/patch_specs/` | Ignored local workspace for generated draft/reviewed patch specs. |
| `patch_specs/inbox/` | Queue of patch specs waiting to be applied. Use only after explicit approval. |
| `patch_specs/applied/` | Patch specs already applied by the GitHub Action. |
| `patch_specs/README.md` | Existing quick workflow notes. |
| `.github/workflows/apply_repo_mods.yml` | GitHub Action that applies queued specs on push or manual dispatch. High-risk; not default run-unica path. |

## What the runner does

`Tools/repo_patch_runner/apply_repo_mods.py` can:

```text
read a JSON patch spec
validate paths stay inside the repository root
remove UTF-8 BOM when present
apply exact replacements
apply regex replacements
insert text before or after anchors
validate required strings before and after patching
validate forbidden strings before and after patching
check expected line-count deltas
create backups unless disabled
print line counts before/after
show git diff after applying changes
```

## Manual apply policy

Patch application is not a normal Full0To10 side effect.

The default run-unica state is:

```text
patch_application_performed=false
source_writes_performed=false
manual_review_only=true
```

Local apply, queueing a spec under `patch_specs/inbox/`, pushing a queued spec or triggering the GitHub Action requires explicit approval scoped to that apply/queue action.

## Local dry run

Always dry-run first when a spec is intentionally being reviewed for apply:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --dry-run
```

## Local apply with diff

Apply locally only after explicit approval:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --write --show-diff
```

Apply locally without backup only when the patch is generated, reviewed, dry-run clean and explicitly authorized:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_specs\inbox\example.json --write --no-backup --show-diff
```

## GitHub Action queue

The Action watches:

```text
patch_specs/inbox/*.json
```

When a spec is pushed to `master`, the workflow:

```text
collects specs from patch_specs/inbox/
runs dry-run
applies with --write --no-backup --show-diff
moves the spec to patch_specs/applied/
commits resulting file changes with message: Apply repo patch specs
```

Policy:

```text
Do not queue or push patch_specs/inbox/*.json as part of normal Full0To10.
Do not treat the GitHub Action queue as a default apply lane.
Use it only after explicit approval for a reviewed spec.
```

## Minimal spec format

```json
{
  "version": 1,
  "description": "Short description of the patch",
  "operations": [
    {
      "path": "relative/path/file.md",
      "replacements": [
        {
          "type": "exact",
          "old": "old text",
          "new": "new text",
          "count": 1
        }
      ],
      "require_contains_after": ["new text"],
      "forbid_contains_after": ["old text"]
    }
  ]
}
```

## Supported replacement types

### exact

```json
{
  "type": "exact",
  "old": "old text",
  "new": "new text",
  "count": 1
}
```

### regex

```json
{
  "type": "regex",
  "pattern": "old\\s+pattern",
  "new": "new text",
  "count": 1,
  "flags": ["MULTILINE"]
}
```

Supported regex flags:

```text
MULTILINE
DOTALL
IGNORECASE
```

### insert_after

```json
{
  "type": "insert_after",
  "anchor": "existing text",
  "insert": "\nnew inserted text\n",
  "count": 1
}
```

### insert_before

```json
{
  "type": "insert_before",
  "anchor": "existing text",
  "insert": "new inserted text\n",
  "count": 1
}
```

## Validation fields

Use these fields to make patches safe:

| Field | Meaning |
|---|---|
| `require_contains_before` | Strings that must exist before the patch. |
| `forbid_contains_before` | Strings that must not exist before the patch. |
| `require_contains_after` | Strings that must exist after the patch. |
| `forbid_contains_after` | Strings that must not exist after the patch. |
| `expected_line_delta` | Exact line-count delta expected for the operation. |

## Recommended use cases

Good use cases:

```text
documentation edits
replacing repeated text blocks
adding small sections to README files
targeted config corrections
mechanical edits with stable anchors
AI-generated patch proposals that require deterministic validation
```

Avoid patch specs for:

```text
large code rewrites
artistic Blender scene behavior changes
patches requiring runtime reasoning
binary files
generated full frame-by-frame analysis JSON files
run-unica evidence/patch handoffs that lack telemetry/capability/discovery/file-line context
```

## Line-budget policy interaction

Patch specs must not create or expand maintained docs/source files beyond current line-budget policy without also planning the required split/refactor.

```text
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
Markdown >500 lines -> compact index + <file>.md/part-001.md layout
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split
Existing oversized files -> technical debt; patch only focused sections unless the task explicitly scopes a split/refactor
```

## AI usage policy

AI agents may generate patch specs when:

```text
the change is small
the target anchor is explicit
before/after validation strings are included
the patch can be dry-run before application
line count and diff can be reviewed
line-budget impact is known
run-unica-derived proposals include telemetry/capability/discovery/file-line context
```

AI agents should not push queued specs without explicit approval.

## Proposal-derived draft specs

Validated repository proposals can be converted into draft patch-spec shells by the appropriate launcher/patch-spec lane or focused tool.

These drafts are intentionally inert:

```text
they live under ignored output/patch_specs/
they contain target operations and review metadata
they contain empty replacements lists
they use draft_status=needs_concrete_replacements
they must not be copied into patch_specs/inbox/ without a separate review step
```

The draft validator rejects concrete replacements and queued inbox paths.

If proposals come from run-unica evidence, the draft manifest or surrounding handoff must reference companion telemetry/capability/final summary and relevant discovery/index/CSV-count/file-line surfaces.

## Review-to-concrete promotion

Promotion from draft to a concrete reviewed spec requires a separate replacement plan.

The promotion tool:

```text
reads a draft spec and a replacement plan
requires replacement operations to target files already listed in the draft
writes a reviewed_patch_spec under ignored output/patch_specs/
runs apply_repo_mods.py in dry-run mode through the shared runner code
refuses reviewed specs whose dry-run does not change at least one target
never uses --write and never writes patch_specs/inbox/
```

Reviewed specs are still not queued patches. Choosing local apply or GitHub Action queue remains a separate explicit step after human/trusted-agent approval.

## Local workflow for AI-assisted patching

Use this flow only after explicit apply/patch-spec review approval:

```text
1. create or review patch spec
2. dry-run patch spec
3. inspect expected changes
4. apply locally only when approved
5. validate repository
6. inspect git status and diff
7. commit manually when approved
```

## Remote queue workflow

Remote queueing is a high-risk explicit action, not a default run-unica behavior.

```text
1. create or copy a reviewed spec into patch_specs/inbox/
2. review risk and target branch
3. commit queue entry intentionally
4. push only after explicit approval
5. let GitHub Action dry-run/apply/commit if configured
```

## Generated patch specs to review PR bridge

For proposal/provider runs that produce generated patch specs instead of fenced
task-Markdown `patch_suggestion` blocks, use the bridge lane:

```text
proposal_patch_spec_manifest
  -> apply_generated_patch_specs_for_review_pr.py
  -> patch_suggestion_bundle_apply-compatible report
  -> prepare_review_pr.py --auto-include-from-apply-report
```

This lane does not replace the current product owners. The bridge applies only
concrete deterministic operations supported by `patch_suggestion_bundle`; inert
metadata-only drafts remain manual-review items. Generated/runtime/evidence
paths stay denied, including `output/**`, generated `indexAI` chunks,
`docs/LOCAL_VALIDATION_EVIDENCE/**`, databases and renders.

Launcher flags:

```text
-ReviewPrFromGeneratedPatchSpecs
-ReviewPrPatchSpecManifest <manifest>
-ReviewPrMaxAppliedPatches <n>
-ReviewPrRequireAllValidators
-ReviewPrDraft
```

Use this only when a run already produced reviewed concrete operations or when a
trusted operator supplied an explicit generated patch-spec manifest.

## Current recommendation

Use patch specs for mechanical documentation and validation-policy edits.

For the current Markdown-to-review-PR product flow, prefer:

```text
build_task_patch_suggestion_report.py
apply_patch_suggestion_bundle.py
check_patch_suggestion_product_separation.py
prepare_review_pr.py
```

For source-code refactors, prefer normal reviewed commits unless the edit is small, exact and easy to validate.

For run-unica-derived patch plans/specs, require evidence plus telemetry/capability/discovery/file-line bundle context before treating the recommendation as complete.
