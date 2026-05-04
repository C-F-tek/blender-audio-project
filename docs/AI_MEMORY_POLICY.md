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

The unified launcher is the preferred entrypoint for full memory-aware local AI runs:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

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
```

## Storage

Default local SQLite path:

```text
indexAI/agent_memory/agent_memory.sqlite
```

This path is generated local data and must stay untracked.

JSONL memory is allowed when append-only reviewability matters more than lookup speed.

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
Blender/audio smoke outcomes
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
```

Promotion means copying a reviewed summary into a stable target such as:

```text
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/TECH_DEBT_TRACKER.md
docs/PROJECT_STATUS_POINT.md
docs/EXECUTION_PLANS/
curated JSONL memory selected by the app
```

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

Reason:

```text
The rule is durable, has a clear scope and is useful for future validators.
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

Reason:

```text
The memory selector must not place the content back into prompts or generated docs.
```

### Promote

Use `promote_candidate` when a memory is stable enough to become durable documentation.

Example record summary:

```text
PR #31, #32 and #33 established the generated artifact path policy, artifact report scanning and generic generated Python policy. Local runtime validation remains workstation-owned.
```

Suggested promotion target:

```text
docs/PROJECT_STATUS_POINT.md
docs/TECH_DEBT_TRACKER.md
```

Reason:

```text
This is project state, not temporary chat context.
```

### Drop

Use `drop_candidate` for records that should not continue to influence agents after review.

Example record summary:

```text
Temporary branch name from a completed GitHub-only PR, duplicated by the merged PR body and no longer needed.
```

Suggested metadata:

```json
{
  "kind": "temporary_workflow_note",
  "scope": "completed-branch",
  "tags": ["duplicate", "obsolete"],
  "confidence": "medium"
}
```

Reason:

```text
The durable source is the merged PR or stable documentation; retaining the duplicate note increases noise.
```

## GitHub-only handling

GitHub-only agents cannot inspect the local SQLite database, local `output/` reports, Blender runtime logs, GPU/NPU activity or workstation audio files.

When working from GitHub-only access:

```text
document memory policy examples
update stable docs with clearly sourced merged-PR facts
mark local validation pending
avoid claiming runtime validation without logs
leave SQLite DB and generated indexes untouched
```

## Commands

Review local memory:

```powershell
python .\Tools\ai\review_agent_memory.py --repo-root .
```

Build memory inventory:

```powershell
python .\Tools\ai\build_agent_memory_inventory.py --repo-root . --output .\output\validation\agent_memory_inventory.json
```

Validate the policy and the local DB when it exists:

```powershell
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
```

Build a task packet with SQLite memory:

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan Blender/audio smoke tests" --memory-db .\indexAI\agent_memory\agent_memory.sqlite --save-inputs-to-memory-db --memory-note "Keep runtime packages unchanged until smoke passes."
```

Preferred unified launcher memory-aware run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode agent_state,context_pack,contract,full_validation `
  -SaveInputsToMemoryDb
```

## Blender/Audio Rule

Blender/audio runtime facts become durable memory only after a focused smoke test or manual validation has passed.

Before that, store them as task-local notes or tech debt, not stable project truth.
