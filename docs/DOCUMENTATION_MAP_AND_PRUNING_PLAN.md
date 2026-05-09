# Documentation Map and Pruning Plan

## Purpose

Control point for reducing Markdown redundancy and keeping one clear reading flow.

The goal is not to add more documentation. The goal is to make each Markdown file have a lifecycle, owner and reading position. New stable material must update an existing canonical document or explicitly mark older material as superseded, historical, generated or delete-candidate.

This file is report-only. It does not authorize deletion by itself.

## Canonical entrypoint chain

| Rank | File | Role | Rule |
|---:|---|---|---|
| 1 | `AGENTS.md` | Hard AI/agent contract | Keep compact; guardrails only. |
| 2 | `CHATGPT.md` | ChatGPT memory pointer | Current handoff and session-memory index. |
| 3 | `CHATGPT/README.md` | ChatGPT memory index | Compact reading order for resumed sessions. |
| 4 | `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` | Current branch state bridge | Start here for phase context. |
| 5 | `docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md` | Current capability depth map | Distinguish active/report-only/provider-gated/manual-review/target capability. |
| 6 | `docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md` | Launcher parameter decision map | Choose lane before flags. |
| 7 | `docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md` | Hidden/old script review queue | Notice wrappers/legacy scripts; not a deletion list. |
| 8 | `README.md` | Human project identity | Keep short; link to workflows. |
| 9 | `WORKFLOW.md` | Operational lifecycle | Keep short; no scenario-specific long runs. |
| 10 | `docs/README.md` | Documentation index | Single reading flow and doc family map. |
| 11 | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | Markdown lifecycle and pruning policy | Cleanup control point. |
| 12 | `docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md` | GPU1/GPU0/NPU role contract | Canonical peer-exchange doctrine. |
| 13 | `docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md` | MD-only cleanup policy | GitHub-only doc coherence rules. |
| 14 | `docs/LOCAL_AI_RUN_BOOTSTRAP.md` | Local checkout bootstrap | Local-run prerequisites. |
| 15 | `docs/LOCAL_AI_TASKS/README.md` | Task routing | Current vs historical task entrypoints. |
| 16 | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Unified local AI run-unica entrypoint | Canonical launcher runbook. |
| 17 | `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` | Current code/tool/evidence flow | Launcher, provider, broker, telemetry, discovery, CSV, bundle and evidence flow. |
| 18 | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` | Tool placement audit | Tool/candidate classification. |
| 19 | `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` | Tool promotion guide | Project-tool, broker-tool and full-run-lane promotion. |
| 20 | `Tools/validation/README.md` | Validator catalog | Tool commands and contracts only. |

Legacy monolithic 0-to-10 runbooks have been removed or demoted from the active documentation set. The unified launcher is now the only active run-unica entrypoint.

## Run unica / TUTTO SU TUTTO pruning rule

Markdown that describes local-AI execution must preserve:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = budget/intensity, not scope reduction
-No* flags = explicit opt-out from selected lanes
```

Prune or rewrite docs that imply a quick Full0To10 run is a partial run, that legacy wrappers are first entrypoints, or that a run-unica flow may silently skip core lanes.

The perimeter of `tutto` is expandable. New stable lanes and data surfaces must update canonical docs or be explicitly excluded with rationale.

## Capability and parameter map rule

Docs are stale if a new AI must infer capability or launcher parameters from scattered historical runbooks.

Canonical decision surfaces:

```text
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
```

Rules:

```text
capability map answers what exists and what evidence proves it
parameter map answers which launcher lane/flags to use
script aging audit answers what may be hidden/legacy and needs review
older docs must link to these maps rather than restating partial state
```

## GPU peer-exchange pruning rule

Docs are stale if they describe local AI lanes as isolated providers only.

Canonical production roles:

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner
GPU0 / OpenVINO = companion peer worker
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1 and GPU0 requests
```

Docs must not present GPU0 as only preflight, smoke or final evidence. Missing peer exchange must be classified explicitly.

Canonical document:

```text
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
```

## Visibility-first documentation rule

A local-AI run must be understandable from compact, indexed surfaces before opening detailed evidence.

Required reading order:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
runtime tool telemetry and capability manifest
full toolbox telemetry summary
production AI-to-AI bundle
compact Markdown or CSV/count summaries
detailed evidence only when needed
```

