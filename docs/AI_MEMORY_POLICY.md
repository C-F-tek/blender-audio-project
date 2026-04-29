# AI Memory Policy

## Purpose

This document defines how local agent memory is kept useful without becoming noisy, stale or unsafe.

The policy applies to generic memory records produced by:

```text
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
indexAI/agent_memory/agent_memory.sqlite
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

## Commands

Review local memory:

```powershell
python .\Tools\ai\review_agent_memory.py --repo-root .
```

Validate the policy and the local DB when it exists:

```powershell
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
```

Build a task packet with SQLite memory:

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Plan Blender/audio smoke tests" --memory-db .\indexAI\agent_memory\agent_memory.sqlite --save-inputs-to-memory-db --memory-note "Keep runtime packages unchanged until smoke passes."
```

## Blender/Audio Rule

Blender/audio runtime facts become durable memory only after a focused smoke test or manual validation has passed.

Before that, store them as task-local notes or tech debt, not stable project truth.
