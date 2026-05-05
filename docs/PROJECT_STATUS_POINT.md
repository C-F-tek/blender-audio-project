# Project Status Point

## Purpose

Current technical status of `IA-Carmine Local AI Orchestration Workbench` for GitHub-only and local continuation work.

The repository slug remains `C-F-tek/blender-audio-project`, but the active architecture is now local AI orchestration, provider-lane routing, validation, evidence, runtime broker telemetry, tool governance and manual-review patch planning.

Blender/audio remains the first application domain. It is not the boundary of the active architecture.

## Current doctrine

The active operating doctrine is **TUTTO SU TUTTO** through one unified local-AI flow.

`-Full0To10` means whole-repository coverage across active lanes. `quick`, `balanced`, `deep` and `custom` are intensity profiles only: they change budgets and depth, not semantic scope.

The perimeter of `tutto` is expandable. When a new tool, broker capability, validation lane, provider diagnostic, evidence surface, repository-consistency check or memory/context builder becomes production-ready, it must be added to the full-run contract or explicitly excluded with rationale.

Telemetry is AI-critical evidence. Future local/cloud AI agents must use telemetry to decide whether a lane was executed, failed, blocked, degraded, skipped intentionally or unavailable; file existence alone is not enough.

## Current branch context

Current consolidation branch:

```text
codex/unified-local-ai-refactor-launcher
```

Recent relevant commits on this branch include:

| Commit | Meaning |
|---|---|
| `a85bbf4` | Preserves broker report in final runtime telemetry. Validated by run `20260505-073332`. |
| `c420c5c` | Improves provider diagnostics and patch-plan target hygiene. Validated by run `20260505-081141`. |
| `9b01b92` | Uses real `rounds[*].elapsed_seconds` as GPU sync timing source. Smoke-validated locally. |
| `30c3dd7` | Includes full-toolbox diagnostics in shared bundle templates. |
| `0bbd829` | Clarifies planned shared module references in onboarding docs. |
| `db56fa0` | Clarifies optional local reference folders in AI reference onboarding. |
| `7c31754` | Codifies full-run coverage and patch bundle policy in `AGENTS.md`. |
| `2cf03d9` | Adds expandable TUTTO SU TUTTO doctrine to local task index. |
| `78691f8` | Demotes legacy full-toolbox semi-automatic procedure snapshot from active entrypoint. |
| `fcea9f2` | Promotes telemetry as AI reasoning evidence in current code-flow docs. |

GitHub-only agents must not infer local runtime success without evidence. When local validation exists, cite the exact run stamp and reported fields.

## Active local-AI entrypoint

The active local-AI operator model is unified around one launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

The unified launcher owns the selectable 0-to-10 flow. Older monolithic full-toolbox, code-refactor and Markdown-refactor 0-to-10 runbooks are not active starting points.

Current supporting docs:

```text
FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
```

## Current operator posture

```text
manifest-first review
phase-selectable local runs
Full0To10 profile for complete loops
quick/balanced/deep/custom intensities without scope reduction
workload quality gate before primary advisory routing
Ollama/GPU advisory only when explicit and quality-gated
NPU/OpenVINO probe/guardrail/decode diagnostic only
SQLite memory local-only, explicit and non-committed
runtime broker report and telemetry surfaced in compact evidence
runtime capability manifest surfaced in compact evidence
full toolbox telemetry summary carried with AI-to-AI bundle
patch specs generated as review-only artifacts
patch application remains separate and explicit
no audio/media output during normal AI/tooling runs
```

## Current provider-lane status

| Lane | Provider | Role | Current meaning |
|---|---|---|---|
| GPU/CUDA | Ollama | Primary advisory provider when explicitly requested and quality-gated. | Advisory lane, not implicit execution. |
| NPU/OpenVINO | OpenVINO GenAI | Probe, guardrail and decode diagnostics. | Not promoted to general advisory lane. |
| Blender/audio/media runtime | Blender Python, FFmpeg, audio tools | Application-domain runtime. | Frozen unless explicitly scoped. |

