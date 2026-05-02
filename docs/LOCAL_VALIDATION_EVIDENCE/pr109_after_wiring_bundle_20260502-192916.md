# Local Validation Evidence Bundle

- Generated at: `2026-05-02T19:29:16`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `4`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/validation/python_syntax_pr109_after_wiring.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/analysis/code_interpreter_report_pr109_after_wiring.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `64`

## Artifact manifest

- `output/validation/python_syntax_pr109_after_wiring.json` exists=`True` size=`31633` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_report_pr109_after_wiring.json` exists=`True` size=`661564` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/code_interpreter_report_pr109_after_wiring.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7482`
- SHA-256: `f89c0f4b9983554989f4da8f5bca5177837fa16595207b37ff1215a8aef3163f`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `129`
- Parsed files: `129`
- Total lines: `33281`
- Total functions: `1196`
- Total classes: `29`
- Risk signals: `12`
- TODO/FIXME markers: `17`
- Recommendation count: `64`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `714` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/ai/build_repository_change_proposals.py` — `582` lines, risk `medium`
- `Tools/ai/build_ai_context_pack.py` — `575` lines, risk `medium`
- `Tools/ai/run_pipeline_dry_run_matrix.py` — `573` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `562` lines, risk `medium`
- `Tools/ai/suggest_repository_updates.py` — `551` lines, risk `medium`
- `Tools/ai/agent_state.py` — `544` lines, risk `medium`
- `Tools/ai/run_megalithic_repo_review.py` — `519` lines, risk `medium`
- `Tools/ai/build_agent_review_code_patch_plan.py` — `499` lines, risk `medium`
- `Tools/validation/ai_pipeline_report_contracts.py` — `497` lines, risk `medium`
- `Tools/ai/refine_megalithic_review_signals.py` — `489` lines, risk `medium`
- `Tools/validation/run_agent_review_patch_plan_full_validation.py` — `487` lines, risk `medium`
- `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` — `483` lines, risk `medium`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `478` lines, risk `medium`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `471` lines, risk `medium`
- `Tools/validation/check_reviewed_patch_specs.py` — `446` lines, risk `medium`
- `Tools/ai/promote_patch_spec_draft.py` — `442` lines, risk `medium`
- `Tools/ai/build_code_interpreter_report.py` — `437` lines, risk `medium`

## Recommendations

- `code_static_001` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_002` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_003` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_004` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_005` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_006` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_007` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_008` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_009` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_010` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_011` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_012` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_013` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_014` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_015` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_017` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_018` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_019` `Tools/ai/model_json.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/pipeline/preflight.py` risk `medium`: complex functions detected
- `code_static_021` `Tools/ai/pipeline/remediation.py` risk `medium`: large functions detected, complex functions detected, TODO/FIXME markers detected
- `code_static_022` `Tools/ai/pipeline/steps.py` risk `medium`: large functions detected
- `code_static_023` `Tools/ai/promote_patch_spec_draft.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Tools/ai/refine_megalithic_review_signals.py` risk `medium`: medium-size Python module
- `code_static_025` `Tools/ai/review_wave_entrypoints.py` risk `medium`: large functions detected, complex functions detected
- `code_static_026` `Tools/ai/run_agent_gpu_deep_planning_review.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_027` `Tools/ai/run_agent_gpu_deep_planning_supervised.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_028` `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_029` `Tools/ai/run_local_provider_probe.py` risk `medium`: complex functions detected
- `code_static_030` `Tools/ai/run_megalithic_repo_review.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_031` `Tools/ai/run_npu_decode_smoke_diagnostic.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_032` `Tools/ai/run_npu_gpu_deep_review_auditor.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_033` `Tools/ai/run_pipeline_dry_run_matrix.py` risk `medium`: medium-size Python module, large functions detected, static risk calls detected
- `code_static_034` `Tools/ai/select_semantic_code_chunks.py` risk `medium`: large functions detected, complex functions detected
- `code_static_035` `Tools/ai/smart_ai_gatekeeper.py` risk `medium`: complex functions detected, TODO/FIXME markers detected
- `code_static_036` `Tools/ai/suggest_repository_updates.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_037` `Tools/ai/validate_ai_artifacts.py` risk `medium`: complex functions detected
- `code_static_038` `Tools/validation/ai_pipeline_report_contracts.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_039` `Tools/validation/check_ai_context_pack_contract.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_040` `Tools/validation/check_ai_dry_run_matrix_cases.py` risk `medium`: large functions detected, complex functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `docs/LOCAL_AI_TASKS/pr109-meta-doc-index-2026-05-02.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1674`
- SHA-256: `b4571c40e5861187e1f41f7a699bd870bcded3165a79da817e15bf28c10126ff`
- Content included: `True`
- Content truncated: `False`

