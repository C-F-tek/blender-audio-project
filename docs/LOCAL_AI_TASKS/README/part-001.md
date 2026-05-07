<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_AI_TASKS README — part 001 of 002

Source index: [`../README.md`](../README.md)

## Navigation

- [Split index](README.md)
- [Next part](part-002.md)

# Local AI Tasks

Markdown task files and operator entrypoints for local AI work.

This index is a router, not a command source. Executable commands for full runs, quick tests, deep tests, reset, provider probes, memory, discovery repair, CSV/count surfaces and patch-spec generation live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Non-negotiable rule

There is one active local-AI operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

All test/full-run/provider/memory/patch-spec/reset/discovery/index-repair flows must be expressed as launcher modes, profiles, flags or explicitly scoped helper tools behind the launcher.

Do not create or promote separate active-start runbooks for:

```text
full toolbox runs
code-refactor runs
Markdown-refactor runs
provider probes
full validation
quick tests
deep tests
reset cleanup
SQLite memory handoff
patch-spec generation
auto-discovery repair
index repair
CSV/count generation
```

Supporting wrappers may exist, but they are implementation lanes behind the launcher or explicitly scoped helper tools.

## Current active state

Current compact operational bridge:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

Current code-derived behavior map:

```text
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
```

Recent telemetry baseline:

```text
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
```

Historical telemetry notes are useful context only when current code and current run manifests confirm relevance.

## TUTTO SU TUTTO doctrine

Every full-run task must preserve whole-repository coverage: **TUTTO SU TUTTO**.

`quick`, `balanced`, `deep` and `custom` are budget/intensity profiles. They do not define smaller scopes. A quick full run still traverses all active full-run lanes with reduced capacity; it is not a smoke test.

The set of lanes is allowed to grow. New production-ready tools, broker capabilities, provider diagnostics, registries, evidence builders, memory/context surfaces, repository-consistency checks, auto-discovery repair, index repair and CSV/count surfaces must update the full-run contract or be explicitly excluded.

## GPU peer-exchange doctrine

Canonical production roles:

```text
GPU1 / Ollama / RTX 5080 = primary advisory planner
GPU0 / OpenVINO = companion peer worker
NPU = non-blocking micro/task assistant unless explicitly promoted by code/config
Deterministic scripts = heavy audit and validation authority
Runtime tool broker = controlled tool execution for provider requests
```

Canonical document:

```text
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
```

Current implementation details and caveats are tracked in the code-derived map.

## Current stable reading order

Use this order for current IA-Carmine local-AI work:

```text
1. CHATGPT/README.md
2. docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
3. docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
4. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
5. docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
6. docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md
7. docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
8. docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
9. docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
10. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
11. docs/LOCAL_AI_TASKS/project-tool-registry.md
12. docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
13. docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
14. docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

Do not start from historical PR handoffs, legacy master-branch runbooks, or long semi-automatic procedure snapshots.

## Required context

Every active task file must preserve hard guardrails from:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

If a task conflicts with `AGENTS.md`, preserve hard guardrails and stop with a conflict report.

## Visibility-first rule

Every local-AI run must be inspectable from compact surfaces before opening detailed evidence.

Required reading order for a run:

```text
1. launcher command from unified-local-ai-refactor-launcher.md
2. unified_local_ai_refactor_manifest.json
3. phase_status / phase_reports
4. production bundle and telemetry summary
5. compact Markdown or CSV/count summaries
6. detailed evidence only when needed
```

Each active launcher phase should expose at least one visible output:

```text
phase_status
phase_reports
context_files
report_files
compact Markdown summary
CSV/JSON inventory
line-count CSV
function/class/method inventory CSV
index repair report
auto-discovery report
```

## Discovery, index repair and CSV/count surfaces

Discovery and count surfaces are part of `TUTTO SU TUTTO` when relevant.

Expected surfaces include:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
file line-limit JSON/MD report
semantic chunk manifest
selected chunk evidence
repository consistency map/smoke
auto-discovery or missing-index report
index repair plan/report
```

