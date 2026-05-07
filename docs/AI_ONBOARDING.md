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
master contains PR #187 unified launcher baseline
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
400 lines = hard limit for maintained docs and source files
limitations = backlog to overcome, not reasons to skip available tools
```

Telemetry is not a replacement for evidence or patch plans. It is the required accessory that tells future agents whether lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

## Main runtime architecture

Current target architecture:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Read the canonical contract before runtime, provider, broker, registry, validator or telemetry work:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Interpretation:

```text
providers advise, classify or respond through explicit lanes;
broker unico executor is the execution gateway for registered tools;
semantic tools registry is the capability source of truth;
deterministic CPU validators remain local pass/fail authority;
telemetry/event stream records executed, skipped, degraded and blocked phases.
```

## Current branch phase

```text
Baseline: master after PR #187 merge
Current documentation PR: #196 docs(ai): add main runtime architecture contract
Mode: GitHub-only/API when maintainer is away
```

Do not treat `codex/unified-local-ai-refactor-launcher` or PR #187 as the active branch anymore. PR #187 is the merged baseline.

## Source-of-truth order

Use this priority when documents disagree:

1. `AGENTS.md` for repository rules, safety limits and required validation.
2. `CHATGPT.md` and `CHATGPT/README.md` for current chat/session handoff routing.
3. `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` for current code/state bridge.
4. `docs/MAIN_RUNTIME_ARCHITECTURE.md` for blackboard, GPU1/GPU0/NPU, broker, registry, validators and telemetry model.
5. `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` for launcher manifest/phase contract.
6. `docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md` for oversized Markdown handling.
7. `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md` for the 400-line validator contract.
8. `README.md`, `WORKFLOW.md` and `docs/README.md` for project identity and navigation.
9. `docs/LOCAL_AI_RUN_BOOTSTRAP.md` for local checkout bootstrap.
10. `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` for the run-unica entrypoint.
11. `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` for current broker/provider/telemetry/bundle/discovery/CSV/evidence flow.
12. `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md`, `docs/LOCAL_AI_WORKFLOW.md` and target package/tool READMEs.
13. The target source file itself.
14. Generated indexes under `indexAI/` and `Tools/npu/*_index.md` as derived context only.
15. `docs/PROJECT_AI_CONSCIOUSNESS.md` only as historical/orientation material.

If a status document says a file is missing but the file exists, treat the file tree as current evidence and update the stale document in a small documentation patch.

## Current baseline

| Area | Baseline |
|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical run-unica local-AI entrypoint. |
| `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Canonical runbook for run-unica commands and parameters. |
| `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Compact launcher manifest and phase contract. |
| `docs/MAIN_RUNTIME_ARCHITECTURE.md` | Canonical blackboard/broker/registry/validator/telemetry architecture target. |
| `Tools/ai/` | AI orchestration, provider diagnostics, deterministic recommendations, broker reports, runtime telemetry, capability manifests, telemetry summaries and AI-to-AI bundle tooling. |
| `Tools/validation/` | Non-invasive validators and report-contract checks. Its README is a catalog/reference, not a primary entrypoint if too large/truncated. |
| `Tools/validation/check_file_line_limits.py` | Report-only 400-line policy validator for maintained docs and source files. |
| `Tools/npu/` | AI/NPU/Ollama context and review tooling. NPU remains probe/guardrail/decode diagnostic or microtask responder unless future quality-gated promotion exists. |
| `Tools/npu/pipeline/` | Additive app-agnostic helper package. It is not runtime-provider wiring by default. |
| `Scripting/v61b/` | Stable reference Blender package. Do not destructively refactor. |
| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Usable standalone Blender/audio package, still monolithic. |
| `Scripting/shared/` | Package-agnostic utilities exist. Treat future-facing references carefully and verify actual files before editing. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable validation/evidence/telemetry handoff area. Use selected task-scoped files, not bulk evidence commits. |
| `indexAI/` | Generated AI context. Do not hand-refactor as source. Do not commit `indexAI/code_chunks/**`. |
| `docs/JSON_SCHEMAS.md` | Broad schema notebook/catalog. Prefer compact contracts for active run-unica semantics. |

Not yet complete / still debt to overcome:

```text
strict production schemas for every new runtime-architecture report
blackboard state reports wired into launcher manifest
semantic tools registry snapshot emitted by full runs
runtime event stream as a first-class report
full automatic Blender runtime validation
existing oversized docs/source files above 400 lines
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
file-line-limit reports when maintainability is in scope
blackboard/broker/registry/validator/event-stream reports when implemented
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

## 400-line rule

Active maintained Markdown and source files must stay under 400 lines.

```text
Markdown over 400 lines -> compact index + <file>.md/part-001.md, part-002.md, ...
Code over 400 lines -> compact entrypoint + responsibility-based package/module split
```

Use compact bridge docs and manifests first.

## Tool usage and limitation rule

Use every relevant available tool lane by default.

```text
A limitation is backlog to overcome.
A limitation is not a static prohibition.
A tool/lane is unavailable only when current code, telemetry, capability manifest, provider diagnostic or validator evidence says so.
Historical notes about missing tools are obsolete unless current evidence confirms them.
```

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
- Do not create a second execution path outside broker/registry/validator/telemetry once the main runtime architecture is implemented.
- Do not claim `Full0To10` success from focused validation, dry-run reports, provider reports, NPU smoke, large Markdown content or file existence alone.

## Task routing

| Task type | Preferred first move |
|---|---|
| Documentation clarity | Patch docs directly, keep edits small, update indexes if adding a stable doc. |
| Main runtime architecture | Read `docs/MAIN_RUNTIME_ARCHITECTURE.md`; add report-only validators/manifests before execution changes. |
| Shared utility extraction | Add package-agnostic module first, validate without Blender, then consider adapters. |
| v61b runtime issue | Read `Scripting/v61b/README.md` and target source; patch one concern only. |
| New generated package | Start from `Scripting/_template_audio_reactive_package/` and `docs/QUALITY_GATE.md`. |
| NPU/AI pipeline refactor | Split provider, prompt, validation and artifact-writing concerns without changing CLI behavior. |
| GitHub-only work | Read `docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`; do not ask for local sync/runs while maintainer is away unless requested. |
| Run-unica evidence or patch-plan review | Inspect manifest, evidence, telemetry, capability manifest, full toolbox summary, CSV/index/discovery/file-line-limit surfaces and shared AI-to-AI bundle together. |

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
