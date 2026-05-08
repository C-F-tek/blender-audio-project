# AI Memory Policy

## Purpose

This document defines how local agent memory is kept useful without becoming noisy, stale or unsafe.

The policy applies to generic memory records produced by:

```text
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/ai/build_agent_memory_inventory.py
indexAI/agent_memory/agent_memory.sqlite
```

The active memory-aware local-AI entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

This policy is not a command catalog. Current memory-aware run commands live in the unified launcher runbook.

## Current code-driven references

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Full-run memory doctrine

Memory/context is part of **TUTTO SU TUTTO** when enabled by the unified launcher.

`Full0To10` should include memory input/output surfaces unless explicit memory disablers are used. A memory lane must not silently disappear from a full run.

Memory output must be visible through compact, non-private surfaces:

```text
unified manifest memory fields
phase_status / phase_reports
agent-state packet path
runtime telemetry / full toolbox telemetry summary when relevant
shared AI-to-AI bundle reference when used for handoff
```

SQLite DB files remain private local runtime state. They are never the handoff artifact and must not be committed.

Telemetry explains whether memory/context was enabled, disabled, skipped or unavailable. It does not replace memory evidence or agent-state packets; it accompanies them.

## Active memory components

These files are active memory/context helpers and must not be treated as forgotten or obsolete simply because they are not all user-facing commands.

| File | Role | User-facing status |
|---|---|---|
| `Tools/ai/agent_state.py` | Generic memory record and microtask packet model. | Internal library. |
| `Tools/ai/build_agent_state_packet.py` | Builds task-local agent-state packets and optional memory handoff context. | Supporting CLI, invoked by unified launcher. |
| `Tools/ai/review_agent_memory.py` | Reviews local memory for keep/promote/quarantine/drop decisions. | Supporting CLI. |
| `Tools/ai/build_agent_memory_inventory.py` | Builds memory inventory / visibility reports. | Supporting CLI. |
| `Tools/ai/agent_memory_policy.py` | Deterministic retention and promotion policy logic. | Internal policy module. |
| `Tools/ai/agent_memory_routing_policy.py` | Routing policy for memory selection and context placement. | Internal policy module. |
| `Tools/ai/agent_runtime_sqlite_memory.py` | SQLite-backed runtime memory helpers. | Internal/local runtime helper. |
| `Tools/npu/ai_memory_context.py` | NPU-side memory/context integration helper. | Runtime-adjacent helper; provider execution remains explicit. |

Policy:

```text
Do not remove these references unless the corresponding files are removed from the repo.
Do not commit SQLite DBs or local memory output files.
Do not select quarantined/private/local-only records into provider prompts.
Expose memory input/output in the unified launcher manifest when used.
Expose memory/context handoff state in telemetry or bundle surfaces when it contributes to a production run.
```

## Storage

Default local SQLite path:

```text
indexAI/agent_memory/agent_memory.sqlite
```

This path is generated local data and must stay untracked.

JSONL memory is allowed when append-only reviewability matters more than lookup speed.

## Launcher integration

Memory is part of the unified flow through launcher modes and flags.

Expected surfaces when memory is enabled:

```text
mode includes agent_state or Full0To10 implies agent_state
memory_db recorded in unified manifest
memory_in_enabled recorded in unified manifest
memory_out_enabled recorded in unified manifest
save_inputs_to_memory_db recorded in unified manifest
agent-state packet path recorded in phase_reports/context_files when produced
memory/context contribution referenced in telemetry/bundle when part of production handoff
SQLite DB remains untracked
```

`Full0To10` should include memory IN/OUT unless explicitly disabled with documented memory controls in the unified launcher runbook.

## Record Shape

Every memory record should remain generic:

```text
record_id
kind
scope
source
summary
content
tags
confidence
created_at
updated_at
expires_at
metadata
```

Do not create Blender-only, audio-only or app-only memory schemas. Use `kind`, `scope`, `source`, `tags` and `metadata` to adapt the same record model to future file types, multi-file tasks or specialized agents.