Provider execution must be explicit and report-bound. A full tooling run must not silently treat degraded provider lanes as successful advisory output.

Validated provider-diagnostic state from run `20260505-081141`:

```text
provider_advisory_state=recovered_degraded_provider
provider_failure_detected=true
deterministic_recovery_used=true
provider_failure_reasons includes: output/validation/local_provider_probe.json: ollama: probe failed
patch_application_performed=false
source_writes_performed=false
```

## Runtime broker telemetry status

Current P0:

```text
closed
```

Status:

```text
CODE_PATCH_PUSHED
RUNTIME_VALIDATED
```

Relevant files:

```text
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
```

Validated run:

```text
20260505-073332
```

Validated telemetry fields:

```text
runtime_tool_usage_telemetry_20260505-073332.json
  inputs.broker_reports includes output/validation/runtime_tool_broker_full_toolbox_20260505-073332.json
  summary.tool_call_entry_count=3
  summary.executed_count=3
  summary.failed_count=0
  summary.blocked_count=0
```

Expected broker-executed tools:

```text
check_python_syntax
build_python_line_count_csv
check_validation_report_contract
```

Do not relabel broker telemetry as open unless a newer run regresses these fields.

## Telemetry and AI handoff status

Telemetry is now part of the production AI-to-AI contract.

Required handoff surfaces:

```text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
output/analysis/shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

AI-critical fields include:

```text
tool_call_entry_count
executed_count
failed_count
blocked_count
broker_reports
provider_advisory_state
provider_failure_reasons
degraded_provider_components
gpu_metrics_source
round_duration_source
patch_application_performed
source_writes_performed
```

A next AI must not infer success from file presence alone. It must inspect telemetry and capability manifests.

## Audio/media output status

Normal AI/tooling workflows are report/evidence workflows, not media-generation workflows.

Forbidden unless explicitly scoped as application-domain runtime work:

```text
audio playback
audio export
WAV/MP3/AAC conversion
FFmpeg encode or mux operation
Blender render
video generation
media output side effect
```

Current guardrail doc:

```text
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

If a non-application run produces audio/media output, classify it as a guardrail breach and record phase, tool, path, tracked/ignored state and mitigation.

## Tool governance status

Current tool governance layer:

```text
docs/LOCAL_AI_TASKS/project-tool-registry.md
docs/LOCAL_AI_TASKS/project-tool-registry-generation-task.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
```

Tool promotion levels:

```text
Level 0 — discovered script
Level 1 — documented candidate
Level 2 — project tool
Level 3 — broker tool
Level 4 — full-run lane
```

Important rule:

```text
Not every project tool is broker-safe.
```

Audio/Blender/FFmpeg tools can be project tools, but they must not be automatically executed by broker or full-run tooling lanes unless an explicit application-domain task enables them.

Examples of application-domain tools that are not broker-safe by default:

```text
analyze_wav.py
build_track_summary.py
Scripting/v61b/main_v61b.py
Scripting/v61b/encode_image_sequence_v61b.py
Scripting/v61b/encode_ffmpeg_v61b.py
Scripting/v61b/hot_update_scene_v61b.py
Scripting/v61b/scene_tuning_panel.py
```

## Documentation status

Current documentation consolidation has removed or de-indexed old active-start runbooks and now routes through:

```text
AGENTS.md
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Legacy PR handoffs and master-branch runbooks should not be restored as active docs. Historical details should come from git history or compact evidence.

Current pruning principles:

```text
root docs stay descriptive and command-free
commands live in owning runbooks/tool READMEs
stable docs are indexed
historical evidence is not source documentation
no obsolete monolithic 0-to-10 runbook remains active
no audio/media runtime instructions from AI/tooling entrypoints unless explicitly scoped
```

## Evidence and artifact policy

Commit only compact Git-trackable evidence when required:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md
```

