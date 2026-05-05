# AI Onboarding

## Purpose

First-session guide for AI agents entering `IA-Carmine Local AI Orchestration Workbench`.

This file is a compact onboarding bridge. It is not a command catalog, not generated evidence and not a place for long managed patch-plan blocks.

Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Tool/validator catalogs may be larger reference files and should not be treated as primary operational entrypoints if they are too large to open reliably.

## Current doctrine

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
```

Telemetry is not a replacement for evidence or patch plans. It is the required accessory that tells future agents whether lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

## Current branch phase

```text
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

The runtime bundle is a GitHub draft release asset linked from PR #187 and is intentionally not committed to the repository. Do not infer bundle contents from file existence alone.

## Source-of-truth order

Use this priority when documents disagree:

1. `AGENTS.md` for repository rules, safety limits and required validation.
2. `CHATGPT.md` and `CHATGPT/README.md` for current chat/session handoff routing.
3. `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` for current branch state.
4. `docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md` for oversized Markdown handling.
5. `README.md` and `WORKFLOW.md` for human/project identity and lifecycle.
6. `docs/README.md` for documentation navigation.
7. `docs/LOCAL_AI_RUN_BOOTSTRAP.md` for local checkout bootstrap.
8. `docs/LOCAL_AI_TASKS/README.md` for task routing.
9. `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` for the run-unica entrypoint.
10. `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` for launcher manifest/phase contract.
11. `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` for current broker/provider/telemetry/bundle/discovery/CSV/evidence flow.
12. `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md`, `docs/LOCAL_AI_WORKFLOW.md` and target package/tool READMEs for architecture and migration direction.
13. The target source file itself.
14. Generated indexes under `indexAI/` and `Tools/npu/*_index.md` as derived context only.
15. `docs/PROJECT_AI_CONSCIOUSNESS.md` only as historical/orientation material; it must not override current contracts.

If a status document says a file is missing but the file exists, treat the file tree as current evidence and update the stale document in a small documentation patch.

## Current baseline

As of PR #187 / branch `codex/unified-local-ai-refactor-launcher`:

| Area | Baseline |
|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical run-unica local-AI entrypoint. |
| `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Canonical runbook for run-unica commands and parameters. |
| `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Compact launcher manifest and phase contract. |
| `Tools/ai/` | AI orchestration, provider diagnostics, deterministic recommendations, broker reports, runtime telemetry, capability manifests, telemetry summaries and AI-to-AI bundle tooling. |
| `Tools/validation/` | Non-invasive validators and report-contract checks. Its README is a catalog/reference, not a primary entrypoint if too large/truncated. |
| `Tools/npu/` | AI/NPU/Ollama context and review tooling. NPU remains probe/guardrail/decode diagnostic unless future quality-gated promotion exists. |
| `Tools/npu/pipeline/` | Additive app-agnostic helper package. It is not runtime-provider wiring by default. |
| `Scripting/v61b/` | Stable reference Blender package. Do not destructively refactor. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Usable standalone Blender/audio package, still monolithic. |
| `Scripting/shared/` | Package-agnostic utilities exist. Treat future-facing references carefully and verify actual files before editing. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable validation/evidence/telemetry handoff area. Use selected task-scoped files, not bulk evidence commits. |
| `indexAI/` | Generated AI context. Do not hand-refactor as source. Do not commit `indexAI/code_chunks/**`. |
| `docs/JSON_SCHEMAS.md` | Broad schema notebook/catalog. Prefer compact contracts for active run-unica semantics. |

Not yet complete:

```text
Scripting/shared/blender_compat.py
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
runtime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py
full production JSON schemas
automated Blender runtime validation
strict validation of every telemetry/bundle completeness path
```

These are planned or future-facing candidates. Their absence is expected until a dedicated implementation PR creates and validates them.

## Full-run / run-unica handoff checklist

A production run-unica handoff is not complete from evidence or patch plan alone.

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
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
```

Never infer success only from:

```text
file exists
patch plan exists
dry-run matrix passed
provider report exists
NPU smoke passed
reviewed patch spec exists
large Markdown mentions it
```

## Large Markdown rule

Markdown that is too large to be reliably opened by a future chat, local AI context pack or GitHub-only reviewer must not be a primary operational entrypoint.

Examples currently treated as catalog/supporting rather than primary:

```text
docs/JSON_SCHEMAS.md
Tools/validation/README.md
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

Use compact bridge docs and manifests first.

## Common traps

- Do not assume every status document is current; compare it with the actual file tree.
- Do not treat `indexAI/` as source code. It is generated context.
- Do not commit `indexAI/code_chunks/**` or `output/**`.
- Do not overwrite full frame-by-frame analysis JSON files.
- Do not rewrite `Scripting/v61b/main_v61b.py` to improve architecture.
- Do not split the Ready To Jazz package before shared infrastructure and adapters are validated.
- Do not push patch specs that trigger GitHub Actions without explicit human approval.
- Do not add dependencies, CI changes, long Blender renders or GPU-heavy jobs without explicit approval.
- Do not assume Blender version compatibility unless it is documented or tested; mark it `not specified`.
- Do not wire `Tools/npu/pipeline/` helpers into `Tools/npu/run_dual_ai_pipeline.py` until local validation, index regeneration, quality gates, telemetry/bundle visibility and migration readiness gates are green.
- Do not treat planned files listed in `Not yet complete` as stale broken links; verify whether they are explicitly future-facing before changing code or docs.
- Do not claim `Full0To10` success from focused validation, dry-run reports, provider reports, NPU smoke, large Markdown content or file existence alone.

## Task routing

| Task type | Preferred first move |
|---|---|
| Documentation clarity | Patch docs directly, keep edits small, update indexes if adding a stable doc. |
| Documentation patch-plan evidence | Use current run-unica/task docs; apply only allowed doc targets; include telemetry/capability context when patch plan comes from full-run evidence. |
| Shared utility extraction | Add package-agnostic module first, validate without Blender, then consider adapters. |
| v61b runtime issue | Read `Scripting/v61b/README.md` and target source; patch one concern only. |
| New generated package | Start from `Scripting/_template_audio_reactive_package/` and `docs/QUALITY_GATE.md`. |
| NPU/AI pipeline refactor | Split provider, prompt, validation and artifact-writing concerns without changing CLI behavior. |
| NPU helper package work | Keep helpers app-agnostic, run focused helper validation when local execution is available, and defer runtime wiring to a later proven phase. |
| GitHub-only work | Read `docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`; do not ask for local sync/runs while maintainer is away unless requested. |
| Run-unica evidence or patch-plan review | Inspect manifest, evidence, telemetry, capability manifest, full toolbox summary, CSV/index/discovery surfaces and shared AI-to-AI bundle together. |

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
