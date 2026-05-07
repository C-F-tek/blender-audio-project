# Local Validation Evidence Bundle

- Generated at: `2026-05-06T15:32:40`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `False`
- `selected_chunks_built`: `False`
- `budget_respected`: `False`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `5`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_adapter_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_ai_task_pipeline_adapter_manifest`
- Passed: `None`
- Patch application performed: `False`

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_telemetry.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_ai_task_pipeline_telemetry`
- Passed: `None`

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': False, 'model': None, 'error': '', 'text_preview': ''}`

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet_manifest`
- Passed: `None`

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/validation/md_bundle_telemetry_smoke_20260506-152951_repository_change_proposals_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposal_contract`
- Passed: `True`

## Artifact manifest

- `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_adapter_manifest.json` exists=`True` size=`7117` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_telemetry.json` exists=`True` size=`7495` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951.json` exists=`True` size=`105317` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_manifest.json` exists=`True` size=`6247` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_proposals.json` exists=`True` size=`5912` suffix=`.json` preview_chars=`1500`
- `output/validation/md_bundle_telemetry_smoke_20260506-152951_repository_change_proposals_contract.json` exists=`True` size=`2297` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `CHATGPT.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1356`
- SHA-256: `7c70e0c995a1cbde0e07f36dc38edbbc78bd2cf4d5ca16369b864fe8972bcfa1`
- Content included: `True`
- Content truncated: `False`

```text
# CHATGPT operational memory

This is the root pointer for ChatGPT-assisted repository memory.

Read this directory early when entering the repository as a human, cloud AI, local AI, Codex-style agent or automated review assistant:

```text
CHATGPT/
```

Primary file:

```text
CHATGPT/README.md
```

Current handoff file:

```text
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
```

Current active task:

```text
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Current runtime bundle to inspect:

```text
ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

The bundle is a runtime artifact published as a GitHub draft release asset from PR #187 and is intentionally not committed to the repository.

Robust chat/tooling recovery notes:

```text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
```

Contract:

```text
- CHATGPT/*.md is durable operational memory.
- It is advisory but should be read before planning new local AI/full-toolbox work.
- Source-of-truth remains code, validation reports, canonical docs, runtime bundle evidence and current git state.
- Do not use CHATGPT notes to override AGENTS.md guardrails.
```

Local AI discovery rule:

```text
Any repository scanner/context-pack builder should include CHATGPT/*.md as lightweight high-priority context.
```

```

### `docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `5864`
- SHA-256: `3e614453fe51732d28dfc3f147cc8fece30a80752226447949c81764dc60f5c7`
- Content included: `True`
- Content truncated: `False`

```text
# Refactor/reuse methods, classes and tools planning task

## Status

Stable local-AI planning task for IA-Carmine refactor/reuse work.

This task is intended for a full-run planning pass, not for automatic patch application.

## Objective

Analyze the repository code and produce a manual-review refactor/reuse plan for:

```text
duplicate methods/classes
reusable helper functions
base-class/superclass opportunities
project-tool promotion candidates
support-library extraction candidates
workflow/provider/telemetry utility centralization
code that should remain app-specific and not be promoted
The goal is a controlled mega patch plan, not a blind rewrite.

Current doctrine
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
telemetry accompanies evidence and patch plans for completeness

For this task, tutto includes code, docs, workflow scripts, validation tools, provider diagnostics, telemetry builders, memory/context lanes and Blender/audio application boundaries.

Hard requirements

The run must be review-only:

patch_application_performed=false
source_writes_performed=false

Do not:

apply patches automatically
perform source writes
run Blender
run FFmpeg
commit output/**
commit *.db or *.sqlite
commit indexAI/code_chunks/**
touch secrets, permissions, billing, visibility or deploy settings
merge to master
force-push or rewrite history
Required focus areas
Workflow and orchestration

Inspect for reusable workflow helpers across:

Tools/workflow/**
Tools/ai/**
Tools/validation/**
Tools/npu/**

Candidate themes:

report writing
manifest writing
path normalization
PowerShell command wrappers
provider diagnostic result normalization
telemetry summary assembly
bundle/final-summary assembly
patch-plan target hygiene
error/failure/blocked/degraded state propagation
Validation and report contracts

Inspect validator/report code for shared abstractions:

common report fields
schema_version/kind/repo_root/passed/errors/warnings
provider_execution_performed
patch_application_performed
source_writes_performed
blender_runtime_execution_performed
ffmpeg_execution_performed
JSON/Markdown paired output helpers
scoped report validation
warning policy ledgers
Provider and runtime diagnostics

Inspect provider-related code for extraction candidates, but do not promote provider execution by default.

Candidate reusable objects:

provider advisory state
provider failure reasons
degraded provider components
GPU/NPU timing summaries
real per-round elapsed_seconds extraction
workload quality lane routing
provider preflight normalization
Broker/tool promotion

Use docs/LOCAL_AI_TASKS/project-tool-registry.md and promotion docs to classify tools.

Do not promote these as broker-default tools:

Blender runtime tools
FFmpeg/audio encoding tools
Git write tools
patch apply tools
arbitrary shell execution tools
provider execution tools without explicit diagnostic-only contract
SQLite persistent write tools unless explicitly allowed
Blender/audio application boundary

Inspect Blender/audio files for reusable helper candidates, but keep app-specific runtime behavior separate.

Candidate extraction must preserve:

no Blender runtime during planning
no FFmpeg runtime during planning
no automatic behavior changes
manual-review patch plan only
Python string patch hygiene

Treat command-example cleanup and embedded Markdown/code fences as high-risk for multiline rewrites.

Do not introduce broad triple-quoted/raw multiline rewrites to fix command examples.

Prefer:

minimal one-line literal edits
POSIX-style relative examples such as ./Tools/...
explicit doubled backslashes when Windows path syntax must be preserved

Validate string/command-example changes with:

python -m py_compile
git diff --check
line counts
focused diff review
Required output

The full run should produce or update review artifacts containing:

recommendations
patch plan
review-only patch specs when supported
telemetry/capability/final-summary context
provider degradation notes if provider probes fail
source-write and patch-application flags
safe target list
unsafe/deferred target list
promotion/backlog notes
Acceptance criteria

A valid result must show:

patch_application_performed=false
source_writes_performed=false
provider state visible in telemetry/bundle/final summary
patch plan targets source/docs only when safe
no ordinary patch targets under docs/LOCAL_VALIDATION_EVIDENCE/**
no ordinary patch targets under output/**
no ordinary patch targets under indexAI/code_chunks/**
no generated/runtime artifacts committed as source

The patch plan must explicitly distinguish:

safe mechanical refactor
manual-review refactor
requires local runtime validation
requires Blender runtime validation
requires provider execution validation
defer/do not promote
Suggested command

Use the unified launcher from the repository root:

powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Tools\workflow\run_unified_local_ai_refactor.ps1" `
  -TaskFile ".\docs\LOCAL_AI_TASKS\refactor-reuse-methods-classes-tools-planning.md" `
  -Full0To10 `
  -RunIntensity quick `
  -SkipGitSync `
  -NoBranch `
  -NoExecutionTail

Increase intensity only after the quick planning pass is inspectable from manifest, telemetry, bundle/final summary and patch plan.

Post-run handling

After the run:

Read the latest unified_local_ai_refactor_manifest.json.
Inspect provider diagnostics and workload quality reports.
Inspect decision loop recommendation and patch-plan counts.
Group evidence, patch plan, telemetry, capability manifest, full toolbox telemetry summary and AI-to-AI bundle/final summary.
Push runtime artifact bundle as a draft GitHub release asset or attach to PR; do not commit output/**.
Select a controlled patch subset manually.
Apply source/docs changes in a normal reviewed commit only after focused validation.

```

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_telemetry.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2219`
- SHA-256: `4c2f8d722172077834c7d4a2ce23794d197892c0b2006bd6fbf9cc5f1701db6f`
- Content included: `True`
- Content truncated: `False`

```text
# Local AI task pipeline telemetry

- Kind: `local_ai_task_pipeline_telemetry`
- Basename: `md_bundle_telemetry_smoke_20260506-152951`
- Profile: `docs`
- Pipeline output: `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline`
- Provider execution requested: `False`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Build evidence requested: `True`
- Output checks passed: `True`

## Output Checks

| Name | Kind | Required | Exists | Bytes | Path |
|---|---|---:|---:|---:|---|
| `adapter_manifest` | `manifest` | `True` | `True` | `7117` | `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_adapter_manifest.json` |
| `packet_json` | `packet` | `True` | `True` | `105317` | `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951.json` |
| `packet_markdown` | `packet` | `True` | `True` | `3307` | `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951.md` |
| `packet_manifest` | `manifest` | `True` | `True` | `6247` | `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_manifest.json` |
| `proposals_json` | `proposal` | `True` | `True` | `5912` | `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_proposals.json` |
| `proposals_markdown` | `proposal` | `True` | `True` | `2344` | `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_proposals.md` |
| `proposal_validation` | `validation` | `True` | `True` | `2297` | `output/validation/md_bundle_telemetry_smoke_20260506-152951_repository_change_proposals_contract.json` |

## Validation Summaries

| Name | Exists | JSON OK | Passed | Errors | Warnings | Path |
|---|---:|---:|---:|---:|---:|---|
| `proposal_validation` | `True` | `True` | `True` | `0` | `0` | `output/validation/md_bundle_telemetry_smoke_20260506-152951_repository_change_proposals_contract.json` |


```

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3307`
- SHA-256: `114c78922a3e63b910321ec6c476cf3db00140b5dabc1df533d51d52e1d596a6`
- Content included: `True`
- Content truncated: `False`

```text
# Post-Validation AI Work Packet

- Generated at: `2026-05-06T15:32:39`
- Repo: `C:\Users\carmi\blender\blender-audio-project`
- Profile: `docs`
- Ollama used: `False`
- Packet manifest: `C:\Users\carmi\blender\blender-audio-project\output\local_ai_runs\md_bundle_telemetry_smoke_20260506-152951\pipeline\md_bundle_telemetry_smoke_20260506-152951_manifest.json`

## Advisory context routing

- Enforced: `True`
- Provider execution performed: `False`
- Advisory lanes: `npu`
- Excluded advisory lanes: `none`

## Deterministic suggestions

### P2 — Run or review missing validation reports before strict follow-up work

- Area: `validation`
- Details: C:\Users\carmi\blender\blender-audio-project\output\validation\docs_links.json; C:\Users\carmi\blender\blender-audio-project\output\validation\execution_plan_status.json; C:\Users\carmi\blender\blender-audio-project\output\validation\json_artifacts.json; C:\Users\carmi\blender\blender-audio-project\output\validation\validation_report_contract.json; C:\Users\carmi\blender\blender-audio-project\output\validation\python_syntax.json

### P2 — Review active execution plans before opening the next milestone

- Area: `execution_plans`
- Details: docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md; docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md; docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md; docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md; docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md; docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md; docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md

### P2 — Prefer additive observability before provider or Blender runtime changes

- Area: `agnostic_core`
- Details: Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.

## Inputs

### Trusted context files
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/README.md`
- `docs/AI_DOCS_ENTRYPOINT.md`
- `docs/PROJECT_STATUS_POINT.md`
- `docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`
- `docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md`
- `docs/TECH_DEBT_TRACKER.md`
- `CHATGPT.md`
- `docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md`

### Report files
- `output/validation/docs_links.json`
- `output/validation/execution_plan_status.json`
- `output/validation/json_artifacts.json`
- `output/validation/validation_report_contract.json`
- `output/validation/python_syntax.json`
- `output/validation/ai_workload_quality_lane_routing.json`
- `output/validation/npu_decode_quality_remediation.json`

## Guardrails

- Advisory only: do not auto-apply edits from this packet.
- Output/input paths are configurable; defaults are not part of the architecture boundary.
- Validate locally before committing generated indexes.
- Keep provider execution changes in a separate explicitly scoped milestone.

```

### `output/local_ai_runs/md_bundle_telemetry_smoke_20260506-152951/pipeline/md_bundle_telemetry_smoke_20260506-152951_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2344`
- SHA-256: `bd07ce4a2a36d36f0d2a6c75a4e197b482eb5475917252ae4d4e21604ee474ae`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-06T15:32:40`
- Profile: `docs`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-NEXT-NPU-OBSERVABILITY — Add additive NPU observability before provider execution changes

- Priority: `P2`
- Area: `npu_backend`
- Change type: `observability_extension`
- Apply mode: `manual_review_only`
- Rationale: Current reports do not indicate blocking failures. The next safe app-agnostic step is deeper observability, not provider behavior changes.

### Target files
- `Tools/npu/build_runtime_output_manifest.py`
- `Tools/ai/check_local_resource_lanes.py`
- `Tools/ai/suggest_repository_updates.py`
- `docs/JSON_SCHEMAS.md`
- `Tools/validation/README.md`

### Patch sketch
- Include runtime-output manifest and resource-lane reports in the default NPU packet profile.
- Add proposal generation output next to packet JSON/Markdown.
- Keep every output advisory and generated under output/.

### Suggestion outputs
- `python_code` `Tools/npu/build_runtime_output_manifest.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/check_local_resource_lanes.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1`
- `python .\Tools\ai\check_local_resource_lanes.py --repo-root . --parallel --output .\output\validation\local_ai_resource_lanes.json --markdown-output .\output\validation\local_ai_resource_lanes.md`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_after_tests -ReportFile output/validation/local_ai_resource_lanes.json -ReportFile output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change requires modifying provider execution, prompt prose, Blender runtime or generated indexes manually.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
