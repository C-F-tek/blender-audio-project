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

Status: completed and merged on 2026-04-29.

Implemented as a passive optional pipeline touchpoint:

```text
--agent-state-packet <path>
```

Implementation result:

```text
Tools/ai/pipeline/cli.py
  added optional CLI argument

Tools/ai/pipeline/preflight.py
  validates the optional packet path
  adds packet metadata to preflight

Tools/ai/pipeline/schema_report.py
  exposes agent_state_packet metadata in schema-v6 reports

Tools/ai/run_pipeline_dry_run_matrix.py
  adds with_agent_state_packet case when a local packet exists
```

Observed local validation result:

```text
git status: clean
check_ai_pipeline_modules.py: PASS
run_pipeline_dry_run_matrix.py: PASS
case_count: 6
with_agent_state_packet: PASS
agent_state_packet.enabled: true
agent_state_packet.exists: true
agent_state_packet.source: cli
step_count for with_agent_state_packet: 3
lanes unchanged: CPU review_wave_entrypoints/build_smart_ai_context, NPU npu_guardrail
```

Important: Phase 2 is still passive. The packet is not injected into prompts and does not modify scheduler, runner, Blender runtime or FFmpeg behavior.

### Phase 3 — controlled integration

- Add optional, disabled-by-default packet input to a real context-building stage only after schema validation proves the report contract.
- Validate dry-run matrix.
- Confirm no runtime Blender behavior changes.

### Phase 4 — promotion policy

- Define which results may be copied to durable docs.
- Require reviewed summaries for promotion.
- Keep project-specific facts in docs, not opaque memory.

## Progress log

- 2026-04-29: Plan created from handoff state after agent memory foundation was added and marked `TD-010` in progress.
- 2026-04-29: Phase 1 packet smoke completed locally. Packet generation worked with and without SQLite; memory review passed; memory policy validator passed; working tree remained clean.
- 2026-04-29: Phase 2 passive pipeline touchpoint merged. Local validation confirmed the optional packet appears in reports and does not change planned steps or lanes.

## Result

Phase 1 completed. The packet model and local SQLite path are usable for controlled follow-up work.

Phase 2 completed. The pipeline can now accept an optional `--agent-state-packet` argument and report its metadata without using it for generation.

The execution plan remains active because controlled integration and promotion policy are not implemented yet.

## Follow-up

Next safest task: add schema/contract validation for the new `agent_state_packet` report section under the existing formal JSON schema validation plan. Do not inject the packet into prompts until this contract is validated by the dry-run matrix.
