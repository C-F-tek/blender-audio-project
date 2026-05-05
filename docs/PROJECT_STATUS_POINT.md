# Project Status Point

## Purpose

Current technical status of `IA-Carmine Local AI Orchestration Workbench` for GitHub-only and local continuation work.

The repository slug remains `C-F-tek/blender-audio-project`, but the active architecture is now local AI orchestration, provider-lane routing, validation, evidence, runtime broker telemetry, tool governance and manual-review patch planning.

Blender/audio remains the first application domain. It is not the boundary of the active architecture.

## Current doctrine

The active operating doctrine is **run unica parametrica + TUTTO SU TUTTO**.

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
```

`-Full0To10` means whole-repository coverage across active lanes. `quick`, `balanced`, `deep` and `custom` change budgets, limits, rounds, context, tokens and depth; they do not change semantic scope.

The perimeter of `tutto` is expandable. When a new tool, broker capability, validation lane, provider diagnostic, evidence surface, repository-consistency check, memory/context builder, discovery/index surface or CSV/count surface becomes production-ready, it must be added to the run unica full-run contract or explicitly excluded with rationale.

Telemetry is AI-critical evidence. Future local/cloud AI agents must use telemetry to decide whether a lane was executed, failed, blocked, degraded, skipped intentionally or unavailable; file existence alone is not enough.

## Current branch context

Current consolidation branch:

```text
codex/unified-local-ai-refactor-launcher
```

Current active phase:

```text
PR: #187 feat(workflow): add unified local AI refactor launcher
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
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

The active local-AI operator model is unified around one parameterized launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

The unified launcher owns the run unica. Older monolithic full-toolbox, code-refactor and Markdown-refactor 0-to-10 runbooks are not active starting points.

Current supporting docs:

```text
FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

## Current operator posture

```text
manifest-first review
one parameterized run unica
Full0To10 perimeter = TUTTO SU TUTTO
quick/balanced/deep/custom as parameters, not scope profiles
provider/probe/workload-quality lanes included by default in Full0To10 unless disabled/unavailable
CSV/count and discovery/index surfaces included when relevant
workload quality gate before primary advisory routing
Ollama/GPU advisory quality-gated and opt-out under Full0To10
NPU/OpenVINO probe/guardrail/decode diagnostic opt-out under Full0To10
SQLite memory local-only and non-committed
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
| GPU/CUDA | Ollama | Primary advisory provider for Full0To10 when available and quality-gated. | Included by default unless disabled or diagnosed unavailable. |
| NPU/OpenVINO | OpenVINO GenAI | Probe, guardrail and decode diagnostics. | Included by default for diagnostics unless disabled or diagnosed unavailable; not promoted to general advisory lane. |
| Blender/audio/media runtime | Blender Python, FFmpeg, audio tools | Application-domain runtime. | Frozen unless explicitly scoped. |

Provider execution is explicit when the operator selects `-Full0To10` or provider/probe modes. It is not an additional per-lane opt-in after Full0To10 is selected.

A full tooling run must not silently treat degraded provider lanes as successful advisory output.

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

Relevant compact context:

```text
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
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

## Discovery, index repair and CSV/count status

Discovery and count surfaces are evidence lanes, not source authority.

Expected surfaces when relevant:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report when scanner/index visibility drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Policy:

```text
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Do not hand-edit generated indexes/chunks as source.
Index repair is plan/report-first unless explicitly requested.
CSV/count outputs support review and sizing but do not override source code or canonical docs.
```

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

Audio/Blender/FFmpeg tools can be project tools, but they must not be automatically executed by broker or run unica tooling lanes unless an explicit application-domain task enables them.

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
CHATGPT.md
CHATGPT/README.md
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
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
indexAI/code_chunks/**
raw checkpoints
large full analysis JSON outside compact evidence policy
generated audio/video/media output
```

Production bundle and telemetry are the preferred handoff surfaces for run-unica communication.

## Current blockers and limits