Do not use a long generated bundle as the first operational interface.

## Telemetry-first pruning rule

Telemetry is a maintained documentation concern because it controls how future AI agents interpret a run.

Docs are stale if they encourage any of these patterns:

```text
infer success from output file existence alone
treat broker telemetry as optional after a broker lane ran
hide provider degradation outside the AI-to-AI handoff
omit capability manifests from full-run communication
claim patch/source writes happened without telemetry evidence
claim a lane succeeded without executed/failed/blocked/degraded fields
```

Canonical telemetry handoff surfaces:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

## Discovery/index/CSV pruning rule

Discovery and count surfaces are evidence, not source authority.

Docs are stale if they:

```text
treat generated indexes or code chunks as manually maintained source
commit or recommend committing output/** as ordinary source
commit or recommend committing indexAI/code_chunks/**
omit Python line-count CSV/MD from refactor/reuse review reporting
omit function/class/method CSV from duplication/helper-reuse review
treat index repair as automatic source mutation instead of plan/report-first
```

## Length and readability policy

| File type | Preferred maximum | Hard action threshold | Required action when exceeded |
|---|---:|---:|---|
| Active operator runbook | ~400 lines | 500 lines | Split, summarize or move verbose detail to supporting docs. |
| Maintained source documentation | ~400 lines | 500 lines | Keep original as compact index and move detail to `<file>.md/part-xxx.md`. |
| Generated compact evidence | ~1200 lines | N/A | Add manifest/summary and classify as evidence. |
| Large historical/evidence bundle | Any size only if unavoidable | N/A | Must be indexed and must not be the first operational entrypoint. |

Policy:

```text
No active runbook should require opening a huge bundle.
Generated evidence may be long only if it has a compact manifest/summary.
Prefer manifest + index + focused report over one huge Markdown file.
Do not create new monolithic AI-to-AI bundles without companion manifests.
```

## Repository Markdown families

| Family | Pattern | Lifecycle |
|---|---|---|
| Root entrypoints | `AGENTS.md`, `README.md`, `WORKFLOW.md` | Canonical, concise |
| ChatGPT memory | `CHATGPT.md`, `CHATGPT/*.md` | Advisory operational memory |
| Session notes | `docs/AI_SESSION_NOTES/*.md` | Factual notes; promote stable rules to canonical docs |
| Stable docs | `docs/*.md` | Maintained source docs |
| Task runbooks | `docs/LOCAL_AI_TASKS/*.md` | Current task input, supporting detail or historical handoff |
| Tool governance | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-*.md`, `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-*.md` | Tool discovery and promotion |
| Execution plans | `docs/EXECUTION_PLANS/**/*.md` | Durable state records |
| Evidence | `docs/LOCAL_VALIDATION_EVIDENCE/*` | Snapshot evidence, not source docs |
| Tool READMEs | `Tools/**/README.md` | Package-local |
| Generated/index context | `indexAI/**/*.md`, `Tools/npu/npu_code_*.md` | Regenerated, not hand-edited |
| Blender/application docs | `Scripting/**/*.md` | Application-domain only |

## Duplication map

| Topic | Canonical target | Pruning rule |
|---|---|---|
| Provider lane policy | `AGENTS.md`, `LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md` | Other docs link or summarize one line. |
| Current capability status | `LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md` | Other docs do not duplicate status matrices. |
| Launcher parameter selection | `LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md` | Other docs avoid flat parameter lists unless generated from code. |
| Script aging / hidden wrappers | `LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md` | Do not delete from age alone. |
| Run unica procedure | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | No copied command blocks in entrypoints. |
| TUTTO SU TUTTO doctrine | `AGENTS.md`, `README.md`, `WORKFLOW.md`, `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Other docs may summarize but must not narrow scope. |
| MD-only cleanup | `LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md` | Other docs link to it. |
| Current code/tool/evidence flow | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` | Other docs link or summarize. |
| Telemetry-first AI handoff | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md`, `LOCAL_AI_WORKFLOW.md`, `DATA_FLOW.md` | Do not scatter conflicting success criteria. |
| Discovery/index/CSV-count surfaces | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md`, `DATA_FLOW.md`, `LOCAL_AI_WORKFLOW.md` | Do not treat generated indexes as source. |
| Historical full-toolbox procedure | git history / compact evidence | Do not restore as active runbook. |
| Evidence bundle policy | `WORKFLOW.md` and unified launcher runbook | Evidence snapshots are not source docs. |
| Validation command catalog | `Tools/validation/README.md` | Task docs list only focused commands. |

## Add-before-prune rule

When adding or updating Markdown:

1. Check whether the content belongs in an existing canonical file.
2. If a new file is needed, add it to the correct index.
3. Mark older overlap as one of:
   - `superseded by <path>`
   - `historical evidence`
   - `application-domain only`
   - `generated, do not hand-edit`
   - `delete candidate, requires explicit approval unless clearly obsolete and non-evidence`
4. Replace repeated commands with links to canonical runbooks.
5. Run Markdown inventory and docs link validation when local execution is available.

## Safe cleanup actions

Allowed without deletion:

```text
shorten root entrypoints
update indexes
mark historical/superseded/domain-only status
replace copied command blocks with canonical links
add or update report-only inventory tooling
add visibility/length policy
add guardrails for provider/runtime/broker/media side effects
update telemetry-first handoff rules
update run-unica terminology and opt-out semantics
update discovery/index/CSV evidence rules
```

Deletion is allowed only for clearly obsolete non-evidence docs or when explicitly requested. Do not delete compact validation evidence only because it is old.

Never treat as manually maintained source:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.md
indexAI/**/*.md
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
output/**/*.md
```

