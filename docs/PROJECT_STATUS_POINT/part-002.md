<!-- IA-CARMINE-MD-SPLIT: part -->
# PROJECT_STATUS_POINT — parte 002 di 002

Sorgente indice: [`../PROJECT_STATUS_POINT.md`](../PROJECT_STATUS_POINT.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

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
