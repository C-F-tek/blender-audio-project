# Local Validation Evidence Bundle

- Generated at: `2026-05-06T14:34:58`
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

### `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_adapter_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_ai_task_pipeline_adapter_manifest`
- Passed: `None`
- Patch application performed: `False`

### `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': False, 'model': None, 'error': '', 'text_preview': ''}`

### `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet_manifest`
- Passed: `None`

### `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/validation/md_task_review_bundle_smoke_20260506-143456_repository_change_proposals_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposal_contract`
- Passed: `True`

### `output/patch_specs/md_task_review_bundle_smoke_20260506-143456_patch_specs_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `proposal_patch_spec_manifest`
- Passed: `True`
- Provider execution performed: `False`

## Artifact manifest

- `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_adapter_manifest.json` exists=`True` size=`6984` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456.json` exists=`True` size=`99370` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_manifest.json` exists=`True` size=`5827` suffix=`.json` preview_chars=`1500`
- `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_proposals.json` exists=`True` size=`5912` suffix=`.json` preview_chars=`1500`
- `output/validation/md_task_review_bundle_smoke_20260506-143456_repository_change_proposals_contract.json` exists=`True` size=`2301` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/md_task_review_bundle_smoke_20260506-143456_patch_specs_manifest.json` exists=`True` size=`2286` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `AGENTS.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `10223`
- SHA-256: `00815e7c0610e1001e0d07c5a69811920607974d6cd7b750d7d6e7bb136457dd`
- Content included: `True`
- Content truncated: `True`

```text
# AGENTS.md

This is the primary repository contract for AI assistants, local agents, automated review systems and GitHub-only assistants working on this repository.

## Mandatory contract

Before planning, editing, validating, opening a PR or suggesting changes, the agent must:

1. read `AGENTS.md`;
2. read `CHATGPT.md` and `CHATGPT/README.md` when resuming ChatGPT-assisted, local-AI, full-toolbox or handoff-driven work;
3. read `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` for the current branch phase when present;
4. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md` when working from or delegating to a local checkout;
5. follow hard guardrails unless the human explicitly approves a normally restricted action;
6. report task/request conflicts before modifying files;
7. inspect the target source/document before proposing a patch.

## Repository identity

| Field | Value |
|---|---|
| Working title | `IA-Carmine Local AI Orchestration Workbench` |
| Repository | `C-F-tek/blender-audio-project` |
| Main language | Python |
| Active architecture | Local AI orchestration, validation, provider routing, guardrail/evidence workflows |
| Primary provider lane | `Ollama -> GPU/CUDA -> primary advisory` |
| Secondary provider lane | `OpenVINO -> NPU -> probe / guardrail / decode diagnostic` |
| Legacy domain | Blender audio-reactive scene automation |

The repository name is historical. Do not infer that Blender/audio is the current architectural boundary.

## Canonical reading order

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
CHATGPT/next-chat-handoff-*.md           # when present and relevant
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md          # local checkout only
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
nearest package/tool README
target file
```

For full toolbox, refactor, provider or 0-to-10 local AI runs, use the unified launcher as the active entrypoint:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current compact operational state lives in:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
```

Current active task:

```text
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Historical PR handoffs and old master-branch runbooks are not active entrypoints. If historical details are needed, recover them from git history or compact evidence, not from active task docs.

## Current active branch phase

```text
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

The runtime bundle is a GitHub draft release asset linked from PR #187 and is intentionally not committed to the repository. Do not infer bundle contents from file existence alone.

The earlier broker telemetry gap is resolved/historical unless a new regression is found. Use `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` for the recent telemetry baseline.

## ChatGPT operational memory

`CHATGPT/` is a lightweight operational-memory surface for long ChatGPT-assisted repository sessions.

Agents must treat it as discoverable advisory context:

```text
CHATGPT.md                         # root pointer
CHATGPT/README.md                  # index and reading order
CHATGPT/next-chat-handoff-*.md     # current handoff state
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
```

Rules:

```text
Read CHATGPT notes early when resuming a handoff or local-AI workflow.
Use CHATGPT notes to avoid repeating known chat/tooling failures.
Do not let CHATGPT notes override AGENTS.md, source code, validation reports or canonical docs.
Keep CHATGPT notes small, plain Markdown and useful to local context pack builders.
```

## Current provider posture

```text
Ollama/GPU is the primary advisory lane for Full0To10 unless explicitly disabled or diagnosed unavailable.
NPU/OpenVINO is a validated smoke/probe/diagnostic lane for Full0To10 unless explicitly disabled or diagnosed unavailable.
Provider execution is explicit when Full0To10 or a provider mode/flag is selected; it is not an extra per-lane opt-in.
Visible provider degradation can be acceptable when quality-gated and recovered in telemetry/bundle evidence.
Blender runtime is frozen unless explicitly scoped.
```

## Unified 0-to-10 rule

A valid `-Full0To10` run must include every major phase unless the operator disables a phase explicitly with a `-No*` flag.

Expected by default:

```text
pipeline adapter ufficiale eseguito
packet/proposals generati
Ollama advisory usato or explicitly diagnosed as degraded
patch specs creati e validati
primary provider routing completo or explicit recovered provider diagnostic
workload quality routing presente
multistep provider workflow richiesto
probe Ollama/NPU richiesti
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
quality gate registrato nel manifest
runtime broker report produced and absorbed into telemetry
p
```

### `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6076`
- SHA-256: `01d05c1b68fc295c77d1681e051ad2ce9216fd2f00b8f607fdc793d0b163b78b`
- Content included: `True`
- Content truncated: `True`

```text
# Current operational state — IA-Carmine — 2026-05-05

## Status

Current doc-only operational state bridge for PR #187 on branch `codex/unified-local-ai-refactor-launcher`.

This file exists to keep future agents oriented without requiring a full rewrite of long indexes or opening large runtime bundles first.

## Active repository state

```text
Repository: C-F-tek/blender-audio-project
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Mode for ChatGPT/cloud work: GitHub-only/API unless local access is explicitly requested
```

## Active doctrine

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
all full-run lanes are included by default
if the operator does not want a lane, the operator must disable it explicitly with -No* flags or documented exclusion
telemetry accompanies evidence and patch plans
AI-to-AI bundle, runtime telemetry, capability manifest and full toolbox telemetry summary are operational handoff surfaces
```

Provider/probe policy for full runs:

```text
In a Full0To10 run, provider probes, provider diagnostics, workload quality, runtime broker telemetry and capability manifests are expected by default.
They do not require a separate per-lane confirmation once Full0To10 is selected.
They may be skipped only through explicit -No* flags, unavailable-tool/provider diagnostics, dry-run planned state or a documented operator exclusion.
```

## Current active work item

```text
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Bundle location: GitHub draft release asset linked from PR #187
Patch mode: review-only until explicit human instruction
```

The runtime bundle is not committed to the repository and must not be reconstructed from guesses.

## Current handoff state

Expected current handoff file:

```text
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
```

If this file is absent from GitHub, it is expected to be pending local add/commit/push. Use the PR comment and compact notes as interim context, not as a replacement for the handoff.

## Compact docs to read before long indexes

```text
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/project-tool-registry.md
docs/TECH_DEBT_TRACKER.md
```

## Recent validated baseline

Recent committed evidence shows:

```text
20260505-073332:
  passed=true
  recommendation_count=5
  patch_plan_count=5
  provider_execution_performed=true
  runtime broker bootstrap executed=3 failed=0 blocked=0

20260505-081141:
  passed=true
  recommendation_count=3
  patch_plan_count=3
  provider_execution_performed=true
  patch_application_performed=false
  source_writes_performed=false
  runtime broker bootstrap executed=3 failed=0 blocked=0
  local_provider_probe passed=false with ollama: probe failed
  ai_workload_report_quality passed=true
  usable_lanes=['npu']
```

Interpretation:

```text
The old broker telemetry loss is closed unless a new regression appears.
Provider degradation can be acceptable when visible, quality-gated and recovered.
Patch planning remains review-only.
File existence is not proof of execution; inspect telemetry fields.
```

## Current bundle inspection requirement