| Blocker / limit | Impact | Correct handling |
|---|---|---|
| Runtime bundle `20260505-143844` not committed | GitHub-only agents may not inspect the ZIP through standard repo files. | Use PR comment/compact docs until the bundle is locally inspected or uploaded. |
| External launcher controls not fully passed through | Some exposed knobs are documented/manifested but not yet wired into all subordinate calls. | Follow-up patch; do not treat as current P1 unless selected. |
| Repository slug still says `blender-audio-project` | Name no longer reflects active architecture. | Docs use `IA-Carmine Local AI Orchestration Workbench`; repo rename needs explicit confirmation. |
| Ollama/provider health can degrade locally | Advisory lane may be unavailable in a given run. | Require workload quality routing and explicit diagnostics. |
| NPU smoke/probe does not prove general advisory quality | Prevents unsafe NPU promotion. | Keep NPU as probe/guardrail/diagnostic until quality gates prove usable advisory text. |
| `output/**` is ignored | Long local reports cannot be reviewed directly on GitHub. | Promote only compact evidence when needed. |
| Blender/audio/media runtime is frozen | Prevents accidental media generation or scene breakage. | Enter only with explicit application-domain task. |

## Active task queue status

| Area | Status | Notes |
|---|---|---|
| Unified launcher / run unica | active | Canonical local-AI entrypoint. |
| Full0To10 perimeter | active | Everything active by default unless explicit `No*` flag, unavailable diagnostic or documented exclusion disables it. |
| Refactor/reuse full-run review | active P1 | Run `20260505-143844`; inspect runtime bundle before selecting patch. |
| Discovery/index/CSV-count surfaces | active evidence surfaces | Included when relevant; no generated-index commit unless explicitly requested. |
| Runtime broker telemetry | closed / validated | `a85bbf4`; run `20260505-073332`. |
| Provider diagnostics | closed / validated baseline | `c420c5c`; run `20260505-081141`. New runs may still degrade but must expose diagnostics. |
| GPU sync timing source | patched / smoke validated | `rounds[*].elapsed_seconds` is now primary source. |
| AI-to-AI bundle completeness | patched | Full-toolbox diagnostics added to bundle templates. |
| Project tool registry | seeded | Stable `docs/LOCAL_AI_TASKS/project-tool-registry.md` exists. |
| Tool governance | active | Tool placement audit and promotion guide are indexed. |
| Audio/media output guardrail | active | No media output during AI/tooling runs. |
| Documentation pruning | active | Legacy active-start runbooks removed, de-indexed or demoted. |
| Provider lane health | diagnostic | GPU/Ollama advisory quality-gated; NPU probe/diagnostic only. |
| Blender/audio domain | frozen for core AI work | Explicit application-domain tasks only. |

## Recommended next technical directions

1. Inspect the `20260505-143844` refactor/reuse runtime bundle and classify recommendations/patch plans.
2. Select a review-first refactor/reuse patch family only after evidence review.
3. Keep pruning obsolete MD from active entrypoints while preserving compact evidence.
4. Enrich `project-tool-registry.md` from the next run-unica evidence and tool inventory.
5. Promote only safe report-only tools to broker level.
6. Continue making telemetry/capability manifests first-class AI handoff inputs.
7. Filter patch-plan noise from archived evidence docs in a future quality improvement.
8. Keep no-audio/media guardrail visible in runbooks and PR reports.
9. Finish external-control pass-through as a follow-up after the current refactor/reuse phase or when explicitly selected.

## Do not do yet

Do not do these without explicit scope approval:

```text
rewrite Blender runtime packages
split Ready To Jazz monolith
migrate package imports broadly
edit full frame-level analysis JSON files
hand-edit generated AI/NPU indexes
claim NPU as general advisory lane based on smoke success
run audio playback/export, FFmpeg encode/mux, Blender render or media generation during AI/tooling work
rename the GitHub repository
merge to master
change Full0To10 from opt-out-by-lane to silent opt-in per capability
```

## Final technical position

The repository has crossed from a Blender/audio project into a local AI orchestration workbench.

The active architecture is now validated around:

```text
run unica parameterized local-AI launcher as primary operator entrypoint
TUTTO SU TUTTO perimeter with expandable coverage
quick/balanced/deep/custom as execution parameters, not scopes
Ollama/GPU advisory quality-gated and included by default in Full0To10 when available
NPU/OpenVINO probe and decode-smoke diagnostics included by default in Full0To10 when available
quality-based advisory context filtering
runtime broker report and telemetry
runtime tool capability manifest
full toolbox telemetry summary
compact GitHub evidence bundles
production AI-to-AI bundles
task-scoped context packs
SQLite-backed local agent state
selected semantic chunks
CSV/count evidence surfaces
auto-discovery and index repair reports/plans
deterministic recommendations
review-only patch specs
manual patch application
no audio/media output in normal AI/tooling runs
```

Blender/audio remains important as an application domain, but not as the project identity or architecture boundary.