Policy:

```text
CSV/count outputs are evidence surfaces, not source authority.
Generated indexes and code chunks are not hand-maintained source.
Do not commit output/** or indexAI/code_chunks/**.
Commit only compact evidence under docs/LOCAL_VALIDATION_EVIDENCE when needed.
Index repair must be plan/report-first unless explicitly requested.
```

## Markdown and code line policy

Maintained documentation and source files must stay small enough for human review and AI-assisted patching.

```text
active Markdown hard threshold: <= 500 lines
preferred active runbook: <= 400 lines
maintained Python/PowerShell/script file: <= 400 lines
```

Markdown split rule:

```text
Keep the original file as a compact index.
Create a sibling folder named exactly like the file, including .md: <file>.md/.
Move detailed content into <file>.md/part-001.md, part-002.md, ...
Keep each part <= 500 lines.
The index must list all parts and state why the document was split.
```

Code split rule:

```text
Keep public entrypoints/wrappers compact.
Move implementation into a same-purpose package or module folder.
Split by responsibility, not by arbitrary line number only.
Preserve CLI/API compatibility unless explicitly allowed to break it.
Report resulting line count for every created or modified code/script file.
```

Existing files already over the limits are technical debt. Do not split them blindly during unrelated work.

## Maintained task files

| File | Status | Purpose |
|---|---|---|
| `code-derived-ai-toolchain-map-2026-05-07.md` | active map | Source-code-derived behavior map for launcher, full-toolbox, provider mesh and review PR phases. |
| `current-operational-state-2026-05-05.md` | active bridge | Compact current state and guardrails. |
| `gpu-peer-exchange-operational-principle.md` | active principle | GPU1/Ollama, GPU0/OpenVINO, NPU and deterministic validator roles. |
| `patch-suggestion-bundle-final-phase.md` | active final phase | Current deterministic patch suggestion and review PR final-phase behavior. |
| `md-coherence-only-github-pass-2026-05-06.md` | active policy | GitHub-only Markdown cleanup, split and pruning policy. |
| `file-line-limit-validator-2026-05-06.md` | active validator note | File line-limit validator contract. |
| `refactor-reuse-methods-classes-tools-planning.md` | active P1 task | Method/class/helper/tool reuse planning. |
| `recent-telemetry-state-2026-05-05.md` | active baseline | Recent telemetry and broker context. |
| `unified-local-ai-refactor-launcher.md` | canonical active | Operator guide for the single full-run entrypoint. |
| `no-audio-media-output-guardrail-2026-05-05.md` | active guardrail | Prevent unintended media output in AI/tooling runs. |
| `tool-inventory-placement-audit-2026-05-05.md` | active audit | Repository-wide tool/candidate audit. |
| `project-tool-promotion-and-insertion-guide-2026-05-05.md` | active guide | Project tool, broker tool and full-run lane promotion. |
| `project-tool-registry.md` | active registry | Project-tool registry and promotion visibility surface. |
| `current-code-flow-guide-2026-05-05.md` | active guide | Current launcher/provider/broker/bundle/evidence flow. |

## Historical task files

Historical handoffs and generated evidence remain useful as past state, but must not become the first reading path unless explicitly referenced.

Rules:

```text
Do not promote historical PR handoffs back to active entrypoints.
Do not use generated evidence snapshots as canonical workflow docs.
Do not delete production evidence automatically; evidence pruning requires a separate explicit evidence-retention decision.
```

## Audio/media output guardrail

Normal AI/tooling runs must not produce application-domain media output.

Forbidden side effects during docs/provider/tooling/evidence/refactor tasks:

```text
audio playback
audio export
WAV/MP3/AAC conversion
FFmpeg encode or mux operation
Blender render
video generation
media output side effect
```

Use `no-audio-media-output-guardrail-2026-05-05.md` for detailed policy.
