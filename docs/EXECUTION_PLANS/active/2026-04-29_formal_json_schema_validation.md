# Formal JSON Schema Validation

## Status

active

## Current phase

Phase: dry-run matrix report contract validation
Status: implementation started

## Goal

Introduce formal JSON schema validation gradually so generated AI artifacts remain stable, machine-checkable and reusable across future file types and software integrations.

The first objective is not to freeze every artifact. The objective is to define the contracts that are already relied on by validators, reports and downstream scripts.

## Scope

Initial schema candidates:

```text
AI pipeline report schema v6
AI pipeline dry-run matrix report
agent state packet
music summary
scene specification
```

Initial folders likely involved:

```text
Tools/ai/pipeline/
Tools/validation/
docs/
output/ai_pipeline/
indexAI/
```

## Out of scope

```text
Changing schema-v6 field meanings
Rewriting generated historical artifacts
Modifying full frame-level analysis JSON
Adding third-party schema dependencies
Changing Blender render behavior
Changing FFmpeg output behavior
```

Use standard-library validation first where practical. If a third-party JSON schema library becomes useful, document the requirement before adding it.

## Files likely touched

```text
docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md
docs/TECH_DEBT_TRACKER.md
docs/QUALITY_GATE.md
Tools/validation/check_json_artifacts.py
Tools/validation/check_ai_pipeline_modules.py
Tools/validation/check_ai_dry_run_matrix_contract.py
Tools/validation/check_agent_memory_policy.py
Tools/ai/pipeline/schema_report.py
Tools/ai/pipeline/artifact_contracts.py
```

## Validation commands

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
```

## Risk level

medium

Risk is medium because schemas can accidentally harden unstable fields or reject useful forward-compatible artifacts. Mitigate this with permissive initial checks and explicit version fields.

## Guardrails

- Add schemas incrementally.
- Start with generated reports, not runtime Blender files.
- Prefer additive required fields; avoid rejecting unknown optional fields too early.
- Do not change existing schema-v6 semantics during validation work.
- Keep validators non-destructive.
- Keep output reports readable as both JSON and Markdown when applicable.
- Validate report contracts without executing heavy runtime workloads.

## Proposed phases

### Phase 1 — inventory

Status: in progress.

Known initial contract families:

```text
AI pipeline report schema-v6
AI pipeline dry-run matrix report
agent_state_packet report metadata
agent state packet JSON
music summary
scene specification
```

### Phase 2 — contract docs

Status: in progress.

Initial `agent_state_packet` report metadata contract:

```text
agent_state_packet.enabled: bool
agent_state_packet.path: string|null
agent_state_packet.exists: bool
agent_state_packet.source: "disabled"|"cli"
agent_state_packet.repo_relative_path: string, required only when enabled=true and path is inside repo
```

This contract is additive to schema-v6 and must not change existing report field meanings.

Initial dry-run matrix report contract:

```text
schema_version: int
repo_root: string
output_dir: string
case_count: int
passed: bool
results: list
```

Each matrix result keeps a permissive contract around the current stable fields:

```text
name: non-empty string
purpose: non-empty string
command: non-empty list
returncode: int
duration_sec: int|float
stdout_tail: string, optional
stderr_tail: string, optional
report_path: string
report_exists: bool
report_passed: bool|null
step_count: int|null
lanes: object|null
summary: object|null
schedule: object|null
agent_state_packet: object|null
```

Unknown future fields must be accepted.

### Phase 3 — validators

Status: in progress.

Current validator targets:

```text
Tools/validation/check_ai_pipeline_modules.py
Tools/validation/check_ai_dry_run_matrix_contract.py
```

`check_ai_pipeline_modules.py` checks both disabled and enabled `agent_state_packet` states without running NPU, GPU, Blender, FFmpeg or long-running artifact jobs.

`check_ai_dry_run_matrix_contract.py` checks the generated dry-run matrix report without executing the matrix and without modifying generated artifacts.

### Phase 4 — dry-run proof

Status: pending local validation.

Required proof:

```text
check_python_syntax.py: pending
run_pipeline_dry_run_matrix.py: pending
check_ai_dry_run_matrix_contract.py: pending
check_ai_pipeline_modules.py: pending
check_ai_model_json.py: pending
check_generated_blender_script_policy.py: pending
check_docs_links.py: pending
check_json_artifacts.py: pending
```

## Progress log

- 2026-04-29: Plan created from handoff state for `TD-006`.
- 2026-04-29: Started first concrete schema/contract validator target for `agent_state_packet` report metadata after passive pipeline touchpoint was merged.
- 2026-04-30: Started dry-run matrix report contract validation with `Tools/validation/check_ai_dry_run_matrix_contract.py`.

## Result

not completed yet

## Follow-up

Run the dry-run matrix locally, then run the contract validator against `output/ai_pipeline/dry_run_matrix_report.json`. Mark this phase completed only after the local validation report is coherent.