## Retention Actions

| Action | Meaning |
|---|---|
| `keep` | Safe to keep selecting when relevant. |
| `human_review` | Still usable, but old or low-confidence enough to review. |
| `trim_review` | Useful but oversized; distill before long-term reuse. |
| `expire_review` | Old or explicitly expired; do not rely on it without review. |
| `quarantine` | Potential secret or blocked content; do not select into context. |
| `promote_candidate` | Good candidate for human promotion into stable docs or curated memory. |
| `drop_candidate` | Safe to ignore or delete after human review because it is obsolete, duplicate, noisy or not useful. |

The review tool is non-destructive. It never deletes records or writes promoted docs by itself.

## Promotion Rule

Promote only distilled, durable lessons:

```text
validated constraints
runtime validation results
architecture decisions
guardrail decisions
provider/broker/validator telemetry decisions
Blender/audio smoke outcomes with explicit application-domain scope
known risks with date and scope
```

Do not promote:

```text
raw chat noise
temporary CLI notes
large source dumps
secrets or credentials
unverified assumptions
obsolete local paths unless needed for reproducibility
old PR/branch state already superseded by merged docs
```

Promotion means copying a reviewed summary into a stable current target such as:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/TECH_DEBT_TRACKER.md
docs/EXECUTION_PLANS/
curated JSONL memory selected by the app
```

Historical/reference docs such as `docs/PROJECT_STATUS_POINT.md` must not receive new current-state memory unless they are first reclassified as active.

## Generic examples

These examples are intentionally input-agnostic and output-application-agnostic. They can apply to Blender/audio work, non-Blender generated Python, report contracts or future adapters.

### Retain / keep

Use `keep` when a record is validated, scoped and still useful.

Example record summary:

```text
Generated Python policy warnings do not fail validation; syntax errors fail. Application adapters should compose the generic policy instead of duplicating parser logic.
```

Suggested metadata:

```json
{
  "kind": "architecture_rule",
  "scope": "Tools/validation",
  "tags": ["generated-python-policy", "validator", "adapter-boundary"],
  "confidence": "high"
}
```

### Quarantine

Use `quarantine` when a record may contain secrets, private local data, unsafe instructions or blocked content.

Example record summary:

```text
Local command note includes an API token, private path with credentials or pasted environment values.
```

Suggested metadata:

```json
{
  "kind": "security_review",
  "scope": "local-only",
  "tags": ["secret-risk", "do-not-select"],
  "confidence": "high"
}
```

### Promote

Use `promote_candidate` when a memory is stable enough to become durable documentation.

Example record summary:

```text
A PR established an artifact path policy, report scanning rule or validated runtime decision that future agents must preserve.
```

Suggested promotion targets:

```text
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/TECH_DEBT_TRACKER.md
```

### Drop

Use `drop_candidate` for records that should not continue to influence agents after review.

Example record summary:

```text
Temporary branch name from a completed GitHub-only PR, duplicated by the merged PR body and no longer needed.
```

## GitHub-only handling

GitHub-only agents cannot inspect the local SQLite database, local `output/` reports, Blender runtime logs, GPU/NPU activity or workstation audio files.

When working from GitHub-only access:

```text
document memory policy examples
update stable docs with clearly sourced merged-PR facts
mark local validation pending unless compact evidence exists
avoid claiming runtime validation without logs or telemetry
leave SQLite DB and generated indexes untouched
```

## Validation ownership

Use the unified launcher runbook for current memory-aware commands.

Focused memory tools may be invoked directly only when debugging or validating that specific tool. Direct focused invocations must still preserve:

```text
no SQLite DB commit
no output/** commit
no provider execution unless explicit
manifest/report visibility when routed through launcher
telemetry/capability visibility when memory contributes to full-run handoff
```

Focused validation cycle selection lives in:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Blender/Audio Rule

Blender/audio runtime facts become durable memory only after a focused smoke test or manual validation has passed.

Before that, store them as task-local notes or tech debt, not stable project truth.