Do not commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
generated audio/video/media output
```

Production bundle and telemetry are the preferred handoff surfaces for full-run communication.

## Current blockers and limits

| Blocker / limit | Impact | Correct handling |
|---|---|---|
| External launcher controls not fully passed through | Some exposed knobs are documented/manifested but not yet wired into all subordinate calls. | Patch with ZIP bundle or focused workflow patch; validate PowerShell parser and dry-run locally. |
| Repository slug still says `blender-audio-project` | Name no longer reflects active architecture. | Docs use `IA-Carmine Local AI Orchestration Workbench`; repo rename needs explicit confirmation. |
| Ollama/provider health can degrade locally | Advisory lane may be unavailable in a given run. | Require workload quality routing and explicit diagnostics. |
| NPU smoke/probe does not prove general advisory quality | Prevents unsafe NPU promotion. | Keep NPU as probe/guardrail/diagnostic until quality gates prove usable advisory text. |
| `output/**` is ignored | Long local reports cannot be reviewed directly on GitHub. | Promote only compact evidence when needed. |
| Blender/audio/media runtime is frozen | Prevents accidental media generation or scene breakage. | Enter only with explicit application-domain task. |

## Active task queue status

| Area | Status | Notes |
|---|---|---|
| Unified launcher | active | Canonical local-AI entrypoint. |
| Full0To10 procedure | active | Current flow: everything active by default unless explicit `No*` flag disables it. |
| Runtime broker telemetry | closed / validated | `a85bbf4`; run `20260505-073332`. |
| Provider diagnostics | closed / validated | `c420c5c`; run `20260505-081141`. |
| GPU sync timing source | patched / smoke validated | `rounds[*].elapsed_seconds` is now primary source. |
| AI-to-AI bundle completeness | patched | Full-toolbox diagnostics added to bundle templates. |
| Project tool registry | seeded | Stable `docs/LOCAL_AI_TASKS/project-tool-registry.md` exists. |
| Tool governance | active | Tool placement audit and promotion guide are indexed. |
| Audio/media output guardrail | active | No media output during AI/tooling runs. |
| Documentation pruning | active | Legacy active-start runbooks removed, de-indexed or demoted. |
| Provider lane health | diagnostic | GPU/Ollama advisory explicit and quality-gated; NPU probe/diagnostic only. |
| Blender/audio domain | frozen for core AI work | Explicit application-domain tasks only. |

## Recommended next technical directions

1. Finish external-control pass-through for the unified launcher subordinate calls.
2. Keep pruning obsolete MD from active entrypoints while preserving compact evidence.
3. Enrich `project-tool-registry.md` from the next full-run evidence and tool inventory.
4. Promote only safe report-only tools to broker level.
5. Continue making telemetry/capability manifests first-class AI handoff inputs.
6. Filter patch-plan noise from archived evidence docs in a future quality improvement.
7. Keep no-audio/media guardrail visible in runbooks and PR reports.
8. Continue using compact production AI-to-AI bundles for cross-session communication.

## Do not do yet

Do not do these without explicit scope approval:

```text
rewrite Blender runtime packages
split Ready To Jazz monolith
migrate package imports broadly
change provider execution from explicit to implicit
edit full frame-level analysis JSON files
hand-edit generated AI/NPU indexes
claim NPU as general advisory lane based on smoke success
run audio playback/export, FFmpeg encode/mux, Blender render or media generation during AI/tooling work
rename the GitHub repository
merge to master
```

## Final technical position

The repository has crossed from a Blender/audio project into a local AI orchestration workbench.

The active architecture is now validated around:

```text
unified local-AI launcher as primary operator entrypoint
TUTTO SU TUTTO full-run doctrine with expandable perimeter
Ollama/GPU advisory when explicit and quality-gated
NPU/OpenVINO probe and decode-smoke diagnostics
quality-based advisory context filtering
runtime broker report and telemetry
runtime tool capability manifest
full toolbox telemetry summary
compact GitHub evidence bundles
production AI-to-AI bundles
task-scoped context packs
SQLite-backed local agent state
selected semantic chunks
deterministic recommendations
review-only patch specs
manual patch application
no audio/media output in normal AI/tooling runs
```

Blender/audio remains important as an application domain, but not as the project identity or architecture boundary.