Before selecting any refactor/reuse patch from run `20260505-143844`, inspect:

```text
unified_local_ai_refactor_manifest.json
decision loop
recommendations
patch plan
runtime tool usage telemetry
runtime capability manifest
full toolbox telemetry summary
shared toolbox AI-to-AI bundle/final summary
provider diagnostics
ai_workload_report_quality
```

If the GitHub connector cannot download the draft release asset, state that limitation and continue only with committed evidence and PR comments.

## Candidate refactor family from committed code/docs inspection

The current safe-looking candidate family is:

```text
centralize report/telemetry helper functions in Tools/validation/report_utils.py
reuse them from Tools/ai/build_runtime_tool_usage_telemetry.py
reuse them from Tools/ai/build_full_toolbox_run_telemetry_summary.py
evaluate Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py separately after bundle review
```

This remains provisional until the `20260505-143844` bundle is inspected.

## Current patch classification policy

Every recommendation/patch plan must be classified as one of:

```text
SAFE_MECHANICAL
MANUAL_REVIEW
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

## Known documentation drift to clean incrementally

Some long indexes may still describe broker telemetry follow-up as active work.

Current policy:

```text
Treat broker telemetry follow-up as historical/resolved unless investigating a new regression.
Treat refactor/reuse bundle inspection as the current active P1.
Treat external-controls pass-through as a follow-up, not as the current active task unless explicitly selected.
```

Preferred cleanup strategy:

```text
small focused doc patches
compact bridge notes
no full API rewrites of large Markdown indexes unless necessary
run docs-link/report-contract validation locally when available
```

## Hard guardrails

```text
No merge to master.
No delete, force-push or rewrite history.
No deploy.
No secret/permission/billing/visibility changes.
No commit of output/**.
No commit of indexAI/code_chunks/**.
No commit of *.db, *.sqlite or *.sqlite3.
No commit of renders/**.
No Blender runtime.
No FFmpeg runtime.
No automatic patch-spec apply.
No broad triple-quote/raw multiline rewrites for command-example cleanup.
Full0To10 is opt-out by lane: provider/probe/telemetry/discovery lane
```

### `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3286`
- SHA-256: `3aac9f7ac235db594796d79fdeb9ea9f62d65a0e5c881ec26424a933a87601fa`
- Content included: `True`
- Content truncated: `False`

```text
# Post-Validation AI Work Packet

- Generated at: `2026-05-06T14:34:57`
- Repo: `C:\Users\carmi\blender\blender-audio-project`
- Profile: `docs`
- Ollama used: `False`
- Packet manifest: `C:\Users\carmi\blender\blender-audio-project\output\local_ai_runs\md_task_review_bundle_smoke_20260506-143456\pipeline\md_task_review_bundle_smoke_20260506-143456_manifest.json`

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
- `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`

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

### `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2344`
- SHA-256: `8f823ba04218db6d321e3350dd6bb1f1e2ea315fbbfe73fbbaa1af5fab07b806`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-06T14:34:57`
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

### `output/patch_specs/md_task_review_bundle_smoke_20260506-143456_patch_specs_manifest.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `705`
- SHA-256: `4961d8052955b9965d0d47e870c63e96ef48bbbdbec1557b6c63294c9c2b36b2`
- Content included: `True`
- Content truncated: `False`

```text
# Proposal Patch Spec Drafts

- Generated at: `2026-05-06T14:34:58`
- Source proposal report: `output/local_ai_runs/md_task_review_bundle_smoke_20260506-143456/pipeline/md_task_review_bundle_smoke_20260506-143456_proposals.json`
- Draft spec count: `1`
- Skipped target count: `0`
- Provider execution performed: `False`

## Draft specs

- `P-NEXT-NPU-OBSERVABILITY` -> `output/patch_specs/md_task_review_bundle_smoke_20260506-143456_patch_specs/P-NEXT-NPU-OBSERVABILITY.json` (5 target operations)

## Skipped targets

- none

## Guardrail

These drafts are not queued patches. Keep them under `output/` until a human or trusted agent adds concrete replacements and dry-runs the spec.

```

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