```text
# PR109 meta-documentation index — 2026-05-02

## Purpose

Compact index of PR #109 meta-documents created during GitHub-only preparation.

Use this file as the first read when resuming locally.

## Read order

```text
1. docs/LOCAL_AI_TASKS/pr109-pre-return-status-2026-05-02.md
2. docs/LOCAL_AI_TASKS/pr109-docs-only-phase-log-2026-05-02.md
3. docs/LOCAL_AI_TASKS/pr109-evidence-flow.md
4. docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
5. docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md
6. docs/LOCAL_AI_TASKS/open-issue-triage-2026-05-02.md
```

## File purposes

### `pr109-pre-return-status-2026-05-02.md`

```text
single-page snapshot
current PR stack
hard blocker
what to do / what not to do at workstation
```

### `pr109-docs-only-phase-log-2026-05-02.md`

```text
GitHub-only docs/metadata phase boundary
completed docs-only tasks
explicit stop condition before local validation resumes
```

### `pr109-evidence-flow.md`

```text
short operational evidence flow
run levels: focused, multi, macro
raw evidence versus compact Git evidence boundary
merge gate
```

### `pr109-prelocal-github-only-audit.md`

```text
detailed audit
local command blocks
wiring sequence
bundle rebuild sequence
long touched-file inventory
```

### `open-pr-triage-2026-05-02.md`

```text
open and closed PR state
recommended PR ordering
PR #110 scratch-only handling
```

### `open-issue-triage-2026-05-02.md`

```text
open issues #57 and #104
future queue
risk classification for docs cleanup versus provider/GPU work
```

## Local resume rule

Do not start with merge/rebase/cleanup. Start with sync, status, diff check and compile gates from the pre-return status note.

```

### `docs/LOCAL_AI_TASKS/pr109-pre-return-status-2026-05-02.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3076`
- SHA-256: `41950271ec3d0d1c1a04275e556c2085ac3d9ddfeae18d9368bc8db4c219c490`
- Content included: `True`
- Content truncated: `False`

```text
# PR109 pre-return status — 2026-05-02

## Scope

Snapshot of safe GitHub-only preparation before local workstation access resumes.

No code execution, provider execution, Blender runtime, merge, rebase, delete, force-push or branch rewrite was performed by this note.

## Current active PR stack

```text
PR #108: open, mergeable, documentation/validator lane
PR #109: open, mergeable again as of latest GitHub check, official active PR, local wiring still pending
PR #110: open draft, scratch-only workspace, do not merge
```

Closed as stale/superseded during triage:

```text
PR #1: closed, merged=false
PR #2: closed, merged=false
```

## GitHub-only work completed

```text
updated PR #109 body with current operating flow
added concise PR109 evidence flow note
added open PR triage note
updated open PR triage after closing stale PRs
added open issue triage note
added pre-return status snapshot
cleaned code-quality unused imports before the final docs-only phase
```

## Docs created for local return

```text
docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
docs/LOCAL_AI_TASKS/pr109-evidence-flow.md
docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md
docs/LOCAL_AI_TASKS/open-issue-triage-2026-05-02.md
docs/LOCAL_AI_TASKS/pr109-pre-return-status-2026-05-02.md
```

## Current blocker

The final orchestrator wiring still requires local filesystem access:

```text
copy Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py
over  Tools/ai/build_github_evidence_bundle.py
```

This was intentionally not done via GitHub API because of earlier long-file truncation/corruption risk.

## Mergeability note

GitHub briefly reported PR #109 as non-mergeable after documentation-only commits, then later reported it as mergeable again. Treat mergeability as a local-return verification item, not as a reason to do structural GitHub-only changes.

Required local checks:

```powershell
git fetch origin
git switch codex/design-code-patch-plan-lane
git pull --ff-only origin codex/design-code-patch-plan-lane
git status --short
git diff --check
```

If GitHub reports conflicts after sync, inspect conflict source locally before any rebase/merge/update action.

## Do next at workstation

```text
1. Sync PR #109 branch.
2. Run git diff --check.
3. Compile refactored entry points.
4. Wire build_github_evidence_bundle.py locally.
5. Compile wired orchestrator.
6. Run focused validation.
7. Build fresh compact evidence bundle.
8. Validate bundle.
9. Stage only wiring + compact evidence.
10. Commit and push.
```

## Do not do before local validation

```text
merge PR #109
merge PR #108
close PR #110
edit build_github_evidence_bundle.py through API
edit large evidence bundles through API
start provider/GPU/NPU heavy runs
open new PRs
```

## Future queue

```text
Issue #57: safest next docs-only cleanup candidate after PR #108/#109 stabilize
Issue #104: future provider/GPU workload-depth task, parked until explicit local provider work is planned
PR #110: close only after PR #109 contains all useful changes and has fresh local evidence
```

```

