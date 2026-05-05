# AI Onboarding

## Purpose

This file is the first-session guide for AI agents entering `IA-Carmine Local AI Orchestration Workbench`.

Use it to quickly understand the canonical reading order, current full-run doctrine, what is generated context, what is safe to touch, and how to avoid damaging working Blender workflows or overclaiming local/runtime validation.

This file is orientation, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

## Current doctrine

```text
one canonical launcher flow
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
smoke = separate non-full mode
perimeter of tutto can expand explicitly
telemetry accompanies evidence and patch plans for completeness
```

Telemetry is not a replacement for evidence or patch plans. It is the required accessory that tells future agents whether lanes executed, failed, were blocked, degraded, disabled or planned-only.

## Source-of-truth order

Use this priority when documents disagree:

1. `AGENTS.md` for repository rules, safety limits and required validation.
2. `README.md` and `WORKFLOW.md` for human/project identity and lifecycle.
3. `docs/README.md` for documentation navigation.
4. `docs/LOCAL_AI_RUN_BOOTSTRAP.md` for local checkout bootstrap.
5. `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` for the active local-AI entrypoint.
6. `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` for launcher manifest/phase contract.
7. `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` for current broker/provider/telemetry/bundle/evidence flow.
8. `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md`, `docs/LOCAL_AI_WORKFLOW.md` and `docs/REFACTORING_AND_REUSE_PLAN.md` for architecture and migration direction.
9. The README nearest to the target package or tool.
10. The target source file itself.
11. Generated indexes under `indexAI/` and `Tools/npu/*_index.md` as derived context only.
12. `docs/PROJECT_AI_CONSCIOUSNESS.md` only as historical/orientation material; it must not override the launcher contract or guardrails.

If a status document says a file is missing but the file exists, treat the file tree as current evidence and update the stale document in a small documentation patch.

## Current baseline

As of PR #187 / branch `codex/unified-local-ai-refactor-launcher`:

| Area | Baseline |
|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical local-AI entrypoint. |
| `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Canonical runbook for full-run/local-AI commands. |
| `Tools/ai/` | AI orchestration, provider diagnostics, deterministic recommendations, broker reports, runtime telemetry, capability manifests, telemetry summaries and AI-to-AI bundle tooling. |
| `Tools/validation/` | Lightweight non-invasive validators and report-contract checks. |
| `Tools/npu/` | AI/NPU/Ollama context and review tooling. NPU remains probe/guardrail/decode diagnostic unless future quality-gated promotion exists. |
| `Tools/npu/pipeline/` | Additive app-agnostic helper package. It is not runtime-provider wiring by default. |
| `Scripting/v61b/` | Stable reference Blender package. Do not destructively refactor. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Usable standalone Blender/audio package, still monolithic. |
| `Scripting/shared/` | Package-agnostic utilities exist. Treat future-facing references carefully and verify actual files before editing. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable validation/evidence/telemetry handoff area. Use selected task-scoped files, not bulk evidence commits. |
| `indexAI/` | Generated AI context. Do not hand-refactor as source. |
| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |

Not yet complete:

The entries below are planned or future-facing candidates, not guaranteed existing files in the current checkout. Their absence is expected until a dedicated implementation PR creates and validates them.

```text
Scripting/shared/blender_compat.py
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
runtime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py
full production JSON schemas
automated Blender runtime validation
strict validation of every telemetry/bundle completeness path
```

## First-session checklist

For GitHub-only/API work:

```text
read AGENTS.md, README.md, WORKFLOW.md, docs/README.md
read this file
read docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md
read docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
inspect the PR/branch state directly through GitHub
use committed or pasted evidence/telemetry only for runtime claims
```

For local workstation work, command ownership belongs to:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

Do not copy old command blocks from historical docs into new tasks. Use the canonical runbook.

## Full-run handoff checklist

A production full-run handoff is not complete from evidence or patch plan alone.

Review this group together:

```text
launcher manifest
phase_status / phase_reports
evidence artifacts
patch-plan artifacts when produced
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

Never infer success only from:

```text
file exists
patch plan exists
dry-run matrix passed
provider report exists
NPU smoke passed
reviewed patch spec exists
```

## Common traps

- Do not assume every status document is current; compare it with the actual file tree.
- Do not treat `indexAI/` as source code. It is generated context.
- Do not overwrite full frame-by-frame analysis JSON files.
- Do not rewrite `Scripting/v61b/main_v61b.py` to improve architecture.
- Do not split the Ready To Jazz package before shared infrastructure and adapters are validated.
- Do not push patch specs that trigger GitHub Actions without explicit human approval.
- Do not add dependencies, CI changes, long Blender renders or GPU-heavy jobs without explicit approval.
- Do not assume Blender version compatibility unless it is documented or tested; mark it `not specified`.
- Do not wire `Tools/npu/pipeline/` helpers into `Tools/npu/run_dual_ai_pipeline.py` until local validation, index regeneration, quality gates, telemetry/bundle visibility and migration readiness gates are green.
- Do not treat planned files listed in `Not yet complete` as stale broken links; verify whether they are explicitly future-facing before changing code or docs.
- Do not commit ignored `output/**` validation reports; commit only compact task-scoped evidence when a workflow explicitly writes it under `docs/LOCAL_VALIDATION_EVIDENCE/`.
- Do not claim `Full0To10` success from focused validation, dry-run reports, provider reports, NPU smoke or file existence alone.

## Task routing

| Task type | Preferred first move |
|---|---|
| Documentation clarity | Patch docs directly, keep edits small, update indexes if adding a stable doc. |
| Documentation patch-plan evidence | Use the current launcher/task docs; apply only allowed doc targets; include telemetry/capability context when the patch plan comes from full-run evidence. |
| Shared utility extraction | Add package-agnostic module first, validate without Blender, then consider adapters. |
| v61b runtime issue | Read `Scripting/v61b/README.md` and target source; patch one concern only. |
| New generated package | Start from `Scripting/_template_audio_reactive_package/` and `docs/QUALITY_GATE.md`. |
| NPU/AI pipeline refactor | Split provider, prompt, validation and artifact-writing concerns without changing CLI behavior. |
| NPU helper package work | Keep helpers app-agnostic, run focused helper validation when local execution is available, and defer runtime wiring to a later proven phase. |
| GitHub-only work | Read `docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`; do not ask for local sync/runs while maintainer is away unless requested. |
| Full-run evidence or patch-plan review | Inspect manifest, evidence, telemetry, capability manifest, full toolbox summary and shared AI-to-AI bundle together. |

## Reporting template

Every implementation response should include:

```text
changed files
purpose
line counts for created or modified scripts
assumptions
validation commands and results, or explicit GitHub-only validation limits
telemetry/capability/final-summary artifacts reviewed when relevant
risks
recommended next step
```

For documentation-only changes, script line counts can be reported as `not applicable`.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:START -->

## IA-Carmine patch-plan application notes

This managed block was generated from `output/patch_specs/agent_review_patch_plan.json`.
It records the manual-review patch-plan decisions for this file without applying runtime/provider changes.

### `det_doc_code_001` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/AI_ONBOARDING.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/config_model.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

### `det_doc_code_002` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/AI_ONBOARDING.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/diagnostics.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:END -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_001:docs-ai_onboarding.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_001`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/AI_ONBOARDING.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/config_model.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_001:docs-ai_onboarding.md -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_002:docs-ai_onboarding.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_002`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/AI_ONBOARDING.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/diagnostics.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_002:docs-ai_onboarding.md -->
