# Main Runtime Architecture

## Purpose

This document defines the primary runtime architecture target for `IA-Carmine Local AI Orchestration Workbench`.

It is a stable architecture contract for human maintainers, Codex, ChatGPT-assisted work and local AI agents. It describes the intended coordination model for provider lanes, tools, validators, shared state and telemetry.

This file is not a command catalog. Current executable runbooks and launcher flags remain in task-specific documentation and workflow scripts.

Current implemented capability depth is tracked separately in:

```text
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
```

Use that map to distinguish active, report-only, provider-gated, manual-review, local-private, target and legacy/diagnostic capabilities before claiming that an architecture component executed.

## Runtime topology

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

## Architectural doctrine

The runtime is moving from script-by-script orchestration to a coordinated shared execution model.

Core principles:

```text
state is shared through an explicit runtime heap / blackboard
provider lanes publish observations, proposals and diagnostics into shared state
only one broker executes tool actions and writes runtime events
semantic tools are registered, discovered and invoked by capability contract
CPU validators remain deterministic authority for pass/fail decisions
telemetry/event stream records what happened, what was skipped, what degraded and why
```

The architecture must preserve the existing report-only and manual-review posture unless a human explicitly requests execution or source-changing action.

## Component responsibilities

| Component | Responsibility | Authority |
|---|---|---|
| Shared runtime heap / blackboard | Shared state surface for plans, evidence, recommendations, tool outputs, validator results and event references. | State coordination only. |
| GPU1 primary advisory / planner | Main high-capacity advisory lane for planning, recommendation synthesis and patch-plan reasoning. | Advisory; cannot apply patches directly. |
| GPU0 coworker/helper OpenVINO | Secondary helper lane for auxiliary review, focused model tasks, local acceleration experiments or OpenVINO-backed support work. | Helper/advisory; not primary authority. |
| NPU microtask responder | Small bounded tasks, probes, decode smoke, guardrail checks, focused classification or quick-response diagnostics. | Microtask/diagnostic; not primary advisory by default. |
| Broker unico executor | Single executor for tool invocation, runtime capability routing and event emission. | Execution gateway; must enforce guardrails. |
| Semantic tools registry | Discoverable registry of tool capabilities, inputs, outputs, risk class and validation contract. | Capability source of truth. |
| Deterministic validators / CPU authority | Static and deterministic checks: syntax, contracts, schemas, file limits, reports, inventories and evidence validation. | Final local pass/fail authority. |
| Telemetry/event stream | Append-only runtime observation surface for tool usage, provider degradation, skipped phases, errors, warnings and evidence pointers. | Audit trail. |

## State model

The blackboard must not become an unbounded dump of raw provider output.

Preferred blackboard records are compact and typed:

```text
run metadata
phase status
provider lane status
capability registry snapshot
semantic tool invocation records
validator result references
recommendation summaries
patch-plan summaries
artifact/evidence manifests
telemetry/event stream pointers
warnings, errors and degradation reasons
```

Raw local artifacts stay under ignored runtime paths such as `output/**` and are represented by compact references or Git-trackable evidence when needed.

## Provider lane policy

### GPU1 primary advisory / planner

GPU1 is the preferred primary advisory/planning lane when available and explicitly selected by the active workflow.

Expected work:

```text
whole-repository planning
recommendation synthesis
patch-plan review
large-context advisory reasoning
cross-report interpretation
```

Restrictions:

```text
no direct patch application
no direct commit/push/merge
must route tool execution through broker
must be quality-gated by deterministic validators and telemetry
```

### GPU0 coworker/helper OpenVINO

GPU0 is a helper/coworker lane, useful for focused secondary work and OpenVINO-assisted support.

Expected work:

```text
secondary review
focused classification
small model helper tasks
provider comparison diagnostics
auxiliary semantic processing
```

Restrictions:

```text
must not silently replace GPU1 primary advisory
must not become authority over deterministic validators
must not execute repository mutations outside broker policy
```

### NPU microtask responder

NPU is a bounded microtask and diagnostic responder.

Expected work:

```text
probe / smoke / decode diagnostics
small classification tasks
quick guardrail responses
focused context checks
microtask confirmations
```

Restrictions:

```text
not primary advisory by default
not patch-plan authority
not source-write authority
not a reason to skip CPU validators
```

## Broker unico executor

The broker is the only runtime component that should execute registered tools.

It must enforce:

```text
one execution path for tools
capability lookup through semantic tools registry
risk-aware invocation policy
explicit provider execution flags when required
no implicit patch apply
no implicit Blender or FFmpeg runtime
no implicit commit, push, merge or delete
structured event emission for every action
```

If multiple provider lanes propose actions, the broker arbitrates execution through deterministic policy and validator feedback, not through provider preference alone.

## Semantic tools registry

The registry should describe each tool in a machine-readable way:

```text
tool id
owner module
capability tags
input contract
output contract
risk class
provider requirements
writes performed
runtime artifacts produced
validator to run after invocation
telemetry fields emitted
```

The registry is the foundation for scalable growth: new tools become discoverable capabilities instead of ad-hoc script calls.

## Deterministic validators / CPU authority

CPU validators remain the final authority for local correctness claims.

Examples:

```text
Python syntax validation
PowerShell parser validation
JSON/report contract validation
repository proposal validation
patch spec validation
file-line-limit validation
selected chunk/evidence validation
Git diff whitespace validation
```

Provider output can recommend or explain; validators decide whether the repository state and reports are acceptable.

## Telemetry/event stream

Every meaningful runtime action should leave structured telemetry.

Minimum event classes:

```text
phase_started
phase_completed
phase_failed
tool_invoked
tool_skipped
provider_requested
provider_degraded
provider_unavailable
validator_passed
validator_failed
artifact_written
evidence_compacted
guardrail_blocked_action
```

Telemetry must make silent fallback visible. A lane can be skipped or degraded only when the manifest, telemetry or validator evidence says so explicitly.

## Full0To10 integration

`Full0To10` remains **TUTTO SU TUTTO**.

This architecture expands what `tutto` should eventually cover:

```text
blackboard state
GPU1 advisory/planner lane
GPU0 coworker/helper OpenVINO lane
NPU microtask responder lane
broker execution report
semantic tools registry snapshot
deterministic validator authority report
telemetry/event stream summary
compact evidence bundle
```

Run intensity may change budget and depth, not the semantic scope of available lanes.

## Codex/refactor implications

When refactoring workflow scripts or provider orchestration, prefer this direction:

```text
PowerShell wrappers stay thin and compatible
Python modules own runtime state, manifests, tool calls and validation surfaces
broker logic is centralized, not duplicated in per-script runners
provider lanes publish to blackboard instead of applying side effects directly
semantic tool metadata is explicit and testable
validators remain deterministic and report-only unless explicitly scoped otherwise
telemetry is emitted for executed, skipped and degraded phases
```

Do not implement this architecture through a single monolithic file. Split by responsibility and preserve the 400-line policy for maintained source and Markdown.

## Guardrails

This architecture does not authorize:

```text
automatic patch application
automatic merge to master
force-push or history rewrite
secret, permission, billing or visibility changes
Blender runtime execution
FFmpeg runtime execution
provider execution without explicit workflow request
committing output/**, renders/**, SQLite databases or generated raw indexes
```

## Related documents

Read with:

```text
AGENTS.md
docs/README.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md
```