### `docs/LOCAL_AI_TASKS/pr109-evidence-flow.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2708`
- SHA-256: `d8dd8a6419374be6484263f3991166d84334728834ccaebf5a47402e6a1cde61`
- Content included: `True`
- Content truncated: `False`

```text
# PR109 evidence flow

## Purpose

This note gives the short operational flow for PR #109 after GitHub-only preparation and before merge review.

It complements:

```text
docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
```

## Flow

```text
entry Markdown / PR state
-> sync official PR branch
-> local compile and hygiene gate
-> controlled local wiring
-> focused single-run validators
-> optional multi-run / macro validators
-> collect raw reports under ignored output/**
-> build compact evidence bundle under docs/LOCAL_VALIDATION_EVIDENCE/
-> validate compact bundle
-> stage only source wiring + compact evidence
-> push PR branch
-> GitHub audit from committed evidence
```

## Entry sources

```text
PR: #109
branch: codex/design-code-patch-plan-lane
audit note: docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
replacement-ready orchestrator: Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py
final target orchestrator: Tools/ai/build_github_evidence_bundle.py
```

PR #110 / `codex/refactor-workspace-109` is scratch-only and must not be merged.

## Run levels

```text
focused run = py_compile + check_python_syntax + static report + bundle validation
multi run = selected validator batch over Tools/ai and Tools/validation
macro run = broader local validation runner / dry-run matrix when workstation time allows
```

Start with the focused run. Move to multi/macro only after the focused run is green.

## Evidence boundary

Raw evidence remains local and ignored:

```text
output/validation/*.json
output/analysis/*.json
output/analysis/*.md
output/patch_specs/*.json
output/patch_specs/*.md
```

Git-tracked evidence must be compact, bounded and timestamped:

```text
docs/LOCAL_VALIDATION_EVIDENCE/<purpose>_<YYYYMMDD-HHMMSS>.json
docs/LOCAL_VALIDATION_EVIDENCE/<purpose>_<YYYYMMDD-HHMMSS>.md
```

## Push boundary

Allowed to stage:

```text
reviewed source/doc changes
compact evidence bundle JSON/Markdown
small task notes
```

Forbidden to stage:

```text
raw output/**
full analysis JSON
SQLite/database files
runtime media
render outputs
large provider transcripts
```

## Required post-wiring evidence

After locally copying the replacement-ready orchestrator over `Tools/ai/build_github_evidence_bundle.py`, build a fresh bundle and confirm at least:

```text
patch_plan_summary_seen=true
artifact_manifest_built=true
included_artifacts_built=true
included_artifact_count>=1
provider_execution_seen=false
```

## Merge gate

Do not merge PR #109 to `master` until:

```text
local wiring commit is pushed
fresh compact evidence bundle is pushed
bundle validation passes
manual review confirms no raw output/** or forbidden artifacts are staged
```

```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
