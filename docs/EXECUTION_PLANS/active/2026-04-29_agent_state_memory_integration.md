# Agent State Memory Integration

## Status

active

## Goal

Integrate the generic agent state and memory policy foundation into the real AI pipeline while keeping memory records compact, reviewed and reusable across future scenarios.

The packet model should support audio files, non-audio files, multi-file tasks, software integrations and CPU/NPU/GPU lane planning.

## Scope

```text
Tools/ai/agent_state.py
Tools/ai/agent_memory_policy.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/validation/check_agent_memory_policy.py
docs/AI_MEMORY_POLICY.md
docs/PROJECT_AI_CONSCIOUSNESS.md
indexAI/agent_memory/
```

Initial work is documentation, validation and packet-shape verification only.

## Out of scope

```text
Runtime Blender behavior changes
Scripting/v61b/ rewrites
Ready To Jazz splitting
Full frame-level analysis JSON changes
New external dependencies
Automatic promotion of local memory into stable docs
Long Blender renders or GPU workloads
```

Do not wire memory selection into production-like generation until packet examples and policy checks are validated.

## Files likely touched

```text
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/TECH_DEBT_TRACKER.md
docs/AI_MEMORY_POLICY.md
docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md
Tools/validation/check_agent_memory_policy.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
```

## Validation commands

```powershell
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Validate agent state memory integration plan" --include-file .\docs\AI_MEMORY_POLICY.md
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Validate agent state memory integration plan with local SQLite" --memory-db .\indexAI\agent_memory\agent_memory.sqlite --save-inputs-to-memory-db --memory-note "Keep persistent memory generic and avoid Blender-only schema decisions."
python .\Tools\ai\review_agent_memory.py --repo-root .
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
```

## Risk level

low

The initial plan is non-runtime and documentation/validation focused. Risk becomes medium only when memory selection starts affecting real AI pipeline inputs.

## Guardrails

- Treat task-local state, durable memory and lane planning as separate concepts.
- Durable memory must remain generic and schema-light.
- Do not promote memory records automatically.
- Do not store large source dumps, raw chat noise or full frame-level JSON as durable memory.
- Any Blender/audio runtime fact must be validated by smoke/manual test before becoming stable project truth.
- Keep SQLite memory generated and untracked.

## Proposed phases

### Phase 1 — packet smoke

Status: completed locally on 2026-04-29.

- Generate one packet without SQLite.
- Generate one packet with SQLite.
- Review memory state.
- Confirm validator output.

Observed local result:

```text
packet without SQLite: PASS
  selected_memory: 1
  microtasks: 4
  selected_memory_chars: 3059
  memory_db: null
  memory_db_saved: 0

packet with SQLite: PASS
  selected_memory: 4
  microtasks: 4
  selected_memory_chars: 8535
  memory_db: indexAI/agent_memory/agent_memory.sqlite
  memory_db_saved: 1

review_agent_memory.py: PASS
  record_count: 4
  promotion_candidate_count: 0
  review_count: 0
  risk_count: 0

check_agent_memory_policy.py: PASS
  memory_db_exists: true
  actual record_count: 4
  actual action_counts: keep=4

git status: clean
```

### Phase 2 — pipeline touchpoint design

- Identify where the AI artifact pipeline can accept an optional state packet.
- Keep the entrypoint thin.
- Avoid changing schema-v6 report meanings.

### Phase 3 — controlled integration

- Add optional, disabled-by-default packet input to the pipeline.
- Validate dry-run matrix.
- Confirm no runtime Blender behavior changes.

### Phase 4 — promotion policy

- Define which results may be copied to durable docs.
- Require reviewed summaries for promotion.
- Keep project-specific facts in docs, not opaque memory.

## Progress log

- 2026-04-29: Plan created from handoff state after agent memory foundation was added and marked `TD-010` in progress.
- 2026-04-29: Phase 1 packet smoke completed locally. Packet generation worked with and without SQLite; memory review passed; memory policy validator passed; working tree remained clean.

## Result

Phase 1 completed. The packet model and local SQLite path are usable for controlled follow-up work.

The execution plan remains active because pipeline touchpoint design and controlled integration are not implemented yet.

## Follow-up

Create or update a focused implementation task for Phase 2: optional state-packet input design for the AI artifact pipeline. Do not wire it into real generation until the dry-run matrix proves that schema-v6 meanings and runtime Blender behavior remain unchanged.