## Audio/media output pruning rule

Normal AI/tooling docs must not imply that full-run validation, broker telemetry, provider diagnostics, tool promotion or patch planning may produce media output.

If a document describes audio playback, audio export, FFmpeg encoding, muxing, Blender render or media generation, classify it as one of:

```text
application-domain doc
historical evidence
explicit media runtime task
guardrail breach report
```

## Current cleanup sequence

1. Keep root entrypoints focused on the single reading flow.
2. Keep current capability, parameter and script visibility maps indexed before historical task runbooks.
3. Keep the canonical unified launcher as the only active run-unica command surface.
4. Keep TUTTO SU TUTTO and expandable perimeter doctrine visible.
5. Keep GPU peer-exchange doctrine visible.
6. Keep broker telemetry, capability manifest, provider quality and full toolbox telemetry visible.
7. Keep discovery/index/CSV-count surfaces visible in refactor/reuse and run-unica docs.
8. Keep no-audio/media output policy visible in task routing.
9. Use inventory output to identify missing-index, long-file and prune candidates.
10. Split maintained Markdown over 500 lines using `<file>.md/part-xxx.md`.
11. Validate links and report contracts after deletion when local execution is available.

## Acceptance criteria

```text
single reading flow is explicit
capability depth map is indexed before historical runbooks
launcher parameter decision map is indexed before copied command blocks
script aging visibility audit is indexed before cleanup/deprecation work
unified launcher is the active run-unica entrypoint
TUTTO SU TUTTO remains full-scope across quick/balanced/deep/custom parameters
GPU1/GPU0/NPU peer-exchange roles are documented
root entrypoints are compact
active Markdown files stay <= 500 lines or are split/indexed
stable docs are indexed or intentionally excluded
evidence/generated MD is not treated as source documentation
script/tool inventory is available for refactor planning
runtime broker telemetry and capability manifest are surfaced when relevant
full toolbox telemetry summary is included in AI-to-AI handoff
audio/media output is forbidden in normal AI/tooling runs
no output/**, indexAI/code_chunks/**, renders/**, generated media, *.db or *.sqlite files are committed
no obsolete monolithic 0-to-10 runbook remains indexed as active documentation
```
